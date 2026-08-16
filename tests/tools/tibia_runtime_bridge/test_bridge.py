from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest

from tools.tibia_runtime_bridge.ipc_client import (
    BridgeClientError,
    BridgePeerIdentityError,
    PeerIdentityExpectation,
    request,
    session_status,
)
from tools.tibia_runtime_bridge.launcher import BridgeConfigError, build_env, load_profile, sha256_file
from tools.tibia_runtime_bridge.resolver import ResolverError, itanium_nested_name


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
            doc = self.profile(); doc["schema"] = "wrong"
            with self.assertRaises(BridgeConfigError): load_profile(self.write_profile(directory, doc))

    def test_profile_rejects_non_hex_offset(self):
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            doc = self.profile(); doc["targets"]["player_protocol_handler"]["vptr_offset"] = "1234"
            with self.assertRaises(BridgeConfigError): load_profile(self.write_profile(directory, doc))

    def test_profile_rejects_bad_digest(self):
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            doc = self.profile(); doc["binary_sha256"] = "ABC"
            with self.assertRaises(BridgeConfigError): load_profile(self.write_profile(directory, doc))

    def test_sha256_file(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "blob"; path.write_bytes(b"abc")
            self.assertEqual("ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad", sha256_file(path))

    def test_itanium_nested_name(self):
        self.assertEqual(b"N5tibia4game29TPlayerProtocolMessageHandlerE\0", itanium_nested_name("tibia::game::TPlayerProtocolMessageHandler"))
        with self.assertRaises(ResolverError): itanium_nested_name("tibia::::Broken")


class IpcClientTests(unittest.TestCase):
    def run_server_responses(self, path: Path, responses: list[bytes]) -> threading.Thread:
        ready = threading.Event()
        def serve() -> None:
            server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                server.bind(str(path)); server.listen(max(1, len(responses))); ready.set()
                for response in responses:
                    conn, _ = server.accept()
                    try: conn.recv(4096); conn.sendall(response)
                    finally: conn.close()
            finally: server.close()
        thread = threading.Thread(target=serve); thread.start(); self.assertTrue(ready.wait(2)); return thread

    def run_server(self, path: Path, response: bytes) -> threading.Thread:
        return self.run_server_responses(path, [response])

    @staticmethod
    def process_start_ticks(pid: int) -> int:
        raw = Path(f"/proc/{pid}/stat").read_text(encoding="ascii")
        close = raw.rfind(")")
        fields = raw[close + 2 :].split()
        return int(fields[19])

    @staticmethod
    def sha256_path(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb", buffering=0) as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def expectation_for_pid(self, pid: int) -> PeerIdentityExpectation:
        boot = Path("/proc/sys/kernel/random/boot_id").read_text(encoding="ascii").strip().encode()
        exe = Path(os.readlink(f"/proc/{pid}/exe"))
        return PeerIdentityExpectation(
            boot_id_sha256=hashlib.sha256(boot).hexdigest(),
            pid=pid,
            process_start_ticks=self.process_start_ticks(pid),
            client_version="test-peer",
            client_size=exe.stat().st_size,
            client_sha256=self.sha256_path(exe),
        )

    @staticmethod
    def start_process_server(path: Path) -> subprocess.Popen[bytes]:
        script = (
            "import socket,sys\n"
            "path=sys.argv[1]\n"
            "server=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)\n"
            "server.bind(path); server.listen(8)\n"
            "while True:\n"
            "  conn,_=server.accept()\n"
            "  try:\n"
            "    conn.recv(4096)\n"
            "    conn.sendall(b'{\\\"ok\\\":true,\\\"command\\\":\\\"PING\\\"}\\n')\n"
            "  finally:\n"
            "    conn.close()\n"
        )
        process = subprocess.Popen(
            [sys.executable, "-c", script, str(path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        deadline = time.monotonic() + 3.0
        while time.monotonic() < deadline:
            if path.exists():
                return process
            if process.poll() is not None:
                stderr = process.stderr.read().decode("utf-8", errors="replace") if process.stderr else ""
                raise AssertionError(f"server exited before binding socket: {stderr}")
            time.sleep(0.01)
        process.terminate(); process.wait(timeout=2)
        raise AssertionError("server did not bind Unix socket")

    @staticmethod
    def stop_process_server(process: subprocess.Popen[bytes], path: Path) -> None:
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill(); process.wait(timeout=2)
        try:
            path.unlink()
        except FileNotFoundError:
            pass

    def test_ping_response(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "bridge.sock"; thread = self.run_server(path, b'{"ok":true,"command":"PING"}\n')
            try: self.assertEqual("PING", request(path, "PING")["command"])
            finally: thread.join(2)

    def test_discover_response(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "bridge.sock"; thread = self.run_server(path, b'{"ok":true,"target":"player_protocol_handler","scan_status":"OK","vptr_hits":1,"validated_hits":1}\n')
            try: self.assertEqual(1, request(path, "DISCOVER player_protocol_handler")["validated_hits"])
            finally: thread.join(2)

    def test_session_status_candidate_requires_all_markers(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "bridge.sock"
            thread = self.run_server_responses(path, [
                b'{"ok":true,"target":"player_protocol_handler","scan_status":"OK","vptr_hits":1,"validated_hits":1}\n',
                b'{"ok":true,"target":"gameserver_game_session","scan_status":"OK","vptr_hits":1,"validated_hits":1}\n',
                b'{"ok":true,"target":"worldmap_handler","scan_status":"OK","vptr_hits":1,"validated_hits":1}\n'])
            try:
                result = session_status(path); self.assertTrue(result["in_game_candidate"]); self.assertEqual("DERIVED_UNTIL_LIVE_CORRELATION", result["evidence_level"])
            finally: thread.join(2)

    def test_session_status_zero_hits_is_successful_not_in_game(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "bridge.sock"
            thread = self.run_server_responses(path, [
                b'{"ok":true,"target":"player_protocol_handler","scan_status":"OK","vptr_hits":0,"validated_hits":0}\n',
                b'{"ok":true,"target":"gameserver_game_session","scan_status":"OK","vptr_hits":1,"validated_hits":1}\n',
                b'{"ok":true,"target":"worldmap_handler","scan_status":"OK","vptr_hits":1,"validated_hits":1}\n'])
            try:
                result = session_status(path)
                self.assertTrue(result["ok"])
                self.assertFalse(result["in_game_candidate"])
                self.assertEqual("DERIVED_UNTIL_LIVE_CORRELATION", result["evidence_level"])
            finally: thread.join(2)

    def test_session_status_scan_failure_fails_closed(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "bridge.sock"
            thread = self.run_server(path, b'{"ok":false,"error":"PROC_MEM_OPEN_FAILED"}\n')
            try:
                result = session_status(path)
                self.assertFalse(result["ok"])
                self.assertFalse(result["in_game_candidate"])
                self.assertEqual("UNKNOWN", result["evidence_level"])
                self.assertEqual("player_protocol_handler", result["failed_target"])
                self.assertEqual("PROC_MEM_OPEN_FAILED", result["response"]["error"])
            finally: thread.join(2)

    @unittest.skipUnless(hasattr(socket, "SO_PEERCRED") and Path("/proc").is_dir(), "Linux peer credentials required")
    def test_same_path_process_replacement_rejects_stale_peer_identity(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "bridge.sock"
            first = self.start_process_server(path)
            try:
                stale_identity = self.expectation_for_pid(first.pid)
                self.assertTrue(request(path, "PING", expected_identity=stale_identity)["ok"])
            finally:
                self.stop_process_server(first, path)

            second = self.start_process_server(path)
            try:
                with self.assertRaises(BridgePeerIdentityError):
                    request(path, "PING", expected_identity=stale_identity)
            finally:
                self.stop_process_server(second, path)

    def test_invalid_json_fails_closed(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "bridge.sock"; thread = self.run_server(path, b'not-json\n')
            try:
                with self.assertRaises(BridgeClientError): request(path, "PING")
            finally: thread.join(2)

    def test_multiline_command_rejected(self):
        with self.assertRaises(BridgeClientError): request(Path("/unused"), "PING\nSECOND")

    def test_bridge_source_propagates_scan_failures(self):
        source = (Path(__file__).parents[3] / "tools/tibia_runtime_bridge/bridge.cpp").read_text(encoding="utf-8")
        self.assertIn('"PROC_MEM_OPEN_FAILED"', source)
        self.assertIn('"PROC_MEM_READ_FAILED"', source)
        self.assertIn("if (!scan.ok)", source)
        self.assertIn("return errorJson(scan.error);", source)
        self.assertIn('\\"scan_status\\":\\"OK\\"', source)


if __name__ == "__main__":
    unittest.main()
