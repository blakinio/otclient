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
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.tibia_re_control_center import agent_reconcile as reconcile_module
from tools.tibia_re_control_center.agent_protocol import (
    AgentOperationalState,
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
    QWEN_VISION_DIGEST,
    QWEN_VISION_MODEL,
    AgentVisionSensor,
    ModelSlotScheduler,
    ModelSlotUnavailable,
    SecretSafeCapture,
)
from tools.tibia_re_control_center.control_api import ControlApiServer
from tools.tibia_re_control_center.control_cli import (
    ControlApiClient,
    ControlClientError,
)
from tools.tibia_re_control_center.control_domain import ControlDomainService
from tools.tibia_re_control_center.model import EffectBound, PrivacyError
from tools.tibia_re_vision.evidence import UnsafeInputError


class _TestExecutor:
    """Test-only read/capture adapter; never a production executor."""

    def __init__(self, *, performed_unknown: bool = False) -> None:
        self.performed_unknown = performed_unknown
        self.execute_calls: list[object] = []
        self.screenshot_calls: list[tuple[str, str]] = []
        self.capture = CaptureReceipt("CAPTURED", "capture-safe", "c" * 64, True)

    def execute(self, request: object) -> AgentActionReceipt:
        self.execute_calls.append(request)
        request_id = getattr(request, "action_id", "test-action")
        if self.performed_unknown:
            return AgentActionReceipt(request_id, "PERFORMED_UNKNOWN", True, False, 1, ())
        return AgentActionReceipt(request_id, "PERFORMED", True, True, 1, ("effect-safe",))

    def execute_guarded(
        self,
        delegated: object,
        request: object,
        *,
        token: object,
        final_commit_check: object,
    ) -> AgentActionReceipt:
        self.execute_calls.append(request)
        receipt = delegated(
            request,
            token=token,
            final_commit_check=final_commit_check,
        )
        if self.performed_unknown:
            return AgentActionReceipt(
                getattr(request, "action_id", "test-action"),
                "PERFORMED_UNKNOWN",
                True,
                False,
                receipt.low_level_event_count,
                receipt.evidence_refs,
            )
        return receipt

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


