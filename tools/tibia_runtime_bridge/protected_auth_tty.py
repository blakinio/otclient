from __future__ import annotations

import argparse
import ctypes
import json
import os
from pathlib import Path
import resource
import stat
import struct
import sys
import termios

try:
    import fcntl as _fcntl
except ImportError:  # pragma: no cover - Linux-only Track A helper
    _fcntl = None

from tools.tibia_runtime_bridge.experimental_auth_client import auth_with_credentials_fd
from tools.tibia_runtime_bridge.ipc_client import BridgeClientError, PeerIdentityExpectation

EXACT_CLIENT_VERSION = "15.32.df7b29"
EXACT_CLIENT_SIZE = 51965216
EXACT_CLIENT_SHA256 = "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"
MAX_SECRET_BYTES = 1024
_SECRET_BUFFER_BYTES = MAX_SECRET_BYTES + 2
_MAX_IDENTITY_JSON_BYTES = 4096
_PR_SET_DUMPABLE = 4
_LEGACY_SECRET_ENV = ("TIBIA_TEST_EMAIL", "TIBIA_TEST_PASSWORD")

_libc = ctypes.CDLL(None, use_errno=True)
_libc.mlock.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
_libc.mlock.restype = ctypes.c_int
_libc.munlock.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
_libc.munlock.restype = ctypes.c_int
if hasattr(_libc, "prctl"):
    _libc.prctl.argtypes = [ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong]
    _libc.prctl.restype = ctypes.c_int


class ProtectedSecretBuffer:
    """Small mutable secret buffer whose pages are locked for its lifetime."""

    def __init__(self, capacity: int = _SECRET_BUFFER_BYTES) -> None:
        if capacity <= MAX_SECRET_BYTES:
            raise BridgeClientError("protected secret buffer capacity is too small")
        self.storage = bytearray(capacity)
        self.length = 0
        self._address = ctypes.addressof(ctypes.c_char.from_buffer(self.storage))
        if _libc.mlock(ctypes.c_void_p(self._address), ctypes.c_size_t(len(self.storage))) != 0:
            err = ctypes.get_errno()
            self.wipe()
            raise BridgeClientError(f"mlock failed for protected secret buffer: errno={err}")
        self._locked = True

    def view(self) -> memoryview:
        return memoryview(self.storage)[: self.length]

    def wipe(self) -> None:
        if self.storage:
            ctypes.memset(ctypes.c_void_p(self._address), 0, len(self.storage))
        self.length = 0

    def close(self) -> None:
        self.wipe()
        if getattr(self, "_locked", False):
            _libc.munlock(ctypes.c_void_p(self._address), ctypes.c_size_t(len(self.storage)))
            self._locked = False

    def __enter__(self) -> "ProtectedSecretBuffer":
        return self

    def __exit__(self, _exc_type, _exc, _tb) -> None:
        self.close()


def _reject_legacy_secret_environment() -> None:
    if any(name in os.environ for name in _LEGACY_SECRET_ENV):
        raise BridgeClientError("credential-bearing environment variables are forbidden")


def _harden_secret_process() -> None:
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    if not hasattr(_libc, "prctl"):
        raise BridgeClientError("PR_SET_DUMPABLE is unavailable")
    if _libc.prctl(_PR_SET_DUMPABLE, 0, 0, 0, 0) != 0:
        err = ctypes.get_errno()
        raise BridgeClientError(f"PR_SET_DUMPABLE failed: errno={err}")


def _copy_termios(attrs: list[object]) -> list[object]:
    copied = list(attrs)
    copied[6] = list(attrs[6])
    return copied


def _drain_line(tty_fd: int) -> None:
    scratch = bytearray(256)
    try:
        while True:
            count = os.readv(tty_fd, [scratch])
            if count <= 0 or b"\n" in memoryview(scratch)[:count] or b"\r" in memoryview(scratch)[:count]:
                break
    finally:
        ctypes.memset(ctypes.addressof(ctypes.c_char.from_buffer(scratch)), 0, len(scratch))


