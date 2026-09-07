#!/usr/bin/env python3
"""Canonical transition shim admitting the corrected Kasm-only inventory scope."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
from types import ModuleType
from typing import Any, Sequence

BASE_PATH = Path(__file__).with_name("tibia-official-client-re-canonical-live-transition.py")
CANONICAL_SCOPE = "canonical_kasm_container"
LEGACY_SCOPE = "all_running_docker_containers"
ALLOWED_SCOPES = {CANONICAL_SCOPE, LEGACY_SCOPE}


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


def _hex64(value: Any) -> bool:
    return bool(
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value.lower())
    )


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
_base._require_kasm_launch_matches_manifest = _require_kasm_launch_matches_manifest


def main(argv: Sequence[str] | None = None) -> int:
    return int(_base.main(argv))


if __name__ == "__main__":
    raise SystemExit(main())
