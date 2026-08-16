from __future__ import annotations

import argparse
from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Mapping

HEALTH_SCHEMA = "otclient.tibia-runtime-bridge.health.v1"
OBSERVATION_SCHEMA = "otclient.tibia-runtime-bridge.runtime-observation.v1"
CANONICAL_NAMESPACE = "canonical-live-runtime"
CANONICAL_RUNTIME_ID = "track-a-canonical-live"
REGISTRATION_SCHEMA_VERSION = 1
EXACT_CLIENT_VERSION = "15.32.df7b29"
EXACT_CLIENT_SIZE = 51965216
EXACT_CLIENT_SHA256 = "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"


class Readiness(str, Enum):
    READY = "READY"
    NOT_REGISTERED = "NOT_REGISTERED"
    REGISTRATION_INVALID = "REGISTRATION_INVALID"
    EXPECTED_AUTHORITY_UNAVAILABLE = "EXPECTED_AUTHORITY_UNAVAILABLE"
    LEASE_GENERATION_MISMATCH = "LEASE_GENERATION_MISMATCH"
    GATE_B_NOT_PROVEN = "GATE_B_NOT_PROVEN"
    NAMESPACE_MISMATCH = "NAMESPACE_MISMATCH"
    OBSERVATION_STALE = "OBSERVATION_STALE"
    OBSERVATION_FROM_FUTURE = "OBSERVATION_FROM_FUTURE"
    IDENTITY_MISMATCH = "IDENTITY_MISMATCH"
    BRIDGE_UNHEALTHY = "BRIDGE_UNHEALTHY"


class ReacquisitionAction(str, Enum):
    KEEP_CURRENT = "KEEP_CURRENT"
    ACCEPT_REACQUIRED = "ACCEPT_REACQUIRED"
    DROP_CURRENT_AND_WAIT = "DROP_CURRENT_AND_WAIT"
    WAIT_FOR_VALID_REGISTRATION = "WAIT_FOR_VALID_REGISTRATION"


class RecoveryState(str, Enum):
    DETACHED = "DETACHED"
    READY = "READY"
    DEGRADED = "DEGRADED"
    REACQUIRING = "REACQUIRING"


class RecoveryAction(str, Enum):
    NONE = "NONE"
    REACQUIRE = "REACQUIRE"
    WAIT_FOR_VALID_REGISTRATION = "WAIT_FOR_VALID_REGISTRATION"


