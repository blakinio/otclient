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


class PropertyDispatchSelectionTests(unittest.TestCase):
    def test_selects_read_property_full_range_candidate(self):
        candidates = [
            {"selector_values": [0], "full_range": True, "table": 0x1000},
            {"selector_values": [1], "full_range": True, "table": 0x2000},
            {"selector_values": [2], "full_range": True, "table": 0x3000},
        ]
        result = module.select_unique_property_dispatch_candidate(candidates, 1)
        self.assertEqual(0x2000, result["table"])

    def test_rejects_ambiguous_read_property_tables(self):
        candidates = [
            {"selector_values": [1], "full_range": True, "table": 0x2000},
            {"selector_values": [1], "full_range": True, "table": 0x2100},
        ]
        with self.assertRaisesRegex(module.DurableStateError, "READ_PROPERTY_DISPATCH_NOT_UNIQUE"):
            module.select_unique_property_dispatch_candidate(candidates, 1)

    def test_rejects_selector_context_polluted_by_other_calls(self):
        candidates = [{"selector_values": [0, 1], "full_range": True, "table": 0x2000}]
        with self.assertRaisesRegex(module.DurableStateError, "READ_PROPERTY_DISPATCH_NOT_UNIQUE"):
            module.select_unique_property_dispatch_candidate(candidates, 1)


class PropertyCaseTraceTests(unittest.TestCase):
    def test_stops_at_terminal_jump_and_retains_direct_call(self):
        raw = bytearray(0x80)
        # 0x1000 mov rax,[rdi+0x20]; 0x1004 call 0x1010; 0x1009 jmp 0x1015
        raw[:14] = bytes.fromhex("488b4720e807000000e907000000")
        sections = [(0x1000, 0, 0x80, 0x6)]
        trace = module.extract_bounded_case_trace(bytes(raw), sections, 0x1000)
        self.assertEqual([0x1010], trace["direct_calls"])
        self.assertEqual(0x1015, trace["terminal_jump"])
        self.assertEqual(3, len(trace["instructions"]))


class QStringBackingMemberShapeTests(unittest.TestCase):
    def test_classifies_direct_24_byte_qstring_member_copy(self):
        trace = {"instructions": [
            {"mnemonic": "movdqu", "op_str": "xmm0, xmmword ptr [rbx + 0x60]"},
            {"mnemonic": "mov", "op_str": "rdx, qword ptr [rbx + 0x70]"},
            {"mnemonic": "call", "op_str": "0x6a7270"},
        ]}
        result = module.classify_qstring_member_copy(trace)
        self.assertEqual("rbx", result["base_register"])
        self.assertEqual(0x60, result["member_offset"])
        self.assertEqual(24, result["byte_width"])

    def test_ignores_stack_qstring_temporary_copy(self):
        trace = {"instructions": [
            {"mnemonic": "movdqu", "op_str": "xmm0, xmmword ptr [rbx + 0x60]"},
            {"mnemonic": "mov", "op_str": "rdx, qword ptr [rbx + 0x70]"},
            {"mnemonic": "movdqu", "op_str": "xmm1, xmmword ptr [rsp + 0x50]"},
            {"mnemonic": "mov", "op_str": "rax, qword ptr [rsp + 0x60]"},
            {"mnemonic": "call", "op_str": "0x6a7270"},
        ]}
        result = module.classify_qstring_member_copy(trace)
        self.assertEqual("rbx", result["base_register"])
        self.assertEqual(0x60, result["member_offset"])

    def test_rejects_noncontiguous_qstring_shape(self):
        trace = {"instructions": [
            {"mnemonic": "movdqu", "op_str": "xmm0, xmmword ptr [rbx + 0x60]"},
            {"mnemonic": "mov", "op_str": "rdx, qword ptr [rbx + 0x78]"},
        ]}
        with self.assertRaisesRegex(module.DurableStateError, "QSTRING_MEMBER_COPY_NOT_UNIQUE"):
            module.classify_qstring_member_copy(trace)


class QMetaBackingObjectAliasTests(unittest.TestCase):
    def test_proves_backing_member_base_from_static_metacall_prologue(self):
        entry = {"instructions": [
            {"mnemonic": "push", "op_str": "rbx"},
            {"mnemonic": "mov", "op_str": "rbx, rdi"},
            {"mnemonic": "sub", "op_str": "rsp, 0x98"},
        ]}
        shape = {"base_register": "rbx", "member_offset": 0x60, "byte_width": 24}
        result = module.prove_qmeta_backing_member(entry, shape)
        self.assertEqual(0x60, result["member_offset"])
        self.assertEqual("rdi", result["qmeta_object_argument_register"])

    def test_rejects_unbound_backing_register(self):
        entry = {"instructions": [{"mnemonic": "mov", "op_str": "rbx, rax"}]}
        shape = {"base_register": "rbx", "member_offset": 0x60, "byte_width": 24}
        with self.assertRaisesRegex(module.DurableStateError, "QMETA_BACKING_OBJECT_ALIAS_NOT_PROVEN"):
            module.prove_qmeta_backing_member(entry, shape)


