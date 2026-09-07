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
    def test_launch_uses_official_linux_entrypoint_directory(self) -> None:
        worker = load(WORKER, "kasm_launch_readiness_worker")
        launcher_dir = "/home/kasm-user/Tibia"
        command = worker._launch_command("a" * 64, launcher_dir)
        flat = " ".join(command)
        self.assertEqual(worker.LAUNCH_METHOD, "docker_exec_detached_official_linux_entrypoint")
        self.assertIn("HOME=/home/kasm-user", command)
        self.assertIn("DISPLAY=:1", command)
        self.assertIn("XAUTHORITY=/home/kasm-user/.Xauthority", command)
        self.assertIn("-w", command)
        self.assertEqual(launcher_dir, command[command.index("-w") + 1])
        self.assertIn("sh", command)
        self.assertIn("-lc", command)
        self.assertIn(f"cd {launcher_dir} && exec ./Tibia", flat)
        self.assertNotIn("exec ./client", flat)
        self.assertNotIn(
            "/home/kasm-user/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin:/home/kasm-user/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/lib",
            command,
        )
        ld_index = command.index("LD_LIBRARY_PATH")
        self.assertEqual("-u", command[ld_index - 1])
        for name in (
            "TIBIA_TEST_EMAIL", "TIBIA_TEST_PASSWORD", "TRACK_A_CANONICAL_LEASE_TOKEN",
            "TRACK_A_CANONICAL_LEASE_TOKEN_FILE", "LD_PRELOAD", "OTCLIENT_TIBIA_RE_SOCKET",
            "OTCLIENT_TIBIA_RE_AUTH_SOCKET", "OTCLIENT_TIBIA_RE_CHARACTER_SOCKET",
        ):
            self.assertIn(name, command)

    def test_launcher_aware_candidate_scan_skips_only_prechecked_launcher_path(self) -> None:
        worker = load(WORKER, "kasm_launcher_aware_candidate_worker")
        self.assertIn("if exe==sys.argv[2]: continue", worker.LAUNCHER_AWARE_CANDIDATE_SCRIPT)
        self.assertEqual(1, worker._base.CANDIDATE_SCRIPT.count("    hint=("))
        self.assertNotIn("if exe==sys.argv[2]: continue", worker._base.CANDIDATE_SCRIPT)

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
            "launcher_path": "/home/kasm-user/Tibia/Tibia",
            "launcher_dir": "/home/kasm-user/Tibia",
            "launcher_size": 123456,
            "launcher_sha256": "c" * 64,
            "launcher_selection": "unique",
        }
        payload["preflight_fingerprint"] = worker._base._fingerprint(payload)
        return payload

    def test_collect_preflight_binds_launcher_identity_into_fingerprint(self) -> None:
        worker = load(WORKER, "kasm_launcher_preflight_worker")
        base_payload = {
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
        base_payload["preflight_fingerprint"] = worker._base._fingerprint(base_payload)
        launcher = {
            "launcher_path": "/home/kasm-user/Tibia/Tibia",
            "launcher_dir": "/home/kasm-user/Tibia",
            "launcher_size": 123456,
            "launcher_sha256": "c" * 64,
            "launcher_selection": "desktop",
        }
        original_collect = worker._original_collect_preflight
        original_identity = worker.launcher_identity
        worker._original_collect_preflight = lambda _runner: dict(base_payload)
        worker.launcher_identity = lambda _container, _runner: dict(launcher)
        try:
            result = worker.collect_preflight(lambda _command: "")
        finally:
            worker._original_collect_preflight = original_collect
            worker.launcher_identity = original_identity
        self.assertEqual(launcher["launcher_path"], result["launcher_path"])
        unsigned = dict(result)
        fingerprint = unsigned.pop("preflight_fingerprint")
        self.assertEqual(fingerprint, worker._base._fingerprint(unsigned))
        self.assertNotEqual(fingerprint, base_payload["preflight_fingerprint"])

    def test_launch_persists_identity_before_launcher_and_window_readiness_waits(self) -> None:
        text = WORKER.read_text(encoding="utf-8")
        write = text.index("_base.write_record(path, launch)")
        launcher_wait = text.index("_wait_launcher_exit", write)
        window = text.index("windows = _base._window_count", write)
        self.assertLess(write, launcher_wait)
        self.assertLess(launcher_wait, window)
        self.assertIn("launcher_residue", text)
        self.assertIn("postlaunch_window_not_ready", text)
        self.assertIn("postlaunch_identity_drift", text)

    def test_preidentity_rollback_cleans_launcher_then_late_client_then_reproves_zero_state(self) -> None:
        worker = load(WORKER, "kasm_entrypoint_preidentity_rollback_worker")
        saved = self._preflight_record(worker)
        calls: list[str] = []
        original_launcher_cleanup = worker._kill_launcher_residue
        original_client_cleanup = worker._kill_late_exact_client
        original_wait_clean = worker._wait_clean_preflight
        with tempfile.TemporaryDirectory() as tmp:
            record = Path(tmp) / "record.json"
            worker._base.write_record(record, saved)
            worker._kill_launcher_residue = lambda *_args, **_kwargs: calls.append("launcher")
            worker._kill_late_exact_client = lambda *_args, **_kwargs: calls.append("client")
            worker._wait_clean_preflight = lambda fp, *_args, **_kwargs: calls.append(f"clean:{fp}")
            try:
                worker.rollback_launch(record, runner=lambda _command: "", sleeper=lambda _seconds: None)
            finally:
                worker._kill_launcher_residue = original_launcher_cleanup
                worker._kill_late_exact_client = original_client_cleanup
                worker._wait_clean_preflight = original_wait_clean
        self.assertEqual(["launcher", "client", f"clean:{saved['preflight_fingerprint']}"], calls)

    def test_launch_record_rollback_keeps_existing_exact_client_cleanup_and_adds_launcher_cleanup(self) -> None:
        worker = load(WORKER, "kasm_entrypoint_launch_rollback_worker")
        saved = self._preflight_record(worker)
        launch = {
            "schema": worker._base.LAUNCH_SCHEMA,
            "preflight_fingerprint": saved["preflight_fingerprint"],
            "container_name": worker._base.TARGET_CONTAINER,
            "container_id": saved["container_id"],
            "display": worker._base.TARGET_DISPLAY,
            "package_dir": worker._base.PACKAGE_DIR,
            "client_path": worker._base.CLIENT_PATH,
            "client_size": worker._base.SIZE,
            "client_sha256": worker._base.SHA,
            "pid": 321,
            "process_start_ticks": 654,
            "launch_method": worker.LAUNCH_METHOD,
            "bootstrap_helper_residue": False,
            "client_dir": worker.CLIENT_DIR,
            "launcher_path": saved["launcher_path"],
            "launcher_dir": saved["launcher_dir"],
            "launcher_size": saved["launcher_size"],
            "launcher_sha256": saved["launcher_sha256"],
            "launcher_selection": saved["launcher_selection"],
        }
        calls: list[str] = []
        original_base_rollback = worker._original_rollback_launch
        original_launcher_cleanup = worker._kill_launcher_residue
        original_wait_clean = worker._wait_clean_preflight
        with tempfile.TemporaryDirectory() as tmp:
            record = Path(tmp) / "record.json"
            worker._base.write_record(record, launch)
            worker._original_rollback_launch = lambda *_args, **_kwargs: calls.append("client")
            worker._kill_launcher_residue = lambda *_args, **_kwargs: calls.append("launcher")
            worker._wait_clean_preflight = lambda fp, *_args, **_kwargs: calls.append(f"clean:{fp}")
            try:
                worker.rollback_launch(record, runner=lambda _command: "", sleeper=lambda _seconds: None)
            finally:
                worker._original_rollback_launch = original_base_rollback
                worker._kill_launcher_residue = original_launcher_cleanup
                worker._wait_clean_preflight = original_wait_clean
        self.assertEqual(["client", "launcher", f"clean:{saved['preflight_fingerprint']}"], calls)

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
