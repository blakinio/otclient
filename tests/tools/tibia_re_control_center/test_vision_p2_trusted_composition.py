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
from tools.tibia_re_control_center.agent_reconcile import ReconciledState
from tools.tibia_re_control_center.agent_runtime_admission import (
    admit_read_only_runtime,
)
from tools.tibia_re_control_center.agent_runtime_signals import (
    RuntimeSignalBinding,
    RuntimeSignalSample,
)
from tools.tibia_re_control_center.agent_vision import (
    QWEN_VISION_PROFILE_ID,
    VisionObservation,
)
from tools.tibia_re_control_center.control_domain import ControlDomainService
from tools.tibia_re_control_center.model import ValidationError
from tools.tibia_re_control_center.vision_p2_trusted_composition import (
    ReviewedCapturePolicy,
    TrustedCaptureArtifact,
    VisionP2TrustedComposition,
)
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
        client_version="15.32.be4f48",
        client_size=52_105_824,
        client_sha256="552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1",
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


def _visual(capture: dict[str, object], *, screen_class: str = "WORLD_VISUAL") -> VisionObservation:
    return VisionObservation(
        screen_class=screen_class,
        visible_text=(),
        confidence=None,
        model_profile_id=QWEN_VISION_PROFILE_ID,
        evidence_ref=str(capture["artifact_ref"]),
        capture_sha256=str(capture["sha256"]),
    )


def _admitted_capture(service: ControlDomainService, runtime, *, now_ms: int = 1_000_000):
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
    capture_edge = runtime.build_capture_edge(
        binding_reader=lambda: current,
        frame_source=_FrameSource(current),
        monotonic_ns=iter((1_100, 1_200, 1_300, 1_400)).__next__,
    )
    capture_evidence = capture_edge.capture(run_id="run-edge-1", max_binding_age_ns=500)
    snapshot = runtime.ingest_capture(
        "session-edge-1",
        capture_evidence,
        current_binding=current,
        now_ns=1_450,
        max_age_ns=500,
    )
    return agent, resolver, signal_binding, snapshot["edge"]["capture"]