def _stack(
    root: Path,
    *,
    session_id: str,
    run_id: str,
    submit: bool = True,
    performed_unknown: bool = False,
) -> _ApiStack:
    domain = ControlDomainService(root, backend_epoch=f"backend-{session_id}")
    adapter = domain.adapter
    adapter.add_capability("agent.enter_world", read=False, action=True)
    adapter.set_effect_bound("agent_enter_world", EffectBound(max_actions=1))
    guarded = GuardedMutationActionExecutor(
        domain.coordinator,
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
    executor = _TestExecutor(performed_unknown=performed_unknown)
    domain.agent.executor = executor
    domain.agent.guarded_executor = guarded
    if performed_unknown:
        original_execute_committed = adapter.execute_committed

        def uncertain_execute_committed(request: object, commit_dispatch: object) -> dict[str, object]:
            execution = original_execute_committed(request, commit_dispatch)
            if execution.get("committed"):
                execution = dict(execution)
                execution.update({
                    "outcome": "ambiguous",
                    "reason_code": "TEST_EXECUTOR_PERFORMED_UNKNOWN",
                })
            return execution

        adapter.execute_committed = uncertain_execute_committed  # type: ignore[method-assign]

        original_guarded_execute = guarded.execute_guarded

        def fake_guarded_execute(request: object, *, token: object, final_commit_check: object) -> AgentActionReceipt:
            return executor.execute_guarded(
                original_guarded_execute,
                request,
                token=token,
                final_commit_check=final_commit_check,
            )

        guarded.execute_guarded = fake_guarded_execute  # type: ignore[method-assign]
    server = ControlApiServer(root, domain=domain).start()
    stack = _ApiStack(server, executor)
    if submit:
        accepted = stack.client.post(
            "/v1/agent/tasks",
            _task_body(_task(
                session_id,
                run_id,
                actions=(NamedAgentAction.ENTER_WORLD, NamedAgentAction.SCREENSHOT),
            )),
            request_id=f"accept-{session_id}",
        )
        assert accepted["accepted_new"] is True
        assert accepted["session"]["runtime_access"] == "none"
    return stack


def _close(stack: _ApiStack, *, allow_inconclusive: bool = False) -> None:
    clean = stack.server.close()
    if not clean and not allow_inconclusive:
        raise AssertionError("offline foundation stack did not cleanly shut down")


def _propose(agent: AgentSessionCoordinator, session_id: str, action_id: str) -> AgentActionReceipt:
    return agent.propose_named_action(
        session_id,
        action_id,
        NamedAgentAction.ENTER_WORLD,
        provenance=AgentProvenance.SUPERVISOR,
        expected_source_states=("CHARACTER_SELECT",),
        current_state="CHARACTER_SELECT",
    )


class _TrustedRuntimeFixture:
    """Test-only reviewed runtime producer for the existing trusted seam."""

    def __init__(self, runtime: RuntimeObservation) -> None:
        self.runtime = runtime

    def resolve_current_reviewed(self, runtime: RuntimeObservation) -> RuntimeObservation | None:
        if runtime == self.runtime:
            return runtime
        return None


@dataclass
class _ApiStack:
    server: ControlApiServer
    executor: _TestExecutor

    @property
    def client(self) -> ControlApiClient:
        return ControlApiClient(self.server.data_root)

    @property
    def domain(self) -> ControlDomainService:
        return self.server.domain

    @property
    def adapter(self) -> Any:
        return self.domain.adapter

    @property
    def store(self) -> Any:
        return self.domain.store

    @property
    def control(self) -> Any:
        return self.domain.coordinator

    @property
    def agent(self) -> AgentSessionCoordinator:
        return self.domain.agent


def _task_body(task: TaskEnvelope) -> dict[str, object]:
    body = asdict(task)
    body["client_identity"] = asdict(task.client_identity)
    body["allowed_actions"] = [action.value for action in task.allowed_actions]
    body["required_evidence"] = list(task.required_evidence)
    return body


def _vision(root: Path, screen_class: str, *, run_id: str, evidence_ref: str) -> Any:
    return _VisionFixture(screen_class).observe(root, run_id=run_id, evidence_ref=evidence_ref)


def _safe_capture(root: Path, *, run_id: str, evidence_ref: str) -> SecretSafeCapture:
    path = root / f"{evidence_ref.replace(':', '-')}.png"
    payload = b"synthetic secret-safe capture"
    path.write_bytes(payload)
    path.chmod(0o400)
    return SecretSafeCapture(
        run_id=run_id,
        evidence_ref=evidence_ref,
        path=path,
        sha256=hashlib.sha256(payload).hexdigest(),
        secret_safe=True,
        source_monotonic_ns=0,
    )


def scenario_a_safe_login_evidence() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        stack = _stack(root, session_id="a", run_id="run-a")
        try:
            accepted_events = [
                event for event in stack.client.get("/v1/agent/session?session_id=a")["events"]
                if event.get("kind") == "TASK_ACCEPTED"
            ]
            assert len(accepted_events) == 1
            assert accepted_events[0]["provenance"] == "SUPERVISOR"
            visual = _vision(root, "LOGIN_SCREEN", run_id="run-a", evidence_ref="capture-a")
            runtime = RuntimeObservation("UNKNOWN", RuntimeEvidenceClass.UNKNOWN, ())
            result = reconcile_module.reconcile_state(visual, runtime)
            assert result.state is ReconciledState.LOGIN_SCREEN
            capture = stack.client.post(
                "/v1/agent/control",
                {"session_id": "a", "command": OwnerControlCommand.SCREENSHOT.value},
                request_id="capture-a-control",
            )
            assert capture["status"] == "CAPTURED"
            completed = stack.agent.complete_run(
                "a",
                status="PASS",
                final_state=AgentVisualState.LOGIN_SCREEN.value,
                evidence_manifest_sha256="d" * 64,
            )
            assert completed.status.value == "PASS"
            assert completed.evidence_manifest_sha256 == "d" * 64
            api_result = stack.client.get("/v1/agent/result?run_id=run-a")
            assert api_result["status"] == "PASS"
            assert stack.adapter.physical_effects == []
        finally:
            _close(stack)


def scenario_b_visual_never_promotes_world() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        stack = _stack(root, session_id="b", run_id="run-b", submit=False)
        try:
            status = stack.client.get("/v1/status")
            assert status["official_client_access"] == "NONE"
            visual = _vision(root, "IN_GAME_VISUAL", run_id="run-b", evidence_ref="capture-b")
            result = reconcile_module.reconcile_state(
                visual,
                RuntimeObservation("UNKNOWN", RuntimeEvidenceClass.UNKNOWN, ()),
            )
            assert result.state is ReconciledState.UNKNOWN
            assert result.state is not ReconciledState.WORLD_CONFIRMED
            assert stack.adapter.physical_effects == []
        finally:
            _close(stack)


def scenario_c_reviewed_runtime_conflicts_with_login_visual() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        stack = _stack(root, session_id="c", run_id="run-c", submit=False)
        try:
            assert stack.client.get("/v1/status")["runtime"]["adapter_kind"] == "FAKE_TEST"
            visual = _vision(root, "LOGIN_SCREEN", run_id="run-c", evidence_ref="capture-c")
            runtime = RuntimeObservation("IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime-c",))
            reconciler = reconcile_module._compose_trusted_reconciler(_TrustedRuntimeFixture(runtime))
            result = reconciler.reconcile_state(visual, runtime)
            assert result.state is ReconciledState.CONFLICT
            assert stack.adapter.physical_effects == []
        finally:
            _close(stack)


