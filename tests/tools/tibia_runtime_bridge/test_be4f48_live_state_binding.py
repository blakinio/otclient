from __future__ import annotations

import json
from pathlib import Path
import unittest

from tools.tibia_runtime_bridge.launcher import load_profile


ROOT = Path(__file__).resolve().parents[3]
EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52_105_824
EXPECTED_SHA = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"


class Be4f48LiveStateBindingTests(unittest.TestCase):
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

    def test_live_reader_derives_exact_current_binding_instead_of_trusting_stale_constants(self) -> None:
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
        if not profile_path.is_file():
            self.skipTest("profile intentionally absent in RED phase")
        raw = profile_path.read_text(encoding="utf-8")
        doc = json.loads(raw)
        self.assertNotIn("password", raw.lower())
        self.assertNotIn("email", raw.lower())
        self.assertNotIn("credential", raw.lower())
        self.assertEqual("otclient.tibia-runtime-bridge.profile.v1", doc["schema"])


if __name__ == "__main__":
    unittest.main()
