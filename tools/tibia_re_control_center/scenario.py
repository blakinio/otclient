from __future__ import annotations

import json
import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any

from .canonical import sha256_jcs
from .model import (
    MAX_I32,
    AbortCondition,
    Authority,
    DestinationRef,
    EffectBound,
    EntityRef,
    EquipmentSlot,
    ItemRef,
    Predicate,
    SemanticFieldPath,
    SideEffectBudget,
    ValidationError,
    checked_non_negative,
    require_exact_keys,
    validate_opaque_id,
    validate_scenario_id,
    validate_semantic_key,
)

MAX_DOCUMENT_BYTES = 262144
MAX_NESTING_DEPTH = 32
MAX_COLLECTION_ITEMS = 4096
MAX_STRING_BYTES = 8192
MAX_STEPS = 1024
MAX_TIMEOUT_MS = 300000
STANDARD_ABORT_CODES = {
    "STOP_LATCHED",
    "CONTROL_GENERATION_CHANGED",
    "BACKEND_EPOCH_CHANGED",
    "ADAPTER_GENERATION_CHANGED",
    "RUNTIME_INSTANCE_CHANGED",
    "SESSION_EPOCH_CHANGED",
    "AUTHORITY_LOST",
    "CAPABILITY_LOST",
    "TARGET_IDENTITY_CHANGED",
    "CLIENT_NOT_IN_GAME",
    "BUDGET_EXHAUSTED",
    "TIMEOUT",
    "PRIVACY_REJECTION",
    "RECORDER_FATAL",
    "ARTIFACT_FATAL",
}
PREDICATE_OPS = {
    "EQ", "NE", "LT", "LTE", "GT", "GTE", "EXISTS", "NOT_EXISTS",
    "CHANGED", "UNCHANGED", "IN_SET", "CONTAINS",
}
UNKNOWN_POLICIES = {"FAIL", "WAIT", "ACCEPT"}
RETRYABLE_PRE_DISPATCH = {"REFUSED", "FAILED_BEFORE_DISPATCH", "TIMED_OUT_BEFORE_DISPATCH"}
DIRECTIONS = {"NORTH", "EAST", "SOUTH", "WEST"}
ACTION_KINDS = {
    "move", "turn", "stop_movement", "say_controlled_text", "cast_spell",
    "use_consumable", "eat_food", "use_rune", "select_target", "attack",
    "cancel_attack", "follow", "cancel_follow", "open_container",
    "close_container", "use_item", "look_item", "move_item", "equip",
    "unequip", "open_panel", "close_panel", "logout",
}
NON_EXECUTABLE_PLACEHOLDERS = {"login_request", "enter_game_request"}


class PredicateOutcome(str, Enum):
    TRUE = "TRUE"
    FALSE = "FALSE"
    UNKNOWN = "UNKNOWN"
    ERROR = "ERROR"


@dataclass(frozen=True)
class ValidatedStep:
    step_id: str
    step_type: str
    body: Mapping[str, Any]


@dataclass(frozen=True)
class ValidatedScenario:
    ast: Mapping[str, Any]
    scenario_hash: str
    scenario_id: str
    steps: tuple[ValidatedStep, ...]
    side_effect_budget: SideEffectBudget
    required_reads: tuple[str, ...]
    required_actions: tuple[str, ...]
    mutation_capable: bool


@dataclass(frozen=True)
class ScenarioValidationResult:
    valid: bool
    schema_version: int
    scenario_id: str | None
    scenario_hash: str | None
    normalized_step_ids: tuple[str, ...]
    required_reads: tuple[str, ...]
    required_actions: tuple[str, ...]
    errors: tuple[Mapping[str, Any], ...]


class _DuplicateKey(ValueError):
    pass


def _object_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKey(key)
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValidationError("NON_FINITE_NUMBER", f"non-finite numeric value {value} is forbidden")


def _pre_scan_depth(text: str) -> None:
    depth = 0
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char in "[{":
            depth += 1
            if depth > MAX_NESTING_DEPTH:
                raise ValidationError("NESTING_LIMIT", "document nesting depth exceeds Package A limit")
        elif char in "]}":
            depth = max(0, depth - 1)


def _walk_limits(value: Any, depth: int = 0) -> None:
    if depth > MAX_NESTING_DEPTH:
        raise ValidationError("NESTING_LIMIT", "document nesting depth exceeds Package A limit")
    if isinstance(value, str):
        try:
            encoded = value.encode("utf-8", "strict")
        except UnicodeEncodeError as exc:
            raise ValidationError("INVALID_UTF8", "string is not valid UTF-8") from exc
        if len(encoded) > MAX_STRING_BYTES:
            raise ValidationError("STRING_LIMIT", "string exceeds Package A byte limit")
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValidationError("NON_FINITE_NUMBER", "non-finite numbers are forbidden")
        return
    if isinstance(value, Mapping):
        if len(value) > MAX_COLLECTION_ITEMS:
            raise ValidationError("COLLECTION_LIMIT", "mapping exceeds Package A collection limit")
        for key, child in value.items():
            if not isinstance(key, str):
                raise ValidationError("INVALID_MAPPING_KEY", "mapping keys must be strings")
            _walk_limits(key, depth + 1)
            _walk_limits(child, depth + 1)
        return
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        if len(value) > MAX_COLLECTION_ITEMS:
            raise ValidationError("COLLECTION_LIMIT", "sequence exceeds Package A collection limit")
        for child in value:
            _walk_limits(child, depth + 1)


