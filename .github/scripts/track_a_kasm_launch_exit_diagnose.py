#!/usr/bin/env python3
"""One-shot sanitized launch/exit diagnostic for the canonical Track A Kasm client."""
from __future__ import annotations

import argparse
import fcntl
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from types import ModuleType
from typing import Any, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

WORKER_PATH = Path(__file__).with_name("tibia-official-client-re-kasm-bootstrap-worker-compatible.py")
STATE_DIR = Path("/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime")
REGISTRATION = STATE_DIR / "runtime-registration.json"
LOCK_PATH = STATE_DIR / "coordination.lock"
GUARD_ENV = "TRACK_A_KASM_LAUNCH_EXIT_DIAGNOSTIC_GUARDED"
TASK_ROOT = "/tmp/otclient-kasm-launch-exit-diagnostic"
PID_FILE = TASK_ROOT + "/client.pid"
RC_FILE = TASK_ROOT + "/client.rc"
STDOUT_FILE = TASK_ROOT + "/client.stdout"
STDERR_FILE = TASK_ROOT + "/client.stderr"
STATUS_SCRIPT = r'''
import json,pathlib,re,sys
root=pathlib.Path(sys.argv[1])
def text(name):
    try: return (root/name).read_text(encoding='utf-8',errors='replace').strip()
    except OSError: return ''
def payload_bytes(name):
    try:
        data=(root/name).read_bytes()
    except OSError:
        return b''
    return data[:1048577]
pid=text('client.pid'); rc=text('client.rc')
out=payload_bytes('client.stdout'); err=payload_bytes('client.stderr')
if len(err)>1048576:
    cls='stderr_too_large'
else:
    lower=err.decode('utf-8','replace').lower()
    if not err: cls='stderr_empty'
    elif 'error while loading shared libraries' in lower or 'cannot open shared object file' in lower: cls='loader_error'
    elif 'could not connect to display' in lower or 'cannot connect to display' in lower: cls='display_error'
    elif 'could not load the qt platform plugin' in lower or 'qt.qpa.plugin' in lower: cls='qt_platform_error'
    elif 'no such file or directory' in lower: cls='missing_file'
    elif 'permission denied' in lower: cls='permission_denied'
    elif 'segmentation fault' in lower: cls='segmentation_fault'
    elif 'aborted' in lower: cls='aborted'
    else: cls='stderr_other'
print(json.dumps({
    'pid': int(pid) if pid.isdigit() else None,
    'rc': int(rc) if re.fullmatch(r'-?[0-9]+',rc or '') else None,
    'stdout_nonempty': bool(out),
    'stdout_bytes': min(len(out),1048576),
    'stderr_nonempty': bool(err),
    'stderr_bytes': min(len(err),1048576),
    'stderr_class': cls,
},sort_keys=True,separators=(',',':')))
'''


class DiagnosticError(RuntimeError):
    pass


def _load_worker() -> ModuleType:
    spec = importlib.util.spec_from_file_location("track_a_launch_exit_worker", WORKER_PATH)
    if spec is None or spec.loader is None:
        raise DiagnosticError("worker_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise DiagnosticError("worker_import_failed") from exc
    if module._base.TARGET_CONTAINER != "otclient-track-a-kasmvnc":
        raise DiagnosticError("canonical_container_contract_mismatch")
    if not str(module.CLIENT_DIR).endswith("/packages/Tibia/bin"):
        raise DiagnosticError("client_dir_contract_mismatch")
    return module


def _require_external_guard() -> None:
    if os.environ.get(GUARD_ENV) != "1":
        raise DiagnosticError("canonical_guard_required")
    try:
        fd = os.open(LOCK_PATH, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0))
    except OSError as exc:
        raise DiagnosticError("canonical_guard_required") from exc
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
    raise DiagnosticError("canonical_guard_required")


def _run(command: Sequence[str], *, timeout: int = 20) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            list(command), check=False, text=True, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout,
            close_fds=True,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise DiagnosticError("host_command_failed") from exc


def _docker_success(command: Sequence[str], code: str, *, timeout: int = 20) -> str:
    result = _run(command, timeout=timeout)
    if result.returncode != 0:
        raise DiagnosticError(code)
    return result.stdout


