import hashlib
import importlib
import struct
import tempfile
import unittest
import zlib
from dataclasses import replace
from pathlib import Path


_capture_edge = importlib.import_module("tools.tibia_re_vision.capture_edge") if importlib.util.find_spec("tools.tibia_re_vision.capture_edge") else None


def _reviewed_policy(geometry, *, policy_id="fixture-mask-v1"):
    return _capture_edge.ReviewedSecretMaskPolicy(
        policy_id=policy_id,
        expected_width=geometry.width,
        expected_height=geometry.height,
        secret_regions=(_capture_edge.PixelRegion(x=0, y=0, width=1, height=1),),
    )


class _FrameSource:
    def __init__(self, geometry, pixels):
        self.geometry_value = geometry
        self.pixels = pixels
        self.geometry_calls = []
        self.capture_calls = []

    def geometry(self, binding):
        self.geometry_calls.append(binding)
        return self.geometry_value

    def capture_rgb(self, binding, geometry):
        self.capture_calls.append((binding, geometry))
        return self.pixels


class _GeometryDriftSource(_FrameSource):
    def __init__(self, geometries, pixels):
        super().__init__(geometries[0], pixels)
        self.geometries = iter(geometries)

    def geometry(self, binding):
        self.geometry_calls.append(binding)
        return next(self.geometries)


