from __future__ import annotations

from pathlib import Path
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
from tools.tibia_runtime_bridge.ipc_client import BridgeProtocolError, BridgeTransportError


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
    def ping_ok(path: Path, command: str, *, timeout: float) -> dict[str, object]:
        assert path.is_absolute()
        assert command == "PING"
        assert timeout > 0
        return {"ok": True, "command": "PING", "main_base_resolved": True}

    @staticmethod
    def status_ok(path: Path, *, timeout: float) -> dict[str, object]:
        assert path.is_absolute()
        assert timeout > 0
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

    def test_transport_failure_is_unreachable(self):
        current = self.binding()

        def unreachable(path: Path, command: str, *, timeout: float) -> dict[str, object]:
            raise BridgeTransportError("synthetic socket unavailable")

        session = BridgeSession(lambda: current, request_fn=unreachable, status_fn=self.status_ok)
        session.reacquire()
        self.assertEqual(HealthState.UNREACHABLE, session.probe().state)

    def test_protocol_failure_is_malformed(self):
        current = self.binding()

        def malformed(path: Path, command: str, *, timeout: float) -> dict[str, object]:
            raise BridgeProtocolError("synthetic malformed response")

        session = BridgeSession(lambda: current, request_fn=malformed, status_fn=self.status_ok)
        session.reacquire()
        self.assertEqual(HealthState.MALFORMED, session.probe().state)

    def test_incomplete_ping_is_malformed(self):
        current = self.binding()

        def incomplete(path: Path, command: str, *, timeout: float) -> dict[str, object]:
            return {"ok": True, "command": "PING"}

        session = BridgeSession(lambda: current, request_fn=incomplete, status_fn=self.status_ok)
        session.reacquire()
        self.assertEqual(HealthState.MALFORMED, session.probe().state)

    def test_bridge_side_discovery_failure_is_degraded(self):
        current = self.binding()

        def failed_status(path: Path, *, timeout: float) -> dict[str, object]:
            return {"ok": False, "in_game_candidate": False, "evidence_level": "UNKNOWN"}

        session = BridgeSession(lambda: current, request_fn=self.ping_ok, status_fn=failed_status)
        session.reacquire()
        health = session.probe()
        self.assertEqual(HealthState.DEGRADED, health.state)
        self.assertFalse(health.bridge_ready)

    def test_generation_change_during_probe_discards_cached_channel(self):
        holder = {"binding": self.binding()}
        replacement = self.binding(
            "bridge-b.sock", registration_generation=2, lease_generation=2, pid=101, process_start_ticks=1001
        )

        def ping_and_replace(path: Path, command: str, *, timeout: float) -> dict[str, object]:
            holder["binding"] = replacement
            return {"ok": True, "command": "PING", "main_base_resolved": True}

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

    def test_recovery_reacquires_new_generation_after_transport_failure(self):
        holder = {"binding": self.binding()}
        replacement = self.binding(
            "bridge-b.sock", registration_generation=2, lease_generation=2, pid=101, process_start_ticks=1001
        )
        calls = {"ping": 0}

        def flaky_ping(path: Path, command: str, *, timeout: float) -> dict[str, object]:
            calls["ping"] += 1
            if calls["ping"] == 1:
                holder["binding"] = replacement
                raise BridgeTransportError("synthetic first endpoint loss")
            return {"ok": True, "command": "PING", "main_base_resolved": True}

        session = BridgeSession(lambda: holder["binding"], request_fn=flaky_ping, status_fn=self.status_ok)
        result = session.recover(RecoveryPolicy(max_attempts=3))

        self.assertTrue(result.recovered)
        self.assertEqual(2, result.attempts)
        self.assertEqual(HealthState.HEALTHY, result.health.state)
        self.assertEqual(replacement, session.binding)

    def test_recovery_exhausts_bounded_attempts_without_side_effects(self):
        current = self.binding()
        retries: list[tuple[int, BridgeHealth]] = []

        def unavailable(path: Path, command: str, *, timeout: float) -> dict[str, object]:
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
