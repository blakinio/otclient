from __future__ import annotations

import importlib.util
import unittest


class _SyntheticExecutor:
    def status(self) -> dict[str, object]:
        return {
            "state": "READY",
            "bound": True,
            "current": True,
            "physical_effect": False,
            "reason": "NATIVE_LOGIN_RUNTIME_READY",
        }


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

    def test_03_start_fails_closed_when_runtime_is_unbound(self) -> None:
        from tools.tibia_re_control_center.native_login_lifecycle import (
            NativeLoginLifecycle,
            NativeLoginLifecycleError,
        )

        lifecycle = NativeLoginLifecycle()
        with self.assertRaises(NativeLoginLifecycleError) as caught:
            lifecycle.start()
        self.assertEqual(caught.exception.code, "NATIVE_LOGIN_UNBOUND")
        self.assertEqual(
            caught.exception.safe_message,
            "native login runtime is not bound",
        )
        self.assertFalse(caught.exception.physical_effect)
        self.assertFalse(lifecycle.status()["physical_effect"])

    def test_04_bound_lifecycle_projects_executor_status(self) -> None:
        from tools.tibia_re_control_center.native_login_lifecycle import NativeLoginLifecycle

        lifecycle = NativeLoginLifecycle(executor=_SyntheticExecutor())
        self.assertEqual(
            lifecycle.status(),
            {
                "state": "READY",
                "bound": True,
                "current": True,
                "physical_effect": False,
                "reason": "NATIVE_LOGIN_RUNTIME_READY",
            },
        )


if __name__ == "__main__":
    unittest.main()
