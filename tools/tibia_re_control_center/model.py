from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Any

SCHEMA_VERSION = 1
MAX_SAFE_INTEGER = (1 << 53) - 1
MAX_U64 = (1 << 64) - 1
MAX_I32 = (1 << 31) - 1

SCENARIO_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
SEMANTIC_KEY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$")
FIELD_SEGMENT_RE = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
HEX_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

EFFECT_DIMENSIONS = (
    "max_actions",
    "max_movement_tiles",
    "max_spells",
    "max_consumables",
    "max_items_moved",
    "max_gold",
    "max_tibia_coins",
    "max_irreversible_changes",
)
FIELD_ROOTS = {
    "client_state",
    "player",
    "conditions",
    "action_state",
    "target",
    "inventory",
    "containers",
    "battle_list",
    "source_quality",
}


class ControlCenterError(Exception):
    pass


class ValidationError(ControlCenterError):
    def __init__(self, code: str, safe_message: str, field: str | None = None):
        super().__init__(safe_message)
        self.code = code
        self.safe_message = safe_message
        self.field = field


class DurabilityError(ControlCenterError):
    pass


class DurabilityTimeout(DurabilityError):
    pass


class SimulatedCrash(ControlCenterError):
    pass


class PrivacyError(ControlCenterError):
    def __init__(self, category: str, reason: str):
        super().__init__(reason)
        self.category = category
        self.reason = reason


class Authority(str, Enum):
    READ_ONLY = "READ_ONLY"
    MUTATION = "MUTATION"


class AdapterKind(str, Enum):
    OFFICIAL_TIBIA = "OFFICIAL_TIBIA"
    OTERYN_V2 = "OTERYN_V2"
    FAKE_TEST = "FAKE_TEST"


class LifecycleState(str, Enum):
    CREATED = "CREATED"
    VALIDATED = "VALIDATED"
    RESERVED = "RESERVED"
    WAITING_AUTHORITY = "WAITING_AUTHORITY"
    DISPATCH_COMMITTED = "DISPATCH_COMMITTED"
    DISPATCHING = "DISPATCHING"
    CONFIRMING = "CONFIRMING"
    CONFIRMED = "CONFIRMED"
    REFUSED = "REFUSED"
    CANCELLED_BEFORE_DISPATCH = "CANCELLED_BEFORE_DISPATCH"
    CANCELLED_AFTER_DISPATCH = "CANCELLED_AFTER_DISPATCH"
    FAILED_BEFORE_DISPATCH = "FAILED_BEFORE_DISPATCH"
    FAILED_AFTER_DISPATCH = "FAILED_AFTER_DISPATCH"
    TIMED_OUT_BEFORE_DISPATCH = "TIMED_OUT_BEFORE_DISPATCH"
    TIMED_OUT_AFTER_DISPATCH = "TIMED_OUT_AFTER_DISPATCH"
    AMBIGUOUS = "AMBIGUOUS"


TERMINAL_STATES = {
    LifecycleState.CONFIRMED,
    LifecycleState.REFUSED,
    LifecycleState.CANCELLED_BEFORE_DISPATCH,
    LifecycleState.CANCELLED_AFTER_DISPATCH,
    LifecycleState.FAILED_BEFORE_DISPATCH,
    LifecycleState.FAILED_AFTER_DISPATCH,
    LifecycleState.TIMED_OUT_BEFORE_DISPATCH,
    LifecycleState.TIMED_OUT_AFTER_DISPATCH,
    LifecycleState.AMBIGUOUS,
}


class DispatchState(str, Enum):
    NOT_DISPATCHED = "NOT_DISPATCHED"
    POSSIBLY_DISPATCHED = "POSSIBLY_DISPATCHED"
    DISPATCHED = "DISPATCHED"


class ActionStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    REFUSED = "REFUSED"
    TIMEOUT = "TIMEOUT"
    CANCELLED = "CANCELLED"
    AMBIGUOUS = "AMBIGUOUS"
    UNKNOWN = "UNKNOWN"


class Confirmation(str, Enum):
    PROVEN = "PROVEN"
    DERIVED = "DERIVED"
    NOT_AVAILABLE = "NOT_AVAILABLE"
    UNKNOWN = "UNKNOWN"


class Freshness(str, Enum):
    FRESH = "FRESH"
    STALE = "STALE"
    UNKNOWN = "UNKNOWN"


