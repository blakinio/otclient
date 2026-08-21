import json
import unittest

from tools.tibia_re_surveyor.auth_session import (
    CURRENT_LAYOUT,
    QT_STATE_MACHINE_SHA256,
    QT_STATE_MACHINE_SIZE,
    READ_ONLY_PROBE,
    AuthSessionResolverError,
    derive_auth_controller_offset,
    derive_qstate_running_layout,
    read_auth_session,
    resolve_layout,
)


class AuthSessionResolverTests(unittest.TestCase):
    def test_current_layout_matches_exact_current_build_discovery(self):
        self.assertEqual(0x30ADCE8, CURRENT_LAYOUT.game_client_vptr)
        self.assertEqual(0x30A7778, CURRENT_LAYOUT.game_client_typeinfo)
        self.assertEqual(0x30B5290, CURRENT_LAYOUT.auth_controller_vptr)
        self.assertEqual(0x30B4410, CURRENT_LAYOUT.auth_controller_typeinfo)
        self.assertEqual(0x8D0, CURRENT_LAYOUT.auth_controller_offset)
        self.assertEqual(0x8, CURRENT_LAYOUT.qstate_private_offset)
        self.assertEqual(0xF0, CURRENT_LAYOUT.qstate_state_offset)
        self.assertEqual(2, CURRENT_LAYOUT.qstate_running_value)
        self.assertEqual(394824, QT_STATE_MACHINE_SIZE)
        self.assertEqual(
            "26f504ae723fa15c77e0c33a93a964a305c63577f2bed3f136c098b7b06921e8",
            QT_STATE_MACHINE_SHA256,
        )

    def test_resolver_reconstructs_exact_current_layout(self):
        strings = """1cb43b0 tibia::client::TGameClient
1cb3bd0 N5tibia6client11TGameClientE
1c91620 tibia::authentication::TAuthenticationProcessController
1cc4520 N5tibia14authentication32TAuthenticationProcessControllerE
"""
        relocs = """00000000030a7780  0 R_X86_64_RELATIVE 1cb3bd0
00000000030adce0  0 R_X86_64_RELATIVE 30a7778
00000000030adce8  0 R_X86_64_RELATIVE d0c0a0
00000000030b4418  0 R_X86_64_RELATIVE 1cc4520
00000000030b5288  0 R_X86_64_RELATIVE 30b4410
00000000030b5290  0 R_X86_64_RELATIVE d0be00
"""
        game_connected = "6e10eb:\t48 8b 9f d0 08 00 00\tmov    0x8d0(%rdi),%rbx\n"
        is_running = """23844:\t48 8b 47 08\tmov    0x8(%rdi),%rax
23848:\t83 b8 f0 00 00 00 02\tcmpl   $0x2,0xf0(%rax)
2384f:\t0f 94 c0\tsete   %al
"""
        self.assertEqual(
            CURRENT_LAYOUT,
            resolve_layout(
                strings_text=strings,
                relocations_text=relocs,
                game_session_connected_disassembly=game_connected,
                qstate_is_running_disassembly=is_running,
            ),
        )

    def test_auth_controller_member_load_must_be_unique(self):
        self.assertEqual(
            0x8D0,
            derive_auth_controller_offset("1: mov 0x8d0(%rdi),%rbx\n"),
        )
        with self.assertRaises(AuthSessionResolverError):
            derive_auth_controller_offset(
                "1: mov 0x8d0(%rdi),%rbx\n2: mov 0x900(%rdi),%rax\n"
            )

    def test_qstate_is_running_layout_requires_boolean_shape(self):
        text = """1: mov 0x8(%rdi),%rax
2: cmpl $0x2,0xf0(%rax)
3: sete %al
"""
        self.assertEqual((0x8, 0xF0, 2), derive_qstate_running_layout(text))
        with self.assertRaises(AuthSessionResolverError):
            derive_qstate_running_layout("1: mov 0x8(%rdi),%rax\n2: cmpl $0x2,0xf0(%rax)\n")

    def test_runtime_probe_is_strictly_read_only_and_secret_free(self):
        self.assertIn("os.O_RDONLY|os.O_CLOEXEC", READ_ONLY_PROBE)
        self.assertNotIn("os.pwrite", READ_ONLY_PROBE)
        self.assertNotIn("O_RDWR", READ_ONLY_PROBE)
        self.assertNotIn("O_WRONLY", READ_ONLY_PROBE)
        self.assertIn("EXACT_FENCE_MISMATCH", READ_ONLY_PROBE)
        self.assertIn("QT_STATE_MACHINE_FENCE_MISMATCH", READ_ONLY_PROBE)
        self.assertIn("AUTH_CONTROLLER_VPTR_MISMATCH", READ_ONLY_PROBE)
        self.assertNotIn("sessionkey", READ_ONLY_PROBE.lower())
        self.assertNotIn("email", READ_ONLY_PROBE.lower())

    def test_runtime_failure_is_nonsemantic_unavailable(self):
        result = read_auth_session(
            pid=1,
            start_ticks=2,
            runner=lambda args: (_ for _ in ()).throw(RuntimeError("no runtime")),
        )
        self.assertEqual("UNAVAILABLE", result["state"])
        self.assertFalse(result["semantic_promotion_allowed"])

    def test_valid_payload_remains_lifecycle_only(self):
        payload = {
            "state": "AVAILABLE",
            "reader_id": "auth_session_typed_reader",
            "game_client_object_count": 1,
            "authentication_process_object_count": 1,
            "authentication_state_machine_running": False,
            "process_memory_access": "read_only",
            "semantic_state": "TYPED_AUTH_LIFECYCLE_ONLY",
            "in_game_claimed": False,
            "credentials_retained": False,
            "session_secrets_retained": False,
        }
        result = read_auth_session(
            pid=1,
            start_ticks=2,
            runner=lambda args: json.dumps(payload),
        )
        self.assertEqual("AVAILABLE", result["state"])
        self.assertFalse(result["authentication_state_machine_running"])
        self.assertFalse(result["in_game_claimed"])
        self.assertFalse(result["semantic_promotion_allowed"])

    def test_semantically_overclaimed_payload_fails_closed(self):
        payload = {
            "state": "AVAILABLE",
            "reader_id": "auth_session_typed_reader",
            "authentication_state_machine_running": False,
            "process_memory_access": "read_only",
            "semantic_state": "TYPED_AUTH_LIFECYCLE_ONLY",
            "in_game_claimed": True,
            "credentials_retained": False,
            "session_secrets_retained": False,
        }
        result = read_auth_session(
            pid=1,
            start_ticks=2,
            runner=lambda args: json.dumps(payload),
        )
        self.assertEqual("UNAVAILABLE", result["state"])
        self.assertFalse(result["semantic_promotion_allowed"])


if __name__ == "__main__":
    unittest.main()
