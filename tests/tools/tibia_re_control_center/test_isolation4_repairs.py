from __future__ import annotations

import threading
import unittest

from test_codex_review_repairs import abort_scenario_json, make_request, make_stack

from tools.tibia_re_control_center.artifact import ArtifactStore
from tools.tibia_re_control_center.model import ActionStatus, PrivacyError
from tools.tibia_re_control_center.recorder import Recorder
from tools.tibia_re_control_center.scenario import parse_and_validate


class IsolationFourRegressionTests(unittest.TestCase):
    def test_action_timeout_is_rechecked_after_final_safety_hook(self) -> None:
        clock, adapter, _, coordinator = make_stack(epoch="post-hook-timeout")
        request = make_request(coordinator, adapter, "post-hook-timeout-action")

        def final_check():
            clock.advance_ms(request.timeout_ms + 1)

        result = coordinator.execute_action(request, final_commit_check=final_check)
        self.assertEqual(ActionStatus.TIMEOUT, result.status)
        self.assertEqual("ACTION_TIMEOUT_EXPIRED", result.reason_code)
        self.assertEqual([], adapter.physical_effects)

    def test_recover_run_publication_linearizes_with_stop(self) -> None:
        _, _, _, coordinator = make_stack(epoch="recovery-stop-race")
        run_id = next(iter(coordinator.runs))
        coordinator.finish_run(run_id)
        checked = threading.Event()
        release = threading.Event()
        original = coordinator.mutation_admission_allowed

        def blocking_admission():
            allowed = original()
            checked.set()
            if not release.wait(2):
                raise RuntimeError("recovery admission release timed out")
            return allowed

        coordinator.mutation_admission_allowed = blocking_admission
        recovered_holder = []
        recover_thread = threading.Thread(target=lambda: recovered_holder.append(coordinator.recover_run(run_id)))
        stop_done = threading.Event()
        stop_thread = threading.Thread(target=lambda: (coordinator.stop_all(), stop_done.set()))
        recover_thread.start()
        self.assertTrue(checked.wait(1))
        stop_thread.start()
        self.assertFalse(stop_done.wait(0.05))
        release.set()
        recover_thread.join(2)
        stop_thread.join(2)
        self.assertFalse(recover_thread.is_alive())
        self.assertFalse(stop_thread.is_alive())
        self.assertTrue(recovered_holder[0].cancelled)

    def test_duplicate_key_json_secret_is_rejected(self) -> None:
        scenario = parse_and_validate(abort_scenario_json())
        artifacts = ArtifactStore()
        artifacts.create_run(
            run_id="duplicate-json",
            scenario_id=scenario.scenario_id,
            scenario_hash=scenario.scenario_hash,
            scenario_ast=scenario.ast,
            adapter_identity={"adapter_id": "fake"},
            backend_epoch="b",
            initial_control_generation=0,
            started_monotonic_ns=0,
            privacy_policy=scenario.ast["privacy_policy"],
        )
        with self.assertRaises(Exception) as ctx:
            artifacts.write_stage(
                "duplicate-json",
                "metadata.json",
                b'{"note":"PASSWORD=hunter2","note":"safe"}',
            )
        self.assertIn("duplicate JSON key", str(ctx.exception))

    def test_source_sequence_is_privacy_classified(self) -> None:
        clock, adapter, _, coordinator = make_stack(epoch="event-source-sequence")
        identity = adapter.identity()
        recorder = Recorder(
            clock,
            backend_epoch=coordinator.backend_epoch,
            adapter_id=identity.adapter_id,
            adapter_generation=identity.adapter_generation,
        )
        with self.assertRaises(PrivacyError):
            recorder.record_event(
                kind="SNAPSHOT",
                payload={},
                source_sequence="PASSWORD=hunter2",
            )


if __name__ == "__main__":
    unittest.main()
