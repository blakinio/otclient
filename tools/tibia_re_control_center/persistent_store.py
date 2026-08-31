from __future__ import annotations

import copy
import hashlib
import json
import os
import sqlite3
import threading
from collections.abc import Mapping
from contextlib import contextmanager
from dataclasses import asdict, dataclass, replace
from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Any

from .canonical import jcs_dumps
from .agent_protocol import (
    AgentEvent,
    AgentOperationalState,
    AgentProvenance,
    AgentSessionRecord,
    ResultEnvelope,
    ResultStatus,
    TaskEnvelope,
)
from .model import (
    ActionLedgerRecord,
    BudgetDimension,
    BudgetLedger,
    Confirmation,
    ControlState,
    DispatchState,
    DurabilityError,
    DurabilityTimeout,
    EffectBound,
    LifecycleState,
    MAX_SAFE_INTEGER,
    ValidationError,
    checked_non_negative,
    require_exact_keys,
    validate_opaque_id,
)
from .recorder import ensure_no_secret_material


def _ensure_persistable(value: Any, *, key_path: str = "payload") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = str(key).lower()
            if normalized == "private_chat" and child in {"OMIT", "REDACT"}:
                continue
            if normalized == "secret_material" and child == "REJECT":
                continue
            if normalized in {
                "password", "passwd", "2fa", "otp", "auth_token", "access_token",
                "refresh_token", "session_token", "cookie", "cookies", "authorization",
                "control_nonce", "api_key", "private_key", "secret", "credential",
                "credentials", "ticket", "private_message", "raw_chat",
            } or normalized.endswith(("_password", "_token", "_nonce")):
                raise ValidationError("SECRET_MATERIAL_REJECTED", f"secret-class field rejected at {key_path}")
            _ensure_persistable(child, key_path=f"{key_path}.{key}")
        return
    if isinstance(value, (list, tuple)):
        for child in value:
            _ensure_persistable(child, key_path=key_path)
        return
    if isinstance(value, str):
        ensure_no_secret_material(value, key_path=key_path)


REQUEST_STATUSES = {"ACCEPTED", "COMPLETED", "FAILED"}


@dataclass(frozen=True)
class RequestLedgerRecord:
    request_id: str
    request_hash: str
    backend_epoch_created: str
    operation: str
    resource_id: str
    status: str
    result_status: str | None = None
    result_control_generation: int | None = None
    result_ref: str | None = None
    response_code: int | None = None
    response_body_hash: str | None = None
    response_body: dict[str, Any] | None = None
    created_monotonic_ns: int = 0
    updated_monotonic_ns: int = 0
    schema_version: int = 1

    def __post_init__(self) -> None:
        if self.status not in REQUEST_STATUSES:
            raise ValidationError("REQUEST_STATUS_INVALID", "RequestLedger status is invalid")