def _reviewed_world_signal(agent, resolver, signal_binding):
    source = resolver.bind_reviewed_source(
        producer_id="fixture-causal-producer",
        contract_id="fixture-causal-v1",
    )
    signal = resolver.ingest(
        source,
        RuntimeSignalSample(
            binding=signal_binding,
            clock_domain_id="clock:control-center",
            observed_monotonic_ns=950,
            source_state="WORLD_ENTERED",
            evidence_refs=("producer:evidence-current",),
        ),
    )
    if signal is None:
        raise AssertionError("reviewed signal fixture was rejected")
    agent.ingest_runtime_signal("session-edge-1", signal)
    return signal

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

    def test_current_reviewed_runtime_and_matching_visual_persist_world_confirmation(self) -> None:
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
                capture_edge = runtime.build_capture_edge(
                    binding_reader=lambda: current,
                    frame_source=_FrameSource(current),
                    monotonic_ns=iter((1_100, 1_200, 1_300, 1_400)).__next__,
                )
                capture_evidence = capture_edge.capture(run_id="run-edge-1", max_binding_age_ns=500)
                snapshot = runtime.ingest_capture(
                    "session-edge-1",
                    capture_evidence,
                    current_binding=current,
                    now_ns=1_450,
                    max_age_ns=500,
                )
                capture = snapshot["edge"]["capture"]
                self.assertTrue(capture["current"])

                source = resolver.bind_reviewed_source(
                    producer_id="fixture-causal-producer",
                    contract_id="fixture-causal-v1",
                )
                signal = resolver.ingest(
                    source,
                    RuntimeSignalSample(
                        binding=signal_binding,
                        clock_domain_id="clock:control-center",
                        observed_monotonic_ns=950,
                        source_state="WORLD_ENTERED",
                        evidence_refs=("producer:evidence-current",),
                    ),
                )
                self.assertIsNotNone(signal)
                updated = agent.ingest_runtime_signal("session-edge-1", signal)
                self.assertTrue(updated["edge"]["runtime"]["current"])

                self.assertTrue(
                    hasattr(runtime, "reconcile_vision"),
                    "trusted composition must expose the Wave 2 reconciliation seam",
                )
                result = runtime.reconcile_vision("session-edge-1", _visual(capture))
                self.assertEqual(ReconciledState.WORLD_CONFIRMED, result.state)
                self.assertEqual(tuple(capture["artifact_ref"] for _ in range(1)), result.visual_evidence_refs)
                self.assertEqual((signal.signal_ref,), result.runtime_evidence_refs)

                event = next(
                    item
                    for item in reversed(agent._events_for("session-edge-1"))
                    if item["kind"] == "VISION_RECONCILED"
                )
                self.assertEqual("WORLD_CONFIRMED", event["payload"]["state"])
                self.assertEqual([signal.signal_ref], event["payload"]["runtime_evidence_refs"])
                self.assertFalse(event["payload"]["physical_effect"])
                self.assertEqual(0, agent.snapshot("session-edge-1")["physical_action_count"])

    def test_world_visual_without_current_runtime_stays_unknown(self) -> None:
        composition = VisionP2TrustedComposition(
            runtime_authority_configuration=_authority_configuration(),
            capture_policy=_policy(),
        )
        with tempfile.TemporaryDirectory() as raw:
            with _service(raw, composition) as (service, runtime):
                agent, _resolver, _binding_value, capture = _admitted_capture(service, runtime)
                self.assertFalse(agent.snapshot("session-edge-1")["edge"]["runtime"]["current"])
                result = runtime.reconcile_vision("session-edge-1", _visual(capture))
                self.assertEqual(ReconciledState.UNKNOWN, result.state)
                self.assertEqual((), result.runtime_evidence_refs)
                event = next(
                    item
                    for item in reversed(agent._events_for("session-edge-1"))
                    if item["kind"] == "VISION_RECONCILED"
                )
                self.assertFalse(event["payload"]["runtime_current"])
                self.assertEqual(0, agent.snapshot("session-edge-1")["physical_action_count"])

    def test_stale_reviewed_runtime_cannot_promote_world_visual(self) -> None:
        composition = VisionP2TrustedComposition(
            runtime_authority_configuration=_authority_configuration(),
            capture_policy=_policy(),
        )
        with tempfile.TemporaryDirectory() as raw:
            with _service(raw, composition) as (service, runtime):
                agent, resolver, signal_binding, capture = _admitted_capture(service, runtime)
                signal = _reviewed_world_signal(agent, resolver, signal_binding)
                self.assertTrue(agent.snapshot("session-edge-1")["edge"]["runtime"]["current"])
                resolver._monotonic_ns = lambda: 1_200
                self.assertFalse(agent.snapshot("session-edge-1")["edge"]["runtime"]["current"])
                result = runtime.reconcile_vision("session-edge-1", _visual(capture))
                self.assertEqual(ReconciledState.UNKNOWN, result.state)
                self.assertEqual((), result.runtime_evidence_refs)
                self.assertNotIn(signal.signal_ref, result.runtime_evidence_refs)
                event = next(
                    item
                    for item in reversed(agent._events_for("session-edge-1"))
                    if item["kind"] == "VISION_RECONCILED"
                )
                self.assertFalse(event["payload"]["runtime_current"])

    def test_visual_runtime_disagreement_persists_conflict(self) -> None:
        composition = VisionP2TrustedComposition(
            runtime_authority_configuration=_authority_configuration(),
            capture_policy=_policy(),
        )
        with tempfile.TemporaryDirectory() as raw:
            with _service(raw, composition) as (service, runtime):
                agent, resolver, signal_binding, capture = _admitted_capture(service, runtime)
                signal = _reviewed_world_signal(agent, resolver, signal_binding)
                result = runtime.reconcile_vision(
                    "session-edge-1",
                    _visual(capture, screen_class="LOGIN_SCREEN"),
                )
                self.assertEqual(ReconciledState.CONFLICT, result.state)
                self.assertEqual((signal.signal_ref,), result.runtime_evidence_refs)
                event = next(
                    item
                    for item in reversed(agent._events_for("session-edge-1"))
                    if item["kind"] == "VISION_RECONCILED"
                )
                self.assertEqual("CONFLICT", event["payload"]["state"])
                self.assertTrue(event["payload"]["runtime_current"])
                self.assertFalse(event["payload"]["physical_effect"])

    def test_visual_from_noncurrent_capture_is_rejected_before_persistence(self) -> None:
        composition = VisionP2TrustedComposition(
            runtime_authority_configuration=_authority_configuration(),
            capture_policy=_policy(),
        )
        with tempfile.TemporaryDirectory() as raw:
            with _service(raw, composition) as (service, runtime):
                agent, _resolver, _binding_value, capture = _admitted_capture(service, runtime)
                before = len(agent._events_for("session-edge-1"))
                forged = replace(_visual(capture), capture_sha256="0" * 64)
                with self.assertRaises(ValidationError) as rejected:
                    runtime.reconcile_vision("session-edge-1", forged)
                self.assertEqual("VISION_CAPTURE_BINDING_MISMATCH", rejected.exception.code)
                self.assertEqual(before, len(agent._events_for("session-edge-1")))
                parameters = inspect.signature(runtime.reconcile_vision).parameters
                self.assertNotIn("runtime", parameters)
                self.assertNotIn("resolver", parameters)

    def test_persisted_reconciliation_survives_restart_without_restoring_runtime_authority(self) -> None:
        composition = VisionP2TrustedComposition(
            runtime_authority_configuration=_authority_configuration(),
            capture_policy=_policy(),
        )
        with tempfile.TemporaryDirectory() as raw:
            with _service(raw, composition) as (service_one, runtime_one):
                agent_one, resolver, signal_binding, capture = _admitted_capture(service_one, runtime_one)
                signal = _reviewed_world_signal(agent_one, resolver, signal_binding)
                result = runtime_one.reconcile_vision("session-edge-1", _visual(capture))
                self.assertEqual(ReconciledState.WORLD_CONFIRMED, result.state)
                self.assertEqual((signal.signal_ref,), result.runtime_evidence_refs)

            with _service(raw, composition) as (service_two, runtime_two):
                persisted = next(
                    item
                    for item in reversed(service_two.agent._events_for("session-edge-1"))
                    if item["kind"] == "VISION_RECONCILED"
                )
                self.assertEqual("WORLD_CONFIRMED", persisted["payload"]["state"])
                self.assertEqual([signal.signal_ref], persisted["payload"]["runtime_evidence_refs"])
                self.assertTrue(persisted["payload"]["runtime_current"])
                snapshot = service_two.agent.snapshot("session-edge-1")
                self.assertFalse(snapshot["edge"]["current"])
                self.assertFalse(snapshot["edge"]["runtime"]["current"])
                self.assertEqual("NONE", snapshot["official_client_access"])
                with self.assertRaises(ValidationError) as rejected:
                    runtime_two.reconcile_vision("session-edge-1", _visual(capture))
                self.assertEqual("VISION_EDGE_CURRENT_REQUIRED", rejected.exception.code)

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
