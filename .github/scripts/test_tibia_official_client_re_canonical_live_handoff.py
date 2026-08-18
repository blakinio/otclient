#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path

HANDOFF = Path(__file__).with_name("tibia-official-client-re-canonical-live-handoff.py")
LEASE = Path(__file__).with_name("tibia-official-client-re-canonical-live-lease.py")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.handoff = load(HANDOFF, "handoff_tested")
        self.lease = load(LEASE, "lease_for_handoff_test")
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.state = self.root / "canonical"
        self.tasks = self.root / "tasks"
        self.task = "OTC-TEST"
        self.current = self.tasks / self.task / "runtime" / "canonical-lease-token"
        self.next = self.tasks / self.task / "runtime" / "canonical-lease-token.g2"
        self.current.parent.mkdir(parents=True)
        self.handoff.TASK_ROOT = self.tasks
        os.environ["TRACK_A_CANONICAL_HANDOFF_CONTRACT_TEST"] = "1"
        self._seed("old-session", generation=1, expires_at=1000)

    def tearDown(self):
        os.environ.pop("TRACK_A_CANONICAL_HANDOFF_CONTRACT_TEST", None)
        self.temp.cleanup()

    def _seed(self, session: str, *, generation: int, expires_at: int) -> None:
        token = "a" * 64
        self.lease._atomic_write_text(self.current, token + "\n", 0o600)
        manager = self.lease.LeaseManager(self.state)
        manager._prepare()
        with manager.locked():
            manager._write_state_unlocked(
                {
                    "schema_version": self.lease.SCHEMA_VERSION,
                    "runtime_id": self.lease.RUNTIME_ID,
                    "status": "active",
                    "generation": generation,
                    "controller_task": self.task,
                    "controller_session": session,
                    "token_sha256": self.lease._token_digest(token),
                    "acquired_at": 1,
                    "renewed_at": 1,
                    "expires_at": expires_at,
                    "takeover_from": None,
                }
            )

    def test_handoff_discovers_old_session_rotates_capability_and_generation(self):
        result = self.handoff.handoff(
            task_id=self.task,
            new_session_id="new-session",
            current_token_file=self.current,
            new_token_file=self.next,
            expected_generation=1,
            ttl_seconds=600,
            reason="replacement agent after orphaned session preflight",
            state_dir=self.state,
            now=100,
        )
        self.assertEqual(result["generation"], 2)
        self.assertEqual(result["previous_session"], "old-session")
        self.assertFalse(self.current.exists())
        self.assertTrue(self.next.exists())

        manager = self.lease.LeaseManager(self.state)
        state = manager._load_state_unlocked()
        self.assertEqual(state["controller_task"], self.task)
        self.assertEqual(state["controller_session"], "new-session")
        self.assertEqual(state["generation"], 2)
        self.assertEqual(state["token_slot"], self.next.name)
        self.assertEqual(state["handoff_from"]["controller_session"], "old-session")
        validated = manager.validate(
            self.lease.LeaseIdentity(self.task, "new-session"),
            self.next,
            now=101,
        )
        self.assertEqual(validated.generation, 2)

    def test_handoff_rejects_cross_task_even_with_matching_capability_bytes(self):
        other_current = self.tasks / "OTC-OTHER" / "runtime" / "token"
        other_current.parent.mkdir(parents=True)
        self.lease._atomic_write_text(other_current, "a" * 64 + "\n", 0o600)
        with self.assertRaisesRegex(self.handoff.HandoffError, "handoff_cross_task_forbidden"):
            self.handoff.handoff(
                task_id="OTC-OTHER",
                new_session_id="new-session",
                current_token_file=other_current,
                new_token_file=self.tasks / "OTC-OTHER" / "runtime" / "token.g2",
                expected_generation=1,
                ttl_seconds=600,
                reason="must not cross task",
                state_dir=self.state,
                now=100,
            )
        self.assertTrue(self.current.exists())

    def test_handoff_rejects_changed_generation(self):
        with self.assertRaisesRegex(self.handoff.HandoffError, "lease_generation_changed"):
            self.handoff.handoff(
                task_id=self.task,
                new_session_id="new-session",
                current_token_file=self.current,
                new_token_file=self.next,
                expected_generation=2,
                ttl_seconds=600,
                reason="stale preflight",
                state_dir=self.state,
                now=100,
            )
        self.assertFalse(self.next.exists())

    def test_handoff_rejects_expired_lease(self):
        self._seed("old-session", generation=1, expires_at=50)
        with self.assertRaisesRegex(self.handoff.HandoffError, "lease_expired"):
            self.handoff.handoff(
                task_id=self.task,
                new_session_id="new-session",
                current_token_file=self.current,
                new_token_file=self.next,
                expected_generation=1,
                ttl_seconds=600,
                reason="expired lease must use stale takeover path",
                state_dir=self.state,
                now=100,
            )

    def test_handoff_never_overwrites_a_new_token_slot(self):
        self.lease._atomic_write_text(self.next, "b" * 64 + "\n", 0o600)
        with self.assertRaisesRegex(self.handoff.HandoffError, "handoff_new_token_exists"):
            self.handoff.handoff(
                task_id=self.task,
                new_session_id="new-session",
                current_token_file=self.current,
                new_token_file=self.next,
                expected_generation=1,
                ttl_seconds=600,
                reason="collision",
                state_dir=self.state,
                now=100,
            )
        self.assertEqual(self.next.read_text().strip(), "b" * 64)

    def test_source_has_no_credential_ingress(self):
        source = HANDOFF.read_text()
        self.assertNotIn("TIBIA_TEST_EMAIL", source)
        self.assertNotIn("TIBIA_TEST_PASSWORD", source)
        self.assertNotIn("--current-session-id", source)


if __name__ == "__main__":
    unittest.main()
