from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / ".github/workflows/track-a-native-login-be4f48-physical.yml"
WORKER = ROOT / ".github/scripts/track_a_native_login_be4f48_physical.py"
INGRESS = ROOT / "tools/tibia_runtime_bridge/native_login_secret_ingress.py"

EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = "52105824"
EXPECTED_SHA = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"


class ProvenSecretIngressContractTests(unittest.TestCase):
    def test_current_ingress_module_exists_and_is_exact_fenced(self) -> None:
        self.assertTrue(INGRESS.is_file(), "current Kasm-local secret ingress is missing")
        text = INGRESS.read_text(encoding="utf-8")
        for needle in (
            EXPECTED_VERSION,
            EXPECTED_SIZE,
            EXPECTED_SHA,
            "os.environ.pop",
            "TIBIA_TEST_EMAIL",
            "TIBIA_TEST_PASSWORD",
            "os.memfd_create",
            "F_ADD_SEALS",
            "F_SEAL_SEAL",
            "auth_with_credentials_fd",
            "AUTH_RESPONSE_UNAVAILABLE_AFTER_SEND",
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, text)
        for forbidden in (
            "print(email",
            "print(password",
            "args.email",
            "args.password",
            "--email",
            "--password",
        ):
            self.assertNotIn(forbidden, text)

    def test_worker_uses_local_vault_then_bounded_docker_exec_ingress(self) -> None:
        text = WORKER.read_text(encoding="utf-8")
        for needle in (
            "native_login_secret_ingress.py",
            "_run_proven_secret_ingress",
            "_decrypt_frame",
            "TIBIA_TEST_EMAIL",
            "TIBIA_TEST_PASSWORD",
            '"docker", "exec"',
            '"-e", "TIBIA_TEST_EMAIL"',
            '"-e", "TIBIA_TEST_PASSWORD"',
            "PASS_WITH_PROCESS_HANDOFF",
            "secret_attempt_count",
            "NO_SECOND_SECRET_ATTEMPT",
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, text)
        self.assertNotIn("_runner_sidecar_metadata(vault_dir)", text)
        self.assertNotIn("_sidecar_auth_command", text)

    def test_physical_workflow_removes_sidecar_probe_from_critical_path(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertNotIn("sidecar-probe", text)
        self.assertNotIn("SIDECAR_FD_TRANSPORT_PROBE", text)
        self.assertNotIn("NO_SECRET_ACCESS_BEFORE_SIDECAR_PROBE", text)
        self.assertNotIn("sidecar_transport_metadata_ready", text)
        self.assertIn("native_login_secret_ingress.py", text)
        self.assertIn("NO_SECRET_ACCESS_BEFORE_AUTH=true", text)
        self.assertIn("auth-one-shot", text)
        self.assertIn("CONFIRM_UNIQUE=PASS", text)
        self.assertIn("STRUCTURAL_IN_GAME=PASS", text)


if __name__ == "__main__":
    unittest.main()
