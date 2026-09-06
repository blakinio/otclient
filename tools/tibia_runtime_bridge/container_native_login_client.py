from __future__ import annotations

"""Container-namespace native-login client using an inherited sealed memfd only."""

import argparse
import array
import fcntl
import hashlib
import json
import os
from pathlib import Path
import socket
import stat
import struct
import sys
from typing import Any

EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52105824
EXPECTED_SHA = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"
_MIN_CREDENTIAL_FRAME_BYTES = 10
_MAX_CREDENTIAL_FRAME_BYTES = 8 + 2 * 1024
_MAX_RESPONSE_BYTES = 1024 * 1024
_PEERCRED = struct.Struct("3i")


class ClientError(RuntimeError):
    pass


class PeerIdentityExpectation:
    def __init__(
        self,
        *,
        boot_id_sha256: str,
        pid: int,
        process_start_ticks: int,
        client_version: str,
        client_size: int,
        client_sha256: str,
    ) -> None:
        self.boot_id_sha256 = boot_id_sha256
        self.pid = pid
        self.process_start_ticks = process_start_ticks
        self.client_version = client_version
        self.client_size = client_size
        self.client_sha256 = client_sha256


def _hex64(value: str, label: str) -> str:
    lowered = value.lower()
    if len(lowered) != 64 or any(ch not in "0123456789abcdef" for ch in lowered):
        raise ClientError(f"{label} must be lowercase SHA-256 hex")
    return lowered


def _identity(args: argparse.Namespace) -> PeerIdentityExpectation:
    if args.pid < 2 or args.start_ticks < 1:
        raise ClientError("runtime identity numeric fields are invalid")
    if args.client_version != EXPECTED_VERSION or args.client_size != EXPECTED_SIZE:
        raise ClientError("runtime identity is not exact-current be4f48")
    if _hex64(args.client_sha256, "client digest") != EXPECTED_SHA:
        raise ClientError("runtime identity digest is not exact-current be4f48")
    return PeerIdentityExpectation(
        boot_id_sha256=_hex64(args.boot_id_sha256, "boot identity"),
        pid=args.pid,
        process_start_ticks=args.start_ticks,
        client_version=args.client_version,
        client_size=args.client_size,
        client_sha256=args.client_sha256,
    )


def _drop_to(uid: int, gid: int) -> None:
    if uid < 1 or gid < 1:
        raise ClientError("drop uid/gid must be positive")
    if os.geteuid() != 0:
        raise ClientError("namespace credential bridge must start as root")
    os.setgroups([])
    os.setgid(gid)
    os.setuid(uid)
    if os.geteuid() != uid or os.getegid() != gid:
        raise ClientError("namespace credential bridge privilege drop failed")


def _process_start_ticks(pid: int) -> int:
    try:
        raw = Path(f"/proc/{pid}/stat").read_text(encoding="ascii")
    except OSError as exc:
        raise ClientError("peer process stat unavailable") from exc
    close = raw.rfind(")")
    fields = raw[close + 2 :].split()
    if close < 0 or len(fields) < 20:
        raise ClientError("peer process stat malformed")
    return int(fields[19])


def _boot_id_sha256() -> str:
    try:
        raw = Path("/proc/sys/kernel/random/boot_id").read_bytes()
    except OSError as exc:
        raise ClientError("peer boot identity unavailable") from exc
    return hashlib.sha256(raw).hexdigest()


def _sha256_fd(fd: int) -> str:
    digest = hashlib.sha256()
    os.lseek(fd, 0, os.SEEK_SET)
    while True:
        block = os.read(fd, 1024 * 1024)
        if not block:
            return digest.hexdigest()
        digest.update(block)


def _verify_peer(sock: socket.socket, expected: PeerIdentityExpectation) -> None:
    try:
        raw = sock.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, _PEERCRED.size)
        peer_pid, _uid, _gid = _PEERCRED.unpack(raw)
    except OSError as exc:
        raise ClientError("SO_PEERCRED verification failed") from exc
    if peer_pid != expected.pid:
        raise ClientError("Unix peer PID does not match admitted runtime")
    if _boot_id_sha256() != expected.boot_id_sha256:
        raise ClientError("runtime boot identity changed")
    if _process_start_ticks(peer_pid) != expected.process_start_ticks:
        raise ClientError("runtime process start identity changed")
    try:
        fd = os.open(f"/proc/{peer_pid}/exe", os.O_RDONLY | os.O_CLOEXEC)
    except OSError as exc:
        raise ClientError("peer executable unavailable") from exc
    try:
        st = os.fstat(fd)
        if st.st_size != expected.client_size or _sha256_fd(fd) != expected.client_sha256:
            raise ClientError("peer executable exact-current fence failed")
    finally:
        os.close(fd)


def _validate_credentials_memfd(credentials_fd: int) -> None:
    if credentials_fd < 0:
        raise ClientError("credentials FD is invalid")
    try:
        st = os.fstat(credentials_fd)
        target = os.readlink(f"/proc/self/fd/{credentials_fd}")
        seals = fcntl.fcntl(credentials_fd, fcntl.F_GET_SEALS)
    except OSError as exc:
        raise ClientError("credentials FD validation failed") from exc
    if not stat.S_ISREG(st.st_mode):
        raise ClientError("credentials FD is not regular memfd storage")
    if not (_MIN_CREDENTIAL_FRAME_BYTES <= st.st_size <= _MAX_CREDENTIAL_FRAME_BYTES):
        raise ClientError("credentials FD frame size is invalid")
    if not (target.startswith("/memfd:") or target.startswith("memfd:")):
        raise ClientError("credentials FD is not anonymous memfd storage")
    required = fcntl.F_SEAL_SEAL | fcntl.F_SEAL_SHRINK | fcntl.F_SEAL_GROW | fcntl.F_SEAL_WRITE
    if seals & required != required:
        raise ClientError("credentials memfd is not fully sealed")


