#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).with_name("tibia-official-client-re-canonical-live-resume.py")


def load():
    spec = importlib.util.spec_from_file_location("resume_tested", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ResumeTests(unittest.TestCase):
    def setUp(self):
        self.m = load()
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.m.TASK_ROOT = root / "tasks"
        self.m.LEASE_STATE = root / "canonical" / "lease.json"
        self.m.REGISTRATION = root / "canonical" / "runtime-registration.json"
        self.task = "OTC-TEST"
        self.args = argparse.Namespace(
            task_id=self.task,
            session_id="new-session",
            replace_active_same_task=False,
            reason=None,
            ttl_seconds=600,
            probe=Path("/probe"),
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_session_is_derived_from_current_github_job_not_history(self):
        with mock.patch.dict(
            os.environ,
            {"GITHUB_RUN_ID": "123", "GITHUB_RUN_ATTEMPT": "2", "GITHUB_JOB": "physical viewer"},
            clear=True,
        ):
            self.assertEqual(self.m._derive_session(None), "gha-123-2-physical-viewer")

    def test_outside_github_actions_requires_explicit_new_session(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(
                self.m.ResumeError, "session_id_required_outside_github_actions"
            ):
                self.m._derive_session(None)

    def test_active_same_task_never_reuses_old_session_without_explicit_replacement(self):
        public = {
            "status": "active",
            "generation": 7,
            "controller_task": self.task,
            "controller_session": "old-session",
            "expired": False,
        }
        with mock.patch.object(self.m, "_lease_status", return_value=public), \
                mock.patch.object(self.m, "_safe_json", return_value=None):
            with self.assertRaisesRegex(
                self.m.ResumeError, "active_same_task_requires_explicit_replacement"
            ):
                self.m.resume(self.args)

    def test_explicit_replacement_handoffs_then_rebinds_and_gate_b(self):
        self.args.replace_active_same_task = True
        self.args.reason = "replacement session after recovery preflight"
        before = {
            "status": "active",
            "generation": 7,
            "controller_task": self.task,
            "controller_session": "old-session",
            "expired": False,
        }
        after = {
            "status": "active",
            "generation": 8,
            "controller_task": self.task,
            "controller_session": "new-session",
            "expired": False,
        }
        registration = {"lease_generation": 7}
        current_token = self.m.TASK_ROOT / self.task / "runtime" / "canonical-lease-token"
        new_token = self.m.TASK_ROOT / self.task / "runtime" / "canonical-lease-token.g8"
        calls = []
        with mock.patch.object(self.m, "_lease_status", side_effect=[before, after]), \
                mock.patch.object(self.m, "_safe_json", side_effect=[{}, registration]), \
                mock.patch.object(self.m, "_token_path", return_value=current_token), \
                mock.patch.object(self.m, "_handoff", return_value=new_token) as handoff, \
                mock.patch.object(
                    self.m, "_transition", side_effect=lambda *a: calls.append(a)
                ):
            rc = self.m.resume(self.args)
        self.assertEqual(rc, 0)
        handoff.assert_called_once_with(
            self.task,
            "new-session",
            current_token,
            7,
            600,
            "replacement session after recovery preflight",
        )
        self.assertEqual([c[0] for c in calls], ["rebind", "gate-b"])

    def test_registration_absence_keeps_new_lease_but_does_not_launch_client(self):
        absent = {
            "status": "released",
            "generation": 3,
            "controller_task": None,
            "controller_session": None,
            "expired": False,
        }
        after = {
            "status": "active",
            "generation": 4,
            "controller_task": self.task,
            "controller_session": "new-session",
            "expired": False,
        }
        with mock.patch.object(self.m, "_lease_status", side_effect=[absent, after]), \
                mock.patch.object(self.m, "_safe_json", return_value=None), \
                mock.patch.object(self.m, "_acquire") as acquire, \
                mock.patch.object(self.m, "_transition") as transition:
            rc = self.m.resume(self.args)
        self.assertEqual(rc, 0)
        acquire.assert_called_once()
        transition.assert_not_called()

    def test_release_discovers_current_session_and_token_slot(self):
        public = {
            "status": "active",
            "generation": 8,
            "controller_task": self.task,
            "controller_session": "live-session",
            "expired": False,
        }
        raw = {"token_slot": "canonical-lease-token.g8"}
        captured = []
        with mock.patch.object(self.m, "_lease_status", return_value=public), \
                mock.patch.object(self.m, "_safe_json", return_value=raw), \
                mock.patch.object(
                    self.m, "_run", side_effect=lambda command, capture=False: captured.append(command)
                ):
            rc = self.m.release(argparse.Namespace(task_id=self.task))
        self.assertEqual(rc, 0)
        command = captured[0]
        self.assertIn("--session-id", command)
        self.assertIn("live-session", command)
        self.assertIn("canonical-lease-token.g8", command[-1])

    def test_source_does_not_read_credentials(self):
        source = SCRIPT.read_text()
        self.assertNotIn("TIBIA_TEST_EMAIL", source)
        self.assertNotIn("TIBIA_TEST_PASSWORD", source)


if __name__ == "__main__":
    unittest.main()
