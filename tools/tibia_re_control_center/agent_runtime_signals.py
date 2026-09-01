"""Trusted reviewed runtime-signal ingestion with no runtime side effects.

The resolver is a repository/control-plane adapter only.  It accepts samples
through resolver-owned reviewed-source handles, binds them to one immutable
session/run/runtime identity, applies a trusted monotonic freshness policy, and
issues content-addressed runtime evidence.  Sample data never chooses its own
semantic evidence class or authority.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from .agent_reconcile import RuntimeEvidenceClass, RuntimeObservation
from .canonical import sha256_jcs
from .model import PrivacyError
from .privacy import ensure_no_secret_material

_MAX_TOKEN_BYTES = 128
_MAX_SOURCE_EVIDENCE_REFS = 32
_RUNTIME_STATES = frozenset({"UNKNOWN", "IN_GAME", "WORLD_EXIT"})


@dataclass(frozen=True)
class RuntimeSignalBinding:
    session_id: str
    run_id: str
    runtime_id: str
    runtime_instance_id: str
    runtime_binding_sha256: str


@dataclass(frozen=True)
class ReviewedRuntimeSignalRule:
    source_state: str
    runtime_state: str
    evidence_class: RuntimeEvidenceClass


@dataclass(frozen=True)
class ReviewedRuntimeSignalContract:
    producer_id: str
    contract_id: str
    rules: tuple[ReviewedRuntimeSignalRule, ...]


@dataclass(frozen=True)
class RuntimeSignalSample:
    binding: RuntimeSignalBinding
    clock_domain_id: str
    observed_monotonic_ns: int
    source_state: str
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeSignalEvidence:
    signal_ref: str
    observation: RuntimeObservation
    binding: RuntimeSignalBinding
    clock_domain_id: str
    producer_id: str
    contract_id: str
    source_state: str
    observed_monotonic_ns: int
    source_evidence_refs: tuple[str, ...]


@dataclass(frozen=True)
class _ReviewedRuntimeSignalSource:
    producer_id: str
    contract_id: str
    resolver_token: object


@dataclass(frozen=True)
class _RuntimeSignalRecord:
    evidence: RuntimeSignalEvidence
    source: _ReviewedRuntimeSignalSource


def _safe_token(value: Any) -> str | None:
    if type(value) is not str or not value or value in {".", ".."}:
        return None
    try:
        encoded = value.encode("utf-8", "strict")
    except UnicodeEncodeError:
        return None
    if (
        len(encoded) > _MAX_TOKEN_BYTES
        or any(0xD800 <= ord(char) <= 0xDFFF for char in value)
        or any(ord(char) < 0x20 or ord(char) == 0x7F for char in value)
        or "/" in value
        or "\\" in value
    ):
        return None
    try:
        ensure_no_secret_material(value, key_path="runtime_signal.token")
    except PrivacyError:
        return None
    return value


def _binding_is_valid(binding: Any) -> bool:
    return (
        type(binding) is RuntimeSignalBinding
        and all(
            _safe_token(value) is not None
            for value in (
                binding.session_id,
                binding.run_id,
                binding.runtime_id,
                binding.runtime_instance_id,
            )
        )
        and type(binding.runtime_binding_sha256) is str
        and len(binding.runtime_binding_sha256) == 64
        and all(char in "0123456789abcdef" for char in binding.runtime_binding_sha256)
    )


def _validate_contract(contract: Any) -> None:
    if type(contract) is not ReviewedRuntimeSignalContract:
        raise ValueError("reviewed runtime-signal contract invalid")
    if (
        _safe_token(contract.producer_id) is None
        or _safe_token(contract.contract_id) is None
        or type(contract.rules) is not tuple
        or not contract.rules
    ):
        raise ValueError("reviewed runtime-signal contract invalid")

    source_states: set[str] = set()
    for rule in contract.rules:
        if (
            type(rule) is not ReviewedRuntimeSignalRule
            or _safe_token(rule.source_state) is None
            or type(rule.runtime_state) is not str
            or rule.runtime_state not in _RUNTIME_STATES
            or type(rule.evidence_class) is not RuntimeEvidenceClass
            or rule.source_state in source_states
        ):
            raise ValueError("reviewed runtime-signal rule invalid or ambiguous")
        if (
            rule.evidence_class is not RuntimeEvidenceClass.REVIEWED_CAUSAL
            and rule.runtime_state != "UNKNOWN"
        ):
            raise ValueError("non-causal runtime-signal evidence cannot assert semantic state")
        source_states.add(rule.source_state)


def _sample_evidence_refs_are_valid(
    refs: Any,
    *,
    require_provenance: bool,
) -> bool:
    if (
        type(refs) is not tuple
        or len(refs) > _MAX_SOURCE_EVIDENCE_REFS
        or (require_provenance and not refs)
    ):
        return False
    return all(_safe_token(ref) is not None for ref in refs)


class RuntimeSignalResolver:
    """Own reviewed producer contracts and current runtime-signal provenance."""

    def __init__(
        self,
        *,
        current_binding: RuntimeSignalBinding,
        reviewed_contracts: tuple[ReviewedRuntimeSignalContract, ...],
        monotonic_ns: Callable[[], int],
        max_age_ns: int,
        clock_domain_id: str,
    ) -> None:
        if not _binding_is_valid(current_binding):
            raise ValueError("current runtime-signal binding invalid")
        if type(reviewed_contracts) is not tuple:
            raise ValueError("reviewed runtime-signal contracts must be a tuple")
        if not callable(monotonic_ns):
            raise TypeError("runtime-signal monotonic clock invalid")
        if _safe_token(clock_domain_id) is None:
            raise ValueError("runtime-signal clock domain invalid")
        if type(max_age_ns) is not int or max_age_ns < 0:
            raise ValueError("runtime-signal freshness window invalid")

        contracts: dict[tuple[str, str], ReviewedRuntimeSignalContract] = {}
        for contract in reviewed_contracts:
            _validate_contract(contract)
            key = (contract.producer_id, contract.contract_id)
            if key in contracts:
                raise ValueError("duplicate reviewed runtime-signal contract")
            contracts[key] = contract

        self._current_binding = current_binding
        self._monotonic_ns = monotonic_ns
        self._max_age_ns = max_age_ns
        self._clock_domain_id = clock_domain_id
        self._resolver_token = object()
        self._contracts = contracts
        self._records: dict[str, _RuntimeSignalRecord] = {}
        self._latest_by_source: dict[tuple[str, str], str] = {}

    def bind_reviewed_source(
        self,
        *,
        producer_id: str,
        contract_id: str,
    ) -> _ReviewedRuntimeSignalSource:
        if _safe_token(producer_id) is None or _safe_token(contract_id) is None:
            raise ValueError("runtime-signal producer identity invalid")
        key = (producer_id, contract_id)
        if key not in self._contracts:
            raise ValueError("runtime-signal producer contract is not reviewed")
        return _ReviewedRuntimeSignalSource(
            producer_id=producer_id,
            contract_id=contract_id,
            resolver_token=self._resolver_token,
        )

    def _is_current_time(self, observed_monotonic_ns: Any) -> bool:
        try:
            current = self._monotonic_ns()
        except (OSError, ValueError):
            return False
        except RuntimeError as error:
            if type(error) is RuntimeError:
                return False
            raise
        return (
            type(observed_monotonic_ns) is int
            and type(current) is int
            and observed_monotonic_ns >= 0
            and current >= 0
            and observed_monotonic_ns <= current
            and current - observed_monotonic_ns <= self._max_age_ns
        )

    def ingest(
        self,
        source: _ReviewedRuntimeSignalSource,
        sample: RuntimeSignalSample,
    ) -> RuntimeSignalEvidence | None:
        if (
            type(source) is not _ReviewedRuntimeSignalSource
            or source.resolver_token is not self._resolver_token
            or type(sample) is not RuntimeSignalSample
            or not _binding_is_valid(sample.binding)
            or sample.binding != self._current_binding
            or _safe_token(sample.clock_domain_id) is None
            or sample.clock_domain_id != self._clock_domain_id
            or not self._is_current_time(sample.observed_monotonic_ns)
            or _safe_token(sample.source_state) is None
        ):
            return None

        contract = self._contracts.get((source.producer_id, source.contract_id))
        if contract is None:
            return None
        rules = tuple(
            rule for rule in contract.rules if rule.source_state == sample.source_state
        )
        if len(rules) != 1:
            return None
        rule = rules[0]
        source_key = (source.producer_id, source.contract_id)
        previous_ref = self._latest_by_source.get(source_key)
        previous = self._records.get(previous_ref) if previous_ref is not None else None
        if (
            previous is not None
            and sample.observed_monotonic_ns
            < previous.evidence.observed_monotonic_ns
        ):
            return None
        if not _sample_evidence_refs_are_valid(
            sample.evidence_refs,
            require_provenance=(rule.evidence_class is not RuntimeEvidenceClass.UNKNOWN),
        ):
            return None

        digest = sha256_jcs(
            {
                "schema": "otclient.local-agent.runtime-signal.v1",
                "session_id": sample.binding.session_id,
                "run_id": sample.binding.run_id,
                "clock_domain_id": sample.clock_domain_id,
                "runtime_id": sample.binding.runtime_id,
                "runtime_instance_id": sample.binding.runtime_instance_id,
                "runtime_binding_sha256": sample.binding.runtime_binding_sha256,
                "producer_id": source.producer_id,
                "contract_id": source.contract_id,
                "observed_monotonic_ns": sample.observed_monotonic_ns,
                "source_state": sample.source_state,
                "source_evidence_refs": list(sample.evidence_refs),
                "runtime_state": rule.runtime_state,
                "evidence_class": rule.evidence_class.value,
            }
        )
        signal_ref = f"runtime-signal:{digest}"
        observation = RuntimeObservation(
            state=rule.runtime_state,
            evidence_class=rule.evidence_class,
            evidence_refs=(signal_ref,),
        )
        if previous is not None:
            previous_time = previous.evidence.observed_monotonic_ns
            if sample.observed_monotonic_ns == previous_time:
                if signal_ref == previous.evidence.signal_ref:
                    return previous.evidence
                return None

        evidence = RuntimeSignalEvidence(
            signal_ref=signal_ref,
            observation=observation,
            binding=sample.binding,
            clock_domain_id=sample.clock_domain_id,
            producer_id=source.producer_id,
            contract_id=source.contract_id,
            source_state=sample.source_state,
            observed_monotonic_ns=sample.observed_monotonic_ns,
            source_evidence_refs=sample.evidence_refs,
        )
        if previous_ref is not None:
            self._records.pop(previous_ref, None)
        self._records[signal_ref] = _RuntimeSignalRecord(evidence=evidence, source=source)
        self._latest_by_source[source_key] = signal_ref
        return evidence

    def _has_current_causal_conflict(self) -> bool:
        states: set[str] = set()
        for signal_ref in self._latest_by_source.values():
            record = self._records.get(signal_ref)
            if record is None:
                continue
            observation = record.evidence.observation
            if (
                observation.evidence_class is RuntimeEvidenceClass.REVIEWED_CAUSAL
                and observation.state in {"IN_GAME", "WORLD_EXIT"}
                and self._is_current_time(record.evidence.observed_monotonic_ns)
            ):
                states.add(observation.state)
        return len(states) > 1

    def resolve_current_reviewed(
        self,
        runtime: RuntimeObservation,
    ) -> RuntimeObservation | None:
        if (
            type(runtime) is not RuntimeObservation
            or type(runtime.evidence_refs) is not tuple
            or len(runtime.evidence_refs) != 1
            or _safe_token(runtime.evidence_refs[0]) is None
        ):
            return None
        record = self._records.get(runtime.evidence_refs[0])
        if (
            record is None
            or record.source.resolver_token is not self._resolver_token
            or record.evidence.observation != runtime
            or record.evidence.binding != self._current_binding
            or not self._is_current_time(record.evidence.observed_monotonic_ns)
        ):
            return None
        key = (record.source.producer_id, record.source.contract_id)
        if (
            self._contracts.get(key) is None
            or self._latest_by_source.get(key) != record.evidence.signal_ref
        ):
            return None
        if (
            runtime.evidence_class is RuntimeEvidenceClass.REVIEWED_CAUSAL
            and self._has_current_causal_conflict()
        ):
            return None
        return record.evidence.observation


__all__ = [
    "ReviewedRuntimeSignalContract",
    "ReviewedRuntimeSignalRule",
    "RuntimeSignalBinding",
    "RuntimeSignalEvidence",
    "RuntimeSignalResolver",
    "RuntimeSignalSample",
]