@dataclass(frozen=True)
class _YamlLine:
    indent: int
    text: str
    line_no: int


def _strip_yaml_comment(text: str) -> str:
    quote: str | None = None
    escaped = False
    for index, char in enumerate(text):
        if quote is not None:
            if quote == '"' and escaped:
                escaped = False
            elif quote == '"' and char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {"'", '"'}:
            quote = char
        elif char == "#" and (index == 0 or text[index - 1].isspace()):
            return text[:index].rstrip()
    return text.rstrip()


def _split_top_level(text: str, delimiter: str = ",") -> list[str]:
    parts: list[str] = []
    start = 0
    depth = 0
    quote: str | None = None
    escaped = False
    for index, char in enumerate(text):
        if quote is not None:
            if quote == '"' and escaped:
                escaped = False
            elif quote == '"' and char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {"'", '"'}:
            quote = char
        elif char in "[{(":
            depth += 1
        elif char in "]})":
            depth -= 1
        elif char == delimiter and depth == 0:
            parts.append(text[start:index].strip())
            start = index + 1
    parts.append(text[start:].strip())
    return parts


def _split_mapping(text: str) -> tuple[str, str]:
    depth = 0
    quote: str | None = None
    escaped = False
    for index, char in enumerate(text):
        if quote is not None:
            if quote == '"' and escaped:
                escaped = False
            elif quote == '"' and char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {"'", '"'}:
            quote = char
        elif char in "[{(":
            depth += 1
        elif char in "]})":
            depth -= 1
        elif char == ":" and depth == 0:
            return text[:index].strip(), text[index + 1:].strip()
    raise ValidationError("YAML_SYNTAX", "expected a mapping key followed by ':'")


def _forbidden_yaml_token(text: str) -> bool:
    stripped = text.lstrip()
    if stripped.startswith(("!", "&", "*")):
        return True
    return bool(re.search(r"(^|[\s\[\{,:-])[!&*][A-Za-z0-9_]", text)) or "<<:" in text


def _parse_yaml_scalar(text: str, *, allow_container: bool = True) -> Any:
    text = text.strip()
    if not text:
        return None
    if _forbidden_yaml_token(text):
        raise ValidationError("YAML_TAG_ALIAS_FORBIDDEN", "YAML tags, anchors, aliases and merge keys are forbidden")
    if text in {"|", ">", "|-", ">-", "|+", ">+"}:
        raise ValidationError("YAML_MULTILINE_FORBIDDEN", "multiline YAML scalars are not admitted")
    if allow_container and text.startswith("["):
        if not text.endswith("]"):
            raise ValidationError("YAML_SYNTAX", "unterminated inline sequence")
        inner = text[1:-1].strip()
        return [] if not inner else [_parse_yaml_scalar(part) for part in _split_top_level(inner)]
    if allow_container and text.startswith("{"):
        if not text.endswith("}"):
            raise ValidationError("YAML_SYNTAX", "unterminated inline mapping")
        inner = text[1:-1].strip()
        result: dict[str, Any] = {}
        if not inner:
            return result
        for part in _split_top_level(inner):
            key_text, value_text = _split_mapping(part)
            key = _parse_yaml_scalar(key_text, allow_container=False)
            if not isinstance(key, str) or not key:
                raise ValidationError("YAML_MAPPING_KEY", "YAML mapping keys must be non-empty strings")
            if key in result:
                raise ValidationError("DUPLICATE_KEY", f"duplicate mapping key: {key}")
            result[key] = _parse_yaml_scalar(value_text)
        return result
    if text.startswith('"'):
        try:
            value = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValidationError("YAML_STRING", "invalid double-quoted YAML string") from exc
        if not isinstance(value, str):
            raise ValidationError("YAML_STRING", "quoted scalar must be a string")
        return value
    if text.startswith("'"):
        if len(text) < 2 or not text.endswith("'"):
            raise ValidationError("YAML_STRING", "unterminated single-quoted YAML string")
        return text[1:-1].replace("''", "'")
    lowered = text.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if lowered in {"null", "~"}:
        return None
    if lowered in {".nan", ".inf", "+.inf", "-.inf", "nan", "inf", "+inf", "-inf", "infinity", "+infinity", "-infinity"}:
        raise ValidationError("NON_FINITE_NUMBER", "non-finite YAML numeric values are forbidden")
    if re.fullmatch(r"[-+]?(0|[1-9][0-9]*)", text):
        return int(text, 10)
    if re.fullmatch(r"[-+]?(?:[0-9]+\.[0-9]*|[0-9]*\.[0-9]+)(?:[eE][-+]?[0-9]+)?|[-+]?[0-9]+[eE][-+]?[0-9]+", text):
        value = float(text)
        if not math.isfinite(value):
            raise ValidationError("NON_FINITE_NUMBER", "non-finite YAML numeric values are forbidden")
        return value
    return text


