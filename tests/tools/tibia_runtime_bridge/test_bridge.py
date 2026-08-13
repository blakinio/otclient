from __future__ import annotations

import json
from pathlib import Path
import socket
import tempfile
import threading
import unittest

from tools.tibia_runtime_bridge.ipc_client import BridgeClientError, request, session_status
from tools.tibia_runtime_bridge.launcher import BridgeConfigError, build_env, load_profile, sha256_file


class ProfileTests(unittest.TestCase):
    def profile(self) -> dict:
        return {
            "schema": "otclient.tibia-runtime-bridge.profile.v1",
            "client_version": "15.32.test",
            "binary_sha256": "a" * 64,
            "targets": {
                "player_protocol_handler": {
                    "resolver": "primary_vptr",
                    "vptr_offset": "0x1234",
                    "expected_qt_class": "tibia::game::TPlayerProtocolMessageHandler",
                    "evidence": "synthetic",
                }
            },
        }

    def write_profile(self, directory: Path, doc: dict) -> Path:
        path = directory / "profile.json"
        path.write_text(json.dumps(doc), encoding="utf-8")
        return path

    def test_valid_profile_and_environment(self):
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            profile = load_profile(self.write_profile(directory, self.profile()))
            env = build_env(profile, directory / "bridge.so", directory / "bridge.sock", {"LD_PRELOAD": "/x.so"})
            self.assertEqual(f"{directory / 'bridge.so'}:/x.so", env["LD_PRELOAD"])
            self.assertEqual(str(directory / "bridge.sock"), env["OTCLIENT_TIBIA_RE_SOCKET"])
            self.assertIn("player_protocol_handler,1234,tibia::game::TPlayerProtocolMessageHandler", env["OTCLIENT_TIBIA_RE_TARGETS"])

    def test_profile_rejects_unknown_schema(self):
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            doc = self.profile()
            doc["schema"] = "wrong"
            with self.assertRaises(BridgeConfigError):
                load_profile(self.write_profile(directory, doc))

    def test_profile_rejects_non_hex_offset(self):
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            doc = self.profile()
            doc["targets"]["player_protocol_handler"]["vptr_offset"] = "1234"
            with self.assertRaises(BridgeConfigError):
                load_profile(self.write_profile(directory, doc))

    def test_profile_rejects_bad_digest(self):
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            doc = self.profile()
            doc["binary_sha256"] = "ABC"
            with self.assertRaises(BridgeConfigError):
                load_profile(self.write_profile(directory, doc))

    def test_sha256_file(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "blob"
            path.write_bytes(b"abc")
            self.assertEqual(
                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
                sha256_file(path),
            )


class IpcClientTests(unittest.TestCase):
    def run_server_responses(self, path: Path, responses: list[bytes]) -> threading.Thread:
        ready = threading.Event()

        def serve() -> None:
            server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                server.bind(str(path))
                server.listen(max(1, len(responses)))
                ready.set()
                for response in responses:
                    conn, _ = server.accept()
                    try:
                        conn.recv(4096)
                        conn.sendall(response)
                    finally:
                        conn.close()
            finally:
                server.close()

        thread = threading.Thread(target=serve)
        thread.start()
        self.assertTrue(ready.wait(2))
        return thread

    def run_server(self, path: Path, response: bytes) -> threading.Thread:
        return self.run_server_responses(path, [response])

    def test_ping_response(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "bridge.sock"
            thread = self.run_server(path, b'{"ok":true,"command":"PING"}\n')
            try:
                self.assertEqual("PING", request(path, "PING")["command"])
            finally:
                thread.join(2)

    def test_discover_response(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "bridge.sock"
            thread = self.run_server(path, b'{"ok":true,"target":"player_protocol_handler","vptr_hits":1,"validated_hits":1}\n')
            try:
                result = request(path, "DISCOVER player_protocol_handler")
                self.assertEqual(1, result["validated_hits"])
            finally:
                thread.join(2)

    def test_session_status_candidate_requires_all_markers(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "bridge.sock"
            responses = [
                b'{"ok":true,"target":"player_protocol_handler","vptr_hits":1,"validated_hits":1}\n',
                b'{"ok":true,"target":"gameserver_game_session","vptr_hits":1,"validated_hits":1}\n',
                b'{"ok":true,"target":"worldmap_handler","vptr_hits":1,"validated_hits":1}\n',
            ]
            thread = self.run_server_responses(path, responses)
            try:
                result = session_status(path)
                self.assertTrue(result["in_game_candidate"])
                self.assertEqual("DERIVED_UNTIL_LIVE_CORRELATION", result["evidence_level"])
            finally:
                thread.join(2)

    def test_session_status_false_when_marker_absent(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "bridge.sock"
            responses = [
                b'{"ok":true,"target":"player_protocol_handler","vptr_hits":0,"validated_hits":0}\n',
                b'{"ok":true,"target":"gameserver_game_session","vptr_hits":1,"validated_hits":1}\n',
                b'{"ok":true,"target":"worldmap_handler","vptr_hits":1,"validated_hits":1}\n',
            ]
            thread = self.run_server_responses(path, responses)
            try:
                self.assertFalse(session_status(path)["in_game_candidate"])
            finally:
                thread.join(2)

    def test_invalid_json_fails_closed(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "bridge.sock"
            thread = self.run_server(path, b'not-json\n')
            try:
                with self.assertRaises(BridgeClientError):
                    request(path, "PING")
            finally:
                thread.join(2)

    def test_multiline_command_rejected(self):
        with self.assertRaises(BridgeClientError):
            request(Path("/unused"), "PING\nSECOND")


if __name__ == "__main__":
    unittest.main()
