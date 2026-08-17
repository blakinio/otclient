#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

import orchestrator

HERE = Path(__file__).resolve().parent
FIXTURE_ROOT = HERE / "testdata" / "orchestrator"
CONFIG_PATH = FIXTURE_ROOT / "config.json"
TASKS_ROOT = FIXTURE_ROOT / "active"


class OrchestratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = orchestrator.load_config(CONFIG_PATH)
        self.tasks = orchestrator.discover_tasks(TASKS_ROOT, self.config)

    def test_first_wave_parallel_selection_and_holds(self) -> None:
        plan = orchestrator.build_plan(self.tasks, self.config)
        self.assertEqual([item["task_id"] for item in plan["selected"]], ["OTC-TEST-A", "OTC-TEST-B"])
        held = {item["task_id"]: item for item in plan["held"]}
        self.assertEqual(held["OTC-TEST-C"]["reasons"], ["DEPENDENCY_NOT_DONE"])
        self.assertEqual(held["OTC-TEST-D"]["reasons"], ["CONTEXT_ROTATE_REQUIRED"])
        self.assertEqual(held["OTC-TEST-E"]["reasons"], ["OWNERSHIP_OVERLAP"])
        self.assertEqual(held["OTC-TEST-F"]["reasons"], ["CAPACITY"])
        self.assertFalse(plan["executor"]["real_model_executor_enabled"])

    def test_wave_id_is_deterministic(self) -> None:
        first = orchestrator.build_plan(self.tasks, self.config)
        second = orchestrator.build_plan(self.tasks, self.config)
        self.assertEqual(first["wave_id"], second["wave_id"])
        self.assertEqual(first, second)

    def test_barrier_unlocks_dependent_next_wave(self) -> None:
        plan = orchestrator.build_plan(self.tasks, self.config)
        selected = {item["task_id"]: item for item in plan["selected"]}
        results = []
        for task_id in ("OTC-TEST-A", "OTC-TEST-B"):
            dispatch = selected[task_id]
            args = type(
                "Args",
                (),
                {
                    "task_id": task_id,
                    "branch": dispatch["branch"],
                    "dispatch_head": dispatch["dispatch_head"],
                },
            )()
            results.append(orchestrator.simulate_worker(args))
        barrier = orchestrator.run_barrier(self.tasks, self.config, plan, results)
        self.assertEqual(barrier["invalid_results"], [])
        self.assertEqual(barrier["missing_results"], [])
        next_wave = barrier["next_wave"]
        self.assertIsNotNone(next_wave)
        assert next_wave is not None
        self.assertEqual(next_wave["parent_wave_id"], plan["wave_id"])
        self.assertIn("OTC-TEST-C", [item["task_id"] for item in next_wave["selected"]])
        self.assertNotIn("OTC-TEST-A", [item["task_id"] for item in next_wave["selected"]])
        self.assertNotIn("OTC-TEST-B", [item["task_id"] for item in next_wave["selected"]])

    def test_result_branch_mismatch_is_rejected(self) -> None:
        plan = orchestrator.build_plan(self.tasks, self.config)
        dispatch = plan["selected"][0]
        task = next(item for item in self.tasks if item.task_id == dispatch["task_id"])
        args = type(
            "Args",
            (),
            {
                "task_id": dispatch["task_id"],
                "branch": dispatch["branch"],
                "dispatch_head": dispatch["dispatch_head"],
            },
        )()
        result = orchestrator.simulate_worker(args)
        result["branch"] = "feat/wrong"
        errors = orchestrator.validate_worker_result(result, dispatch, task, self.config)
        self.assertIn("branch does not match dispatch", errors)


    def test_empty_evidence_is_rejected(self) -> None:
        plan = orchestrator.build_plan(self.tasks, self.config)
        dispatch = plan["selected"][0]
        task = next(item for item in self.tasks if item.task_id == dispatch["task_id"])
        args = type(
            "Args",
            (),
            {
                "task_id": dispatch["task_id"],
                "branch": dispatch["branch"],
                "dispatch_head": dispatch["dispatch_head"],
            },
        )()
        result = orchestrator.simulate_worker(args)
        result["evidence"] = []
        errors = orchestrator.validate_worker_result(result, dispatch, task, self.config)
        self.assertIn("evidence must be a non-empty list of strings", errors)

    def test_completed_result_with_failed_validation_is_rejected(self) -> None:
        plan = orchestrator.build_plan(self.tasks, self.config)
        dispatch = plan["selected"][0]
        task = next(item for item in self.tasks if item.task_id == dispatch["task_id"])
        args = type(
            "Args",
            (),
            {
                "task_id": dispatch["task_id"],
                "branch": dispatch["branch"],
                "dispatch_head": dispatch["dispatch_head"],
            },
        )()
        result = orchestrator.simulate_worker(args)
        result["validation"][0]["result"] = "FAIL"
        errors = orchestrator.validate_worker_result(result, dispatch, task, self.config)
        self.assertIn("completed result contains non-terminal validation outcome", errors)

    def test_result_path_outside_ownership_is_rejected(self) -> None:
        plan = orchestrator.build_plan(self.tasks, self.config)
        dispatch = plan["selected"][0]
        task = next(item for item in self.tasks if item.task_id == dispatch["task_id"])
        args = type(
            "Args",
            (),
            {
                "task_id": dispatch["task_id"],
                "branch": dispatch["branch"],
                "dispatch_head": dispatch["dispatch_head"],
            },
        )()
        result = orchestrator.simulate_worker(args)
        result["changed_paths"] = ["src/not-owned/file.cpp"]
        errors = orchestrator.validate_worker_result(result, dispatch, task, self.config)
        self.assertTrue(any("outside declared ownership" in error for error in errors))

    def test_missing_worker_result_is_not_redispatched(self) -> None:
        plan = orchestrator.build_plan(self.tasks, self.config)
        dispatch = plan["selected"][0]
        args = type(
            "Args",
            (),
            {
                "task_id": dispatch["task_id"],
                "branch": dispatch["branch"],
                "dispatch_head": dispatch["dispatch_head"],
            },
        )()
        barrier = orchestrator.run_barrier(
            self.tasks, self.config, plan, [orchestrator.simulate_worker(args)]
        )
        self.assertEqual(barrier["missing_results"], ["OTC-TEST-B"])
        next_wave = barrier["next_wave"]
        assert next_wave is not None
        selected_ids = [item["task_id"] for item in next_wave["selected"]]
        self.assertNotIn("OTC-TEST-B", selected_ids)
        self.assertNotIn("OTC-TEST-C", selected_ids)

    def test_medium_rising_context_rotates(self) -> None:
        context = orchestrator.ContextState("medium", "rising", 8, None)
        action, reasons = orchestrator.context_decision(context, self.config)
        self.assertEqual(action, "rotate")
        self.assertEqual(reasons, ["CONTEXT_MEDIUM_RISING"])

    def test_provider_context_signal_can_rotate_early(self) -> None:
        context = orchestrator.ContextState("low", "stable", 2, 0.15)
        action, reasons = orchestrator.context_decision(context, self.config)
        self.assertEqual(action, "rotate")
        self.assertEqual(reasons, ["PROVIDER_CONTEXT_LOW"])

    def test_context_assessment_never_claims_exact_tokens(self) -> None:
        args = type(
            "Args",
            (),
            {
                "scope_breadth": 1,
                "evidence_volume": 2,
                "history_dependency": 1,
                "iteration_uncertainty": 2,
                "parallel_hypotheses": 1,
                "growth": "stable",
                "provider_remaining_ratio": None,
            },
        )()
        payload = orchestrator.assess_context(args, self.config)
        self.assertEqual(payload["context"]["score"], 7)
        self.assertEqual(payload["context"]["pressure"], "medium")
        self.assertFalse(payload["exact_remaining_tokens_known"])


    def test_invalid_provider_context_ratio_is_rejected(self) -> None:
        args = type(
            "Args",
            (),
            {
                "scope_breadth": 1,
                "evidence_volume": 1,
                "history_dependency": 1,
                "iteration_uncertainty": 1,
                "parallel_hypotheses": 1,
                "growth": "stable",
                "provider_remaining_ratio": 1.1,
            },
        )()
        with self.assertRaises(orchestrator.OrchestratorError):
            orchestrator.assess_context(args, self.config)

    def test_malformed_context_score_pressure_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "OTC-BAD.md"
            path.write_text(
                "---\n"
                "task_id: OTC-BAD\n"
                "status: ready\n"
                "branch: feat/bad\n"
                "context_pressure: low\n"
                "context_score: 11\n"
                "owned_paths:\n"
                "  - src/bad/**\n"
                "---\n"
                "## Context checkpoint\n"
                "```yaml\n"
                "head: 1111111111111111111111111111111111111111\n"
                "status: ready\n"
                "context_pressure: low\n"
                "context_score: 11\n"
                "owned_paths:\n"
                "  - src/bad/**\n"
                "```\n",
                encoding="utf-8",
            )
            with self.assertRaises(orchestrator.OrchestratorError):
                orchestrator.task_from_path(path, self.config)

    def test_external_dependency_is_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "OTC-EXT.md"
            path.write_text(
                "---\n"
                "task_id: OTC-EXT\n"
                "project_lane: otclient\n"
                "status: ready\n"
                "branch: feat/ext\n"
                "context_pressure: low\n"
                "context_score: 1\n"
                "owned_paths:\n"
                "  - src/ext/**\n"
                "depends_on:\n"
                "  - external deployment approval\n"
                "---\n"
                "## Context checkpoint\n"
                "```yaml\n"
                "head: 2222222222222222222222222222222222222222\n"
                "status: ready\n"
                "context_pressure: low\n"
                "context_score: 1\n"
                "owned_paths:\n"
                "  - src/ext/**\n"
                "```\n",
                encoding="utf-8",
            )
            task = orchestrator.task_from_path(path, self.config)
            plan = orchestrator.build_plan([task], self.config)
            self.assertEqual(plan["selected"], [])
            self.assertEqual(plan["held"][0]["reasons"], ["EXTERNAL_DEPENDENCY_UNRESOLVED"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
