from __future__ import annotations

import argparse
import json
from pathlib import Path
import socket
import sys
from typing import Any

SESSION_MARKERS = (
    "player_protocol_handler",
    "gameserver_game_session",
    "worldmap_handler",
)


class BridgeClientError(RuntimeError):
    pass


def request(socket_path: Path, command: str, *, timeout: float = 3.0) -> dict[str, Any]:
    if not command or "\n" in command or "\r" in command:
        raise BridgeClientError("command must be one non-empty line")
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.settimeout(timeout)
    try:
        client.connect(str(socket_path))
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
                raise BridgeClientError("bridge response exceeds 1 MiB")
            if b"\n" in chunk:
                break
    except OSError as exc:
        raise BridgeClientError(f"IPC request failed: {exc}") from exc
    finally:
        client.close()

    raw = b"".join(chunks)
    line = raw.split(b"\n", 1)[0]
    try:
        doc = json.loads(line.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BridgeClientError("bridge returned invalid JSON") from exc
    if not isinstance(doc, dict) or not isinstance(doc.get("ok"), bool):
        raise BridgeClientError("bridge response must contain boolean ok")
    return doc


def session_status(socket_path: Path, *, timeout: float = 3.0) -> dict[str, Any]:
    markers: dict[str, dict[str, Any]] = {}
    for target in SESSION_MARKERS:
        response = request(socket_path, f"DISCOVER {target}", timeout=timeout)
        if not response.get("ok"):
            return {
                "ok": False,
                "in_game_candidate": False,
                "evidence_level": "UNKNOWN",
                "failed_target": target,
                "response": response,
                "markers": markers,
            }
        validated = response.get("validated_hits")
        if not isinstance(validated, int) or isinstance(validated, bool) or validated < 0:
            raise BridgeClientError(f"target {target} returned invalid validated_hits")
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
