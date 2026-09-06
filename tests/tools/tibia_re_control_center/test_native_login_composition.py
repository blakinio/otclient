from __future__ import annotations

import json
import os
from pathlib import Path
import socket
import tempfile
import threading
import unittest


class _StatusServer:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._ready = threading.Event()
        self._thread = threading.Thread(target=self._serve, daemon=True)

    def start(self) -> "_StatusServer":
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
            server.listen(1)
            self._ready.set()
            client, _ = server.accept()
            with client:
                raw = b""
                while b"\n" not in raw:
                    raw += client.recv(4096)
                request = json.loads(raw.split(b"\n", 1)[0])
                if request != {"version": 1, "command": "STATUS"}:
                    raise AssertionError(request)
                response = {
                    "version": 1,
                    "state": "READY",
                    "bound": True,
                    "current": True,
                    "physical_effect": False,
                    "reason": "NATIVE_LOGIN_RUNTIME_READY",
                }
                client.sendall(json.dumps(response, separators=(",", ":")).encode() + b"\n")
        finally:
            server.close()
            try:
                self.path.unlink()
            except FileNotFoundError:
                pass


class NativeLoginCompositionTests(unittest.TestCase):
    def test_control_api_composes_native_login_socket_only_from_environment(self) -> None:
        from tools.tibia_re_control_center.control_api import ControlApiServer

        with tempfile.TemporaryDirectory() as root:
            socket_path = Path(root) / "native-login.sock"
            status_server = _StatusServer(socket_path).start()
            old = os.environ.get("OTCLIENT_TIBIA_RE_NATIVE_LOGIN_SOCKET")
            os.environ["OTCLIENT_TIBIA_RE_NATIVE_LOGIN_SOCKET"] = str(socket_path)
            server = ControlApiServer(Path(root) / "control")
            try:
                status = server.domain.native_login_lifecycle.status()
                self.assertEqual(status["state"], "READY")
                self.assertTrue(status["bound"])
            finally:
                server.close()
                status_server.join()
                if old is None:
                    os.environ.pop("OTCLIENT_TIBIA_RE_NATIVE_LOGIN_SOCKET", None)
                else:
                    os.environ["OTCLIENT_TIBIA_RE_NATIVE_LOGIN_SOCKET"] = old

    def test_control_api_without_environment_remains_unbound(self) -> None:
        from tools.tibia_re_control_center.control_api import ControlApiServer

        with tempfile.TemporaryDirectory() as root:
            old = os.environ.pop("OTCLIENT_TIBIA_RE_NATIVE_LOGIN_SOCKET", None)
            server = ControlApiServer(Path(root) / "control")
            try:
                status = server.domain.native_login_lifecycle.status()
                self.assertEqual(status["state"], "UNBOUND")
                self.assertFalse(status["bound"])
            finally:
                server.close()
                if old is not None:
                    os.environ["OTCLIENT_TIBIA_RE_NATIVE_LOGIN_SOCKET"] = old


if __name__ == "__main__":
    unittest.main()
