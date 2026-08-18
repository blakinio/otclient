from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import socket
import struct
import sys
import threading
from typing import Any

SESSION_MARKERS = (
    "player_protocol_handler",
    "gameserver_game_session",
    "worldmap_handler",
)


class BridgeClientError(RuntimeError):
    pass


class BridgeTransportError(BridgeClientError):
    """The local bridge endpoint could not be reached or completed I/O."""


class BridgeProtocolError(BridgeClientError):
    """The bridge endpoint returned a structurally invalid response."""


class BridgePeerIdentityError(BridgeClientError):
    """The connected Unix peer is not the explicitly admitted runtime process."""


@dataclass(frozen=True)
class PeerIdentityExpectation:
    """Exact process identity supplied by the admitted runtime producer.

    The transport never discovers a candidate PID. It verifies only the explicit peer
    selected by the caller and fails closed if the connected Unix peer, current boot,
    process start time or executable fence differs.
    """

    boot_id_sha256: str
    pid: int
    process_start_ticks: int
    client_version: str
    client_size: int
    client_sha256: str


_PEERCRED = struct.Struct("3i")
_executable_digest_cache: dict[tuple[int, int, int, int, int, int, int], str] = {}
_executable_digest_cache_lock = threading.Lock()


def _boot_id_sha256() -> str:
    raw = Path("/proc/sys/kernel/random/boot_id").read_text(encoding="ascii").strip().encode()
    return hashlib.sha256(raw).hexdigest()


def _process_start_ticks(pid: int) -> int:
    raw = Path(f"/proc/{pid}/stat").read_text(encoding="ascii")
    close = raw.rfind(")")
    if close < 0:
        raise ValueError("peer /proc stat is malformed")
    fields = raw[close + 2 :].split()
    if len(fields) < 20:
        raise ValueError("peer /proc stat is incomplete")
    return int(fields[19])


def _sha256_fd(fd: int) -> str:
    digest = hashlib.sha256()
    os.lseek(fd, 0, os.SEEK_SET)
    while True:
        chunk = os.read(fd, 1024 * 1024)
        if not chunk:
            break
        digest.update(chunk)
    return digest.hexdigest()


def _verify_peer_executable(expectation: PeerIdentityExpectation) -> None:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    fd = os.open(f"/proc/{expectation.pid}/exe", flags)
    try:
        stat = os.fstat(fd)
        if stat.st_size != expectation.client_size:
            raise BridgePeerIdentityError(
                f"peer executable size mismatch: expected {expectation.client_size}, got {stat.st_size}"
            )
        cache_key = (
            expectation.pid,
            expectation.process_start_ticks,
            stat.st_dev,
            stat.st_ino,
            stat.st_size,
            stat.st_mtime_ns,
            stat.st_ctime_ns,
        )
        with _executable_digest_cache_lock:
            actual_sha256 = _executable_digest_cache.get(cache_key)
        if actual_sha256 is None:
            actual_sha256 = _sha256_fd(fd)
            with _executable_digest_cache_lock:
                if len(_executable_digest_cache) >= 16:
                    _executable_digest_cache.pop(next(iter(_executable_digest_cache)))
                _executable_digest_cache[cache_key] = actual_sha256
        if actual_sha256 != expectation.client_sha256:
            raise BridgePeerIdentityError(
                f"peer executable SHA-256 mismatch: expected {expectation.client_sha256}, got {actual_sha256}"
            )
    finally:
        os.close(fd)


