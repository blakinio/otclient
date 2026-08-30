import hashlib
from pathlib import Path
import tempfile
import unittest

from tools.tibia_re_control_center.agent_protocol import AgentVisualState
from tools.tibia_re_control_center.agent_vision import (
    AgentVisionSensor,
    ModelSlotScheduler,
    ModelSlotUnavailable,
    QWEN_NUM_CTX,
    QWEN_NUM_PREDICT,
    QWEN_TEMPERATURE,
    QWEN_VISION_DIGEST,
    QWEN_VISION_MODEL,
    QWEN_VISION_PROFILE_ID,
    SecretSafeCapture,
)
from tools.tibia_re_vision.evidence import UnsafeInputError


def _visual_evidence(capture: SecretSafeCapture, *, screen_class: str = "LOGIN_SCREEN"):
    return {
        "schema_version": 1,
        "capture": {
            "evidence_ref": capture.evidence_ref,
            "sha256": capture.sha256,
            "source_monotonic_ns": capture.source_monotonic_ns,
        },
        "model": {"model_profile_id": QWEN_VISION_PROFILE_ID},
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


class ModelSlotSchedulerTests(unittest.TestCase):
    def _scheduler(self, resident, *, digest=QWEN_VISION_DIGEST, response=None):
        self.unloads = []
        self.inferences = []

        def ps():
            return resident[0]

        def unload(model):
            self.unloads.append(model)
            resident[0] = []

        def infer(**kwargs):
            self.inferences.append(kwargs)
            resident[0] = [kwargs["model"]]
            return response

        return ModelSlotScheduler(ps=ps, digest=lambda model: digest, infer=infer, unload=unload)

    def test_empty_slot_acquires_only_verified_exact_digest(self):
        resident = [[]]
        scheduler = self._scheduler(resident, response={"ok": True})

        self.assertEqual({"ok": True}, scheduler.infer(model=QWEN_VISION_MODEL, expected_digest=QWEN_VISION_DIGEST))
        self.assertTrue(scheduler.owns(QWEN_VISION_MODEL))
        self.assertEqual([], self.unloads)

    def test_exact_digest_mismatch_refuses_before_infer(self):
        resident = [[]]
        scheduler = self._scheduler(resident, digest="0" * 64)

        with self.assertRaisesRegex(ModelSlotUnavailable, "MODEL_DIGEST_MISMATCH"):
            scheduler.infer(model=QWEN_VISION_MODEL, expected_digest=QWEN_VISION_DIGEST)
        self.assertEqual([], self.inferences)

    def test_foreign_model_is_never_unloaded(self):
        resident = [["foreign:model"]]
        scheduler = self._scheduler(resident)

        with self.assertRaisesRegex(ModelSlotUnavailable, "DIFFERENT_RESIDENT_MODEL"):
            scheduler.infer(model=QWEN_VISION_MODEL, expected_digest=QWEN_VISION_DIGEST)
        self.assertEqual([], self.unloads)
        self.assertEqual([["foreign:model"]], resident)

    def test_multiple_and_unknown_residency_fail_closed(self):
        for resident in ([[QWEN_VISION_MODEL, "foreign:model"]], [None]):
            scheduler = self._scheduler(resident)
            with self.assertRaises(ModelSlotUnavailable) as failure:
                scheduler.infer(model=QWEN_VISION_MODEL, expected_digest=QWEN_VISION_DIGEST)
            self.assertIn(failure.exception.code, {"MULTIPLE_RESIDENT_MODELS", "RESIDENCY_UNKNOWN"})
            self.assertEqual([], self.unloads)

    def test_only_scheduler_owned_exact_target_is_reused(self):
        resident = [[]]
        scheduler = self._scheduler(resident, response={"ok": True})
        scheduler.infer(model=QWEN_VISION_MODEL, expected_digest=QWEN_VISION_DIGEST)
        scheduler.infer(model=QWEN_VISION_MODEL, expected_digest=QWEN_VISION_DIGEST)

        self.assertEqual(2, len(self.inferences))
        self.assertEqual([], self.unloads)

    def test_exact_but_unowned_target_fails_closed(self):
        resident = [[QWEN_VISION_MODEL]]
        scheduler = self._scheduler(resident)

        with self.assertRaisesRegex(ModelSlotUnavailable, "TARGET_NOT_OWNED"):
            scheduler.infer(model=QWEN_VISION_MODEL, expected_digest=QWEN_VISION_DIGEST)
        self.assertEqual([], self.unloads)

    def test_switch_unloads_owned_model_and_verifies_empty_before_load(self):
        resident = [[]]
        scheduler = self._scheduler(resident, response={"ok": True})
        scheduler.infer(model=QWEN_VISION_MODEL, expected_digest=QWEN_VISION_DIGEST)
        scheduler.infer(model="other:exact", expected_digest=QWEN_VISION_DIGEST)

        self.assertEqual([QWEN_VISION_MODEL], self.unloads)
        self.assertTrue(scheduler.owns("other:exact"))

    def test_release_unloads_only_owned_target_and_verifies_empty(self):
        resident = [[]]
        scheduler = self._scheduler(resident, response={"ok": True})
        scheduler.infer(model=QWEN_VISION_MODEL, expected_digest=QWEN_VISION_DIGEST)

        scheduler.release()

        self.assertEqual([QWEN_VISION_MODEL], self.unloads)
        self.assertFalse(scheduler.owns(QWEN_VISION_MODEL))

    def test_release_does_not_unload_foreign_replacement(self):
        resident = [[]]
        scheduler = self._scheduler(resident, response={"ok": True})
        scheduler.infer(model=QWEN_VISION_MODEL, expected_digest=QWEN_VISION_DIGEST)
        resident[0] = ["foreign:model"]

        with self.assertRaisesRegex(ModelSlotUnavailable, "MODEL_SLOT_NOT_OWNED"):
            scheduler.release()
        self.assertEqual([], self.unloads)
        self.assertTrue(scheduler.owns(QWEN_VISION_MODEL))

    def test_release_verify_empty_failure_preserves_ownership(self):
        resident = [[]]
        unloads = []
        def unload_without_effect(model):
            unloads.append(model)

        scheduler = ModelSlotScheduler(
            ps=lambda: resident[0],
            digest=lambda model: QWEN_VISION_DIGEST,
            infer=lambda **kwargs: resident.__setitem__(0, [kwargs["model"]]),
            unload=unload_without_effect,
        )
        scheduler.infer(model=QWEN_VISION_MODEL, expected_digest=QWEN_VISION_DIGEST)
        with self.assertRaisesRegex(ModelSlotUnavailable, "MODEL_UNLOAD_NOT_VERIFIED"):
            scheduler.release()
        self.assertTrue(scheduler.owns(QWEN_VISION_MODEL))
        self.assertEqual([QWEN_VISION_MODEL], unloads)


class AgentVisionSensorTests(unittest.TestCase):
    def _capture(self, directory: Path, *, body: bytes = b"safe frame", secret_safe=True, digest=None):
        path = directory / "frame.bin"
        path.write_bytes(body)
        return SecretSafeCapture(
            run_id="run-1",
            evidence_ref="capture:one",
            path=path,
            sha256=hashlib.sha256(body).hexdigest() if digest is None else digest,
            secret_safe=secret_safe,
            source_monotonic_ns=42,
        )

    def _sensor(self, provider):
        resident = [[]]
        return AgentVisionSensor(
            ModelSlotScheduler(
                ps=lambda: resident[0],
                digest=lambda model: QWEN_VISION_DIGEST,
                infer=lambda **kwargs: provider(kwargs),
                unload=lambda model: resident.__setitem__(0, []),
            )
        )

    def test_unsafe_capture_refuses_before_provider_call(self):
        calls = []
        with tempfile.TemporaryDirectory() as raw:
            capture = self._capture(Path(raw), secret_safe=False)
            sensor = self._sensor(lambda kwargs: calls.append(kwargs))
            with self.assertRaises(UnsafeInputError):
                sensor.observe(capture)
        self.assertEqual([], calls)

    def test_missing_empty_or_sha_mismatched_bytes_refuse_before_provider(self):
        for body, digest in ((b"", None), (b"safe", "0" * 64)):
            calls = []
            with tempfile.TemporaryDirectory() as raw:
                capture = self._capture(Path(raw), body=body, digest=digest)
                sensor = self._sensor(lambda kwargs: calls.append(kwargs))
                with self.assertRaises(ValueError):
                    sensor.observe(capture)
            self.assertEqual([], calls)

    def test_provider_arguments_are_pinned_and_keep_alive_is_zero(self):
        with tempfile.TemporaryDirectory() as raw:
            capture = self._capture(Path(raw))
            calls = []
            sensor = self._sensor(lambda kwargs: calls.append(kwargs) or _visual_evidence(capture))
            sensor.observe(capture)

        self.assertEqual(1, len(calls))
        self.assertEqual(QWEN_VISION_MODEL, calls[0]["model"])
        self.assertEqual("0s", calls[0]["keep_alive"])
        self.assertEqual(QWEN_NUM_CTX, calls[0]["num_ctx"])
        self.assertEqual(QWEN_NUM_PREDICT, calls[0]["num_predict"])
        self.assertEqual(QWEN_TEMPERATURE, calls[0]["temperature"])
        self.assertEqual(QWEN_VISION_PROFILE_ID, calls[0]["model_profile_id"])

    def test_invalid_strict_schema_is_rejected(self):
        with tempfile.TemporaryDirectory() as raw:
            capture = self._capture(Path(raw))
            bad = _visual_evidence(capture)
            bad["model"]["untrusted_authority"] = "WORLD_CONFIRMED"
            sensor = self._sensor(lambda kwargs: bad)
            with self.assertRaisesRegex(ValueError, "VisualEvidence"):
                sensor.observe(capture)

    def test_visual_only_invariants_and_in_game_mapping_are_preserved(self):
        with tempfile.TemporaryDirectory() as raw:
            capture = self._capture(Path(raw))
            sensor = self._sensor(lambda kwargs: _visual_evidence(capture, screen_class="IN_GAME_VISUAL"))
            observation = sensor.observe(capture)

        self.assertEqual(AgentVisualState.WORLD_VISUAL.value, observation.screen_class)
        self.assertTrue(observation.visual_only)
        self.assertFalse(observation.structural_authority)
        self.assertNotEqual("WORLD_CONFIRMED", observation.screen_class)

    def test_exact_duplicate_sha_is_rejected_without_second_provider_call(self):
        calls = []
        with tempfile.TemporaryDirectory() as raw:
            capture = self._capture(Path(raw))
            sensor = self._sensor(lambda kwargs: calls.append(kwargs) or _visual_evidence(capture))
            sensor.observe(capture)
            with self.assertRaisesRegex(ValueError, "DUPLICATE_CAPTURE_SHA256"):
                sensor.observe(capture)
        self.assertEqual(1, len(calls))


if __name__ == "__main__":
    unittest.main()
