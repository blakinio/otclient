from __future__ import annotations

"""Fail-closed local supervisor for the Control Center native-login lifecycle."""

from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import secrets
import socket
import stat
import threading
import time
from typing import Any, Callable

from tools.tibia_re_control_center.current_client_fence import current_client_fence

_PROTOCOL_VERSION = 1
_MAX_FRAME_BYTES = 8192
_MAX_PERMIT_BYTES = 4096
_MAX_PERMIT_LIFETIME_SECONDS = 900
_SAFE_OPERATION_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_PERMIT_SCHEMA = "otclient.track-a.native-login-permit.v1"
_PERMIT_AUTHORIZATION = "ONE_SHOT_NATIVE_LOGIN"
_ACTIVE_STATES = frozenset({"STARTING", "STOPPING", "IN_GAME"})


@dataclass(frozen=True, slots=True)
class NativeLoginPermit:
    expires_at_epoch: int
    boot_id_sha256: str
    pid: int
    process_start_ticks: int
    client_version: str
    client_size: int
    client_sha256: str


class NativeLoginPermitStore:
    """Atomically consumes one exact-current, short-lived local permit."""

    def __init__(self, path: str | Path, *, now: Callable[[], float] = time.time) -> None:
        self.path = Path(path)
        self._now = now

    def consume(self, operation_id: str) -> NativeLoginPermit:
        _validate_operation_id(operation_id)
        claimed = self.path.with_name(
            f".{self.path.name}.claim-{os.getpid()}-{threading.get_ident()}-{secrets.token_hex(4)}"
        )
        try:
            os.rename(self.path, claimed)
        except FileNotFoundError as exc:
            raise RuntimeError("AUTHORIZATION_REQUIRED") from exc
        except OSError as exc:
            raise RuntimeError("AUTHORIZATION_INVALID") from exc

        try:
            info = os.lstat(claimed)
            if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
                raise RuntimeError("AUTHORIZATION_INVALID")
            if stat.S_IMODE(info.st_mode) != 0o600 or not (0 < info.st_size <= _MAX_PERMIT_BYTES):
                raise RuntimeError("AUTHORIZATION_INVALID")
            with claimed.open("r", encoding="utf-8") as handle:
                payload = json.load(handle, object_pairs_hook=_no_duplicate_keys)
            return self._validate(payload)
        except RuntimeError:
            raise
        except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
            raise RuntimeError("AUTHORIZATION_INVALID") from exc
        finally:
            try:
                claimed.unlink()
            except FileNotFoundError:
                pass

    def _validate(self, payload: Any) -> NativeLoginPermit:
        expected_keys = {
            "schema",
            "authorization",
            "expires_at_epoch",
            "boot_id_sha256",
            "pid",
            "process_start_ticks",
            "client_version",
            "client_size",
            "client_sha256",
        }
        if not isinstance(payload, dict) or set(payload) != expected_keys:
            raise RuntimeError("AUTHORIZATION_INVALID")
        if payload["schema"] != _PERMIT_SCHEMA or payload["authorization"] != _PERMIT_AUTHORIZATION:
            raise RuntimeError("AUTHORIZATION_INVALID")

        expires_at = payload["expires_at_epoch"]
        if isinstance(expires_at, bool) or not isinstance(expires_at, int):
            raise RuntimeError("AUTHORIZATION_INVALID")
        now = int(self._now())
        if expires_at <= now:
            raise RuntimeError("AUTHORIZATION_EXPIRED")
        if expires_at - now > _MAX_PERMIT_LIFETIME_SECONDS:
            raise RuntimeError("AUTHORIZATION_INVALID")

        boot_id = payload["boot_id_sha256"]
        pid = payload["pid"]
        start_ticks = payload["process_start_ticks"]
        if not isinstance(boot_id, str) or _SHA256_RE.fullmatch(boot_id) is None:
            raise RuntimeError("AUTHORIZATION_INVALID")
        if isinstance(pid, bool) or not isinstance(pid, int) or pid < 2:
            raise RuntimeError("AUTHORIZATION_INVALID")
        if isinstance(start_ticks, bool) or not isinstance(start_ticks, int) or start_ticks <= 0:
            raise RuntimeError("AUTHORIZATION_INVALID")

        fence = current_client_fence()
        if (
            payload["client_version"] != fence.version
            or payload["client_size"] != fence.size
            or payload["client_sha256"] != fence.sha256
        ):
            raise RuntimeError("AUTHORIZATION_CURRENT_CLIENT_MISMATCH")

        return NativeLoginPermit(
            expires_at_epoch=expires_at,
            boot_id_sha256=boot_id,
            pid=pid,
            process_start_ticks=start_ticks,
            client_version=fence.version,
            client_size=fence.size,
            client_sha256=fence.sha256,
        )


def _no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate key")
        result[key] = value
    return result


