#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import orchestrator_core
import orchestrator_executor

HERE = Path(__file__).resolve().parent
FAKE_WORKER = HERE / "testdata" / "orchestrator" / "fake_real_worker.py"


def run(*args: str, cwd: Path) -> str:
    proc = subprocess.run(list(args), cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode:
        raise AssertionError(f"command failed: {args}: {proc.stderr}")
    return proc.stdout.strip()


class RealExecutorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        run("git", "init", "-q", cwd=self.repo)
        run("git", "config", "user.name", "executor-test", cwd=self.repo)
        run("git", "config", "user.email", "executor-test@example.invalid", cwd=self.repo)
        (self.repo / "README.md").write_text("fixture\n", encoding="utf-8")
        run("git", "add", "README.md", cwd=self.repo)
        run("git", "commit", "-q", "-m", "test: base", cwd=self.repo)
        self.base = run("git", "rev-parse", "HEAD", cwd=self.repo)

        self.tasks = self.root / "tasks"
        self.tasks.mkdir()
        self.task_path = self.tasks / "OTC-EXECUTOR-TEST.md"
        self.task_path.write_text(self._task_text(), encoding="utf-8")
        self.workspace_root = self.root / "workspaces"
        self.results = self.root / "results"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _task_text(self) -> str:
        return f"""---
task_id: OTC-EXECUTOR-TEST
project_lane: otclient
status: ready
branch: feat/executor-test
context_pressure: low
context_growth: stable
context_score: 1
owned_paths:
  - src/a/**
depends_on: []
---
# Executor fixture
## Context checkpoint
```yaml
checkpoint_version: 1
updated_at: 2026-08-17T12:40:00Z
head: {self.base}
branch: feat/executor-test
pr: none
status: ready
context_routes:
  - testing
owned_paths:
  - src/a/**
proven:
  - deterministic fixture
derived: []
unknown: []
conflicts: []
first_failure:
  marker: none
  evidence: none
rejected_hypotheses: []
changed_paths: []
validation:
  - command: fixture preflight
    result: PASS
    evidence: deterministic fixture
blockers: []
next_action: implement worker fixture
```
"""

    def _config(self, **executor_overrides: object) -> dict[str, object]:
        executor: dict[str, object] = {
            "mode": "external_process",
            "provider": "deterministic-fixture",
            "command": [sys.executable, str(FAKE_WORKER)],
            "real_model_executor_enabled": True,
            "requires_owner_funded_ai": False,
            "owner_funded_ai_allowed": False,
            "timeout_seconds": 2,
            "max_parallel_workers": 2,
            "pass_env": ["FAKE_WORKER_MODE"],
            "publish_results": False,
            "remote": "origin",
        }
        executor.update(executor_overrides)
        return {
            "schema_version": 1,
            "max_parallel_workers": 2,
            "selection": {
                "require_owned_paths": True,
                "hold_unresolved_external_dependencies": True,
            },
            "context": {
                "require_pressure": True,
                "pressure_bands": {
                    "low": [0, 5],
                    "medium": [6, 9],
                    "high": [10, 12],
                    "unbounded": [13, 15],
                },
                "rotate_at_pressure": ["high", "unbounded"],
                "rotate_medium_when_growth": ["rising", "rapid"],
                "provider_remaining_ratio_rotate_below": 0.2,
            },
            "executor": executor,
        }

    def _plan(self, config: dict[str, object]) -> dict[str, object]:
        task = orchestrator_core.task_from_path(self.task_path, config)
        plan = orchestrator_core.build_plan([task], config, lane="otclient")
        self.assertEqual([item["task_id"] for item in plan["selected"]], ["OTC-EXECUTOR-TEST"])
        return plan

    def _execute(self, mode: str, config: dict[str, object] | None = None) -> dict[str, object]:
        cfg = config or self._config()
        plan = self._plan(cfg)
        with patch.dict(os.environ, {"FAKE_WORKER_MODE": mode}, clear=False):
            return orchestrator_executor.execute_plan(
                self.repo,
                self.tasks,
                plan,
                cfg,
                self.results,
                workspace_root=self.workspace_root,
            )

    def test_real_executor_is_disabled_by_default_policy(self) -> None:
        config = self._config(real_model_executor_enabled=False)
        with self.assertRaisesRegex(orchestrator_executor.ExecutorError, "disabled"):
            orchestrator_executor.validate_executor_enabled(config)

    def test_owner_funded_provider_requires_explicit_authorization(self) -> None:
        config = self._config(requires_owner_funded_ai=True, owner_funded_ai_allowed=False)
        with self.assertRaisesRegex(orchestrator_executor.ExecutorError, "owner-funded"):
            orchestrator_executor.validate_executor_enabled(config)

    def test_worker_environment_does_not_inherit_unlisted_secret(self) -> None:
        config = self._config()
        executor = config["executor"]
        assert isinstance(executor, dict)
        with patch.dict(os.environ, {"UNLISTED_SECRET": "do-not-pass", "FAKE_WORKER_MODE": "success"}, clear=False):
            env = orchestrator_executor._sanitized_env(executor)
        self.assertNotIn("UNLISTED_SECRET", env)
        self.assertEqual(env["FAKE_WORKER_MODE"], "success")

    def test_protected_branch_is_rejected(self) -> None:
        with self.assertRaisesRegex(orchestrator_executor.ExecutorError, "protected branch"):
            orchestrator_executor._validate_branch(self.repo, "main")

    def test_stale_plan_is_rejected_before_worker_launch(self) -> None:
        config = self._config()
        plan = self._plan(config)
        self.task_path.write_text(self._task_text().replace("status: ready", "status: waiting"), encoding="utf-8")
        with self.assertRaisesRegex(orchestrator_executor.ExecutorError, "plan is stale"):
            orchestrator_executor.execute_plan(
                self.repo,
                self.tasks,
                plan,
                config,
                self.results,
                workspace_root=self.workspace_root,
            )

    def test_successful_external_worker_is_accepted_from_isolated_worktree(self) -> None:
        summary = self._execute("success")
        self.assertEqual(summary["accepted"], ["OTC-EXECUTOR-TEST"])
        self.assertEqual(summary["failures"], [])
        result_path = self.results / "OTC-EXECUTOR-TEST.json"
        result = json.loads(result_path.read_text(encoding="utf-8"))
        self.assertEqual(result["changed_paths"], ["src/a/worker.txt"])
        self.assertEqual(run("git", "cat-file", "-t", result["head_sha"], cwd=self.repo), "commit")
        self.assertFalse((self.workspace_root / "OTC-EXECUTOR-TEST").exists())

    def test_resume_request_is_built_from_current_checkpoint(self) -> None:
        config = self._config()
        task = orchestrator_core.task_from_path(self.task_path, config)
        dispatch = orchestrator_core.build_plan([task], config)["selected"][0]
        request = orchestrator_executor._render_request(dispatch, self.task_path, Path("/tmp/worktree"))
        self.assertEqual(request["result_contract"], "worker-result-v1")
        self.assertIn("Continue task OTC-EXECUTOR-TEST", request["prompt"])
        self.assertIn("NEXT_ACTION: implement worker fixture", request["prompt"])

    def test_malformed_json_fails_closed(self) -> None:
        summary = self._execute("malformed")
        self.assertEqual(summary["accepted"], [])
        self.assertIn("invalid JSON", summary["failures"][0]["error"])
        self.assertEqual(list(self.results.glob("*.json")), [])

    def test_nonzero_exit_fails_closed(self) -> None:
        summary = self._execute("nonzero")
        self.assertEqual(summary["accepted"], [])
        self.assertIn("worker exited 3", summary["failures"][0]["error"])

    def test_timeout_fails_closed(self) -> None:
        summary = self._execute("timeout", self._config(timeout_seconds=1))
        self.assertEqual(summary["accepted"], [])
        self.assertIn("timed out", summary["failures"][0]["error"])

    def test_dirty_worktree_fails_closed(self) -> None:
        summary = self._execute("dirty")
        self.assertEqual(summary["accepted"], [])
        self.assertIn("dirty worktree", summary["failures"][0]["error"])

    def test_head_mismatch_fails_closed(self) -> None:
        summary = self._execute("head_mismatch")
        self.assertEqual(summary["accepted"], [])
        self.assertIn("head_sha does not match", summary["failures"][0]["error"])

    def test_changed_path_escape_fails_closed(self) -> None:
        summary = self._execute("escape")
        self.assertEqual(summary["accepted"], [])
        self.assertIn("outside declared ownership", summary["failures"][0]["error"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
