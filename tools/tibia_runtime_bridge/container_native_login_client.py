from __future__ import annotations

"""Container-side native-login client with sealed-FD credential handoff only."""

import argparse
import json
import os
from pathlib import Path
import sys

from tools.tibia_runtime_bridge.experimental_auth_client import auth_with_credentials_fd
from tools.tibia_runtime_bridge.ipc_client import BridgeClientError, PeerIdentityExpectation, request
from tools.tibia_runtime_bridge.secret_vault import SecretVaultError, decrypt_to_sealed_memfd

_AUTH_ALLOWLIST = ("ok", "command", "invocation_dispatched", "qmeta_method_id")
_STATE_ALLOWLIST = ("ok", "character_count", "confirm_method_present", "error")
_CONFIRM_ALLOWLIST = ("ok", "character_index", "confirmation_dispatched", "error", "character_count")


def _hex64(value: str, label: str) -> str:
    lowered = value.lower()
    if len(lowered) != 64 or any(ch not in "0123456789abcdef" for ch in lowered):
        raise BridgeClientError(f"{label} must be lowercase SHA-256 hex")
    return lowered


def _identity(args: argparse.Namespace) -> PeerIdentityExpectation:
    if args.pid < 2 or args.start_ticks < 1 or args.client_size < 1:
        raise BridgeClientError("runtime identity numeric fields are invalid")
    return PeerIdentityExpectation(
        boot_id_sha256=_hex64(args.boot_id_sha256, "boot identity"),
        pid=args.pid,
        process_start_ticks=args.start_ticks,
        client_version=args.client_version,
        client_size=args.client_size,
        client_sha256=_hex64(args.client_sha256, "client digest"),
    )


def _drop_to(uid: int, gid: int) -> None:
    if uid < 1 or gid < 1:
        raise BridgeClientError("drop uid/gid must be positive")
    if os.geteuid() != 0:
        raise BridgeClientError("vault auth privilege drop must start as root")
    os.setgroups([])
    os.setgid(gid)
    os.setuid(uid)
    if os.geteuid() != uid or os.getegid() != gid:
        raise BridgeClientError("vault auth privilege drop did not take effect")


def run_auth(args: argparse.Namespace) -> dict[str, object]:
    identity = _identity(args)
    credentials_fd = -1
    try:
        credentials_fd = decrypt_to_sealed_memfd(Path(args.vault_dir))
        _drop_to(args.drop_uid, args.drop_gid)
        response = auth_with_credentials_fd(
            Path(args.socket),
            credentials_fd,
            timeout=args.timeout,
            expected_identity=identity,
        )
        return {key: response[key] for key in _AUTH_ALLOWLIST if key in response}
    except SecretVaultError as exc:
        raise BridgeClientError(f"machine-local vault unavailable: {exc}") from exc
    finally:
        if credentials_fd >= 0:
            try:
                os.close(credentials_fd)
            except OSError:
                pass


def run_character(args: argparse.Namespace) -> dict[str, object]:
    identity = _identity(args)
    command = "STATE" if args.operation == "character-state" else "CONFIRM_UNIQUE"
    response = request(Path(args.socket), command, timeout=args.timeout, expected_identity=identity)
    allowed = _STATE_ALLOWLIST if command == "STATE" else _CONFIRM_ALLOWLIST
    sanitized = {key: response[key] for key in allowed if key in response}
    if command == "STATE" and response.get("ok") is True:
        count = response.get("character_count")
        method_present = response.get("confirm_method_present")
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            raise BridgeClientError("character helper returned invalid count")
        if not isinstance(method_present, bool):
            raise BridgeClientError("character helper returned invalid confirmation capability")
    return sanitized


def _add_identity(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--socket", required=True)
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
    auth = sub.add_parser("auth")
    _add_identity(auth)
    auth.add_argument("--vault-dir", required=True)
    auth.add_argument("--drop-uid", required=True, type=int)
    auth.add_argument("--drop-gid", required=True, type=int)
    for name in ("character-state", "confirm-unique"):
        command = sub.add_parser(name)
        _add_identity(command)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    result = run_auth(args) if args.operation == "auth" else run_character(args)
    json.dump(result, sys.stdout, sort_keys=True, separators=(",", ":"))
    sys.stdout.write("\n")
    return 0 if result.get("ok") is True else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BridgeClientError as exc:
        print(f"container native login client error: {exc}", file=sys.stderr)
        raise SystemExit(2)