def scenario_d_pause_dominates_proposal() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        stack = _stack(root, session_id="d", run_id="run-d")
        try:
            paused = stack.client.post(
                "/v1/agent/control",
                {"session_id": "d", "command": OwnerControlCommand.PAUSE.value},
                request_id="pause-d-control",
            )
            assert paused["status"] == "PAUSED"
            receipt = _propose(stack.agent, "d", "action-d")
            assert receipt.status == "REFUSED_OWNER_PAUSED"
            assert stack.adapter.physical_effects == []
        finally:
            _close(stack, allow_inconclusive=True)


def scenario_e_stop_before_fake_commit() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        stack = _stack(root, session_id="e", run_id="run-e")
        entered = threading.Event()
        release = threading.Event()
        stack.adapter.authority_wait_hook = lambda: (entered.set(), release.wait(timeout=2))
        receipts: list[AgentActionReceipt] = []
        action_thread = threading.Thread(target=lambda: receipts.append(_propose(stack.agent, "e", "action-e")))
        action_thread.start()
        try:
            assert entered.wait(timeout=1)
            stopped = stack.client.post(
                "/v1/agent/control",
                {"session_id": "e", "command": OwnerControlCommand.STOP.value},
                request_id="stop-e-control",
            )
            assert stopped["status"] == "STOPPED"
            release.set()
            action_thread.join(timeout=2)
            assert not action_thread.is_alive()
            assert receipts and receipts[0].status == "NOT_PERFORMED"
            assert stack.adapter.physical_effects == []
        finally:
            release.set()
            action_thread.join(timeout=2)
            _close(stack)


def scenario_f_idempotent_task_and_action() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        stack = _stack(root, session_id="f", run_id="run-f")
        try:
            accepted = _task("f", "run-f", actions=(NamedAgentAction.ENTER_WORLD, NamedAgentAction.SCREENSHOT))
            first_task = stack.client.post(
                "/v1/agent/tasks",
                _task_body(accepted),
                request_id="task-f-idempotent",
            )
            second_task = stack.client.post(
                "/v1/agent/tasks",
                _task_body(accepted),
                request_id="task-f-idempotent",
            )
            assert first_task == second_task
            first = _propose(stack.agent, "f", "action-f")
            second = _propose(stack.agent, "f", "action-f")
            assert first.status == "PERFORMED"
            assert second.status == "PERFORMED"
            assert len(stack.adapter.physical_effects) == 1
        finally:
            _close(stack)


