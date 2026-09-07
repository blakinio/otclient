from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / ".github/workflows/track-a-same-boot-zero-client-recovery-v2.yml"
RECOVERY = ROOT / "docs/agents/tasks/active/OTC-20260907-same-boot-zero-client-recovery-v2-live.md"
BOOTSTRAP = ROOT / "docs/agents/tasks/active/OTC-20260907-same-boot-zero-client-bootstrap-v2-live.md"
CENSUS = ROOT / "docs/agents/contracts/TRACK_A_DOCKER_OFFICIAL_CANDIDATE_CENSUS_V1.md"


class Tests(unittest.TestCase):
    def test_workflow_has_separate_owner_precheck_and_execute(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        for required in (
            "github.event.issue.number == 975",
            "github.event.comment.user.login == github.repository_owner",
            "/track-a-same-boot-zero-client-recovery-v2 PRECHECK",
            "/track-a-same-boot-zero-client-recovery-v2 EXECUTE",
            "runs-on: [otclient, synology]",
            "ref: main",
            "recovery-v2-precheck-attempt-consumed.json",
            "recovery-v2-precheck-pass.json",
            "recovery-v2-execute-attempt-consumed.json",
            "os.O_EXCL",
            "RECOVERY_V2_PRECHECK_PASS=VERIFIED",
            "tibia-official-client-re-kasm-bootstrap-worker-compatible.py",
            "tibia-official-client-re-kasm-existing-runtime-probe-compatible.py",
            "tibia-official-client-re-same-boot-zero-client-invalidate-compatible.py",
            "guard-run",
            "kasm-bootstrap",
            "NO_CREDENTIAL_ACCESS=true",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        for forbidden in (
            "${{ secrets.",
            "TIBIA_TEST_EMAIL",
            "TIBIA_TEST_PASSWORD",
            "auth-one-shot",
            "same-boot-zero-client-recovery-attempt-consumed.json",
            "bootstrap-attempt-consumed.json",
        ):
            self.assertNotIn(forbidden, text)

    def test_precheck_is_zero_action_and_execute_is_gated_by_same_main_pass(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        precheck = text.split("  live-precheck:", 1)[1].split("  live-execute:", 1)[0]
        execute = text.split("  live-execute:", 1)[1]
        self.assertIn('python3 "$worker" preflight "$record"', precheck)
        self.assertNotIn("kasm-bootstrap", precheck)
        self.assertNotIn("invalidate-compatible.py", precheck)
        self.assertIn("pre['candidate_count']==0", precheck)
        self.assertIn("pre['boot_id_sha256']==reg['boot_id_sha256']", precheck)
        self.assertIn("'trusted_main':sys.argv[2]", precheck)
        self.assertIn("d['trusted_main']==sys.argv[2]", execute)
        self.assertLess(execute.index("RECOVERY_V2_PRECHECK_PASS=VERIFIED"), execute.index("recovery-v2-execute-attempt-consumed.json"))
        self.assertLess(execute.index("recovery-v2-execute-attempt-consumed.json"), execute.index("Invalidate only same-boot"))

    def test_recovery_and_bootstrap_admissions_remain_narrow(self) -> None:
        recovery = RECOVERY.read_text(encoding="utf-8")
        for required in (
            "runtime_access: canonical_recovery",
            "canonical_registration: PRESENT",
            "registration_lease_generation: 55",
            "recovery_mode: same_boot_zero_client_invalidation_v1",
            "mutation_authorized: false",
            "credentials_allowed: false",
            "login_allowed: false",
            "process_control_authorized: false",
            "physical_action_budget: 0",
            "precheck_attempt_limit: 1",
            "recovery_attempt_limit: 1",
        ):
            self.assertIn(required, recovery)

        bootstrap = BOOTSTRAP.read_text(encoding="utf-8")
        for required in (
            "runtime_access: canonical_bootstrap",
            "canonical_registration: ABSENT",
            "bootstrap: PASS",
            "bootstrap_mode: create_new",
            "bootstrap_attempt_limit: 1",
            "credentials_allowed: false",
            "login_allowed: false",
            "process_control_authorized: true",
            "physical_action_budget: 1",
        ):
            self.assertIn(required, bootstrap)

    def test_census_contract_keeps_all_container_fail_closed_boundary(self) -> None:
        text = CENSUS.read_text(encoding="utf-8")
        for required in (
            "every running Docker container",
            "docker top",
            "comm == client",
            "comm` begins with `Tibia",
            "deep proof cannot execute",
            "fail closed",
            "narrow inventory to the canonical Kasm container only",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
