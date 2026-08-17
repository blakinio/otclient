#!/usr/bin/env python3
"""Fail-closed external-process executor for repository-native agent waves."""

from __future__ import annotations

import concurrent.futures
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading
from typing import Any

import orchestrator_core
import orchestrator_results
import resume


class ExecutorError(RuntimeError):
    pass


_WORKTREE_LOCK = threading.Lock()
_PROTECTED_BRANCHES = {"main", "master"}


def _executor_config(config: dict[str, Any]) -> dict[str, Any]:
    raw = config.get("executor")
    if not isinstance(raw, dict):
        raise ExecutorError("executor config must be an object")
    return raw


def validate_executor_enabled(config: dict[str, Any]) -> dict[str, Any]:
    cfg = _executor_config(config)
    if not cfg.get("real_model_executor_enabled", False):
        raise ExecutorError("real model executor is disabled")
    if cfg.get("mode") != "external_process":
        raise ExecutorError("executor.mode must be external_process")
    provider = cfg.get("provider")
    if not isinstance(provider, str) or not provider.strip():
        raise ExecutorError("executor.provider must identify the concrete worker runtime")
    if cfg.get("requires_owner_funded_ai", True) and not cfg.get("owner_funded_ai_allowed", False):
        raise ExecutorError("executor provider requires owner-funded AI but authorization is false")
    command = cfg.get("command")
    if not isinstance(command, list) or not command or not all(isinstance(x, str) and x for x in command):
        raise ExecutorError("executor.command must be a non-empty argv list")
    timeout_seconds = cfg.get("timeout_seconds", 1200)
    if not isinstance(timeout_seconds, int) or not 1 <= timeout_seconds <= 2700:
        raise ExecutorError("executor.timeout_seconds must be in 1..2700")
    max_workers = cfg.get("max_parallel_workers", config.get("max_parallel_workers"))
    if not isinstance(max_workers, int) or max_workers < 1:
        raise ExecutorError("executor.max_parallel_workers must be a positive integer")
    if not isinstance(cfg.get("publish_results", False), bool):
        raise ExecutorError("executor.publish_results must be boolean")
    remote = cfg.get("remote", "origin")
    if not isinstance(remote, str) or not remote.strip():
        raise ExecutorError("executor.remote must be a non-empty remote name")
    return cfg


def _safe_name(task_id: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in task_id)


def _run_git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    run = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and run.returncode:
        raise ExecutorError(f"git {' '.join(args)} failed: {(run.stderr or '').strip()[-800:]}")
    return run


def _validate_branch(repo_root: Path, branch: str) -> None:
    if branch in _PROTECTED_BRANCHES:
        raise ExecutorError(f"protected branch cannot be a worker branch: {branch}")
    check = _run_git(repo_root, "check-ref-format", "--branch", branch, check=False)
    if check.returncode:
        raise ExecutorError(f"invalid worker branch: {branch}")


def _changed_paths(worktree: Path, base_sha: str) -> list[str]:
    run = _run_git(worktree, "diff", "--name-only", f"{base_sha}...HEAD")
    return sorted(line.strip() for line in run.stdout.splitlines() if line.strip())


def _render_request(dispatch: dict[str, Any], task_path: Path, worktree: Path) -> dict[str, Any]:
    bundle = resume.build_bundle(task_path)
    return {
        "schema_version": 1,
        "task_id": dispatch["task_id"],
        "task_path": dispatch["task_path"],
        "branch": dispatch["branch"],
        "base_sha": dispatch["dispatch_head"],
        "owned_paths": dispatch["owned_paths"],
        "workspace": str(worktree),
        "prompt": resume.render_prompt(bundle),
        "result_contract": "worker-result-v1",
    }


def _sanitized_env(cfg: dict[str, Any]) -> dict[str, str]:
    allow = {"PATH", "HOME", "LANG", "LC_ALL", "TMPDIR", "TEMP", "TMP", "SYSTEMROOT", "WINDIR"}
    extra = cfg.get("pass_env", [])
    if not isinstance(extra, list) or not all(isinstance(item, str) and item for item in extra):
        raise ExecutorError("executor.pass_env must be a list of variable names")
    allow.update(extra)
    return {key: value for key, value in os.environ.items() if key in allow}


