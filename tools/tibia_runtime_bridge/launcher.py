from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

PROFILE_SCHEMA = "otclient.tibia-runtime-bridge.profile.v1"


class BridgeConfigError(ValueError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_profile(path: Path) -> dict[str, Any]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(doc, dict) or doc.get("schema") != PROFILE_SCHEMA:
        raise BridgeConfigError(f"profile schema must be {PROFILE_SCHEMA}")
    version = doc.get("client_version")
    digest = doc.get("binary_sha256")
    targets = doc.get("targets")
    if not isinstance(version, str) or not version.strip():
        raise BridgeConfigError("client_version must be a non-empty string")
    if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        raise BridgeConfigError("binary_sha256 must be a lowercase SHA-256 hex digest")
    if not isinstance(targets, dict):
        raise BridgeConfigError("targets must be an object")
    for name, target in targets.items():
        if not isinstance(name, str) or not name or not isinstance(target, dict):
            raise BridgeConfigError("target entries must be named objects")
        if target.get("resolver") != "primary_vptr":
            raise BridgeConfigError(f"unsupported resolver for target {name}")
        raw_offset = target.get("vptr_offset")
        expected_class = target.get("expected_qt_class")
        if not isinstance(raw_offset, str) or not raw_offset.startswith("0x"):
            raise BridgeConfigError(f"target {name} vptr_offset must be hexadecimal text")
        try:
            offset = int(raw_offset, 16)
        except ValueError as exc:
            raise BridgeConfigError(f"target {name} vptr_offset is invalid") from exc
        if offset <= 0:
            raise BridgeConfigError(f"target {name} vptr_offset must be positive")
        if not isinstance(expected_class, str) or not expected_class:
            raise BridgeConfigError(f"target {name} expected_qt_class must be non-empty")
    return doc


def build_env(profile: dict[str, Any], helper: Path, socket_path: Path, base_env: dict[str, str] | None = None) -> dict[str, str]:
    env = dict(os.environ if base_env is None else base_env)
    existing = env.get("LD_PRELOAD", "").strip()
    env["LD_PRELOAD"] = f"{helper}:{existing}" if existing else str(helper)
    env["OTCLIENT_TIBIA_RE_SOCKET"] = str(socket_path)
    env["OTCLIENT_TIBIA_RE_BINARY_SHA256"] = profile["binary_sha256"]
    env["OTCLIENT_TIBIA_RE_CLIENT_VERSION"] = profile["client_version"]
    targets = profile["targets"]
    env["OTCLIENT_TIBIA_RE_TARGETS"] = ";".join(
        f"{name},{int(target['vptr_offset'], 16):x},{target['expected_qt_class']}" for name, target in sorted(targets.items())
    )
    return env


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Launch an exact Tibia client with the OTClient runtime bridge helper")
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--helper", required=True, type=Path)
    parser.add_argument("--socket", required=True, type=Path)
    parser.add_argument("client", type=Path)
    parser.add_argument("client_args", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)

    profile = load_profile(args.profile)
    client = args.client.resolve()
    helper = args.helper.resolve()
    if not client.is_file():
        raise BridgeConfigError(f"client does not exist: {client}")
    if not helper.is_file():
        raise BridgeConfigError(f"helper does not exist: {helper}")
    actual = sha256_file(client)
    expected = profile["binary_sha256"]
    if actual != expected:
        raise BridgeConfigError(f"client SHA-256 mismatch: expected {expected}, got {actual}")

    args.socket.parent.mkdir(parents=True, exist_ok=True)
    try:
        args.socket.unlink()
    except FileNotFoundError:
        pass
    env = build_env(profile, helper, args.socket)
    result = subprocess.run([str(client), *args.client_args], env=env, check=False)
    return result.returncode


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BridgeConfigError as exc:
        print(f"bridge configuration error: {exc}", file=sys.stderr)
        raise SystemExit(2)
