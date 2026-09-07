#!/usr/bin/env python3
"""Guarded metadata-only invalidation for same-boot zero-client canonical state."""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import time
from types import ModuleType
from typing import Any, Sequence

STATE_DIR = Path("/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime")
REGISTRATION_NAME = "runtime-registration.json"
LEASE_NAME = "lease.json"
LOCK_NAME = "coordination.lock"
GUARD_ENV = "TRACK_A_SAME_BOOT_INVALIDATION_GUARDED"
RECOVERY_MODE = "same_boot_zero_client_invalidation_v1"
EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52105824
EXPECTED_SHA = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"
APPROVED_WORKER = Path(__file__).with_name("tibia-official-client-re-kasm-bootstrap-worker.py")


class InvalidationError(RuntimeError):
    pass


def _private_json(path: Path) -> tuple[dict[str, Any], bytes]:
    try:
        info = path.lstat()
        if not stat.S_ISREG(info.st_mode) or path.is_symlink() or stat.S_IMODE(info.st_mode) != 0o600:
            raise InvalidationError(f"unsafe_file:{path.name}")
        if hasattr(os, "getuid") and info.st_uid != os.getuid():
            raise InvalidationError(f"unsafe_owner:{path.name}")
        raw = path.read_bytes()
        data = json.loads(raw)
    except InvalidationError:
        raise
    except (OSError, json.JSONDecodeError) as exc:
        raise InvalidationError(f"invalid_file:{path.name}") from exc
    if not isinstance(data, dict):
        raise InvalidationError(f"invalid_object:{path.name}")
    return data, raw


def _fsync_dir(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _load_worker(path: Path) -> ModuleType:
    try:
        if path.resolve(strict=True) != APPROVED_WORKER.resolve(strict=True):
            raise InvalidationError("worker_not_approved")
    except OSError as exc:
        raise InvalidationError("worker_unavailable") from exc
    spec = importlib.util.spec_from_file_location("track_a_same_boot_zero_client_worker", path)
    if spec is None or spec.loader is None:
        raise InvalidationError("worker_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise InvalidationError("worker_import_failed") from exc
    for name in ("collect_preflight", "process_identity"):
        if not callable(getattr(module, name, None)):
            raise InvalidationError("worker_contract_invalid")
    if (
        getattr(module, "VER", None),
        getattr(module, "SIZE", None),
        getattr(module, "SHA", None),
    ) != (EXPECTED_VERSION, EXPECTED_SIZE, EXPECTED_SHA):
        raise InvalidationError("worker_current_fence_mismatch")
    return module


def _require_external_guard(state_dir: Path) -> None:
    if os.environ.get(GUARD_ENV) != "1":
        raise InvalidationError("canonical_guard_required")
    lock_path = state_dir / LOCK_NAME
    try:
        fd = os.open(lock_path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0))
    except OSError as exc:
        raise InvalidationError("canonical_guard_required") from exc
    acquired = False
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            acquired = True
        except BlockingIOError:
            return
    finally:
        if acquired:
            fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)
    raise InvalidationError("canonical_guard_required")


def _validate_registration(registration: dict[str, Any]) -> None:
    required = {
        "schema_version", "runtime_id", "registration_generation", "lease_generation",
        "boot_id_sha256", "pid", "process_start_ticks", "client_version", "client_size",
        "client_sha256", "display",
    }
    if not required.issubset(registration):
        raise InvalidationError("registration_schema_invalid")
    if registration.get("schema_version") != 1 or registration.get("runtime_id") != "track-a-canonical-live":
        raise InvalidationError("registration_schema_invalid")
    if (
        registration.get("client_version"),
        registration.get("client_size"),
        registration.get("client_sha256"),
    ) != (EXPECTED_VERSION, EXPECTED_SIZE, EXPECTED_SHA):
        raise InvalidationError("registration_client_fence_invalid")
    for field in ("registration_generation", "lease_generation", "pid", "process_start_ticks"):
        if not isinstance(registration.get(field), int) or int(registration[field]) < 1:
            raise InvalidationError(f"registration_{field}_invalid")
    boot = registration.get("boot_id_sha256")
    if not isinstance(boot, str) or len(boot) != 64 or any(ch not in "0123456789abcdef" for ch in boot.lower()):
        raise InvalidationError("registration_boot_invalid")


def _validate_lease(
    lease: dict[str, Any],
    task_id: str,
    session_id: str,
    registration_lease_generation: int,
) -> int:
    if lease.get("schema_version") != 1 or lease.get("runtime_id") != "track-a-canonical-live":
        raise InvalidationError("lease_schema_invalid")
    if lease.get("status") != "active" or lease.get("controller_task") != task_id or lease.get("controller_session") != session_id:
        raise InvalidationError("lease_identity_invalid")
    generation = lease.get("generation")
    expires_at = lease.get("expires_at")
    if not isinstance(generation, int) or generation < 1 or not isinstance(expires_at, int):
        raise InvalidationError("lease_state_invalid")
    if expires_at <= int(time.time()):
        raise InvalidationError("lease_expired")
    if registration_lease_generation >= generation:
        raise InvalidationError("registration_lease_not_stale")
    return generation


def _validate_preflight(preflight: dict[str, Any], registration: dict[str, Any]) -> None:
    required = {
        "client_size": EXPECTED_SIZE,
        "client_sha256": EXPECTED_SHA,
        "candidate_count": 0,
        "main_window_count": 0,
    }
    for key, expected in required.items():
        if preflight.get(key) != expected:
            raise InvalidationError(f"preflight_{key}_invalid")
    if preflight.get("display") != registration.get("display"):
        raise InvalidationError("preflight_display_changed")
    if preflight.get("boot_id_sha256") != registration.get("boot_id_sha256"):
        raise InvalidationError("registration_boot_not_current")
    container_id = preflight.get("container_id")
    if not isinstance(container_id, str) or len(container_id) != 64 or any(ch not in "0123456789abcdef" for ch in container_id.lower()):
        raise InvalidationError("preflight_container_invalid")


