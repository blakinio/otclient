import json
import unittest

from tools.tibia_re_surveyor.action_protocol import (
    MANGLED_TYPE_NAME,
    READER_ID,
    TYPE_NAME,
    read_action_protocol,
)


STRINGS = f"1000 {TYPE_NAME}\n2000 {MANGLED_TYPE_NAME}\n"
RELOCS = (
    "0000000000003008  0000000000000008 R_X86_64_RELATIVE                    2000\n"
    "0000000000004008  0000000000000008 R_X86_64_RELATIVE                    3000\n"
    "0000000000004010  0000000000000008 R_X86_64_RELATIVE                    5000\n"
)


class ActionProtocolReaderTests(unittest.TestCase):
    def test_available_reader_keeps_structural_semantic_boundary(self):
        calls = []

        def runner(command):
            calls.append(command)
            if command[3] == "strings":
                return STRINGS
            if command[3] == "readelf":
                return RELOCS
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
        self.assertEqual(3, len(calls))

    def test_static_resolution_failure_returns_unavailable(self):
        def runner(command):
            if command[3] == "strings":
                return ""
            return RELOCS

        doc = read_action_protocol(pid=123, start_ticks=456, runner=runner)
        self.assertEqual("UNAVAILABLE", doc["state"])
        self.assertTrue(doc["reason"].startswith("READ_FAILED:"))
        self.assertFalse(doc["semantic_promotion_allowed"])


if __name__ == "__main__":
    unittest.main()
