"""Offline vertical-slice proof for the local agent foundation.

Every effect-capable check uses the real Control Center coordinator/store and
the real guarded named-action path.  The adapter, vision provider and
executor in this file are deliberately test-only fakes; this script never
contacts Ollama, an Official client, a GUI, a process, or a network.
"""

from __future__ import annotations

import hashlib
import sys
import tempfile
import threading
from dataclasses import asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.tibia_re_control_center import agent_reconcile as reconcile_module
from tools.tibia_re_control_center.agent_protocol import (
    AgentProvenance,
    AgentVisualState,
    ClientIdentity,
    NamedAgentAction,
    OwnerControlCommand,
    TaskEnvelope,
)
from tools.tibia_re_control_center.agent_reconcile import (
    ReconciledState,
    RuntimeEvidenceClass,
    RuntimeObservation,
)
from tools.tibia_re_control_center.agent_session import (
    AgentActionReceipt,
    AgentSessionCoordinator,
    CaptureReceipt,
    GuardedActionBinding,
    GuardedMutationActionExecutor,
)
from tools.tibia_re_control_center.agent_vision import (
    AgentVisionSensor,
    ModelSlotScheduler,
    ModelSlotUnavailable,
    QWEN_NUM_CTX,
    QWEN_NUM_PREDICT,
    QWEN_TEMPERATURE,
    QWEN_VISION_DIGEST,
    QWEN_VISION_MODEL,
    QWEN_VISION_PROFILE_ID,
    SecretSafeCapture,
)
from tools.tibia_re_control_center.execution import MutationCoordinator
from tools.tibia_re_control_center.fake import FakeAdapter, ManualClock
from tools.tibia_re_control_center.model import EffectBound, PrivacyError
from tools.tibia_re_control_center.persistent_store import SQLitePersistentStore
from tools.tibia_re_vision.evidence import UnsafeInputError


class _TestExecutor:
    """Test-only read/capture adapter; never a production executor."""

    def __init__(self) -> None:
        self.execute_calls: list[object] = []
        self.screenshot_calls: list[tuple[str, str]] = []
        self.capture = CaptureReceipt("CAPTURED", "capture-safe", "c" * 64, True)

    def execute(self, request: object) -> AgentActionReceipt:
        self.execute_calls.append(request)
        request_id = getattr(request, "action_id", "test-action")
        return AgentActionReceipt(request_id, "PERFORMED", True, True, 1, ("effect-safe",))

    def screenshot(self, session_id: str, run_id: str) -> CaptureReceipt:
        self.screenshot_calls.append((session_id, run_id))
        return self.capture


class _VisionFixture:
    """A deterministic provider fixture with the real scheduler/sensor."""

    def __init__(self, screen_class: str) -> None:
        self.screen_class = screen_class
        self.resident: list[str] = []
        self.provider_calls: list[dict[str, object]] = []
        self.unload_calls: list[str] = []
        self.scheduler = ModelSlotScheduler(
            ps=lambda: list(self.resident),
            digest=lambda _model: QWEN_VISION_DIGEST,
            infer=self._infer,
            unload=self._unload,
        )

    def _infer(
        self,
        model: str,
        image_path: str | Path,
        _prompt: str,
        *,
        evidence_ref: str,
        capture_sha256: str,
        model_profile_id: str,
        source_monotonic_ns: int | None,
        keep_alive: str,
        num_ctx: int,
        num_predict: int,
    ) -> dict[str, object]:
        self.provider_calls.append({
            "model": model,
            "image_path": image_path,
            "evidence_ref": evidence_ref,
            "capture_sha256": capture_sha256,
            "model_profile_id": model_profile_id,
            "source_monotonic_ns": source_monotonic_ns,
            "keep_alive": keep_alive,
            "num_ctx": num_ctx,
            "num_predict": num_predict,
        })
        self.resident[:] = [model]
        return {
            "schema_version": 1,
            "capture": {
                "evidence_ref": evidence_ref,
                "sha256": capture_sha256,
                "source_monotonic_ns": source_monotonic_ns,
            },
            "model": {"model_profile_id": model_profile_id},
            "observation": {
                "screen_class": self.screen_class,
                "visible_text": ["synthetic fixture"],
                "ui_objects": [],
                "appeared": [],
                "disappeared": [],
                "changed": [],
            },
            "quality": {
                "schema_valid": True,
                "visual_only": True,
                "structural_authority": False,
                "unknown_fields": [],
            },
        }

    def _unload(self, model: str) -> None:
        self.unload_calls.append(model)
        self.resident.clear()

    def observe(self, root: Path, *, run_id: str, evidence_ref: str) -> Any:
        path = root / f"{evidence_ref.replace(':', '-')}.png"
        payload = b"synthetic secret-safe capture"
        path.write_bytes(payload)
        path.chmod(0o400)
        capture = SecretSafeCapture(
            run_id=run_id,
            evidence_ref=evidence_ref,
            path=path,
            sha256=hashlib.sha256(payload).hexdigest(),
            secret_safe=True,
            source_monotonic_ns=0,
        )
        return AgentVisionSensor(self.scheduler).observe(capture)