class OrderingConfidence(str, Enum):
    KNOWN = "KNOWN"
    PARTIAL = "PARTIAL"
    UNKNOWN = "UNKNOWN"


class ScreenshotDisposition(str, Enum):
    SAFE = "SAFE"
    QUARANTINED = "QUARANTINED"
    REJECTED = "REJECTED"


class RunArtifactState(str, Enum):
    ACTIVE = "ACTIVE"
    CLOSING = "CLOSING"
    FINALIZED = "FINALIZED"
    INCOMPLETE = "INCOMPLETE"
    AMBIGUOUS = "AMBIGUOUS"
    FAILED = "FAILED"


def _utf8(value: str, field_name: str) -> bytes:
    try:
        encoded = value.encode("utf-8", "strict")
    except UnicodeEncodeError as exc:
        raise ValidationError("INVALID_UTF8", f"{field_name} is not valid UTF-8", field_name) from exc
    if any(0xD800 <= ord(ch) <= 0xDFFF for ch in value):
        raise ValidationError("INVALID_UTF8", f"{field_name} contains a surrogate", field_name)
    return encoded


def checked_non_negative(value: Any, *, maximum: int = MAX_U64, field_name: str = "value") -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError("INVALID_INTEGER", f"{field_name} must be an integer", field_name)
    if value < 0 or value > maximum:
        raise ValidationError("INTEGER_OUT_OF_RANGE", f"{field_name} is outside the admitted range", field_name)
    return value


def checked_add(a: int, b: int, *, maximum: int = MAX_U64, field_name: str = "value") -> int:
    a = checked_non_negative(a, maximum=maximum, field_name=field_name)
    b = checked_non_negative(b, maximum=maximum, field_name=field_name)
    if a > maximum - b:
        raise ValidationError("ARITHMETIC_OVERFLOW", f"{field_name} addition overflow", field_name)
    return a + b


def checked_mul(a: int, b: int, *, maximum: int = MAX_U64, field_name: str = "value") -> int:
    a = checked_non_negative(a, maximum=maximum, field_name=field_name)
    b = checked_non_negative(b, maximum=maximum, field_name=field_name)
    if a and b > maximum // a:
        raise ValidationError("ARITHMETIC_OVERFLOW", f"{field_name} multiplication overflow", field_name)
    return a * b


def require_exact_keys(value: Mapping[str, Any], required: Iterable[str], optional: Iterable[str] = ()) -> None:
    required_set = set(required)
    optional_set = set(optional)
    missing = required_set - set(value)
    unknown = set(value) - required_set - optional_set
    if missing:
        raise ValidationError("MISSING_FIELD", f"missing required field(s): {', '.join(sorted(missing))}")
    if unknown:
        raise ValidationError("UNKNOWN_FIELD", f"unknown field(s): {', '.join(sorted(unknown))}")


def validate_scenario_id(value: Any, *, field_name: str = "id") -> str:
    if not isinstance(value, str) or not SCENARIO_ID_RE.fullmatch(value):
        raise ValidationError("INVALID_IDENTIFIER", f"{field_name} is not a valid ScenarioId", field_name)
    _utf8(value, field_name)
    return value


def validate_opaque_id(value: Any, *, field_name: str = "id", max_bytes: int = 128) -> str:
    if not isinstance(value, str) or not value:
        raise ValidationError("INVALID_IDENTIFIER", f"{field_name} must be a non-empty string", field_name)
    raw = _utf8(value, field_name)
    if len(raw) > max_bytes or any(ch in value for ch in ("/", "\\", "\x00")) or value in {".", ".."}:
        raise ValidationError("INVALID_IDENTIFIER", f"{field_name} is outside the admitted identifier grammar", field_name)
    return value


def validate_semantic_key(value: Any, *, field_name: str = "semantic_key") -> str:
    if not isinstance(value, str) or not SEMANTIC_KEY_RE.fullmatch(value):
        raise ValidationError("INVALID_SEMANTIC_KEY", f"{field_name} is not a valid SemanticKey", field_name)
    _utf8(value, field_name)
    return value


