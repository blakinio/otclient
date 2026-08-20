from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .fake import ManualClock
from .model import (
    Event,
    OrderingConfidence,
    PrivacyError,
    ScreenshotDisposition,
    ValidationError,
    validate_opaque_id,
)

_SECRET_KEYS = {
    "password", "passwd", "2fa", "otp", "auth_token", "access_token",
    "refresh_token", "session_token", "cookie", "cookies", "authorization",
    "control_nonce", "api_key", "private_key", "secret", "credential",
    "credentials", "ticket",
}
_SECRET_VALUE_PATTERNS = (
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{8,}"),
    re.compile(r"(?i)\b(?:OPENAI_API_KEY|API_KEY|PASSWORD|AUTH_TOKEN|SESSION_TOKEN|CONTROL_NONCE)\s*="),
    re.compile(r"(?i)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)
_EVENT_KINDS = {
    "SYSTEM", "AUTHORITY", "ACTION", "TRACE", "NET", "STATE", "SCREEN",
    "SNAPSHOT", "ASSERTION", "RESULT", "ERROR",
}
_SENSITIVITIES = {"PUBLIC", "RESEARCH_INTERNAL", "PERSONAL_REDACTED", "SECRET_REJECTED"}


def ensure_no_secret_material(value: Any, *, key_path: str = "payload") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = str(key).lower()
            if normalized in _SECRET_KEYS or normalized.endswith(("_password", "_token", "_nonce")):
                raise PrivacyError("SECRET_FIELD", f"secret-class field rejected at {key_path}")
            if normalized in {"private_chat", "private_message", "raw_chat"}:
                raise PrivacyError("PRIVATE_CHAT", "unapproved private-chat content is not admitted")
            ensure_no_secret_material(child, key_path=f"{key_path}.{key}")
        return
    if isinstance(value, (list, tuple)):
        for child in value:
            ensure_no_secret_material(child, key_path=key_path)
        return
    if isinstance(value, str):
        for pattern in _SECRET_VALUE_PATTERNS:
            if pattern.search(value):
                raise PrivacyError("SECRET_VALUE", "secret-shaped text rejected before event construction")


def safe_error(code: str, *, safe_message: str, exception: BaseException | None = None) -> dict[str, str]:
    del exception
    if not code or not isinstance(code, str):
        raise ValidationError("INVALID_ERROR_CODE", "error code must be a non-empty string")
    ensure_no_secret_material(safe_message, key_path="safe_message")
    return {"code": code, "safe_message": safe_message}


def classify_screenshot(
    *,
    contains_auth_or_secret: bool,
    known_safe: bool,
    quarantine_unknown: bool = True,
) -> ScreenshotDisposition:
    if contains_auth_or_secret:
        return ScreenshotDisposition.REJECTED
    if known_safe:
        return ScreenshotDisposition.SAFE
    return ScreenshotDisposition.QUARANTINED if quarantine_unknown else ScreenshotDisposition.REJECTED


@dataclass(frozen=True)
class ScreenshotRecord:
    screenshot_id: str
    disposition: ScreenshotDisposition
    normal_artifact_bytes: bytes | None
    quarantine_bytes: bytes | None


def construct_screenshot(
    screenshot_id: str,
    pixels: bytes,
    *,
    contains_auth_or_secret: bool = False,
    known_safe: bool = False,
    quarantine_unknown: bool = True,
) -> ScreenshotRecord:
    validate_opaque_id(screenshot_id, field_name="screenshot_id")
    disposition = classify_screenshot(
        contains_auth_or_secret=contains_auth_or_secret,
        known_safe=known_safe,
        quarantine_unknown=quarantine_unknown,
    )
    if disposition == ScreenshotDisposition.SAFE:
        return ScreenshotRecord(screenshot_id, disposition, bytes(pixels), None)
    if disposition == ScreenshotDisposition.QUARANTINED:
        return ScreenshotRecord(screenshot_id, disposition, None, bytes(pixels))
    return ScreenshotRecord(screenshot_id, disposition, None, None)


class Recorder:
    def __init__(
        self,
        clock: ManualClock,
        *,
        backend_epoch: str,
        adapter_id: str,
        adapter_generation: str,
        control_generation: int = 0,
    ) -> None:
        self.clock = clock
        self.backend_epoch = backend_epoch
        self.adapter_id = adapter_id
        self.adapter_generation = adapter_generation
        self.control_generation = control_generation
        self._ingest_seq = 0
        self.events: list[Event] = []
        self.supplemental_events: list[Event] = []
        self.state = "ACTIVE"
        self.terminal_results: dict[str, Any] = {}

    def record_event(
        self,
        *,
        kind: str,
        payload: Mapping[str, Any],
        source_timestamp: int | str | None = None,
        source_clock_domain: str | None = None,
        source_sequence: int | None = None,
        source_sequence_scope: str | None = None,
        ordering_confidence: OrderingConfidence = OrderingConfidence.UNKNOWN,
        runtime_instance_id: str | None = None,
        session_epoch: str | None = None,
        run_id: str | None = None,
        experiment_id: str | None = None,
        step_id: str | None = None,
        stimulus_id: str | None = None,
        sensitivity: str = "RESEARCH_INTERNAL",
        late: bool | None = None,
    ) -> Event:
        if kind not in _EVENT_KINDS:
            raise ValidationError("INVALID_EVENT_KIND", "event kind is not admitted")
        if sensitivity not in _SENSITIVITIES or sensitivity == "SECRET_REJECTED":
            raise ValidationError("INVALID_EVENT_SENSITIVITY", "ordinary event cannot be constructed as SECRET_REJECTED")
        ensure_no_secret_material(payload)
        self._ingest_seq += 1
        is_late = self.state != "ACTIVE" if late is None else bool(late)
        event = Event(
            event_id=f"event-{self._ingest_seq}",
            ingest_seq=self._ingest_seq,
            ingested_monotonic_ns=self.clock.now_ns(),
            source_timestamp=source_timestamp,
            source_clock_domain=source_clock_domain,
            source_sequence=source_sequence,
            source_sequence_scope=source_sequence_scope,
            ordering_confidence=ordering_confidence,
            late=is_late,
            backend_epoch=self.backend_epoch,
            control_generation=self.control_generation,
            adapter_id=self.adapter_id,
            adapter_generation=self.adapter_generation,
            runtime_instance_id=runtime_instance_id,
            session_epoch=session_epoch,
            run_id=run_id,
            experiment_id=experiment_id,
            step_id=step_id,
            stimulus_id=stimulus_id,
            kind=kind,
            sensitivity=sensitivity,
            payload=dict(payload),
        )
        if self.state == "FINALIZED":
            self.supplemental_events.append(event)
        else:
            self.events.append(event)
        return event

    def record_secret_rejection(self, *, category: str, reason: str, run_id: str | None = None) -> dict[str, Any]:
        return {
            "kind": "SECRET_REJECTED",
            "category": category,
            "reason": reason,
            "run_id": run_id,
            "value_present": False,
        }

    def set_terminal_result(self, action_id: str, result: Any) -> None:
        if action_id in self.terminal_results and self.terminal_results[action_id] != result:
            raise ValidationError("TERMINAL_RESULT_IMMUTABLE", "terminal result cannot be rewritten")
        self.terminal_results[action_id] = result

    def begin_closing(self) -> None:
        if self.state == "ACTIVE":
            self.state = "CLOSING"

    def finalize(self) -> None:
        if self.state == "ACTIVE":
            self.begin_closing()
        self.state = "FINALIZED"

    @staticmethod
    def causal_order_claim(event: Event) -> str:
        if event.ordering_confidence == OrderingConfidence.KNOWN and event.source_sequence is not None:
            return "SOURCE_ORDER_KNOWN"
        return "INGESTION_ORDER_ONLY"
