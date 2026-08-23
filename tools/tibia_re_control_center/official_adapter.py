from __future__ import annotations

from typing import Any

from .model import AdapterIdentity, Capability
from .official_adapter_contract import OfficialTibiaAdapterContract


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
        self._promotions = tuple(promotions)

    @property
    def allow_mutation(self) -> bool:
        return False

    def identity(self) -> AdapterIdentity:
        return self._identity

    def capabilities(self) -> tuple[Capability, ...]:
        return self._prep.capabilities()

    def capability(self, capability_id: str) -> Capability | None:
        return self._prep.capability(capability_id)
