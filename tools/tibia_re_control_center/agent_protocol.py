"""Strict, authority-neutral protocol types for the local vision agent."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from math import isfinite
from types import MappingProxyType
from typing import Any, cast

from .model import (
    MAX_SAFE_INTEGER,
    ValidationError,
    checked_non_negative,
    require_exact_keys,
    validate_opaque_id,
)


class AgentOperationalState(str, Enum):
    OFFLINE = "OFFLINE"
    IDLE = "IDLE"
    OBSERVING = "OBSERVING"
    RUNNING = "RUNNING"
    WAITING_MODEL_SLOT = "WAITING_MODEL_SLOT"
    PAUSED = "PAUSED"
    PAUSED_AUTHORITY = "PAUSED_AUTHORITY"
    DEGRADED = "DEGRADED"
    STOPPED = "STOPPED"
    TERMINAL = "TERMINAL"


class AgentProvenance(str, Enum):
    OWNER = "OWNER"
    SUPERVISOR = "SUPERVISOR"
    SYSTEM = "SYSTEM"
    MODEL = "MODEL"
    SENSOR = "SENSOR"
    RUNTIME = "RUNTIME"


class AgentVisualState(str, Enum):
    UNKNOWN = "UNKNOWN"
    LOGIN_SCREEN = "LOGIN_SCREEN"
    CHARACTER_SELECT = "CHARACTER_SELECT"
    WORLD_VISUAL = "WORLD_VISUAL"
    WORLD_EXIT_VISUAL = "WORLD_EXIT_VISUAL"
    ERROR_SCREEN = "ERROR_SCREEN"


class NamedAgentAction(str, Enum):
    SCREENSHOT = "SCREENSHOT"
    SUBMIT_AUTHORIZED_LOGIN = "SUBMIT_AUTHORIZED_LOGIN"
    SELECT_CHARACTER = "SELECT_CHARACTER"
    ENTER_WORLD = "ENTER_WORLD"
    EXIT_WORLD = "EXIT_WORLD"


class OwnerControlCommand(str, Enum):
    PAUSE = "PAUSE"
    STOP = "STOP"
    RESUME = "RESUME"
    SCREENSHOT = "SCREENSHOT"


class ResultStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"


_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_RUNTIME_ACCESS = frozenset({
    "none", "read_only", "ephemeral_isolated", "canonical_reuse_or_mutation",
    "canonical_bootstrap", "canonical_rebind", "canonical_recovery",
    "canonical_boot_epoch_recovery",
})


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValidationError("INVALID_FIELD", f"{field} must be a non-empty string", field)
    return value


def _sha(value: Any, field: str, pattern: re.Pattern[str], length: int) -> str:
    if not isinstance(value, str) or not pattern.fullmatch(value):
        code = "INVALID_SHA1" if length == 40 else "INVALID_SHA256"
        raise ValidationError(code, f"{field} must be lowercase hexadecimal SHA ({length} characters)", field)
    return value


def _enum(value: Any, enum_type: type[Enum], field: str) -> Any:
    try:
        return enum_type(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError("INVALID_ENUM", f"{field} is not an admitted value", field) from exc


def _validate_payload_string(value: str, field: str) -> str:
    try:
        value.encode("utf-8", "strict")
    except UnicodeEncodeError as exc:
        raise ValidationError("INVALID_UTF8", "payload strings must be valid UTF-8", field) from exc
    if any(0xD800 <= ord(char) <= 0xDFFF for char in value):
        raise ValidationError("INVALID_UTF8", "payload strings cannot contain surrogates", field)
    return value


def _freeze_payload(value: Any, field: str = "payload") -> MappingProxyType:
    if not isinstance(value, dict):
        raise ValidationError("INVALID_FIELD", "payload must be a dictionary", field)
    frozen: dict[str, object] = {}
    for key, item in value.items():
        if not isinstance(key, str):
            raise ValidationError("INVALID_FIELD", "payload keys must be strings", field)
        frozen[_validate_payload_string(key, field)] = _freeze_value(item, field)
    return MappingProxyType(frozen)


def _freeze_value(value: Any, field: str) -> object:
    if isinstance(value, dict):
        return _freeze_payload(value, field)
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_value(entry, field) for entry in value)
    if isinstance(value, str):
        return _validate_payload_string(value, field)
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, int):
        if abs(value) > MAX_SAFE_INTEGER:
            raise ValidationError("INTEGER_OUT_OF_RANGE", "payload integer exceeds safe range", field)
        return value
    if isinstance(value, float):
        if not isfinite(value):
            raise ValidationError("INVALID_NUMBER", "payload floats must be finite", field)
        return value
    raise ValidationError("INVALID_FIELD", "payload contains an unsupported value", field)


@dataclass(frozen=True)
class ClientIdentity:
    version: str
    size: int | str
    sha256: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> ClientIdentity:
        if not isinstance(value, Mapping):
            raise ValidationError("INVALID_FIELD", "client_identity must be a mapping", "client_identity")
        require_exact_keys(value, ("version", "size", "sha256"))
        size = value["size"]
        if isinstance(size, bool) or not isinstance(size, (int, str)):
            raise ValidationError("INVALID_FIELD", "size must be an integer or string", "size")
        if isinstance(size, int):
            checked_non_negative(size, maximum=MAX_SAFE_INTEGER, field_name="size")
        return cls(_text(value["version"], "version"), size, _sha(value["sha256"], "sha256", _SHA256, 64))


@dataclass(frozen=True)
class TaskEnvelope:
    schema: str
    session_id: str
    task_id: str
    run_id: str
    idempotency_key: str
    trusted_main_sha: str
    client_identity: ClientIdentity
    objective: str
    allowed_actions: tuple[NamedAgentAction, ...]
    physical_action_budget: int
    max_attempts: int
    deadline_epoch_ms: int
    runtime_access: str
    required_evidence: tuple[str, ...]
    secret_capability_ref: str | None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> TaskEnvelope:
        if not isinstance(value, Mapping):
            raise ValidationError("INVALID_FIELD", "task envelope must be a mapping")
        keys = ("schema", "session_id", "task_id", "run_id", "idempotency_key", "trusted_main_sha", "client_identity", "objective", "allowed_actions", "physical_action_budget", "max_attempts", "deadline_epoch_ms", "runtime_access", "required_evidence", "secret_capability_ref")
        require_exact_keys(value, keys)
        if value["schema"] != "otclient.local-agent.task.v1":
            raise ValidationError("INVALID_SCHEMA", "schema must be otclient.local-agent.task.v1", "schema")
        ids = {field: validate_opaque_id(value[field], field_name=field) for field in ("session_id", "task_id", "run_id", "idempotency_key")}
        trusted = _sha(value["trusted_main_sha"], "trusted_main_sha", _SHA40, 40)
        actions = value["allowed_actions"]
        if not isinstance(actions, (list, tuple)):
            raise ValidationError("INVALID_FIELD", "allowed_actions must be a sequence", "allowed_actions")
        parsed_actions = tuple(_enum(action, NamedAgentAction, "allowed_actions") for action in actions)
        evidence = value["required_evidence"]
        if not isinstance(evidence, (list, tuple)):
            raise ValidationError("INVALID_FIELD", "required_evidence must be a sequence", "required_evidence")
        if value["runtime_access"] not in _RUNTIME_ACCESS:
            raise ValidationError("INVALID_RUNTIME_ACCESS", "runtime_access is not an admitted vocabulary value", "runtime_access")
        secret_ref = value["secret_capability_ref"]
        if secret_ref is not None:
            secret_ref = validate_opaque_id(secret_ref, field_name="secret_capability_ref")
        attempts = checked_non_negative(value["max_attempts"], maximum=3, field_name="max_attempts")
        if attempts < 1:
            raise ValidationError("INTEGER_OUT_OF_RANGE", "max_attempts must be at least 1", "max_attempts")
        return cls(value["schema"], ids["session_id"], ids["task_id"], ids["run_id"], ids["idempotency_key"], trusted, ClientIdentity.from_mapping(value["client_identity"]), _text(value["objective"], "objective"), parsed_actions, checked_non_negative(value["physical_action_budget"], maximum=MAX_SAFE_INTEGER, field_name="physical_action_budget"), attempts, checked_non_negative(value["deadline_epoch_ms"], maximum=MAX_SAFE_INTEGER, field_name="deadline_epoch_ms"), value["runtime_access"], tuple(_text(item, "required_evidence") for item in evidence), secret_ref)


@dataclass(frozen=True)
class AgentEvent:
    schema: str
    session_id: str
    run_id: str | None
    seq: int
    observed_epoch_ms: int
    provenance: AgentProvenance
    kind: str
    state_before: str
    state_after: str
    artifact_refs: tuple[str, ...]
    action_id: str | None
    payload: dict[str, object]

    def __post_init__(self) -> None:
        object.__setattr__(self, "payload", cast("dict[str, object]", _freeze_payload(self.payload)))

    @classmethod
    def new(cls, *, session_id: str, run_id: str | None, provenance: AgentProvenance, kind: str, state_before: str, state_after: str, observed_epoch_ms: int = 0, artifact_refs: tuple[str, ...] = (), action_id: str | None = None, payload: dict[str, object] | None = None) -> AgentEvent:
        if not isinstance(artifact_refs, tuple):
            raise ValidationError("INVALID_FIELD", "artifact_refs must be a tuple", "artifact_refs")
        return cls("otclient.local-agent.event.v1", validate_opaque_id(session_id, field_name="session_id"), None if run_id is None else validate_opaque_id(run_id, field_name="run_id"), 0, checked_non_negative(observed_epoch_ms, maximum=MAX_SAFE_INTEGER, field_name="observed_epoch_ms"), _enum(provenance, AgentProvenance, "provenance"), _text(kind, "kind"), _text(state_before, "state_before"), _text(state_after, "state_after"), tuple(validate_opaque_id(ref, field_name="artifact_ref") for ref in artifact_refs), None if action_id is None else validate_opaque_id(action_id, field_name="action_id"), {} if payload is None else payload)


@dataclass(frozen=True)
class ResultEnvelope:
    schema: str
    session_id: str
    run_id: str
    status: ResultStatus
    trusted_main_sha: str
    final_state: str
    action_count: int
    physical_action_budget: int
    evidence_manifest_sha256: str
    unresolved_conflicts: tuple[str, ...]


@dataclass(frozen=True)
class AgentSessionRecord:
    session_id: str
    operational_state: AgentOperationalState
    current_run_id: str | None
    last_event_seq: int
    pause_latched: bool
    stop_latched: bool
    heartbeat_epoch_ms: int | None
