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
from tools.tibia_re_control_center.canonical import jcs_dumps
from tools.tibia_re_control_center.model import MAX_SAFE_INTEGER, ValidationError


def envelope(**overrides):
    value = {
        "schema": "otclient.local-agent.task.v1",
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

    def test_rejects_short_task_schema_type_name(self):
        with self.assertRaises(ValidationError):
            TaskEnvelope.from_mapping(envelope(schema="TaskEnvelope.v1"))

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

    def test_event_payload_is_immutable_recursively(self):
        event = AgentEvent.new(
            session_id="session-1", run_id=None, provenance=AgentProvenance.SENSOR,
            kind="observation", state_before="IDLE", state_after="OBSERVING",
            payload={"nested": {"items": [1]}},
        )
        with self.assertRaises(TypeError):
            event.payload["new"] = 1
        with self.assertRaises(TypeError):
            event.payload["nested"]["new"] = 1
        with self.assertRaises(AttributeError):
            event.payload["nested"]["items"].append(2)
        self.assertEqual(event.payload["nested"]["items"], (1,))

    def test_event_payload_rejects_unsupported_shapes(self):
        with self.assertRaises(ValidationError):
            AgentEvent.new(session_id="session-1", run_id=None, provenance=AgentProvenance.SENSOR,
                           kind="observation", state_before="IDLE", state_after="OBSERVING",
                           payload={1: "non-string key"})
        with self.assertRaises(ValidationError):
            AgentEvent.new(session_id="session-1", run_id=None, provenance=AgentProvenance.SENSOR,
                           kind="observation", state_before="IDLE", state_after="OBSERVING",
                           payload={"unsupported": object()})

    def test_event_rejects_bare_string_artifact_refs(self):
        with self.assertRaises(ValidationError):
            AgentEvent.new(session_id="session-1", run_id=None, provenance=AgentProvenance.SENSOR,
                           kind="observation", state_before="IDLE", state_after="OBSERVING",
                           artifact_refs="artifact-1")

    def test_sha_error_code_matches_digest_length(self):
        with self.assertRaises(ValidationError) as context:
            TaskEnvelope.from_mapping(envelope(trusted_main_sha="z" * 40))
        self.assertEqual(context.exception.code, "INVALID_SHA1")

    def test_event_payload_base_dict_mutation_does_not_change_event_value(self):
        event = AgentEvent.new(
            session_id="session-1", run_id=None, provenance=AgentProvenance.SENSOR,
            kind="observation", state_before="IDLE", state_after="OBSERVING",
            payload={"nested": {"original": 1}},
        )

        with self.assertRaises(TypeError):
            dict.__setitem__(event.payload, "injected", True)
        with self.assertRaises(TypeError):
            dict.update(event.payload, {"injected": True})
        with self.assertRaises(TypeError):
            dict.__setitem__(event.payload["nested"], "injected", True)
        with self.assertRaises(TypeError):
            dict.update(event.payload["nested"], {"injected": True})

        self.assertEqual(event.payload, {"nested": {"original": 1}})

    def test_event_payload_isolated_from_caller_mutation(self):
        supplied = {"nested": {"items": [1]}}
        event = AgentEvent.new(
            session_id="session-1", run_id=None, provenance=AgentProvenance.SENSOR,
            kind="observation", state_before="IDLE", state_after="OBSERVING",
            payload=supplied,
        )

        supplied["nested"]["items"].append(2)
        supplied["nested"]["replacement"] = True
        supplied["replacement"] = True

        self.assertEqual(event.payload, {"nested": {"items": (1,)}})

    def test_event_payload_rejects_noncanonical_numbers(self):
        for value in (float("nan"), float("inf"), float("-inf"), MAX_SAFE_INTEGER + 1, -MAX_SAFE_INTEGER - 1):
            with self.subTest(value=value), self.assertRaises(ValidationError):
                AgentEvent.new(
                    session_id="session-1", run_id=None, provenance=AgentProvenance.SENSOR,
                    kind="observation", state_before="IDLE", state_after="OBSERVING",
                    payload={"value": value},
                )

    def test_event_payload_is_canonical_serializer_safe(self):
        event = AgentEvent.new(
            session_id="session-1", run_id=None, provenance=AgentProvenance.SENSOR,
            kind="observation", state_before="IDLE", state_after="OBSERVING",
            payload={"nested": {"items": [1, True, None]}, "ratio": 1.5},
        )

        expected = '{"nested":{"items":[1,true,null]},"ratio":1.5}'
        self.assertEqual(jcs_dumps(event.payload), expected)
        self.assertEqual(jcs_dumps(event.payload), expected)

    def test_event_payload_rejects_unpaired_surrogates_in_keys_and_values(self):
        cases = (
            {"bad\ud800": "ok"},
            {"ok": "bad\udfff"},
            {"nested": {"bad\ud800": "ok"}},
            {"nested": {"ok": "bad\udfff"}},
        )
        for payload in cases:
            with self.subTest(payload=repr(payload)), self.assertRaises(ValidationError):
                AgentEvent.new(
                    session_id="session-1", run_id=None, provenance=AgentProvenance.SENSOR,
                    kind="observation", state_before="IDLE", state_after="OBSERVING",
                    payload=payload,
                )

        event = AgentEvent.new(
            session_id="session-1", run_id=None, provenance=AgentProvenance.SENSOR,
            kind="observation", state_before="IDLE", state_after="OBSERVING",
            payload={"café": {"value": "世界"}},
        )
        self.assertEqual(jcs_dumps(event.payload), '{"café":{"value":"世界"}}')

    def test_protocol_schema_literals_match_bindings(self):
        self.assertEqual(TaskEnvelope.from_mapping(envelope(schema="otclient.local-agent.task.v1")).schema, "otclient.local-agent.task.v1")
        event = AgentEvent.new(
            session_id="session-1", run_id=None, provenance=AgentProvenance.SENSOR,
            kind="observation", state_before="IDLE", state_after="OBSERVING",
        )
        self.assertEqual(event.schema, "otclient.local-agent.event.v1")


if __name__ == "__main__":
    unittest.main()