def read_hidden_tty_line(tty_fd: int, prompt: bytes, target: ProtectedSecretBuffer) -> None:
    if not os.isatty(tty_fd):
        raise BridgeClientError("EXTERNAL_INTERACTIVE_TTY_REQUIRED")
    if not prompt or b"\n" in prompt or b"\r" in prompt:
        raise BridgeClientError("TTY prompt must be one static line fragment")

    original = termios.tcgetattr(tty_fd)
    hidden = _copy_termios(original)
    hidden[3] &= ~(termios.ECHO | termios.ECHONL)
    target.wipe()
    termios.tcsetattr(tty_fd, termios.TCSAFLUSH, hidden)
    try:
        os.write(tty_fd, prompt)
        count = os.readv(tty_fd, [target.storage])
        if count <= 0:
            raise BridgeClientError("protected TTY input returned no data")

        end = count
        while end > 0 and target.storage[end - 1] in (10, 13):
            end -= 1
        if end > MAX_SECRET_BYTES:
            if count == len(target.storage) and 10 not in target.storage[:count] and 13 not in target.storage[:count]:
                _drain_line(tty_fd)
            raise BridgeClientError("protected TTY input exceeds 1024 bytes")
        if end == 0:
            raise BridgeClientError("protected TTY input must be non-empty")
        if 0 in target.storage[:end]:
            raise BridgeClientError("NUL is forbidden in protected TTY input")
        target.length = end
    finally:
        try:
            os.write(tty_fd, b"\n")
        finally:
            termios.tcsetattr(tty_fd, termios.TCSAFLUSH, original)


def _required_memfd_seals() -> int:
    if _fcntl is None:
        raise BridgeClientError("memfd sealing support is unavailable")
    names = ("F_ADD_SEALS", "F_GET_SEALS", "F_SEAL_SEAL", "F_SEAL_SHRINK", "F_SEAL_GROW", "F_SEAL_WRITE")
    if any(not hasattr(_fcntl, name) for name in names):
        raise BridgeClientError("memfd sealing support is unavailable")
    return _fcntl.F_SEAL_SEAL | _fcntl.F_SEAL_SHRINK | _fcntl.F_SEAL_GROW | _fcntl.F_SEAL_WRITE


def create_sealed_credential_memfd(email: ProtectedSecretBuffer, password: ProtectedSecretBuffer) -> int:
    if not hasattr(os, "memfd_create") or not hasattr(os, "MFD_ALLOW_SEALING"):
        raise BridgeClientError("memfd_create with sealing is unavailable")
    if not (1 <= email.length <= MAX_SECRET_BYTES and 1 <= password.length <= MAX_SECRET_BYTES):
        raise BridgeClientError("credential buffer lengths are invalid")

    flags = getattr(os, "MFD_CLOEXEC", 0) | os.MFD_ALLOW_SEALING
    fd = os.memfd_create("otclient-tibia-native-auth", flags)
    try:
        header = struct.pack("<II", email.length, password.length)
        expected = len(header) + email.length + password.length
        written = os.writev(fd, [header, email.view(), password.view()])
        if written != expected or os.fstat(fd).st_size != expected:
            raise BridgeClientError("credential memfd frame write was incomplete")
        required = _required_memfd_seals()
        _fcntl.fcntl(fd, _fcntl.F_ADD_SEALS, required)
        actual = _fcntl.fcntl(fd, _fcntl.F_GET_SEALS)
        if actual & required != required:
            raise BridgeClientError("credential memfd seals did not apply")
        os.lseek(fd, 0, os.SEEK_SET)
        return fd
    except Exception:
        os.close(fd)
        raise