def _publish_result(worktree: Path, branch: str, base_sha: str, head_sha: str, cfg: dict[str, Any]) -> None:
    if not cfg.get("publish_results", False):
        return
    remote = str(cfg.get("remote", "origin"))
    remote_ref = f"refs/heads/{branch}"
    before = _run_git(worktree, "ls-remote", remote, remote_ref).stdout.strip()
    if before:
        remote_head = before.split()[0]
        if remote_head != base_sha:
            raise ExecutorError("remote task branch moved since dispatch")
    push = _run_git(worktree, "push", remote, f"HEAD:{remote_ref}", check=False)
    if push.returncode:
        raise ExecutorError(f"git push failed: {(push.stderr or '').strip()[-800:]}")
    after = _run_git(worktree, "ls-remote", remote, remote_ref).stdout.strip()
    if not after or after.split()[0] != head_sha:
        raise ExecutorError("published branch head does not match worker result")


def _dispatch_projection(item: dict[str, Any]) -> tuple[Any, ...]:
    return (
        item.get("task_id"),
        item.get("task_path"),
        item.get("branch"),
        item.get("dispatch_head"),
        tuple(item.get("owned_paths", [])),
        tuple(item.get("depends_on", [])),
    )


def execute_dispatch(
    repo_root: Path,
    dispatch: dict[str, Any],
    task: orchestrator_core.TaskRecord,
    config: dict[str, Any],
    workspace_root: Path,
) -> dict[str, Any]:
    cfg = validate_executor_enabled(config)
    task_id = str(dispatch["task_id"])
    base_sha = str(dispatch["dispatch_head"])
    branch = str(dispatch.get("branch", ""))
    if not orchestrator_core.SHA_RE.fullmatch(base_sha):
        raise ExecutorError("dispatch head must be a 40-hex commit id")
    _validate_branch(repo_root, branch)
    if branch != task.branch:
        raise ExecutorError("dispatch branch differs from current task branch")
    if task.head != base_sha:
        raise ExecutorError("task head moved since plan creation")

    coordinator_task_path = repo_root / dispatch["task_path"]
    if not coordinator_task_path.is_file():
        raise ExecutorError("current coordinator task checkpoint is missing")

    workspace_root.mkdir(parents=True, exist_ok=True)
    worktree = workspace_root / _safe_name(task_id)
    if worktree.exists():
        raise ExecutorError(f"workspace already exists: {worktree}")

    added = False
    try:
        with _WORKTREE_LOCK:
            add = subprocess.run(
                ["git", "-C", str(repo_root), "worktree", "add", "--detach", str(worktree), base_sha],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        if add.returncode:
            raise ExecutorError(f"git worktree add failed: {(add.stderr or '').strip()[-800:]}")
        added = True

        request = _render_request(dispatch, coordinator_task_path, worktree)
        command = list(cfg["command"])
        try:
            run = subprocess.run(
                command,
                input=json.dumps(request),
                text=True,
                cwd=worktree,
                env=_sanitized_env(cfg),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=int(cfg.get("timeout_seconds", 1200)),
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise ExecutorError(f"worker timed out after {cfg.get('timeout_seconds', 1200)}s") from exc
        except FileNotFoundError as exc:
            raise ExecutorError(f"worker executable not found: {command[0]}") from exc
        if run.returncode:
            tail = (run.stderr or "")[-1200:].strip()
            raise ExecutorError(f"worker exited {run.returncode}: {tail}")
        try:
            result = json.loads(run.stdout)
        except json.JSONDecodeError as exc:
            raise ExecutorError(f"worker returned invalid JSON: {exc}") from exc
        if not isinstance(result, dict):
            raise ExecutorError("worker result must be a JSON object")

        status = _run_git(worktree, "status", "--porcelain").stdout.strip()
        if status:
            raise ExecutorError("worker left an uncommitted/dirty worktree")
        actual_head = _run_git(worktree, "rev-parse", "HEAD").stdout.strip()
        ancestry = _run_git(worktree, "merge-base", "--is-ancestor", base_sha, actual_head, check=False)
        if ancestry.returncode:
            raise ExecutorError("worker HEAD is not a descendant of the dispatch base")
        if result.get("head_sha") != actual_head:
            raise ExecutorError("worker result head_sha does not match actual worktree HEAD")
        actual_changed = _changed_paths(worktree, base_sha)
        result_changed = sorted(result.get("changed_paths", [])) if isinstance(result.get("changed_paths"), list) else []
        if actual_changed != result_changed:
            raise ExecutorError("worker changed_paths do not match actual Git diff")
        errors = orchestrator_results.validate_worker_result(result, dispatch, task, config)
        if errors:
            raise ExecutorError("invalid worker-result-v1: " + "; ".join(errors))
        _publish_result(worktree, task.branch, base_sha, actual_head, cfg)
        return result
    finally:
        if added:
            with _WORKTREE_LOCK:
                subprocess.run(
                    ["git", "-C", str(repo_root), "worktree", "remove", "--force", str(worktree)],
                    text=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
        if worktree.exists():
            shutil.rmtree(worktree, ignore_errors=True)


def execute_plan(
    repo_root: Path,
    tasks_root: Path,
    plan: dict[str, Any],
    config: dict[str, Any],
    results_dir: Path,
    workspace_root: Path | None = None,
) -> dict[str, Any]:
    cfg = validate_executor_enabled(config)
    tasks = orchestrator_core.discover_tasks(tasks_root, config)
    task_map = {task.task_id: task for task in tasks}
    selected = plan.get("selected", [])
    if not isinstance(selected, list) or not all(isinstance(item, dict) for item in selected):
        raise ExecutorError("plan.selected must be a list of objects")
    if plan.get("executor") != config.get("executor"):
        raise ExecutorError("plan executor policy differs from current executor config")
    if len({item.get("task_id") for item in selected}) != len(selected):
        raise ExecutorError("plan contains duplicate selected task ids")
    branches = [item.get("branch") for item in selected]
    if any(not isinstance(branch, str) or not branch for branch in branches):
        raise ExecutorError("selected workers require concrete branches")
    if len(set(branches)) != len(branches):
        raise ExecutorError("selected workers must use distinct branches")

    fresh_plan = orchestrator_core.build_plan(
        tasks,
        config,
        lane=plan.get("lane"),
        max_parallel=plan.get("max_parallel_workers"),
    )
    if [_dispatch_projection(item) for item in fresh_plan["selected"]] != [
        _dispatch_projection(item) for item in selected
    ]:
        raise ExecutorError("plan is stale; live task/dependency/ownership state changed, rerun plan")

    results_dir.mkdir(parents=True, exist_ok=True)
    root_ctx = tempfile.TemporaryDirectory(prefix="orchestrator-workers-") if workspace_root is None else None
    root = Path(root_ctx.name) if root_ctx else workspace_root
    assert root is not None
    failures: list[dict[str, str]] = []
    accepted: list[str] = []

    def one(dispatch: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        task_id = str(dispatch.get("task_id", ""))
        task = task_map.get(task_id)
        if task is None:
            raise ExecutorError(f"selected task not found: {task_id}")
        return task_id, execute_dispatch(repo_root, dispatch, task, config, root)

    try:
        max_workers = min(int(cfg.get("max_parallel_workers", config["max_parallel_workers"])), len(selected) or 1)
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
            future_map = {pool.submit(one, dispatch): dispatch for dispatch in selected}
            for future in concurrent.futures.as_completed(future_map):
                dispatch = future_map[future]
                task_id = str(dispatch.get("task_id", ""))
                try:
                    result_task_id, result = future.result()
                except Exception as exc:
                    failures.append({"task_id": task_id, "error": str(exc)})
                    continue
                orchestrator_results.write_json(result, results_dir / f"{_safe_name(result_task_id)}.json")
                accepted.append(result_task_id)
    finally:
        if root_ctx is not None:
            root_ctx.cleanup()

    return {
        "schema_version": 1,
        "wave_id": plan.get("wave_id"),
        "provider": cfg.get("provider"),
        "accepted": sorted(accepted),
        "failures": sorted(failures, key=lambda item: item["task_id"]),
        "results_dir": str(results_dir),
    }