def _receive_json(sock: socket.socket, *, allow_post_send_eof: bool = False) -> dict[str, Any]:
    chunks: list[bytes] = []
    total = 0
    while True:
        try:
            chunk = sock.recv(4096)
        except (ConnectionError, socket.timeout):
            if allow_post_send_eof and not chunks:
                return {"ok": False, "error": "AUTH_RESPONSE_UNAVAILABLE_AFTER_SEND", "fd_sent": True}
            raise ClientError("helper response transport failed")
        if not chunk:
            if allow_post_send_eof and not chunks:
                return {"ok": False, "error": "AUTH_RESPONSE_UNAVAILABLE_AFTER_SEND", "fd_sent": True}
            break
        chunks.append(chunk)
        total += len(chunk)
        if total > _MAX_RESPONSE_BYTES:
            raise ClientError("helper response exceeds bounded size")
        if b"\n" in chunk:
            break
    if not chunks:
        raise ClientError("helper returned no response")
    line = b"".join(chunks).split(b"\n", 1)[0]
    try:
        result = json.loads(line.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ClientError("helper returned invalid JSON") from exc
    if not isinstance(result, dict) or not isinstance(result.get("ok"), bool):
        raise ClientError("helper response shape is invalid")
    return result


def auth_with_credentials_fd(
    socket_path: Path,
    credentials_fd: int,
    expected_identity: PeerIdentityExpectation,
    timeout: float,
) -> dict[str, Any]:
    _validate_credentials_memfd(credentials_fd)
    payload = b"AUTH_WITH_CREDENTIALS\n"
    descriptors = array.array("i", [credentials_fd])
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect(str(socket_path))
        _verify_peer(sock, expected_identity)
        sent = sock.sendmsg(
            [payload],
            [(socket.SOL_SOCKET, socket.SCM_RIGHTS, descriptors.tobytes())],
        )
        if sent != len(payload):
            raise ClientError("credential descriptor command was partially sent")
        return _receive_json(sock, allow_post_send_eof=True)
    except OSError as exc:
        raise ClientError("native auth IPC failed") from exc
    finally:
        sock.close()


def request(
    socket_path: Path,
    command: str,
    expected_identity: PeerIdentityExpectation,
    timeout: float,
) -> dict[str, Any]:
    if not command or "\n" in command or "\r" in command:
        raise ClientError("character command is invalid")
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect(str(socket_path))
        _verify_peer(sock, expected_identity)
        sock.sendall(command.encode("ascii") + b"\n")
        return _receive_json(sock)
    except OSError as exc:
        raise ClientError("character IPC failed") from exc
    finally:
        sock.close()


def _sanitize_auth(result: dict[str, Any]) -> dict[str, Any]:
    allowed = ("ok", "command", "invocation_dispatched", "qmeta_method_id", "error", "fd_sent")
    return {key: result[key] for key in allowed if key in result}


def _sanitize_character(result: dict[str, Any], command: str) -> dict[str, Any]:
    allowed = (
        "ok", "character_count", "confirm_method_present", "character_index",
        "confirmation_dispatched", "error",
    )
    sanitized = {key: result[key] for key in allowed if key in result}
    if command == "STATE" and result.get("ok") is True:
        count = result.get("character_count")
        method_present = result.get("confirm_method_present")
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            raise ClientError("character helper returned invalid count")
        if not isinstance(method_present, bool):
            raise ClientError("character helper returned invalid confirmation capability")
    return sanitized


def _add_identity(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--socket", required=True, type=Path)
    parser.add_argument("--boot-id-sha256", required=True)
    parser.add_argument("--pid", required=True, type=int)
    parser.add_argument("--start-ticks", required=True, type=int)
    parser.add_argument("--client-version", required=True)
    parser.add_argument("--client-size", required=True, type=int)
    parser.add_argument("--client-sha256", required=True)
    parser.add_argument("--timeout", type=float, default=5.0)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation", required=True)
    auth = sub.add_parser("auth-fd")
    _add_identity(auth)
    auth.add_argument("--credentials-fd", required=True, type=int)
    auth.add_argument("--drop-uid", required=True, type=int)
    auth.add_argument("--drop-gid", required=True, type=int)
    for name in ("character-state", "confirm-unique"):
        command = sub.add_parser(name)
        _add_identity(command)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    identity = _identity(args)
    if args.operation == "auth-fd":
        _drop_to(args.drop_uid, args.drop_gid)
        result = _sanitize_auth(
            auth_with_credentials_fd(args.socket, args.credentials_fd, identity, args.timeout)
        )
        json.dump(result, sys.stdout, sort_keys=True, separators=(",", ":"))
        sys.stdout.write("\n")
        if result.get("ok") is True:
            return 0
        if result.get("fd_sent") is True and result.get("error") == "AUTH_RESPONSE_UNAVAILABLE_AFTER_SEND":
            return 79
        return 2

    command = "STATE" if args.operation == "character-state" else "CONFIRM_UNIQUE"
    result = _sanitize_character(request(args.socket, command, identity, args.timeout), command)
    json.dump(result, sys.stdout, sort_keys=True, separators=(",", ":"))
    sys.stdout.write("\n")
    return 0 if result.get("ok") is True else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ClientError, OSError, ValueError) as exc:
        print(f"container native login client error: {type(exc).__name__}", file=sys.stderr)
        raise SystemExit(2)