def _collect_zero_client(worker: ModuleType, registration: dict[str, Any], *, code: str) -> dict[str, Any]:
    try:
        preflight = worker.collect_preflight()
    except Exception as exc:
        raise InvalidationError(code) from exc
    if not isinstance(preflight, dict):
        raise InvalidationError(f"{code}_invalid")
    _validate_preflight(preflight, registration)
    return preflight


def _registered_identity_absent(
    worker: ModuleType,
    registration: dict[str, Any],
    preflight: dict[str, Any],
) -> dict[str, Any]:
    try:
        identity = worker.process_identity(str(preflight["container_id"]), int(registration["pid"]))
    except Exception as exc:
        raise InvalidationError("registered_process_identity_unverifiable") from exc
    if not isinstance(identity, dict) or not isinstance(identity.get("present"), bool):
        raise InvalidationError("registered_process_identity_unverifiable")
    if identity["present"] is True:
        raise InvalidationError("registered_process_still_present")
    return identity


def invalidate(
    *,
    state_dir: Path,
    task_id: str,
    session_id: str,
    worker: ModuleType,
    run_id: str,
) -> dict[str, Any]:
    _require_external_guard(state_dir)
    registration_path = state_dir / REGISTRATION_NAME
    lease_path = state_dir / LEASE_NAME

    registration, registration_raw = _private_json(registration_path)
    _validate_registration(registration)
    lease, lease_raw = _private_json(lease_path)
    generation = _validate_lease(lease, task_id, session_id, int(registration["lease_generation"]))

    preflight = _collect_zero_client(worker, registration, code="zero_client_preflight_failed")
    registered_identity = _registered_identity_absent(worker, registration, preflight)

    # Repeat every mutable proof immediately before the atomic metadata commit.
    registration_again, registration_raw_again = _private_json(registration_path)
    lease_again, lease_raw_again = _private_json(lease_path)
    if registration_raw_again != registration_raw or registration_again != registration:
        raise InvalidationError("registration_drift")
    if lease_raw_again != lease_raw or lease_again != lease:
        raise InvalidationError("lease_drift")
    _validate_lease(lease_again, task_id, session_id, int(registration["lease_generation"]))
    preflight_again = _collect_zero_client(worker, registration, code="zero_client_precommit_preflight_failed")
    if preflight_again != preflight:
        raise InvalidationError("zero_client_preflight_drift")
    registered_identity_again = _registered_identity_absent(worker, registration, preflight_again)
    if registered_identity_again != registered_identity:
        raise InvalidationError("registered_process_identity_drift")

    safe_run = "".join(ch for ch in run_id if ch.isalnum() or ch in "-_")[:80]
    if not safe_run:
        raise InvalidationError("run_id_invalid")
    tombstone = state_dir / f"runtime-registration.invalidated-same-boot-zero-client.{safe_run}.json"
    if tombstone.exists():
        raise InvalidationError("invalidation_tombstone_exists")

    os.replace(registration_path, tombstone)
    os.chmod(tombstone, 0o600)
    _fsync_dir(state_dir)
    if registration_path.exists():
        raise InvalidationError("registration_invalidation_commit_failed")
    if tombstone.read_bytes() != registration_raw:
        raise InvalidationError("invalidation_tombstone_mismatch")

    # Post-commit failure must stay fail-closed: never restore a stale registration.
    postflight = _collect_zero_client(worker, registration, code="zero_client_postcommit_preflight_failed")
    if postflight != preflight:
        raise InvalidationError("zero_client_postcommit_preflight_drift")
    post_identity = _registered_identity_absent(worker, registration, postflight)
    if post_identity != registered_identity:
        raise InvalidationError("registered_process_postcommit_identity_drift")
    lease_after, lease_raw_after = _private_json(lease_path)
    if lease_after != lease or lease_raw_after != lease_raw:
        raise InvalidationError("lease_postcommit_drift")
    _validate_lease(lease_after, task_id, session_id, int(registration["lease_generation"]))

    return {
        "schema": "otclient.track-a.same-boot-zero-client-invalidation.v1",
        "recovery_mode": RECOVERY_MODE,
        "lease_generation": generation,
        "registration_generation": registration["registration_generation"],
        "registration_lease_generation": registration["lease_generation"],
        "boot_id_sha256": registration["boot_id_sha256"],
        "candidate_count": preflight["candidate_count"],
        "main_window_count": preflight["main_window_count"],
        "tombstone_name": tombstone.name,
        "tombstone_sha256": hashlib.sha256(tombstone.read_bytes()).hexdigest(),
        "credential_accessed": False,
        "client_process_mutation": False,
        "canonical_registration": "ABSENT",
    }


def _write_result(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, sort_keys=True, separators=(",", ":"))
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--worker", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        worker = _load_worker(args.worker)
        payload = invalidate(
            state_dir=STATE_DIR,
            task_id=args.task_id,
            session_id=args.session_id,
            worker=worker,
            run_id=os.environ.get("GITHUB_RUN_ID", "local"),
        )
        _write_result(args.result, payload)
        print("TRACK_A_SAME_BOOT_ZERO_CLIENT_INVALIDATION=PASS")
        print("NO_CREDENTIAL_ACCESS=true")
        return 0
    except (InvalidationError, OSError, ValueError) as exc:
        print(f"TRACK_A_SAME_BOOT_ZERO_CLIENT_INVALIDATION_ERROR={getattr(exc, 'args', ['failure'])[0]}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
