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
NON_INGAME_STATES = ("UNKNOWN", "LOGIN", "CHARACTER_SELECT", "DISCONNECTED")


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
    @staticmethod
    def move_request():
        return {
            "schema_version": 1,
            "action_hash": "a" * 64,
            "kind": "move",
            "parameters": {"direction": "east", "tiles": 1},
        }

    @staticmethod
    def transition_registration(transition, state):
        return {
            "runtime_id": transition.RID,
            "registration_generation": 7,
            "lease_generation": 35,
            "boot_id_sha256": "b" * 64,
            "process_start_ticks": 1394843,
            "client_sha256": transition.SHA,
            "runtime_locator": "docker:otclient-track-a-kasmvnc:container123",
            "candidate_fingerprint": "c" * 64,
            "state": state,
        }

    @staticmethod
    def transition_manifest(state):
        return {
            "state": state,
            "window_identity": "x11:0x17:pid:646:class:client/Tibia:title_sha256:" + "d" * 64,
        }

    def test_guarded_move_non_ingame_states_refuse_before_ready(self):
        transition = load(TRANSITION, "transition_ingame_regression")
        request = self.move_request()
        args = SimpleNamespace(request_file=Path("unused"))
        for state in NON_INGAME_STATES:
            with self.subTest(state=state):
                registration = self.transition_registration(transition, state)
                manifest = self.transition_manifest(state)
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

    def test_guarded_move_state_drift_after_ready_refuses_before_worker(self):
        transition = load(TRANSITION, "transition_ingame_drift_regression")
        request = self.move_request()
        ingame_registration = self.transition_registration(transition, "IN_GAME")
        ingame_manifest = self.transition_manifest("IN_GAME")
        unknown_registration = self.transition_registration(transition, "UNKNOWN")
        unknown_manifest = self.transition_manifest("UNKNOWN")
        probes = [
            (ingame_registration, ingame_manifest),
            (ingame_registration, ingame_manifest),
            (unknown_registration, unknown_manifest),
        ]
        ready = mock.Mock()
        worker = mock.Mock()
        with mock.patch.object(transition, "_read_guarded_request", return_value=request), \
                mock.patch.object(transition, "_probe_reg", side_effect=probes), \
                mock.patch.object(transition, "_acquire_input_lock", return_value=Held()), \
                mock.patch.object(transition, "_emit_guarded_ready", ready), \
                mock.patch.object(transition, "_read_guarded_decision", return_value="COMMIT"), \
                mock.patch.object(transition, "_run_guarded_worker", worker):
            with self.assertRaisesRegex(
                transition.E, "guarded_dispatch_move_requires_proven_ingame"
            ):
                transition._guarded_dispatch(
                    SimpleNamespace(request_file=Path("unused")),
                    object(), object(), object(), object(), 35,
                )
        ready.assert_called_once()
        worker.assert_not_called()

    def test_guarded_move_proven_ingame_can_reach_worker(self):
        transition = load(TRANSITION, "transition_ingame_positive_regression")
        request = self.move_request()
        registration = self.transition_registration(transition, "IN_GAME")
        manifest = self.transition_manifest("IN_GAME")
        ready = mock.Mock()
        worker = mock.Mock(return_value={"status": "ABORTED", "effect_count": 0})
        args = SimpleNamespace(
            request_file=Path("unused"),
            token_file=Path("unused-token"),
        )
        with mock.patch.object(transition, "_read_guarded_request", return_value=request), \
                mock.patch.object(transition, "_probe_reg", return_value=(registration, manifest)), \
                mock.patch.object(transition, "_acquire_input_lock", return_value=Held()), \
                mock.patch.object(transition, "_emit_guarded_ready", ready), \
                mock.patch.object(transition, "_read_guarded_decision", return_value="COMMIT"), \
                mock.patch.object(transition, "_lease"), \
                mock.patch.object(transition, "_run_guarded_worker", worker):
            result = transition._guarded_dispatch(
                args, object(), object(), object(), object(), 35,
            )
        self.assertEqual(result, {"status": "ABORTED", "effect_count": 0})
        ready.assert_called_once()
        worker.assert_called_once()

    @staticmethod
    def worker_request(worker):
        semantic = {
            "schema_version": 1,
            "kind": "move",
            "parameters": {"direction": "east", "tiles": 1},
        }
        request = dict(semantic)
        request["action_hash"] = hashlib.sha256(
            json.dumps(semantic, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        return request

    @staticmethod
    def worker_registration(worker, state):
        return {
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
            "state": state,
            "proof_kind": worker.PROOF_KIND,
        }

    def test_worker_non_ingame_registration_refuses_before_dispatch(self):
        worker = load(WORKER, "worker_ingame_regression")
        request = self.worker_request(worker)
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
        for state in NON_INGAME_STATES:
            with self.subTest(state=state):
                dispatches = []
                result = worker.execute_once(
                    request,
                    self.worker_registration(worker, state),
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
