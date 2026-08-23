from __future__ import annotations

import threading
from collections.abc import Iterator
from contextlib import AbstractContextManager, contextmanager
from dataclasses import dataclass
from typing import Any, Protocol

from .model import (
    ActionRequest,
    AdapterIdentity,
    Authority,
    Capability,
    EffectBound,
)
from .official_adapter_contract import OfficialTibiaAdapterContract
from .scenario import ACTION_KINDS, default_effect_bound, validate_action_parameters

CURRENT_CLIENT_SHA256 = "ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8"
_ACTIONABLE_READ_GATES = frozenset({"R1", "R2", "R3", "R4"})
_ACTIONABLE_ACTION_GATES = frozenset({"A3", "A4"})
_ALLOWED_EXECUTION_OUTCOMES = frozenset({"confirmed", "ambiguous"})


@dataclass(frozen=True)
class OfficialCapabilityPromotion:
    action_kind: str
    client_sha256: str
    read_gate: str
    action_gate: str
    semantic_path_id: str
    confirmation_id: str
    requires_input_lock: bool
    evidence_refs: tuple[str, ...]
    adapter_generation: str


@dataclass(frozen=True)
class GuardedRuntimeView:
    adapter_generation: str
    runtime_instance_id: str | None
    session_epoch: str | None
    client_state: str
    authority_current: bool
    target_unique: bool
    input_lock_held: bool
    fence_digest: str


@dataclass(frozen=True)
class GuardedExecutionOutcome:
    outcome: str
    reason_code: str | None
    evidence_refs: tuple[str, ...] = ()


class GuardedDispatchSession(Protocol):
    def current_view(self) -> GuardedRuntimeView:
        ...

    def cross_once_and_reconcile(self, request: ActionRequest) -> GuardedExecutionOutcome:
        ...


class TrackAAuthorityBridge(Protocol):
    def advisory_available(self, request: ActionRequest) -> bool:
        ...

    def guarded_dispatch(self, request: ActionRequest) -> AbstractContextManager[GuardedDispatchSession]:
        ...

    def emergency_stop(self, reason: str) -> None:
        ...


def _promotion_is_actionable(
    promotion: OfficialCapabilityPromotion,
    identity: AdapterIdentity,
) -> bool:
    return bool(
        promotion.action_kind in ACTION_KINDS
        and promotion.client_sha256 == CURRENT_CLIENT_SHA256
        and promotion.adapter_generation == identity.adapter_generation
        and promotion.read_gate in _ACTIONABLE_READ_GATES
        and promotion.action_gate in _ACTIONABLE_ACTION_GATES
        and promotion.semantic_path_id
        and promotion.confirmation_id
        and promotion.requires_input_lock is True
        and promotion.evidence_refs
        and all(isinstance(ref, str) and bool(ref) for ref in promotion.evidence_refs)
    )


def _valid_fence_digest(value: str) -> bool:
    return bool(
        len(value) == 64
        and all(character in "0123456789abcdef" for character in value.lower())
    )


