from __future__ import annotations

import tempfile
import unittest

from tools.tibia_re_control_center.control_domain import ControlDomainService
from tools.tibia_re_control_center.native_login_lifecycle import NativeLoginLifecycle


class _SyntheticLoginExecutor:
    def __init__(self) -> None:
        self.start_calls: list[str] = []
        self.stop_calls: list[str] = []
        self.stop_latch_observations: list[bool] = []
        self.stop_latched_probe = lambda: False

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

    def stop(self, operation_id: str) -> dict[str, object]:
        self.stop_calls.append(operation_id)
        self.stop_latch_observations.append(self.stop_latched_probe())
        return {
            "state": "STOPPED",
            "bound": True,
            "current": True,
            "physical_effect": False,
            "reason": "NATIVE_LOGIN_STOP_CONFIRMED",
            "operation_id": operation_id,
        }


class NativeLoginControlTests(unittest.TestCase):
    @staticmethod
    def _post(domain: ControlDomainService, *, path: str, operation: str, request_id: str, handler):
        return domain.process_post(
            canonical_path=path,
            operation=operation,
            request_id=request_id,
            body={},
            handler=handler,
        )

    def test_native_login_start_uses_durable_resource_identity_and_replays_once(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            executor = _SyntheticLoginExecutor()
            lifecycle = NativeLoginLifecycle(executor=executor)
            domain = ControlDomainService(root, native_login_lifecycle=lifecycle)
            try:
                def invoke():
                    return self._post(
                        domain,
                        path="/v1/native-login/start",
                        operation="NATIVE_LOGIN_START",
                        request_id="native-login-request-1",
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

    def test_stop_is_durable_before_native_cancel_and_replay_does_not_cancel_twice(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            executor = _SyntheticLoginExecutor()
            domain = ControlDomainService(
                root,
                native_login_lifecycle=NativeLoginLifecycle(executor=executor),
            )
            executor.stop_latched_probe = lambda: domain.coordinator.control_state.stop_latched
            try:
                started = self._post(
                    domain,
                    path="/v1/native-login/start",
                    operation="NATIVE_LOGIN_START",
                    request_id="native-login-before-stop",
                    handler=domain.native_login_start,
                )
                self.assertEqual(202, started.code)

                def invoke_stop():
                    return self._post(
                        domain,
                        path="/v1/stop-all",
                        operation="STOP_ALL",
                        request_id="native-login-stop-1",
                        handler=domain.stop_all,
                    )

                first = invoke_stop()
                replay = invoke_stop()
                self.assertEqual(200, first.code)
                self.assertEqual(first.body, replay.body)
                self.assertTrue(first.body["stop_latched"])
                self.assertEqual([first.body["resource_id"]], executor.stop_calls)
                self.assertEqual([True], executor.stop_latch_observations)
            finally:
                domain.close()

    def test_native_login_start_after_stop_fails_before_executor(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            executor = _SyntheticLoginExecutor()
            domain = ControlDomainService(
                root,
                native_login_lifecycle=NativeLoginLifecycle(executor=executor),
            )
            try:
                stopped = self._post(
                    domain,
                    path="/v1/stop-all",
                    operation="STOP_ALL",
                    request_id="stop-before-native-login",
                    handler=domain.stop_all,
                )
                self.assertEqual(200, stopped.code)
                self.assertTrue(domain.coordinator.control_state.stop_latched)

                rejected = self._post(
                    domain,
                    path="/v1/native-login/start",
                    operation="NATIVE_LOGIN_START",
                    request_id="native-login-after-stop",
                    handler=domain.native_login_start,
                )
                self.assertEqual(409, rejected.code)
                self.assertEqual("NATIVE_LOGIN_STOP_LATCHED", rejected.body["code"])
                self.assertEqual([], executor.start_calls)
            finally:
                domain.close()


if __name__ == "__main__":
    unittest.main()
