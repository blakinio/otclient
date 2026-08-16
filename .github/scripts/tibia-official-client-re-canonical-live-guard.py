#!/usr/bin/env python3
"""Supervisor-backed guard-run for the Track A canonical-live lease.

The production shell entrypoint routes guard-run here so the coordination flock
is owned by a supervisor process, not by the guarded command. The supervisor is
a Linux child subreaper and keeps the flock until the guarded command and every
orphaned descendant have exited. This prevents a guarded command from dropping
the lock by closing inherited file descriptors, daemonizing, or outliving a
foreground process-group cancellation.
"""

from __future__ import annotations

import argparse
import ctypes
import fcntl
import importlib.util
import os
from pathlib import Path
import signal
import subprocess
import sys
from typing import Sequence

SCRIPT = Path(__file__).with_name("tibia-official-client-re-canonical-live-lease.py")
SPEC = importlib.util.spec_from_file_location("track_a_lease_guarded", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load canonical lease implementation")
lease = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = lease
SPEC.loader.exec_module(lease)

PR_SET_CHILD_SUBREAPER = 36
SUPERVISOR_CANCELLATION_SIGNALS = (
    signal.SIGHUP,
    signal.SIGINT,
    signal.SIGQUIT,
    signal.SIGTERM,
)
_supervisor_cancel_signal: int | None = None


def _become_child_subreaper() -> None:
    if not sys.platform.startswith("linux"):
        raise lease.LeaseError(
            "guard_supervisor_unsupported",
            "guard-run supervisor requires native Linux",
        )
    libc = ctypes.CDLL(None, use_errno=True)
    prctl = libc.prctl
    prctl.argtypes = [
        ctypes.c_int,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.c_ulong,
    ]
    prctl.restype = ctypes.c_int
    if prctl(PR_SET_CHILD_SUBREAPER, 1, 0, 0, 0) != 0:
        err = ctypes.get_errno()
        raise lease.LeaseError(
            "guard_supervisor_unavailable",
            f"PR_SET_CHILD_SUBREAPER failed with errno {err}",
        )


def _record_supervisor_cancellation(signum: int, _frame: object) -> None:
    """Keep the lock-owning supervisor alive while recording cancellation."""
    global _supervisor_cancel_signal
    if _supervisor_cancel_signal is None:
        _supervisor_cancel_signal = signum


def _install_supervisor_signal_handlers(previous_mask: set[signal.Signals]) -> None:
    for signum in SUPERVISOR_CANCELLATION_SIGNALS:
        signal.signal(signum, _record_supervisor_cancellation)
    signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)


def _wait_for_all_descendants() -> None:
    while True:
        try:
            os.waitpid(-1, 0)
        except ChildProcessError:
            return


def _normalized_process_exit(returncode: int) -> int:
    if returncode < 0:
        return min(255, 128 + abs(returncode))
    return max(0, min(255, returncode))


def _supervise_locked_command(
    lock_fd: int,
    command: Sequence[str],
    previous_mask: set[signal.Signals],
) -> None:
    """Run in the detached lock-owning child and never return."""
    global _supervisor_cancel_signal
    _supervisor_cancel_signal = None
    exit_code = 125
    try:
        # The caller blocks cancellation signals before fork. Install handlers
        # before restoring that mask so process-group cancellation cannot kill
        # the lock owner in the post-fork setup window.
        _install_supervisor_signal_handlers(previous_mask)
        _become_child_subreaper()

        cancel_signal = _supervisor_cancel_signal
        if cancel_signal is not None:
            exit_code = _normalized_process_exit(-cancel_signal)
        else:
            completed = subprocess.Popen(list(command), close_fds=True)

            # A cancellation may land after the pre-dispatch check but before
            # exec. The command was not present for that group signal, so relay
            # the recorded cancellation once. A command that deliberately
            # ignores it remains supervised and serialized until it exits.
            cancel_signal = _supervisor_cancel_signal
            if cancel_signal is not None:
                try:
                    completed.send_signal(cancel_signal)
                except ProcessLookupError:
                    pass

            primary_returncode = completed.wait()
            _wait_for_all_descendants()
            exit_code = _normalized_process_exit(primary_returncode)
    except lease.LeaseError as exc:
        print(f"TRACK_A_CANONICAL_LEASE_ERROR={exc.code}", file=sys.stderr, flush=True)
    except BaseException:
        print("TRACK_A_CANONICAL_LEASE_ERROR=guard_supervisor_failure", file=sys.stderr, flush=True)
    finally:
        try:
            os.close(lock_fd)
        except OSError:
            pass
    os._exit(exit_code)