class CaptureEdgeTests(unittest.TestCase):
    def test_reviewed_secret_policy_is_bound_to_edge_not_each_capture(self):
        self.assertTrue(
            hasattr(_capture_edge, "ReviewedSecretMaskPolicy"),
            "capture edge must expose a reviewed composition-time mask policy",
        )
        binding = _binding()
        geometry = _capture_edge.WindowGeometry(x=0, y=0, width=2, height=1)
        policy = _capture_edge.ReviewedSecretMaskPolicy(
            policy_id="fixture-login-mask-v1",
            expected_width=2,
            expected_height=1,
            secret_regions=(_capture_edge.PixelRegion(0, 0, 1, 1),),
        )
        source = _FrameSource(geometry, bytes((9, 8, 7, 1, 2, 3)))
        edge = _capture_edge.CaptureEdge(
            binding_reader=lambda: binding,
            frame_source=source,
            monotonic_ns=iter((1_100, 1_200)).__next__,
            secret_policy=policy,
        )
        with tempfile.TemporaryDirectory() as raw:
            evidence = edge.capture(
                run_id="run-reviewed-policy",
                evidence_root=Path(raw),
                max_binding_age_ns=500,
            )
            self.assertTrue(evidence.secret_safe)
            self.assertEqual(policy.policy_ref, evidence.secret_policy_ref)
            import inspect
            self.assertNotIn("secret_policy", inspect.signature(edge.capture).parameters)
            pixels = _decode_rgb_png(evidence.full_frame.path.read_bytes())
            self.assertEqual(bytes((0, 0, 0, 1, 2, 3)), pixels)

    def test_reviewed_secret_policy_requires_nonempty_regions(self):
        geometry = _capture_edge.WindowGeometry(x=0, y=0, width=1, height=1)
        with self.assertRaisesRegex(ValueError, "reviewed secret regions invalid"):
            _capture_edge.ReviewedSecretMaskPolicy(
                policy_id="fixture-empty-mask-v1",
                expected_width=geometry.width,
                expected_height=geometry.height,
                secret_regions=(),
            )

    def test_reviewed_policy_geometry_mismatch_fails_before_capture_or_persistence(self):
        binding = _binding()
        geometry = _capture_edge.WindowGeometry(x=0, y=0, width=2, height=1)
        wrong_geometry_policy = _capture_edge.ReviewedSecretMaskPolicy(
            policy_id="fixture-wrong-geometry-v1",
            expected_width=1,
            expected_height=1,
            secret_regions=(_capture_edge.PixelRegion(0, 0, 1, 1),),
        )
        source = _FrameSource(geometry, bytes((9, 8, 7, 1, 2, 3)))
        edge = _capture_edge.CaptureEdge(
            binding_reader=lambda: binding,
            frame_source=source,
            monotonic_ns=iter((1_100, 1_200)).__next__,
            secret_policy=wrong_geometry_policy,
        )
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            with self.assertRaisesRegex(
                _capture_edge.CaptureEdgeError, "CAPTURE_SECRET_POLICY_GEOMETRY_MISMATCH"
            ):
                edge.capture(
                    run_id="run-policy-geometry-mismatch",
                    evidence_root=root,
                    max_binding_age_ns=500,
                )
            self.assertEqual([], list(root.iterdir()))
        self.assertEqual([binding], source.geometry_calls)
        self.assertEqual([], source.capture_calls)

    def test_stable_capture_is_content_addressed_and_feeds_vision_foundation(self):
        self.assertIsNotNone(_capture_edge, "capture_edge module must exist")
        binding = _binding()
        geometry = _capture_edge.WindowGeometry(x=7, y=9, width=2, height=1)
        source = _FrameSource(geometry, bytes((10, 20, 30, 40, 50, 60)))
        binding_reads = []
        clock = iter((1_100, 1_200))
        edge = _capture_edge.CaptureEdge(
            binding_reader=lambda: binding_reads.append(binding) or binding,
            frame_source=source,
            monotonic_ns=lambda: next(clock),
            secret_policy=_reviewed_policy(geometry),
        )

        with tempfile.TemporaryDirectory() as raw:
            evidence = edge.capture(
                run_id="run-1",
                evidence_root=Path(raw),
                max_binding_age_ns=500,
            )
            artifact_bytes = evidence.full_frame.path.read_bytes()
            self.assertEqual(hashlib.sha256(artifact_bytes).hexdigest(), evidence.full_frame.sha256)
            self.assertEqual(f"{evidence.full_frame.sha256}.png", evidence.full_frame.path.name)
            self.assertTrue(evidence.secret_safe)
            self.assertEqual(geometry, evidence.geometry)
            self.assertEqual(binding, evidence.runtime_binding)
            self.assertEqual(1_200, evidence.source_monotonic_ns)
            self.assertFalse(hasattr(evidence, "to_vision_capture"))
            vision = evidence.validated_vision_capture(
                current_binding=binding, now_ns=1_300, max_age_ns=500
            )
            self.assertEqual("run-1", vision.run_id)
            self.assertEqual(evidence.full_frame.path, vision.path)
            self.assertEqual(evidence.full_frame.sha256, vision.sha256)
            self.assertTrue(vision.secret_safe)
            self.assertEqual(1_200, vision.source_monotonic_ns)

        self.assertEqual([binding, binding, binding], binding_reads)
        self.assertEqual([binding, binding], source.geometry_calls)
        self.assertEqual([(binding, geometry)], source.capture_calls)

    def test_secret_mask_and_crop_are_derived_before_any_artifact_is_persisted(self):
        self.assertTrue(hasattr(_capture_edge, "PixelRegion"), "capture edge must expose bounded pixel regions")
        binding = _binding()
        geometry = _capture_edge.WindowGeometry(x=10, y=20, width=3, height=2)
        pixels = bytes((255, 0, 0, 0, 255, 0, 0, 0, 255, 255, 255, 255, 1, 2, 3, 255, 255, 0))
        source = _FrameSource(geometry, pixels)
        secret = _capture_edge.PixelRegion(x=0, y=0, width=1, height=1)
        edge = _capture_edge.CaptureEdge(
            binding_reader=lambda: binding,
            frame_source=source,
            monotonic_ns=iter((1_100, 1_200)).__next__,
            secret_policy=_capture_edge.ReviewedSecretMaskPolicy(
                policy_id="fixture-secret-crop-v1",
                expected_width=geometry.width,
                expected_height=geometry.height,
                secret_regions=(secret,),
            ),
        )
        crop = _capture_edge.PixelRegion(x=0, y=0, width=2, height=1)
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            evidence = edge.capture(
                run_id="run-secret",
                evidence_root=root,
                crop=crop,
                max_binding_age_ns=500,
            )
            self.assertIsNotNone(evidence.crop)
            full_pixels = _decode_rgb_png(evidence.full_frame.path.read_bytes())
            crop_pixels = _decode_rgb_png(evidence.crop.path.read_bytes())
            self.assertEqual(bytes((0, 0, 0)), full_pixels[:3])
            self.assertEqual(bytes((0, 255, 0)), full_pixels[3:6])
            self.assertEqual(bytes((0, 0, 0, 0, 255, 0)), crop_pixels)
            self.assertEqual(evidence.full_frame.sha256, evidence.crop.parent_full_sha256)
            self.assertEqual(crop, evidence.crop.region)
            self.assertEqual(
                {evidence.full_frame.path.name, evidence.crop.path.name},
                {path.name for path in root.iterdir()},
            )
        self.assertEqual(1, len(source.capture_calls))


    def test_stale_runtime_binding_fails_before_capture_and_persistence(self):
        binding = _binding()
        geometry = _capture_edge.WindowGeometry(x=0, y=0, width=1, height=1)
        source = _FrameSource(geometry, bytes((1, 2, 3)))
        edge = _capture_edge.CaptureEdge(
            binding_reader=lambda: binding,
            frame_source=source,
            monotonic_ns=iter((1_600, 1_700)).__next__,
            secret_policy=_reviewed_policy(geometry),
        )
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            with self.assertRaisesRegex(_capture_edge.CaptureEdgeError, "RUNTIME_BINDING_STALE"):
                edge.capture(
                    run_id="run-stale",
                    evidence_root=root,

                    max_binding_age_ns=500,
                )
            self.assertEqual([], list(root.iterdir()))
        self.assertEqual([], source.capture_calls)
    def test_runtime_binding_drift_fails_before_persistence(self):
        before = _binding()
        after = replace(before, xid=before.xid + 1)
        bindings = iter((before, after))
        geometry = _capture_edge.WindowGeometry(x=0, y=0, width=1, height=1)
        source = _FrameSource(geometry, bytes((1, 2, 3)))
        edge = _capture_edge.CaptureEdge(
            binding_reader=bindings.__next__,
            frame_source=source,
            monotonic_ns=iter((1_100, 1_200)).__next__,
            secret_policy=_reviewed_policy(geometry),
        )
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            with self.assertRaisesRegex(_capture_edge.CaptureEdgeError, "RUNTIME_BINDING_CHANGED"):
                edge.capture(
                    run_id="run-drift",
                    evidence_root=root,

                    max_binding_age_ns=500,
                )
            self.assertEqual([], list(root.iterdir()))
        self.assertEqual(1, len(source.capture_calls))
    def test_binding_drift_during_post_geometry_recheck_fails_before_persistence(self):
        before = _binding()
        drifted = replace(before, xid=before.xid + 1)
        reads = iter((before, before, drifted))
        geometry = _capture_edge.WindowGeometry(x=0, y=0, width=1, height=1)
        source = _FrameSource(geometry, bytes((1, 2, 3)))
        edge = _capture_edge.CaptureEdge(
            binding_reader=lambda: next(reads),
            frame_source=source,
            monotonic_ns=iter((1_100, 1_200)).__next__,
            secret_policy=_reviewed_policy(geometry),
        )
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            with self.assertRaisesRegex(_capture_edge.CaptureEdgeError, "RUNTIME_BINDING_CHANGED"):
                edge.capture(
                    run_id="run-final-binding-drift",
                    evidence_root=root,

                    max_binding_age_ns=500,
                )
            self.assertEqual([], list(root.iterdir()))

    def test_geometry_drift_fails_before_persistence(self):
        binding = _binding()
        before_geometry = _capture_edge.WindowGeometry(x=0, y=0, width=2, height=1)
        after_geometry = _capture_edge.WindowGeometry(x=1, y=0, width=2, height=1)
        source = _GeometryDriftSource(
            (before_geometry, after_geometry),
            bytes((1, 2, 3, 4, 5, 6)),
        )
        edge = _capture_edge.CaptureEdge(
            binding_reader=lambda: binding,
            frame_source=source,
            monotonic_ns=iter((1_100, 1_200)).__next__,
            secret_policy=_reviewed_policy(before_geometry),
        )
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            with self.assertRaisesRegex(_capture_edge.CaptureEdgeError, "CAPTURE_GEOMETRY_CHANGED"):
                edge.capture(
                    run_id="run-geometry-drift",
                    evidence_root=root,

                    max_binding_age_ns=500,
                )
            self.assertEqual([], list(root.iterdir()))
        self.assertEqual([binding, binding], source.geometry_calls)

    def test_validated_vision_capture_rechecks_full_and_crop_integrity(self):
        binding = _binding()
        geometry = _capture_edge.WindowGeometry(x=0, y=0, width=2, height=1)
        source = _FrameSource(geometry, bytes((1, 2, 3, 4, 5, 6)))
        edge = _capture_edge.CaptureEdge(
            binding_reader=lambda: binding,
            frame_source=source,
            monotonic_ns=iter((1_100, 1_200)).__next__,
            secret_policy=_reviewed_policy(geometry),
        )
        with tempfile.TemporaryDirectory() as raw:
            evidence = edge.capture(
                run_id="run-integrity",
                evidence_root=Path(raw),
                crop=_capture_edge.PixelRegion(0, 0, 1, 1),
                max_binding_age_ns=500,
            )
            self.assertTrue(hasattr(evidence, "validated_vision_capture"))
            vision = evidence.validated_vision_capture(
                current_binding=binding, now_ns=1_300, max_age_ns=500
            )
            self.assertEqual(evidence.crop.sha256, vision.sha256)
            evidence.full_frame.path.write_bytes(b"tampered")
            with self.assertRaisesRegex(_capture_edge.CaptureEdgeError, "CAPTURE_ARTIFACT_INTEGRITY_INVALID"):
                evidence.validated_vision_capture(
                    current_binding=binding, now_ns=1_300, max_age_ns=500
                )
    def test_validated_vision_capture_rejects_stale_or_foreign_binding(self):
        binding = _binding()
        geometry = _capture_edge.WindowGeometry(x=0, y=0, width=1, height=1)
        edge = _capture_edge.CaptureEdge(
            binding_reader=lambda: binding,
            frame_source=_FrameSource(geometry, bytes((1, 2, 3))),
            monotonic_ns=iter((1_100, 1_200)).__next__,
            secret_policy=_reviewed_policy(geometry),
        )
        with tempfile.TemporaryDirectory() as raw:
            evidence = edge.capture(
                run_id="run-currentness",
                evidence_root=Path(raw),
                max_binding_age_ns=500,
            )
            cases = (
                (replace(binding, xid=binding.xid + 1), 1_300, "CAPTURE_RUNTIME_BINDING_MISMATCH"),
                (binding, 1_701, "CAPTURE_EVIDENCE_STALE"),
            )
            for current, now_ns, reason in cases:
                with self.subTest(reason=reason):
                    with self.assertRaisesRegex(_capture_edge.CaptureEdgeError, reason):
                        evidence.validated_vision_capture(
                            current_binding=current, now_ns=now_ns, max_age_ns=500
                        )
