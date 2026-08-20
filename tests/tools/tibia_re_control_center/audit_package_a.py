from __future__ import annotations

import ast
import json
from pathlib import Path

from tools.tibia_re_control_center.artifact import ArtifactStore
from tools.tibia_re_control_center.engine import ScenarioEngine
from tools.tibia_re_control_center.execution import MutationCoordinator
from tools.tibia_re_control_center.fake import FakeAdapter, ManualClock
from tools.tibia_re_control_center.model import (
    ActionRequest,
    ActionStatus,
    Authority,
    DispatchFence,
    DispatchState,
    PrivacyError,
    SideEffectBudget,
)
from tools.tibia_re_control_center.recorder import Recorder
from tools.tibia_re_control_center.scenario import action_request_hash, parse_and_validate
from tools.tibia_re_control_center.store import DeterministicDurableStore


def hard_budget() -> SideEffectBudget:
    return SideEffectBudget(10, 4, 4, 0, 0, 0, 0, 0, 0)


def make_stack(*, store: DeterministicDurableStore | None = None, epoch: str = "audit-one"):
    clock = ManualClock()
    adapter = FakeAdapter(clock)
    adapter.add_capability("move")
    durable = store or DeterministicDurableStore()
    coordinator = MutationCoordinator(adapter, durable, clock, backend_epoch=epoch)
    coordinator.start_run("audit-run", hard_budget())
    return clock, adapter, durable, coordinator


def make_request(coordinator: MutationCoordinator, adapter: FakeAdapter, action_id: str = "audit-action") -> ActionRequest:
    parameters = {"direction": "NORTH", "tiles": 1}
    identity = adapter.identity()
    request_hash = action_request_hash(
        schema_version=1,
        run_id="audit-run",
        step_id="audit-step",
        attempt_index=1,
        kind="move",
        parameters=parameters,
        timeout_ms=1000,
        required_capability="move",
        required_authority=Authority.MUTATION,
    )
    return ActionRequest(
        action_id=action_id,
        run_id="audit-run",
        step_id="audit-step",
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


def scenario_json() -> str:
    return json.dumps({
        "schema_version": 1,
        "id": "audit-scenario",
        "name": "Fresh validator scenario",
        "adapter_requirements": {"reads": [], "actions": ["move"]},
        "preconditions": [],
        "side_effect_budget": hard_budget().as_dict(),
        "capture_policy": {"state": True, "events": True, "screenshots": "NONE", "network": "NONE", "traces": "NONE"},
        "steps": [{"action": {"kind": "move", "parameters": {"direction": "NORTH", "tiles": 1}, "timeout_ms": 1000}}],
        "abort_conditions": [],
        "expected_result": [],
        "privacy_policy": {"secret_material": "REJECT", "private_chat": "OMIT", "identities": "OMIT", "screenshots": "SAFE_ONLY"},
    })


def audit_runtime_boundary() -> None:
    forbidden_modules = {
        "socket", "subprocess", "requests", "httpx", "urllib.request",
        "selenium", "playwright", "docker", "paramiko",
    }
    forbidden_calls = {"system", "popen", "Popen", "exec", "eval"}
    violations: list[str] = []
    for path in sorted(Path("tools/tibia_re_control_center").glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in forbidden_modules:
                        violations.append(f"{path}:{node.lineno}:import {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module in forbidden_modules:
                violations.append(f"{path}:{node.lineno}:from {node.module}")
            elif isinstance(node, ast.Call):
                name = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
                if name in forbidden_calls:
                    violations.append(f"{path}:{node.lineno}:call {name}")
    if violations:
        raise AssertionError("runtime_access:none violation(s): " + "; ".join(violations))


def main() -> None:
    audit_runtime_boundary()

    _, adapter, _, coordinator = make_stack()
    adapter.before_commit_hook = coordinator.stop_all
    stopped = coordinator.execute_action(make_request(coordinator, adapter))
    assert stopped.dispatch_state == DispatchState.NOT_DISPATCHED
    assert adapter.physical_effects == []

    _, adapter, store, coordinator = make_stack()
    store.inject_fault("dispatch_commit", "error")
    failed_commit = coordinator.execute_action(make_request(coordinator, adapter))
    assert failed_commit.dispatch_state == DispatchState.NOT_DISPATCHED
    assert adapter.physical_effects == []

    clock, _, store, first = make_stack(epoch="audit-old")
    first.finish_run("audit-run")
    second = MutationCoordinator(FakeAdapter(clock), store, clock, backend_epoch="audit-new")
    assert second.control_state.recovery_required is True
    assert second.mutation_admission_allowed() is False

    recorder = Recorder(ManualClock(), backend_epoch="audit", adapter_id="fake", adapter_generation="g")
    try:
        recorder.record_event(kind="ERROR", payload={"access_token": "secret"})
    except PrivacyError:
        pass
    else:
        raise AssertionError("secret-shaped event reached ordinary recorder")

    scenario = parse_and_validate(scenario_json())
    clock = ManualClock()
    adapter = FakeAdapter(clock)
    adapter.add_capability("move")
    store = DeterministicDurableStore()
    coordinator = MutationCoordinator(adapter, store, clock, backend_epoch="audit-e2e")
    recorder = Recorder(clock, backend_epoch=coordinator.backend_epoch, adapter_id="fake", adapter_generation=adapter.identity().adapter_generation)
    result = ScenarioEngine(
        adapter=adapter,
        coordinator=coordinator,
        artifacts=ArtifactStore(),
        recorder=recorder,
    ).run(scenario, run_id="audit-e2e-run")
    assert result.status == "PASS"
    assert len(adapter.physical_effects) == 1
    assert next(iter(result.action_results.values())).status == ActionStatus.PASS

    print("PACKAGE_A_FRESH_AUDIT=PASS")
    print("MATERIAL_FINDINGS_OPEN=0")
    print("RUNTIME_ACCESS_NONE=PASS")
    print("FAKE_ONE_STEP_E2E=PASS")


if __name__ == "__main__":
    main()
