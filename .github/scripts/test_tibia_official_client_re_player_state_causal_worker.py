#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import hashlib
import json
import tempfile
import unittest
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("tibia-official-client-re-player-state-causal-worker.py")


def load_module():
    spec = importlib.util.spec_from_file_location("player_state_causal_worker", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("worker module unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PlayerStateCausalWorkerTests(unittest.TestCase):
    def setUp(self):
        self.m = load_module()
        self.action_hash = hashlib.sha256(json.dumps({"schema_version":1,"kind":"move","parameters":{"direction":"east","tiles":1}}, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    def request(self, direction="east", tiles=1):
        payload = {
            "schema_version": 1,
            "kind": "move",
            "parameters": {"direction": direction, "tiles": tiles},
        }
        payload["action_hash"] = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        return payload

    def registration(self):
        return {
            "schema_version": 1,
            "runtime_id": "track-a-canonical-live",
            "registration_generation": 4,
            "lease_generation": 27,
            "pid": 646,
            "process_start_ticks": 1394843,
            "client_version": "15.32",
            "client_size": 52109920,
            "client_sha256": "ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8",
            "display": ":1",
            "window_identity": "x11:0x400011:pid:646:class:client/Tibia:title_sha256:" + "b" * 64,
            "runtime_locator": "docker:otclient-track-a-kasmvnc:container123",
            "state": "UNKNOWN",
            "proof_kind": "existing_runtime_adoption_v1",
        }

    @staticmethod
    def candidate(x, y, z=7):
        return {
            "state": "AVAILABLE",
            "reader_id": "player_state_typed_reader",
            "position": {"x": x, "y": y, "z": z},
            "object_count": 1,
            "position_mirror_consistent": True,
            "process_memory_access": "read_only",
            "semantic_state": "CANDIDATE_PENDING_CAUSAL_E2E",
            "semantic_promotion_allowed": False,
        }

    def test_request_accepts_only_one_cardinal_tile(self):
        self.assertEqual(self.m.validate_request(self.request())["parameters"]["direction"], "east")
        for bad in (
            self.request("north-east"),
            self.request("east", 2),
            {**self.request(), "extra": True},
        ):
            with self.assertRaises(self.m.WorkerRefusal):
                self.m.validate_request(bad)

    def test_request_rejects_hash_not_bound_to_semantic_payload(self):
        bad = self.request()
        bad["action_hash"] = "f" * 64
        with self.assertRaises(self.m.WorkerRefusal):
            self.m.validate_request(bad)

    def test_registration_requires_current_exact_fence_and_xres_bound_pid(self):
        target = self.m.validate_registration(self.registration())
        self.assertEqual(target.container, "otclient-track-a-kasmvnc")
        self.assertEqual(target.window_id, "0x400011")
        bad = self.registration(); bad["client_sha256"] = "0" * 64
        with self.assertRaises(self.m.WorkerRefusal):
            self.m.validate_registration(bad)
        bad = self.registration(); bad["window_identity"] = bad["window_identity"].replace("pid:646", "pid:647")
        with self.assertRaises(self.m.WorkerRefusal):
            self.m.validate_registration(bad)

    def test_candidate_requires_unique_mirrored_plausible_pending_causal_position(self):
        self.assertEqual(self.m.validate_candidate(self.candidate(100, 200)), (100, 200, 7))
        bad = self.candidate(100, 200); bad["position_mirror_consistent"] = False
        with self.assertRaises(self.m.WorkerRefusal):
            self.m.validate_candidate(bad)
        bad = self.candidate(100, 200); bad["semantic_state"] = "PROVEN"
        with self.assertRaises(self.m.WorkerRefusal):
            self.m.validate_candidate(bad)

    def test_exact_direction_delta_confirms_one_tile(self):
        self.assertTrue(self.m.delta_confirms((100, 200, 7), (101, 200, 7), "east"))
        self.assertTrue(self.m.delta_confirms((100, 200, 7), (99, 200, 7), "west"))
        self.assertTrue(self.m.delta_confirms((100, 200, 7), (100, 199, 7), "north"))
        self.assertTrue(self.m.delta_confirms((100, 200, 7), (100, 201, 7), "south"))
        self.assertFalse(self.m.delta_confirms((100, 200, 7), (102, 200, 7), "east"))
        self.assertFalse(self.m.delta_confirms((100, 200, 7), (101, 200, 8), "east"))

    def test_dispatch_command_uses_validated_xid_not_pid_selector(self):
        target = self.m.validate_registration(self.registration())
        command = self.m.dispatch_command(target, "east")
        joined = " ".join(command)
        self.assertIn("xdotool key --window 4194321 Right", joined)
        self.assertNotIn("--pid", joined)
        self.assertNotIn("search", joined)

    def test_run_refuses_before_effect_when_baseline_is_unavailable(self):
        calls = []
        result = self.m.execute_once(
            self.request(), self.registration(),
            read_candidate=lambda _reg: {"state": "UNAVAILABLE"},
            tool_ready=lambda _target: True,
            dispatch=lambda _command: calls.append("dispatch") or 0,
            sleep=lambda _seconds: None,
            reconciliation_attempts=1,
        )
        self.assertEqual(result["status"], "REFUSED")
        self.assertEqual(result["effect_count"], 0)
        self.assertEqual(calls, [])

    def test_run_dispatches_exactly_once_and_confirms_causal_delta(self):
        reads = iter([self.candidate(100, 200), self.candidate(101, 200)])
        commands = []
        result = self.m.execute_once(
            self.request(), self.registration(),
            read_candidate=lambda _reg: next(reads),
            tool_ready=lambda _target: True,
            dispatch=lambda command: commands.append(tuple(command)) or 0,
            sleep=lambda _seconds: None,
            reconciliation_attempts=2,
        )
        self.assertEqual(result, {"status": "CONFIRMED", "effect_count": 1, "action_hash": self.action_hash})
        self.assertEqual(len(commands), 1)

    def test_no_delta_after_dispatch_is_ambiguous_without_retry(self):
        reads = iter([self.candidate(100, 200), self.candidate(100, 200), self.candidate(100, 200)])
        commands = []
        result = self.m.execute_once(
            self.request(), self.registration(),
            read_candidate=lambda _reg: next(reads),
            tool_ready=lambda _target: True,
            dispatch=lambda command: commands.append(tuple(command)) or 0,
            sleep=lambda _seconds: None,
            reconciliation_attempts=2,
        )
        self.assertEqual(result["status"], "AMBIGUOUS")
        self.assertEqual(result["reason_code"], "MOVE_DELTA_NOT_CONFIRMED")
        self.assertEqual(result["effect_count"], 1)
        self.assertEqual(len(commands), 1)

    def test_dispatch_error_is_ambiguous_and_never_retried(self):
        commands = []
        result = self.m.execute_once(
            self.request(), self.registration(),
            read_candidate=lambda _reg: self.candidate(100, 200),
            tool_ready=lambda _target: True,
            dispatch=lambda command: commands.append(tuple(command)) or 9,
            sleep=lambda _seconds: None,
            reconciliation_attempts=2,
        )
        self.assertEqual(result["status"], "AMBIGUOUS")
        self.assertEqual(result["reason_code"], "INPUT_DISPATCH_UNCERTAIN")
        self.assertEqual(result["effect_count"], 1)
        self.assertEqual(len(commands), 1)

    def test_cli_writes_only_sanitized_result_keys(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            request_path = root / "request.json"
            result_path = root / "result.json"
            request_path.write_text(json.dumps(self.request()))
            reg_path = root / "registration.json"
            reg_path.write_text(json.dumps(self.registration()))
            result = {"status": "CONFIRMED", "effect_count": 1, "action_hash": self.action_hash}
            self.m.write_result(result_path, result)
            parsed = json.loads(result_path.read_text())
            self.assertEqual(set(parsed), {"status", "effect_count", "action_hash"})


if __name__ == "__main__":
    unittest.main()
