from __future__ import annotations

import json
import threading
import unittest
from collections.abc import Mapping

from tools.tibia_re_control_center.artifact import ArtifactStore
from tools.tibia_re_control_center.engine import ScenarioEngine
from tools.tibia_re_control_center.execution import MutationCoordinator
from tools.tibia_re_control_center.fake import FakeAdapter, ManualClock
from tools.tibia_re_control_center.model import (
    ActionRequest,
    ActionStatus,
    Authority,
    DispatchFence,
    PrivacyError,
    SideEffectBudget,
)
from tools.tibia_re_control_center.recorder import Recorder
from tools.tibia_re_control_center.scenario import action_request_hash, parse_and_validate
from tools.tibia_re_control_center.store import DeterministicDurableStore


def budget() -> SideEffectBudget:
    return SideEffectBudget(10, 4, 4, 0, 0, 0, 0, 0, 0)


def stack(epoch: str = "cycle2"):
    clock = ManualClock()
    adapter = FakeAdapter(clock)
    adapter.add_capability("move")
    store = DeterministicDurableStore()
    coordinator = MutationCoordinator(adapter, store, clock, backend_epoch=epoch)
    coordinator.start_run("run", budget())
    return clock, adapter, store, coordinator


def request_for(coordinator: MutationCoordinator, adapter: FakeAdapter, parameters: Mapping[str, object] | None = None):
    params = dict(parameters or {"direction": "NORTH", "tiles": 1})
    identity = adapter.identity()
    digest = action_request_hash(
        schema_version=1,
        run_id="run",
        step_id="step",
        attempt_index=1,
        kind="move",
        parameters=params,
        timeout_ms=1000,
        required_capability="move",
        required_authority=Authority.MUTATION,
    )
    return ActionRequest(
        action_id="run:step:attempt-1",
        run_id="run",
        step_id="step",
        attempt_index=1,
        kind="move",
        parameters=params,
        timeout_ms=1000,
        required_capability="move",
        required_authority=Authority.MUTATION,
        dispatch_fence=DispatchFence(
            expected_backend_epoch=coordinator.backend_epoch,
            expected_control_generation=coordinator.control_generation,
            expected_adapter_generation=identity.adapter_generation,
            expected_runtime_instance_id=identity.runtime_instance_id,
            expected_session_epoch=identity.session_epoch,
        ),
        effect_bound=adapter.effect_bound("move", params),
        action_request_hash=digest,
    )


def scenario_json(name: str = "safe") -> str:
    return json.dumps({
        "schema_version": 1,
        "scenario_id": "cycle2-scenario",
        "name": name,
        "side_effect_budget": {
            "max_runtime_seconds": 10,
            "max_tiles_moved": 4,
            "max_target_changes": 4,
            "max_items_used": 0,
            "max_items_moved": 0,
            "max_chat_messages": 0,
            "max_ui_writes": 0,
            "max_other_mutations": 0,
            "max_irreversible_actions": 0,
        },
        "privacy_policy": {"secret_material": "REJECT"},
        "preconditions": [],
        "abort_conditions": [],
        "steps": [],
        "expected_result": [],
    })


class FlipMapping(Mapping[str, object]):
    def __init__(self) -> None:
        self.reads = 0

    def __iter__(self):
        return iter(("adapter_id", "adapter_kind"))

    def __len__(self) -> int:
        return 2

    def __getitem__(self, key: str) -> object:
        if key == "adapter_kind":
            return "fake"
        self.reads += 1
        return "fake" if self.reads == 1 else "PASSWORD=hunter2"


class CycleTwoIsolationTests(unittest.TestCase):
    def test_artifact_rejection_releases_run_lease(self):
        scenario = parse_and_validate(scenario_json("PASSWORD=hunter2"))
        clock = ManualClock()
        adapter = FakeAdapter(clock)
        store = DeterministicDurableStore()
        coordinator = MutationCoordinator(adapter, store, clock, backend_epoch="lease")
        recorder = Recorder(clock, backend_epoch="lease", adapter_id="fake", adapter_generation="g")
        engine = ScenarioEngine(adapter=adapter, coordinator=coordinator, artifacts=ArtifactStore(), recorder=recorder)
        with self.assertRaises(PrivacyError):
            engine.run(scenario, run_id="lease-run")
        self.assertIsNone(coordinator.active_mutation_run_id)
        self.assertEqual({}, coordinator.runs)

    def test_stop_cancelled_run_stays_terminal_after_reset(self):
        _, _, _, coordinator = stack("cancel")
        coordinator.pause_run("run")
        self.assertTrue(coordinator.stop_all())
        self.assertTrue(coordinator.reset_stop())
        self.assertFalse(coordinator.resume_run("run"))

    def test_event_metadata_secret_rejected(self):
        clock = ManualClock()
        recorder = Recorder(clock, backend_epoch="b", adapter_id="a", adapter_generation="g")
        with self.assertRaises(PrivacyError):
            recorder.record_event(kind="SYSTEM", payload={}, source_clock_domain="PASSWORD=hunter2")
        self.assertEqual([], recorder.events)

    def test_artifact_metadata_is_snapshotted_before_scan(self):
        scenario = parse_and_validate(scenario_json())
        store = ArtifactStore()
        run = store.create_run(
            run_id="artifact-run",
            scenario_id=scenario.scenario_id,
            scenario_hash=scenario.scenario_hash,
            scenario_ast=scenario.ast,
            adapter_identity=FlipMapping(),
            backend_epoch="backend",
            initial_control_generation=0,
            started_monotonic_ns=0,
            privacy_policy=scenario.ast["privacy_policy"],
        )
        self.assertEqual("fake", run.adapter_identity["adapter_id"])

    def test_request_parameters_are_snapshotted_before_execution(self):
        _, adapter, _, coordinator = stack("snapshot")
        params = {"direction": "NORTH", "tiles": 1}
        request = request_for(coordinator, adapter, params)
        entered = threading.Event()
        release = threading.Event()
        original = adapter.await_authority

        def wait(req):
            entered.set()
            release.wait(2)
            return original(req)

        adapter.await_authority = wait
        result_box = []
        worker = threading.Thread(target=lambda: result_box.append(coordinator.execute_action(request)))
        worker.start()
        self.assertTrue(entered.wait(2))
        params["direction"] = "SOUTH"
        release.set()
        worker.join(2)
        self.assertEqual(ActionStatus.PASS, result_box[0].status)
        self.assertEqual("NORTH", adapter.physical_effects[0]["parameters"]["direction"])


if __name__ == "__main__":
    unittest.main()
