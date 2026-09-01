import tempfile
import unittest
from contextlib import suppress
from pathlib import Path

from tools.tibia_re_control_center.agent_protocol import (
    ClientIdentity,
    NamedAgentAction,
    TaskEnvelope,
)
from tools.tibia_re_control_center.agent_session import AgentSessionCoordinator
from tools.tibia_re_control_center.control_ui import render_control_ui
from tools.tibia_re_control_center.execution import MutationCoordinator
from tools.tibia_re_control_center.fake import FakeAdapter, ManualClock
from tools.tibia_re_control_center.model import ValidationError
from tools.tibia_re_control_center.persistent_store import SQLitePersistentStore


def read_only_task() -> TaskEnvelope:
    return TaskEnvelope(
        schema="otclient.local-agent.task.v1",
        session_id="session-edge-1",
        task_id="task-edge-1",
        run_id="run-edge-1",
        idempotency_key="idem-edge-1",
        trusted_main_sha="a" * 40,
        client_identity=ClientIdentity("15.32.75d4a0", 52105824, "b" * 64),
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
        self.agent = AgentSessionCoordinator(self.store, self.control)
        self.now_ms = 1_000_000
        self.agent._now_epoch_ms = lambda: self.now_ms

    def tearDown(self) -> None:
        with suppress(Exception):
            self.store.close()
        self.temp.cleanup()

    def test_current_read_only_edge_observation_is_owner_visible_without_binding_physical_executor(self) -> None:
        self.agent.submit_task(read_only_task())
        update = {
            "schema": "otclient.local-agent.edge-observation.v1",
            "session_id": "session-edge-1",
            "run_id": "run-edge-1",
            "edge_instance_id": "edge-instance-1",
            "observed_epoch_ms": self.now_ms,
            "heartbeat_epoch_ms": self.now_ms,
            "capture": {
                "status": "AVAILABLE",
                "artifact_ref": "capture-edge-1",
                "sha256": "c" * 64,
                "observed_epoch_ms": self.now_ms,
                "secret_safe": True,
            },
            "runtime": {
                "status": "IN_GAME",
                "evidence_refs": ["runtime-edge-1"],
                "observed_epoch_ms": self.now_ms,
            },
        }

        self.agent.ingest_edge_observation(update)
        snapshot = self.agent.snapshot("session-edge-1")

        self.assertEqual("read_only", snapshot["runtime_access"])
        self.assertEqual("READ_ONLY", snapshot["official_client_access"])
        self.assertEqual("CONNECTED", snapshot["edge"]["availability"])
        self.assertTrue(snapshot["edge"]["current"])
        self.assertEqual(self.now_ms, snapshot["heartbeat_epoch_ms"])
        self.assertTrue(snapshot["edge"]["capture"]["current"])
        self.assertEqual("capture-edge-1", snapshot["edge"]["capture"]["artifact_ref"])
        self.assertTrue(snapshot["edge"]["runtime"]["current"])
        self.assertEqual("IN_GAME", snapshot["edge"]["runtime"]["status"])
        self.assertEqual("NULL", snapshot["executor"])
        self.assertEqual("NONE", snapshot["mutation_authority"])
        self.assertEqual(0, snapshot["physical_action_budget"])
        self.assertEqual(0, snapshot["physical_action_count"])

        capture = self.agent.owner_control("session-edge-1", "SCREENSHOT")
        self.assertEqual("AVAILABLE", capture["status"])
        self.assertEqual("capture-edge-1", capture["capture"]["artifact_ref"])
        self.assertEqual(0, capture["session"]["physical_action_count"])
        self.assertEqual("NULL", capture["session"]["executor"])


    def _edge_update(
        self,
        *,
        edge_instance_id: str = "edge-instance-1",
        observed_epoch_ms: int | None = None,
        heartbeat_epoch_ms: int | None = None,
        include_capture: bool = True,
        include_runtime: bool = True,
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
        self.agent = AgentSessionCoordinator(self.store, self.control)
        self.agent._now_epoch_ms = lambda: self.now_ms

    def test_heartbeat_loss_degrades_operational_state_and_stales_edge_evidence(self) -> None:
        self.agent.submit_task(read_only_task())
        self.agent.ingest_edge_observation(self._edge_update())

        self.now_ms += 15_001
        snapshot = self.agent.snapshot("session-edge-1")

        self.assertEqual("DEGRADED", snapshot["operational_state"])
        self.assertEqual("CONNECTED", snapshot["edge"]["availability"])
        self.assertFalse(snapshot["edge"]["current"])
        self.assertEqual("HEARTBEAT_STALE", snapshot["edge"]["reason"])
        self.assertFalse(snapshot["edge"]["capture"]["current"])
        self.assertFalse(snapshot["edge"]["runtime"]["current"])
        self.assertEqual("NULL", snapshot["executor"])
        self.assertEqual(0, snapshot["physical_action_count"])

        capture = self.agent.owner_control("session-edge-1", "SCREENSHOT")
        self.assertEqual("UNAVAILABLE", capture["status"])
        self.assertEqual(0, capture["session"]["physical_action_count"])

    def test_disconnect_degrades_and_fresh_reconnect_does_not_replay_old_evidence(self) -> None:
        self.agent.submit_task(read_only_task())
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
                include_runtime=False,
            )
        )
        self.assertEqual("RUNNING", heartbeat_only["operational_state"])
        self.assertTrue(heartbeat_only["edge"]["current"])
        self.assertFalse(heartbeat_only["edge"]["capture"]["current"])
        self.assertFalse(heartbeat_only["edge"]["runtime"]["current"])
        self.assertIsNone(heartbeat_only["edge"]["capture"]["artifact_ref"])

        self.now_ms += 1
        refreshed = self.agent.ingest_edge_observation(
            self._edge_update(edge_instance_id="edge-instance-2")
        )
        self.assertTrue(refreshed["edge"]["capture"]["current"])
        self.assertEqual("capture-edge-instance-2", refreshed["edge"]["capture"]["artifact_ref"])
        self.assertEqual(0, refreshed["physical_action_count"])

    def test_disconnect_rejects_replayed_observation_even_inside_freshness_window(self) -> None:
        self.agent.submit_task(read_only_task())
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
        self.agent.ingest_edge_observation(self._edge_update())
        self.now_ms += 1

        with self.assertRaises(ValidationError) as replaced:
            self.agent.ingest_edge_observation(self._edge_update(edge_instance_id="edge-instance-2"))
        self.assertEqual("EDGE_BINDING_MISMATCH", getattr(replaced.exception, "code", None))
        snapshot = self.agent.snapshot("session-edge-1")
        self.assertEqual("edge-instance-1", snapshot["edge"]["edge_instance_id"])
        self.assertTrue(snapshot["edge"]["current"])

    def test_restart_marks_persisted_edge_evidence_disconnected_until_fresh_observation(self) -> None:
        self.agent.submit_task(read_only_task())
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
        fresh = self.agent.ingest_edge_observation(
            self._edge_update(edge_instance_id="edge-instance-2")
        )
        self.assertTrue(fresh["edge"]["current"])
        self.assertEqual("PAUSED_AUTHORITY", fresh["operational_state"])
        self.assertEqual(0, fresh["physical_action_count"])

    def test_owner_stop_dominates_fresh_edge_updates(self) -> None:
        self.agent.submit_task(read_only_task())
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

    def test_owner_ui_renders_edge_availability_capture_and_runtime_without_claiming_mutation(self) -> None:
        rendered = render_control_ui("a" * 64, "csp-nonce")
        self.assertIn("session.edge", rendered)
        self.assertIn("edge.availability", rendered)
        self.assertIn("edge.capture", rendered)
        self.assertIn("edge.runtime", rendered)
        self.assertNotIn("Runtime access: <strong>none</strong>", rendered)
        self.assertIn("Mutation authority: <strong>NONE</strong>", rendered)


if __name__ == "__main__":
    unittest.main()