def _parse_yaml_block(lines: list[_YamlLine], index: int, indent: int, depth: int = 0) -> tuple[Any, int]:
    if depth > MAX_NESTING_DEPTH:
        raise ValidationError("NESTING_LIMIT", "YAML nesting exceeds Package A limit")
    if index >= len(lines) or lines[index].indent != indent:
        raise ValidationError("YAML_INDENT", "invalid YAML indentation")
    is_list = lines[index].text == "-" or lines[index].text.startswith("- ")
    if is_list:
        result_list: list[Any] = []
        while index < len(lines) and lines[index].indent == indent:
            line = lines[index]
            if not (line.text == "-" or line.text.startswith("- ")):
                break
            rest = line.text[1:].strip()
            index += 1
            if not rest:
                if index >= len(lines) or lines[index].indent <= indent:
                    raise ValidationError("YAML_SYNTAX", f"empty sequence item at line {line.line_no}")
                item, index = _parse_yaml_block(lines, index, lines[index].indent, depth + 1)
            else:
                try:
                    key_text, value_text = _split_mapping(rest)
                    mapping_item = True
                except ValidationError:
                    mapping_item = False
                if mapping_item:
                    key = _parse_yaml_scalar(key_text, allow_container=False)
                    if not isinstance(key, str) or not key:
                        raise ValidationError("YAML_MAPPING_KEY", "YAML mapping keys must be non-empty strings")
                    item_map: dict[str, Any] = {}
                    if value_text:
                        item_map[key] = _parse_yaml_scalar(value_text)
                    elif index < len(lines) and lines[index].indent > indent:
                        child, index = _parse_yaml_block(lines, index, lines[index].indent, depth + 1)
                        item_map[key] = child
                    else:
                        item_map[key] = None
                    if index < len(lines) and lines[index].indent > indent:
                        extra, index = _parse_yaml_block(lines, index, lines[index].indent, depth + 1)
                        if not isinstance(extra, dict):
                            raise ValidationError("YAML_SYNTAX", "mapping sequence item has invalid continuation")
                        for extra_key, extra_value in extra.items():
                            if extra_key in item_map:
                                raise ValidationError("DUPLICATE_KEY", f"duplicate mapping key: {extra_key}")
                            item_map[extra_key] = extra_value
                    item = item_map
                else:
                    item = _parse_yaml_scalar(rest)
                    if index < len(lines) and lines[index].indent > indent:
                        raise ValidationError("YAML_SYNTAX", "scalar sequence item cannot own an indented continuation")
            result_list.append(item)
            if len(result_list) > MAX_COLLECTION_ITEMS:
                raise ValidationError("COLLECTION_LIMIT", "YAML sequence exceeds Package A collection limit")
        return result_list, index
    result_map: dict[str, Any] = {}
    while index < len(lines) and lines[index].indent == indent:
        line = lines[index]
        if line.text == "-" or line.text.startswith("- "):
            break
        key_text, value_text = _split_mapping(line.text)
        key = _parse_yaml_scalar(key_text, allow_container=False)
        if not isinstance(key, str) or not key:
            raise ValidationError("YAML_MAPPING_KEY", "YAML mapping keys must be non-empty strings")
        if key in result_map:
            raise ValidationError("DUPLICATE_KEY", f"duplicate mapping key: {key}")
        index += 1
        if value_text:
            result_map[key] = _parse_yaml_scalar(value_text)
        elif index < len(lines) and lines[index].indent > indent:
            child, index = _parse_yaml_block(lines, index, lines[index].indent, depth + 1)
            result_map[key] = child
        else:
            result_map[key] = None
        if len(result_map) > MAX_COLLECTION_ITEMS:
            raise ValidationError("COLLECTION_LIMIT", "YAML mapping exceeds Package A collection limit")
    return result_map, index


def _parse_yaml(text: str) -> Any:
    lines: list[_YamlLine] = []
    for line_no, raw in enumerate(text.splitlines(), 1):
        leading = raw[: len(raw) - len(raw.lstrip(" \t"))]
        if "\t" in leading:
            raise ValidationError("YAML_INDENT", f"tabs are forbidden in YAML indentation at line {line_no}")
        stripped = _strip_yaml_comment(raw)
        if not stripped.strip():
            continue
        indent = len(stripped) - len(stripped.lstrip(" "))
        body = stripped[indent:]
        if _forbidden_yaml_token(body):
            raise ValidationError("YAML_TAG_ALIAS_FORBIDDEN", f"YAML tags, anchors, aliases and merge keys are forbidden at line {line_no}")
        lines.append(_YamlLine(indent, body, line_no))
    if not lines:
        raise ValidationError("EMPTY_DOCUMENT", "scenario document is empty")
    if lines[0].indent != 0:
        raise ValidationError("YAML_INDENT", "top-level YAML must start at indentation zero")
    value, index = _parse_yaml_block(lines, 0, 0)
    if index != len(lines):
        raise ValidationError("YAML_INDENT", "YAML contains inconsistent indentation")
    return value


