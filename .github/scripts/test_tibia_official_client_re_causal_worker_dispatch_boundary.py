#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

WORKER_PATH = Path(__file__).with_name("tibia-official-client-re-player-state-causal-worker.py")


def load_worker():
    spec = importlib.util.spec_from_file_location("causal_worker_dispatch_boundary", WORKER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("worker module unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class Clock:
    def __init__(self, now: float = 100.0):
        self.now = now

    def __call__(self) -> float:
        return self.now


class DispatchBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.m = load_worker()
        payload = {
            "schema_version": 1,
            "kind": "move",
            "parameters": {"direction": "east", "tiles": 1},
        }
        payload["action_hash"] = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        self.request = payload
        self.registration = {
            "schema_version": 1,
            "runtime_id": "track-a-canonical-live",
            "registration_generation": 4,
            "lease_generation": 27,
            "pid": 646,
            "process_start_ticks": 1394843,
            "client_version": "15.32",
            "client_size": 52109920,
            "client_sha256": self.m.SHA,
            "display": ":1",
            "window_identity": "x11:0x400011:pid:646:class:client/Tibia:title_sha256:" + "b" * 64,
            "runtime_locator": "docker:otclient-track-a-kasmvnc:container123",
            "state": "UNKNOWN",
            "proof_kind": "existing_runtime_adoption_v1",
        }
        self.candidate = {
            "state": "AVAILABLE",
            "reader_id": "player_state_typed_reader",
            "position": {"x": 100, "y": 200, "z": 7},
            "object_count": 1,
            "position_mirror_consistent": True,
            "process_memory_access": "read_only",
            "semantic_state": "CANDIDATE_PENDING_CAUSAL_E2E",
            "semantic_promotion_allowed": False,
        }

    def test_deadline_before_subprocess_creation_is_refused_effect_zero(self):
        clock = Clock()
        budget = self.m.DeadlineBudget(
            clock() + self.m.RESULT_WRITE_RESERVE_SECONDS + 1.0,
            clock=clock,
        )

        def baseline(_reg, _budget):
            clock.now += 1.0
            return self.candidate

        with mock.patch.object(self.m.subprocess, "run") as run:
            result = self.m.execute_once(
                self.request,
                self.registration,
                budget=budget,
                read_candidate_fn=baseline,
                tool_ready_fn=lambda _target, _budget: True,
                dispatch_fn=self.m.dispatch,
            )
        self.assertEqual(result["status"], "REFUSED")
        self.assertEqual(result["effect_count"], 0)
        self.assertEqual(result["reason_code"], "INPUT_DISPATCH_DEADLINE_BEFORE_START")
        run.assert_not_called()

    def test_spawn_failure_is_refused_effect_zero(self):
        clock = Clock()
        budget = self.m.DeadlineBudget(clock() + 10.0, clock=clock)
        with mock.patch.object(self.m.subprocess, "run", side_effect=FileNotFoundError("docker")):
            result = self.m.execute_once(
                self.request,
                self.registration,
                budget=budget,
                read_candidate_fn=lambda _reg, _budget: self.candidate,
                tool_ready_fn=lambda _target, _budget: True,
                dispatch_fn=self.m.dispatch,
            )
        self.assertEqual(result["status"], "REFUSED")
        self.assertEqual(result["effect_count"], 0)
        self.assertEqual(result["reason_code"], "INPUT_DISPATCH_NOT_STARTED")


if __name__ == "__main__":
    unittest.main()
