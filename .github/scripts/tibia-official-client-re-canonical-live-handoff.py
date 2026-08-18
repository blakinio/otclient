#!/usr/bin/env python3
"""Fail-closed same-task controller handoff for Track A canonical runtime."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import secrets
import sys
from pathlib import Path
from typing import Any, Sequence

LEASE_PATH = Path(__file__).with_name("tibia-official-client-re-canonical-live-lease.py")
CANONICAL_STATE = Path("/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime")
TASK_ROOT = Path("/home/runner/_work/_otclient_tibia_re_state/tasks")
IDENT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,199}$")


class HandoffError(RuntimeError):
    def __init__(self, code: str, message: str = "") -> None:
        super().__init__(message or code)
        self.code = code


def _load_lease():
    spec = importlib.util.spec_from_file_location("track_a_handoff_lease", LEASE_PATH)
    if spec is None or spec.loader is None:
        raise HandoffError("lease_module_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _identity(value: str, field: str) -> str:
    if not IDENT_RE.fullmatch(value):
        raise HandoffError("invalid_identity", f"invalid {field}")
    return value


def _reason(value: str) -> str:
    result = value.strip()
    if not result or len(result) > 256 or "\n" in result or "\r" in result:
        raise HandoffError("invalid_handoff_reason")
    return result


def _task_token_path(task_id: str, path: Path) -> Path:
    task_root = (TASK_ROOT / task_id).resolve(strict=False)
    candidate = path.resolve(strict=False)
    try:
        candidate.relative_to(task_root)
    except ValueError as exc:
        raise HandoffError("token_path_outside_task_state") from exc
    return candidate


def _state_dir(path: Path) -> Path:
    if path != CANONICAL_STATE and os.environ.get("TRACK_A_CANONICAL_HANDOFF_CONTRACT_TEST") != "1":
        raise HandoffError("noncanonical_state_override_forbidden")
    return path


def _task_root(path: Path) -> Path:
    if path != TASK_ROOT and os.environ.get("TRACK_A_CANONICAL_HANDOFF_CONTRACT_TEST") != "1":
        raise HandoffError("nontask_root_override_forbidden")
    return path


def handoff(
    *,
    task_id: str,
    new_session_id: str,
    current_token_file: Path,
    new_token_file: Path,
    expected_generation: int,
    ttl_seconds: int,
    reason: str,
    state_dir: Path = CANONICAL_STATE,
    now: float | None = None,
) -> dict[str, Any]:
    """Move one fresh same-task lease to a new disposable controller session.

    The previous session id is discovered from authoritative lease state. A new
    capability is durably written to a distinct task-local token slot before the
    lease record commits, so a pre-commit crash leaves the old controller usable
    and a post-commit crash leaves the new token already present.
    """
    lease = _load_lease()
    task_id = _identity(task_id, "task-id")
    new_session_id = _identity(new_session_id, "session-id")
    reason = _reason(reason)
    if expected_generation < 1:
        raise HandoffError("invalid_expected_generation")
    if not lease.MIN_TTL_SECONDS <= ttl_seconds <= lease.MAX_TTL_SECONDS:
        raise HandoffError("invalid_ttl")
    state_dir = _state_dir(state_dir)
    current_token_file = _task_token_path(task_id, current_token_file)
    new_token_file = _task_token_path(task_id, new_token_file)
    if current_token_file == new_token_file:
        raise HandoffError("handoff_token_paths_must_differ")
    if new_token_file.exists():
        raise HandoffError("handoff_new_token_exists")

    current_token = lease._read_private_token(current_token_file)
    manager = lease.LeaseManager(state_dir)
    now_epoch = lease._now_epoch(now)

    with manager.locked():
        state = manager._load_state_unlocked()
        if state is None or state.get("status") != "active":
            raise HandoffError("lease_not_active")
        if int(state.get("generation", 0)) != expected_generation:
            raise HandoffError("lease_generation_changed")
        if int(state.get("expires_at", 0)) <= now_epoch:
            raise HandoffError("lease_expired")
        if state.get("controller_task") != task_id:
            raise HandoffError("handoff_cross_task_forbidden")
        current_session = str(state.get("controller_session") or "")
        if not current_session:
            raise HandoffError("current_session_missing")
        if current_session == new_session_id:
            raise HandoffError("handoff_same_session")
        if not manager._token_matches(state, current_token):
            raise HandoffError("lease_token_mismatch")

        new_generation = expected_generation + 1
        new_token = secrets.token_hex(32)
        lease._atomic_write_text(new_token_file, new_token + "\n", 0o600)
        updated = dict(state)
        updated.update(
            generation=new_generation,
            controller_session=new_session_id,
            token_sha256=lease._token_digest(new_token),
            token_slot=new_token_file.name,
            acquired_at=now_epoch,
            renewed_at=now_epoch,
            expires_at=now_epoch + ttl_seconds,
            handoff_from={
                "generation": expected_generation,
                "controller_task": task_id,
                "controller_session": current_session,
                "handoff_at": now_epoch,
                "reason": reason,
            },
        )
        try:
            manager._write_state_unlocked(updated)
        except BaseException:
            new_token_file.unlink(missing_ok=True)
            raise

        # State now rejects the old capability. Unlink is cleanup only; a stale
        # token file has no authority even if it survives.
        current_token_file.unlink(missing_ok=True)
        reread = manager._load_state_unlocked()
        if reread != updated:
            raise HandoffError("handoff_revalidation_failed")
        if not manager._token_matches(updated, lease._read_private_token(new_token_file)):
            raise HandoffError("handoff_new_token_revalidation_failed")

    return {
        "runtime_id": lease.RUNTIME_ID,
        "generation": new_generation,
        "controller_task": task_id,
        "controller_session": new_session_id,
        "expires_at": now_epoch + ttl_seconds,
        "token_slot": new_token_file.name,
        "previous_session": current_session,
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--state-dir", type=Path, default=CANONICAL_STATE)
    result.add_argument("--task-root", type=Path, default=TASK_ROOT)
    result.add_argument("--task-id", required=True)
    result.add_argument("--session-id", required=True, help="new controller session id")
    result.add_argument("--token-file", required=True, type=Path, help="current capability token")
    result.add_argument("--new-token-file", required=True, type=Path)
    result.add_argument("--expected-generation", required=True, type=int)
    result.add_argument("--ttl-seconds", type=int, default=45 * 60)
    result.add_argument("--handoff-reason", required=True)
    result.add_argument("--json", action="store_true")
    return result


def main(argv: Sequence[str] | None = None) -> int:
    global TASK_ROOT
    args = parser().parse_args(argv)
    try:
        TASK_ROOT = _task_root(args.task_root)
        data = handoff(
            task_id=args.task_id,
            new_session_id=args.session_id,
            current_token_file=args.token_file,
            new_token_file=args.new_token_file,
            expected_generation=args.expected_generation,
            ttl_seconds=args.ttl_seconds,
            reason=args.handoff_reason,
            state_dir=args.state_dir,
        )
    except Exception as exc:
        print(
            f"TRACK_A_CANONICAL_HANDOFF_ERROR={getattr(exc, 'code', 'handoff_failure')}",
            file=sys.stderr,
        )
        return 2
    if args.json:
        print(json.dumps(data, sort_keys=True))
    else:
        print("TRACK_A_CANONICAL_HANDOFF=PASS")
        print(f"TRACK_A_CANONICAL_LEASE_GENERATION={data['generation']}")
        print(f"TRACK_A_CANONICAL_CONTROLLER_SESSION={data['controller_session']}")
        print(f"TRACK_A_CANONICAL_TOKEN_SLOT={data['token_slot']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
