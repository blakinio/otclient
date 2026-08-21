from __future__ import annotations

import threading
import unittest
from dataclasses import replace

from test_codex_review_repairs import abort_scenario_json, make_request, make_stack

from tools.tibia_re_control_center.artifact import ArtifactStore
from tools.tibia_re_control_center.fake import FakeAdapter, ManualClock
from tools.tibia_re_control_center.model import ActionStatus, Authority, PrivacyError
from tools.tibia_re_control_center.recorder import Recorder
from tools.tibia_re_control_center.scenario import (
    action_request_hash,
    parse_and_validate,
)


class IsolationFiveRegressionTests(unittest.TestCase):
    def test_effect_request_requires_mutation_authority(self) -> None:
        _, adapter, _, coordinator = make_stack(epoch="authority-p1")
        adapter.add_capability("move", read=True, action=False)
        original = make_request(coordinator, adapter, "read-authority-effect")
        request_hash = action_request_hash(
            schema_version=original.schema_version,
            run_id=original.run_id,
            step_id=original.step_id,
            attempt_index=original.attempt_index,
            kind=original.kind,
            parameters=original.parameters,
            timeout_ms=original.timeout_ms,
            required_capability=original.required_capability,
            required_authority=Authority.READ_ONLY,
        )
        request = replace(original, required_authority=Authority.READ_ONLY, action_request_hash=request_hash)
        result = coordinator.execute_action(request)
        self.assertEqual(ActionStatus.REFUSED, result.status)
        self.assertEqual("MUTATION_AUTHORITY_REQUIRED", result.reason_code)
        self.assertEqual([], adapter.physical_effects)

    def test_timeout_is_checked_after_last_authority_revalidation(self) -> None:
        clock, adapter, _, coordinator = make_stack(epoch="last-timeout-p1")
        request = make_request(coordinator, adapter, "last-timeout")
        original = adapter.current_authority
        calls = 0

        def delayed_current_authority(authority):
            nonlocal calls
            calls += 1
            result = original(authority)
            if calls >= 3:
                clock.advance_ms(request.timeout_ms + 1)
            return result

        adapter.current_authority = delayed_current_authority
        result = coordinator.execute_action(request)
        self.assertEqual(ActionStatus.TIMEOUT, result.status)
        self.assertEqual("ACTION_TIMEOUT_EXPIRED", result.reason_code)
        self.assertEqual([], adapter.physical_effects)

    def test_overlapping_stop_cleanup_remains_fenced(self) -> None:
        _, adapter, _, coordinator = make_stack(epoch="overlap-stop-p1")
        entered_first = threading.Event()
        entered_second = threading.Event()
        release_first = threading.Event()
        release_second = threading.Event()
        count_lock = threading.Lock()
        count = 0

        def blocking_stop(reason):
            del reason
            nonlocal count
            with count_lock:
                count += 1
                current = count
            if current == 1:
                entered_first.set()
                self.assertTrue(release_first.wait(2))
            else:
                entered_second.set()
                self.assertTrue(release_second.wait(2))
            adapter.emergency_stop_calls += 1

        adapter.emergency_stop = blocking_stop
        first = threading.Thread(target=coordinator.stop_all)
        second = threading.Thread(target=coordinator.stop_all)
        first.start()
        self.assertTrue(entered_first.wait(1))
        second.start()
        self.assertFalse(entered_second.wait(0.05))
        self.assertTrue(coordinator.stop_cleanup_in_progress)
        release_first.set()
        self.assertTrue(entered_second.wait(1))
        self.assertTrue(coordinator.stop_cleanup_in_progress)
        self.assertFalse(coordinator.reset_stop())
        release_second.set()
        first.join(2)
        second.join(2)
        self.assertFalse(first.is_alive())
        self.assertFalse(second.is_alive())
        self.assertFalse(coordinator.stop_cleanup_in_progress)

    def test_event_payload_is_recursively_immutable(self) -> None:
        clock = ManualClock()
        adapter = FakeAdapter(clock)
        identity = adapter.identity()
        recorder = Recorder(
            clock,
            backend_epoch="event-freeze",
            adapter_id=identity.adapter_id,
            adapter_generation=identity.adapter_generation,
        )
        event = recorder.record_event(kind="SNAPSHOT", payload={"nested": {"safe": "value"}})
        with self.assertRaises(TypeError):
            event.payload["password"] = "hunter2"
        with self.assertRaises(TypeError):
            event.payload["nested"]["password"] = "hunter2"
        self.assertEqual("value", event.payload["nested"]["safe"])

    def test_finalize_rejects_secret_shaped_result_inputs(self) -> None:
        scenario = parse_and_validate(abort_scenario_json())
        clock = ManualClock()
        adapter = FakeAdapter(clock)
        identity = adapter.identity()
        recorder = Recorder(
            clock,
            backend_epoch="finalize-privacy",
            adapter_id=identity.adapter_id,
            adapter_generation=identity.adapter_generation,
        )
        artifacts = ArtifactStore()
        artifacts.create_run(
            run_id="finalize-privacy",
            scenario_id=scenario.scenario_id,
            scenario_hash=scenario.scenario_hash,
            scenario_ast=scenario.ast,
            adapter_identity={"adapter_id": "fake"},
            backend_epoch="finalize-privacy",
            initial_control_generation=0,
            started_monotonic_ns=0,
            privacy_policy=scenario.ast["privacy_policy"],
        )
        with self.assertRaises(PrivacyError):
            artifacts.finalize(
                "finalize-privacy",
                recorder=recorder,
                action_results={},
                requested_status="REFUSED",
                final_control_generation=0,
                budget_summary={"safe": 1},
                assertions={"safe": True},
                reason_codes=["PASSWORD=hunter2"],
            )
        self.assertNotIn("result.json", artifacts.runs["finalize-privacy"].stage)


if __name__ == "__main__":
    unittest.main()
