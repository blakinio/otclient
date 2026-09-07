from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
INVALIDATOR = ROOT / ".github/scripts/tibia-official-client-re-same-boot-zero-client-invalidate.py"
WORKFLOW = ROOT / ".github/workflows/track-a-same-boot-zero-client-recovery.yml"
CONTRACT = ROOT / "docs/agents/contracts/TRACK_A_SAME_BOOT_ZERO_CLIENT_INVALIDATION_V1.md"

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
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        for forbidden in ("manual edit", "bypass Gate A", "credential plaintext"):
            self.assertNotIn(forbidden, text.lower())

    def test_invalidator_is_exact_fenced_atomic_and_same_boot_only(self) -> None:
        self.assertTrue(INVALIDATOR.is_file(), "same-boot invalidator missing")
        text = INVALIDATOR.read_text(encoding="utf-8")
        for required in (
            EXPECTED_VERSION,
            EXPECTED_SIZE,
            EXPECTED_SHA,
            "same_boot_zero_client_invalidation_v1",
            "coordination.lock",
            "LOCK_EX",
            "lease_generation",
            "boot_id_sha256",
            "candidate_count",
            "main_window_count",
            "registration_boot_not_current",
            "registration_lease_not_stale",
            "registered_process_still_present",
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
            "workflow_dispatch:",
            "github.actor == github.repository_owner",
            "github.ref == 'refs/heads/main'",
            "INVALIDATE_SAME_BOOT_ZERO_CLIENT_THEN_CREATE_NEW_KASM_CANONICAL_BOOTSTRAP",
            "runs-on: [otclient, synology]",
            "tibia-official-client-re-same-boot-zero-client-invalidate.py",
            "tibia-official-client-re-canonical-live-lease",
            "tibia-official-client-re-canonical-live-transition.py",
            "kasm-bootstrap",
            "NO_CREDENTIAL_ACCESS=true",
            "test ! -e \"$CANONICAL_STATE/runtime-registration.json\"",
            "GITHUB_RUN_ATTEMPT",
            "BOOTSTRAP_ONE_SHOT_AUTHORIZATION_CONSUMED=PASS",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        for forbidden in (
            "${{ secrets.",
            "TIBIA_TEST_EMAIL",
            "TIBIA_TEST_PASSWORD",
            "auth-one-shot",
        ):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
