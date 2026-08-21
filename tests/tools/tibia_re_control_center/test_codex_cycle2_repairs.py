from __future__ import annotations

import json
import threading
import unittest
from collections.abc import Iterator, Mapping
from typing import Any

from test_codex_review_repairs import (
    abort_scenario_json,
    hard_budget,
    make_request,
    make_stack,
)

import tools.tibia_re_control_center.execution as execution_module
from tools.tibia_re_control_center.artifact import ArtifactStore
from tools.tibia_re_control_center.engine import ScenarioEngine
from tools.tibia_re_control_center.execution import MutationCoordinator
from tools.tibia_re_control_center.fake import FakeAdapter, ManualClock
from tools.tibia_re_control_center.model import ActionStatus, PrivacyError, ValidationError
from tools.tibia_re_control_center.recorder import Recorder
from tools.tibia_re_control_center.scenario import parse_and_validate
from tools.tibia_re_control_center.store import DeterministicDurableStore


class BlockingActivationStore(DeterministicDurableStore):
    def __init__(self) -> None:
        super().__init__()
        self.activation_started = threading.Event()
        self.activation_release = threading.Event()

    def persist_run_activation(self, run_id: str, started_ns: int, deadline_ns: int) -> None:
        if run_id == "race-run":
            self.activation_started.set()
            if not self.activation_release.wait(2):
                raise RuntimeError("activation release timed out")
        super().persist_run_activation(run_id, started_ns, deadline_ns)


class FlipIdentity(Mapping[str, Any]):
    def __init__(self) -> None:
        self.adapter_id_reads = 0
        self.values = {
            "adapter_kind": "fake",
            "adapter_version": "1",
            "adapter_generation": "generation-1",
            "runtime_instance_id": "runtime-1",
            "session_epoch": "session-1",
        }

    def __iter__(self) -> Iterator[str]:
        return iter(("adapter_id", *self.values.keys()))

    def __len__(self) -> int:
        return 1 + len(self.values)

    def __getitem__(self, key: str) -> Any:
        if key == "adapter_id":
            self.adapter_id_reads += 1
            return "fake" if self.adapter_id_reads == 1 else "PASSWORD=hunter2"
        return self.values[key]


