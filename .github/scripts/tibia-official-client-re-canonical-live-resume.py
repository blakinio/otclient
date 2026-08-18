#!/usr/bin/env python3
"""High-level Track A canonical controller resume/release without historical session IDs."""
from __future__ import annotations

import argparse
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence

CANONICAL_STATE = Path("/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime")
TASK_ROOT = Path("/home/runner/_work/_otclient_tibia_re_state/tasks")
REGISTRATION = CANONICAL_STATE / "runtime-registration.json"
LEASE_STATE = CANONICAL_STATE / "lease.json"
SCRIPT_DIR = Path(__file__).resolve().parent
LEASE_WRAPPER = SCRIPT_DIR / "tibia-official-client-re-canonical-live-lease"
HANDOFF = SCRIPT_DIR / "tibia-official-client-re-canonical-live-handoff.py"
TRANSITION = SCRIPT_DIR / "tibia-official-client-re-canonical-live-transition.py"
DEFAULT_PROBE = SCRIPT_DIR / "tibia-official-client-re-canonical-live-session.sh"
IDENT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,199}$")


class ResumeError(RuntimeError):
    def __init__(self, code: str, message: str = "") -> None:
        super().__init__(message or code)
        self.code = code


def _validate_identity(value: str, field: str) -> str:
    if not IDENT_RE.fullmatch(value):
        raise ResumeError("invalid_identity", f"invalid {field}")
    return value


def _derive_session(explicit: str | None) -> str:
    if explicit:
        return _validate_identity(explicit, "session-id")
    run_id = os.environ.get("GITHUB_RUN_ID")
    attempt = os.environ.get("GITHUB_RUN_ATTEMPT")
    job = os.environ.get("GITHUB_JOB")
    if run_id and attempt and job:
        clean_job = re.sub(r"[^A-Za-z0-9._-]+", "-", job).strip("-") or "job"
        return _validate_identity(f"gha-{run_id}-{attempt}-{clean_job}"[:200], "session-id")
    raise ResumeError("session_id_required_outside_github_actions")


def _safe_json(path: Path, *, mode: int = 0o600) -> dict[str, Any] | None:
    if not path.exists():
        return None
    st = path.lstat()
    if not stat.S_ISREG(st.st_mode) or path.is_symlink():
        raise ResumeError("state_file_unsafe")
    if stat.S_IMODE(st.st_mode) != mode:
        raise ResumeError("state_file_permissions")
    if hasattr(os, "getuid") and st.st_uid != os.getuid():
        raise ResumeError("state_file_owner")
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ResumeError("state_file_invalid_json") from exc
    if not isinstance(data, dict):
        raise ResumeError("state_file_invalid_shape")
    return data


def _token_path(task_id: str, lease_state: dict[str, Any] | None) -> Path:
    root = TASK_ROOT / task_id / "runtime"
    slot = None if lease_state is None else lease_state.get("token_slot")
    if slot is not None:
        if not isinstance(slot, str) or not re.fullmatch(r"[A-Za-z0-9._-]{1,120}", slot):
            raise ResumeError("token_slot_invalid")
        return root / slot
    return root / "canonical-lease-token"


def _new_token_path(task_id: str, generation: int) -> Path:
    return TASK_ROOT / task_id / "runtime" / f"canonical-lease-token.g{generation}"


def _run(command: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        command,
        text=True,
        capture_output=capture,
        close_fds=True,
        check=False,
    )
    if completed.returncode:
        if capture and completed.stderr:
            sys.stderr.write(completed.stderr)
        raise ResumeError("subprocess_failed", " ".join(command[:2]))
    return completed


def _lease_status() -> dict[str, Any]:
    completed = _run([str(LEASE_WRAPPER), "status", "--json"], capture=True)
    try:
        data = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise ResumeError("lease_status_invalid_json") from exc
    if not isinstance(data, dict):
        raise ResumeError("lease_status_invalid_shape")
    return data


def _acquire(
    task_id: str,
    session_id: str,
    token_file: Path,
    ttl: int,
    *,
    stale_reason: str | None = None,
) -> None:
    token_file.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    command = [
        str(LEASE_WRAPPER),
        "acquire",
        "--task-id",
        task_id,
        "--session-id",
        session_id,
        "--token-file",
        str(token_file),
        "--ttl-seconds",
        str(ttl),
    ]
    if stale_reason:
        command += ["--stale-takeover-reason", stale_reason]
    _run(command)


def _renew(task_id: str, session_id: str, token_file: Path, ttl: int) -> None:
    _run(
        [
            str(LEASE_WRAPPER),
            "renew",
            "--task-id",
            task_id,
            "--session-id",
            session_id,
            "--token-file",
            str(token_file),
            "--ttl-seconds",
            str(ttl),
        ]
    )


def _handoff(
    task_id: str,
    session_id: str,
    current_token: Path,
    generation: int,
    ttl: int,
    reason: str,
) -> Path:
    target = _new_token_path(task_id, generation + 1)
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    _run(
        [
            sys.executable,
            str(HANDOFF),
            "--task-id",
            task_id,
            "--session-id",
            session_id,
            "--token-file",
            str(current_token),
            "--new-token-file",
            str(target),
            "--expected-generation",
            str(generation),
            "--ttl-seconds",
            str(ttl),
            "--handoff-reason",
            reason,
        ]
    )
    return target