@dataclass(frozen=True)
class SemanticFieldPath:
    value: str

    @classmethod
    def parse(cls, value: Any) -> SemanticFieldPath:
        if not isinstance(value, str):
            raise ValidationError("INVALID_FIELD_PATH", "SemanticFieldPath must be a string", "field")
        encoded = _utf8(value, "field")
        if len(encoded) > 256 or any(token in value for token in ("[", "]", "*", "/")):
            raise ValidationError("INVALID_FIELD_PATH", "SemanticFieldPath contains forbidden syntax", "field")
        segments = value.split(".")
        if not 1 <= len(segments) <= 8 or any(not FIELD_SEGMENT_RE.fullmatch(seg) for seg in segments):
            raise ValidationError("INVALID_FIELD_PATH", "SemanticFieldPath has invalid segments", "field")
        if segments[0] not in FIELD_ROOTS:
            raise ValidationError("INVALID_FIELD_ROOT", "SemanticFieldPath root is not normalized schema v1", "field")
        return cls(value)


@dataclass(frozen=True)
class SideEffectBudget:
    max_runtime_seconds: int
    max_actions: int
    max_movement_tiles: int
    max_spells: int
    max_consumables: int
    max_items_moved: int
    max_gold: int
    max_tibia_coins: int
    max_irreversible_changes: int

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> SideEffectBudget:
        if not isinstance(value, Mapping):
            raise ValidationError("INVALID_BUDGET", "side_effect_budget must be an object")
        require_exact_keys(value, ("max_runtime_seconds", *EFFECT_DIMENSIONS))
        runtime = checked_non_negative(value["max_runtime_seconds"], maximum=86400, field_name="max_runtime_seconds")
        if runtime < 1:
            raise ValidationError("BUDGET_RUNTIME_RANGE", "max_runtime_seconds must be in 1..86400")
        effects = {name: checked_non_negative(value[name], maximum=MAX_I32, field_name=name) for name in EFFECT_DIMENSIONS}
        return cls(runtime, **effects)

    def effect_limits(self) -> dict[str, int]:
        return {name: getattr(self, name) for name in EFFECT_DIMENSIONS}

    def as_dict(self) -> dict[str, int]:
        return {"max_runtime_seconds": self.max_runtime_seconds, **self.effect_limits()}


@dataclass(frozen=True)
class EffectBound:
    max_actions: int = 0
    max_movement_tiles: int = 0
    max_spells: int = 0
    max_consumables: int = 0
    max_items_moved: int = 0
    max_gold: int = 0
    max_tibia_coins: int = 0
    max_irreversible_changes: int = 0
    measurable_after: bool = True
    reason_codes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in EFFECT_DIMENSIONS:
            checked_non_negative(getattr(self, name), maximum=MAX_I32, field_name=name)

    def as_dict(self) -> dict[str, Any]:
        return {name: getattr(self, name) for name in EFFECT_DIMENSIONS} | {
            "measurable_after": self.measurable_after,
            "reason_codes": list(self.reason_codes),
        }


class EquipmentSlot(str, Enum):
    HEAD = "HEAD"
    NECK = "NECK"
    BACK = "BACK"
    ARMOR = "ARMOR"
    RIGHT_HAND = "RIGHT_HAND"
    LEFT_HAND = "LEFT_HAND"
    LEGS = "LEGS"
    FEET = "FEET"
    RING = "RING"
    AMMO = "AMMO"
    OTHER = "OTHER"


@dataclass(frozen=True)
class WorldPosition:
    x: int
    y: int
    z: int

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> WorldPosition:
        if not isinstance(value, Mapping):
            raise ValidationError("INVALID_POSITION", "position must be an object")
        require_exact_keys(value, ("x", "y", "z"))
        return cls(
            checked_non_negative(value["x"], maximum=65535, field_name="x"),
            checked_non_negative(value["y"], maximum=65535, field_name="y"),
            checked_non_negative(value["z"], maximum=15, field_name="z"),
        )


@dataclass(frozen=True)
class EntityRef:
    kind: str
    creature_id: int | None = None
    snapshot_path: SemanticFieldPath | None = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> EntityRef:
        if not isinstance(value, Mapping):
            raise ValidationError("INVALID_ENTITY_REF", "target must be an EntityRef object")
        kind = value.get("kind")
        if kind in {"SELF", "SELECTED_TARGET"}:
            require_exact_keys(value, ("kind",))
            return cls(str(kind))
        if kind == "CREATURE_ID":
            require_exact_keys(value, ("kind", "creature_id"))
            return cls("CREATURE_ID", checked_non_negative(value["creature_id"], maximum=0xFFFFFFFF, field_name="creature_id"))
        if kind == "SNAPSHOT_PATH":
            require_exact_keys(value, ("kind", "snapshot_path"))
            return cls("SNAPSHOT_PATH", snapshot_path=SemanticFieldPath.parse(value["snapshot_path"]))
        raise ValidationError("INVALID_ENTITY_REF", "EntityRef kind is not admitted")


