#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

MODULE_PATH = Path(__file__).with_name("tibia-official-client-re-player-state-causal-worker.py")


def load_module():
    spec = importlib.util.spec_from_file_location("player_state_causal_worker", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("worker module unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class FakeClock:
    def __init__(self, now: float = 100.0):
        self.now = now

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


class PlayerStateCausalWorkerTests(unittest.TestCase):
    def setUp(self):
        self.m = load_module()
        self.action_hash = hashlib.sha256(
            json.dumps(
                {"schema_version": 1, "kind": "move", "parameters": {"direction": "east", "tiles": 1}},
                sort_keys=True,
                separators=(",", ":"),
            ).encode()
        ).hexdigest()

    def request(self, direction="east", tiles=1):
        payload = {
            "schema_version": 1,
            "kind": "move",
            "parameters": {"direction": direction, "tiles": tiles},
        }
        payload["action_hash"] = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
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

    def budget(self, seconds=10.0):
        clock = FakeClock()
        return clock, self.m.DeadlineBudget(clock() + seconds, clock=clock)

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
        bad = self.registration()
        bad["client_sha256"] = "0" * 64
        with self.assertRaises(self.m.WorkerRefusal):
            self.m.validate_registration(bad)
        bad = self.registration()
        bad["window_identity"] = bad["window_identity"].replace("pid:646", "pid:647")
        with self.assertRaises(self.m.WorkerRefusal):
            self.m.validate_registration(bad)

    def test_candidate_requires_unique_mirrored_plausible_pending_causal_position(self):
        self.assertEqual(self.m.validate_candidate(self.candidate(100, 200)), (100, 200, 7))
        bad = self.candidate(100, 200)
        bad["position_mirror_consistent"] = False
        with self.assertRaises(self.m.WorkerRefusal):
            self.m.validate_candidate(bad)
        bad = self.candidate(100, 200)
        bad["semantic_state"] = "PROVEN"
        with self.assertRaises(self.m.WorkerRefusal):
            self.m.validate_candidate(bad)

    def test_exact_direction_delta_confirms_one_tile(self):
        self.assertTrue(self.m.delta_confirms((100, 200, 7), (101, 200, 7), "east"))
        self.assertTrue(self.m.delta_confirms((100, 200, 7), (99, 200, 7), "west"))
        self.assertTrue(self.m.delta_confirms((100, 200, 7), (100, 199, 7), "north"))
        self.assertTrue(self.m.delta_confirms((100, 200, 7), (100, 201, 7), "south"))
        self.assertFalse(self.m.delta_confirms((100, 200, 7), (102, 200, 7), "east"))

    def test_dispatch_command_uses_validated_xid_not_pid_selector(self):
        target = self.m.validate_registration(self.registration())
        command = self.m.dispatch_command(target, "east")
        joined = " ".join(command)
        self.assertIn("xdotool key --window 4194321 Right", joined)
        self.assertNotIn("--pid", joined)
        self.assertNotIn("search", joined)

    def test_outer_timeout_contract_leaves_write_and_supervisor_margins(self):
        self.assertEqual(self.m.OUTER_GUARDED_DISPATCH_TIMEOUT_SECONDS, 30.0)
        self.assertEqual(
            self.m.WORKER_TOTAL_BUDGET_SECONDS + self.m.SUPERVISOR_RETURN_MARGIN_SECONDS,
            self.m.OUTER_GUARDED_DISPATCH_TIMEOUT_SECONDS,
        )
        self.assertGreater(
            self.m.WORKER_TOTAL_BUDGET_SECONDS,
            self.m.RESULT_WRITE_RESERVE_SECONDS,
        )
        self.assertGreaterEqual(self.m.SUPERVISOR_RETURN_MARGIN_SECONDS, 1.0)

    def test_bounded_subprocess_uses_only_remaining_operation_budget(self):
        clock = FakeClock()
        budget = self.m.DeadlineBudget(clock() + 8.0, clock=clock)
        seen = []

        def fake_run(*_args, **kwargs):
            seen.append(kwargs["timeout"])
            return mock.Mock(returncode=0, stdout="", stderr="")

        with mock.patch.object(self.m.subprocess, "run", side_effect=fake_run):
            self.m._run(["true"], budget, timeout_cap=20.0)
            clock.advance(4.5)
            self.m._run(["true"], budget, timeout_cap=20.0)

        self.assertAlmostEqual(seen[0], 6.0)
        self.assertAlmostEqual(seen[1], 1.5)
        self.assertLess(seen[1], seen[0])

    def test_slow_hung_baseline_reader_refuses_before_effect(self):
        clock, budget = self.budget(6.0)
        dispatches = []

        def hung_reader(_reg, _budget):
            clock.advance(4.0)
            raise subprocess.TimeoutExpired(["reader"], 4.0)

        result = self.m.execute_once(
            self.request(),
            self.registration(),
            budget=budget,
            read_candidate_fn=hung_reader,
            tool_ready_fn=lambda _target, _budget: True,
            dispatch_fn=lambda command, _budget: dispatches.append(tuple(command)) or 0,
            reconciliation_attempts=2,
        )
        self.assertEqual(result["status"], "REFUSED")
        self.assertEqual(result["effect_count"], 0)
        self.assertEqual(result["reason_code"], "SEMANTIC_PRECONDITION_FAILED")
        self.assertEqual(dispatches, [])

    def test_deadline_exhausted_during_precondition_is_explicit_refusal(self):
        clock, budget = self.budget(2.0)
        result = self.m.execute_once(
            self.request(),
            self.registration(),
            budget=budget,
            read_candidate_fn=lambda _reg, _budget: self.candidate(100, 200),
            tool_ready_fn=lambda _target, _budget: True,
            dispatch_fn=lambda _command, _budget: 0,
        )
        self.assertEqual(result["status"], "REFUSED")
        self.assertEqual(result["effect_count"], 0)
        self.assertEqual(result["reason_code"], "SEMANTIC_PRECONDITION_TIMEOUT")
        self.assertEqual(clock.now, 100.0)

    def test_dispatches_exactly_once_and_confirms_causal_delta(self):
        _clock, budget = self.budget(10.0)
        reads = iter([self.candidate(100, 200), self.candidate(101, 200)])
        commands = []
        result = self.m.execute_once(
            self.request(),
            self.registration(),
            budget=budget,
            read_candidate_fn=lambda _reg, _budget: next(reads),
            tool_ready_fn=lambda _target, _budget: True,
            dispatch_fn=lambda command, _budget: commands.append(tuple(command)) or 0,
            sleep_fn=lambda _seconds: None,
            reconciliation_attempts=2,
        )
        self.assertEqual(
            result,
            {"status": "CONFIRMED", "effect_count": 1, "action_hash": self.action_hash},
        )
        self.assertEqual(len(commands), 1)

    def test_slow_dispatch_is_ambiguous_and_never_retried(self):
        _clock, budget = self.budget(10.0)
        commands = []
        result = self.m.execute_once(
            self.request(),
            self.registration(),
            budget=budget,
            read_candidate_fn=lambda _reg, _budget: self.candidate(100, 200),
            tool_ready_fn=lambda _target, _budget: True,
            dispatch_fn=lambda command, _budget: commands.append(tuple(command)) or 255,
            reconciliation_attempts=3,
        )
        self.assertEqual(result["status"], "AMBIGUOUS")
        self.assertEqual(result["reason_code"], "INPUT_DISPATCH_UNCERTAIN")
        self.assertEqual(result["effect_count"], 1)
        self.assertEqual(len(commands), 1)

    def test_hung_post_dispatch_reader_exhausts_deadline_as_ambiguous_no_retry(self):
        clock, budget = self.budget(7.0)
        commands = []
        reads = 0

        def reader(_reg, _budget):
            nonlocal reads
            reads += 1
            if reads == 1:
                return self.candidate(100, 200)
            clock.advance(5.0)
            raise subprocess.TimeoutExpired(["reader"], 5.0)

        result = self.m.execute_once(
            self.request(),
            self.registration(),
            budget=budget,
            read_candidate_fn=reader,
            tool_ready_fn=lambda _target, _budget: True,
            dispatch_fn=lambda command, _budget: commands.append(tuple(command)) or 0,
            sleep_fn=clock.advance,
            reconciliation_attempts=12,
        )
        self.assertEqual(result["status"], "AMBIGUOUS")
        self.assertEqual(result["effect_count"], 1)
        self.assertEqual(result["reason_code"], "RECONCILIATION_DEADLINE_EXHAUSTED")
        self.assertEqual(len(commands), 1)

    def test_reconciliation_attempt_exhaustion_is_ambiguous_without_retry(self):
        _clock, budget = self.budget(10.0)
        reads = iter(
            [
                self.candidate(100, 200),
                self.candidate(100, 200),
                self.candidate(100, 200),
            ]
        )
        commands = []
        result = self.m.execute_once(
            self.request(),
            self.registration(),
            budget=budget,
            read_candidate_fn=lambda _reg, _budget: next(reads),
            tool_ready_fn=lambda _target, _budget: True,
            dispatch_fn=lambda command, _budget: commands.append(tuple(command)) or 0,
            sleep_fn=lambda _seconds: None,
            reconciliation_attempts=2,
        )
        self.assertEqual(result["status"], "AMBIGUOUS")
        self.assertEqual(result["reason_code"], "MOVE_DELTA_NOT_CONFIRMED")
        self.assertEqual(result["effect_count"], 1)
        self.assertEqual(len(commands), 1)

    def test_unexpected_delta_is_ambiguous_without_retry(self):
        _clock, budget = self.budget(10.0)
        reads = iter([self.candidate(100, 200), self.candidate(102, 200)])
        commands = []
        result = self.m.execute_once(
            self.request(),
            self.registration(),
            budget=budget,
            read_candidate_fn=lambda _reg, _budget: next(reads),
            tool_ready_fn=lambda _target, _budget: True,
            dispatch_fn=lambda command, _budget: commands.append(tuple(command)) or 0,
            reconciliation_attempts=2,
        )
        self.assertEqual(result["status"], "AMBIGUOUS")
        self.assertEqual(result["reason_code"], "UNEXPECTED_POSITION_DELTA")
        self.assertEqual(len(commands), 1)

    def test_result_write_refuses_to_start_without_durable_write_budget(self):
        clock = FakeClock()
        budget = self.m.DeadlineBudget(
            clock() + self.m.MIN_DURABLE_WRITE_START_SECONDS / 2,
            clock=clock,
        )
        with tempfile.TemporaryDirectory() as td:
            result_path = Path(td) / "result.json"
            with self.assertRaises(self.m.WorkerDeadlineExceeded):
                self.m.write_result(
                    result_path,
                    {"status": "AMBIGUOUS", "effect_count": 1, "action_hash": self.action_hash},
                    budget,
                )
            self.assertFalse(result_path.exists())
            self.assertEqual(list(Path(td).glob(".player-state-result-*")), [])

    def test_result_write_is_atomic_and_fsyncs_file_and_directory(self):
        _clock, budget = self.budget(5.0)
        with tempfile.TemporaryDirectory() as td:
            result_path = Path(td) / "result.json"
            real_fsync = os.fsync
            calls = []

            def recording_fsync(fd):
                calls.append(fd)
                return real_fsync(fd)

            with mock.patch.object(self.m.os, "fsync", side_effect=recording_fsync):
                self.m.write_result(
                    result_path,
                    {
                        "status": "AMBIGUOUS",
                        "effect_count": 1,
                        "action_hash": self.action_hash,
                        "reason_code": "MOVE_DELTA_NOT_CONFIRMED",
                        "forbidden": "raw",
                    },
                    budget,
                )
            parsed = json.loads(result_path.read_text())
            self.assertEqual(
                set(parsed),
                {"status", "effect_count", "action_hash", "reason_code"},
            )
            self.assertGreaterEqual(len(calls), 2)

    def test_worker_nonzero_on_result_write_failure_never_masks_success(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            request_path = root / "request.json"
            result_path = root / "result.json"
            registration_path = root / "registration.json"
            request_path.write_text(json.dumps(self.request()))
            registration_path.write_text(json.dumps(self.registration()))
            with mock.patch.object(self.m, "REGISTRATION", registration_path), \
                    mock.patch.object(
                        self.m,
                        "execute_once",
                        return_value={
                            "status": "CONFIRMED",
                            "effect_count": 1,
                            "action_hash": self.action_hash,
                        },
                    ), \
                    mock.patch.object(self.m, "write_result", side_effect=OSError("disk failed")):
                self.assertNotEqual(
                    self.m.main(["guarded-dispatch", str(request_path), str(result_path)]),
                    0,
                )


    def test_reconciliation_does_not_start_doomed_reader_that_consumes_write_reserve(self):
        clock, budget = self.budget(27.0)
        reads = 0
        commands = []

        def reader(_reg, current_budget):
            nonlocal reads
            reads += 1
            if reads <= 2:
                clock.advance(10.0)
                return self.candidate(100, 200)
            timeout = current_budget.timeout(
                self.m.READER_TIMEOUT_CAP_SECONDS,
                reserve=self.m.RESULT_WRITE_RESERVE_SECONDS,
            )
            clock.advance(timeout + 2.5)
            raise subprocess.TimeoutExpired(["reader"], timeout)

        result = self.m.execute_once(
            self.request(),
            self.registration(),
            budget=budget,
            read_candidate_fn=reader,
            tool_ready_fn=lambda _target, _budget: True,
            dispatch_fn=lambda command, _budget: commands.append(tuple(command)) or 0,
            sleep_fn=clock.advance,
            reconciliation_attempts=12,
        )
        self.assertEqual(reads, 2)
        self.assertEqual(result["status"], "AMBIGUOUS")
        self.assertEqual(result["effect_count"], 1)
        self.assertEqual(result["reason_code"], "RECONCILIATION_DEADLINE_EXHAUSTED")
        self.assertEqual(len(commands), 1)
        self.assertGreaterEqual(budget.remaining(), self.m.RESULT_WRITE_RESERVE_SECONDS)

    def test_post_dispatch_checkpoint_precedes_hung_reconciliation(self):
        clock, budget = self.budget(27.0)
        reads = 0
        events = []
        commands = []

        def reader(_reg, current_budget):
            nonlocal reads
            reads += 1
            if reads == 1:
                clock.advance(10.0)
                events.append("baseline")
                return self.candidate(100, 200)
            events.append("reconciliation")
            timeout = current_budget.timeout(
                self.m.READER_TIMEOUT_CAP_SECONDS,
                reserve=self.m.RESULT_WRITE_RESERVE_SECONDS,
            )
            clock.advance(timeout + 2.5)
            raise subprocess.TimeoutExpired(["reader"], timeout)

        checkpoints = []
        try:
            result = self.m.execute_once(
                self.request(),
                self.registration(),
                budget=budget,
                read_candidate_fn=reader,
                tool_ready_fn=lambda _target, _budget: True,
                dispatch_fn=lambda command, _budget: commands.append(tuple(command)) or 0,
                sleep_fn=clock.advance,
                reconciliation_attempts=12,
                post_dispatch_checkpoint_fn=lambda checkpoint, _budget: (
                    events.append("checkpoint"), checkpoints.append(dict(checkpoint))
                ),
            )
        except TypeError as exc:
            self.fail(f"post-dispatch checkpoint hook unavailable: {exc}")
        self.assertEqual(events[:3], ["baseline", "checkpoint", "reconciliation"])
        self.assertEqual(len(commands), 1)
        self.assertEqual(len(checkpoints), 1)
        self.assertEqual(
            checkpoints[0],
            {
                "status": "AMBIGUOUS",
                "effect_count": 1,
                "action_hash": self.action_hash,
                "reason_code": "POST_DISPATCH_RECONCILIATION_INCOMPLETE",
            },
        )
        self.assertEqual(result["status"], "AMBIGUOUS")
        self.assertEqual(result["effect_count"], 1)

    def test_main_persists_post_dispatch_checkpoint_to_distinct_path(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            request_path = root / "request.json"
            result_path = root / "result.json"
            registration_path = root / "registration.json"
            request_path.write_text(json.dumps(self.request()))
            registration_path.write_text(json.dumps(self.registration()))
            seen = {}
            writes = []
            fallback = {
                "status": "AMBIGUOUS",
                "effect_count": 1,
                "action_hash": self.action_hash,
                "reason_code": "POST_DISPATCH_RECONCILIATION_INCOMPLETE",
            }

            def fake_execute(*_args, **kwargs):
                seen["hook"] = kwargs.get("post_dispatch_checkpoint_fn")
                if seen["hook"] is not None:
                    seen["hook"](fallback, kwargs["budget"])
                return fallback

            def fake_write(path, result, _budget):
                writes.append((Path(path), dict(result)))

            with mock.patch.object(self.m, "REGISTRATION", registration_path), \
                    mock.patch.object(self.m, "execute_once", side_effect=fake_execute), \
                    mock.patch.object(self.m, "write_result", side_effect=fake_write):
                rc = self.m.main(["guarded-dispatch", str(request_path), str(result_path)])
            self.assertEqual(rc, 0)
            self.assertIsNotNone(seen.get("hook"))
            self.assertEqual(
                [path.name for path, _result in writes],
                [".guarded-dispatch-post-dispatch.json", "result.json"],
            )
            self.assertEqual(writes[0][1], fallback)
            self.assertEqual(writes[1][1], fallback)

    def test_reconciliation_allows_exact_baseline_cost_plus_write_reserve(self):
        clock, budget = self.budget(12.0)
        reads = 0
        commands = []

        def reader(_reg, _budget):
            nonlocal reads
            reads += 1
            if reads == 1:
                clock.advance(5.0)
                return self.candidate(100, 200)
            clock.advance(1.0)
            return self.candidate(101, 200)

        result = self.m.execute_once(
            self.request(),
            self.registration(),
            budget=budget,
            read_candidate_fn=reader,
            tool_ready_fn=lambda _target, _budget: True,
            dispatch_fn=lambda command, _budget: commands.append(tuple(command)) or 0,
            post_dispatch_checkpoint_fn=lambda _checkpoint, _budget: None,
        )
        self.assertEqual(reads, 2)
        self.assertEqual(len(commands), 1)
        self.assertEqual(result["status"], "CONFIRMED")
        self.assertEqual(result["effect_count"], 1)
        self.assertGreaterEqual(budget.remaining(), self.m.RESULT_WRITE_RESERVE_SECONDS)

if __name__ == "__main__":
    unittest.main()
