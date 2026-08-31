"""Shared secret-material admission guard for Control Center boundaries."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any

from .model import PrivacyError

_SECRET_KEYS = {
    "password", "passwd", "2fa", "otp", "auth_token", "access_token",
    "refresh_token", "session_token", "cookie", "cookies", "authorization",
    "control_nonce", "api_key", "api_token", "private_key", "secret", "credential",
    "credentials", "ticket", "token",
}
_SECRET_VALUE_PATTERNS = (
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{8,}"),
    re.compile(
        r"(?i)\b(?:"
        r"OPENAI[-_\s]*API[-_\s]*KEY|API[-_\s]*(?:KEY|TOKEN)|PASSWORD|PASSWD|TOKEN|"
        r"AUTH[-_\s]*TOKEN|ACCESS[-_\s]*TOKEN|REFRESH[-_\s]*TOKEN|"
        r"SESSION[-_\s]*TOKEN|CONTROL[-_\s]*NONCE|AUTHORIZATION|"
        r"CREDENTIALS?|SECRET|PRIVATE[-_\s]*KEY"
        r")\b\s*[:=]\s*\S+"
    ),
    re.compile(r"(?i)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


def ensure_no_secret_material(value: Any, *, key_path: str = "payload") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = re.sub(r"[^a-z0-9]+", "_", str(key).casefold()).strip("_")
            if normalized in _SECRET_KEYS or normalized.endswith(("_password", "_token", "_nonce")):
                raise PrivacyError("SECRET_FIELD", f"secret-class field rejected at {key_path}")
            if normalized in {"private_chat", "private_message", "raw_chat"}:
                raise PrivacyError("PRIVATE_CHAT", "unapproved private-chat content is not admitted")
            ensure_no_secret_material(child, key_path=f"{key_path}.{key}")
        return
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for child in value:
            ensure_no_secret_material(child, key_path=key_path)
        return
    if isinstance(value, str):
        for pattern in _SECRET_VALUE_PATTERNS:
            if pattern.search(value):
                raise PrivacyError("SECRET_VALUE", "secret-shaped text rejected before event construction")
