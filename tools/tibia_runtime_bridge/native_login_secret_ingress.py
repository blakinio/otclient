from __future__ import annotations

"""One-shot Kasm-local credential ingress for exact-current native Tibia auth."""

import argparse
import ctypes
import fcntl
import importlib.util
import json
import os
from pathlib import Path
import resource
import struct
import sys
from typing import Any

EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52105824
EXPECTED_SHA = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"
EMAIL_ENV = "TIBIA_TEST_EMAIL"
PASSWORD_ENV = "TIBIA_TEST_PASSWORD"
_MAX_FIELD_BYTES = 1024
_HEADER = struct.Struct("<II")
_REQUIRED_SEALS = (
    fcntl.F_SEAL_SEAL | fcntl.F_SEAL_SHRINK | fcntl.F_SEAL_GROW | fcntl.F_SEAL_WRITE
)
_CLIENT_PATH = Path(__file__).with_name("container_native_login_client.py")


class IngressError(RuntimeError):
    pass


def _harden_process() -> None:
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    try:
        libc = ctypes.CDLL(None, use_errno=True)
        libc.prctl(4, 0, 0, 0, 0)  # PR_SET_DUMPABLE
    except (AttributeError, OSError):
        pass


def _load_client() -> Any:
    spec = importlib.util.spec_from_file_location("native_login_ingress_client", _CLIENT_PATH)
    if spec is None or spec.loader is None:
        raise IngressError("client_helper_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _credential_frame(email: str, password: str) -> bytearray:
    email_bytes = email.encode("utf-8")
    password_bytes = password.encode("utf-8")
    if not (1 <= len(email_bytes) <= _MAX_FIELD_BYTES):
        raise IngressError("credential_email_length_invalid")
    if not (1 <= len(password_bytes) <= _MAX_FIELD_BYTES):
        raise IngressError("credential_password_length_invalid")
    if b"\0" in email_bytes or b"\0" in password_bytes:
        raise IngressError("credential_nul_invalid")
    return bytearray(_HEADER.pack(len(email_bytes), len(password_bytes)) + email_bytes + password_bytes)


def _sealed_memfd(frame: bytearray) -> int:
    flags = getattr(os, "MFD_CLOEXEC", 0) | getattr(os, "MFD_ALLOW_SEALING", 0)
    fd = os.memfd_create("tibia-native-auth-credentials", flags)
    try:
        os.write(fd, frame)
        os.lseek(fd, 0, os.SEEK_SET)
        fcntl.fcntl(fd, fcntl.F_ADD_SEALS, _REQUIRED_SEALS)
        return fd
    except Exception:
        os.close(fd)
        raise


def _sanitize(result: dict[str, Any]) -> dict[str, Any]:
    allowed = ("ok", "command", "invocation_dispatched", "qmeta_method_id", "error", "fd_sent")
    return {key: result[key] for key in allowed if key in result}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--socket", required=True, type=Path)
    parser.add_argument("--boot-id-sha256", required=True)
    parser.add_argument("--pid", required=True, type=int)
    parser.add_argument("--start-ticks", required=True, type=int)
    parser.add_argument("--client-version", required=True)
    parser.add_argument("--client-size", required=True, type=int)
    parser.add_argument("--client-sha256", required=True)
    parser.add_argument("--timeout", type=float, default=8.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if (
        args.client_version != EXPECTED_VERSION
        or args.client_size != EXPECTED_SIZE
        or args.client_sha256 != EXPECTED_SHA
    ):
        raise IngressError("exact_current_fence_failed")
    _harden_process()
    email = os.environ.pop(EMAIL_ENV, "")
    password = os.environ.pop(PASSWORD_ENV, "")
    if not email or not password:
        raise IngressError("credential_environment_missing")
    frame = _credential_frame(email, password)
    fd = -1
    try:
        # Drop the immutable string references as soon as the mutable frame exists.
        email = ""
        password = ""
        fd = _sealed_memfd(frame)
        client = _load_client()
        identity = client.PeerIdentityExpectation(
            boot_id_sha256=args.boot_id_sha256,
            pid=args.pid,
            process_start_ticks=args.start_ticks,
            client_version=args.client_version,
            client_size=args.client_size,
            client_sha256=args.client_sha256,
        )
        response = _sanitize(client.auth_with_credentials_fd(args.socket, fd, identity, args.timeout))
        json.dump(response, sys.stdout, sort_keys=True, separators=(",", ":"))
        sys.stdout.write("\n")
        sys.stdout.flush()
        if response.get("ok") is True:
            return 0
        if response.get("fd_sent") is True and response.get("error") == "AUTH_RESPONSE_UNAVAILABLE_AFTER_SEND":
            return 79
        return 2
    finally:
        for index in range(len(frame)):
            frame[index] = 0
        if fd >= 0:
            os.close(fd)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (IngressError, OSError, ValueError) as exc:
        print(f"native login secret ingress error: {type(exc).__name__}", file=sys.stderr)
        raise SystemExit(2)
