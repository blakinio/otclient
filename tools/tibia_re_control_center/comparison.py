from __future__ import annotations

import math
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Any

from .model import ValidationError


class ComparisonClass(str, Enum):
    EXACT = "EXACT"
    NORMALIZED_EXACT = "NORMALIZED_EXACT"
    SET_EQUIVALENT = "SET_EQUIVALENT"
    ORDERED_EQUIVALENT = "ORDERED_EQUIVALENT"
    TOLERANCE = "TOLERANCE"
    REFERENCE_ONLY = "REFERENCE_ONLY"
    NOT_COMPARABLE = "NOT_COMPARABLE"


class ObservationStatus(str, Enum):
    OBSERVED = "OBSERVED"
    UNKNOWN = "UNKNOWN"
    NOT_SUPPORTED = "NOT_SUPPORTED"
    NOT_OBSERVABLE = "NOT_OBSERVABLE"
    STALE = "STALE"


class FieldStatus(str, Enum):
    MATCH = "MATCH"
    MISMATCH = "MISMATCH"
    COVERAGE_GAP = "COVERAGE_GAP"
    REFERENCE_ONLY = "REFERENCE_ONLY"
    NOT_COMPARABLE = "NOT_COMPARABLE"


class ComparisonStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    COVERAGE_INCOMPLETE = "COVERAGE_INCOMPLETE"
    INVALID_INPUT = "INVALID_INPUT"


@dataclass(frozen=True)
class CheckpointPair:
    checkpoint_id: str
    reference_step_id: str
    candidate_step_id: str
    transition: str = "AFTER"


@dataclass(frozen=True)
class NormalizedObservation:
    field: str
    checkpoint_id: str
    status: ObservationStatus
    value: Any = None
    source_quality: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class ProfileField:
    path: str
    comparison_class: ComparisonClass
    normalizer: str | None = None
    set_key: str | None = None
    absolute_tolerance: float | None = None
    relative_tolerance: float | None = None
    time_tolerance_ms: int | None = None
    required: bool = True
    tolerance_mode: str = "ANY"

    def __post_init__(self) -> None:
        for value in (self.absolute_tolerance, self.relative_tolerance):
            if value is not None and (
                not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0
            ):
                raise ValidationError("INVALID_TOLERANCE", "comparison tolerance must be finite and non-negative")
        if self.time_tolerance_ms is not None and (
            isinstance(self.time_tolerance_ms, bool) or self.time_tolerance_ms < 0
        ):
            raise ValidationError("INVALID_TOLERANCE", "time_tolerance_ms must be non-negative")
        if self.tolerance_mode not in {"ANY", "ALL"}:
            raise ValidationError("INVALID_TOLERANCE_MODE", "tolerance_mode must be ANY or ALL")


@dataclass(frozen=True)
class ComparisonProfile:
    profile_id: str
    profile_version: str
    fields: tuple[ProfileField, ...]
    schema_version: int = 1


@dataclass(frozen=True)
class FieldComparisonResult:
    field: str
    checkpoint_id: str
    comparison_class: ComparisonClass
    status: FieldStatus
    reference_status: ObservationStatus | None
    candidate_status: ObservationStatus | None
    normalized_reference: Any = None
    normalized_candidate: Any = None
    delta: Any = None
    tolerance_used: Mapping[str, Any] | None = None
    reason_code: str | None = None
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class ComparisonResult:
    comparison_id: str
    profile_id: str
    profile_version: str
    reference_run_id: str
    candidate_run_id: str
    scenario_id: str
    status: ComparisonStatus
    field_results: tuple[FieldComparisonResult, ...]
    reason_code: str | None = None
    schema_version: int = 1


def _identity(value: Any) -> Any:
    return value


def _position_xyz(value: Any) -> tuple[int, int, int]:
    if not isinstance(value, Mapping) or set(value) != {"x", "y", "z"}:
        raise ValidationError("NORMALIZER_INPUT_INVALID", "position_xyz_v1 requires exactly x/y/z")
    return int(value["x"]), int(value["y"]), int(value["z"])


def _semantic_collection(value: Any) -> tuple[Any, ...]:
    if isinstance(value, Mapping):
        return tuple(sorted((str(key), repr(item)) for key, item in value.items()))
    if isinstance(value, (list, tuple, set)):
        return tuple(sorted(repr(item) for item in value))
    raise ValidationError("NORMALIZER_INPUT_INVALID", "semantic collection normalizer requires a collection")


