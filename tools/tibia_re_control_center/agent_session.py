"""Persistent, deterministic agent-session control with no production runtime edge."""

from __future__ import annotations

import hashlib
import threading
import time
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
from .execution import MutationCoordinator
from .model import MAX_SAFE_INTEGER, PrivacyError, ValidationError, validate_opaque_id
from .persistent_store import SQLitePersistentStore
from .recorder import ensure_no_secret_material


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
    ) -> None:
        self.store = store
        self.control = control
        self.executor: BoundedActionExecutor = executor if executor is not None else NullBoundedActionExecutor()
        self._lock = threading.RLock()
        self._sessions: dict[str, AgentSessionRecord] = {}
        self._tasks: dict[str, TaskEnvelope] = {}
        self._results: dict[str, ResultEnvelope] = {}
        self._receipts: dict[tuple[str, str], AgentActionReceipt] = {}
        self._attempts: dict[str, int] = {}
        self._action_counts: dict[str, int] = {}
        self._evidence_refs: dict[str, list[str]] = {}
        self._inconclusive: set[str] = set()

    @staticmethod
    def _now_epoch_ms() -> int:
        return min(time.time_ns() // 1_000_000, MAX_SAFE_INTEGER)

    def _events_for(self, session_id: str) -> list[dict[str, Any]]:
        events, _ = self.store.list_events(cursor=0, limit=self.store.event_retention)
        return [event for event in events if event.get("session_id") == session_id]

    def _hydrate_from_events(self, session_id: str) -> None:
        attempts = 0
        count = 0
        evidence: list[str] = []
        pending: set[str] = set()
        for event in self._events_for(session_id):
            action_id = event.get("action_id")
            kind = event.get("kind")
            if (
                kind == "ACTION_RESERVED"
                and event.get("schema") == "otclient.local-agent.event.v1"
                and event.get("provenance") == AgentProvenance.SUPERVISOR.value
                and isinstance(action_id, str)
            ):
                attempts += 1
                pending.add(action_id)
            if (
                kind != "ACTION_RESULT"
                or event.get("schema") != "otclient.local-agent.event.v1"
                or event.get("provenance") != AgentProvenance.RUNTIME.value
                or not isinstance(action_id, str)
                or action_id not in pending
            ):
                continue
            payload = event.get("payload")
            if not isinstance(payload, dict):
                continue
            refs = tuple(event.get("artifact_refs") or ())
            try:
                receipt = AgentActionReceipt(
                    action_id=action_id,
                    status=str(payload["status"]),
                    performed=payload["performed"],
                    outcome_known=payload["outcome_known"],
                    low_level_event_count=payload["low_level_event_count"],
                    evidence_refs=refs,
                )
            except (KeyError, TypeError, ValueError):
                continue
            receipt = self._validated_receipt(action_id, receipt)
            self._receipts[(session_id, action_id)] = receipt
            pending.discard(action_id)
            if receipt.performed:
                count += 1
            evidence.extend(ref for ref in refs if ref not in evidence)
            if receipt.status == "PERFORMED_UNKNOWN":
                self._inconclusive.add(session_id)
        for action_id in pending:
            # A durable reservation without a result crossed a restart boundary.  The
            # executor may have received it, so its identity is permanently latched.
            self._receipts[(session_id, action_id)] = AgentActionReceipt(
                action_id, "PERFORMED_UNKNOWN", True, False, 0, (),
            )
            self._inconclusive.add(session_id)
            count += 1
        self._attempts[session_id] = attempts
        self._action_counts[session_id] = count
        self._evidence_refs[session_id] = evidence

    def ensure_session(self, session_id: str) -> AgentSessionRecord:
        validate_opaque_id(session_id, field_name="session_id")
        with self._lock:
            known = self._sessions.get(session_id)
            if known is not None:
                return known
            loaded = self.store.load_agent_session(session_id)
            if loaded is None:
                loaded = AgentSessionRecord(
                    session_id=session_id,
                    operational_state=AgentOperationalState.IDLE,
                    current_run_id=None,
                    last_event_seq=0,
                    pause_latched=False,
                    stop_latched=False,
                    heartbeat_epoch_ms=None,
                )
                self.store.write_agent_session(loaded)
            elif loaded.stop_latched:
                loaded = replace(loaded, operational_state=AgentOperationalState.STOPPED)
                self.store.write_agent_session(loaded)
            elif loaded.pause_latched:
                loaded = replace(loaded, operational_state=AgentOperationalState.PAUSED)
                self.store.write_agent_session(loaded)
            elif loaded.current_run_id is not None and loaded.operational_state not in {
                AgentOperationalState.TERMINAL,
                AgentOperationalState.PAUSED_AUTHORITY,
            }:
                before = loaded.operational_state
                paused = replace(loaded, operational_state=AgentOperationalState.PAUSED_AUTHORITY)
                event = self.store.append_agent_event(AgentEvent.new(
                    session_id=session_id,
                    run_id=loaded.current_run_id,
                    provenance=AgentProvenance.SYSTEM,
                    kind="RESTART_RECONCILIATION_REQUIRED",
                    state_before=before.value,
                    state_after=AgentOperationalState.PAUSED_AUTHORITY.value,
                    observed_epoch_ms=self._now_epoch_ms(),
                    payload={"auto_resume": False},
                ))
                loaded = replace(paused, last_event_seq=event.seq)
                self.store.write_agent_session(loaded)
            self._sessions[session_id] = loaded
            self._hydrate_from_events(session_id)
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
        target_state = record.operational_state if state_after is None else state_after
        persisted = self.store.append_agent_event(AgentEvent.new(
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
        ))
        next_record = replace(
            record,
            operational_state=target_state,
            last_event_seq=persisted.seq,
            pause_latched=record.pause_latched if pause_latched is None else pause_latched,
            stop_latched=record.stop_latched if stop_latched is None else stop_latched,
        )
        self.store.write_agent_session(next_record)
        self._sessions[session_id] = next_record
        return next_record

    def submit_task(self, envelope: TaskEnvelope) -> dict[str, object]:
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
            session = self.ensure_session(parsed_input.session_id)
            if session.current_run_id not in {None, parsed_input.run_id} and session.operational_state is not AgentOperationalState.TERMINAL:
                raise ValidationError("SESSION_RUN_CONFLICT", "session already has another active run")
            accepted = self.store.accept_agent_task(parsed_input)
            parsed = _task_from_stored(accepted["envelope"])
            result = _result_from_stored(accepted["result"])
            self._tasks[parsed.session_id] = parsed
            if result is not None:
                self._results[parsed.session_id] = result
            if bool(accepted["accepted_new"]):
                state = AgentOperationalState.RUNNING
                event = self.store.append_agent_event(AgentEvent.new(
                    session_id=parsed.session_id,
                    run_id=parsed.run_id,
                    provenance=AgentProvenance.SUPERVISOR,
                    kind="TASK_ACCEPTED",
                    state_before=session.operational_state.value,
                    state_after=state.value,
                    observed_epoch_ms=self._now_epoch_ms(),
                    payload={
                        "task_id": parsed.task_id,
                        "runtime_access": parsed.runtime_access,
                        "physical_action_budget": parsed.physical_action_budget,
                        "max_attempts": parsed.max_attempts,
                    },
                ))
                session = replace(
                    session,
                    operational_state=state,
                    current_run_id=parsed.run_id,
                    last_event_seq=event.seq,
                )
                self.store.write_agent_session(session)
                self._sessions[parsed.session_id] = session
                self._attempts[parsed.session_id] = 0
                self._action_counts[parsed.session_id] = 0
                self._evidence_refs[parsed.session_id] = []
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

    def _control_refusal(self, session_id: str, status: str) -> dict[str, object]:
        self._persist_event(
            session_id,
            provenance=AgentProvenance.OWNER,
            kind="CONTROL_REFUSED",
            payload={"status": status},
        )
        return {"status": status, "session": self.snapshot(session_id)}

    def owner_control(self, session_id: str, command: OwnerControlCommand | str) -> dict[str, object]:
        with self._lock:
            parsed = self._command(command)
            session = self.ensure_session(session_id)
            if parsed is OwnerControlCommand.SCREENSHOT:
                return self._capture(session_id, AgentProvenance.OWNER)
            if parsed is OwnerControlCommand.STOP:
                if session.stop_latched:
                    return {"status": "STOPPED", "session": self.snapshot(session_id)}
                if not self.control.stop_all(reason_code="AGENT_OWNER_STOP"):
                    raise ValidationError("OWNER_STOP_DURABILITY_FAILED", "owner STOP did not durably converge")
                self._persist_event(
                    session_id,
                    provenance=AgentProvenance.OWNER,
                    kind="OWNER_STOP",
                    state_after=AgentOperationalState.STOPPED,
                    stop_latched=True,
                )
                return {"status": "STOPPED", "session": self.snapshot(session_id)}
            if parsed is OwnerControlCommand.PAUSE:
                if session.stop_latched:
                    return {"status": "STOPPED", "session": self.snapshot(session_id)}
                if not session.pause_latched:
                    self._persist_event(
                        session_id,
                        provenance=AgentProvenance.OWNER,
                        kind="OWNER_PAUSE",
                        state_after=AgentOperationalState.PAUSED,
                        pause_latched=True,
                    )
                return {"status": "PAUSED", "session": self.snapshot(session_id)}

            global_state = self.control.control_state
            if global_state.stop_latched:
                return self._control_refusal(session_id, "REFUSED_GLOBAL_STOP_LATCHED")
            if global_state.recovery_required:
                return self._control_refusal(session_id, "REFUSED_GLOBAL_RECOVERY_REQUIRED")
            if (
                self.control.in_memory_stop
                or self.control.mutation_disabled
                or self.control.stop_cleanup_in_progress
                or self.control.stop_durability_unresolved
                or self.control.activation_error is not None
            ):
                return self._control_refusal(session_id, "REFUSED_GLOBAL_MUTATION_DISABLED")
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
                payload={"authority_reconciliation_required": bool(session.current_run_id)},
            )
            return {"status": target.value, "session": self.snapshot(session_id)}

    def record_message(self, session_id: str, provenance: AgentProvenance, text: str) -> dict[str, object]:
        if type(provenance) is not AgentProvenance:
            raise ValidationError("INVALID_PROVENANCE", "message provenance is invalid")
        if not isinstance(text, str) or not text.strip():
            raise ValidationError("INVALID_MESSAGE", "message text must be non-empty")
        ensure_no_secret_material(text, key_path="agent_message")
        token = text.strip().upper()
        if provenance is AgentProvenance.OWNER and token in OwnerControlCommand._value2member_map_:
            return self.owner_control(session_id, OwnerControlCommand(token))
        encoded = text.encode("utf-8", "strict")
        with self._lock:
            self._persist_event(
                session_id,
                provenance=provenance,
                kind="MESSAGE_RECORDED",
                payload={
                    "message_sha256": hashlib.sha256(encoded).hexdigest(),
                    "message_bytes": len(encoded),
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
        state = self.ensure_session(session_id).operational_state
        if receipt.status == "PERFORMED_UNKNOWN":
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
        if receipt.performed:
            self._action_counts[session_id] = self._action_counts.get(session_id, 0) + 1
        refs = self._evidence_refs.setdefault(session_id, [])
        refs.extend(ref for ref in receipt.evidence_refs if ref not in refs)
        return receipt

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
        with self._lock:
            duplicate = self._receipts.get((session_id, action_id))
            if duplicate is not None:
                return duplicate
            session = self.ensure_session(session_id)
            task = self._tasks.get(session_id)
            if task is None:
                return self._refuse_action(session_id, action_id, action, provenance, "REFUSED_TASK_MISSING")
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
            count = self._action_counts.get(session_id, 0)
            if count >= task.physical_action_budget:
                return self._refuse_action(session_id, action_id, action, provenance, "REFUSED_BUDGET_EXHAUSTED")
            attempts = self._attempts.get(session_id, 0)
            if attempts >= task.max_attempts:
                return self._refuse_action(session_id, action_id, action, provenance, "REFUSED_ATTEMPTS_EXHAUSTED")
            if self._now_epoch_ms() >= task.deadline_epoch_ms:
                return self._refuse_action(session_id, action_id, action, provenance, "REFUSED_DEADLINE_EXPIRED")

            request = AgentActionRequest(
                action_id=action_id,
                session_id=session_id,
                run_id=task.run_id,
                action=action,
                expected_source_states=expected_source_states,
                remaining_budget=task.physical_action_budget - count,
                deadline_epoch_ms=task.deadline_epoch_ms,
                secret_capability_ref=task.secret_capability_ref,
            )
            self._persist_event(
                session_id,
                provenance=AgentProvenance.SUPERVISOR,
                kind="ACTION_RESERVED",
                action_id=action_id,
                payload={
                    "action": action.value,
                    "remaining_budget": request.remaining_budget,
                    "attempt_index": attempts + 1,
                },
            )
            self._attempts[session_id] = attempts + 1
            # The safety state is checked again immediately before crossing the
            # executor boundary, while this coordinator's serialization lock is held.
            if not self.control.mutation_admission_allowed():
                return self._record_action_receipt(
                    session_id, action, self._zero_receipt(action_id, "NOT_PERFORMED_SYSTEM_STATE_CHANGED")
                )
            try:
                received = self.executor.execute(request)
            except Exception:  # noqa: BLE001 -- exception occurred before any receipt/effect claim
                received = AgentActionReceipt(action_id, "NOT_PERFORMED", False, True, 0, ())
            receipt = self._validated_receipt(action_id, received)
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
                    action_count=self._action_counts.get(session_id, 0),
                    physical_action_budget=task.physical_action_budget,
                    evidence_manifest_sha256=evidence_manifest_sha256,
                    unresolved_conflicts=tuple(unresolved_conflicts),
                )
            if type(result) is not ResultEnvelope:
                raise ValidationError("INVALID_RESULT", "result must be an exact ResultEnvelope")
            if session_id in self._inconclusive:
                conflicts = tuple(result.unresolved_conflicts)
                if "PERFORMED_UNKNOWN" not in conflicts:
                    conflicts += ("PERFORMED_UNKNOWN",)
                result = replace(result, status=ResultStatus.INCONCLUSIVE, unresolved_conflicts=conflicts)
            existing = self._results.get(session_id)
            self.store.finish_agent_task(task.idempotency_key, result)
            if existing is not None:
                if existing != result:
                    raise ValidationError("IDEMPOTENCY_CONFLICT", "agent task result is already bound")
                return existing
            self._results[session_id] = result
            self._persist_event(
                session_id,
                provenance=AgentProvenance.SYSTEM,
                kind="RUN_COMPLETED",
                state_after=AgentOperationalState.TERMINAL,
                artifact_refs=(result.evidence_manifest_sha256,),
                payload={
                    "status": result.status.value,
                    "action_count": result.action_count,
                    "physical_action_budget": result.physical_action_budget,
                    "unresolved_conflicts": result.unresolved_conflicts,
                },
            )
            return result

    def snapshot(self, session_id: str) -> dict[str, object]:
        with self._lock:
            session = self.ensure_session(session_id)
            task = self._tasks.get(session_id)
            result = self._results.get(session_id)
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
                "remaining_physical_action_budget": 0 if task is None else max(
                    0, task.physical_action_budget - self._action_counts.get(session_id, 0)
                ),
                "attempt_count": self._attempts.get(session_id, 0),
                "max_attempts": 0 if task is None else task.max_attempts,
                "run_status": "INCONCLUSIVE" if session_id in self._inconclusive else (
                    None if result is None else result.status.value
                ),
                "result": None if result is None else _jsonable(asdict(result)),
                "evidence_refs": list(self._evidence_refs.get(session_id, [])),
                "events": events,
                "executor": "NULL" if isinstance(self.executor, NullBoundedActionExecutor) else "INJECTED_TEST",
                "mutation_authority": "NONE",
                "official_client_access": "NONE",
            }

    def foundation_status(self) -> dict[str, object]:
        """Secret-safe aggregate used by the existing Package B status document."""
        return {
            "state": "FOUNDATION",
            "runtime_access": "none",
            "executor": "NULL" if isinstance(self.executor, NullBoundedActionExecutor) else "INJECTED_TEST",
            "mutation_authority": "NONE",
            "official_client_access": "NONE",
            "physical_action_budget": 0,
            "physical_action_count": 0,
        }
