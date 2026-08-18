from __future__ import annotations

import argparse
import array
import json
import os
from pathlib import Path
import socket
import stat
import sys

try:
    import fcntl as _fcntl
except ImportError:  # pragma: no cover - Linux-only experimental auth surface
    _fcntl = None

from tools.tibia_runtime_bridge.ipc_client import (
    BridgeClientError,
    BridgeTransportError,
    PeerIdentityExpectation,
    _receive_response,
    _verify_peer_identity,
)

_MAX_CREDENTIAL_FRAME_BYTES = 8 + 2 * 1024
_MIN_CREDENTIAL_FRAME_BYTES = 10


def _validate_credentials_memfd(credentials_fd: int) -> None:
    if not isinstance(credentials_fd, int) or isinstance(credentials_fd, bool) or credentials_fd < 0:
        raise BridgeClientError("credentials_fd must be a non-negative file descriptor")
    if _fcntl is None:
        raise BridgeClientError("memfd sealing support is unavailable")
    required_names = ("F_GET_SEALS", "F_SEAL_SEAL", "F_SEAL_SHRINK", "F_SEAL_GROW", "F_SEAL_WRITE")
    if any(not hasattr(_fcntl, name) for name in required_names):
        raise BridgeClientError("memfd sealing support is unavailable")
    try:
        stat_result = os.fstat(credentials_fd)
        if not stat.S_ISREG(stat_result.st_mode):
            raise BridgeClientError("credentials_fd must refer to an anonymous sealed memfd")
        if not (_MIN_CREDENTIAL_FRAME_BYTES <= stat_result.st_size <= _MAX_CREDENTIAL_FRAME_BYTES):
            raise BridgeClientError("credentials memfd size is outside the bounded frame")
        target = os.readlink(f"/proc/self/fd/{credentials_fd}")
        if "memfd:" not in target:
            raise BridgeClientError("credentials_fd must refer to an anonymous memfd")
        seals = _fcntl.fcntl(credentials_fd, _fcntl.F_GET_SEALS)
        required = _fcntl.F_SEAL_SEAL | _fcntl.F_SEAL_SHRINK | _fcntl.F_SEAL_GROW | _fcntl.F_SEAL_WRITE
        if seals & required != required:
            raise BridgeClientError("credentials memfd must be fully sealed before handoff")
    except BridgeClientError:
        raise
    except OSError as exc:
        raise BridgeClientError(f"credentials_fd validation failed: {exc}") from exc


def auth_with_credentials_fd(
    socket_path: Path,
    credentials_fd: int,
    *,
    timeout: float = 3.0,
    expected_identity: PeerIdentityExpectation | None = None,
) -> dict[str, object]:
    """Pass an already-sealed credential memfd without reading its payload bytes."""

    if not socket_path.is_absolute():
        raise BridgeClientError("experimental auth socket path must be absolute")
    _validate_credentials_memfd(credentials_fd)
    if not hasattr(socket, "SCM_RIGHTS") or not hasattr(socket.socket, "sendmsg"):
        raise BridgeClientError("SCM_RIGHTS descriptor passing is unavailable")

    payload = b"AUTH_WITH_CREDENTIALS\n"
    descriptor_array = array.array("i", [credentials_fd])
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.settimeout(timeout)
    try:
        client.connect(str(socket_path))
        if expected_identity is not None:
            _verify_peer_identity(client, expected_identity)
        sent = client.sendmsg(
            [payload],
            [(socket.SOL_SOCKET, socket.SCM_RIGHTS, descriptor_array.tobytes())],
        )
        if sent != len(payload):
            raise BridgeTransportError("experimental auth command was only partially sent")
        return _receive_response(client)
    except BridgeClientError:
        raise
    except OSError as exc:
        raise BridgeTransportError(f"experimental auth IPC failed: {exc}") from exc
    finally:
        client.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Invoke the one-shot experimental native-auth helper using an already-open sealed credential memfd"
    )
    parser.add_argument("--socket", required=True, type=Path)
    parser.add_argument("--credentials-fd", required=True, type=int)
    args = parser.parse_args(argv)
    response = auth_with_credentials_fd(args.socket, args.credentials_fd)
    json.dump(response, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0 if response.get("ok") else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BridgeClientError as exc:
        print(f"experimental auth client error: {exc}", file=sys.stderr)
        raise SystemExit(2)