def _task(session_id: str, run_id: str, *, actions: tuple[NamedAgentAction, ...]) -> TaskEnvelope:
    return TaskEnvelope(
        schema="otclient.local-agent.task.v1",
        session_id=session_id,
        task_id=f"task-{session_id}",
        run_id=run_id,
        idempotency_key=f"idem-{session_id}",
        trusted_main_sha="a" * 40,
        client_identity=ClientIdentity("NOT_APPLICABLE", "NOT_APPLICABLE", "b" * 64),
        objective="bounded offline agent fixture",
        allowed_actions=actions,
        physical_action_budget=1,
        max_attempts=2,
        deadline_epoch_ms=4_000_000_000_000,
        runtime_access="none",
        required_evidence=("secret-safe fixture",),
        secret_capability_ref=None,
    )


def _stack(root: Path, *, session_id: str, run_id: str) -> tuple[
    SQLitePersistentStore,
    FakeAdapter,
    MutationCoordinator,
    _TestExecutor,
    AgentSessionCoordinator,
]:
    clock = ManualClock()
    adapter = FakeAdapter(clock, allow_mutation=True)
    adapter.add_capability("agent.enter_world", read=False, action=True)
    adapter.set_effect_bound("agent_enter_world", EffectBound(max_actions=1))
    store = SQLitePersistentStore(root)
    control = MutationCoordinator(adapter, store, clock, backend_epoch=f"backend-{session_id}")
    guarded = GuardedMutationActionExecutor(
        control,
        bindings={
            NamedAgentAction.ENTER_WORLD: GuardedActionBinding(
                kind="agent_enter_world",
                parameters={},
                required_capability="agent.enter_world",
                timeout_ms=1_000,
            ),
        },
        source_state_provider=lambda _request: "CHARACTER_SELECT",
    )
    executor = _TestExecutor()
    agent = AgentSessionCoordinator(store, control, executor, guarded_executor=guarded)
    agent._now_epoch_ms = lambda: 1_000_000
    accepted = agent.submit_task(_task(
        session_id,
        run_id,
        actions=(NamedAgentAction.ENTER_WORLD, NamedAgentAction.SCREENSHOT),
    ), operation_id=f"accept-{session_id}")
    assert accepted["accepted_new"] is True
    assert accepted["envelope"]["runtime_access"] == "none"
    return store, adapter, control, executor, agent


def _close(
    store: SQLitePersistentStore,
    control: MutationCoordinator,
    *,
    allow_inconclusive: bool = False,
) -> None:
    clean = control.clean_shutdown()
    if not clean and not allow_inconclusive:
        raise AssertionError("offline foundation stack did not cleanly shut down")
    store.close()


