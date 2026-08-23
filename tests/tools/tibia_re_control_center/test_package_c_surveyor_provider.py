from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import signal
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.tibia_re_control_center.model import Freshness, ValidationError
from tools.tibia_re_surveyor.collect_all import build_collect_all, write_collect_all
from tools.tibia_re_surveyor.survey import build_bundle

ROOT = Path(__file__).resolve().parents[3]
PRODUCER_COMMIT = "1affb3a094a06f2a250140e8173501b3a6938164"

AUTH_LAYOUT = {
    "source_object": "tibia::client::TGameClient", "auth_controller_object": "tibia::authentication::TAuthenticationProcessController",
    "game_client_vptr_offset": "0x30adce8", "game_client_typeinfo_offset": "0x30a7778",
    "auth_controller_vptr_offset": "0x30b5290", "auth_controller_typeinfo_offset": "0x30b4410",
    "auth_controller_member_offset": "0x8d0", "qstate_private_offset": "0x8",
    "qstate_state_offset": "0xf0", "qstate_running_value": 2,
    "representation": "qt_qstatemachine_isRunning_equivalent", "semantic_state": "TYPED_AUTH_LIFECYCLE_ONLY",
    "in_game_claimed": False, "credentials_retained": False, "session_secrets_retained": False,
}
PLAYER_LAYOUT = {
    "source_object": "tibia::cyclopedia::TCyclopediaMapStorage", "source_handler": "onPlayerPositionWasUpdated",
    "source_signal": "playerPositionChanged", "cyclopedia_vptr_offset": "0x30c2738",
    "cyclopedia_typeinfo_offset": "0x30c0aa0", "qt_metacast_offset": "0xd1eef0",
    "position_handler_offset": "0xd19ef0", "position_primary_offsets": ["0x2f0", "0x2f4", "0x2f8"],
    "position_mirror_offsets": ["0x408", "0x40c", "0x410"], "representation": "signed_i32_x3_mirrored",
    "semantic_state": "CANDIDATE_PENDING_CAUSAL_E2E",
}

ACTION_LAYOUT = {
    "type_name": "tibia::game::TPlayerProtocolMessageHandler",
    "mangled_name": "N5tibia4game29TPlayerProtocolMessageHandlerE",
    "vptr_offset": "0x30bf620",
    "typeinfo_offset": "0x30bf298",
    "representation": "exact_rtti_primary_vptr_object_identity",
}


def provider_module():
    try:
        return importlib.import_module("tools.tibia_re_control_center.surveyor_provider")
    except ModuleNotFoundError:
        return None


def survey_args(output: Path) -> argparse.Namespace:
    return argparse.Namespace(
        repo_root=ROOT,
        repo_container=None,
        repo_container_root=None,
        output_dir=output,
        collect_all=True,
        runtime_docker=False,
        runtime_container="otclient-track-a-kasmvnc",
        control_container="otclient-synology-runner",
        display=":1",
        keepalive=False,
        keepalive_authority=None,
        keepalive_trigger_seconds=480,
        turn_modifier="ctrl",
        top_next=20,
    )


def build_repo_bundle(root: Path) -> None:
    result = build_bundle(survey_args(root))
    if result.get("collect_all") is None:
        raise AssertionError("Surveyor collect-all output was not produced")


def load_json(root: Path, relative: str):
    return json.loads((root / relative).read_text(encoding="utf-8"))


