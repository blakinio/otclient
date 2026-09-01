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
from tools.tibia_re_control_center.execution import MutationCoordinator
from tools.tibia_re_control_center.fake import FakeAdapter, ManualClock
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


if __name__ == "__main__":
    unittest.main()
