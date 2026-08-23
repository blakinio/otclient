from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .model import AdapterIdentity, Capability
from .official_adapter_contract import OfficialTibiaAdapterContract
from .scenario import ACTION_KINDS


CURRENT_CLIENT_SHA256 = "ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8"


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


class OfficialTibiaAdapter:
    """Fail-closed production shell for a separately admitted Track A adapter."""

    concurrency_safe_reads = False

    def __init__(
        self,
        identity: AdapterIdentity,
        authority_bridge: Any,
        *,
        promotions: tuple[Any, ...] = (),
    ) -> None:
        self._prep = OfficialTibiaAdapterContract(identity)
        self._identity = identity
        self._authority_bridge = authority_bridge
        self._promotions = {
            promotion.action_kind: promotion
            for promotion in promotions
            if promotion.action_kind in ACTION_KINDS
            and promotion.client_sha256 == CURRENT_CLIENT_SHA256
            and promotion.adapter_generation == identity.adapter_generation
            and promotion.read_gate in {"R1", "R2", "R3", "R4"}
            and promotion.action_gate in {"A3", "A4"}
            and bool(promotion.semantic_path_id)
            and bool(promotion.confirmation_id)
            and promotion.requires_input_lock is True
            and bool(promotion.evidence_refs)
        }

    @property
    def allow_mutation(self) -> bool:
        return bool(self._promotions)

    def identity(self) -> AdapterIdentity:
        return self._identity

    def capabilities(self) -> tuple[Capability, ...]:
        return self._prep.capabilities()

    def capability(self, capability_id: str) -> Capability | None:
        base = self._prep.capability(capability_id)
        if base is None:
            return None
        if capability_id in self._promotions:
            return Capability(
                capability_id=capability_id,
                read_supported=base.read_supported,
                action_supported=True,
                source="official-package-d-evidence-promotion",
            )
        return base
