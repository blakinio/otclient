from __future__ import annotations

import tempfile
import unittest

from tools.tibia_re_control_center.control_domain import ControlDomainService
from tools.tibia_re_control_center.native_login_lifecycle import NativeLoginLifecycle


class _SyntheticLoginExecutor:
    def __init__(self) -> None:
        self.start_calls: list[str] = []

    def status(self) -> dict[str, object]:
        return {
            "state": "READY",
            "bound": True,
            "current": True,
            "physical_effect": False,
            "reason": "NATIVE_LOGIN_RUNTIME_READY",
        }

    def start(self, operation_id: str) -> dict[str, object]:
        self.start_calls.append(operation_id)
        return {
            "state": "STARTING",
            "bound": True,
            "current": True,
            "physical_effect": False,
            "reason": "NATIVE_LOGIN_START_ACCEPTED",
            "operation_id": operation_id,
        }


class NativeLoginControlTests(unittest.TestCase):
    def test_native_login_start_uses_durable_resource_identity_and_replays_once(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            executor = _SyntheticLoginExecutor()
            lifecycle = NativeLoginLifecycle(executor=executor)
            domain = ControlDomainService(root, native_login_lifecycle=lifecycle)
            try:
                def invoke():
                    return domain.process_post(
                        canonical_path="/v1/native-login/start",
                        operation="NATIVE_LOGIN_START",
                        request_id="native-login-request-1",
                        body={},
                        handler=domain.native_login_start,
                    )

                first = invoke()
                second = invoke()
                self.assertEqual(202, first.code)
                self.assertEqual(first.body, second.body)
                operation_id = first.body["operation_id"]
                self.assertTrue(operation_id.startswith("native-login-"))
                self.assertEqual(executor.start_calls, [operation_id])
                self.assertEqual("STARTING", first.body["state"])
                self.assertFalse(first.body["physical_effect"])
            finally:
                domain.close()


if __name__ == "__main__":
    unittest.main()
