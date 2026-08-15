#!/usr/bin/env python3
from __future__ import annotations

import fcntl
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

LEASE_SCRIPT = Path(__file__).with_name("tibia-official-client-re-canonical-live-lease.py")
GUARD_SCRIPT = Path(__file__).with_name("tibia-official-client-re-canonical-live-guard.py")
SPEC = importlib.util.spec_from_file_location("track_a_lease_guard_test", LEASE_SCRIPT)
assert SPEC and SPEC.loader
lease = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = lease
SPEC.loader.exec_module(lease)


class CanonicalLiveGuardSupervisorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "canonical-live-runtime"
        self.manager = lease.LeaseManager(self.root)
        self.identity = lease.LeaseIdentity("OTC-guard-test", "guard-session")
        self.token = Path(self.temp.name) / "guard.token"
        self.manager.acquire(self.identity, self.token, 300)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def helper_command(self, *command: str) -> list[str]:
        return [
            sys.executable,
            str(GUARD_SCRIPT),
            "--state-dir",
            str(self.root),
            "guard-run",
            "--task-id",
            self.identity.task_id,
            "--session-id",
            self.identity.session_id,
            "--token-file",
            str(self.token),
            "--",
            *command,
        ]

    def test_guard_supervisor_preserves_exit_contract(self) -> None:
        completed = subprocess.run(
            self.helper_command(sys.executable, "-c", "raise SystemExit(23)"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10,
            check=False,
        )
        self.assertEqual(completed.returncode, 23, completed.stderr)
        self.assertIn("TRACK_A_CANONICAL_LEASE_GUARD_RUN=true", completed.stdout)
        self.assertIn("TRACK_A_CANONICAL_LEASE_GENERATION=1", completed.stdout)
        self.assertIn("TRACK_A_CANONICAL_LEASE_GUARD_COMMAND_RC=23", completed.stdout)

    def test_guard_lock_survives_caller_kill_fd_close_and_daemonization(self) -> None:
        daemon_program = r'''
import os
import sys
import time
pid = os.fork()
if pid:
    os._exit(0)
os.setsid()
for fd in range(3, 512):
    try:
        os.close(fd)
    except OSError:
        pass
print(os.getpid(), flush=True)
time.sleep(1.5)
'''
        guard = subprocess.Popen(
            self.helper_command(sys.executable, "-c", daemon_program),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        lock_fd: int | None = None
        try:
            assert guard.stdout is not None
            line = guard.stdout.readline().strip()
            self.assertTrue(line.isdigit(), f"missing daemon pid; got {line!r}")

            guard.kill()
            guard.wait(timeout=5)
            if guard.stdout is not None:
                guard.stdout.close()
            if guard.stderr is not None:
                guard.stderr.close()

            lock_fd = os.open(self.manager.lock_path, os.O_RDWR)
            with self.assertRaises(BlockingIOError):
                fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

            deadline = time.monotonic() + 6.0
            while True:
                try:
                    fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() >= deadline:
                        self.fail("supervisor did not retain/release the lock with daemon lifetime")
                    time.sleep(0.05)
        finally:
            if lock_fd is not None:
                try:
                    fcntl.flock(lock_fd, fcntl.LOCK_UN)
                except OSError:
                    pass
                os.close(lock_fd)
            if guard.poll() is None:
                guard.kill()
                guard.wait(timeout=5)
            if guard.stdout is not None and not guard.stdout.closed:
                guard.stdout.close()
            if guard.stderr is not None and not guard.stderr.closed:
                guard.stderr.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