class CycleThreeRegressionTests(unittest.TestCase):
    def test_artifact_rejection_releases_mutation_run_lease(self) -> None:
        raw = json.loads(abort_scenario_json())
        raw["name"] = "PASSWORD=hunter2"
        scenario = parse_and_validate(json.dumps(raw))
        clock = ManualClock()
        adapter = FakeAdapter(clock)
        adapter.add_capability("move")
        store = DeterministicDurableStore()
        coordinator = MutationCoordinator(
            adapter, store, clock, backend_epoch="artifact-reject"
        )
        recorder = Recorder(
            clock,
            backend_epoch=coordinator.backend_epoch,
            adapter_id=adapter.identity().adapter_id,
            adapter_generation=adapter.identity().adapter_generation,
        )
        engine = ScenarioEngine(
            adapter=adapter,
            coordinator=coordinator,
            artifacts=ArtifactStore(),
            recorder=recorder,
        )
        with self.assertRaises(PrivacyError):
            engine.run(scenario, run_id="rejected-run")
        self.assertIsNone(coordinator.active_mutation_run_id)
        self.assertEqual({}, coordinator.runs)

    def test_stop_linearizes_with_inflight_run_admission(self) -> None:
        clock = ManualClock()
        adapter = FakeAdapter(clock)
        adapter.add_capability("move")
        store = BlockingActivationStore()
        coordinator = MutationCoordinator(
            adapter, store, clock, backend_epoch="admission-stop"
        )
        admitted: list[object] = []
        stop_done = threading.Event()
        start_worker = threading.Thread(
            target=lambda: admitted.append(coordinator.start_run("race-run", hard_budget()))
        )
        start_worker.start()
        self.assertTrue(store.activation_started.wait(2))
        stop_worker = threading.Thread(
            target=lambda: (coordinator.stop_all(), stop_done.set())
        )
        stop_worker.start()
        self.assertFalse(stop_done.wait(0.1))
        store.activation_release.set()
        start_worker.join(2)
        stop_worker.join(2)
        self.assertFalse(start_worker.is_alive())
        self.assertFalse(stop_worker.is_alive())
        self.assertEqual(1, len(admitted))
        self.assertTrue(coordinator.runs["race-run"].cancelled)
        self.assertTrue(coordinator.control_state.stop_latched)

    def test_stop_cancelled_run_stays_invalid_after_reset(self) -> None:
        _, _, _, coordinator = make_stack(epoch="cancel-generation")
        coordinator.pause_run("repair-run")
        self.assertTrue(coordinator.stop_all())
        self.assertTrue(coordinator.runs["repair-run"].cancelled)
        self.assertTrue(coordinator.reset_stop())
        self.assertTrue(coordinator.runs["repair-run"].cancelled)
        self.assertFalse(coordinator.resume_run("repair-run"))

    def test_event_metadata_secret_rejected_before_construction(self) -> None:
        recorder = Recorder(
            ManualClock(),
            backend_epoch="backend",
            adapter_id="fake",
            adapter_generation="generation",
        )
        with self.assertRaises(PrivacyError):
            recorder.record_event(
                kind="SYSTEM", payload={}, source_timestamp="PASSWORD=hunter2"
            )
        self.assertEqual([], recorder.events)

    def test_concrete_abort_reason_is_in_result_envelope(self) -> None:
        scenario = parse_and_validate(abort_scenario_json())
        clock = ManualClock()
        adapter = FakeAdapter(clock)
        adapter.add_capability("move")
        store = DeterministicDurableStore()
        coordinator = MutationCoordinator(
            adapter, store, clock, backend_epoch="reason-envelope"
        )
        recorder = Recorder(
            clock,
            backend_epoch=coordinator.backend_epoch,
            adapter_id=adapter.identity().adapter_id,
            adapter_generation=adapter.identity().adapter_generation,
        )
        adapter.authority_wait_hook = lambda: adapter.snapshot_values.__setitem__(
            "client_state", "OFFLINE"
        )
        result = ScenarioEngine(
            adapter=adapter,
            coordinator=coordinator,
            artifacts=ArtifactStore(),
            recorder=recorder,
        ).run(scenario, run_id="reason-run")
        self.assertEqual(("CLIENT_NOT_IN_GAME",), result.reason_codes)
        self.assertEqual(
            ["CLIENT_NOT_IN_GAME"], result.artifact_result["reason_codes"]
        )

    def test_action_semantics_are_snapshotted_before_execution_lock(self) -> None:
        _, adapter, store, coordinator = make_stack(epoch="semantic-snapshot")
        parameters = {"direction": "NORTH", "tiles": 1}
        request = execution_module.replace(
            make_request(coordinator, adapter, "snapshot-action"), parameters=parameters
        )
        snapshotted = threading.Event()
        original_deepcopy = execution_module.copy.deepcopy

        def signaled_deepcopy(value: Any) -> Any:
            result = original_deepcopy(value)
            snapshotted.set()
            return result

        coordinator.mutation_execution_lock.acquire()
        execution_module.copy.deepcopy = signaled_deepcopy
        results: list[Any] = []
        try:
            worker = threading.Thread(
                target=lambda: results.append(coordinator.execute_action(request))
            )
            worker.start()
            self.assertTrue(snapshotted.wait(2))
            parameters["direction"] = "SOUTH"
            coordinator.mutation_execution_lock.release()
            worker.join(2)
        finally:
            execution_module.copy.deepcopy = original_deepcopy
            if coordinator.mutation_execution_lock.locked():
                coordinator.mutation_execution_lock.release()
        self.assertEqual(ActionStatus.PASS, results[0].status)
        self.assertEqual(
            "NORTH", adapter.physical_effects[0]["parameters"]["direction"]
        )
        self.assertEqual(
            request.action_request_hash,
            store.load_action(request.action_id).action_request_hash,
        )

    def test_artifact_metadata_is_snapshotted_before_privacy_scan(self) -> None:
        scenario = parse_and_validate(abort_scenario_json())
        identity = FlipIdentity()
        artifacts = ArtifactStore()
        run = artifacts.create_run(
            run_id="snapshot-metadata",
            scenario_id=scenario.scenario_id,
            scenario_hash=scenario.scenario_hash,
            scenario_ast=scenario.ast,
            adapter_identity=identity,
            backend_epoch="backend",
            initial_control_generation=0,
            started_monotonic_ns=0,
            privacy_policy=scenario.ast["privacy_policy"],
        )
        self.assertEqual(1, identity.adapter_id_reads)
        self.assertEqual("fake", run.adapter_identity["adapter_id"])

    def test_recovered_mutation_run_cannot_rebase_after_stop_restart(self) -> None:
        clock = ManualClock()
        adapter = FakeAdapter(clock)
        adapter.add_capability("move")
        store = DeterministicDurableStore()
        first = MutationCoordinator(adapter, store, clock, backend_epoch="recover-one")
        first.start_run("old-run", hard_budget())
        self.assertTrue(first.stop_all())
        second_adapter = FakeAdapter(clock)
        second_adapter.add_capability("move")
        second = MutationCoordinator(
            second_adapter, store, clock, backend_epoch="recover-two"
        )
        recovered = second.recover_run("old-run")
        self.assertTrue(recovered.cancelled)
        self.assertTrue(second.reset_stop())
        with self.assertRaises(ValidationError):
            second.acquire_mutation_run("old-run")

    def test_privacy_policy_snapshot_is_scanned_and_must_match_ast(self) -> None:
        scenario = parse_and_validate(abort_scenario_json())
        artifacts = ArtifactStore()
        with self.assertRaises(PrivacyError):
            artifacts.create_run(
                run_id="privacy-policy",
                scenario_id=scenario.scenario_id,
                scenario_hash=scenario.scenario_hash,
                scenario_ast=scenario.ast,
                adapter_identity={"adapter_id": "fake"},
                backend_epoch="b",
                initial_control_generation=0,
                started_monotonic_ns=0,
                privacy_policy={"password": "hunter2"},
            )

    def test_write_stage_rejects_secret_shaped_bytes(self) -> None:
        scenario = parse_and_validate(abort_scenario_json())
        artifacts = ArtifactStore()
        artifacts.create_run(
            run_id="stage-privacy",
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
            artifacts.write_stage("stage-privacy", "trace.txt", b"PASSWORD=hunter2")

    def test_dynamic_action_request_rejects_non_enum_authority(self) -> None:
        _, adapter, _, coordinator = make_stack(epoch="authority-enum")
        request = make_request(coordinator, adapter, "authority-action")
        with self.assertRaises(ValidationError):
            execution_module.replace(request, required_authority="INVALID")


if __name__ == "__main__":
    unittest.main()
