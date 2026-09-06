from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from tools.tibia_runtime_bridge.ipc_client import BridgeClientError


_CURRENT = {
    "version": "15.32.be4f48",
    "size": 52105824,
    "sha256": "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1",
}


def _write_identity(path: Path, **overrides: object) -> None:
    doc: dict[str, object] = {
        "boot_id_sha256": "a" * 64,
        "pid": 4242,
        "process_start_ticks": 123456,
        "client_version": _CURRENT["version"],
        "client_size": _CURRENT["size"],
        "client_sha256": _CURRENT["sha256"],
    }
    doc.update(overrides)
    path.write_text(json.dumps(doc) + "\n", encoding="utf-8")
    os.chmod(path, 0o600)


class SecretVaultAuthTests(unittest.TestCase):
    def test_load_identity_requires_exact_current_fence(self) -> None:
        from tools.tibia_runtime_bridge.secret_vault_auth import load_current_runtime_identity

        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "identity.json"
            _write_identity(path)
            identity = load_current_runtime_identity(path)
            self.assertEqual(identity.pid, 4242)
            self.assertEqual(identity.process_start_ticks, 123456)
            self.assertEqual(identity.client_version, _CURRENT["version"])
            self.assertEqual(identity.client_size, _CURRENT["size"])
            self.assertEqual(identity.client_sha256, _CURRENT["sha256"])

            _write_identity(path, client_sha256="0" * 64)
            with self.assertRaisesRegex(BridgeClientError, "current client"):
                load_current_runtime_identity(path)

    def test_vault_auth_rejects_legacy_credential_environment(self) -> None:
        from tools.tibia_runtime_bridge.secret_vault_auth import run_vault_auth

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            identity = root / "identity.json"
            _write_identity(identity)
            with mock.patch.dict(os.environ, {"TIBIA_TEST_EMAIL": "forbidden"}, clear=False):
                with self.assertRaisesRegex(BridgeClientError, "environment"):
                    run_vault_auth(root / "vault", root / "auth.sock", identity)

    def test_vault_auth_passes_only_sealed_fd_and_current_identity_then_closes_fd(self) -> None:
        from tools.tibia_runtime_bridge.secret_vault_auth import run_vault_auth

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            identity_path = root / "identity.json"
            _write_identity(identity_path)
            read_fd, write_fd = os.pipe()
            os.close(write_fd)
            try:
                with (
                    mock.patch(
                        "tools.tibia_runtime_bridge.secret_vault_auth.decrypt_to_sealed_memfd",
                        return_value=read_fd,
                    ) as decrypt,
                    mock.patch(
                        "tools.tibia_runtime_bridge.secret_vault_auth.auth_with_credentials_fd",
                        return_value={
                            "ok": True,
                            "command": "AUTH_WITH_CREDENTIALS",
                            "invocation_dispatched": True,
                            "qmeta_method_id": 17,
                            "qmeta_signature": "must-not-leak",
                            "secret": "must-not-leak",
                        },
                    ) as auth,
                ):
                    result = run_vault_auth(root / "vault", root / "auth.sock", identity_path)
                decrypt.assert_called_once_with(root / "vault")
                args, kwargs = auth.call_args
                self.assertEqual(args[0], root / "auth.sock")
                self.assertEqual(args[1], read_fd)
                expected = kwargs["expected_identity"]
                self.assertEqual(expected.pid, 4242)
                self.assertEqual(expected.client_version, _CURRENT["version"])
                self.assertEqual(
                    result,
                    {
                        "ok": True,
                        "command": "AUTH_WITH_CREDENTIALS",
                        "invocation_dispatched": True,
                        "qmeta_method_id": 17,
                    },
                )
                with self.assertRaises(OSError):
                    os.fstat(read_fd)
            finally:
                try:
                    os.close(read_fd)
                except OSError:
                    pass

    def test_paths_must_be_absolute_and_identity_file_private(self) -> None:
        from tools.tibia_runtime_bridge.secret_vault_auth import load_current_runtime_identity, run_vault_auth

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            identity = root / "identity.json"
            _write_identity(identity)
            os.chmod(identity, 0o666)
            with self.assertRaisesRegex(BridgeClientError, "permissions"):
                load_current_runtime_identity(identity)
            os.chmod(identity, 0o600)
            with self.assertRaisesRegex(BridgeClientError, "absolute"):
                run_vault_auth(Path("vault"), root / "auth.sock", identity)


if __name__ == "__main__":
    unittest.main()
