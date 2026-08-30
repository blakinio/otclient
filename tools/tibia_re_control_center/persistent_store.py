from __future__ import annotations

import copy
import hashlib
import json
import os
import sqlite3
import threading
from collections.abc import Mapping
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
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
    ValidationError,
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
    data = dict(value)
    data["operational_state"] = AgentOperationalState(data["operational_state"])
    return AgentSessionRecord(**data)


def _task_obj(envelope: TaskEnvelope) -> dict[str, Any]:
    return asdict(envelope)


def _canonical_task(envelope: TaskEnvelope) -> tuple[TaskEnvelope, dict[str, Any]]:
    parsed = TaskEnvelope.from_mapping(_task_obj(envelope))
    return parsed, _task_obj(parsed)


def _canonical_result(result: ResultEnvelope) -> dict[str, Any]:
    if result.schema != _RESULT_SCHEMA:
        raise ValidationError("INVALID_SCHEMA", "result schema is invalid")
    return asdict(result)


def _result_from(value: Mapping[str, Any]) -> ResultEnvelope:
    data = dict(value)
    if data.get("schema") != _RESULT_SCHEMA:
        raise ValidationError("PERSISTENT_STATE_CORRUPT", "persistent agent result schema is invalid")
    data["status"] = ResultStatus(data["status"])
    data["unresolved_conflicts"] = tuple(data["unresolved_conflicts"])
    return ResultEnvelope(**data)


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


