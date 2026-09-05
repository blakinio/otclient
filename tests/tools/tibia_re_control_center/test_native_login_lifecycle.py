from __future__ import annotations

import importlib.util
import unittest


class NativeLoginLifecycleTests(unittest.TestCase):
    def test_01_native_login_lifecycle_module_exists(self) -> None:
        spec = importlib.util.find_spec(
            "tools.tibia_re_control_center.native_login_lifecycle"
        )
        self.assertIsNotNone(spec, "Control Center native login lifecycle seam is missing")


if __name__ == "__main__":
    unittest.main()
