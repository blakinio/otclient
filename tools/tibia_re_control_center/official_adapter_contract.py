from __future__ import annotations

from dataclasses import dataclass

from .model import (
    ActionRequest,
    AdapterIdentity,
    AdapterKind,
    Authority,
    Capability,
    EffectBound,
    Freshness,
    RuntimeStatus,
    ValidationError,
)
from .scenario import ACTION_KINDS, default_effect_bound, validate_action_parameters

OFFICIAL_RUNTIME_NOT_ADMITTED = "OFFICIAL_RUNTIME_NOT_ADMITTED"
NO_ACTION_CANDIDATE_READY = "NO_ACTION_CANDIDATE_READY"
CURRENT_AUTHORITATIVE_RECONCILIATION_REQUIRED = "CURRENT_AUTHORITATIVE_RECONCILIATION_REQUIRED"
_UNMAPPED_TRACK_A_PATH = "UNMAPPED_REQUIRES_CURRENT_RUNTIME_EVIDENCE"


@dataclass(frozen=True)
class OfficialActionReadiness:
    action_kind: str
    required_capability: str
    current_read_gate: str
    current_action_gate: str
    evidence_refs: tuple[str, ...]
    reference_ui_path_known: str
    track_a_semantic_path: str
    raw_transport_hidden: bool
    finite_effect_bound_available: bool
    confirmation_source: str
    required_gui_input_lock: str
    runtime_preconditions: tuple[str, ...]
    open_gaps: tuple[str, ...]
    recommended_for_first_real_slice: bool


@dataclass(frozen=True)
class OfficialActionMapping:
    action_kind: str
    required_capability: str
    required_authority: Authority
    effect_bound: EffectBound
    raw_transport_hidden: bool
    confirmation_source: str


@dataclass(frozen=True)
class OfficialPreflight:
    admitted: bool
    reason_code: str
    mapping: OfficialActionMapping


def official_action_readiness() -> tuple[OfficialActionReadiness, ...]:
    """Return static preparation facts only; never promote live Track A evidence grades."""
    common_preconditions = (
        "FRESH_THEN_CURRENT_TRACK_A_RUNTIME_ADMISSION",
        "CURRENT_CANONICAL_IDENTITY_AND_AUTHORITY",
        "CURRENT_SEMANTIC_CAPABILITY_EVIDENCE",
        "CURRENT_REQUIRED_INPUT_LOCK",
        "CURRENT_AUTHORITATIVE_CONFIRMATION_PATH",
    )
    common_gaps = (
        "CURRENT_READ_GATE_NOT_REVALIDATED_IN_RUNTIME_ACCESS_NONE_TASK",
        "CURRENT_ACTION_GATE_NOT_REVALIDATED_IN_RUNTIME_ACCESS_NONE_TASK",
        "TRACK_A_SEMANTIC_ACTION_PATH_NOT_ADMITTED",
        "REFERENCE_UI_PARITY_NOT_REVALIDATED",
        "GUI_INPUT_LOCK_REQUIREMENT_NOT_REVALIDATED_PER_ACTION",
        "AUTHORITATIVE_POST_EFFECT_CONFIRMATION_NOT_REVALIDATED_PER_ACTION",
    )
    return tuple(
        OfficialActionReadiness(
            action_kind=kind,
            required_capability=kind,
            current_read_gate="UNKNOWN",
            current_action_gate="UNKNOWN",
            evidence_refs=(
                "tools/tibia_re_control_center/scenario.py:ACTION_KINDS",
                "tools/tibia_re_control_center/scenario.py:default_effect_bound",
                "docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md",
            ),
            reference_ui_path_known="unknown",
            track_a_semantic_path=_UNMAPPED_TRACK_A_PATH,
            raw_transport_hidden=True,
            finite_effect_bound_available=True,
            confirmation_source=CURRENT_AUTHORITATIVE_RECONCILIATION_REQUIRED,
            required_gui_input_lock="UNKNOWN",
            runtime_preconditions=common_preconditions,
            open_gaps=common_gaps,
            recommended_for_first_real_slice=False,
        )
        for kind in sorted(ACTION_KINDS)
    )


