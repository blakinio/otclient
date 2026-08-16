from __future__ import annotations

from pathlib import Path
import socket
import tempfile
import threading
from typing import Any
import unittest

from tools.tibia_runtime_bridge.health import (
    BridgeBinding,
    BridgeHealth,
    BridgeIdentityError,
    BridgeSession,
    HealthState,
    ReacquireState,
    RecoveryPolicy,
)
from tools.tibia_runtime_bridge.ipc_client import (
    BridgePeerIdentityError,
    BridgeProtocolError,
    BridgeTransportError,
    PeerIdentityExpectation,
    request,
)


class BridgeHealthTests(unittest.TestCase):
    def registration(
        self,
        *,
        registration_generation: int = 1,
        lease_generation: int = 1,
        pid: int = 100,
        process_start_ticks: int = 1000,
    ) -> dict[str, object]:
        return {
            "schema_version": 1,
            "runtime_id": "track-a-canonical-live",
            "registration_generation": registration_generation,
            "lease_generation": lease_generation,
            "boot_id_sha256": "b" * 64,
            "pid": pid,
            "process_start_ticks": process_start_ticks,
            "client_version": "15.32.df7b29",
            "client_size": 51_965_216,
            "client_sha256": "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe",
        }

    def binding(self, name: str = "bridge-a.sock", **registration: int) -> BridgeBinding:
        return BridgeBinding.from_registration(
            self.registration(**registration), socket_path=Path("/tmp") / name
        )

    @staticmethod
    def ping_ok(
        path: Path,
        command: str,
        *,
        timeout: float,
        expected_identity: PeerIdentityExpectation | None = None,
    ) -> dict[str, object]:
        assert path.is_absolute()
        assert command == "PING"
        assert timeout > 0
        assert expected_identity is not None
        return {
            "ok": True,
            "command": "PING",
            "main_base_resolved": True,
            "boot_id_sha256": expected_identity.boot_id_sha256,
            "pid": expected_identity.pid,
            "process_start_ticks": expected_identity.process_start_ticks,
            "client_version": expected_identity.client_version,
            "client_size": expected_identity.client_size,
            "client_sha256": expected_identity.client_sha256,
        }

    @staticmethod
    def status_ok(
        path: Path,
        *,
        timeout: float,
        expected_identity: PeerIdentityExpectation | None = None,
    ) -> dict[str, object]:
        assert path.is_absolute()
        assert timeout > 0
        assert expected_identity is not None
        return {
            "ok": True,
            "in_game_candidate": False,
            "evidence_level": "DERIVED_UNTIL_LIVE_CORRELATION",
            "markers": {},
        }

    def test_exact_fence_mismatch_is_rejected(self):
        registration = self.registration()
        registration["client_sha256"] = "a" * 64
        with self.assertRaises(BridgeIdentityError):
            BridgeBinding.from_registration(registration, socket_path=Path("/tmp/bridge.sock"))

    def test_relative_socket_path_is_rejected(self):
        with self.assertRaises(BridgeIdentityError):
            BridgeBinding.from_registration(
                self.registration(), socket_path=Path("bridge.sock")
            )

    def test_real_missing_socket_is_transport_error(self):
        with tempfile.TemporaryDirectory() as raw:
            missing = Path(raw) / "missing.sock"
            with self.assertRaises(BridgeTransportError):
                request(missing, "PING", timeout=0.1)

    def test_real_invalid_json_is_protocol_error(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "bridge.sock"
            ready = threading.Event()

            def serve() -> None:
                server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                try:
                    server.bind(str(path))
                    server.listen(1)
                    ready.set()
                    connection, _ = server.accept()
                    try:
                        connection.recv(4096)
                        connection.sendall(b"not-json\n")
                    finally:
                        connection.close()
                finally:
                    server.close()

            thread = threading.Thread(target=serve)
            thread.start()
            self.assertTrue(ready.wait(2))
            try:
                with self.assertRaises(BridgeProtocolError):
                    request(path, "PING", timeout=1.0)
            finally:
                thread.join(2)
            self.assertFalse(thread.is_alive())

    def test_healthy_bridge_keeps_session_candidate_derived(self):
        current = self.binding()
        session = BridgeSession(lambda: current, request_fn=self.ping_ok, status_fn=self.status_ok)
        self.assertEqual(ReacquireState.ACQUIRED, session.reacquire().state)

        health = session.probe()

        self.assertEqual(HealthState.HEALTHY, health.state)
        self.assertTrue(health.bridge_ready)
        self.assertFalse(health.in_game_candidate)
        self.assertEqual("DERIVED_UNTIL_LIVE_CORRELATION", health.evidence_level)

    def test_missing_identity_fails_closed(self):
        session = BridgeSession(lambda: None, request_fn=self.ping_ok, status_fn=self.status_ok)
        self.assertEqual(ReacquireState.NO_IDENTITY, session.reacquire().state)
        health = session.probe()
        self.assertEqual(HealthState.NO_IDENTITY, health.state)
        self.assertFalse(health.bridge_ready)

    def test_invalid_binding_source_fails_closed(self):
        session = BridgeSession(lambda: "not-a-binding", request_fn=self.ping_ok, status_fn=self.status_ok)  # type: ignore[arg-type,return-value]
        result = session.reacquire()
        self.assertEqual(ReacquireState.INVALID_IDENTITY, result.state)
        self.assertIsNone(session.binding)

    def test_transport_failure_is_unreachable(self):
        current = self.binding()

        def unreachable(
            path: Path,
            command: str,
            *,
            timeout: float,
            expected_identity: PeerIdentityExpectation | None = None,
        ) -> dict[str, object]:
            assert expected_identity is not None
            raise BridgeTransportError("synthetic socket unavailable")

        session = BridgeSession(lambda: current, request_fn=unreachable, status_fn=self.status_ok)
        session.reacquire()
        self.assertEqual(HealthState.UNREACHABLE, session.probe().state)

    def test_peer_identity_failure_is_stale_and_discards_binding(self):
        current = self.binding()

        def wrong_peer(
            path: Path,
            command: str,
            *,
            timeout: float,
            expected_identity: PeerIdentityExpectation | None = None,
        ) -> dict[str, object]:
            assert expected_identity is not None
            raise BridgePeerIdentityError("synthetic same-path replacement")

        session = BridgeSession(lambda: current, request_fn=wrong_peer, status_fn=self.status_ok)
        session.reacquire()
        health = session.probe()
        self.assertEqual(HealthState.STALE_IDENTITY, health.state)
        self.assertFalse(health.bridge_ready)
        self.assertIsNone(session.binding)

    def test_protocol_failure_is_malformed(self):
        current = self.binding()

        def malformed(
            path: Path,
            command: str,
            *,
            timeout: float,
            expected_identity: PeerIdentityExpectation | None = None,
        ) -> dict[str, object]:
            assert expected_identity is not None
            raise BridgeProtocolError("synthetic malformed response")

        session = BridgeSession(lambda: current, request_fn=malformed, status_fn=self.status_ok)
        session.reacquire()
        self.assertEqual(HealthState.MALFORMED, session.probe().state)

    def test_non_object_ping_is_malformed(self):
        current = self.binding()

        def non_object(
            path: Path,
            command: str,
            *,
            timeout: float,
            expected_identity: PeerIdentityExpectation | None = None,
        ) -> Any:
            assert expected_identity is not None
            return ["not", "an", "object"]

        session = BridgeSession(lambda: current, request_fn=non_object, status_fn=self.status_ok)
        session.reacquire()
        self.assertEqual(HealthState.MALFORMED, session.probe().state)

    def test_incomplete_ping_is_malformed(self):
        current = self.binding()

        def incomplete(
            path: Path,
            command: str,
            *,
            timeout: float,
            expected_identity: PeerIdentityExpectation | None = None,
        ) -> dict[str, object]:
            assert expected_identity is not None
            return {"ok": True, "command": "PING", "main_base_resolved": True}

        session = BridgeSession(lambda: current, request_fn=incomplete, status_fn=self.status_ok)
        session.reacquire()
        self.assertEqual(HealthState.MALFORMED, session.probe().state)

    def test_ping_identity_envelope_mismatch_is_stale(self):
        current = self.binding()

        def mismatched_ping(
            path: Path,
            command: str,
            *,
            timeout: float,
            expected_identity: PeerIdentityExpectation | None = None,
        ) -> dict[str, object]:
            response = self.ping_ok(
                path,
                command,
                timeout=timeout,
                expected_identity=expected_identity,
            )
            response["process_start_ticks"] = int(response["process_start_ticks"]) + 1
            return response

        session = BridgeSession(lambda: current, request_fn=mismatched_ping, status_fn=self.status_ok)
        session.reacquire()
        health = session.probe()
        self.assertEqual(HealthState.STALE_IDENTITY, health.state)
        self.assertIsNone(session.binding)

    def test_bridge_side_discovery_failure_is_degraded(self):
        current = self.binding()

        def failed_status(
            path: Path,
            *,
            timeout: float,
            expected_identity: PeerIdentityExpectation | None = None,
        ) -> dict[str, object]:
            assert expected_identity is not None
            return {
                "ok": False,
                "in_game_candidate": False,
                "evidence_level": "UNKNOWN",
                "response": {"ok": False, "error": "PROC_MEM_OPEN_FAILED"},
            }

        session = BridgeSession(lambda: current, request_fn=self.ping_ok, status_fn=failed_status)
        session.reacquire()
        health = session.probe()
        self.assertEqual(HealthState.DEGRADED, health.state)
        self.assertFalse(health.bridge_ready)

    def test_wrong_session_evidence_level_is_malformed(self):
        current = self.binding()

        def promoted_status(
            path: Path,
            *,
            timeout: float,
            expected_identity: PeerIdentityExpectation | None = None,
        ) -> dict[str, object]:
            assert expected_identity is not None
            return {
                "ok": True,
                "in_game_candidate": True,
                "evidence_level": "AUTHORITATIVE",
            }

        session = BridgeSession(lambda: current, request_fn=self.ping_ok, status_fn=promoted_status)
        session.reacquire()
        self.assertEqual(HealthState.MALFORMED, session.probe().state)

    def test_generation_change_during_probe_discards_cached_channel(self):
        holder = {"binding": self.binding()}
        replacement = self.binding(
            "bridge-b.sock", registration_generation=2, lease_generation=2, pid=101, process_start_ticks=1001
        )

        def ping_and_replace(
            path: Path,
            command: str,
            *,
            timeout: float,
            expected_identity: PeerIdentityExpectation | None = None,
        ) -> dict[str, object]:
            response = self.ping_ok(
                path,
                command,
                timeout=timeout,
                expected_identity=expected_identity,
            )
            holder["binding"] = replacement
            return response

        session = BridgeSession(
            lambda: holder["binding"], request_fn=ping_and_replace, status_fn=self.status_ok
        )
        session.reacquire()
        health = session.probe()
        self.assertEqual(HealthState.STALE_IDENTITY, health.state)
        self.assertIsNone(session.binding)

    def test_same_generation_process_change_is_rejected(self):
        holder = {"binding": self.binding()}
        session = BridgeSession(lambda: holder["binding"], request_fn=self.ping_ok, status_fn=self.status_ok)
        session.reacquire()
        holder["binding"] = self.binding(pid=999, process_start_ticks=9999)

        health = session.probe()

        self.assertEqual(HealthState.STALE_IDENTITY, health.state)
        self.assertIsNone(session.binding)

    def test_generation_regression_is_rejected_on_reacquire(self):
        holder = {
            "binding": self.binding(
                "bridge-b.sock", registration_generation=2, lease_generation=2, pid=101, process_start_ticks=1001
            )
        }
        session = BridgeSession(lambda: holder["binding"], request_fn=self.ping_ok, status_fn=self.status_ok)
        self.assertEqual(ReacquireState.ACQUIRED, session.reacquire().state)
        holder["binding"] = self.binding()

        reacquired = session.reacquire()

        self.assertEqual(ReacquireState.STALE_IDENTITY, reacquired.state)
        self.assertIsNone(session.binding)

    def test_lease_generation_regression_is_rejected_with_new_registration(self):
        holder = {
            "binding": self.binding(
                "bridge-b.sock", registration_generation=2, lease_generation=2, pid=101, process_start_ticks=1001
            )
        }
        session = BridgeSession(lambda: holder["binding"], request_fn=self.ping_ok, status_fn=self.status_ok)
        self.assertEqual(ReacquireState.ACQUIRED, session.reacquire().state)
        holder["binding"] = self.binding(
            "bridge-c.sock", registration_generation=3, lease_generation=1, pid=102, process_start_ticks=1002
        )

        reacquired = session.reacquire()

        self.assertEqual(ReacquireState.STALE_IDENTITY, reacquired.state)
        self.assertIsNone(session.binding)

    def test_recovery_reacquires_new_generation_after_transport_failure(self):
        holder = {"binding": self.binding()}
        replacement = self.binding(
            "bridge-b.sock", registration_generation=2, lease_generation=2, pid=101, process_start_ticks=1001
        )
        calls = {"ping": 0}

        def flaky_ping(
            path: Path,
            command: str,
            *,
            timeout: float,
            expected_identity: PeerIdentityExpectation | None = None,
        ) -> dict[str, object]:
            calls["ping"] += 1
            if calls["ping"] == 1:
                holder["binding"] = replacement
                raise BridgeTransportError("synthetic first endpoint loss")
            return self.ping_ok(
                path,
                command,
                timeout=timeout,
                expected_identity=expected_identity,
            )

        session = BridgeSession(lambda: holder["binding"], request_fn=flaky_ping, status_fn=self.status_ok)
        result = session.recover(RecoveryPolicy(max_attempts=3))

        self.assertTrue(result.recovered)
        self.assertEqual(2, result.attempts)
        self.assertEqual(HealthState.HEALTHY, result.health.state)
        self.assertEqual(replacement, session.binding)

    def test_recovery_exhausts_bounded_attempts_without_side_effects(self):
        current = self.binding()
        retries: list[tuple[int, BridgeHealth]] = []

        def unavailable(
            path: Path,
            command: str,
            *,
            timeout: float,
            expected_identity: PeerIdentityExpectation | None = None,
        ) -> dict[str, object]:
            assert expected_identity is not None
            raise BridgeTransportError("synthetic persistent endpoint loss")

        session = BridgeSession(lambda: current, request_fn=unavailable, status_fn=self.status_ok)
        result = session.recover(
            RecoveryPolicy(max_attempts=2),
            on_retry=lambda attempt, health: retries.append((attempt, health)),
        )

        self.assertFalse(result.recovered)
        self.assertEqual(2, result.attempts)
        self.assertEqual(HealthState.UNREACHABLE, result.health.state)
        self.assertEqual(1, len(retries))
        self.assertEqual(1, retries[0][0])


if __name__ == "__main__":
    unittest.main()
