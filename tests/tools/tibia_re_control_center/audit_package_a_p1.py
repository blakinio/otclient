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
    PrivacyError,
    SideEffectBudget,
    ValidationError,
)
from tools.tibia_re_control_center.recorder import Recorder
from tools.tibia_re_control_center.scenario import (
    action_request_hash,
    parse_and_validate,
)
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
    _, stop_adapter, store, coordinator = stack(epoch="audit-stop")
    capture = stop_adapter.capture_start({"state": True})
    store.inject_fault("stop", "error")
    assert coordinator.stop_all() is False
    assert coordinator.stop_durability_unresolved is True
    assert coordinator.runs["audit-p1-run"].cancelled is True
    assert stop_adapter.emergency_stop_calls == 1
    assert stop_adapter.capture_sessions[capture]["active"] is False
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
    abort_action = next(iter(result.action_results.values()))
    assert abort_action.reason_code == "CLIENT_NOT_IN_GAME"

    _, adapter, store, coordinator = stack(epoch="audit-callback")
    request = request_for(coordinator, adapter, "audit-callback-action")
    coordinator._reserve(coordinator.runs["audit-p1-run"], request)
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

    _, race_adapter, race_store, race_coordinator = stack(epoch="audit-callback-race")
    race_request = request_for(race_coordinator, race_adapter, "audit-callback-race-action")
    race_identity = race_adapter.identity()
    callback_results: list[bool] = []

    def callback_during_execution() -> None:
        callback_results.append(
            race_coordinator.accept_callback(
                race_request.action_id,
                backend_epoch=race_coordinator.backend_epoch,
                control_generation=race_coordinator.control_generation,
                adapter_generation=race_identity.adapter_generation,
                runtime_instance_id=race_identity.runtime_instance_id,
                session_epoch=race_identity.session_epoch,
                lifecycle_state=LifecycleState.CONFIRMING,
            )
        )

    race_adapter.after_commit_hook = callback_during_execution
    race_result = race_coordinator.execute_action(race_request)
    assert callback_results == [False]
    assert race_result.status == ActionStatus.PASS
    assert race_store.load_action(race_request.action_id).lifecycle_state == LifecycleState.CONFIRMED

    secret_raw = json.loads(abort_scenario())
    secret_raw["name"] = "PASSWORD=hunter2"
    secret_scenario = parse_and_validate(json.dumps(secret_raw))
    secret_artifacts = ArtifactStore()
    try:
        secret_artifacts.create_run(
            run_id="audit-secret-run",
            scenario_id=secret_scenario.scenario_id,
            scenario_hash=secret_scenario.scenario_hash,
            scenario_ast=secret_scenario.ast,
            adapter_identity={"adapter_id": "fake"},
            backend_epoch="audit-secret",
            initial_control_generation=0,
            started_monotonic_ns=0,
            privacy_policy=secret_scenario.ast["privacy_policy"],
        )
    except PrivacyError:
        pass
    else:
        raise AssertionError("secret-shaped scenario was serialized")
    assert secret_artifacts.runs == {}

    class BlockingActivationStore(DeterministicDurableStore):
        def __init__(self) -> None:
            super().__init__()
            self.calls = 0
            self.calls_lock = threading.Lock()
            self.first_entered = threading.Event()
            self.second_entered = threading.Event()
            self.release_first = threading.Event()

        def persist_run_activation(self, run_id: str, started_ns: int, deadline_ns: int) -> None:
            with self.calls_lock:
                self.calls += 1
                call = self.calls
            if call == 1:
                self.first_entered.set()
                if not self.release_first.wait(2):
                    raise RuntimeError("audit first admission was not released")
            else:
                self.second_entered.set()
            super().persist_run_activation(run_id, started_ns, deadline_ns)

    admission_clock = ManualClock()
    admission_adapter = FakeAdapter(admission_clock)
    admission_store = BlockingActivationStore()
    admission = MutationCoordinator(admission_adapter, admission_store, admission_clock, backend_epoch="audit-admission")
    admission_successes: list[str] = []
    admission_errors: list[str] = []

    def start_admission(run_id: str) -> None:
        try:
            admission_successes.append(admission.start_run(run_id, audit_budget()).run_id)
        except ValidationError as exc:
            admission_errors.append(exc.code)

    first = threading.Thread(target=start_admission, args=("audit-run-a",))
    second = threading.Thread(target=start_admission, args=("audit-run-b",))
    first.start()
    assert admission_store.first_entered.wait(2)
    second.start()
    assert not admission_store.second_entered.wait(0.1)
    admission_store.release_first.set()
    first.join(2)
    second.join(2)
    assert not first.is_alive() and not second.is_alive()
    assert len(admission_successes) == 1
    assert admission_errors == ["REFUSED_MUTATION_RUN_CONFLICT"]
    assert admission_store.calls == 1

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


    _, cleanup_adapter, _, cleanup_coordinator = stack(epoch="audit-cleanup-overlap")
    cleanup_started = threading.Event()
    cleanup_release = threading.Event()
    cleanup_original = cleanup_adapter.emergency_stop
    cleanup_results: list[bool] = []

    def blocking_cleanup(reason: str = "STOP"):
        cleanup_started.set()
        if not cleanup_release.wait(2):
            raise RuntimeError("audit cleanup was not released")
        return cleanup_original(reason)

    cleanup_adapter.emergency_stop = blocking_cleanup
    cleanup_worker = threading.Thread(target=lambda: cleanup_results.append(cleanup_coordinator.stop_all()))
    cleanup_worker.start()
    assert cleanup_started.wait(2)
    assert cleanup_coordinator.stop_cleanup_in_progress is True
    assert cleanup_coordinator.reset_stop() is False
    assert cleanup_coordinator.mutation_admission_allowed() is False
    assert cleanup_coordinator.clean_shutdown() is False
    cleanup_release.set()
    cleanup_worker.join(2)
    assert not cleanup_worker.is_alive()
    assert cleanup_results == [True]
    assert cleanup_coordinator.stop_cleanup_in_progress is False

    _, hook_adapter, hook_store, hook_coordinator = stack(epoch="audit-hook-stop")
    hook_request = request_for(hook_coordinator, hook_adapter, "audit-hook-stop-action")

    def stop_from_final_hook() -> None:
        assert hook_coordinator.stop_all(reason_code="AUDIT_HOOK_STOP") is True

    hook_result = hook_coordinator.execute_action(hook_request, final_commit_check=stop_from_final_hook)
    assert hook_result.status == ActionStatus.REFUSED
    assert hook_result.dispatch_state == DispatchState.NOT_DISPATCHED
    assert hook_adapter.physical_effects == []
    assert hook_store.load_control_state().stop_latched is True

    _, hash_adapter, _, hash_coordinator = stack(epoch="audit-hash-guard")
    first_hash_request = request_for(hash_coordinator, hash_adapter, "audit-hash-action")
    assert hash_coordinator.execute_action(first_hash_request).status == ActionStatus.PASS
    changed = {"direction": "SOUTH", "tiles": 1}
    forged = ActionRequest(
        action_id=first_hash_request.action_id,
        run_id=first_hash_request.run_id,
        step_id=first_hash_request.step_id,
        attempt_index=first_hash_request.attempt_index,
        kind=first_hash_request.kind,
        parameters=changed,
        timeout_ms=first_hash_request.timeout_ms,
        required_capability=first_hash_request.required_capability,
        required_authority=first_hash_request.required_authority,
        dispatch_fence=first_hash_request.dispatch_fence,
        effect_bound=hash_adapter.effect_bound(first_hash_request.kind, changed),
        action_request_hash=first_hash_request.action_request_hash,
    )
    forged_result = hash_coordinator.execute_action(forged)
    assert forged_result.status == ActionStatus.REFUSED
    assert forged_result.reason_code == "REFUSED_IDEMPOTENCY_CONFLICT"

    metadata_scenario = parse_and_validate(abort_scenario())
    metadata_artifacts = ArtifactStore()
    try:
        metadata_artifacts.create_run(
            run_id="audit-metadata-privacy",
            scenario_id=metadata_scenario.scenario_id,
            scenario_hash=metadata_scenario.scenario_hash,
            scenario_ast=metadata_scenario.ast,
            adapter_identity={
                "adapter_id": "PASSWORD=hunter2",
                "adapter_kind": "fake",
                "adapter_version": "1",
                "adapter_generation": "generation-1",
                "runtime_instance_id": "runtime-1",
                "session_epoch": "session-1",
            },
            backend_epoch="audit-metadata-backend",
            initial_control_generation=0,
            started_monotonic_ns=0,
            privacy_policy=metadata_scenario.ast["privacy_policy"],
        )
    except PrivacyError:
        pass
    else:
        raise AssertionError("secret-shaped artifact metadata was serialized")
    assert metadata_artifacts.runs == {}
    print("STOP_CLEANUP_RESET_OVERLAP_FENCE=PASS")
    print("POST_FINAL_HOOK_DISPATCH_RECHECK=PASS")
    print("CANONICAL_ACTION_HASH_GUARD=PASS")
    print("ARTIFACT_METADATA_PRIVACY_GATE=PASS")

    print("PACKAGE_A_CODEX_P1_AUDIT=PASS")
    print("FAILED_STOP_RESET_FENCE=PASS")
    print("FINAL_GATE_ABORT_REVALIDATION=PASS")
    print("CALLBACK_IDENTITY_TERMINAL_FENCE=PASS")
    print("CLEAN_SHUTDOWN_INFLIGHT_FENCE=PASS")
    print("MUTATION_RUN_ADMISSION_SERIALIZATION=PASS")
    print("FAILED_STOP_CLEANUP=PASS")
    print("CALLBACK_RECONCILIATION_SERIALIZATION=PASS")
    print("SCENARIO_ARTIFACT_PRIVACY_GATE=PASS")
    print("FINAL_GATE_ABORT_REASON=PASS")


if __name__ == "__main__":
    main()