@dataclass(frozen=True)
class ItemRef:
    kind: str
    inventory_slot: str | None = None
    container_ref: str | None = None
    slot_index: int | None = None
    equipment_slot: EquipmentSlot | None = None
    snapshot_path: SemanticFieldPath | None = None
    expected_semantic_item: str | None = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> ItemRef:
        if not isinstance(value, Mapping):
            raise ValidationError("INVALID_ITEM_REF", "item must be an ItemRef object")
        kind = value.get("kind")
        optional = ("expected_semantic_item",)
        expected = value.get("expected_semantic_item")
        if expected is not None:
            expected = validate_semantic_key(expected, field_name="expected_semantic_item")
        if kind == "INVENTORY_SLOT":
            require_exact_keys(value, ("kind", "inventory_slot"), optional)
            return cls(kind, inventory_slot=validate_semantic_key(value["inventory_slot"], field_name="inventory_slot"), expected_semantic_item=expected)
        if kind == "CONTAINER_SLOT":
            require_exact_keys(value, ("kind", "container_ref", "slot_index"), optional)
            return cls(kind, container_ref=validate_semantic_key(value["container_ref"], field_name="container_ref"), slot_index=checked_non_negative(value["slot_index"], maximum=65535, field_name="slot_index"), expected_semantic_item=expected)
        if kind == "EQUIPMENT_SLOT":
            require_exact_keys(value, ("kind", "equipment_slot"), optional)
            try:
                slot = EquipmentSlot(value["equipment_slot"])
            except (TypeError, ValueError) as exc:
                raise ValidationError("INVALID_EQUIPMENT_SLOT", "equipment_slot is invalid") from exc
            return cls(kind, equipment_slot=slot, expected_semantic_item=expected)
        if kind == "SNAPSHOT_PATH":
            require_exact_keys(value, ("kind", "snapshot_path"), optional)
            return cls(kind, snapshot_path=SemanticFieldPath.parse(value["snapshot_path"]), expected_semantic_item=expected)
        raise ValidationError("INVALID_ITEM_REF", "ItemRef kind is not admitted")


@dataclass(frozen=True)
class DestinationRef:
    kind: str
    inventory_slot: str | None = None
    container_ref: str | None = None
    slot_index: int | None = None
    equipment_slot: EquipmentSlot | None = None
    position: WorldPosition | None = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> DestinationRef:
        if not isinstance(value, Mapping):
            raise ValidationError("INVALID_DESTINATION_REF", "destination must be a DestinationRef object")
        kind = value.get("kind")
        if kind == "INVENTORY_SLOT":
            require_exact_keys(value, ("kind", "inventory_slot"))
            return cls(kind, inventory_slot=validate_semantic_key(value["inventory_slot"], field_name="inventory_slot"))
        if kind == "CONTAINER_SLOT":
            require_exact_keys(value, ("kind", "container_ref", "slot_index"))
            return cls(kind, container_ref=validate_semantic_key(value["container_ref"], field_name="container_ref"), slot_index=checked_non_negative(value["slot_index"], maximum=65535, field_name="slot_index"))
        if kind == "EQUIPMENT_SLOT":
            require_exact_keys(value, ("kind", "equipment_slot"))
            try:
                return cls(kind, equipment_slot=EquipmentSlot(value["equipment_slot"]))
            except (TypeError, ValueError) as exc:
                raise ValidationError("INVALID_EQUIPMENT_SLOT", "equipment_slot is invalid") from exc
        if kind == "GROUND_POSITION":
            require_exact_keys(value, ("kind", "position"))
            return cls(kind, position=WorldPosition.from_mapping(value["position"]))
        raise ValidationError("INVALID_DESTINATION_REF", "DestinationRef kind is not admitted")


@dataclass(frozen=True)
class Predicate:
    field: SemanticFieldPath
    op: str
    value: Any = None
    from_checkpoint: str | None = None
    unknown_policy: str = "FAIL"


@dataclass(frozen=True)
class AbortCondition:
    condition: Predicate
    reason_code: str
    id: str | None = None


