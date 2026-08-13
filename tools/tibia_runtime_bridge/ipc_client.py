from __future__ import annotations

import argparse
import json
from pathlib import Path
import socket
import sys
from typing import Any


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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Query the OTClient Tibia runtime bridge")
    parser.add_argument("--socket", required=True, type=Path)
    sub = parser.add_subparsers(dest="operation", required=True)
    sub.add_parser("ping")
    discover = sub.add_parser("discover")
    discover.add_argument("target")
    args = parser.parse_args(argv)

    command = "PING" if args.operation == "ping" else f"DISCOVER {args.target}"
    response = request(args.socket, command)
    json.dump(response, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0 if response.get("ok") else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BridgeClientError as exc:
        print(f"bridge client error: {exc}", file=sys.stderr)
        raise SystemExit(2)
