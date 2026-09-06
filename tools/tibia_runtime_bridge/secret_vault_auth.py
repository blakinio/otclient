from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any

from tools.tibia_re_control_center.current_client_fence import current_client_fence
from tools.tibia_runtime_bridge.experimental_auth_client import auth_with_credentials_fd
from tools.tibia_runtime_bridge.ipc_client import BridgeClientError, PeerIdentityExpectation
from tools.tibia_runtime_bridge.secret_vault import SecretVaultError, decrypt_to_sealed_memfd

_FORBIDDEN_CREDENTIAL_ENV = ("TIBIA_TEST_EMAIL", "TIBIA_TEST_PASSWORD")
_IDENTITY_KEYS = {
    "boot_id_sha256",
    "pid",
    "process_start_ticks",
    "client_version",
    "client_size",
    "client_sha256",
}
_RESPONSE_ALLOWLIST = (
    "ok",
    "command",
    "invocation_dispatched",
    "qmeta_method_id",
)


def _hex64(value: object) -> bool:
    return bool(
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value.lower())
    )


def _require_absolute(path: Path, label: str) -> Path:
    if not path.is_absolute():
        raise BridgeClientError(f"{label} path must be absolute")
    return path


def _reject_credential_environment() -> None:
    if any(name in os.environ for name in _FORBIDDEN_CREDENTIAL_ENV):
        raise BridgeClientError("credential-bearing environment variables are forbidden for vault auth")


def load_current_runtime_identity(path: Path) -> PeerIdentityExpectation:
    path = _require_absolute(Path(path), "identity")
    try:
        info = path.lstat()
    except OSError as exc:
        raise BridgeClientError(f"runtime identity is unavailable: {exc}") from exc
    if path.is_symlink() or not stat.S_ISREG(info.st_mode):
        raise BridgeClientError("runtime identity must be a private regular file")
    if stat.S_IMODE(info.st_mode) != 0o600:
        raise BridgeClientError("runtime identity permissions must be 0600")
    if hasattr(os, "geteuid") and info.st_uid != os.geteuid():
        raise BridgeClientError("runtime identity must be owned by the current user")
    try:
        document: Any = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise BridgeClientError("runtime identity JSON is invalid") from exc
    if not isinstance(document, dict) or set(document) != _IDENTITY_KEYS:
        raise BridgeClientError("runtime identity has unexpected fields")

    boot_id = document["boot_id_sha256"]
    pid = document["pid"]
    start_ticks = document["process_start_ticks"]
    version = document["client_version"]
    size = document["client_size"]
    sha256 = document["client_sha256"]
    if not _hex64(boot_id):
        raise BridgeClientError("runtime boot identity is invalid")
    if isinstance(pid, bool) or not isinstance(pid, int) or pid < 2:
        raise BridgeClientError("runtime PID is invalid")
    if isinstance(start_ticks, bool) or not isinstance(start_ticks, int) or start_ticks <= 0:
        raise BridgeClientError("runtime process start ticks are invalid")
    if not isinstance(version, str) or isinstance(size, bool) or not isinstance(size, int) or not _hex64(sha256):
        raise BridgeClientError("runtime client identity is invalid")

    fence = current_client_fence()
    if (version, size, sha256) != (fence.version, fence.size, fence.sha256):
        raise BridgeClientError("runtime identity does not match the current client fence")
    return PeerIdentityExpectation(
        boot_id_sha256=boot_id,
        pid=pid,
        process_start_ticks=start_ticks,
        client_version=fence.version,
        client_size=fence.size,
        client_sha256=fence.sha256,
    )


def run_vault_auth(vault_dir: Path, socket_path: Path, identity_path: Path) -> dict[str, object]:
    vault_dir = _require_absolute(Path(vault_dir), "vault")
    socket_path = _require_absolute(Path(socket_path), "auth socket")
    identity_path = _require_absolute(Path(identity_path), "identity")
    _reject_credential_environment()
    identity = load_current_runtime_identity(identity_path)
    credentials_fd = -1
    try:
        credentials_fd = decrypt_to_sealed_memfd(vault_dir)
        response = auth_with_credentials_fd(
            socket_path,
            credentials_fd,
            expected_identity=identity,
        )
    except SecretVaultError as exc:
        raise BridgeClientError(f"machine-local credential vault unavailable: {exc}") from exc
    finally:
        if credentials_fd >= 0:
            try:
                os.close(credentials_fd)
            except OSError:
                pass
    return {key: response[key] for key in _RESPONSE_ALLOWLIST if key in response}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Consume the machine-local Track A credential vault into the exact native-auth FD transport"
    )
    parser.add_argument("--vault-dir", required=True, type=Path)
    parser.add_argument("--socket", required=True, type=Path)
    parser.add_argument("--identity", required=True, type=Path)
    args = parser.parse_args(argv)
    result = run_vault_auth(args.vault_dir, args.socket, args.identity)
    json.dump(result, sys.stdout, sort_keys=True, separators=(",", ":"))
    sys.stdout.write("\n")
    return 0 if result.get("ok") is True else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BridgeClientError as exc:
        print(f"secret vault auth error: {exc}", file=sys.stderr)
        raise SystemExit(2)
