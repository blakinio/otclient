import tempfile
import unittest
from contextlib import suppress
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

from tools.tibia_re_control_center.agent_edge_bridge import (
    ReviewedRuntimeAuthorityConfiguration,
)
from tools.tibia_re_control_center.agent_protocol import (
    ClientIdentity,
    NamedAgentAction,
    TaskEnvelope,
)
from tools.tibia_re_control_center.agent_reconcile import (
    RuntimeEvidenceClass,
    RuntimeObservation,
)
from tools.tibia_re_control_center.agent_runtime_admission import (
    ReadOnlyRuntimeAdmission,
    admit_read_only_runtime,
)
from tools.tibia_re_control_center.agent_runtime_signals import (
    ReviewedRuntimeSignalContract,
    ReviewedRuntimeSignalRule,
    RuntimeSignalBinding,
    RuntimeSignalEvidence,
    RuntimeSignalResolver,
    RuntimeSignalSample,
)
from tools.tibia_re_control_center.agent_session import AgentSessionCoordinator
from tools.tibia_re_control_center.canonical import sha256_jcs
from tools.tibia_re_control_center.control_ui import render_control_ui
from tools.tibia_re_control_center.execution import MutationCoordinator
from tools.tibia_re_control_center.fake import FakeAdapter, ManualClock
from tools.tibia_re_control_center.model import ValidationError
from tools.tibia_re_control_center.persistent_store import SQLitePersistentStore


def _reviewed_contract() -> ReviewedRuntimeSignalContract:
    return ReviewedRuntimeSignalContract(
        producer_id="fixture-causal-producer",
        contract_id="fixture-causal-v1",
        rules=(
            ReviewedRuntimeSignalRule(
                source_state="WORLD_ENTERED",
                runtime_state="IN_GAME",
                evidence_class=RuntimeEvidenceClass.REVIEWED_CAUSAL,
            ),
        ),
    )


def _signal_resolver(binding: RuntimeSignalBinding) -> RuntimeSignalResolver:
    return RuntimeSignalResolver(
        current_binding=binding,
        reviewed_contracts=(_reviewed_contract(),),
        monotonic_ns=lambda: 1_000,
        max_age_ns=100,
        clock_domain_id="clock:control-center",
    )


def _authority_configuration() -> ReviewedRuntimeAuthorityConfiguration:
    return ReviewedRuntimeAuthorityConfiguration(
        reviewed_contracts=(_reviewed_contract(),),
        clock_domain_id="clock:control-center",
        max_age_ns=100,
    )


def _admission_observation(now_ms: int) -> dict[str, object]:
    return {
        "schema": "otclient.local-agent.runtime-observation.v1",
        "track_id": "official-client-re",
        "task_id": "task-edge-1",
        "runtime_owner_task": "task-edge-1",
        "runtime_namespace": "synology:kasm:edge-runtime",
        "observed_at_epoch_ms": now_ms,
        "locator": {
            "runner": "synology-otclient-01",
            "remote_device": "Synology",
            "container": "otclient-track-a-kasmvnc",
            "container_gui_user": "kasm-user",
            "display": ":1",
            "observer_endpoint": "https://synology:6902/",
            "host_reachable": True,
            "container_running": True,
            "display_reachable": True,
        },
        "process": {
            "boot_id_sha256": "b" * 64,
            "pid": 123,
            "process_start_ticks": 456,
            "exe_path": "/home/kasm-user/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client",
            "display": ":1",
            "client_version": "15.32.75d4a0",
            "client_size": 52_105_824,
            "client_sha256": "d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a",
        },
        "window": {"xid": 321, "pid": 123, "display": ":1", "ownership_proven": True},
        "inventory": {
            "inventory_scope": "DECLARED_RUNTIME_NAMESPACE",
            "official_client_candidate_count": 1,
            "exact_client_candidate_count": 1,
            "mismatched_or_unverifiable_candidate_count": 0,
            "target_uniqueness": "PROVEN",
        },
        "safety": {
            "credentials_used": False,
            "gui_input_sent": False,
            "anti_idle_input_sent": False,
            "process_control_used": False,
            "process_memory_access_used": False,
            "network_payload_capture_used": False,
            "physical_action_count": 0,
        },
    }


def read_only_task() -> TaskEnvelope:
    return TaskEnvelope(
        schema="otclient.local-agent.task.v1",
        session_id="session-edge-1",
        task_id="task-edge-1",
        run_id="run-edge-1",
        idempotency_key="idem-edge-1",
        trusted_main_sha="a" * 40,
        client_identity=ClientIdentity("15.32.75d4a0", 52_105_824, "d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a"),
        objective="observe the admitted runtime edge without physical effects",
        allowed_actions=(NamedAgentAction.SCREENSHOT,),
        physical_action_budget=0,
        max_attempts=1,
        deadline_epoch_ms=4_000_000_000_000,
        runtime_access="read_only",
        required_evidence=("edge-heartbeat", "capture", "runtime"),
        secret_capability_ref=None,
    )


class AgentEdgeBridgeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.store = SQLitePersistentStore(self.root)
        self.clock = ManualClock()
        self.control = MutationCoordinator(
            FakeAdapter(self.clock, allow_mutation=True),
            self.store,
            self.clock,
            backend_epoch="edge-test",
        )
        self.agent = AgentSessionCoordinator(
            self.store,
            self.control,
            runtime_authority_configuration=_authority_configuration(),
        )
        self.now_ms = 1_000_000
        self.agent._now_epoch_ms = lambda: self.now_ms

    def tearDown(self) -> None:
        with suppress(Exception):
            self.store.close()
        self.temp.cleanup()

    def _admit_and_bind(self) -> tuple[ReadOnlyRuntimeAdmission, RuntimeSignalResolver, RuntimeSignalBinding]:
        admission = admit_read_only_runtime(
            _admission_observation(self.now_ms),
            now_epoch_ms=self.now_ms,
            max_age_ms=15_000,
        )
        binding = RuntimeSignalBinding(
            session_id="session-edge-1",
            run_id="run-edge-1",
            runtime_id=admission.runtime_namespace,
            runtime_instance_id="runtime-instance-1",
            runtime_binding_sha256=admission.runtime_binding_sha256,
        )
        resolver = _signal_resolver(binding)
        authority = self.agent._issue_read_only_runtime_authority(
            "session-edge-1",
            admission,
            runtime_signal_resolver=resolver,
            runtime_signal_binding=binding,
        )
        self.agent.bind_read_only_runtime(
            "session-edge-1",
            authority,
        )
        return admission, resolver, binding

    def _issue_authority(
        self,
        admission: ReadOnlyRuntimeAdmission,
        resolver: RuntimeSignalResolver,
        binding: RuntimeSignalBinding,
    ) -> object:
        return self.agent._issue_read_only_runtime_authority(
            "session-edge-1",
            admission,
            runtime_signal_resolver=resolver,
            runtime_signal_binding=binding,
        )

    def _reviewed_signal(
        self,
        resolver: RuntimeSignalResolver,
        binding: RuntimeSignalBinding,
    ) -> RuntimeSignalEvidence:
        source = resolver.bind_reviewed_source(
            producer_id="fixture-causal-producer",
            contract_id="fixture-causal-v1",
        )
        evidence = resolver.ingest(
            source,
            RuntimeSignalSample(
                binding=binding,
                clock_domain_id="clock:control-center",
                observed_monotonic_ns=950,
                source_state="WORLD_ENTERED",
                evidence_refs=("producer:evidence-current",),
            ),
        )
        self.assertIsNotNone(evidence)
        return evidence

    def test_caller_declared_read_only_and_fabricated_runtime_refs_do_not_become_current(self) -> None:
        self.agent.submit_task(read_only_task())

        with self.assertRaises(ValidationError) as fabricated:
            self.agent.ingest_edge_observation(self._edge_update(include_runtime=True))
        self.assertEqual("EDGE_RUNTIME_SIGNAL_REQUIRED", fabricated.exception.code)

        snapshot = self.agent.ingest_edge_observation(self._edge_update(include_runtime=False))
        self.assertFalse(snapshot["edge"]["current"] )
        self.assertEqual("RUNTIME_ADMISSION_REQUIRED", snapshot["edge"]["reason"] )
        self.assertEqual("NONE", snapshot["official_client_access"] )
        self.assertFalse(snapshot["edge"]["runtime"]["current"] )
        self.assertEqual(0, snapshot["physical_action_count"] )

    def test_preconnect_caller_minted_authority_is_rejected_before_any_live_edge_exists(self) -> None:
        self.agent.submit_task(read_only_task())
        admission = admit_read_only_runtime(
            _admission_observation(self.now_ms), now_epoch_ms=self.now_ms, max_age_ms=15_000
        )
        binding = RuntimeSignalBinding(
            session_id="session-edge-1",
            run_id="run-edge-1",
            runtime_id=admission.runtime_namespace,
            runtime_instance_id="runtime-instance-caller-minted",
            runtime_binding_sha256=admission.runtime_binding_sha256,
        )
        with self.assertRaises(ValidationError) as caller_minted:
            self.agent.bind_read_only_runtime(
                "session-edge-1",
                admission,
                runtime_signal_resolver=_signal_resolver(binding),
                runtime_signal_binding=binding,
            )
        self.assertEqual("EDGE_RUNTIME_AUTHORITY_REQUIRED", caller_minted.exception.code)
        self.assertEqual("NONE", self.agent.snapshot("session-edge-1")["official_client_access"])

    def test_composition_rejects_exact_resolver_with_unapproved_causal_contract(self) -> None:
        self.agent.submit_task(read_only_task())
        admission = admit_read_only_runtime(
            _admission_observation(self.now_ms), now_epoch_ms=self.now_ms, max_age_ms=15_000
        )
        binding = RuntimeSignalBinding(
            session_id="session-edge-1",
            run_id="run-edge-1",
            runtime_id=admission.runtime_namespace,
            runtime_instance_id="runtime-instance-unapproved",
            runtime_binding_sha256=admission.runtime_binding_sha256,
        )
        unapproved = RuntimeSignalResolver(
            current_binding=binding,
            reviewed_contracts=(
                ReviewedRuntimeSignalContract(
                    producer_id="caller-causal-producer",
                    contract_id="caller-causal-v1",
                    rules=(ReviewedRuntimeSignalRule(
                        source_state="CALLER_ASSERTED_IN_GAME",
                        runtime_state="IN_GAME",
                        evidence_class=RuntimeEvidenceClass.REVIEWED_CAUSAL,
                    ),),
                ),
            ),
            monotonic_ns=lambda: 1_000,
            max_age_ns=100,
            clock_domain_id="clock:control-center",
        )
        with self.assertRaises(ValidationError) as rejected:
            self._issue_authority(admission, unapproved, binding)
        self.assertEqual("EDGE_RUNTIME_COMPOSITION_MISMATCH", rejected.exception.code)
        self.assertEqual("NONE", self.agent.snapshot("session-edge-1")["official_client_access"])

    def test_expired_task_cannot_bind_ingest_or_remain_runtime_current(self) -> None:
        expiring_task = replace(read_only_task(), deadline_epoch_ms=self.now_ms + 1)
        self.agent.submit_task(expiring_task)
        _admission, resolver, binding = self._admit_and_bind()
        self.agent.ingest_edge_observation(self._edge_update())
        evidence = self._reviewed_signal(resolver, binding)

        self.now_ms += 1
        expired_snapshot = self.agent.snapshot("session-edge-1")
        self.assertEqual("NONE", expired_snapshot["official_client_access"])
        self.assertFalse(expired_snapshot["edge"]["current"])
        self.assertEqual("EDGE_TASK_DEADLINE_EXPIRED", expired_snapshot["edge"]["reason"])

        with self.assertRaises(ValidationError) as signal_rejected:
            self.agent.ingest_runtime_signal("session-edge-1", evidence)
        self.assertEqual("EDGE_TASK_DEADLINE_EXPIRED", signal_rejected.exception.code)
        with self.assertRaises(ValidationError) as edge_rejected:
            self.agent.ingest_edge_observation(self._edge_update(observed_epoch_ms=self.now_ms))
        self.assertEqual("EDGE_TASK_DEADLINE_EXPIRED", edge_rejected.exception.code)

        fresh_admission = admit_read_only_runtime(
            _admission_observation(self.now_ms), now_epoch_ms=self.now_ms, max_age_ms=15_000
        )
        fresh_binding = replace(
            binding,
            runtime_instance_id="runtime-instance-expired-bind",
            runtime_binding_sha256=fresh_admission.runtime_binding_sha256,
        )
        with self.assertRaises(ValidationError) as bind_rejected:
            self._issue_authority(fresh_admission, _signal_resolver(fresh_binding), fresh_binding)
        self.assertEqual("EDGE_TASK_DEADLINE_EXPIRED", bind_rejected.exception.code)

    def test_valid_admission_and_reviewed_signal_are_required_for_semantic_runtime(self) -> None:
        self.agent.submit_task(read_only_task())
        admission, resolver, binding = self._admit_and_bind()
        self.assertEqual(admission.runtime_binding_sha256, binding.runtime_binding_sha256)

        edge = self.agent.ingest_edge_observation(self._edge_update(include_runtime=False))
        self.assertTrue(edge["edge"]["current"] )
        self.assertEqual("READ_ONLY", edge["official_client_access"] )
        self.assertFalse(edge["edge"]["runtime"]["current"] )

        evidence = self._reviewed_signal(resolver, binding)
        updated = self.agent.ingest_runtime_signal("session-edge-1", evidence)
        self.assertTrue(updated["edge"]["runtime"]["current"] )
        self.assertEqual("IN_GAME", updated["edge"]["runtime"]["status"] )
        self.assertEqual([evidence.signal_ref], updated["edge"]["runtime"]["evidence_refs"] )
        self.assertEqual("REVIEWED_CAUSAL", updated["edge"]["runtime"]["evidence_class"] )
        self.assertEqual(0, updated["physical_action_count"] )

    def test_current_read_only_edge_observation_is_owner_visible_without_binding_physical_executor(self) -> None:
        self.agent.submit_task(read_only_task())
        _, resolver, binding = self._admit_and_bind()
        update = self._edge_update()
        self.agent.ingest_edge_observation(update)
        evidence = self._reviewed_signal(resolver, binding)
        self.agent.ingest_runtime_signal("session-edge-1", evidence)

        snapshot = self.agent.snapshot("session-edge-1")

        self.assertEqual("read_only", snapshot["runtime_access"])
        self.assertEqual("READ_ONLY", snapshot["official_client_access"])
        self.assertEqual("CONNECTED", snapshot["edge"]["availability"])
        self.assertTrue(snapshot["edge"]["current"])
        self.assertEqual(self.now_ms, snapshot["heartbeat_epoch_ms"])
        self.assertTrue(snapshot["edge"]["capture"]["current"])
        self.assertEqual("capture-edge-instance-1", snapshot["edge"]["capture"]["artifact_ref"])
        self.assertTrue(snapshot["edge"]["runtime"]["current"])
        self.assertEqual("IN_GAME", snapshot["edge"]["runtime"]["status"])
        self.assertEqual("REVIEWED_CAUSAL", snapshot["edge"]["runtime"]["evidence_class"])
        self.assertEqual("NULL", snapshot["executor"])
        self.assertEqual("NONE", snapshot["mutation_authority"])
        self.assertEqual(0, snapshot["physical_action_budget"])
        self.assertEqual(0, snapshot["physical_action_count"])

        capture = self.agent.owner_control("session-edge-1", "SCREENSHOT")
        self.assertEqual("AVAILABLE", capture["status"])
        self.assertEqual("capture-edge-instance-1", capture["capture"]["artifact_ref"])
        self.assertEqual(0, capture["session"]["physical_action_count"])
        self.assertEqual("NULL", capture["session"]["executor"])

    def _edge_update(
        self,
        *,
        edge_instance_id: str = "edge-instance-1",
        observed_epoch_ms: int | None = None,
        heartbeat_epoch_ms: int | None = None,
        include_capture: bool = True,
        include_runtime: bool = False,
    ) -> dict[str, object]:
        observed = self.now_ms if observed_epoch_ms is None else observed_epoch_ms
        heartbeat = observed if heartbeat_epoch_ms is None else heartbeat_epoch_ms
        return {
            "schema": "otclient.local-agent.edge-observation.v1",
            "session_id": "session-edge-1",
            "run_id": "run-edge-1",
            "edge_instance_id": edge_instance_id,
            "observed_epoch_ms": observed,
            "heartbeat_epoch_ms": heartbeat,
            "capture": None if not include_capture else {
                "status": "AVAILABLE",
                "artifact_ref": f"capture-{edge_instance_id}",
                "sha256": "c" * 64,
                "observed_epoch_ms": observed,
                "secret_safe": True,
            },
            "runtime": None if not include_runtime else {
                "status": "IN_GAME",
                "evidence_refs": [f"runtime-{edge_instance_id}"],
                "observed_epoch_ms": observed,
            },
        }

    def _restart(self) -> None:
        self.control.clean_shutdown()
        self.store.close()
        self.store = SQLitePersistentStore(self.root)
        self.clock = ManualClock()
        self.control = MutationCoordinator(
            FakeAdapter(self.clock, allow_mutation=True),
            self.store,
            self.clock,
            backend_epoch="edge-restart",
        )
        self.agent = AgentSessionCoordinator(
            self.store,
            self.control,
            runtime_authority_configuration=_authority_configuration(),
        )
        self.agent._now_epoch_ms = lambda: self.now_ms

    def test_heartbeat_loss_degrades_operational_state_and_stales_edge_evidence(self) -> None:
        self.agent.submit_task(read_only_task())
        self._admit_and_bind()
        self.agent.ingest_edge_observation(
            self._edge_update(heartbeat_epoch_ms=self.now_ms - 15_001)
        )

        snapshot = self.agent.snapshot("session-edge-1")

        self.assertEqual("DEGRADED", snapshot["operational_state"])
        self.assertEqual("CONNECTED", snapshot["edge"]["availability"])
        self.assertFalse(snapshot["edge"]["current"])
        self.assertEqual("HEARTBEAT_STALE", snapshot["edge"]["reason"])
        self.assertFalse(snapshot["edge"]["capture"]["current"])
        self.assertFalse(snapshot["edge"]["runtime"]["current"])
        self.assertEqual("NONE", snapshot["official_client_access"])
        self.assertEqual("NULL", snapshot["executor"])
        self.assertEqual(0, snapshot["physical_action_count"])

        capture = self.agent.owner_control("session-edge-1", "SCREENSHOT")
        self.assertEqual("UNAVAILABLE", capture["status"])
        self.assertEqual(0, capture["session"]["physical_action_count"])

    def test_disconnect_degrades_and_fresh_reconnect_does_not_replay_old_evidence(self) -> None:
        self.agent.submit_task(read_only_task())
        self._admit_and_bind()
        self.agent.ingest_edge_observation(self._edge_update())

        disconnected = self.agent.edge_disconnected(
            "session-edge-1",
            edge_instance_id="edge-instance-1",
        )
        self.assertEqual("DEGRADED", disconnected["operational_state"])
        self.assertEqual("DISCONNECTED", disconnected["edge"]["availability"])
        self.assertFalse(disconnected["edge"]["current"])
        self.assertFalse(disconnected["edge"]["capture"]["current"])

        self.now_ms += 1
        heartbeat_only = self.agent.ingest_edge_observation(
            self._edge_update(
                edge_instance_id="edge-instance-2",
                include_capture=False,
            )
        )
        self.assertEqual("DEGRADED", heartbeat_only["operational_state"])
        self.assertEqual("CONNECTED", heartbeat_only["edge"]["availability"])
        self.assertFalse(heartbeat_only["edge"]["current"])
        self.assertEqual("RUNTIME_ADMISSION_REQUIRED", heartbeat_only["edge"]["reason"])
        self.assertFalse(heartbeat_only["edge"]["capture"]["current"])
        self.assertFalse(heartbeat_only["edge"]["runtime"]["current"])
        self.assertIsNone(heartbeat_only["edge"]["capture"]["artifact_ref"])

        rebound = self._admit_and_bind()[0]
        self.assertEqual("read_only", rebound.runtime_access)
        after_admission = self.agent.snapshot("session-edge-1")
        self.assertEqual("RUNNING", after_admission["operational_state"])
        self.assertTrue(after_admission["edge"]["current"])

        self.now_ms += 1
        refreshed = self.agent.ingest_edge_observation(
            self._edge_update(edge_instance_id="edge-instance-2")
        )
        self.assertTrue(refreshed["edge"]["capture"]["current"])
        self.assertEqual("capture-edge-instance-2", refreshed["edge"]["capture"]["artifact_ref"])
        self.assertEqual(0, refreshed["physical_action_count"])

    def test_disconnect_rejects_replayed_observation_even_inside_freshness_window(self) -> None:
        self.agent.submit_task(read_only_task())
        self._admit_and_bind()
        original = self._edge_update()
        self.agent.ingest_edge_observation(original)
        self.agent.edge_disconnected("session-edge-1", edge_instance_id="edge-instance-1")

        with self.assertRaises(ValidationError) as replayed:
            self.agent.ingest_edge_observation(original)
        self.assertEqual("EDGE_OBSERVATION_REPLAY", getattr(replayed.exception, "code", None))
        snapshot = self.agent.snapshot("session-edge-1")
        self.assertEqual("DISCONNECTED", snapshot["edge"]["availability"])
        self.assertFalse(snapshot["edge"]["current"])

    def test_connected_edge_instance_cannot_be_replaced_without_disconnect(self) -> None:
        self.agent.submit_task(read_only_task())
        self._admit_and_bind()
        self.agent.ingest_edge_observation(self._edge_update())
        self.now_ms += 1

        with self.assertRaises(ValidationError) as replaced_error:
            self.agent.ingest_edge_observation(self._edge_update(edge_instance_id="edge-instance-2"))
        self.assertEqual("EDGE_BINDING_MISMATCH", getattr(replaced_error.exception, "code", None))
        snapshot = self.agent.snapshot("session-edge-1")
        self.assertEqual("edge-instance-1", snapshot["edge"]["edge_instance_id"])
        self.assertTrue(snapshot["edge"]["current"])

    def test_restart_marks_persisted_edge_evidence_disconnected_until_fresh_observation(self) -> None:
        self.agent.submit_task(read_only_task())
        self._admit_and_bind()
        self.agent.ingest_edge_observation(self._edge_update())
        before = self.agent.snapshot("session-edge-1")
        self.assertTrue(before["edge"]["current"])

        self._restart()
        restarted = self.agent.snapshot("session-edge-1")

        self.assertEqual("PAUSED_AUTHORITY", restarted["operational_state"])
        self.assertEqual("DISCONNECTED", restarted["edge"]["availability"])
        self.assertFalse(restarted["edge"]["current"])
        self.assertEqual("EDGE_DISCONNECTED", restarted["edge"]["reason"])
        self.assertFalse(restarted["edge"]["capture"]["current"])
        self.assertEqual("capture-edge-instance-1", restarted["edge"]["capture"]["artifact_ref"])
        self.assertEqual("NULL", restarted["executor"])
        self.assertEqual(0, restarted["physical_action_count"])

        stale_capture = self.agent.owner_control("session-edge-1", "SCREENSHOT")
        self.assertEqual("UNAVAILABLE", stale_capture["status"])

        self.now_ms += 1
        without_admission = self.agent.ingest_edge_observation(
            self._edge_update(edge_instance_id="edge-instance-2")
        )
        self.assertFalse(without_admission["edge"]["current"])
        self.assertEqual("RUNTIME_ADMISSION_REQUIRED", without_admission["edge"]["reason"])
        self.assertEqual("PAUSED_AUTHORITY", without_admission["operational_state"])

        self._admit_and_bind()
        fresh = self.agent.snapshot("session-edge-1")
        self.assertTrue(fresh["edge"]["current"])
        self.assertEqual("PAUSED_AUTHORITY", fresh["operational_state"])
        self.assertEqual(0, fresh["physical_action_count"])

    def test_owner_stop_dominates_fresh_edge_updates(self) -> None:
        self.agent.submit_task(read_only_task())
        self._admit_and_bind()
        self.agent.ingest_edge_observation(self._edge_update())
        stopped = self.agent.owner_control("session-edge-1", "STOP")
        self.assertEqual("STOPPED", stopped["status"])

        self.now_ms += 1
        updated = self.agent.ingest_edge_observation(self._edge_update())
        self.assertEqual("STOPPED", updated["operational_state"])
        self.assertTrue(updated["stop_latched"])
        self.assertTrue(updated["edge"]["current"])
        self.assertEqual(0, updated["physical_action_count"])
        self.assertEqual("NULL", updated["executor"])

    def test_edge_observation_rejects_unadmitted_wrong_run_future_and_unsafe_capture_without_persisting(self) -> None:
        baseline = self.agent.ensure_session("session-edge-1")
        before_seq = baseline.last_event_seq
        with self.assertRaises(ValidationError) as unadmitted:
            self.agent.ingest_edge_observation(self._edge_update())
        self.assertIn("EDGE_RUNTIME_NOT_ADMITTED", str(getattr(unadmitted.exception, "code", "")))
        self.assertEqual(before_seq, self.agent.snapshot("session-edge-1")["last_event_seq"])

        self.agent.submit_task(read_only_task())
        accepted_seq = self.agent.snapshot("session-edge-1")["last_event_seq"]

        wrong_run = self._edge_update()
        wrong_run["run_id"] = "foreign-run"
        with self.assertRaises(ValidationError) as mismatched:
            self.agent.ingest_edge_observation(wrong_run)
        self.assertEqual("EDGE_BINDING_MISMATCH", getattr(mismatched.exception, "code", None))

        future = self._edge_update(observed_epoch_ms=self.now_ms + 1)
        with self.assertRaises(ValidationError) as future_error:
            self.agent.ingest_edge_observation(future)
        self.assertEqual("EDGE_OBSERVATION_FUTURE", getattr(future_error.exception, "code", None))

        unsafe = self._edge_update()
        unsafe["capture"]["secret_safe"] = False
        with self.assertRaises(ValidationError) as unsafe_error:
            self.agent.ingest_edge_observation(unsafe)
        self.assertEqual("EDGE_CAPTURE_INVALID", getattr(unsafe_error.exception, "code", None))

        snapshot = self.agent.snapshot("session-edge-1")
        self.assertEqual(accepted_seq, snapshot["last_event_seq"])
        self.assertEqual("NO_EDGE_OBSERVATION", snapshot["edge"]["reason"])
        self.assertEqual([], snapshot["evidence_refs"])
        self.assertEqual(0, snapshot["physical_action_count"])

    def test_admission_must_match_task_client_identity(self) -> None:
        mismatched_task = replace(
            read_only_task(),
            client_identity=ClientIdentity("15.32.75d4a0", 52_105_824, "e" * 64),
        )
        self.agent.submit_task(mismatched_task)
        admission = admit_read_only_runtime(
            _admission_observation(self.now_ms),
            now_epoch_ms=self.now_ms,
            max_age_ms=15_000,
        )
        binding = RuntimeSignalBinding(
            session_id="session-edge-1",
            run_id="run-edge-1",
            runtime_id=admission.runtime_namespace,
            runtime_instance_id="runtime-instance-1",
            runtime_binding_sha256=admission.runtime_binding_sha256,
        )
        with self.assertRaises(ValidationError) as mismatch:
            self.agent.bind_read_only_runtime(
                "session-edge-1",
                self._issue_authority(admission, _signal_resolver(binding), binding),
            )
        self.assertEqual("EDGE_RUNTIME_COMPOSITION_MISMATCH", mismatch.exception.code)
        self.assertEqual("NONE", self.agent.snapshot("session-edge-1")["official_client_access"])

    def test_stale_or_forged_admission_fails_closed_without_current_access(self) -> None:
        self.agent.submit_task(read_only_task())
        admission = admit_read_only_runtime(
            _admission_observation(self.now_ms),
            now_epoch_ms=self.now_ms,
            max_age_ms=15_000,
        )
        forged = replace(admission, runtime_binding_sha256="f" * 64)
        forged_binding = RuntimeSignalBinding(
            session_id="session-edge-1",
            run_id="run-edge-1",
            runtime_id=forged.runtime_namespace,
            runtime_instance_id="runtime-instance-forged",
            runtime_binding_sha256=forged.runtime_binding_sha256,
        )
        with self.assertRaises(ValidationError) as forged_error:
            self.agent.bind_read_only_runtime(
                "session-edge-1",
                self._issue_authority(forged, _signal_resolver(forged_binding), forged_binding),
            )
        self.assertEqual("EDGE_RUNTIME_ADMISSION_INVALID", forged_error.exception.code)

        self.now_ms += 15_001
        stale_binding = replace(
            forged_binding,
            runtime_instance_id="runtime-instance-stale",
            runtime_binding_sha256=admission.runtime_binding_sha256,
        )
        with self.assertRaises(ValidationError) as stale_error:
            self.agent.bind_read_only_runtime(
                "session-edge-1",
                self._issue_authority(admission, _signal_resolver(stale_binding), stale_binding),
            )
        self.assertEqual("EDGE_RUNTIME_ADMISSION_STALE", stale_error.exception.code)
        snapshot = self.agent.snapshot("session-edge-1")
        self.assertEqual("NONE", snapshot["official_client_access"])
        self.assertEqual(0, snapshot["physical_action_count"])

    def test_foreign_unreviewed_or_untyped_runtime_signal_fails_closed(self) -> None:
        self.agent.submit_task(read_only_task())
        _, resolver, binding = self._admit_and_bind()
        self.agent.ingest_edge_observation(self._edge_update())
        evidence = self._reviewed_signal(resolver, binding)
        unreviewed_source_refs = ("producer:evidence-unreviewed",)
        unreviewed_ref = "runtime-signal:" + sha256_jcs({
            "schema": "otclient.local-agent.runtime-signal.v1",
            "session_id": binding.session_id,
            "run_id": binding.run_id,
            "clock_domain_id": "clock:control-center",
            "runtime_id": binding.runtime_id,
            "runtime_instance_id": binding.runtime_instance_id,
            "runtime_binding_sha256": binding.runtime_binding_sha256,
            "producer_id": "fixture-causal-producer",
            "contract_id": "fixture-causal-v1",
            "observed_monotonic_ns": 960,
            "source_state": "WORLD_ENTERED",
            "source_evidence_refs": list(unreviewed_source_refs),
            "runtime_state": "IN_GAME",
            "evidence_class": RuntimeEvidenceClass.REVIEWED_CAUSAL.value,
        })
        unreviewed_observation = RuntimeObservation(
            state="IN_GAME",
            evidence_class=RuntimeEvidenceClass.REVIEWED_CAUSAL,
            evidence_refs=(unreviewed_ref,),
        )
        unreviewed_evidence = RuntimeSignalEvidence(
            signal_ref=unreviewed_ref,
            observation=unreviewed_observation,
            binding=binding,
            clock_domain_id="clock:control-center",
            producer_id="fixture-causal-producer",
            contract_id="fixture-causal-v1",
            source_state="WORLD_ENTERED",
            observed_monotonic_ns=960,
            source_evidence_refs=unreviewed_source_refs,
        )

        with self.assertRaises(ValidationError) as unreviewed:
            self.agent.ingest_runtime_signal("session-edge-1", unreviewed_evidence)
        self.assertEqual("EDGE_RUNTIME_SIGNAL_UNTRUSTED", unreviewed.exception.code)

        tampered_provenance = replace(evidence, producer_id="forged-producer")
        with self.assertRaises(ValidationError) as tampered:
            self.agent.ingest_runtime_signal("session-edge-1", tampered_provenance)
        self.assertEqual("EDGE_RUNTIME_SIGNAL_INVALID", tampered.exception.code)

        foreign_binding = replace(binding, run_id="run-foreign")
        foreign_evidence = replace(evidence, binding=foreign_binding)
        with self.assertRaises(ValidationError) as foreign:
            self.agent.ingest_runtime_signal("session-edge-1", foreign_evidence)
        self.assertEqual("EDGE_RUNTIME_SIGNAL_BINDING_MISMATCH", foreign.exception.code)

        with self.assertRaises(ValidationError) as untyped:
            self.agent.ingest_runtime_signal("session-edge-1", {"runtime_state": "IN_GAME"})
        self.assertEqual("EDGE_RUNTIME_SIGNAL_INVALID", untyped.exception.code)

        snapshot = self.agent.snapshot("session-edge-1")
        self.assertFalse(snapshot["edge"]["runtime"]["current"])
        self.assertEqual(0, snapshot["physical_action_count"])

    def test_duck_typed_runtime_signal_objects_are_rejected(self) -> None:
        self.agent.submit_task(read_only_task())
        admission = admit_read_only_runtime(
            _admission_observation(self.now_ms),
            now_epoch_ms=self.now_ms,
            max_age_ms=15_000,
        )
        binding = RuntimeSignalBinding(
            session_id="session-edge-1",
            run_id="run-edge-1",
            runtime_id=admission.runtime_namespace,
            runtime_instance_id="runtime-instance-1",
            runtime_binding_sha256=admission.runtime_binding_sha256,
        )
        resolver = _signal_resolver(binding)
        duck_binding = SimpleNamespace(
            session_id=binding.session_id,
            run_id=binding.run_id,
            runtime_id=binding.runtime_id,
            runtime_instance_id=binding.runtime_instance_id,
            runtime_binding_sha256=binding.runtime_binding_sha256,
        )
        with self.assertRaises(ValidationError) as untyped_binding:
            self._issue_authority(
                admission,
                resolver,
                duck_binding,
            )
        self.assertEqual("EDGE_RUNTIME_SIGNAL_BINDING_INVALID", untyped_binding.exception.code)

        self.agent.bind_read_only_runtime(
            "session-edge-1",
            self._issue_authority(admission, resolver, binding),
        )
        self.agent.ingest_edge_observation(self._edge_update())
        evidence = self._reviewed_signal(resolver, binding)
        duck_evidence = SimpleNamespace(
            signal_ref=evidence.signal_ref,
            observation=evidence.observation,
            binding=evidence.binding,
            clock_domain_id=evidence.clock_domain_id,
            producer_id=evidence.producer_id,
            contract_id=evidence.contract_id,
            source_state=evidence.source_state,
            observed_monotonic_ns=evidence.observed_monotonic_ns,
            source_evidence_refs=evidence.source_evidence_refs,
        )
        with self.assertRaises(ValidationError) as untyped_evidence:
            self.agent.ingest_runtime_signal("session-edge-1", duck_evidence)
        self.assertEqual("EDGE_RUNTIME_SIGNAL_INVALID", untyped_evidence.exception.code)

    def test_live_runtime_authority_cannot_swap_resolver_or_drop_signal_provenance(self) -> None:
        self.agent.submit_task(read_only_task())
        admission, resolver, binding = self._admit_and_bind()
        self.agent.ingest_edge_observation(self._edge_update())

        with self.assertRaises(ValidationError) as swapped:
            self.agent.bind_read_only_runtime(
                "session-edge-1",
                admission,
                runtime_signal_resolver=_signal_resolver(binding),
                runtime_signal_binding=binding,
            )
        self.assertEqual("EDGE_RUNTIME_AUTHORITY_REQUIRED", swapped.exception.code)

        missing_provenance = replace(
            self._reviewed_signal(resolver, binding),
            source_evidence_refs=(),
        )
        with self.assertRaises(ValidationError) as missing:
            self.agent.ingest_runtime_signal("session-edge-1", missing_provenance)
        self.assertEqual("EDGE_RUNTIME_SIGNAL_INVALID", missing.exception.code)
        self.assertFalse(self.agent.snapshot("session-edge-1")["edge"]["runtime"]["current"])

    def test_admission_ages_out_and_stales_reviewed_runtime_signal(self) -> None:
        self.agent.submit_task(read_only_task())
        _, resolver, binding = self._admit_and_bind()
        self.agent.ingest_edge_observation(self._edge_update())
        evidence = self._reviewed_signal(resolver, binding)
        current = self.agent.ingest_runtime_signal("session-edge-1", evidence)
        self.assertTrue(current["edge"]["runtime"]["current"])

        self.now_ms += 15_001
        stale = self.agent.snapshot("session-edge-1")

        self.assertEqual("DEGRADED", stale["operational_state"])
        self.assertFalse(stale["edge"]["current"])
        self.assertEqual("EDGE_RUNTIME_ADMISSION_STALE", stale["edge"]["reason"])
        self.assertFalse(stale["edge"]["runtime"]["current"])
        self.assertEqual("NONE", stale["official_client_access"])
        self.assertEqual(0, stale["physical_action_count"])

    def test_owner_ui_renders_edge_availability_capture_and_runtime_without_claiming_mutation(self) -> None:
        rendered = render_control_ui("a" * 64, "csp-nonce")
        self.assertIn("session.edge", rendered)
        self.assertIn("edge.availability", rendered)
        self.assertIn("edge.admission", rendered)
        self.assertIn("edge.capture", rendered)
        self.assertIn("edge.runtime", rendered)
        self.assertNotIn("Runtime access: <strong>none</strong>", rendered)
        self.assertIn("Mutation authority: <strong>NONE</strong>", rendered)


if __name__ == "__main__":
    unittest.main()
