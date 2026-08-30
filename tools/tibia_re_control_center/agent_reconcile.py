"""Deterministic, authority-neutral reconciliation of visual and runtime evidence.

This module deliberately has no runtime producer or action surface.  It only
combines a bounded visual observation with already-reviewed runtime evidence.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Any

from .agent_vision import VisionObservation


class RuntimeEvidenceClass(str, Enum):
    UNKNOWN = "UNKNOWN"
    STRUCTURAL_ONLY = "STRUCTURAL_ONLY"
    REVIEWED_CAUSAL = "REVIEWED_CAUSAL"


@dataclass(frozen=True)
class RuntimeObservation:
    state: str
    evidence_class: RuntimeEvidenceClass
    evidence_refs: tuple[str, ...]


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
    return value


def _visual_parts(visual: Any) -> tuple[str | None, tuple[str, ...]]:
    if type(visual) is not VisionObservation:
        return None, ()
    if (
        type(visual.screen_class) is not str
        or type(visual.capture_sha256) is not str
        or not _SHA256.fullmatch(visual.capture_sha256)
        or visual.visual_only is not True
        or visual.structural_authority is not False
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


def _result(
    state: ReconciledState,
    visual_refs: tuple[str, ...],
    runtime_refs: tuple[str, ...],
) -> ReconciliationResult:
    return ReconciliationResult(state, visual_refs, runtime_refs)


def reconcile_state(visual: VisionObservation, runtime: RuntimeObservation) -> ReconciliationResult:
    """Reconcile only validated current evidence, failing closed on ambiguity.

    ``WORLD_CONFIRMED`` is reachable only through the exact table row for an
    ``IN_GAME`` runtime state carrying ``REVIEWED_CAUSAL`` evidence and at
    least one retained runtime provenance reference.  Visual evidence never
    establishes an in-game semantic state by itself.
    """
    visual_state, visual_refs = _visual_parts(visual)
    runtime_state, evidence_class, runtime_refs = _runtime_parts(runtime)
    if visual_state is None or runtime_state is None or evidence_class is None:
        return _result(ReconciledState.UNKNOWN, visual_refs, runtime_refs)

    if evidence_class is RuntimeEvidenceClass.REVIEWED_CAUSAL and not runtime_refs:
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
    "ReconciledState",
    "ReconciliationResult",
    "RuntimeEvidenceClass",
    "RuntimeObservation",
    "reconcile_state",
]
