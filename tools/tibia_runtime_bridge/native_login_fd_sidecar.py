#!/usr/bin/env python3
"""Ephemeral sealed-FD sidecar for the trusted-main native-login IPC relay."""
from __future__ import annotations

import argparse
import array
import fcntl
import importlib.util
import json
import os
from pathlib import Path
import signal
import socket
import stat
from typing import Any, Sequence

SECRET_VAULT_MODULE = Path("/tmp/secret_vault.py")
VAULT_DIR = Path("/vault")
RELAY_ROOT = Path("/relay-shm")
RELAY_PREFIX = "otclient-native-login-relay-"
RELAY_PROBE_COMMAND = b"relay-probe\n"
RELAY_AUTH_COMMAND = b"relay-auth-fd\n"
REQUIRED_SEALS = fcntl.F_SEAL_WRITE | fcntl.F_SEAL_GROW | fcntl.F_SEAL_SHRINK | fcntl.F_SEAL_SEAL
_MAX_RESPONSE_BYTES = 1024 * 1024


class SidecarError(RuntimeError):
    pass


def _emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")), flush=True)


def _sealed_probe_fd() -> int:
    flags = getattr(os, "MFD_CLOEXEC", 0) | getattr(os, "MFD_ALLOW_SEALING", 0)
    fd = os.memfd_create("otclient-native-login-sidecar-probe", flags)
    try:
        os.write(fd, b"probe")
        os.lseek(fd, 0, os.SEEK_SET)
        fcntl.fcntl(fd, fcntl.F_ADD_SEALS, REQUIRED_SEALS)
        return fd
    except BaseException:
        os.close(fd)
        raise


def _validate_sealed_fd(fd: int) -> None:
    st = os.fstat(fd)
    if not stat.S_ISREG(st.st_mode):
        raise SidecarError("sealed_fd_not_regular")
    target = os.readlink(f"/proc/self/fd/{fd}")
    if not (target.startswith("/memfd:") or target.startswith("memfd:")):
        raise SidecarError("sealed_fd_not_memfd")
    seals = fcntl.fcntl(fd, fcntl.F_GET_SEALS)
    if seals & REQUIRED_SEALS != REQUIRED_SEALS:
        raise SidecarError("sealed_fd_incomplete")


def _relay_path(path: Path) -> Path:
    if not path.is_absolute() or path.parent != RELAY_ROOT:
        raise SidecarError("relay_socket_outside_shared_mount")
    if not path.name.startswith(RELAY_PREFIX):
        raise SidecarError("relay_socket_namespace_invalid")
    return path


def _receive_json(sock: socket.socket) -> dict[str, Any]:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        if total > _MAX_RESPONSE_BYTES:
            raise SidecarError("relay_response_too_large")
        if b"\n" in chunk:
            break
    if not chunks:
        raise SidecarError("relay_response_missing")
    line = b"".join(chunks).split(b"\n", 1)[0]
    try:
        response = json.loads(line.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SidecarError("relay_response_invalid") from exc
    if not isinstance(response, dict) or not isinstance(response.get("ok"), bool):
        raise SidecarError("relay_response_invalid")
    return response


def _relay_fd(relay_socket: Path, command: bytes, fd: int, timeout: float) -> dict[str, Any]:
    path = _relay_path(relay_socket)
    if b"\n" not in command or command.count(b"\n") != 1 or not command.endswith(b"\n"):
        raise SidecarError("relay_command_invalid")
    descriptors = array.array("i", [fd])
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect(str(path))
        sent = sock.sendmsg(
            [command],
            [(socket.SOL_SOCKET, socket.SCM_RIGHTS, descriptors.tobytes())],
        )
        if sent != len(command):
            raise SidecarError("relay_descriptor_send_partial")
        return _receive_json(sock)
    except (OSError, ConnectionError, socket.timeout) as exc:
        raise SidecarError("relay_transport_failed") from exc
    finally:
        sock.close()


def _probe(args: argparse.Namespace) -> int:
    fd = -1
    try:
        fd = _sealed_probe_fd()
        _validate_sealed_fd(fd)
        response = _relay_fd(args.relay_socket, RELAY_PROBE_COMMAND, fd, args.timeout)
        if response != {"ok": True, "sealed_fd_preserved": True, "target_mount_visible": True}:
            raise SidecarError("probe_response_invalid")
        _emit(response)
        return 0
    finally:
        if fd >= 0:
            os.close(fd)


def _load_secret_vault() -> Any:
    if not SECRET_VAULT_MODULE.is_file() or SECRET_VAULT_MODULE.is_symlink():
        raise SidecarError("secret_vault_module_unavailable")
    spec = importlib.util.spec_from_file_location("native_login_sidecar_secret_vault", SECRET_VAULT_MODULE)
    if spec is None or spec.loader is None:
        raise SidecarError("secret_vault_module_unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _auth(args: argparse.Namespace) -> int:
    fd = -1
    try:
        vault = _load_secret_vault()
        try:
            fd = vault.decrypt_to_sealed_memfd(VAULT_DIR)
        except Exception as exc:
            raise SidecarError("machine_local_vault_decrypt_failed") from exc
        _validate_sealed_fd(fd)
        response = _relay_fd(args.relay_socket, RELAY_AUTH_COMMAND, fd, args.timeout)
        if response.get("ok") is True:
            if response.get("invocation_dispatched") is not True:
                raise SidecarError("auth_dispatch_not_proven")
            _emit(response)
            return 0
        if not (
            response.get("fd_sent") is True
            and response.get("error") == "AUTH_RESPONSE_UNAVAILABLE_AFTER_SEND"
        ):
            raise SidecarError("auth_fd_send_not_proven")
        _emit({"ok": False, "fd_sent": True, "error": "AUTH_RESPONSE_UNAVAILABLE_AFTER_SEND"})
        return 79
    finally:
        if fd >= 0:
            os.close(fd)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation", required=True)
    probe = sub.add_parser("probe")
    probe.add_argument("--relay-socket", required=True, type=Path)
    probe.add_argument("--timeout", type=float, default=12.0)
    auth = sub.add_parser("auth")
    auth.add_argument("--relay-socket", required=True, type=Path)
    auth.add_argument("--timeout", type=float, default=15.0)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    signal.alarm(40)
    args = _parser().parse_args(argv)
    try:
        return _probe(args) if args.operation == "probe" else _auth(args)
    except (SidecarError, OSError, ValueError):
        _emit({"ok": False, "error": "SIDECAR_FAIL_CLOSED"})
        return 2
    finally:
        signal.alarm(0)


if __name__ == "__main__":
    raise SystemExit(main())
