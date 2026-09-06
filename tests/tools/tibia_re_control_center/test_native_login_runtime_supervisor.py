from __future__ import annotations

import json
import os
from pathlib import Path
import socket
import tempfile
import threading
import time
import unittest


_CURRENT = {
    "version": "15.32.be4f48",
    "size": 52105824,
    "sha256": "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1",
}


class _FakeRunner:
    def __init__(self) -> None:
        self.calls: list[str] = []
        self.entered = threading.Event()
        self.release = threading.Event()

    def __call__(self, operation_id: str, permit: object, cancelled: threading.Event) -> str:
        self.calls.append(operation_id)
        self.entered.set()
        while not self.release.wait(0.01):
            if cancelled.is_set():
                return "STOPPED"
        return "IN_GAME"


def _write_permit(path: Path, *, expires_at: int | None = None) -> None:
    payload = {
        "schema": "otclient.track-a.native-login-permit.v1",
        "authorization": "ONE_SHOT_NATIVE_LOGIN",
        "expires_at_epoch": expires_at or int(time.time()) + 300,
        "boot_id_sha256": "a" * 64,
        "pid": 4242,
        "process_start_ticks": 123456,
        "client_version": _CURRENT["version"],
        "client_size": _CURRENT["size"],
        "client_sha256": _CURRENT["sha256"],
    }
    path.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    os.chmod(path, 0o600)


class NativeLoginRuntimeSupervisorTests(unittest.TestCase):
    def test_permit_is_exact_current_bounded_and_consumed_once(self) -> None:
        from tools.tibia_re_control_center.native_login_runtime_supervisor import NativeLoginPermitStore

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            permit_path = root / "permit.json"
            _write_permit(permit_path)
            store = NativeLoginPermitStore(permit_path)
            permit = store.consume("op-1")
            self.assertEqual(permit.client_version, _CURRENT["version"])
            self.assertEqual(permit.client_size, _CURRENT["size"])
            self.assertEqual(permit.client_sha256, _CURRENT["sha256"])
            self.assertFalse(permit_path.exists())
            with self.assertRaisesRegex(RuntimeError, "AUTHORIZATION_REQUIRED"):
                store.consume("op-2")

    def test_missing_or_expired_permit_refuses_before_physical_effect(self) -> None:
        from tools.tibia_re_control_center.native_login_runtime_supervisor import NativeLoginPermitStore

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            store = NativeLoginPermitStore(root / "missing.json")
            with self.assertRaisesRegex(RuntimeError, "AUTHORIZATION_REQUIRED"):
                store.consume("op-1")
            expired = root / "expired.json"
            _write_permit(expired, expires_at=int(time.time()) - 1)
            with self.assertRaisesRegex(RuntimeError, "AUTHORIZATION_EXPIRED"):
                NativeLoginPermitStore(expired).consume("op-2")

    def test_supervisor_start_without_permit_is_safe_and_secret_free(self) -> None:
        from tools.tibia_re_control_center.native_login_runtime_supervisor import NativeLoginRuntimeSupervisor

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            runner = _FakeRunner()
            supervisor = NativeLoginRuntimeSupervisor(
                socket_path=root / "runtime.sock",
                permit_store_path=root / "missing-permit.json",
                login_runner=runner,
            )
            reply = supervisor.handle({"version": 1, "command": "START", "operation_id": "op-1"})
            self.assertEqual(reply["state"], "BLOCKED")
            self.assertEqual(reply["reason"], "NATIVE_LOGIN_AUTHORIZATION_REQUIRED")
            self.assertFalse(reply["physical_effect"])
            self.assertEqual(runner.calls, [])
            self.assertNotIn("password", json.dumps(reply).lower())
            self.assertNotIn("email", json.dumps(reply).lower())

    def test_one_start_reaches_in_game_and_second_operation_is_refused(self) -> None:
        from tools.tibia_re_control_center.native_login_runtime_supervisor import NativeLoginRuntimeSupervisor

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _write_permit(root / "permit.json")
            runner = _FakeRunner()
            supervisor = NativeLoginRuntimeSupervisor(
                socket_path=root / "runtime.sock",
                permit_store_path=root / "permit.json",
                login_runner=runner,
            )
            first = supervisor.handle({"version": 1, "command": "START", "operation_id": "op-1"})
            self.assertEqual(first["state"], "STARTING")
            self.assertTrue(runner.entered.wait(1))
            second = supervisor.handle({"version": 1, "command": "START", "operation_id": "op-2"})
            self.assertEqual(second["state"], "STARTING")
            self.assertEqual(second["reason"], "NATIVE_LOGIN_SESSION_ALREADY_ACTIVE")
            self.assertEqual(runner.calls, ["op-1"])
            runner.release.set()
            for _ in range(100):
                status = supervisor.handle({"version": 1, "command": "STATUS"})
                if status["state"] == "IN_GAME":
                    break
                time.sleep(0.01)
            self.assertEqual(status["state"], "IN_GAME")
            self.assertEqual(status["reason"], "NATIVE_LOGIN_IN_GAME")

    def test_stop_only_cancels_current_operation_and_never_kills_runtime(self) -> None:
        from tools.tibia_re_control_center.native_login_runtime_supervisor import NativeLoginRuntimeSupervisor

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _write_permit(root / "permit.json")
            runner = _FakeRunner()
            supervisor = NativeLoginRuntimeSupervisor(
                socket_path=root / "runtime.sock",
                permit_store_path=root / "permit.json",
                login_runner=runner,
            )
            supervisor.handle({"version": 1, "command": "START", "operation_id": "op-1"})
            self.assertTrue(runner.entered.wait(1))
            stop = supervisor.handle({"version": 1, "command": "STOP", "operation_id": "op-1"})
            self.assertEqual(stop["state"], "STOPPING")
            self.assertEqual(stop["reason"], "NATIVE_LOGIN_STOP_REQUESTED")
            self.assertFalse(stop["physical_effect"])
            for _ in range(100):
                status = supervisor.handle({"version": 1, "command": "STATUS"})
                if status["state"] == "STOPPED":
                    break
                time.sleep(0.01)
            self.assertEqual(status["state"], "STOPPED")
            self.assertEqual(runner.calls, ["op-1"])

    def test_unix_server_accepts_only_exact_closed_protocol(self) -> None:
        from tools.tibia_re_control_center.native_login_runtime_supervisor import NativeLoginRuntimeSupervisor

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            supervisor = NativeLoginRuntimeSupervisor(
                socket_path=root / "runtime.sock",
                permit_store_path=root / "permit.json",
                login_runner=_FakeRunner(),
            )
            thread = threading.Thread(target=supervisor.serve_forever, daemon=True)
            thread.start()
            for _ in range(100):
                if (root / "runtime.sock").exists():
                    break
                time.sleep(0.01)
            client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                client.connect(str(root / "runtime.sock"))
                client.sendall(b'{"version":1,"command":"STATUS","password":"forbidden"}\n')
                raw_reply = b""
                while b"\n" not in raw_reply:
                    raw_reply += client.recv(4096)
            finally:
                client.close()
                supervisor.close()
                thread.join(2)
            reply = json.loads(raw_reply.split(b"\n", 1)[0])
            self.assertEqual(reply["state"], "ERROR")
            self.assertEqual(reply["reason"], "NATIVE_LOGIN_PROTOCOL_INVALID")
            self.assertFalse(reply["physical_effect"])


if __name__ == "__main__":
    unittest.main()
