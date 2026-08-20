from __future__ import annotations

import json
import threading
import unittest

from tools.tibia_re_control_center.artifact import ArtifactStore
from tools.tibia_re_control_center.engine import ScenarioEngine
from tools.tibia_re_control_center.execution import MutationCoordinator
from tools.tibia_re_control_center.fake import FakeAdapter, ManualClock
from tools.tibia_re_control_center.model import (
    ActionRequest,
    ActionStatus,
    Authority,
    Confirmation,
    DispatchFence,
    DispatchState,
    LifecycleState,
    SideEffectBudget,
)
from tools.tibia_re_control_center.recorder import Recorder
from tools.tibia_re_control_center.scenario import (
    action_request_hash,
    parse_and_validate,
)
from tools.tibia_re_control_center.store import DeterministicDurableStore


def hard_budget() -> SideEffectBudget:
    return SideEffectBudget(10, 4, 4, 0, 0, 0, 0, 0, 0)


def make_stack(*, epoch: str = "repair-backend"):
    clock = ManualClock()
    adapter = FakeAdapter(clock)
    adapter.add_capability("move")
    store = DeterministicDurableStore()
    coordinator = MutationCoordinator(adapter, store, clock, backend_epoch=epoch)
    coordinator.start_run("repair-run", hard_budget())
    return clock, adapter, store, coordinator


def make_request(coordinator: MutationCoordinator, adapter: FakeAdapter, action_id: str = "repair-action") -> ActionRequest:
    parameters = {"direction": "NORTH", "tiles": 1}
    identity = adapter.identity()
    request_hash = action_request_hash(
        schema_version=1,
        run_id="repair-run",
        step_id="repair-step",
        attempt_index=1,
        kind="move",
        parameters=parameters,
        timeout_ms=1000,
        required_capability="move",
        required_authority=Authority.MUTATION,
    )
    return ActionRequest(
        action_id=action_id,
        run_id="repair-run",
        step_id="repair-step",
        attempt_index=1,
        kind="move",
        parameters=parameters,
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
        effect_bound=adapter.effect_bound("move", parameters),
        action_request_hash=request_hash,
    )


def abort_scenario_json() -> str:
    return json.dumps(
        {
            "schema_version": 1,
            "id": "abort-final-gate",
            "name": "Abort revalidation at final dispatch gate",
            "adapter_requirements": {"reads": [], "actions": ["move"]},
            "preconditions": [],
            "side_effect_budget": hard_budget().as_dict(),
            "capture_policy": {
                "state": True,
                "events": True,
                "screenshots": "NONE",
                "network": "NONE",
                "traces": "NONE",
            },
            "steps": [
                {
                    "action": {
                        "kind": "move",
                        "parameters": {"direction": "NORTH", "tiles": 1},
                        "timeout_ms": 1000,
                    }
                }
            ],
            "abort_conditions": [
                {
                    "condition": {
                        "field": "client_state",
                        "op": "NE",
                        "value": "IN_GAME",
                        "unknown_policy": "FAIL",
                    },
                    "reason_code": "CLIENT_NOT_IN_GAME",
                }
            ],
            "expected_result": [],
            "privacy_policy": {
                "secret_material": "REJECT",
                "private_chat": "OMIT",
                "identities": "OMIT",
                "screenshots": "SAFE_ONLY",
            },
        }
    )


