#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
WORKER_PATH = HERE / "tibia-official-client-re-player-state-causal-worker.py"
TRANSITION_PATH = HERE / "tibia-official-client-re-canonical-live-transition.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CausalWorkerOuterTimeoutContractTests(unittest.TestCase):
    def setUp(self):
        self.worker = load(WORKER_PATH, "causal_worker_timeout_contract_worker")
        self.transition = load(TRANSITION_PATH, "causal_worker_timeout_contract_transition")

    def test_worker_budget_is_strictly_inside_guarded_dispatch_default_timeout(self):
        parsed = self.transition.parser().parse_args(
            [
                "guarded-dispatch",
                "--task-id", "OTC-TEST",
                "--session-id", "session",
                "--token-file", "/tmp/token",
                "--probe", "/tmp/probe",
                "--worker", "/tmp/worker",
                "--request-file", "/tmp/request",
            ]
        )
        self.assertEqual(parsed.worker_timeout, 30)
        self.assertEqual(
            self.worker.OUTER_GUARDED_DISPATCH_TIMEOUT_SECONDS,
            float(parsed.worker_timeout),
        )
        self.assertLess(
            self.worker.WORKER_TOTAL_BUDGET_SECONDS,
            float(parsed.worker_timeout),
        )
        self.assertEqual(
            float(parsed.worker_timeout) - self.worker.WORKER_TOTAL_BUDGET_SECONDS,
            self.worker.SUPERVISOR_RETURN_MARGIN_SECONDS,
        )

    def test_dispatch_subprocess_timeout_is_bounded_by_remaining_budget(self):
        now = [50.0]
        budget = self.worker.DeadlineBudget(55.0, clock=lambda: now[0])
        target = self.worker.Target(
            pid=646,
            start_ticks=1,
            container=self.worker.CONTAINER,
            display=self.worker.DISPLAY,
            window_id="0x400011",
        )
        command = self.worker.dispatch_command(target, "east")
        seen = []

        def timed_out(*_args, **kwargs):
            seen.append(kwargs["timeout"])
            raise subprocess.TimeoutExpired(command, kwargs["timeout"])

        with mock.patch.object(self.worker.subprocess, "run", side_effect=timed_out):
            rc = self.worker.dispatch(command, budget)
        self.assertEqual(rc, 255)
        self.assertEqual(len(seen), 1)
        self.assertAlmostEqual(seen[0], 3.0)

    def test_parent_never_accepts_valid_looking_result_after_worker_process_death(self):
        with tempfile.TemporaryDirectory() as td:
            state = Path(td)
            args = argparse.Namespace(
                worker=Path("/tmp/fake-worker"),
                request_file=Path("/tmp/request.json"),
                worker_timeout=30,
            )

            def died(*_args, **_kwargs):
                (state / ".guarded-dispatch-result.json").write_text(
                    '{"status":"CONFIRMED","effect_count":1,"action_hash":"' + "a" * 64 + '"}\n'
                )
                return mock.Mock(returncode=-9)

            with mock.patch.object(self.transition, "STATE", state), \
                    mock.patch.object(self.transition.subprocess, "run", side_effect=died):
                with self.assertRaisesRegex(
                    self.transition.E,
                    "guarded_dispatch_worker_failed",
                ):
                    self.transition._run_guarded_worker(
                        args,
                        {"action_hash": "a" * 64},
                    )
            self.assertFalse((state / ".guarded-dispatch-result.json").exists())


if __name__ == "__main__":
    unittest.main()
