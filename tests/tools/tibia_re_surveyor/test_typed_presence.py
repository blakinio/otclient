import unittest

from tools.tibia_re_surveyor.typed_presence import (
    READ_ONLY_PRESENCE_PROBE,
    TypedPresenceResolverError,
    resolve_primary_vptr,
)


TYPE = "tibia::game::TPlayerProtocolMessageHandler"
MANGLED = "N5tibia4game29TPlayerProtocolMessageHandlerE"


class TypedPresenceResolverTests(unittest.TestCase):
    def test_resolves_unique_primary_vptr_from_exact_rtti_relocations(self):
        layout = resolve_primary_vptr(
            strings_text=f"1000 {TYPE}\n2000 {MANGLED}\n",
            relocations_text=(
                "0000000000003008  0000000000000008 R_X86_64_RELATIVE                    2000\n"
                "0000000000004008  0000000000000008 R_X86_64_RELATIVE                    3000\n"
                "0000000000004010  0000000000000008 R_X86_64_RELATIVE                    5000\n"
            ),
            type_name=TYPE,
            mangled_name=MANGLED,
        )
        self.assertEqual(0x4010, layout.vptr)
        self.assertEqual(0x3000, layout.typeinfo)
        self.assertEqual(TYPE, layout.type_name)

    def test_fails_closed_when_type_string_is_missing(self):
        with self.assertRaises(TypedPresenceResolverError):
            resolve_primary_vptr(
                strings_text=f"2000 {MANGLED}\n",
                relocations_text="",
                type_name=TYPE,
                mangled_name=MANGLED,
            )

    def test_fails_closed_when_primary_vptr_is_ambiguous(self):
        relocations = (
            "0000000000003008  0000000000000008 R_X86_64_RELATIVE                    2000\n"
            "0000000000004008  0000000000000008 R_X86_64_RELATIVE                    3000\n"
            "0000000000004010  0000000000000008 R_X86_64_RELATIVE                    5000\n"
            "0000000000005008  0000000000000008 R_X86_64_RELATIVE                    3000\n"
            "0000000000005010  0000000000000008 R_X86_64_RELATIVE                    6000\n"
        )
        with self.assertRaises(TypedPresenceResolverError):
            resolve_primary_vptr(
                strings_text=f"1000 {TYPE}\n2000 {MANGLED}\n",
                relocations_text=relocations,
                type_name=TYPE,
                mangled_name=MANGLED,
            )

    def test_runtime_probe_is_read_only_and_bounded(self):
        self.assertIn("os.O_RDONLY", READ_ONLY_PRESENCE_PROBE)
        self.assertNotIn("os.O_RDWR", READ_ONLY_PRESENCE_PROBE)
        self.assertIn("RW_SCAN_BOUND_EXCEEDED", READ_ONLY_PRESENCE_PROBE)
        self.assertIn("START_TICKS_CHANGED_DURING_READ", READ_ONLY_PRESENCE_PROBE)
        self.assertIn("EXACT_FENCE_MISMATCH", READ_ONLY_PRESENCE_PROBE)


if __name__ == "__main__":
    unittest.main()
