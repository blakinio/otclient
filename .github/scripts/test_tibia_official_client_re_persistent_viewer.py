#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).with_name("tibia-official-client-re-persistent-viewer.py")


def load():
    spec = importlib.util.spec_from_file_location("viewer_tested", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ViewerTests(unittest.TestCase):
    def setUp(self):
        self.m = load()
        self.binding = {
            "runtime_id": "track-a-canonical-live",
            "boot_id_sha256": "b" * 64,
            "pid": 4242,
            "process_start_ticks": 99,
            "client_size": 100,
            "client_sha256": "c" * 64,
            "display": ":99",
            "window_identity": "x11-window:12582929",
        }

    def test_viewer_identity_is_runtime_bound_not_controller_bound(self):
        identity = self.m._viewer_identity(self.binding, "instance", 6081)
        self.assertEqual(identity["pid"], 4242)
        self.assertEqual(identity["backend_port"], 6081)
        for forbidden in (
            "controller_session",
            "controller_task",
            "lease_generation",
            "registration_generation",
            "token",
        ):
            self.assertNotIn(forbidden, identity)

    def test_environment_strips_runner_tracking_credentials_and_capabilities(self):
        with mock.patch.dict(
            os.environ,
            {
                "RUNNER_TRACKING_ID": "runner",
                "TIBIA_TEST_EMAIL": "secret",
                "TIBIA_TEST_PASSWORD": "secret",
                "TRACK_A_CANONICAL_LEASE_TOKEN": "secret",
                "OTHER_CAPABILITY": "secret",
                "SAFE": "yes",
            },
            clear=True,
        ):
            env = self.m._sanitized_env({"DISPLAY": ":99"})
        self.assertEqual(env, {"SAFE": "yes", "DISPLAY": ":99"})

    def test_runtime_health_remains_pass_when_only_viewer_state_is_missing(self):
        registration = dict(self.binding)
        calls = 0

        def safe_json(_path, **_kwargs):
            nonlocal calls
            calls += 1
            if calls == 1:
                return registration
            raise self.m.ViewerError("state_missing")

        with mock.patch.object(self.m, "_safe_json", side_effect=safe_json), \
                mock.patch.object(self.m, "_runtime_binding", return_value=dict(self.binding)), \
                mock.patch.object(self.m, "_resolve_toolroot", return_value=Path("/tool")), \
                mock.patch.object(self.m, "_resolve_window", return_value=12582929):
            result = self.m._health(
                registration_path=Path("/registration"),
                state_dir=Path("/viewer"),
                toolroot=Path("/tool"),
            )
        self.assertEqual(result["runtime_health"], "PASS")
        self.assertEqual(result["viewer_health"], "FAIL_STATE_MISSING")

    def test_runtime_binding_failure_is_not_relabelled_as_viewer_failure(self):
        with mock.patch.object(self.m, "_safe_json", return_value=dict(self.binding)), \
                mock.patch.object(
                    self.m,
                    "_runtime_binding",
                    side_effect=self.m.ViewerError("runtime_process_missing"),
                ):
            with self.assertRaisesRegex(self.m.ViewerError, "runtime_process_missing"):
                self.m._health(
                    registration_path=Path("/registration"),
                    state_dir=Path("/viewer"),
                    toolroot=Path("/tool"),
                )

    def test_noncanonical_state_override_is_contract_test_only(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(
                self.m.ViewerError, "noncanonical_viewer_state_override"
            ):
                self.m._contract_override(
                    Path("/tmp/viewer"), self.m.VIEWER_STATE, "noncanonical_viewer_state_override"
                )
        with mock.patch.dict(
            os.environ, {"TRACK_A_PERSISTENT_VIEWER_CONTRACT_TEST": "1"}, clear=True
        ):
            self.assertEqual(
                self.m._contract_override(Path("/tmp/viewer"), self.m.VIEWER_STATE, "bad"),
                Path("/tmp/viewer"),
            )

    def test_source_fixes_backend_public_port_split_and_is_view_only(self):
        source = SCRIPT.read_text()
        self.assertIn("DEFAULT_BACKEND_PORT = 6081", source)
        self.assertIn('DEFAULT_PUBLIC_URL = "http://synology:6082/"', source)
        self.assertIn('"-viewonly"', source)
        self.assertIn('"viewer-identity.json"', source)
        self.assertIn("_resolve_window(binding", source)
        self.assertNotIn("xdotool", source)

    def test_source_does_not_read_or_persist_tibia_credentials(self):
        source = SCRIPT.read_text()
        self.assertNotIn('os.environ.get("TIBIA_TEST_', source)
        self.assertNotIn('os.getenv("TIBIA_TEST_', source)
        self.assertNotIn("clipboard", source.lower())


if __name__ == "__main__":
    unittest.main()
