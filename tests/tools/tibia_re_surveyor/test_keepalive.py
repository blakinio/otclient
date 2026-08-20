import unittest

from tools.tibia_re_surveyor.keepalive import evaluate_authority, run_keepalive_once
from tools.tibia_re_surveyor.runtime import EXPECTED_CLIENT_SHA256, EXPECTED_CLIENT_SIZE


class FakeTransport:
    def __init__(self, age=None, result="KEEPALIVE_ROTATION_SENT"):
        self.age = age
        self.result = result
        self.calls = []
    def heartbeat_age(self):
        return self.age
    def rotate_once(self, **kwargs):
        self.calls.append(kwargs)
        return self.result


def valid_snapshot():
    process = {"pid": 123, "process_start_ticks": 456, "client_size": EXPECTED_CLIENT_SIZE, "client_sha256": EXPECTED_CLIENT_SHA256, "exact_fence_match": True}
    registration = {"pid": 123, "process_start_ticks": 456, "client_size": EXPECTED_CLIENT_SIZE, "client_sha256": EXPECTED_CLIENT_SHA256, "display": ":1", "lease_generation": 7, "state": "IN_GAME"}
    return {"display": ":1", "target_uniqueness": "PROVEN", "exact_current_fence": {"match": True}, "processes": [process], "visible_tibia_windows": [{"xid": 99, "pid": 123, "title_class": "CHARACTER_CONTEXT"}], "canonical_control": {"registration_present": True, "registration": registration, "lease_present": True, "lease": {"generation": 7, "controller_task": "OTC-test"}, "lease_expired": False}}


def valid_authority():
    return {"runtime_access": "canonical_reuse_or_mutation", "gate_a": "PASS", "generation_rebind": "NOT_APPLICABLE", "gate_b": "PASS", "target_uniqueness": "PROVEN", "whole_lifetime_supervisor": "PASS", "mutation_authorized": True, "gui_input_authorized": True, "runtime_owner_task": "OTC-test"}


class KeepaliveTests(unittest.TestCase):
    def test_no_authority_fails_closed_without_input(self):
        transport = FakeTransport(age=600)
        event = run_keepalive_once(valid_snapshot(), None, transport)
        self.assertEqual("KEEPALIVE_SKIPPED_UNAUTHORIZED", event["result"])
        self.assertFalse(transport.calls)
        self.assertIn("NO_KEEPALIVE_AUTHORITY_INPUT", event["authority_reasons"])

    def test_missing_registration_fails_closed(self):
        snapshot = valid_snapshot()
        snapshot["canonical_control"]["registration_present"] = False
        snapshot["canonical_control"]["registration"] = None
        decision = evaluate_authority(valid_authority(), snapshot)
        self.assertFalse(decision.allowed)
        self.assertIn("CANONICAL_REGISTRATION_ABSENT", decision.reasons)

    def test_not_due_never_sends_input(self):
        transport = FakeTransport(age=120)
        event = run_keepalive_once(valid_snapshot(), valid_authority(), transport)
        self.assertEqual("KEEPALIVE_NOT_DUE", event["result"])
        self.assertFalse(transport.calls)

    def test_valid_guarded_authority_can_send_one_rotation(self):
        transport = FakeTransport(age=600)
        event = run_keepalive_once(valid_snapshot(), valid_authority(), transport)
        self.assertEqual("KEEPALIVE_ROTATION_SENT", event["result"])
        self.assertEqual(1, len(transport.calls))
        self.assertEqual(123, transport.calls[0]["pid"])
        self.assertEqual(99, transport.calls[0]["xid"])
        self.assertFalse(event["semantic_evidence"])

    def test_expired_lease_refuses_input(self):
        snapshot = valid_snapshot()
        snapshot["canonical_control"]["lease_expired"] = True
        transport = FakeTransport(age=600)
        event = run_keepalive_once(snapshot, valid_authority(), transport)
        self.assertEqual("KEEPALIVE_SKIPPED_UNAUTHORIZED", event["result"])
        self.assertFalse(transport.calls)
        self.assertIn("CANONICAL_LEASE_EXPIRED_OR_UNKNOWN", event["authority_reasons"])


if __name__ == "__main__":
    unittest.main()
