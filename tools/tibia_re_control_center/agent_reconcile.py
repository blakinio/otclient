"""Deterministic, authority-neutral reconciliation of visual and runtime evidence.

This module deliberately has no runtime producer or action surface.  It only
combines a bounded visual observation with runtime evidence that a separate,
Control-Center-owned context verifies as reviewed and current.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from math import isfinite
from typing import Any

from .agent_vision import QWEN_VISION_PROFILE_ID, VisionObservation
from .model import PrivacyError, ValidationError
from .recorder import ensure_no_secret_material


class RuntimeEvidenceClass(str, Enum):
    UNKNOWN = "UNKNOWN"
    STRUCTURAL_ONLY = "STRUCTURAL_ONLY"
    REVIEWED_CAUSAL = "REVIEWED_CAUSAL"


@dataclass(frozen=True)
class RuntimeObservation:
    state: str
    evidence_class: RuntimeEvidenceClass
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True)
class ReviewedRuntimeProducer:
    """A Control-Center-reviewed producer and its exact evidence contract."""

    producer_id: str
    contract_id: str


@dataclass(frozen=True)
class TrustedRuntimeEvidence:
    """Control-Center-owned binding for one exact runtime observation."""

    observation: RuntimeObservation
    session_id: str
    run_id: str
    runtime_id: str
    runtime_instance_id: str
    producer_id: str
    producer_contract_id: str
    observed_monotonic_ns: int


@dataclass(frozen=True)
class TrustedReconciliationContext:
    """Current Control Center facts used to verify reviewed runtime evidence.

    The repository supplies no live producer.  Tests inject this narrow value
    in place of the future Control-Center-owned resolver boundary.  Its two
    monotonic values must come from the same Control Center clock domain.
    """

    current_session_id: str
    current_run_id: str
    current_runtime_id: str
    current_runtime_instance_id: str
    current_monotonic_ns: int
    max_age_ns: int
    reviewed_producers: tuple[ReviewedRuntimeProducer, ...]
    runtime_evidence: TrustedRuntimeEvidence


class ReconciledState(str, Enum):
    UNKNOWN = "UNKNOWN"
    LOGIN_SCREEN = "LOGIN_SCREEN"
    CHARACTER_SELECT = "CHARACTER_SELECT"
    WORLD_CONFIRMED = "WORLD_CONFIRMED"
    WORLD_EXIT = "WORLD_EXIT"
    CONFLICT = "CONFLICT"


@dataclass(frozen=True)
class ReconciliationResult:
    """A semantic result plus the validated provenance retained for it."""

    state: ReconciledState
    visual_evidence_refs: tuple[str, ...]
    runtime_evidence_refs: tuple[str, ...]


_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_MAX_REF_BYTES = 128
_MAX_VISIBLE_TEXT_ENTRIES = 256
_MAX_VISIBLE_TEXT_BYTES = 4096

# ``IN_GAME_VISUAL`` and ``WORLD_EXIT`` are the Task 5 model vocabulary;
# Task 5's sensor normally emits their normalized forms.  No trimming or case
# folding is permitted, so untrusted spelling cannot acquire semantics.
_VISUAL_NORMALIZATION = {
    "UNKNOWN": "UNKNOWN",
    "OTHER": "UNKNOWN",
    "LOGIN_SCREEN": "LOGIN_SCREEN",
    "CHARACTER_SELECT": "CHARACTER_SELECT",
    "WORLD_VISUAL": "WORLD_VISUAL",
    "IN_GAME_VISUAL": "WORLD_VISUAL",
    "WORLD_EXIT_VISUAL": "WORLD_EXIT_VISUAL",
    "WORLD_EXIT": "WORLD_EXIT_VISUAL",
    "ERROR_SCREEN": "ERROR_SCREEN",
}

# The result-producing cases are intentionally finite.  Every unlisted
# combination is inconclusive rather than an inferred semantic state.
_RULES = {
    ("WORLD_VISUAL", "IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL): ReconciledState.WORLD_CONFIRMED,
    ("UNKNOWN", "IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL): ReconciledState.WORLD_CONFIRMED,
    ("LOGIN_SCREEN", "IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL): ReconciledState.CONFLICT,
    ("CHARACTER_SELECT", "IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL): ReconciledState.CONFLICT,
    ("WORLD_EXIT_VISUAL", "IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL): ReconciledState.CONFLICT,
    ("WORLD_VISUAL", "WORLD_EXIT", RuntimeEvidenceClass.REVIEWED_CAUSAL): ReconciledState.CONFLICT,
    ("LOGIN_SCREEN", "WORLD_EXIT", RuntimeEvidenceClass.REVIEWED_CAUSAL): ReconciledState.CONFLICT,
    ("CHARACTER_SELECT", "WORLD_EXIT", RuntimeEvidenceClass.REVIEWED_CAUSAL): ReconciledState.CONFLICT,
    ("WORLD_EXIT_VISUAL", "WORLD_EXIT", RuntimeEvidenceClass.REVIEWED_CAUSAL): ReconciledState.WORLD_EXIT,
    ("UNKNOWN", "WORLD_EXIT", RuntimeEvidenceClass.REVIEWED_CAUSAL): ReconciledState.WORLD_EXIT,
}


def _safe_ref(value: Any) -> str | None:
    """Validate a retained provenance token without exposing invalid input."""
    if type(value) is not str or not value or value in {".", ".."}:
        return None
    try:
        encoded = value.encode("utf-8", "strict")
    except UnicodeEncodeError:
        return None
    if (
        len(encoded) > _MAX_REF_BYTES
        or any(0xD800 <= ord(char) <= 0xDFFF for char in value)
        or any(ord(char) < 0x20 or ord(char) == 0x7F for char in value)
        or "/" in value
        or "\\" in value
    ):
        return None
    try:
        ensure_no_secret_material(value, key_path="reconciliation.evidence_ref")
    except (PrivacyError, ValidationError):
        return None
    return value


def _safe_visible_text(value: Any) -> bool:
    if type(value) is not tuple or len(value) > _MAX_VISIBLE_TEXT_ENTRIES:
        return False
    for item in value:
        if type(item) is not str:
            return False
        try:
            encoded = item.encode("utf-8", "strict")
        except UnicodeEncodeError:
            return False
        if (
            len(encoded) > _MAX_VISIBLE_TEXT_BYTES
            or any(0xD800 <= ord(char) <= 0xDFFF for char in item)
            or any(ord(char) < 0x20 or ord(char) == 0x7F for char in item)
        ):
            return False
        try:
            ensure_no_secret_material(item, key_path="reconciliation.visible_text")
        except (PrivacyError, ValidationError):
            return False
    return True


def _visual_parts(visual: Any) -> tuple[str | None, tuple[str, ...]]:
    if type(visual) is not VisionObservation:
        return None, ()
    if (
        type(visual.screen_class) is not str
        or type(visual.capture_sha256) is not str
        or type(visual.model_profile_id) is not str
        or not _SHA256.fullmatch(visual.capture_sha256)
        or not _safe_visible_text(visual.visible_text)
        or visual.model_profile_id != QWEN_VISION_PROFILE_ID
        or visual.visual_only is not True
        or visual.structural_authority is not False
    ):
        return None, ()
    if visual.confidence is not None and (
        type(visual.confidence) is not float
        or not isfinite(visual.confidence)
        or not 0.0 <= visual.confidence <= 1.0
    ):
        return None, ()
    screen = _VISUAL_NORMALIZATION.get(visual.screen_class)
    evidence_ref = _safe_ref(visual.evidence_ref)
    profile_ref = _safe_ref(visual.model_profile_id)
    if screen is None or evidence_ref is None or profile_ref is None:
        return None, ()
    return screen, (evidence_ref,)


def _runtime_parts(runtime: Any) -> tuple[str | None, RuntimeEvidenceClass | None, tuple[str, ...]]:
    if type(runtime) is not RuntimeObservation:
        return None, None, ()
    if (
        type(runtime.state) is not str
        or type(runtime.evidence_class) is not RuntimeEvidenceClass
        or type(runtime.evidence_refs) is not tuple
    ):
        return None, None, ()
    if runtime.state not in {"UNKNOWN", "IN_GAME", "WORLD_EXIT"}:
        return None, None, ()
    refs: list[str] = []
    for value in runtime.evidence_refs:
        ref = _safe_ref(value)
        if ref is None:
            return None, None, ()
        refs.append(ref)
    return runtime.state, runtime.evidence_class, tuple(refs)


def _trusted_reviewed_runtime(
    runtime: RuntimeObservation,
    trusted_context: Any,
) -> bool:
    """Verify current provenance without interpreting opaque evidence refs."""
    if type(trusted_context) is not TrustedReconciliationContext:
        return False
    evidence = trusted_context.runtime_evidence
    if type(evidence) is not TrustedRuntimeEvidence:
        return False
    if type(evidence.observation) is not RuntimeObservation or evidence.observation != runtime:
        return False

    identity_values = (
        trusted_context.current_session_id,
        trusted_context.current_run_id,
        trusted_context.current_runtime_id,
        trusted_context.current_runtime_instance_id,
        evidence.session_id,
        evidence.run_id,
        evidence.runtime_id,
        evidence.runtime_instance_id,
        evidence.producer_id,
        evidence.producer_contract_id,
    )
    if any(_safe_ref(value) is None for value in identity_values):
        return False
    if (
        evidence.session_id != trusted_context.current_session_id
        or evidence.run_id != trusted_context.current_run_id
        or evidence.runtime_id != trusted_context.current_runtime_id
        or evidence.runtime_instance_id != trusted_context.current_runtime_instance_id
    ):
        return False

    producers = trusted_context.reviewed_producers
    if type(producers) is not tuple or not producers:
        return False
    reviewed_pairs: set[tuple[str, str]] = set()
    for producer in producers:
        if (
            type(producer) is not ReviewedRuntimeProducer
            or _safe_ref(producer.producer_id) is None
            or _safe_ref(producer.contract_id) is None
        ):
            return False
        reviewed_pairs.add((producer.producer_id, producer.contract_id))
    if (evidence.producer_id, evidence.producer_contract_id) not in reviewed_pairs:
        return False

    current_ns = trusted_context.current_monotonic_ns
    observed_ns = evidence.observed_monotonic_ns
    max_age_ns = trusted_context.max_age_ns
    if (
        type(current_ns) is not int
        or type(observed_ns) is not int
        or type(max_age_ns) is not int
        or current_ns < 0
        or observed_ns < 0
        or max_age_ns < 0
        or observed_ns > current_ns
        or current_ns - observed_ns > max_age_ns
    ):
        return False
    return True


def _result(
    state: ReconciledState,
    visual_refs: tuple[str, ...],
    runtime_refs: tuple[str, ...],
) -> ReconciliationResult:
    return ReconciliationResult(state, visual_refs, runtime_refs)


def reconcile_state(
    visual: VisionObservation,
    runtime: RuntimeObservation,
    *,
    trusted_context: TrustedReconciliationContext | None = None,
) -> ReconciliationResult:
    """Reconcile only validated current evidence, failing closed on ambiguity.

    ``WORLD_CONFIRMED`` is reachable only through the exact table row for an
    ``IN_GAME`` runtime state carrying ``REVIEWED_CAUSAL`` evidence, at least
    one retained runtime provenance reference, and a separately verified
    current trust context.  Visual evidence and opaque provenance references
    never establish an in-game semantic state by themselves.
    """
    visual_state, visual_refs = _visual_parts(visual)
    runtime_state, evidence_class, runtime_refs = _runtime_parts(runtime)
    if visual_state is None or runtime_state is None or evidence_class is None:
        return _result(ReconciledState.UNKNOWN, (), ())

    if evidence_class is RuntimeEvidenceClass.REVIEWED_CAUSAL:
        if not runtime_refs or not _trusted_reviewed_runtime(runtime, trusted_context):
            return _result(ReconciledState.UNKNOWN, visual_refs, runtime_refs)

    rule = _RULES.get((visual_state, runtime_state, evidence_class))
    if rule is not None:
        return _result(rule, visual_refs, runtime_refs)

    if runtime_state == "UNKNOWN" and evidence_class is RuntimeEvidenceClass.UNKNOWN:
        if visual_state == "LOGIN_SCREEN":
            return _result(ReconciledState.LOGIN_SCREEN, visual_refs, runtime_refs)
        if visual_state == "CHARACTER_SELECT":
            return _result(ReconciledState.CHARACTER_SELECT, visual_refs, runtime_refs)

    return _result(ReconciledState.UNKNOWN, visual_refs, runtime_refs)


__all__ = [
    "ReviewedRuntimeProducer",
    "ReconciledState",
    "ReconciliationResult",
    "RuntimeEvidenceClass",
    "RuntimeObservation",
    "TrustedReconciliationContext",
    "TrustedRuntimeEvidence",
    "reconcile_state",
]