def _propose(agent: AgentSessionCoordinator, session_id: str, action_id: str) -> AgentActionReceipt:
    return agent.propose_named_action(
        session_id,
        action_id,
        NamedAgentAction.ENTER_WORLD,
        provenance=AgentProvenance.SUPERVISOR,
        expected_source_states=("CHARACTER_SELECT",),
        current_state="CHARACTER_SELECT",
    )


def _trusted_context(runtime: RuntimeObservation) -> reconcile_module._ResolverStateSnapshot:
    return reconcile_module._ResolverStateSnapshot(
        current_session_id="session-c",
        current_run_id="run-c",
        current_runtime_id="fake-runtime",
        current_runtime_instance_id="instance-c",
        current_monotonic_ns=1_000,
        max_age_ns=100,
        reviewed_producers=(
            reconcile_module._ReviewedProducerContract("fake-producer", "runtime-state-v1"),
        ),
        runtime_evidence=reconcile_module._RuntimeEvidenceRecord(
            observation=runtime,
            session_id="session-c",
            run_id="run-c",
            runtime_id="fake-runtime",
            runtime_instance_id="instance-c",
            producer_id="fake-producer",
            producer_contract_id="runtime-state-v1",
            observed_monotonic_ns=950,
        ),
    )


class _TrustedRuntimeResolver:
    def __init__(self, context: reconcile_module._ResolverStateSnapshot) -> None:
        self.context = context

    def resolve_current_reviewed(self, runtime: RuntimeObservation) -> RuntimeObservation | None:
        if reconcile_module._resolver_state_matches_runtime(runtime, self.context):
            return runtime
        return None


def _vision(root: Path, screen_class: str, *, run_id: str, evidence_ref: str) -> Any:
    return _VisionFixture(screen_class).observe(root, run_id=run_id, evidence_ref=evidence_ref)


def scenario_a_safe_login_evidence() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        store, adapter, control, _executor, agent = _stack(root, session_id="a", run_id="run-a")
        try:
            accepted_events = [
                event for event in agent.snapshot("a")["events"]
                if event.get("kind") == "TASK_ACCEPTED"
            ]
            assert len(accepted_events) == 1
            assert accepted_events[0]["provenance"] == "SUPERVISOR"
            visual = _vision(root, "LOGIN_SCREEN", run_id="run-a", evidence_ref="capture-a")
            runtime = RuntimeObservation("UNKNOWN", RuntimeEvidenceClass.UNKNOWN, ())
            result = reconcile_module.reconcile_state(visual, runtime)
            assert result.state is ReconciledState.LOGIN_SCREEN
            capture = agent.owner_control("a", OwnerControlCommand.SCREENSHOT)
            assert capture["status"] == "CAPTURED"
            completed = agent.complete_run(
                "a",
                status="PASS",
                final_state=AgentVisualState.LOGIN_SCREEN.value,
                evidence_manifest_sha256="d" * 64,
            )
            assert completed.status.value == "PASS"
            assert completed.evidence_manifest_sha256 == "d" * 64
            assert adapter.physical_effects == []
        finally:
            _close(store, control)


def scenario_b_visual_never_promotes_world() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        visual = _vision(root, "IN_GAME_VISUAL", run_id="run-b", evidence_ref="capture-b")
        result = reconcile_module.reconcile_state(
            visual,
            RuntimeObservation("UNKNOWN", RuntimeEvidenceClass.UNKNOWN, ()),
        )
        assert result.state is ReconciledState.UNKNOWN
        assert result.state is not ReconciledState.WORLD_CONFIRMED


def scenario_c_reviewed_runtime_conflicts_with_login_visual() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        visual = _vision(root, "LOGIN_SCREEN", run_id="run-c", evidence_ref="capture-c")
        runtime = RuntimeObservation("IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime-c",))
        context = _trusted_context(runtime)
        reconciler = reconcile_module._compose_trusted_reconciler(_TrustedRuntimeResolver(context))
        result = reconciler.reconcile_state(visual, runtime)
        assert result.state is ReconciledState.CONFLICT


