from __future__ import annotations

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from types import MappingProxyType

from tools.tibia_re_control_center.agent_protocol import (
    AgentEvent,
    AgentOperationalState,
    AgentProvenance,
    AgentSessionRecord,
    ClientIdentity,
    NamedAgentAction,
    ResultEnvelope,
    ResultStatus,
    TaskEnvelope,
)
from tools.tibia_re_control_center.model import DurabilityError, ValidationError
from tools.tibia_re_control_center.persistent_store import SQLitePersistentStore


def task(*, objective: str = "observe", idempotency_key: str = "idem-1", run_id: str = "run-1") -> TaskEnvelope:
    return TaskEnvelope(
        schema="otclient.local-agent.task.v1",
        session_id="session-1",
        task_id="task-1",
        run_id=run_id,
        idempotency_key=idempotency_key,
        trusted_main_sha="a" * 40,
        client_identity=ClientIdentity("1", 123, "b" * 64),
        objective=objective,
        allowed_actions=(NamedAgentAction.SCREENSHOT,),
        physical_action_budget=0,
        max_attempts=1,
        deadline_epoch_ms=1,
        runtime_access="none",
        required_evidence=("screenshot",),
        secret_capability_ref=None,
    )


def result(*, status: ResultStatus = ResultStatus.PASS) -> ResultEnvelope:
    return ResultEnvelope(
        schema="otclient.local-agent.result.v1",
        session_id="session-1",
        run_id="run-1",
        status=status,
        trusted_main_sha="a" * 40,
        final_state="IDLE",
        action_count=0,
        physical_action_budget=0,
        evidence_manifest_sha256="c" * 64,
        unresolved_conflicts=("none",),
    )


def event(*, payload: dict[str, object] | None = None) -> AgentEvent:
    return AgentEvent.new(
        session_id="session-1", run_id="run-1", provenance=AgentProvenance.SENSOR,
        kind="observation", state_before="IDLE", state_after="OBSERVING",
        observed_epoch_ms=1, artifact_refs=("artifact-1",), payload=payload,
    )


class AgentPersistenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.store = SQLitePersistentStore(self.root)

    def tearDown(self) -> None:
        self.store.close()
        self.temp.cleanup()

    def test_restart_preserves_agent_session_and_reconstructs_record(self):
        record = AgentSessionRecord(
            session_id="session-1",
            operational_state=AgentOperationalState.PAUSED,
            current_run_id=None,
            last_event_seq=7,
            pause_latched=True,
            stop_latched=False,
            heartbeat_epoch_ms=None,
        )
        self.store.write_agent_session(record)
        self.store.close()
        self.store = SQLitePersistentStore(self.root)
        loaded = self.store.load_agent_session("session-1")
        self.assertEqual(record, loaded)
        self.assertIsInstance(loaded.operational_state, AgentOperationalState)

    def test_existing_package_b_database_gains_only_additive_agent_tables(self):
        self.store.close()
        self.root = self.root / "legacy"
        db = self.root / "control" / "control-center.sqlite3"
        db.parent.mkdir(parents=True)
        connection = sqlite3.connect(db)
        try:
            connection.executescript("""
                CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                CREATE TABLE control_state (singleton INTEGER PRIMARY KEY CHECK(singleton=1), body TEXT NOT NULL);
                CREATE TABLE control_history (transition_id TEXT PRIMARY KEY, body TEXT NOT NULL);
                CREATE TABLE actions (action_id TEXT PRIMARY KEY, request_hash TEXT NOT NULL, run_id TEXT NOT NULL, body TEXT NOT NULL);
                CREATE TABLE budgets (run_id TEXT PRIMARY KEY, body TEXT NOT NULL);
                CREATE TABLE run_activation (run_id TEXT PRIMARY KEY, body TEXT NOT NULL);
                CREATE TABLE recovery (run_id TEXT PRIMARY KEY, body TEXT NOT NULL);
                CREATE TABLE requests (request_id TEXT PRIMARY KEY, body TEXT NOT NULL);
                CREATE TABLE request_claims (request_id TEXT PRIMARY KEY, resource_id TEXT NOT NULL UNIQUE);
                CREATE TABLE resources (resource_id TEXT PRIMARY KEY, request_id TEXT NOT NULL UNIQUE, operation TEXT NOT NULL, state TEXT NOT NULL, body TEXT NOT NULL, result TEXT);
                CREATE TABLE events (seq INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT, body TEXT NOT NULL);
                CREATE TABLE artifacts (run_id TEXT NOT NULL, path TEXT NOT NULL, sha256 TEXT NOT NULL, body BLOB NOT NULL, PRIMARY KEY(run_id,path));
            """)
            connection.execute("INSERT INTO events(run_id,body) VALUES(?,?)", ("legacy", json.dumps({"kind": "legacy"})))
            connection.commit()
        finally:
            connection.close()
        self.store = SQLitePersistentStore(self.root)
        names = {row[0] for row in self.store._fetchall("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")}
        self.assertEqual(
            {"agent_sessions", "agent_tasks"},
            names - {"meta", "control_state", "control_history", "actions", "budgets", "run_activation", "recovery", "requests", "request_claims", "resources", "events", "artifacts"},
        )
        self.assertEqual([{"cursor": 1, "kind": "legacy"}], self.store.list_events(limit=10)[0])

    def test_agent_event_uses_positive_committed_sequence_in_persisted_body(self):
        first = self.store.append_agent_event(event())
        second = self.store.append_agent_event(event(payload={"n": 2}))
        self.assertGreater(first.seq, 0)
        self.assertGreater(second.seq, first.seq)
        row = self.store._fetchone("SELECT seq,body FROM events WHERE seq=?", (first.seq,))
        self.assertEqual(first.seq, row[0])
        self.assertEqual(first.seq, json.loads(row[1])["seq"])
        self.assertIsInstance(first.provenance, AgentProvenance)
        self.assertIsInstance(first.payload, MappingProxyType)
        self.assertEqual(("artifact-1",), first.artifact_refs)

    def test_task_accept_replays_canonical_equal_and_rejects_conflict(self):
        accepted = self.store.accept_agent_task(task())
        replay = self.store.accept_agent_task(task())
        self.assertTrue(accepted["accepted_new"])
        self.assertFalse(replay["accepted_new"])
        self.assertEqual("otclient.local-agent.task.v1", replay["envelope"]["schema"])
        with self.assertRaises(ValidationError) as context:
            self.store.accept_agent_task(task(objective="different"))
        self.assertEqual("IDEMPOTENCY_CONFLICT", context.exception.code)

    def test_task_result_is_first_write_idempotent_and_conflicts_fail_closed(self):
        self.store.accept_agent_task(task())
        self.store.finish_agent_task("idem-1", result())
        self.store.finish_agent_task("idem-1", result())
        loaded = self.store.load_agent_task("idem-1")
        self.assertEqual({"envelope", "result"}, set(loaded))
        self.assertEqual("PASS", loaded["result"]["status"])
        with self.assertRaises(ValidationError) as context:
            self.store.finish_agent_task("idem-1", result(status=ResultStatus.FAIL))
        self.assertEqual("IDEMPOTENCY_CONFLICT", context.exception.code)
        with self.assertRaises(ValidationError) as context:
            self.store.finish_agent_task("missing", result())
        self.assertEqual("AGENT_TASK_MISSING", context.exception.code)

    def test_mappingproxy_payload_secret_is_rejected_before_event_write(self):
        sensitive = event(payload={"nested": {"password": "do-not-persist"}})
        with self.assertRaises(ValidationError) as context:
            self.store.append_agent_event(sensitive)
        self.assertEqual("SECRET_MATERIAL_REJECTED", context.exception.code)
        self.assertEqual(0, self.store._fetchone("SELECT COUNT(*) FROM events")[0])

    def test_failed_transaction_leaves_no_partial_agent_task(self):
        self.store.inject_fault("agent_task_accept")
        with self.assertRaises(DurabilityError):
            self.store.accept_agent_task(task())
        self.assertIsNone(self.store.load_agent_task("idem-1"))


if __name__ == "__main__":
    unittest.main()
