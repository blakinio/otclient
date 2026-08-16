from __future__ import annotations

import copy
import unittest

from tools.tibia_runtime_bridge.health import (
    CANONICAL_NAMESPACE,
    EXACT_CLIENT_SHA256,
    EXACT_CLIENT_SIZE,
    EXACT_CLIENT_VERSION,
    Readiness,
    ReacquisitionAction,
    RecoveryAction,
    RecoveryState,
    build_recovery_report,
    decide_reacquisition,
    evaluate_health,
    recovery_transition,
)


class HealthFixture(unittest.TestCase):
    now_ms = 10_500
    lease_generation = 9

    def registration(self) -> dict:
        return {
            "schema_version": 1,
            "runtime_id": "track-a-canonical-live",
            "registration_generation": 7,
            "lease_generation": self.lease_generation,
            "registered_at": "2026-08-16T13:00:00+02:00",
            "boot_id_sha256": "b" * 64,
            "pid": 1234,
            "process_start_ticks": 5678,
            "client_version": EXACT_CLIENT_VERSION,
            "client_size": EXACT_CLIENT_SIZE,
            "client_sha256": EXACT_CLIENT_SHA256,
            "display": ":98",
            "window_identity": {"window_id": "0x123", "pid": 1234},
            "remote_view_endpoint": None,
            "remote_view_mapping": "UNKNOWN",
            "state": "LOGIN",
            "source_task": "synthetic-runtime-producer",
            "source_run": "synthetic-run",
        }

    def observation(self, registration: dict | None = None) -> dict:
        reg = self.registration() if registration is None else registration
        return {
            "schema": "otclient.tibia-runtime-bridge.runtime-observation.v1",
            "runtime_namespace": CANONICAL_NAMESPACE,
            "checked_at_unix_ms": 10_000,
            "gate_b": "PASS",
            "target_uniqueness": "PROVEN",
            "registration_generation": reg["registration_generation"],
            "lease_generation": reg["lease_generation"],
            "boot_id_sha256": reg["boot_id_sha256"],
            "pid": reg["pid"],
            "process_start_ticks": reg["process_start_ticks"],
            "client_version": reg["client_version"],
            "client_size": reg["client_size"],
            "client_sha256": reg["client_sha256"],
            "display": reg["display"],
            "window_identity": copy.deepcopy(reg["window_identity"]),
        }

    def ping(self, registration: dict | None = None) -> dict:
        reg = self.registration() if registration is None else registration
        return {
            "ok": True,
            "command": "PING",
            "main_base_resolved": True,
            "pid": reg["pid"],
            "process_start_ticks": reg["process_start_ticks"],
            "client_version": reg["client_version"],
            "binary_sha256": reg["client_sha256"],
        }

    def health(self, registration: dict | None = None, observation: dict | None = None, ping: dict | None = None, **kwargs):
        reg = self.registration() if registration is None else registration
        obs = self.observation(reg) if observation is None else observation
        bridge_ping = self.ping(reg) if ping is None else ping
        return evaluate_health(
            reg,
            obs,
            bridge_ping,
            expected_lease_generation=kwargs.pop("expected_lease_generation", self.lease_generation),
            now_ms=kwargs.pop("now_ms", self.now_ms),
            **kwargs,
        )