def scenario_d_pause_dominates_proposal() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        store, adapter, control, _executor, agent = _stack(root, session_id="d", run_id="run-d")
        try:
            paused = agent.owner_control("d", OwnerControlCommand.PAUSE)
            assert paused["status"] == "PAUSED"
            receipt = _propose(agent, "d", "action-d")
            assert receipt.status == "REFUSED_OWNER_PAUSED"
            assert adapter.physical_effects == []
        finally:
            _close(store, control, allow_inconclusive=True)


def scenario_e_stop_before_fake_commit() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        store, adapter, control, _executor, agent = _stack(root, session_id="e", run_id="run-e")
        entered = threading.Event()
        release = threading.Event()
        adapter.authority_wait_hook = lambda: (entered.set(), release.wait(timeout=2))
        receipts: list[AgentActionReceipt] = []
        action_thread = threading.Thread(target=lambda: receipts.append(_propose(agent, "e", "action-e")))
        action_thread.start()
        try:
            assert entered.wait(timeout=1)
            stopped = agent.owner_control("e", OwnerControlCommand.STOP)
            assert stopped["status"] == "STOPPED"
            release.set()
            action_thread.join(timeout=2)
            assert not action_thread.is_alive()
            assert receipts and receipts[0].status == "NOT_PERFORMED"
            assert adapter.physical_effects == []
        finally:
            release.set()
            action_thread.join(timeout=2)
            _close(store, control)


def scenario_f_idempotent_task_and_action() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        store, adapter, control, _executor, agent = _stack(root, session_id="f", run_id="run-f")
        try:
            accepted = _task("f", "run-f", actions=(NamedAgentAction.ENTER_WORLD, NamedAgentAction.SCREENSHOT))
            first_task = agent.submit_task(accepted, operation_id="task-f-idempotent")
            second_task = agent.submit_task(accepted, operation_id="task-f-idempotent")
            assert first_task == second_task
            first = _propose(agent, "f", "action-f")
            second = _propose(agent, "f", "action-f")
            assert first.status == "PERFORMED"
            assert second.status == "PERFORMED"
            assert len(adapter.physical_effects) == 1
        finally:
            _close(store, control)


def scenario_g_performed_unknown_never_replays() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        store, adapter, control, _executor, agent = _stack(root, session_id="g", run_id="run-g")
        try:
            store.inject_fault("reconcile", "error")
            first = _propose(agent, "g", "action-g")
            assert first.status == "PERFORMED_UNKNOWN"
            assert first.performed is True and first.outcome_known is False
            assert len(adapter.physical_effects) == 1
            assert agent.snapshot("g")["run_status"] == "INCONCLUSIVE"
            store.clear_faults()
            replay = _propose(agent, "g", "action-g")
            assert replay.status == "PERFORMED_UNKNOWN"
            assert len(adapter.physical_effects) == 1
        finally:
            _close(store, control, allow_inconclusive=True)


def scenario_h_restart_preserves_owner_latches() -> None:
    for suffix, command, expected in (
        ("pause", OwnerControlCommand.PAUSE, "PAUSED"),
        ("stop", OwnerControlCommand.STOP, "STOPPED"),
    ):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            store, _adapter, control, _executor, agent = _stack(root, session_id=suffix, run_id=f"run-{suffix}")
            try:
                assert agent.owner_control(suffix, command)["status"] == expected
                _close(store, control)
                store = SQLitePersistentStore(root)
                clock = ManualClock()
                adapter = FakeAdapter(clock, allow_mutation=True)
                restarted_control = MutationCoordinator(adapter, store, clock, backend_epoch=f"restart-{suffix}")
                restarted = AgentSessionCoordinator(store, restarted_control)
                session = restarted.ensure_session(suffix)
                assert session.operational_state.value == expected
                if command is OwnerControlCommand.PAUSE:
                    assert session.pause_latched is True and session.stop_latched is False
                else:
                    assert session.stop_latched is True
                assert session.operational_state.value != "RUNNING"
                _close(store, restarted_control)
                store = None  # type: ignore[assignment]
            finally:
                if store is not None:
                    store.close()


