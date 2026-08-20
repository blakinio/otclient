from __future__ import annotations

import json
import threading

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
from tools.tibia_re_control_center.scenario import action_request_hash, parse_and_validate
from tools.tibia_re_control_center.store import DeterministicDurableStore


def audit_budget() -> SideEffectBudget:
    return SideEffectBudget(10, 4, 4, 0, 0, 0, 0, 0, 0)


def stack(*, epoch: str):
    clock = ManualClock()
    adapter = FakeAdapter(clock)
    adapter.add_capability("move")
    store = DeterministicDurableStore()
    coordinator = MutationCoordinator(adapter, store, clock, backend_epoch=epoch)
    coordinator.start_run("audit-p1-run", audit_budget())
    return clock, adapter, store, coordinator


def request_for(coordinator: MutationCoordinator, adapter: FakeAdapter, action_id: str) -> ActionRequest:
    parameters = {"direction": "NORTH", "tiles": 1}
    identity = adapter.identity()
    return ActionRequest(
        action_id=action_id,
        run_id="audit-p1-run",
        step_id="audit-p1-step",
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
        action_request_hash=action_request_hash(
            schema_version=1,
            run_id="audit-p1-run",
            step_id="audit-p1-step",
            attempt_index=1,
            kind="move",
            parameters=parameters,
            timeout_ms=1000,
            required_capability="move",
            required_authority=Authority.MUTATION,
        ),
    )


def abort_scenario() -> str:
    return json.dumps(
        {
            "schema_version": 1,
            "id": "audit-p1-abort",
            "name": "P1 final-gate abort audit",
            "adapter_requirements": {"reads": [], "actions": ["move"]},
            "preconditions": [],
            "side_effect_budget": audit_budget().as_dict(),
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


def main() -> None:
    _, _, store, coordinator = stack(epoch="audit-stop")
    store.inject_fault("stop", "error")
    assert coordinator.stop_all() is False
    assert coordinator.stop_durability_unresolved is True
    assert coordinator.reset_stop() is False
    assert coordinator.mutation_admission_allowed() is False
    assert coordinator.stop_all() is True
    assert coordinator.stop_durability_unresolved is False

    scenario = parse_and_validate(abort_scenario())
    clock = ManualClock()
    adapter = FakeAdapter(clock)
    adapter.add_capability("move")
    durable = DeterministicDurableStore()
    guarded = MutationCoordinator(adapter, durable, clock, backend_epoch="audit-abort")
    recorder = Recorder(
        clock,
        backend_epoch=guarded.backend_epoch,
        adapter_id=adapter.identity().adapter_id,
        adapter_generation=adapter.identity().adapter_generation,
    )
    adapter.authority_wait_hook = lambda: adapter.snapshot_values.__setitem__("client_state", "OFFLINE")
    result = ScenarioEngine(
        adapter=adapter,
        coordinator=guarded,
        artifacts=ArtifactStore(),
        recorder=recorder,
    ).run(scenario, run_id="audit-abort-run")
    assert result.status == "REFUSED"
    assert adapter.physical_effects == []

    _, adapter, store, coordinator = stack(epoch="audit-callback")
    request = request_for(coordinator, adapter, "audit-callback-action")
    coordinator._reserve(coordinator.runs["audit-p1-run"], request)  # noqa: SLF001
    identity = adapter.identity()
    assert coordinator.accept_callback(
        request.action_id,
        backend_epoch=coordinator.backend_epoch,
        control_generation=coordinator.control_generation,
        adapter_generation=identity.adapter_generation,
        runtime_instance_id=identity.runtime_instance_id,
        session_epoch=identity.session_epoch,
        lifecycle_state=LifecycleState.CONFIRMED,
        authoritative_confirmation=Confirmation.PROVEN,
    ) is False
    adapter.set_identity(session_epoch="replacement-session")
    assert coordinator.accept_callback(
        request.action_id,
        backend_epoch=coordinator.backend_epoch,
        control_generation=coordinator.control_generation,
        adapter_generation=identity.adapter_generation,
        runtime_instance_id=identity.runtime_instance_id,
        session_epoch=identity.session_epoch,
        lifecycle_state=LifecycleState.DISPATCHING,
    ) is False
    assert store.load_action(request.action_id).lifecycle_state == LifecycleState.RESERVED

    _, adapter, store, coordinator = stack(epoch="audit-shutdown")
    request = request_for(coordinator, adapter, "audit-shutdown-action")
    committed = threading.Event()
    release = threading.Event()
    results = []

    def hold_after_commit() -> None:
        committed.set()
        if not release.wait(2):
            raise RuntimeError("audit action was not released")

    adapter.after_commit_hook = hold_after_commit
    worker = threading.Thread(target=lambda: results.append(coordinator.execute_action(request)))
    worker.start()
    assert committed.wait(2)
    assert store.load_action(request.action_id).dispatch_state != DispatchState.NOT_DISPATCHED
    assert coordinator.clean_shutdown() is False
    assert store.load_control_state().active_backend_epoch == coordinator.backend_epoch
    release.set()
    worker.join(2)
    assert not worker.is_alive()
    assert results and results[0].status == ActionStatus.PASS

    print("PACKAGE_A_CODEX_P1_AUDIT=PASS")
    print("FAILED_STOP_RESET_FENCE=PASS")
    print("FINAL_GATE_ABORT_REVALIDATION=PASS")
    print("CALLBACK_IDENTITY_TERMINAL_FENCE=PASS")
    print("CLEAN_SHUTDOWN_INFLIGHT_FENCE=PASS")


if __name__ == "__main__":
    main()