class HealthEvaluationTests(HealthFixture):
    def test_ready_requires_registration_gate_b_and_identity_bound_ping(self):
        report = self.health()
        self.assertTrue(report.ready)
        self.assertEqual(Readiness.READY, report.readiness)
        self.assertIsNotNone(report.identity)
        self.assertEqual("UNKNOWN_NOT_EVALUATED_BY_HEALTH_API", report.as_dict()["in_game"])

    def test_absent_registration_fails_closed(self):
        report = evaluate_health(
            None,
            None,
            None,
            expected_lease_generation=self.lease_generation,
            now_ms=self.now_ms,
        )
        self.assertFalse(report.ready)
        self.assertEqual(Readiness.NOT_REGISTERED, report.readiness)
        self.assertIsNone(report.as_dict()["usable_identity"])

    def test_unknown_expected_lease_generation_fails_closed(self):
        report = evaluate_health(self.registration(), self.observation(), self.ping(), expected_lease_generation=None, now_ms=self.now_ms)
        self.assertEqual(Readiness.EXPECTED_AUTHORITY_UNAVAILABLE, report.readiness)

    def test_registration_lease_generation_mismatch_rejected(self):
        registration = self.registration()
        registration["lease_generation"] = self.lease_generation - 1
        observation = self.observation(registration)
        report = self.health(registration, observation, expected_lease_generation=self.lease_generation)
        self.assertEqual(Readiness.LEASE_GENERATION_MISMATCH, report.readiness)

    def test_boolean_pid_is_not_accepted_as_integer(self):
        registration = self.registration()
        registration["pid"] = True
        observation = self.observation(registration)
        report = self.health(registration, observation)
        self.assertEqual(Readiness.REGISTRATION_INVALID, report.readiness)

    def test_exact_client_fence_mismatch_rejected(self):
        registration = self.registration()
        registration["client_sha256"] = "a" * 64
        observation = self.observation(registration)
        report = self.health(registration, observation)
        self.assertEqual(Readiness.REGISTRATION_INVALID, report.readiness)

    def test_incomplete_canonical_registration_rejected(self):
        registration = self.registration()
        del registration["source_run"]
        report = self.health(registration, self.observation(registration))
        self.assertEqual(Readiness.REGISTRATION_INVALID, report.readiness)

    def test_non_json_window_identity_rejected(self):
        registration = self.registration()
        registration["window_identity"] = {"bad": {1, 2}}
        observation = self.observation(registration)
        report = self.health(registration, observation)
        self.assertEqual(Readiness.REGISTRATION_INVALID, report.readiness)

    def test_observation_namespace_mismatch_rejected(self):
        observation = self.observation()
        observation["runtime_namespace"] = "historical-display-98"
        report = self.health(observation=observation)
        self.assertEqual(Readiness.NAMESPACE_MISMATCH, report.readiness)

    def test_gate_b_or_uniqueness_not_proven_rejected(self):
        observation = self.observation()
        observation["gate_b"] = "REQUIRED_NOT_PROVEN"
        report = self.health(observation=observation)
        self.assertEqual(Readiness.GATE_B_NOT_PROVEN, report.readiness)

    def test_stale_observation_rejected(self):
        report = self.health(now_ms=30_001, max_observation_age_ms=15_000)
        self.assertEqual(Readiness.OBSERVATION_STALE, report.readiness)

    def test_future_observation_beyond_skew_rejected(self):
        observation = self.observation()
        observation["checked_at_unix_ms"] = 12_000
        report = self.health(observation=observation, now_ms=10_000, max_future_skew_ms=1_000)
        self.assertEqual(Readiness.OBSERVATION_FROM_FUTURE, report.readiness)

    def test_gate_b_identity_mismatch_rejected(self):
        observation = self.observation()
        observation["process_start_ticks"] += 1
        report = self.health(observation=observation)
        self.assertEqual(Readiness.IDENTITY_MISMATCH, report.readiness)

    def test_bridge_ping_must_prove_main_base(self):
        ping = self.ping()
        ping["main_base_resolved"] = False
        report = self.health(ping=ping)
        self.assertEqual(Readiness.BRIDGE_UNHEALTHY, report.readiness)

    def test_bridge_ping_must_match_registered_pid_and_start_ticks(self):
        ping = self.ping()
        ping["pid"] += 1
        report = self.health(ping=ping)
        self.assertEqual(Readiness.BRIDGE_UNHEALTHY, report.readiness)

    def test_bridge_ping_must_match_exact_profile_identity(self):
        ping = self.ping()
        ping["binary_sha256"] = "a" * 64
        report = self.health(ping=ping)
        self.assertEqual(Readiness.BRIDGE_UNHEALTHY, report.readiness)

    def test_game_state_does_not_change_runtime_readiness_claim(self):
        login_registration = self.registration()
        in_game_registration = self.registration()
        in_game_registration["state"] = "IN_GAME"
        login = self.health(login_registration, self.observation(login_registration))
        in_game = self.health(in_game_registration, self.observation(in_game_registration))
        self.assertTrue(login.ready)
        self.assertTrue(in_game.ready)
        self.assertEqual("UNKNOWN_NOT_EVALUATED_BY_HEALTH_API", login.as_dict()["in_game"])
        self.assertEqual("UNKNOWN_NOT_EVALUATED_BY_HEALTH_API", in_game.as_dict()["in_game"])


class ReacquisitionTests(HealthFixture):
    def test_first_ready_identity_is_accepted(self):
        latest = self.health()
        self.assertEqual(ReacquisitionAction.ACCEPT_REACQUIRED, decide_reacquisition(None, latest))

    def test_same_exact_identity_can_be_kept(self):
        latest = self.health()
        self.assertEqual(ReacquisitionAction.KEEP_CURRENT, decide_reacquisition(latest.identity, latest))

    def test_new_registration_generation_is_reacquired(self):
        current = self.health().identity
        registration = self.registration()
        registration["registration_generation"] += 1
        latest = self.health(registration, self.observation(registration))
        self.assertEqual(ReacquisitionAction.ACCEPT_REACQUIRED, decide_reacquisition(current, latest))

    def test_invalid_latest_evidence_drops_old_identity(self):
        current = self.health().identity
        stale = self.health(now_ms=30_001, max_observation_age_ms=15_000)
        self.assertEqual(ReacquisitionAction.DROP_CURRENT_AND_WAIT, decide_reacquisition(current, stale))

    def test_no_current_and_invalid_latest_waits_without_guessing(self):
        report = evaluate_health(None, None, None, expected_lease_generation=self.lease_generation, now_ms=self.now_ms)
        self.assertEqual(ReacquisitionAction.WAIT_FOR_VALID_REGISTRATION, decide_reacquisition(None, report))


class RecoveryTests(HealthFixture):
    def test_ready_to_degraded_to_reacquiring_and_back_to_ready(self):
        ready = self.health()
        unhealthy_ping = self.ping()
        unhealthy_ping["ok"] = False
        unhealthy = self.health(ping=unhealthy_ping)
        state, action = recovery_transition(RecoveryState.READY, unhealthy)
        self.assertEqual(RecoveryState.DEGRADED, state)
        self.assertEqual(RecoveryAction.REACQUIRE, action)
        state, action = recovery_transition(state, unhealthy)
        self.assertEqual(RecoveryState.REACQUIRING, state)
        self.assertEqual(RecoveryAction.WAIT_FOR_VALID_REGISTRATION, action)
        state, action = recovery_transition(state, ready)
        self.assertEqual(RecoveryState.READY, state)
        self.assertEqual(RecoveryAction.NONE, action)

    def test_recovery_report_never_exposes_old_identity_on_failure(self):
        current = self.health().identity
        unhealthy_ping = self.ping()
        unhealthy_ping["ok"] = False
        unhealthy = self.health(ping=unhealthy_ping)
        report = build_recovery_report(current, RecoveryState.READY, unhealthy)
        self.assertEqual("DROP_CURRENT_AND_WAIT", report["reacquisition_action"])
        self.assertIsNone(report["accepted_identity"])
        self.assertEqual("UNKNOWN_NOT_EVALUATED_BY_RECOVERY_API", report["in_game"])


if __name__ == "__main__":
    unittest.main()
