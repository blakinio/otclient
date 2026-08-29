from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from vision_benchmark import (  # noqa: E402
    admit_residency,
    evaluate_hard_gates,
    score_profile,
    sha256_file,
    validate_visual_evidence,
)


def valid_payload(screen_class="LOGIN_SCREEN"):
    return {
        "schema_version": 1,
        "capture": {
            "evidence_ref": "fixture:login",
            "sha256": "a" * 64,
            "source_monotonic_ns": None,
        },
        "model": {"model_profile_id": "test-profile"},
        "observation": {
            "screen_class": screen_class,
            "visible_text": ["ACCOUNT LOGIN"],
            "ui_objects": [],
            "appeared": [],
            "disappeared": [],
            "changed": [],
        },
        "quality": {
            "schema_valid": True,
            "visual_only": True,
            "structural_authority": False,
            "unknown_fields": [],
        },
    }


def valid_trial(screen_class="LOGIN_SCREEN", ground_truth="LOGIN_SCREEN"):
    return {
        "visual_evidence": valid_payload(screen_class),
        "ground_truth_screen_class": ground_truth,
        "secret_leakage": False,
        "runtime_action_authority": False,
        "model_authored_executable_action_parameters": False,
        "single_model_residency_violation": False,
        "silent_cloud_fallback": False,
        "provenance_complete": True,
    }


class VisualEvidenceSchemaTests(unittest.TestCase):
    def test_valid_payload_passes(self):
        self.assertEqual(validate_visual_evidence(valid_payload()), [])

    def test_visual_only_and_non_authority_are_mandatory(self):
        payload = valid_payload()
        payload["quality"]["visual_only"] = False
        payload["quality"]["structural_authority"] = True
        errors = validate_visual_evidence(payload)
        self.assertIn("quality.visual_only must be true", errors)
        self.assertIn("quality.structural_authority must be false", errors)

    def test_invalid_screen_class_fails(self):
        payload = valid_payload("IN_GAME")
        self.assertIn("observation.screen_class invalid", validate_visual_evidence(payload))

    def test_missing_provenance_shape_fails(self):
        payload = valid_payload()
        del payload["capture"]["sha256"]
        self.assertIn("capture.sha256 invalid", validate_visual_evidence(payload))


class HardGateTests(unittest.TestCase):
    def test_false_in_game_on_login_fails_primary_gate(self):
        result = evaluate_hard_gates([valid_trial("IN_GAME_VISUAL", "LOGIN_SCREEN")])
        self.assertFalse(result["eligible"])
        self.assertFalse(result["zero_false_in_game_on_login_or_character_select"])

    def test_secret_leakage_fails_gate(self):
        trial = valid_trial()
        trial["secret_leakage"] = True
        result = evaluate_hard_gates([trial])
        self.assertFalse(result["eligible"])
        self.assertFalse(result["zero_secret_leakage"])

    def test_all_valid_trials_are_eligible(self):
        result = evaluate_hard_gates([valid_trial(), valid_trial("OTHER", "OTHER")])
        self.assertTrue(result["eligible"])
        self.assertTrue(all(v for k, v in result.items() if k != "failure_reasons"))


class ResidencyTests(unittest.TestCase):
    def test_empty_residency_admits_target(self):
        self.assertEqual(admit_residency([], "qwen"), (True, "EMPTY_SLOT"))

    def test_exact_target_alone_admits_reuse(self):
        self.assertEqual(admit_residency(["qwen"], "qwen"), (True, "EXACT_TARGET_ONLY"))

    def test_different_or_multiple_models_refuse(self):
        self.assertEqual(admit_residency(["other"], "qwen")[0], False)
        self.assertEqual(admit_residency(["qwen", "other"], "qwen")[0], False)

    def test_unknown_residency_refuses(self):
        self.assertEqual(admit_residency(None, "qwen"), (False, "RESIDENCY_UNKNOWN"))


class ScoringTests(unittest.TestCase):
    def test_weighted_score(self):
        metrics = {
            "semantic_correctness": 1.0,
            "hallucination_resistance": 0.8,
            "ocr_exact_match": 0.5,
            "repeatability": 1.0,
            "latency_efficiency": 0.6,
            "memory_efficiency": 0.4,
        }
        self.assertAlmostEqual(score_profile(metrics), 78.0)

    def test_score_rejects_out_of_range_metric(self):
        with self.assertRaises(ValueError):
            score_profile({
                "semantic_correctness": 1.1,
                "hallucination_resistance": 1.0,
                "ocr_exact_match": 1.0,
                "repeatability": 1.0,
                "latency_efficiency": 1.0,
                "memory_efficiency": 1.0,
            })


class HashTests(unittest.TestCase):
    def test_sha256_file(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "sample.bin"
            path.write_bytes(b"abc")
            self.assertEqual(
                sha256_file(path),
                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            )


if __name__ == "__main__":
    unittest.main()
