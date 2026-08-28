from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest
import struct

SCRIPT = Path(__file__).with_name("track_a_current_world_entered_durable_state.py")
spec = importlib.util.spec_from_file_location("durable_state", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DurableStateSelectionTests(unittest.TestCase):
    def test_selects_field_set_on_world_and_reset_by_two_exit_paths(self):
        observations = {
            "onWorldEntered": [{"offset": 0x128, "width": 1, "value": 1}],
            "onGameSessionDisconnected": [{"offset": 0x128, "width": 1, "value": 0}],
            "onDialogResponseShowCharacterSelection": [{"offset": 0x128, "width": 1, "value": 0}],
            "onDialogResponseShowLoginDialog": [],
        }
        result = module.select_durable_field_candidate(observations)
        self.assertEqual(0x128, result["offset"])
        self.assertEqual(1, result["world_value"])
        self.assertEqual(0, result["reset_value"])
        self.assertEqual(2, len(result["reset_methods"]))
    def test_rejects_ambiguous_world_fields(self):
        observations = {
            "onWorldEntered": [
                {"offset": 0x128, "width": 1, "value": 1},
                {"offset": 0x130, "width": 1, "value": 1},
            ],
            "onGameSessionDisconnected": [
                {"offset": 0x128, "width": 1, "value": 0},
                {"offset": 0x130, "width": 1, "value": 0},
            ],
            "onDialogResponseShowCharacterSelection": [
                {"offset": 0x128, "width": 1, "value": 0},
                {"offset": 0x130, "width": 1, "value": 0},
            ],
        }
        with self.assertRaisesRegex(module.DurableStateError, "DURABLE_FIELD_NOT_UNIQUE"):
            module.select_durable_field_candidate(observations)

    def test_rejects_single_reset_path(self):
        observations = {
            "onWorldEntered": [{"offset": 0x128, "width": 1, "value": 1}],
            "onGameSessionDisconnected": [{"offset": 0x128, "width": 1, "value": 0}],
            "onDialogResponseShowCharacterSelection": [],
            "onDialogResponseShowLoginDialog": [],
        }
        with self.assertRaisesRegex(module.DurableStateError, "DURABLE_FIELD_RESET_PATHS_INSUFFICIENT"):
            module.select_durable_field_candidate(observations)


class QMetaPropertyParsingTests(unittest.TestCase):
    def test_parses_qt6_five_word_property_rows(self):
        raw = bytearray(0x800)
        stringdata = 0x200
        metadata = 0x500
        texts = ["gameVisible", "bool", "sessionState"]
        cursor = 0x300
        for index, text in enumerate(texts):
            encoded = text.encode("utf-8")
            struct.pack_into("<II", raw, stringdata + index * 8, cursor - stringdata, len(encoded))
            raw[cursor:cursor + len(encoded)] = encoded
            cursor += len(encoded) + 1
        rows = [
            [0, 1, 0x00000001, 3, 0],
            [2, 0x80000001, 0x00000001, 4, 2],
        ]
        for row_index, row in enumerate(rows):
            for field_index, value in enumerate(row):
                struct.pack_into("<I", raw, metadata + (14 + row_index * 5 + field_index) * 4, value)
        sections = [(0x100, 0x100, 0x700, 2)]
        properties = module.parse_qmeta_properties(bytes(raw), sections, stringdata, metadata, 2, 14)
        self.assertEqual(["gameVisible", "sessionState"], [p["name"] for p in properties])
        self.assertEqual(1, properties[0]["raw_type"])
        self.assertEqual("bool", properties[0]["type_name"])
        self.assertEqual("bool", properties[1]["type_name"])
        self.assertEqual(2, properties[1]["revision"])

    def test_semantic_property_filter_is_bounded(self):
        properties = [
            {"name": "mapZoom"},
            {"name": "gameVisible"},
            {"name": "sessionState"},
            {"name": "worldName"},
            {"name": "healthBarVisible"},
        ]
        names = [p["name"] for p in module.select_world_semantic_properties(properties)]
        self.assertEqual(["gameVisible", "sessionState", "worldName"], names)


if __name__ == "__main__":
    unittest.main()