def scenario_i_foreign_model_waits_without_eviction() -> None:
    resident = ["foreign:model"]
    unloads: list[str] = []
    inference_calls: list[str] = []
    scheduler = ModelSlotScheduler(
        ps=lambda: list(resident),
        digest=lambda _model: QWEN_VISION_DIGEST,
        infer=lambda model, *_args, **_kwargs: inference_calls.append(model),
        unload=lambda model: unloads.append(model),
    )
    try:
        scheduler.infer(
            model=QWEN_VISION_MODEL,
            expected_digest=QWEN_VISION_DIGEST,
            image_path=Path("not-read"),
            evidence_ref="capture-i",
            capture_sha256="a" * 64,
            model_profile_id=QWEN_VISION_PROFILE_ID,
            source_monotonic_ns=0,
            keep_alive="0s",
            num_ctx=QWEN_NUM_CTX,
            num_predict=QWEN_NUM_PREDICT,
        )
    except ModelSlotUnavailable as exc:
        assert exc.code == "DIFFERENT_RESIDENT_MODEL"
    else:
        raise AssertionError("foreign model residency was admitted")
    assert unloads == [] and inference_calls == [] and resident == ["foreign:model"]


def scenario_j_secret_boundaries() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        store, _adapter, control, executor, agent = _stack(root, session_id="j", run_id="run-j")
        try:
            unsafe = _task("secret-task", "secret-run", actions=(NamedAgentAction.SCREENSHOT,))
            unsafe = unsafe.__class__(**{
                **asdict(unsafe),
                "objective": "PASSWORD=hunter2",
            })
            try:
                agent.submit_task(unsafe, operation_id="secret-task-op")
            except PrivacyError:
                pass
            else:
                raise AssertionError("secret-bearing task reached persistence")
            assert store.load_agent_session("secret-task") is None
            before_events = len(agent.snapshot("j")["events"])
            try:
                agent.record_message("j", AgentProvenance.OWNER, "token=hunter2")
            except PrivacyError:
                pass
            else:
                raise AssertionError("secret-bearing chat reached persistence")
            assert len(agent.snapshot("j")["events"]) == before_events

            fixture = _VisionFixture("LOGIN_SCREEN")
            capture_path = root / "unsafe-capture.png"
            capture_path.write_bytes(b"unsafe")
            capture = SecretSafeCapture(
                run_id="run-j",
                evidence_ref="capture-j-unsafe",
                path=capture_path,
                sha256=hashlib.sha256(b"unsafe").hexdigest(),
                secret_safe=False,
                source_monotonic_ns=0,
            )
            try:
                AgentVisionSensor(fixture.scheduler).observe(capture)
            except UnsafeInputError:
                pass
            else:
                raise AssertionError("unsafe capture reached provider")
            assert fixture.provider_calls == []
            assert executor.execute_calls == []
        finally:
            _close(store, control)


def main() -> int:
    scenario_a_safe_login_evidence()
    scenario_b_visual_never_promotes_world()
    scenario_c_reviewed_runtime_conflicts_with_login_visual()
    scenario_d_pause_dominates_proposal()
    scenario_e_stop_before_fake_commit()
    scenario_f_idempotent_task_and_action()
    scenario_g_performed_unknown_never_replays()
    scenario_h_restart_preserves_owner_latches()
    scenario_i_foreign_model_waits_without_eviction()
    scenario_j_secret_boundaries()
    print("AGENT_FOUNDATION_E2E=PASS")
    print("OFFICIAL_RUNTIME_ACCESS=NONE")
    print("PHYSICAL_EFFECTS=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