class QMetaSignalEmitterScanTests(unittest.TestCase):
    def test_finds_direct_signal_activation_stub(self):
        raw = bytearray(0x300)
        # xor ecx,ecx; mov edx,24; lea rsi,[rip+0xf2] -> 0x1100; jmp 0x1200
        code = bytes.fromhex("31c9ba18000000488d35f2000000e9ed010000")
        raw[:len(code)] = code
        sections = [
            (0x1000, 0, 0x80, 0x6),
            (0x1100, 0x100, 0x40, 0x2),
            (0x1200, 0x200, 0x40, 0x6),
        ]
        sites = module.scan_qmeta_signal_activation_sites(bytes(raw), sections, 0x1100, 24, 0x1200)
        self.assertEqual(1, len(sites))
        self.assertEqual(0x1000, sites[0]["sequence_start_va"])
        self.assertEqual(0x100e, sites[0]["branch_site_va"])
        self.assertEqual([24], sites[0]["edx_values"])
        self.assertEqual([0x1100], sites[0]["static_meta_refs"])
        self.assertEqual(0x1000, sites[0]["context"][0]["address"])
        self.assertEqual(2, sites[0]["context"][0]["size"])

    def test_rejects_wrong_signal_index(self):
        raw = bytearray(0x300)
        raw[:19] = bytes.fromhex("31c9ba17000000488d35f2000000e9ed010000")
        sections = [(0x1000,0,0x80,0x6),(0x1100,0x100,0x40,0x2),(0x1200,0x200,0x40,0x6)]
        sites = module.scan_qmeta_signal_activation_sites(bytes(raw), sections, 0x1100, 24, 0x1200)
        self.assertEqual([], sites)


class QStringStateAssignmentSourceTests(unittest.TestCase):
    def test_extracts_rip_source_for_backing_member_assignment(self):
        sites = [{"sequence_start_va": 0x2000, "context": [
            {"address": 0x2000, "size": 7, "mnemonic": "lea", "op_str": "rsi, [rip + 0xf9]"},
            {"address": 0x2007, "size": 7, "mnemonic": "lea", "op_str": "rdi, [rbx + 0x60]"},
            {"address": 0x200e, "size": 5, "mnemonic": "call", "op_str": "0x3000"},
        ]}]
        result = module.extract_qstring_member_assignment_sources(sites, 0x60)
        self.assertEqual(1, len(result))
        self.assertEqual(0x2100, result[0]["source_va"])
        self.assertEqual(0x3000, result[0]["helper_target_va"])

    def test_ignores_other_member_offsets(self):
        sites = [{"sequence_start_va": 0x2000, "context": [
            {"address": 0x2000, "size": 7, "mnemonic": "lea", "op_str": "rsi, [rip + 0xf9]"},
            {"address": 0x2007, "size": 7, "mnemonic": "lea", "op_str": "rdi, [rbx + 0x80]"},
            {"address": 0x200e, "size": 5, "mnemonic": "call", "op_str": "0x3000"},
        ]}]
        self.assertEqual([], module.extract_qstring_member_assignment_sources(sites, 0x60))


class StaticQStringSourceDecodeTests(unittest.TestCase):
    def test_decodes_relocation_backed_qstring_source(self):
        raw = bytearray(0x800)
        sections = [(0x400, 0x400, 0x400, 2)]
        source = 0x480
        data = 0x600
        text = "GameScreen"
        struct.pack_into("<q", raw, source + 16, len(text))
        raw[data:data + len(text.encode("utf-16-le"))] = text.encode("utf-16-le")
        relocs = {source: 0x500, source + 8: data}
        result = module.decode_static_qstring_source(bytes(raw), sections, relocs, source)
        self.assertEqual("GameScreen", result["value"])
        self.assertEqual(len(text), result["length"])
        self.assertEqual(data, result["data_va"])

    def test_rejects_unbounded_qstring_source(self):
        raw = bytearray(0x800)
        sections = [(0x400, 0x400, 0x400, 2)]
        source = 0x480
        struct.pack_into("<q", raw, source + 16, 257)
        relocs = {source: 0x500, source + 8: 0x600}
        with self.assertRaisesRegex(module.DurableStateError, "STATIC_QSTRING_LENGTH_OUT_OF_BOUNDS"):
            module.decode_static_qstring_source(bytes(raw), sections, relocs, source)


class GlobalQStringInitializerXrefTests(unittest.TestCase):
    def test_finds_rip_reference_to_bss_source_with_context(self):
        raw = bytearray(0x400)
        # 0x1000: lea rdi,[rip+0xf9] -> 0x1100; nop; ret
        raw[0x100:0x108] = bytes.fromhex("48 8d 3d f9 00 00 00 90")
        raw[0x108] = 0xC3
        sections = [(0x1000, 0x100, 0x100, 6)]
        result = module.scan_rip_target_xrefs(bytes(raw), sections, {0x1100})
        self.assertIn(0x1100, result)
        self.assertEqual(1, len(result[0x1100]))
        self.assertEqual(0x1000, result[0x1100][0]["reference_va"])
        self.assertEqual("lea", result[0x1100][0]["reference"]["mnemonic"])

    def test_ignores_other_rip_targets(self):
        raw = bytearray(0x400)
        raw[0x100:0x108] = bytes.fromhex("48 8d 3d f9 00 00 00 90")
        raw[0x108] = 0xC3
        sections = [(0x1000, 0x100, 0x100, 6)]
        result = module.scan_rip_target_xrefs(bytes(raw), sections, {0x1200})
        self.assertEqual({0x1200: []}, result)


if __name__ == "__main__":
    unittest.main()
