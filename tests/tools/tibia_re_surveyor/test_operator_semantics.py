from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]


class OperatorSemanticRegressionTests(unittest.TestCase):
    def test_surveyor_bridge_presence_cannot_claim_ingame_or_no_login(self):
        text = (ROOT / ".github/workflows/track-a-surveyor-v2-readonly.yml").read_text(encoding="utf-8")
        self.assertIn("UNKNOWN:BRIDGE_3_OF_3_SEMANTICS_UNPROVEN", text)
        self.assertNotIn("PASS:BRIDGE_3_OF_3", text)
        self.assertNotIn("state=PASS; login=NO", text)
        self.assertIn("state=UNKNOWN", text)
        self.assertIn("login=UNKNOWN", text)

    def test_native_login_bridge_presence_cannot_claim_gameplay_success(self):
        text = (ROOT / ".github/workflows/track-a-native-login.yml").read_text(encoding="utf-8")
        self.assertIn("BRIDGE_3_OF_3=YES", text)
        self.assertIn("RESULT=INCONCLUSIVE", text)
        self.assertIn("CHARACTER_ACTUALLY_LOGGED_INTO_GAME=UNKNOWN", text)
        self.assertIn("STRUCTURAL_IN_GAME=UNKNOWN", text)
        self.assertNotIn("CHARACTER_ACTUALLY_LOGGED_INTO_GAME=YES", text)
        self.assertNotIn("STRUCTURAL_IN_GAME=PASS", text)


if __name__ == "__main__":
    unittest.main()
