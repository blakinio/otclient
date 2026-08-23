from __future__ import annotations

import importlib
import unittest
from contextlib import contextmanager

from tools.tibia_re_control_center.execution import MutationCoordinator
from tools.tibia_re_control_center.fake import FakeAdapter, ManualClock
from tools.tibia_re_control_center.model import (
    ActionRequest,
    AdapterIdentity,
    AdapterKind,
    ActionStatus,
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
        base = dict(
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
        base = dict(
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


if __name__ == "__main__":
    unittest.main()