def _status(worker: ModuleType) -> dict[str, Any]:
    raw = _docker_success([
        "docker", "exec", worker._base.TARGET_CONTAINER,
        "python3", "-c", STATUS_SCRIPT, TASK_ROOT,
    ], "diagnostic_status_unavailable")
    try:
        data = json.loads(raw.strip())
    except json.JSONDecodeError as exc:
        raise DiagnosticError("diagnostic_status_invalid") from exc
    allowed_classes = {
        "stderr_empty", "stderr_too_large", "loader_error", "display_error",
        "qt_platform_error", "missing_file", "permission_denied",
        "segmentation_fault", "aborted", "stderr_other",
    }
    if not isinstance(data, dict) or data.get("stderr_class") not in allowed_classes:
        raise DiagnosticError("diagnostic_status_invalid")
    for key in ("stdout_nonempty", "stderr_nonempty"):
        if not isinstance(data.get(key), bool):
            raise DiagnosticError("diagnostic_status_invalid")
    for key in ("stdout_bytes", "stderr_bytes"):
        if not isinstance(data.get(key), int) or not 0 <= data[key] <= 1048576:
            raise DiagnosticError("diagnostic_status_invalid")
    if data.get("pid") is not None and (not isinstance(data["pid"], int) or data["pid"] < 2):
        raise DiagnosticError("diagnostic_status_invalid")
    if data.get("rc") is not None and not isinstance(data["rc"], int):
        raise DiagnosticError("diagnostic_status_invalid")
    return data


def _launch(worker: ModuleType) -> None:
    base = worker._base
    client_dir = str(worker.CLIENT_DIR)
    # The wrapper writes PID/exit status and captures raw output only inside a private
    # task-local directory. Raw output is never emitted by this diagnostic.
    script = (
        f"umask 077; rm -rf {TASK_ROOT}; mkdir -p {TASK_ROOT}; "
        f": > {STDOUT_FILE}; : > {STDERR_FILE}; "
        f"./client >{STDOUT_FILE} 2>{STDERR_FILE} & p=$!; "
        f"printf '%s\\n' \"$p\" >{PID_FILE}; "
        f"wait \"$p\"; r=$?; printf '%s\\n' \"$r\" >{RC_FILE}"
    )
    legacy_email, legacy_password = "TIBIA_TEST_EMAIL", "TIBIA_TEST_PASSWORD"
    command = [
        "docker", "exec", "-d", "-u", base.TARGET_USER, "-w", client_dir,
        "-e", f"HOME={base.HOME_DIR}",
        "-e", f"DISPLAY={base.TARGET_DISPLAY}",
        "-e", f"XAUTHORITY={base.HOME_DIR}/.Xauthority",
        "-e", f"LD_LIBRARY_PATH={client_dir}:{client_dir}/lib",
        base.TARGET_CONTAINER,
        "/usr/bin/env",
        "-u", "RUNNER_TRACKING_ID",
        "-u", legacy_email,
        "-u", legacy_password,
        "-u", "TRACK_A_CANONICAL_LEASE_TOKEN",
        "-u", "TRACK_A_CANONICAL_LEASE_TOKEN_FILE",
        "-u", "LD_PRELOAD",
        "-u", "OTCLIENT_TIBIA_RE_SOCKET",
        "-u", "OTCLIENT_TIBIA_RE_AUTH_SOCKET",
        "-u", "OTCLIENT_TIBIA_RE_CHARACTER_SOCKET",
        "-u", "OTCLIENT_TIBIA_RE_BINARY_SHA256",
        "-u", "OTCLIENT_TIBIA_RE_CLIENT_VERSION",
        "-u", "OTCLIENT_TIBIA_RE_TARGETS",
        "sh", "-lc", script,
    ]
    result = _run(command)
    if result.returncode != 0:
        raise DiagnosticError("docker_exec_launch_failed")


def _exact_candidates(worker: ModuleType) -> list[dict[str, Any]]:
    containers = worker._base.docker_containers()
    rows = worker.exact_candidates(containers)
    return rows


def _cleanup(worker: ModuleType) -> None:
    base = worker._base
    rows = _exact_candidates(worker)
    if len(rows) > 2:
        raise DiagnosticError("cleanup_candidate_count_unbounded")
    for row in rows:
        pid = row.get("pid")
        if row.get("container_id") is None or not isinstance(pid, int) or pid < 2:
            raise DiagnosticError("cleanup_identity_unproven")
        result = _run([
            "docker", "exec", "-u", base.TARGET_USER, base.TARGET_CONTAINER,
            "kill", "-TERM", str(pid),
        ])
        if result.returncode != 0:
            raise DiagnosticError("cleanup_sigterm_failed")
    deadline = time.monotonic() + 8.0
    while time.monotonic() < deadline:
        if not _exact_candidates(worker):
            break
        time.sleep(0.25)
    remaining = _exact_candidates(worker)
    for row in remaining:
        pid = row.get("pid")
        if not isinstance(pid, int) or pid < 2:
            raise DiagnosticError("cleanup_identity_unproven")
        result = _run([
            "docker", "exec", "-u", base.TARGET_USER, base.TARGET_CONTAINER,
            "kill", "-KILL", str(pid),
        ])
        if result.returncode != 0:
            raise DiagnosticError("cleanup_sigkill_failed")
    deadline = time.monotonic() + 4.0
    while time.monotonic() < deadline and _exact_candidates(worker):
        time.sleep(0.25)
    if _exact_candidates(worker):
        raise DiagnosticError("cleanup_exact_candidate_remaining")


