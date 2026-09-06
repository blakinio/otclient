#!/usr/bin/env python3
"""Bounded be4f48 physical worker with target-proc-root relay transport."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
from typing import Any, Sequence

_BASE_PATH = Path(__file__).with_name("track_a_native_login_be4f48_physical_base.py")
PROC_ROOT_RELAY_ROOT = "/proc/1/root/dev/shm"


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

_SAFE_PROBE_CLIENT_ERRORS = frozenset({
    "sealed_fd_not_regular",
    "sealed_fd_not_memfd",
    "sealed_fd_incomplete",
    "relay_socket_outside_target_proc_root",
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


def _proc_root_relay_socket(relay_socket: str) -> str:
    target = Path(relay_socket)
    if target.parent != Path(_base.RELAY_ROOT) or not target.name.startswith(_base.RELAY_PREFIX):
        raise PhysicalError("relay_socket_mapping_invalid")
    suffix = target.name[len(_base.RELAY_PREFIX):]
    if not suffix or any(ch not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for ch in suffix):
        raise PhysicalError("relay_socket_mapping_invalid")
    return str(Path(PROC_ROOT_RELAY_ROOT) / target.name)


def _sidecar_base(metadata: dict[str, Any], operation: str) -> list[str]:
    sidecar_host = _base._host_source(_base.SIDECAR_SOURCE, metadata)
    return [
        "docker", "run", "--rm",
        "--name", _base._sidecar_name(operation),
        "--label", f"{_base.SIDECAR_LABEL}={_base.TASK_ID}",
        "--network", "none",
        "--read-only",
        "--user", "0:0",
        "--pid", f"container:{_base.TARGET_CONTAINER}",
        "--cap-drop", "ALL",
        "--cap-add", "SETUID",
        "--cap-add", "SETGID",
        "--security-opt", "no-new-privileges",
        "--env", "PYTHONDONTWRITEBYTECODE=1",
        "--mount", f"type=bind,src={sidecar_host},dst=/tmp/native_login_fd_sidecar.py,readonly",
        "--entrypoint", "python3",
        str(metadata["image"]),
        "/tmp/native_login_fd_sidecar.py",
    ]


def _install_proc_root_transport_overlay() -> None:
    # Base replacement/auth/character logic remains byte-for-byte unchanged. Only
    # the sidecar command and relay pathname mapping are replaced for both probe
    # and auth, so base auth_one_shot automatically uses the same reviewed seam.
    _base._sidecar_base = _sidecar_base
    _base._sidecar_relay_socket = _proc_root_relay_socket


_install_proc_root_transport_overlay()


def _classify_sidecar_probe_failure(completed: subprocess.CompletedProcess[str]) -> str:
    """Map sidecar failure data to a static non-sensitive error code."""
    try:
        response = _base._parse_sidecar_response(completed)
    except PhysicalError:
        response = None
    if isinstance(response, dict):
        code = response.get("error")
        if isinstance(code, str) and code in _SAFE_PROBE_CLIENT_ERRORS:
            return f"sidecar_probe_client_{code}"
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
        "transport": "target_proc_root",
        "credential_plaintext_accessed": False,
        "secret_attempt_count": 0,
    })


def precheck(vault_dir: Path, bundle: Path, result: Path) -> None:
    _base._vault_precheck(vault_dir)
    _base._verify_bundle(bundle)
    registration = _base._read_registration()
    manifest = _base._current_manifest()
    _base._require_manifest_matches_registration(manifest, registration)
    uid, gid = _base._numeric_user()
    if not _base.same_numeric_uid(int(manifest["pid"]), uid):
        raise PhysicalError("same_numeric_uid_failed")
    _base._runner_sidecar_metadata(vault_dir)
    for operation in ("probe", "auth"):
        relay_socket = _base._relay_socket(operation)
        _proc_root_relay_socket(relay_socket)
        if _base._run(["docker", "exec", _base.TARGET_CONTAINER, "test", "!", "-e", relay_socket]).returncode != 0:
            raise PhysicalError("relay_socket_residue_present")
    _base._write_json(result, {
        "schema": "otclient.track-a.native-login-physical-precheck.v1",
        "exact_current": True,
        "target_unique": True,
        "registration_current": True,
        "sidecar_transport_metadata_ready": True,
        "sidecar_transport": "target_proc_root",
        "same_numeric_uid": True,
        "vault_bind": "HOST_ONLY_PRESENT_PRIVATE",
        "credential_plaintext_accessed": False,
        "sidecar_created": False,
        "target_uid": uid,
        "target_gid": gid,
    })


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
