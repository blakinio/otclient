from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / ".github/workflows/track-a-native-login-be4f48-proven.yml"
WORKER = ROOT / ".github/scripts/track_a_native_login_be4f48_proven.py"
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
            '"secret_ingress": "bounded_docker_exec"',
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, text)
        self.assertNotIn("_runner_sidecar_metadata(vault_dir)", text)
        self.assertNotIn("_sidecar_auth_command", text)
        self.assertNotIn("native_login_fd_sidecar.py", text)

    def test_corrected_physical_workflow_has_no_sidecar_critical_path(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        for forbidden in (
            "sidecar-probe",
            "SIDECAR_FD_TRANSPORT_PROBE",
            "NO_SECRET_ACCESS_BEFORE_SIDECAR_PROBE",
            "sidecar_transport_metadata_ready",
            "native_login_fd_sidecar.py",
            "nsenter",
        ):
            self.assertNotIn(forbidden, text)
        for required in (
            "/track-a-native-login-be4f48-proven PRECHECK",
            "/track-a-native-login-be4f48-proven EXECUTE",
            "native_login_secret_ingress.py",
            "NO_SECRET_ACCESS_BEFORE_AUTH=true",
            "auth-one-shot",
            "CONFIRM_UNIQUE=PASS",
            "STRUCTURAL_IN_GAME=PASS",
            "runs-on: [otclient, synology]",
            "github.event.comment.user.login == github.repository_owner",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        self.assertNotIn("${{ secrets.", text)

    def test_wrapper_installs_helpers_as_target_user_without_chown_or_docker_cp(self) -> None:
        text = WORKER.read_text(encoding="utf-8")
        for required in (
            "def _install_bundle_user_owned(",
            "def _write_bundle_file_as_target(",
            "_base._numeric_user()",
            '"-u", _base.TARGET_USER',
            '"-u", "0", _base.TARGET_CONTAINER',
            '"id", "-u"',
            '"rm", "-rf", _base.TASK_ROOT',
            '"install", "-d", "-m", "700", _base.TASK_ROOT',
            "helper_install_root_exec_unavailable",
            "helper_install_reset_failed",
            "helper_install_prepare_failed",
            "helper_install_stream_failed",
            "helper_install_identity_invalid",
            "helper_install_digest_read_failed",
            "installed_helper_digest_mismatch",
            "_base._install_bundle = _install_bundle_user_owned",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        for forbidden in (
            "def replace(",
            "def confirm_unique(",
            "_base.replace =",
            "_base.confirm_unique =",
            '"docker", "cp"',
            '"chown"',
            "TASK_ROOT}/*",
        ):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
