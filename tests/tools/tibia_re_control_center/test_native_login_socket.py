from __future__ import annotations

import json
import os
from pathlib import Path
import socket
import tempfile
import threading
import unittest


class _OneShotUnixServer:
    def __init__(self, path: Path, responses: list[dict[str, object]]) -> None:
        self.path = path
        self.responses = list(responses)
        self.requests: list[dict[str, object]] = []
        self._ready = threading.Event()
        self._thread = threading.Thread(target=self._serve, daemon=True)

    def start(self) -> "_OneShotUnixServer":
        self._thread.start()
        self._ready.wait(2)
        return self

    def join(self) -> None:
        self._thread.join(2)

    def _serve(self) -> None:
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            server.bind(str(self.path))
            os.chmod(self.path, 0o600)
            server.listen(len(self.responses) or 1)
            self._ready.set()
            for response in self.responses:
                client, _ = server.accept()
                with client:
                    raw = b""
                    while b"\n" not in raw:
                        chunk = client.recv(4096)
                        if not chunk:
                            break
                        raw += chunk
                    self.requests.append(json.loads(raw.split(b"\n", 1)[0]))
                    client.sendall(json.dumps(response, separators=(",", ":")).encode() + b"\n")
        finally:
            server.close()
            try:
                self.path.unlink()
            except FileNotFoundError:
                pass


class NativeLoginSocketExecutorTests(unittest.TestCase):
    def test_environment_without_socket_keeps_default_unbound(self) -> None:
        from tools.tibia_re_control_center.native_login_socket import lifecycle_from_environment

        old = os.environ.pop("OTCLIENT_TIBIA_RE_NATIVE_LOGIN_SOCKET", None)
        try:
            lifecycle = lifecycle_from_environment()
            self.assertEqual(lifecycle.status()["state"], "UNBOUND")
            self.assertFalse(lifecycle.status()["bound"])
        finally:
            if old is not None:
                os.environ["OTCLIENT_TIBIA_RE_NATIVE_LOGIN_SOCKET"] = old

    def test_status_start_and_stop_use_exact_secret_free_protocol(self) -> None:
        from tools.tibia_re_control_center.native_login_socket import NativeLoginSocketExecutor

        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "native-login.sock"
            responses = [
                {"version": 1, "state": "READY", "bound": True, "current": True, "physical_effect": False, "reason": "NATIVE_LOGIN_RUNTIME_READY"},
                {"version": 1, "state": "STARTING", "bound": True, "current": True, "physical_effect": False, "reason": "NATIVE_LOGIN_START_ACCEPTED", "operation_id": "native-login-1"},
                {"version": 1, "state": "STOPPED", "bound": True, "current": True, "physical_effect": False, "reason": "NATIVE_LOGIN_STOPPED", "operation_id": "native-login-stop-1"},
            ]
            server = _OneShotUnixServer(path, responses).start()
            executor = NativeLoginSocketExecutor(path)
            self.assertEqual(executor.status()["state"], "READY")
            self.assertEqual(executor.start("native-login-1")["state"], "STARTING")
            self.assertEqual(executor.stop("native-login-stop-1")["state"], "STOPPED")
            server.join()
            self.assertEqual(server.requests, [
                {"version": 1, "command": "STATUS"},
                {"version": 1, "command": "START", "operation_id": "native-login-1"},
                {"version": 1, "command": "STOP", "operation_id": "native-login-stop-1"},
            ])
            self.assertNotIn("password", json.dumps(server.requests).lower())
            self.assertNotIn("credential", json.dumps(server.requests).lower())

    def test_missing_socket_fails_closed_before_effect(self) -> None:
        from tools.tibia_re_control_center.native_login_lifecycle import NativeLoginLifecycleError
        from tools.tibia_re_control_center.native_login_socket import NativeLoginSocketExecutor

        with tempfile.TemporaryDirectory() as root:
            executor = NativeLoginSocketExecutor(Path(root) / "missing.sock")
            with self.assertRaises(NativeLoginLifecycleError) as caught:
                executor.start("native-login-2")
            self.assertEqual(caught.exception.code, "NATIVE_LOGIN_RUNTIME_UNAVAILABLE")
            self.assertFalse(caught.exception.physical_effect)

    def test_response_unknown_or_secret_field_is_rejected(self) -> None:
        from tools.tibia_re_control_center.native_login_lifecycle import NativeLoginLifecycleError
        from tools.tibia_re_control_center.native_login_socket import NativeLoginSocketExecutor

        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "native-login.sock"
            server = _OneShotUnixServer(path, [{
                "version": 1,
                "state": "READY",
                "bound": True,
                "current": True,
                "physical_effect": False,
                "reason": "NATIVE_LOGIN_RUNTIME_READY",
                "password": "forbidden",
            }]).start()
            with self.assertRaises(NativeLoginLifecycleError) as caught:
                NativeLoginSocketExecutor(path).status()
            server.join()
            self.assertEqual(caught.exception.code, "NATIVE_LOGIN_RUNTIME_PROTOCOL_INVALID")
            self.assertFalse(caught.exception.physical_effect)

    def test_operation_identity_mismatch_is_rejected_conservatively(self) -> None:
        from tools.tibia_re_control_center.native_login_lifecycle import NativeLoginLifecycleError
        from tools.tibia_re_control_center.native_login_socket import NativeLoginSocketExecutor

        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "native-login.sock"
            server = _OneShotUnixServer(path, [{
                "version": 1,
                "state": "STARTING",
                "bound": True,
                "current": True,
                "physical_effect": True,
                "reason": "NATIVE_LOGIN_START_ACCEPTED",
                "operation_id": "other-operation",
            }]).start()
            with self.assertRaises(NativeLoginLifecycleError) as caught:
                NativeLoginSocketExecutor(path).start("native-login-3")
            server.join()
            self.assertEqual(caught.exception.code, "NATIVE_LOGIN_OPERATION_ID_MISMATCH")
            self.assertTrue(caught.exception.physical_effect)


if __name__ == "__main__":
    unittest.main()
