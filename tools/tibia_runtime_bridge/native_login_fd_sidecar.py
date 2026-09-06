#!/usr/bin/env python3
"""Ephemeral sealed-FD transport used by the trusted-main native-login executor."""
from __future__ import annotations

import argparse
import fcntl
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import stat
import subprocess
import sys
from typing import Any, Sequence

CLIENT_PATH = "/home/kasm-user/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client"
CONTAINER_CLIENT = "/tmp/otclient-native-login-current-sha/container_native_login_client.py"
AUTH_SOCKET = "/tmp/otclient-native-login-current-sha/auth.sock"
EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52105824
EXPECTED_SHA = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"
SECRET_VAULT_MODULE = Path("/tmp/secret_vault.py")
VAULT_DIR = Path("/vault")
REQUIRED_SEALS = fcntl.F_SEAL_WRITE | fcntl.F_SEAL_GROW | fcntl.F_SEAL_SHRINK | fcntl.F_SEAL_SEAL


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
    seals = fcntl.fcntl(fd, fcntl.F_GET_SEALS)
    if seals & REQUIRED_SEALS != REQUIRED_SEALS:
        raise SidecarError("sealed_fd_incomplete")


def _nsenter_prefix() -> list[str]:
    nsenter = shutil.which("nsenter")
    if not nsenter:
        raise SidecarError("nsenter_unavailable")
    if not Path("/proc/1/ns/mnt").exists() or not Path("/proc/1/root").exists():
        raise SidecarError("target_namespace_unavailable")
    return [
        nsenter,
        "--target", "1",
        "--mount",
        "--root=/proc/1/root",
        "--wd=/",
        "--",
    ]


def _run_target(command: Sequence[str], *, fd: int, timeout: int) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            [*_nsenter_prefix(), *command],
            check=False,
            text=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=timeout,
            close_fds=True,
            pass_fds=(fd,),
            env={"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "PYTHONDONTWRITEBYTECODE": "1"},
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise SidecarError("target_namespace_command_failed") from exc


def _probe() -> int:
    fd = -1
    try:
        fd = _sealed_probe_fd()
        _validate_sealed_fd(fd)
        inner = r'''
import fcntl,hashlib,json,os,stat,sys
fd=int(sys.argv[1]); path=sys.argv[2]; size=int(sys.argv[3]); digest=sys.argv[4]
required=fcntl.F_SEAL_WRITE|fcntl.F_SEAL_GROW|fcntl.F_SEAL_SHRINK|fcntl.F_SEAL_SEAL
st=os.fstat(fd)
if not stat.S_ISREG(st.st_mode) or fcntl.fcntl(fd,fcntl.F_GET_SEALS)&required!=required:
    raise SystemExit(2)
pst=os.stat(path)
if not stat.S_ISREG(pst.st_mode) or pst.st_size!=size:
    raise SystemExit(3)
h=hashlib.sha256()
with open(path,'rb',buffering=0) as f:
    for block in iter(lambda:f.read(1<<20),b''): h.update(block)
if h.hexdigest()!=digest:
    raise SystemExit(4)
print(json.dumps({'ok':True,'sealed_fd_preserved':True,'target_mount_visible':True},sort_keys=True,separators=(',',':')))
'''
        completed = _run_target(
            ["python3", "-c", inner, str(fd), CLIENT_PATH, str(EXPECTED_SIZE), EXPECTED_SHA],
            fd=fd,
            timeout=15,
        )
        if completed.returncode != 0 or not completed.stdout.strip():
            raise SidecarError("probe_target_validation_failed")
        try:
            response = json.loads(completed.stdout.strip().splitlines()[-1])
        except json.JSONDecodeError as exc:
            raise SidecarError("probe_response_invalid") from exc
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
        command = [
            "python3", CONTAINER_CLIENT, "auth-fd",
            "--socket", AUTH_SOCKET,
            "--boot-id-sha256", args.boot_id_sha256,
            "--pid", str(args.pid),
            "--start-ticks", str(args.start_ticks),
            "--client-version", EXPECTED_VERSION,
            "--client-size", str(EXPECTED_SIZE),
            "--client-sha256", EXPECTED_SHA,
            "--credentials-fd", str(fd),
            "--drop-uid", str(args.drop_uid),
            "--drop-gid", str(args.drop_gid),
            "--timeout", "8.0",
        ]
        completed = _run_target(command, fd=fd, timeout=15)
        if not completed.stdout.strip():
            raise SidecarError("auth_response_missing")
        try:
            response = json.loads(completed.stdout.strip().splitlines()[-1])
        except json.JSONDecodeError as exc:
            raise SidecarError("auth_response_invalid") from exc
        if completed.returncode == 0:
            if response.get("ok") is not True or response.get("invocation_dispatched") is not True:
                raise SidecarError("auth_dispatch_not_proven")
            _emit(response)
            return 0
        if not (
            completed.returncode == 79
            and response.get("fd_sent") is True
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
    sub.add_parser("probe")
    auth = sub.add_parser("auth")
    auth.add_argument("--boot-id-sha256", required=True)
    auth.add_argument("--pid", required=True, type=int)
    auth.add_argument("--start-ticks", required=True, type=int)
    auth.add_argument("--drop-uid", required=True, type=int)
    auth.add_argument("--drop-gid", required=True, type=int)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    signal.alarm(40)
    args = _parser().parse_args(argv)
    try:
        return _probe() if args.operation == "probe" else _auth(args)
    except (SidecarError, OSError, ValueError):
        _emit({"ok": False, "error": "SIDECAR_FAIL_CLOSED"})
        return 2
    finally:
        signal.alarm(0)


if __name__ == "__main__":
    raise SystemExit(main())
