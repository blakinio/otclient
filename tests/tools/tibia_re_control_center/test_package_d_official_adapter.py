from __future__ import annotations

import unittest

from tools.tibia_re_control_center.execution import MutationCoordinator
from tools.tibia_re_control_center.fake import FakeAdapter, ManualClock
from tools.tibia_re_control_center.model import (
    ActionRequest,
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


if __name__ == "__main__":
    unittest.main()
