from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Mapping

from .ipc_client import (
    BridgeClientError,
    BridgeProtocolError,
    BridgeTransportError,
    request,
    session_status,
)

EXPECTED_RUNTIME_ID = "track-a-canonical-live"
EXPECTED_CLIENT_VERSION = "15.32.df7b29"
EXPECTED_CLIENT_SIZE = 51_965_216
EXPECTED_CLIENT_SHA256 = "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"
DERIVED_SESSION_EVIDENCE = "DERIVED_UNTIL_LIVE_CORRELATION"


class BridgeIdentityError(ValueError):
    """An explicit runtime identity/binding is absent from the accepted fence."""


def _positive_int(value: object, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise BridgeIdentityError(f"{field} must be a positive integer")
    return value


def _sha256(value: object, field: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise BridgeIdentityError(f"{field} must be a lowercase SHA-256 hex digest")
    return value


@dataclass(frozen=True)
class RuntimeIdentity:
    runtime_id: str
    registration_generation: int
    lease_generation: int
    boot_id_sha256: str
    pid: int
    process_start_ticks: int
    client_version: str
    client_size: int
    client_sha256: str

    def __post_init__(self) -> None:
        if self.runtime_id != EXPECTED_RUNTIME_ID:
            raise BridgeIdentityError(f"runtime_id must be {EXPECTED_RUNTIME_ID}")
        _positive_int(self.registration_generation, "registration_generation")
        _positive_int(self.lease_generation, "lease_generation")
        _sha256(self.boot_id_sha256, "boot_id_sha256")
        _positive_int(self.pid, "pid")
        _positive_int(self.process_start_ticks, "process_start_ticks")
        if self.client_version != EXPECTED_CLIENT_VERSION:
            raise BridgeIdentityError(f"client_version must be {EXPECTED_CLIENT_VERSION}")
        if self.client_size != EXPECTED_CLIENT_SIZE:
            raise BridgeIdentityError(f"client_size must be {EXPECTED_CLIENT_SIZE}")
        if self.client_sha256 != EXPECTED_CLIENT_SHA256:
            raise BridgeIdentityError(f"client_sha256 must be {EXPECTED_CLIENT_SHA256}")

    @classmethod
    def from_registration(cls, registration: Mapping[str, object]) -> RuntimeIdentity:
        if registration.get("schema_version") != 1:
            raise BridgeIdentityError("registration schema_version must be 1")
        return cls(
            runtime_id=str(registration.get("runtime_id", "")),
            registration_generation=_positive_int(
                registration.get("registration_generation"), "registration_generation"
            ),
            lease_generation=_positive_int(registration.get("lease_generation"), "lease_generation"),
            boot_id_sha256=_sha256(registration.get("boot_id_sha256"), "boot_id_sha256"),
            pid=_positive_int(registration.get("pid"), "pid"),
            process_start_ticks=_positive_int(
                registration.get("process_start_ticks"), "process_start_ticks"
            ),
            client_version=str(registration.get("client_version", "")),
            client_size=_positive_int(registration.get("client_size"), "client_size"),
            client_sha256=_sha256(registration.get("client_sha256"), "client_sha256"),
        )


@dataclass(frozen=True)
class BridgeBinding:
    identity: RuntimeIdentity
    socket_path: Path

    def __post_init__(self) -> None:
        socket_path = Path(self.socket_path)
        if not socket_path.is_absolute():
            raise BridgeIdentityError("bridge socket_path must be absolute")
        if not socket_path.name:
            raise BridgeIdentityError("bridge socket_path must name an endpoint")
        object.__setattr__(self, "socket_path", socket_path)

    @classmethod
    def from_registration(
        cls, registration: Mapping[str, object], *, socket_path: Path
    ) -> BridgeBinding:
        return cls(RuntimeIdentity.from_registration(registration), socket_path)


class ReacquireState(str, Enum):
    ACQUIRED = "ACQUIRED"
    NO_IDENTITY = "NO_IDENTITY"
    INVALID_IDENTITY = "INVALID_IDENTITY"
    STALE_IDENTITY = "STALE_IDENTITY"


@dataclass(frozen=True)
class ReacquireResult:
    state: ReacquireState
    binding: BridgeBinding | None
    detail: str


class HealthState(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNREACHABLE = "UNREACHABLE"
    MALFORMED = "MALFORMED"
    NO_IDENTITY = "NO_IDENTITY"
    INVALID_IDENTITY = "INVALID_IDENTITY"
    STALE_IDENTITY = "STALE_IDENTITY"


@dataclass(frozen=True)
class BridgeHealth:
    state: HealthState
    bridge_ready: bool
    in_game_candidate: bool | None
    evidence_level: str
    detail: str
    identity: RuntimeIdentity | None


@dataclass(frozen=True)
class RecoveryPolicy:
    max_attempts: int = 3

    def __post_init__(self) -> None:
        _positive_int(self.max_attempts, "max_attempts")


@dataclass(frozen=True)
class RecoveryResult:
    recovered: bool
    attempts: int
    health: BridgeHealth


BindingSource = Callable[[], BridgeBinding | None]
RequestFunction = Callable[..., dict[str, Any]]
StatusFunction = Callable[..., dict[str, Any]]
RetryHook = Callable[[int, BridgeHealth], None]


class BridgeSession:
    """Fail-closed P1 view over an explicitly supplied runtime binding.

    The session never reads canonical runtime state itself and never launches, restarts,
    logs in, signals, attaches to, or mutates a client. A caller/RUNTIME producer must
    supply each current identity and endpoint explicitly.
    """

    def __init__(
        self,
        binding_source: BindingSource,
        *,
        timeout: float = 3.0,
        request_fn: RequestFunction = request,
        status_fn: StatusFunction = session_status,
    ) -> None:
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        self._binding_source = binding_source
        self._timeout = timeout
        self._request = request_fn
        self._session_status = status_fn
        self._binding: BridgeBinding | None = None
        self._latest_observed: BridgeBinding | None = None

    @property
    def binding(self) -> BridgeBinding | None:
        return self._binding

    def _observe(self) -> BridgeBinding | None:
        candidate = self._binding_source()
        if candidate is None:
            return None
        if not isinstance(candidate, BridgeBinding):
            raise BridgeIdentityError("binding source must return BridgeBinding or None")

        previous = self._latest_observed
        if previous is not None:
            old = previous.identity
            new = candidate.identity
            if new.registration_generation < old.registration_generation:
                raise BridgeIdentityError("registration_generation regressed")
            if new.lease_generation < old.lease_generation:
                raise BridgeIdentityError("lease_generation regressed")
            if new.registration_generation == old.registration_generation and candidate != previous:
                raise BridgeIdentityError("runtime binding changed without registration_generation advance")
        self._latest_observed = candidate
        return candidate

    def reacquire(self) -> ReacquireResult:
        try:
            candidate = self._observe()
        except BridgeIdentityError as exc:
            self._binding = None
            state = (
                ReacquireState.STALE_IDENTITY
                if "regressed" in str(exc) or "without registration_generation" in str(exc)
                else ReacquireState.INVALID_IDENTITY
            )
            return ReacquireResult(state, None, str(exc))

        if candidate is None:
            self._binding = None
            return ReacquireResult(
                ReacquireState.NO_IDENTITY,
                None,
                "no explicit runtime binding is currently available",
            )

        self._binding = candidate
        return ReacquireResult(ReacquireState.ACQUIRED, candidate, "explicit runtime binding acquired")

    def _identity_guard(self, stage: str) -> BridgeHealth | None:
        binding = self._binding
        if binding is None:
            return self._health(HealthState.NO_IDENTITY, False, None, "no binding; reacquisition required")
        try:
            current = self._observe()
        except BridgeIdentityError as exc:
            self._binding = None
            return self._health(HealthState.STALE_IDENTITY, False, None, f"{stage}: {exc}", identity=binding.identity)
        if current is None:
            self._binding = None
            return self._health(
                HealthState.NO_IDENTITY,
                False,
                None,
                f"{stage}: explicit runtime binding disappeared",
                identity=binding.identity,
            )
        if current != binding:
            self._binding = None
            return self._health(
                HealthState.STALE_IDENTITY,
                False,
                None,
                f"{stage}: runtime identity or endpoint changed; cached channel discarded",
                identity=binding.identity,
            )
        return None

    def _health(
        self,
        state: HealthState,
        bridge_ready: bool,
        in_game_candidate: bool | None,
        detail: str,
        *,
        identity: RuntimeIdentity | None = None,
        evidence_level: str = "UNKNOWN",
    ) -> BridgeHealth:
        if identity is None and self._binding is not None:
            identity = self._binding.identity
        return BridgeHealth(
            state=state,
            bridge_ready=bridge_ready,
            in_game_candidate=in_game_candidate,
            evidence_level=evidence_level,
            detail=detail,
            identity=identity,
        )

    def probe(self) -> BridgeHealth:
        guard = self._identity_guard("before PING")
        if guard is not None:
            return guard
        assert self._binding is not None
        binding = self._binding

        try:
            ping = self._request(binding.socket_path, "PING", timeout=self._timeout)
        except BridgeTransportError as exc:
            return self._health(HealthState.UNREACHABLE, False, None, str(exc))
        except BridgeProtocolError as exc:
            return self._health(HealthState.MALFORMED, False, None, str(exc))
        except BridgeClientError as exc:
            return self._health(HealthState.MALFORMED, False, None, str(exc))

        if ping.get("command") != "PING" or not isinstance(ping.get("main_base_resolved"), bool):
            return self._health(HealthState.MALFORMED, False, None, "PING response is structurally incomplete")
        if not ping.get("ok") or not ping["main_base_resolved"]:
            return self._health(HealthState.DEGRADED, False, None, "PING did not establish a ready bridge")

        guard = self._identity_guard("after PING")
        if guard is not None:
            return guard
        assert self._binding is not None

        try:
            status = self._session_status(self._binding.socket_path, timeout=self._timeout)
        except BridgeTransportError as exc:
            return self._health(HealthState.UNREACHABLE, False, None, str(exc))
        except BridgeProtocolError as exc:
            return self._health(HealthState.MALFORMED, False, None, str(exc))
        except BridgeClientError as exc:
            return self._health(HealthState.MALFORMED, False, None, str(exc))

        guard = self._identity_guard("after session-status")
        if guard is not None:
            return guard

        if not isinstance(status, dict) or not isinstance(status.get("ok"), bool):
            return self._health(HealthState.MALFORMED, False, None, "session-status response is structurally invalid")
        if not status["ok"]:
            return self._health(HealthState.DEGRADED, False, False, "session-status reported a bridge-side discovery failure")
        candidate = status.get("in_game_candidate")
        evidence_level = status.get("evidence_level")
        if not isinstance(candidate, bool) or evidence_level != DERIVED_SESSION_EVIDENCE:
            return self._health(
                HealthState.MALFORMED,
                False,
                None,
                "session-status must retain derived candidate semantics",
            )
        return self._health(
            HealthState.HEALTHY,
            True,
            candidate,
            "bridge and bounded read API are responsive",
            evidence_level=DERIVED_SESSION_EVIDENCE,
        )

    def recover(
        self,
        policy: RecoveryPolicy = RecoveryPolicy(),
        *,
        on_retry: RetryHook | None = None,
    ) -> RecoveryResult:
        last_health = self._health(
            HealthState.NO_IDENTITY,
            False,
            None,
            "recovery has not acquired an explicit runtime binding",
        )
        for attempt in range(1, policy.max_attempts + 1):
            reacquired = self.reacquire()
            if reacquired.state is ReacquireState.ACQUIRED:
                last_health = self.probe()
            elif reacquired.state is ReacquireState.NO_IDENTITY:
                last_health = self._health(HealthState.NO_IDENTITY, False, None, reacquired.detail)
            elif reacquired.state is ReacquireState.STALE_IDENTITY:
                last_health = self._health(HealthState.STALE_IDENTITY, False, None, reacquired.detail)
            else:
                last_health = self._health(HealthState.INVALID_IDENTITY, False, None, reacquired.detail)

            if last_health.state is HealthState.HEALTHY:
                return RecoveryResult(True, attempt, last_health)
            if attempt < policy.max_attempts and on_retry is not None:
                on_retry(attempt, last_health)
        return RecoveryResult(False, policy.max_attempts, last_health)
