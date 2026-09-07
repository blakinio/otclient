from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / ".github/scripts/track_a_kasm_zero_client_stage_diagnose.py"
WORKFLOW = ROOT / ".github/workflows/track-a-kasm-zero-client-stage-diagnose.yml"
LIVE_TASK = ROOT / "docs/agents/tasks/active/OTC-20260907-zero-client-stage-diagnostic-live.md"


def _load_script():
    spec = importlib.util.spec_from_file_location("track_a_kasm_zero_client_stage_contract", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeWorkerError(RuntimeError):
    pass


def _worker(*, candidate_failure: bool = False, display_failure: bool = False):
    target = "a" * 64
    other = "b" * 64

    def docker_containers():
        return [(target, "canonical"), (other, "other")]

    def resolve_target(containers):
        assert containers
        return target

    def run(command):
        if display_failure and command[-1] == "xdpyinfo":
            raise FakeWorkerError("command_failed:docker:126")
        return "ok\n"

    def package_identity(container_id):
        assert container_id == target
        return {"client_size": 52105824}

    def boot_identity(container_id, runner=run):
        assert container_id == target
        runner(["docker", "exec", target, "python3", "-c", "boot"])
        return "c" * 64

    def candidate_rows(container_id):
        if candidate_failure and container_id == other:
            raise FakeWorkerError("command_failed:docker:126")
        return []

    def window_count(container_id):
        assert container_id == target
        return 0

    return SimpleNamespace(
        WorkerError=FakeWorkerError,
        TARGET_USER="kasm-user",
        TARGET_DISPLAY=":1",
        docker_containers=docker_containers,
        _target=resolve_target,
        run=run,
        package_identity=package_identity,
        boot_identity=boot_identity,
        candidate_rows=candidate_rows,
        _window_count=window_count,
    )


class KasmZeroClientStageDiagnosticContractTests(unittest.TestCase):
    def test_candidate_loop_localizes_non_target_failure_and_keeps_scanning(self) -> None:
        module = _load_script()
        errors, metadata = module.diagnose(_worker(candidate_failure=True))
        self.assertEqual(
            errors,
            [{"stage": "candidate_inventory_non_target_0", "code": "command_failed:docker:126"}],
        )
        self.assertEqual(metadata["running_container_count"], 2)
        self.assertEqual(metadata["non_target_container_count"], 1)
        self.assertEqual(metadata["exact_candidate_count"], 0)
        self.assertEqual(metadata["main_window_count"], 0)

    def test_independent_stage_failure_does_not_hide_candidate_or_window_results(self) -> None:
        module = _load_script()
        errors, metadata = module.diagnose(_worker(display_failure=True))
        self.assertEqual(errors, [{"stage": "display", "code": "command_failed:docker:126"}])
        self.assertEqual(metadata["running_container_count"], 2)
        self.assertEqual(metadata["non_target_container_count"], 1)
        self.assertEqual(metadata["main_window_count"], 0)

    def test_stage_wrapper_is_guarded_manifest_driven_and_read_only(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        for required in (
            "tibia-official-client-re-kasm-bootstrap-worker.py",
            "current_client_fence",
            "coordination.lock",
            "LOCK_EX",
            "LOCK_NB",
            "TRACK_A_ZERO_CLIENT_STAGE_DIAGNOSTIC_GUARDED",
            "docker_inventory",
            "target_resolution",
            "display",
            "package_identity",
            "boot_identity",
            "candidate_inventory_target",
            "candidate_inventory_non_target_",
            "window_inventory",
            "RUNNING_CONTAINER_COUNT=",
            "NON_TARGET_CONTAINER_COUNT=",
            "CREDENTIAL_ACCESS=false",
            "RUNTIME_MUTATION=false",
            "SAFE_CODE_RE",
            "SAFE_STAGE_RE",
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
            "kasm-bootstrap",
        ):
            self.assertNotIn(forbidden, text)

    def test_owner_workflow_is_one_shot_diagnostic_only(self) -> None:
        self.assertTrue(WORKFLOW.is_file(), "stage diagnostic workflow missing")
        text = WORKFLOW.read_text(encoding="utf-8")
        for required in (
            "github.event_name == 'issue_comment'",
            "github.event.issue.number == 975",
            "github.event.comment.user.login == github.repository_owner",
            "/track-a-same-boot-zero-client-stage-diagnose RUN",
            "runs-on: [otclient, synology]",
            "ref: main",
            "TRACK_A_ZERO_CLIENT_STAGE_DIAGNOSTIC_GUARDED=1",
            "tibia-official-client-re-canonical-live-lease",
            "guard-run",
            "track_a_kasm_zero_client_stage_diagnose.py",
            "zero-client-stage-diagnostic-attempt-consumed.json",
            "os.O_EXCL",
            "STAGE_DIAGNOSTIC_ONE_SHOT_AUTHORIZATION_CONSUMED=PASS",
            "NO_CREDENTIAL_ACCESS=true",
            "RUNTIME_MUTATION=false",
            "GITHUB_RUN_ATTEMPT",
            "diagnostic_rc -eq 0 || $diagnostic_rc -eq 2",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        for forbidden in (
            "${{ secrets.",
            "TIBIA_TEST_EMAIL",
            "TIBIA_TEST_PASSWORD",
            "auth-one-shot",
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
