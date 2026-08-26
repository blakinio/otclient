#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

HERE = Path(__file__).resolve().parent
TRANSITION = HERE / "tibia-official-client-re-canonical-live-transition.py"
WORKER = HERE / "tibia-official-client-re-player-state-causal-worker.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class Held:
    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        return False


class InGameAdmissionRegressionTests(unittest.TestCase):
    def test_guarded_move_unknown_state_refuses_before_ready(self):
        transition = load(TRANSITION, "transition_ingame_regression")
        request = {
            "schema_version": 1,
            "action_hash": "a" * 64,
            "kind": "move",
            "parameters": {"direction": "east", "tiles": 1},
        }
        registration = {
            "runtime_id": transition.RID,
            "registration_generation": 7,
            "lease_generation": 35,
            "boot_id_sha256": "b" * 64,
            "process_start_ticks": 1394843,
            "client_sha256": transition.SHA,
            "runtime_locator": "docker:otclient-track-a-kasmvnc:container123",
            "candidate_fingerprint": "c" * 64,
            "state": "UNKNOWN",
        }
        manifest = {
            "state": "UNKNOWN",
            "window_identity": "x11:0x17:pid:646:class:client/Tibia:title_sha256:" + "d" * 64,
        }
        args = SimpleNamespace(request_file=Path("unused"))
        ready = mock.Mock()
        worker = mock.Mock()
        with mock.patch.object(transition, "_read_guarded_request", return_value=request), \
                mock.patch.object(transition, "_probe_reg", return_value=(registration, manifest)), \
                mock.patch.object(transition, "_acquire_input_lock", return_value=Held()), \
                mock.patch.object(transition, "_emit_guarded_ready", ready), \
                mock.patch.object(transition, "_read_guarded_decision", return_value="ABORT"), \
                mock.patch.object(transition, "_run_guarded_worker", worker):
            with self.assertRaisesRegex(
                transition.E, "guarded_dispatch_move_requires_proven_ingame"
            ):
                transition._guarded_dispatch(args, object(), object(), object(), object(), 35)
        ready.assert_not_called()
        worker.assert_not_called()

    def test_worker_unknown_registration_refuses_before_dispatch(self):
        worker = load(WORKER, "worker_ingame_regression")
        semantic = {
            "schema_version": 1,
            "kind": "move",
            "parameters": {"direction": "east", "tiles": 1},
        }
        request = dict(semantic)
        request["action_hash"] = hashlib.sha256(
            json.dumps(semantic, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        registration = {
            "schema_version": 1,
            "runtime_id": worker.RID,
            "registration_generation": 7,
            "lease_generation": 35,
            "pid": 646,
            "process_start_ticks": 1394843,
            "client_version": worker.VER,
            "client_size": worker.SIZE,
            "client_sha256": worker.SHA,
            "display": worker.DISPLAY,
            "window_identity": "x11:0x17:pid:646:class:client/Tibia:title_sha256:" + "d" * 64,
            "runtime_locator": "docker:otclient-track-a-kasmvnc:container123",
            "state": "UNKNOWN",
            "proof_kind": worker.PROOF_KIND,
        }
        candidate = {
            "state": "AVAILABLE",
            "reader_id": "player_state_typed_reader",
            "position": {"x": 100, "y": 200, "z": 7},
            "object_count": 1,
            "position_mirror_consistent": True,
            "process_memory_access": "read_only",
            "semantic_state": "CANDIDATE_PENDING_CAUSAL_E2E",
            "semantic_promotion_allowed": False,
        }
        dispatches = []
        result = worker.execute_once(
            request,
            registration,
            budget=worker.DeadlineBudget.start(),
            read_candidate_fn=lambda _reg, _budget: candidate,
            tool_ready_fn=lambda _target, _budget: True,
            dispatch_fn=lambda command, _budget: dispatches.append(tuple(command)) or 0,
            reconciliation_attempts=1,
        )
        self.assertEqual(result["status"], "REFUSED")
        self.assertEqual(result["effect_count"], 0)
        self.assertEqual(result["reason_code"], "SEMANTIC_PRECONDITION_FAILED")
        self.assertEqual(dispatches, [])


if __name__ == "__main__":
    unittest.main()
