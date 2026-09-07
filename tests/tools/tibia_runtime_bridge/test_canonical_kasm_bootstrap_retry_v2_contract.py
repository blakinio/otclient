from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / ".github/workflows/track-a-canonical-kasm-bootstrap-retry-v2.yml"
TASK = ROOT / "docs/agents/tasks/active/OTC-20260907-canonical-kasm-bootstrap-retry-v2-live.md"
WORKER = ROOT / ".github/scripts/tibia-official-client-re-kasm-bootstrap-worker-compatible.py"


class Tests(unittest.TestCase):
    def test_owner_precheck_and_execute_are_new_one_shot_main_only_commands(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        for required in (
            "TASK_ID: OTC-20260907-canonical-kasm-bootstrap-retry-v2-live",
            "github.event.issue.number == 975",
            "github.event.comment.user.login == github.repository_owner",
            "/track-a-canonical-kasm-bootstrap-retry-v2 PRECHECK",
            "/track-a-canonical-kasm-bootstrap-retry-v2 EXECUTE",
            "runs-on: [otclient, synology]",
            "ref: main",
            "bootstrap-retry-v2-precheck-attempt-consumed.json",
            "bootstrap-retry-v2-precheck-pass.json",
            "bootstrap-retry-v2-execute-attempt-consumed.json",
            "BOOTSTRAP_RETRY_V2_PRECHECK_PASS=VERIFIED",
            "tibia-official-client-re-canonical-live-transition-scoped.py",
            "kasm-bootstrap",
            "NO_CREDENTIAL_ACCESS=true",
        ):
            self.assertIn(required, text)
        for forbidden in (
            "${{ secrets.", "auth-one-shot", "same-boot-zero-client", "invalidate-compatible.py",
            "/track-a-canonical-kasm-bootstrap-retry PRECHECK'",
            "/track-a-canonical-kasm-bootstrap-retry EXECUTE'",
        ):
            self.assertNotIn(forbidden, text)

    def test_precheck_is_zero_process_action_and_execute_requires_registration_absent(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        precheck = text.split("  live-precheck:", 1)[1].split("  live-execute:", 1)[0]
        execute = text.split("  live-execute:", 1)[1]
        self.assertIn("test ! -e", precheck)
        self.assertIn('python3 "$2" preflight "$3"', precheck)
        self.assertNotIn('python3 "$transition" kasm-bootstrap', precheck)
        self.assertNotIn("docker exec -d", precheck)
        self.assertIn("test ! -e", execute)
        self.assertLess(
            execute.index("BOOTSTRAP_RETRY_V2_PRECHECK_PASS=VERIFIED"),
            execute.index("bootstrap-retry-v2-execute-attempt-consumed.json"),
        )
        self.assertLess(
            execute.index("bootstrap-retry-v2-execute-attempt-consumed.json"),
            execute.index('python3 "$transition" kasm-bootstrap'),
        )
        self.assertIn("inventory_scope']=='canonical_kasm_container", execute)
        self.assertIn("main_window_count']==1", execute)

    def test_live_task_is_narrow_single_process_bootstrap_after_zero_state_survey(self) -> None:
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
            "34122156989",
            "TARGET_NAMESPACE_CLIENTS=0",
        ):
            self.assertIn(required, text)
        self.assertIn("does **not** authorize another registration invalidation", text)

    def test_worker_uses_exact_binary_directory_and_fail_closed_preidentity_rollback(self) -> None:
        text = WORKER.read_text(encoding="utf-8")
        for required in (
            "CLIENT_DIR = str(Path(_base.CLIENT_PATH).parent)",
            '"-w", CLIENT_DIR',
            'LD_LIBRARY_PATH={CLIENT_DIR}:{CLIENT_DIR}/lib',
            "cd {shlex.quote(CLIENT_DIR)} && exec ./client",
            "rollback_prelaunch_zero_state_unproven",
            "fresh = _base.collect_preflight(runner)",
            "if fresh != saved",
            "_base.rollback_launch = rollback_launch",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