def _jsonable(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return {str(key): _jsonable(child) for key, child in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(child) for child in value]
    return value


def _dump(value: Any) -> str:
    return jcs_dumps(_jsonable(value))


def _load(text: str) -> Any:
    try:
        return json.loads(text)
    except (TypeError, json.JSONDecodeError) as exc:
        raise ValidationError("PERSISTENT_STATE_CORRUPT", "persistent Control Center state is corrupt") from exc


def _effect_from(value: dict[str, Any]) -> EffectBound:
    data = dict(value)
    data["reason_codes"] = tuple(data.get("reason_codes") or ())
    return EffectBound(**data)


def _action_from(value: dict[str, Any]) -> ActionLedgerRecord:
    data = dict(value)
    data["lifecycle_state"] = LifecycleState(data["lifecycle_state"])
    data["dispatch_state"] = DispatchState(data["dispatch_state"])
    data["authoritative_confirmation"] = Confirmation(data["authoritative_confirmation"])
    data["effect_bound"] = _effect_from(data["effect_bound"])
    return ActionLedgerRecord(**data)


def _budget_from(value: dict[str, Any]) -> BudgetLedger:
    return BudgetLedger(
        run_id=value["run_id"],
        limit_seconds=int(value["limit_seconds"]),
        started_monotonic_ns=int(value["started_monotonic_ns"]),
        deadline_monotonic_ns=int(value["deadline_monotonic_ns"]),
        dimensions={name: BudgetDimension(**item) for name, item in value["dimensions"].items()},
        expired=bool(value.get("expired", False)),
        updated_monotonic_ns=int(value.get("updated_monotonic_ns", 0)),
        reservations={name: _effect_from(item) for name, item in value.get("reservations", {}).items()},
        schema_version=int(value.get("schema_version", 1)),
    )


def _budget_obj(ledger: BudgetLedger) -> dict[str, Any]:
    return {
        "run_id": ledger.run_id,
        "limit_seconds": ledger.limit_seconds,
        "started_monotonic_ns": ledger.started_monotonic_ns,
        "deadline_monotonic_ns": ledger.deadline_monotonic_ns,
        "dimensions": {name: asdict(item) for name, item in ledger.dimensions.items()},
        "expired": ledger.expired,
        "updated_monotonic_ns": ledger.updated_monotonic_ns,
        "reservations": {name: item.as_dict() for name, item in ledger.reservations.items()},
        "schema_version": ledger.schema_version,
    }


_TASK_SCHEMA = "otclient.local-agent.task.v1"
_EVENT_SCHEMA = "otclient.local-agent.event.v1"
_RESULT_SCHEMA = "otclient.local-agent.result.v1"


def _agent_session_obj(record: AgentSessionRecord) -> dict[str, Any]:
    return asdict(record)


def _agent_session_from(value: Mapping[str, Any]) -> AgentSessionRecord:
    if type(value) is not dict:
        raise TypeError("session body must be an object")
    require_exact_keys(value, (
        "session_id", "operational_state", "current_run_id", "last_event_seq",
        "pause_latched", "stop_latched", "heartbeat_epoch_ms",
    ))
    current_run_id = value["current_run_id"]
    if current_run_id is not None:
        current_run_id = validate_opaque_id(current_run_id, field_name="current_run_id")
    heartbeat_epoch_ms = value["heartbeat_epoch_ms"]
    if heartbeat_epoch_ms is not None:
        if isinstance(heartbeat_epoch_ms, bool):
            raise TypeError("heartbeat must be an integer")
        heartbeat_epoch_ms = checked_non_negative(
            heartbeat_epoch_ms, maximum=MAX_SAFE_INTEGER, field_name="heartbeat_epoch_ms"
        )
    last_event_seq = value["last_event_seq"]
    if isinstance(last_event_seq, bool):
        raise TypeError("last event sequence must be an integer")
    if type(value["pause_latched"]) is not bool or type(value["stop_latched"]) is not bool:
        raise TypeError("latches must be booleans")
    return AgentSessionRecord(
        session_id=validate_opaque_id(value["session_id"], field_name="session_id"),
        operational_state=AgentOperationalState(value["operational_state"]),
        current_run_id=current_run_id,
        last_event_seq=checked_non_negative(last_event_seq, maximum=MAX_SAFE_INTEGER, field_name="last_event_seq"),
        pause_latched=value["pause_latched"],
        stop_latched=value["stop_latched"],
        heartbeat_epoch_ms=heartbeat_epoch_ms,
    )


def _task_obj(envelope: TaskEnvelope) -> dict[str, Any]:
    return asdict(envelope)


def _canonical_task(envelope: TaskEnvelope) -> tuple[TaskEnvelope, dict[str, Any]]:
    parsed = TaskEnvelope.from_mapping(_task_obj(envelope))
    return parsed, _task_obj(parsed)


def _canonical_result(result: ResultEnvelope) -> dict[str, Any]:
    if result.schema != _RESULT_SCHEMA:
        raise ValidationError("INVALID_SCHEMA", "result schema is invalid")
    if isinstance(result.action_count, bool) or isinstance(result.physical_action_budget, bool):
        raise ValidationError("INVALID_FIELD", "result counters must be integers")
    validate_opaque_id(result.session_id, field_name="session_id")
    validate_opaque_id(result.run_id, field_name="run_id")
    checked_non_negative(result.action_count, maximum=MAX_SAFE_INTEGER, field_name="action_count")
    checked_non_negative(result.physical_action_budget, maximum=MAX_SAFE_INTEGER, field_name="physical_action_budget")
    if not isinstance(result.status, ResultStatus):
        raise ValidationError("INVALID_ENUM", "result status is invalid")
    if (not isinstance(result.trusted_main_sha, str) or len(result.trusted_main_sha) != 40
            or any(char not in "0123456789abcdef" for char in result.trusted_main_sha)):
        raise ValidationError("INVALID_SHA1", "result trusted main SHA is invalid")
    if (not isinstance(result.evidence_manifest_sha256, str) or len(result.evidence_manifest_sha256) != 64
            or any(char not in "0123456789abcdef" for char in result.evidence_manifest_sha256)):
        raise ValidationError("INVALID_SHA256", "result evidence manifest SHA is invalid")
    if not isinstance(result.final_state, str) or not result.final_state:
        raise ValidationError("INVALID_FIELD", "result final state is invalid")
    if not isinstance(result.unresolved_conflicts, (list, tuple)) or any(
            not isinstance(item, str) or not item for item in result.unresolved_conflicts):
        raise ValidationError("INVALID_FIELD", "result conflicts are invalid")
    return asdict(result)


def _result_from(value: Mapping[str, Any]) -> ResultEnvelope:
    if type(value) is not dict:
        raise TypeError("result body must be an object")
    require_exact_keys(value, (
        "schema", "session_id", "run_id", "status", "trusted_main_sha", "final_state",
        "action_count", "physical_action_budget", "evidence_manifest_sha256", "unresolved_conflicts",
    ))
    if value["schema"] != _RESULT_SCHEMA:
        raise ValueError("result schema is invalid")
    if not isinstance(value["unresolved_conflicts"], list):
        raise TypeError("result conflicts must be a list")
    result = ResultEnvelope(
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
    _canonical_result(result)
    return result


def _agent_event_obj(event: AgentEvent, *, seq: int) -> dict[str, Any]:
    return {
        "schema": event.schema,
        "session_id": event.session_id,
        "run_id": event.run_id,
        "seq": seq,
        "observed_epoch_ms": event.observed_epoch_ms,
        "provenance": event.provenance,
        "kind": event.kind,
        "state_before": event.state_before,
        "state_after": event.state_after,
        "artifact_refs": event.artifact_refs,
        "action_id": event.action_id,
        "payload": event.payload,
    }


def _agent_event_from(value: Mapping[str, Any]) -> AgentEvent:
    data = dict(value)
    if data.get("schema") != _EVENT_SCHEMA:
        raise ValidationError("PERSISTENT_STATE_CORRUPT", "persistent agent event schema is invalid")
    data["provenance"] = AgentProvenance(data["provenance"])
    data["artifact_refs"] = tuple(data["artifact_refs"])
    data["payload"] = dict(data["payload"])
    return AgentEvent(**data)


_DURABLE_AGENT_DATA_ERRORS = (ValidationError, ValueError, TypeError, KeyError, UnicodeError, OverflowError)


def _persistent_agent_corruption() -> ValidationError:
    return ValidationError("PERSISTENT_STATE_CORRUPT", "persistent agent row is corrupt")


def _validated_agent_session_record(record: AgentSessionRecord) -> AgentSessionRecord:
    if type(record) is not AgentSessionRecord:
        raise ValidationError("INVALID_FIELD", "agent session record is invalid")
    try:
        return _agent_session_from(_agent_session_obj(record))
    except ValidationError:
        raise
    except ValueError:
        raise ValidationError("INVALID_ENUM", "agent session state is invalid") from None
    except (TypeError, KeyError, UnicodeError, OverflowError):
        raise ValidationError("INVALID_FIELD", "agent session record is invalid") from None


def _validated_agent_event(event: AgentEvent) -> AgentEvent:
    if type(event) is not AgentEvent:
        raise ValidationError("INVALID_FIELD", "agent event is invalid")
    if event.schema != _EVENT_SCHEMA:
        raise ValidationError("INVALID_SCHEMA", "agent event schema is invalid")
    if type(event.seq) is not int or event.seq != 0:
        raise ValidationError("INVALID_INTEGER", "agent event sequence must be unallocated")
    validate_opaque_id(event.session_id, field_name="session_id")
    if event.run_id is not None:
        validate_opaque_id(event.run_id, field_name="run_id")
    if type(event.provenance) is not AgentProvenance:
        raise ValidationError("INVALID_ENUM", "agent event provenance is invalid")
    checked_non_negative(event.observed_epoch_ms, maximum=MAX_SAFE_INTEGER, field_name="observed_epoch_ms")
    for value, field in ((event.kind, "kind"), (event.state_before, "state_before"), (event.state_after, "state_after")):
        if not isinstance(value, str) or not value:
            raise ValidationError("INVALID_FIELD", f"agent event {field} is invalid")
    if type(event.artifact_refs) is not tuple:
        raise ValidationError("INVALID_FIELD", "agent event artifact references must be a tuple")
    for artifact_ref in event.artifact_refs:
        validate_opaque_id(artifact_ref, field_name="artifact_ref")
    if event.action_id is not None:
        validate_opaque_id(event.action_id, field_name="action_id")
    if type(event.payload) is not MappingProxyType:
        raise ValidationError("INVALID_FIELD", "agent event payload must be immutable")
    prospective = _agent_event_obj(event, seq=0)
    _ensure_persistable(prospective, key_path="agent_event")
    try:
        return _agent_event_from(_load(_dump(prospective)))
    except ValidationError:
        raise
    except (ValueError, TypeError, KeyError, UnicodeError, OverflowError):
        raise ValidationError("INVALID_FIELD", "agent event is invalid") from None


def _checked_agent_session(row: Any, requested_session_id: str) -> AgentSessionRecord:
    try:
        if not isinstance(row, tuple) or len(row) != 2:
            raise TypeError("invalid session row")
        row_session_id, body = row
        if not isinstance(row_session_id, str) or not isinstance(body, str):
            raise TypeError("invalid session row values")
        record = _agent_session_from(_load(body))
        if requested_session_id != row_session_id or record.session_id != row_session_id:
            raise ValueError("session identity mismatch")
        if body != _dump(_agent_session_obj(record)):
            raise ValueError("session body is not canonical")
        return record
    except _DURABLE_AGENT_DATA_ERRORS:
        pass
    raise _persistent_agent_corruption()


def _checked_agent_task_row(
    row: Any, requested_idempotency_key: str,
) -> tuple[TaskEnvelope, dict[str, Any], ResultEnvelope | None, dict[str, Any] | None]:
    try:
        if not isinstance(row, tuple) or len(row) != 6:
            raise TypeError("invalid task row")
        idempotency_key, session_id, run_id, envelope_hash, body, result_body = row
        if (not all(isinstance(item, str) for item in (idempotency_key, session_id, run_id, envelope_hash, body))
                or result_body is not None and not isinstance(result_body, str)):
            raise TypeError("invalid task row values")
        envelope = TaskEnvelope.from_mapping(_load(body))
        _, canonical_envelope = _canonical_task(envelope)
        canonical_body = _dump(canonical_envelope)
        canonical_hash = hashlib.sha256(canonical_body.encode("utf-8")).hexdigest()
        if (requested_idempotency_key != idempotency_key or envelope.idempotency_key != idempotency_key
                or envelope.session_id != session_id or envelope.run_id != run_id
                or body != canonical_body or envelope_hash != canonical_hash):
            raise ValueError("task identity or canonical form mismatch")
        parsed_result = None
        canonical_result = None
        if result_body is not None:
            parsed_result = _result_from(_load(result_body))
            canonical_result = _canonical_result(parsed_result)
            if (result_body != _dump(canonical_result)
                    or parsed_result.session_id != envelope.session_id
                    or parsed_result.run_id != envelope.run_id
                    or parsed_result.trusted_main_sha != envelope.trusted_main_sha):
                raise ValueError("result identity or canonical form mismatch")
        return envelope, canonical_envelope, parsed_result, canonical_result
    except _DURABLE_AGENT_DATA_ERRORS:
        pass
    raise _persistent_agent_corruption()


class SQLitePersistentStore:
    """Artifact-v1 safety/request store backed by one local SQLite transaction domain."""

    def __init__(self, root: str | Path, *, event_retention: int = 4096) -> None:
        self.root = Path(root).expanduser().resolve()
        self.control_dir = self.root / "control"
        self.control_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.control_dir / "control-center.sqlite3"
        self._lock = threading.RLock()
        self._transaction_depth = 0
        self._faults: dict[str, list[str]] = {}
        self.safety_flush_count = 0
        self.event_retention = max(32, min(int(event_retention), 100_000))
        self._db = sqlite3.connect(self.db_path, check_same_thread=False, isolation_level=None)
        self._db.execute("PRAGMA journal_mode=WAL")
        self._db.execute("PRAGMA synchronous=FULL")
        self._db.execute("PRAGMA foreign_keys=ON")
        self._create_schema()
        try:
            os.chmod(self.db_path, 0o600)
        except OSError:
            pass
        self.initialized = self._meta("initialized") == "1"
        self.control_state = self._load_control_state_unchecked()
        self.action_ledgers = self._load_actions()
        self.budget_ledgers = self._load_budgets()
        self.run_activation = self._load_run_activations()
        self.recovery_records = self._load_recoveries()

    def _create_schema(self) -> None:
        with self._lock:
            self._db.executescript("""
                CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS control_state (singleton INTEGER PRIMARY KEY CHECK(singleton=1), body TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS control_history (transition_id TEXT PRIMARY KEY, body TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS actions (action_id TEXT PRIMARY KEY, request_hash TEXT NOT NULL, run_id TEXT NOT NULL, body TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS budgets (run_id TEXT PRIMARY KEY, body TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS run_activation (run_id TEXT PRIMARY KEY, body TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS recovery (run_id TEXT PRIMARY KEY, body TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS requests (request_id TEXT PRIMARY KEY, body TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS request_claims (request_id TEXT PRIMARY KEY, resource_id TEXT NOT NULL UNIQUE);
                CREATE TABLE IF NOT EXISTS resources (resource_id TEXT PRIMARY KEY, request_id TEXT NOT NULL UNIQUE, operation TEXT NOT NULL, state TEXT NOT NULL, body TEXT NOT NULL, result TEXT);
                CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT, body TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS artifacts (run_id TEXT NOT NULL, path TEXT NOT NULL, sha256 TEXT NOT NULL, body BLOB NOT NULL, PRIMARY KEY(run_id,path));
                CREATE TABLE IF NOT EXISTS agent_sessions (session_id TEXT PRIMARY KEY, body TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS agent_tasks (idempotency_key TEXT PRIMARY KEY, session_id TEXT NOT NULL, run_id TEXT NOT NULL UNIQUE, envelope_hash TEXT NOT NULL, body TEXT NOT NULL, result TEXT);
            """)

    @contextmanager
    def _transaction(self, operation: str):
        with self._lock:
            if self._transaction_depth:
                savepoint = f"nested_{self._transaction_depth}"
                self._db.execute(f"SAVEPOINT {savepoint}")
                self._transaction_depth += 1
                try:
                    self._before_write(operation)
                    yield
                    self._db.execute(f"RELEASE SAVEPOINT {savepoint}")
                except Exception:
                    self._db.execute(f"ROLLBACK TO SAVEPOINT {savepoint}")
                    self._db.execute(f"RELEASE SAVEPOINT {savepoint}")
                    raise
                finally:
                    self._transaction_depth -= 1
                return
            self._db.execute("BEGIN IMMEDIATE")
            self._transaction_depth = 1
            try:
                self._before_write(operation)
                yield
                self._db.execute("COMMIT")
            except Exception:
                self._db.execute("ROLLBACK")
                raise
            finally:
                self._transaction_depth = 0

    @contextmanager
    def agent_resource_transaction(self):
        """One SQLite commit domain for an agent resource and its event/session result."""
        with self._transaction("agent_resource_domain"):
            yield

    def _write_control_state_locked(self, state: ControlState) -> None:
        body = _dump(asdict(state))
        self._db.execute(
            "INSERT INTO control_state(singleton,body) VALUES(1,?) "
            "ON CONFLICT(singleton) DO UPDATE SET body=excluded.body",
            (body,),
        )
        self._db.execute(
            "INSERT INTO control_history(transition_id,body) VALUES(?,?) "
            "ON CONFLICT(transition_id) DO NOTHING",
            (state.transition_id, body),
        )
        self._db.execute(
            "INSERT INTO meta(key,value) VALUES('initialized','1') "
            "ON CONFLICT(key) DO UPDATE SET value='1'"
        )

    def _write_agent_session_locked(self, record: AgentSessionRecord) -> None:
        self._db.execute(
            "INSERT INTO agent_sessions(session_id,body) VALUES(?,?) "
            "ON CONFLICT(session_id) DO UPDATE SET body=excluded.body",
            (record.session_id, _dump(_agent_session_obj(record))),
        )

    def _append_agent_event_locked(self, event: AgentEvent) -> AgentEvent:
        cursor = self._db.execute("INSERT INTO events(run_id,body) VALUES(?,?)", (event.run_id, "{}"))
        seq = int(cursor.lastrowid)
        if seq <= 0:
            raise DurabilityError("agent event sequence was not committed")
        self._before_write("agent_event_body")
        body = _dump(_agent_event_obj(event, seq=seq))
        cursor = self._db.execute("UPDATE events SET body=? WHERE seq=?", (body, seq))
        if cursor.rowcount != 1:
            raise DurabilityError("agent event body update did not persist")
        row = self._db.execute("SELECT MAX(seq) FROM events").fetchone()
        maximum = 0 if row is None or row[0] is None else int(row[0])
        cutoff = maximum - self.event_retention
        if cutoff > 0:
            self._db.execute("DELETE FROM events WHERE seq<=?", (cutoff,))
        return _agent_event_from(_load(body))

    def _fetchone(self, query: str, parameters: tuple[Any, ...] = ()) -> Any:
        with self._lock:
            return self._db.execute(query, parameters).fetchone()

    def _fetchall(self, query: str, parameters: tuple[Any, ...] = ()) -> list[Any]:
        with self._lock:
            return self._db.execute(query, parameters).fetchall()

    def _meta(self, key: str) -> str | None:
        row = self._fetchone("SELECT value FROM meta WHERE key=?", (key,))
        return None if row is None else str(row[0])

    def inject_fault(self, operation: str, kind: str = "error", *, count: int = 1) -> None:
        if kind not in {"error", "timeout"} or count < 1:
            raise ValueError("fault kind must be error/timeout and count >= 1")
        self._faults.setdefault(operation, []).extend([kind] * count)

    def clear_faults(self) -> None:
        self._faults.clear()

    def _before_write(self, operation: str) -> None:
        queue = self._faults.get(operation)
        if not queue:
            return
        kind = queue.pop(0)
        if not queue:
            self._faults.pop(operation, None)
        if kind == "timeout":
            raise DurabilityTimeout(f"durability timeout during {operation}")
        raise DurabilityError(f"durability failure during {operation}")

    def _load_control_state_unchecked(self) -> ControlState | None:
        row = self._fetchone("SELECT body FROM control_state WHERE singleton=1")
        return None if row is None else ControlState(**_load(row[0]))

    def load_control_state(self) -> ControlState | None:
        state = self._load_control_state_unchecked()
        if self.initialized and state is None:
            raise ValidationError("CONTROL_STATE_MISSING", "initialized store is missing authoritative ControlState")
        self.control_state = state
        return copy.deepcopy(state)

    def write_control_state(self, state: ControlState, *, operation: str = "control_state") -> None:
        with self._transaction(operation):
            self._write_control_state_locked(state)
        self.initialized = True
        self.control_state = copy.deepcopy(state)

    def load_control_transition(self, transition_id: str) -> ControlState | None:
        row = self._fetchone("SELECT body FROM control_history WHERE transition_id=?", (transition_id,))
        return None if row is None else ControlState(**_load(row[0]))

    def _load_actions(self) -> dict[str, ActionLedgerRecord]:
        return {row[0]: _action_from(_load(row[1])) for row in self._fetchall("SELECT action_id,body FROM actions")}

    def load_action(self, action_id: str) -> ActionLedgerRecord | None:
        row = self._fetchone("SELECT body FROM actions WHERE action_id=?", (action_id,))
        return None if row is None else _action_from(_load(row[0]))

    def write_action(self, record: ActionLedgerRecord, *, operation: str = "action") -> None:
        body = _dump(asdict(record))
        existing = self.load_action(record.action_id)
        if existing and existing.action_request_hash != record.action_request_hash:
            raise ValidationError("IDEMPOTENCY_CONFLICT", "action_id already exists with a different request hash")
        with self._transaction(operation):
            self._db.execute("INSERT INTO actions(action_id,request_hash,run_id,body) VALUES(?,?,?,?) ON CONFLICT(action_id) DO UPDATE SET body=excluded.body", (record.action_id, record.action_request_hash, record.run_id, body))
        self.action_ledgers[record.action_id] = copy.deepcopy(record)

    def list_actions_for_run(self, run_id: str) -> list[ActionLedgerRecord]:
        return [
            _action_from(_load(row[0]))
            for row in self._fetchall("SELECT body FROM actions WHERE run_id=? ORDER BY rowid", (run_id,))
        ]

    def atomic_reserve_action(
        self,
        record: ActionLedgerRecord,
        previous_ledger: BudgetLedger,
        reserved_ledger: BudgetLedger,
    ) -> tuple[ActionLedgerRecord, BudgetLedger, bool]:
        action_body = _dump(asdict(record))
        reserved_budget_body = _dump(_budget_obj(reserved_ledger))
        previous_budget_body = _dump(_budget_obj(previous_ledger))
        accepted = False
        durable_record = record
        durable_budget = reserved_ledger
        with self._transaction("action_reserve"):
            row = self._db.execute(
                "SELECT request_hash,run_id,body FROM actions WHERE action_id=?",
                (record.action_id,),
            ).fetchone()
            if row is not None:
                durable_record = _action_from(_load(row[2]))
                if row[0] != record.action_request_hash or durable_record.action_request_hash != record.action_request_hash:
                    raise ValidationError("IDEMPOTENCY_CONFLICT", "action_id already exists with a different request hash")
                budget_row = self._db.execute("SELECT body FROM budgets WHERE run_id=?", (row[1],)).fetchone()
                if budget_row is None:
                    raise ValidationError("BUDGET_LEDGER_MISSING", "action reservation requires its durable budget")
                durable_budget = _budget_from(_load(budget_row[0]))
            else:
                budget_row = self._db.execute(
                    "SELECT body FROM budgets WHERE run_id=?", (previous_ledger.run_id,)
                ).fetchone()
                if budget_row is None or budget_row[0] != previous_budget_body:
                    raise ValidationError("BUDGET_LEDGER_STALE", "action reservation budget changed concurrently")
                self._db.execute(
                    "INSERT INTO actions(action_id,request_hash,run_id,body) VALUES(?,?,?,?)",
                    (record.action_id, record.action_request_hash, record.run_id, action_body),
                )
                self._db.execute(
                    "UPDATE budgets SET body=? WHERE run_id=?",
                    (reserved_budget_body, reserved_ledger.run_id),
                )
                accepted = True
        self.action_ledgers[durable_record.action_id] = copy.deepcopy(durable_record)
        self.budget_ledgers[durable_budget.run_id] = durable_budget.clone()
        return durable_record, durable_budget, accepted

    def _load_budgets(self) -> dict[str, BudgetLedger]:
        return {row[0]: _budget_from(_load(row[1])) for row in self._fetchall("SELECT run_id,body FROM budgets")}

    def load_budget(self, run_id: str) -> BudgetLedger | None:
        row = self._fetchone("SELECT body FROM budgets WHERE run_id=?", (run_id,))
        return None if row is None else _budget_from(_load(row[0]))

    def write_budget(self, ledger: BudgetLedger, *, operation: str = "budget") -> None:
        body = _dump(_budget_obj(ledger))
        with self._transaction(operation):
            self._db.execute("INSERT INTO budgets(run_id,body) VALUES(?,?) ON CONFLICT(run_id) DO UPDATE SET body=excluded.body", (ledger.run_id, body))
        self.budget_ledgers[ledger.run_id] = ledger.clone()

    def _load_run_activations(self) -> dict[str, tuple[int, int]]:
        result: dict[str, tuple[int, int]] = {}
        for run_id, body in self._fetchall("SELECT run_id,body FROM run_activation"):
            value = _load(body)
            result[run_id] = (int(value["started_ns"]), int(value["deadline_ns"]))
        return result

    def persist_run_activation(self, run_id: str, started_ns: int, deadline_ns: int) -> None:
        existing = self.load_run_activation(run_id)
        if existing is not None and existing != (started_ns, deadline_ns):
            raise ValidationError("RUN_ACTIVATION_CONFLICT", "run activation/deadline is immutable")
        body = _dump({"started_ns": started_ns, "deadline_ns": deadline_ns})
        with self._transaction("run_activation"):
            self._db.execute("INSERT INTO run_activation(run_id,body) VALUES(?,?) ON CONFLICT(run_id) DO NOTHING", (run_id, body))
        self.run_activation[run_id] = (started_ns, deadline_ns)

    def load_run_activation(self, run_id: str) -> tuple[int, int] | None:
        row = self._fetchone("SELECT body FROM run_activation WHERE run_id=?", (run_id,))
        if row is None:
            return None
        value = _load(row[0])
        return int(value["started_ns"]), int(value["deadline_ns"])

    def _load_recoveries(self) -> dict[str, dict[str, Any]]:
        return {row[0]: _load(row[1]) for row in self._fetchall("SELECT run_id,body FROM recovery")}

    def write_recovery(self, run_id: str, record: dict[str, Any]) -> None:
        body = _dump(record)
        with self._transaction("recovery"):
            self._db.execute("INSERT INTO recovery(run_id,body) VALUES(?,?) ON CONFLICT(run_id) DO UPDATE SET body=excluded.body", (run_id, body))
        self.recovery_records[run_id] = copy.deepcopy(record)

    def load_recovery(self, run_id: str) -> dict[str, Any] | None:
        row = self._fetchone("SELECT body FROM recovery WHERE run_id=?", (run_id,))
        return None if row is None else _load(row[0])

    def atomic_dispatch_commit(self, record: ActionLedgerRecord, ledger: BudgetLedger) -> bool:
        action_body = _dump(asdict(record))
        budget_body = _dump(_budget_obj(ledger))
        committed = False
        with self._transaction("dispatch_commit"):
            row = self._db.execute(
                "SELECT request_hash,body FROM actions WHERE action_id=?", (record.action_id,)
            ).fetchone()
            if row is None:
                raise ValidationError("ACTION_LEDGER_MISSING", "dispatch commit requires a durable reservation")
            current = _action_from(_load(row[1]))
            if row[0] != record.action_request_hash or current.action_request_hash != record.action_request_hash:
                raise ValidationError("IDEMPOTENCY_CONFLICT", "action_id already exists with a different request hash")
            if current.dispatch_state == DispatchState.NOT_DISPATCHED:
                self._db.execute("UPDATE actions SET body=? WHERE action_id=?", (action_body, record.action_id))
                self._db.execute(
                    "INSERT INTO budgets(run_id,body) VALUES(?,?) ON CONFLICT(run_id) DO UPDATE SET body=excluded.body",
                    (ledger.run_id, budget_body),
                )
                committed = True
        if committed:
            self.action_ledgers[record.action_id] = copy.deepcopy(record)
            self.budget_ledgers[ledger.run_id] = ledger.clone()
        return committed

    def atomic_reconcile(self, record: ActionLedgerRecord, ledger: BudgetLedger) -> None:
        if self.load_action(record.action_id) is None:
            raise ValidationError("ACTION_LEDGER_MISSING", "cannot reconcile an unknown action")
        action_body = _dump(asdict(record))
        budget_body = _dump(_budget_obj(ledger))
        with self._transaction("reconcile"):
            self._db.execute("UPDATE actions SET body=? WHERE action_id=?", (action_body, record.action_id))
            self._db.execute("INSERT INTO budgets(run_id,body) VALUES(?,?) ON CONFLICT(run_id) DO UPDATE SET body=excluded.body", (ledger.run_id, budget_body))
        self.action_ledgers[record.action_id] = copy.deepcopy(record)
        self.budget_ledgers[ledger.run_id] = ledger.clone()

    def flush_safety_state(self) -> None:
        self._before_write("safety_flush")
        with self._lock:
            self._db.execute("PRAGMA wal_checkpoint(FULL)")
        self.safety_flush_count += 1

    def load_request(self, request_id: str) -> RequestLedgerRecord | None:
        row = self._fetchone("SELECT body FROM requests WHERE request_id=?", (request_id,))
        return None if row is None else RequestLedgerRecord(**_load(row[0]))

    def accept_request(self, record: RequestLedgerRecord) -> RequestLedgerRecord:
        body = _dump(asdict(record))
        with self._transaction("request_accept"):
            row = self._db.execute("SELECT body FROM requests WHERE request_id=?", (record.request_id,)).fetchone()
            if row is not None:
                return RequestLedgerRecord(**_load(row[0]))
            claim = self._db.execute("SELECT resource_id FROM request_claims WHERE request_id=?", (record.request_id,)).fetchone()
            if claim is not None:
                raise ValidationError("REQUEST_LEDGER_CONTRADICTION", "request claim exists without its RequestLedger record")
            self._db.execute("INSERT INTO requests(request_id,body) VALUES(?,?)", (record.request_id, body))
            self._db.execute("INSERT INTO request_claims(request_id,resource_id) VALUES(?,?)", (record.request_id, record.resource_id))
        return record

    def finish_request(self, record: RequestLedgerRecord) -> None:
        existing = self.load_request(record.request_id)
        if existing is None or existing.request_hash != record.request_hash or existing.resource_id != record.resource_id:
            raise ValidationError("REQUEST_LEDGER_CONTRADICTION", "request completion contradicts durable acceptance")
        _ensure_persistable(record.response_body or {}, key_path="request_response")
        with self._transaction("request_finish"):
            self._db.execute("UPDATE requests SET body=? WHERE request_id=?", (_dump(asdict(record)), record.request_id))

    def ensure_resource(self, resource_id: str, request_id: str, operation: str, body: dict[str, Any]) -> dict[str, Any]:
        existing = self.get_resource(resource_id)
        if existing is not None:
            if existing["request_id"] != request_id or existing["operation"] != operation:
                raise ValidationError("RESOURCE_ID_CONFLICT", "resource identity is already bound to another request")
            return existing
        ledger = self.load_request(request_id)
        if ledger is None or ledger.resource_id != resource_id:
            raise ValidationError("REQUEST_LEDGER_CONTRADICTION", "resource creation requires its durable accepted request")
        _ensure_persistable(body, key_path="resource")
        with self._transaction("resource_create"):
            self._db.execute("INSERT INTO resources(resource_id,request_id,operation,state,body,result) VALUES(?,?,?,?,?,NULL)", (resource_id, request_id, operation, "CREATED", _dump(body)))
        return self.get_resource(resource_id) or {}

    def get_resource(self, resource_id: str) -> dict[str, Any] | None:
        row = self._fetchone("SELECT request_id,operation,state,body,result FROM resources WHERE resource_id=?", (resource_id,))
        if row is None:
            return None
        return {"resource_id": resource_id, "request_id": row[0], "operation": row[1], "state": row[2], "body": _load(row[3]), "result": None if row[4] is None else _load(row[4])}

    def finish_resource(self, resource_id: str, state: str, result: dict[str, Any]) -> None:
        _ensure_persistable(result, key_path="resource_result")
        with self._transaction("resource_finish"):
            cursor = self._db.execute("UPDATE resources SET state=?,result=? WHERE resource_id=?", (state, _dump(result), resource_id))
            if cursor.rowcount != 1:
                raise ValidationError("RESOURCE_MISSING", "cannot finish an unknown resource")

    def list_run_resources(self, *, offset: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        rows = self._fetchall("SELECT resource_id FROM resources WHERE operation IN ('CREATE_RUN','ONE_STEP_EXPERIMENT') ORDER BY rowid DESC LIMIT ? OFFSET ?", (limit, offset))
        return [self.get_resource(row[0]) or {} for row in rows]

    def write_agent_session(self, record: AgentSessionRecord) -> None:
        validated = _validated_agent_session_record(record)
        body_obj = _agent_session_obj(validated)
        _ensure_persistable(body_obj, key_path="agent_session")
        with self._transaction("agent_session"):
            self._write_agent_session_locked(validated)

    def load_agent_session(self, session_id: str) -> AgentSessionRecord | None:
        row = self._fetchone(
            "SELECT session_id,body FROM agent_sessions WHERE session_id=?", (session_id,)
        )
        return None if row is None else _checked_agent_session(row, session_id)

    def atomic_agent_transition(
        self,
        record: AgentSessionRecord,
        event: AgentEvent,
        *,
        operation: str,
        control_state: ControlState | None = None,
    ) -> tuple[AgentSessionRecord, AgentEvent]:
        validated_record = _validated_agent_session_record(record)
        validated_event = _validated_agent_event(event)
        if validated_event.session_id != validated_record.session_id:
            raise ValidationError("AGENT_TRANSITION_MISMATCH", "agent event and session identities differ")
        if validated_event.state_after != validated_record.operational_state.value:
            raise ValidationError("AGENT_TRANSITION_MISMATCH", "agent event and session state differ")
        with self._transaction(operation):
            persisted = self._append_agent_event_locked(validated_event)
            durable_record = replace(validated_record, last_event_seq=persisted.seq)
            self._write_agent_session_locked(durable_record)
            if control_state is not None:
                self._write_control_state_locked(control_state)
        if control_state is not None:
            self.initialized = True
            self.control_state = copy.deepcopy(control_state)
        return durable_record, persisted

    def _agent_task_values(self, row: Any, idempotency_key: str) -> dict[str, object]:
        _, canonical_envelope, _, canonical_result = _checked_agent_task_row(row, idempotency_key)
        return {
            "envelope": _jsonable(canonical_envelope),
            "result": None if canonical_result is None else _jsonable(canonical_result),
        }

    def _validate_agent_result_counters_locked(
        self,
        task: TaskEnvelope,
        result: ResultEnvelope,
    ) -> None:
        budget_row = self._db.execute("SELECT body FROM budgets WHERE run_id=?", (task.run_id,)).fetchone()
        action_row = self._db.execute("SELECT COUNT(*) FROM actions WHERE run_id=?", (task.run_id,)).fetchone()
        action_rows = 0 if action_row is None else int(action_row[0])
        if budget_row is None:
            if action_rows:
                raise ValidationError("PERSISTENT_STATE_CORRUPT", "agent actions exist without their budget ledger")
            authoritative_count = 0
            authoritative_budget = task.physical_action_budget
        else:
            ledger = _budget_from(_load(budget_row[0]))
            dimension = ledger.dimensions.get("max_actions")
            if dimension is None:
                raise ValidationError("PERSISTENT_STATE_CORRUPT", "agent budget lacks max_actions")
            authoritative_count = dimension.at_risk + dimension.committed + dimension.uncertain
            authoritative_budget = dimension.limit
            if authoritative_budget != task.physical_action_budget:
                raise ValidationError("PERSISTENT_STATE_CORRUPT", "agent task budget contradicts action ledger")
        if result.action_count != authoritative_count or result.physical_action_budget != authoritative_budget:
            raise ValidationError("RESULT_COUNTER_MISMATCH", "agent result counters must match authoritative ledgers")

    def accept_agent_task(self, envelope: TaskEnvelope) -> dict[str, object]:
        parsed, canonical_envelope = _canonical_task(envelope)
        _ensure_persistable(canonical_envelope, key_path="agent_task")
        body = _dump(canonical_envelope)
        envelope_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
        with self._transaction("agent_task_accept"):
            row = self._db.execute(
                "SELECT idempotency_key,session_id,run_id,envelope_hash,body,result "
                "FROM agent_tasks WHERE idempotency_key=?",
                (parsed.idempotency_key,),
            ).fetchone()
            if row is not None:
                self._agent_task_values(row, parsed.idempotency_key)
                if row[3] != envelope_hash or row[4] != body:
                    raise ValidationError("IDEMPOTENCY_CONFLICT", "agent task idempotency key is already bound")
                return {"accepted_new": False, **self._agent_task_values(row, parsed.idempotency_key)}
            run_row = self._db.execute(
                "SELECT idempotency_key FROM agent_tasks WHERE run_id=?", (parsed.run_id,)
            ).fetchone()
            if run_row is not None:
                raise ValidationError("IDEMPOTENCY_CONFLICT", "agent task run is already bound")
            self._db.execute(
                "INSERT INTO agent_tasks(idempotency_key,session_id,run_id,envelope_hash,body,result) "
                "VALUES(?,?,?,?,?,NULL)",
                (parsed.idempotency_key, parsed.session_id, parsed.run_id, envelope_hash, body),
            )
        row = (parsed.idempotency_key, parsed.session_id, parsed.run_id, envelope_hash, body, None)
        return {"accepted_new": True, **self._agent_task_values(row, parsed.idempotency_key)}

    def accept_agent_task_transition(
        self,
        envelope: TaskEnvelope,
        record: AgentSessionRecord,
        event: AgentEvent,
    ) -> dict[str, object]:
        parsed, canonical_envelope = _canonical_task(envelope)
        validated_record = _validated_agent_session_record(record)
        validated_event = _validated_agent_event(event)
        if (
            parsed.session_id != validated_record.session_id
            or parsed.run_id != validated_record.current_run_id
            or validated_event.session_id != parsed.session_id
            or validated_event.run_id != parsed.run_id
            or validated_event.state_after != validated_record.operational_state.value
        ):
            raise ValidationError("AGENT_TRANSITION_MISMATCH", "task, event, and session transition differ")
        _ensure_persistable(canonical_envelope, key_path="agent_task")
        body = _dump(canonical_envelope)
        envelope_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
        with self._transaction("agent_task_accept_transition"):
            row = self._db.execute(
                "SELECT idempotency_key,session_id,run_id,envelope_hash,body,result "
                "FROM agent_tasks WHERE idempotency_key=?",
                (parsed.idempotency_key,),
            ).fetchone()
            if row is not None:
                self._agent_task_values(row, parsed.idempotency_key)
                if row[3] != envelope_hash or row[4] != body:
                    raise ValidationError("IDEMPOTENCY_CONFLICT", "agent task idempotency key is already bound")
                return {"accepted_new": False, **self._agent_task_values(row, parsed.idempotency_key)}
            run_row = self._db.execute(
                "SELECT idempotency_key FROM agent_tasks WHERE run_id=?", (parsed.run_id,)
            ).fetchone()
            if run_row is not None:
                raise ValidationError("IDEMPOTENCY_CONFLICT", "agent task run is already bound")
            self._db.execute(
                "INSERT INTO agent_tasks(idempotency_key,session_id,run_id,envelope_hash,body,result) "
                "VALUES(?,?,?,?,?,NULL)",
                (parsed.idempotency_key, parsed.session_id, parsed.run_id, envelope_hash, body),
            )
            persisted = self._append_agent_event_locked(validated_event)
            self._write_agent_session_locked(replace(validated_record, last_event_seq=persisted.seq))
        row = (parsed.idempotency_key, parsed.session_id, parsed.run_id, envelope_hash, body, None)
        return {"accepted_new": True, **self._agent_task_values(row, parsed.idempotency_key)}

    def load_agent_task(self, idempotency_key: str) -> dict[str, object] | None:
        row = self._fetchone(
            "SELECT idempotency_key,session_id,run_id,envelope_hash,body,result "
            "FROM agent_tasks WHERE idempotency_key=?", (idempotency_key,)
        )
        return None if row is None else self._agent_task_values(row, idempotency_key)

    def load_agent_task_for_session(self, session_id: str) -> dict[str, object] | None:
        row = self._fetchone(
            "SELECT idempotency_key,session_id,run_id,envelope_hash,body,result "
            "FROM agent_tasks WHERE session_id=? ORDER BY rowid DESC LIMIT 1",
            (session_id,),
        )
        return None if row is None else self._agent_task_values(row, row[0])

    def load_agent_task_for_run(self, run_id: str) -> dict[str, object] | None:
        validate_opaque_id(run_id, field_name="run_id")
        row = self._fetchone(
            "SELECT idempotency_key,session_id,run_id,envelope_hash,body,result "
            "FROM agent_tasks WHERE run_id=?",
            (run_id,),
        )
        return None if row is None else self._agent_task_values(row, row[0])

    def finish_agent_task(self, idempotency_key: str, result: ResultEnvelope) -> None:
        canonical_result = _canonical_result(result)
        _ensure_persistable(canonical_result, key_path="agent_result")
        result_body = _dump(canonical_result)
        with self._transaction("agent_task_finish"):
            row = self._db.execute(
                "SELECT idempotency_key,session_id,run_id,envelope_hash,body,result "
                "FROM agent_tasks WHERE idempotency_key=?", (idempotency_key,)
            ).fetchone()
            if row is None:
                raise ValidationError("AGENT_TASK_MISSING", "cannot finish an unknown agent task")
            task, _, _, _ = _checked_agent_task_row(row, idempotency_key)
            if (result.session_id != task.session_id or result.run_id != task.run_id
                    or result.trusted_main_sha != task.trusted_main_sha):
                raise ValidationError("TASK_RESULT_MISMATCH", "agent result does not match accepted task")
            self._validate_agent_result_counters_locked(task, result)
            if row[5] is None:
                self._db.execute(
                    "UPDATE agent_tasks SET result=? WHERE idempotency_key=?",
                    (result_body, idempotency_key),
                )
            elif row[5] != result_body:
                raise ValidationError("IDEMPOTENCY_CONFLICT", "agent task result is already bound")

    def finish_agent_task_transition(
        self,
        idempotency_key: str,
        result: ResultEnvelope,
        record: AgentSessionRecord,
        event: AgentEvent,
    ) -> None:
        canonical_result = _canonical_result(result)
        validated_record = _validated_agent_session_record(record)
        validated_event = _validated_agent_event(event)
        _ensure_persistable(canonical_result, key_path="agent_result")
        result_body = _dump(canonical_result)
        if (
            validated_record.session_id != result.session_id
            or validated_record.current_run_id != result.run_id
            or validated_event.session_id != result.session_id
            or validated_event.run_id != result.run_id
            or validated_event.state_after != validated_record.operational_state.value
        ):
            raise ValidationError("AGENT_TRANSITION_MISMATCH", "result, event, and session transition differ")
        with self._transaction("agent_task_finish_transition"):
            row = self._db.execute(
                "SELECT idempotency_key,session_id,run_id,envelope_hash,body,result "
                "FROM agent_tasks WHERE idempotency_key=?", (idempotency_key,)
            ).fetchone()
            if row is None:
                raise ValidationError("AGENT_TASK_MISSING", "cannot finish an unknown agent task")
            task, _, _, _ = _checked_agent_task_row(row, idempotency_key)
            if (
                result.session_id != task.session_id
                or result.run_id != task.run_id
                or result.trusted_main_sha != task.trusted_main_sha
            ):
                raise ValidationError("TASK_RESULT_MISMATCH", "agent result does not match accepted task")
            self._validate_agent_result_counters_locked(task, result)
            if row[5] is not None:
                if row[5] != result_body:
                    raise ValidationError("IDEMPOTENCY_CONFLICT", "agent task result is already bound")
                return
            self._db.execute(
                "UPDATE agent_tasks SET result=? WHERE idempotency_key=?",
                (result_body, idempotency_key),
            )
            persisted = self._append_agent_event_locked(validated_event)
            self._write_agent_session_locked(replace(validated_record, last_event_seq=persisted.seq))

    def append_agent_event(self, event: AgentEvent) -> AgentEvent:
        validated = _validated_agent_event(event)
        with self._transaction("agent_event"):
            return self._append_agent_event_locked(validated)

    def append_events(self, run_id: str, events: list[dict[str, Any]]) -> None:
        for event in events:
            _ensure_persistable(event, key_path="event")
        with self._transaction("events"):
            self._db.executemany("INSERT INTO events(run_id,body) VALUES(?,?)", [(run_id, _dump(event)) for event in events])
            row = self._db.execute("SELECT MAX(seq) FROM events").fetchone()
            maximum = 0 if row is None or row[0] is None else int(row[0])
            cutoff = maximum - self.event_retention
            if cutoff > 0:
                self._db.execute("DELETE FROM events WHERE seq<=?", (cutoff,))

    def list_events(self, *, cursor: int = 0, limit: int = 100) -> tuple[list[dict[str, Any]], int]:
        row = self._fetchone("SELECT MIN(seq),MAX(seq) FROM events")
        minimum = 0 if row is None or row[0] is None else int(row[0])
        maximum = 0 if row is None or row[1] is None else int(row[1])
        if cursor and minimum and cursor < minimum - 1:
            raise ValidationError("CONTROL_EVENT_BACKPRESSURE", "event cursor fell behind bounded retention; resynchronization is required")
        rows = self._fetchall("SELECT seq,body FROM events WHERE seq>? ORDER BY seq LIMIT ?", (cursor, limit))
        return [{"cursor": int(seq), **_load(body)} for seq, body in rows], maximum

    def persist_artifacts(self, run_id: str, files: dict[str, bytes], hashes: dict[str, str]) -> None:
        with self._transaction("artifacts"):
            for path, body in files.items():
                digest = hashes.get(path)
                if digest is None:
                    raise ValidationError("ARTIFACT_HASH_MISSING", "persisted artifact requires an exact hash")
                self._db.execute("INSERT INTO artifacts(run_id,path,sha256,body) VALUES(?,?,?,?) ON CONFLICT(run_id,path) DO UPDATE SET sha256=excluded.sha256,body=excluded.body", (run_id, path, digest, sqlite3.Binary(body)))

    def list_artifacts(self, run_id: str) -> list[dict[str, Any]]:
        return [{"path": path, "sha256": digest, "size": len(body)} for path, digest, body in self._fetchall("SELECT path,sha256,body FROM artifacts WHERE run_id=? ORDER BY path", (run_id,))]

    def snapshot(self) -> dict[str, Any]:
        return {"initialized": self.initialized, "control_state": self.load_control_state(), "actions": copy.deepcopy(self.action_ledgers), "budgets": {key: value.clone() for key, value in self.budget_ledgers.items()}, "run_activation": dict(self.run_activation), "recovery": copy.deepcopy(self.recovery_records)}

    def close(self) -> None:
        with self._lock:
            self._db.close()
