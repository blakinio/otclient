from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
WORKER = ROOT / ".github/scripts/track_a_native_login_be4f48_physical.py"
SIDECAR = ROOT / "tools/tibia_runtime_bridge/native_login_fd_sidecar.py"


class ProcRootRelayContractTests(unittest.TestCase):
    def test_worker_maps_kasm_relay_through_pid1_root_without_daemon_shm_bind(self) -> None:
        text = WORKER.read_text(encoding="utf-8")
        for needle in (
            'PROC_ROOT_RELAY_ROOT = "/proc/1/root/dev/shm"',
            "_proc_root_relay_socket",
            '"--pid", f"container:{_base.TARGET_CONTAINER}"',
            '"--network", "none"',
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, text)
        for forbidden in (
            "target_shm_source",
            "dst=/relay-shm,readonly",
            '"--ipc"',
            '"--network", f"container:',
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, text)

    def test_sidecar_accepts_only_proc_root_dev_shm_native_login_namespace(self) -> None:
        text = SIDECAR.read_text(encoding="utf-8")
        for needle in (
            'RELAY_ROOT = Path("/proc/1/root/dev/shm")',
            "RELAY_PREFIX = \"otclient-native-login-relay-\"",
            "relay_socket_outside_target_proc_root",
            "relay_socket_namespace_invalid",
            "SCM_RIGHTS",
            "sendmsg",
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, text)
        for forbidden in (
            'RELAY_ROOT = Path("/relay-shm")',
            'RELAY_ROOT = Path("/dev/shm")',
            "TIBIA_TEST_EMAIL",
            "TIBIA_TEST_PASSWORD",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, text)

    def test_public_worker_preserves_base_auth_and_character_delegation(self) -> None:
        text = WORKER.read_text(encoding="utf-8")
        for needle in (
            "_base.replace(vault_dir, bundle, result)",
            "_base.auth_one_shot(vault_dir, result)",
            "_base.confirm_unique(result)",
            "_base.sidecar_probe = sidecar_probe",
        ):
            self.assertIn(needle, text)


if __name__ == "__main__":
    unittest.main()