def first_slice_recommendation() -> str:
    """Static preparation cannot select an executable Official Tibia action slice."""
    return NO_ACTION_CANDIDATE_READY


class OfficialTibiaAdapterContract:
    """Hard-disabled static boundary for a future separately admitted Official Tibia adapter.

    The class intentionally does not implement the Package A physical-dispatch protocol. It has
    no external guard acquisition, input-lock acquisition, capture, bridge, process, GUI or
    irreversible-boundary method. A future runtime implementation must be a separate admitted
    producer that reuses then-current Track A authority and supplies fresh runtime evidence.
    """

    def __init__(self, identity: AdapterIdentity):
        if identity.adapter_kind is not AdapterKind.OFFICIAL_TIBIA:
            raise ValidationError(
                "OFFICIAL_ADAPTER_IDENTITY_REQUIRED",
                "Package D preparation requires AdapterKind.OFFICIAL_TIBIA",
            )
        self._identity = identity
        self._capabilities = tuple(
            Capability(
                capability_id=kind,
                read_supported=False,
                action_supported=False,
                source="official-package-d-prep-static",
                notes=OFFICIAL_RUNTIME_NOT_ADMITTED,
            )
            for kind in sorted(ACTION_KINDS)
        )

    def identity(self) -> AdapterIdentity:
        return self._identity

    def capabilities(self) -> tuple[Capability, ...]:
        return self._capabilities

    def capability(self, capability_id: str) -> Capability | None:
        return next(
            (capability for capability in self._capabilities if capability.capability_id == capability_id),
            None,
        )

    def runtime_status(self) -> RuntimeStatus:
        return RuntimeStatus(
            adapter_id=self._identity.adapter_id,
            adapter_generation=self._identity.adapter_generation,
            runtime_state="UNKNOWN",
            client_state="UNKNOWN",
            recorder_state="STOPPED",
            authority_state="NOT_ADMITTED",
            session_epoch=None,
            runtime_instance_id=None,
            observed_monotonic_ns=0,
            freshness=Freshness.UNKNOWN,
            reasons=(OFFICIAL_RUNTIME_NOT_ADMITTED,),
        )

    def action_readiness(self) -> tuple[OfficialActionReadiness, ...]:
        return official_action_readiness()

    def map_action(self, request: ActionRequest) -> OfficialActionMapping:
        normalized_parameters = validate_action_parameters(request.kind, request.parameters)
        expected_effect_bound = default_effect_bound(request.kind, normalized_parameters)
        if request.effect_bound != expected_effect_bound:
            raise ValidationError(
                "EFFECT_BOUND_MISMATCH",
                "Official adapter preparation requires the exact Scenario v1 finite EffectBound",
            )
        return OfficialActionMapping(
            action_kind=request.kind,
            required_capability=request.required_capability,
            required_authority=request.required_authority,
            effect_bound=expected_effect_bound,
            raw_transport_hidden=True,
            confirmation_source=CURRENT_AUTHORITATIVE_RECONCILIATION_REQUIRED,
        )

    def preflight(
        self,
        request: ActionRequest,
        *,
        observed_status: RuntimeStatus | None = None,
    ) -> OfficialPreflight:
        # A reported/cached status is diagnostic data only. This preparation task has no live
        # admission provider and therefore cannot convert it into capability or authority.
        del observed_status
        return OfficialPreflight(
            admitted=False,
            reason_code=OFFICIAL_RUNTIME_NOT_ADMITTED,
            mapping=self.map_action(request),
        )

    def execute(self, request: ActionRequest) -> None:
        self.map_action(request)
        raise ValidationError(
            OFFICIAL_RUNTIME_NOT_ADMITTED,
            "Official Tibia runtime execution is not admitted by Package D preparation",
        )
