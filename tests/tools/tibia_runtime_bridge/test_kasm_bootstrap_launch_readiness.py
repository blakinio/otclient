from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
WORKER = ROOT / ".github/scripts/tibia-official-client-re-kasm-bootstrap-worker-compatible.py"
PROBE = ROOT / ".github/scripts/tibia-official-client-re-kasm-existing-runtime-probe-compatible.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class Tests(unittest.TestCase):
    def test_plain_launch_matches_physically_proven_bin_environment(self) -> None:
        worker = load(WORKER, "kasm_launch_readiness_worker")
        command = worker._launch_command("a" * 64)
        flat = " ".join(command)
        client_dir = "/home/kasm-user/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin"
        self.assertEqual(client_dir, worker.CLIENT_DIR)
        self.assertIn("HOME=/home/kasm-user", command)
        self.assertIn("DISPLAY=:1", command)
        self.assertIn("XAUTHORITY=/home/kasm-user/.Xauthority", command)
        self.assertIn(f"LD_LIBRARY_PATH={client_dir}:{client_dir}/lib", command)
        self.assertIn("-w", command)
        self.assertEqual(client_dir, command[command.index("-w") + 1])
        self.assertIn("sh", command)
        self.assertIn("-lc", command)
        self.assertIn(f"cd '{client_dir}' && exec ./client", flat)
        self.assertNotIn(
            "LD_LIBRARY_PATH=/home/kasm-user/.local/share/CipSoft GmbH/Tibia/packages/Tibia:/home/kasm-user/.local/share/CipSoft GmbH/Tibia/packages/Tibia/lib",
            command,
        )
        for name in (
            "TIBIA_TEST_EMAIL", "TIBIA_TEST_PASSWORD", "TRACK_A_CANONICAL_LEASE_TOKEN",
            "TRACK_A_CANONICAL_LEASE_TOKEN_FILE", "LD_PRELOAD", "OTCLIENT_TIBIA_RE_SOCKET",
            "OTCLIENT_TIBIA_RE_AUTH_SOCKET", "OTCLIENT_TIBIA_RE_CHARACTER_SOCKET",
        ):
            self.assertIn(name, command)

    def test_launch_persists_identity_before_window_readiness_wait(self) -> None:
        text = WORKER.read_text(encoding="utf-8")
        write = text.index("_base.write_record(path, launch)")
        window = text.index("windows = _base._window_count", write)
        self.assertLess(write, window)
        self.assertIn("postlaunch_window_not_ready", text)
        self.assertIn("postlaunch_identity_drift", text)

    def _preflight_record(self, worker):
        payload = {
            "schema": worker._base.PREFLIGHT_SCHEMA,
            "container_name": worker._base.TARGET_CONTAINER,
            "container_id": "a" * 64,
            "display": worker._base.TARGET_DISPLAY,
            "package_dir": worker._base.PACKAGE_DIR,
            "client_path": worker._base.CLIENT_PATH,
            "client_size": worker._base.SIZE,
            "client_sha256": worker._base.SHA,
            "boot_id_sha256": "b" * 64,
            "candidate_count": 0,
            "main_window_count": 0,
        }
        payload["preflight_fingerprint"] = worker._base._fingerprint(payload)
        return payload

    def test_rollback_accepts_preidentity_early_exit_only_after_fresh_zero_state(self) -> None:
        worker = load(WORKER, "kasm_launch_early_exit_rollback_worker")
        saved = self._preflight_record(worker)
        original_collect = worker._base.collect_preflight
        with tempfile.TemporaryDirectory() as tmp:
            record = Path(tmp) / "record.json"
            worker._base.write_record(record, saved)
            worker._base.collect_preflight = lambda _runner: dict(saved)
            try:
                worker.rollback_launch(record, runner=lambda _command: "", sleeper=lambda _seconds: None)
            finally:
                worker._base.collect_preflight = original_collect

    def test_rollback_rejects_preidentity_early_exit_when_zero_state_drifted(self) -> None:
        worker = load(WORKER, "kasm_launch_early_exit_drift_worker")
        saved = self._preflight_record(worker)
        drifted = dict(saved)
        drifted["main_window_count"] = 1
        original_collect = worker._base.collect_preflight
        with tempfile.TemporaryDirectory() as tmp:
            record = Path(tmp) / "record.json"
            worker._base.write_record(record, saved)
            worker._base.collect_preflight = lambda _runner: dict(drifted)
            try:
                with self.assertRaisesRegex(worker.WorkerError, "rollback_prelaunch_zero_state_unproven"):
                    worker.rollback_launch(record, runner=lambda _command: "", sleeper=lambda _seconds: None)
            finally:
                worker._base.collect_preflight = original_collect

    def test_probe_retries_only_bounded_readiness_errors(self) -> None:
        probe = load(PROBE, "kasm_launch_readiness_probe")
        calls = 0

        def fake_collect(_runner):
            nonlocal calls
            calls += 1
            if calls < 3:
                raise probe.ProbeError("main_window_count:0")
            return {"ok": True}

        original = probe.collect
        probe.collect = fake_collect
        try:
            result = probe.collect_when_ready(lambda _command: "", sleeper=lambda _seconds: None, attempts=4)
        finally:
            probe.collect = original
        self.assertEqual({"ok": True}, result)
        self.assertEqual(3, calls)

    def test_probe_does_not_retry_hard_identity_failure(self) -> None:
        probe = load(PROBE, "kasm_launch_hard_failure_probe")
        calls = 0

        def fake_collect(_runner):
            nonlocal calls
            calls += 1
            raise probe.ProbeError("conflicting_official_client_candidate")

        original = probe.collect
        probe.collect = fake_collect
        try:
            with self.assertRaisesRegex(probe.ProbeError, "conflicting_official_client_candidate"):
                probe.collect_when_ready(lambda _command: "", sleeper=lambda _seconds: None, attempts=4)
        finally:
            probe.collect = original
        self.assertEqual(1, calls)

    def test_probe_error_output_is_allowlisted_value_free_shape(self) -> None:
        probe = load(PROBE, "kasm_launch_error_probe")
        self.assertEqual("main_window_count:0", probe._safe_error(probe.ProbeError("main_window_count:0")))
        self.assertEqual("ProbeError", probe._safe_error(probe.ProbeError("unsafe path /tmp/x y")))


if __name__ == "__main__":
    unittest.main()
