#!/usr/bin/env python3
"""Cancellation-safe teardown for one exact Track A canonical live runtime.

This transition is deliberately separate from bootstrap/rebind/gate-b so the
already-promoted old-client control plane is not changed while that exact
runtime is still live.  It validates the current registration under the same
lease flock, proves the exact registered process group, commits to teardown
only after the final cancellation check, then finishes cleanup even if a
cancellation arrives after that destructive boundary.
"""
from __future__ import annotations

import argparse
import fcntl
import importlib.util
import os
from pathlib import Path
import signal
import sys
import time
from typing import Any, Sequence

TRANSITION_PATH = Path(__file__).with_name(
    'tibia-official-client-re-canonical-live-transition.py'
)


class TeardownError(RuntimeError):
    def __init__(self, code: str, message: str = '') -> None:
        super().__init__(message or code)
        self.code = code


def _load_transition() -> Any:
    spec = importlib.util.spec_from_file_location(
        'track_a_canonical_teardown_transition', TRANSITION_PATH
    )
    if spec is None or spec.loader is None:
        raise TeardownError('transition_unavailable')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _wait_group_empty(transition: Any, pgid: int, timeout: float = 5.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        members = transition._group_members(pgid)
        if not members:
            return
        try:
            while os.waitpid(-1, os.WNOHANG)[0] > 0:
                pass
        except ChildProcessError:
            pass
        time.sleep(0.1)
    members = transition._group_members(pgid)
    if members:
        raise TeardownError(
            'teardown_process_group_survived',
            'registered canonical process group still has live members',
        )


def _teardown_locked(
    args: argparse.Namespace,
    transition: Any,
    guard: Any,
    lease: Any,
    manager: Any,
    identity: Any,
    generation: int,
) -> None:
    if generation != args.expected_generation:
        raise TeardownError('teardown_generation_mismatch')

    registration, manifest = transition._probe_reg(
        args, guard, lease, manager, identity, generation, False
    )
    pgid = manifest.get('process_group_id')
    if not isinstance(pgid, int) or pgid < 2:
        raise TeardownError('teardown_process_group_invalid')
    if pgid == os.getpgrp():
        raise TeardownError('teardown_refuse_controller_process_group')

    # Final exact proof immediately before the irreversible boundary.
    transition._assert_group_tracked(manifest)
    if transition._read() != registration:
        raise TeardownError('teardown_registration_changed')
    transition._lease(
        manager, lease, identity, args.token_file, generation
    )
    transition._cancel(guard)

    print('TRACK_A_CANONICAL_TEARDOWN_COMMIT=true', flush=True)
    print(f'TRACK_A_CANONICAL_TEARDOWN_PID={registration["pid"]}', flush=True)
    print(f'TRACK_A_CANONICAL_TEARDOWN_PGID={pgid}', flush=True)

    # From this point on cancellation is intentionally not re-checked.  Once
    # the exact registered runtime has begun stopping, leaving its registration
    # behind would be a more dangerous half-state than completing teardown.
    transition._kill(pgid)
    _wait_group_empty(transition, pgid)

    cleanup_error: BaseException | None = None
    try:
        transition._worker(args.worker, 'rollback', str(pgid))
    except BaseException as exc:  # registration cleanup still must complete
        cleanup_error = exc

    candidates = transition._candidates()
    if candidates:
        raise TeardownError(
            'teardown_official_client_candidate_survived',
            f'official client candidates remain after exact group stop: {candidates}',
        )

    transition._remove(registration)
    if transition._read() is not None:
        raise TeardownError('teardown_registration_survived')

    # Lease ownership is intentionally retained for the following update step.
    transition._lease(
        manager, lease, identity, args.token_file, generation
    )

    print('TRACK_A_CANONICAL_TEARDOWN_RUNTIME_GONE=true', flush=True)
    print('TRACK_A_CANONICAL_TEARDOWN_REGISTRATION_ABSENT=true', flush=True)
    print('TRACK_A_CANONICAL_TEARDOWN_LEASE_RETAINED=true', flush=True)
    print('TRACK_A_CANONICAL_TEARDOWN_SECRET_ACCESS=false', flush=True)

    if cleanup_error is not None:
        raise TeardownError(
            'teardown_worker_cleanup_failed_after_unregister', str(cleanup_error)
        )


def _child(
    args: argparse.Namespace,
    transition: Any,
    guard: Any,
    lock_fd: int,
    previous_mask: set[signal.Signals],
) -> None:
    rc = 2
    try:
        guard._supervisor_cancel_signal = None
        guard._install_supervisor_signal_handlers(previous_mask)
        guard._become_child_subreaper()
        lease = guard.lease
        manager = lease.LeaseManager(transition.STATE)
        identity = lease.LeaseIdentity(args.task_id, args.session_id)
        generation = transition._lease(
            manager, lease, identity, args.token_file
        )
        transition._cancel(guard)
        _teardown_locked(
            args, transition, guard, lease, manager, identity, generation
        )
        print('TRACK_A_CANONICAL_TEARDOWN=PASS', flush=True)
        print(f'TRACK_A_CANONICAL_LEASE_GENERATION={generation}', flush=True)
        rc = 0
    except (TeardownError, transition.E, guard.lease.LeaseError) as exc:
        print(
            'TRACK_A_CANONICAL_TEARDOWN_ERROR='
            + str(getattr(exc, 'code', 'lease_error')),
            file=sys.stderr,
            flush=True,
        )
    except BaseException:
        print(
            'TRACK_A_CANONICAL_TEARDOWN_ERROR=supervisor_failure',
            file=sys.stderr,
            flush=True,
        )
    finally:
        try:
            os.close(lock_fd)
        except OSError:
            pass
    os._exit(rc)


def _supervise(args: argparse.Namespace) -> int:
    transition = _load_transition()
    guard = transition._guard()
    lease = guard.lease
    identity = lease.LeaseIdentity(
        lease._validate_identity(args.task_id, 'task-id'),
        lease._validate_identity(args.session_id, 'session-id'),
    )
    manager = lease.LeaseManager(transition.STATE)
    token = lease._read_private_token(args.token_file)
    manager._prepare()
    lock_fd = os.open(manager.lock_path, os.O_RDWR)
    previous_mask: set[signal.Signals] | None = None
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        state = manager._load_state_unlocked()
        manager._require_current_unlocked(
            state, identity, token, lease._now_epoch(None)
        )
        previous_mask = signal.pthread_sigmask(
            signal.SIG_BLOCK, guard.SUPERVISOR_CANCELLATION_SIGNALS
        )
        supervisor_pid = os.fork()
        if supervisor_pid == 0:
            _child(args, transition, guard, lock_fd, previous_mask)

        pending = signal.sigpending()
        for signum in guard.SUPERVISOR_CANCELLATION_SIGNALS:
            if signum in pending:
                try:
                    os.kill(supervisor_pid, signum)
                except ProcessLookupError:
                    pass
                break
        signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)
        previous_mask = None
        os.close(lock_fd)
        lock_fd = -1
        _, wait_status = os.waitpid(supervisor_pid, 0)
        return os.waitstatus_to_exitcode(wait_status)
    finally:
        if previous_mask is not None:
            try:
                signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)
            except OSError:
                pass
        if lock_fd >= 0:
            try:
                os.close(lock_fd)
            except OSError:
                pass


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument('--task-id', required=True)
    result.add_argument('--session-id', required=True)
    result.add_argument('--token-file', required=True, type=Path)
    result.add_argument('--probe', required=True, type=Path)
    result.add_argument('--worker', required=True, type=Path)
    result.add_argument('--expected-generation', type=int, required=True)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    try:
        return _supervise(parser().parse_args(argv))
    except Exception as exc:
        print(
            'TRACK_A_CANONICAL_TEARDOWN_ERROR='
            + str(getattr(exc, 'code', 'controller_failure')),
            file=sys.stderr,
        )
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