def write_json(root: Path, relative: str, value) -> None:
    (root / relative).write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def rewrite_manifest(root: Path) -> None:
    lines: list[str] = []
    for path in sorted(
        item for item in root.rglob("*") if item.is_file() and item.name != "manifest.sha256"
    ):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(root).as_posix()}")
    (root / "manifest.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


def assert_validation_code(test: unittest.TestCase, code: str, fn) -> None:
    with test.assertRaises(ValidationError) as caught:
        fn()
    test.assertEqual(code, caught.exception.code)



def make_live_shaped_bundle(root: Path) -> None:
    build_repo_bundle(root)
    coverage = load_json(root, "surveyor/coverage.json")
    bundle = load_json(root, "surveyor/agent_bundle.json")
    bundle["runtime"] = {
        "observed_at_epoch": 1,
        "target_container": "otclient-track-a-kasmvnc",
        "control_container": "otclient-synology-runner",
        "display": ":1",
        "target_running": True,
        "runtime_namespace_scope": "DECLARED_TARGET_ONLY",
        "external_containers_scanned": False,
        "target_process_count": 1,
        "target_uniqueness_scope": "DECLARED_RUNTIME_NAMESPACE",
        "target_uniqueness": "PROVEN",
        "runtime_access": "READ_ONLY_ADMITTED",
        "visible_tibia_windows": [{"xid": 321, "pid": 123, "title_class": "CHARACTER_CONTEXT"}],
        "processes": [{
            "pid": 123,
            "process_start_ticks": 456,
            "exe_basename": "client",
            "client_size": 52109920,
            "client_sha256": "ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8",
            "exact_fence_match": True,
        }],
        "exact_current_fence": {
            "version": "15.32",
            "size": 52109920,
            "sha256": "ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8",
            "match": True,
        },
        "canonical_control": {
            "registration_present": True,
            "registration": {
                "schema_version": 1,
                "runtime_id": "track-a-canonical-live",
                "registration_generation": 7,
                "lease_generation": 7,
                "boot_id_sha256": "1" * 64,
                "pid": 123,
                "process_start_ticks": 456,
                "client_version": "15.32",
                "client_size": 52109920,
                "client_sha256": "ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8",
                "display": ":1",
                "remote_view_mapping": "UNKNOWN",
                "state": "IN_GAME",
                "source_task": "synthetic-package-c-test",
                "source_run": "synthetic-live-shaped",
            },
            "lease_present": True,
            "lease": {
                "schema_version": 1, "runtime_id": "track-a-canonical-live",
                "generation": 7, "status": "active", "controller_task": "synthetic-controller",
                "acquired_at": 0, "renewed_at": 1, "expires_at": 9999999999, "takeover_from": None,
            },
            "lease_expired": False,
        },
    }
    bundle["typed_readers"] = {
        "action_protocol_typed_reader": {
            "state": "UNAVAILABLE", "reader_id": "action_protocol_typed_reader",
            "reason": "STATIC_LAYOUT_FAILED:RuntimeError", "semantic_promotion_allowed": False,
        },
        "auth_session_typed_reader": {
            "state": "UNAVAILABLE", "reader_id": "auth_session_typed_reader",
            "reason": "READ_FAILED:RuntimeError", "semantic_promotion_allowed": False,
        },
        "ui_settings_typed_reader": {
            "state": "UNAVAILABLE", "reader_id": "ui_settings_typed_reader",
            "reason": "STATIC_SETTINGS_MODEL_FAILED:RuntimeError", "semantic_promotion_allowed": False,
        },
        "player_state_typed_reader": {
            "state": "AVAILABLE",
            "reader_id": "player_state_typed_reader",
            "position": {"x": 32547, "y": 32506, "z": 7},
            "object_count": 1,
            "position_mirror_consistent": True,
            "process_memory_access": "read_only",
            "semantic_state": "CANDIDATE_PENDING_CAUSAL_E2E",
            "layout_evidence": PLAYER_LAYOUT,
            "semantic_promotion_allowed": False,
        }
    }
    write_json(root, "surveyor/agent_bundle.json", bundle)
    write_json(root, "surveyor/runtime.json", bundle["runtime"])
    collect_all = build_collect_all(bundle, coverage["rows"])
    write_collect_all(root, collect_all)

class PackageCSurveyorProviderTests(unittest.TestCase):
    def provider(self):
        module = provider_module()
        self.assertIsNotNone(module, "Package C Surveyor provider is not implemented")
        return module

    def test_repository_only_round_trip_is_fail_closed(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            model = module.load_surveyor_bundle(
                root,
                producer_commit=PRODUCER_COMMIT,
                ingested_monotonic_ns=123,
            )
        self.assertEqual("UNKNOWN", model.runtime_status.runtime_state)
        self.assertEqual("UNKNOWN", model.runtime_status.client_state)
        self.assertEqual("READ_ONLY", model.runtime_status.authority_state)
        self.assertEqual(Freshness.UNKNOWN, model.runtime_status.freshness)
        self.assertIsNone(model.runtime_status.runtime_instance_id)
        self.assertEqual("UNKNOWN", model.snapshot.client_state)
        self.assertEqual({"x": None, "y": None, "z": None}, model.snapshot.player["position"])
        self.assertTrue(all(not capability.action_supported for capability in model.capabilities))
        self.assertEqual("UNAVAILABLE", model.readiness["runtime_identity"])

    def test_empty_runtime_identity_cannot_project_online(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            path = root / "telemetry" / "auth-session.json"
            doc = json.loads(path.read_text(encoding="utf-8"))
            doc["source_states"]["runtime_identity"] = {
                "state": "AVAILABLE", "evidence_level": "PROVEN",
                "value": {}, "source": "surveyor.runtime",
            }
            path.write_text(json.dumps(doc, sort_keys=True) + "\n", encoding="utf-8")
            rewrite_manifest(root)
            assert_validation_code(
                self,
                "SURVEYOR_PROVENANCE_MISMATCH",
                lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
            )

    def test_live_shaped_bundle_maps_identity_but_not_semantic_position_or_authority(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            make_live_shaped_bundle(root)
            model = module.load_surveyor_bundle(
                root,
                producer_commit=PRODUCER_COMMIT,
                ingested_monotonic_ns=456,
            )
        self.assertEqual("ONLINE", model.runtime_status.runtime_state)
        self.assertEqual("UNKNOWN", model.runtime_status.client_state)
        self.assertEqual("READ_ONLY", model.runtime_status.authority_state)
        self.assertEqual("track-a-canonical-live", model.runtime_status.runtime_instance_id)
        self.assertIsNone(model.runtime_status.session_epoch)
        self.assertEqual({"x": None, "y": None, "z": None}, model.snapshot.player["position"])
        candidate = model.snapshot.source_quality["candidate_fields"]["player.position"]
        self.assertEqual({"x": 32547, "y": 32506, "z": 7}, candidate["value"])
        self.assertFalse(candidate["semantic_promotion_allowed"])
        player_capability = next(c for c in model.capabilities if c.capability_id == "surveyor.player-state")
        self.assertTrue(player_capability.read_supported)
        self.assertFalse(player_capability.action_supported)

    def test_admitted_runtime_display_must_match_producer_contract(self):
        module = self.provider()
        for display in (None, "1", ":1.0", " :1", {"display": ":1"}):
            with self.subTest(display=display), tempfile.TemporaryDirectory() as raw:
                root = Path(raw) / "survey"
                make_live_shaped_bundle(root)
                agent = load_json(root, "surveyor/agent_bundle.json")
                agent["runtime"]["display"] = display
                agent["runtime"]["canonical_control"]["registration"]["display"] = display
                write_json(root, "surveyor/agent_bundle.json", agent)
                write_json(root, "surveyor/runtime.json", agent["runtime"])
                collect_all = build_collect_all(agent, load_json(root, "surveyor/coverage.json")["rows"])
                write_collect_all(root, collect_all)
                assert_validation_code(
                    self, "SURVEYOR_PROVENANCE_MISMATCH",
                    lambda root=root: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
                )

    def test_available_readers_require_complete_producer_evidence_envelopes(self):
        module = self.provider()
        payloads = {
            "player_state_typed_reader": {
                "state": "AVAILABLE", "reader_id": "player_state_typed_reader",
                "position": {"x": 32547, "y": 32506, "z": 7}, "object_count": 1,
                "position_mirror_consistent": True, "process_memory_access": "read_only",
                "semantic_state": "CANDIDATE_PENDING_CAUSAL_E2E", "layout_evidence": PLAYER_LAYOUT,
                "semantic_promotion_allowed": False,
            },
            "action_protocol_typed_reader": {
                "state": "AVAILABLE", "reader_id": "action_protocol_typed_reader",
                "type_name": "tibia::game::TPlayerProtocolMessageHandler", "object_count": 1,
                "typed_object_identity": "PROVEN", "process_memory_access": "read_only",
                "layout_evidence": ACTION_LAYOUT,
                "semantic_state": "TYPED_ACTION_PROTOCOL_OBJECT_IDENTITY_ONLY", "protocol_message_handler_present": True,
                "action_to_protocol_connection_claimed": False, "serialized_message_semantics_claimed": False,
                "protocol_opcodes_claimed": False, "packet_payloads_retained": False, "in_game_claimed": False,
                "credentials_retained": False, "session_secrets_retained": False, "semantic_promotion_allowed": False,
            },
            "auth_session_typed_reader": {
                "state": "AVAILABLE", "reader_id": "auth_session_typed_reader", "game_client_object_count": 1,
                "authentication_process_object_count": 1, "authentication_state_machine_running": True,
                "process_memory_access": "read_only", "semantic_state": "TYPED_AUTH_LIFECYCLE_ONLY",
                "in_game_claimed": False, "credentials_retained": False, "session_secrets_retained": False,
                "layout_evidence": AUTH_LAYOUT, "qt_state_machine_fence": {"library": "libQt6StateMachine.so.6", "size": 394824, "sha256": "26f504ae723fa15c77e0c33a93a964a305c63577f2bed3f136c098b7b06921e8"},
                "semantic_promotion_allowed": False,
            },
            "ui_settings_typed_reader": {
                "state": "AVAILABLE", "reader_id": "ui_settings_typed_reader", "master_volume": 80,
                "master_volume_old": 70, "persistence_relative_path": "conf/clientoptions.json",
                "filesystem_access": "read_only", "process_memory_access": "not_used",
                "semantic_state": "TYPED_UI_SETTINGS_MASTER_VOLUME_FILE_READ_ONLY", "settings_model_type": "tibia::config::TClientOptions",
                "settings_model_type_present": True, "persistence_fields": ["options.soundMasterVolume", "options.soundMasterVolumeOld"],
                "master_volume_persistence_field_semantics": "PROVEN_ON_EXACT_BUILD_BY_PRIOR_REVERSIBLE_CAUSAL_EVIDENCE",
                "live_ui_application_state_claimed": False, "all_settings_model_claimed": False,
                "qsettings_linkage_claimed": False, "client_options_to_file_linkage_claimed": False,
                "credentials_retained": False, "session_secrets_retained": False, "semantic_promotion_allowed": False,
                "static_evidence": {"state": "AVAILABLE", "type_name": "tibia::config::TClientOptions", "type_string_count": 1, "clientoptions_literal_count": 1},
            },
        }
        telemetry_paths = {
            "player_state_typed_reader": "telemetry/player-state.json", "action_protocol_typed_reader": "telemetry/action-protocol.json",
            "auth_session_typed_reader": "telemetry/auth-session.json", "ui_settings_typed_reader": "telemetry/ui-settings.json",
        }
        evidence_keys = {
            "player_state_typed_reader": "layout_evidence",
            "action_protocol_typed_reader": "layout_evidence",
            "auth_session_typed_reader": "qt_state_machine_fence",
            "ui_settings_typed_reader": "static_evidence",
        }
        for reader_id, complete in payloads.items():
            for removed_key in (None, evidence_keys[reader_id]):
                with self.subTest(reader_id=reader_id, removed_key=removed_key), tempfile.TemporaryDirectory() as raw:
                    root = Path(raw) / "survey"
                    make_live_shaped_bundle(root)
                    value = json.loads(json.dumps(complete))
                    if removed_key is not None:
                        del value[removed_key]
                    agent = load_json(root, "surveyor/agent_bundle.json")
                    agent["typed_readers"][reader_id] = value
                    write_json(root, "surveyor/agent_bundle.json", agent)
                    telemetry = load_json(root, telemetry_paths[reader_id])
                    telemetry["source_states"]["subsystem_typed_reader"] = {
                        "state": "AVAILABLE", "evidence_level": "PROVEN", "source": reader_id,
                        "value": value, "reason": None,
                    }
                    write_json(root, telemetry_paths[reader_id], telemetry)
                    rewrite_manifest(root)
                    if removed_key is None:
                        model = module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT)
                        capability_id = telemetry_paths[reader_id].removeprefix("telemetry/").removesuffix(".json")
                        capability = next(item for item in model.capabilities if item.capability_id == f"surveyor.{capability_id}")
                        self.assertTrue(capability.read_supported)
                    else:
                        assert_validation_code(self, "SURVEYOR_PROVENANCE_MISMATCH", lambda root=root: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))


    def test_action_protocol_layout_offsets_are_exactly_pinned(self):
        module = self.provider()
        for field, bad_value in (("vptr_offset", "0x1"), ("typeinfo_offset", "0x2")):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as raw:
                root = Path(raw) / "survey"
                make_live_shaped_bundle(root)
                value = {
                    "state": "AVAILABLE", "reader_id": "action_protocol_typed_reader",
                    "type_name": "tibia::game::TPlayerProtocolMessageHandler", "object_count": 1,
                    "typed_object_identity": "PROVEN", "process_memory_access": "read_only",
                    "layout_evidence": json.loads(json.dumps(ACTION_LAYOUT)),
                    "semantic_state": "TYPED_ACTION_PROTOCOL_OBJECT_IDENTITY_ONLY", "protocol_message_handler_present": True,
                    "action_to_protocol_connection_claimed": False, "serialized_message_semantics_claimed": False,
                    "protocol_opcodes_claimed": False, "packet_payloads_retained": False, "in_game_claimed": False,
                    "credentials_retained": False, "session_secrets_retained": False, "semantic_promotion_allowed": False,
                }
                value["layout_evidence"][field] = bad_value
                agent = load_json(root, "surveyor/agent_bundle.json")
                agent["typed_readers"]["action_protocol_typed_reader"] = value
                write_json(root, "surveyor/agent_bundle.json", agent)
                telemetry = load_json(root, "telemetry/action-protocol.json")
                telemetry["source_states"]["subsystem_typed_reader"] = {
                    "state": "AVAILABLE", "evidence_level": "PROVEN",
                    "source": "action_protocol_typed_reader", "value": value, "reason": None,
                }
                write_json(root, "telemetry/action-protocol.json", telemetry)
                rewrite_manifest(root)
                assert_validation_code(
                    self, "SURVEYOR_PROVENANCE_MISMATCH",
                    lambda root=root: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
                )


    def test_admitted_runtime_requires_complete_visible_window_evidence(self):
        module = self.provider()
        malformed = (
            {"pid": 123},
            {"xid": 0, "pid": 123, "title_class": "CHARACTER_CONTEXT"},
            {"xid": True, "pid": 123, "title_class": "CHARACTER_CONTEXT"},
            {"xid": 321, "pid": 123, "title_class": "OTHER"},
        )
        for window in malformed:
            with self.subTest(window=window), tempfile.TemporaryDirectory() as raw:
                root = Path(raw) / "survey"
                make_live_shaped_bundle(root)
                agent = load_json(root, "surveyor/agent_bundle.json")
                agent["runtime"]["visible_tibia_windows"] = [window]
                write_json(root, "surveyor/agent_bundle.json", agent)
                write_json(root, "surveyor/runtime.json", agent["runtime"])
                collect_all = build_collect_all(agent, load_json(root, "surveyor/coverage.json")["rows"])
                write_collect_all(root, collect_all)
                assert_validation_code(
                    self, "SURVEYOR_PROVENANCE_MISMATCH",
                    lambda root=root: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
                )

    def test_admitted_runtime_rejects_non_finite_lease_expiry(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            make_live_shaped_bundle(root)
            for relative in ("surveyor/agent_bundle.json", "surveyor/runtime.json"):
                path = root / relative
                text = path.read_text(encoding="utf-8")
                old = '"expires_at": 9999999999'
                self.assertEqual(1, text.count(old), relative)
                path.write_text(text.replace(old, '"expires_at": 1e309'), encoding="utf-8")
            rewrite_manifest(root)
            assert_validation_code(
                self, "SURVEYOR_PROVENANCE_MISMATCH",
                lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
            )


    def test_admitted_runtime_rejects_non_finite_lease_history_timestamps(self):
        module = self.provider()
        for field, original in (("acquired_at", "0"), ("renewed_at", "1")):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as raw:
                root = Path(raw) / "survey"
                make_live_shaped_bundle(root)
                needle = f'"{field}": {original}'
                for relative in ("surveyor/agent_bundle.json", "surveyor/runtime.json"):
                    path = root / relative
                    text = path.read_text(encoding="utf-8")
                    self.assertEqual(1, text.count(needle), relative)
                    path.write_text(text.replace(needle, f'"{field}": 1e309'), encoding="utf-8")
                rewrite_manifest(root)
                assert_validation_code(
                    self, "SURVEYOR_PROVENANCE_MISMATCH",
                    lambda root=root: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
                )

    def test_admitted_runtime_uses_integer_lease_expiry_semantics(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            make_live_shaped_bundle(root)
            agent = load_json(root, "surveyor/agent_bundle.json")
            agent["runtime"]["canonical_control"]["lease"]["expires_at"] = 1.5
            write_json(root, "surveyor/agent_bundle.json", agent)
            write_json(root, "surveyor/runtime.json", agent["runtime"])
            collect_all = build_collect_all(agent, load_json(root, "surveyor/coverage.json")["rows"])
            write_collect_all(root, collect_all)
            assert_validation_code(
                self, "SURVEYOR_PROVENANCE_MISMATCH",
                lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
            )


    def test_markdown_payloads_are_independently_privacy_scanned(self):
        module = self.provider()
        for relative in ("summary.md", "surveyor/summary.md"):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as raw:
                root = Path(raw) / "survey"
                build_repo_bundle(root)
                path = root / relative
                path.write_text(path.read_text(encoding="utf-8") + "\nBearer super-secret-value\n", encoding="utf-8")
                rewrite_manifest(root)
                assert_validation_code(
                    self, "SURVEYOR_PRIVACY_RISK",
                    lambda root=root: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
                )

    def test_non_admitted_runtime_identity_is_suppressed_from_provenance(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            make_live_shaped_bundle(root)
            agent = load_json(root, "surveyor/agent_bundle.json")
            runtime = agent["runtime"]
            runtime["runtime_access"] = "READ_ONLY_NOT_ADMITTED"
            runtime["processes"][0]["pid"] = "fabricated-pid"
            runtime["canonical_control"]["registration"]["runtime_id"] = "fabricated-runtime"
            runtime["canonical_control"]["lease"]["runtime_id"] = "fabricated-runtime"
            agent["typed_readers"] = {}
            write_json(root, "surveyor/agent_bundle.json", agent)
            write_json(root, "surveyor/runtime.json", runtime)
            collect_all = build_collect_all(agent, load_json(root, "surveyor/coverage.json")["rows"])
            write_collect_all(root, collect_all)
            model = module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT)
            self.assertEqual("UNKNOWN", model.runtime_status.runtime_state)
            self.assertIsNone(model.runtime_status.runtime_instance_id)
            self.assertEqual("UNKNOWN", model.provenance["runtime_identity"]["state"])
            self.assertEqual("UNKNOWN", model.provenance["runtime_identity"]["evidence_level"])
            self.assertIsNone(model.provenance["runtime_identity"]["value"] )

    def test_non_admitted_runtime_rejects_non_collection_visible_windows(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            make_live_shaped_bundle(root)
            agent = load_json(root, "surveyor/agent_bundle.json")
            runtime = agent["runtime"]
            runtime["runtime_access"] = "READ_ONLY_NOT_ADMITTED"
            runtime["visible_tibia_windows"] = 1
            agent["typed_readers"] = {}
            write_json(root, "surveyor/agent_bundle.json", agent)
            write_json(root, "surveyor/runtime.json", runtime)
            rewrite_manifest(root)
            assert_validation_code(
                self, "SURVEYOR_PROVENANCE_MISMATCH",
                lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
            )

    def test_unknown_runtime_access_value_fails_closed(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            make_live_shaped_bundle(root)
            agent = load_json(root, "surveyor/agent_bundle.json")
            agent["runtime"]["runtime_access"] = "FABRICATED_ACCESS"
            agent["typed_readers"] = {}
            write_json(root, "surveyor/agent_bundle.json", agent)
            write_json(root, "surveyor/runtime.json", agent["runtime"])
            collect_all = build_collect_all(agent, load_json(root, "surveyor/coverage.json")["rows"])
            write_collect_all(root, collect_all)
            assert_validation_code(
                self, "SURVEYOR_PROVENANCE_MISMATCH",
                lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
            )


    def test_decoded_string_sensitive_json_fragment_fails_closed(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            agent = load_json(root, "surveyor/agent_bundle.json")
            agent["generated_at"] = '"password": "super-secret-value"'
            write_json(root, "surveyor/agent_bundle.json", agent)
            collect_all = build_collect_all(agent, load_json(root, "surveyor/coverage.json")["rows"])
            write_collect_all(root, collect_all)
            assert_validation_code(
                self, "SURVEYOR_PRIVACY_RISK",
                lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
            )

    def test_admitted_runtime_requires_true_control_presence_flags(self):
        module = self.provider()
        for field in ("registration_present", "lease_present"):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as raw:
                root = Path(raw) / "survey"
                make_live_shaped_bundle(root)
                agent = load_json(root, "surveyor/agent_bundle.json")
                agent["runtime"]["canonical_control"][field] = False
                write_json(root, "surveyor/agent_bundle.json", agent)
                write_json(root, "surveyor/runtime.json", agent["runtime"])
                collect_all = build_collect_all(agent, load_json(root, "surveyor/coverage.json")["rows"])
                write_collect_all(root, collect_all)
                assert_validation_code(
                    self, "SURVEYOR_PROVENANCE_MISMATCH",
                    lambda root=root: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
                )

    def test_manifest_digest_mismatch_fails_closed(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            doc = load_json(root, "aliases/TIBIA-RE-PLAYER-STATE.json")
            doc["alias"] = "tampered"
            write_json(root, "aliases/TIBIA-RE-PLAYER-STATE.json", doc)
            assert_validation_code(
                self,
                "SURVEYOR_MANIFEST_DIGEST_MISMATCH",
                lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
            )

    def test_schema_upgrade_or_downgrade_is_incompatible_even_with_valid_manifest(self):
        module = self.provider()
        for schema in ("otclient.tibia-re-surveyor.alias-view.v1", "otclient.tibia-re-surveyor.alias-view.v3"):
            with self.subTest(schema=schema), tempfile.TemporaryDirectory() as raw:
                root = Path(raw) / "survey"
                build_repo_bundle(root)
                doc = load_json(root, "aliases/TIBIA-RE-PLAYER-STATE.json")
                doc["schema"] = schema
                write_json(root, "aliases/TIBIA-RE-PLAYER-STATE.json", doc)
                rewrite_manifest(root)
                assert_validation_code(self, "SURVEYOR_SCHEMA_INCOMPATIBLE", lambda root=root: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_duplicate_and_unsafe_manifest_paths_fail_closed(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            line = (root / "manifest.sha256").read_text(encoding="utf-8").splitlines()[0]
            (root / "manifest.sha256").write_text(line + "\n" + line + "\n", encoding="utf-8")
            assert_validation_code(self, "SURVEYOR_MANIFEST_DUPLICATE_PATH", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            digest = "0" * 64
            (root / "manifest.sha256").write_text(f"{digest}  ../escape.json\n", encoding="utf-8")
            assert_validation_code(self, "SURVEYOR_MANIFEST_UNSAFE_PATH", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_missing_or_extra_files_fail_closed(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            (root / "aliases" / "TIBIA-RE-PLAYER-STATE.json").unlink()
            assert_validation_code(self, "SURVEYOR_MANIFEST_MISSING_FILE", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            (root / "unexpected.json").write_text('{"safe":true}\n', encoding="utf-8")
            assert_validation_code(
                self,
                "SURVEYOR_MANIFEST_FILE_SET_MISMATCH",
                lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
            )

    def test_privacy_risk_is_rejected_without_leaking_secret(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            path = root / "telemetry" / "player-state.json"
            doc = json.loads(path.read_text(encoding="utf-8"))
            doc["password"] = "do-not-leak-this-secret"
            path.write_text(json.dumps(doc, sort_keys=True) + "\n", encoding="utf-8")
            rewrite_manifest(root)
            with self.assertRaises(ValidationError) as caught:
                module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT)
            self.assertEqual("SURVEYOR_PRIVACY_RISK", caught.exception.code)
            self.assertNotIn("do-not-leak-this-secret", str(caught.exception))

    def test_bundle_validation_does_not_materialize_recursive_tree(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            with patch.object(Path, "rglob", side_effect=AssertionError("unbounded recursive traversal")):
                module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT)
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            extra = root / "unexpected" / "nested"
            extra.mkdir(parents=True)
            (extra / "payload.json").write_text("{}\n", encoding="utf-8")
            assert_validation_code(
                self,
                "SURVEYOR_MANIFEST_FILE_SET_MISMATCH",
                lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
            )

    def test_sensitive_values_are_rejected_even_under_innocent_keys(self):
        module = self.provider()
        cases = (
            "Bearer super-secret-value",
            "eyJabcdefghijk.abcdefghijk.abcdefghijk",
            "owner@example.com",
        )
        for secret in cases:
            with self.subTest(secret_kind=secret.split(" ", 1)[0]), tempfile.TemporaryDirectory() as raw:
                root = Path(raw) / "survey"
                build_repo_bundle(root)
                path = root / "telemetry" / "auth-session.json"
                doc = json.loads(path.read_text(encoding="utf-8"))
                doc["harmless_note"] = secret
                path.write_text(json.dumps(doc, sort_keys=True) + "\n", encoding="utf-8")
                rewrite_manifest(root)
                with self.assertRaises(ValidationError) as caught:
                    module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT)
                self.assertEqual("SURVEYOR_PRIVACY_RISK", caught.exception.code)
                self.assertNotIn(secret, str(caught.exception))

    def test_all_producer_sensitive_keys_fail_closed(self):
        module = self.provider()
        for key in ("passwd", "otp", "2fa"):
            with self.subTest(key=key), tempfile.TemporaryDirectory() as raw:
                root = Path(raw) / "survey"
                build_repo_bundle(root)
                path = root / "telemetry" / "auth-session.json"
                doc = json.loads(path.read_text(encoding="utf-8"))
                doc[key] = "123456"
                path.write_text(json.dumps(doc, sort_keys=True) + "\n", encoding="utf-8")
                rewrite_manifest(root)
                assert_validation_code(
                    self,
                    "SURVEYOR_PRIVACY_RISK",
                    lambda root=root: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
                )

    def test_runtime_provenance_fields_must_match_agent_runtime(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            make_live_shaped_bundle(root)
            path = root / "telemetry" / "auth-session.json"
            doc = json.loads(path.read_text(encoding="utf-8"))
            doc["run_provenance"]["runtime_id"] = None
            path.write_text(json.dumps(doc, sort_keys=True) + "\n", encoding="utf-8")
            rewrite_manifest(root)
            assert_validation_code(
                self,
                "SURVEYOR_PROVENANCE_MISMATCH",
                lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
            )

    def test_registration_must_be_bound_to_current_lease_generation(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            make_live_shaped_bundle(root)
            agent = load_json(root, "surveyor/agent_bundle.json")
            agent["runtime"]["canonical_control"]["registration"]["lease_generation"] = 6
            write_json(root, "surveyor/agent_bundle.json", agent)
            rewrite_manifest(root)
            assert_validation_code(self, "SURVEYOR_PROVENANCE_MISMATCH", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_read_capability_requires_available_proven_reader(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            doc = load_json(root, "telemetry/player-state.json")
            doc["source_states"]["subsystem_typed_reader"] = {
                "state": "UNKNOWN", "evidence_level": "UNKNOWN",
                "source": "player_state_typed_reader",
            }
            write_json(root, "telemetry/player-state.json", doc)
            rewrite_manifest(root)
            assert_validation_code(
                self,
                "SURVEYOR_PROVENANCE_MISMATCH",
                lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
            )

    def test_runtime_json_must_match_agent_runtime(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            make_live_shaped_bundle(root)
            write_json(root, "surveyor/runtime.json", None)
            rewrite_manifest(root)
            assert_validation_code(self, "SURVEYOR_PROVENANCE_MISMATCH", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_runtime_identity_observation_must_match_agent_runtime(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            make_live_shaped_bundle(root)
            agent = load_json(root, "surveyor/agent_bundle.json")
            agent["runtime"]["runtime_access"] = "READ_ONLY_NOT_ADMITTED"
            write_json(root, "surveyor/agent_bundle.json", agent)
            write_json(root, "surveyor/runtime.json", agent["runtime"])
            rewrite_manifest(root)
            assert_validation_code(self, "SURVEYOR_PROVENANCE_MISMATCH", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_available_typed_reader_must_match_agent_bundle(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            make_live_shaped_bundle(root)
            doc = load_json(root, "telemetry/player-state.json")
            doc["source_states"]["subsystem_typed_reader"]["value"]["position"]["x"] += 1
            write_json(root, "telemetry/player-state.json", doc)
            rewrite_manifest(root)
            assert_validation_code(self, "SURVEYOR_PROVENANCE_MISMATCH", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_released_lease_cannot_project_online(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            make_live_shaped_bundle(root)
            agent = load_json(root, "surveyor/agent_bundle.json")
            agent["runtime"]["canonical_control"]["lease"]["status"] = "released"
            write_json(root, "surveyor/agent_bundle.json", agent)
            write_json(root, "surveyor/runtime.json", agent["runtime"])
            collect_all = build_collect_all(agent, load_json(root, "surveyor/coverage.json")["rows"])
            write_collect_all(root, collect_all)
            assert_validation_code(
                self,
                "SURVEYOR_PROVENANCE_MISMATCH",
                lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
            )

    def test_telemetry_cannot_select_another_alias_reader(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            make_live_shaped_bundle(root)
            player = load_json(root, "telemetry/player-state.json")
            inventory = load_json(root, "telemetry/inventory-containers.json")
            inventory["source_states"]["subsystem_typed_reader"] = player["source_states"]["subsystem_typed_reader"]
            write_json(root, "telemetry/inventory-containers.json", inventory)
            alias = load_json(root, "aliases/TIBIA-RE-INVENTORY-CONTAINERS.json")
            alias["missing_reader"] = None
            write_json(root, "aliases/TIBIA-RE-INVENTORY-CONTAINERS.json", alias)
            rewrite_manifest(root)
            assert_validation_code(self, "SURVEYOR_INTERFACE_INCOMPATIBLE", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_semantic_promotion_must_remain_exactly_false(self):
        module = self.provider()
        for promoted in (True, "false"):
            with self.subTest(promoted=promoted), tempfile.TemporaryDirectory() as raw:
                root = Path(raw) / "survey"
                make_live_shaped_bundle(root)
                agent = load_json(root, "surveyor/agent_bundle.json")
                agent["typed_readers"]["player_state_typed_reader"]["semantic_promotion_allowed"] = promoted
                write_json(root, "surveyor/agent_bundle.json", agent)
                telemetry = load_json(root, "telemetry/player-state.json")
                telemetry["source_states"]["subsystem_typed_reader"]["value"]["semantic_promotion_allowed"] = promoted
                write_json(root, "telemetry/player-state.json", telemetry)
                rewrite_manifest(root)
                assert_validation_code(self, "SURVEYOR_PROVENANCE_MISMATCH", lambda root=root: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_registration_and_lease_runtime_ids_must_match(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            make_live_shaped_bundle(root)
            agent = load_json(root, "surveyor/agent_bundle.json")
            agent["runtime"]["canonical_control"]["lease"]["runtime_id"] = "other-runtime"
            write_json(root, "surveyor/agent_bundle.json", agent)
            write_json(root, "surveyor/runtime.json", agent["runtime"])
            rewrite_manifest(root)
            assert_validation_code(self, "SURVEYOR_PROVENANCE_MISMATCH", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_runtime_online_requires_full_admission_evidence(self):
        module = self.provider()
        mutations = (
            ("target_running", lambda runtime: runtime.__setitem__("target_running", False)),
            ("namespace", lambda runtime: runtime.__setitem__("runtime_namespace_scope", "OTHER")),
            ("external_scan", lambda runtime: runtime.__setitem__("external_containers_scanned", True)),
            ("uniqueness_scope", lambda runtime: runtime.__setitem__("target_uniqueness_scope", "OTHER")),
            ("fence_match", lambda runtime: runtime["exact_current_fence"].__setitem__("match", False)),
            ("process_fence", lambda runtime: runtime["processes"][0].__setitem__("exact_fence_match", False)),
            ("fence_sha", lambda runtime: runtime["exact_current_fence"].__setitem__("sha256", "0" * 64)),
            ("fence_size", lambda runtime: runtime["exact_current_fence"].__setitem__("size", 1)),
            ("pid", lambda runtime: runtime["processes"][0].__setitem__("pid", None)),
            ("start_ticks", lambda runtime: runtime["processes"][0].__setitem__("process_start_ticks", None)),
        )
        for label, mutate in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as raw:
                root = Path(raw) / "survey"
                make_live_shaped_bundle(root)
                agent = load_json(root, "surveyor/agent_bundle.json")
                mutate(agent["runtime"])
                write_json(root, "surveyor/agent_bundle.json", agent)
                write_json(root, "surveyor/runtime.json", agent["runtime"])
                collect_all = build_collect_all(agent, load_json(root, "surveyor/coverage.json")["rows"])
                write_collect_all(root, collect_all)
                assert_validation_code(
                    self,
                    "SURVEYOR_PROVENANCE_MISMATCH",
                    lambda root=root: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
                )

    def test_runtime_fence_must_match_pinned_executable(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            make_live_shaped_bundle(root)
            agent = load_json(root, "surveyor/agent_bundle.json")
            runtime = agent["runtime"]
            runtime["processes"][0]["client_size"] = 1
            runtime["processes"][0]["client_sha256"] = "0" * 64
            runtime["exact_current_fence"].update({"version": "99.99", "size": 1, "sha256": "0" * 64, "match": True})
            registration = runtime["canonical_control"]["registration"]
            registration.update({"client_version": "99.99", "client_size": 1, "client_sha256": "0" * 64})
            write_json(root, "surveyor/agent_bundle.json", agent)
            write_json(root, "surveyor/runtime.json", runtime)
            collect_all = build_collect_all(agent, load_json(root, "surveyor/coverage.json")["rows"])
            write_collect_all(root, collect_all)
            assert_validation_code(self, "SURVEYOR_PROVENANCE_MISMATCH", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_registration_must_match_observed_process_identity(self):
        module = self.provider()
        mutations = (
            ("pid", lambda registration: registration.__setitem__("pid", 999)),
            ("start_ticks", lambda registration: registration.__setitem__("process_start_ticks", 999)),
            ("version", lambda registration: registration.__setitem__("client_version", "99.99")),
            ("size", lambda registration: registration.__setitem__("client_size", 1)),
            ("sha", lambda registration: registration.__setitem__("client_sha256", "0" * 64)),
            ("display", lambda registration: registration.__setitem__("display", ":9")),
            ("boot_id", lambda registration: registration.__setitem__("boot_id_sha256", None)),
        )
        for label, mutate in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as raw:
                root = Path(raw) / "survey"
                make_live_shaped_bundle(root)
                agent = load_json(root, "surveyor/agent_bundle.json")
                mutate(agent["runtime"]["canonical_control"]["registration"])
                write_json(root, "surveyor/agent_bundle.json", agent)
                write_json(root, "surveyor/runtime.json", agent["runtime"])
                collect_all = build_collect_all(agent, load_json(root, "surveyor/coverage.json")["rows"])
                write_collect_all(root, collect_all)
                assert_validation_code(self, "SURVEYOR_PROVENANCE_MISMATCH", lambda root=root: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_active_lease_must_be_unexpired_from_its_timestamps(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            make_live_shaped_bundle(root)
            agent = load_json(root, "surveyor/agent_bundle.json")
            agent["runtime"]["canonical_control"]["lease"]["expires_at"] = 0
            agent["runtime"]["canonical_control"]["lease_expired"] = False
            write_json(root, "surveyor/agent_bundle.json", agent)
            write_json(root, "surveyor/runtime.json", agent["runtime"])
            collect_all = build_collect_all(agent, load_json(root, "surveyor/coverage.json")["rows"])
            write_collect_all(root, collect_all)
            assert_validation_code(self, "SURVEYOR_PROVENANCE_MISMATCH", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_canonical_runtime_id_is_exactly_pinned(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            make_live_shaped_bundle(root)
            agent = load_json(root, "surveyor/agent_bundle.json")
            agent["runtime"]["canonical_control"]["registration"]["runtime_id"] = "other"
            agent["runtime"]["canonical_control"]["lease"]["runtime_id"] = "other"
            write_json(root, "surveyor/agent_bundle.json", agent)
            write_json(root, "surveyor/runtime.json", agent["runtime"])
            collect_all = build_collect_all(agent, load_json(root, "surveyor/coverage.json")["rows"])
            write_collect_all(root, collect_all)
            assert_validation_code(self, "SURVEYOR_PROVENANCE_MISMATCH", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_process_and_generation_identity_reject_boolean_integers(self):
        module = self.provider()
        mutations = (
            ("pid", lambda runtime: (runtime["processes"][0].__setitem__("pid", True), runtime["canonical_control"]["registration"].__setitem__("pid", True), runtime["visible_tibia_windows"][0].__setitem__("pid", True))),
            ("start_ticks", lambda runtime: (runtime["processes"][0].__setitem__("process_start_ticks", True), runtime["canonical_control"]["registration"].__setitem__("process_start_ticks", True))),
            ("registration_generation", lambda runtime: runtime["canonical_control"]["registration"].__setitem__("registration_generation", True)),
            ("lease_generation", lambda runtime: (runtime["canonical_control"]["lease"].__setitem__("generation", True), runtime["canonical_control"]["registration"].__setitem__("lease_generation", True))),
            ("process_count", lambda runtime: runtime.__setitem__("target_process_count", True)),
        )
        for label, mutate in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as raw:
                root = Path(raw) / "survey"
                make_live_shaped_bundle(root)
                agent = load_json(root, "surveyor/agent_bundle.json")
                mutate(agent["runtime"])
                write_json(root, "surveyor/agent_bundle.json", agent)
                write_json(root, "surveyor/runtime.json", agent["runtime"])
                collect_all = build_collect_all(agent, load_json(root, "surveyor/coverage.json")["rows"])
                write_collect_all(root, collect_all)
                assert_validation_code(self, "SURVEYOR_PROVENANCE_MISMATCH", lambda root=root: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_typed_reader_set_is_bound_to_runtime_admission(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            make_live_shaped_bundle(root)
            agent = load_json(root, "surveyor/agent_bundle.json")
            agent["runtime"]["runtime_access"] = "READ_ONLY_NOT_ADMITTED"
            write_json(root, "surveyor/agent_bundle.json", agent)
            write_json(root, "surveyor/runtime.json", agent["runtime"])
            collect_all = build_collect_all(agent, load_json(root, "surveyor/coverage.json")["rows"])
            write_collect_all(root, collect_all)
            assert_validation_code(self, "SURVEYOR_PROVENANCE_MISMATCH", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            make_live_shaped_bundle(root)
            agent = load_json(root, "surveyor/agent_bundle.json")
            del agent["typed_readers"]["player_state_typed_reader"]
            write_json(root, "surveyor/agent_bundle.json", agent)
            collect_all = build_collect_all(agent, load_json(root, "surveyor/coverage.json")["rows"])
            write_collect_all(root, collect_all)
            assert_validation_code(self, "SURVEYOR_PROVENANCE_MISMATCH", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_producer_and_telemetry_guardrails_are_pinned(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            agent = load_json(root, "surveyor/agent_bundle.json")
            agent["guardrails"]["collect_all_runtime_mutation_allowed"] = True
            write_json(root, "surveyor/agent_bundle.json", agent)
            rewrite_manifest(root)
            assert_validation_code(self, "SURVEYOR_PROVENANCE_MISMATCH", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            telemetry = load_json(root, "telemetry/player-state.json")
            telemetry["guardrails"]["runtime_mutation_requested"] = True
            write_json(root, "telemetry/player-state.json", telemetry)
            rewrite_manifest(root)
            assert_validation_code(self, "SURVEYOR_PROVENANCE_MISMATCH", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_player_position_candidate_requires_exact_reader_shape(self):
        module = self.provider()
        for bad_value in (True, "32547", -1, 70000):
            with self.subTest(bad_value=bad_value), tempfile.TemporaryDirectory() as raw:
                root = Path(raw) / "survey"
                make_live_shaped_bundle(root)
                agent = load_json(root, "surveyor/agent_bundle.json")
                agent["typed_readers"]["player_state_typed_reader"]["position"]["x"] = bad_value
                write_json(root, "surveyor/agent_bundle.json", agent)
                telemetry = load_json(root, "telemetry/player-state.json")
                telemetry["source_states"]["subsystem_typed_reader"]["value"]["position"]["x"] = bad_value
                write_json(root, "telemetry/player-state.json", telemetry)
                rewrite_manifest(root)
                assert_validation_code(self, "SURVEYOR_PROVENANCE_MISMATCH", lambda root=root: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_nonstandard_json_constants_fail_closed(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            path = root / "telemetry" / "player-state.json"
            text = path.read_text(encoding="utf-8")
            text = text[:-2] + ',"nonstandard":NaN}\n'
            path.write_text(text, encoding="utf-8")
            rewrite_manifest(root)
            assert_validation_code(self, "SURVEYOR_JSON_INVALID", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_generated_at_must_match_producer_utc_isoformat(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            coverage = load_json(root, "surveyor/coverage.json")
            agent = load_json(root, "surveyor/agent_bundle.json")
            agent["generated_at"] = "not-a-timestamp"
            coverage["generated_at"] = agent["generated_at"]
            write_json(root, "surveyor/agent_bundle.json", agent)
            write_json(root, "surveyor/coverage.json", coverage)
            collect_all = build_collect_all(agent, coverage["rows"])
            write_collect_all(root, collect_all)
            assert_validation_code(
                self,
                "SURVEYOR_PROVENANCE_MISMATCH",
                lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
            )

    def test_generated_at_must_match_across_producer_documents(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            coverage = load_json(root, "surveyor/coverage.json")
            coverage["generated_at"] = "2000-01-01T00:00:00+00:00"
            write_json(root, "surveyor/coverage.json", coverage)
            rewrite_manifest(root)
            assert_validation_code(
                self,
                "SURVEYOR_PROVENANCE_MISMATCH",
                lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT),
            )

    def test_duplicate_json_keys_and_provenance_mismatch_fail_closed(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            privacy = root / "privacy-scan.json"
            privacy.write_text('{"schema":"otclient.tibia-re-surveyor.privacy-scan.v1","result":"PASS","result":"FAIL","findings":[]}\n', encoding="utf-8")
            rewrite_manifest(root)
            assert_validation_code(self, "SURVEYOR_JSON_DUPLICATE_KEY", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            path = root / "telemetry" / "player-state.json"
            doc = json.loads(path.read_text(encoding="utf-8"))
            doc["run_provenance"]["generated_at"] = "2000-01-01T00:00:00+00:00"
            path.write_text(json.dumps(doc, sort_keys=True) + "\n", encoding="utf-8")
            rewrite_manifest(root)
            assert_validation_code(self, "SURVEYOR_PROVENANCE_MISMATCH", lambda root=root: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_wrong_producer_pin_and_unbounded_manifest_fail_closed(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            assert_validation_code(self, "SURVEYOR_PRODUCER_INCOMPATIBLE", lambda: module.load_surveyor_bundle(root, producer_commit="0" * 40))
            (root / "manifest.sha256").write_text("x" * (64 * 1024 + 1), encoding="utf-8")
            assert_validation_code(self, "SURVEYOR_MANIFEST_TOO_LARGE", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_manifest_cannot_omit_or_add_interface_files(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            (root / "telemetry" / "player-state.json").unlink()
            rewrite_manifest(root)
            assert_validation_code(self, "SURVEYOR_INTERFACE_INCOMPATIBLE", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            (root / "extra.json").write_text('{"safe":true}\n', encoding="utf-8")
            rewrite_manifest(root)
            assert_validation_code(self, "SURVEYOR_INTERFACE_INCOMPATIBLE", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_symlinked_bundle_file_is_rejected(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            with patch("pathlib.Path.is_symlink", return_value=True):
                assert_validation_code(self, "SURVEYOR_MANIFEST_UNSAFE_PATH", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_payload_read_uses_stable_handle_not_second_path_lookup(self):
        module = self.provider()
        original_read_bytes = Path.read_bytes
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            target = root / "summary.md"
            raced_payload = b"x" * (module.MAX_FILE_BYTES + 1)

            def race_second_path_read(path):
                if path == target:
                    return raced_payload
                return original_read_bytes(path)

            with patch.object(Path, "read_bytes", race_second_path_read):
                model = module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT)
            self.assertEqual("surveyor", model.runtime_status.adapter_id)

    def test_size_bounds_are_checked_before_reading_untrusted_bytes(self):
        module = self.provider()
        original_read_bytes = Path.read_bytes
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            manifest = root / "manifest.sha256"
            manifest.write_bytes(b"x" * (module.MAX_MANIFEST_BYTES + 1))
            def guard_manifest(path):
                if path == manifest:
                    raise AssertionError("oversized manifest was read")
                return original_read_bytes(path)
            with patch.object(Path, "read_bytes", guard_manifest):
                assert_validation_code(self, "SURVEYOR_MANIFEST_TOO_LARGE", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            target = root / "telemetry" / "player-state.json"
            target.write_bytes(b"x" * (module.MAX_FILE_BYTES + 1))
            def guard_payload(path):
                if path == target:
                    raise AssertionError("oversized payload was read")
                return original_read_bytes(path)
            with patch.object(Path, "read_bytes", guard_payload):
                assert_validation_code(self, "SURVEYOR_FILE_TOO_LARGE", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))


    def test_bundle_root_swap_does_not_follow_replacement_symlink(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            root = base / "survey"
            replacement = base / "replacement"
            build_repo_bundle(root)
            build_repo_bundle(replacement)
            (replacement / "summary.md").write_text("Bearer super-secret-value\n", encoding="utf-8")
            rewrite_manifest(replacement)
            original_parse = module._parse_manifest
            swapped = False

            def swap_root_then_parse(path):
                nonlocal swapped
                if not swapped:
                    swapped = True
                    original = base / "original"
                    root.rename(original)
                    os.symlink(replacement, root, target_is_directory=True)
                return original_parse(path)

            with patch.object(module, "_parse_manifest", side_effect=swap_root_then_parse):
                try:
                    model = module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT)
                except ValidationError as exc:
                    self.assertEqual("SURVEYOR_MANIFEST_UNSAFE_PATH", exc.code)
                else:
                    self.assertEqual("surveyor", model.runtime_status.adapter_id)

    def test_deep_json_structure_fails_closed_without_recursion_error(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            agent_path = root / "surveyor" / "agent_bundle.json"
            text = agent_path.read_text(encoding="utf-8")
            deep = "[" * 600 + "0" + "]" * 600
            agent_path.write_text(text.replace("{", '{"deep":' + deep + ",", 1), encoding="utf-8")
            rewrite_manifest(root)
            assert_validation_code(self, "SURVEYOR_JSON_INVALID", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))

    def test_oversized_json_integer_fails_closed(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            privacy = root / "privacy-scan.json"
            text = privacy.read_text(encoding="utf-8")
            huge = "9" * 5000
            privacy.write_text(text.replace("{", '{"innocent_number":' + huge + ",", 1), encoding="utf-8")
            rewrite_manifest(root)
            assert_validation_code(self, "SURVEYOR_JSON_INVALID", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))


    @unittest.skipUnless(os.name == "posix" and hasattr(os, "mkfifo"), "POSIX FIFO semantics required")
    def test_fifo_manifest_and_fallback_open_fail_closed_without_blocking(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            manifest = root / "manifest.sha256"
            manifest.unlink()
            os.mkfifo(manifest)
            previous = signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError("blocking FIFO open")))
            signal.setitimer(signal.ITIMER_REAL, 1.0)
            try:
                assert_validation_code(self, "SURVEYOR_MANIFEST_UNSAFE_PATH", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))
            finally:
                signal.setitimer(signal.ITIMER_REAL, 0)
                signal.signal(signal.SIGALRM, previous)


    @unittest.skipUnless(os.name == "nt", "Windows junction semantics required")
    def test_windows_directory_junctions_fail_closed(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            real = base / "real"
            build_repo_bundle(real)
            root = base / "root-junction"
            subprocess.run(["cmd", "/c", "mklink", "/J", str(root), str(real)], check=True, capture_output=True)
            assert_validation_code(self, "SURVEYOR_MANIFEST_UNSAFE_PATH", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            root = base / "survey"
            replacement = base / "replacement"
            build_repo_bundle(root)
            build_repo_bundle(replacement)
            telemetry = root / "telemetry"
            for child in telemetry.iterdir():
                child.unlink()
            telemetry.rmdir()
            subprocess.run(["cmd", "/c", "mklink", "/J", str(telemetry), str(replacement / "telemetry")], check=True, capture_output=True)
            assert_validation_code(self, "SURVEYOR_MANIFEST_UNSAFE_PATH", lambda: module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT))


    @unittest.skipUnless(os.name == "nt", "Windows junction race semantics required")
    def test_windows_transient_parent_junction_cannot_redirect_handle_relative_leaf_open(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            root = base / "survey"
            replacement = base / "replacement"
            build_repo_bundle(root)
            build_repo_bundle(replacement)
            telemetry = root / "telemetry"
            saved = base / "telemetry-saved"
            external = replacement / "telemetry" / "player-state.json"
            external.write_text('{"redirected":true}\n', encoding="utf-8")
            native = module._WINDOWS_NATIVE
            self.assertIsNotNone(native)
            original_open = native.open_relative
            original_close = native.close
            attempted = False
            attacked_leaf = None
            restore_pending = False

            def racing_open(parent, name, *, directory):
                nonlocal attempted, attacked_leaf, restore_pending
                if name == "player-state.json" and not directory and not attempted:
                    attempted = True
                    telemetry.rename(saved)
                    subprocess.run(["cmd", "/c", "mklink", "/J", str(telemetry),
                                    str(replacement / "telemetry")], check=True, capture_output=True)
                    attacked_leaf = original_open(parent, name, directory=directory)
                    restore_pending = True
                    return attacked_leaf
                return original_open(parent, name, directory=directory)

            def racing_close(handle):
                nonlocal restore_pending
                original_close(handle)
                if restore_pending and handle == attacked_leaf:
                    subprocess.run(["cmd", "/c", "rmdir", str(telemetry)], check=True, capture_output=True)
                    saved.rename(telemetry)
                    restore_pending = False

            try:
                with patch.object(native, "open_relative", side_effect=racing_open), \
                     patch.object(native, "close", side_effect=racing_close):
                    model = module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT)
            finally:
                if telemetry.exists() and telemetry.is_junction():
                    subprocess.run(["cmd", "/c", "rmdir", str(telemetry)], check=True, capture_output=True)
                if saved.exists() and not telemetry.exists():
                    saved.rename(telemetry)
            self.assertEqual("surveyor", model.runtime_status.adapter_id)
            self.assertTrue(attempted)
            self.assertFalse(restore_pending)


    @unittest.skipUnless(os.name == "posix" and hasattr(os, "O_NONBLOCK"), "POSIX nonblocking open required")
    def test_posix_leaf_opens_include_nonblocking_flag(self):
        module = self.provider()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "survey"
            build_repo_bundle(root)
            real_open = module.os.open
            seen_flags = []

            def recording_open(path, flags, *args, **kwargs):
                seen_flags.append(flags)
                return real_open(path, flags, *args, **kwargs)

            with patch.object(module.os, "open", side_effect=recording_open):
                module.load_surveyor_bundle(root, producer_commit=PRODUCER_COMMIT)
            leaf_flags = [flags for flags in seen_flags if not (flags & module.os.O_DIRECTORY)]
            self.assertTrue(leaf_flags)
            self.assertTrue(all(flags & module.os.O_NONBLOCK for flags in leaf_flags))


if __name__ == "__main__":
    unittest.main()