def _lower_sha256(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(ch in "0123456789abcdef" for ch in value)


def _identity_stat_key(metadata: os.stat_result) -> tuple[int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def load_exact_runtime_identity(path: Path) -> PeerIdentityExpectation:
    if not path.is_absolute():
        raise BridgeClientError("runtime identity path must be absolute")
    if not hasattr(os, "O_NOFOLLOW"):
        raise BridgeClientError("O_NOFOLLOW is unavailable for runtime identity")

    flags = os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise BridgeClientError(f"runtime identity open failed: {exc}") from exc
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode):
            raise BridgeClientError("runtime identity must be a regular file")
        if before.st_uid != os.geteuid():
            raise BridgeClientError("runtime identity must be owned by the current effective user")
        if before.st_mode & 0o022:
            raise BridgeClientError("runtime identity must not be group/world writable")
        if before.st_size <= 0 or before.st_size > _MAX_IDENTITY_JSON_BYTES:
            raise BridgeClientError("runtime identity JSON size is invalid")

        raw = bytearray()
        while len(raw) < before.st_size:
            chunk = os.read(fd, min(1024, before.st_size - len(raw)))
            if not chunk:
                break
            raw.extend(chunk)
        after = os.fstat(fd)
        if len(raw) != before.st_size or _identity_stat_key(before) != _identity_stat_key(after):
            raise BridgeClientError("runtime identity changed during read")
        try:
            doc = json.loads(raw.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise BridgeClientError(f"runtime identity JSON is invalid: {exc}") from exc
        finally:
            raw.clear()
    finally:
        os.close(fd)

    if not isinstance(doc, dict):
        raise BridgeClientError("runtime identity JSON must be an object")
    if doc.get("client_version") != EXACT_CLIENT_VERSION:
        raise BridgeClientError("runtime identity client version mismatch")
    if doc.get("client_size") != EXACT_CLIENT_SIZE:
        raise BridgeClientError("runtime identity client size mismatch")
    if doc.get("client_sha256") != EXACT_CLIENT_SHA256:
        raise BridgeClientError("runtime identity client SHA-256 mismatch")

    boot_id_sha256 = doc.get("boot_id_sha256")
    pid = doc.get("pid")
    process_start_ticks = doc.get("process_start_ticks")
    if not _lower_sha256(boot_id_sha256):
        raise BridgeClientError("runtime identity boot hash is invalid")
    if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 0:
        raise BridgeClientError("runtime identity PID is invalid")
    if not isinstance(process_start_ticks, int) or isinstance(process_start_ticks, bool) or process_start_ticks <= 0:
        raise BridgeClientError("runtime identity process start ticks are invalid")

    return PeerIdentityExpectation(
        boot_id_sha256=boot_id_sha256,
        pid=pid,
        process_start_ticks=process_start_ticks,
        client_version=EXACT_CLIENT_VERSION,
        client_size=EXACT_CLIENT_SIZE,
        client_sha256=EXACT_CLIENT_SHA256,
    )


def sanitize_auth_response(response: dict[str, object]) -> dict[str, object]:
    sanitized: dict[str, object] = {"ok": response.get("ok") is True}
    for key in ("command", "invocation_dispatched", "qmeta_method_id", "error"):
        value = response.get(key)
        if isinstance(value, (str, bool, int)) and not isinstance(value, float):
            sanitized[key] = value
    return sanitized


def _open_controlling_tty() -> int:
    flags = os.O_RDWR | getattr(os, "O_NOCTTY", 0) | getattr(os, "O_CLOEXEC", 0)
    try:
        return os.open("/dev/tty", flags)
    except OSError as exc:
        raise BridgeClientError("EXTERNAL_INTERACTIVE_TTY_REQUIRED") from exc


def run_interactive_auth(socket_path: Path, identity_path: Path) -> dict[str, object]:
    _reject_legacy_secret_environment()
    _harden_secret_process()
    identity = load_exact_runtime_identity(identity_path)
    if not socket_path.is_absolute():
        raise BridgeClientError("experimental auth socket path must be absolute")

    tty_fd = _open_controlling_tty()
    credentials_fd = -1
    try:
        with ProtectedSecretBuffer() as account, ProtectedSecretBuffer() as password:
            read_hidden_tty_line(tty_fd, b"Tibia account identifier (hidden): ", account)
            read_hidden_tty_line(tty_fd, b"Tibia password (hidden): ", password)
            credentials_fd = create_sealed_credential_memfd(account, password)
            response = auth_with_credentials_fd(
                socket_path,
                credentials_fd,
                expected_identity=identity,
            )
            return sanitize_auth_response(response)
    finally:
        if credentials_fd >= 0:
            os.close(credentials_fd)
        os.close(tty_fd)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Protected controlling-TTY source for the one-shot native Tibia auth helper"
    )
    parser.add_argument("--socket", required=True, type=Path)
    parser.add_argument("--identity-json", required=True, type=Path)
    args = parser.parse_args(argv)

    result = run_interactive_auth(args.socket, args.identity_json)
    json.dump(result, sys.stdout, sort_keys=True)
    sys.stdout.write("\n")
    return 0 if result.get("ok") else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BridgeClientError as exc:
        print(f"protected auth TTY error: {exc}", file=sys.stderr)
        raise SystemExit(2)
