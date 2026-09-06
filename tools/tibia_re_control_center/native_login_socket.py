from __future__ import annotations

"""Secret-free local Unix-socket composition for native login lifecycle control."""

import json
import os
from pathlib import Path
import re
import socket
import stat
from typing import Any

from .native_login_lifecycle import NativeLoginLifecycle, NativeLoginLifecycleError

_SOCKET_ENV = "OTCLIENT_TIBIA_RE_NATIVE_LOGIN_SOCKET"
_PROTOCOL_VERSION = 1
_MAX_FRAME_BYTES = 8192
_MAX_SOCKET_PATH_BYTES = 103
_SAFE_TOKEN = re.compile(r"^[A-Z][A-Z0-9_]{0,95}$")
_SAFE_OPERATION_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_BASE_RESPONSE_KEYS = {"version", "state", "bound", "current", "physical_effect", "reason"}


def _protocol_error(*, physical_effect: bool = False) -> NativeLoginLifecycleError:
    return NativeLoginLifecycleError(
        "NATIVE_LOGIN_RUNTIME_PROTOCOL_INVALID",
        "native login runtime returned an invalid response",
        physical_effect=physical_effect,
    )


def _safe_socket_path(path: Path) -> Path:
    candidate = path.expanduser()
    if not candidate.is_absolute():
        raise ValueError("native login socket path must be absolute")
    encoded = os.fsencode(candidate)
    if not encoded or len(encoded) > _MAX_SOCKET_PATH_BYTES or b"\0" in encoded:
        raise ValueError("native login socket path is outside the admitted Unix-socket bound")
    return candidate


class NativeLoginSocketExecutor:
    """Client for the local runtime supervisor's closed native-login protocol."""

    def __init__(self, path: str | Path, *, timeout_seconds: float = 2.0) -> None:
        self.path = _safe_socket_path(Path(path))
        if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, (int, float)):
            raise TypeError("timeout_seconds must be a finite positive number")
        timeout = float(timeout_seconds)
        if not (0.0 < timeout <= 10.0):
            raise ValueError("timeout_seconds must be in (0, 10]")
        self.timeout_seconds = timeout

    def status(self) -> dict[str, object]:
        return self._request("STATUS", None)

    def start(self, operation_id: str) -> dict[str, object]:
        self._validate_operation_id(operation_id)
        return self._request("START", operation_id)

    def stop(self, operation_id: str) -> dict[str, object]:
        self._validate_operation_id(operation_id)
        return self._request("STOP", operation_id)

    @staticmethod
    def _validate_operation_id(operation_id: str) -> None:
        if not isinstance(operation_id, str) or _SAFE_OPERATION_ID.fullmatch(operation_id) is None:
            raise NativeLoginLifecycleError(
                "NATIVE_LOGIN_OPERATION_ID_INVALID",
                "native login operation identity is invalid",
            )

    def _preflight_socket(self) -> None:
        try:
            info = os.lstat(self.path)
        except OSError as exc:
            raise NativeLoginLifecycleError(
                "NATIVE_LOGIN_RUNTIME_UNAVAILABLE",
                "native login runtime is unavailable",
            ) from exc
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISSOCK(info.st_mode):
            raise NativeLoginLifecycleError(
                "NATIVE_LOGIN_RUNTIME_UNAVAILABLE",
                "native login runtime is unavailable",
            )
        if info.st_mode & 0o022:
            raise NativeLoginLifecycleError(
                "NATIVE_LOGIN_RUNTIME_UNAVAILABLE",
                "native login runtime is unavailable",
            )

    def _request(self, command: str, operation_id: str | None) -> dict[str, object]:
        self._preflight_socket()
        request: dict[str, object] = {"version": _PROTOCOL_VERSION, "command": command}
        if operation_id is not None:
            request["operation_id"] = operation_id
        encoded = json.dumps(request, separators=(",", ":"), ensure_ascii=True).encode("ascii") + b"\n"
        if len(encoded) > _MAX_FRAME_BYTES:
            raise NativeLoginLifecycleError(
                "NATIVE_LOGIN_RUNTIME_PROTOCOL_INVALID",
                "native login runtime request is outside the admitted bound",
            )

        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            client.settimeout(self.timeout_seconds)
            client.connect(str(self.path))
            client.sendall(encoded)
            raw = bytearray()
            while b"\n" not in raw:
                chunk = client.recv(min(4096, _MAX_FRAME_BYTES + 1 - len(raw)))
                if not chunk:
                    raise _protocol_error()
                raw.extend(chunk)
                if len(raw) > _MAX_FRAME_BYTES:
                    raise _protocol_error()
        except NativeLoginLifecycleError:
            raise
        except OSError as exc:
            raise NativeLoginLifecycleError(
                "NATIVE_LOGIN_RUNTIME_UNAVAILABLE",
                "native login runtime is unavailable",
            ) from exc
        finally:
            client.close()

        frame, trailing = bytes(raw).split(b"\n", 1)
        if trailing:
            raise _protocol_error()
        try:
            decoded = json.loads(frame)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise _protocol_error() from exc
        return self._validate_response(decoded, operation_id)

    @staticmethod
    def _validate_response(value: Any, operation_id: str | None) -> dict[str, object]:
        possible_effect = bool(value.get("physical_effect")) if isinstance(value, dict) else False
        if not isinstance(value, dict):
            raise _protocol_error(physical_effect=possible_effect)
        required = set(_BASE_RESPONSE_KEYS)
        if operation_id is not None:
            required.add("operation_id")
        if set(value) != required:
            raise _protocol_error(physical_effect=possible_effect)
        if isinstance(value["version"], bool) or value["version"] != _PROTOCOL_VERSION:
            raise _protocol_error(physical_effect=possible_effect)
        if type(value["bound"]) is not bool or type(value["current"]) is not bool or type(value["physical_effect"]) is not bool:
            raise _protocol_error(physical_effect=possible_effect)
        state = value["state"]
        reason = value["reason"]
        if not isinstance(state, str) or _SAFE_TOKEN.fullmatch(state) is None:
            raise _protocol_error(physical_effect=possible_effect)
        if not isinstance(reason, str) or _SAFE_TOKEN.fullmatch(reason) is None:
            raise _protocol_error(physical_effect=possible_effect)
        if operation_id is not None:
            returned_id = value["operation_id"]
            if returned_id != operation_id:
                raise NativeLoginLifecycleError(
                    "NATIVE_LOGIN_OPERATION_ID_MISMATCH",
                    "native login runtime operation identity did not match",
                    physical_effect=bool(value["physical_effect"]),
                )
        result = dict(value)
        result.pop("version", None)
        return result


def lifecycle_from_environment() -> NativeLoginLifecycle:
    raw = os.environ.get(_SOCKET_ENV, "")
    if not raw:
        return NativeLoginLifecycle()
    try:
        executor = NativeLoginSocketExecutor(raw)
    except (TypeError, ValueError) as exc:
        raise NativeLoginLifecycleError(
            "NATIVE_LOGIN_RUNTIME_CONFIGURATION_INVALID",
            "native login runtime configuration is invalid",
        ) from exc
    return NativeLoginLifecycle(executor=executor)


__all__ = ("NativeLoginSocketExecutor", "lifecycle_from_environment")
