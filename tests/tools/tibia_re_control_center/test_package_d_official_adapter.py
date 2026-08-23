from __future__ import annotations

import importlib
import io
import json
import tempfile
import unittest
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path
from unittest import mock

from tools.tibia_re_control_center.execution import MutationCoordinator
from tools.tibia_re_control_center.fake import FakeAdapter, ManualClock
from tools.tibia_re_control_center.model import (
    ActionRequest,
    ActionStatus,
    AdapterIdentity,
    AdapterKind,
    Authority,
    Confirmation,
    DispatchFence,
    DispatchState,
    LifecycleState,
    SideEffectBudget,
)
from tools.tibia_re_control_center.scenario import action_request_hash
from tools.tibia_re_control_center.store import DeterministicDurableStore


def mutation_budget() -> SideEffectBudget:
    return SideEffectBudget(
        max_runtime_seconds=10,
        max_actions=4,
        max_movement_tiles=4,
        max_spells=0,
        max_consumables=0,
        max_items_moved=0,
        max_gold=0,
        max_tibia_coins=0,
        max_irreversible_changes=4,
    )


def request_for_adapter(coordinator: MutationCoordinator, adapter: FakeAdapter) -> ActionRequest:
    parameters = {"direction": "NORTH"}
    identity = adapter.identity()
    request_hash = action_request_hash(
        schema_version=1,
        run_id="run-d",
        step_id="turn-step",
        attempt_index=1,
        kind="turn",
        parameters=parameters,
        timeout_ms=1000,
        required_capability="turn",
        required_authority=Authority.MUTATION,
    )
    return ActionRequest(
        action_id="action-turn-1",
        run_id="run-d",
        step_id="turn-step",
        attempt_index=1,
        kind="turn",
        parameters=parameters,
        timeout_ms=1000,
        required_capability="turn",
        required_authority=Authority.MUTATION,
        dispatch_fence=DispatchFence(
            expected_backend_epoch=coordinator.backend_epoch,
            expected_control_generation=coordinator.control_generation,
            expected_adapter_generation=identity.adapter_generation,
            expected_runtime_instance_id=identity.runtime_instance_id,
            expected_session_epoch=identity.session_epoch,
        ),
        effect_bound=adapter.effect_bound("turn", parameters),
        action_request_hash=request_hash,
    )


class CommittedAmbiguousAdapter(FakeAdapter):
    def execute_committed(self, request, commit_dispatch):
        committed = commit_dispatch()
        return {
            "committed": committed,
            "effect": None,
            "outcome": "ambiguous" if committed else None,
            "reason_code": "OFFICIAL_CONFIRMATION_UNAVAILABLE",
        }


class InvalidOutcomeAdapter(FakeAdapter):
    def execute_committed(self, request, commit_dispatch):
        committed = commit_dispatch()
        return {
            "committed": committed,
            "effect": None,
            "outcome": "unexpected" if committed else None,
        }


class PackageDExecutionResultTests(unittest.TestCase):
    def test_committed_ambiguous_execution_never_becomes_pass(self):
        clock = ManualClock()
        adapter = CommittedAmbiguousAdapter(clock)
        adapter.add_capability("turn")
        store = DeterministicDurableStore()
        coordinator = MutationCoordinator(adapter, store, clock, backend_epoch="backend-d")
        coordinator.start_run("run-d", mutation_budget(), mutation_capable=True)
        request = request_for_adapter(coordinator, adapter)

        result = coordinator.execute_action(request)

        self.assertEqual(result.lifecycle_state, LifecycleState.AMBIGUOUS)
        self.assertEqual(result.status, ActionStatus.AMBIGUOUS)
        self.assertEqual(result.dispatch_state, DispatchState.POSSIBLY_DISPATCHED)
        self.assertEqual(result.authoritative_confirmation, Confirmation.UNKNOWN)
        self.assertEqual(result.reason_code, "OFFICIAL_CONFIRMATION_UNAVAILABLE")
        ledger = store.load_budget("run-d")
        self.assertIsNotNone(ledger)
        assert ledger is not None
        self.assertEqual(ledger.dimensions["max_actions"].at_risk, 0)
        self.assertEqual(ledger.dimensions["max_actions"].uncertain, 1)

    def test_invalid_committed_outcome_is_conservatively_ambiguous(self):
        clock = ManualClock()
        adapter = InvalidOutcomeAdapter(clock)
        adapter.add_capability("turn")
        store = DeterministicDurableStore()
        coordinator = MutationCoordinator(adapter, store, clock, backend_epoch="backend-d")
        coordinator.start_run("run-d", mutation_budget(), mutation_capable=True)
        request = request_for_adapter(coordinator, adapter)

        result = coordinator.execute_action(request)

        self.assertEqual(result.lifecycle_state, LifecycleState.AMBIGUOUS)
        self.assertEqual(result.status, ActionStatus.AMBIGUOUS)
        self.assertEqual(result.dispatch_state, DispatchState.POSSIBLY_DISPATCHED)
        self.assertEqual(result.authoritative_confirmation, Confirmation.UNKNOWN)
        self.assertEqual(result.reason_code, "POST_DISPATCH_OUTCOME_INVALID")
        ledger = store.load_budget("run-d")
        self.assertIsNotNone(ledger)
        assert ledger is not None
        self.assertEqual(ledger.dimensions["max_actions"].at_risk, 0)
        self.assertEqual(ledger.dimensions["max_actions"].uncertain, 1)


