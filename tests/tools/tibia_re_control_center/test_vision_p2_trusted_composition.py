from __future__ import annotations

import hashlib
import inspect
import tempfile
import unittest
from contextlib import contextmanager
from dataclasses import replace

from tests.tools.tibia_re_control_center.test_agent_edge_bridge import (
    _admission_observation,
    _authority_configuration,
    _signal_resolver,
    read_only_task,
)
from tools.tibia_re_control_center.agent_edge_transport import (
    EdgeFrameKind,
    EdgeTransportSigner,
)
from tools.tibia_re_control_center.agent_runtime_admission import (
    admit_read_only_runtime,
)
from tools.tibia_re_control_center.agent_runtime_signals import (
    RuntimeSignalBinding,
    RuntimeSignalResolver,
)
from tools.tibia_re_control_center.control_domain import ControlDomainService
from tools.tibia_re_control_center.current_client_fence import current_client_fence
from tools.tibia_re_control_center.model import ValidationError
from tools.tibia_re_control_center.vision_p2_trusted_composition import (
    ReviewedCapturePolicy,
    TrustedCaptureArtifact,
    VisionP2TrustedComposition,
)

_CURRENT_CLIENT_FENCE = current_client_fence()

from tools.tibia_re_vision.capture_edge import (
    CaptureEdgeError,
    PixelRegion,
    RuntimeBinding,
    WindowGeometry,
    _encode_rgb_png,
)

_EDGE_KEY = b"edge-auth-key-for-tests-32-bytes!!"


def _binding(*, xid: int = 321) -> RuntimeBinding:
    return RuntimeBinding(
        provenance_ref="admission:test",
        runtime_id="synology:kasm:edge-runtime",
        target_container="otclient-track-a-kasmvnc",
        display=":1",
        pid=123,
        process_start_ticks=456,
        xid=xid,
        client_version=_CURRENT_CLIENT_FENCE.version,
        client_size=_CURRENT_CLIENT_FENCE.size,
        client_sha256=_CURRENT_CLIENT_FENCE.sha256,
        observed_monotonic_ns=1_000,
        runtime_access="read_only",
        target_uniqueness="PROVEN",
    )


def _policy() -> ReviewedCapturePolicy:
    return ReviewedCapturePolicy(
        policy_id="fixture-login-mask-v1",
        expected_width=2,
        expected_height=1,
        secret_regions=(PixelRegion(0, 0, 1, 1),),
    )


class _FrameSource:
    def __init__(self, binding: RuntimeBinding, *, mutate_binding: bool = False) -> None:
        self.binding = binding
        self.mutate_binding = mutate_binding
        self.capture_calls = 0

    def geometry(self, _binding_value: RuntimeBinding) -> WindowGeometry:
        return WindowGeometry(0, 0, 2, 1)

    def capture_rgb(self, _binding_value: RuntimeBinding, _geometry: WindowGeometry) -> bytes:
        self.capture_calls += 1
        if self.mutate_binding:
            object.__setattr__(self.binding, "xid", self.binding.xid + 1)
        return bytes((9, 8, 7, 1, 2, 3))


@contextmanager
def _service(root: str, composition: VisionP2TrustedComposition):
    service = ControlDomainService(root)
    runtime = composition.attach(service)
    try:
        yield service, runtime
    finally:
        service.store.close()


