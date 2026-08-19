#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("tibia-official-client-re-kasm-existing-runtime-probe.py")


def load():
    spec = importlib.util.spec_from_file_location("kasm_probe_tested", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class Fake:
    def __init__(
        self,
        second: bool = False,
        wrong_sha: bool = False,
        wrong_pid: bool = False,
        bridge: bool = True,
        bridge_bad: bool = False,
    ):
        self.second = second
        self.wrong_sha = wrong_sha
        self.wrong_pid = wrong_pid
        self.bridge = bridge
        self.bridge_bad = bridge_bad
        self.commands: list[list[str]] = []

    def __call__(self, cmd):
        self.commands.append(list(cmd))
        text = " ".join(cmd)
        module = load()
        if cmd[:3] == ["docker", "ps", "--format"]:
            return "abc123\totclient-track-a-kasmvnc\n" + ("def456\tother\n" if self.second else "")
        if cmd[:2] == ["docker", "exec"] and "xwininfo -root -tree" in text:
            return '    0x1a00017 "Tibia - Redacted Character": ("client" "Tibia") 3440x1174+0+24\n'
        if cmd[:2] == ["docker", "exec"] and "xprop -id" in text:
            pid = 999 if self.wrong_pid else 11365
            return f'_NET_WM_PID(CARDINAL) = {pid}\nWM_CLASS(STRING) = "client", "Tibia"\n'
        if cmd[:3] == ["docker", "exec", "abc123"] and "for d in /proc" in text:
            sha = "0" * 64 if self.wrong_sha else module.SHA
            return f"11365\t/home/u/Tibia-x/bin/client\t{module.SIZE}\t{sha}\t74970818\n"
        if cmd[:3] == ["docker", "exec", "def456"] and "for d in /proc" in text:
            return f"222\t/home/u/Tibia-y/bin/client\t{module.SIZE}\t{module.SHA}\t11\n"
        if cmd[:3] == ["docker", "exec", "abc123"] and "pid=11365" in text:
            return (
                f"EXE=/home/u/Tibia-x/bin/client\nSIZE={module.SIZE}\nSHA={module.SHA}\n"
                f"START=74970818\nBOOT={'b' * 64}\n"
            )
        if cmd[:3] == ["docker", "exec", "abc123"] and "if [ -S" in text:
            return "PRESENT\n" if self.bridge else "ABSENT\n"
        if cmd[:3] == ["docker", "exec", "abc123"] and len(cmd) > 3 and cmd[3] == "python3":
            rows = [
                {
                    "ok": True,
                    "command": "PING",
                    "pid": 11365,
                    "process_start_ticks": 74970818,
                    "client_size": module.SIZE,
                    "client_sha256": module.SHA,
                }
            ]
            for index, target in enumerate(module.BRIDGE_TARGETS):
                rows.append(
                    {
                        "ok": True,
                        "target": target,
                        "scan_status": "OK",
                        "validated_hits": 0 if self.bridge_bad and index == 0 else 1,
                    }
                )
            return json.dumps(rows)
        if cmd[:3] == ["docker", "exec", "def456"]:
            return ""
        raise AssertionError(cmd)


class Tests(unittest.TestCase):
    def setUp(self):
        self.m = load()

    def test_exact_single_target_requires_structural_bridge_for_ingame(self):
        fake = Fake()
        payload = self.m.collect(fake)
        self.assertEqual(payload["proof_kind"], self.m.PROOF_KIND)
        self.assertEqual(payload["candidate_count"], 1)
        self.assertTrue(payload["inventory_complete"])
        self.assertEqual(payload["state"], "IN_GAME")
        self.assertEqual(payload["state_evidence"], "BRIDGE_3_OF_3")
        self.assertNotIn("Redacted Character", payload["window_identity"])
        self.assertEqual(payload["client_sha256"], self.m.SHA)
        self.assertFalse(any("/proc/$pid/environ" in " ".join(cmd) for cmd in fake.commands))

    def test_title_alone_never_promotes_ingame_without_structural_bridge(self):
        payload = self.m.collect(Fake(bridge=False))
        self.assertEqual(payload["state"], "UNKNOWN")
        self.assertEqual(payload["state_evidence"], "NO_STRUCTURAL_BRIDGE")

    def test_structural_bridge_mismatch_fails_closed(self):
        with self.assertRaisesRegex(self.m.ProbeError, "bridge_player_protocol_handler_not_unique"):
            self.m.collect(Fake(bridge_bad=True))

    def test_second_exact_candidate_fails_closed(self):
        with self.assertRaises(self.m.ProbeError):
            self.m.collect(Fake(second=True))

    def test_official_looking_wrong_sha_fails_closed(self):
        with self.assertRaisesRegex(self.m.ProbeError, "conflicting_official_client_candidate"):
            self.m.collect(Fake(wrong_sha=True))

    def test_window_pid_mismatch_fails_closed(self):
        with self.assertRaisesRegex(self.m.ProbeError, "window_pid_mismatch"):
            self.m.collect(Fake(wrong_pid=True))


if __name__ == "__main__":
    unittest.main()
