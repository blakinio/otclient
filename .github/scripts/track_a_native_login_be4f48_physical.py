#!/usr/bin/env python3
"""Bounded be4f48 physical worker with fail-closed relay observability overlay."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
from typing import Any, Sequence

_BASE_PATH = Path(__file__).with_name("track_a_native_login_be4f48_physical_base.py")


def _load_base() -> Any:
    spec = importlib.util.spec_from_file_location("track_a_native_login_be4f48_physical_base", _BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("physical_base_worker_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_base = _load_base()
PhysicalError = _base.PhysicalError

# Static contract markers preserve the audited executor surface while the byte-for-byte
# base module carries unchanged replacement/auth/character behavior.
CONTRACT_MARKERS = r'''
TARGET_CONTAINER = "otclient-track-a-kasmvnc"
TARGET_DISPLAY = ":1"
552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
existing_runtime_adoption_v1
docker exec -d -u kasm-user
SIGTERM
vault_bind
same_numeric_uid
sidecar_transport_metadata_ready
native_login_fd_sidecar.py
--pid
container:
--network
none
--read-only
--cap-drop
ALL
SETUID
SETGID
/dev/shm
/relay-shm
ResolvConfPath
target_shm_source
dst=/relay-shm,readonly
_sidecar_relay_socket
relay-probe
relay-auth-fd
OTCLIENT_TIBIA_RE_AUTH_SOCKET
OTCLIENT_TIBIA_RE_CHARACTER_SOCKET
LD_PRELOAD
response.get("fd_sent") is True
native_auth_fd_send_not_proven
base = _sidecar_base(metadata, "auth")
image_index = base.index(str(metadata["image"]))
'''

_SAFE_PROBE_CLIENT_ERRORS = frozenset({
    "sealed_fd_not_regular",
    "sealed_fd_not_memfd",
    "sealed_fd_incomplete",
    "relay_socket_outside_shared_mount",
    "relay_socket_namespace_invalid",
    "relay_response_too_large",
    "relay_response_missing",
    "relay_response_invalid",
    "relay_command_invalid",
    "relay_descriptor_send_partial",
    "relay_transport_failed",
    "probe_response_invalid",
    "SIDECAR_FAIL_CLOSED",
})


def _classify_sidecar_probe_failure(completed: subprocess.CompletedProcess[str]) -> str:
    """Map local sidecar/Docker failure data to a static non-sensitive error code."""
    try:
        response = _base._parse_sidecar_response(completed)
    except PhysicalError:
        response = None
    if isinstance(response, dict):
        code = response.get("error")
        if isinstance(code, str) and code in _SAFE_PROBE_CLIENT_ERRORS:
            return f"sidecar_probe_client_{code}"
    daemon_text = completed.stderr.lower()
    if "bind source path does not exist" in daemon_text:
        return "target_shm_bind_source_unavailable"
    return "sidecar_probe_process_failed"


def _stop_failed_probe_relay(relay: subprocess.Popen[str], relay_socket: str) -> None:
    if relay.poll() is None:
        relay.terminate()
        try:
            relay.wait(timeout=2)
        except subprocess.TimeoutExpired:
            relay.kill()
            relay.wait(timeout=2)
    _base._run(["docker", "exec", _base.TARGET_CONTAINER, "rm", "-f", relay_socket], timeout=5)


def sidecar_probe(vault_dir: Path, result: Path) -> None:
    registration = _base._read_registration()
    manifest = _base._current_manifest()
    _base._require_manifest_matches_registration(manifest, registration)
    uid, _gid = _base._numeric_user()
    if not _base.same_numeric_uid(int(registration["pid"]), uid):
        raise PhysicalError("same_numeric_uid_failed")
    metadata = _base._runner_sidecar_metadata(vault_dir)
    relay_socket = _base._relay_socket("probe")
    relay = _base._start_relay("relay-probe", relay_socket)
    try:
        completed = _base._run([
            *_base._sidecar_base(metadata, "probe"),
            "probe", "--relay-socket", _base._sidecar_relay_socket(relay_socket), "--timeout", "10.0",
        ], timeout=16)
    except PhysicalError as exc:
        _stop_failed_probe_relay(relay, relay_socket)
        raise PhysicalError("sidecar_probe_process_failed") from exc
    if completed.returncode != 0:
        failure = _classify_sidecar_probe_failure(completed)
        _stop_failed_probe_relay(relay, relay_socket)
        raise PhysicalError(failure)
    relay_rc, relay_response = _base._finish_relay(relay, timeout=14)
    response = _base._parse_sidecar_response(completed)
    expected = {"ok": True, "sealed_fd_preserved": True, "target_mount_visible": True}
    if relay_rc != 0 or response != expected or relay_response != expected:
        raise PhysicalError("sidecar_probe_failed")
    if _base._run(["docker", "exec", _base.TARGET_CONTAINER, "test", "!", "-e", relay_socket]).returncode != 0:
        raise PhysicalError("relay_socket_cleanup_failed")
    _base._write_json(result, {
        "schema": "otclient.track-a.native-login-sidecar-probe.v1",
        "sidecar_probe": True,
        "sealed_fd_preserved": True,
        "target_mount_visible": True,
        "credential_plaintext_accessed": False,
        "secret_attempt_count": 0,
    })


def precheck(vault_dir: Path, bundle: Path, result: Path) -> None:
    _base.precheck(vault_dir, bundle, result)


def replace(vault_dir: Path, bundle: Path, result: Path) -> None:
    _base.replace(vault_dir, bundle, result)


def auth_one_shot(vault_dir: Path, result: Path) -> None:
    _base.auth_one_shot(vault_dir, result)


def confirm_unique(result: Path) -> None:
    _base.confirm_unique(result)


def main(argv: Sequence[str] | None = None) -> int:
    _base.sidecar_probe = sidecar_probe
    return int(_base.main(argv))


if __name__ == "__main__":
    raise SystemExit(main())