def _verify_peer_identity(client: socket.socket, expectation: PeerIdentityExpectation) -> None:
    if not hasattr(socket, "SO_PEERCRED"):
        raise BridgePeerIdentityError("SO_PEERCRED is unavailable on this platform")
    try:
        raw = client.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, _PEERCRED.size)
        peer_pid, _peer_uid, _peer_gid = _PEERCRED.unpack(raw)
        if peer_pid != expectation.pid:
            raise BridgePeerIdentityError(
                f"Unix peer PID mismatch: expected {expectation.pid}, got {peer_pid}"
            )
        current_boot = _boot_id_sha256()
        if current_boot != expectation.boot_id_sha256:
            raise BridgePeerIdentityError("runtime boot identity no longer matches the admitted binding")
        current_start_ticks = _process_start_ticks(peer_pid)
        if current_start_ticks != expectation.process_start_ticks:
            raise BridgePeerIdentityError(
                "runtime process start ticks no longer match the admitted binding"
            )
        _verify_peer_executable(expectation)
    except BridgePeerIdentityError:
        raise
    except (OSError, UnicodeError, ValueError) as exc:
        raise BridgePeerIdentityError(f"peer identity verification failed: {exc}") from exc


def request(
    socket_path: Path,
    command: str,
    *,
    timeout: float = 3.0,
    expected_identity: PeerIdentityExpectation | None = None,
) -> dict[str, Any]:
    if not command or "\n" in command or "\r" in command:
        raise BridgeClientError("command must be one non-empty line")
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.settimeout(timeout)
    try:
        client.connect(str(socket_path))
        if expected_identity is not None:
            _verify_peer_identity(client, expected_identity)
        client.sendall(command.encode("utf-8") + b"\n")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = client.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > 1024 * 1024:
                raise BridgeProtocolError("bridge response exceeds 1 MiB")
            if b"\n" in chunk:
                break
    except BridgeClientError:
        raise
    except OSError as exc:
        raise BridgeTransportError(f"IPC request failed: {exc}") from exc
    finally:
        client.close()

    raw = b"".join(chunks)
    line = raw.split(b"\n", 1)[0]
    try:
        doc = json.loads(line.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BridgeProtocolError("bridge returned invalid JSON") from exc
    if not isinstance(doc, dict) or not isinstance(doc.get("ok"), bool):
        raise BridgeProtocolError("bridge response must contain boolean ok")
    return doc


def session_status(
    socket_path: Path,
    *,
    timeout: float = 3.0,
    expected_identity: PeerIdentityExpectation | None = None,
) -> dict[str, Any]:
    markers: dict[str, dict[str, Any]] = {}
    for target in SESSION_MARKERS:
        response = request(
            socket_path,
            f"DISCOVER {target}",
            timeout=timeout,
            expected_identity=expected_identity,
        )
        if not response.get("ok"):
            return {
                "ok": False,
                "in_game_candidate": False,
                "evidence_level": "UNKNOWN",
                "failed_target": target,
                "response": response,
                "markers": markers,
            }
        if response.get("target") != target or response.get("scan_status") != "OK":
            raise BridgeProtocolError(
                f"target {target} did not prove a successful matching discovery scan"
            )
        validated = response.get("validated_hits")
        if not isinstance(validated, int) or isinstance(validated, bool) or validated < 0:
            raise BridgeProtocolError(f"target {target} returned invalid validated_hits")
        markers[target] = response

    candidate = all(markers[target]["validated_hits"] > 0 for target in SESSION_MARKERS)
    return {
        "ok": True,
        "in_game_candidate": candidate,
        "evidence_level": "DERIVED_UNTIL_LIVE_CORRELATION",
        "required_markers": list(SESSION_MARKERS),
        "markers": markers,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Query the OTClient Tibia runtime bridge")
    parser.add_argument("--socket", required=True, type=Path)
    sub = parser.add_subparsers(dest="operation", required=True)
    sub.add_parser("ping")
    discover = sub.add_parser("discover")
    discover.add_argument("target")
    sub.add_parser("session-status")
    args = parser.parse_args(argv)

    if args.operation == "ping":
        response = request(args.socket, "PING")
    elif args.operation == "discover":
        response = request(args.socket, f"DISCOVER {args.target}")
    else:
        response = session_status(args.socket)
    json.dump(response, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0 if response.get("ok") else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BridgeClientError as exc:
        print(f"bridge client error: {exc}", file=sys.stderr)
        raise SystemExit(2)
