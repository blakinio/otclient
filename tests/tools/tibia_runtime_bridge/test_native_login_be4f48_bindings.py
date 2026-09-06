from __future__ import annotations

import json
import re
from pathlib import Path
import unittest

from tools.tibia_runtime_bridge.launcher import load_profile


ROOT = Path(__file__).resolve().parents[3]
EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SHA = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"
EXPECTED_SIZE = 52_105_824


class NativeLoginBe4f48BindingTests(unittest.TestCase):
    def test_python_gate_is_pinned_to_exact_be4f48_contract(self) -> None:
        source = (ROOT / "tools/tibia_runtime_bridge/current_sha_native_login_gate.py").read_text(encoding="utf-8")
        required = (
            f'EXPECTED_SHA256 = "{EXPECTED_SHA}"',
            "EXPECTED_SIZE = 52_105_824",
            '"game_client": (\n        "N5tibia6client11TGameClientE",\n        0x30ACD08,',
            '"character_controller": (\n        "N5tibia10gamewindow29TCharacterSelectionControllerE",\n        0x30C29A8,',
            '"player_protocol_handler": (\n        "N5tibia4game29TPlayerProtocolMessageHandlerE",\n        0x30BE640,',
            '"gameserver_game_session": (\n        "N5tibia4game22TGameserverGameSessionE",\n        0x30AEFA0,',
            '"worldmap_handler": (\n        "N5tibia8worldmap31TWorldmapProtocolMessageHandlerE",\n        0x30BF1F0,',
            "game_base = 0x1CB3CF4",
            "game_data = 0x1CB3740",
            "0x1D8F2C4,\n        17,\n        0xD18D70,",
            '"488b5110488b71084883c4485b5de94d679cff0f1f440000488bbfa009000048"',
            "char_base = 0x1CC3C14",
            "char_data = 0x1CC37C0",
            "0x1D97EE4,\n        0,\n        0xD516C0,",
            "0x1D97EE4,\n        11,\n        0xD51690,",
            "auth_base = 0x1CAB760",
            "auth_data = 0x1CAB140",
            "0x1D8EE20,\n        5,\n        0xD0F3A7,",
            "0x1D8EE20,\n        27,\n        0xD0F1E2,",
        )
        for fragment in required:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, source)

    def test_experimental_auth_helper_matches_exact_be4f48_auth_binding(self) -> None:
        source = (ROOT / "tools/tibia_runtime_bridge/experimental_auth.cpp").read_text(encoding="utf-8")
        self.assertIn(f'constexpr char kClientSha256[] = "{EXPECTED_SHA}";', source)
        self.assertIn(f"constexpr std::uint64_t kClientSize = {EXPECTED_SIZE};", source)
        self.assertIn("constexpr std::uintptr_t kGameClientVptrOffset = 0x30acd08;", source)
        self.assertIn("constexpr std::uintptr_t kColdAuthTargetOffset = 0xd18d70;", source)
        fence = re.search(r"constexpr std::array<unsigned char, 32> kColdAuthFence = \{(?P<body>.*?)\};", source, re.S)
        self.assertIsNotNone(fence)
        bytes_hex = "".join(f"{int(value, 16):02x}" for value in re.findall(r"0x([0-9a-fA-F]{2})", fence.group("body")))
        self.assertEqual("488b5110488b71084883c4485b5de94d679cff0f1f440000488bbfa009000048", bytes_hex)

    def test_character_helper_matches_exact_be4f48_character_binding(self) -> None:
        source = (ROOT / "tools/tibia_runtime_bridge/experimental_character_control_current.cpp").read_text(encoding="utf-8")
        self.assertIn(f'constexpr char kClientSha256[] = "{EXPECTED_SHA}";', source)
        self.assertIn(f"constexpr std::uint64_t kClientSize = {EXPECTED_SIZE};", source)
        self.assertIn("constexpr std::uintptr_t kCharacterControllerVptrOffset = 0x30c29a8;", source)

    def test_rebind_includes_exact_current_game_window_state_contract(self) -> None:
        analyzer = ROOT / "tools/tibia_runtime_bridge/game_window_state_rebind.py"
        self.assertTrue(analyzer.is_file(), "be4f48 game-window-state analyzer missing")
        source = analyzer.read_text(encoding="utf-8")
        self.assertIn(f'EXPECTED_SHA256 = "{EXPECTED_SHA}"', source)
        self.assertIn("EXPECTED_SIZE = 52_105_824", source)
        self.assertIn('GAME_WINDOW_CLASS = "tibia::gamewindow::TGameWindowController"', source)
        self.assertIn('GAME_WINDOW_STATE_PROPERTY = "gameWindowState"', source)
        self.assertIn('INGAME_TEXT = "INGAME"', source)
        self.assertNotIn("d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a", source)
        wrapper = (ROOT / "tools/tibia_runtime_bridge/rebind_native_login_current.py").read_text(encoding="utf-8")
        self.assertIn("augment_rebind_output", wrapper)

    def test_exact_current_bridge_profile_uses_proven_rtti_targets(self) -> None:
        profile_path = ROOT / "tools/tibia_runtime_bridge/profiles/tibia-15.32.be4f48.json"
        self.assertTrue(profile_path.is_file(), "exact-current be4f48 bridge profile is missing")
        profile = load_profile(profile_path)
        self.assertEqual(EXPECTED_VERSION, profile["client_version"])
        self.assertEqual(EXPECTED_SHA, profile["binary_sha256"])
        expected = {
            "game_client": ("0x30acd08", "tibia::client::TGameClient"),
            "character_controller": ("0x30c29a8", "tibia::gamewindow::TCharacterSelectionController"),
            "player_protocol_handler": ("0x30be640", "tibia::game::TPlayerProtocolMessageHandler"),
            "gameserver_game_session": ("0x30aefa0", "tibia::game::TGameserverGameSession"),
            "worldmap_handler": ("0x30bf1f0", "tibia::worldmap::TWorldmapProtocolMessageHandler"),
        }
        self.assertEqual(set(expected), set(profile["targets"]))
        for name, (offset, qt_class) in expected.items():
            target = profile["targets"][name]
            self.assertEqual("primary_vptr", target["resolver"])
            self.assertEqual(offset, target["vptr_offset"])
            self.assertEqual(qt_class, target["expected_qt_class"])

    def test_live_reader_derives_exact_current_binding(self) -> None:
        reader = (ROOT / ".github/scripts/track_a_game_window_state_qualification.py").read_text(encoding="utf-8")
        self.assertIn("from tools.tibia_re_control_center.current_client_fence import current_client_fence", reader)
        self.assertIn("from tools.tibia_runtime_bridge.game_window_state_rebind import analyze_game_window_state", reader)
        self.assertIn("binding = analyze_game_window_state(exe)", reader)
        self.assertIn('binding["read_property"]["backing_member"]', reader)
        self.assertIn('binding["rtti"]["vptr_offset"]', reader)
        self.assertIn("member_offset=member_offset", reader)
        self.assertNotIn('CURRENT_VERSION = "15.32.75d4a0"', reader)
        self.assertNotIn("GAME_WINDOW_STATE_MEMBER_OFFSET = 0x60", reader)
        self.assertNotIn("anchor.EXPECTED_SHA256", reader)
        self.assertNotIn("anchor.EXPECTED_SIZE", reader)

    def test_profile_is_secret_free_static_metadata(self) -> None:
        profile_path = ROOT / "tools/tibia_runtime_bridge/profiles/tibia-15.32.be4f48.json"
        self.assertTrue(profile_path.is_file(), "exact-current be4f48 bridge profile is missing")
        raw = profile_path.read_text(encoding="utf-8")
        doc = json.loads(raw)
        self.assertNotIn("password", raw.lower())
        self.assertNotIn("email", raw.lower())
        self.assertNotIn("credential", raw.lower())
        self.assertEqual("otclient.tibia-runtime-bridge.profile.v1", doc["schema"])


if __name__ == "__main__":
    unittest.main()
