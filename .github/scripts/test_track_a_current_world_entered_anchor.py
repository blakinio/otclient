#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path
import struct
import unittest

MODULE_PATH = Path(__file__).with_name("track_a_current_world_entered_anchor.py")
spec = importlib.util.spec_from_file_location("world_entered_anchor", MODULE_PATH)
if spec is None or spec.loader is None:
    raise SystemExit("WORLD_ENTERED_ANCHOR_IMPORT_SPEC_FAILED")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

CLASS_NAME = "tibia::game::TPlayerProtocolMessageHandler"


def put_u32(raw: bytearray, offset: int, values: list[int]) -> None:
    for index, value in enumerate(values):
        struct.pack_into("<I", raw, offset + index * 4, value)


def make_fixture(*, duplicate: bool = False, signal_count: int = 3):
    raw = bytearray(0x2000)
    text_va = 0x100
    data_va = 0x400
    static_meta = 0x400
    stringdata = 0x600
    metadata = 0x900
    static_metacall = 0x180
    names = [CLASS_NAME, "sendEnterWorld", "worldEntered", "publishGameAction"]
    if duplicate:
        names[3] = "worldEntered"
    cursor = 0x700
    for index, text in enumerate(names):
        encoded = text.encode("utf-8")
        struct.pack_into("<II", raw, stringdata + index * 8, cursor - stringdata, len(encoded))
        raw[cursor : cursor + len(encoded)] = encoded
        cursor += len(encoded) + 1

    header = [12, 0, 0, 0, 3, 14, 0, 0, 0, 0, 0, 0, 0, signal_count]
    put_u32(raw, metadata, header)
    rows = [
        [1, 0, 32, 0, 0x06, 0],
        [2, 0, 33, 0, 0x06, 0],
        [3, 0, 34, 0, 0x06, 0],
    ]
    row_offset = metadata + 14 * 4
    for row in rows:
        put_u32(raw, row_offset, row)
        row_offset += 6 * 4

    sections = [
        (text_va, text_va, 0x200, module.SHF_ALLOC | module.SHF_EXECINSTR),
        (data_va, data_va, 0x1400, module.SHF_ALLOC),
    ]
    relocs = {
        static_meta + 8: stringdata,
        static_meta + 16: metadata,
        static_meta + 24: static_metacall,
    }
    return bytes(raw), sections, relocs


class WorldEnteredAnchorTests(unittest.TestCase):
    def test_recovers_unique_zero_arg_world_entered_signal(self):
        raw, sections, relocs = make_fixture()
        result = module.recover_world_entered_anchor(raw, sections, relocs)
        self.assertEqual(CLASS_NAME, result["class_name"])
        self.assertEqual(0x400, result["static_metaobject_va"])
        self.assertEqual(0x600, result["stringdata_va"])
        self.assertEqual(0x900, result["metadata_va"])
        self.assertEqual(0x180, result["static_metacall_va"])
        self.assertEqual(3, result["method_count"])
        self.assertEqual(3, result["signal_count"])
        self.assertEqual(1, result["world_entered_method_index"])
        self.assertEqual(0, result["world_entered_argc"])
        self.assertTrue(result["world_entered_is_signal"])

    def test_rejects_duplicate_world_entered_methods(self):
        raw, sections, relocs = make_fixture(duplicate=True)
        with self.assertRaisesRegex(module.AnchorError, "WORLD_ENTERED_NOT_UNIQUE"):
            module.recover_world_entered_anchor(raw, sections, relocs)

    def test_rejects_world_entered_outside_signal_range(self):
        raw, sections, relocs = make_fixture(signal_count=1)
        with self.assertRaisesRegex(module.AnchorError, "WORLD_ENTERED_NOT_SIGNAL"):
            module.recover_world_entered_anchor(raw, sections, relocs)



# Additional activation-boundary behavioral checks.
class ActivationBoundaryTests(unittest.TestCase):
    def test_selects_unique_branch_target_common_to_all_signal_traces(self):
        traces = [
            {"branch_targets": [0x5000, 0x7000 + index]}
            for index in range(3)
        ]
        self.assertEqual(0x5000, module.select_unique_common_branch_target(traces))

    def test_rejects_multiple_common_branch_targets(self):
        traces = [
            {"branch_targets": [0x5000, 0x6000, 0x7000 + index]}
            for index in range(3)
        ]
        with self.assertRaisesRegex(module.AnchorError, "COMMON_ACTIVATION_TARGET_NOT_UNIQUE"):
            module.select_unique_common_branch_target(traces)

    def test_requires_world_signal_index_and_static_metaobject_reference(self):
        trace = {"edx_values": [17], "rip_refs": [0x30B6BA0]}
        self.assertTrue(module.require_signal_activation_arguments(trace, 17, 0x30B6BA0))
        with self.assertRaisesRegex(module.AnchorError, "SIGNAL_INDEX_ARGUMENT_NOT_PROVEN"):
            module.require_signal_activation_arguments(trace, 18, 0x30B6BA0)
        with self.assertRaisesRegex(module.AnchorError, "STATIC_METAOBJECT_ARGUMENT_NOT_PROVEN"):
            module.require_signal_activation_arguments(trace, 17, 0x1234)

if __name__ == "__main__":
    unittest.main()
