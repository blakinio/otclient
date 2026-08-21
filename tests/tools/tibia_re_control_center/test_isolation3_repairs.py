from __future__ import annotations

import unittest

from test_codex_review_repairs import abort_scenario_json, make_request, make_stack

from tools.tibia_re_control_center.artifact import ArtifactStore
from tools.tibia_re_control_center.model import ActionStatus, PrivacyError
from tools.tibia_re_control_center.scenario import parse_and_validate


class IsolationThreeRegressionTests(unittest.TestCase):
    def test_action_local_timeout_refuses_before_dispatch(self) -> None:
        clock, adapter, _, coordinator = make_stack(epoch="action-timeout")
        request = make_request(coordinator, adapter, "timeout-action")
        adapter.authority_wait_hook = lambda: clock.advance_ms(request.timeout_ms + 1)
        result = coordinator.execute_action(request)
        self.assertEqual(ActionStatus.TIMEOUT, result.status)
        self.assertEqual("ACTION_TIMEOUT_EXPIRED", result.reason_code)
        self.assertEqual([], adapter.physical_effects)

    def test_preflight_cannot_mutate_frozen_action_parameters(self) -> None:
        _, adapter, _, coordinator = make_stack(epoch="deep-freeze")
        request = make_request(coordinator, adapter, "frozen-action")
        original_preflight = adapter.preflight
        mutation_blocked: list[bool] = []

        def mutating_preflight(candidate):
            try:
                candidate.parameters["direction"] = "SOUTH"
            except TypeError:
                mutation_blocked.append(True)
            return original_preflight(candidate)

        adapter.preflight = mutating_preflight
        result = coordinator.execute_action(request)
        self.assertEqual(ActionStatus.PASS, result.status)
        self.assertEqual([True], mutation_blocked)
        self.assertEqual("NORTH", adapter.physical_effects[0]["parameters"]["direction"])

    def test_stop_after_dispatch_commit_is_cancelled_after_dispatch(self) -> None:
        _, adapter, _, coordinator = make_stack(epoch="post-commit-stop")
        request = make_request(coordinator, adapter, "stop-after-commit")
        adapter.after_commit_hook = lambda: coordinator.stop_all()
        result = coordinator.execute_action(request)
        self.assertEqual(ActionStatus.CANCELLED, result.status)
        self.assertEqual("CANCELLED_AFTER_DISPATCH", result.reason_code)
        self.assertEqual(1, len(adapter.physical_effects))

    def test_structured_stage_json_secret_key_is_rejected(self) -> None:
        scenario = parse_and_validate(abort_scenario_json())
        artifacts = ArtifactStore()
        artifacts.create_run(
            run_id="structured-stage",
            scenario_id=scenario.scenario_id,
            scenario_hash=scenario.scenario_hash,
            scenario_ast=scenario.ast,
            adapter_identity={"adapter_id": "fake"},
            backend_epoch="b",
            initial_control_generation=0,
            started_monotonic_ns=0,
            privacy_policy=scenario.ast["privacy_policy"],
        )
        with self.assertRaises(PrivacyError):
            artifacts.write_stage(
                "structured-stage", "metadata.json", b'{"password":"hunter2"}'
            )

    def test_supplement_secret_is_rejected_by_privacy_admission(self) -> None:
        scenario = parse_and_validate(abort_scenario_json())
        artifacts = ArtifactStore()
        run = artifacts.create_run(
            run_id="supplement-privacy",
            scenario_id=scenario.scenario_id,
            scenario_hash=scenario.scenario_hash,
            scenario_ast=scenario.ast,
            adapter_identity={"adapter_id": "fake"},
            backend_epoch="b",
            initial_control_generation=0,
            started_monotonic_ns=0,
            privacy_policy=scenario.ast["privacy_policy"],
        )
        run.final_result = {"status": "PASS"}
        with self.assertRaises(PrivacyError):
            artifacts.add_supplement(
                "supplement-privacy",
                "late-secret",
                {"trace.txt": b"PASSWORD=hunter2"},
            )


if __name__ == "__main__":
    unittest.main()
