from __future__ import annotations

import json
import sqlite3
import tempfile
import traceback
import unittest
from dataclasses import replace
from pathlib import Path
from types import MappingProxyType
from unittest.mock import patch

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
from tools.tibia_re_control_center import persistent_store
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


def raw_event(**overrides) -> AgentEvent:
    value = {
        "schema": "otclient.local-agent.event.v1",
        "session_id": "session-1",
        "run_id": "run-1",
        "seq": 0,
        "observed_epoch_ms": 1,
        "provenance": AgentProvenance.SENSOR,
        "kind": "observation",
        "state_before": "IDLE",
        "state_after": "OBSERVING",
        "artifact_refs": ("artifact-1",),
        "action_id": None,
        "payload": {},
    }
    value.update(overrides)
    return AgentEvent(**value)


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

    def test_task_and_result_reconstruct_after_restart_and_replay_canonical_input(self):
        accepted = self.store.accept_agent_task(task())
        self.store.finish_agent_task("idem-1", result())
        self.store.close()
        self.store = SQLitePersistentStore(self.root)
        loaded = self.store.load_agent_task("idem-1")
        self.assertEqual(accepted["envelope"], loaded["envelope"])
        self.assertEqual("PASS", loaded["result"]["status"])
        equivalent = replace(
            task(),
            allowed_actions=["SCREENSHOT"],
            required_evidence=["screenshot"],
        )
        replay = self.store.accept_agent_task(equivalent)
        self.assertFalse(replay["accepted_new"])
        self.store.finish_agent_task("idem-1", replace(result(), unresolved_conflicts=["none"]))

    def test_corrupt_session_body_identity_fails_closed(self):
        self.store.write_agent_session(AgentSessionRecord(
            "session-1", AgentOperationalState.IDLE, None, 0, False, False, None,
        ))
        body = json.loads(self.store._fetchone("SELECT body FROM agent_sessions WHERE session_id='session-1'")[0])
        body["session_id"] = "session-other"
        self.store._db.execute("UPDATE agent_sessions SET body=? WHERE session_id='session-1'", (json.dumps(body),))
        self._assert_corrupt(lambda: self.store.load_agent_session("session-1"))

    def test_corruption_error_is_cause_free_and_does_not_echo_durable_text(self):
        secret_text = "PASSWORD=hunter2"
        self.store.write_agent_session(AgentSessionRecord(
            "session-1", AgentOperationalState.IDLE, None, 0, False, False, None,
        ))
        body = json.loads(self.store._fetchone("SELECT body FROM agent_sessions WHERE session_id='session-1'")[0])
        body["operational_state"] = secret_text
        self.store._db.execute("UPDATE agent_sessions SET body=? WHERE session_id='session-1'", (json.dumps(body),))
        with self.assertRaises(ValidationError) as context:
            self.store.load_agent_session("session-1")
        error = context.exception
        self.assertEqual("PERSISTENT_STATE_CORRUPT", error.code)
        self.assertIsNone(error.__cause__)
        self.assertIsNone(error.__context__)
        self.assertNotIn(secret_text, str(error))
        self.assertNotIn(secret_text, error.safe_message)
        self.assertNotIn(secret_text, "".join(traceback.format_exception(error)))
        self.assertTrue(all(secret_text not in str(linked) for linked in self._exception_links(error)))

    def test_unexpected_decode_failures_propagate_unchanged(self):
        self.store.write_agent_session(AgentSessionRecord(
            "session-1", AgentOperationalState.IDLE, None, 0, False, False, None,
        ))
        for failure in (RuntimeError("internal decoder failure"), MemoryError(), KeyboardInterrupt(), SystemExit()):
            with self.subTest(failure=type(failure).__name__), patch.object(persistent_store, "_load", side_effect=failure):
                with self.assertRaises(type(failure)):
                    self.store.load_agent_session("session-1")

    def test_invalid_session_inputs_fail_before_transaction(self):
        cases = (
            replace(AgentSessionRecord("session-1", AgentOperationalState.IDLE, None, 0, False, False, None), session_id="bad/id"),
            replace(AgentSessionRecord("session-1", AgentOperationalState.IDLE, None, 0, False, False, None), operational_state="PASSWORD=hunter2"),
            replace(AgentSessionRecord("session-1", AgentOperationalState.IDLE, None, 0, False, False, None), last_event_seq=-1),
            replace(AgentSessionRecord("session-1", AgentOperationalState.IDLE, None, 0, False, False, None), heartbeat_epoch_ms=True),
            replace(AgentSessionRecord("session-1", AgentOperationalState.IDLE, None, 0, False, False, None), pause_latched=1),
        )
        for record in cases:
            with self.subTest(record=record):
                with self.assertRaises(ValidationError) as raised:
                    self.store.write_agent_session(record)
                self.assertTrue(raised.exception.code.startswith(("INVALID", "INTEGER")))
                self.assertEqual(0, self.store._fetchone("SELECT COUNT(*) FROM agent_sessions")[0])

    def test_invalid_event_inputs_fail_before_event_insert(self):
        cases = (
            raw_event(schema="wrong"),
            raw_event(seq=1),
            raw_event(session_id="bad/id"),
            raw_event(run_id="bad/id"),
            raw_event(provenance="PASSWORD=hunter2"),
            raw_event(observed_epoch_ms=True),
            raw_event(kind=""),
            raw_event(state_before=""),
            raw_event(artifact_refs=["artifact-1"]),
            raw_event(artifact_refs=("bad/id",)),
            raw_event(action_id="bad/id"),
        )
        for invalid in cases:
            with self.subTest(invalid=repr(invalid)):
                with self.assertRaises(ValidationError):
                    self.store.append_agent_event(invalid)
                self.assertEqual(0, self.store._fetchone("SELECT COUNT(*) FROM events")[0])

    def test_corrupt_task_canonical_body_hash_and_identities_fail_closed(self):
        self.store.accept_agent_task(task())
        original_body = self.store._fetchone("SELECT body FROM agent_tasks WHERE idempotency_key='idem-1'")[0]
        body = json.loads(original_body)
        body["objective"] = "corrupt but valid JSON"
        self.store._db.execute("UPDATE agent_tasks SET body=? WHERE idempotency_key='idem-1'", (json.dumps(body),))
        self._assert_corrupt(lambda: self.store.load_agent_task("idem-1"))

        self.store._db.execute("UPDATE agent_tasks SET body=? WHERE idempotency_key='idem-1'", (original_body,))
        self.store._db.execute("UPDATE agent_tasks SET session_id='session-other' WHERE idempotency_key='idem-1'")
        self._assert_corrupt(lambda: self.store.accept_agent_task(task()))

    def test_corrupt_task_hash_result_identity_and_shape_fail_closed(self):
        self.store.accept_agent_task(task())
        self.store.finish_agent_task("idem-1", result())
        original_hash = self.store._fetchone("SELECT envelope_hash FROM agent_tasks WHERE idempotency_key='idem-1'")[0]
        self.store._db.execute("UPDATE agent_tasks SET envelope_hash=? WHERE idempotency_key='idem-1'", ("0" * 64,))
        self._assert_corrupt(lambda: self.store.load_agent_task("idem-1"))

        self.store._db.execute("UPDATE agent_tasks SET envelope_hash=? WHERE idempotency_key='idem-1'", (original_hash,))
        corrupt_result = json.loads(self.store._fetchone("SELECT result FROM agent_tasks WHERE idempotency_key='idem-1'")[0])
        corrupt_result["run_id"] = "run-other"
        self.store._db.execute("UPDATE agent_tasks SET result=? WHERE idempotency_key='idem-1'", (json.dumps(corrupt_result),))
        self._assert_corrupt(lambda: self.store.load_agent_task("idem-1"))

        self.store._db.execute("UPDATE agent_tasks SET result=? WHERE idempotency_key='idem-1'", (json.dumps({"schema": "otclient.local-agent.result.v1"}),))
        self._assert_corrupt(lambda: self.store.load_agent_task("idem-1"))

    def test_same_run_under_different_idempotency_key_conflicts(self):
        self.store.accept_agent_task(task())
        with self.assertRaises(ValidationError) as context:
            self.store.accept_agent_task(task(idempotency_key="idem-2"))
        self.assertEqual("IDEMPOTENCY_CONFLICT", context.exception.code)

    def test_result_identity_mismatch_is_rejected_as_caller_input(self):
        self.store.accept_agent_task(task())
        with self.assertRaises(ValidationError) as context:
            self.store.finish_agent_task("idem-1", replace(result(), run_id="run-other"))
        self.assertEqual("TASK_RESULT_MISMATCH", context.exception.code)

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

    def test_event_body_failure_rolls_back_placeholder_and_mixed_retention_backpressure(self):
        self.store.inject_fault("agent_event_body")
        with self.assertRaises(DurabilityError):
            self.store.append_agent_event(event())
        self.assertEqual(0, self.store._fetchone("SELECT COUNT(*) FROM events")[0])
        appended = self.store.append_agent_event(event())
        body = json.loads(self.store._fetchone("SELECT body FROM events WHERE seq=?", (appended.seq,))[0])
        self.assertEqual(appended.seq, body["seq"])
        self.assertIsInstance(appended.payload, MappingProxyType)

        self.store.close()
        self.store = SQLitePersistentStore(self.root, event_retention=32)
        self.store.append_events("legacy", [{"kind": "legacy", "payload": {"index": index}} for index in range(32)])
        self.store.append_agent_event(event())
        self.store.append_agent_event(event(payload={"index": 33}))
        with self.assertRaises(ValidationError) as context:
            self.store.list_events(cursor=1, limit=10)
        self.assertEqual("CONTROL_EVENT_BACKPRESSURE", context.exception.code)

    def _assert_corrupt(self, callback):
        with self.assertRaises(ValidationError) as context:
            callback()
        self.assertEqual("PERSISTENT_STATE_CORRUPT", context.exception.code)

    def _exception_links(self, error):
        pending = [error]
        visited = set()
        while pending:
            current = pending.pop()
            if id(current) in visited:
                continue
            visited.add(id(current))
            yield current
            pending.extend(linked for linked in (current.__cause__, current.__context__) if linked is not None)


if __name__ == "__main__":
    unittest.main()