class TrustedCompositionTests(unittest.TestCase):
    def test_composition_is_not_a_control_domain_request_constructor_parameter(self) -> None:
        self.assertNotIn("trusted_vision_p2_composition", inspect.signature(ControlDomainService.__init__).parameters)
        with tempfile.TemporaryDirectory() as raw:
            service = ControlDomainService(raw)
            try:
                service.agent.ensure_session("session-used")
                with self.assertRaises(ValidationError) as late:
                    VisionP2TrustedComposition(capture_policy=_policy()).attach(service)
                self.assertEqual("VISION_P2_COMPOSITION_LATE_ATTACH", late.exception.code)
            finally:
                service.store.close()

    def test_default_composition_allows_admission_only_zero_contract_resolver(self) -> None:
        composition = VisionP2TrustedComposition()
        with tempfile.TemporaryDirectory() as raw:
            with _service(raw, composition) as (service, runtime):
                agent = service.agent
                now_ms = 1_000_000
                agent._now_epoch_ms = lambda: now_ms
                agent.submit_task(read_only_task())
                admission = admit_read_only_runtime(
                    _admission_observation(now_ms),
                    now_epoch_ms=now_ms,
                    max_age_ms=15_000,
                )
                binding = RuntimeSignalBinding(
                    session_id="session-edge-1",
                    run_id="run-edge-1",
                    runtime_id=admission.runtime_namespace,
                    runtime_instance_id="runtime-instance-admission-only",
                    runtime_binding_sha256=admission.runtime_binding_sha256,
                )
                resolver = RuntimeSignalResolver(
                    current_binding=binding,
                    reviewed_contracts=(),
                    monotonic_ns=lambda: 1_000,
                    max_age_ns=100,
                    clock_domain_id="clock:control-center",
                )
                authority = agent._issue_read_only_runtime_authority(
                    "session-edge-1", admission,
                    runtime_signal_resolver=resolver,
                    runtime_signal_binding=binding,
                )
                agent.bind_read_only_runtime("session-edge-1", authority)
                runtime.ingest_edge_observation({
                    "schema": "otclient.local-agent.edge-observation.v1",
                    "session_id": "session-edge-1",
                    "run_id": "run-edge-1",
                    "edge_instance_id": "edge-admission-only",
                    "observed_epoch_ms": now_ms,
                    "heartbeat_epoch_ms": now_ms,
                    "capture": None,
                    "runtime": None,
                })
                snapshot = agent.snapshot("session-edge-1")
                self.assertTrue(snapshot["edge"]["current"])
                self.assertEqual("UNKNOWN", snapshot["edge"]["runtime"]["status"])
                self.assertFalse(snapshot["edge"]["runtime"]["current"])
                with self.assertRaises(ValueError):
                    resolver.bind_reviewed_source(producer_id="unreviewed", contract_id="unreviewed")

    def test_default_composition_rejects_nonempty_runtime_resolver(self) -> None:
        composition = VisionP2TrustedComposition()
        with tempfile.TemporaryDirectory() as raw:
            with _service(raw, composition) as (service, _runtime):
                agent = service.agent
                now_ms = 1_000_000
                agent._now_epoch_ms = lambda: now_ms
                agent.submit_task(read_only_task())
                admission = admit_read_only_runtime(_admission_observation(now_ms), now_epoch_ms=now_ms, max_age_ms=15_000)
                binding = RuntimeSignalBinding(session_id="session-edge-1", run_id="run-edge-1", runtime_id=admission.runtime_namespace, runtime_instance_id="runtime-instance-nonempty", runtime_binding_sha256=admission.runtime_binding_sha256)
                resolver = _signal_resolver(binding)
                with self.assertRaises(ValidationError) as mismatch:
                    agent._issue_read_only_runtime_authority("session-edge-1", admission, runtime_signal_resolver=resolver, runtime_signal_binding=binding)
                self.assertEqual("EDGE_RUNTIME_COMPOSITION_MISMATCH", mismatch.exception.code)

    def test_capture_policy_and_root_are_composition_owned_and_secret_safety_is_recomputed(self) -> None:
        current = _binding()
        source = _FrameSource(current)
        composition = VisionP2TrustedComposition(capture_policy=_policy())
        with tempfile.TemporaryDirectory() as raw:
            with _service(raw, composition) as (service, runtime):
                edge = runtime.build_capture_edge(
                    binding_reader=lambda: current,
                    frame_source=source,
                    monotonic_ns=iter((1_100, 1_200, 1_300, 1_400)).__next__,
                )
                parameters = inspect.signature(edge.capture).parameters
                self.assertNotIn("secret_policy", parameters)
                self.assertNotIn("evidence_root", parameters)
                evidence = edge.capture(run_id="run-1", max_binding_age_ns=500)
                self.assertFalse(hasattr(evidence, "secret_safe"))
                safe = runtime.validate_capture(
                    evidence,
                    current_binding=current,
                    now_ns=1_450,
                    max_age_ns=500,
                )
                self.assertTrue(safe.secret_safe)
                self.assertEqual(service.store.control_dir / "vision-p2-captures", safe.path.parent)
                self.assertEqual(evidence.full_frame.sha256, safe.sha256)

    def test_forged_unmasked_png_fails_recomputed_secret_mask(self) -> None:
        current = _binding()
        composition = VisionP2TrustedComposition(capture_policy=_policy())
        with tempfile.TemporaryDirectory() as raw:
            with _service(raw, composition) as (service, runtime):
                edge = runtime.build_capture_edge(
                    binding_reader=lambda: current,
                    frame_source=_FrameSource(current),
                    monotonic_ns=iter((1_100, 1_200, 1_300, 1_400)).__next__,
                )
                evidence = edge.capture(run_id="run-1", max_binding_age_ns=500)
                payload = _encode_rgb_png(2, 1, bytes((9, 8, 7, 1, 2, 3)))
                digest = hashlib.sha256(payload).hexdigest()
                path = service.store.control_dir / "vision-p2-captures" / f"{digest}.png"
                path.write_bytes(payload)
                forged = replace(
                    evidence,
                    full_frame=TrustedCaptureArtifact(path=path, sha256=digest),
                )
                with self.assertRaisesRegex(CaptureEdgeError, "CAPTURE_SECRET_MASK_INVALID"):
                    runtime.validate_capture(
                        forged,
                        current_binding=current,
                        now_ns=1_450,
                        max_age_ns=500,
                    )

    def test_slow_capture_and_same_object_binding_mutation_fail_before_persistence(self) -> None:
        composition = VisionP2TrustedComposition(capture_policy=_policy())
        with tempfile.TemporaryDirectory() as raw:
            with _service(raw, composition) as (service, runtime):
                current = _binding()
                slow = runtime.build_capture_edge(
                    binding_reader=lambda: current,
                    frame_source=_FrameSource(current),
                    monotonic_ns=iter((1_100, 1_200, 2_000, 2_100)).__next__,
                )
                with self.assertRaisesRegex(CaptureEdgeError, "RUNTIME_BINDING_STALE"):
                    slow.capture(run_id="run-slow", max_binding_age_ns=500)
                self.assertEqual([], list((service.store.control_dir / "vision-p2-captures").iterdir()))

                current = _binding()
                drift = runtime.build_capture_edge(
                    binding_reader=lambda: current,
                    frame_source=_FrameSource(current, mutate_binding=True),
                    monotonic_ns=iter((1_100, 1_200, 1_300, 1_400)).__next__,
                )
                with self.assertRaisesRegex(CaptureEdgeError, "RUNTIME_BINDING_CHANGED"):
                    drift.capture(run_id="run-drift", max_binding_age_ns=500)
                self.assertEqual([], list((service.store.control_dir / "vision-p2-captures").iterdir()))

    def test_raw_edge_capture_cannot_self_assert_secret_safe(self) -> None:
        composition = VisionP2TrustedComposition()
        with tempfile.TemporaryDirectory() as raw:
            with _service(raw, composition) as (service, _runtime):
                with self.assertRaises(ValidationError) as rejected:
                    service.agent.edge.accept(
                        {"capture": {"status": "AVAILABLE", "secret_safe": True}},
                        now_epoch_ms=1_000,
                        expected_session_id="session-1",
                        expected_run_id="run-1",
                    )
                self.assertEqual("EDGE_CAPTURE_TRUSTED_EVIDENCE_REQUIRED", rejected.exception.code)

    def test_validated_capture_must_match_current_runtime_admission_identity(self) -> None:
        composition = VisionP2TrustedComposition(
            runtime_authority_configuration=_authority_configuration(),
            capture_policy=_policy(),
        )
        now_ms = 1_000_000
        with tempfile.TemporaryDirectory() as raw:
            with _service(raw, composition) as (service, runtime):
                agent = service.agent
                agent._now_epoch_ms = lambda: now_ms
                agent.submit_task(read_only_task())
                admission = admit_read_only_runtime(
                    _admission_observation(now_ms),
                    now_epoch_ms=now_ms,
                    max_age_ms=15_000,
                )
                signal_binding = RuntimeSignalBinding(
                    session_id="session-edge-1",
                    run_id="run-edge-1",
                    runtime_id=admission.runtime_namespace,
                    runtime_instance_id="runtime-instance-1",
                    runtime_binding_sha256=admission.runtime_binding_sha256,
                )
                resolver = _signal_resolver(signal_binding)
                authority = agent._issue_read_only_runtime_authority(
                    "session-edge-1",
                    admission,
                    runtime_signal_resolver=resolver,
                    runtime_signal_binding=signal_binding,
                )
                agent.bind_read_only_runtime("session-edge-1", authority)
                runtime.ingest_edge_observation(
                    {
                        "schema": "otclient.local-agent.edge-observation.v1",
                        "session_id": "session-edge-1",
                        "run_id": "run-edge-1",
                        "edge_instance_id": "edge-instance-1",
                        "observed_epoch_ms": now_ms,
                        "heartbeat_epoch_ms": now_ms,
                        "capture": None,
                        "runtime": None,
                    }
                )
                current = _binding()
                edge = runtime.build_capture_edge(
                    binding_reader=lambda: current,
                    frame_source=_FrameSource(current),
                    monotonic_ns=iter((1_100, 1_200, 1_300, 1_400)).__next__,
                )
                evidence = edge.capture(run_id="run-edge-1", max_binding_age_ns=500)
                accepted = runtime.ingest_capture(
                    "session-edge-1",
                    evidence,
                    current_binding=current,
                    now_ns=1_450,
                    max_age_ns=500,
                )
                self.assertTrue(accepted["edge"]["capture"]["current"])

                wrong = _binding(xid=322)
                wrong_edge = runtime.build_capture_edge(
                    binding_reader=lambda: wrong,
                    frame_source=_FrameSource(wrong),
                    monotonic_ns=iter((1_101, 1_201, 1_301, 1_401)).__next__,
                )
                wrong_evidence = wrong_edge.capture(run_id="run-edge-1", max_binding_age_ns=500)
                with self.assertRaises(ValidationError) as mismatch:
                    runtime.ingest_capture(
                        "session-edge-1",
                        wrong_evidence,
                        current_binding=wrong,
                        now_ns=1_451,
                        max_age_ns=500,
                    )
                self.assertEqual("CAPTURE_RUNTIME_ADMISSION_MISMATCH", mismatch.exception.code)

    def test_replay_ledger_survives_store_restart_and_rejects_a_b_a(self) -> None:
        composition = VisionP2TrustedComposition()
        signer = EdgeTransportSigner(
            local_peer_id="edge-peer",
            local_auth_key=_EDGE_KEY,
            session_id="session-replay",
            run_id="run-replay",
        )
        packet_a = signer.seal(
            kind=EdgeFrameKind.HEARTBEAT,
            connection_id="connection-a",
            connection_generation="generation-a",
            sequence=1,
            sent_epoch_ms=1_000,
            payload={"edge_state": "ONLINE"},
        )
        packet_b = signer.seal(
            kind=EdgeFrameKind.HEARTBEAT,
            connection_id="connection-b",
            connection_generation="generation-b",
            sequence=1,
            sent_epoch_ms=1_001,
            payload={"edge_state": "ONLINE"},
        )
        with tempfile.TemporaryDirectory() as raw:
            with _service(raw, composition) as (_service_one, runtime_one):
                verifier_a = runtime_one.durable_edge_verifier(
                    session_id="session-replay",
                    run_id="run-replay",
                    expected_peer_id="edge-peer",
                    expected_peer_auth_key=_EDGE_KEY,
                    expected_connection_id="connection-a",
                )
                self.assertEqual("connection-a", verifier_a.verify(packet_a, now_epoch_ms=1_000).connection_id)
                verifier_b = runtime_one.durable_edge_verifier(
                    session_id="session-replay",
                    run_id="run-replay",
                    expected_peer_id="edge-peer",
                    expected_peer_auth_key=_EDGE_KEY,
                    expected_connection_id="connection-b",
                )
                self.assertEqual("connection-b", verifier_b.verify(packet_b, now_epoch_ms=1_001).connection_id)

            with _service(raw, composition) as (_service_two, runtime_two):
                replay = runtime_two.durable_edge_verifier(
                    session_id="session-replay",
                    run_id="run-replay",
                    expected_peer_id="edge-peer",
                    expected_peer_auth_key=_EDGE_KEY,
                    expected_connection_id="connection-a",
                )
                with self.assertRaises(ValidationError) as rejected:
                    replay.verify(packet_a, now_epoch_ms=1_002)
                self.assertEqual("EDGE_EPOCH_REUSE_REJECTED", rejected.exception.code)

    def test_malformed_persisted_replay_state_fails_closed(self) -> None:
        composition = VisionP2TrustedComposition()
        with tempfile.TemporaryDirectory() as raw:
            with _service(raw, composition) as (service, runtime):
                verifier = runtime.durable_edge_verifier(
                    session_id="session-bad",
                    run_id="run-bad",
                    expected_peer_id="edge-peer",
                    expected_peer_auth_key=_EDGE_KEY,
                    expected_connection_id="connection-bad",
                )
                with service.store._transaction("test_corrupt_replay"):
                    service.store._db.execute(
                        "INSERT OR REPLACE INTO meta(key, value) VALUES(?, ?)",
                        (verifier._meta_key, "{not-json"),
                    )
                signer = EdgeTransportSigner(
                    local_peer_id="edge-peer",
                    local_auth_key=_EDGE_KEY,
                    session_id="session-bad",
                    run_id="run-bad",
                )
                packet = signer.seal(
                    kind=EdgeFrameKind.HEARTBEAT,
                    connection_id="connection-bad",
                    connection_generation="generation-bad",
                    sequence=1,
                    sent_epoch_ms=1_000,
                    payload={"edge_state": "ONLINE"},
                )
                with self.assertRaises(ValidationError) as rejected:
                    verifier.verify(packet, now_epoch_ms=1_000)
                self.assertEqual("EDGE_REPLAY_STATE_INVALID", rejected.exception.code)


if __name__ == "__main__":
    unittest.main()
