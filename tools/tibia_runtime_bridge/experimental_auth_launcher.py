from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess

from tools.tibia_runtime_bridge.launcher import BridgeConfigError, build_env, load_profile, sha256_file


def build_experimental_env(
    profile: dict,
    bridge_helper: Path,
    bridge_socket: Path,
    auth_helper: Path,
    auth_socket: Path,
    base_env: dict[str, str] | None = None,
) -> dict[str, str]:
    env = build_env(profile, bridge_helper, bridge_socket, base_env)
    existing_preload = env.get("LD_PRELOAD", "").strip()
    env["LD_PRELOAD"] = f"{auth_helper}:{existing_preload}" if existing_preload else str(auth_helper)
    env["OTCLIENT_TIBIA_RE_AUTH_SOCKET"] = str(auth_socket)
    return env


def _prepare_socket_path(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Launch an exact Tibia client with the read-only runtime bridge and one-shot experimental native-auth helper"
    )
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--bridge-helper", required=True, type=Path)
    parser.add_argument("--bridge-socket", required=True, type=Path)
    parser.add_argument("--auth-helper", required=True, type=Path)
    parser.add_argument("--auth-socket", required=True, type=Path)
    parser.add_argument("client", type=Path)
    parser.add_argument("client_args", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)

    profile = load_profile(args.profile)
    client = args.client.resolve()
    bridge_helper = args.bridge_helper.resolve()
    auth_helper = args.auth_helper.resolve()
    if not client.is_file():
        raise BridgeConfigError(f"client does not exist: {client}")
    if not bridge_helper.is_file():
        raise BridgeConfigError(f"bridge helper does not exist: {bridge_helper}")
    if not auth_helper.is_file():
        raise BridgeConfigError(f"experimental auth helper does not exist: {auth_helper}")

    expected = profile["binary_sha256"]
    actual = sha256_file(client)
    if actual != expected:
        raise BridgeConfigError(f"client SHA-256 mismatch: expected {expected}, got {actual}")

    _prepare_socket_path(args.bridge_socket)
    _prepare_socket_path(args.auth_socket)
    env = build_experimental_env(
        profile,
        bridge_helper,
        args.bridge_socket,
        auth_helper,
        args.auth_socket,
        os.environ,
    )
    result = subprocess.run([str(client), *args.client_args], env=env, check=False)
    return result.returncode


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BridgeConfigError as exc:
        print(f"experimental auth launcher error: {exc}", file=os.sys.stderr)
        raise SystemExit(2)
