import argparse
import json
from pathlib import Path
import tempfile
import unittest

from tools.tibia_re_surveyor.collect_all import (
    ALIAS_ROWS,
    TELEMETRY_FILES,
    _safe_path,
    build_collect_all,
    scan_generated_privacy,
    write_collect_all,
)
from tools.tibia_re_surveyor.survey import build_bundle

ROOT = Path(__file__).resolve().parents[3]


class CollectAllModelTests(unittest.TestCase):
    def test_registry_contains_exactly_twelve_aliases_and_full_coordinator(self):
        self.assertEqual(12, len(ALIAS_ROWS))
        self.assertEqual(11, len(TELEMETRY_FILES))
        self.assertIn("TIBIA-RE-COORDINATOR", ALIAS_ROWS)
        self.assertEqual(169, len(ALIAS_ROWS["TIBIA-RE-COORDINATOR"]))
        self.assertEqual(169, len(set(ALIAS_ROWS["TIBIA-RE-COORDINATOR"])))

    def test_runtime_view_is_allowlisted_and_does_not_retain_raw_window_title(self):
        bundle = {
            "generated_at": "2026-08-20T07:00:00+00:00",
            "recommended_next": [],
            "runtime": {
                "observed_at_epoch": 1,
                "target_container": "target",
                "display": ":1",
                "target_running": True,
                "candidate_process_count": 1,
                "target_uniqueness": "PROVEN",
                "runtime_access": "READ_ONLY_ADMITTED",
                "visible_tibia_windows": [
                    {"pid": 123, "title": "Tibia - SecretCharacter", "title_class": "CHARACTER_CONTEXT"}
                ],
                "processes": [
                    {
                        "pid": 123,
                        "process_start_ticks": 456,
                        "exe_basename": "client",
                        "client_size": 100,
                        "client_sha256": "a" * 64,
                        "exact_fence_match": True,
                    }
                ],
                "exact_current_fence": {
                    "version": "15.32",
                    "size": 100,
                    "sha256": "a" * 64,
                    "match": True,
                },
                "canonical_control": {
                    "registration_present": True,
                    "registration": {
                        "runtime_id": "track-a-canonical-live",
                        "registration_generation": 7,
                        "state": "IN_GAME",
                    },
                    "lease_present": True,
                    "lease": {"generation": 8, "status": "active"},
                    "lease_expired": False,
                },
            },
        }
        result = build_collect_all(bundle, [])
        serialized = json.dumps(result, sort_keys=True)
        self.assertNotIn("SecretCharacter", serialized)
        auth = result["telemetry"]["auth-session.json"]
        runtime = auth["source_states"]["runtime_identity"]
        self.assertEqual("AVAILABLE", runtime["state"])
        self.assertFalse(runtime["value"]["window_title_values_retained"])
        self.assertEqual(123, runtime["value"]["process"]["pid"])

    def test_missing_reader_ranking_uses_canonical_priority(self):
        coverage = [
            {
                "row_id": "A15",
                "title": "Restart/relogin stability",
                "canonical_status": "BLOCKED",
                "evidence_index": {"mention_count": 1, "current_sha_match_count": 1},
            },
            {
                "row_id": "C10",
                "title": "Authoritative local-player XYZ",
                "canonical_status": "BLOCKED",
                "evidence_index": {"mention_count": 1, "current_sha_match_count": 0},
            },
            {
                "row_id": "G24",
                "title": "Economy panel",
                "canonical_status": "PARTIAL",
                "evidence_index": {"mention_count": 0, "current_sha_match_count": 0},
            },
        ]
        bundle = {
            "generated_at": "2026-08-20T07:00:00+00:00",
            "runtime": None,
            "recommended_next": [
                {"row_id": "C10", "priority_score": 125},
                {"row_id": "A15", "priority_score": 125},
                {"row_id": "G24", "priority_score": 40},
            ],
        }
        result = build_collect_all(bundle, coverage)
        gaps = result["missing_readers"]["reader_gaps"]
        self.assertEqual(11, len(gaps))
        self.assertEqual("TIBIA-RE-AUTH-SESSION", gaps[0]["alias"])
        self.assertEqual(125, gaps[0]["canonical_priority_score"])
        self.assertEqual("TIBIA-RE-PLAYER-STATE", gaps[1]["alias"])
        self.assertEqual(125, gaps[1]["canonical_priority_score"])
        self.assertEqual(1, gaps[0]["rank"])
        self.assertFalse(gaps[0]["semantic_promotion_allowed"])

    def test_safe_output_path_rejects_escape(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            with self.assertRaises(ValueError):
                _safe_path(root, "../escape.json")
            with self.assertRaises(ValueError):
                _safe_path(root, "/absolute.json")


class CollectAllOutputTests(unittest.TestCase):
    def test_write_collect_all_emits_manifest_and_privacy_pass(self):
        coverage = [
            {
                "row_id": "A15",
                "title": "Restart/relogin stability",
                "canonical_status": "BLOCKED",
                "evidence_index": {"mention_count": 0, "current_sha_match_count": 0},
            }
        ]
        bundle = {
            "generated_at": "2026-08-20T07:00:00+00:00",
            "runtime": None,
            "recommended_next": [{"row_id": "A15", "priority_score": 125}],
        }
        result = build_collect_all(bundle, coverage)
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            write_collect_all(root, result)
            self.assertTrue((root / "missing-readers.json").is_file())
            self.assertTrue((root / "privacy-scan.json").is_file())
            self.assertTrue((root / "manifest.sha256").is_file())
            self.assertEqual(12, len(list((root / "aliases").glob("*.json"))))
            self.assertEqual(11, len(list((root / "telemetry").glob("*.json"))))
            privacy = json.loads((root / "privacy-scan.json").read_text(encoding="utf-8"))
            self.assertEqual("PASS", privacy["result"])
            manifest = (root / "manifest.sha256").read_text(encoding="utf-8").splitlines()
            paths = [line.split("  ", 1)[1] for line in manifest]
            self.assertEqual(sorted(paths), paths)
            self.assertNotIn("manifest.sha256", paths)

    def test_privacy_scan_finds_secret_like_values(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "bad.json").write_text(
                '{"password":"should-not-survive","safe":false}\n', encoding="utf-8"
            )
            result = scan_generated_privacy(root)
            self.assertEqual("FAIL", result["result"])
            self.assertEqual("sensitive_json_value", result["findings"][0]["kind"])

    def test_real_repository_collect_all_build_is_complete_without_runtime(self):
        with tempfile.TemporaryDirectory() as raw:
            output = Path(raw) / "survey"
            args = argparse.Namespace(
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
            bundle = build_bundle(args)
            self.assertEqual(169, sum(bundle["coverage_counts"].values()))
            self.assertEqual(12, bundle["collect_all"]["alias_count"])
            self.assertEqual(11, bundle["collect_all"]["missing_reader_count"])
            self.assertEqual("NO_EXACT_CURRENT_PROFILE", bundle["bridge_profile"]["state"])
            self.assertEqual(0, bundle["bridge_profile"]["exact_current_profile_count"])
            self.assertTrue((output / "surveyor" / "coverage.json").is_file())
            self.assertTrue((output / "surveyor" / "runtime.json").is_file())
            self.assertTrue((output / "surveyor" / "agent_bundle.json").is_file())
            self.assertTrue((output / "aliases" / "TIBIA-RE-COORDINATOR.json").is_file())
            self.assertTrue((output / "missing-readers.json").is_file())
            self.assertTrue((output / "manifest.sha256").is_file())
            missing = json.loads((output / "missing-readers.json").read_text(encoding="utf-8"))
            self.assertEqual("NO_RUNTIME_INPUT_THIS_RUN", missing["run_unavailable_inputs"][0]["reason"])
            self.assertFalse(missing["guardrails"]["gap_authorizes_runtime_mutation"])


if __name__ == "__main__":
    unittest.main()