def _strict_positive_int(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        return None
    return value


def _strict_nonnegative_int(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


def _sha256_text(value: Any) -> str | None:
    if not isinstance(value, str) or len(value) != 64:
        return None
    if any(ch not in "0123456789abcdef" for ch in value):
        return None
    return value


def _nonempty_text(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    return value


def _stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


@dataclass(frozen=True)
class RuntimeIdentity:
    registration_generation: int
    lease_generation: int
    boot_id_sha256: str
    pid: int
    process_start_ticks: int
    client_version: str
    client_size: int
    client_sha256: str
    display: str
    window_identity: Any

    def as_dict(self) -> dict[str, Any]:
        return {
            "registration_generation": self.registration_generation,
            "lease_generation": self.lease_generation,
            "boot_id_sha256": self.boot_id_sha256,
            "pid": self.pid,
            "process_start_ticks": self.process_start_ticks,
            "client_version": self.client_version,
            "client_size": self.client_size,
            "client_sha256": self.client_sha256,
            "display": self.display,
            "window_identity": self.window_identity,
        }

    def fingerprint(self) -> str:
        raw = _stable_json(self.as_dict()).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class HealthReport:
    readiness: Readiness
    reason: str
    identity: RuntimeIdentity | None = None

    @property
    def ready(self) -> bool:
        return self.readiness is Readiness.READY and self.identity is not None

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": HEALTH_SCHEMA,
            "ready": self.ready,
            "readiness": self.readiness.value,
            "reason": self.reason,
            "usable_identity": self.identity.as_dict() if self.ready and self.identity is not None else None,
            "in_game": "UNKNOWN_NOT_EVALUATED_BY_HEALTH_API",
        }


def _registration_identity(registration: Mapping[str, Any]) -> tuple[RuntimeIdentity | None, str | None]:
    schema_version = _strict_positive_int(registration.get("schema_version"))
    if schema_version != REGISTRATION_SCHEMA_VERSION:
        return None, "registration schema_version must be 1"
    if registration.get("runtime_id") != CANONICAL_RUNTIME_ID:
        return None, "registration runtime_id is not canonical Track A"

    registration_generation = _strict_positive_int(registration.get("registration_generation"))
    lease_generation = _strict_positive_int(registration.get("lease_generation"))
    boot_id_sha256 = _sha256_text(registration.get("boot_id_sha256"))
    pid = _strict_positive_int(registration.get("pid"))
    process_start_ticks = _strict_positive_int(registration.get("process_start_ticks"))
    client_version = _nonempty_text(registration.get("client_version"))
    client_size = _strict_positive_int(registration.get("client_size"))
    client_sha256 = _sha256_text(registration.get("client_sha256"))
    display = _nonempty_text(registration.get("display"))
    window_identity = registration.get("window_identity")

    if registration_generation is None:
        return None, "registration_generation must be a positive integer"
    if lease_generation is None:
        return None, "lease_generation must be a positive integer"
    if boot_id_sha256 is None:
        return None, "boot_id_sha256 must be a lowercase SHA-256 digest"
    if pid is None:
        return None, "pid must be a positive integer"
    if process_start_ticks is None:
        return None, "process_start_ticks must be a positive integer"
    if client_version != EXACT_CLIENT_VERSION:
        return None, "client_version does not match the exact Track A fence"
    if client_size != EXACT_CLIENT_SIZE:
        return None, "client_size does not match the exact Track A fence"
    if client_sha256 != EXACT_CLIENT_SHA256:
        return None, "client_sha256 does not match the exact Track A fence"
    if display is None:
        return None, "display must be a non-empty declared value"
    if window_identity is None or window_identity == "" or window_identity == {} or window_identity == []:
        return None, "window_identity must contain current non-secret window evidence"

    return RuntimeIdentity(
        registration_generation=registration_generation,
        lease_generation=lease_generation,
        boot_id_sha256=boot_id_sha256,
        pid=pid,
        process_start_ticks=process_start_ticks,
        client_version=client_version,
        client_size=client_size,
        client_sha256=client_sha256,
        display=display,
        window_identity=window_identity,
    ), None


def _observation_matches_identity(observation: Mapping[str, Any], identity: RuntimeIdentity) -> bool:
    expected = identity.as_dict()
    return all(observation.get(field) == value for field, value in expected.items())


def evaluate_health(
    registration: Mapping[str, Any] | None,
    observation: Mapping[str, Any] | None,
    bridge_ping: Mapping[str, Any] | None,
    *,
    expected_lease_generation: int | None,
    now_ms: int,
    max_observation_age_ms: int = 15_000,
    max_future_skew_ms: int = 1_000,
    expected_namespace: str = CANONICAL_NAMESPACE,
) -> HealthReport:
    """Evaluate bridge readiness from caller-supplied authoritative evidence only.

    This function performs no filesystem, process, socket, X11, VNC or network discovery.
    A caller must obtain registration/Gate-B/bridge evidence through the separately
    authorized runtime owner and pass it in. Readiness is deliberately independent
    from structural IN_GAME evidence.
    """

    expected_generation = _strict_positive_int(expected_lease_generation)
    if expected_generation is None:
        return HealthReport(Readiness.EXPECTED_AUTHORITY_UNAVAILABLE, "current controller lease generation is not proven")
    if expected_namespace != CANONICAL_NAMESPACE:
        return HealthReport(Readiness.NAMESPACE_MISMATCH, "expected namespace is not the canonical Track A namespace")
    now = _strict_nonnegative_int(now_ms)
    age_limit = _strict_positive_int(max_observation_age_ms)
    future_limit = _strict_nonnegative_int(max_future_skew_ms)
    if now is None or age_limit is None or future_limit is None:
        return HealthReport(Readiness.REGISTRATION_INVALID, "health timing policy is invalid")

    if registration is None:
        return HealthReport(Readiness.NOT_REGISTERED, "authoritative runtime registration is absent")
    if not isinstance(registration, Mapping):
        return HealthReport(Readiness.REGISTRATION_INVALID, "registration must be an object")

    identity, registration_error = _registration_identity(registration)
    if identity is None:
        return HealthReport(Readiness.REGISTRATION_INVALID, registration_error or "registration identity is invalid")
    if identity.lease_generation != expected_generation:
        return HealthReport(Readiness.LEASE_GENERATION_MISMATCH, "registration lease generation does not match current controller generation")

    if observation is None or not isinstance(observation, Mapping):
        return HealthReport(Readiness.GATE_B_NOT_PROVEN, "fresh Gate B observation is absent")
    if observation.get("schema") != OBSERVATION_SCHEMA:
        return HealthReport(Readiness.GATE_B_NOT_PROVEN, "runtime observation schema is not recognized")
    if observation.get("runtime_namespace") != expected_namespace:
        return HealthReport(Readiness.NAMESPACE_MISMATCH, "runtime observation namespace does not match canonical namespace")
    if observation.get("gate_b") != "PASS" or observation.get("target_uniqueness") != "PROVEN":
        return HealthReport(Readiness.GATE_B_NOT_PROVEN, "Gate B and target uniqueness must both be freshly proven")

    checked_at = _strict_nonnegative_int(observation.get("checked_at_unix_ms"))
    if checked_at is None:
        return HealthReport(Readiness.GATE_B_NOT_PROVEN, "runtime observation timestamp is invalid")
    if checked_at > now + future_limit:
        return HealthReport(Readiness.OBSERVATION_FROM_FUTURE, "runtime observation is beyond the permitted future clock skew")
    if now - checked_at > age_limit:
        return HealthReport(Readiness.OBSERVATION_STALE, "runtime observation is older than the configured health window")

    if observation.get("registration_generation") != identity.registration_generation:
        return HealthReport(Readiness.IDENTITY_MISMATCH, "observation registration generation differs from registration")
    if observation.get("lease_generation") != expected_generation:
        return HealthReport(Readiness.LEASE_GENERATION_MISMATCH, "observation lease generation differs from current controller generation")
    if not _observation_matches_identity(observation, identity):
        return HealthReport(Readiness.IDENTITY_MISMATCH, "fresh Gate B identity does not exactly match the registered runtime")

    if not isinstance(bridge_ping, Mapping):
        return HealthReport(Readiness.BRIDGE_UNHEALTHY, "bridge PING evidence is absent")
    if bridge_ping.get("ok") is not True or bridge_ping.get("command") != "PING" or bridge_ping.get("main_base_resolved") is not True:
        return HealthReport(Readiness.BRIDGE_UNHEALTHY, "bridge PING did not prove a healthy exact-runtime helper")

    return HealthReport(Readiness.READY, "registration, current lease, fresh Gate B identity and bridge PING agree", identity)


def decide_reacquisition(current: RuntimeIdentity | None, latest: HealthReport) -> ReacquisitionAction:
    """Decide whether a previously accepted runtime identity may still be used.

    Any non-ready latest authoritative health result invalidates reuse of the old
    identity. This prevents stale PID/session/generation fallback.
    """

    if not latest.ready or latest.identity is None:
        return ReacquisitionAction.DROP_CURRENT_AND_WAIT if current is not None else ReacquisitionAction.WAIT_FOR_VALID_REGISTRATION
    if current is None:
        return ReacquisitionAction.ACCEPT_REACQUIRED
    if current.fingerprint() == latest.identity.fingerprint():
        return ReacquisitionAction.KEEP_CURRENT
    return ReacquisitionAction.ACCEPT_REACQUIRED


def recovery_transition(previous: RecoveryState, latest: HealthReport) -> tuple[RecoveryState, RecoveryAction]:
    """Pure recovery state transition; never performs login/restart/rebind itself."""

    if latest.ready:
        return RecoveryState.READY, RecoveryAction.NONE
    if previous is RecoveryState.READY:
        return RecoveryState.DEGRADED, RecoveryAction.REACQUIRE
    if previous in {RecoveryState.DEGRADED, RecoveryState.REACQUIRING}:
        return RecoveryState.REACQUIRING, RecoveryAction.WAIT_FOR_VALID_REGISTRATION
    return RecoveryState.DETACHED, RecoveryAction.WAIT_FOR_VALID_REGISTRATION


def build_recovery_report(
    current: RuntimeIdentity | None,
    previous_state: RecoveryState,
    latest: HealthReport,
) -> dict[str, Any]:
    next_state, recovery_action = recovery_transition(previous_state, latest)
    reacquisition_action = decide_reacquisition(current, latest)
    return {
        "schema": "otclient.tibia-runtime-bridge.recovery.v1",
        "previous_state": previous_state.value,
        "next_state": next_state.value,
        "recovery_action": recovery_action.value,
        "reacquisition_action": reacquisition_action.value,
        "health": latest.as_dict(),
        "accepted_identity": latest.identity.as_dict() if latest.ready and latest.identity is not None else None,
        "in_game": "UNKNOWN_NOT_EVALUATED_BY_RECOVERY_API",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate Track A runtime bridge health from authoritative evidence")
    parser.add_argument("evidence", type=Path, help="JSON evidence envelope; no runtime discovery is performed")
    args = parser.parse_args(argv)
    doc = json.loads(args.evidence.read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        raise ValueError("evidence envelope must be an object")
    report = evaluate_health(
        doc.get("registration"),
        doc.get("observation"),
        doc.get("bridge_ping"),
        expected_lease_generation=doc.get("expected_lease_generation"),
        now_ms=doc.get("now_ms"),
        max_observation_age_ms=doc.get("max_observation_age_ms", 15_000),
        max_future_skew_ms=doc.get("max_future_skew_ms", 1_000),
        expected_namespace=doc.get("expected_namespace", CANONICAL_NAMESPACE),
    )
    json.dump(report.as_dict(), sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0 if report.ready else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"bridge health error: {exc}", file=sys.stderr)
        raise SystemExit(2)
