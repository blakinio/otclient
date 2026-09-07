from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / ".github/workflows/track-a-same-boot-zero-client-recovery-v2.yml"
RECOVERY = ROOT / "docs/agents/tasks/active/OTC-20260907-same-boot-zero-client-recovery-v2-live.md"
BOOTSTRAP = ROOT / "docs/agents/tasks/active/OTC-20260907-same-boot-zero-client-bootstrap-v2-live.md"
SCOPE = ROOT / "docs/agents/contracts/TRACK_A_CANONICAL_KASM_RUNTIME_SCOPE_V1.md"
TRANSITION = ROOT / ".github/scripts/tibia-official-client-re-canonical-live-transition-scoped.py"


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
            "tibia-official-client-re-canonical-live-transition-scoped.py",
            "guard-run",
            "kasm-bootstrap",
            "canonical_kasm_container",
            "NO_CREDENTIAL_ACCESS=true",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        for forbidden in (
            "${{ secrets.",
            "TIBIA_TEST_EMAIL",
            "TIBIA_TEST_PASSWORD",
            "auth-one-shot",
            "docker top",
            "all_running_docker_containers",
            "same-boot-zero-client-recovery-attempt-consumed.json",
            "bootstrap-attempt-consumed.json",
        ):
            self.assertNotIn(forbidden, text)

    def test_precheck_is_zero_action_and_execute_is_gated_by_same_main_pass(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        precheck = text.split("  live-precheck:", 1)[1].split("  live-execute:", 1)[0]
        execute = text.split("  live-execute:", 1)[1]
        self.assertIn('python3 "$worker" preflight "$record"', precheck)
        self.assertNotIn('python3 "$transition" kasm-bootstrap', precheck)
        self.assertNotIn("invalidate-compatible.py", precheck)
        self.assertIn("pre['container_name']=='otclient-track-a-kasmvnc'", precheck)
        self.assertIn("pre['candidate_count']==0", precheck)
        self.assertIn("pre['boot_id_sha256']==reg['boot_id_sha256']", precheck)
        self.assertIn("d['trusted_main']==sys.argv[2]", execute)
        self.assertLess(execute.index("RECOVERY_V2_PRECHECK_PASS=VERIFIED"), execute.index("recovery-v2-execute-attempt-consumed.json"))
        self.assertLess(execute.index("recovery-v2-execute-attempt-consumed.json"), execute.index("Invalidate only same-boot"))

    def test_transition_accepts_truthful_canonical_scope_without_weakening_legacy_reads(self) -> None:
        text = TRANSITION.read_text(encoding="utf-8")
        self.assertIn('CANONICAL_SCOPE = "canonical_kasm_container"', text)
        self.assertIn('LEGACY_SCOPE = "all_running_docker_containers"', text)
        self.assertIn("ALLOWED_SCOPES", text)
        self.assertIn('"inventory_scope": CANONICAL_SCOPE', text)
        self.assertIn("_base._read = _read", text)
        self.assertIn("_base._manifest = _manifest", text)
        self.assertIn("_base._require_kasm_launch_matches_manifest", text)
        self.assertLess(text.index("lstat()"), text.index("read_text()"))

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
            "TRACK_A_CANONICAL_KASM_RUNTIME_SCOPE_V1",
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
            "TRACK_A_CANONICAL_KASM_RUNTIME_SCOPE_V1",
            "inventory_scope: canonical_kasm_container",
        ):
            self.assertIn(required, bootstrap)

    def test_scope_contract_is_canonical_container_only(self) -> None:
        text = SCOPE.read_text(encoding="utf-8")
        for required in (
            "otclient-track-a-kasmvnc",
            "Other Docker containers on the Synology host are outside",
            "MUST NOT be executed into",
            "candidate_count == 0",
            "main_window_count == 0",
            "second official-client process inside the canonical container is forbidden",
            "supersedes earlier wording",
        ):
            self.assertIn(required, text)
        self.assertNotIn("every running Docker container", text)


if __name__ == "__main__":
    unittest.main()
