#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).with_name("tibia-official-client-re-persistent-viewer-controller.py")


def load():
    spec = importlib.util.spec_from_file_location("viewer_controller_tested", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PersistentViewerControllerTests(unittest.TestCase):
    def setUp(self):
        self.m = load()
        self.args = argparse.Namespace(
            task_id="OTC-TEST",
            session_id="fresh-session",
            token_file=Path("/task/token"),
            toolroot=None,
            x11vnc=None,
            websockify=None,
            novnc_root=None,
            rfb_port=5901,
            backend_port=6081,
            public_url="http://synology:6082/",
        )

    def test_gate_b_command_uses_raw_xres_probe(self):
        commands = []
        with mock.patch.object(self.m, "_run", side_effect=lambda cmd: commands.append(cmd) or 0):
            self.m._gate_b("OTC-TEST", "fresh-session", Path("/task/token"))
        command = commands[0]
        self.assertIn("gate-b", command)
        self.assertIn("--probe", command)
        self.assertIn("tibia-official-client-re-canonical-live-xres-probe.py", command[-1])

    def test_gate_b_failure_prevents_viewer_start(self):
        with mock.patch.object(
            self.m, "_gate_b", side_effect=self.m.ControllerError("gate_b_failed")
        ), mock.patch.object(self.m, "_run") as run:
            with self.assertRaises(self.m.ControllerError) as raised:
                self.m.start(self.args)
        self.assertEqual(raised.exception.code, "gate_b_failed")
        run.assert_not_called()

    def test_viewer_start_runs_only_after_gate_b(self):
        order = []
        with mock.patch.object(self.m, "_gate_b", side_effect=lambda *_: order.append("gate-b")), \
                mock.patch.object(self.m, "_run", side_effect=lambda _cmd: order.append("viewer") or 0):
            rc = self.m.start(self.args)
        self.assertEqual(rc, 0)
        self.assertEqual(order, ["gate-b", "viewer"])

    def test_defaults_keep_runner_backend_and_public_endpoint_distinct(self):
        args = self.m.parser().parse_args(
            [
                "start",
                "--task-id",
                "OTC-TEST",
                "--session-id",
                "fresh-session",
                "--token-file",
                "/task/token",
            ]
        )
        self.assertEqual(args.rfb_port, 5901)
        self.assertEqual(args.backend_port, 6081)
        self.assertEqual(args.public_url, "http://synology:6082/")


if __name__ == "__main__":
    unittest.main()
