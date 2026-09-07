from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / ".github/workflows/track-a-canonical-kasm-bootstrap-retry-v2.yml"
TASK = ROOT / "docs/agents/tasks/active/OTC-20260907-official-entrypoint-transition-compat-bootstrap.md"
WORKER = ROOT / ".github/scripts/tibia-official-client-re-kasm-bootstrap-worker-compatible.py"
TRANSITION = ROOT / ".github/scripts/tibia-official-client-re-canonical-live-transition-scoped.py"


def load_transition():
    name = "test_track_a_official_entrypoint_transition_scoped"
    sys.modules.pop(name, None)
    spec = importlib.util.spec_from_file_location(name, TRANSITION)
    if spec is None or spec.loader is None:
        raise RuntimeError("scoped transition unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def official_preflight(module):
    base = module._base
    record = {
        "schema": base.KASM_PREFLIGHT_SCHEMA,
        "container_name": base.KASM_TARGET_CONTAINER,
        "container_id": "a" * 64,
        "display": base.KASM_TARGET_DISPLAY,
        "package_dir": base.KASM_PACKAGE_DIR,
        "client_path": base.KASM_CLIENT_PATH,
        "client_size": base.SIZE,
        "client_sha256": base.SHA,
        "boot_id_sha256": "b" * 64,
        "candidate_count": 0,
        "main_window_count": 0,
        "launcher_path": "/home/kasm-user/Tibia/Tibia",
        "launcher_dir": "/home/kasm-user/Tibia",
        "launcher_size": 123456,
        "launcher_sha256": "c" * 64,
        "launcher_selection": "unique",
    }
    record["preflight_fingerprint"] = hashlib.sha256(
        json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return record


def official_launch(module, preflight):
    base = module._base
    return {
        "schema": base.KASM_LAUNCH_SCHEMA,
        "preflight_fingerprint": preflight["preflight_fingerprint"],
        "container_name": base.KASM_TARGET_CONTAINER,
        "container_id": preflight["container_id"],
        "display": base.KASM_TARGET_DISPLAY,
        "package_dir": base.KASM_PACKAGE_DIR,
        "client_path": base.KASM_CLIENT_PATH,
        "client_size": base.SIZE,
        "client_sha256": base.SHA,
        "pid": 123,
        "process_start_ticks": 456,
        "launch_method": module.OFFICIAL_ENTRYPOINT_LAUNCH_METHOD,
        "bootstrap_helper_residue": False,
        "client_dir": module.KASM_CLIENT_DIR,
        "launcher_path": preflight["launcher_path"],
        "launcher_dir": preflight["launcher_dir"],
        "launcher_size": preflight["launcher_size"],
        "launcher_sha256": preflight["launcher_sha256"],
        "launcher_selection": preflight["launcher_selection"],
    }


def read_record(module, record, schema):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "record.json"
        path.write_text(json.dumps(record), encoding="utf-8")
        return module._read_kasm_bootstrap_record(path, schema)


class Tests(unittest.TestCase):
    def test_owner_precheck_and_execute_are_fresh_one_shot_main_only_commands(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        for required in (
            "TASK_ID: OTC-20260907-official-entrypoint-transition-compat-bootstrap",
            "github.event.issue.number == 975",
            "github.event.comment.user.login == github.repository_owner",
            "/track-a-official-entrypoint-transition-compat-bootstrap PRECHECK",
            "/track-a-official-entrypoint-transition-compat-bootstrap EXECUTE",
            "runs-on: [otclient, synology]",
            "ref: main",
            "transition-compat-precheck-attempt-consumed.json",
            "transition-compat-precheck-pass.json",
            "transition-compat-execute-attempt-consumed.json",
            "OFFICIAL_ENTRYPOINT_TRANSITION_COMPAT_PRECHECK_PASS=VERIFIED",
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
            execute.index("OFFICIAL_ENTRYPOINT_TRANSITION_COMPAT_PRECHECK_PASS=VERIFIED"),
            execute.index("transition-compat-execute-attempt-consumed.json"),
        )
        self.assertLess(
            execute.index("transition-compat-execute-attempt-consumed.json"),
            execute.index('python3 "$transition" kasm-bootstrap'),
        )
        self.assertIn("inventory_scope']=='canonical_kasm_container", execute)
        self.assertIn("main_window_count']==1", execute)

    def test_live_task_is_fresh_compatibility_bootstrap_after_schema_failure(self) -> None:
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
            "34131050885",
            "34131140019",
            "34131763597",
            "kasm_bootstrap_record_invalid",
            "official Linux entrypoint",
        ):
            self.assertIn(required, text)
        self.assertIn("one additional narrow corrective Track A PR", text)

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

    def test_scoped_transition_accepts_exact_official_entrypoint_records(self) -> None:
        module = load_transition()
        preflight = official_preflight(module)
        launch = official_launch(module, preflight)
        self.assertEqual(
            read_record(module, preflight, module._base.KASM_PREFLIGHT_SCHEMA),
            preflight,
        )
        self.assertEqual(
            read_record(module, launch, module._base.KASM_LAUNCH_SCHEMA),
            launch,
        )
        module._require_kasm_launch_bound_to_preflight(preflight, launch)

    def test_scoped_transition_preserves_legacy_preflight_reader(self) -> None:
        module = load_transition()
        record = official_preflight(module)
        for key in tuple(module._LAUNCHER_FIELDS):
            record.pop(key)
        record.pop("preflight_fingerprint")
        record["preflight_fingerprint"] = hashlib.sha256(
            json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        self.assertEqual(
            read_record(module, record, module._base.KASM_PREFLIGHT_SCHEMA),
            record,
        )

    def test_scoped_transition_rejects_partial_launcher_record(self) -> None:
        module = load_transition()
        record = official_preflight(module)
        record.pop("launcher_sha256")
        with self.assertRaises(module._base.E) as caught:
            read_record(module, record, module._base.KASM_PREFLIGHT_SCHEMA)
        self.assertEqual(caught.exception.code, "kasm_bootstrap_record_invalid")

    def test_scoped_transition_rejects_launcher_drift_between_preflight_and_launch(self) -> None:
        module = load_transition()
        preflight = official_preflight(module)
        launch = official_launch(module, preflight)
        launch["launcher_size"] += 1
        launch = read_record(module, launch, module._base.KASM_LAUNCH_SCHEMA)
        with self.assertRaises(module._base.E) as caught:
            module._require_kasm_launch_bound_to_preflight(preflight, launch)
        self.assertEqual(caught.exception.code, "kasm_bootstrap_launch_preflight_mismatch")


if __name__ == "__main__":
    unittest.main()