@dataclass(frozen=True)
class AdapterIdentity:
    adapter_id: str
    adapter_kind: AdapterKind
    adapter_version: str
    adapter_generation: str
    runtime_instance_id: str | None = None
    session_epoch: str | None = None


@dataclass(frozen=True)
class Capability:
    capability_id: str
    semantic_version: str = "1.0"
    read_supported: bool = False
    action_supported: bool = False
    source: str = "fake"
    notes: str | None = None


@dataclass(frozen=True)
class RuntimeStatus:
    adapter_id: str
    adapter_generation: str
    runtime_state: str = "ONLINE"
    client_state: str = "IN_GAME"
    recorder_state: str = "STOPPED"
    authority_state: str = "READ_ONLY"
    session_epoch: str | None = None
    runtime_instance_id: str | None = None
    observed_monotonic_ns: int = 0
    freshness: Freshness = Freshness.FRESH
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True)
class GameSnapshot:
    snapshot_id: str
    adapter_id: str
    adapter_generation: str
    ingested_monotonic_ns: int
    client_state: str = "UNKNOWN"
    session_epoch: str | None = None
    runtime_instance_id: str | None = None
    source_timestamp: int | str | None = None
    source_clock_domain: str | None = None
    player: Mapping[str, Any] = field(default_factory=dict)
    conditions: Mapping[str, Any] | None = None
    action_state: Mapping[str, Any] | None = None
    target: Mapping[str, Any] | None = None
    inventory: Mapping[str, Any] | None = None
    containers: Mapping[str, Any] | None = None
    battle_list: Mapping[str, Any] | None = None
    source_quality: Mapping[str, Any] = field(default_factory=lambda: {"field_sources": {}, "unknown_fields": [], "stale_fields": []})
    schema_version: int = SCHEMA_VERSION


@dataclass(frozen=True)
class DispatchFence:
    expected_backend_epoch: str
    expected_control_generation: int
    expected_adapter_generation: str
    expected_runtime_instance_id: str | None
    expected_session_epoch: str | None


@dataclass(frozen=True)
class ActionRequest:
    action_id: str
    run_id: str
    step_id: str
    attempt_index: int
    kind: str
    parameters: Mapping[str, Any]
    timeout_ms: int
    required_capability: str
    required_authority: Authority
    dispatch_fence: DispatchFence
    effect_bound: EffectBound
    action_request_hash: str
    schema_version: int = SCHEMA_VERSION

    def __post_init__(self) -> None:
        validate_opaque_id(self.action_id, field_name="action_id", max_bytes=192)
        validate_opaque_id(self.run_id, field_name="run_id")
        validate_opaque_id(self.step_id, field_name="step_id", max_bytes=192)
        checked_non_negative(self.attempt_index, maximum=MAX_I32, field_name="attempt_index")
        if not HEX_SHA256_RE.fullmatch(self.action_request_hash):
            raise ValidationError("INVALID_ACTION_HASH", "action_request_hash must be lowercase SHA-256")


@dataclass(frozen=True)
class ActionResult:
    action_id: str
    lifecycle_state: LifecycleState
    status: ActionStatus
    dispatch_state: DispatchState
    authoritative_confirmation: Confirmation
    backend_epoch: str
    control_generation: int
    adapter_generation: str
    runtime_instance_id: str | None
    session_epoch: str | None
    monotonic_started_ns: int
    monotonic_finished_ns: int
    normalized_delta: Mapping[str, Any] | None = None
    budget_effect: Mapping[str, Any] = field(default_factory=dict)
    evidence_refs: tuple[str, ...] = ()
    reason_code: str | None = None
    safe_message: str | None = None
    schema_version: int = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.status == ActionStatus.PASS and self.lifecycle_state != LifecycleState.CONFIRMED:
            raise ValidationError("INVALID_SUCCESS_STATE", "PASS requires terminal CONFIRMED lifecycle state")


@dataclass(frozen=True)
class ControlState:
    stop_latched: bool
    recovery_required: bool
    control_generation: int
    transition_id: str
    active_backend_epoch: str | None
    written_by_backend_epoch: str
    reason_code: str
    updated_monotonic_ns: int
    schema_version: int = SCHEMA_VERSION