def diagnose(result_path: Path, *, seconds: float = 20.0) -> None:
    _require_external_guard()
    worker = _load_worker()
    if REGISTRATION.exists():
        raise DiagnosticError("canonical_registration_present")
    initial = worker.collect_preflight()
    if initial.get("candidate_count") != 0 or initial.get("main_window_count") != 0:
        raise DiagnosticError("initial_zero_state_unproven")

    outcome = "unknown"
    observed: dict[str, Any] = {
        "pid": None, "rc": None, "stdout_nonempty": False, "stdout_bytes": 0,
        "stderr_nonempty": False, "stderr_bytes": 0, "stderr_class": "stderr_empty",
    }
    window_ready = False
    launch_pid_proven = False
    try:
        _launch(worker)
        deadline = time.monotonic() + max(2.0, min(seconds, 30.0))
        while time.monotonic() < deadline:
            observed = _status(worker)
            pid = observed.get("pid")
            if isinstance(pid, int):
                identity = worker.process_identity(str(initial["container_id"]), pid)
                if identity.get("present") is True and identity.get("unverifiable") is not True:
                    exact = (
                        identity.get("exe") == worker._base.CLIENT_PATH
                        and identity.get("size") == worker._base.SIZE
                        and identity.get("sha256") == worker._base.SHA
                    )
                    if not exact:
                        raise DiagnosticError("launched_pid_identity_mismatch")
                    launch_pid_proven = True
            windows = worker._base._window_count(str(initial["container_id"]))
            if windows > 1:
                raise DiagnosticError("diagnostic_window_count_unbounded")
            if windows == 1:
                window_ready = True
                outcome = "window_ready"
                break
            if observed.get("rc") is not None:
                outcome = "process_exited"
                break
            time.sleep(0.25)
        else:
            outcome = "alive_no_window" if launch_pid_proven else "pid_not_observed"
    finally:
        _cleanup(worker)

    if REGISTRATION.exists():
        raise DiagnosticError("canonical_registration_created")
    final = worker.collect_preflight()
    if final != initial:
        raise DiagnosticError("postcleanup_zero_state_drift")

    payload = {
        "schema": "otclient.track-a.kasm-launch-exit-diagnostic.v1",
        "outcome": outcome,
        "launch_pid_observed": observed.get("pid") is not None,
        "launch_pid_exact_proven": launch_pid_proven,
        "exit_code": observed.get("rc"),
        "window_ready": window_ready,
        "stdout_nonempty": observed["stdout_nonempty"],
        "stdout_bytes": observed["stdout_bytes"],
        "stderr_nonempty": observed["stderr_nonempty"],
        "stderr_bytes": observed["stderr_bytes"],
        "stderr_class": observed["stderr_class"],
        "canonical_registration": "ABSENT",
        "final_candidate_count": 0,
        "final_main_window_count": 0,
        "credential_access": False,
    }
    result_path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(result_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, sort_keys=True, separators=(",", ":"))
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    print("TRACK_A_KASM_LAUNCH_EXIT_DIAGNOSTIC=PASS")
    print(f"LAUNCH_OUTCOME={outcome}")
    print(f"LAUNCH_PID_OBSERVED={'true' if payload['launch_pid_observed'] else 'false'}")
    print(f"LAUNCH_PID_EXACT_PROVEN={'true' if launch_pid_proven else 'false'}")
    print("EXIT_CODE=" + (str(payload["exit_code"]) if payload["exit_code"] is not None else "UNKNOWN"))
    print(f"WINDOW_READY={'true' if window_ready else 'false'}")
    print(f"STDOUT_NONEMPTY={'true' if payload['stdout_nonempty'] else 'false'}")
    print(f"STDERR_NONEMPTY={'true' if payload['stderr_nonempty'] else 'false'}")
    print(f"STDERR_CLASS={payload['stderr_class']}")
    print("CLEANUP_ZERO_STATE=PASS")
    print("CANONICAL_REGISTRATION=ABSENT")
    print("CREDENTIAL_ACCESS=false")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--seconds", type=float, default=20.0)
    args = parser.parse_args(argv)
    try:
        diagnose(args.result, seconds=args.seconds)
        return 0
    except (DiagnosticError, OSError, ValueError) as exc:
        code = str(exc.args[0] if exc.args else "diagnostic_failure")
        if re.fullmatch(r"[a-z0-9_]+", code) is None:
            code = "diagnostic_failure"
        print(f"TRACK_A_KASM_LAUNCH_EXIT_DIAGNOSTIC_ERROR={code}", file=sys.stderr)
        print("CREDENTIAL_ACCESS=false")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