class CaptureAnalysisTests(unittest.TestCase):
    def test_black_and_blank_flags_are_deterministic(self):
        binding = _binding()
        geometry = _capture_edge.WindowGeometry(x=0, y=0, width=2, height=1)
        edge = _capture_edge.CaptureEdge(
            binding_reader=lambda: binding,
            frame_source=_FrameSource(geometry, b"\x00" * 6),
            monotonic_ns=iter((1_100, 1_200)).__next__,
            secret_policy=_reviewed_policy(geometry),
        )
        with tempfile.TemporaryDirectory() as raw:
            evidence = edge.capture(
                run_id="run-black",
                evidence_root=Path(raw),
                max_binding_age_ns=500,
            )
        self.assertTrue(evidence.is_black)
        self.assertTrue(evidence.is_blank)

    def test_change_flag_binds_to_previous_full_frame_digest(self):
        binding = _binding()
        geometry = _capture_edge.WindowGeometry(x=0, y=0, width=2, height=1)
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            first = _capture_once(
                binding, geometry, bytes((9, 9, 9, 1, 2, 3)), root, "run-first"
            )
            same = _capture_once(
                binding, geometry, bytes((9, 9, 9, 1, 2, 3)), root, "run-same",
                previous_full_sha256=first.full_frame.sha256,
            )
            changed = _capture_once(
                binding, geometry, bytes((9, 9, 9, 4, 5, 6)), root, "run-changed",
                previous_full_sha256=first.full_frame.sha256,
            )
        self.assertIsNone(first.changed_from_previous)
        self.assertFalse(same.changed_from_previous)
        self.assertTrue(changed.changed_from_previous)