def _guard_run(
    manager: lease.LeaseManager,
    identity: lease.LeaseIdentity,
    token_file: Path,
    command: Sequence[str],
) -> tuple[lease.LeaseResult, int]:
    if not command:
        raise lease.LeaseError("guard_command_missing", "guard-run requires a command")

    token = lease._read_private_token(token_file)
    manager._prepare()
    lock_fd = os.open(manager.lock_path, os.O_RDWR)
    supervisor_pid: int | None = None
    previous_mask: set[signal.Signals] | None = None
    try:
        # Acquire and validate in the caller before forking. If the caller is
        # cancelled while waiting for the flock, no detached command exists.
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        now_epoch = lease._now_epoch()
        state = manager._load_state_unlocked()
        manager._require_current_unlocked(state, identity, token, now_epoch)
        assert state is not None
        result = lease.LeaseResult(int(state["generation"]), int(state["expires_at"]))

        # Block normal cancellation signals across fork. The supervisor installs
        # non-terminating handlers before restoring the inherited mask, closing
        # the race where SIGTERM could otherwise kill the only surviving flock
        # owner before it became cancellation-safe.
        previous_mask = signal.pthread_sigmask(
            signal.SIG_BLOCK,
            SUPERVISOR_CANCELLATION_SIGNALS,
        )
        supervisor_pid = os.fork()
        if supervisor_pid == 0:
            _supervise_locked_command(lock_fd, command, previous_mask)

        # If cancellation was already pending in the caller before fork, POSIX
        # does not inherit that pending set. Relay it while the supervisor still
        # has the signals blocked; it will handle the signal before dispatch.
        pending = signal.sigpending()
        for signum in SUPERVISOR_CANCELLATION_SIGNALS:
            if signum in pending:
                try:
                    os.kill(supervisor_pid, signum)
                except ProcessLookupError:
                    pass
                break
        signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)
        previous_mask = None

        # flock is tied to the inherited open-file description. Closing the
        # caller's copy does not unlock while the supervisor copy survives.
        os.close(lock_fd)
        lock_fd = -1
        _, wait_status = os.waitpid(supervisor_pid, 0)
        return result, os.waitstatus_to_exitcode(wait_status)
    except BaseException:
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
        raise


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-dir", type=Path, required=True)
    sub = parser.add_subparsers(dest="operation", required=True)
    guard = sub.add_parser("guard-run")
    guard.add_argument("--task-id", required=True)
    guard.add_argument("--session-id", required=True)
    guard.add_argument("--token-file", required=True, type=Path)
    guard.add_argument("command", nargs=argparse.REMAINDER)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        identity = lease.LeaseIdentity(
            lease._validate_identity(args.task_id, "task-id"),
            lease._validate_identity(args.session_id, "session-id"),
        )
        command = list(args.command)
        if command and command[0] == "--":
            command = command[1:]
        result, rc = _guard_run(
            lease.LeaseManager(args.state_dir),
            identity,
            args.token_file,
            command,
        )
        lease._print_result("guard_run", result)
        print(f"TRACK_A_CANONICAL_LEASE_GUARD_COMMAND_RC={rc}")
        return rc
    except lease.LeaseError as exc:
        print(f"TRACK_A_CANONICAL_LEASE_ERROR={exc.code}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