def scenario_g_performed_unknown_never_replays() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        stack = _stack(root, session_id="g", run_id="run-g", performed_unknown=True)
        try:
            first = _propose(stack.agent, "g", "action-g")
            assert first.status == "PERFORMED_UNKNOWN"
            assert first.performed is True and first.outcome_known is False
            assert len(stack.adapter.physical_effects) == 1
            assert len(stack.executor.execute_calls) == 1
            assert stack.agent.snapshot("g")["run_status"] == "INCONCLUSIVE"
            replay = _propose(stack.agent, "g", "action-g")
            assert replay.status == "PERFORMED_UNKNOWN"
            assert len(stack.adapter.physical_effects) == 1
            assert len(stack.executor.execute_calls) == 1
        finally:
            _close(stack, allow_inconclusive=True)


def scenario_h_restart_preserves_owner_latches() -> None:
    for suffix, command, expected in (
        ("pause", OwnerControlCommand.PAUSE, "PAUSED"),
        ("stop", OwnerControlCommand.STOP, "STOPPED"),
    ):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = _stack(root, session_id=suffix, run_id=f"run-{suffix}")
            try:
                controlled = first.client.post(
                    "/v1/agent/control",
                    {"session_id": suffix, "command": command.value},
                    request_id=f"{suffix}-control",
                )
                assert controlled["status"] == expected
                _close(first)
                second = _stack(root, session_id=suffix, run_id=f"run-{suffix}", submit=False)
                try:
                    session = second.client.get(f"/v1/agent/session?session_id={suffix}")
                    assert session["operational_state"] == expected
                    if command is OwnerControlCommand.PAUSE:
                        assert session["pause_latched"] is True and session["stop_latched"] is False
                    else:
                        assert session["stop_latched"] is True
                    assert session["operational_state"] != "RUNNING"
                finally:
                    _close(second)
            finally:
                if not first.server._closed:
                    first.server.close()