class _ProcessResult:
    def __init__(self, returncode, stdout=b"", stderr=b""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class _ProcessRunner:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def run(self, args, *, timeout_s):
        self.calls.append((tuple(args), timeout_s))
        return self.responses.pop(0)


class KasmX11FfmpegFrameSourceTests(unittest.TestCase):
    def test_exact_binding_drives_dynamic_geometry_and_read_only_ffmpeg_capture(self):
        binding = _binding()
        runner = _ProcessRunner((
            _ProcessResult(0, b"WINDOW=789\nX=7\nY=9\nWIDTH=2\nHEIGHT=1\nSCREEN=0\n"),
            _ProcessResult(0, bytes((1, 2, 3, 4, 5, 6))),
        ))
        source = _capture_edge.KasmX11FfmpegFrameSource(runner=runner, timeout_s=3.0)
        geometry = source.geometry(binding)
        pixels = source.capture_rgb(binding, geometry)
        self.assertEqual(_capture_edge.WindowGeometry(7, 9, 2, 1), geometry)
        self.assertEqual(bytes((1, 2, 3, 4, 5, 6)), pixels)
        prefix = (
            "docker", "exec", "-u", "kasm-user", "-e", "DISPLAY=:98",
            "otclient-track-a-kasmvnc",
        )
        self.assertEqual(
            prefix + ("xdotool", "getwindowgeometry", "--shell", "789"),
            runner.calls[0][0],
        )
        self.assertEqual(
            prefix + (
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin",
                "-f", "x11grab", "-video_size", "2x1", "-i", ":98+7,9",
                "-frames:v", "1", "-pix_fmt", "rgb24", "-f", "rawvideo", "pipe:1",
            ),
            runner.calls[1][0],
        )


def _capture_once(binding, geometry, pixels, root, run_id, *, previous_full_sha256=None):
    edge = _capture_edge.CaptureEdge(
        binding_reader=lambda: binding,
        frame_source=_FrameSource(geometry, pixels),
        monotonic_ns=iter((1_100, 1_200)).__next__,
        secret_policy=_reviewed_policy(geometry),
    )
    return edge.capture(
        run_id=run_id,
        evidence_root=root,
        max_binding_age_ns=500,
        previous_full_sha256=previous_full_sha256,
    )
def _binding():
    return _capture_edge.RuntimeBinding(
        provenance_ref="admission:test",
        runtime_id="runtime-1",
        target_container="otclient-track-a-kasmvnc",
        display=":98",
        pid=123,
        process_start_ticks=456,
        xid=789,
        client_version="15.32.75d4a0",
        client_size=52_105_824,
        client_sha256="a" * 64,
        observed_monotonic_ns=1_000,
        runtime_access="read_only",
        target_uniqueness="PROVEN",
    )


def _decode_rgb_png(payload):
    self_header = b"\x89PNG\r\n\x1a\n"
    if not payload.startswith(self_header):
        raise AssertionError("not PNG")
    offset = len(self_header)
    compressed = bytearray()
    width = height = None
    while offset < len(payload):
        size = struct.unpack(">I", payload[offset : offset + 4])[0]
        kind = payload[offset + 4 : offset + 8]
        body = payload[offset + 8 : offset + 8 + size]
        offset += 12 + size
        if kind == b"IHDR":
            width, height = struct.unpack(">II", body[:8])
        elif kind == b"IDAT":
            compressed.extend(body)
        elif kind == b"IEND":
            break
    raw = zlib.decompress(bytes(compressed))
    stride = width * 3
    rows = []
    for row in range(height):
        start = row * (stride + 1)
        if raw[start] != 0:
            raise AssertionError("unexpected PNG filter")
        rows.append(raw[start + 1 : start + 1 + stride])
    return b"".join(rows)


if __name__ == "__main__":
    unittest.main()
