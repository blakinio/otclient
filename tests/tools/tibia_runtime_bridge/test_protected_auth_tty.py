from __future__ import annotations

import json
import os
from pathlib import Path
import pty
import select
import struct
import tempfile
import termios
import threading
import unittest
from unittest import mock

try:
    import fcntl
except ImportError:  # pragma: no cover - Linux-only test
    fcntl = None

from tools.tibia_runtime_bridge.ipc_client import BridgeClientError
from tools.tibia_runtime_bridge.protected_auth_tty import (
    EXACT_CLIENT_SHA256,
    EXACT_CLIENT_SIZE,
    EXACT_CLIENT_VERSION,
    ProtectedSecretBuffer,
    _reject_legacy_secret_environment,
    create_sealed_credential_memfd,
    load_exact_runtime_identity,
    read_hidden_tty_line,
    sanitize_auth_response,
)


@unittest.skipUnless(os.name == "posix", "Linux/POSIX TTY behavior required")
class ProtectedAuthTtyTests(unittest.TestCase):
    def valid_identity(self) -> dict[str, object]:
        return {
            "boot_id_sha256": "a" * 64,
            "pid": 123,
            "process_start_ticks": 456,
            "client_version": EXACT_CLIENT_VERSION,
            "client_size": EXACT_CLIENT_SIZE,
            "client_sha256": EXACT_CLIENT_SHA256,
        }

    def test_exact_runtime_identity_accepts_only_exact_client_fence(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "identity.json"
            path.write_text(json.dumps(self.valid_identity()), encoding="utf-8")
            path.chmod(0o600)
            identity = load_exact_runtime_identity(path.resolve())
            self.assertEqual(EXACT_CLIENT_VERSION, identity.client_version)
            self.assertEqual(EXACT_CLIENT_SIZE, identity.client_size)
            self.assertEqual(EXACT_CLIENT_SHA256, identity.client_sha256)
            self.assertEqual(123, identity.pid)
            self.assertEqual(456, identity.process_start_ticks)

            doc = self.valid_identity()
            doc["client_sha256"] = "b" * 64
            path.write_text(json.dumps(doc), encoding="utf-8")
            path.chmod(0o600)
            with self.assertRaises(BridgeClientError):
                load_exact_runtime_identity(path.resolve())

    def test_runtime_identity_rejects_relative_and_writable_metadata(self):
        with self.assertRaises(BridgeClientError):
            load_exact_runtime_identity(Path("identity.json"))
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "identity.json"
            path.write_text(json.dumps(self.valid_identity()), encoding="utf-8")
            path.chmod(0o622)
            with self.assertRaises(BridgeClientError):
                load_exact_runtime_identity(path.resolve())

    def test_legacy_secret_environment_fails_closed_without_reading_values(self):
        with mock.patch.dict(os.environ, {"TIBIA_TEST_EMAIL": "synthetic-do-not-read"}, clear=False):
            with self.assertRaises(BridgeClientError):
                _reject_legacy_secret_environment()
        with mock.patch.dict(os.environ, {"TIBIA_TEST_PASSWORD": "synthetic-do-not-read"}, clear=False):
            with self.assertRaises(BridgeClientError):
                _reject_legacy_secret_environment()

    def test_hidden_tty_capture_does_not_echo_and_restores_terminal(self):
        master_fd, slave_fd = pty.openpty()
        before = termios.tcgetattr(slave_fd)
        secret = b"synthetic-secret-value"
        captured = bytearray()
        error: list[BaseException] = []
        buffer = ProtectedSecretBuffer()

        def reader() -> None:
            try:
                read_hidden_tty_line(slave_fd, b"hidden prompt: ", buffer)
            except BaseException as exc:  # test thread must surface failures
                error.append(exc)

        thread = threading.Thread(target=reader)
        thread.start()
        try:
            ready, _, _ = select.select([master_fd], [], [], 2.0)
            self.assertTrue(ready, "TTY prompt was not emitted")
            captured.extend(os.read(master_fd, 4096))
            os.write(master_fd, secret + b"\n")
            thread.join(2.0)
            self.assertFalse(thread.is_alive(), "hidden TTY reader did not finish")
            self.assertFalse(error, error)

            while True:
                ready, _, _ = select.select([master_fd], [], [], 0.05)
                if not ready:
                    break
                captured.extend(os.read(master_fd, 4096))

            self.assertEqual(secret, bytes(buffer.view()))
            self.assertNotIn(secret, bytes(captured))
            after = termios.tcgetattr(slave_fd)
            self.assertEqual(before[3] & termios.ECHO, after[3] & termios.ECHO)
            self.assertEqual(before[3] & termios.ECHONL, after[3] & termios.ECHONL)

            buffer.wipe()
            self.assertEqual(0, buffer.length)
            self.assertTrue(all(value == 0 for value in buffer.storage))
        finally:
            if thread.is_alive():
                os.write(master_fd, b"\n")
                thread.join(1.0)
            buffer.close()
            os.close(master_fd)
            os.close(slave_fd)

    @unittest.skipUnless(
        hasattr(os, "memfd_create") and hasattr(os, "MFD_ALLOW_SEALING") and fcntl is not None,
        "Linux memfd sealing required",
    )
    def test_sealed_memfd_frame_is_exact_and_fully_sealed(self):
        account_bytes = b"synthetic@example.invalid"
        password_bytes = b"synthetic-password"
        account = ProtectedSecretBuffer()
        password = ProtectedSecretBuffer()
        fd = -1
        try:
            account.storage[: len(account_bytes)] = account_bytes
            account.length = len(account_bytes)
            password.storage[: len(password_bytes)] = password_bytes
            password.length = len(password_bytes)
            fd = create_sealed_credential_memfd(account, password)
            size = os.fstat(fd).st_size
            payload = os.pread(fd, size, 0)
            self.assertEqual(
                struct.pack("<II", len(account_bytes), len(password_bytes)) + account_bytes + password_bytes,
                payload,
            )
            required = fcntl.F_SEAL_SEAL | fcntl.F_SEAL_SHRINK | fcntl.F_SEAL_GROW | fcntl.F_SEAL_WRITE
            actual = fcntl.fcntl(fd, fcntl.F_GET_SEALS)
            self.assertEqual(required, actual & required)
        finally:
            if fd >= 0:
                os.close(fd)
            account.close()
            password.close()

    def test_sanitizer_never_forwards_unrecognized_response_fields(self):
        result = sanitize_auth_response(
            {
                "ok": True,
                "command": "AUTH_WITH_CREDENTIALS",
                "invocation_dispatched": True,
                "qmeta_method_id": 17,
                "password": "must-not-escape",
                "session": "must-not-escape",
            }
        )
        self.assertEqual(
            {
                "ok": True,
                "command": "AUTH_WITH_CREDENTIALS",
                "invocation_dispatched": True,
                "qmeta_method_id": 17,
            },
            result,
        )

    def test_source_has_no_unsafe_secret_fallback(self):
        source = (
            Path(__file__).parents[3] / "tools/tibia_runtime_bridge/protected_auth_tty.py"
        ).read_text(encoding="utf-8")
        self.assertNotIn("input(", source)
        self.assertNotIn("getpass", source)
        self.assertNotIn("sys.stdin", source)
        self.assertNotIn('add_argument("--email', source)
        self.assertNotIn('add_argument("--password', source)
        self.assertNotIn("os.environ[", source)
        self.assertNotIn("os.getenv(", source)
        self.assertIn('os.open("/dev/tty"', source)
        self.assertIn("termios.ECHO", source)
        self.assertIn("mlock", source)
        self.assertIn("PR_SET_DUMPABLE", source)
        self.assertIn("os.memfd_create", source)
        self.assertIn("F_SEAL_WRITE", source)
        self.assertIn("auth_with_credentials_fd", source)
        self.assertIn("EXTERNAL_INTERACTIVE_TTY_REQUIRED", source)
        self.assertIn("metadata.st_uid != os.geteuid()", source)
        self.assertIn("metadata.st_mode & 0o022", source)
        self.assertIn("finally:\n            termios.tcsetattr", source)


if __name__ == "__main__":
    unittest.main()
