#!/usr/bin/env python3
from __future__ import annotations

import argparse
from contextlib import contextmanager
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import types
import unittest
from unittest import mock

SCRIPT = Path(__file__).with_name("tibia-official-client-re-canonical-live-transition.py")


def load_module():
    spec = importlib.util.spec_from_file_location("track_a_transition_tested", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class FakeManager:
    generation = 1

    def __init__(self, _state_dir: Path) -> None:
        pass

    @contextmanager
    def locked(self):
        yield 9

    def _load_state_unlocked(self):
        return {"generation": self.generation}

    def _require_current_unlocked(self, state, identity, token, now):
        if state["generation"] != self.generation or token != "token":
            raise RuntimeError("not current")


class FakeLease:
    LeaseManager = FakeManager

    @staticmethod
    def LeaseIdentity(task: str, session: str):
        return (task, session)

    @staticmethod
    def _read_private_token(_path: Path):
        return "token"

    @staticmethod
    def _now_epoch(_value):
        return 100


class FakePopen:
    def __init__(self, _command, **kwargs) -> None:
        self.pid = 777
        self.kwargs = kwargs

    def wait(self, timeout=None):
        return 0


class TransitionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.m = load_module()
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.m.STATE_DIR = root
        self.m.REGISTRATION = root / "runtime-registration.json"
        self.args = argparse.Namespace(
            task_id="OTC-TEST",
            session_id="session-test",
            token_file=root / "token",
            worker=Path("/fake/worker"),
            probe=Path("/fake/worker"),
            worker_timeout=2,
        )
        self.identity = {
            "boot_id_sha256": "b" * 64,
            "pid": 4242,
            "process_start_ticks": 12345,
            "client_size": self.m.EXPECTED_SIZE,
            "client_sha256": self.m.EXPECTED_SHA256,
        }
        self.manifest = {
            "pid": 4242,
            "process_group_id": 777,
            "display": ":104",
            "window_identity": "x11-window:9001",
            "remote_view_endpoint": "127.0.0.1:6091",
            "remote_view_mapping": "PROVEN",
            "state": "LOGIN",
        }

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def common_patches(self):
        return (
            mock.patch.object(self.m, "_load_lease_module", return_value=FakeLease),
            mock.patch.object(self.m, "_identity", return_value=dict(self.identity)),
            mock.patch.object(self.m, "_exact_identity", return_value=None),
        )

    def registration(self, lease_generation=1, registration_generation=1):
        return {
            "schema_version": 1,
            "runtime_id": self.m.RUNTIME_ID,
            "registration_generation": registration_generation,
            "lease_generation": lease_generation,
            "registered_at": 1,
            "boot_id_sha256": self.identity["boot_id_sha256"],
            "pid": 4242,
            "process_start_ticks": self.identity["process_start_ticks"],
            "client_version": self.m.EXPECTED_VERSION,
            "client_size": self.m.EXPECTED_SIZE,
            "client_sha256": self.m.EXPECTED_SHA256,
            "display": self.manifest["display"],
            "window_identity": self.manifest["window_identity"],
            "remote_view_endpoint": self.manifest["remote_view_endpoint"],
            "remote_view_mapping": self.manifest["remote_view_mapping"],
            "state": self.manifest["state"],
            "source_task": "old-task",
            "source_run": "old-run",
        }

    def write_registration(self, data):
        self.m.STATE_DIR.mkdir(parents=True, exist_ok=True)
        self.m.REGISTRATION.write_text(json.dumps(data), encoding="utf-8")
        self.m.REGISTRATION.chmod(0o600)

    def test_bootstrap_commits_only_after_post_probe(self):
        candidates = iter(([], [4242], [4242]))
        p1, p2, p3 = self.common_patches()
        with p1, p2, p3, \
             mock.patch.object(self.m, "_candidate_pids", side_effect=lambda: next(candidates)), \
             mock.patch.object(self.m.subprocess, "Popen", FakePopen), \
             mock.patch.object(self.m, "_load_manifest", return_value=dict(self.manifest)), \
             mock.patch.object(self.m, "_run_probe", return_value=dict(self.manifest)) as probe:
            self.m.bootstrap(self.args)
        data = self.m._read_registration()
        self.assertIsNotNone(data)
        self.assertEqual(data["lease_generation"], 1)
        self.assertEqual(data["registration_generation"], 1)
        self.assertEqual(stat.S_IMODE(self.m.REGISTRATION.stat().st_mode), 0o600)
        self.assertEqual(probe.call_count, 1)

    def test_bootstrap_failure_cleans_only_spawned_group_and_no_registration(self):
        candidates = iter(([], [4242]))
        killed = []
        p1, p2, p3 = self.common_patches()
        with p1, p2, p3, \
             mock.patch.object(self.m, "_candidate_pids", side_effect=lambda: next(candidates)), \
             mock.patch.object(self.m.subprocess, "Popen", FakePopen), \
             mock.patch.object(self.m, "_load_manifest", return_value=dict(self.manifest)), \
             mock.patch.object(self.m, "_run_probe", side_effect=self.m.TransitionError("post_probe_failed")), \
             mock.patch.object(self.m, "_terminate_group", side_effect=lambda pgid: killed.append(pgid)):
            with self.assertRaises(self.m.TransitionError):
                self.m.bootstrap(self.args)
        self.assertEqual(killed, [777])
        self.assertFalse(self.m.REGISTRATION.exists())

    def test_bootstrap_refuses_existing_candidate_before_spawn(self):
        p1, p2, p3 = self.common_patches()
        with p1, p2, p3, \
             mock.patch.object(self.m, "_candidate_pids", return_value=[999]), \
             mock.patch.object(self.m.subprocess, "Popen") as popen:
            with self.assertRaisesRegex(self.m.TransitionError, "official_client_candidate_present"):
                self.m.bootstrap(self.args)
        popen.assert_not_called()

    def test_rebind_is_metadata_only_and_advances_generation(self):
        self.write_registration(self.registration(lease_generation=1, registration_generation=4))
        FakeManager.generation = 2
        p1, p2, p3 = self.common_patches()
        try:
            with p1, p2, p3, \
                 mock.patch.object(self.m, "_candidate_pids", return_value=[4242]), \
                 mock.patch.object(self.m, "_run_probe", return_value=dict(self.manifest)):
                self.m.rebind(self.args)
            data = self.m._read_registration()
            self.assertEqual(data["lease_generation"], 2)
            self.assertEqual(data["registration_generation"], 5)
            self.assertEqual(data["pid"], 4242)
        finally:
            FakeManager.generation = 1

    def test_gate_b_requires_generation_binding_and_unique_registered_pid(self):
        self.write_registration(self.registration())
        p1, p2, p3 = self.common_patches()
        with p1, p2, p3, \
             mock.patch.object(self.m, "_candidate_pids", return_value=[4242]), \
             mock.patch.object(self.m, "_run_probe", return_value=dict(self.manifest)):
            self.m.gate_b(self.args)
        FakeManager.generation = 2
        try:
            p1, p2, p3 = self.common_patches()
            with p1, p2, p3, mock.patch.object(self.m, "_run_probe", return_value=dict(self.manifest)):
                with self.assertRaisesRegex(self.m.TransitionError, "registration_generation_mismatch"):
                    self.m.gate_b(self.args)
        finally:
            FakeManager.generation = 1

    def test_probe_environment_drops_capability_material(self):
        with mock.patch.dict(os.environ, {
            "TRACK_A_CANONICAL_LEASE_TOKEN": "secret",
            "SOME_CAPABILITY": "secret2",
            "SAFE_VALUE": "ok",
        }, clear=True):
            env = self.m._sanitized_env()
        self.assertNotIn("TRACK_A_CANONICAL_LEASE_TOKEN", env)
        self.assertNotIn("SOME_CAPABILITY", env)
        self.assertEqual(env["SAFE_VALUE"], "ok")


if __name__ == "__main__":
    unittest.main()