class OfficialTibiaAdapter:
    """Fail-closed Official Tibia adapter over a separately admitted Track A session."""

    concurrency_safe_reads = False

    def __init__(
        self,
        identity: AdapterIdentity,
        authority_bridge: TrackAAuthorityBridge,
        *,
        promotions: tuple[OfficialCapabilityPromotion, ...] = (),
    ) -> None:
        self._prep = OfficialTibiaAdapterContract(identity)
        self._identity = identity
        self._authority_bridge = authority_bridge
        self._active_session = threading.local()
        candidates: dict[str, OfficialCapabilityPromotion] = {}
        duplicate_kinds: set[str] = set()
        for promotion in promotions:
            if not _promotion_is_actionable(promotion, identity):
                continue
            if promotion.action_kind in candidates:
                duplicate_kinds.add(promotion.action_kind)
                candidates.pop(promotion.action_kind, None)
                continue
            if promotion.action_kind not in duplicate_kinds:
                candidates[promotion.action_kind] = promotion
        self._promotions = candidates

    @property
    def allow_mutation(self) -> bool:
        """Local capability enablement only; never external Track A authority."""
        return bool(self._promotions)

    def identity(self) -> AdapterIdentity:
        return self._identity

    def capabilities(self) -> tuple[Capability, ...]:
        return tuple(
            capability
            for kind in sorted(ACTION_KINDS)
            if (capability := self.capability(kind)) is not None
        )

    def capability(self, capability_id: str) -> Capability | None:
        base = self._prep.capability(capability_id)
        if base is None:
            return None
        promotion = self._promotions.get(capability_id)
        if promotion is None:
            return base
        return Capability(
            capability_id=capability_id,
            read_supported=False,
            action_supported=True,
            source="official-package-d-evidence-promotion",
            notes=f"{promotion.read_gate}/{promotion.action_gate}",
        )

    def effect_bound(self, kind: str, parameters: Any) -> EffectBound:
        normalized = validate_action_parameters(kind, parameters)
        return default_effect_bound(kind, normalized)

    def runtime_status(self):
        return self._prep.runtime_status()

    def _promotion_for(self, request: ActionRequest) -> OfficialCapabilityPromotion | None:
        promotion = self._promotions.get(request.required_capability)
        if promotion is None or promotion.action_kind != request.kind:
            return None
        return promotion

    def await_authority(self, request: ActionRequest) -> bool:
        if request.required_authority is not Authority.MUTATION:
            return False
        if self._promotion_for(request) is None:
            return False
        try:
            return bool(self._authority_bridge.advisory_available(request))
        except Exception:  # noqa: BLE001 -- advisory failure must fail closed
            return False

    def preflight(self, request: ActionRequest) -> bool:
        self._prep.map_action(request)
        return bool(
            request.required_authority is Authority.MUTATION
            and self._promotion_for(request) is not None
            and self.await_authority(request)
        )

    def _active_guarded_session(self) -> GuardedDispatchSession | None:
        return getattr(self._active_session, "value", None)

    def _view_allows(self, request: ActionRequest, view: GuardedRuntimeView) -> bool:
        return bool(
            self._promotion_for(request) is not None
            and view.adapter_generation == self._identity.adapter_generation
            and view.runtime_instance_id == self._identity.runtime_instance_id
            and view.session_epoch == self._identity.session_epoch
            and view.client_state == "IN_GAME"
            and view.authority_current
            and view.target_unique
            and view.input_lock_held
            and _valid_fence_digest(view.fence_digest)
        )

    def current_authority(self, required: Authority) -> bool:
        if required is not Authority.MUTATION:
            return False
        session = self._active_guarded_session()
        if session is None:
            return False
        try:
            view = session.current_view()
        except Exception:  # noqa: BLE001 -- guard view failure must fail closed
            return False
        return bool(
            view.adapter_generation == self._identity.adapter_generation
            and view.runtime_instance_id == self._identity.runtime_instance_id
            and view.session_epoch == self._identity.session_epoch
            and view.client_state == "IN_GAME"
            and view.authority_current
            and view.target_unique
            and view.input_lock_held
            and _valid_fence_digest(view.fence_digest)
        )

    @contextmanager
    def dispatch_guard(
        self,
        request: ActionRequest,
    ) -> Iterator[tuple[AdapterIdentity, Capability | None, bool]]:
        session = self._active_guarded_session()
        capability = self.capability(request.required_capability)
        authority_current = False
        if session is not None:
            try:
                authority_current = self._view_allows(request, session.current_view())
            except Exception:  # noqa: BLE001 -- fail closed on any revalidation failure
                authority_current = False
        yield self._identity, capability, authority_current

    def execute_committed(self, request: ActionRequest, commit_dispatch) -> dict[str, Any]:
        self._prep.map_action(request)
        if self._promotion_for(request) is None:
            return {"committed": False, "effect": None}

        committed = False
        self._active_session.value = None
        try:
            with self._authority_bridge.guarded_dispatch(request) as session:
                self._active_session.value = session
                if not self._view_allows(request, session.current_view()):
                    return {"committed": False, "effect": None}
                committed = bool(commit_dispatch())
                if not committed:
                    return {"committed": False, "effect": None}
                try:
                    outcome = session.cross_once_and_reconcile(request)
                except Exception:  # noqa: BLE001 -- uncertainty after commit is always ambiguous
                    return {
                        "committed": True,
                        "effect": None,
                        "outcome": "ambiguous",
                        "reason_code": "TRACK_A_RECONCILIATION_FAILED",
                    }
                normalized = (
                    outcome.outcome
                    if outcome.outcome in _ALLOWED_EXECUTION_OUTCOMES
                    else "ambiguous"
                )
                reason_code = outcome.reason_code
                if normalized == "ambiguous" and not reason_code:
                    reason_code = (
                        "TRACK_A_OUTCOME_INVALID"
                        if outcome.outcome not in _ALLOWED_EXECUTION_OUTCOMES
                        else "TRACK_A_RECONCILIATION_AMBIGUOUS"
                    )
                return {
                    "committed": True,
                    "effect": None,
                    "outcome": normalized,
                    "reason_code": reason_code,
                }
        except Exception:  # noqa: BLE001 -- external guard failure is fail-closed
            if committed:
                return {
                    "committed": True,
                    "effect": None,
                    "outcome": "ambiguous",
                    "reason_code": "TRACK_A_GUARDED_DISPATCH_FAILED",
                }
            return {"committed": False, "effect": None}
        finally:
            self._active_session.value = None

    def emergency_stop(self, reason: str = "STOP") -> dict[str, Any]:
        cleanup_failed = False
        try:
            self._authority_bridge.emergency_stop(reason)
        except Exception:  # noqa: BLE001 -- STOP cleanup failure grants no authority
            cleanup_failed = True
        return {
            "status": "HARNESS_CLEANUP_DEGRADED" if cleanup_failed else "HARNESS_CLEANUP_ONLY",
            "reason": reason,
            "new_external_effects": 0,
        }