class PackageDOfficialAdapterTests(unittest.TestCase):
    def test_official_adapter_is_non_actionable_without_promotion(self):
        try:
            module = importlib.import_module("tools.tibia_re_control_center.official_adapter")
        except ModuleNotFoundError:
            self.fail("OfficialTibiaAdapter production module is missing")
        identity = AdapterIdentity(
            adapter_id="official",
            adapter_kind=AdapterKind.OFFICIAL_TIBIA,
            adapter_version="1.0",
            adapter_generation="official-generation-1",
            runtime_instance_id="runtime-1",
            session_epoch="session-1",
        )
        adapter = module.OfficialTibiaAdapter(identity, object(), promotions=())

        capability = adapter.capability("turn")

        self.assertIsNotNone(capability)
        self.assertFalse(adapter.allow_mutation)
        self.assertFalse(capability.action_supported)

    def test_current_evidence_promotion_enables_only_that_action_locally(self):
        module = importlib.import_module("tools.tibia_re_control_center.official_adapter")
        self.assertTrue(hasattr(module, "OfficialCapabilityPromotion"))
        identity = AdapterIdentity(
            adapter_id="official",
            adapter_kind=AdapterKind.OFFICIAL_TIBIA,
            adapter_version="1.0",
            adapter_generation="official-generation-1",
            runtime_instance_id="runtime-1",
            session_epoch="session-1",
        )
        promotion = module.OfficialCapabilityPromotion(
            action_kind="turn",
            client_sha256=module.CURRENT_CLIENT_SHA256,
            read_gate="R2",
            action_gate="A3",
            semantic_path_id="turn-v1",
            confirmation_id="facing-direction-v1",
            requires_input_lock=True,
            evidence_refs=("evidence:current-turn",),
            adapter_generation=identity.adapter_generation,
        )
        adapter = module.OfficialTibiaAdapter(identity, object(), promotions=(promotion,))

        self.assertTrue(adapter.allow_mutation)
        self.assertTrue(adapter.capability("turn").action_supported)
        self.assertFalse(adapter.capability("move").action_supported)

    def test_stale_promotion_build_or_generation_is_not_actionable(self):
        module = importlib.import_module("tools.tibia_re_control_center.official_adapter")
        identity = AdapterIdentity(
            adapter_id="official",
            adapter_kind=AdapterKind.OFFICIAL_TIBIA,
            adapter_version="1.0",
            adapter_generation="official-generation-1",
            runtime_instance_id="runtime-1",
            session_epoch="session-1",
        )
        base = {
            "action_kind": "turn",
            "client_sha256": module.CURRENT_CLIENT_SHA256,
            "read_gate": "R2",
            "action_gate": "A3",
            "semantic_path_id": "turn-v1",
            "confirmation_id": "facing-direction-v1",
            "requires_input_lock": True,
            "evidence_refs": ("evidence:current-turn",),
            "adapter_generation": identity.adapter_generation,
        }
        stale_cases = (
            dict(base, client_sha256="0" * 64),
            dict(base, adapter_generation="old-generation"),
        )
        for values in stale_cases:
            with self.subTest(values=values):
                promotion = module.OfficialCapabilityPromotion(**values)
                adapter = module.OfficialTibiaAdapter(identity, object(), promotions=(promotion,))
                self.assertFalse(adapter.allow_mutation)
                self.assertFalse(adapter.capability("turn").action_supported)

    def test_incomplete_or_insufficient_promotion_never_enables_mutation(self):
        module = importlib.import_module("tools.tibia_re_control_center.official_adapter")
        identity = AdapterIdentity(
            adapter_id="official",
            adapter_kind=AdapterKind.OFFICIAL_TIBIA,
            adapter_version="1.0",
            adapter_generation="official-generation-1",
            runtime_instance_id="runtime-1",
            session_epoch="session-1",
        )
        base = {
            "action_kind": "turn",
            "client_sha256": module.CURRENT_CLIENT_SHA256,
            "read_gate": "R2",
            "action_gate": "A3",
            "semantic_path_id": "turn-v1",
            "confirmation_id": "facing-direction-v1",
            "requires_input_lock": True,
            "evidence_refs": ("evidence:current-turn",),
            "adapter_generation": identity.adapter_generation,
        }
        invalid_cases = (
            dict(base, action_kind="not-a-scenario-action"),
            dict(base, read_gate="R0"),
            dict(base, action_gate="A1"),
            dict(base, semantic_path_id=""),
            dict(base, confirmation_id=""),
            dict(base, requires_input_lock=False),
            dict(base, evidence_refs=()),
        )
        for values in invalid_cases:
            with self.subTest(values=values):
                promotion = module.OfficialCapabilityPromotion(**values)
                adapter = module.OfficialTibiaAdapter(identity, object(), promotions=(promotion,))
                self.assertFalse(adapter.allow_mutation)
                self.assertFalse(adapter.capability("turn").action_supported)

    def test_guarded_session_wraps_commit_and_crosses_exactly_once(self):
        module = importlib.import_module("tools.tibia_re_control_center.official_adapter")
        self.assertTrue(hasattr(module, "GuardedRuntimeView"))
        self.assertTrue(hasattr(module, "GuardedExecutionOutcome"))
        identity = AdapterIdentity(
            adapter_id="official",
            adapter_kind=AdapterKind.OFFICIAL_TIBIA,
            adapter_version="1.0",
            adapter_generation="official-generation-1",
            runtime_instance_id="runtime-1",
            session_epoch="session-1",
        )
        promotion = module.OfficialCapabilityPromotion(
            action_kind="turn",
            client_sha256=module.CURRENT_CLIENT_SHA256,
            read_gate="R2",
            action_gate="A3",
            semantic_path_id="turn-v1",
            confirmation_id="facing-direction-v1",
            requires_input_lock=True,
            evidence_refs=("evidence:current-turn",),
            adapter_generation=identity.adapter_generation,
        )

        class Session:
            def __init__(self):
                self.cross_calls = 0

            def current_view(self):
                return module.GuardedRuntimeView(
                    adapter_generation=identity.adapter_generation,
                    runtime_instance_id=identity.runtime_instance_id,
                    session_epoch=identity.session_epoch,
                    client_state="IN_GAME",
                    authority_current=True,
                    target_unique=True,
                    input_lock_held=True,
                    fence_digest="a" * 64,
                )

            def cross_once_and_reconcile(self, request):
                self.cross_calls += 1
                if self.cross_calls != 1:
                    raise AssertionError("physical boundary crossed more than once")
                return module.GuardedExecutionOutcome(
                    outcome="confirmed",
                    reason_code=None,
                    evidence_refs=("evidence:turn-after",),
                )

        class Bridge:
            def __init__(self, session):
                self.session = session
                self.guard_entries = 0

            def advisory_available(self, request):
                return True

            @contextmanager
            def guarded_dispatch(self, request):
                self.guard_entries += 1
                yield self.session

            def emergency_stop(self, reason):
                return None

        session = Session()
        bridge = Bridge(session)
        adapter = module.OfficialTibiaAdapter(identity, bridge, promotions=(promotion,))
        clock = ManualClock()
        store = DeterministicDurableStore()
        coordinator = MutationCoordinator(adapter, store, clock, backend_epoch="backend-d")
        coordinator.start_run("run-d", mutation_budget(), mutation_capable=True)
        request = request_for_adapter(coordinator, adapter)

        result = coordinator.execute_action(request)

        self.assertEqual(result.lifecycle_state, LifecycleState.CONFIRMED)
        self.assertEqual(result.status, ActionStatus.PASS)
        self.assertEqual(result.dispatch_state, DispatchState.DISPATCHED)
        self.assertEqual(result.authoritative_confirmation, Confirmation.PROVEN)
        self.assertEqual(bridge.guard_entries, 1)
        self.assertEqual(session.cross_calls, 1)


