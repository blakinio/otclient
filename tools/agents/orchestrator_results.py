#!/usr/bin/env python3
"""Worker-result validation and barrier fan-in for the agent orchestrator."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
from pathlib import Path
from typing import Any

from orchestrator_core import (
    ContextState,
    GLOB_CHARS,
    OrchestratorError,
    Overlay,
    SHA_RE,
    TaskRecord,
    VALID_GROWTH,
    VALID_PRESSURES,
    VALID_RESULT_STATUS,
    VALID_VALIDATION_RESULT,
    build_plan,
    pressure_from_score,
)

def _owned_path_matches(path: str, pattern: str) -> bool:
    normalized = path.replace("\\", "/").lstrip("./")
    patt = pattern.replace("\\", "/").lstrip("./")
    if patt.endswith("/**"):
        prefix = patt[:-3].rstrip("/")
        return normalized == prefix or normalized.startswith(prefix + "/")
    if any(ch in patt for ch in GLOB_CHARS):
        return fnmatch.fnmatchcase(normalized, patt)
    return normalized == patt


def validate_worker_result(
    raw: dict[str, Any], dispatch: dict[str, Any], task: TaskRecord, config: dict[str, Any]
) -> list[str]:
    errors: list[str] = []
    if raw.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if raw.get("task_id") != dispatch["task_id"]:
        errors.append("task_id does not match dispatch")
    if raw.get("branch") != dispatch["branch"]:
        errors.append("branch does not match dispatch")
    if raw.get("base_sha") != dispatch["dispatch_head"]:
        errors.append("base_sha does not match dispatch_head")
    head_sha = raw.get("head_sha")
    if not isinstance(head_sha, str) or not SHA_RE.fullmatch(head_sha):
        errors.append("head_sha must be a 40-hex commit id")
    status = raw.get("status")
    if status not in VALID_RESULT_STATUS:
        errors.append(f"status must be one of {sorted(VALID_RESULT_STATUS)}")
    next_action = raw.get("next_action")
    if not isinstance(next_action, str):
        errors.append("next_action must be a string")
    elif status != "completed" and not next_action.strip():
        errors.append("incomplete result requires one concrete next_action")

    changed_paths = raw.get("changed_paths")
    if not isinstance(changed_paths, list) or not all(isinstance(item, str) for item in changed_paths):
        errors.append("changed_paths must be a list of strings")
    else:
        for path in changed_paths:
            if not any(_owned_path_matches(path, pattern) for pattern in task.owned_paths):
                errors.append(f"changed path outside declared ownership: {path}")

    evidence = raw.get("evidence")
    if (
        not isinstance(evidence, list)
        or not evidence
        or not all(isinstance(item, str) and item.strip() for item in evidence)
    ):
        errors.append("evidence must be a non-empty list of strings")

    validation = raw.get("validation")
    if not isinstance(validation, list) or not validation:
        errors.append("validation must be a non-empty list")
    else:
        for index, item in enumerate(validation):
            if not isinstance(item, dict):
                errors.append(f"validation[{index}] must be an object")
                continue
            if not isinstance(item.get("command"), str) or not item.get("command", "").strip():
                errors.append(f"validation[{index}].command is required")
            if item.get("result") not in VALID_VALIDATION_RESULT:
                errors.append(f"validation[{index}].result is invalid")
            if not isinstance(item.get("evidence"), str) or not item.get("evidence", "").strip():
                errors.append(f"validation[{index}].evidence is required")
        if status == "completed":
            blocking = [
                item.get("result")
                for item in validation
                if isinstance(item, dict)
                and item.get("result") in {"FAIL", "BLOCKED", "NOT_RUN"}
            ]
            if blocking:
                errors.append("completed result contains non-terminal validation outcome")

    context_raw = raw.get("context")
    if not isinstance(context_raw, dict):
        errors.append("context must be an object")
    else:
        pressure = str(context_raw.get("pressure", "")).casefold()
        growth = str(context_raw.get("growth", "unknown")).casefold()
        score = context_raw.get("score")
        if pressure not in VALID_PRESSURES:
            errors.append("context.pressure is invalid")
        if growth not in VALID_GROWTH:
            errors.append("context.growth is invalid")
        if score is not None and (not isinstance(score, int) or not 0 <= score <= 15):
            errors.append("context.score must be null or integer 0..15")
        ratio = context_raw.get("provider_remaining_ratio")
        if ratio is not None and (not isinstance(ratio, (int, float)) or not 0.0 <= float(ratio) <= 1.0):
            errors.append("context.provider_remaining_ratio must be null or 0..1")
        if pressure in VALID_PRESSURES and isinstance(score, int) and 0 <= score <= 15:
            try:
                computed = pressure_from_score(score, config)
            except OrchestratorError as exc:
                errors.append(str(exc))
            else:
                if computed != pressure:
                    errors.append("context pressure/score mismatch")
    return errors


def _result_context(raw: dict[str, Any]) -> ContextState:
    context = raw["context"]
    ratio = context.get("provider_remaining_ratio")
    return ContextState(
        pressure=str(context["pressure"]).casefold(),
        growth=str(context.get("growth", "unknown")).casefold(),
        score=context.get("score"),
        provider_remaining_ratio=float(ratio) if ratio is not None else None,
    )


def run_barrier(
    tasks: list[TaskRecord], config: dict[str, Any], plan: dict[str, Any], results: list[dict[str, Any]]
) -> dict[str, Any]:
    selected = {item["task_id"]: item for item in plan.get("selected", [])}
    task_map = {task.task_id: task for task in tasks}
    overlays: dict[str, Overlay] = {}
    accepted: list[dict[str, Any]] = []
    invalid: list[dict[str, Any]] = []
    seen: set[str] = set()

    for raw in results:
        task_id = raw.get("task_id")
        if not isinstance(task_id, str) or task_id not in selected or task_id not in task_map:
            invalid.append({"task_id": task_id, "errors": ["result is not for a selected task"]})
            continue
        if task_id in seen:
            invalid.append({"task_id": task_id, "errors": ["duplicate worker result"]})
            continue
        seen.add(task_id)
        errors = validate_worker_result(raw, selected[task_id], task_map[task_id], config)
        if errors:
            invalid.append({"task_id": task_id, "errors": errors})
            continue
        status = str(raw["status"])
        state = {
            "completed": "DONE",
            "ready": "READY",
            "waiting": "WAITING",
            "blocked": "BLOCKED",
        }[status]
        overlays[task_id] = Overlay(
            state=state,
            head=str(raw["head_sha"]),
            context=_result_context(raw),
            reason="WORKER_RESULT",
        )
        accepted.append({"task_id": task_id, "status": status, "head_sha": raw["head_sha"]})

    missing = sorted(set(selected) - seen)
    for task_id in missing:
        overlays[task_id] = Overlay(state="WAITING", reason="RESULT_MISSING")

    next_wave: dict[str, Any] | None = None
    if not invalid:
        next_wave = build_plan(
            tasks,
            config,
            overlays=overlays,
            lane=plan.get("lane"),
            max_parallel=int(plan.get("max_parallel_workers") or config["max_parallel_workers"]),
            parent_wave_id=str(plan.get("wave_id")),
            generation=int(plan.get("generation", 1)) + 1,
        )
    return {
        "schema_version": 1,
        "parent_wave_id": plan.get("wave_id"),
        "accepted_results": accepted,
        "invalid_results": invalid,
        "missing_results": missing,
        "next_wave": next_wave,
    }


def load_result_files(results_dir: Path) -> list[dict[str, Any]]:
    if not results_dir.exists():
        raise OrchestratorError(f"results directory does not exist: {results_dir}")
    results: list[dict[str, Any]] = []
    for path in sorted(results_dir.glob("*.json")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise OrchestratorError(f"worker result must be an object: {path}")
        results.append(raw)
    return results


def write_json(payload: dict[str, Any], output: Path | None) -> None:
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


def simulate_worker(args: argparse.Namespace) -> dict[str, Any]:
    result_head = hashlib.sha1(
        f"{args.task_id}\0{args.branch}\0{args.dispatch_head}\0simulated".encode("utf-8")
    ).hexdigest()
    return {
        "schema_version": 1,
        "task_id": args.task_id,
        "branch": args.branch,
        "base_sha": args.dispatch_head,
        "head_sha": result_head,
        "status": "completed",
        "changed_paths": [],
        "validation": [
            {
                "command": "orchestrator simulated worker",
                "result": "PASS",
                "evidence": "deterministic GitHub-hosted smoke; no AI/model invocation",
            }
        ],
        "evidence": ["simulated-worker:no-ai"],
        "context": {
            "pressure": "low",
            "growth": "stable",
            "score": 1,
            "provider_remaining_ratio": None,
        },
        "next_action": "none",
    }
