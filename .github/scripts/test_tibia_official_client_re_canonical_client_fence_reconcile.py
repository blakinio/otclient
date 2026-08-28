#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).with_name(
    "tibia-official-client-re-canonical-client-fence-reconcile.py"
)
GOVERNANCE = Path(__file__).with_name("test_track_a_agent_runtime_governance.py")


def load():
    if not SCRIPT.exists():
        raise AssertionError("canonical client-fence reconciliation implementation missing")
    spec = importlib.util.spec_from_file_location("canonical_fence_reconcile_tested", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_governance():
    spec = importlib.util.spec_from_file_location("track_a_governance_tested", GOVERNANCE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def fingerprint(document: dict[str, object]) -> str:
    payload = (
        f"{document['runtime_locator']}:{document['pid']}:"
        f"{document['process_start_ticks']}:{document['client_size']}:"
        f"{document['client_sha256']}"
    )
    return hashlib.sha256(payload.encode()).hexdigest()


class Tests(unittest.TestCase):
    def setUp(self):
        self.m = load()
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.root = root
        self.m.STATE = root
        self.m.REG = root / "runtime-registration.json"
        self.m.LEASE = root / "lease.json"
        self.m.LOCK = root / "coordination.lock"
        self.m.STATE.mkdir(parents=True, exist_ok=True)
        self.m.LOCK.write_text("")

        self.args = argparse.Namespace(
            task_id="OTC-TEST",
            session_id="session",
            probe=Path(__file__).with_name(
                "tibia-official-client-re-kasm-existing-runtime-probe.py"
            ),
        )
        self.old = {
            "schema_version": 1,
            "runtime_id": "track-a-canonical-live",
            "registration_generation": 7,
            "lease_generation": 30,
            "registered_at": 1,
            "boot_id_sha256": "a" * 64,
            "pid": 19590,
            "process_start_ticks": 76611792,
            "client_version": "15.32",
            "client_size": 52109920,
            "client_sha256": "ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8",
            "display": ":1",
            "window_identity": "x11:0x9:pid:19590:class:client/Tibia:title_sha256:" + "b" * 64,
            "remote_view_endpoint": "https://127.0.0.1:6901/",
            "remote_view_mapping": "PROVEN",
            "state": "UNKNOWN",
            "proof_kind": "existing_runtime_adoption_v1",
            "runtime_locator": "docker:otclient-track-a-kasmvnc:old-container-id",
            "inventory_scope": "all_running_docker_containers",
            "inventory_complete": True,
            "candidate_count": 1,
            "candidate_fingerprint": "",
            "state_evidence": "BRIDGE_3_OF_3_SEMANTICS_UNPROVEN",
            "source_task": "old-task",
            "source_run": "old-run",
        }
        self.old["candidate_fingerprint"] = fingerprint(self.old)

        self.fresh = {
            "proof_kind": "existing_runtime_adoption_v1",
            "boot_id_sha256": "c" * 64,
            "pid": 646,
            "process_start_ticks": 1394843,
            "client_version": "15.32.75d4a0",
            "client_size": 52105824,
            "client_sha256": "d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a",
            "display": ":1",
            "window_identity": "x11:0x17:pid:646:class:client/Tibia:title_sha256:" + "d" * 64,
            "remote_view_endpoint": "https://127.0.0.1:6901/",
            "remote_view_mapping": "PROVEN",
            "state": "UNKNOWN",
            "runtime_locator": "docker:otclient-track-a-kasmvnc:new-container-id",
            "inventory_scope": "all_running_docker_containers",
            "inventory_complete": True,
            "candidate_count": 1,
            "candidate_fingerprint": "",
            "state_evidence": "NO_STRUCTURAL_BRIDGE",
        }
        self.fresh["candidate_fingerprint"] = fingerprint(self.fresh)
        self.write_registration(self.old)
        self.write_lease(31)

    def tearDown(self):
        self.temp.cleanup()

    def write_registration(self, data: dict[str, object]) -> None:
        self.m.REG.write_text(json.dumps(data, sort_keys=True) + "\n")
        self.m.REG.chmod(0o600)

    def write_lease(self, generation: int) -> None:
        data = {
            "schema_version": 1,
            "runtime_id": "track-a-canonical-live",
            "status": "active",
            "generation": generation,
            "controller_task": self.args.task_id,
            "controller_session": self.args.session_id,
        }
        self.m.LEASE.write_text(json.dumps(data, sort_keys=True) + "\n")
        self.m.LEASE.chmod(0o600)

    def write_recovery_admission(self, *, recovery_mode: str | None) -> Path:
        path = self.root / f"admission-{recovery_mode or 'legacy'}.md"
        extra = ""
        if recovery_mode:
            extra = (
                f"recovery_mode: {recovery_mode}\n"
                "client_fence_reconciliation_contract: "
                "TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_V1\n"
            )
        path.write_text(
            "---\n"
            "task_id: OTC-TEST\n"
            "track_id: official-client-re\n"
            "runtime_access: canonical_recovery\n"
            "runtime_owner_task: OTC-TEST\n"
            "runtime_namespace: canonical-live-runtime\n"
            "canonical_registration: PRESENT\n"
            "canonical_lease_generation: UNKNOWN\n"
            "registration_lease_generation: UNKNOWN\n"
            "gate_a: REQUIRED_NOT_PROVEN\n"
            "generation_rebind: NOT_APPLICABLE\n"
            "gate_b: NOT_APPLICABLE\n"
            "bootstrap: NOT_APPLICABLE\n"
            "target_uniqueness: UNKNOWN\n"
            "mutation_authorized: false\n"
            + extra
            + "---\n"
        )
        return path

    def reconcile(self, probes=None):
        probes = probes or [dict(self.fresh), dict(self.fresh), dict(self.fresh)]
        with mock.patch.object(self.m, "_require_external_guard", return_value=None), \
                mock.patch.object(self.m, "_probe", side_effect=probes) as probe, \
                mock.patch.object(self.m.time, "time", return_value=100), \
                mock.patch.dict(os.environ, {"GITHUB_RUN_ID": "123"}, clear=False):
            self.m.reconcile(self.args)
        return probe

    def test_reconciles_only_approved_superseded_fence_to_current_exact_target(self):
        probe = self.reconcile()
        data = json.loads(self.m.REG.read_text())
        self.assertEqual(probe.call_count, 3)
        self.assertEqual(
            (data["client_version"], data["client_size"], data["client_sha256"]),
            self.m.CURRENT_FENCE,
        )
        self.assertEqual(data["registration_generation"], 8)
        self.assertEqual(data["lease_generation"], 31)
        self.assertEqual(data["pid"], self.fresh["pid"])
        self.assertEqual(data["process_start_ticks"], self.fresh["process_start_ticks"])
        self.assertEqual(data["boot_id_sha256"], self.fresh["boot_id_sha256"])
        self.assertEqual(data["state"], "UNKNOWN")
        self.assertEqual(data["state_evidence"], "NO_STRUCTURAL_BRIDGE")
        self.assertEqual(data["source_task"], "OTC-TEST")
        self.assertEqual(data["source_run"], "123")
        self.assertEqual(stat.S_IMODE(self.m.REG.stat().st_mode), 0o600)

    def test_reconciles_when_stable_remote_view_mapping_is_unknown(self):
        old = dict(self.old, remote_view_mapping="UNKNOWN")
        old["candidate_fingerprint"] = fingerprint(old)
        fresh = dict(self.fresh, remote_view_mapping="UNKNOWN")
        fresh["candidate_fingerprint"] = fingerprint(fresh)
        self.write_registration(old)
        probe = self.reconcile([dict(fresh), dict(fresh), dict(fresh)])
        data = json.loads(self.m.REG.read_text())
        self.assertEqual(probe.call_count, 3)
        self.assertEqual(data["remote_view_mapping"], "UNKNOWN")
        self.assertEqual(data["state"], "UNKNOWN")

    def test_rejects_invalid_source_remote_view_mapping_before_probe(self):
        bad = dict(self.old, remote_view_mapping="UNVERIFIED")
        self.write_registration(bad)
        with mock.patch.object(self.m, "_require_external_guard", return_value=None), \
                mock.patch.object(self.m, "_probe") as probe:
            with self.assertRaisesRegex(self.m.ReconcileError, "source_registration_remote_mapping_invalid"):
                self.m.reconcile(self.args)
        probe.assert_not_called()

    def test_rejects_any_unapproved_source_fence_before_probe(self):
        bad = dict(self.old, client_version="15.31")
        self.write_registration(bad)
        with mock.patch.object(self.m, "_require_external_guard", return_value=None), \
                mock.patch.object(self.m, "_probe") as probe:
            with self.assertRaisesRegex(self.m.ReconcileError, "source_fence_not_approved"):
                self.m.reconcile(self.args)
        probe.assert_not_called()

    def test_rejects_non_fail_closed_source_registration(self):
        bad = dict(self.old, state="IN_GAME", state_evidence="BRIDGE_3_OF_3")
        self.write_registration(bad)
        with mock.patch.object(self.m, "_require_external_guard", return_value=None), \
                mock.patch.object(self.m, "_probe") as probe:
            with self.assertRaisesRegex(self.m.ReconcileError, "source_registration_not_fail_closed"):
                self.m.reconcile(self.args)
        probe.assert_not_called()

    def test_requires_newer_current_controller_generation(self):
        self.write_lease(self.old["lease_generation"])
        with mock.patch.object(self.m, "_require_external_guard", return_value=None), \
                mock.patch.object(self.m, "_probe") as probe:
            with self.assertRaisesRegex(self.m.ReconcileError, "controller_generation_not_newer"):
                self.m.reconcile(self.args)
        probe.assert_not_called()

    def test_rejects_namespace_display_or_remote_mapping_drift(self):
        cases = (
            ("runtime_locator", "docker:other-container:newid", "runtime_namespace_changed"),
            ("display", ":2", "display_changed"),
            ("remote_view_endpoint", "https://127.0.0.1:6902/", "remote_view_endpoint_changed"),
            ("remote_view_mapping", "UNKNOWN", "remote_view_mapping_changed"),
        )
        for field, value, code in cases:
            with self.subTest(field=field):
                self.write_registration(self.old)
                fresh = dict(self.fresh, **{field: value})
                fresh["candidate_fingerprint"] = fingerprint(fresh)
                with mock.patch.object(self.m, "_require_external_guard", return_value=None), \
                        mock.patch.object(self.m, "_probe", return_value=fresh):
                    with self.assertRaisesRegex(self.m.ReconcileError, code):
                        self.m.reconcile(self.args)
                self.assertEqual(json.loads(self.m.REG.read_text()), self.old)

    def test_rejects_probe_identity_drift_before_commit_without_mutating_registration(self):
        changed = dict(self.fresh, pid=647)
        changed["window_identity"] = "x11:0x18:pid:647:class:client/Tibia:title_sha256:" + "e" * 64
        changed["candidate_fingerprint"] = fingerprint(changed)
        with mock.patch.object(self.m, "_require_external_guard", return_value=None), \
                mock.patch.object(self.m, "_probe", side_effect=[dict(self.fresh), changed]):
            with self.assertRaisesRegex(self.m.ReconcileError, "fresh_identity_changed_before_commit"):
                self.m.reconcile(self.args)
        self.assertEqual(json.loads(self.m.REG.read_text()), self.old)

    def test_rolls_back_exact_old_registration_after_post_commit_probe_drift(self):
        changed = dict(self.fresh, process_start_ticks=1394844)
        changed["candidate_fingerprint"] = fingerprint(changed)
        with mock.patch.object(self.m, "_require_external_guard", return_value=None), \
                mock.patch.object(
                    self.m,
                    "_probe",
                    side_effect=[dict(self.fresh), dict(self.fresh), changed],
                ), \
                mock.patch.object(self.m.time, "time", return_value=100), \
                mock.patch.dict(os.environ, {"GITHUB_RUN_ID": "123"}, clear=False):
            with self.assertRaisesRegex(self.m.ReconcileError, "fresh_identity_changed_after_commit"):
                self.m.reconcile(self.args)
        self.assertEqual(json.loads(self.m.REG.read_text()), self.old)

    def test_requires_external_canonical_guard(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(self.m.ReconcileError, "canonical_guard_required"):
                self.m._require_external_guard()

    def test_pending_client_fence_recovery_is_an_explicit_governance_mode(self):
        governance = load_governance()
        path = self.write_recovery_admission(
            recovery_mode="client_fence_reconciliation_v1"
        )
        self.assertTrue(governance.validate_track_a_task(path))

    def test_legacy_canonical_recovery_does_not_gain_unknown_generation_admission(self):
        governance = load_governance()
        path = self.write_recovery_admission(recovery_mode=None)
        with self.assertRaises(SystemExit):
            governance.validate_track_a_task(path)

    def test_client_fence_recovery_requires_exact_contract_binding(self):
        governance = load_governance()
        path = self.write_recovery_admission(
            recovery_mode="client_fence_reconciliation_v1"
        )
        text = path.read_text().replace(
            "TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_V1",
            "NOT_APPLICABLE",
        )
        path.write_text(text)
        with self.assertRaises(SystemExit):
            governance.validate_track_a_task(path)

    def test_source_contains_no_client_mutation_or_memory_observation_primitive(self):
        source = SCRIPT.read_text()
        for forbidden in (
            "ptrace",
            "/proc/",
            "os.kill",
            "killpg",
            "xdotool",
            "pyautogui",
            "process_vm_writev",
            "O_RDWR | os.O_CLOEXEC, /proc",
        ):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