class SQLitePersistentStore:
    """Artifact-v1 safety/request store backed by one local SQLite transaction domain."""

    def __init__(self, root: str | Path, *, event_retention: int = 4096) -> None:
        self.root = Path(root).expanduser().resolve()
        self.control_dir = self.root / "control"
        self.control_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.control_dir / "control-center.sqlite3"
        self._lock = threading.RLock()
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
            self._db.execute("BEGIN IMMEDIATE")
            try:
                self._before_write(operation)
                yield
                self._db.execute("COMMIT")
            except Exception:
                self._db.execute("ROLLBACK")
                raise

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
        body = _dump(asdict(state))
        with self._transaction(operation):
            self._db.execute("INSERT INTO control_state(singleton,body) VALUES(1,?) ON CONFLICT(singleton) DO UPDATE SET body=excluded.body", (body,))
            self._db.execute("INSERT INTO control_history(transition_id,body) VALUES(?,?) ON CONFLICT(transition_id) DO NOTHING", (state.transition_id, body))
            self._db.execute("INSERT INTO meta(key,value) VALUES('initialized','1') ON CONFLICT(key) DO UPDATE SET value='1'")
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

    def atomic_dispatch_commit(self, record: ActionLedgerRecord, ledger: BudgetLedger) -> None:
        action_body = _dump(asdict(record))
        budget_body = _dump(_budget_obj(ledger))
        with self._transaction("dispatch_commit"):
            self._db.execute("INSERT INTO actions(action_id,request_hash,run_id,body) VALUES(?,?,?,?) ON CONFLICT(action_id) DO UPDATE SET body=excluded.body", (record.action_id, record.action_request_hash, record.run_id, action_body))
            self._db.execute("INSERT INTO budgets(run_id,body) VALUES(?,?) ON CONFLICT(run_id) DO UPDATE SET body=excluded.body", (ledger.run_id, budget_body))
        self.action_ledgers[record.action_id] = copy.deepcopy(record)
        self.budget_ledgers[ledger.run_id] = ledger.clone()

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
        body_obj = _agent_session_obj(record)
        _ensure_persistable(body_obj, key_path="agent_session")
        with self._transaction("agent_session"):
            self._db.execute(
                "INSERT INTO agent_sessions(session_id,body) VALUES(?,?) "
                "ON CONFLICT(session_id) DO UPDATE SET body=excluded.body",
                (record.session_id, _dump(body_obj)),
            )

    def load_agent_session(self, session_id: str) -> AgentSessionRecord | None:
        row = self._fetchone("SELECT body FROM agent_sessions WHERE session_id=?", (session_id,))
        return None if row is None else _agent_session_from(_load(row[0]))

    def _agent_task_values(self, body: str, result: str | None) -> dict[str, object]:
        _, canonical_envelope = _canonical_task(TaskEnvelope.from_mapping(_load(body)))
        canonical_result = None
        if result is not None:
            parsed_result = _result_from(_load(result))
            canonical_result = _canonical_result(parsed_result)
        return {
            "envelope": _jsonable(canonical_envelope),
            "result": None if canonical_result is None else _jsonable(canonical_result),
        }

    def accept_agent_task(self, envelope: TaskEnvelope) -> dict[str, object]:
        parsed, canonical_envelope = _canonical_task(envelope)
        _ensure_persistable(canonical_envelope, key_path="agent_task")
        body = _dump(canonical_envelope)
        envelope_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
        with self._transaction("agent_task_accept"):
            row = self._db.execute(
                "SELECT envelope_hash,body,result FROM agent_tasks WHERE idempotency_key=?",
                (parsed.idempotency_key,),
            ).fetchone()
            if row is not None:
                if row[0] != envelope_hash or row[1] != body:
                    raise ValidationError("IDEMPOTENCY_CONFLICT", "agent task idempotency key is already bound")
                return {"accepted_new": False, **self._agent_task_values(row[1], row[2])}
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
        return {"accepted_new": True, **self._agent_task_values(body, None)}

    def load_agent_task(self, idempotency_key: str) -> dict[str, object] | None:
        row = self._fetchone(
            "SELECT body,result FROM agent_tasks WHERE idempotency_key=?", (idempotency_key,)
        )
        return None if row is None else self._agent_task_values(row[0], row[1])

    def finish_agent_task(self, idempotency_key: str, result: ResultEnvelope) -> None:
        canonical_result = _canonical_result(result)
        _ensure_persistable(canonical_result, key_path="agent_result")
        result_body = _dump(canonical_result)
        with self._transaction("agent_task_finish"):
            row = self._db.execute(
                "SELECT body,result FROM agent_tasks WHERE idempotency_key=?", (idempotency_key,)
            ).fetchone()
            if row is None:
                raise ValidationError("AGENT_TASK_MISSING", "cannot finish an unknown agent task")
            task = TaskEnvelope.from_mapping(_load(row[0]))
            if (result.session_id != task.session_id or result.run_id != task.run_id
                    or result.trusted_main_sha != task.trusted_main_sha):
                raise ValidationError("TASK_RESULT_MISMATCH", "agent result does not match accepted task")
            if row[1] is None:
                self._db.execute(
                    "UPDATE agent_tasks SET result=? WHERE idempotency_key=?",
                    (result_body, idempotency_key),
                )
            elif row[1] != result_body:
                raise ValidationError("IDEMPOTENCY_CONFLICT", "agent task result is already bound")

    def append_agent_event(self, event: AgentEvent) -> AgentEvent:
        if event.schema != _EVENT_SCHEMA:
            raise ValidationError("INVALID_SCHEMA", "agent event schema is invalid")
        prospective = _agent_event_obj(event, seq=0)
        _ensure_persistable(prospective, key_path="agent_event")
        with self._transaction("agent_event"):
            cursor = self._db.execute("INSERT INTO events(run_id,body) VALUES(?,?)", (event.run_id, "{}"))
            seq = int(cursor.lastrowid)
            if seq <= 0:
                raise DurabilityError("agent event sequence was not committed")
            body_obj = _agent_event_obj(event, seq=seq)
            body = _dump(body_obj)
            self._db.execute("UPDATE events SET body=? WHERE seq=?", (body, seq))
            row = self._db.execute("SELECT MAX(seq) FROM events").fetchone()
            maximum = 0 if row is None or row[0] is None else int(row[0])
            cutoff = maximum - self.event_retention
            if cutoff > 0:
                self._db.execute("DELETE FROM events WHERE seq<=?", (cutoff,))
        return _agent_event_from(_load(body))

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
