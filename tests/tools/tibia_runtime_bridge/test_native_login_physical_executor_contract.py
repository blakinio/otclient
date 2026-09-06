from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / ".github/workflows/track-a-native-login-be4f48-physical.yml"
WORKER = ROOT / ".github/scripts/track_a_native_login_be4f48_physical.py"
CONTAINER_CLIENT = ROOT / "tools/tibia_runtime_bridge/container_native_login_client.py"
TASK = ROOT / "docs/agents/tasks/active/OTC-20260906-native-login-physical-executor.md"
EXPECTED_SHA = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"


class PhysicalExecutorContractTests(unittest.TestCase):
    def test_trusted_main_owner_gate_and_pr_boundary(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        required = (
            "issue_comment:",
            "pull_request:",
            "/track-a-native-login-be4f48 PRECHECK",
            "/track-a-native-login-be4f48 EXECUTE",
            "github.event.comment.user.login == github.repository_owner",
            "github.event.issue.pull_request",
            "runs-on: ubuntu-24.04",
            "runs-on: [otclient, synology]",
            "ref: main",
            "git ls-remote origin refs/heads/main",
            "persist-credentials: false",
            "needs: prepare",
        )
        for needle in required:
            with self.subTest(needle=needle):
                self.assertIn(needle, text)
        self.assertNotIn("runs-on: [otclient, synology]\n    if: github.event_name == 'pull_request'", text)

    def test_execution_is_current_fenced_canonical_and_one_shot(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        required = (
            EXPECTED_SHA,
            "OTC-20260906-native-login-physical-executor",
            "canonical-live-lease",
            " acquire ",
            " rebind ",
            " gate-b ",
            " guard-run ",
            " stale-registration-recovery ",
            "tibia-official-client-re-kasm-existing-runtime-probe.py",
            "ONE_SHOT_NATIVE_LOGIN",
            "NO_SECOND_SECRET_ATTEMPT",
            "VAULT_DIR: /work/_otclient_tibia_re_state/secret-vault",
            "gameWindowState",
            "CONFIRM_UNIQUE",
        )
        for needle in required:
            with self.subTest(needle=needle):
                self.assertIn(needle, text)
        for forbidden in (
            "${{ secrets.",
            "secrets.TIBIA_TEST_EMAIL",
            "secrets.TIBIA_TEST_PASSWORD",
            "pkill ",
            "killall ",
            "kill -9",
            "gdb ",
            "ptrace",
            "xdotool",
            "pyautogui",
        ):
            self.assertNotIn(forbidden.lower(), text.lower())

    def test_worker_uses_exact_pid_host_vault_and_namespace_fd_bridge(self) -> None:
        text = WORKER.read_text(encoding="utf-8")
        required = (
            "TARGET_CONTAINER = \"otclient-track-a-kasmvnc\"",
            "TARGET_DISPLAY = \":1\"",
            EXPECTED_SHA,
            "existing_runtime_adoption_v1",
            "docker", "exec", "-d", "-u", "kasm-user",
            "SIGTERM",
            "vault_bind",
            "same_numeric_uid",
            "decrypt_to_sealed_memfd",
            "nsenter",
            "pass_fds",
            "OTCLIENT_TIBIA_RE_AUTH_SOCKET",
            "OTCLIENT_TIBIA_RE_CHARACTER_SOCKET",
            "LD_PRELOAD",
        )
        for needle in required:
            with self.subTest(needle=needle):
                self.assertIn(needle, text)
        for forbidden in ("pkill", "killall", "SIGKILL", "TIBIA_TEST_EMAIL", "TIBIA_TEST_PASSWORD"):
            self.assertNotIn(forbidden, text)

    def test_container_client_receives_only_inherited_sealed_fd(self) -> None:
        text = CONTAINER_CLIENT.read_text(encoding="utf-8")
        required = (
            "auth-fd",
            "_validate_credentials_memfd",
            "F_GET_SEALS",
            "SCM_RIGHTS",
            "sendmsg",
            "PeerIdentityExpectation",
            "os.setgid",
            "os.setuid",
            "CONFIRM_UNIQUE",
            "request(",
        )
        for needle in required:
            with self.subTest(needle=needle):
                self.assertIn(needle, text)
        for forbidden in (
            "decrypt_to_sealed_memfd",
            "secret_vault",
            "--vault-dir",
            "TIBIA_TEST_EMAIL",
            "TIBIA_TEST_PASSWORD",
            "password=",
            "email=",
        ):
            self.assertNotIn(forbidden, text)

    def test_runtime_task_is_pregate_fail_closed(self) -> None:
        text = TASK.read_text(encoding="utf-8")
        required = (
            "runtime_access: canonical_reuse_or_mutation",
            "runtime_owner_task: OTC-20260906-native-login-physical-executor",
            "runtime_namespace: canonical-live-runtime",
            "physical_runtime_locator: synology:otclient-track-a-kasmvnc:display-1",
            "canonical_registration: PRESENT",
            "canonical_lease_generation: UNKNOWN",
            "registration_lease_generation: UNKNOWN",
            "gate_a: REQUIRED_NOT_PROVEN",
            "generation_rebind: REQUIRED_NOT_PROVEN",
            "gate_b: REQUIRED_NOT_PROVEN",
            "target_uniqueness: UNKNOWN",
            "mutation_authorized: false",
            "physical_e2e_required: true",
        )
        for needle in required:
            with self.subTest(needle=needle):
                self.assertIn(needle, text)


if __name__ == "__main__":
    unittest.main()
