"""Fail-closed, authority-neutral Control Center view of a read-only runtime edge."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from typing import Any

from .model import (
    MAX_SAFE_INTEGER,
    ValidationError,
    checked_non_negative,
    require_exact_keys,
    validate_opaque_id,
)
from .recorder import ensure_no_secret_material

_EDGE_SCHEMA = "otclient.local-agent.edge-observation.v1"
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_CAPTURE_STATUSES = frozenset({"AVAILABLE", "UNAVAILABLE", "STALE", "REJECTED_UNSAFE_CAPTURE"})
_RUNTIME_STATUSES = frozenset({"UNKNOWN", "IN_GAME", "WORLD_EXIT"})


def _epoch(value: Any, field: str) -> int:
    return checked_non_negative(value, maximum=MAX_SAFE_INTEGER, field_name=field)


def _optional_ref(value: Any, field: str) -> str | None:
    if value is None:
        return None
    return validate_opaque_id(value, field_name=field, max_bytes=384)


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
class EdgeRuntimeObservation:
    status: str
    evidence_refs: tuple[str, ...]
    observed_epoch_ms: int

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> EdgeRuntimeObservation:
        if not isinstance(value, Mapping):
            raise ValidationError("EDGE_RUNTIME_INVALID", "edge runtime evidence must be a mapping")
        require_exact_keys(value, ("status", "evidence_refs", "observed_epoch_ms"))
        status = value["status"]
        if status not in _RUNTIME_STATUSES:
            raise ValidationError("EDGE_RUNTIME_INVALID", "edge runtime status is not admitted")
        refs = value["evidence_refs"]
        if not isinstance(refs, Sequence) or isinstance(refs, (str, bytes, bytearray)):
            raise ValidationError("EDGE_RUNTIME_INVALID", "edge runtime evidence_refs must be a sequence")
        parsed_refs = tuple(validate_opaque_id(ref, field_name="runtime_evidence_ref", max_bytes=384) for ref in refs)
        if status != "UNKNOWN" and not parsed_refs:
            raise ValidationError("EDGE_RUNTIME_INVALID", "non-unknown runtime status requires evidence provenance")
        return cls(status, parsed_refs, _epoch(value["observed_epoch_ms"], "runtime.observed_epoch_ms"))


@dataclass(frozen=True)
class EdgeObservation:
    schema: str
    session_id: str
    run_id: str
    edge_instance_id: str
    observed_epoch_ms: int
    heartbeat_epoch_ms: int
    capture: EdgeCaptureObservation | None
    runtime: EdgeRuntimeObservation | None

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
        parsed = cls(
            schema=_EDGE_SCHEMA,
            session_id=validate_opaque_id(value["session_id"], field_name="session_id"),
            run_id=validate_opaque_id(value["run_id"], field_name="run_id"),
            edge_instance_id=validate_opaque_id(value["edge_instance_id"], field_name="edge_instance_id", max_bytes=192),
            observed_epoch_ms=_epoch(value["observed_epoch_ms"], "observed_epoch_ms"),
            heartbeat_epoch_ms=_epoch(value["heartbeat_epoch_ms"], "heartbeat_epoch_ms"),
            capture=None if value["capture"] is None else EdgeCaptureObservation.from_mapping(value["capture"]),
            runtime=None if value["runtime"] is None else EdgeRuntimeObservation.from_mapping(value["runtime"]),
        )
        if parsed.heartbeat_epoch_ms > parsed.observed_epoch_ms:
            raise ValidationError("EDGE_OBSERVATION_INVALID", "edge heartbeat cannot postdate its observation")
        if parsed.capture is not None and parsed.capture.observed_epoch_ms > parsed.observed_epoch_ms:
            raise ValidationError("EDGE_OBSERVATION_INVALID", "edge capture cannot postdate its observation")
        if parsed.runtime is not None and parsed.runtime.observed_epoch_ms > parsed.observed_epoch_ms:
            raise ValidationError("EDGE_OBSERVATION_INVALID", "edge runtime evidence cannot postdate its observation")
        ensure_no_secret_material(asdict(parsed), key_path="edge_observation")
        return parsed


class AgentEdgeBridge:
    """Track live edge connection identity while deriving currentness from durable evidence."""

    def __init__(self, *, heartbeat_timeout_ms: int = 15_000) -> None:
        if type(heartbeat_timeout_ms) is not int or heartbeat_timeout_ms < 1 or heartbeat_timeout_ms > 300_000:
            raise ValueError("heartbeat_timeout_ms must be between 1 and 300000")
        self.heartbeat_timeout_ms = heartbeat_timeout_ms
        self._live_instances: dict[str, str] = {}

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

    def disconnect(self, session_id: str, edge_instance_id: str | None = None) -> None:
        validate_opaque_id(session_id, field_name="session_id")
        if edge_instance_id is not None:
            validate_opaque_id(edge_instance_id, field_name="edge_instance_id", max_bytes=192)
            current = self._live_instances.get(session_id)
            if current is not None and current != edge_instance_id:
                raise ValidationError("EDGE_BINDING_MISMATCH", "edge disconnect does not match the live instance")
        self._live_instances.pop(session_id, None)

    def heartbeat_is_fresh(self, heartbeat_epoch_ms: int | None, *, now_epoch_ms: int) -> bool:
        if heartbeat_epoch_ms is None:
            return False
        now = _epoch(now_epoch_ms, "now_epoch_ms")
        return heartbeat_epoch_ms <= now and now - heartbeat_epoch_ms <= self.heartbeat_timeout_ms

    @staticmethod
    def _latest_observation(events: Sequence[Mapping[str, Any]]) -> Mapping[str, Any] | None:
        for event in reversed(events):
            if event.get("kind") == "EDGE_OBSERVATION" and isinstance(event.get("payload"), Mapping):
                return event
        return None

    @staticmethod
    def _empty_capture() -> dict[str, object]:
        return {"status": "UNAVAILABLE", "artifact_ref": None, "sha256": None, "observed_epoch_ms": None, "secret_safe": True, "current": False}

    @staticmethod
    def _empty_runtime() -> dict[str, object]:
        return {"status": "UNKNOWN", "evidence_refs": [], "observed_epoch_ms": None, "current": False}

    def status(
        self,
        *,
        session_id: str,
        current_run_id: str | None,
        runtime_access: str,
        heartbeat_epoch_ms: int | None,
        events: Sequence[Mapping[str, Any]],
        now_epoch_ms: int,
    ) -> dict[str, object]:
        latest = self._latest_observation(events)
        if latest is None:
            return {
                "availability": "DISCONNECTED",
                "current": False,
                "reason": "NO_EDGE_OBSERVATION",
                "edge_instance_id": None,
                "heartbeat_epoch_ms": heartbeat_epoch_ms,
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
        current = bool(connected and heartbeat_fresh and observation_fresh and run_matches and admitted)
        if not admitted:
            reason = "RUNTIME_NOT_ADMITTED"
        elif not connected:
            reason = "EDGE_DISCONNECTED"
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
        runtime_value = payload.get("runtime")
        if isinstance(runtime_value, Mapping):
            runtime = dict(runtime_value)
            runtime_observed = runtime.get("observed_epoch_ms")
            runtime["evidence_refs"] = list(runtime.get("evidence_refs") or [])
            runtime["current"] = bool(
                current
                and type(runtime_observed) is int
                and runtime_observed <= now_epoch_ms
                and now_epoch_ms - runtime_observed <= self.heartbeat_timeout_ms
            )
        else:
            runtime = self._empty_runtime()
        return {
            "availability": "CONNECTED" if connected else "DISCONNECTED",
            "current": current,
            "reason": reason,
            "edge_instance_id": edge_instance_id if isinstance(edge_instance_id, str) else None,
            "heartbeat_epoch_ms": heartbeat_epoch_ms,
            "capture": capture,
            "runtime": runtime,
        }


__all__ = [
    "AgentEdgeBridge",
    "EdgeCaptureObservation",
    "EdgeObservation",
    "EdgeRuntimeObservation",
]