def _validate_operation_id(operation_id: Any) -> str:
    if not isinstance(operation_id, str) or _SAFE_OPERATION_ID.fullmatch(operation_id) is None:
        raise RuntimeError("OPERATION_ID_INVALID")
    return operation_id


LoginRunner = Callable[[str, NativeLoginPermit, threading.Event], str]


class NativeLoginRuntimeSupervisor:
    """One-session local runtime coordinator behind an exact Unix-socket protocol."""

    def __init__(
        self,
        *,
        socket_path: str | Path,
        permit_store_path: str | Path,
        login_runner: LoginRunner,
    ) -> None:
        self.socket_path = Path(socket_path)
        self.permit_store_path = Path(permit_store_path)
        if not callable(login_runner):
            raise TypeError("login_runner must be callable")
        self._login_runner = login_runner
        self._lock = threading.RLock()
        self._state = "READY"
        self._reason = "NATIVE_LOGIN_READY"
        self._operation_id: str | None = None
        self._cancelled: threading.Event | None = None
        self._worker: threading.Thread | None = None
        self._effect_observed = False
        self._closed = threading.Event()
        self._server: socket.socket | None = None

    def handle(self, request: Any) -> dict[str, object]:
        parsed = self._validate_request(request)
        if parsed is None:
            return self._reply(
                state="ERROR",
                reason="NATIVE_LOGIN_PROTOCOL_INVALID",
                physical_effect=False,
            )
        command, operation_id = parsed
        if command == "STATUS":
            with self._lock:
                return self._reply(
                    state=self._state,
                    reason=self._reason,
                    physical_effect=self._effect_observed,
                )
        if command == "START":
            assert operation_id is not None
            return self._start(operation_id)
        assert command == "STOP" and operation_id is not None
        return self._stop(operation_id)

    @staticmethod
    def _validate_request(request: Any) -> tuple[str, str | None] | None:
        if not isinstance(request, dict):
            return None
        version = request.get("version")
        command = request.get("command")
        if isinstance(version, bool) or version != _PROTOCOL_VERSION or not isinstance(command, str):
            return None
        if command == "STATUS":
            if set(request) != {"version", "command"}:
                return None
            return command, None
        if command not in {"START", "STOP"} or set(request) != {"version", "command", "operation_id"}:
            return None
        try:
            operation_id = _validate_operation_id(request["operation_id"])
        except RuntimeError:
            return None
        return command, operation_id

    def _start(self, operation_id: str) -> dict[str, object]:
        with self._lock:
            if self._state in _ACTIVE_STATES or self._worker is not None:
                return self._reply(
                    state=self._state,
                    reason="NATIVE_LOGIN_SESSION_ALREADY_ACTIVE",
                    operation_id=operation_id,
                    physical_effect=False,
                )
            self._state = "STARTING"
            self._reason = "NATIVE_LOGIN_STARTING"
            self._operation_id = operation_id
            self._cancelled = threading.Event()
            self._effect_observed = False

        try:
            permit = NativeLoginPermitStore(self.permit_store_path).consume(operation_id)
        except RuntimeError as exc:
            code = str(exc)
            reason = {
                "AUTHORIZATION_REQUIRED": "NATIVE_LOGIN_AUTHORIZATION_REQUIRED",
                "AUTHORIZATION_EXPIRED": "NATIVE_LOGIN_AUTHORIZATION_EXPIRED",
                "AUTHORIZATION_CURRENT_CLIENT_MISMATCH": "NATIVE_LOGIN_CURRENT_CLIENT_MISMATCH",
            }.get(code, "NATIVE_LOGIN_AUTHORIZATION_INVALID")
            with self._lock:
                self._state = "BLOCKED"
                self._reason = reason
                self._operation_id = None
                self._cancelled = None
                self._worker = None
            return self._reply(
                state="BLOCKED",
                reason=reason,
                operation_id=operation_id,
                physical_effect=False,
            )

        with self._lock:
            cancelled = self._cancelled
            if cancelled is None:
                self._state = "BLOCKED"
                self._reason = "NATIVE_LOGIN_RUNTIME_FAILED"
                return self._reply(
                    state=self._state,
                    reason=self._reason,
                    operation_id=operation_id,
                    physical_effect=False,
                )
            worker = threading.Thread(
                target=self._run_login,
                args=(operation_id, permit, cancelled),
                name="native-login-runtime",
                daemon=True,
            )
            self._worker = worker
            worker.start()
            return self._reply(
                state="STARTING",
                reason="NATIVE_LOGIN_STARTING",
                operation_id=operation_id,
                physical_effect=False,
            )

    def _run_login(
        self,
        operation_id: str,
        permit: NativeLoginPermit,
        cancelled: threading.Event,
    ) -> None:
        try:
            with self._lock:
                if self._operation_id != operation_id:
                    return
                self._effect_observed = True
            outcome = self._login_runner(operation_id, permit, cancelled)
        except Exception:
            outcome = "FAILED"

        mapping = {
            "IN_GAME": ("IN_GAME", "NATIVE_LOGIN_IN_GAME"),
            "STOPPED": ("STOPPED", "NATIVE_LOGIN_STOPPED"),
            "EXTERNAL_ACTION_REQUIRED": ("BLOCKED", "NATIVE_LOGIN_EXTERNAL_ACTION_REQUIRED"),
            "CHALLENGE_REQUIRED": ("BLOCKED", "NATIVE_LOGIN_EXTERNAL_ACTION_REQUIRED"),
            "FAILED": ("BLOCKED", "NATIVE_LOGIN_RUNTIME_FAILED"),
        }
        state, reason = mapping.get(outcome, ("BLOCKED", "NATIVE_LOGIN_RUNTIME_FAILED"))
        with self._lock:
            if self._operation_id != operation_id:
                return
            self._state = state
            self._reason = reason
            self._worker = None
            self._cancelled = None

    def _stop(self, operation_id: str) -> dict[str, object]:
        with self._lock:
            if self._operation_id is None:
                return self._reply(
                    state=self._state,
                    reason="NATIVE_LOGIN_NO_ACTIVE_SESSION",
                    operation_id=operation_id,
                    physical_effect=False,
                )
            if self._operation_id != operation_id:
                return self._reply(
                    state=self._state,
                    reason="NATIVE_LOGIN_OPERATION_MISMATCH",
                    operation_id=operation_id,
                    physical_effect=False,
                )
            if self._cancelled is None or self._worker is None:
                return self._reply(
                    state=self._state,
                    reason=self._reason,
                    operation_id=operation_id,
                    physical_effect=False,
                )
            self._cancelled.set()
            self._state = "STOPPING"
            self._reason = "NATIVE_LOGIN_STOP_REQUESTED"
            return self._reply(
                state="STOPPING",
                reason="NATIVE_LOGIN_STOP_REQUESTED",
                operation_id=operation_id,
                physical_effect=False,
            )

    def _reply(
        self,
        *,
        state: str,
        reason: str,
        physical_effect: bool,
        operation_id: str | None = None,
    ) -> dict[str, object]:
        reply: dict[str, object] = {
            "version": _PROTOCOL_VERSION,
            "state": state,
            "bound": True,
            "current": True,
            "physical_effect": physical_effect,
            "reason": reason,
        }
        if operation_id is not None:
            reply["operation_id"] = operation_id
        return reply

    def serve_forever(self) -> None:
        if not self.socket_path.is_absolute():
            raise RuntimeError("SOCKET_PATH_INVALID")
        self.socket_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.lstat(self.socket_path)
        except FileNotFoundError:
            pass
        else:
            raise RuntimeError("SOCKET_PATH_ALREADY_EXISTS")

        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._server = server
        try:
            server.bind(str(self.socket_path))
            os.chmod(self.socket_path, 0o600)
            server.listen(4)
            server.settimeout(0.2)
            while not self._closed.is_set():
                try:
                    client, _ = server.accept()
                except TimeoutError:
                    continue
                except OSError:
                    if self._closed.is_set():
                        break
                    raise
                with client:
                    self._serve_client(client)
        finally:
            try:
                server.close()
            finally:
                self._server = None
                try:
                    info = os.lstat(self.socket_path)
                    if stat.S_ISSOCK(info.st_mode):
                        self.socket_path.unlink()
                except FileNotFoundError:
                    pass

    def _serve_client(self, client: socket.socket) -> None:
        if hasattr(socket, "SO_PEERCRED"):
            try:
                peer = client.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, 12)
                peer_uid = int.from_bytes(peer[4:8], byteorder="little", signed=True)
            except OSError:
                return
            if peer_uid != os.geteuid():
                return
        client.settimeout(2.0)
        raw = bytearray()
        try:
            while b"\n" not in raw:
                chunk = client.recv(min(4096, _MAX_FRAME_BYTES + 1 - len(raw)))
                if not chunk:
                    return
                raw.extend(chunk)
                if len(raw) > _MAX_FRAME_BYTES:
                    raise ValueError("frame too large")
            frame, trailing = bytes(raw).split(b"\n", 1)
            if trailing:
                raise ValueError("trailing data")
            request = json.loads(frame.decode("utf-8"), object_pairs_hook=_no_duplicate_keys)
            reply = self.handle(request)
        except (UnicodeError, json.JSONDecodeError, ValueError):
            reply = self._reply(
                state="ERROR",
                reason="NATIVE_LOGIN_PROTOCOL_INVALID",
                physical_effect=False,
            )
        encoded = json.dumps(reply, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii") + b"\n"
        try:
            client.sendall(encoded)
        except OSError:
            return

    def close(self) -> None:
        self._closed.set()
        server = self._server
        if server is not None:
            try:
                server.close()
            except OSError:
                pass


__all__ = (
    "NativeLoginPermit",
    "NativeLoginPermitStore",
    "NativeLoginRuntimeSupervisor",
)
