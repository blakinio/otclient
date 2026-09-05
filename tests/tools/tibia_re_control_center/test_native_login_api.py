from __future__ import annotations

import tempfile
import unittest

from tools.tibia_re_control_center.control_api import ControlApiServer
from tools.tibia_re_control_center.control_cli import ControlApiClient, ControlClientError
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


class NativeLoginApiTests(unittest.TestCase):
    def test_status_and_start_routes_expose_only_secret_free_lifecycle_contract(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            executor = _SyntheticLoginExecutor()
            domain = ControlDomainService(
                root,
                native_login_lifecycle=NativeLoginLifecycle(executor=executor),
            )
            server = ControlApiServer(root, domain=domain).start()
            client = ControlApiClient(root)
            try:
                self.assertEqual(
                    client.get("/v1/native-login/status"),
                    executor.status(),
                )
                first = client.post(
                    "/v1/native-login/start",
                    {},
                    request_id="native-login-api-start-1",
                )
                replay = client.post(
                    "/v1/native-login/start",
                    {},
                    request_id="native-login-api-start-1",
                )
                self.assertEqual(first, replay)
                self.assertEqual([first["operation_id"]], executor.start_calls)
                self.assertEqual("STARTING", first["state"])
                self.assertFalse(first["physical_effect"])
                self.assertNotIn("password", first)
                self.assertNotIn("username", first)
                self.assertNotIn("email", first)
            finally:
                server.close()

    def test_start_rejects_credential_fields_before_executor_invocation(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            executor = _SyntheticLoginExecutor()
            domain = ControlDomainService(
                root,
                native_login_lifecycle=NativeLoginLifecycle(executor=executor),
            )
            server = ControlApiServer(root, domain=domain).start()
            client = ControlApiClient(root)
            try:
                for index, body in enumerate(
                    (
                        {"password": "not-a-real-secret"},
                        {"username": "not-a-real-user"},
                        {"email": "nobody@example.invalid"},
                        {"credential": "opaque-but-forbidden-here"},
                    )
                ):
                    with self.subTest(body=tuple(body)):
                        with self.assertRaises(ControlClientError) as caught:
                            client.post(
                                "/v1/native-login/start",
                                body,
                                request_id=f"native-login-secret-shape-{index}",
                            )
                        self.assertEqual(400, caught.exception.status)
                        self.assertEqual(
                            "CONTROL_BODY_INVALID",
                            caught.exception.payload["code"],
                        )
                self.assertEqual([], executor.start_calls)
            finally:
                server.close()

    def test_default_unbound_start_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            server = ControlApiServer(root).start()
            client = ControlApiClient(root)
            try:
                self.assertEqual(
                    client.get("/v1/native-login/status"),
                    {
                        "state": "UNBOUND",
                        "bound": False,
                        "current": False,
                        "physical_effect": False,
                        "reason": "NATIVE_LOGIN_RUNTIME_NOT_BOUND",
                    },
                )
                with self.assertRaises(ControlClientError) as caught:
                    client.post(
                        "/v1/native-login/start",
                        {},
                        request_id="native-login-default-unbound",
                    )
                self.assertEqual(409, caught.exception.status)
                self.assertEqual("NATIVE_LOGIN_UNBOUND", caught.exception.payload["code"])
            finally:
                server.close()


if __name__ == "__main__":
    unittest.main()