@dataclass(frozen=True)
class ActionLedgerRecord:
    action_id: str
    action_request_hash: str
    run_id: str
    step_id: str
    attempt_index: int
    lifecycle_state: LifecycleState
    dispatch_state: DispatchState
    backend_epoch: str
    control_generation: int
    adapter_id: str
    adapter_generation: str
    runtime_instance_id: str | None
    session_epoch: str | None
    effect_bound: EffectBound
    authoritative_confirmation: Confirmation = Confirmation.UNKNOWN
    reason_code: str | None = None
    created_monotonic_ns: int = 0
    updated_monotonic_ns: int = 0
    schema_version: int = SCHEMA_VERSION

    @property
    def terminal(self) -> bool:
        return self.lifecycle_state in TERMINAL_STATES

    def with_state(self, state: LifecycleState, now_ns: int, **changes: Any) -> ActionLedgerRecord:
        if self.terminal and state != self.lifecycle_state:
            raise ValidationError("TERMINAL_STATE_IMMUTABLE", "terminal ActionLedger state cannot be rewritten")
        return replace(self, lifecycle_state=state, updated_monotonic_ns=now_ns, **changes)


@dataclass
class BudgetDimension:
    limit: int
    reserved: int = 0
    at_risk: int = 0
    committed: int = 0
    uncertain: int = 0

    def available(self) -> int:
        consumed = checked_add(
            checked_add(self.reserved, self.at_risk, field_name="budget"),
            checked_add(self.committed, self.uncertain, field_name="budget"),
            field_name="budget",
        )
        if consumed > self.limit:
            raise ValidationError("BUDGET_CONTRADICTION", "budget accounting exceeds limit")
        return self.limit - consumed

    def clone(self) -> BudgetDimension:
        return BudgetDimension(self.limit, self.reserved, self.at_risk, self.committed, self.uncertain)


@dataclass
class BudgetLedger:
    run_id: str
    limit_seconds: int
    started_monotonic_ns: int
    deadline_monotonic_ns: int
    dimensions: dict[str, BudgetDimension]
    expired: bool = False
    updated_monotonic_ns: int = 0
    reservations: dict[str, EffectBound] = field(default_factory=dict)
    schema_version: int = SCHEMA_VERSION

    def clone(self) -> BudgetLedger:
        return BudgetLedger(
            self.run_id,
            self.limit_seconds,
            self.started_monotonic_ns,
            self.deadline_monotonic_ns,
            {key: value.clone() for key, value in self.dimensions.items()},
            self.expired,
            self.updated_monotonic_ns,
            dict(self.reservations),
            self.schema_version,
        )


@dataclass(frozen=True)
class Event:
    event_id: str
    ingest_seq: int
    ingested_monotonic_ns: int
    source_timestamp: int | str | None
    source_clock_domain: str | None
    source_sequence: int | None
    source_sequence_scope: str | None
    ordering_confidence: OrderingConfidence
    late: bool
    backend_epoch: str
    control_generation: int
    adapter_id: str
    adapter_generation: str
    runtime_instance_id: str | None
    session_epoch: str | None
    run_id: str | None
    experiment_id: str | None
    step_id: str | None
    stimulus_id: str | None
    kind: str
    sensitivity: str
    payload: Mapping[str, Any]
    wall_time: str | None = None
    schema_version: int = SCHEMA_VERSION


@dataclass(frozen=True)
class PolicyActionProposal:
    kind: str
    parameters: Mapping[str, Any]
    timeout_ms: int
    requested_budget_ceiling: SideEffectBudget | None = None


@dataclass(frozen=True)
class PolicyObservationEnvelope:
    observation_id: str
    adapter_id: str
    adapter_kind: str
    backend_epoch: str
    observed_monotonic_ns: int
    freshness: Freshness
    snapshot: GameSnapshot
    capability_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    active_run_summary: Mapping[str, Any] | None
    budget_available: Mapping[str, Any]
    control_state: Mapping[str, Any]
    schema_version: int = SCHEMA_VERSION


@dataclass(frozen=True)
class PolicyResultEnvelope:
    decision_id: str
    accepted: bool
    resource_id: str | None
    status: str
    reason_codes: tuple[str, ...]
    result_ref: str | None
    evidence_refs: tuple[str, ...]
    next_observation_required: bool
    schema_version: int = SCHEMA_VERSION


def negotiate_major(required: int, supported: Iterable[int], *, contract_name: str) -> int:
    supported_set = {checked_non_negative(value, maximum=MAX_I32, field_name=contract_name) for value in supported}
    if required not in supported_set:
        raise ValidationError("UNSUPPORTED_CONTRACT_MAJOR", f"unsupported required {contract_name} major version")
    return required
