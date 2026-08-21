from __future__ import annotations

import json
import unittest
from collections import UserList

from test_codex_review_repairs import abort_scenario_json, make_request, make_stack

from tools.tibia_re_control_center.artifact import ArtifactStore
from tools.tibia_re_control_center.comparison import (
    ComparisonClass,
    ComparisonProfile,
    ComparisonStatus,
    ProfileField,
    compare_runs,
)
from tools.tibia_re_control_center.engine import ScenarioEngine
from tools.tibia_re_control_center.execution import MutationCoordinator
from tools.tibia_re_control_center.fake import FakeAdapter, ManualClock
from tools.tibia_re_control_center.model import (
    ActionStatus,
    PrivacyError,
    ValidationError,
)
from tools.tibia_re_control_center.recorder import Recorder
from tools.tibia_re_control_center.scenario import parse_and_validate
from tools.tibia_re_control_center.store import DeterministicDurableStore


class IsolationSevenRegressionTests(unittest.TestCase):
    def test_atomic_final_dispatch_guard_observes_authority_revocation(self) -> None:
        _, adapter, _, coordinator = make_stack(epoch="atomic-guard-p1")
        request = make_request(coordinator, adapter, "atomic-guard")

        def revoke_inside_guard() -> None:
            adapter.authority_available = False

        adapter.dispatch_guard_hook = revoke_inside_guard
        result = coordinator.execute_action(request)
        self.assertEqual(ActionStatus.REFUSED, result.status)
        self.assertEqual([], adapter.physical_effects)

    def test_event_userlist_is_admitted_as_immutable_sequence(self) -> None:
        clock = ManualClock()
        adapter = FakeAdapter(clock)
        identity = adapter.identity()
        recorder = Recorder(
            clock,
            backend_epoch="sequence-freeze",
            adapter_id=identity.adapter_id,
            adapter_generation=identity.adapter_generation,
        )
        source = UserList(["safe"])
        event = recorder.record_event(kind="SNAPSHOT", payload={"sequence": source})
        source.append("PASSWORD=hunter2")
        self.assertEqual(("safe",), event.payload["sequence"])
        with self.assertRaises(PrivacyError):
            recorder.record_event(
                kind="SNAPSHOT",
                payload={"sequence": UserList(["PASSWORD=hunter2"])},
            )

    def test_wait_poll_latches_transient_abort_before_later_action(self) -> None:
        scenario_data = json.loads(abort_scenario_json())
        scenario_data["id"] = "wait-abort-latch"
        scenario_data["abort_conditions"] = [
            {
                "condition": {
                    "field": "player.hp",
                    "op": "LTE",
                    "value": 10,
                    "unknown_policy": "FAIL",
                },
                "reason_code": "CLIENT_NOT_IN_GAME",
            }
        ]
        scenario_data["steps"] = [
            {
                "wait": {
                    "condition": {
                        "field": "player.mana",
                        "op": "LT",
                        "value": 50,
                        "unknown_policy": "FAIL",
                    },
                    "timeout_ms": 10,
                }
            },
            {
                "action": {
                    "kind": "move",
                    "parameters": {"direction": "NORTH", "tiles": 1},
                    "timeout_ms": 1000,
                }
            },
        ]
        scenario = parse_and_validate(json.dumps(scenario_data))
        clock = ManualClock()
        adapter = FakeAdapter(clock)
        adapter.add_capability("move")
        coordinator = MutationCoordinator(
            adapter,
            DeterministicDurableStore(),
            clock,
            backend_epoch="wait-abort",
        )
        recorder = Recorder(
            clock,
            backend_epoch=coordinator.backend_epoch,
            adapter_id=adapter.identity().adapter_id,
            adapter_generation=adapter.identity().adapter_generation,
        )

        def controlled_wait(run_id, predicate, *, timeout_ms, token=None, poll_ms=1):
            del run_id, timeout_ms, token, poll_ms
            player = adapter.snapshot_values["player"]
            player["hp"] = 5
            player["mana"] = 100
            first = predicate()
            player["hp"] = 100
            player["mana"] = 0
            if first:
                return "READY"
            return "READY" if predicate() else "TIMEOUT"

        coordinator.wait_until = controlled_wait
        result = ScenarioEngine(
            adapter=adapter,
            coordinator=coordinator,
            artifacts=ArtifactStore(),
            recorder=recorder,
        ).run(scenario, run_id="wait-abort-run")
        self.assertEqual("CANCELLED", result.status)
        self.assertIn("CLIENT_NOT_IN_GAME", result.reason_codes)
        self.assertEqual([], adapter.physical_effects)

    def test_required_comparison_without_checkpoints_is_incomplete(self) -> None:
        profile = ComparisonProfile(
            "required-profile",
            "1",
            (ProfileField("player.hp", ComparisonClass.EXACT, required=True),),
        )
        result = compare_runs(
            comparison_id="comparison-empty",
            profile=profile,
            reference_run_id="reference",
            candidate_run_id="candidate",
            scenario_id="scenario",
            reference_scenario_hash="a" * 64,
            candidate_scenario_hash="a" * 64,
            checkpoint_pairs=(),
            reference_observations={},
            candidate_observations={},
        )
        self.assertEqual(ComparisonStatus.COVERAGE_INCOMPLETE, result.status)
        self.assertEqual("REQUIRED_CHECKPOINT_COVERAGE_MISSING", result.reason_code)

    def test_artifact_requested_status_is_closed_enum(self) -> None:
        scenario = parse_and_validate(abort_scenario_json())
        clock = ManualClock()
        adapter = FakeAdapter(clock)
        identity = adapter.identity()
        recorder = Recorder(
            clock,
            backend_epoch="invalid-status",
            adapter_id=identity.adapter_id,
            adapter_generation=identity.adapter_generation,
        )
        artifacts = ArtifactStore()
        artifacts.create_run(
            run_id="invalid-status",
            scenario_id=scenario.scenario_id,
            scenario_hash=scenario.scenario_hash,
            scenario_ast=scenario.ast,
            adapter_identity={"adapter_id": "fake"},
            backend_epoch="invalid-status",
            initial_control_generation=0,
            started_monotonic_ns=0,
            privacy_policy=scenario.ast["privacy_policy"],
        )
        with self.assertRaises(ValidationError) as raised:
            artifacts.finalize(
                "invalid-status",
                recorder=recorder,
                action_results={},
                requested_status="SUCCESS",
                final_control_generation=0,
                budget_summary={"safe": 1},
            )
        self.assertEqual("INVALID_RUN_RESULT_STATUS", raised.exception.code)
        self.assertNotIn("result.json", artifacts.runs["invalid-status"].stage)


if __name__ == "__main__":
    unittest.main()