def scenario_i_foreign_model_waits_without_eviction() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary) / "foreign"
        root.mkdir()
        stack = _stack(root, session_id="i", run_id="run-i")
        resident = ["foreign:model"]
        unloads: list[str] = []
        inference_calls: list[str] = []
        scheduler = ModelSlotScheduler(
            ps=lambda: list(resident),
            digest=lambda _model: QWEN_VISION_DIGEST,
            infer=lambda model, *_args, **_kwargs: inference_calls.append(model),
            unload=lambda model: unloads.append(model),
        )
        sensor = AgentVisionSensor(scheduler)
        observe = getattr(stack.domain, "observe_agent_vision", None)
        try:
            assert callable(observe), "ControlDomainService vision composition seam is required"
            capture = _safe_capture(root, run_id="run-i", evidence_ref="capture-i")
            try:
                observe("i", sensor, capture)
            except ModelSlotUnavailable as exc:
                assert exc.code == "DIFFERENT_RESIDENT_MODEL"
            else:
                raise AssertionError("foreign model residency was admitted")
            waiting = stack.client.get("/v1/agent/session?session_id=i")
            assert waiting["operational_state"] == AgentOperationalState.WAITING_MODEL_SLOT.value
            waiting_event = waiting["events"][-1]
            assert waiting_event["kind"] == "MODEL_SLOT_WAITING"
            assert waiting_event["provenance"] == AgentProvenance.SYSTEM.value
            assert waiting_event["payload"] == {"reason_code": "DIFFERENT_RESIDENT_MODEL"}
            assert unloads == [] and inference_calls == [] and resident == ["foreign:model"]
            assert stack.executor.execute_calls == []
            assert stack.adapter.physical_effects == []
        finally:
            _close(stack)

        restarted = _stack(root, session_id="i", run_id="run-i", submit=False)
        try:
            durable = restarted.client.get("/v1/agent/session?session_id=i")
            assert durable["operational_state"] == AgentOperationalState.WAITING_MODEL_SLOT.value
            assert durable["events"][-1]["payload"] == {"reason_code": "DIFFERENT_RESIDENT_MODEL"}
            assert restarted.executor.execute_calls == []
            assert restarted.adapter.physical_effects == []
        finally:
            _close(restarted)

        for suffix, digest, provider in (
            ("digest", "0" * 64, lambda *_args, **_kwargs: None),
            (
                "inference",
                QWEN_VISION_DIGEST,
                lambda model, *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("provider failed")),
            ),
        ):
            negative_root = Path(temporary) / suffix
            negative_root.mkdir()
            negative = _stack(negative_root, session_id=f"i-{suffix}", run_id=f"run-i-{suffix}")
            resident_state: list[str] = []
            inference_count: list[str] = []

            def failing_provider(
                model: str,
                *args: object,
                count: list[str] = inference_count,
                state: list[str] = resident_state,
                candidate=provider,
                **kwargs: object,
            ) -> object:
                count.append(model)
                state[:] = [model]
                return candidate(model, *args, **kwargs)

            negative_scheduler = ModelSlotScheduler(
                ps=lambda state=resident_state: list(state),
                digest=lambda _model, value=digest: value,
                infer=failing_provider,
                unload=lambda _model: None,
            )
            negative_observe = getattr(negative.domain, "observe_agent_vision", None)
            try:
                assert callable(negative_observe), "ControlDomainService vision composition seam is required"
                capture = _safe_capture(
                    negative_root,
                    run_id=f"run-i-{suffix}",
                    evidence_ref=f"capture-i-{suffix}",
                )
                try:
                    negative_observe(
                        f"i-{suffix}",
                        AgentVisionSensor(negative_scheduler),
                        capture,
                    )
                except ModelSlotUnavailable as exc:
                    expected = "MODEL_DIGEST_MISMATCH" if suffix == "digest" else "MODEL_INFERENCE_FAILED"
                    assert exc.code == expected
                else:
                    raise AssertionError(f"{suffix} failure unexpectedly succeeded")
                unchanged = negative.client.get(
                    f"/v1/agent/session?session_id=i-{suffix}"
                )
                assert unchanged["operational_state"] == AgentOperationalState.RUNNING.value
                assert not any(event["kind"] == "MODEL_SLOT_WAITING" for event in unchanged["events"])
                assert negative.executor.execute_calls == []
                assert negative.adapter.physical_effects == []
                if suffix == "digest":
                    assert inference_count == []
                else:
                    assert inference_count == [QWEN_VISION_MODEL]
            finally:
                _close(negative)


def scenario_j_secret_boundaries() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        stack = _stack(root, session_id="j", run_id="run-j")
        try:
            unsafe = _task("secret-task", "secret-run", actions=(NamedAgentAction.SCREENSHOT,))
            unsafe = unsafe.__class__(**{
                **asdict(unsafe),
                "objective": "PASSWORD=hunter2",
            })
            try:
                stack.agent.submit_task(unsafe, operation_id="secret-task-op")
            except PrivacyError:
                pass
            else:
                raise AssertionError("secret-bearing task reached persistence")
            assert stack.store.load_agent_session("secret-task") is None
            before_events = len(stack.client.get("/v1/agent/session?session_id=j")["events"])
            try:
                stack.client.post(
                    "/v1/agent/chat",
                    {"session_id": "j", "text": "token=hunter2"},
                    request_id="secret-chat-op",
                )
            except ControlClientError as exc:
                assert exc.payload["code"] == "CONTROL_PRIVACY_REJECTED"
            else:
                raise AssertionError("secret-bearing chat reached persistence")
            assert len(stack.client.get("/v1/agent/session?session_id=j")["events"]) == before_events

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
            assert stack.executor.execute_calls == []
        finally:
            _close(stack)


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
