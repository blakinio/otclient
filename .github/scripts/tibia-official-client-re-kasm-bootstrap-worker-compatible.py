#!/usr/bin/env python3
"""Kasm bootstrap entrypoint scoped to the canonical Track A container."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import shlex
import sys
import time
from types import ModuleType
from typing import Any, Callable, Sequence

BASE_PATH = Path(__file__).with_name("tibia-official-client-re-kasm-bootstrap-worker.py")
CANONICAL_CONTAINER = "otclient-track-a-kasmvnc"


def _load_base() -> ModuleType:
    spec = importlib.util.spec_from_file_location("track_a_kasm_bootstrap_worker_scoped_base", BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("bootstrap_worker_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_base = _load_base()
if _base.TARGET_CONTAINER != CANONICAL_CONTAINER:
    raise RuntimeError("canonical_container_contract_mismatch")
_original_candidate_rows = _base.candidate_rows


def exact_candidates(
    containers: list[tuple[str, str]],
    runner: Callable[[Sequence[str]], str] = _base.run,
) -> list[dict[str, Any]]:
    """Deep-scan only the one canonical Kasm container."""
    target = [(container_id, name) for container_id, name in containers if name == CANONICAL_CONTAINER]
    if len(target) != 1:
        raise _base.WorkerError(f"target_container_count:{len(target)}")
    return _original_candidate_rows(target[0][0], runner)


_base.exact_candidates = exact_candidates


def _launch_command(container_id: str) -> list[str]:
    """Return the plain exact-client launch shape already proven by the login worker."""
    launch_script = f"cd {shlex.quote(_base.PACKAGE_DIR)} && exec ./client"
    return [
        "docker", "exec", "-d", "-u", _base.TARGET_USER, "-w", _base.PACKAGE_DIR,
        "-e", f"HOME={_base.HOME_DIR}",
        "-e", f"DISPLAY={_base.TARGET_DISPLAY}",
        "-e", f"XAUTHORITY={_base.HOME_DIR}/.Xauthority",
        "-e", f"LD_LIBRARY_PATH={_base.PACKAGE_DIR}:{_base.PACKAGE_DIR}/lib",
        container_id,
        "/usr/bin/env",
        "-u", "RUNNER_TRACKING_ID",
        "-u", "TIBIA_TEST_EMAIL",
        "-u", "TIBIA_TEST_PASSWORD",
        "-u", "TRACK_A_CANONICAL_LEASE_TOKEN",
        "-u", "TRACK_A_CANONICAL_LEASE_TOKEN_FILE",
        "-u", "LD_PRELOAD",
        "-u", "OTCLIENT_TIBIA_RE_SOCKET",
        "-u", "OTCLIENT_TIBIA_RE_AUTH_SOCKET",
        "-u", "OTCLIENT_TIBIA_RE_CHARACTER_SOCKET",
        "-u", "OTCLIENT_TIBIA_RE_BINARY_SHA256",
        "-u", "OTCLIENT_TIBIA_RE_CLIENT_VERSION",
        "-u", "OTCLIENT_TIBIA_RE_TARGETS",
        "sh", "-lc", launch_script,
    ]


def launch_from_preflight(
    path: Path,
    runner: Callable[[Sequence[str]], str] = _base.run,
    sleeper: Callable[[float], None] = time.sleep,
    attempts: int = 80,
) -> dict[str, Any]:
    """Launch one plain exact client and return only after its Tibia window exists."""
    saved = _base.read_record(path, _base.PREFLIGHT_SCHEMA)
    _base._validate_preflight(saved)
    fresh = _base.collect_preflight(runner)
    if fresh != saved:
        raise _base.WorkerError("preflight_drift")
    container_id = str(saved["container_id"])
    runner(_launch_command(container_id))

    candidate: dict[str, Any] | None = None
    for _ in range(max(1, attempts)):
        containers = _base.docker_containers(runner)
        try:
            current_target = _base._target(containers)
        except _base.WorkerError as exc:
            raise _base.WorkerError("postlaunch_target_not_unique") from exc
        found = exact_candidates(containers, runner)
        if len(found) > 1:
            raise _base.WorkerError("postlaunch_target_not_unique")
        if len(found) == 1:
            candidate = found[0]
            if candidate.get("container_id") != container_id or current_target != container_id:
                raise _base.WorkerError("postlaunch_target_not_unique")
            break
        sleeper(0.25)
    if candidate is None:
        raise _base.WorkerError("postlaunch_target_not_unique")
    if candidate.get("exe") != _base.CLIENT_PATH or candidate.get("size") != _base.SIZE or candidate.get("sha256") != _base.SHA:
        raise _base.WorkerError("postlaunch_identity_mismatch")
    pid = candidate.get("pid")
    start = candidate.get("start_ticks")
    if not isinstance(pid, int) or pid < 2 or not isinstance(start, int) or start < 1:
        raise _base.WorkerError("postlaunch_identity_mismatch")

    launch = {
        "schema": _base.LAUNCH_SCHEMA,
        "preflight_fingerprint": saved["preflight_fingerprint"],
        "container_name": _base.TARGET_CONTAINER,
        "container_id": container_id,
        "display": _base.TARGET_DISPLAY,
        "package_dir": _base.PACKAGE_DIR,
        "client_path": _base.CLIENT_PATH,
        "client_size": _base.SIZE,
        "client_sha256": _base.SHA,
        "pid": pid,
        "process_start_ticks": start,
        "launch_method": _base.LAUNCH_METHOD,
        "bootstrap_helper_residue": False,
    }
    # Persist the exact launch identity before waiting for GUI readiness so the
    # canonical transition can always execute identity-bound rollback on timeout.
    _base.write_record(path, launch)

    for _ in range(max(1, attempts)):
        current = _base.process_identity(container_id, pid, runner)
        if current.get("present") is not True or current.get("unverifiable") is True:
            raise _base.WorkerError("postlaunch_identity_drift")
        expected = {
            "pid": pid,
            "exe": _base.CLIENT_PATH,
            "size": _base.SIZE,
            "sha256": _base.SHA,
            "start_ticks": start,
        }
        if any(current.get(key) != value for key, value in expected.items()):
            raise _base.WorkerError("postlaunch_identity_drift")
        windows = _base._window_count(container_id, runner)
        if windows > 1:
            raise _base.WorkerError(f"main_window_count:{windows}")
        if windows == 1:
            return launch
        sleeper(0.25)
    raise _base.WorkerError("postlaunch_window_not_ready")


_base.launch_from_preflight = launch_from_preflight

WorkerError = _base.WorkerError
VER = _base.VER
SIZE = _base.SIZE
SHA = _base.SHA
collect_preflight = _base.collect_preflight
process_identity = _base.process_identity


def main(argv: Sequence[str] | None = None) -> int:
    return int(_base.main(argv))


if __name__ == "__main__":
    raise SystemExit(main())
