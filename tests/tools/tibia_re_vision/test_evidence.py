import subprocess
import sys
import unittest
from pathlib import Path

from tools.tibia_re_vision.evidence import (
    normalize_ocr_transcription,
    validate_visual_evidence,
)


class VisualEvidenceSafetyTests(unittest.TestCase):
    def test_visual_only_is_required(self):
        payload = _valid_payload()
        payload["quality"]["visual_only"] = False

        self.assertIn("quality.visual_only must be true", validate_visual_evidence(payload))

    def test_structural_authority_is_forbidden(self):
        payload = _valid_payload()
        payload["quality"]["structural_authority"] = True

        self.assertIn("quality.structural_authority must be false", validate_visual_evidence(payload))

    def test_black_or_empty_ocr_stays_empty(self):
        result = normalize_ocr_transcription(
            "\n \n",
            evidence_ref="fixture:black",
            capture_sha256="a" * 64,
            model_profile_id="ocr-profile",
        )

        self.assertEqual(result["observation"]["visible_text"], [])

    def test_benchmark_direct_script_help_is_offline(self):
        repository_root = Path(__file__).resolve().parents[3]
        result = subprocess.run(
            [
                sys.executable,
                str(repository_root / "tools/tibia-re-vision-benchmark/vision_benchmark.py"),
                "--help",
            ],
            capture_output=True,
            check=False,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("usage:", result.stdout)


def _valid_payload():
    return {
        "schema_version": 1,
        "capture": {
            "evidence_ref": "fixture:login",
            "sha256": "a" * 64,
            "source_monotonic_ns": None,
        },
        "model": {"model_profile_id": "test-profile"},
        "observation": {
            "screen_class": "LOGIN_SCREEN",
            "visible_text": [],
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
