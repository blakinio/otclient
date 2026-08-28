from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

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


if __name__ == "__main__":
    unittest.main()
