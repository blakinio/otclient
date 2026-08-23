from __future__ import annotations

import unittest
from contextlib import contextmanager

from tools.tibia_re_control_center.execution import MutationCoordinator
from tools.tibia_re_control_center.fake import ManualClock
from tools.tibia_re_control_center.model import (
    ActionStatus,
    AdapterIdentity,
    AdapterKind,
    Confirmation,
    DispatchState,
    LifecycleState,
)
from tools.tibia_re_control_center.official_adapter import (
    CURRENT_CLIENT_SHA256,
    GuardedExecutionOutcome,
    GuardedRuntimeView,
    OfficialCapabilityPromotion,
    OfficialTibiaAdapter,
)
from tools.tibia_re_control_center.store import DeterministicDurableStore

from .test_package_d_official_adapter import mutation_budget, request_for_adapter


def official_identity() -> AdapterIdentity:
    return AdapterIdentity(
        adapter_id="official",
        adapter_kind=AdapterKind.OFFICIAL_TIBIA,
        adapter_version="1.0",
        adapter_generation="official-generation-1",
        runtime_instance_id="runtime-1",
        session_epoch="session-1",
    )


def turn_promotion(identity: AdapterIdentity) -> OfficialCapabilityPromotion:
    return OfficialCapabilityPromotion(
        action_kind="turn",
        client_sha256=CURRENT_CLIENT_SHA256,
        read_gate="R2",
        action_gate="A3",
        semantic_path_id="turn-v1",
        confirmation_id="facing-direction-v1",
        requires_input_lock=True,
        evidence_refs=("evidence:current-turn",),
        adapter_generation=identity.adapter_generation,
    )


class Session:
    def __init__(
        self,
        identity: AdapterIdentity,
        *,
        input_lock_held: bool = True,
        target_unique: bool = True,
        raise_after_cross: bool = False,
    ) -> None:
        self.identity = identity
        self.input_lock_held = input_lock_held
        self.target_unique = target_unique
        self.raise_after_cross = raise_after_cross
        self.cross_calls = 0

    def current_view(self) -> GuardedRuntimeView:
        return GuardedRuntimeView(
            adapter_generation=self.identity.adapter_generation,
            runtime_instance_id=self.identity.runtime_instance_id,
            session_epoch=self.identity.session_epoch,
            client_state="IN_GAME",
            authority_current=True,
            target_unique=self.target_unique,
            input_lock_held=self.input_lock_held,
            fence_digest="a" * 64,
        )

    def cross_once_and_reconcile(self, request) -> GuardedExecutionOutcome:
        self.cross_calls += 1
        if self.cross_calls != 1:
            raise AssertionError("physical boundary crossed more than once")
        if self.raise_after_cross:
            raise RuntimeError("synthetic reconciliation failure")
        return GuardedExecutionOutcome(
            outcome="confirmed",
            reason_code=None,
            evidence_refs=("evidence:turn-after",),
        )


class Bridge:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.guard_entries = 0

    def advisory_available(self, request) -> bool:
        return True

    @contextmanager
    def guarded_dispatch(self, request):
        self.guard_entries += 1
        yield self.session

    def emergency_stop(self, reason: str) -> None:
        return None


def execute_with(session: Session):
    identity = session.identity
    bridge = Bridge(session)
    adapter = OfficialTibiaAdapter(
        identity,
        bridge,
        promotions=(turn_promotion(identity),),
    )
    clock = ManualClock()
    store = DeterministicDurableStore()
    coordinator = MutationCoordinator(adapter, store, clock, backend_epoch="backend-d")
    coordinator.start_run("run-d", mutation_budget(), mutation_capable=True)
    request = request_for_adapter(coordinator, adapter)
    result = coordinator.execute_action(request)
    return result, bridge


class PackageDOfficialAdapterFalsificationTests(unittest.TestCase):
    def test_missing_input_lock_refuses_before_commit_with_zero_effects(self):
        session = Session(official_identity(), input_lock_held=False)

        result, bridge = execute_with(session)

        self.assertEqual(result.status, ActionStatus.REFUSED)
        self.assertEqual(result.dispatch_state, DispatchState.NOT_DISPATCHED)
        self.assertEqual(session.cross_calls, 0)
        self.assertEqual(bridge.guard_entries, 1)

    def test_non_unique_target_refuses_before_commit_with_zero_effects(self):
        session = Session(official_identity(), target_unique=False)

        result, bridge = execute_with(session)

        self.assertEqual(result.status, ActionStatus.REFUSED)
        self.assertEqual(result.dispatch_state, DispatchState.NOT_DISPATCHED)
        self.assertEqual(session.cross_calls, 0)
        self.assertEqual(bridge.guard_entries, 1)

    def test_reconciliation_failure_after_commit_stays_ambiguous(self):
        session = Session(official_identity(), raise_after_cross=True)

        result, bridge = execute_with(session)

        self.assertEqual(result.lifecycle_state, LifecycleState.AMBIGUOUS)
        self.assertEqual(result.status, ActionStatus.AMBIGUOUS)
        self.assertEqual(result.dispatch_state, DispatchState.POSSIBLY_DISPATCHED)
        self.assertEqual(result.authoritative_confirmation, Confirmation.UNKNOWN)
        self.assertEqual(result.reason_code, "TRACK_A_RECONCILIATION_FAILED")
        self.assertEqual(session.cross_calls, 1)
        self.assertEqual(bridge.guard_entries, 1)


if __name__ == "__main__":
    unittest.main()
