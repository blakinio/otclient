import hashlib
import importlib
import tempfile
import unittest
from pathlib import Path

capture_edge = importlib.import_module("tools.tibia_re_vision.capture_edge")


def binding():
    return capture_edge.RuntimeBinding(
        provenance_ref="admission:test", runtime_id="runtime-1",
        target_container="otclient-track-a-kasmvnc", display=":98", pid=123,
        process_start_ticks=456, xid=789, client_version="15.32.75d4a0",
        client_size=52_105_824, client_sha256="a" * 64,
        observed_monotonic_ns=1_000, runtime_access="read_only",
        target_uniqueness="PROVEN",
    )


class FrameSource:
    def __init__(self):
        self.calls = 0

    def geometry(self, current_binding):
        self.calls += 1
        return capture_edge.WindowGeometry(0, 0, 1, 1)

    def capture_rgb(self, current_binding, geometry):
        self.calls += 1
        return b"\x01\x02\x03"


class CaptureTrustBoundaryTests(unittest.TestCase):
    def test_no_hidden_tokens_or_issuance_registry_remain(self):
        self.assertFalse(hasattr(capture_edge, "_CAPTURE_EVIDENCE_ISSUANCE_TOKEN"))
        self.assertFalse(hasattr(capture_edge, "_SECRET_POLICY_ISSUANCE_TOKEN"))
        self.assertFalse(hasattr(capture_edge, "_ISSUED_EVIDENCE"))

    def test_public_resolver_cannot_self_certify_an_incomplete_policy(self):
        with self.assertRaisesRegex(capture_edge.CaptureEdgeError, "CAPTURE_TRUSTED_POLICY_CONSUMER_REQUIRED"):
            capture_edge.ReviewedSecretMaskPolicyResolver(
                policy_id="attacker-incomplete", expected_width=1, expected_height=1,
                secret_regions=(capture_edge.PixelRegion(0, 0, 1, 1),),
            )

    def test_direct_policy_issue_and_subclass_issue_fail_closed(self):
        class AttackerPolicy(capture_edge.ReviewedSecretMaskPolicy):
            pass

        for policy_type in (capture_edge.ReviewedSecretMaskPolicy, AttackerPolicy):
            with self.subTest(policy_type=policy_type.__name__), self.assertRaisesRegex(
                capture_edge.CaptureEdgeError, "CAPTURE_TRUSTED_POLICY_CONSUMER_REQUIRED"
            ):
                policy_type._issue(
                    object(), object(), policy_id="attacker", expected_width=1,
                    expected_height=1, secret_regions=(capture_edge.PixelRegion(0, 0, 1, 1),),
                )

    def test_public_evidence_issue_and_subclass_issue_fail_closed(self):
        artifact = capture_edge.CaptureArtifact(Path("does-not-exist"), "a" * 64)

        class AttackerEvidence(capture_edge.CaptureEvidence):
            pass

        for evidence_type in (capture_edge.CaptureEvidence, AttackerEvidence):
            with self.subTest(evidence_type=evidence_type.__name__), self.assertRaisesRegex(
                capture_edge.CaptureEdgeError, "CAPTURE_TRUSTED_POLICY_CONSUMER_REQUIRED"
            ):
                evidence_type._issue(
                    issuance_token=object(), run_id="attacker", runtime_binding=binding(),
                    geometry=capture_edge.WindowGeometry(0, 0, 1, 1), source_monotonic_ns=1_001,
                    full_frame=artifact, secret_policy_ref="attacker", is_blank=False,
                    is_black=False, changed_from_previous=None, crop=None,
                )

    def test_object_setattr_cannot_turn_allocated_evidence_into_vision_input(self):
        forged = object.__new__(capture_edge.CaptureEvidence)
        object.__setattr__(forged, "secret_safe", True)
        object.__setattr__(forged, "runtime_binding", binding())
        with self.assertRaisesRegex(capture_edge.CaptureEdgeError, "CAPTURE_TRUSTED_POLICY_CONSUMER_REQUIRED"):
            forged.validated_vision_capture(current_binding=binding(), now_ns=1_001, max_age_ns=500)

    def test_capture_construction_fails_before_frame_access(self):
        source = FrameSource()
        with self.assertRaisesRegex(capture_edge.CaptureEdgeError, "CAPTURE_TRUSTED_POLICY_CONSUMER_REQUIRED"):
            capture_edge.CaptureEdge(
                binding_reader=binding, frame_source=source, monotonic_ns=lambda: 1_001,
                secret_policy=object(),
            )
        self.assertEqual(0, source.calls)

    def test_object_new_capture_cannot_write_to_attacker_selected_root(self):
        forged = object.__new__(capture_edge.CaptureEdge)
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            with self.assertRaisesRegex(capture_edge.CaptureEdgeError, "CAPTURE_TRUSTED_POLICY_CONSUMER_REQUIRED"):
                forged.capture(run_id="attacker", evidence_root=root, max_binding_age_ns=500)
            self.assertEqual([], list(root.iterdir()))