def _transition(
    operation: str,
    task_id: str,
    session_id: str,
    token_file: Path,
    probe: Path,
) -> None:
    _run(
        [
            sys.executable,
            str(TRANSITION),
            operation,
            "--task-id",
            task_id,
            "--session-id",
            session_id,
            "--token-file",
            str(token_file),
            "--probe",
            str(probe),
        ]
    )


def resume(args: argparse.Namespace) -> int:
    task_id = _validate_identity(args.task_id, "task-id")
    session_id = _derive_session(args.session_id)
    public = _lease_status()
    raw = _safe_json(LEASE_STATE)
    status = str(public.get("status") or "absent")
    generation = int(public.get("generation") or 0)
    token_file = _token_path(task_id, raw)

    if status in {"absent", "released"}:
        token_file = TASK_ROOT / task_id / "runtime" / "canonical-lease-token"
        _acquire(task_id, session_id, token_file, args.ttl_seconds)
    elif status == "active" and bool(public.get("expired")):
        if not args.reason:
            raise ResumeError("stale_takeover_reason_required")
        token_file = TASK_ROOT / task_id / "runtime" / "canonical-lease-token"
        _acquire(
            task_id,
            session_id,
            token_file,
            args.ttl_seconds,
            stale_reason=args.reason,
        )
    elif status == "active":
        current_task = str(public.get("controller_task") or "")
        current_session = str(public.get("controller_session") or "")
        if current_task != task_id:
            raise ResumeError("active_lease_owned_by_other_task")
        if current_session == session_id:
            _renew(task_id, session_id, token_file, args.ttl_seconds)
        else:
            if not args.replace_active_same_task:
                raise ResumeError("active_same_task_requires_explicit_replacement")
            if not args.reason:
                raise ResumeError("handoff_reason_required")
            token_file = _handoff(
                task_id,
                session_id,
                token_file,
                generation,
                args.ttl_seconds,
                args.reason,
            )
    else:
        raise ResumeError("lease_status_unknown")

    public = _lease_status()
    generation = int(public.get("generation") or 0)
    if public.get("controller_task") != task_id or public.get("controller_session") != session_id:
        raise ResumeError("controller_identity_not_committed")

    registration = _safe_json(REGISTRATION)
    print(f"TRACK_A_CANONICAL_CONTROLLER_SESSION={session_id}")
    print(f"TRACK_A_CANONICAL_LEASE_GENERATION={generation}")
    print(f"TRACK_A_CANONICAL_TOKEN_FILE={token_file}")

    if registration is None:
        print("TRACK_A_CANONICAL_REGISTRATION=ABSENT")
        print("TRACK_A_CANONICAL_CONTROL_READY=false")
        print("TRACK_A_CANONICAL_NEXT_TRANSITION=canonical_bootstrap")
        return 0

    registered_generation = registration.get("lease_generation")
    if not isinstance(registered_generation, int):
        raise ResumeError("registration_lease_generation_invalid")
    if registered_generation != generation:
        _transition("rebind", task_id, session_id, token_file, args.probe)
        print("TRACK_A_CANONICAL_GENERATION_REBIND=PASS")
    _transition("gate-b", task_id, session_id, token_file, args.probe)
    print("TRACK_A_CANONICAL_GATE_B=PASS")
    print("TRACK_A_CANONICAL_CONTROL_READY=true")
    return 0


def release(args: argparse.Namespace) -> int:
    task_id = _validate_identity(args.task_id, "task-id")
    public = _lease_status()
    if public.get("status") != "active":
        raise ResumeError("lease_not_active")
    if public.get("controller_task") != task_id:
        raise ResumeError("active_lease_owned_by_other_task")
    session_id = str(public.get("controller_session") or "")
    if not session_id:
        raise ResumeError("controller_session_missing")
    raw = _safe_json(LEASE_STATE)
    token_file = _token_path(task_id, raw)
    _run(
        [
            str(LEASE_WRAPPER),
            "release",
            "--task-id",
            task_id,
            "--session-id",
            session_id,
            "--token-file",
            str(token_file),
        ]
    )
    print("TRACK_A_CANONICAL_CONTROLLER_RELEASE=PASS")
    print("TRACK_A_CANONICAL_RUNTIME_PRESERVED=true")
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="operation", required=True)
    resume_parser = sub.add_parser("resume")
    resume_parser.add_argument("--task-id", required=True)
    resume_parser.add_argument("--session-id")
    resume_parser.add_argument("--replace-active-same-task", action="store_true")
    resume_parser.add_argument("--reason")
    resume_parser.add_argument("--ttl-seconds", type=int, default=45 * 60)
    resume_parser.add_argument("--probe", type=Path, default=DEFAULT_PROBE)
    release_parser = sub.add_parser("release")
    release_parser.add_argument("--task-id", required=True)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return {"resume": resume, "release": release}[args.operation](args)
    except Exception as exc:
        print(
            f"TRACK_A_CANONICAL_RESUME_ERROR={getattr(exc, 'code', 'controller_failure')}",
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