FORBIDDEN_PUBLIC_KEY_PARTS = {
    "pid", "xid", "display", "window", "token", "coordinate",
    "address", "pointer", "opcode", "keycode", "lease_capability",
}


def assert_sanitized_mapping(testcase, value):
    for key in value:
        lowered = key.lower()
        testcase.assertFalse(any(part in lowered for part in FORBIDDEN_PUBLIC_KEY_PARTS))


class PackageDTrackABridgeProtocolTests(unittest.TestCase):
    def test_bridge_strict_normalized_records_reject_extra_keys(self):
        module = importlib.import_module(
            "tools.tibia_re_control_center.track_a_authority_bridge"
        )
        ready = {"type": "ready", "action_hash": "a" * 64, "fence_digest": "b" * 64}
        result = {
            "type": "result",
            "outcome": "confirmed",
            "reason_code": None,
            "evidence_refs": (),
        }
        self.assertEqual(module.require_exact_record(ready, module.READY_KEYS), ready)
        self.assertEqual(module.require_exact_record(result, module.RESULT_KEYS), result)
        assert_sanitized_mapping(self, ready)
        assert_sanitized_mapping(self, result)
        with self.assertRaises(Exception) as caught:
            module.require_exact_record(dict(ready, pid=123), module.READY_KEYS)
        self.assertEqual(caught.exception.code, "TRACK_A_BRIDGE_PROTOCOL_INVALID")
        with self.assertRaises(Exception) as caught:
            module.normalize_result(dict(result, outcome="unexpected"))
        self.assertEqual(caught.exception.code, "TRACK_A_BRIDGE_PROTOCOL_INVALID")

    def _bridge_and_fake_process(self, lines, *, client_state="IN_GAME"):
        module = importlib.import_module(
            "tools.tibia_re_control_center.track_a_authority_bridge"
        )
        repo = Path(__file__).resolve().parents[3]
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        token = root / "lease.token"
        token.write_text("secret-never-read")
        probe = repo / ".github/scripts/tibia-official-client-re-canonical-live-session.sh"

        class FakeProcess:
            def __init__(self):
                self.stdin = io.StringIO()
                self.stdout = io.StringIO("".join(lines))
                self.returncode = None

            def poll(self):
                return self.returncode

            def wait(self, timeout=None):
                self.returncode = 0
                return 0

            def terminate(self):
                self.returncode = 2

        process = FakeProcess()
        bridge = module.CanonicalTrackAAuthorityBridge(
            repo, "OTC-TEST", "session-test", token, probe, probe,
            client_state_provider=lambda: client_state,
            ready_timeout_seconds=0.03,
            result_timeout_seconds=0.03,
            process_factory=lambda _command, _cwd: process,
        )
        return module, temp, bridge, process

    def test_guarded_session_normalizes_ready_and_commits_once(self):
        action_hash = "a" * 64
        fence = "b" * 64
        ready = "TRACK_A_GUARDED_DISPATCH_READY=" + json.dumps({
            "protocol": "track-a-guarded-dispatch-v1",
            "status": "READY",
            "action_hash": action_hash,
            "fence_digest": fence,
        }, separators=(",", ":")) + "\n"
        result = "TRACK_A_GUARDED_DISPATCH_RESULT=" + json.dumps({
            "status": "CONFIRMED",
            "effect_count": 1,
            "action_hash": action_hash,
        }, separators=(",", ":")) + "\n"
        module, temp, bridge, process = self._bridge_and_fake_process([ready, result])
        request = mock.Mock(
            action_request_hash=action_hash,
            kind="turn",
            parameters={"direction": "NORTH"},
            dispatch_fence=mock.Mock(
                expected_adapter_generation="g1",
                expected_runtime_instance_id="r1",
                expected_session_epoch="s1",
            ),
        )
        try:
            with bridge.guarded_dispatch(request) as session:
                    view = session.current_view()
                    self.assertEqual(view.client_state, "IN_GAME")
                    self.assertTrue(view.authority_current)
                    self.assertTrue(view.target_unique)
                    self.assertTrue(view.input_lock_held)
                    self.assertEqual(view.fence_digest, fence)
                    outcome = session.cross_once_and_reconcile(request)
                    self.assertEqual(outcome.outcome, "confirmed")
                    self.assertEqual(outcome.reason_code, None)
                    with self.assertRaises(Exception):
                        session.cross_once_and_reconcile(request)
            self.assertEqual(process.stdin.getvalue(), "COMMIT\n")
        finally:
            temp.cleanup()

    def test_guarded_context_exit_before_commit_sends_abort(self):
        action_hash = "a" * 64
        ready = "TRACK_A_GUARDED_DISPATCH_READY=" + json.dumps({
            "protocol": "track-a-guarded-dispatch-v1", "status": "READY",
            "action_hash": action_hash, "fence_digest": "b" * 64,
        }, separators=(",", ":")) + "\n"
        module, temp, bridge, process = self._bridge_and_fake_process([ready])
        request = mock.Mock(
            action_request_hash=action_hash, kind="turn", parameters={"direction": "NORTH"},
            dispatch_fence=mock.Mock(
                expected_adapter_generation="g1", expected_runtime_instance_id="r1",
                expected_session_epoch="s1",
            ),
        )
        try:
            with bridge.guarded_dispatch(request):
                    pass
            self.assertEqual(process.stdin.getvalue(), "ABORT\n")
        finally:
            temp.cleanup()

    def test_timeout_after_commit_is_ambiguous_without_second_commit(self):
        action_hash = "a" * 64
        ready = "TRACK_A_GUARDED_DISPATCH_READY=" + json.dumps({
            "protocol": "track-a-guarded-dispatch-v1", "status": "READY",
            "action_hash": action_hash, "fence_digest": "b" * 64,
        }, separators=(",", ":")) + "\n"
        module, temp, bridge, process = self._bridge_and_fake_process([ready])
        request = mock.Mock(
            action_request_hash=action_hash, kind="turn", parameters={"direction": "NORTH"},
            dispatch_fence=mock.Mock(
                expected_adapter_generation="g1", expected_runtime_instance_id="r1",
                expected_session_epoch="s1",
            ),
        )
        try:
            with bridge.guarded_dispatch(request) as session:
                    outcome = session.cross_once_and_reconcile(request)
            self.assertEqual(outcome.outcome, "ambiguous")
            self.assertEqual(outcome.reason_code, "TRACK_A_RESULT_TIMEOUT")
            self.assertEqual(process.stdin.getvalue(), "COMMIT\n")
        finally:
            temp.cleanup()

    def test_bridge_command_passes_token_path_without_reading_contents(self):
        module = importlib.import_module(
            "tools.tibia_re_control_center.track_a_authority_bridge"
        )
        repo = Path(__file__).resolve().parents[3]
        with tempfile.TemporaryDirectory() as td:
            token = Path(td) / "lease.token"
            token.write_text("secret-never-read")
            probe = repo / ".github/scripts/tibia-official-client-re-canonical-live-session.sh"
            worker = probe
            bridge = module.CanonicalTrackAAuthorityBridge(
                repo, "OTC-TEST", "session-test", token, probe, worker
            )
            with mock.patch.object(Path, "read_text", side_effect=AssertionError("token read")):
                command = bridge.command_for_request_file(Path(td) / "request.json")
            self.assertEqual(command[0], module.sys.executable)
            self.assertIn("guarded-dispatch", command)
            self.assertIn(str(token), command)
            self.assertNotIn("secret-never-read", command)


