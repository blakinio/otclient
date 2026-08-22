import json
import unittest

from tools.tibia_re_surveyor.action_protocol_presence import (
    DIAGNOSTIC_READ_ONLY_PRESENCE_PROBE,
    read_action_protocol_presence,
)
from tools.tibia_re_surveyor.typed_presence import READ_ONLY_PRESENCE_PROBE

READER_ID = "action_protocol_typed_reader"
TYPE_NAME = "tibia::game::TPlayerProtocolMessageHandler"
MANGLED = "N5tibia4game29TPlayerProtocolMessageHandlerE"


class ActionProtocolPresenceTests(unittest.TestCase):
    @staticmethod
    def _layout():
        return json.dumps(
            {
                "state": "AVAILABLE",
                "type_name": TYPE_NAME,
                "mangled_name": MANGLED,
                "vptr_offset": 0x4010,
                "typeinfo_offset": 0x3000,
            }
        )

    def test_diagnostic_probe_stays_read_only_count_only_and_action_bounded(self):
        self.assertIn("os.O_RDONLY", DIAGNOSTIC_READ_ONLY_PRESENCE_PROBE)
        self.assertNotIn("os.O_RDWR", DIAGNOSTIC_READ_ONLY_PRESENCE_PROBE)
        self.assertIn("raw_hits.append(obj)", DIAGNOSTIC_READ_ONLY_PRESENCE_PROBE)
        self.assertIn("RAW_VPTR_COUNT=", DIAGNOSTIC_READ_ONLY_PRESENCE_PROBE)
        self.assertIn("> 2*1024*1024*1024", DIAGNOSTIC_READ_ONLY_PRESENCE_PROBE)
        self.assertNotIn("> 1536*1024*1024", DIAGNOSTIC_READ_ONLY_PRESENCE_PROBE)
        self.assertIn("> 1536*1024*1024", READ_ONLY_PRESENCE_PROBE)
        self.assertNotIn("> 2*1024*1024*1024", READ_ONLY_PRESENCE_PROBE)

    def test_live_count_failure_preserves_only_safe_counts(self):
        calls = []

        def runner(command):
            calls.append(command)
            if len(calls) == 1:
                return self._layout()
            raise RuntimeError("TYPED_OBJECT_COUNT=0 RAW_VPTR_COUNT=1")

        doc = read_action_protocol_presence(
            reader_id=READER_ID,
            type_name=TYPE_NAME,
            mangled_name=MANGLED,
            pid=123,
            start_ticks=456,
            runner=runner,
        )
        self.assertEqual("UNAVAILABLE", doc["state"])
        self.assertEqual(
            "LIVE_TYPED_PROBE_FAILED:TYPED_OBJECT_COUNT=0:RAW_VPTR_COUNT=1",
            doc["reason"],
        )
        self.assertEqual("0x4010", doc["layout_evidence"]["vptr_offset"])
        self.assertEqual("0x3000", doc["layout_evidence"]["typeinfo_offset"])
        self.assertFalse(doc["semantic_promotion_allowed"])

    def test_unknown_live_failure_does_not_expose_exception_text(self):
        calls = []

        def runner(command):
            calls.append(command)
            if len(calls) == 1:
                return self._layout()
            raise RuntimeError("sensitive arbitrary child stderr")

        doc = read_action_protocol_presence(
            reader_id=READER_ID,
            type_name=TYPE_NAME,
            mangled_name=MANGLED,
            pid=123,
            start_ticks=456,
            runner=runner,
        )
        self.assertEqual("LIVE_TYPED_PROBE_FAILED:RuntimeError", doc["reason"])
        self.assertNotIn("sensitive", json.dumps(doc))

    def test_success_contract_is_unchanged(self):
        calls = []

        def runner(command):
            calls.append(command)
            if len(calls) == 1:
                return self._layout()
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

        doc = read_action_protocol_presence(
            reader_id=READER_ID,
            type_name=TYPE_NAME,
            mangled_name=MANGLED,
            pid=123,
            start_ticks=456,
            runner=runner,
        )
        self.assertEqual("AVAILABLE", doc["state"])
        self.assertEqual(1, doc["object_count"])
        self.assertEqual("PROVEN", doc["typed_object_identity"])
        self.assertEqual("read_only", doc["process_memory_access"])
        self.assertFalse(doc["semantic_promotion_allowed"])


if __name__ == "__main__":
    unittest.main()