def parse_document(data: bytes | str) -> Any:
    if isinstance(data, str):
        try:
            raw = data.encode("utf-8", "strict")
        except UnicodeEncodeError as exc:
            raise ValidationError("INVALID_UTF8", "scenario input must be valid UTF-8") from exc
    elif isinstance(data, (bytes, bytearray)):
        raw = bytes(data)
    else:
        raise ValidationError("INVALID_DOCUMENT_TYPE", "scenario document must be UTF-8 bytes or text")
    if len(raw) > MAX_DOCUMENT_BYTES:
        raise ValidationError("DOCUMENT_LIMIT", "scenario document exceeds Package A byte limit")
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise ValidationError("INVALID_UTF8", "scenario input must be valid UTF-8") from exc
    stripped = text.lstrip()
    if not stripped:
        raise ValidationError("EMPTY_DOCUMENT", "scenario document is empty")
    if stripped[0] in "[{":
        _pre_scan_depth(stripped)
        try:
            value = json.loads(stripped, object_pairs_hook=_object_no_duplicates, parse_constant=_reject_constant)
        except _DuplicateKey as exc:
            raise ValidationError("DUPLICATE_KEY", f"duplicate mapping key: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise ValidationError("JSON_SYNTAX", "invalid JSON scenario document") from exc
    else:
        value = _parse_yaml(text)
    _walk_limits(value)
    return value


def _normalize_string(value: Any, *, field_name: str, max_bytes: int = MAX_STRING_BYTES, non_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise ValidationError("INVALID_STRING", f"{field_name} must be a string", field_name)
    try:
        encoded = value.encode("utf-8", "strict")
    except UnicodeEncodeError as exc:
        raise ValidationError("INVALID_UTF8", f"{field_name} must be UTF-8", field_name) from exc
    if non_empty and not value:
        raise ValidationError("EMPTY_STRING", f"{field_name} must not be empty", field_name)
    if len(encoded) > max_bytes:
        raise ValidationError("STRING_LIMIT", f"{field_name} exceeds its UTF-8 byte limit", field_name)
    return value


def _normalize_semantic_key_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise ValidationError("INVALID_LIST", f"{field_name} must be a list", field_name)
    return [validate_semantic_key(item, field_name=field_name) for item in value]


def validate_predicate(value: Mapping[str, Any], *, safety_context: bool = False) -> tuple[Predicate, dict[str, Any]]:
    if not isinstance(value, Mapping):
        raise ValidationError("INVALID_PREDICATE", "predicate must be an object")
    require_exact_keys(value, ("field", "op"), ("value", "from_checkpoint", "unknown_policy"))
    field_path = SemanticFieldPath.parse(value["field"])
    op = value["op"]
    if op not in PREDICATE_OPS:
        raise ValidationError("INVALID_PREDICATE_OP", "predicate op is not admitted", "op")
    unknown_policy = value.get("unknown_policy", "FAIL")
    if unknown_policy not in UNKNOWN_POLICIES:
        raise ValidationError("INVALID_UNKNOWN_POLICY", "unknown_policy is not admitted", "unknown_policy")
    if safety_context and unknown_policy != "FAIL":
        raise ValidationError("UNSAFE_UNKNOWN_POLICY", "safety predicates require unknown_policy=FAIL", "unknown_policy")
    predicate_value = value.get("value")
    if op in {"EQ", "NE", "LT", "LTE", "GT", "GTE", "IN_SET", "CONTAINS"} and "value" not in value:
        raise ValidationError("PREDICATE_VALUE_REQUIRED", f"predicate op {op} requires value")
    if op in {"EXISTS", "NOT_EXISTS", "CHANGED", "UNCHANGED"} and predicate_value is not None:
        raise ValidationError("PREDICATE_VALUE_FORBIDDEN", f"predicate op {op} does not accept a concrete value")
    if op == "IN_SET" and not isinstance(predicate_value, list):
        raise ValidationError("PREDICATE_VALUE_TYPE", "IN_SET requires a list value")
    from_checkpoint = value.get("from_checkpoint")
    if from_checkpoint is not None:
        from_checkpoint = validate_opaque_id(from_checkpoint, field_name="from_checkpoint", max_bytes=192)
    normalized = {
        "field": field_path.value,
        "op": op,
        "value": predicate_value,
        "from_checkpoint": from_checkpoint,
        "unknown_policy": unknown_policy,
    }
    return Predicate(field_path, op, predicate_value, from_checkpoint, unknown_policy), normalized


def validate_abort_condition(value: Mapping[str, Any]) -> tuple[AbortCondition, dict[str, Any]]:
    if not isinstance(value, Mapping):
        raise ValidationError("INVALID_ABORT_CONDITION", "abort condition must be an object")
    require_exact_keys(value, ("condition", "reason_code"), ("id",))
    identifier = value.get("id")
    if identifier is not None:
        identifier = validate_scenario_id(identifier, field_name="abort.id")
    predicate, normalized_predicate = validate_predicate(value["condition"], safety_context=True)
    reason_code = value["reason_code"]
    if reason_code not in STANDARD_ABORT_CODES:
        raise ValidationError("INVALID_ABORT_CODE", "abort reason_code is not admitted by Scenario v1")
    return AbortCondition(predicate, reason_code, identifier), {
        "id": identifier,
        "condition": normalized_predicate,
        "reason_code": reason_code,
    }


def _normalize_entity(value: Any) -> dict[str, Any]:
    ref = EntityRef.from_mapping(value)
    result: dict[str, Any] = {"kind": ref.kind}
    if ref.creature_id is not None:
        result["creature_id"] = ref.creature_id
    if ref.snapshot_path is not None:
        result["snapshot_path"] = ref.snapshot_path.value
    return result


def _normalize_item(value: Any) -> dict[str, Any]:
    ref = ItemRef.from_mapping(value)
    result: dict[str, Any] = {"kind": ref.kind}
    if ref.inventory_slot is not None:
        result["inventory_slot"] = ref.inventory_slot
    if ref.container_ref is not None:
        result["container_ref"] = ref.container_ref
    if ref.slot_index is not None:
        result["slot_index"] = ref.slot_index
    if ref.equipment_slot is not None:
        result["equipment_slot"] = ref.equipment_slot.value
    if ref.snapshot_path is not None:
        result["snapshot_path"] = ref.snapshot_path.value
    if ref.expected_semantic_item is not None:
        result["expected_semantic_item"] = ref.expected_semantic_item
    return result


def _normalize_destination(value: Any) -> dict[str, Any]:
    ref = DestinationRef.from_mapping(value)
    result: dict[str, Any] = {"kind": ref.kind}
    if ref.inventory_slot is not None:
        result["inventory_slot"] = ref.inventory_slot
    if ref.container_ref is not None:
        result["container_ref"] = ref.container_ref
    if ref.slot_index is not None:
        result["slot_index"] = ref.slot_index
    if ref.equipment_slot is not None:
        result["equipment_slot"] = ref.equipment_slot.value
    if ref.position is not None:
        result["position"] = {"x": ref.position.x, "y": ref.position.y, "z": ref.position.z}
    return result


def _enum(value: Any, allowed: set[str], field_name: str) -> str:
    if value not in allowed:
        raise ValidationError("INVALID_ENUM", f"{field_name} is not an admitted value", field_name)
    return str(value)


def validate_action_parameters(kind: str, value: Any) -> dict[str, Any]:
    if kind in NON_EXECUTABLE_PLACEHOLDERS:
        raise ValidationError("NON_EXECUTABLE_PLACEHOLDER", f"{kind} is not executable in Scenario v1")
    if kind not in ACTION_KINDS:
        raise ValidationError("UNSUPPORTED_ACTION_KIND", f"unknown Scenario v1 action kind: {kind}")
    if not isinstance(value, Mapping):
        raise ValidationError("INVALID_ACTION_PARAMETERS", "action parameters must be an object")
    if kind == "move":
        require_exact_keys(value, ("direction", "tiles"))
        if value["tiles"] != 1 or isinstance(value["tiles"], bool):
            raise ValidationError("MOVE_NOT_ATOMIC", "Scenario v1 move is exactly one tile")
        return {"direction": _enum(value["direction"], DIRECTIONS, "direction"), "tiles": 1}
    if kind == "turn":
        require_exact_keys(value, ("direction",))
        return {"direction": _enum(value["direction"], DIRECTIONS, "direction")}
    if kind in {"stop_movement", "cancel_attack", "cancel_follow", "logout"}:
        require_exact_keys(value, ())
        return {}
    if kind == "say_controlled_text":
        require_exact_keys(value, ("text", "text_class"))
        if value["text_class"] != "TEST_GENERATED":
            raise ValidationError("CHAT_CLASS_FORBIDDEN", "controlled chat text must be TEST_GENERATED")
        return {"text": _normalize_string(value["text"], field_name="text", max_bytes=256, non_empty=True), "text_class": "TEST_GENERATED"}
    if kind == "cast_spell":
        require_exact_keys(value, ("spell_key", "target"))
        target = None if value["target"] is None else _normalize_entity(value["target"])
        return {"spell_key": validate_semantic_key(value["spell_key"], field_name="spell_key"), "target": target}
    if kind in {"use_consumable", "use_rune"}:
        key_name = "consumable_key" if kind == "use_consumable" else "rune_key"
        require_exact_keys(value, (key_name, "target", "quantity"))
        if value["quantity"] != 1 or isinstance(value["quantity"], bool):
            raise ValidationError("ACTION_NOT_ATOMIC", f"{kind} quantity must be exactly 1")
        return {key_name: validate_semantic_key(value[key_name], field_name=key_name), "target": _normalize_entity(value["target"]), "quantity": 1}
    if kind == "eat_food":
        require_exact_keys(value, ("food_key", "quantity"))
        if value["quantity"] != 1 or isinstance(value["quantity"], bool):
            raise ValidationError("ACTION_NOT_ATOMIC", "eat_food quantity must be exactly 1")
        return {"food_key": validate_semantic_key(value["food_key"], field_name="food_key"), "quantity": 1}
    if kind in {"select_target", "attack", "follow"}:
        require_exact_keys(value, ("target",))
        return {"target": _normalize_entity(value["target"])}
    if kind == "open_container":
        require_exact_keys(value, ("item",))
        return {"item": _normalize_item(value["item"])}
    if kind == "close_container":
        require_exact_keys(value, ("container",))
        return {"container": validate_semantic_key(value["container"], field_name="container")}
    if kind == "use_item":
        require_exact_keys(value, ("item", "target"))
        target = value["target"]
        if target is None:
            normalized_target = None
        elif isinstance(target, Mapping) and target.get("kind") in {"SELF", "SELECTED_TARGET", "CREATURE_ID", "SNAPSHOT_PATH"}:
            normalized_target = _normalize_entity(target)
        else:
            normalized_target = _normalize_destination(target)
        return {"item": _normalize_item(value["item"]), "target": normalized_target}
    if kind == "look_item":
        require_exact_keys(value, ("item",))
        return {"item": _normalize_item(value["item"])}
    if kind == "move_item":
        require_exact_keys(value, ("item", "destination", "count"))
        count = checked_non_negative(value["count"], maximum=MAX_I32, field_name="count")
        if count < 1:
            raise ValidationError("MOVE_ITEM_COUNT", "move_item count must be positive")
        return {"item": _normalize_item(value["item"]), "destination": _normalize_destination(value["destination"]), "count": count}
    if kind == "equip":
        require_exact_keys(value, ("item", "slot"))
        try:
            slot = EquipmentSlot(value["slot"]).value
        except (TypeError, ValueError) as exc:
            raise ValidationError("INVALID_EQUIPMENT_SLOT", "slot is invalid") from exc
        return {"item": _normalize_item(value["item"]), "slot": slot}
    if kind == "unequip":
        require_exact_keys(value, ("slot", "destination"))
        try:
            slot = EquipmentSlot(value["slot"]).value
        except (TypeError, ValueError) as exc:
            raise ValidationError("INVALID_EQUIPMENT_SLOT", "slot is invalid") from exc
        return {"slot": slot, "destination": _normalize_destination(value["destination"])}
    if kind in {"open_panel", "close_panel"}:
        require_exact_keys(value, ("panel_key",))
        return {"panel_key": validate_semantic_key(value["panel_key"], field_name="panel_key")}
    raise ValidationError("UNSUPPORTED_ACTION_KIND", f"unhandled Scenario v1 action kind: {kind}")


def default_effect_bound(kind: str, parameters: Mapping[str, Any]) -> EffectBound:
    if kind not in ACTION_KINDS:
        raise ValidationError("UNBOUNDED_EFFECT", "cannot produce a finite EffectBound for unsupported action")
    base = {name: 0 for name in (
        "max_actions", "max_movement_tiles", "max_spells", "max_consumables",
        "max_items_moved", "max_gold", "max_tibia_coins", "max_irreversible_changes",
    )}
    base["max_actions"] = 1
    if kind == "move":
        base["max_movement_tiles"] = 1
    elif kind == "cast_spell":
        base["max_spells"] = 1
    elif kind in {"use_consumable", "eat_food", "use_rune", "use_item"}:
        base["max_consumables"] = 1
    elif kind == "move_item":
        base["max_items_moved"] = int(parameters["count"])
        if parameters["destination"]["kind"] == "GROUND_POSITION":
            base["max_irreversible_changes"] = 1
    elif kind in {"equip", "unequip"}:
        base["max_items_moved"] = 1
        if kind == "unequip" and parameters["destination"]["kind"] == "GROUND_POSITION":
            base["max_irreversible_changes"] = 1
    elif kind == "logout":
        base["max_irreversible_changes"] = 1
    return EffectBound(**base, measurable_after=True, reason_codes=(f"SCENARIO_V1_{kind.upper()}",))


def _normalize_capture_policy(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValidationError("INVALID_CAPTURE_POLICY", "capture_policy must be an object")
    require_exact_keys(value, ("state", "events", "screenshots", "network", "traces"))
    if not isinstance(value["state"], bool) or not isinstance(value["events"], bool):
        raise ValidationError("INVALID_CAPTURE_POLICY", "capture state/events must be booleans")
    return {
        "state": value["state"],
        "events": value["events"],
        "screenshots": _enum(value["screenshots"], {"NONE", "BEFORE_AFTER", "CHECKPOINTS"}, "screenshots"),
        "network": _enum(value["network"], {"NONE", "METADATA"}, "network"),
        "traces": _enum(value["traces"], {"NONE", "TARGETED"}, "traces"),
    }


def _normalize_privacy_policy(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValidationError("INVALID_PRIVACY_POLICY", "privacy_policy must be an object")
    require_exact_keys(value, ("secret_material", "private_chat", "identities", "screenshots"))
    if value["secret_material"] != "REJECT":
        raise ValidationError("PRIVACY_WEAKENING", "secret_material is fixed to REJECT in Scenario v1")
    return {
        "secret_material": "REJECT",
        "private_chat": _enum(value["private_chat"], {"OMIT", "REDACT"}, "private_chat"),
        "identities": _enum(value["identities"], {"KEEP_TEST_ONLY", "HASH_NON_SECRET", "OMIT"}, "identities"),
        "screenshots": _enum(value["screenshots"], {"SAFE_ONLY", "QUARANTINE_UNKNOWN"}, "screenshots"),
    }


def _normalize_retry(value: Any) -> dict[str, Any]:
    if value is None:
        return {"max_attempts": 1, "retry_on": []}
    if not isinstance(value, Mapping):
        raise ValidationError("INVALID_RETRY", "retry must be an object")
    require_exact_keys(value, ("max_attempts", "retry_on"))
    attempts = checked_non_negative(value["max_attempts"], maximum=3, field_name="max_attempts")
    if attempts < 1:
        raise ValidationError("INVALID_RETRY", "retry.max_attempts must be in 1..3")
    retry_on = value["retry_on"]
    if not isinstance(retry_on, list) or any(item not in RETRYABLE_PRE_DISPATCH for item in retry_on):
        raise ValidationError("INVALID_RETRY", "retry_on contains a non-pre-dispatch state")
    if len(set(retry_on)) != len(retry_on):
        raise ValidationError("DUPLICATE_RETRY_STATE", "retry_on cannot contain duplicates")
    return {"max_attempts": attempts, "retry_on": list(retry_on)}


def _normalize_step(step: Any, scenario_id: str, ordinal: int) -> ValidatedStep:
    if not isinstance(step, Mapping) or len(step) != 1:
        raise ValidationError("INVALID_STEP_UNION", "each scenario step must contain exactly one step kind")
    step_type, body = next(iter(step.items()))
    if step_type not in {"snapshot", "action", "wait", "assert", "checkpoint"}:
        raise ValidationError("INVALID_STEP_KIND", f"unsupported step kind: {step_type}")
    if not isinstance(body, Mapping):
        raise ValidationError("INVALID_STEP", f"{step_type} step body must be an object")
    local_id = body.get("id")
    if local_id is not None:
        local_id = validate_scenario_id(local_id, field_name="step.id")
        step_id = f"{scenario_id}:{local_id}"
    else:
        step_id = f"{scenario_id}:step-{ordinal:04d}"
    if len(step_id.encode("utf-8")) > 192:
        raise ValidationError("STEP_ID_TOO_LONG", "derived step_id exceeds 192 bytes")
    if step_type == "snapshot":
        require_exact_keys(body, ("name",), ("id",))
        normalized = {"id": local_id, "name": _normalize_string(body["name"], field_name="snapshot.name", non_empty=True)}
    elif step_type == "checkpoint":
        require_exact_keys(body, ("label",), ("id",))
        normalized = {"id": local_id, "label": _normalize_string(body["label"], field_name="checkpoint.label", non_empty=True)}
    elif step_type == "wait":
        require_exact_keys(body, ("condition", "timeout_ms"), ("id",))
        _, normalized_predicate = validate_predicate(body["condition"])
        timeout = checked_non_negative(body["timeout_ms"], maximum=MAX_TIMEOUT_MS, field_name="timeout_ms")
        if timeout < 1:
            raise ValidationError("TIMEOUT_RANGE", "timeout_ms must be in 1..300000")
        normalized = {"id": local_id, "condition": normalized_predicate, "timeout_ms": timeout}
    elif step_type == "assert":
        require_exact_keys(body, ("condition",), ("id",))
        _, normalized_predicate = validate_predicate(body["condition"])
        normalized = {"id": local_id, "condition": normalized_predicate}
    else:
        require_exact_keys(body, ("kind", "parameters", "timeout_ms"), ("id", "retry"))
        kind = validate_semantic_key(body["kind"], field_name="action.kind")
        parameters = validate_action_parameters(kind, body["parameters"])
        timeout = checked_non_negative(body["timeout_ms"], maximum=MAX_TIMEOUT_MS, field_name="timeout_ms")
        if timeout < 1:
            raise ValidationError("TIMEOUT_RANGE", "timeout_ms must be in 1..300000")
        normalized = {
            "id": local_id,
            "kind": kind,
            "parameters": parameters,
            "timeout_ms": timeout,
            "retry": _normalize_retry(body.get("retry")),
        }
    return ValidatedStep(step_id, step_type, normalized)


def validate_scenario(value: Mapping[str, Any]) -> ValidatedScenario:
    if not isinstance(value, Mapping):
        raise ValidationError("INVALID_SCENARIO", "scenario root must be an object")
    require_exact_keys(value, (
        "schema_version", "id", "name", "adapter_requirements", "preconditions",
        "side_effect_budget", "capture_policy", "steps", "abort_conditions",
        "expected_result", "privacy_policy",
    ))
    if value["schema_version"] != 1 or isinstance(value["schema_version"], bool):
        raise ValidationError("UNSUPPORTED_SCENARIO_MAJOR", "Scenario v1 requires schema_version=1")
    scenario_id = validate_scenario_id(value["id"])
    name = _normalize_string(value["name"], field_name="name", non_empty=True)
    adapter_requirements = value["adapter_requirements"]
    if not isinstance(adapter_requirements, Mapping):
        raise ValidationError("INVALID_ADAPTER_REQUIREMENTS", "adapter_requirements must be an object")
    require_exact_keys(adapter_requirements, ("reads", "actions"))
    reads = _normalize_semantic_key_list(adapter_requirements["reads"], "adapter_requirements.reads")
    actions = _normalize_semantic_key_list(adapter_requirements["actions"], "adapter_requirements.actions")
    preconditions = value["preconditions"]
    if not isinstance(preconditions, list):
        raise ValidationError("INVALID_PRECONDITIONS", "preconditions must be a list")
    normalized_preconditions = [validate_predicate(item, safety_context=True)[1] for item in preconditions]
    budget = SideEffectBudget.from_mapping(value["side_effect_budget"])
    capture_policy = _normalize_capture_policy(value["capture_policy"])
    privacy_policy = _normalize_privacy_policy(value["privacy_policy"])
    steps_raw = value["steps"]
    if not isinstance(steps_raw, list) or not steps_raw:
        raise ValidationError("INVALID_STEPS", "steps must be a non-empty list")
    if len(steps_raw) > MAX_STEPS:
        raise ValidationError("STEP_LIMIT", "scenario exceeds Package A max_steps")
    validated_steps = tuple(_normalize_step(step, scenario_id, index) for index, step in enumerate(steps_raw, 1))
    step_ids = [step.step_id for step in validated_steps]
    if len(set(step_ids)) != len(step_ids):
        raise ValidationError("DUPLICATE_STEP_ID", "derived scenario step IDs must be unique")
    aborts = value["abort_conditions"]
    if not isinstance(aborts, list):
        raise ValidationError("INVALID_ABORT_CONDITIONS", "abort_conditions must be a list")
    normalized_aborts = [validate_abort_condition(item)[1] for item in aborts]
    expected = value["expected_result"]
    if not isinstance(expected, list):
        raise ValidationError("INVALID_EXPECTED_RESULT", "expected_result must be a list")
    normalized_expected = [validate_predicate(item)[1] for item in expected]
    normalized_ast = {
        "schema_version": 1,
        "id": scenario_id,
        "name": name,
        "adapter_requirements": {"reads": reads, "actions": actions},
        "preconditions": normalized_preconditions,
        "side_effect_budget": budget.as_dict(),
        "capture_policy": capture_policy,
        "steps": [{step.step_type: dict(step.body)} for step in validated_steps],
        "abort_conditions": normalized_aborts,
        "expected_result": normalized_expected,
        "privacy_policy": privacy_policy,
    }
    _walk_limits(normalized_ast)
    return ValidatedScenario(
        normalized_ast,
        sha256_jcs(normalized_ast),
        scenario_id,
        validated_steps,
        budget,
        tuple(reads),
        tuple(actions),
        any(step.step_type == "action" for step in validated_steps),
    )


def parse_and_validate(data: bytes | str) -> ValidatedScenario:
    return validate_scenario(parse_document(data))


def validation_result(data: bytes | str) -> ScenarioValidationResult:
    try:
        scenario = parse_and_validate(data)
        return ScenarioValidationResult(
            True, 1, scenario.scenario_id, scenario.scenario_hash,
            tuple(step.step_id for step in scenario.steps),
            scenario.required_reads, scenario.required_actions, (),
        )
    except ValidationError as exc:
        return ScenarioValidationResult(
            False, 1, None, None, (), (), (),
            ({"code": exc.code, "step_id": None, "field": exc.field, "safe_message": exc.safe_message},),
        )


def action_request_hash(
    *,
    schema_version: int,
    run_id: str,
    step_id: str,
    attempt_index: int,
    kind: str,
    parameters: Mapping[str, Any],
    timeout_ms: int,
    required_capability: str,
    required_authority: Authority | str,
) -> str:
    authority_value = required_authority.value if isinstance(required_authority, Authority) else str(required_authority)
    return sha256_jcs({
        "schema_version": schema_version,
        "run_id": run_id,
        "step_id": step_id,
        "attempt_index": attempt_index,
        "kind": kind,
        "parameters": dict(parameters),
        "timeout_ms": timeout_ms,
        "required_capability": required_capability,
        "required_authority": authority_value,
    })


_UNKNOWN = object()


def _lookup_path(snapshot: Mapping[str, Any], path: SemanticFieldPath) -> Any:
    current: Any = snapshot
    for segment in path.value.split("."):
        if not isinstance(current, Mapping) or segment not in current:
            return _UNKNOWN
        current = current[segment]
        if current is None:
            return _UNKNOWN
    return current


def evaluate_predicate(predicate: Predicate, snapshot: Mapping[str, Any], *, checkpoint: Mapping[str, Any] | None = None) -> PredicateOutcome:
    value = _lookup_path(snapshot, predicate.field)
    if predicate.op == "EXISTS":
        return PredicateOutcome.TRUE if value is not _UNKNOWN else PredicateOutcome.FALSE
    if predicate.op == "NOT_EXISTS":
        return PredicateOutcome.TRUE if value is _UNKNOWN else PredicateOutcome.FALSE
    if value is _UNKNOWN:
        return PredicateOutcome.UNKNOWN
    try:
        if predicate.op in {"CHANGED", "UNCHANGED"}:
            if checkpoint is None:
                return PredicateOutcome.UNKNOWN
            previous = _lookup_path(checkpoint, predicate.field)
            if previous is _UNKNOWN:
                return PredicateOutcome.UNKNOWN
            changed = value != previous
            return PredicateOutcome.TRUE if (changed if predicate.op == "CHANGED" else not changed) else PredicateOutcome.FALSE
        expected = predicate.value
        if predicate.op in {"LT", "LTE", "GT", "GTE"}:
            if isinstance(value, bool) or isinstance(expected, bool) or not isinstance(value, (int, float)) or not isinstance(expected, (int, float)):
                return PredicateOutcome.ERROR
            result = {"LT": value < expected, "LTE": value <= expected, "GT": value > expected, "GTE": value >= expected}[predicate.op]
        elif predicate.op in {"EQ", "NE"}:
            compatible_numeric = (
                isinstance(value, (int, float)) and not isinstance(value, bool)
                and isinstance(expected, (int, float)) and not isinstance(expected, bool)
            )
            if type(value) is not type(expected) and not compatible_numeric:
                return PredicateOutcome.ERROR
            result = value == expected
            if predicate.op == "NE":
                result = not result
        elif predicate.op == "IN_SET":
            result = value in expected
        elif predicate.op == "CONTAINS":
            if not isinstance(value, (str, list, tuple, set, dict)):
                return PredicateOutcome.ERROR
            result = expected in value
        else:
            return PredicateOutcome.ERROR
        return PredicateOutcome.TRUE if result else PredicateOutcome.FALSE
    except (TypeError, ValueError):
        return PredicateOutcome.ERROR


def resolve_unknown_policy(outcome: PredicateOutcome, policy: str) -> bool | None:
    if outcome == PredicateOutcome.TRUE:
        return True
    if outcome == PredicateOutcome.FALSE:
        return False
    if outcome == PredicateOutcome.ERROR:
        return False
    if policy == "ACCEPT":
        return True
    if policy == "WAIT":
        return None
    return False
