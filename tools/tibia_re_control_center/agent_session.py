"""Persistent, deterministic agent-session control with no production runtime edge."""

from __future__ import annotations

import hashlib
import threading
import time
from collections.abc import Callable, Mapping
from dataclasses import asdict, dataclass, replace
from enum import Enum
from typing import Any, Protocol

from .agent_protocol import (
    AgentEvent,
    AgentOperationalState,
    AgentProvenance,
    AgentSessionRecord,
    NamedAgentAction,
    OwnerControlCommand,
    ResultEnvelope,
    ResultStatus,
    TaskEnvelope,
)
from .canonical import jcs_dumps
from .execution import CancellationToken, MutationCoordinator
from .model import (
    EFFECT_DIMENSIONS,
    MAX_SAFE_INTEGER,
    ActionRequest,
    ActionResult,
    Authority,
    Confirmation,
    DispatchFence,
    DispatchState,
    PrivacyError,
    SideEffectBudget,
    ValidationError,
    validate_opaque_id,
)
from .persistent_store import SQLitePersistentStore
from .recorder import ensure_no_secret_material
from .scenario import action_request_hash


@dataclass(frozen=True)
class AgentActionRequest:
    action_id: str
    session_id: str
    run_id: str
    action: NamedAgentAction
    expected_source_states: tuple[str, ...]
    remaining_budget: int
    deadline_epoch_ms: int
    secret_capability_ref: str | None


@dataclass(frozen=True)
class AgentActionReceipt:
    action_id: str
    status: str
    performed: bool
    outcome_known: bool
    low_level_event_count: int
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True)
class CaptureReceipt:
    status: str
    artifact_ref: str | None
    sha256: str | None
    secret_safe: bool


class BoundedActionExecutor(Protocol):
    def execute(self, request: AgentActionRequest) -> AgentActionReceipt: ...

    def screenshot(self, session_id: str, run_id: str) -> CaptureReceipt: ...


class NullBoundedActionExecutor:
    """The production foundation executor: an intentionally inert boundary."""

    def execute(self, request: AgentActionRequest) -> AgentActionReceipt:
        return AgentActionReceipt(
            action_id=request.action_id,
            status="REFUSED_EXECUTOR_UNBOUND",
            performed=False,
            outcome_known=True,
            low_level_event_count=0,
            evidence_refs=(),
        )

    def screenshot(self, session_id: str, run_id: str) -> CaptureReceipt:
        return CaptureReceipt(status="UNAVAILABLE", artifact_ref=None, sha256=None, secret_safe=True)


@dataclass(frozen=True)
class GuardedActionBinding:
    """Explicit named-action translation consumed only by MutationCoordinator."""

    kind: str
    parameters: Mapping[str, object]
    required_capability: str
    timeout_ms: int


