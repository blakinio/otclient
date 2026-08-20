import unittest

from tools.tibia_re_surveyor.player_state import (
    CURRENT_LAYOUT,
    PlayerStateResolverError,
    derive_position_offsets,
    read_player_state,
    resolve_layout,
)


class PlayerStateResolverTests(unittest.TestCase):
    def test_current_layout_is_current_fence_discovery(self):
        self.assertEqual(0x30C1810, CURRENT_LAYOUT.vptr)
        self.assertEqual(0xD40470, CURRENT_LAYOUT.metacast)
        self.assertEqual(0x82D101, CURRENT_LAYOUT.position_xref)
        self.assertEqual((0x78, 0x7C, 0x80), CURRENT_LAYOUT.offsets)

    def test_parsers_recover_bounded_relationships(self):
        strings = "1cc3e58 tibia::game::TPlayerData\n1d00d50 N5tibia4game11TPlayerDataE\n1cfee4c playerPosition\n"
        relocs = """00000000030c1808  0 R_X86_64_RELATIVE 30c0938
00000000030c1810  0 R_X86_64_RELATIVE d2a8a0
00000000030c1818  0 R_X86_64_RELATIVE d40470
00000000030c1820  0 R_X86_64_RELATIVE d436a0
00000000030c0940  0 R_X86_64_RELATIVE 1d00d50
"""
        xrefs = "d4047d: lea # 1cc3e58\n82d101: lea # 1cfee4c\n"
        disasm = {0x82D101: """82cf99: movslq 0x78(%rbx),%rdx
82cfbe: movslq 0x7c(%rbx),%rdx
82cff3: movslq 0x80(%rbx),%rdx
82d101: lea 0x0(%rip),%rdx # 1cfee4c
"""}
        layout = resolve_layout(
            strings_text=strings,
            relocations_text=relocs,
            xrefs_text=xrefs,
            position_disassembly=disasm,
        )
        self.assertEqual(CURRENT_LAYOUT, layout)

    def test_real_objdump_byte_columns_are_accepted(self):
        text = """82cf99:\t48 63 53 78          \tmovslq 0x78(%rbx),%rdx
82cfbe:\t48 63 53 7c          \tmovslq 0x7c(%rbx),%rdx
82cff3:\t48 63 93 80 00 00 00 \tmovslq 0x80(%rbx),%rdx
82d101:\t48 8d 15 44 1d 4d 01 \tlea 0x14d1d44(%rip),%rdx # 1cfee4c
"""
        self.assertEqual((0x78, 0x7C, 0x80), derive_position_offsets(text, xref=0x82D101))

    def test_ambiguous_position_triplet_fails_closed(self):
        text = """100: movslq 0x10(%rbx),%rdx
104: movslq 0x14(%rbx),%rdx
108: movslq 0x18(%rbx),%rdx
110: movslq 0x20(%rbx),%rdx
114: movslq 0x24(%rbx),%rdx
118: movslq 0x28(%rbx),%rdx
200: lea 0x0(%rip),%rdx
"""
        with self.assertRaises(PlayerStateResolverError):
            derive_position_offsets(text, xref=0x200)

    def test_runtime_failure_is_nonsemantic_unavailable(self):
        result = read_player_state(pid=1, start_ticks=2, runner=lambda args: (_ for _ in ()).throw(RuntimeError("no runtime")))
        self.assertEqual("UNAVAILABLE", result["state"])
        self.assertFalse(result["semantic_promotion_allowed"])


if __name__ == "__main__":
    unittest.main()
