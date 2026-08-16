#!/usr/bin/env python3
"""Fail-closed Track A canonical live bootstrap, rebind and Gate B transitions."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
from typing import Any, Sequence

STATE_DIR = Path("/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime")
REGISTRATION = STATE_DIR / "runtime-registration.json"
LEASE_IMPL = Path(__file__).with_name("tibia-official-client-re-canonical-live-lease.py")
RUNTIME_ID = "track-a-canonical-live"
EXPECTED_VERSION = "15.32.df7b29"
EXPECTED_SIZE = 51965216
EXPECTED_SHA256 = "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"
ALLOWED_STATES = {"LOGIN", "CHARACTER_SELECT", "IN_GAME", "DISCONNECTED", "UNKNOWN"}
REQUIRED_REGISTRATION_FIELDS = {
    "schema_version", "runtime_id", "registration_generation", "lease_generation",
    "registered_at", "boot_id_sha256", "pid", "process_start_ticks", "client_version",
    "client_size", "client_sha256", "display", "window_identity", "remote_view_endpoint",
    "remote_view_mapping", "state", "source_task", "source_run",
}


class TransitionError(RuntimeError):
    def __init__(self, code: str, message: str = "") -> None:
        super().__init__(message or code)
        self.code = code


def _load_lease_module():
    spec = importlib.util.spec_from_file_location("track_a_canonical_lease", LEASE_IMPL)
    if spec is None or spec.loader is None:
        raise TransitionError("lease_module_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb", buffering=0) as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _boot_id_sha256() -> str:
    raw = Path("/proc/sys/kernel/random/boot_id").read_text(encoding="ascii").strip().encode()
    return hashlib.sha256(raw).hexdigest()


def _proc_start_ticks(pid: int) -> int:
    raw = Path(f"/proc/{pid}/stat").read_text(encoding="ascii")
    close = raw.rfind(")")
    if close < 0:
        raise TransitionError("proc_stat_invalid")
    fields = raw[close + 2 :].split()
    if len(fields) < 20:
        raise TransitionError("proc_stat_invalid")
    return int(fields[19])


def _exe_path(pid: int) -> Path:
    try:
        return Path(os.readlink(f"/proc/{pid}/exe"))
    except OSError as exc:
        raise TransitionError("client_exe_unreadable", str(exc)) from exc


def _identity(pid: int) -> dict[str, Any]:
    exe = _exe_path(pid)
    st = exe.stat()
    return {
        "boot_id_sha256": _boot_id_sha256(),
        "pid": pid,
        "process_start_ticks": _proc_start_ticks(pid),
        "client_size": st.st_size,
        "client_sha256": _sha256(exe),
    }


def _exact_identity(identity: dict[str, Any]) -> None:
    if identity["client_size"] != EXPECTED_SIZE:
        raise TransitionError("client_size_mismatch")
    if identity["client_sha256"] != EXPECTED_SHA256:
        raise TransitionError("client_sha256_mismatch")


def _candidate_pids() -> list[int]:
    result: list[int] = []
    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit():
            continue
        pid = int(entry.name)
        try:
            exe = _exe_path(pid)
            st = exe.stat()
        except (OSError, TransitionError):
            continue
        plausible = "CipSoft GmbH/Tibia/packages/Tibia" in str(exe)
        if not plausible and st.st_size != EXPECTED_SIZE:
            continue
        try:
            sha = _sha256(exe)
        except OSError:
            if plausible:
                result.append(pid)
            continue
        if plausible or (st.st_size == EXPECTED_SIZE and sha == EXPECTED_SHA256):
            result.append(pid)
    return sorted(set(result))


def _read_registration() -> dict[str, Any] | None:
    if not REGISTRATION.exists():
        return None
    st = REGISTRATION.lstat()
    owner_ok = not hasattr(os, "getuid") or st.st_uid == os.getuid()
    if not REGISTRATION.is_file() or REGISTRATION.is_symlink() or (st.st_mode & 0o777) != 0o600 or not owner_ok:
        raise TransitionError("registration_file_unsafe")
    try:
        data = json.loads(REGISTRATION.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TransitionError("registration_invalid_json", str(exc)) from exc
    if not isinstance(data, dict) or not REQUIRED_REGISTRATION_FIELDS.issubset(data):
        raise TransitionError("registration_schema_invalid")
    if data.get("schema_version") != 1 or data.get("runtime_id") != RUNTIME_ID:
        raise TransitionError("registration_schema_invalid")
    if data.get("client_version") != EXPECTED_VERSION or data.get("client_size") != EXPECTED_SIZE or data.get("client_sha256") != EXPECTED_SHA256:
        raise TransitionError("registration_client_fence_invalid")
    if data.get("state") not in ALLOWED_STATES or data.get("remote_view_mapping") not in {"PROVEN", "UNKNOWN"}:
        raise TransitionError("registration_state_invalid")
    if not isinstance(data.get("registration_generation"), int) or int(data["registration_generation"]) < 1:
        raise TransitionError("registration_generation_invalid")
    if not isinstance(data.get("lease_generation"), int) or int(data["lease_generation"]) < 1:
        raise TransitionError("registration_lease_generation_invalid")
    return data


def _atomic_registration(data: dict[str, Any]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, tmp_name = tempfile.mkstemp(prefix=".runtime-registration.", dir=STATE_DIR)
    tmp = Path(tmp_name)
    try:
        os.fchmod(fd, 0o600)
        payload = (json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n").encode()
        with os.fdopen(fd, "wb", closefd=True) as fh:
            fh.write(payload)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, REGISTRATION)
        dir_fd = os.open(STATE_DIR, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass


def _load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TransitionError("probe_manifest_invalid", str(exc)) from exc
    if not isinstance(data, dict):
        raise TransitionError("probe_manifest_invalid")
    required = {"pid", "display", "window_identity", "remote_view_endpoint", "remote_view_mapping", "state"}
    if not required.issubset(data):
        raise TransitionError("probe_manifest_missing_fields")
    if not isinstance(data["pid"], int) or data["pid"] < 2:
        raise TransitionError("probe_pid_invalid")
    if not isinstance(data["display"], str) or not data["display"].startswith(":"):
        raise TransitionError("probe_display_invalid")
    if not isinstance(data["window_identity"], str) or not data["window_identity"]:
        raise TransitionError("probe_window_invalid")
    if data["remote_view_mapping"] not in {"PROVEN", "UNKNOWN"}:
        raise TransitionError("probe_remote_view_invalid")
    if data["state"] not in ALLOWED_STATES:
        raise TransitionError("probe_state_invalid")
    return data


def _manifest_matches_registration(manifest: dict[str, Any], registration: dict[str, Any]) -> None:
    for key in ("pid", "display", "window_identity", "remote_view_endpoint", "remote_view_mapping", "state"):
        if manifest.get(key) != registration.get(key):
            raise TransitionError(f"probe_registration_{key}_mismatch")
    current = _identity(int(registration["pid"]))
    _exact_identity(current)
    for key in ("boot_id_sha256", "pid", "process_start_ticks"):
        if current[key] != registration.get(key):
            raise TransitionError(f"registered_identity_{key}_mismatch")


def _sanitized_env() -> dict[str, str]:
    env = dict(os.environ)
    for key in list(env):
        upper = key.upper()
        if "CAPABILITY" in upper or "LEASE_TOKEN" in upper or key in {"TRACK_A_CANONICAL_LEASE_TOKEN", "TRACK_A_CANONICAL_LEASE_TOKEN_FILE"}:
            env.pop(key, None)
    return env


def _run_probe(worker: Path, manifest: Path) -> dict[str, Any]:
    try:
        manifest.unlink()
    except FileNotFoundError:
        pass
    completed = subprocess.run([str(worker), "probe", str(manifest)], check=False, env=_sanitized_env(), close_fds=True)
    if completed.returncode != 0:
        raise TransitionError("probe_failed")
    return _load_manifest(manifest)


def _terminate_group(pgid: int) -> None:
    try:
        os.killpg(pgid, signal.SIGTERM)
    except ProcessLookupError:
        return
    deadline = time.monotonic() + 4
    while time.monotonic() < deadline:
        try:
            os.killpg(pgid, 0)
        except ProcessLookupError:
            return
        time.sleep(0.1)
    try:
        os.killpg(pgid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def _validate_lease_locked(manager: Any, lease: Any, task_id: str, session_id: str, token_file: Path) -> tuple[Any, int]:
    token = lease._read_private_token(token_file)
    identity = lease.LeaseIdentity(task_id, session_id)
    state = manager._load_state_unlocked()
    manager._require_current_unlocked(state, identity, token, lease._now_epoch(None))
    assert state is not None
    return identity, int(state["generation"])


def _lease_recheck_locked(manager: Any, lease: Any, identity: Any, token_file: Path, expected_generation: int) -> None:
    token = lease._read_private_token(token_file)
    state = manager._load_state_unlocked()
    manager._require_current_unlocked(state, identity, token, lease._now_epoch(None))
    if state is None or int(state["generation"]) != expected_generation:
        raise TransitionError("lease_generation_changed")


def _source_run() -> str:
    return os.environ.get("GITHUB_RUN_ID") or "manual-unknown"


def bootstrap(args: argparse.Namespace) -> None:
    lease = _load_lease_module()
    manager = lease.LeaseManager(STATE_DIR)
    manifest_path = STATE_DIR / ".bootstrap-manifest.json"
    post_path = STATE_DIR / ".bootstrap-post-manifest.json"
    child: subprocess.Popen[bytes] | None = None
    registration_written = False
    success = False
    generation = 0
    with manager.locked():
        identity, generation = _validate_lease_locked(manager, lease, args.task_id, args.session_id, args.token_file)
        if _read_registration() is not None:
            raise TransitionError("registration_already_present")
        if _candidate_pids():
            raise TransitionError("official_client_candidate_present")
        STATE_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
        for path in (manifest_path, post_path):
            try:
                path.unlink()
            except FileNotFoundError:
                pass
        try:
            child = subprocess.Popen(
                [str(args.worker), "bootstrap", str(manifest_path)],
                env=_sanitized_env(), close_fds=True, start_new_session=True,
            )
            rc = child.wait(timeout=args.worker_timeout)
            if rc != 0:
                raise TransitionError("bootstrap_worker_failed", f"rc={rc}")
            manifest = _load_manifest(manifest_path)
            if not isinstance(manifest.get("process_group_id"), int) or int(manifest["process_group_id"]) != child.pid:
                raise TransitionError("bootstrap_process_group_invalid")
            current = _identity(int(manifest["pid"]))
            _exact_identity(current)
            if _candidate_pids() != [int(manifest["pid"])]:
                raise TransitionError("bootstrap_target_not_unique")
            _lease_recheck_locked(manager, lease, identity, args.token_file, generation)
            record: dict[str, Any] = {
                "schema_version": 1, "runtime_id": RUNTIME_ID,
                "registration_generation": 1, "lease_generation": generation,
                "registered_at": int(time.time()), "boot_id_sha256": current["boot_id_sha256"],
                "pid": current["pid"], "process_start_ticks": current["process_start_ticks"],
                "client_version": EXPECTED_VERSION, "client_size": EXPECTED_SIZE,
                "client_sha256": EXPECTED_SHA256, "display": manifest["display"],
                "window_identity": manifest["window_identity"],
                "remote_view_endpoint": manifest["remote_view_endpoint"],
                "remote_view_mapping": manifest["remote_view_mapping"], "state": manifest["state"],
                "source_task": args.task_id, "source_run": _source_run(),
            }
            _atomic_registration(record)
            registration_written = True
            if _read_registration() != record:
                raise TransitionError("registration_revalidation_failed")
            post = _run_probe(args.worker, post_path)
            _manifest_matches_registration(post, record)
            if _candidate_pids() != [int(record["pid"])]:
                raise TransitionError("bootstrap_uniqueness_changed_before_detach")
            _lease_recheck_locked(manager, lease, identity, args.token_file, generation)
            success = True
        finally:
            if not success:
                if child is not None:
                    _terminate_group(child.pid)
                if registration_written:
                    try:
                        REGISTRATION.unlink()
                    except FileNotFoundError:
                        pass
            for path in (manifest_path, post_path):
                try:
                    path.unlink()
                except FileNotFoundError:
                    pass
    print("TRACK_A_CANONICAL_BOOTSTRAP=PASS")
    print(f"TRACK_A_CANONICAL_LEASE_GENERATION={generation}")


def _probe_registered_locked(args: argparse.Namespace, lease: Any, manager: Any, identity: Any, generation: int, *, permit_rebind: bool) -> tuple[dict[str, Any], dict[str, Any]]:
    registration = _read_registration()
    if registration is None:
        raise TransitionError("registration_absent")
    reg_generation = int(registration["lease_generation"])
    if permit_rebind:
        if reg_generation >= generation:
            raise TransitionError("rebind_generation_not_older")
    elif reg_generation != generation:
        raise TransitionError("registration_generation_mismatch")
    manifest_path = STATE_DIR / ".gate-b-manifest.json"
    try:
        manifest = _run_probe(args.probe, manifest_path)
        _manifest_matches_registration(manifest, registration)
        if _candidate_pids() != [int(registration["pid"])]:
            raise TransitionError("registered_target_not_unique")
        _lease_recheck_locked(manager, lease, identity, args.token_file, generation)
        return registration, manifest
    finally:
        try:
            manifest_path.unlink()
        except FileNotFoundError:
            pass


def rebind(args: argparse.Namespace) -> None:
    lease = _load_lease_module()
    manager = lease.LeaseManager(STATE_DIR)
    with manager.locked():
        identity, generation = _validate_lease_locked(manager, lease, args.task_id, args.session_id, args.token_file)
        registration, manifest = _probe_registered_locked(args, lease, manager, identity, generation, permit_rebind=True)
        updated = dict(registration)
        updated["registration_generation"] = int(registration["registration_generation"]) + 1
        updated["lease_generation"] = generation
        updated["source_task"] = args.task_id
        updated["source_run"] = _source_run()
        for key in ("display", "window_identity", "remote_view_endpoint", "remote_view_mapping", "state"):
            updated[key] = manifest[key]
        _atomic_registration(updated)
        if _read_registration() != updated:
            raise TransitionError("rebind_revalidation_failed")
        final, _ = _probe_registered_locked(args, lease, manager, identity, generation, permit_rebind=False)
        if final != updated:
            raise TransitionError("rebind_final_registration_changed")
    print("TRACK_A_CANONICAL_REBIND=PASS")
    print(f"TRACK_A_CANONICAL_LEASE_GENERATION={generation}")


def gate_b(args: argparse.Namespace) -> None:
    lease = _load_lease_module()
    manager = lease.LeaseManager(STATE_DIR)
    with manager.locked():
        identity, generation = _validate_lease_locked(manager, lease, args.task_id, args.session_id, args.token_file)
        registration, _ = _probe_registered_locked(args, lease, manager, identity, generation, permit_rebind=False)
    print("TRACK_A_CANONICAL_GATE_B=PASS")
    print(f"TRACK_A_CANONICAL_LEASE_GENERATION={generation}")
    print(f"TRACK_A_CANONICAL_RUNTIME_STATE={registration['state']}")


def _common(sub: argparse.ArgumentParser) -> None:
    sub.add_argument("--task-id", required=True)
    sub.add_argument("--session-id", required=True)
    sub.add_argument("--token-file", required=True, type=Path)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    subs = p.add_subparsers(dest="operation", required=True)
    b = subs.add_parser("bootstrap")
    _common(b)
    b.add_argument("--worker-timeout", type=int, default=180)
    b.add_argument("--worker", required=True, type=Path)
    r = subs.add_parser("rebind")
    _common(r)
    r.add_argument("--probe", required=True, type=Path)
    g = subs.add_parser("gate-b")
    _common(g)
    g.add_argument("--probe", required=True, type=Path)
    return p


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        {"bootstrap": bootstrap, "rebind": rebind, "gate-b": gate_b}[args.operation](args)
        return 0
    except TransitionError as exc:
        print(f"TRACK_A_CANONICAL_TRANSITION_ERROR={exc.code}", file=sys.stderr)
        return 2
    except subprocess.TimeoutExpired:
        print("TRACK_A_CANONICAL_TRANSITION_ERROR=worker_timeout", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