class RuntimeBoundaryTests(unittest.TestCase):
    def test_runtime_binding_snapshot_detects_same_object_reflective_mutation(self):
        current = binding()
        snapshot = capture_edge._snapshot_binding(current)
        object.__setattr__(current, "xid", current.xid + 1)
        self.assertNotEqual(snapshot, capture_edge._snapshot_binding(current))

    def test_clock_samples_must_be_exact_positive_and_not_future(self):
        current = binding()
        for now in (-1, 0, True):
            with self.subTest(now=now), self.assertRaisesRegex(capture_edge.CaptureEdgeError, "CAPTURE_CLOCK_INVALID"):
                capture_edge.CaptureEdge._require_current(current, now, 500)
        with self.assertRaisesRegex(capture_edge.CaptureEdgeError, "RUNTIME_BINDING_STALE"):
            capture_edge.CaptureEdge._require_current(current, 999, 500)

    def test_binding_freshness_is_independent_of_evidence_age(self):
        stale = binding()
        object.__setattr__(stale, "observed_monotonic_ns", 1)
        with self.assertRaisesRegex(capture_edge.CaptureEdgeError, "RUNTIME_BINDING_STALE"):
            capture_edge.CaptureEdge._require_current(stale, 1_001, 500)


class EncodingAndCommandTests(unittest.TestCase):
    def test_mask_crop_and_png_integrity_primitives_remain_deterministic(self):
        geometry = capture_edge.WindowGeometry(0, 0, 2, 1)
        pixels = bytes((9, 8, 7, 1, 2, 3))
        masked = capture_edge._mask_rgb(pixels, geometry, (capture_edge.PixelRegion(0, 0, 1, 1),))
        self.assertEqual(bytes((0, 0, 0, 1, 2, 3)), masked)
        self.assertEqual(bytes((0, 0, 0)), capture_edge._crop_rgb(masked, geometry, capture_edge.PixelRegion(0, 0, 1, 1)))
        png = capture_edge._encode_rgb_png(2, 1, masked)
        self.assertEqual(hashlib.sha256(png).hexdigest(), hashlib.sha256(png).hexdigest())
        self.assertTrue(png.startswith(b"\x89PNG\r\n\x1a\n"))

    def test_fixed_read_only_x11_ffmpeg_vocabulary(self):
        class Result:
            def __init__(self, stdout):
                self.returncode = 0
                self.stdout = stdout

        class Runner:
            def __init__(self):
                self.calls = []

            def run(self, args, *, timeout_s):
                self.calls.append(args)
                return Result(b"X=7\nY=9\nWIDTH=1\nHEIGHT=1\n" if len(self.calls) == 1 else b"\x01\x02\x03")

        runner = Runner()
        source = capture_edge.KasmX11FfmpegFrameSource(runner=runner)
        geometry = source.geometry(binding())
        source.capture_rgb(binding(), geometry)
        self.assertEqual(("docker", "exec"), runner.calls[0][:2])
        self.assertIn("xdotool", runner.calls[0])
        self.assertIn("ffmpeg", runner.calls[1])
        self.assertNotIn("shell", " ".join(runner.calls[1]))


if __name__ == "__main__":
    unittest.main()
