from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / ".github/workflows/track-a-canonical-kasm-bootstrap-retry.yml"
TASK = ROOT / "docs/agents/tasks/active/OTC-20260907-canonical-kasm-bootstrap-retry-live.md"
WORKER = ROOT / ".github/scripts/tibia-official-client-re-kasm-bootstrap-worker-compatible.py"
PROBE = ROOT / ".github/scripts/tibia-official-client-re-kasm-existing-runtime-probe-compatible.py"


class Tests(unittest.TestCase):
    def test_owner_precheck_and_execute_are_separate_and_main_only(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        for required in (
            "github.event.issue.number == 975",
            "github.event.comment.user.login == github.repository_owner",
            "/track-a-canonical-kasm-bootstrap-retry PRECHECK",
            "/track-a-canonical-kasm-bootstrap-retry EXECUTE",
            "runs-on: [otclient, synology]",
            "ref: main",
            "bootstrap-retry-precheck-attempt-consumed.json",
            "bootstrap-retry-precheck-pass.json",
            "bootstrap-retry-execute-attempt-consumed.json",
            "BOOTSTRAP_RETRY_PRECHECK_PASS=VERIFIED",
            "tibia-official-client-re-canonical-live-transition-scoped.py",
            "kasm-bootstrap",
            "NO_CREDENTIAL_ACCESS=true",
        ):
            self.assertIn(required, text)
        for forbidden in (
            "${{ secrets.", "TIBIA_TEST_EMAIL", "TIBIA_TEST_PASSWORD", "auth-one-shot",
            "same-boot-zero-client", "invalidate-compatible.py",
        ):
            self.assertNotIn(forbidden, text)

    def test_precheck_is_zero_process_action_and_execute_is_registration_absent_only(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        precheck = text.split("  live-precheck:", 1)[1].split("  live-execute:", 1)[0]
        execute = text.split("  live-execute:", 1)[1]
        self.assertIn("test ! -e", precheck)
        self.assertIn('python3 "$2" preflight "$3"', precheck)
        self.assertNotIn('python3 "$transition" kasm-bootstrap', precheck)
        self.assertNotIn("docker exec -d", precheck)
        self.assertIn("test ! -e", execute)
        self.assertLess(execute.index("BOOTSTRAP_RETRY_PRECHECK_PASS=VERIFIED"), execute.index("bootstrap-retry-execute-attempt-consumed.json"))
        self.assertLess(execute.index("bootstrap-retry-execute-attempt-consumed.json"), execute.index('python3 "$transition" kasm-bootstrap'))
        self.assertIn("inventory_scope']=='canonical_kasm_container", execute)

    def test_live_task_is_narrow_one_process_bootstrap(self) -> None:
        text = TASK.read_text(encoding="utf-8")
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
            "physical_action_count: 0",
            "precheck_attempt_limit: 1",
            "execute_attempt_limit: 1",
            "TRACK_A_CANONICAL_KASM_RUNTIME_SCOPE_V1",
        ):
            self.assertIn(required, text)
        self.assertIn("does **not** authorize another invalidation", text)

    def test_worker_and_probe_are_canonical_scoped_and_readiness_bounded(self) -> None:
        worker = WORKER.read_text(encoding="utf-8")
        probe = PROBE.read_text(encoding="utf-8")
        self.assertIn("XAUTHORITY", worker)
        self.assertIn("LD_LIBRARY_PATH", worker)
        self.assertIn("_base.write_record(path, launch)", worker)
        self.assertIn("_base._window_count", worker)
        self.assertIn("postlaunch_window_not_ready", worker)
        self.assertIn("RETRYABLE_READINESS", probe)
        self.assertIn("main_window_count:0", probe)
        self.assertIn("attempts: int = 48", probe)
        self.assertIn("canonical_kasm_container", probe)


if __name__ == "__main__":
    unittest.main()
