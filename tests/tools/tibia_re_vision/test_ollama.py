import unittest

from tools.tibia_re_vision.ollama import admit_residency


class ResidencyAdmissionTests(unittest.TestCase):
    def test_foreign_residency_fails_closed(self):
        self.assertEqual(admit_residency(["other-model"], "qwen-model")[0], False)

    def test_multiple_residency_fails_closed(self):
        self.assertEqual(admit_residency(["qwen-model", "other-model"], "qwen-model")[0], False)

    def test_unknown_residency_fails_closed(self):
        self.assertEqual(admit_residency(None, "qwen-model"), (False, "RESIDENCY_UNKNOWN"))