class CodexP1RegressionTests(unittest.TestCase):
    def test_failed_stop_cannot_be_reset_until_stop_is_durable(self):
        _, _, store, coordinator = make_stack()
        store.inject_fault("stop", "error")

        self.assertFalse(coordinator.stop_all())
        self.assertTrue(coordinator.in_memory_stop)
        self.assertTrue(coordinator.stop_durability_unresolved)
        self.assertFalse(coordinator.reset_stop())
        self.assertFalse(coordinator.mutation_admission_allowed())
        self.assertFalse(store.load_control_state().stop_latched)

        self.assertTrue(coordinator.stop_all())
        self.assertFalse(coordinator.stop_durability_unresolved)
        self.assertTrue(store.load_control_state().stop_latched)
        self.assertTrue(coordinator.reset_stop())
        self.assertTrue(coordinator.mutation_admission_allowed())

    def test_abort_condition_is_rechecked_at_final_dispatch_gate(self):
        scenario = parse_and_validate(abort_scenario_json())
        clock = ManualClock()
        adapter = FakeAdapter(clock)
        adapter.add_capability("move")
        store = DeterministicDurableStore()
        coordinator = MutationCoordinator(adapter, store, clock, backend_epoch="abort-backend")
        recorder = Recorder(
            clock,
            backend_epoch=coordinator.backend_epoch,
            adapter_id=adapter.identity().adapter_id,
            adapter_generation=adapter.identity().adapter_generation,
        )
        adapter.authority_wait_hook = lambda: adapter.snapshot_values.__setitem__("client_state", "OFFLINE")

        result = ScenarioEngine(
            adapter=adapter,
            coordinator=coordinator,
            artifacts=ArtifactStore(),
            recorder=recorder,
        ).run(scenario, run_id="abort-run")

        self.assertEqual("REFUSED", result.status)
        self.assertEqual([], adapter.physical_effects)
        action = next(iter(result.action_results.values()))
        self.assertEqual(DispatchState.NOT_DISPATCHED, action.dispatch_state)

    def test_callback_cannot_terminalize_or_cross_adapter_session_fence(self):
        _, adapter, store, coordinator = make_stack()
        request = make_request(coordinator, adapter)
        coordinator._reserve(coordinator.runs["repair-run"], request)
        original = adapter.identity()

        self.assertFalse(
            coordinator.accept_callback(
                request.action_id,
                backend_epoch=coordinator.backend_epoch,
                control_generation=coordinator.control_generation,
                adapter_generation=original.adapter_generation,
                runtime_instance_id=original.runtime_instance_id,
                session_epoch=original.session_epoch,
                lifecycle_state=LifecycleState.CONFIRMED,
                authoritative_confirmation=Confirmation.PROVEN,
            )
        )
        self.assertEqual(LifecycleState.RESERVED, store.load_action(request.action_id).lifecycle_state)

        adapter.set_identity(session_epoch="replacement-session")
        self.assertFalse(
            coordinator.accept_callback(
                request.action_id,
                backend_epoch=coordinator.backend_epoch,
                control_generation=coordinator.control_generation,
                adapter_generation=original.adapter_generation,
                runtime_instance_id=original.runtime_instance_id,
                session_epoch=original.session_epoch,
                lifecycle_state=LifecycleState.DISPATCHING,
            )
        )
        self.assertEqual(LifecycleState.RESERVED, store.load_action(request.action_id).lifecycle_state)

    def test_clean_shutdown_refuses_while_committed_action_is_in_flight(self):
        _, adapter, store, coordinator = make_stack()
        request = make_request(coordinator, adapter)
        committed = threading.Event()
        release = threading.Event()
        results = []

        def hold_after_commit() -> None:
            committed.set()
            if not release.wait(2):
                raise RuntimeError("test action was not released")

        adapter.after_commit_hook = hold_after_commit
        worker = threading.Thread(target=lambda: results.append(coordinator.execute_action(request)))
        worker.start()
        self.assertTrue(committed.wait(2))
        self.assertNotEqual(DispatchState.NOT_DISPATCHED, store.load_action(request.action_id).dispatch_state)

        self.assertFalse(coordinator.clean_shutdown())
        self.assertEqual(coordinator.backend_epoch, store.load_control_state().active_backend_epoch)

        release.set()
        worker.join(2)
        self.assertFalse(worker.is_alive())
        self.assertEqual(ActionStatus.PASS, results[0].status)
        coordinator.finish_run("repair-run")
        self.assertTrue(coordinator.clean_shutdown())
        self.assertIsNone(store.load_control_state().active_backend_epoch)


if __name__ == "__main__":
    unittest.main()
