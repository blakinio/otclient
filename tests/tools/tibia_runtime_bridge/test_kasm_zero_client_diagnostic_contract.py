from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / ".github/scripts/track_a_kasm_zero_client_diagnose.py"
WORKFLOW = ROOT / ".github/workflows/track-a-kasm-zero-client-diagnose.yml"
LIVE_TASK = ROOT / "docs/agents/tasks/active/OTC-20260907-same-boot-zero-client-diagnostic-live.md"


def _load_script():
    spec = importlib.util.spec_from_file_location("track_a_kasm_zero_client_diagnostic_contract", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class KasmZeroClientDiagnosticContractTests(unittest.TestCase):
    def test_wrapper_surfaces_only_sanitized_worker_code(self) -> None:
        module = _load_script()

        class FakeWorkerError(RuntimeError):
            pass

        def fail_preflight():
            raise FakeWorkerError("official_client_candidate_count:1")

        worker = SimpleNamespace(WorkerError=FakeWorkerError, collect_preflight=fail_preflight)
        ok, code = module.diagnose(worker)
        self.assertFalse(ok)
        self.assertEqual(code, "official_client_candidate_count:1")

        def unsafe_preflight():
            raise FakeWorkerError("unsafe code /tmp/secret")

        worker.collect_preflight = unsafe_preflight
        with self.assertRaises(module.DiagnosticError):
            module.diagnose(worker)

    def test_wrapper_is_read_only_approved_worker_guarded_and_manifest_driven(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        for required in (
            "tibia-official-client-re-kasm-bootstrap-worker.py",
            "collect_preflight",
            "current_client_fence",
            "coordination.lock",
            "LOCK_EX",
            "LOCK_NB",
            "TRACK_A_ZERO_CLIENT_DIAGNOSTIC_GUARDED",
            "CREDENTIAL_ACCESS=false",
            "RUNTIME_MUTATION=false",
            "TRACK_A_KASM_ZERO_CLIENT_DIAGNOSTIC_ERROR=",
            "SAFE_CODE_RE",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        for forbidden in (
            "TIBIA_TEST_EMAIL",
            "TIBIA_TEST_PASSWORD",
            "runtime-registration.json",
            "os.replace",
            "subprocess.Popen",
            '"-TERM"',
            '"-KILL"',
            '"docker", "exec", "-d"',
        ):
            self.assertNotIn(forbidden, text)

    def test_owner_workflow_is_diagnostic_only_and_never_consumes_recovery_budget(self) -> None:
        self.assertTrue(WORKFLOW.is_file(), "zero-client diagnostic workflow missing")
        text = WORKFLOW.read_text(encoding="utf-8")
        for required in (
            "github.event_name == 'issue_comment'",
            "github.event.issue.number == 975",
            "github.event.comment.user.login == github.repository_owner",
            "/track-a-same-boot-zero-client-diagnose RUN",
            "runs-on: [otclient, synology]",
            "ref: main",
            "TRACK_A_ZERO_CLIENT_DIAGNOSTIC_GUARDED=1",
            "tibia-official-client-re-canonical-live-lease",
            "guard-run",
            "track_a_kasm_zero_client_diagnose.py",
            "zero-client-diagnostic-attempt-consumed.json",
            "os.O_EXCL",
            "DIAGNOSTIC_ONE_SHOT_AUTHORIZATION_CONSUMED=PASS",
            "NO_CREDENTIAL_ACCESS=true",
            "RUNTIME_MUTATION=false",
            "GITHUB_RUN_ATTEMPT",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        for forbidden in (
            "${{ secrets.",
            "TIBIA_TEST_EMAIL",
            "TIBIA_TEST_PASSWORD",
            "auth-one-shot",
            "kasm-bootstrap",
            "same-boot-zero-client-recovery-attempt-consumed",
            "bootstrap-attempt-consumed",
            "runtime-registration.json",
        ):
            self.assertNotIn(forbidden, text)

    def test_live_admission_is_zero_action_canonical_recovery_diagnostic(self) -> None:
        text = LIVE_TASK.read_text(encoding="utf-8")
        for required in (
            "runtime_access: canonical_recovery",
            "canonical_registration: PRESENT",
            "registration_lease_generation: 55",
            "recovery_mode: same_boot_zero_client_invalidation_v1",
            "same_boot_zero_client_contract: TRACK_A_SAME_BOOT_ZERO_CLIENT_INVALIDATION_V1",
            "mutation_authorized: false",
            "credentials_allowed: false",
            "login_allowed: false",
            "process_control_authorized: false",
            "physical_action_budget: 0",
            "diagnostic_attempt_limit: 1",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
