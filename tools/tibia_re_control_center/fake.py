from __future__ import annotations

import threading
from collections.abc import Callable, Mapping
from contextlib import contextmanager
from dataclasses import replace
from typing import Any

from .model import (
    ActionRequest,
    AdapterIdentity,
    AdapterKind,
    Authority,
    Capability,
    EffectBound,
    Freshness,
    GameSnapshot,
    RuntimeStatus,
    SimulatedCrash,
    ValidationError,
)
from .scenario import default_effect_bound


class ManualClock:
    def __init__(self, monotonic_ns: int = 0) -> None:
        if monotonic_ns < 0:
            raise ValueError("monotonic_ns must be non-negative")
        self._ns = monotonic_ns

    def now_ns(self) -> int:
        return self._ns

    def advance_ns(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("manual clock cannot move backwards")
        self._ns += amount
        return self._ns

    def advance_ms(self, amount: int) -> int:
        return self.advance_ns(amount * 1_000_000)

    def advance_seconds(self, amount: float) -> int:
        if amount < 0:
            raise ValueError("manual clock cannot move backwards")
        return self.advance_ns(int(amount * 1_000_000_000))


class FakeAdapter:
    """Deterministic Package A adapter. Its success is never official-client evidence."""

    def __init__(
        self,
        clock: ManualClock,
        *,
        adapter_id: str = "fake-adapter",
        adapter_generation: str = "fake-generation-1",
        runtime_instance_id: str | None = "fake-runtime-1",
        session_epoch: str | None = "fake-session-1",
        allow_mutation: bool = True,
        concurrency_safe_reads: bool = True,
    ) -> None:
        self.clock = clock
        self._dispatch_state_lock = threading.RLock()
        self._identity = AdapterIdentity(
            adapter_id=adapter_id,
            adapter_kind=AdapterKind.FAKE_TEST,
            adapter_version="1.0",
            adapter_generation=adapter_generation,
            runtime_instance_id=runtime_instance_id,
            session_epoch=session_epoch,
        )
        self.allow_mutation = allow_mutation
        self.concurrency_safe_reads = concurrency_safe_reads
        self.authority_available = allow_mutation
        self._capabilities: dict[str, Capability] = {}
        self._effect_bounds: dict[str, EffectBound | None] = {}
        self.physical_effects: list[dict[str, Any]] = []
        self.capture_sessions: dict[str, dict[str, Any]] = {}
        self.capture_requires_invasive: set[str] = set()
        self.emergency_stop_calls = 0
        self.authority_wait_hook: Callable[[], None] | None = None
        self.before_commit_hook: Callable[[], None] | None = None
        self.after_commit_hook: Callable[[], None] | None = None
        self.dispatch_guard_hook: Callable[[], None] | None = None
        self.execution_fault: str | None = None
        self.snapshot_values: dict[str, Any] = {
            "client_state": "IN_GAME",
            "player": {
                "hp": 100,
                "hp_max": 100,
                "mana": 100,
                "mana_max": 100,
                "position": {"x": 100, "y": 100, "z": 7},
            },
            "conditions": {},
            "action_state": {},
            "target": None,
            "inventory": {},
            "containers": {},
            "battle_list": {},
            "source_quality": {"field_sources": {}, "unknown_fields": [], "stale_fields": []},
        }
        self.selector_state: dict[str, str] = {}

    @property
    def allow_mutation(self) -> bool:
        with self._dispatch_state_lock:
            return self._allow_mutation

    @allow_mutation.setter
    def allow_mutation(self, value: bool) -> None:
        with self._dispatch_state_lock:
            self._allow_mutation = bool(value)

    @property
    def authority_available(self) -> bool:
        with self._dispatch_state_lock:
            return self._authority_available

    @authority_available.setter
    def authority_available(self, value: bool) -> None:
        with self._dispatch_state_lock:
            self._authority_available = bool(value)

    @contextmanager
    def dispatch_guard(self, request: ActionRequest):
        with self._dispatch_state_lock:
            callback_failed = False
            try:
                if self.dispatch_guard_hook is not None:
                    self.dispatch_guard_hook()
                # Preserve prior callback-driven revalidation semantics, then read
                # authoritative backing state after every callback has completed.
                self.current_authority(request.required_authority)
                self.capability(request.required_capability)
            except Exception:  # noqa: BLE001 -- fail closed on adapter guard callback failure
                callback_failed = True
            identity = self._identity
            capability = None if callback_failed else self._capabilities.get(request.required_capability)
            authority_current = (
                False
                if callback_failed
                else True
                if request.required_authority == Authority.READ_ONLY
                else bool(self._allow_mutation and self._authority_available)
            )
            yield identity, capability, authority_current

    def identity(self) -> AdapterIdentity:
        with self._dispatch_state_lock:
            return self._identity

    def set_identity(
        self,
        *,
        adapter_generation: str | None = None,
        runtime_instance_id: str | None | object = ...,
        session_epoch: str | None | object = ...,
    ) -> None:
        with self._dispatch_state_lock:
            self._identity = replace(
                self._identity,
                adapter_generation=self._identity.adapter_generation if adapter_generation is None else adapter_generation,
                runtime_instance_id=self._identity.runtime_instance_id if runtime_instance_id is ... else runtime_instance_id,
                session_epoch=self._identity.session_epoch if session_epoch is ... else session_epoch,
            )

    def add_capability(self, capability_id: str, *, read: bool = True, action: bool = True) -> None:
        with self._dispatch_state_lock:
            self._capabilities[capability_id] = Capability(
                capability_id,
                read_supported=read,
                action_supported=action,
                source="fake-fixture",
            )

    def capabilities(self) -> tuple[Capability, ...]:
        return tuple(self._capabilities.values())

    def capability(self, capability_id: str) -> Capability | None:
        with self._dispatch_state_lock:
            return self._capabilities.get(capability_id)

    def set_effect_bound(self, kind: str, bound: EffectBound | None) -> None:
        self._effect_bounds[kind] = bound

    def effect_bound(self, kind: str, parameters: Mapping[str, Any]) -> EffectBound:
        if kind in self._effect_bounds:
            bound = self._effect_bounds[kind]
            if bound is None:
                raise ValidationError("UNBOUNDED_EFFECT", "fake fixture declares the hard external effect unbounded")
            return bound
        return default_effect_bound(kind, parameters)

    def runtime_status(self) -> RuntimeStatus:
        authority = "MUTATION_ALLOWED" if self.allow_mutation and self.authority_available else "READ_ONLY"
        return RuntimeStatus(
            adapter_id=self._identity.adapter_id,
            adapter_generation=self._identity.adapter_generation,
            authority_state=authority,
            session_epoch=self._identity.session_epoch,
            runtime_instance_id=self._identity.runtime_instance_id,
            observed_monotonic_ns=self.clock.now_ns(),
            freshness=Freshness.FRESH,
        )

    def snapshot(self) -> GameSnapshot:
        return GameSnapshot(
            snapshot_id=f"fake-snapshot-{self.clock.now_ns()}",
            adapter_id=self._identity.adapter_id,
            adapter_generation=self._identity.adapter_generation,
            ingested_monotonic_ns=self.clock.now_ns(),
            client_state=str(self.snapshot_values.get("client_state", "UNKNOWN")),
            session_epoch=self._identity.session_epoch,
            runtime_instance_id=self._identity.runtime_instance_id,
            player=dict(self.snapshot_values.get("player") or {}),
            conditions=self.snapshot_values.get("conditions"),
            action_state=self.snapshot_values.get("action_state"),
            target=self.snapshot_values.get("target"),
            inventory=self.snapshot_values.get("inventory"),
            containers=self.snapshot_values.get("containers"),
            battle_list=self.snapshot_values.get("battle_list"),
            source_quality=dict(self.snapshot_values.get("source_quality") or {}),
        )

    def resolve_selector(self, semantic_identity: str) -> bool:
        state = self.selector_state.get(semantic_identity, "FRESH_UNIQUE")
        if state == "FRESH_UNIQUE":
            return True
        if state in {"STALE", "AMBIGUOUS", "MISSING", "UNKNOWN"}:
            raise ValidationError("SELECTOR_NOT_UNIQUE_FRESH", "semantic selector is stale, missing or ambiguous")
        raise ValidationError("SELECTOR_STATE_INVALID", "unknown fake selector fixture")

    def validate_semantic_selectors(self, parameters: Mapping[str, Any]) -> bool:
        def walk(value: Any) -> None:
            if isinstance(value, Mapping):
                kind = value.get("kind")
                key: str | None = None
                if kind == "SELF":
                    key = "self"
                elif kind == "SELECTED_TARGET":
                    key = "selected_target"
                elif kind == "CREATURE_ID":
                    key = f"creature:{value.get('creature_id')}"
                elif kind == "SNAPSHOT_PATH":
                    key = f"snapshot:{value.get('snapshot_path')}"
                elif kind == "INVENTORY_SLOT":
                    key = f"inventory:{value.get('inventory_slot')}"
                elif kind == "CONTAINER_SLOT":
                    key = f"container:{value.get('container_ref')}:{value.get('slot_index')}"
                elif kind == "EQUIPMENT_SLOT":
                    key = f"equipment:{value.get('equipment_slot')}"
                if key is not None:
                    self.resolve_selector(key)
                for child in value.values():
                    walk(child)
            elif isinstance(value, (list, tuple)):
                for child in value:
                    walk(child)

        walk(parameters)
        return True

    def await_authority(self, request: ActionRequest) -> bool:
        if self.authority_wait_hook is not None:
            self.authority_wait_hook()
        return self.current_authority(request.required_authority)

    def preflight(self, request: ActionRequest) -> bool:
        self.validate_semantic_selectors(request.parameters)
        capability = self.capability(request.required_capability)
        if capability is None:
            return False
        if request.required_authority == Authority.MUTATION:
            return bool(capability.action_supported and self.allow_mutation and self.authority_available)
        return bool(capability.read_supported)

    def current_authority(self, required: Authority) -> bool:
        with self._dispatch_state_lock:
            if required == Authority.READ_ONLY:
                return True
            return bool(self._allow_mutation and self._authority_available)

    def cross_irreversible_boundary(self, request: ActionRequest) -> dict[str, Any]:
        if not self.allow_mutation:
            raise ValidationError("READ_ONLY_MUTATION_REFUSED", "fake adapter is configured read-only")
        effect = {"action_id": request.action_id, "kind": request.kind, "parameters": dict(request.parameters)}
        self.physical_effects.append(effect)
        return effect

    def capture_start(self, policy: Mapping[str, Any]) -> str:
        requested = [name for name, enabled in policy.items() if enabled is True]
        if any(name in self.capture_requires_invasive for name in requested):
            raise ValidationError("INVASIVE_CAPTURE_REFUSED", "requested capture requires an invasive enablement transition")
        session = f"capture-{len(self.capture_sessions) + 1}"
        self.capture_sessions[session] = {"policy": dict(policy), "active": True}
        return session

    def capture_stop(self, session: str) -> None:
        if session in self.capture_sessions:
            self.capture_sessions[session]["active"] = False

    def emergency_stop(self, reason: str = "STOP") -> dict[str, Any]:
        self.emergency_stop_calls += 1
        for value in self.capture_sessions.values():
            value["active"] = False
        return {"status": "HARNESS_CLEANUP_ONLY", "reason": reason, "new_external_effects": 0}

    def execute_committed(self, request: ActionRequest, commit_dispatch: Callable[[], bool]) -> dict[str, Any]:
        if self.before_commit_hook:
            self.before_commit_hook()
        committed = commit_dispatch()
        if not committed:
            return {"committed": False, "effect": None}
        if self.after_commit_hook:
            self.after_commit_hook()
        if self.execution_fault == "crash_after_commit_before_effect":
            raise SimulatedCrash("simulated crash after durable commit before effect")
        effect = self.cross_irreversible_boundary(request)
        if self.execution_fault == "crash_after_effect_before_result":
            raise SimulatedCrash("simulated crash after effect before result")
        return {"committed": True, "effect": effect}
