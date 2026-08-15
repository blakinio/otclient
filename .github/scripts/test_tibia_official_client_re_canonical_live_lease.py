#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("tibia-official-client-re-canonical-live-lease.py")
SPEC = importlib.util.spec_from_file_location("track_a_lease", SCRIPT)
assert SPEC and SPEC.loader
lease = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = lease
SPEC.loader.exec_module(lease)


class CanonicalLiveLeaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "canonical-live-runtime"
        self.manager = lease.LeaseManager(self.root)
        self.a = lease.LeaseIdentity("OTC-test-a", "session-a")
        self.b = lease.LeaseIdentity("OTC-test-b", "session-b")
        self.token_a = Path(self.temp.name) / "task-a" / "lease.token"
        self.token_b = Path(self.temp.name) / "task-b" / "lease.token"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def assertLeaseError(self, code: str, fn, *args, **kwargs) -> None:
        with self.assertRaises(lease.LeaseError) as caught:
            fn(*args, **kwargs)
        self.assertEqual(caught.exception.code, code)

    def test_absent_status_is_redacted(self) -> None:
        status = self.manager.status(now=100)
        self.assertEqual(status["status"], "absent")
        self.assertNotIn("token", json.dumps(status).lower())

    def test_acquire_writes_private_token_and_digest_only_state(self) -> None:
        result = self.manager.acquire(self.a, self.token_a, 300, now=100)
        self.assertEqual(result.generation, 1)
        self.assertFalse(result.stale_takeover)
        self.assertEqual(stat.S_IMODE(self.token_a.stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(self.manager.state_path.stat().st_mode), 0o600)
        raw_token = self.token_a.read_text(encoding="ascii").strip()
        state_text = self.manager.state_path.read_text(encoding="utf-8")
        self.assertNotIn(raw_token, state_text)
        self.assertIn(lease._token_digest(raw_token), state_text)
        public = self.manager.status(now=101)
        self.assertNotIn("token", json.dumps(public).lower())

    def test_idempotent_same_controller_acquire_renews_generation(self) -> None:
        first = self.manager.acquire(self.a, self.token_a, 300, now=100)
        second = self.manager.acquire(self.a, self.token_a, 300, now=200)
        self.assertEqual(first.generation, second.generation)
        self.assertTrue(second.idempotent)
        self.assertEqual(second.expires_at, 500)

    def test_live_conflict_fails_closed(self) -> None:
        self.manager.acquire(self.a, self.token_a, 300, now=100)
        self.assertLeaseError(
            "lease_conflict",
            self.manager.acquire,
            self.b,
            self.token_b,
            300,
            now=101,
        )
        self.assertFalse(self.token_b.exists())

    def test_expired_takeover_requires_reason_and_fences_old_token(self) -> None:
        self.manager.acquire(self.a, self.token_a, 60, now=100)
        old_token = self.token_a.read_text(encoding="ascii")
        self.assertLeaseError(
            "stale_takeover_reason_required",
            self.manager.acquire,
            self.a,
            self.token_b,
            60,
            now=161,
        )
        takeover = self.manager.acquire(
            self.a,
            self.token_b,
            60,
            stale_reason="repository lease expired; runtime revalidation required",
            now=161,
        )
        self.assertEqual(takeover.generation, 2)
        self.assertTrue(takeover.stale_takeover)
        self.assertNotEqual(old_token, self.token_b.read_text(encoding="ascii"))
        self.assertLeaseError(
            "lease_token_mismatch",
            self.manager.release,
            self.a,
            self.token_a,
            now=162,
        )
        valid = self.manager.validate(self.a, self.token_b, now=162)
        self.assertEqual(valid.generation, 2)

    def test_renew_requires_current_unexpired_token(self) -> None:
        self.manager.acquire(self.a, self.token_a, 60, now=100)
        renewed = self.manager.renew(self.a, self.token_a, 120, now=120)
        self.assertEqual(renewed.expires_at, 240)
        self.assertLeaseError(
            "lease_expired",
            self.manager.renew,
            self.a,
            self.token_a,
            120,
            now=241,
        )

    def test_expired_release_is_rejected_and_preserves_stale_takeover_path(self) -> None:
        self.manager.acquire(self.a, self.token_a, 60, now=100)
        self.assertLeaseError(
            "lease_expired",
            self.manager.release,
            self.a,
            self.token_a,
            now=161,
        )
        self.assertTrue(self.token_a.exists())
        status = self.manager.status(now=161)
        self.assertEqual(status["status"], "active")
        self.assertEqual(status["generation"], 1)
        self.assertTrue(status["expired"])
        self.assertLeaseError(
            "stale_takeover_reason_required",
            self.manager.acquire,
            self.b,
            self.token_b,
            60,
            now=161,
        )
        takeover = self.manager.acquire(
            self.b,
            self.token_b,
            60,
            stale_reason="expired holder cannot release; explicit takeover required",
            now=161,
        )
        self.assertEqual(takeover.generation, 2)
        self.assertTrue(takeover.stale_takeover)
        self.assertLeaseError(
            "lease_identity_mismatch",
            self.manager.release,
            self.a,
            self.token_a,
            now=162,
        )

    def test_release_is_fenced_and_preserves_generation(self) -> None:
        self.manager.acquire(self.a, self.token_a, 300, now=100)
        released = self.manager.release(self.a, self.token_a, now=110)
        self.assertEqual(released.generation, 1)
        self.assertFalse(self.token_a.exists())
        status = self.manager.status(now=111)
        self.assertEqual(status["status"], "released")
        self.assertEqual(status["generation"], 1)
        second = self.manager.acquire(self.b, self.token_b, 300, now=112)
        self.assertEqual(second.generation, 2)

    def test_guard_run_requires_lease_and_executes_without_shell(self) -> None:
        output = Path(self.temp.name) / "guard-output"
        self.assertLeaseError(
            "token_file_missing",
            self.manager.guard_run,
            self.a,
            self.token_a,
            [sys.executable, "-c", "pass"],
            now=100,
        )
        self.manager.acquire(self.a, self.token_a, 300, now=100)
        result, rc = self.manager.guard_run(
            self.a,
            self.token_a,
            [sys.executable, "-c", f"from pathlib import Path; Path({str(output)!r}).write_text('ok')"],
            now=101,
        )
        self.assertEqual(result.generation, 1)
        self.assertEqual(rc, 0)
        self.assertEqual(output.read_text(), "ok")

    def test_corrupt_state_fails_closed(self) -> None:
        self.root.mkdir(parents=True, mode=0o700)
        self.manager.state_path.write_text("not-json", encoding="utf-8")
        os.chmod(self.manager.state_path, 0o600)
        self.assertLeaseError("state_corrupt", self.manager.status, now=100)

    def test_two_cli_acquires_produce_exactly_one_controller(self) -> None:
        state = Path(self.temp.name) / "cli-state"
        token1 = Path(self.temp.name) / "cli-a.token"
        token2 = Path(self.temp.name) / "cli-b.token"
        env = dict(os.environ)
        env["TRACK_A_LEASE_ALLOW_NONCANONICAL_STATE"] = "1"
        base = [sys.executable, str(SCRIPT), "--state-dir", str(state), "acquire"]
        p1 = subprocess.Popen(
            base + ["--task-id", "OTC-cli-a", "--session-id", "s-a", "--token-file", str(token1)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )
        p2 = subprocess.Popen(
            base + ["--task-id", "OTC-cli-b", "--session-id", "s-b", "--token-file", str(token2)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )
        out1, err1 = p1.communicate(timeout=10)
        out2, err2 = p2.communicate(timeout=10)
        self.assertEqual(sorted([p1.returncode, p2.returncode]), [0, 2])
        combined = out1 + err1 + out2 + err2
        self.assertEqual(combined.count("TRACK_A_CANONICAL_LEASE_ACQUIRE=true"), 1)
        self.assertEqual(combined.count("TRACK_A_CANONICAL_LEASE_ERROR=lease_conflict"), 1)
        status = lease.LeaseManager(state).status()
        self.assertIn(status["controller_task"], {"OTC-cli-a", "OTC-cli-b"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
