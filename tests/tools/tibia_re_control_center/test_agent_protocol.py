import unittest
from dataclasses import FrozenInstanceError

from tools.tibia_re_control_center.agent_protocol import (
    AgentEvent,
    AgentProvenance,
    AgentVisualState,
    ClientIdentity,
    NamedAgentAction,
    TaskEnvelope,
)
from tools.tibia_re_control_center.model import ValidationError


def envelope(**overrides):
    value = {
        "schema": "TaskEnvelope.v1",
        "session_id": "session-1",
        "task_id": "task-1",
        "run_id": "run-1",
        "idempotency_key": "idem-1",
        "trusted_main_sha": "a" * 40,
        "client_identity": {"version": "1", "size": 123, "sha256": "b" * 64},
        "objective": "observe",
        "allowed_actions": ["SCREENSHOT"],
        "physical_action_budget": 0,
        "max_attempts": 1,
        "deadline_epoch_ms": 1,
        "runtime_access": "none",
        "required_evidence": ["screenshot"],
        "secret_capability_ref": None,
    }
    value.update(overrides)
    return value


class AgentProtocolTests(unittest.TestCase):
    def test_parses_exact_immutable_envelope(self):
        parsed = TaskEnvelope.from_mapping(envelope())
        self.assertEqual(parsed.allowed_actions, (NamedAgentAction.SCREENSHOT,))
        with self.assertRaises(FrozenInstanceError):
            parsed.objective = "x"

    def test_rejects_unknown_and_raw_credential_fields(self):
        for field in ("username", "password", "credential", "raw_secret", "unexpected"):
            with self.subTest(field=field), self.assertRaises(ValidationError):
                TaskEnvelope.from_mapping(envelope(**{field: "secret"}))

    def test_rejects_bad_sha_and_ids(self):
        with self.assertRaises(ValidationError):
            TaskEnvelope.from_mapping(envelope(trusted_main_sha="A" * 40))
        with self.assertRaises(ValidationError):
            TaskEnvelope.from_mapping(envelope(session_id="../escape"))

    def test_rejects_unbounded_budget_attempts_and_unknown_action(self):
        for field, value in (("physical_action_budget", -1), ("max_attempts", 0), ("max_attempts", 10**9)):
            with self.subTest(field=field, value=value), self.assertRaises(ValidationError):
                TaskEnvelope.from_mapping(envelope(**{field: value}))
        with self.assertRaises(ValidationError):
            TaskEnvelope.from_mapping(envelope(allowed_actions=["CLICK"]))

    def test_runtime_vocabulary_does_not_promote_visual_state(self):
        parsed = TaskEnvelope.from_mapping(envelope(runtime_access="ephemeral_isolated"))
        self.assertEqual(parsed.runtime_access, "ephemeral_isolated")
        self.assertEqual(AgentVisualState.WORLD_VISUAL.value, "WORLD_VISUAL")
        self.assertNotEqual(AgentVisualState.WORLD_VISUAL.value, "IN_GAME")

    def test_event_new_starts_at_zero(self):
        event = AgentEvent.new(
            session_id="session-1", run_id=None, provenance=AgentProvenance.SENSOR,
            kind="observation", state_before="IDLE", state_after="OBSERVING",
        )
        self.assertEqual(event.seq, 0)
        self.assertEqual(event.artifact_refs, ())


if __name__ == "__main__":
    unittest.main()
