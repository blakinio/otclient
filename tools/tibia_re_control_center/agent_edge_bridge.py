"""Fail-closed, authority-neutral Control Center view of a read-only runtime edge."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from typing import Any

from .agent_reconcile import RuntimeEvidenceClass, RuntimeObservation
from .agent_runtime_admission import (
    OBSERVATION_SCHEMA,
    ReadOnlyRuntimeAdmission,
    admit_read_only_runtime,
)
from .agent_runtime_signals import (
    ReviewedRuntimeSignalContract,
    ReviewedRuntimeSignalRule,
    RuntimeSignalBinding,
    RuntimeSignalEvidence,
    RuntimeSignalResolver,
)
from .canonical import sha256_jcs
from .model import (
    MAX_SAFE_INTEGER,
    PrivacyError,
    ValidationError,
    checked_non_negative,
    require_exact_keys,
    validate_opaque_id,
)
from .recorder import ensure_no_secret_material

_EDGE_SCHEMA = "otclient.local-agent.edge-observation.v1"
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_RUNTIME_SIGNAL_REF = re.compile(r"^runtime-signal:[0-9a-f]{64}$")
_CAPTURE_STATUSES = frozenset({"AVAILABLE", "UNAVAILABLE", "STALE", "REJECTED_UNSAFE_CAPTURE"})
_RUNTIME_STATES = frozenset({"UNKNOWN", "IN_GAME", "WORLD_EXIT"})
_MAX_SIGNAL_TOKEN_BYTES = 128
_MAX_SOURCE_EVIDENCE_REFS = 32


def _epoch(value: Any, field: str) -> int:
    return checked_non_negative(value, maximum=MAX_SAFE_INTEGER, field_name=field)


def _optional_ref(value: Any, field: str) -> str | None:
    if value is None:
        return None
    return validate_opaque_id(value, field_name=field, max_bytes=384)


def _signal_token(value: Any, field: str) -> str:
    if type(value) is not str or not value or value in {".", ".."}:
        raise ValidationError("EDGE_RUNTIME_SIGNAL_INVALID", f"{field} is invalid")
    try:
        encoded = value.encode("utf-8", "strict")
    except UnicodeEncodeError as exc:
        raise ValidationError("EDGE_RUNTIME_SIGNAL_INVALID", f"{field} is invalid") from exc
    if (
        len(encoded) > _MAX_SIGNAL_TOKEN_BYTES
        or any(0xD800 <= ord(char) <= 0xDFFF for char in value)
        or any(ord(char) < 0x20 or ord(char) == 0x7F for char in value)
        or "/" in value
        or "\\" in value
    ):
        raise ValidationError("EDGE_RUNTIME_SIGNAL_INVALID", f"{field} is invalid")
    try:
        ensure_no_secret_material(value, key_path=f"runtime_signal.{field}")
    except (PrivacyError, ValidationError) as exc:
        raise ValidationError("EDGE_RUNTIME_SIGNAL_INVALID", f"{field} is invalid") from exc
    return value


@dataclass(frozen=True)
class EdgeCaptureObservation:
    status: str
    artifact_ref: str | None
    sha256: str | None
    observed_epoch_ms: int
    secret_safe: bool

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> EdgeCaptureObservation:
        if not isinstance(value, Mapping):
            raise ValidationError("EDGE_CAPTURE_INVALID", "edge capture must be a mapping")
        require_exact_keys(value, ("status", "artifact_ref", "sha256", "observed_epoch_ms", "secret_safe"))
        status = value["status"]
        if status not in _CAPTURE_STATUSES:
            raise ValidationError("EDGE_CAPTURE_INVALID", "edge capture status is not admitted")
        secret_safe = value["secret_safe"]
        if type(secret_safe) is not bool:
            raise ValidationError("EDGE_CAPTURE_INVALID", "edge capture secret_safe must be boolean")
        artifact_ref = _optional_ref(value["artifact_ref"], "artifact_ref")
        sha256 = value["sha256"]
        if sha256 is not None and (not isinstance(sha256, str) or not _SHA256.fullmatch(sha256)):
            raise ValidationError("EDGE_CAPTURE_INVALID", "edge capture SHA-256 is invalid")
        if status == "AVAILABLE":
            if artifact_ref is None or sha256 is None or not secret_safe:
                raise ValidationError("EDGE_CAPTURE_INVALID", "available edge capture must be secret-safe and content addressed")
        elif artifact_ref is not None or sha256 is not None:
            raise ValidationError("EDGE_CAPTURE_INVALID", "non-available edge capture cannot expose artifact material")
        if not secret_safe and status != "REJECTED_UNSAFE_CAPTURE":
            raise ValidationError("EDGE_CAPTURE_INVALID", "unsafe edge capture must be explicitly rejected")
        return cls(status, artifact_ref, sha256, _epoch(value["observed_epoch_ms"], "capture.observed_epoch_ms"), secret_safe)


@dataclass(frozen=True)
class EdgeObservation:
    schema: str
    session_id: str
    run_id: str
    edge_instance_id: str
    observed_epoch_ms: int
    heartbeat_epoch_ms: int
    capture: EdgeCaptureObservation | None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> EdgeObservation:
        if not isinstance(value, Mapping):
            raise ValidationError("EDGE_OBSERVATION_INVALID", "edge observation must be a mapping")
        require_exact_keys(
            value,
            ("schema", "session_id", "run_id", "edge_instance_id", "observed_epoch_ms", "heartbeat_epoch_ms", "capture", "runtime"),
        )
        if value["schema"] != _EDGE_SCHEMA:
            raise ValidationError("EDGE_OBSERVATION_INVALID", "edge observation schema is not admitted")
        if value["runtime"] is not None:
            raise ValidationError(
                "EDGE_RUNTIME_SIGNAL_REQUIRED",
                "runtime semantics must come from the trusted reviewed runtime-signal resolver",
            )
        parsed = cls(
            schema=_EDGE_SCHEMA,
            session_id=validate_opaque_id(value["session_id"], field_name="session_id"),
            run_id=validate_opaque_id(value["run_id"], field_name="run_id"),
            edge_instance_id=validate_opaque_id(value["edge_instance_id"], field_name="edge_instance_id", max_bytes=192),
            observed_epoch_ms=_epoch(value["observed_epoch_ms"], "observed_epoch_ms"),
            heartbeat_epoch_ms=_epoch(value["heartbeat_epoch_ms"], "heartbeat_epoch_ms"),
            capture=None if value["capture"] is None else EdgeCaptureObservation.from_mapping(value["capture"]),
        )
        if parsed.heartbeat_epoch_ms > parsed.observed_epoch_ms:
            raise ValidationError("EDGE_OBSERVATION_INVALID", "edge heartbeat cannot postdate its observation")
        if parsed.capture is not None and parsed.capture.observed_epoch_ms > parsed.observed_epoch_ms:
            raise ValidationError("EDGE_OBSERVATION_INVALID", "edge capture cannot postdate its observation")
        ensure_no_secret_material(asdict(parsed), key_path="edge_observation")
        return parsed


@dataclass(frozen=True)
class _RuntimeAuthority:
    admission: ReadOnlyRuntimeAdmission
    signal_binding: RuntimeSignalBinding
    resolver: RuntimeSignalResolver


@dataclass(frozen=True)
class ReviewedRuntimeAuthorityConfiguration:
    """Composition-root allowlist for one reviewed runtime-signal configuration.

    This is deliberately supplied when the coordinator is composed, rather than
    by a task or edge request.  A task may request read-only access, but it may
    not nominate the causal rules that make runtime evidence authoritative.
    """

    reviewed_contracts: tuple[ReviewedRuntimeSignalContract, ...]
    clock_domain_id: str
    max_age_ns: int


@dataclass(frozen=True)
class _IssuedRuntimeAuthority:
    """Registry-owned opaque receipt for one authority bind."""

    admission: ReadOnlyRuntimeAdmission
    resolver: RuntimeSignalResolver
    signal_binding: RuntimeSignalBinding
    session_id: str
    run_id: str
    task_id: str
    expected_client_version: str
    expected_client_size: int | str
    expected_client_sha256: str


def _contract_signature(
    contracts: tuple[ReviewedRuntimeSignalContract, ...],
) -> tuple[tuple[str, str, tuple[tuple[str, str, str], ...]], ...] | None:
    if type(contracts) is not tuple or not contracts:
        return None
    signature: list[tuple[str, str, tuple[tuple[str, str, str], ...]]] = []
    for contract in contracts:
        if type(contract) is not ReviewedRuntimeSignalContract or type(contract.rules) is not tuple:
            return None
        rules: list[tuple[str, str, str]] = []
        for rule in contract.rules:
            if type(rule) is not ReviewedRuntimeSignalRule:
                return None
            rules.append((rule.source_state, rule.runtime_state, rule.evidence_class.value))
        signature.append((contract.producer_id, contract.contract_id, tuple(rules)))
    return tuple(sorted(signature))


class _RuntimeAuthorityRegistry:
    """Issue one-shot authority receipts from the trusted composition root."""

    def __init__(self, configuration: ReviewedRuntimeAuthorityConfiguration | None) -> None:
        self._configuration = configuration
        self._issued: dict[int, _IssuedRuntimeAuthority] = {}
        self._configuration_signature = (
            None
            if configuration is None
            else _contract_signature(configuration.reviewed_contracts)
        )

    def issue(
        self,
        *,
        admission: ReadOnlyRuntimeAdmission,
        resolver: RuntimeSignalResolver,
        binding: RuntimeSignalBinding,
        session_id: str,
        run_id: str,
        task_id: str,
        expected_client_version: str,
        expected_client_size: int | str,
        expected_client_sha256: str,
        now_epoch_ms: int,
        max_age_ms: int,
    ) -> _IssuedRuntimeAuthority:
        configuration = self._configuration
        if (
            configuration is None
            or self._configuration_signature is None
            or type(resolver) is not RuntimeSignalResolver
            or resolver._clock_domain_id != configuration.clock_domain_id
            or resolver._max_age_ns != configuration.max_age_ns
            or _contract_signature(tuple(resolver._contracts.values()))
            != self._configuration_signature
            or resolver._current_binding != binding
        ):
            raise ValidationError(
                "EDGE_RUNTIME_COMPOSITION_MISMATCH",
                "runtime authority does not use the composition-owned reviewed resolver configuration",
            )
        canonical = _validated_admission(
            admission,
            now_epoch_ms=_epoch(now_epoch_ms, "now_epoch_ms"),
            max_age_ms=_epoch(max_age_ms, "max_age_ms"),
        )
        if (
            binding.session_id != session_id
            or binding.run_id != run_id
            or canonical.task_id != task_id
            or canonical.runtime_owner_task != task_id
            or binding.runtime_id != canonical.runtime_namespace
            or binding.runtime_binding_sha256 != canonical.runtime_binding_sha256
            or canonical.process.get("client_version") != expected_client_version
            or canonical.process.get("client_size") != expected_client_size
            or canonical.process.get("client_sha256") != expected_client_sha256
        ):
            raise ValidationError(
                "EDGE_RUNTIME_COMPOSITION_MISMATCH",
                "runtime authority receipt does not bind the trusted task/run/runtime/client identity",
            )
        receipt = _IssuedRuntimeAuthority(
            canonical,
            resolver,
            binding,
            session_id,
            run_id,
            task_id,
            expected_client_version,
            expected_client_size,
            expected_client_sha256,
        )
        self._issued[id(receipt)] = receipt
        return receipt

    def consume(self, receipt: Any) -> _IssuedRuntimeAuthority:
        issued = self._issued.pop(id(receipt), None)
        if type(receipt) is not _IssuedRuntimeAuthority or issued is not receipt:
            raise ValidationError(
                "EDGE_RUNTIME_AUTHORITY_REQUIRED",
                "only a one-shot authority receipt issued by the trusted composition is accepted",
            )
        return issued


def _require_signal_binding(value: Any) -> RuntimeSignalBinding:
    if type(value) is not RuntimeSignalBinding:
        raise ValidationError(
            "EDGE_RUNTIME_SIGNAL_BINDING_INVALID",
            "typed runtime-signal binding is required",
        )
    session_id = _signal_token(value.session_id, "session_id")
    run_id = _signal_token(value.run_id, "run_id")
    runtime_id = _signal_token(value.runtime_id, "runtime_id")
    runtime_instance_id = _signal_token(value.runtime_instance_id, "runtime_instance_id")
    digest = value.runtime_binding_sha256
    if type(digest) is not str or _SHA256.fullmatch(digest) is None:
        raise ValidationError("EDGE_RUNTIME_SIGNAL_BINDING_INVALID", "runtime admission hash is invalid")
    return RuntimeSignalBinding(
        session_id=session_id,
        run_id=run_id,
        runtime_id=runtime_id,
        runtime_instance_id=runtime_instance_id,
        runtime_binding_sha256=digest,
    )


def _persisted_signal_binding(value: Any) -> RuntimeSignalBinding:
    keys = ("session_id", "run_id", "runtime_id", "runtime_instance_id", "runtime_binding_sha256")
    if not isinstance(value, Mapping):
        raise ValidationError("EDGE_RUNTIME_SIGNAL_BINDING_INVALID", "persisted runtime-signal binding is invalid")
    require_exact_keys(value, keys)
    return _require_signal_binding(RuntimeSignalBinding(**{key: value[key] for key in keys}))

def _admission_observation(admission: ReadOnlyRuntimeAdmission) -> dict[str, Any]:
    return {
        "schema": OBSERVATION_SCHEMA,
        "track_id": admission.track_id,
        "task_id": admission.task_id,
        "runtime_owner_task": admission.runtime_owner_task,
        "runtime_namespace": admission.runtime_namespace,
        "observed_at_epoch_ms": admission.observed_at_epoch_ms,
        "locator": dict(admission.locator),
        "process": dict(admission.process),
        "window": dict(admission.window),
        "inventory": dict(admission.inventory),
        "safety": dict(admission.safety),
    }


def _validated_admission(
    admission: Any,
    *,
    now_epoch_ms: int,
    max_age_ms: int,
) -> ReadOnlyRuntimeAdmission:
    if type(admission) is not ReadOnlyRuntimeAdmission:
        raise ValidationError("EDGE_RUNTIME_ADMISSION_INVALID", "typed read-only runtime admission is required")
    try:
        canonical = admit_read_only_runtime(
            _admission_observation(admission),
            now_epoch_ms=now_epoch_ms,
            max_age_ms=max_age_ms,
        )
    except ValidationError as exc:
        code = (
            "EDGE_RUNTIME_ADMISSION_STALE"
            if exc.code == "RUNTIME_OBSERVATION_STALE"
            else "EDGE_RUNTIME_ADMISSION_INVALID"
        )
        raise ValidationError(code, "read-only runtime admission is not current and valid") from exc
    if canonical != admission:
        raise ValidationError("EDGE_RUNTIME_ADMISSION_INVALID", "read-only runtime admission is not canonical")
    return canonical


class AgentEdgeBridge:
    """Track live edge identity and trusted read-only runtime authority."""

    def __init__(
        self,
        *,
        heartbeat_timeout_ms: int = 15_000,
        runtime_authority_configuration: ReviewedRuntimeAuthorityConfiguration | None = None,
    ) -> None:
        if type(heartbeat_timeout_ms) is not int or heartbeat_timeout_ms < 1 or heartbeat_timeout_ms > 300_000:
            raise ValueError("heartbeat_timeout_ms must be between 1 and 300000")
        self.heartbeat_timeout_ms = heartbeat_timeout_ms
        self._live_instances: dict[str, str] = {}
        self._runtime_authorities: dict[str, _RuntimeAuthority] = {}
        self._authority_registry = _RuntimeAuthorityRegistry(runtime_authority_configuration)

    def _issue_trusted_runtime_authority(
        self,
        *,
        admission: ReadOnlyRuntimeAdmission,
        runtime_signal_resolver: RuntimeSignalResolver,
        runtime_signal_binding: RuntimeSignalBinding,
        session_id: str,
        run_id: str,
        task_id: str,
        expected_client_version: str,
        expected_client_size: int | str,
        expected_client_sha256: str,
        now_epoch_ms: int,
    ) -> _IssuedRuntimeAuthority:
        """Private composition-root capability; never an edge/task request API."""
        return self._authority_registry.issue(
            admission=admission,
            resolver=runtime_signal_resolver,
            binding=_require_signal_binding(runtime_signal_binding),
            session_id=session_id,
            run_id=run_id,
            task_id=task_id,
            expected_client_version=expected_client_version,
            expected_client_size=expected_client_size,
            expected_client_sha256=expected_client_sha256,
            now_epoch_ms=now_epoch_ms,
            max_age_ms=self.heartbeat_timeout_ms,
        )

    def bind_runtime_authority(
        self,
        *,
        session_id: str,
        run_id: str,
        task_id: str,
        expected_client_version: str,
        expected_client_size: int | str,
        expected_client_sha256: str,
        authority: Any,
        now_epoch_ms: int,
    ) -> tuple[ReadOnlyRuntimeAdmission, RuntimeSignalBinding]:
        issued = self._authority_registry.consume(authority)
        admission = issued.admission
        runtime_signal_resolver = issued.resolver
        runtime_signal_binding = issued.signal_binding
        if (
            issued.session_id != session_id
            or issued.run_id != run_id
            or issued.task_id != task_id
            or issued.expected_client_version != expected_client_version
            or issued.expected_client_size != expected_client_size
            or issued.expected_client_sha256 != expected_client_sha256
        ):
            raise ValidationError(
                "EDGE_RUNTIME_ADMISSION_BINDING_MISMATCH",
                "runtime authority receipt cannot be substituted for another task/run/runtime/client identity",
            )
        canonical = _validated_admission(
            admission,
            now_epoch_ms=_epoch(now_epoch_ms, "now_epoch_ms"),
            max_age_ms=self.heartbeat_timeout_ms,
        )
        if canonical.task_id != task_id or canonical.runtime_owner_task != task_id:
            raise ValidationError("EDGE_RUNTIME_ADMISSION_BINDING_MISMATCH", "runtime admission is owned by another task")
        if (
            canonical.process.get("client_version") != expected_client_version
            or canonical.process.get("client_size") != expected_client_size
            or canonical.process.get("client_sha256") != expected_client_sha256
        ):
            raise ValidationError(
                "EDGE_RUNTIME_CLIENT_IDENTITY_MISMATCH",
                "runtime admission does not match the task client identity",
            )
        if type(runtime_signal_resolver) is not RuntimeSignalResolver:
            raise ValidationError(
                "EDGE_RUNTIME_SIGNAL_RESOLVER_INVALID",
                "typed trusted runtime-signal resolver is required",
            )
        binding = _require_signal_binding(runtime_signal_binding)
        if (
            binding.session_id != session_id
            or binding.run_id != run_id
            or binding.runtime_id != canonical.runtime_namespace
            or binding.runtime_binding_sha256 != canonical.runtime_binding_sha256
        ):
            raise ValidationError(
                "EDGE_RUNTIME_ADMISSION_BINDING_MISMATCH",
                "runtime admission and runtime-signal binding do not identify the active task/run/runtime",
            )
        existing = self._runtime_authorities.get(session_id)
        if (
            existing is not None
            and self._live_instances.get(session_id) is not None
            and (
                existing.signal_binding != binding
                or existing.admission != canonical
                or existing.resolver is not runtime_signal_resolver
            )
        ):
            raise ValidationError("EDGE_RUNTIME_ADMISSION_BINDING_MISMATCH", "live runtime authority cannot be silently replaced")
        self._runtime_authorities[session_id] = _RuntimeAuthority(canonical, binding, runtime_signal_resolver)
        return canonical, binding

    def _authority_status(
        self,
        *,
        session_id: str,
        task_id: str | None,
        current_run_id: str | None,
        runtime_access: str,
        task_deadline_epoch_ms: int | None,
        now_epoch_ms: int,
    ) -> dict[str, object]:
        authority = self._runtime_authorities.get(session_id)
        if runtime_access != "read_only":
            return {"bound": authority is not None, "current": False, "reason": "RUNTIME_NOT_ADMITTED"}
        if authority is None:
            return {"bound": False, "current": False, "reason": "RUNTIME_ADMISSION_REQUIRED"}
        if (
            type(task_deadline_epoch_ms) is not int
            or task_deadline_epoch_ms < 0
            or _epoch(now_epoch_ms, "now_epoch_ms") >= task_deadline_epoch_ms
        ):
            return {"bound": True, "current": False, "reason": "EDGE_TASK_DEADLINE_EXPIRED"}
        if task_id is None or authority.admission.task_id != task_id or authority.admission.runtime_owner_task != task_id:
            return {"bound": True, "current": False, "reason": "RUNTIME_ADMISSION_BINDING_STALE"}
        if current_run_id is None or authority.signal_binding.run_id != current_run_id:
            return {"bound": True, "current": False, "reason": "RUNTIME_ADMISSION_BINDING_STALE"}
        try:
            canonical = _validated_admission(
                authority.admission,
                now_epoch_ms=_epoch(now_epoch_ms, "now_epoch_ms"),
                max_age_ms=self.heartbeat_timeout_ms,
            )
        except ValidationError as exc:
            return {
                "bound": True,
                "current": False,
                "reason": exc.code,
                "runtime_namespace": authority.admission.runtime_namespace,
                "runtime_binding_sha256": authority.admission.runtime_binding_sha256,
                "observed_at_epoch_ms": authority.admission.observed_at_epoch_ms,
            }
        return {
            "bound": True,
            "current": True,
            "reason": "CURRENT",
            "task_id": canonical.task_id,
            "runtime_namespace": canonical.runtime_namespace,
            "runtime_binding_sha256": canonical.runtime_binding_sha256,
            "runtime_id": authority.signal_binding.runtime_id,
            "runtime_instance_id": authority.signal_binding.runtime_instance_id,
            "observed_at_epoch_ms": canonical.observed_at_epoch_ms,
        }

    def runtime_authority_is_current(
        self,
        *,
        session_id: str,
        task_id: str | None,
        current_run_id: str | None,
        runtime_access: str,
        task_deadline_epoch_ms: int | None,
        now_epoch_ms: int,
    ) -> bool:
        return self._authority_status(
            session_id=session_id,
            task_id=task_id,
            current_run_id=current_run_id,
            runtime_access=runtime_access,
            task_deadline_epoch_ms=task_deadline_epoch_ms,
            now_epoch_ms=now_epoch_ms,
        ).get("current") is True

    def accept(
        self,
        value: Mapping[str, Any],
        *,
        now_epoch_ms: int,
        expected_session_id: str,
        expected_run_id: str,
        previous_observed_epoch_ms: int | None = None,
    ) -> EdgeObservation:
        observation = EdgeObservation.from_mapping(value)
        if observation.session_id != expected_session_id or observation.run_id != expected_run_id:
            raise ValidationError("EDGE_BINDING_MISMATCH", "edge observation does not match the active session/run")
        now = _epoch(now_epoch_ms, "now_epoch_ms")
        if observation.observed_epoch_ms > now or observation.heartbeat_epoch_ms > now:
            raise ValidationError("EDGE_OBSERVATION_FUTURE", "edge observation cannot claim future evidence")
        if previous_observed_epoch_ms is not None:
            previous = _epoch(previous_observed_epoch_ms, "previous_observed_epoch_ms")
            if observation.observed_epoch_ms <= previous:
                raise ValidationError("EDGE_OBSERVATION_REPLAY", "edge observation must advance the active run timeline")
        live_instance = self._live_instances.get(observation.session_id)
        if live_instance is not None and live_instance != observation.edge_instance_id:
            raise ValidationError("EDGE_BINDING_MISMATCH", "a different edge instance is already connected")
        self._live_instances[observation.session_id] = observation.edge_instance_id
        return observation

    def accept_runtime_signal(
        self,
        *,
        session_id: str,
        run_id: str,
        task_id: str,
        task_deadline_epoch_ms: int,
        evidence: RuntimeSignalEvidence,
        now_epoch_ms: int,
    ) -> dict[str, object]:
        authority_status = self._authority_status(
            session_id=session_id,
            task_id=task_id,
            current_run_id=run_id,
            runtime_access="read_only",
            task_deadline_epoch_ms=task_deadline_epoch_ms,
            now_epoch_ms=now_epoch_ms,
        )
        if authority_status.get("current") is not True:
            raise ValidationError(str(authority_status.get("reason")), "current read-only runtime admission is required")
        authority = self._runtime_authorities[session_id]
        if type(evidence) is not RuntimeSignalEvidence:
            raise ValidationError(
                "EDGE_RUNTIME_SIGNAL_INVALID",
                "typed reviewed runtime-signal evidence is required",
            )
        observation = evidence.observation
        signal_ref = evidence.signal_ref
        evidence_binding = evidence.binding
        clock_domain_id = evidence.clock_domain_id
        producer_id = evidence.producer_id
        contract_id = evidence.contract_id
        source_state = evidence.source_state
        observed_monotonic_ns = evidence.observed_monotonic_ns
        source_evidence_refs = evidence.source_evidence_refs
        if type(observation) is not RuntimeObservation:
            raise ValidationError("EDGE_RUNTIME_SIGNAL_INVALID", "runtime-signal observation type is invalid")
        binding = _require_signal_binding(evidence_binding)
        if binding != authority.signal_binding:
            raise ValidationError("EDGE_RUNTIME_SIGNAL_BINDING_MISMATCH", "runtime signal belongs to another runtime binding")
        signal_ref = _signal_token(signal_ref, "signal_ref")
        if _RUNTIME_SIGNAL_REF.fullmatch(signal_ref) is None or observation.evidence_refs != (signal_ref,):
            raise ValidationError("EDGE_RUNTIME_SIGNAL_INVALID", "runtime signal is not content-addressed by its reviewed observation")
        if (
            observation.state not in _RUNTIME_STATES
            or type(observation.evidence_class) is not RuntimeEvidenceClass
            or (
                observation.state in {"IN_GAME", "WORLD_EXIT"}
                and observation.evidence_class is not RuntimeEvidenceClass.REVIEWED_CAUSAL
            )
        ):
            raise ValidationError("EDGE_RUNTIME_SIGNAL_INVALID", "runtime signal semantic authority is invalid")
        clock_domain_id = _signal_token(clock_domain_id, "clock_domain_id")
        producer_id = _signal_token(producer_id, "producer_id")
        contract_id = _signal_token(contract_id, "contract_id")
        source_state = _signal_token(source_state, "source_state")
        if type(observed_monotonic_ns) is not int or observed_monotonic_ns < 0:
            raise ValidationError("EDGE_RUNTIME_SIGNAL_INVALID", "runtime signal monotonic time is invalid")
        if type(source_evidence_refs) is not tuple or len(source_evidence_refs) > _MAX_SOURCE_EVIDENCE_REFS:
            raise ValidationError("EDGE_RUNTIME_SIGNAL_INVALID", "runtime signal source evidence is invalid")
        source_refs = tuple(_signal_token(ref, "source_evidence_ref") for ref in source_evidence_refs)
        if observation.evidence_class is not RuntimeEvidenceClass.UNKNOWN and not source_refs:
            raise ValidationError("EDGE_RUNTIME_SIGNAL_INVALID", "semantic runtime signal requires source provenance")
        expected_signal_ref = "runtime-signal:" + sha256_jcs({
            "schema": "otclient.local-agent.runtime-signal.v1",
            "session_id": binding.session_id,
            "run_id": binding.run_id,
            "clock_domain_id": clock_domain_id,
            "runtime_id": binding.runtime_id,
            "runtime_instance_id": binding.runtime_instance_id,
            "runtime_binding_sha256": binding.runtime_binding_sha256,
            "producer_id": producer_id,
            "contract_id": contract_id,
            "observed_monotonic_ns": observed_monotonic_ns,
            "source_state": source_state,
            "source_evidence_refs": list(source_refs),
            "runtime_state": observation.state,
            "evidence_class": observation.evidence_class.value,
        })
        if signal_ref != expected_signal_ref:
            raise ValidationError(
                "EDGE_RUNTIME_SIGNAL_INVALID",
                "runtime-signal provenance does not match its content-addressed reference",
            )
        try:
            resolved = authority.resolver.resolve_current_reviewed(observation)
        except Exception as exc:
            raise ValidationError("EDGE_RUNTIME_SIGNAL_UNAVAILABLE", "trusted runtime-signal resolver is unavailable") from exc
        if resolved != observation:
            raise ValidationError("EDGE_RUNTIME_SIGNAL_UNTRUSTED", "runtime signal is not current reviewed evidence")
        payload: dict[str, object] = {
            "signal_ref": signal_ref,
            "status": observation.state,
            "evidence_class": observation.evidence_class.value,
            "evidence_refs": list(observation.evidence_refs),
            "binding": asdict(binding),
            "clock_domain_id": clock_domain_id,
            "producer_id": producer_id,
            "contract_id": contract_id,
            "source_state": source_state,
            "observed_monotonic_ns": observed_monotonic_ns,
            "source_evidence_refs": list(source_refs),
            "accepted_epoch_ms": _epoch(now_epoch_ms, "now_epoch_ms"),
            "physical_effect": False,
        }
        ensure_no_secret_material(payload, key_path="edge_runtime_signal")
        return payload

    def disconnect(self, session_id: str, edge_instance_id: str | None = None) -> None:
        validate_opaque_id(session_id, field_name="session_id")
        if edge_instance_id is not None:
            validate_opaque_id(edge_instance_id, field_name="edge_instance_id", max_bytes=192)
            current = self._live_instances.get(session_id)
            if current is not None and current != edge_instance_id:
                raise ValidationError("EDGE_BINDING_MISMATCH", "edge disconnect does not match the live instance")
        self._live_instances.pop(session_id, None)
        self._runtime_authorities.pop(session_id, None)

    def heartbeat_is_fresh(self, heartbeat_epoch_ms: int | None, *, now_epoch_ms: int) -> bool:
        if heartbeat_epoch_ms is None:
            return False
        now = _epoch(now_epoch_ms, "now_epoch_ms")
        return heartbeat_epoch_ms <= now and now - heartbeat_epoch_ms <= self.heartbeat_timeout_ms

    @staticmethod
    def _latest_event(events: Sequence[Mapping[str, Any]], kind: str) -> Mapping[str, Any] | None:
        for event in reversed(events):
            if event.get("kind") == kind and isinstance(event.get("payload"), Mapping):
                return event
        return None

    @staticmethod
    def _empty_capture() -> dict[str, object]:
        return {"status": "UNAVAILABLE", "artifact_ref": None, "sha256": None, "observed_epoch_ms": None, "secret_safe": True, "current": False}

    @staticmethod
    def _empty_runtime() -> dict[str, object]:
        return {
            "status": "UNKNOWN",
            "evidence_class": "UNKNOWN",
            "evidence_refs": [],
            "observed_epoch_ms": None,
            "current": False,
        }

    def _runtime_status(
        self,
        *,
        session_id: str,
        current_run_id: str | None,
        events: Sequence[Mapping[str, Any]],
        now_epoch_ms: int,
        edge_current: bool,
        admission_current: bool,
    ) -> dict[str, object]:
        latest = self._latest_event(events, "EDGE_RUNTIME_SIGNAL")
        authority = self._runtime_authorities.get(session_id)
        if latest is None or authority is None:
            return self._empty_runtime()
        payload = latest["payload"]
        accepted_epoch_ms = payload.get("accepted_epoch_ms")
        if (
            not edge_current
            or not admission_current
            or latest.get("run_id") != current_run_id
            or type(accepted_epoch_ms) is not int
            or accepted_epoch_ms > now_epoch_ms
            or now_epoch_ms - accepted_epoch_ms > self.heartbeat_timeout_ms
        ):
            current = False
        else:
            try:
                binding = _persisted_signal_binding(payload.get("binding"))
                evidence_class = RuntimeEvidenceClass(payload.get("evidence_class"))
                refs_value = payload.get("evidence_refs")
                refs = tuple(refs_value) if isinstance(refs_value, list) else ()
                observation = RuntimeObservation(
                    state=str(payload.get("status", "UNKNOWN")),
                    evidence_class=evidence_class,
                    evidence_refs=refs,
                )
                resolved = authority.resolver.resolve_current_reviewed(observation)
                current = binding == authority.signal_binding and resolved == observation
            except (ValueError, ValidationError, TypeError, AttributeError):
                current = False
            except Exception:  # noqa: BLE001 -- status rendering must fail closed
                current = False
        status = payload.get("status") if payload.get("status") in _RUNTIME_STATES else "UNKNOWN"
        evidence_class_value = payload.get("evidence_class")
        if evidence_class_value not in {member.value for member in RuntimeEvidenceClass}:
            evidence_class_value = "UNKNOWN"
        refs_value = payload.get("evidence_refs")
        refs = list(refs_value) if isinstance(refs_value, list) else []
        return {
            "status": status,
            "evidence_class": evidence_class_value,
            "evidence_refs": refs,
            "observed_epoch_ms": accepted_epoch_ms if type(accepted_epoch_ms) is int else None,
            "current": bool(current),
        }

    def status(
        self,
        *,
        session_id: str,
        task_id: str | None,
        current_run_id: str | None,
        runtime_access: str,
        task_deadline_epoch_ms: int | None,
        heartbeat_epoch_ms: int | None,
        events: Sequence[Mapping[str, Any]],
        now_epoch_ms: int,
    ) -> dict[str, object]:
        admission = self._authority_status(
            session_id=session_id,
            task_id=task_id,
            current_run_id=current_run_id,
            runtime_access=runtime_access,
            task_deadline_epoch_ms=task_deadline_epoch_ms,
            now_epoch_ms=now_epoch_ms,
        )
        latest = self._latest_event(events, "EDGE_OBSERVATION")
        if latest is None:
            return {
                "availability": "DISCONNECTED",
                "current": False,
                "reason": "NO_EDGE_OBSERVATION",
                "edge_instance_id": None,
                "heartbeat_epoch_ms": heartbeat_epoch_ms,
                "admission": admission,
                "capture": self._empty_capture(),
                "runtime": self._empty_runtime(),
            }
        payload = latest["payload"]
        edge_instance_id = payload.get("edge_instance_id")
        observed_epoch_ms = payload.get("observed_epoch_ms")
        event_run_id = latest.get("run_id")
        connected = isinstance(edge_instance_id, str) and self._live_instances.get(session_id) == edge_instance_id
        heartbeat_fresh = self.heartbeat_is_fresh(heartbeat_epoch_ms, now_epoch_ms=now_epoch_ms)
        observation_fresh = (
            type(observed_epoch_ms) is int
            and observed_epoch_ms <= now_epoch_ms
            and now_epoch_ms - observed_epoch_ms <= self.heartbeat_timeout_ms
        )
        run_matches = current_run_id is not None and event_run_id == current_run_id
        admitted = runtime_access == "read_only"
        admission_current = admission.get("current") is True
        current = bool(connected and heartbeat_fresh and observation_fresh and run_matches and admitted and admission_current)
        if not admitted:
            reason = "RUNTIME_NOT_ADMITTED"
        elif not connected:
            reason = "EDGE_DISCONNECTED"
        elif admission.get("bound") is not True:
            reason = "RUNTIME_ADMISSION_REQUIRED"
        elif not admission_current:
            reason = str(admission.get("reason", "RUNTIME_ADMISSION_INVALID"))
        elif not heartbeat_fresh:
            reason = "HEARTBEAT_STALE"
        elif not observation_fresh:
            reason = "EVIDENCE_STALE"
        elif not run_matches:
            reason = "RUN_BINDING_STALE"
        else:
            reason = "CURRENT"
        capture_value = payload.get("capture")
        if isinstance(capture_value, Mapping):
            capture = dict(capture_value)
            capture_observed = capture.get("observed_epoch_ms")
            capture["current"] = bool(
                current
                and capture.get("status") == "AVAILABLE"
                and capture.get("secret_safe") is True
                and type(capture_observed) is int
                and capture_observed <= now_epoch_ms
                and now_epoch_ms - capture_observed <= self.heartbeat_timeout_ms
            )
        else:
            capture = self._empty_capture()
        runtime = self._runtime_status(
            session_id=session_id,
            current_run_id=current_run_id,
            events=events,
            now_epoch_ms=now_epoch_ms,
            edge_current=current,
            admission_current=admission_current,
        )
        return {
            "availability": "CONNECTED" if connected else "DISCONNECTED",
            "current": current,
            "reason": reason,
            "edge_instance_id": edge_instance_id if isinstance(edge_instance_id, str) else None,
            "heartbeat_epoch_ms": heartbeat_epoch_ms,
            "admission": admission,
            "capture": capture,
            "runtime": runtime,
        }


__all__ = [
    "AgentEdgeBridge",
    "EdgeCaptureObservation",
    "EdgeObservation",
    "ReviewedRuntimeAuthorityConfiguration",
]