_NORMALIZERS: dict[str, Callable[[Any], Any]] = {
    "identity_v1": _identity,
    "position_xyz_v1": _position_xyz,
    "condition_semantic_key_v1": _semantic_collection,
    "inventory_slots_v1": _semantic_collection,
    "container_contents_v1": _semantic_collection,
    "equipment_slots_v1": _semantic_collection,
    "cooldown_key_v1": _semantic_collection,
}


def _normalize(rule: ProfileField, value: Any) -> Any:
    if rule.normalizer is None:
        return value
    normalizer = _NORMALIZERS.get(rule.normalizer)
    if normalizer is None:
        raise ValidationError("NORMALIZER_UNAVAILABLE", f"comparison normalizer is unavailable: {rule.normalizer}")
    return normalizer(value)


def _set_value(value: Any, set_key: str | None) -> tuple[Any, ...]:
    if not isinstance(value, (list, tuple, set)):
        raise ValidationError("SET_INPUT_INVALID", "set comparison requires a collection")
    if set_key is None:
        return tuple(sorted(repr(item) for item in value))
    keys = []
    for item in value:
        if not isinstance(item, Mapping) or set_key not in item:
            raise ValidationError("SET_KEY_MISSING", "set comparison item is missing its declared key")
        keys.append(repr(item[set_key]))
    return tuple(sorted(keys))


def _tolerance(rule: ProfileField, reference: Any, candidate: Any) -> tuple[bool, float, dict[str, Any]]:
    if (
        isinstance(reference, bool)
        or isinstance(candidate, bool)
        or not isinstance(reference, (int, float))
        or not isinstance(candidate, (int, float))
    ):
        raise ValidationError("TOLERANCE_INPUT_INVALID", "tolerance comparison requires finite numeric values")
    if not math.isfinite(reference) or not math.isfinite(candidate):
        raise ValidationError("TOLERANCE_INPUT_INVALID", "tolerance comparison requires finite numeric values")
    delta = abs(float(candidate) - float(reference))
    checks: list[bool] = []
    used: dict[str, Any] = {"mode": rule.tolerance_mode}
    if rule.absolute_tolerance is not None:
        checks.append(delta <= float(rule.absolute_tolerance))
        used["absolute_tolerance"] = rule.absolute_tolerance
    if rule.relative_tolerance is not None:
        relative_limit = float(rule.relative_tolerance) * max(abs(float(reference)), 1e-12)
        checks.append(delta <= relative_limit)
        used["relative_tolerance"] = rule.relative_tolerance
    if rule.time_tolerance_ms is not None:
        checks.append(delta <= float(rule.time_tolerance_ms))
        used["time_tolerance_ms"] = rule.time_tolerance_ms
    if not checks:
        raise ValidationError("TOLERANCE_UNSPECIFIED", "TOLERANCE comparison requires a finite bound")
    return (any(checks) if rule.tolerance_mode == "ANY" else all(checks)), delta, used


def _coverage_reason(status: ObservationStatus | None, side: str) -> str:
    if status is None:
        return "CHECKPOINT_UNAVAILABLE"
    return f"{status.value}_{side.upper()}"


