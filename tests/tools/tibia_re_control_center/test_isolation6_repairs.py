from __future__ import annotations

import unittest

from test_codex_review_repairs import abort_scenario_json, make_request, make_stack

from tools.tibia_re_control_center.artifact import ArtifactStore
from tools.tibia_re_control_center.fake import FakeAdapter, ManualClock
from tools.tibia_re_control_center.model import ActionStatus, PrivacyError
from tools.tibia_re_control_center.recorder import Recorder
from tools.tibia_re_control_center.scenario import parse_and_validate


class IsolationSixRegressionTests(unittest.TestCase):
    def test_capability_is_rechecked_after_final_authority_callback(self) -> None:
        _, adapter, _, coordinator = make_stack(epoch="capability-final-p1")
        request = make_request(coordinator, adapter, "capability-final")
        original = adapter.current_authority
        calls = 0

        def revoke_after_authority(authority):
            nonlocal calls
            calls += 1
            result = original(authority)
            if calls >= 3:
                adapter.add_capability(request.required_capability, read=True, action=False)
            return result

        adapter.current_authority = revoke_after_authority
        result = coordinator.execute_action(request)
        self.assertEqual(ActionStatus.REFUSED, result.status)
        self.assertEqual([], adapter.physical_effects)

    def test_event_payload_cannot_be_mutated_via_dict_descriptor(self) -> None:
        clock = ManualClock()
        adapter = FakeAdapter(clock)
        identity = adapter.identity()
        recorder = Recorder(
            clock,
            backend_epoch="event-proxy",
            adapter_id=identity.adapter_id,
            adapter_generation=identity.adapter_generation,
        )
        event = recorder.record_event(kind="SNAPSHOT", payload={"nested": {"safe": "value"}})
        with self.assertRaises(TypeError):
            dict.__setitem__(event.payload, "password", "hunter2")
        with self.assertRaises(TypeError):
            dict.__setitem__(event.payload["nested"], "password", "hunter2")
        self.assertEqual("value", event.payload["nested"]["safe"])

    def test_finalize_privacy_classifies_status(self) -> None:
        scenario = parse_and_validate(abort_scenario_json())
        clock = ManualClock()
        adapter = FakeAdapter(clock)
        identity = adapter.identity()
        recorder = Recorder(
            clock,
            backend_epoch="status-privacy",
            adapter_id=identity.adapter_id,
            adapter_generation=identity.adapter_generation,
        )
        artifacts = ArtifactStore()
        artifacts.create_run(
            run_id="status-privacy",
            scenario_id=scenario.scenario_id,
            scenario_hash=scenario.scenario_hash,
            scenario_ast=scenario.ast,
            adapter_identity={"adapter_id": "fake"},
            backend_epoch="status-privacy",
            initial_control_generation=0,
            started_monotonic_ns=0,
            privacy_policy=scenario.ast["privacy_policy"],
        )
        with self.assertRaises(PrivacyError):
            artifacts.finalize(
                "status-privacy",
                recorder=recorder,
                action_results={},
                requested_status="PASSWORD=hunter2",
                final_control_generation=0,
                budget_summary={"safe": 1},
                assertions={"safe": True},
            )
        self.assertNotIn("result.json", artifacts.runs["status-privacy"].stage)


if __name__ == "__main__":
    unittest.main()
