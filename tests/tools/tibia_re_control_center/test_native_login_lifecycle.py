from __future__ import annotations

import importlib.util
import unittest


class NativeLoginLifecycleTests(unittest.TestCase):
    def test_01_native_login_lifecycle_module_exists(self) -> None:
        spec = importlib.util.find_spec(
            "tools.tibia_re_control_center.native_login_lifecycle"
        )
        self.assertIsNotNone(spec, "Control Center native login lifecycle seam is missing")

    def test_02_default_lifecycle_is_unbound_and_authority_free(self) -> None:
        from tools.tibia_re_control_center.native_login_lifecycle import NativeLoginLifecycle

        lifecycle = NativeLoginLifecycle()
        self.assertEqual(
            lifecycle.status(),
            {
                "state": "UNBOUND",
                "bound": False,
                "current": False,
                "physical_effect": False,
                "reason": "NATIVE_LOGIN_RUNTIME_NOT_BOUND",
            },
        )


if __name__ == "__main__":
    unittest.main()