class RecordingDecisionInput(io.StringIO):
    def __init__(self, process):
        super().__init__()
        self.process = process

    def write(self, value):
        if value == "COMMIT\n":
            self.process.effect_count += 1
        self.process.decisions.append(value)
        return super().write(value)


class FakeTransitionProcess:
    def __init__(self, lines):
        self.decisions = []
        self.effect_count = 0
        self.stdin = RecordingDecisionInput(self)
        self.stdout = io.StringIO("".join(lines))
        self.returncode = None

    def poll(self):
        return self.returncode

    def wait(self, timeout=None):
        self.returncode = 0
        return 0

    def terminate(self):
        self.returncode = 2


class PackageDConcreteBridgeE2ETests(unittest.TestCase):
    def _stack(self, client_state_provider):
        adapter_module = importlib.import_module("tools.tibia_re_control_center.official_adapter")
        bridge_module = importlib.import_module("tools.tibia_re_control_center.track_a_authority_bridge")
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        repo = Path(__file__).resolve().parents[3]
        token = root / "lease.token"
        token.write_text("secret-never-read")
        helper = repo / ".github/scripts/tibia-official-client-re-canonical-live-session.sh"
        identity = AdapterIdentity(
            adapter_id="official", adapter_kind=AdapterKind.OFFICIAL_TIBIA,
            adapter_version="1.0", adapter_generation="official-generation-1",
            runtime_instance_id="runtime-1", session_epoch="session-1",
        )
        transport_holder = {}
        bridge = bridge_module.CanonicalTrackAAuthorityBridge(
            repo, "OTC-TEST", "session-test", token, helper, helper,
            client_state_provider=client_state_provider,
            ready_timeout_seconds=0.03, result_timeout_seconds=0.03,
            process_factory=lambda _command, _cwd: transport_holder["process"],
        )
        bridge._test_transport_holder = transport_holder
        promotion = adapter_module.OfficialCapabilityPromotion(
            action_kind="turn", client_sha256=adapter_module.CURRENT_CLIENT_SHA256,
            read_gate="R2", action_gate="A3", semantic_path_id="turn-v1",
            confirmation_id="facing-direction-v1", requires_input_lock=True,
            evidence_refs=("evidence:fake-turn",), adapter_generation=identity.adapter_generation,
        )
        adapter = adapter_module.OfficialTibiaAdapter(identity, bridge, promotions=(promotion,))
        clock = ManualClock()
        store = DeterministicDurableStore()
        coordinator = MutationCoordinator(adapter, store, clock, backend_epoch="backend-d")
        coordinator.start_run("run-d", mutation_budget(), mutation_capable=True)
        request = request_for_adapter(coordinator, adapter)
        return temp, bridge_module, coordinator, request

    @staticmethod
    def _ready(action_hash):
        return "TRACK_A_GUARDED_DISPATCH_READY=" + json.dumps({
            "protocol": "track-a-guarded-dispatch-v1", "status": "READY",
            "action_hash": action_hash, "fence_digest": "b" * 64,
        }, separators=(",", ":")) + "\n"

    @staticmethod
    def _result(action_hash, status):
        return "TRACK_A_GUARDED_DISPATCH_RESULT=" + json.dumps({
            "status": status, "effect_count": 1, "action_hash": action_hash,
        }, separators=(",", ":")) + "\n"

    def test_concrete_bridge_confirmed_turn_full_path(self):
        temp, module, coordinator, request = self._stack(lambda: "IN_GAME")
        process = FakeTransitionProcess([self._ready(request.action_request_hash), self._result(request.action_request_hash, "CONFIRMED")])
        try:
            coordinator.adapter._authority_bridge._test_transport_holder["process"] = process
            result = coordinator.execute_action(request)
            self.assertEqual(result.lifecycle_state, LifecycleState.CONFIRMED)
            self.assertEqual(result.status, ActionStatus.PASS)
            self.assertEqual(result.dispatch_state, DispatchState.DISPATCHED)
            self.assertEqual(result.authoritative_confirmation, Confirmation.PROVEN)
            self.assertEqual(process.effect_count, 1)
            self.assertEqual(process.decisions.count("COMMIT\n"), 1)
        finally:
            temp.cleanup()

    def test_concrete_bridge_ambiguous_result_is_never_retried(self):
        temp, module, coordinator, request = self._stack(lambda: "IN_GAME")
        process = FakeTransitionProcess([self._ready(request.action_request_hash), self._result(request.action_request_hash, "AMBIGUOUS")])
        try:
            coordinator.adapter._authority_bridge._test_transport_holder["process"] = process
            result = coordinator.execute_action(request)
            self.assertEqual(result.lifecycle_state, LifecycleState.AMBIGUOUS)
            self.assertEqual(result.dispatch_state, DispatchState.POSSIBLY_DISPATCHED)
            self.assertEqual(process.effect_count, 1)
            self.assertEqual(process.decisions.count("COMMIT\n"), 1)
        finally:
            temp.cleanup()

    def test_concrete_bridge_timeout_before_ready_has_zero_effect(self):
        temp, module, coordinator, request = self._stack(lambda: "IN_GAME")
        process = FakeTransitionProcess([])
        try:
            coordinator.adapter._authority_bridge._test_transport_holder["process"] = process
            result = coordinator.execute_action(request)
            self.assertEqual(result.dispatch_state, DispatchState.NOT_DISPATCHED)
            self.assertEqual(process.effect_count, 0)
            self.assertEqual(process.decisions.count("COMMIT\n"), 0)
        finally:
            temp.cleanup()

    def test_concrete_bridge_timeout_after_commit_is_ambiguous_once(self):
        temp, module, coordinator, request = self._stack(lambda: "IN_GAME")
        process = FakeTransitionProcess([self._ready(request.action_request_hash)])
        try:
            coordinator.adapter._authority_bridge._test_transport_holder["process"] = process
            result = coordinator.execute_action(request)
            self.assertEqual(result.lifecycle_state, LifecycleState.AMBIGUOUS)
            self.assertEqual(result.dispatch_state, DispatchState.POSSIBLY_DISPATCHED)
            self.assertEqual(process.effect_count, 1)
            self.assertEqual(process.decisions.count("COMMIT\n"), 1)
        finally:
            temp.cleanup()

    def test_stop_between_ready_and_commit_aborts_with_zero_effect(self):
        holder = {"calls": 0, "coordinator": None, "stopped": False}
        def state_provider():
            holder["calls"] += 1
            if holder["calls"] >= 3 and not holder["stopped"]:
                holder["stopped"] = True
                holder["coordinator"].stop_all(reason_code="TEST_STOP")
            return "IN_GAME"
        temp, module, coordinator, request = self._stack(state_provider)
        holder["coordinator"] = coordinator
        process = FakeTransitionProcess([self._ready(request.action_request_hash)])
        try:
            coordinator.adapter._authority_bridge._test_transport_holder["process"] = process
            result = coordinator.execute_action(request)
            self.assertEqual(result.dispatch_state, DispatchState.NOT_DISPATCHED)
            self.assertIn(result.lifecycle_state, {LifecycleState.REFUSED, LifecycleState.CANCELLED_BEFORE_DISPATCH})
            self.assertEqual(process.effect_count, 0)
            self.assertEqual(process.decisions.count("COMMIT\n"), 0)
            self.assertEqual(process.decisions.count("ABORT\n"), 1)
        finally:
            temp.cleanup()

    def test_control_generation_drift_after_ready_has_zero_effect(self):
        holder = {"calls": 0, "coordinator": None, "drifted": False}
        def state_provider():
            holder["calls"] += 1
            if holder["calls"] >= 3 and not holder["drifted"]:
                holder["drifted"] = True
                c = holder["coordinator"]
                c.control_state = replace(c.control_state, control_generation=c.control_generation + 1)
            return "IN_GAME"
        temp, module, coordinator, request = self._stack(state_provider)
        holder["coordinator"] = coordinator
        process = FakeTransitionProcess([self._ready(request.action_request_hash)])
        try:
            coordinator.adapter._authority_bridge._test_transport_holder["process"] = process
            result = coordinator.execute_action(request)
            self.assertEqual(result.dispatch_state, DispatchState.NOT_DISPATCHED)
            self.assertEqual(process.effect_count, 0)
            self.assertEqual(process.decisions.count("COMMIT\n"), 0)
        finally:
            temp.cleanup()


if __name__ == "__main__":
    unittest.main()
