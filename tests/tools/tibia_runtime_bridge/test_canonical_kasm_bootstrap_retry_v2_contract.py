from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / ".github/workflows/track-a-canonical-kasm-bootstrap-retry-v2.yml"
TASK = ROOT / "docs/agents/tasks/active/OTC-20260907-official-linux-entrypoint-bootstrap.md"
WORKER = ROOT / ".github/scripts/tibia-official-client-re-kasm-bootstrap-worker-compatible.py"


class Tests(unittest.TestCase):
    def test_owner_precheck_and_execute_are_fresh_one_shot_main_only_commands(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        for required in (
            "TASK_ID: OTC-20260907-official-linux-entrypoint-bootstrap",
            "github.event.issue.number == 975",
            "github.event.comment.user.login == github.repository_owner",
            "/track-a-official-linux-entrypoint-bootstrap PRECHECK",
            "/track-a-official-linux-entrypoint-bootstrap EXECUTE",
            "runs-on: [otclient, synology]",
            "ref: main",
            "official-entrypoint-precheck-attempt-consumed.json",
            "official-entrypoint-precheck-pass.json",
            "official-entrypoint-execute-attempt-consumed.json",
            "OFFICIAL_ENTRYPOINT_PRECHECK_PASS=VERIFIED",
            "tibia-official-client-re-canonical-live-transition-scoped.py",
            "kasm-bootstrap",
            "NO_CREDENTIAL_ACCESS=true",
        ):
            self.assertIn(required, text)
        for forbidden in (
            "${{ secrets.", "auth-one-shot", "same-boot-zero-client", "invalidate-compatible.py",
            "/track-a-canonical-kasm-bootstrap-retry-v2 PRECHECK",
            "/track-a-canonical-kasm-bootstrap-retry-v2 EXECUTE",
        ):
            self.assertNotIn(forbidden, text)

    def test_precheck_is_zero_process_action_and_binds_official_entrypoint(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        precheck = text.split("  live-precheck:", 1)[1].split("  live-execute:", 1)[0]
        execute = text.split("  live-execute:", 1)[1]
        self.assertIn("test ! -e", precheck)
        self.assertIn('python3 "$2" preflight "$3"', precheck)
        self.assertIn("pre['launcher_path']", precheck)
        self.assertIn("pre['launcher_sha256']", precheck)
        self.assertNotIn('python3 "$transition" kasm-bootstrap', precheck)
        self.assertNotIn("docker exec -d", precheck)
        self.assertIn("test ! -e", execute)
        self.assertLess(
            execute.index("OFFICIAL_ENTRYPOINT_PRECHECK_PASS=VERIFIED"),
            execute.index("official-entrypoint-execute-attempt-consumed.json"),
        )
        self.assertLess(
            execute.index("official-entrypoint-execute-attempt-consumed.json"),
            execute.index('python3 "$transition" kasm-bootstrap'),
        )
        self.assertIn("inventory_scope']=='canonical_kasm_container", execute)
        self.assertIn("main_window_count']==1", execute)

    def test_live_task_is_single_changed_hypothesis_bootstrap_after_direct_launch_failure(self) -> None:
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
            "34124555199",
            "34124687615",
            "TARGET_NAMESPACE_CLIENTS=0",
            "official Linux top-level entrypoint",
        ):
            self.assertIn(required, text)
        self.assertIn("does **not** authorize another registration invalidation", text)

    def test_worker_uses_official_entrypoint_and_preserves_fail_closed_cleanup(self) -> None:
        text = WORKER.read_text(encoding="utf-8")
        for required in (
            'LAUNCH_METHOD = "docker_exec_detached_official_linux_entrypoint"',
            '"-w", launcher_dir',
            '"-u", "LD_LIBRARY_PATH"',
            "exec ./Tibia",
            "launcher_candidate_count",
            "launcher_process_not_unique",
            "launcher_residue",
            "rollback_launcher_identity_drift",
            "rollback_late_client_not_unique",
            "_launcher_aware_exact_candidates",
            "_base.rollback_launch = rollback_launch",
        ):
            self.assertIn(required, text)
        for forbidden in (
            "cd {shlex.quote(CLIENT_DIR)} && exec ./client",
            '"-e", f"LD_LIBRARY_PATH={CLIENT_DIR}:{CLIENT_DIR}/lib"',
        ):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