class GuardedMutationActionExecutor:
    """Narrow effect facade whose only dispatch path is MutationCoordinator."""

    def __init__(
        self,
        control: MutationCoordinator,
        *,
        bindings: Mapping[NamedAgentAction, GuardedActionBinding],
        source_state_provider: Callable[[AgentActionRequest], str],
    ) -> None:
        self.control = control
        self.bindings = dict(bindings)
        self.source_state_provider = source_state_provider
        self._tasks: dict[str, TaskEnvelope] = {}
        self._lock = threading.RLock()
        for action, binding in self.bindings.items():
            if type(action) is not NamedAgentAction or action is NamedAgentAction.SCREENSHOT:
                raise ValidationError("INVALID_GUARDED_BINDING", "guarded bindings require mutating named actions")
            if type(binding) is not GuardedActionBinding:
                raise ValidationError("INVALID_GUARDED_BINDING", "guarded binding is invalid")
            if not isinstance(binding.kind, str) or not binding.kind:
                raise ValidationError("INVALID_GUARDED_BINDING", "guarded action kind is invalid")
            if not isinstance(binding.parameters, Mapping):
                raise ValidationError("INVALID_GUARDED_BINDING", "guarded action parameters are invalid")
            if not isinstance(binding.required_capability, str) or not binding.required_capability:
                raise ValidationError("INVALID_GUARDED_BINDING", "guarded capability is invalid")
            if type(binding.timeout_ms) is not int or binding.timeout_ms < 1:
                raise ValidationError("INVALID_GUARDED_BINDING", "guarded timeout is invalid")

    def bind_task(self, task: TaskEnvelope, *, activate: bool = False) -> None:
        with self._lock:
            existing = self._tasks.get(task.run_id)
            if existing is not None and existing != task:
                raise ValidationError("IDEMPOTENCY_CONFLICT", "guarded run is already bound to another task")
            self._tasks[task.run_id] = task
        if activate:
            self._activate_task_run(task)

    def _activate_task_run(self, task: TaskEnvelope) -> None:
        if task.run_id in self.control.runs:
            return
        if self.control.store.load_budget(task.run_id) is not None:
            return
        remaining_ms = max(
            1,
            task.deadline_epoch_ms - min(time.time_ns() // 1_000_000, MAX_SAFE_INTEGER),
        )
        runtime_seconds = max(1, min(86_400, (remaining_ms + 999) // 1_000))
        limits = {name: task.physical_action_budget for name in EFFECT_DIMENSIONS}
        self.control.start_run(
            task.run_id,
            SideEffectBudget(max_runtime_seconds=runtime_seconds, **limits),
            mutation_capable=True,
        )

    def _binding(self, action: NamedAgentAction) -> GuardedActionBinding:
        try:
            return self.bindings[action]
        except KeyError as exc:
            raise ValidationError("GUARDED_ACTION_UNBOUND", "named action has no guarded binding") from exc

    def _semantic_step_id(self, request: AgentActionRequest, binding: GuardedActionBinding) -> str:
        body = jcs_dumps({
            "session_id": request.session_id,
            "run_id": request.run_id,
            "action": request.action.value,
            "expected_source_states": list(request.expected_source_states),
            "deadline_epoch_ms": request.deadline_epoch_ms,
            "secret_capability_ref": request.secret_capability_ref,
            "kind": binding.kind,
            "parameters": dict(binding.parameters),
            "required_capability": binding.required_capability,
            "timeout_ms": binding.timeout_ms,
        })
        return f"agent-{hashlib.sha256(body.encode('utf-8')).hexdigest()}"

    def prepare(self, request: AgentActionRequest) -> ActionRequest:
        binding = self._binding(request.action)
        identity = self.control.adapter.identity()
        parameters = dict(binding.parameters)
        step_id = self._semantic_step_id(request, binding)
        request_hash = action_request_hash(
            schema_version=1,
            run_id=request.run_id,
            step_id=step_id,
            attempt_index=0,
            kind=binding.kind,
            parameters=parameters,
            timeout_ms=binding.timeout_ms,
            required_capability=binding.required_capability,
            required_authority=Authority.MUTATION,
        )
        return ActionRequest(
            action_id=request.action_id,
            run_id=request.run_id,
            step_id=step_id,
            attempt_index=0,
            kind=binding.kind,
            parameters=parameters,
            timeout_ms=binding.timeout_ms,
            required_capability=binding.required_capability,
            required_authority=Authority.MUTATION,
            dispatch_fence=DispatchFence(
                expected_backend_epoch=self.control.backend_epoch,
                expected_control_generation=self.control.control_generation,
                expected_adapter_generation=identity.adapter_generation,
                expected_runtime_instance_id=identity.runtime_instance_id,
                expected_session_epoch=identity.session_epoch,
            ),
            effect_bound=self.control.adapter.effect_bound(binding.kind, parameters),
            action_request_hash=request_hash,
        )

    def canonical_request_hash(self, request: AgentActionRequest) -> str:
        return self.prepare(request).action_request_hash

    def _ensure_run(self, request: AgentActionRequest) -> None:
        with self._lock:
            task = self._tasks.get(request.run_id)
        if task is None:
            raise ValidationError("GUARDED_TASK_UNBOUND", "guarded action requires its accepted task")
        if request.run_id in self.control.runs:
            return
        if self.control.store.load_budget(request.run_id) is not None:
            self.control.recover_run(request.run_id, mutation_capable=True)
            self.control.acquire_mutation_run(request.run_id)
            return
        self._activate_task_run(task)

    @staticmethod
    def receipt_from_result(request: AgentActionRequest, result: ActionResult) -> AgentActionReceipt:
        if result.dispatch_state == DispatchState.NOT_DISPATCHED:
            status = result.reason_code if result.reason_code == "REFUSED_IDEMPOTENCY_CONFLICT" else "NOT_PERFORMED"
            return AgentActionReceipt(request.action_id, status, False, True, 0, result.evidence_refs)
        if (
            result.dispatch_state == DispatchState.DISPATCHED
            and result.authoritative_confirmation == Confirmation.PROVEN
        ):
            return AgentActionReceipt(
                request.action_id,
                "PERFORMED",
                True,
                True,
                int(result.budget_effect.get("max_actions", 0)),
                result.evidence_refs,
            )
        return AgentActionReceipt(
            request.action_id,
            "PERFORMED_UNKNOWN",
            True,
            False,
            max(1, result.budget_effect.get("max_actions", 0)),
            result.evidence_refs,
        )

    def execute_guarded(
        self,
        request: AgentActionRequest,
        *,
        token: CancellationToken,
        final_commit_check: Callable[[], str | None],
    ) -> AgentActionReceipt:
        self._ensure_run(request)
        low_level = self.prepare(request)

        def combined_final_check() -> str | None:
            reason = final_commit_check()
            if reason is not None:
                return reason
            try:
                source_state = self.source_state_provider(request)
            except Exception:  # noqa: BLE001 -- trusted-state provider failure blocks dispatch
                return "AUTHORITATIVE_SOURCE_STATE_UNAVAILABLE"
            if not isinstance(source_state, str) or not source_state:
                return "AUTHORITATIVE_SOURCE_STATE_UNAVAILABLE"
            if request.expected_source_states and source_state not in request.expected_source_states:
                return "AUTHORITATIVE_SOURCE_STATE_MISMATCH"
            return None

        result = self.control.execute_action(
            low_level,
            token=token,
            final_commit_check=combined_final_check,
        )
        receipt = self.receipt_from_result(request, result)
        if receipt.performed:
            record = self.control.store.load_action(request.action_id)
            count = 0 if record is None else record.effect_bound.max_actions
            receipt = replace(receipt, low_level_event_count=count)
        return receipt


def _jsonable(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(key): _jsonable(child) for key, child in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(child) for child in value]
    return value


def _task_from_stored(value: object) -> TaskEnvelope:
    if not isinstance(value, dict):
        raise ValidationError("PERSISTENT_STATE_CORRUPT", "persistent agent task is corrupt")
    return TaskEnvelope.from_mapping(value)


def _result_from_stored(value: object) -> ResultEnvelope | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValidationError("PERSISTENT_STATE_CORRUPT", "persistent agent result is corrupt")
    try:
        return ResultEnvelope(
            schema=value["schema"],
            session_id=value["session_id"],
            run_id=value["run_id"],
            status=ResultStatus(value["status"]),
            trusted_main_sha=value["trusted_main_sha"],
            final_state=value["final_state"],
            action_count=value["action_count"],
            physical_action_budget=value["physical_action_budget"],
            evidence_manifest_sha256=value["evidence_manifest_sha256"],
            unresolved_conflicts=tuple(value["unresolved_conflicts"]),
        )
    except (KeyError, TypeError, ValueError):
        raise ValidationError("PERSISTENT_STATE_CORRUPT", "persistent agent result is corrupt") from None


class AgentSessionCoordinator:
    """Serialize agent task/control decisions and persist every authoritative outcome."""

    def __init__(
        self,
        store: SQLitePersistentStore,
        control: MutationCoordinator,
        executor: BoundedActionExecutor | None = None,
        *,
        guarded_executor: GuardedMutationActionExecutor | None = None,
    ) -> None:
        self.store = store
        self.control = control
        self.executor: BoundedActionExecutor = executor if executor is not None else NullBoundedActionExecutor()
        if guarded_executor is not None and (
            type(guarded_executor) is not GuardedMutationActionExecutor
            or guarded_executor.control is not control
        ):
            raise ValidationError(
                "INVALID_GUARDED_EXECUTOR",
                "guarded executor must be the exact MutationCoordinator-backed facade for this control domain",
            )
        self.guarded_executor = guarded_executor
        self._lock = threading.RLock()
        self._sessions: dict[str, AgentSessionRecord] = {}
        self._tasks: dict[str, TaskEnvelope] = {}
        self._results: dict[str, ResultEnvelope] = {}
        self._receipts: dict[tuple[str, str], AgentActionReceipt] = {}
        self._attempts: dict[str, int] = {}
        self._action_counts: dict[str, int] = {}
        self._evidence_refs: dict[str, list[str]] = {}
        self._inconclusive: set[str] = set()
        self._inflight: dict[tuple[str, str], CancellationToken] = {}

    @staticmethod
    def _now_epoch_ms() -> int:
        return min(time.time_ns() // 1_000_000, MAX_SAFE_INTEGER)

    def _events_for(self, session_id: str) -> list[dict[str, Any]]:
        events, _ = self.store.list_events(cursor=0, limit=self.store.event_retention)
        return [event for event in events if event.get("session_id") == session_id]

    def _operation_event(
        self,
        session_id: str,
        operation_id: str | None,
        *kinds: str,
    ) -> dict[str, Any] | None:
        if operation_id is None:
            return None
        validate_opaque_id(operation_id, field_name="operation_id", max_bytes=192)
        admitted = set(kinds)
        return next((
            event for event in self._events_for(session_id)
            if event.get("action_id") == operation_id
            and (not admitted or event.get("kind") in admitted)
        ), None)

    def _hydrate_exact_session(self, session_id: str) -> AgentSessionRecord:
        record = self.store.load_agent_session(session_id)
        if record is None:
            raise ValidationError("PERSISTENT_STATE_CORRUPT", "agent operation event is missing its session")
        task_values = self.store.load_agent_task_for_session(session_id)
        task = None if task_values is None else _task_from_stored(task_values["envelope"])
        result = None if task_values is None else _result_from_stored(task_values["result"])
        self._sessions[session_id] = record
        if task is not None:
            self._tasks[session_id] = task
        if result is not None:
            self._results[session_id] = result
        refs = self._evidence_refs.setdefault(session_id, [])
        for event in self._events_for(session_id):
            for ref in event.get("artifact_refs") or ():
                if isinstance(ref, str) and ref not in refs:
                    refs.append(ref)
        self._hydrate_authoritative_actions(session_id, task)
        return record

    @staticmethod
    def _receipt_from_ledger(record: object) -> AgentActionReceipt:
        if record.dispatch_state == DispatchState.NOT_DISPATCHED:
            status = (
                "REFUSED_IDEMPOTENCY_CONFLICT"
                if record.reason_code == "REFUSED_IDEMPOTENCY_CONFLICT"
                else "NOT_PERFORMED"
            )
            return AgentActionReceipt(record.action_id, status, False, True, 0, ())
        if (
            record.dispatch_state == DispatchState.DISPATCHED
            and record.authoritative_confirmation == Confirmation.PROVEN
        ):
            return AgentActionReceipt(
                record.action_id,
                "PERFORMED",
                True,
                True,
                record.effect_bound.max_actions,
                (),
            )
        return AgentActionReceipt(
            record.action_id,
            "PERFORMED_UNKNOWN",
            True,
            False,
            record.effect_bound.max_actions,
            (),
        )

    def _hydrate_authoritative_actions(self, session_id: str, task: TaskEnvelope | None) -> None:
        if task is None:
            self._attempts[session_id] = 0
            self._action_counts[session_id] = 0
            self._evidence_refs.setdefault(session_id, [])
            return
        actions = self.store.list_actions_for_run(task.run_id)
        ambiguous = False
        for record in actions:
            receipt = self._receipt_from_ledger(record)
            self._receipts[(session_id, record.action_id)] = receipt
            if receipt.status == "PERFORMED_UNKNOWN":
                ambiguous = True
        ledger = self.store.load_budget(task.run_id)
        if ledger is None:
            count = 0
        else:
            dimension = ledger.dimensions["max_actions"]
            count = dimension.at_risk + dimension.committed + dimension.uncertain
            if dimension.at_risk or dimension.uncertain:
                ambiguous = True
        if ambiguous:
            self._inconclusive.add(session_id)
        else:
            self._inconclusive.discard(session_id)
        self._attempts[session_id] = len(actions)
        self._action_counts[session_id] = count
        self._evidence_refs.setdefault(session_id, [])

    def ensure_session(self, session_id: str) -> AgentSessionRecord:
        validate_opaque_id(session_id, field_name="session_id")
        with self._lock:
            known = self._sessions.get(session_id)
            if known is not None:
                return known
            task_values = self.store.load_agent_task_for_session(session_id)
            task = None if task_values is None else _task_from_stored(task_values["envelope"])
            result = None if task_values is None else _result_from_stored(task_values["result"])
            if task is not None:
                self._tasks[session_id] = task
                if self.guarded_executor is not None:
                    self.guarded_executor.bind_task(task)
            if result is not None:
                self._results[session_id] = result
            loaded = self.store.load_agent_session(session_id)
            if loaded is None:
                initial = AgentSessionRecord(
                    session_id=session_id,
                    operational_state=AgentOperationalState.IDLE,
                    current_run_id=None,
                    last_event_seq=0,
                    pause_latched=False,
                    stop_latched=False,
                    heartbeat_epoch_ms=None,
                )
                if task is None:
                    self.store.write_agent_session(initial)
                    loaded = initial
                else:
                    target_state = (
                        AgentOperationalState.TERMINAL
                        if result is not None
                        else AgentOperationalState.PAUSED_AUTHORITY
                    )
                    target = replace(initial, operational_state=target_state, current_run_id=task.run_id)
                    event = AgentEvent.new(
                        session_id=session_id,
                        run_id=task.run_id,
                        provenance=AgentProvenance.SYSTEM,
                        kind="TASK_STATE_HYDRATED",
                        state_before=AgentOperationalState.IDLE.value,
                        state_after=target_state.value,
                        observed_epoch_ms=self._now_epoch_ms(),
                        payload={"result_present": result is not None, "auto_resume": False},
                    )
                    loaded, _ = self.store.atomic_agent_transition(
                        target,
                        event,
                        operation="agent_task_hydration",
                    )
            target_state: AgentOperationalState | None = None
            repair_kind = "SESSION_STATE_REPAIRED"
            if loaded.stop_latched:
                if loaded.operational_state is not AgentOperationalState.STOPPED:
                    target_state = AgentOperationalState.STOPPED
            elif loaded.pause_latched and loaded.operational_state is not AgentOperationalState.PAUSED:
                target_state = AgentOperationalState.PAUSED
            elif result is not None and loaded.operational_state is not AgentOperationalState.TERMINAL:
                target_state = AgentOperationalState.TERMINAL
                repair_kind = "RESULT_STATE_HYDRATED"
            elif task is not None and loaded.current_run_id is None:
                target_state = AgentOperationalState.PAUSED_AUTHORITY
                repair_kind = "TASK_STATE_HYDRATED"
            elif (
                loaded.current_run_id is not None
                and loaded.current_run_id not in self.control.runs
                and loaded.operational_state not in {
                AgentOperationalState.TERMINAL,
                AgentOperationalState.PAUSED_AUTHORITY,
                AgentOperationalState.PAUSED,
                AgentOperationalState.STOPPED,
                }
            ):
                target_state = AgentOperationalState.PAUSED_AUTHORITY
                repair_kind = "RESTART_RECONCILIATION_REQUIRED"
            if target_state is not None:
                before = loaded.operational_state
                target = replace(
                    loaded,
                    operational_state=target_state,
                    current_run_id=loaded.current_run_id if task is None else task.run_id,
                )
                repair_event = AgentEvent.new(
                    session_id=session_id,
                    run_id=target.current_run_id,
                    provenance=AgentProvenance.SYSTEM,
                    kind=repair_kind,
                    state_before=before.value,
                    state_after=target_state.value,
                    observed_epoch_ms=self._now_epoch_ms(),
                    payload={"auto_resume": False, "result_present": result is not None},
                )
                loaded, _ = self.store.atomic_agent_transition(
                    target,
                    repair_event,
                    operation="agent_session_repair",
                )
            self._sessions[session_id] = loaded
            self._hydrate_authoritative_actions(session_id, task)
            return loaded

    def _persist_event(
        self,
        session_id: str,
        *,
        provenance: AgentProvenance,
        kind: str,
        state_after: AgentOperationalState | None = None,
        pause_latched: bool | None = None,
        stop_latched: bool | None = None,
        run_id: str | None = None,
        action_id: str | None = None,
        artifact_refs: tuple[str, ...] = (),
        payload: dict[str, object] | None = None,
    ) -> AgentSessionRecord:
        record = self.ensure_session(session_id)
        durable = self.store.load_agent_session(session_id)
        if durable is not None:
            record = durable
        target_state = record.operational_state if state_after is None else state_after
        if kind != "OWNER_RESUME":
            if record.stop_latched:
                target_state = AgentOperationalState.STOPPED
            elif record.pause_latched and target_state is not AgentOperationalState.STOPPED:
                target_state = AgentOperationalState.PAUSED
        event = AgentEvent.new(
            session_id=session_id,
            run_id=record.current_run_id if run_id is None else run_id,
            provenance=provenance,
            kind=kind,
            state_before=record.operational_state.value,
            state_after=target_state.value,
            observed_epoch_ms=self._now_epoch_ms(),
            artifact_refs=artifact_refs,
            action_id=action_id,
            payload={} if payload is None else payload,
        )
        next_record = replace(
            record,
            operational_state=target_state,
            pause_latched=record.pause_latched if pause_latched is None else pause_latched,
            stop_latched=record.stop_latched if stop_latched is None else stop_latched,
        )
        next_record, _ = self.store.atomic_agent_transition(
            next_record,
            event,
            operation="agent_session_event",
        )
        self._sessions[session_id] = next_record
        return next_record

    def submit_task(
        self,
        envelope: TaskEnvelope,
        *,
        operation_id: str | None = None,
    ) -> dict[str, object]:
        with self._lock:
            if type(envelope) is not TaskEnvelope:
                raise ValidationError("INVALID_TASK", "task must be an exact TaskEnvelope")
            # Re-parse direct dataclass construction before any durable write.
            parsed_input = TaskEnvelope.from_mapping(asdict(envelope))
            ensure_no_secret_material(asdict(parsed_input), key_path="agent_task")
            if parsed_input.runtime_access != "none":
                raise ValidationError(
                    "RUNTIME_ACCESS_UNAVAILABLE",
                    "the repository foundation has no runtime access",
                )
            prior_event = self._operation_event(
                parsed_input.session_id,
                operation_id,
                "TASK_ACCEPTED",
            )
            if prior_event is not None:
                accepted = self.store.load_agent_task(parsed_input.idempotency_key)
                if accepted is None:
                    raise ValidationError(
                        "PERSISTENT_STATE_CORRUPT",
                        "task operation event is missing its accepted task",
                    )
                persisted = _task_from_stored(accepted["envelope"])
                if persisted != parsed_input:
                    raise ValidationError("IDEMPOTENCY_CONFLICT", "agent task operation identity is already bound")
                self._hydrate_exact_session(parsed_input.session_id)
                return {
                    "accepted_new": True,
                    "envelope": _jsonable(accepted["envelope"]),
                    "result": _jsonable(accepted["result"]),
                }
            durable_session = self.store.load_agent_session(parsed_input.session_id)
            stored_task = self.store.load_agent_task_for_session(parsed_input.session_id)
            if durable_session is None and stored_task is None:
                session = AgentSessionRecord(
                    session_id=parsed_input.session_id,
                    operational_state=AgentOperationalState.IDLE,
                    current_run_id=None,
                    last_event_seq=0,
                    pause_latched=False,
                    stop_latched=False,
                    heartbeat_epoch_ms=None,
                )
            else:
                session = self.ensure_session(parsed_input.session_id)
            if session.current_run_id not in {None, parsed_input.run_id} and session.operational_state is not AgentOperationalState.TERMINAL:
                raise ValidationError("SESSION_RUN_CONFLICT", "session already has another active run")
            target = replace(
                session,
                operational_state=AgentOperationalState.RUNNING,
                current_run_id=parsed_input.run_id,
            )
            accepted = self.store.accept_agent_task_transition(
                parsed_input,
                target,
                AgentEvent.new(
                    session_id=parsed_input.session_id,
                    run_id=parsed_input.run_id,
                    provenance=AgentProvenance.SUPERVISOR,
                    kind="TASK_ACCEPTED",
                    state_before=session.operational_state.value,
                    state_after=AgentOperationalState.RUNNING.value,
                    observed_epoch_ms=self._now_epoch_ms(),
                    action_id=operation_id,
                    payload={
                        "task_id": parsed_input.task_id,
                        "runtime_access": parsed_input.runtime_access,
                        "physical_action_budget": parsed_input.physical_action_budget,
                        "max_attempts": parsed_input.max_attempts,
                    },
                ),
            )
            parsed = _task_from_stored(accepted["envelope"])
            result = _result_from_stored(accepted["result"])
            self._tasks[parsed.session_id] = parsed
            if self.guarded_executor is not None:
                self.guarded_executor.bind_task(parsed, activate=bool(accepted["accepted_new"]))
            if result is not None:
                self._results[parsed.session_id] = result
            if bool(accepted["accepted_new"]):
                session = self.store.load_agent_session(parsed.session_id)
                if session is None:
                    raise ValidationError("PERSISTENT_STATE_CORRUPT", "accepted task is missing its session")
                self._sessions[parsed.session_id] = session
            else:
                durable_session = self.store.load_agent_session(parsed.session_id)
                if durable_session is not None:
                    session = durable_session
                    self._sessions[parsed.session_id] = durable_session
            if not bool(accepted["accepted_new"]) and result is not None and session.operational_state is not AgentOperationalState.TERMINAL:
                terminal = replace(session, operational_state=AgentOperationalState.TERMINAL, current_run_id=parsed.run_id)
                terminal, _ = self.store.atomic_agent_transition(
                    terminal,
                    AgentEvent.new(
                        session_id=parsed.session_id,
                        run_id=parsed.run_id,
                        provenance=AgentProvenance.SYSTEM,
                        kind="RESULT_STATE_HYDRATED",
                        state_before=session.operational_state.value,
                        state_after=AgentOperationalState.TERMINAL.value,
                        observed_epoch_ms=self._now_epoch_ms(),
                        payload={"auto_resume": False},
                    ),
                    operation="agent_result_hydration",
                )
                self._sessions[parsed.session_id] = terminal
            elif not bool(accepted["accepted_new"]) and session.current_run_id is None:
                paused = replace(
                    session,
                    operational_state=AgentOperationalState.PAUSED_AUTHORITY,
                    current_run_id=parsed.run_id,
                )
                paused, _ = self.store.atomic_agent_transition(
                    paused,
                    AgentEvent.new(
                        session_id=parsed.session_id,
                        run_id=parsed.run_id,
                        provenance=AgentProvenance.SYSTEM,
                        kind="TASK_STATE_HYDRATED",
                        state_before=session.operational_state.value,
                        state_after=AgentOperationalState.PAUSED_AUTHORITY.value,
                        observed_epoch_ms=self._now_epoch_ms(),
                        payload={"auto_resume": False},
                    ),
                    operation="agent_task_hydration",
                )
                self._sessions[parsed.session_id] = paused
            self._hydrate_authoritative_actions(parsed.session_id, parsed)
            return {
                "accepted_new": bool(accepted["accepted_new"]),
                "envelope": _jsonable(accepted["envelope"]),
                "result": _jsonable(accepted["result"]),
            }

    @staticmethod
    def _command(command: OwnerControlCommand | str) -> OwnerControlCommand:
        if isinstance(command, OwnerControlCommand):
            return command
        if not isinstance(command, str):
            raise ValidationError("INVALID_OWNER_CONTROL", "owner control command is invalid")
        try:
            return OwnerControlCommand(command)
        except ValueError:
            raise ValidationError("INVALID_OWNER_CONTROL", "owner control command is invalid") from None

    def _control_refusal(
        self,
        session_id: str,
        status: str,
        *,
        operation_id: str | None = None,
    ) -> dict[str, object]:
        self._persist_event(
            session_id,
            provenance=AgentProvenance.OWNER,
            kind="CONTROL_REFUSED",
            action_id=operation_id,
            payload={"status": status},
        )
        return {"status": status, "session": self.snapshot(session_id)}

    def _cancel_inflight(self, session_id: str) -> None:
        for (candidate_session, _), token in tuple(self._inflight.items()):
            if candidate_session == session_id:
                token.cancel()

    def owner_control(
        self,
        session_id: str,
        command: OwnerControlCommand | str,
        *,
        operation_id: str | None = None,
    ) -> dict[str, object]:
        with self._lock:
            parsed = self._command(command)
            session = self.ensure_session(session_id)
            prior_event = self._operation_event(
                session_id,
                operation_id,
                "OWNER_STOP",
                "OWNER_PAUSE",
                "OWNER_RESUME",
                "SCREENSHOT_RESULT",
                "CONTROL_REFUSED",
            )
            if prior_event is not None:
                self._hydrate_exact_session(session_id)
                status = prior_event.get("payload", {}).get("status")
                if not isinstance(status, str):
                    status = {
                        "OWNER_STOP": "STOPPED",
                        "OWNER_PAUSE": "PAUSED",
                        "OWNER_RESUME": prior_event.get("state_after", "IDLE"),
                    }.get(str(prior_event.get("kind")), "UNKNOWN")
                return {"status": status, "session": self.snapshot(session_id)}
            if parsed is OwnerControlCommand.RESUME and operation_id is not None:
                historical_reset = self.store.load_control_transition(operation_id)
                if historical_reset is not None:
                    if (
                        historical_reset.reason_code != "AGENT_OWNER_RESUME"
                        or historical_reset.stop_latched
                        or historical_reset.recovery_required
                    ):
                        raise ValidationError(
                            "IDEMPOTENCY_CONFLICT",
                            "owner RESUME operation identity is bound to another control transition",
                        )
                    session = self._hydrate_exact_session(session_id)
                    current_global = self.control.control_state
                    if current_global.stop_latched or current_global.recovery_required:
                        return {
                            "status": session.operational_state.value,
                            "session": self.snapshot(session_id),
                        }
                    if session.stop_latched or session.pause_latched:
                        self._persist_event(
                            session_id,
                            provenance=AgentProvenance.OWNER,
                            kind="OWNER_RESUME",
                            state_after=AgentOperationalState.IDLE,
                            pause_latched=False,
                            stop_latched=False,
                            action_id=operation_id,
                            payload={
                                "authority_reconciliation_required": bool(session.current_run_id),
                                "status": AgentOperationalState.IDLE.value,
                            },
                        )
                        return {"status": "IDLE", "session": self.snapshot(session_id)}
                    return {
                        "status": session.operational_state.value,
                        "session": self.snapshot(session_id),
                    }
            if parsed is OwnerControlCommand.SCREENSHOT:
                return self._capture(
                    session_id,
                    AgentProvenance.OWNER,
                    action_id=operation_id,
                )
            if parsed is OwnerControlCommand.STOP:
                if session.stop_latched:
                    return {"status": "STOPPED", "session": self.snapshot(session_id)}
                self._cancel_inflight(session_id)
                target = replace(
                    session,
                    operational_state=AgentOperationalState.STOPPED,
                    stop_latched=True,
                )
                owner_event = AgentEvent.new(
                    session_id=session_id,
                    run_id=session.current_run_id,
                    provenance=AgentProvenance.OWNER,
                    kind="OWNER_STOP",
                    state_before=session.operational_state.value,
                    state_after=AgentOperationalState.STOPPED.value,
                    observed_epoch_ms=self._now_epoch_ms(),
                    action_id=operation_id,
                    payload={"status": "STOPPED"},
                )
                persisted: list[AgentSessionRecord] = []

                def persist_stop(control_state: object) -> None:
                    durable, _ = self.store.atomic_agent_transition(
                        target,
                        owner_event,
                        operation="agent_owner_stop",
                        control_state=control_state,
                    )
                    persisted.append(durable)

                stopped = self.control.stop_all(
                    transition_id=operation_id,
                    reason_code="AGENT_OWNER_STOP",
                    state_persister=persist_stop,
                )
                if persisted:
                    self._sessions[session_id] = persisted[-1]
                if not stopped:
                    if persisted:
                        raise ValidationError(
                            "OWNER_STOP_CLEANUP_FAILED",
                            "owner STOP is durable but harness cleanup did not converge",
                        )
                    raise ValidationError("OWNER_STOP_DURABILITY_FAILED", "owner STOP did not durably converge")
                if not persisted:
                    raise ValidationError("OWNER_STOP_DURABILITY_FAILED", "owner STOP is missing its atomic session transition")
                return {"status": "STOPPED", "session": self.snapshot(session_id)}
            if parsed is OwnerControlCommand.PAUSE:
                if session.stop_latched:
                    return {"status": "STOPPED", "session": self.snapshot(session_id)}
                if not session.pause_latched:
                    self._cancel_inflight(session_id)
                    target = replace(
                        session,
                        operational_state=AgentOperationalState.PAUSED,
                        pause_latched=True,
                    )
                    owner_event = AgentEvent.new(
                        session_id=session_id,
                        run_id=session.current_run_id,
                        provenance=AgentProvenance.OWNER,
                        kind="OWNER_PAUSE",
                        state_before=session.operational_state.value,
                        state_after=AgentOperationalState.PAUSED.value,
                        observed_epoch_ms=self._now_epoch_ms(),
                        action_id=operation_id,
                        payload={"status": "PAUSED"},
                    )
                    persisted: list[AgentSessionRecord] = []

                    def persist_pause() -> None:
                        durable, _ = self.store.atomic_agent_transition(
                            target,
                            owner_event,
                            operation="agent_owner_pause",
                        )
                        persisted.append(durable)

                    if session.current_run_id in self.control.runs:
                        self.control.pause_run(session.current_run_id, durable_hook=persist_pause)
                    else:
                        persist_pause()
                    self._sessions[session_id] = persisted[-1]
                return {"status": "PAUSED", "session": self.snapshot(session_id)}

            global_state = self.control.control_state
            if global_state.stop_latched:
                target = replace(
                    session,
                    operational_state=AgentOperationalState.IDLE,
                    pause_latched=False,
                    stop_latched=False,
                )
                owner_event = AgentEvent.new(
                    session_id=session_id,
                    run_id=session.current_run_id,
                    provenance=AgentProvenance.OWNER,
                    kind="OWNER_RESUME",
                    state_before=session.operational_state.value,
                    state_after=AgentOperationalState.IDLE.value,
                    observed_epoch_ms=self._now_epoch_ms(),
                    action_id=operation_id,
                    payload={
                        "authority_reconciliation_required": bool(session.current_run_id),
                        "status": AgentOperationalState.IDLE.value,
                    },
                )
                persisted: list[AgentSessionRecord] = []

                def persist_resume(control_state: object) -> None:
                    durable, _ = self.store.atomic_agent_transition(
                        target,
                        owner_event,
                        operation="reset",
                        control_state=control_state,
                    )
                    persisted.append(durable)

                if not self.control.reset_stop(
                    transition_id=operation_id,
                    reason_code="AGENT_OWNER_RESUME",
                    state_persister=persist_resume,
                ):
                    return self._control_refusal(
                        session_id,
                        "REFUSED_GLOBAL_STOP_RESET_FAILED",
                        operation_id=operation_id,
                    )
                if not persisted:
                    raise ValidationError(
                        "OWNER_RESUME_DURABILITY_FAILED",
                        "owner RESUME is missing its atomic session transition",
                    )
                self._sessions[session_id] = persisted[-1]
                return {"status": "IDLE", "session": self.snapshot(session_id)}
            if global_state.recovery_required:
                return self._control_refusal(
                    session_id,
                    "REFUSED_GLOBAL_RECOVERY_REQUIRED",
                    operation_id=operation_id,
                )
            if (
                self.control.in_memory_stop
                or self.control.mutation_disabled
                or self.control.stop_cleanup_in_progress
                or self.control.stop_durability_unresolved
                or self.control.activation_error is not None
            ):
                return self._control_refusal(
                    session_id,
                    "REFUSED_GLOBAL_MUTATION_DISABLED",
                    operation_id=operation_id,
                )
            if not session.pause_latched and not session.stop_latched:
                return {"status": "UNCHANGED", "session": self.snapshot(session_id)}
            target = AgentOperationalState.PAUSED_AUTHORITY if session.current_run_id else AgentOperationalState.IDLE
            self._persist_event(
                session_id,
                provenance=AgentProvenance.OWNER,
                kind="OWNER_RESUME",
                state_after=target,
                pause_latched=False,
                stop_latched=False,
                action_id=operation_id,
                payload={
                    "authority_reconciliation_required": bool(session.current_run_id),
                    "status": target.value,
                },
            )
            return {"status": target.value, "session": self.snapshot(session_id)}

    def record_message(
        self,
        session_id: str,
        provenance: AgentProvenance,
        text: str,
        *,
        operation_id: str | None = None,
    ) -> dict[str, object]:
        if type(provenance) is not AgentProvenance:
            raise ValidationError("INVALID_PROVENANCE", "message provenance is invalid")
        if not isinstance(text, str) or not text.strip():
            raise ValidationError("INVALID_MESSAGE", "message text must be non-empty")
        ensure_no_secret_material(text, key_path="agent_message")
        token = text.strip().upper()
        if provenance is AgentProvenance.OWNER and token in OwnerControlCommand._value2member_map_:
            return self.owner_control(
                session_id,
                OwnerControlCommand(token),
                operation_id=operation_id,
            )
        encoded = text.encode("utf-8", "strict")
        return self.record_message_digest(
            session_id,
            provenance,
            hashlib.sha256(encoded).hexdigest(),
            len(encoded),
            operation_id=operation_id,
        )

    def record_message_digest(
        self,
        session_id: str,
        provenance: AgentProvenance,
        message_sha256: str,
        message_bytes: int,
        *,
        owner_control_command: OwnerControlCommand | str | None = None,
        operation_id: str | None = None,
    ) -> dict[str, object]:
        if type(provenance) is not AgentProvenance:
            raise ValidationError("INVALID_PROVENANCE", "message provenance is invalid")
        if (
            not isinstance(message_sha256, str)
            or len(message_sha256) != 64
            or any(character not in "0123456789abcdef" for character in message_sha256)
        ):
            raise ValidationError("INVALID_MESSAGE_DIGEST", "message SHA-256 is invalid")
        if not isinstance(message_bytes, int) or isinstance(message_bytes, bool) or message_bytes < 1:
            raise ValidationError("INVALID_MESSAGE", "message byte count must be positive")
        if owner_control_command is not None:
            if provenance is not AgentProvenance.OWNER:
                raise ValidationError("INVALID_PROVENANCE", "only OWNER messages can carry control")
            return self.owner_control(
                session_id,
                owner_control_command,
                operation_id=operation_id,
            )
        with self._lock:
            prior_event = self._operation_event(
                session_id,
                operation_id,
                "MESSAGE_RECORDED",
            )
            if prior_event is not None:
                if prior_event.get("payload", {}).get("message_sha256") != message_sha256:
                    raise ValidationError("IDEMPOTENCY_CONFLICT", "agent message operation identity is already bound")
                self._hydrate_exact_session(session_id)
                return {"status": "RECORDED", "session": self.snapshot(session_id)}
            self._persist_event(
                session_id,
                provenance=provenance,
                kind="MESSAGE_RECORDED",
                action_id=operation_id,
                payload={
                    "message_sha256": message_sha256,
                    "message_bytes": message_bytes,
                    "control_token_interpreted": False,
                },
            )
            return {"status": "RECORDED", "session": self.snapshot(session_id)}

    @staticmethod
    def _zero_receipt(action_id: str, status: str) -> AgentActionReceipt:
        return AgentActionReceipt(action_id, status, False, True, 0, ())

    def _refuse_action(
        self,
        session_id: str,
        action_id: str,
        action: NamedAgentAction,
        provenance: AgentProvenance,
        status: str,
    ) -> AgentActionReceipt:
        receipt = self._zero_receipt(action_id, status)
        self._persist_event(
            session_id,
            provenance=provenance,
            kind="MODEL_ACTION_PROPOSED" if provenance is AgentProvenance.MODEL else "ACTION_REFUSED",
            action_id=action_id,
            payload={
                "action": action.value,
                "status": status,
                "approved": False,
                "performed": False,
            },
        )
        return receipt

    def _record_action_receipt(
        self,
        session_id: str,
        action: NamedAgentAction,
        receipt: AgentActionReceipt,
    ) -> AgentActionReceipt:
        durable = self.store.load_agent_session(session_id)
        state = (
            self.ensure_session(session_id).operational_state
            if durable is None
            else durable.operational_state
        )
        if receipt.status == "PERFORMED_UNKNOWN":
            if durable is None or not durable.stop_latched and not durable.pause_latched:
                state = AgentOperationalState.PAUSED_AUTHORITY
            self._inconclusive.add(session_id)
        self._persist_event(
            session_id,
            provenance=AgentProvenance.RUNTIME,
            kind="ACTION_RESULT",
            state_after=state,
            action_id=receipt.action_id,
            artifact_refs=receipt.evidence_refs,
            payload={
                "action": action.value,
                "status": receipt.status,
                "performed": receipt.performed,
                "outcome_known": receipt.outcome_known,
                "low_level_event_count": receipt.low_level_event_count,
            },
        )
        self._receipts[(session_id, receipt.action_id)] = receipt
        refs = self._evidence_refs.setdefault(session_id, [])
        refs.extend(ref for ref in receipt.evidence_refs if ref not in refs)
        self._hydrate_authoritative_actions(session_id, self._tasks.get(session_id))
        return receipt

    def _final_commit_guard(self, session_id: str, request: AgentActionRequest) -> str | None:
        durable = self.store.load_agent_session(session_id)
        if durable is None:
            return "SESSION_STATE_MISSING"
        if durable.stop_latched or durable.operational_state is AgentOperationalState.STOPPED:
            return "OWNER_STOPPED"
        if durable.pause_latched or durable.operational_state is AgentOperationalState.PAUSED:
            return "OWNER_PAUSED"
        if durable.operational_state is not AgentOperationalState.RUNNING:
            return "SESSION_NOT_RUNNING"
        if self._now_epoch_ms() >= request.deadline_epoch_ms:
            return "AGENT_DEADLINE_EXPIRED"
        if not self.control.mutation_admission_allowed():
            return "SYSTEM_MUTATION_BLOCKED"
        return None

    def propose_named_action(
        self,
        session_id: str,
        action_id: str,
        action: NamedAgentAction,
        *,
        provenance: AgentProvenance = AgentProvenance.SUPERVISOR,
        expected_source_states: tuple[str, ...] = (),
        current_state: str = "UNKNOWN",
    ) -> AgentActionReceipt:
        validate_opaque_id(action_id, field_name="action_id")
        if type(action) is not NamedAgentAction:
            raise ValidationError("INVALID_NAMED_ACTION", "action must be an exact named action enum")
        if type(provenance) is not AgentProvenance:
            raise ValidationError("INVALID_PROVENANCE", "action provenance is invalid")
        if type(expected_source_states) is not tuple or any(not isinstance(item, str) or not item for item in expected_source_states):
            raise ValidationError("INVALID_SOURCE_STATES", "expected source states must be a tuple of non-empty strings")
        if not isinstance(current_state, str) or not current_state:
            raise ValidationError("INVALID_SOURCE_STATE", "current source state is invalid")
        guarded_request: AgentActionRequest | None = None
        token: CancellationToken | None = None
        known_action_pending = False
        with self._lock:
            session = self.ensure_session(session_id)
            task = self._tasks.get(session_id)
            if task is None:
                return self._refuse_action(session_id, action_id, action, provenance, "REFUSED_TASK_MISSING")
            if (
                self.guarded_executor is not None
                and action is not NamedAgentAction.SCREENSHOT
                and provenance is AgentProvenance.SUPERVISOR
            ):
                durable_budget = self.store.load_budget(task.run_id)
                early_remaining = (
                    task.physical_action_budget
                    if durable_budget is None
                    else durable_budget.dimensions["max_actions"].available()
                )
                early_request = AgentActionRequest(
                    action_id=action_id,
                    session_id=session_id,
                    run_id=task.run_id,
                    action=action,
                    expected_source_states=expected_source_states,
                    remaining_budget=early_remaining,
                    deadline_epoch_ms=task.deadline_epoch_ms,
                    secret_capability_ref=task.secret_capability_ref,
                )
                early_hash = self.guarded_executor.canonical_request_hash(early_request)
                durable_action = self.store.load_action(action_id)
                if durable_action is not None:
                    if durable_action.action_request_hash != early_hash:
                        return self._refuse_action(
                            session_id,
                            action_id,
                            action,
                            provenance,
                            "REFUSED_IDEMPOTENCY_CONFLICT",
                        )
                    if durable_action.terminal or (
                        durable_action.dispatch_state != DispatchState.NOT_DISPATCHED
                        and not self.control.mutation_execution_lock.locked()
                    ):
                        receipt = self._receipt_from_ledger(durable_action)
                        self._receipts[(session_id, action_id)] = receipt
                        self._hydrate_authoritative_actions(session_id, task)
                        return receipt
                    known_action_pending = True
            if action is not NamedAgentAction.SCREENSHOT:
                # SYSTEM/global state always precedes local owner/session state,
                # regardless of which lower-authority actor made the proposal.
                if self.control.control_state.stop_latched or self.control.in_memory_stop:
                    return self._refuse_action(session_id, action_id, action, provenance, "REFUSED_SYSTEM_STOPPED")
                if self.control.control_state.recovery_required:
                    return self._refuse_action(session_id, action_id, action, provenance, "REFUSED_SYSTEM_RECOVERY_REQUIRED")
                if (
                    self.control.mutation_disabled
                    or self.control.stop_cleanup_in_progress
                    or self.control.stop_durability_unresolved
                    or self.control.activation_error is not None
                ):
                    return self._refuse_action(session_id, action_id, action, provenance, "REFUSED_SYSTEM_MUTATION_DISABLED")
                if session.stop_latched or session.operational_state is AgentOperationalState.STOPPED:
                    return self._refuse_action(session_id, action_id, action, provenance, "REFUSED_OWNER_STOPPED")
                if session.pause_latched or session.operational_state is AgentOperationalState.PAUSED:
                    return self._refuse_action(session_id, action_id, action, provenance, "REFUSED_OWNER_PAUSED")
                if session.operational_state is AgentOperationalState.PAUSED_AUTHORITY:
                    return self._refuse_action(session_id, action_id, action, provenance, "REFUSED_AUTHORITY_RECONCILIATION_REQUIRED")
                if session.operational_state is not AgentOperationalState.RUNNING:
                    return self._refuse_action(session_id, action_id, action, provenance, "REFUSED_SESSION_NOT_RUNNING")
            if provenance is AgentProvenance.MODEL:
                return self._refuse_action(session_id, action_id, action, provenance, "REFUSED_MODEL_NO_AUTHORITY")
            if provenance is not AgentProvenance.SUPERVISOR:
                return self._refuse_action(session_id, action_id, action, provenance, "REFUSED_ACTION_AUTHORITY")
            if action not in task.allowed_actions:
                return self._refuse_action(session_id, action_id, action, provenance, "REFUSED_ACTION_NOT_ALLOWED")
            if action is NamedAgentAction.SCREENSHOT:
                capture = self._capture(session_id, provenance, action_id=action_id)["capture"]
                refs = () if capture["artifact_ref"] is None else (str(capture["artifact_ref"]),)
                return AgentActionReceipt(action_id, str(capture["status"]), False, True, 0, refs)
            if expected_source_states and current_state not in expected_source_states:
                return self._refuse_action(session_id, action_id, action, provenance, "REFUSED_SOURCE_STATE_MISMATCH")
            ledger = self.store.load_budget(task.run_id)
            actions = self.store.list_actions_for_run(task.run_id)
            if ledger is None:
                remaining = task.physical_action_budget
            else:
                dimension = ledger.dimensions["max_actions"]
                remaining = dimension.available()
            if remaining <= 0 and not known_action_pending:
                return self._refuse_action(session_id, action_id, action, provenance, "REFUSED_BUDGET_EXHAUSTED")
            attempts = len(actions)
            if attempts >= task.max_attempts and not known_action_pending:
                return self._refuse_action(session_id, action_id, action, provenance, "REFUSED_ATTEMPTS_EXHAUSTED")
            if self._now_epoch_ms() >= task.deadline_epoch_ms:
                return self._refuse_action(session_id, action_id, action, provenance, "REFUSED_DEADLINE_EXPIRED")

            request = AgentActionRequest(
                action_id=action_id,
                session_id=session_id,
                run_id=task.run_id,
                action=action,
                expected_source_states=expected_source_states,
                remaining_budget=remaining,
                deadline_epoch_ms=task.deadline_epoch_ms,
                secret_capability_ref=task.secret_capability_ref,
            )
            if self.guarded_executor is None:
                if type(self.executor) is not NullBoundedActionExecutor:
                    return self._refuse_action(
                        session_id,
                        action_id,
                        action,
                        provenance,
                        "REFUSED_EXECUTOR_UNGUARDED",
                    )
                received = self.executor.execute(request)
                return self._record_action_receipt(
                    session_id,
                    action,
                    self._validated_receipt(action_id, received),
                )
            expected_hash = self.guarded_executor.canonical_request_hash(request)
            durable_action = self.store.load_action(action_id)
            if durable_action is not None:
                if durable_action.action_request_hash != expected_hash:
                    return self._refuse_action(
                        session_id,
                        action_id,
                        action,
                        provenance,
                        "REFUSED_IDEMPOTENCY_CONFLICT",
                    )
                if durable_action.terminal or (
                    durable_action.dispatch_state != DispatchState.NOT_DISPATCHED
                    and not self.control.mutation_execution_lock.locked()
                ):
                    receipt = self._receipt_from_ledger(durable_action)
                    self._receipts[(session_id, action_id)] = receipt
                    self._hydrate_authoritative_actions(session_id, task)
                    return receipt
            token = CancellationToken()
            self._inflight[(session_id, action_id)] = token
            guarded_request = request

        if guarded_request is None or token is None or self.guarded_executor is None:
            raise RuntimeError("guarded action preparation failed")
        try:
            receipt = self.guarded_executor.execute_guarded(
                guarded_request,
                token=token,
                final_commit_check=lambda: self._final_commit_guard(session_id, guarded_request),
            )
        except Exception:  # noqa: BLE001 -- durable dispatch state decides replay safety
            durable_action = self.store.load_action(action_id)
            receipt = (
                self._zero_receipt(action_id, "NOT_PERFORMED")
                if durable_action is None
                else self._receipt_from_ledger(durable_action)
            )
        with self._lock:
            if self._inflight.get((session_id, action_id)) is token:
                self._inflight.pop((session_id, action_id), None)
            durable_action = self.store.load_action(action_id)
            if durable_action is not None:
                receipt = self._receipt_from_ledger(durable_action)
            receipt = self._validated_receipt(action_id, receipt)
            return self._record_action_receipt(session_id, action, receipt)

    @staticmethod
    def _validated_receipt(action_id: str, value: object) -> AgentActionReceipt:
        valid = (
            type(value) is AgentActionReceipt
            and value.action_id == action_id
            and isinstance(value.status, str) and bool(value.status)
            and type(value.performed) is bool
            and type(value.outcome_known) is bool
            and type(value.low_level_event_count) is int and value.low_level_event_count >= 0
            and type(value.evidence_refs) is tuple
            and all(isinstance(ref, str) and bool(ref) for ref in value.evidence_refs)
        )
        if valid:
            try:
                ensure_no_secret_material(value.status, key_path="executor_receipt.status")
                for evidence_ref in value.evidence_refs:
                    validate_opaque_id(evidence_ref, field_name="evidence_ref")
            except (PrivacyError, ValidationError):
                valid = False
        if not valid:
            return AgentActionReceipt(action_id, "PERFORMED_UNKNOWN", True, False, 0, ())
        if value.performed and not value.outcome_known:
            return replace(value, status="PERFORMED_UNKNOWN")
        if not value.performed:
            return AgentActionReceipt(action_id, value.status, False, True, 0, value.evidence_refs)
        return value

    def _capture(
        self,
        session_id: str,
        provenance: AgentProvenance,
        *,
        action_id: str | None = None,
    ) -> dict[str, object]:
        session = self.ensure_session(session_id)
        run_id = session.current_run_id or f"{session_id}-idle"
        try:
            receipt = self.executor.screenshot(session_id, run_id)
        except Exception:  # noqa: BLE001 -- read-only capture boundary fails closed
            receipt = CaptureReceipt("UNAVAILABLE", None, None, True)
        valid = (
            type(receipt) is CaptureReceipt
            and isinstance(receipt.status, str) and bool(receipt.status)
            and (receipt.artifact_ref is None or isinstance(receipt.artifact_ref, str) and bool(receipt.artifact_ref))
            and (receipt.sha256 is None or isinstance(receipt.sha256, str) and len(receipt.sha256) == 64
                 and all(char in "0123456789abcdef" for char in receipt.sha256))
            and type(receipt.secret_safe) is bool
        )
        if not valid:
            receipt = CaptureReceipt("UNAVAILABLE", None, None, True)
        if not receipt.secret_safe:
            receipt = CaptureReceipt("REJECTED_UNSAFE_CAPTURE", None, None, False)
        refs = () if receipt.artifact_ref is None else (receipt.artifact_ref,)
        self._persist_event(
            session_id,
            provenance=provenance,
            kind="SCREENSHOT_RESULT",
            action_id=action_id,
            artifact_refs=refs,
            payload={
                "status": receipt.status,
                "sha256": receipt.sha256,
                "secret_safe": receipt.secret_safe,
                "physical_effect": False,
            },
        )
        if receipt.artifact_ref is not None:
            evidence = self._evidence_refs.setdefault(session_id, [])
            if receipt.artifact_ref not in evidence:
                evidence.append(receipt.artifact_ref)
        return {"status": receipt.status, "capture": _jsonable(asdict(receipt)), "session": self.snapshot(session_id)}

    def complete_run(
        self,
        session_id: str,
        result: ResultEnvelope | None = None,
        *,
        status: ResultStatus | str | None = None,
        final_state: str | None = None,
        evidence_manifest_sha256: str | None = None,
        unresolved_conflicts: tuple[str, ...] = (),
    ) -> ResultEnvelope:
        with self._lock:
            self.ensure_session(session_id)
            task = self._tasks.get(session_id)
            if task is None:
                raise ValidationError("AGENT_TASK_MISSING", "cannot complete a missing agent task")
            self._hydrate_authoritative_actions(session_id, task)
            ledger = self.store.load_budget(task.run_id)
            if ledger is None:
                authoritative_count = 0
                authoritative_budget = task.physical_action_budget
            else:
                dimension = ledger.dimensions["max_actions"]
                authoritative_count = dimension.at_risk + dimension.committed + dimension.uncertain
                authoritative_budget = dimension.limit
            if result is None:
                try:
                    parsed_status = status if isinstance(status, ResultStatus) else ResultStatus(status)
                except (TypeError, ValueError):
                    raise ValidationError("INVALID_RESULT_STATUS", "result status is invalid") from None
                if not isinstance(final_state, str) or not final_state:
                    raise ValidationError("INVALID_RESULT_STATE", "result final state is invalid")
                if not isinstance(evidence_manifest_sha256, str):
                    raise ValidationError("INVALID_SHA256", "result evidence manifest hash is invalid")
                result = ResultEnvelope(
                    schema="otclient.local-agent.result.v1",
                    session_id=session_id,
                    run_id=task.run_id,
                    status=parsed_status,
                    trusted_main_sha=task.trusted_main_sha,
                    final_state=final_state,
                    action_count=authoritative_count,
                    physical_action_budget=authoritative_budget,
                    evidence_manifest_sha256=evidence_manifest_sha256,
                    unresolved_conflicts=tuple(unresolved_conflicts),
                )
            if type(result) is not ResultEnvelope:
                raise ValidationError("INVALID_RESULT", "result must be an exact ResultEnvelope")
            if (
                result.session_id != session_id
                or result.run_id != task.run_id
                or result.trusted_main_sha != task.trusted_main_sha
            ):
                raise ValidationError("TASK_RESULT_MISMATCH", "agent result does not match accepted task")
            if (
                result.action_count != authoritative_count
                or result.physical_action_budget != authoritative_budget
            ):
                raise ValidationError("RESULT_COUNTER_MISMATCH", "agent result counters must match authoritative ledgers")
            if session_id in self._inconclusive:
                conflicts = tuple(result.unresolved_conflicts)
                if "PERFORMED_UNKNOWN" not in conflicts:
                    conflicts += ("PERFORMED_UNKNOWN",)
                result = replace(result, status=ResultStatus.INCONCLUSIVE, unresolved_conflicts=conflicts)
            existing = self._results.get(session_id)
            if existing is not None:
                if existing != result:
                    raise ValidationError("IDEMPOTENCY_CONFLICT", "agent task result is already bound")
                return existing
            session = self.ensure_session(session_id)
            terminal = replace(session, operational_state=AgentOperationalState.TERMINAL)
            event = AgentEvent.new(
                session_id=session_id,
                run_id=task.run_id,
                provenance=AgentProvenance.SYSTEM,
                kind="RUN_COMPLETED",
                state_before=session.operational_state.value,
                state_after=AgentOperationalState.TERMINAL.value,
                observed_epoch_ms=self._now_epoch_ms(),
                artifact_refs=(result.evidence_manifest_sha256,),
                payload={
                    "status": result.status.value,
                    "action_count": result.action_count,
                    "physical_action_budget": result.physical_action_budget,
                    "unresolved_conflicts": result.unresolved_conflicts,
                },
            )
            self.store.finish_agent_task_transition(
                task.idempotency_key,
                result,
                terminal,
                event,
            )
            self._results[session_id] = result
            durable = self.store.load_agent_session(session_id)
            if durable is None:
                raise ValidationError("PERSISTENT_STATE_CORRUPT", "completed result is missing its session")
            self._sessions[session_id] = durable
            return result

    def snapshot(self, session_id: str) -> dict[str, object]:
        with self._lock:
            session = self.ensure_session(session_id)
            task = self._tasks.get(session_id)
            result = self._results.get(session_id)
            self._hydrate_authoritative_actions(session_id, task)
            ledger = None if task is None else self.store.load_budget(task.run_id)
            if ledger is None:
                remaining_budget = 0 if task is None else task.physical_action_budget
            else:
                remaining_budget = ledger.dimensions["max_actions"].available()
            events = self._events_for(session_id)
            return {
                "session_id": session.session_id,
                "operational_state": session.operational_state.value,
                "current_run_id": session.current_run_id,
                "last_event_seq": session.last_event_seq,
                "pause_latched": session.pause_latched,
                "stop_latched": session.stop_latched,
                "heartbeat_epoch_ms": session.heartbeat_epoch_ms,
                "task_id": None if task is None else task.task_id,
                "trusted_main_sha": None if task is None else task.trusted_main_sha,
                "runtime_access": "none" if task is None else task.runtime_access,
                "allowed_actions": [] if task is None else [action.value for action in task.allowed_actions],
                "physical_action_budget": 0 if task is None else task.physical_action_budget,
                "physical_action_count": self._action_counts.get(session_id, 0),
                "remaining_physical_action_budget": remaining_budget,
                "attempt_count": self._attempts.get(session_id, 0),
                "max_attempts": 0 if task is None else task.max_attempts,
                "run_status": "INCONCLUSIVE" if session_id in self._inconclusive else (
                    None if result is None else result.status.value
                ),
                "result": None if result is None else _jsonable(asdict(result)),
                "evidence_refs": list(self._evidence_refs.get(session_id, [])),
                "events": events,
                "executor": "NULL" if type(self.executor) is NullBoundedActionExecutor else "INJECTED_TEST",
                "mutation_authority": "NONE",
                "official_client_access": "NONE",
            }

    def foundation_status(self) -> dict[str, object]:
        """Secret-safe aggregate used by the existing Package B status document."""
        return {
            "state": "FOUNDATION",
            "runtime_access": "none",
            "executor": "NULL" if type(self.executor) is NullBoundedActionExecutor else "INJECTED_TEST",
            "mutation_authority": "NONE",
            "official_client_access": "NONE",
            "physical_action_budget": 0,
            "physical_action_count": 0,
        }
