#!/usr/bin/env python3
"""Canonical transition shim admitting the corrected Kasm-only inventory scope."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys
from types import ModuleType
from typing import Any, Sequence

BASE_PATH = Path(__file__).with_name("tibia-official-client-re-canonical-live-transition.py")
CANONICAL_SCOPE = "canonical_kasm_container"
LEGACY_SCOPE = "all_running_docker_containers"
ALLOWED_SCOPES = {CANONICAL_SCOPE, LEGACY_SCOPE}
OFFICIAL_ENTRYPOINT_LAUNCH_METHOD = "docker_exec_detached_official_linux_entrypoint"


def _load_base() -> ModuleType:
    spec = importlib.util.spec_from_file_location("track_a_canonical_transition_scoped_base", BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("canonical_transition_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_base = _load_base()
_original_read = _base._read
_original_manifest = _base._manifest
_original_read_kasm_bootstrap_record = _base._read_kasm_bootstrap_record
_original_require_kasm_launch_bound_to_preflight = _base._require_kasm_launch_bound_to_preflight
KASM_CLIENT_DIR = str(PurePosixPath(_base.KASM_CLIENT_PATH).parent)
_LAUNCHER_FIELDS = {
    "launcher_path",
    "launcher_dir",
    "launcher_size",
    "launcher_sha256",
    "launcher_selection",
}


def _hex64(value: Any) -> bool:
    return bool(
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value.lower())
    )


def _launcher_fields_present(data: dict[str, Any]) -> bool:
    return any(field in data for field in _LAUNCHER_FIELDS)


def _validate_launcher_fields(data: dict[str, Any]) -> None:
    path = data.get("launcher_path")
    directory = data.get("launcher_dir")
    size = data.get("launcher_size")
    sha = data.get("launcher_sha256")
    selection = data.get("launcher_selection")
    if not isinstance(path, str) or not isinstance(directory, str):
        raise _base.E("kasm_bootstrap_record_invalid")
    launcher = PurePosixPath(path)
    package = PurePosixPath(_base.KASM_PACKAGE_DIR)
    if (
        not launcher.is_absolute()
        or launcher.name != "Tibia"
        or str(launcher.parent) != directory
        or launcher == package
        or package in launcher.parents
    ):
        raise _base.E("kasm_bootstrap_record_invalid")
    if not isinstance(size, int) or size < 1 or not _hex64(sha):
        raise _base.E("kasm_bootstrap_record_invalid")
    if selection not in {"desktop", "unique"}:
        raise _base.E("kasm_bootstrap_record_invalid")


def _read_kasm_bootstrap_record(path: Path, expected_schema: str) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise _base.E("kasm_bootstrap_record_invalid", str(exc)) from exc
    if not isinstance(data, dict) or data.get("schema") != expected_schema:
        raise _base.E("kasm_bootstrap_record_invalid")

    if expected_schema == _base.KASM_PREFLIGHT_SCHEMA:
        if not _launcher_fields_present(data):
            return _original_read_kasm_bootstrap_record(path, expected_schema)
        required = {
            "schema", "container_name", "container_id", "display", "package_dir",
            "client_path", "client_size", "client_sha256", "boot_id_sha256",
            "candidate_count", "main_window_count", "preflight_fingerprint",
            *_LAUNCHER_FIELDS,
        }
        if set(data) != required:
            raise _base.E("kasm_bootstrap_record_invalid")
        expected = {
            "container_name": _base.KASM_TARGET_CONTAINER,
            "display": _base.KASM_TARGET_DISPLAY,
            "package_dir": _base.KASM_PACKAGE_DIR,
            "client_path": _base.KASM_CLIENT_PATH,
            "client_size": _base.SIZE,
            "client_sha256": _base.SHA,
            "candidate_count": 0,
            "main_window_count": 0,
        }
        if any(data.get(key) != value for key, value in expected.items()):
            raise _base.E("kasm_bootstrap_record_invalid")
        if (
            not _hex64(data.get("container_id"))
            or not _hex64(data.get("boot_id_sha256"))
            or not _hex64(data.get("preflight_fingerprint"))
        ):
            raise _base.E("kasm_bootstrap_record_invalid")
        _validate_launcher_fields(data)
        unsigned = dict(data)
        fingerprint = unsigned.pop("preflight_fingerprint")
        calculated = hashlib.sha256(
            json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        if fingerprint != calculated:
            raise _base.E("kasm_bootstrap_record_invalid")
        return data

    if expected_schema == _base.KASM_LAUNCH_SCHEMA:
        official_entrypoint = (
            _launcher_fields_present(data)
            or "client_dir" in data
            or data.get("launch_method") == OFFICIAL_ENTRYPOINT_LAUNCH_METHOD
        )
        if not official_entrypoint:
            return _original_read_kasm_bootstrap_record(path, expected_schema)
        required = {
            "schema", "preflight_fingerprint", "container_name", "container_id", "display",
            "package_dir", "client_path", "client_size", "client_sha256", "pid",
            "process_start_ticks", "launch_method", "bootstrap_helper_residue", "client_dir",
            *_LAUNCHER_FIELDS,
        }
        if set(data) != required:
            raise _base.E("kasm_bootstrap_record_invalid")
        expected = {
            "container_name": _base.KASM_TARGET_CONTAINER,
            "display": _base.KASM_TARGET_DISPLAY,
            "package_dir": _base.KASM_PACKAGE_DIR,
            "client_path": _base.KASM_CLIENT_PATH,
            "client_size": _base.SIZE,
            "client_sha256": _base.SHA,
            "launch_method": OFFICIAL_ENTRYPOINT_LAUNCH_METHOD,
            "bootstrap_helper_residue": False,
            "client_dir": KASM_CLIENT_DIR,
        }
        if any(data.get(key) != value for key, value in expected.items()):
            raise _base.E("kasm_bootstrap_record_invalid")
        if not _hex64(data.get("container_id")) or not _hex64(data.get("preflight_fingerprint")):
            raise _base.E("kasm_bootstrap_record_invalid")
        for key in ("pid", "process_start_ticks"):
            if not isinstance(data.get(key), int) or data[key] < 1:
                raise _base.E("kasm_bootstrap_record_invalid")
        _validate_launcher_fields(data)
        return data

    return _original_read_kasm_bootstrap_record(path, expected_schema)


def _require_kasm_launch_bound_to_preflight(
    preflight: dict[str, Any], launch: dict[str, Any]
) -> None:
    preflight_official = _launcher_fields_present(preflight)
    launch_official = (
        _launcher_fields_present(launch)
        or "client_dir" in launch
        or launch.get("launch_method") == OFFICIAL_ENTRYPOINT_LAUNCH_METHOD
    )
    if preflight_official != launch_official:
        raise _base.E("kasm_bootstrap_launch_preflight_mismatch")
    _original_require_kasm_launch_bound_to_preflight(preflight, launch)
    if not launch_official:
        return
    _validate_launcher_fields(preflight)
    _validate_launcher_fields(launch)
    if launch.get("launch_method") != OFFICIAL_ENTRYPOINT_LAUNCH_METHOD:
        raise _base.E("kasm_bootstrap_launch_preflight_mismatch")
    if launch.get("client_dir") != KASM_CLIENT_DIR:
        raise _base.E("kasm_bootstrap_launch_preflight_mismatch")
    for key in _LAUNCHER_FIELDS:
        if launch.get(key) != preflight.get(key):
            raise _base.E("kasm_bootstrap_launch_preflight_mismatch")


def _read() -> dict[str, Any] | None:
    if not _base.REG.exists():
        return None
    st = _base.REG.lstat()
    owner = not hasattr(os, "getuid") or st.st_uid == os.getuid()
    if not stat.S_ISREG(st.st_mode) or _base.REG.is_symlink() or (st.st_mode & 0o777) != 0o600 or not owner:
        raise _base.E("registration_file_unsafe")
    try:
        data = json.loads(_base.REG.read_text())
    except (OSError, json.JSONDecodeError):
        return _original_read()
    if not isinstance(data, dict) or data.get("proof_kind") != _base.ADOPTION_PROOF_KIND:
        return _original_read()

    if not _base.FIELDS.issubset(data):
        raise _base.E("registration_schema_invalid")
    if data.get("schema_version") != 1 or data.get("runtime_id") != _base.RID:
        raise _base.E("registration_schema_invalid")
    if (data.get("client_version"), data.get("client_size"), data.get("client_sha256")) != (_base.VER, _base.SIZE, _base.SHA):
        raise _base.E("registration_client_fence_invalid")
    if data.get("state") not in _base.STATES or data.get("remote_view_mapping") not in {"PROVEN", "UNKNOWN"}:
        raise _base.E("registration_state_invalid")
    if not isinstance(data.get("registration_generation"), int) or data["registration_generation"] < 1:
        raise _base.E("registration_generation_invalid")
    if not isinstance(data.get("lease_generation"), int) or data["lease_generation"] < 1:
        raise _base.E("registration_lease_generation_invalid")

    required = {
        "runtime_locator", "inventory_scope", "inventory_complete", "candidate_count",
        "candidate_fingerprint", "state_evidence",
    }
    if not required.issubset(data):
        raise _base.E("adoption_registration_schema_invalid")
    if data["inventory_scope"] not in ALLOWED_SCOPES or data["inventory_complete"] is not True:
        raise _base.E("adoption_registration_inventory_invalid")
    if data["candidate_count"] != 1:
        raise _base.E("adoption_registration_candidate_count_invalid")
    if not isinstance(data["runtime_locator"], str) or not data["runtime_locator"].startswith("docker:"):
        raise _base.E("adoption_registration_runtime_locator_invalid")
    if not _hex64(data["candidate_fingerprint"]):
        raise _base.E("adoption_registration_candidate_fingerprint_invalid")
    if data["state_evidence"] not in _base.ADOPTION_STATE_EVIDENCE:
        raise _base.E("adoption_registration_state_evidence_invalid")
    provenance = data.get("bootstrap_provenance")
    if provenance is not None and (
        provenance != _base.KASM_BOOTSTRAP_PROVENANCE or data.get("proof_kind") != _base.ADOPTION_PROOF_KIND
    ):
        raise _base.E("kasm_bootstrap_provenance_invalid")
    return data


def _manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return _original_manifest(path)
    if not isinstance(data, dict) or data.get("proof_kind") != _base.ADOPTION_PROOF_KIND:
        return _original_manifest(path)

    common = {"pid", "display", "window_identity", "remote_view_endpoint", "remote_view_mapping", "state"}
    if not common.issubset(data):
        raise _base.E("probe_manifest_missing_fields")
    if not isinstance(data["pid"], int) or data["pid"] < 2:
        raise _base.E("probe_pid_invalid")
    if not isinstance(data["display"], str) or not data["display"].startswith(":"):
        raise _base.E("probe_display_invalid")
    if not isinstance(data["window_identity"], str) or not data["window_identity"]:
        raise _base.E("probe_window_invalid")
    if data["remote_view_mapping"] not in {"PROVEN", "UNKNOWN"} or data["state"] not in _base.STATES:
        raise _base.E("probe_state_invalid")

    required = {
        "boot_id_sha256", "process_start_ticks", "client_version", "client_size",
        "client_sha256", "runtime_locator", "inventory_scope", "inventory_complete",
        "candidate_count", "candidate_fingerprint", "state_evidence",
    }
    if not required.issubset(data):
        raise _base.E("adoption_manifest_missing_fields")
    if data["inventory_complete"] is not True or data["inventory_scope"] not in ALLOWED_SCOPES:
        raise _base.E("adoption_inventory_incomplete")
    if data["candidate_count"] != 1:
        raise _base.E("adoption_target_not_unique")
    if data["client_version"] != _base.VER or data["client_size"] != _base.SIZE or data["client_sha256"] != _base.SHA:
        raise _base.E("adoption_client_fence_invalid")
    if not isinstance(data["process_start_ticks"], int) or data["process_start_ticks"] < 1:
        raise _base.E("adoption_start_ticks_invalid")
    for field in ("boot_id_sha256", "candidate_fingerprint"):
        if not _hex64(data[field]):
            raise _base.E(f"adoption_{field}_invalid")
    if not isinstance(data["runtime_locator"], str) or not data["runtime_locator"].startswith("docker:"):
        raise _base.E("adoption_runtime_locator_invalid")
    if data["state_evidence"] not in _base.ADOPTION_STATE_EVIDENCE:
        raise _base.E("adoption_state_evidence_invalid")
    if data["state"] == "IN_GAME":
        raise _base.E("adoption_ingame_semantics_unproven")
    return data


def _require_kasm_launch_matches_manifest(launch: dict[str, Any], manifest: dict[str, Any]) -> None:
    if not _base._is_adoption_manifest(manifest):
        raise _base.E("kasm_bootstrap_adoption_manifest_required")
    locator = f"docker:{launch['container_name']}:{launch['container_id']}"
    required = {
        "pid": launch["pid"],
        "process_start_ticks": launch["process_start_ticks"],
        "client_version": _base.VER,
        "client_size": launch["client_size"],
        "client_sha256": launch["client_sha256"],
        "display": launch["display"],
        "runtime_locator": locator,
        "inventory_scope": CANONICAL_SCOPE,
        "inventory_complete": True,
        "candidate_count": 1,
        "state": "UNKNOWN",
    }
    for key, expected in required.items():
        if manifest.get(key) != expected:
            raise _base.E(f"kasm_bootstrap_manifest_{key}_mismatch")
    window = str(manifest.get("window_identity", ""))
    if f":pid:{launch['pid']}:class:client/Tibia:" not in window:
        raise _base.E("kasm_bootstrap_manifest_window_identity_mismatch")
    expected_fingerprint = _base._recovery_candidate_fingerprint(manifest)
    if manifest.get("candidate_fingerprint") != expected_fingerprint:
        raise _base.E("kasm_bootstrap_manifest_candidate_fingerprint_mismatch")


_base._read = _read
_base._manifest = _manifest
_base._read_kasm_bootstrap_record = _read_kasm_bootstrap_record
_base._require_kasm_launch_bound_to_preflight = _require_kasm_launch_bound_to_preflight
_base._require_kasm_launch_matches_manifest = _require_kasm_launch_matches_manifest


def main(argv: Sequence[str] | None = None) -> int:
    return int(_base.main(argv))


if __name__ == "__main__":
    raise SystemExit(main())
