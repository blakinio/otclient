import json
import unittest

from tools.tibia_re_surveyor.action_protocol import (
    MANGLED_TYPE_NAME,
    READER_ID,
    TYPE_NAME,
    read_action_protocol,
)


class ActionProtocolReaderTests(unittest.TestCase):
    def test_available_reader_keeps_structural_semantic_boundary(self):
        calls = []

        def runner(command):
            calls.append(command)
            if len(calls) == 1:
                return json.dumps(
                    {
                        "state": "AVAILABLE",
                        "type_name": TYPE_NAME,
                        "mangled_name": MANGLED_TYPE_NAME,
                        "vptr_offset": 0x4010,
                        "typeinfo_offset": 0x3000,
                    }
                )
            return json.dumps(
                {
                    "state": "AVAILABLE",
                    "reader_id": READER_ID,
                    "type_name": TYPE_NAME,
                    "object_count": 1,
                    "typed_object_identity": "PROVEN",
                    "process_memory_access": "read_only",
                }
            )

        doc = read_action_protocol(pid=123, start_ticks=456, runner=runner)
        self.assertEqual("AVAILABLE", doc["state"])
        self.assertEqual("TYPED_ACTION_PROTOCOL_OBJECT_IDENTITY_ONLY", doc["semantic_state"])
        self.assertTrue(doc["protocol_message_handler_present"])
        self.assertFalse(doc["action_to_protocol_connection_claimed"])
        self.assertFalse(doc["serialized_message_semantics_claimed"])
        self.assertFalse(doc["protocol_opcodes_claimed"])
        self.assertFalse(doc["packet_payloads_retained"])
        self.assertFalse(doc["in_game_claimed"])
        self.assertFalse(doc["semantic_promotion_allowed"])
        self.assertEqual("0x4010", doc["layout_evidence"]["vptr_offset"])
        self.assertEqual("0x3000", doc["layout_evidence"]["typeinfo_offset"])
        self.assertEqual(2, len(calls))
        self.assertEqual("python3", calls[0][3])
        self.assertEqual("python3", calls[1][3])

    def test_static_resolution_failure_returns_unavailable(self):
        def runner(command):
            raise RuntimeError("static parser failed")

        doc = read_action_protocol(pid=123, start_ticks=456, runner=runner)
        self.assertEqual("UNAVAILABLE", doc["state"])
        self.assertEqual("STATIC_LAYOUT_FAILED:RuntimeError", doc["reason"])
        self.assertFalse(doc["semantic_promotion_allowed"])

    def test_live_probe_failure_preserves_static_layout_evidence(self):
        calls = []

        def runner(command):
            calls.append(command)
            if len(calls) == 1:
                return json.dumps(
                    {
                        "state": "AVAILABLE",
                        "type_name": TYPE_NAME,
                        "mangled_name": MANGLED_TYPE_NAME,
                        "vptr_offset": 0x4010,
                        "typeinfo_offset": 0x3000,
                    }
                )
            raise RuntimeError("live probe failed")

        doc = read_action_protocol(pid=123, start_ticks=456, runner=runner)
        self.assertEqual("UNAVAILABLE", doc["state"])
        self.assertEqual("LIVE_TYPED_PROBE_FAILED:RuntimeError", doc["reason"])
        self.assertEqual("0x4010", doc["layout_evidence"]["vptr_offset"])
        self.assertEqual("0x3000", doc["layout_evidence"]["typeinfo_offset"])
        self.assertFalse(doc["semantic_promotion_allowed"])


if __name__ == "__main__":
    unittest.main()
