from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys

from tools.tibia_runtime_bridge.launcher import BridgeConfigError, build_env, load_profile, sha256_file

_FORBIDDEN_CREDENTIAL_ENV = (
    "TIBIA_TEST_EMAIL",
    "TIBIA_TEST_PASSWORD",
)


def _reject_credential_environment(base_env: dict[str, str]) -> None:
    present = [name for name in _FORBIDDEN_CREDENTIAL_ENV if name in base_env]
    if present:
        raise BridgeConfigError("credential-bearing environment variables are forbidden for experimental native auth")


def build_experimental_env(
    profile: dict,
    bridge_helper: Path,
    bridge_socket: Path,
    auth_helper: Path,
    auth_socket: Path,
    base_env: dict[str, str] | None = None,
) -> dict[str, str]:
    if not bridge_socket.is_absolute() or not auth_socket.is_absolute():
        raise BridgeConfigError("bridge and experimental auth socket paths must be absolute")
    if bridge_socket == auth_socket:
        raise BridgeConfigError("experimental auth socket must be distinct from the read-only bridge socket")
    source_env = dict(os.environ if base_env is None else base_env)
    _reject_credential_environment(source_env)
    env = build_env(profile, bridge_helper, bridge_socket, source_env)
    existing_preload = env.get("LD_PRELOAD", "").strip()
    env["LD_PRELOAD"] = f"{auth_helper}:{existing_preload}" if existing_preload else str(auth_helper)
    env["OTCLIENT_TIBIA_RE_AUTH_SOCKET"] = str(auth_socket)
    return env


def _prepare_socket_path(path: Path) -> None:
    if not path.is_absolute():
        raise BridgeConfigError("socket path must be absolute")
    path.parent.mkdir(parents=True, exist_ok=True)
    if os.path.lexists(path):
        raise BridgeConfigError(f"refusing to replace existing socket path: {path}")


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
    bridge_socket = args.bridge_socket.absolute()
    auth_socket = args.auth_socket.absolute()
    if bridge_socket == auth_socket:
        raise BridgeConfigError("experimental auth socket must be distinct from the read-only bridge socket")
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

    _reject_credential_environment(dict(os.environ))
    _prepare_socket_path(bridge_socket)
    _prepare_socket_path(auth_socket)
    env = build_experimental_env(
        profile,
        bridge_helper,
        bridge_socket,
        auth_helper,
        auth_socket,
        os.environ,
    )
    result = subprocess.run([str(client), *args.client_args], env=env, check=False)
    return result.returncode


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BridgeConfigError as exc:
        print(f"experimental auth launcher error: {exc}", file=sys.stderr)
        raise SystemExit(2)
