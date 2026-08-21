from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping, Sequence
from decimal import Decimal
from typing import Any

from .model import MAX_SAFE_INTEGER, ValidationError


def _validate_string(value: str) -> None:
    try:
        value.encode("utf-8", "strict")
    except UnicodeEncodeError as exc:
        raise ValidationError("INVALID_UTF8", "canonical string is not valid UTF-8") from exc
    if any(0xD800 <= ord(ch) <= 0xDFFF for ch in value):
        raise ValidationError("INVALID_UTF8", "canonical string contains a surrogate code point")


def _utf16_sort_key(value: str) -> bytes:
    _validate_string(value)
    return value.encode("utf-16-be")


def _string(value: str) -> str:
    _validate_string(value)
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _normalize_exponent(text: str) -> str:
    mantissa, exponent = text.lower().split("e", 1)
    sign = ""
    if exponent.startswith(("+", "-")):
        sign, exponent = exponent[0], exponent[1:]
    exponent = exponent.lstrip("0") or "0"
    return f"{mantissa}e{sign}{exponent}" if sign else f"{mantissa}e{exponent}"


def _number(value: float) -> str:
    if isinstance(value, bool):
        raise ValidationError("INVALID_JCS_NUMBER", "boolean is not a JCS number")
    if isinstance(value, int):
        if abs(value) > MAX_SAFE_INTEGER:
            raise ValidationError("JCS_NUMBER_RANGE", "integer exceeds I-JSON IEEE-754 exact range")
        return str(value)
    if not isinstance(value, float) or not math.isfinite(value):
        raise ValidationError("INVALID_JCS_NUMBER", "JCS numbers must be finite")
    if value == 0.0:
        return "0"
    shortest = repr(value).lower()
    absolute = abs(value)
    if 1e-6 <= absolute < 1e21:
        fixed = format(Decimal(shortest), "f")
        if "." in fixed:
            fixed = fixed.rstrip("0").rstrip(".")
        return "0" if fixed == "-0" else fixed
    if "e" not in shortest:
        shortest = format(value, ".17e")
        mantissa, exponent = shortest.split("e", 1)
        shortest = mantissa.rstrip("0").rstrip(".") + "e" + exponent
    else:
        mantissa, exponent = shortest.split("e", 1)
        shortest = mantissa.removesuffix(".0") + "e" + exponent
    return _normalize_exponent(shortest)


def jcs_dumps(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return _number(value)
    if isinstance(value, str):
        return _string(value)
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise ValidationError("INVALID_JCS_OBJECT_KEY", "JCS object keys must be strings")
        return "{" + ",".join(
            _string(key) + ":" + jcs_dumps(value[key])
            for key in sorted(value.keys(), key=_utf16_sort_key)
        ) + "}"
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return "[" + ",".join(jcs_dumps(item) for item in value) + "]"
    raise ValidationError("INVALID_JCS_VALUE", f"unsupported JCS value type: {type(value).__name__}")


def sha256_jcs(value: Any) -> str:
    return hashlib.sha256(jcs_dumps(value).encode("utf-8")).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()
