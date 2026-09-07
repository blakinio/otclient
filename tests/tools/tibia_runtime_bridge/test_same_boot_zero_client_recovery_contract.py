from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
INVALIDATOR = ROOT / ".github/scripts/tibia-official-client-re-same-boot-zero-client-invalidate.py"
WORKFLOW = ROOT / ".github/workflows/track-a-same-boot-zero-client-recovery.yml"
CONTRACT = ROOT / "docs/agents/contracts/TRACK_A_SAME_BOOT_ZERO_CLIENT_INVALIDATION_V1.md"
GOVERNANCE = ROOT / ".github/scripts/test_track_a_agent_runtime_governance.py"
GOVERNANCE_BASE = ROOT / ".github/scripts/track_a_agent_runtime_governance_base.py"
RECOVERY_TASK = ROOT / "docs/agents/tasks/active/OTC-20260907-same-boot-zero-client-invalidation-live.md"
BOOTSTRAP_TASK = ROOT / "docs/agents/tasks/active/OTC-20260907-same-boot-zero-client-bootstrap-live.md"

EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = "52105824"
EXPECTED_SHA = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"


class SameBootZeroClientRecoveryContractTests(unittest.TestCase):
    def test_reviewed_contract_is_narrow_and_credential_free(self) -> None:
        self.assertTrue(CONTRACT.is_file(), "same-boot zero-client invalidation contract missing")
        text = CONTRACT.read_text(encoding="utf-8")
        for required in (
            "same_boot_zero_client_invalidation_v1",
            "metadata-only",
            "candidate_count == 0",
            "main_window_count == 0",
            "registration boot identity MUST equal current boot identity",
            "newer canonical lease generation",
            "create-new canonical bootstrap",
            "credentials_allowed: false",
            "login_allowed: false",
            "process_control_authorized: false",
            "not a manual edit",
            "MUST NOT be renamed back",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        self.assertNotIn("credential plaintext is allowed", text.lower())
        self.assertNotIn("bypass gate a is allowed", text.lower())

    def test_invalidator_is_exact_fenced_atomic_and_same_boot_only(self) -> None:
        self.assertTrue(INVALIDATOR.is_file(), "same-boot invalidator missing")
        text = INVALIDATOR.read_text(encoding="utf-8")
        for required in (
            EXPECTED_VERSION,
            EXPECTED_SIZE,
            EXPECTED_SHA,
            "same_boot_zero_client_invalidation_v1",
            "coordination.lock",
            "TRACK_A_SAME_BOOT_INVALIDATION_GUARDED",
            "LOCK_EX",
            "LOCK_NB",
            "canonical_guard_required",
            "worker_not_approved",
            "worker_current_fence_mismatch",
            "lease_generation",
            "boot_id_sha256",
            "candidate_count",
            "main_window_count",
            "registration_boot_not_current",
            "registration_lease_not_stale",
            "registered_process_still_present",
            "zero_client_postcommit_preflight_drift",
            "lease_postcommit_drift",
            "invalidation_tombstone_mismatch",
            "os.replace",
            "runtime-registration.json",
            "credential_accessed",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        for forbidden in (
            "TIBIA_TEST_EMAIL",
            "TIBIA_TEST_PASSWORD",
            "kill(",
            "SIGTERM",
            "docker exec -d",
            "subprocess.Popen",
        ):
            self.assertNotIn(forbidden, text)

    def test_owner_workflow_invalidates_then_reuses_canonical_create_new(self) -> None:
        self.assertTrue(WORKFLOW.is_file(), "same-boot recovery workflow missing")
        text = WORKFLOW.read_text(encoding="utf-8")
        for required in (
            "issue_comment:",
            "github.event.issue.pull_request",
            "github.event.comment.user.login == github.repository_owner",
            "github.event.comment.body == '/track-a-same-boot-zero-client-recovery EXECUTE'",
            "runs-on: [otclient, synology]",
            "tibia-official-client-re-same-boot-zero-client-invalidate.py",
            "tibia-official-client-re-canonical-live-lease",
            "tibia-official-client-re-canonical-live-transition.py",
            "TRACK_A_SAME_BOOT_INVALIDATION_GUARDED=1",
            "guard-run",
            "kasm-bootstrap",
            "NO_CREDENTIAL_ACCESS=true",
            "test ! -e \"$CANONICAL_STATE/runtime-registration.json\"",
            "GITHUB_RUN_ATTEMPT",
            "BOOTSTRAP_ONE_SHOT_AUTHORIZATION_CONSUMED=PASS",
            "source_task']=='OTC-20260907-same-boot-zero-client-bootstrap-live'",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        for forbidden in (
            "${{ secrets.",
            "TIBIA_TEST_EMAIL",
            "TIBIA_TEST_PASSWORD",
            "auth-one-shot",
            "workflow_dispatch:",
        ):
            self.assertNotIn(forbidden, text)

    def test_governance_extension_preserves_base_and_admits_only_named_mode(self) -> None:
        self.assertTrue(GOVERNANCE.is_file())
        self.assertTrue(GOVERNANCE_BASE.is_file())
        wrapper = GOVERNANCE.read_text(encoding="utf-8")
        base = GOVERNANCE_BASE.read_text(encoding="utf-8")
        for required in (
            "track_a_agent_runtime_governance_base.py",
            "same_boot_zero_client_invalidation_v1",
            "TRACK_A_SAME_BOOT_ZERO_CLIENT_INVALIDATION_V1",
            "_ORIGINAL_VALIDATE",
            "same_boot_zero_client_invalidation_mode_self_test",
            "same-boot zero-client recovery requires a newer current controller generation",
        ):
            self.assertIn(required, wrapper)
        self.assertIn("prior_boot_zero_client_invalidation_mode_self_test", base)
        self.assertNotIn("same_boot_zero_client_invalidation_v1", base)

    def test_live_admission_records_are_separate_and_secret_free(self) -> None:
        for task in (RECOVERY_TASK, BOOTSTRAP_TASK):
            self.assertTrue(task.is_file())
            text = task.read_text(encoding="utf-8")
            self.assertIn("live_runtime_authorization_source: OWNER_CHAT_20260907_CONTINUE_FROM_AUTHORIZED_NATIVE_LOGIN_TASK", text)
            self.assertIn("credentials_allowed: false", text)
            self.assertIn("login_allowed: false", text)
            self.assertNotIn("TIBIA_TEST_EMAIL", text)
            self.assertNotIn("TIBIA_TEST_PASSWORD", text)
        recovery = RECOVERY_TASK.read_text(encoding="utf-8")
        bootstrap = BOOTSTRAP_TASK.read_text(encoding="utf-8")
        self.assertIn("runtime_access: canonical_recovery", recovery)
        self.assertIn("recovery_mode: same_boot_zero_client_invalidation_v1", recovery)
        self.assertIn("registration_lease_generation: 55", recovery)
        self.assertIn("process_control_authorized: false", recovery)
        self.assertIn("runtime_access: canonical_bootstrap", bootstrap)
        self.assertIn("canonical_registration: ABSENT", bootstrap)
        self.assertIn("bootstrap_mode: create_new", bootstrap)
        self.assertIn("physical_action_budget: 1", bootstrap)
        self.assertIn("auth", bootstrap.lower())  # explicit non-authority text is retained


if __name__ == "__main__":
    unittest.main()