def compare_field(
    rule: ProfileField,
    pair: CheckpointPair,
    reference: NormalizedObservation | None,
    candidate: NormalizedObservation | None,
) -> FieldComparisonResult:
    reference_status = None if reference is None else reference.status
    candidate_status = None if candidate is None else candidate.status
    if rule.comparison_class == ComparisonClass.NOT_COMPARABLE:
        return FieldComparisonResult(
            rule.path, pair.checkpoint_id, rule.comparison_class,
            FieldStatus.NOT_COMPARABLE, reference_status, candidate_status,
            reason_code="NOT_COMPARABLE",
        )
    if rule.comparison_class == ComparisonClass.REFERENCE_ONLY:
        return FieldComparisonResult(
            rule.path, pair.checkpoint_id, rule.comparison_class,
            FieldStatus.REFERENCE_ONLY, reference_status, candidate_status,
            reason_code="REFERENCE_ONLY",
        )
    if reference is None or reference.status != ObservationStatus.OBSERVED:
        return FieldComparisonResult(
            rule.path, pair.checkpoint_id, rule.comparison_class,
            FieldStatus.COVERAGE_GAP, reference_status, candidate_status,
            reason_code=_coverage_reason(reference_status, "reference"),
        )
    if candidate is None or candidate.status != ObservationStatus.OBSERVED:
        return FieldComparisonResult(
            rule.path, pair.checkpoint_id, rule.comparison_class,
            FieldStatus.COVERAGE_GAP, reference.status, candidate_status,
            reason_code=_coverage_reason(candidate_status, "candidate"),
        )
    ref_value = _normalize(rule, reference.value)
    candidate_value = _normalize(rule, candidate.value)
    delta: Any = None
    tolerance_used: Mapping[str, Any] | None = None
    if rule.comparison_class in {ComparisonClass.EXACT, ComparisonClass.NORMALIZED_EXACT}:
        matched = ref_value == candidate_value
    elif rule.comparison_class == ComparisonClass.SET_EQUIVALENT:
        matched = _set_value(ref_value, rule.set_key) == _set_value(candidate_value, rule.set_key)
    elif rule.comparison_class == ComparisonClass.ORDERED_EQUIVALENT:
        if not isinstance(ref_value, (list, tuple)) or not isinstance(candidate_value, (list, tuple)):
            raise ValidationError("ORDERED_INPUT_INVALID", "ordered comparison requires sequences")
        matched = tuple(ref_value) == tuple(candidate_value)
    elif rule.comparison_class == ComparisonClass.TOLERANCE:
        matched, delta, tolerance_used = _tolerance(rule, ref_value, candidate_value)
    else:
        raise ValidationError("COMPARISON_CLASS_UNSUPPORTED", "comparison class is not implemented")
    return FieldComparisonResult(
        rule.path,
        pair.checkpoint_id,
        rule.comparison_class,
        FieldStatus.MATCH if matched else FieldStatus.MISMATCH,
        reference.status,
        candidate.status,
        ref_value,
        candidate_value,
        delta=delta,
        tolerance_used=tolerance_used,
        reason_code=None if matched else "VALUE_MISMATCH",
    )


def compare_runs(
    *,
    comparison_id: str,
    profile: ComparisonProfile,
    reference_run_id: str,
    candidate_run_id: str,
    scenario_id: str,
    reference_scenario_hash: str,
    candidate_scenario_hash: str,
    checkpoint_pairs: Iterable[CheckpointPair],
    reference_observations: Mapping[tuple[str, str], NormalizedObservation],
    candidate_observations: Mapping[tuple[str, str], NormalizedObservation],
) -> ComparisonResult:
    if reference_scenario_hash != candidate_scenario_hash:
        return ComparisonResult(
            comparison_id,
            profile.profile_id,
            profile.profile_version,
            reference_run_id,
            candidate_run_id,
            scenario_id,
            ComparisonStatus.INVALID_INPUT,
            (),
            reason_code="SCENARIO_MISMATCH",
        )
    pairs = tuple(checkpoint_pairs)
    if not pairs and any(field.required for field in profile.fields):
        return ComparisonResult(
            comparison_id,
            profile.profile_id,
            profile.profile_version,
            reference_run_id,
            candidate_run_id,
            scenario_id,
            ComparisonStatus.COVERAGE_INCOMPLETE,
            (),
            reason_code="REQUIRED_CHECKPOINT_COVERAGE_MISSING",
        )
    results: list[FieldComparisonResult] = []
    required_by_path = {field.path: field.required for field in profile.fields}
    for pair in pairs:
        for rule in profile.fields:
            reference = reference_observations.get((pair.reference_step_id, rule.path))
            candidate = candidate_observations.get((pair.candidate_step_id, rule.path))
            results.append(compare_field(rule, pair, reference, candidate))
    required_mismatch = any(
        result.status == FieldStatus.MISMATCH and required_by_path.get(result.field, False)
        for result in results
    )
    required_gap = any(
        result.status == FieldStatus.COVERAGE_GAP and required_by_path.get(result.field, False)
        for result in results
    )
    status = (
        ComparisonStatus.FAIL
        if required_mismatch
        else ComparisonStatus.COVERAGE_INCOMPLETE
        if required_gap
        else ComparisonStatus.PASS
    )
    return ComparisonResult(
        comparison_id,
        profile.profile_id,
        profile.profile_version,
        reference_run_id,
        candidate_run_id,
        scenario_id,
        status,
        tuple(results),
    )
