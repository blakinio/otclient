#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).with_name("tibia-official-client-re-canonical-live-xres-probe.py")


def load():
    spec = importlib.util.spec_from_file_location("xres_probe_tested", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CanonicalXResProbeTests(unittest.TestCase):
    def setUp(self):
        self.m = load()

    def test_listener_must_belong_to_expected_process(self):
        with mock.patch.object(self.m, "_listener_inodes", return_value={"123"}), \
                mock.patch.object(self.m, "_process_socket_inodes", return_value={"123", "999"}):
            self.m._require_listener(42, 5901, "vnc")
        with mock.patch.object(self.m, "_listener_inodes", return_value={"123"}), \
                mock.patch.object(self.m, "_process_socket_inodes", return_value={"999"}):
            with self.assertRaisesRegex(self.m.ProbeError, "listener_owner_mismatch"):
                self.m._require_listener(42, 5901, "vnc")

    def test_role_validation_rejects_secret_or_capability_environment(self):
        env = {
            self.m.TRACK_MARK,
            self.m.RUNTIME_MARK,
            self.m.ROLE_MARK + "client",
            "TIBIA_TEST_EMAIL=should-never-survive",
        }
        with mock.patch.object(self.m, "_pgrp", return_value=77), \
                mock.patch.object(self.m, "_proc_env", return_value=env):
            with self.assertRaisesRegex(self.m.ProbeError, "tracked_process_secret_env_leak"):
                self.m._require_role(42, "client", 77)

    def test_raw_xres_window_requires_numeric_positive_xid(self):
        ok = mock.Mock(returncode=0, stdout="12582929\n")
        with mock.patch.object(self.m.subprocess, "run", return_value=ok):
            self.assertEqual(self.m._raw_xres_window(":99", 42, Path("/tool")), 12582929)
        bad = mock.Mock(returncode=0, stdout="not-an-xid\n")
        with mock.patch.object(self.m.subprocess, "run", return_value=bad):
            with self.assertRaisesRegex(self.m.ProbeError, "raw_xres_window_invalid"):
                self.m._raw_xres_window(":99", 42, Path("/tool"))

    def test_probe_manifest_uses_raw_xres_identity_and_exact_roles(self):
        roles = {"client": 41, "xvfb": 42, "vnc": 43, "wireproxy": 44}
        values = {
            "bootstrap-pgid": 40,
            "client.pid": 41,
            "xvfb.pid": 42,
            "vnc.pid": 43,
            "wireproxy.pid": 44,
            "vnc-port": 5901,
            "warp-port": 25354,
        }

        def positive(path: Path) -> int:
            return values[path.name]

        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "manifest.json"
            with mock.patch.dict(
                self.m.os.environ,
                {"RUNNER_NAME": "synology-otclient-01", "GITHUB_REPOSITORY": "blakinio/otclient"},
                clear=True,
            ), mock.patch.object(self.m.SESSION, "is_dir", return_value=True), \
                    mock.patch.object(self.m, "_positive_int", side_effect=positive), \
                    mock.patch.object(self.m, "_toolroot", return_value=Path("/tool")), \
                    mock.patch.object(self.m, "_within", side_effect=lambda _root, path: path), \
                    mock.patch.object(
                        self.m,
                        "_safe_text",
                        side_effect=lambda path: {
                            "wireproxy-bin": "/tool/wireproxy",
                            "display": ":99",
                        }.get(path.name, ""),
                    ), \
                    mock.patch.object(self.m, "_require_role") as require_role, \
                    mock.patch.object(self.m, "_display", return_value=(":99", 99)), \
                    mock.patch.object(self.m, "_require_listener") as require_listener, \
                    mock.patch.object(self.m, "_rfb_banner") as rfb, \
                    mock.patch.object(self.m, "_raw_xres_window", return_value=12582929) as xres:
                result = self.m.probe(output)

            self.assertEqual(result["tracked_processes"], roles)
            self.assertEqual(result["window_identity"], "x11-window:12582929")
            self.assertEqual(result["remote_view_endpoint"], "127.0.0.1:5901")
            self.assertEqual(result["remote_view_mapping"], "PROVEN")
            self.assertEqual(require_role.call_count, 4)
            self.assertEqual(require_listener.call_count, 2)
            rfb.assert_called_once_with(5901)
            xres.assert_called_once_with(":99", 41, Path("/tool"))

    def test_source_contains_no_xdotool_window_lookup(self):
        source = SCRIPT.read_text()
        self.assertNotIn("xdotool", source)
        self.assertIn("tibia-official-client-re-xres-window-owner.py", source)
        self.assertIn("LocalClientPid", source)


if __name__ == "__main__":
    unittest.main()
