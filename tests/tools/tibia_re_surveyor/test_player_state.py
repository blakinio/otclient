import unittest

from tools.tibia_re_surveyor.player_state import (
    CURRENT_LAYOUT,
    READ_ONLY_PROBE,
    PlayerStateResolverError,
    derive_mirrored_position_offsets,
    read_player_state,
    resolve_layout,
    validate_mirrored_position,
)


class PlayerStateResolverTests(unittest.TestCase):
    def test_current_layout_is_exact_current_build_discovery(self):
        self.assertEqual(0x30C2738, CURRENT_LAYOUT.vptr)
        self.assertEqual(0x30C0AA0, CURRENT_LAYOUT.typeinfo)
        self.assertEqual(0xD1EEF0, CURRENT_LAYOUT.metacast)
        self.assertEqual(0xD19EF0, CURRENT_LAYOUT.position_handler)
        self.assertEqual((0x2F0, 0x2F4, 0x2F8), CURRENT_LAYOUT.primary_offsets)
        self.assertEqual((0x408, 0x40C, 0x410), CURRENT_LAYOUT.mirror_offsets)

    def test_resolver_correlates_cyclopedia_type_and_mirrored_position_handler(self):
        strings = """1d45698 tibia::cyclopedia::TCyclopediaMapStorage
1d01060 N5tibia10cyclopedia21TCyclopediaMapStorageE
1d456f7 playerPositionChanged
1d45860 onPlayerPositionWasUpdated
"""
        relocs = """00000000030c0aa8  0 R_X86_64_RELATIVE 1d01060
00000000030c2730  0 R_X86_64_RELATIVE 30c0aa0
00000000030c2738  0 R_X86_64_RELATIVE d0c7e0
00000000030c2740  0 R_X86_64_RELATIVE d1eef0
00000000030c2748  0 R_X86_64_RELATIVE d224c0
"""
        metacast = {0xD1EEF0: "d1eefd: lea 0x0(%rip),%rsi # 1d45698\n"}
        handler = {0xD19EF0: """d19ef8: mov 0x8(%rcx),%rax
d19efc: movq 0x8(%rax),%xmm0
d19f09: mov 0x10(%rax),%eax
d19f01: movq %xmm0,0x408(%rdi)
d19f0c: movq %xmm0,0x2f0(%rdi)
d19f14: paddd %xmm1,%xmm0
d19f18: mov %eax,0x410(%rdi)
d19f1e: mov %eax,0x2f8(%rdi)
d19f24: add $0x1,%eax
d19f27: mov %eax,0x310(%rdi)
d19f37: movq %xmm0,0x308(%rdi)
"""}
        self.assertEqual(
            CURRENT_LAYOUT,
            resolve_layout(
                strings_text=strings,
                relocations_text=relocs,
                metacast_disassembly=metacast,
                position_handler_disassembly=handler,
            ),
        )

    def test_real_handler_shape_recovers_two_mirrored_copies(self):
        text = """d19ef8:\t48 8b 41 08          \tmov    0x8(%rcx),%rax
d19efc:\tf3 0f 7e 40 08       \tmovq   0x8(%rax),%xmm0
d19f01:\t66 0f d6 87 08 04 00 00 \tmovq   %xmm0,0x408(%rdi)
d19f09:\t8b 40 10             \tmov    0x10(%rax),%eax
d19f0c:\t66 0f d6 87 f0 02 00 00 \tmovq   %xmm0,0x2f0(%rdi)
d19f14:\t66 0f fe c1          \tpaddd  %xmm1,%xmm0
d19f18:\t89 87 10 04 00 00    \tmov    %eax,0x410(%rdi)
d19f1e:\t89 87 f8 02 00 00    \tmov    %eax,0x2f8(%rdi)
d19f24:\t83 c0 01             \tadd    $0x1,%eax
d19f27:\t89 87 10 03 00 00    \tmov    %eax,0x310(%rdi)
d19f37:\t66 0f d6 87 08 03 00 00 \tmovq   %xmm0,0x308(%rdi)
"""
        self.assertEqual(
            ((0x2F0, 0x2F4, 0x2F8), (0x408, 0x40C, 0x410)),
            derive_mirrored_position_offsets(text),
        )

    def test_missing_second_copy_fails_closed(self):
        text = """1: movq 0x8(%rax),%xmm0
2: mov 0x10(%rax),%eax
3: movq %xmm0,0x100(%rdi)
4: mov %eax,0x108(%rdi)
5: paddd %xmm1,%xmm0
6: add $0x1,%eax
"""
        with self.assertRaises(PlayerStateResolverError):
            derive_mirrored_position_offsets(text)

    def test_mirror_mismatch_and_implausible_values_fail_closed(self):
        self.assertEqual(
            (32547, 32506, 7),
            validate_mirrored_position((32547, 32506, 7), (32547, 32506, 7)),
        )
        with self.assertRaises(PlayerStateResolverError):
            validate_mirrored_position((32547, 32506, 7), (32548, 32506, 7))
        with self.assertRaises(PlayerStateResolverError):
            validate_mirrored_position((0, 32506, 7), (0, 32506, 7))
        with self.assertRaises(PlayerStateResolverError):
            validate_mirrored_position((32547, 32506, 16), (32547, 32506, 16))

    def test_runtime_probe_remains_strictly_read_only(self):
        self.assertIn("os.O_RDONLY|os.O_CLOEXEC", READ_ONLY_PROBE)
        self.assertNotIn("os.pwrite", READ_ONLY_PROBE)
        self.assertNotIn("O_RDWR", READ_ONLY_PROBE)
        self.assertNotIn("O_WRONLY", READ_ONLY_PROBE)
        self.assertIn("CYCLOPEDIA_POSITION_MIRROR_MISMATCH", READ_ONLY_PROBE)

    def test_runtime_failure_is_nonsemantic_unavailable(self):
        result = read_player_state(
            pid=1,
            start_ticks=2,
            runner=lambda args: (_ for _ in ()).throw(RuntimeError("no runtime")),
        )
        self.assertEqual("UNAVAILABLE", result["state"])
        self.assertFalse(result["semantic_promotion_allowed"])


if __name__ == "__main__":
    unittest.main()
