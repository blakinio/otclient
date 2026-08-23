from __future__ import annotations

import hashlib
import inspect
import json
import threading
import unittest
from pathlib import Path

from tools.tibia_re_control_center.artifact import ArtifactStore
from tools.tibia_re_control_center.canonical import jcs_dumps
from tools.tibia_re_control_center.comparison import (
    CheckpointPair,
    ComparisonClass,
    ComparisonProfile,
    ComparisonStatus,
    NormalizedObservation,
    ObservationStatus,
    ProfileField,
    compare_runs,
)
from tools.tibia_re_control_center.engine import ScenarioEngine
from tools.tibia_re_control_center.execution import (
    CancellationToken,
    MutationCoordinator,
)
from tools.tibia_re_control_center.fake import FakeAdapter, ManualClock
from tools.tibia_re_control_center.model import (
    MAX_U64,
    ActionRequest,
    ActionStatus,
    Authority,
    DispatchFence,
    DispatchState,
    LifecycleState,
    OrderingConfidence,
    PolicyActionProposal,
    PrivacyError,
    SideEffectBudget,
    ValidationError,
    checked_add,
    negotiate_major,
)
from tools.tibia_re_control_center.recorder import (
    Recorder,
    construct_screenshot,
    safe_error,
)
from tools.tibia_re_control_center.scenario import (
    ACTION_KINDS,
    PredicateOutcome,
    action_request_hash,
    default_effect_bound,
    evaluate_predicate,
    parse_and_validate,
    parse_document,
    validate_abort_condition,
    validate_action_parameters,
    validate_predicate,
)
from tools.tibia_re_control_center.store import DeterministicDurableStore


def budget(**overrides: int) -> SideEffectBudget:
    values = {
        "max_runtime_seconds": 10,
        "max_actions": 10,
        "max_movement_tiles": 10,
        "max_spells": 10,
        "max_consumables": 10,
        "max_items_moved": 100,
        "max_gold": 0,
        "max_tibia_coins": 0,
        "max_irreversible_changes": 10,
    }
    values.update(overrides)
    return SideEffectBudget(**values)


def scenario_dict(
    *,
    scenario_id: str = "scenario-json",
    steps: list[dict] | None = None,
    preconditions: list[dict] | None = None,
    expected: list[dict] | None = None,
) -> dict:
    if steps is None:
        steps = [{"action": {"id": "move-one", "kind": "move", "parameters": {"direction": "NORTH", "tiles": 1}, "timeout_ms": 1000}}]
    return {
        "schema_version": 1,
        "id": scenario_id,
        "name": "Package A scenario",
        "adapter_requirements": {"reads": [], "actions": ["move"]},
        "preconditions": preconditions or [],
        "side_effect_budget": budget().as_dict(),
        "capture_policy": {"state": True, "events": True, "screenshots": "NONE", "network": "NONE", "traces": "NONE"},
        "steps": steps,
        "abort_conditions": [],
        "expected_result": expected or [],
        "privacy_policy": {"secret_material": "REJECT", "private_chat": "OMIT", "identities": "OMIT", "screenshots": "SAFE_ONLY"},
    }


def yaml_scenario() -> str:
    return """schema_version: 1
id: scenario-yaml
name: Scenario YAML
adapter_requirements:
  reads: []
  actions: [move]
preconditions: []
side_effect_budget:
  max_runtime_seconds: 10
  max_actions: 2
  max_movement_tiles: 2
  max_spells: 0
  max_consumables: 0
  max_items_moved: 0
  max_gold: 0
  max_tibia_coins: 0
  max_irreversible_changes: 0
capture_policy:
  state: true
  events: true
  screenshots: NONE
  network: NONE
  traces: NONE
steps:
  - action:
      id: move-one
      kind: move
      parameters: {direction: NORTH, tiles: 1}
      timeout_ms: 1000
abort_conditions: []
expected_result: []
privacy_policy:
  secret_material: REJECT
  private_chat: OMIT
  identities: OMIT
  screenshots: SAFE_ONLY
"""


def stack(
    *,
    allow_mutation: bool = True,
    store: DeterministicDurableStore | None = None,
    backend_epoch: str | None = None,
    run_budget: SideEffectBudget | None = None,
    start_run: bool = True,
    concurrency_safe_reads: bool = True,
) -> tuple[ManualClock, FakeAdapter, DeterministicDurableStore, MutationCoordinator]:
    clock = ManualClock()
    adapter = FakeAdapter(clock, allow_mutation=allow_mutation, concurrency_safe_reads=concurrency_safe_reads)
    for capability in ACTION_KINDS:
        adapter.add_capability(capability)
    durable = store or DeterministicDurableStore()
    coordinator = MutationCoordinator(adapter, durable, clock, backend_epoch=backend_epoch)
    if start_run:
        coordinator.start_run("run-1", run_budget or budget(), mutation_capable=True)
    return clock, adapter, durable, coordinator


def request_for(
    coordinator: MutationCoordinator,
    adapter: FakeAdapter,
    *,
    action_id: str = "action-1",
    run_id: str = "run-1",
    kind: str = "move",
    parameters: dict | None = None,
    required_capability: str | None = None,
    authority: Authority = Authority.MUTATION,
    attempt_index: int = 1,
    hash_override: str | None = None,
) -> ActionRequest:
    params = parameters or ({"direction": "NORTH", "tiles": 1} if kind == "move" else {})
    bound = adapter.effect_bound(kind, params)
    capability = required_capability or kind
    identity = adapter.identity()
    request_hash = hash_override or action_request_hash(
        schema_version=1,
        run_id=run_id,
        step_id="step-1",
        attempt_index=attempt_index,
        kind=kind,
        parameters=params,
        timeout_ms=1000,
        required_capability=capability,
        required_authority=authority,
    )
    return ActionRequest(
        action_id=action_id,
        run_id=run_id,
        step_id="step-1",
        attempt_index=attempt_index,
        kind=kind,
        parameters=params,
        timeout_ms=1000,
        required_capability=capability,
        required_authority=authority,
        dispatch_fence=DispatchFence(
            expected_backend_epoch=coordinator.backend_epoch,
            expected_control_generation=coordinator.control_generation,
            expected_adapter_generation=identity.adapter_generation,
            expected_runtime_instance_id=identity.runtime_instance_id,
            expected_session_epoch=identity.session_epoch,
        ),
        effect_bound=bound,
        action_request_hash=request_hash,
    )


def artifact_fixture() -> tuple[ArtifactStore, Recorder, str]:
    scenario = parse_and_validate(json.dumps(scenario_dict()))
    artifacts = ArtifactStore()
    clock = ManualClock()
    recorder = Recorder(clock, backend_epoch="b", adapter_id="fake", adapter_generation="g")
    artifacts.create_run(
        run_id="run-artifact",
        scenario_id=scenario.scenario_id,
        scenario_hash=scenario.scenario_hash,
        scenario_ast=scenario.ast,
        adapter_identity={"adapter_id": "fake", "adapter_kind": "FAKE_TEST", "adapter_version": "1", "adapter_generation": "g"},
        backend_epoch="b",
        initial_control_generation=0,
        started_monotonic_ns=0,
        privacy_policy=scenario.ast["privacy_policy"],
    )
    return artifacts, recorder, "run-artifact"


class PackageAMandatoryTests(unittest.TestCase):
    def test_01_safe_bounded_json_scenario_acceptance(self):
        parsed = parse_and_validate(json.dumps(scenario_dict()))
        self.assertEqual("scenario-json", parsed.scenario_id)
        self.assertEqual(1, len(parsed.steps))

    def test_02_safe_bounded_yaml_scenario_acceptance(self):
        parsed = parse_and_validate(yaml_scenario())
        self.assertEqual("scenario-yaml", parsed.scenario_id)
        self.assertEqual("scenario-yaml:move-one", parsed.steps[0].step_id)

    def test_03_duplicate_key_rejection(self):
        with self.assertRaisesRegex(ValidationError, "duplicate"):
            parse_document('{"schema_version":1,"schema_version":1}')
        with self.assertRaisesRegex(ValidationError, "duplicate"):
            parse_document("a: 1\na: 2\n")

    def test_04_custom_yaml_tag_object_constructor_rejection(self):
        for text in ("a: !!python/object:bad {}", "a: &x 1\nb: *x\n", "a: 1\nb:\n  <<: *x\n"):
            with self.subTest(text=text), self.assertRaises(ValidationError):
                parse_document(text)

    def test_05_alias_depth_size_collection_string_step_limits(self):
        with self.assertRaises(ValidationError):
            parse_document("a: &x 1\nb: *x\n")
        with self.assertRaises(ValidationError):
            parse_document("[" * 33 + "0" + "]" * 33)
        with self.assertRaises(ValidationError):
            parse_document("x" * 262145)
        with self.assertRaises(ValidationError):
            parse_document(json.dumps(list(range(4097))))
        with self.assertRaises(ValidationError):
            parse_document(json.dumps("x" * 8193))
        many_steps = scenario_dict(steps=[{"snapshot": {"name": "x"}} for _ in range(1025)])
        with self.assertRaises(ValidationError):
            parse_and_validate(json.dumps(many_steps))

    def test_06_invalid_non_finite_number_rejection(self):
        for text in ('{"x": NaN}', "x: .inf", "x: -.inf"):
            with self.subTest(text=text), self.assertRaises(ValidationError):
                parse_document(text)
        invalid = scenario_dict()
        invalid["side_effect_budget"]["max_runtime_seconds"] = 0
        with self.assertRaises(ValidationError):
            parse_and_validate(json.dumps(invalid))

    def test_07_canonical_scenario_hash_vector(self):
        parsed = parse_and_validate(json.dumps(scenario_dict()))
        expected = hashlib.sha256(
            json.dumps(parsed.ast, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        ).hexdigest()
        self.assertEqual(expected, parsed.scenario_hash)

    def test_08_canonical_action_request_hash_vector(self):
        payload = {
            "schema_version": 1,
            "run_id": "r",
            "step_id": "s",
            "attempt_index": 1,
            "kind": "move",
            "parameters": {"direction": "NORTH", "tiles": 1},
            "timeout_ms": 1000,
            "required_capability": "move",
            "required_authority": "MUTATION",
        }
        expected = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual(expected, action_request_hash(**payload))

    def test_09_stable_explicit_generated_step_ids(self):
        parsed = parse_and_validate(json.dumps(scenario_dict(steps=[
            {"snapshot": {"id": "before", "name": "before"}},
            {"snapshot": {"name": "generated"}},
        ])))
        self.assertEqual(("scenario-json:before", "scenario-json:step-0002"), tuple(step.step_id for step in parsed.steps))

    def test_10_typed_predicate_unknown_and_type_mismatch(self):
        predicate, _ = validate_predicate({"field": "player.hp", "op": "EQ", "value": 10, "unknown_policy": "FAIL"})
        self.assertEqual(PredicateOutcome.UNKNOWN, evaluate_predicate(predicate, {"player": {}}))
        self.assertEqual(PredicateOutcome.ERROR, evaluate_predicate(predicate, {"player": {"hp": "10"}}))

    def test_11_semantic_action_parameter_validation_every_v1_family(self):
        cases = {
            "move": {"direction": "NORTH", "tiles": 1},
            "turn": {"direction": "EAST"},
            "stop_movement": {},
            "say_controlled_text": {"text": "test", "text_class": "TEST_GENERATED"},
            "cast_spell": {"spell_key": "spell.exura", "target": None},
            "use_consumable": {"consumable_key": "potion", "target": {"kind": "SELF"}, "quantity": 1},
            "eat_food": {"food_key": "ham", "quantity": 1},
            "use_rune": {"rune_key": "rune.sd", "target": {"kind": "SELECTED_TARGET"}, "quantity": 1},
            "select_target": {"target": {"kind": "CREATURE_ID", "creature_id": 1}},
            "attack": {"target": {"kind": "SELECTED_TARGET"}},
            "cancel_attack": {},
            "follow": {"target": {"kind": "SELECTED_TARGET"}},
            "cancel_follow": {},
            "open_container": {"item": {"kind": "INVENTORY_SLOT", "inventory_slot": "backpack"}},
            "close_container": {"container": "backpack"},
            "use_item": {"item": {"kind": "INVENTORY_SLOT", "inventory_slot": "backpack"}, "target": None},
            "look_item": {"item": {"kind": "INVENTORY_SLOT", "inventory_slot": "backpack"}},
            "move_item": {"item": {"kind": "CONTAINER_SLOT", "container_ref": "bag", "slot_index": 0}, "destination": {"kind": "INVENTORY_SLOT", "inventory_slot": "backpack"}, "count": 1},
            "equip": {"item": {"kind": "INVENTORY_SLOT", "inventory_slot": "backpack"}, "slot": "HEAD"},
            "unequip": {"slot": "HEAD", "destination": {"kind": "INVENTORY_SLOT", "inventory_slot": "backpack"}},
            "open_panel": {"panel_key": "skills"},
            "close_panel": {"panel_key": "skills"},
            "logout": {},
        }
        self.assertEqual(ACTION_KINDS, set(cases))
        for kind, parameters in cases.items():
            with self.subTest(kind=kind):
                self.assertIsInstance(validate_action_parameters(kind, parameters), dict)
        with self.assertRaises(ValidationError):
            validate_action_parameters("login_request", {})

    def test_12_stale_ambiguous_semantic_selector_refusal(self):
        _, adapter, _, coordinator = stack()
        adapter.selector_state["selected_target"] = "AMBIGUOUS"
        request = request_for(
            coordinator,
            adapter,
            kind="attack",
            parameters={"target": {"kind": "SELECTED_TARGET"}},
        )
        result = coordinator.execute_action(request)
        self.assertEqual("SELECTOR_NOT_UNIQUE_FRESH", result.reason_code)
        self.assertEqual([], adapter.physical_effects)

    def test_13_unsupported_capability_refusal(self):
        _, adapter, _, coordinator = stack()
        request = request_for(coordinator, adapter, required_capability="missing")
        result = coordinator.execute_action(request)
        self.assertEqual("CAPABILITY_UNSUPPORTED", result.reason_code)
        self.assertEqual([], adapter.physical_effects)

    def test_14_effect_bound_generation_and_unbounded_refusal(self):
        self.assertEqual(1, default_effect_bound("move", {"direction": "NORTH", "tiles": 1}).max_movement_tiles)
        clock = ManualClock()
        adapter = FakeAdapter(clock)
        adapter.set_effect_bound("move", None)
        with self.assertRaisesRegex(ValidationError, "unbounded"):
            adapter.effect_bound("move", {"direction": "NORTH", "tiles": 1})

    def test_15_read_only_mutation_refusal(self):
        _, adapter, _, coordinator = stack(allow_mutation=False)
        result = coordinator.execute_action(request_for(coordinator, adapter))
        self.assertEqual("READ_ONLY_MUTATION_REFUSED", result.reason_code)
        self.assertEqual([], adapter.physical_effects)

    def test_16_fresh_backend_epoch_on_restart(self):
        clock, _, store, first = stack(backend_epoch="backend-one")
        first.clean_shutdown()
        second = MutationCoordinator(FakeAdapter(clock), store, clock, backend_epoch="backend-two")
        self.assertNotEqual(first.backend_epoch, second.backend_epoch)

    def test_17_stale_backend_callback_refusal(self):
        _, adapter, _, coordinator = stack()
        request = request_for(coordinator, adapter)
        coordinator._reserve(coordinator.runs["run-1"], request)
        self.assertFalse(coordinator.accept_callback(
            request.action_id,
            backend_epoch="old-backend",
            control_generation=coordinator.control_generation,
            lifecycle_state=LifecycleState.CONFIRMED,
        ))

    def test_18_authority_loss_exactly_before_commit(self):
        _, adapter, _, coordinator = stack()
        adapter.before_commit_hook = lambda: setattr(adapter, "authority_available", False)
        result = coordinator.execute_action(request_for(coordinator, adapter))
        self.assertEqual(DispatchState.NOT_DISPATCHED, result.dispatch_state)
        self.assertEqual([], adapter.physical_effects)

    def test_19_adapter_runtime_session_change_exactly_before_commit(self):
        for change in ("adapter", "runtime", "session"):
            _, adapter, _, coordinator = stack()
            request = request_for(coordinator, adapter)
            if change == "adapter":
                adapter.before_commit_hook = lambda a=adapter: a.set_identity(adapter_generation="g2")
            elif change == "runtime":
                adapter.before_commit_hook = lambda a=adapter: a.set_identity(runtime_instance_id="r2")
            else:
                adapter.before_commit_hook = lambda a=adapter: a.set_identity(session_epoch="s2")
            result = coordinator.execute_action(request)
            with self.subTest(change=change):
                self.assertEqual(DispatchState.NOT_DISPATCHED, result.dispatch_state)
                self.assertEqual([], adapter.physical_effects)

    def test_20_two_mutation_requests_serialize(self):
        _, adapter, _, coordinator = stack()
        entered = threading.Event()
        release = threading.Event()
        first = request_for(coordinator, adapter, action_id="first")
        second = request_for(coordinator, adapter, action_id="second")

        def block_first() -> None:
            entered.set()
            self.assertTrue(release.wait(2))

        adapter.before_commit_hook = block_first
        results: list = []
        thread_one = threading.Thread(target=lambda: results.append(coordinator.execute_action(first)))
        thread_one.start()
        self.assertTrue(entered.wait(2))
        adapter.before_commit_hook = None
        thread_two = threading.Thread(target=lambda: results.append(coordinator.execute_action(second)))
        thread_two.start()
        self.assertTrue(thread_two.is_alive())
        release.set()
        thread_one.join(2)
        thread_two.join(2)
        self.assertFalse(thread_one.is_alive())
        self.assertFalse(thread_two.is_alive())
        self.assertEqual(2, len(adapter.physical_effects))

    def test_21_same_action_id_hash_dispatches_at_most_once(self):
        _, adapter, _, coordinator = stack()
        request = request_for(coordinator, adapter)
        first = coordinator.execute_action(request)
        second = coordinator.execute_action(request)
        self.assertEqual(ActionStatus.PASS, first.status)
        self.assertEqual(first.status, second.status)
        self.assertEqual(1, len(adapter.physical_effects))

    def test_22_same_action_id_different_hash_conflict(self):
        _, adapter, _, coordinator = stack()
        first = request_for(coordinator, adapter)
        coordinator.execute_action(first)
        conflict = request_for(coordinator, adapter, hash_override="f" * 64)
        result = coordinator.execute_action(conflict)
        self.assertEqual("REFUSED_IDEMPOTENCY_CONFLICT", result.reason_code)
        self.assertEqual(1, len(adapter.physical_effects))

    def test_23_duplicate_action_creates_no_second_reservation(self):
        _, adapter, _, coordinator = stack()
        request = request_for(coordinator, adapter)
        coordinator.execute_action(request)
        before = coordinator.runs["run-1"].budget.dimensions["max_actions"].committed
        coordinator.execute_action(request)
        after = coordinator.runs["run-1"].budget.dimensions["max_actions"].committed
        self.assertEqual((1, 1), (before, after))

    def test_24_stop_wins_dispatch_gate_no_effect(self):
        _, adapter, _, coordinator = stack()
        adapter.before_commit_hook = coordinator.stop_all
        result = coordinator.execute_action(request_for(coordinator, adapter))
        self.assertEqual(DispatchState.NOT_DISPATCHED, result.dispatch_state)
        self.assertTrue(coordinator.control_state.stop_latched)
        self.assertEqual([], adapter.physical_effects)

    def test_25_commit_wins_gate_possible_dispatch_before_stop(self):
        _, adapter, store, coordinator = stack()
        adapter.after_commit_hook = coordinator.stop_all
        request = request_for(coordinator, adapter)
        result = coordinator.execute_action(request)
        durable = store.load_action(request.action_id)
        self.assertIsNotNone(durable)
        self.assertNotEqual(DispatchState.NOT_DISPATCHED, durable.dispatch_state)
        self.assertTrue(coordinator.control_state.stop_latched)
        self.assertEqual(ActionStatus.CANCELLED, result.status)
        self.assertEqual("CANCELLED_AFTER_DISPATCH", result.reason_code)

    def test_26_stop_linearizes_while_action_waits_for_authority(self):
        _, adapter, _, coordinator = stack()
        adapter.authority_wait_hook = coordinator.stop_all
        result = coordinator.execute_action(request_for(coordinator, adapter))
        self.assertEqual(DispatchState.NOT_DISPATCHED, result.dispatch_state)
        self.assertEqual([], adapter.physical_effects)

    def test_27_durability_barrier_failure_no_effect(self):
        _, adapter, store, coordinator = stack()
        store.inject_fault("dispatch_commit", "error")
        result = coordinator.execute_action(request_for(coordinator, adapter))
        self.assertEqual(DispatchState.NOT_DISPATCHED, result.dispatch_state)
        self.assertEqual([], adapter.physical_effects)

    def test_28_durability_barrier_timeout_no_effect(self):
        _, adapter, store, coordinator = stack()
        store.inject_fault("dispatch_commit", "timeout")
        result = coordinator.execute_action(request_for(coordinator, adapter))
        self.assertEqual(DispatchState.NOT_DISPATCHED, result.dispatch_state)
        self.assertEqual([], adapter.physical_effects)

    def test_29_crash_after_durable_commit_before_effect_ambiguous(self):
        _, adapter, _, coordinator = stack()
        adapter.execution_fault = "crash_after_commit_before_effect"
        result = coordinator.execute_action(request_for(coordinator, adapter))
        self.assertEqual(ActionStatus.AMBIGUOUS, result.status)
        self.assertEqual([], adapter.physical_effects)

    def test_30_crash_after_effect_before_result_ambiguous(self):
        _, adapter, _, coordinator = stack()
        adapter.execution_fault = "crash_after_effect_before_result"
        result = coordinator.execute_action(request_for(coordinator, adapter))
        self.assertEqual(ActionStatus.AMBIGUOUS, result.status)
        self.assertEqual(1, len(adapter.physical_effects))

    def test_31_external_effect_budget_reservation_exhaustion(self):
        _, adapter, _, coordinator = stack(run_budget=budget(max_actions=0, max_movement_tiles=0))
        result = coordinator.execute_action(request_for(coordinator, adapter))
        self.assertEqual("BUDGET_EXHAUSTED", result.reason_code)
        self.assertEqual([], adapter.physical_effects)

    def test_32_external_effect_budget_arithmetic_overflow_refusal(self):
        with self.assertRaises(ValidationError):
            checked_add(MAX_U64, 1)

    def test_33_commit_atomically_moves_reserved_to_at_risk(self):
        _, adapter, _, coordinator = stack()
        observed: list[tuple[int, int]] = []

        def after_commit() -> None:
            dimension = coordinator.runs["run-1"].budget.dimensions["max_actions"]
            observed.append((dimension.reserved, dimension.at_risk))

        adapter.after_commit_hook = after_commit
        coordinator.execute_action(request_for(coordinator, adapter))
        self.assertEqual([(0, 1)], observed)

    def test_34_ambiguous_consumable_item_action_consumes_conservative_budget(self):
        _, adapter, _, coordinator = stack()
        adapter.execution_fault = "crash_after_effect_before_result"
        request = request_for(
            coordinator,
            adapter,
            kind="use_consumable",
            parameters={"consumable_key": "potion", "target": {"kind": "SELF"}, "quantity": 1},
        )
        coordinator.execute_action(request)
        dimension = coordinator.runs["run-1"].budget.dimensions["max_consumables"]
        self.assertEqual(1, dimension.uncertain)

    def test_35_explicit_retry_only_after_proven_not_dispatched_uses_new_id(self):
        _, adapter, _, coordinator = stack()
        adapter.authority_available = False
        old = request_for(coordinator, adapter, action_id="old", attempt_index=1)
        first = coordinator.execute_action(old)
        self.assertEqual(DispatchState.NOT_DISPATCHED, first.dispatch_state)
        adapter.authority_available = True
        new = request_for(coordinator, adapter, action_id="new", attempt_index=2)
        retried = coordinator.retry_action("old", new)
        self.assertEqual(ActionStatus.PASS, retried.status)
        bad = coordinator.retry_action("new", new)
        self.assertEqual(ActionStatus.REFUSED, bad.status)

    def test_36_pause_resume_identity_change_refuses_pending_mutation(self):
        _, adapter, _, coordinator = stack()
        coordinator.pause_run("run-1")
        adapter.set_identity(session_epoch="changed")
        self.assertFalse(coordinator.resume_run("run-1"))

    def test_37_wait_timeout_and_cancellation(self):
        _, _, _, coordinator = stack()
        token = CancellationToken()
        self.assertEqual("TIMEOUT", coordinator.wait_until("run-1", lambda: False, timeout_ms=2))
        token.cancel()
        self.assertEqual("CANCELLED", coordinator.wait_until("run-1", lambda: False, timeout_ms=2, token=token))

    def test_38_before_commit_versus_after_commit_cancellation_classification(self):
        _, adapter, _, coordinator = stack()
        token = CancellationToken()
        token.cancel()
        before = coordinator.execute_action(request_for(coordinator, adapter, action_id="before"), token=token)
        self.assertEqual(LifecycleState.CANCELLED_BEFORE_DISPATCH, before.lifecycle_state)
        _, adapter_two, _, coordinator_two = stack()
        token_two = CancellationToken()
        adapter_two.after_commit_hook = token_two.cancel
        after = coordinator_two.execute_action(request_for(coordinator_two, adapter_two, action_id="after"), token=token_two)
        self.assertEqual(LifecycleState.CANCELLED_AFTER_DISPATCH, after.lifecycle_state)

    def test_39_multi_clock_source_ingest_order_stays_distinct(self):
        clock = ManualClock(100)
        recorder = Recorder(clock, backend_epoch="b", adapter_id="a", adapter_generation="g")
        event = recorder.record_event(kind="STATE", payload={"ok": True}, source_timestamp=999, source_clock_domain="server")
        self.assertEqual(100, event.ingested_monotonic_ns)
        self.assertEqual(999, event.source_timestamp)
        self.assertEqual("server", event.source_clock_domain)

    def test_40_ingestion_order_cannot_claim_causal_order(self):
        recorder = Recorder(ManualClock(), backend_epoch="b", adapter_id="a", adapter_generation="g")
        event = recorder.record_event(kind="STATE", payload={"x": 1}, ordering_confidence=OrderingConfidence.UNKNOWN)
        self.assertEqual("INGESTION_ORDER_ONLY", recorder.causal_order_claim(event))

    def test_41_late_event_cannot_rewrite_terminal_result(self):
        recorder = Recorder(ManualClock(), backend_epoch="b", adapter_id="a", adapter_generation="g")
        recorder.set_terminal_result("action", "CONFIRMED")
        recorder.finalize()
        late = recorder.record_event(kind="RESULT", payload={"state": "late"})
        self.assertTrue(late.late)
        self.assertEqual("CONFIRMED", recorder.terminal_results["action"])
        with self.assertRaises(ValidationError):
            recorder.set_terminal_result("action", "FAILED")

    def test_42_causal_fields_preserve_supplied_track_a_metadata(self):
        recorder = Recorder(ManualClock(), backend_epoch="b", adapter_id="a", adapter_generation="g")
        payload = {
            "message_direction": "SERVER_TO_CLIENT",
            "message_sequence": 7,
            "message_type": "KnownType",
            "connection_lane": "game",
            "thread_id": 3,
            "handler": "handler",
            "runtime_object": "object",
            "object_instance_epoch": "epoch",
            "before_state_hash": "a",
            "after_state_hash": "b",
            "semantic_delta": {"hp": -1},
            "evidence_ref": "evidence:test",
        }
        event = recorder.record_event(kind="TRACE", payload=payload, stimulus_id="stimulus")
        self.assertEqual(payload, event.payload)
        self.assertEqual("stimulus", event.stimulus_id)

    def test_43_secret_shaped_event_rejected_before_object_creation(self):
        recorder = Recorder(ManualClock(), backend_epoch="b", adapter_id="a", adapter_generation="g")
        with self.assertRaises(PrivacyError):
            recorder.record_event(kind="ERROR", payload={"password": "secret"})
        self.assertEqual([], recorder.events)

    def test_44_unsanitized_exception_text_excluded_from_safe_message(self):
        error = safe_error("STATIC", safe_message="operation failed", exception=RuntimeError("password=hunter2"))
        self.assertEqual({"code": "STATIC", "safe_message": "operation failed"}, error)
        self.assertNotIn("hunter2", repr(error))

    def test_45_environment_shaped_secret_excluded(self):
        recorder = Recorder(ManualClock(), backend_epoch="b", adapter_id="a", adapter_generation="g")
        with self.assertRaises(PrivacyError):
            recorder.record_event(kind="ERROR", payload={"message": "OPENAI_API_KEY=secretvalue"})

    def test_46_screenshot_safe_quarantined_rejected_states(self):
        safe = construct_screenshot("safe", b"pixels", known_safe=True)
        quarantine = construct_screenshot("unknown", b"pixels")
        rejected = construct_screenshot("auth", b"pixels", contains_auth_or_secret=True)
        self.assertEqual(("SAFE", "QUARANTINED", "REJECTED"), (safe.disposition.value, quarantine.disposition.value, rejected.disposition.value))
        self.assertIsNone(rejected.normal_artifact_bytes)
        self.assertIsNone(rejected.quarantine_bytes)

    def test_47_passive_capture_refuses_invasive_enablement(self):
        adapter = FakeAdapter(ManualClock())
        adapter.capture_requires_invasive.add("state")
        with self.assertRaises(ValidationError):
            adapter.capture_start({"state": True})

    def test_48_emergency_stop_cannot_create_gameplay_process_mutation(self):
        adapter = FakeAdapter(ManualClock())
        before = len(adapter.physical_effects)
        result = adapter.emergency_stop()
        self.assertEqual(0, result["new_external_effects"])
        self.assertEqual(before, len(adapter.physical_effects))

    def test_49_artifact_crash_remains_incomplete(self):
        artifacts, recorder, run_id = artifact_fixture()
        artifacts.mark_crash(run_id)
        result = artifacts.finalize(
            run_id,
            recorder=recorder,
            action_results={},
            requested_status="PASS",
            final_control_generation=0,
            budget_summary={},
        )
        self.assertEqual("INCOMPLETE", result["status"])

    def test_50_finalized_result_not_silently_rewritten(self):
        artifacts, recorder, run_id = artifact_fixture()
        first = artifacts.finalize(
            run_id,
            recorder=recorder,
            action_results={},
            requested_status="PASS",
            final_control_generation=0,
            budget_summary={},
        )
        second = artifacts.finalize(
            run_id,
            recorder=recorder,
            action_results={},
            requested_status="FAIL",
            final_control_generation=99,
            budget_summary={},
        )
        self.assertEqual(first, second)
        self.assertEqual("PASS", second["status"])

    def test_51_fake_one_step_experiment_success(self):
        scenario = parse_and_validate(json.dumps(scenario_dict()))
        clock, adapter, _, coordinator = stack(start_run=False)
        recorder = Recorder(clock, backend_epoch=coordinator.backend_epoch, adapter_id=adapter.identity().adapter_id, adapter_generation=adapter.identity().adapter_generation)
        engine = ScenarioEngine(adapter=adapter, coordinator=coordinator, artifacts=ArtifactStore(), recorder=recorder)
        result = engine.run(scenario, run_id="one-step")
        self.assertEqual("PASS", result.status)
        self.assertEqual(1, len(adapter.physical_effects))

    def test_52_no_operator_facing_adapter_bypass_interface_exists(self):
        import tools.tibia_re_control_center as package

        exported = set(package.__all__)
        self.assertNotIn("FakeAdapter", exported)
        self.assertFalse(any("official" in name.lower() for name in exported))
        root = Path("tools/tibia_re_control_center")
        forbidden = ("subprocess", "socket", "requests", "urllib.request", "os.system", "Popen")
        package_a_core = (
            "artifact.py", "canonical.py", "comparison.py", "engine.py", "execution.py",
            "fake.py", "model.py", "recorder.py", "scenario.py", "store.py",
        )
        text = "\n".join((root / name).read_text(encoding="utf-8") for name in package_a_core)
        self.assertFalse(any(token in text for token in forbidden))

    def test_53_typed_budget_abort_fieldpath_destination_reject_free_form(self):
        with self.assertRaises(ValidationError):
            SideEffectBudget.from_mapping({"max_runtime_seconds": 1})
        with self.assertRaises(ValidationError):
            validate_abort_condition({"condition": {"field": "player.hp", "op": "EQ", "value": 1, "unknown_policy": "WAIT"}, "reason_code": "TIMEOUT"})
        with self.assertRaises(ValidationError):
            validate_predicate({"field": "player[0].hp", "op": "EXISTS"})
        with self.assertRaises(ValidationError):
            validate_action_parameters("move_item", {"item": {"kind": "INVENTORY_SLOT", "inventory_slot": "bag"}, "destination": {"kind": "RAW_COORDINATE", "x": 1}, "count": 1})

    def test_54_confirmed_terminal_callback_cannot_rewrite_or_redispatch(self):
        _, adapter, store, coordinator = stack()
        request = request_for(coordinator, adapter)
        coordinator.execute_action(request)
        self.assertFalse(coordinator.accept_callback(
            request.action_id,
            backend_epoch=coordinator.backend_epoch,
            control_generation=coordinator.control_generation,
            lifecycle_state=LifecycleState.FAILED_AFTER_DISPATCH,
        ))
        self.assertEqual(LifecycleState.CONFIRMED, store.load_action(request.action_id).lifecycle_state)
        coordinator.execute_action(request)
        self.assertEqual(1, len(adapter.physical_effects))

    def test_55_durable_stop_control_state_survives_restart(self):
        clock, _, store, first = stack(backend_epoch="one")
        self.assertTrue(first.stop_all())
        second = MutationCoordinator(FakeAdapter(clock), store, clock, backend_epoch="two")
        self.assertTrue(second.control_state.stop_latched)
        self.assertFalse(second.mutation_admission_allowed())

    def test_56_reset_durability_failure_leaves_stop_recovery_blocking(self):
        _, _, store, coordinator = stack()
        coordinator.stop_all()
        store.inject_fault("reset", "error")
        self.assertFalse(coordinator.reset_stop())
        self.assertTrue(coordinator.in_memory_stop)
        self.assertFalse(coordinator.mutation_admission_allowed())

    def test_57_backend_active_marker_must_be_durable_before_mutation_admission(self):
        store = DeterministicDurableStore()
        store.inject_fault("backend_activate", "error")
        clock = ManualClock()
        coordinator = MutationCoordinator(FakeAdapter(clock), store, clock, backend_epoch="bad")
        self.assertFalse(coordinator.mutation_admission_allowed())
        self.assertEqual("DurabilityError", coordinator.activation_error)

    def test_58_prior_uncleared_active_backend_forces_recovery_required(self):
        clock, _, store, _ = stack(backend_epoch="one")
        second = MutationCoordinator(FakeAdapter(clock), store, clock, backend_epoch="two")
        self.assertTrue(second.control_state.recovery_required)
        self.assertFalse(second.mutation_admission_allowed())

    def test_59_stop_persistence_failure_then_crash_cannot_reopen(self):
        clock, _, store, first = stack(backend_epoch="one")
        store.inject_fault("stop", "error")
        self.assertFalse(first.stop_all())
        second = MutationCoordinator(FakeAdapter(clock), store, clock, backend_epoch="two")
        self.assertTrue(second.control_state.recovery_required)
        self.assertFalse(second.mutation_admission_allowed())

    def test_60_clean_shutdown_marker_failure_conservative_recovery_next_start(self):
        clock, _, store, first = stack(backend_epoch="one")
        store.inject_fault("clean_shutdown", "error")
        self.assertFalse(first.clean_shutdown())
        second = MutationCoordinator(FakeAdapter(clock), store, clock, backend_epoch="two")
        self.assertTrue(second.control_state.recovery_required)

    def test_61_missing_corrupt_initialized_control_state_fail_closed(self):
        _, _, store, _ = stack()
        store.corrupt_control_state()
        with self.assertRaises(ValidationError):
            MutationCoordinator(FakeAdapter(ManualClock()), store, ManualClock(), backend_epoch="two")

    def test_62_runtime_deadline_overflow_fails_closed(self):
        clock = ManualClock(MAX_U64 - 10)
        adapter = FakeAdapter(clock)
        store = DeterministicDurableStore()
        coordinator = MutationCoordinator(adapter, store, clock, backend_epoch="overflow")
        with self.assertRaises(ValidationError):
            coordinator.start_run("overflow-run", budget(max_runtime_seconds=1))

    def test_63_runtime_deadline_expiry_while_waiting_prevents_later_dispatch(self):
        clock, adapter, _, coordinator = stack(run_budget=budget(max_runtime_seconds=1))
        self.assertEqual("TIMEOUT", coordinator.wait_until("run-1", lambda: False, timeout_ms=2000))
        result = coordinator.execute_action(request_for(coordinator, adapter))
        self.assertEqual(LifecycleState.TIMED_OUT_BEFORE_DISPATCH, result.lifecycle_state)
        self.assertEqual([], adapter.physical_effects)
        self.assertGreaterEqual(clock.now_ns(), 1_000_000_000)

    def test_64_pause_does_not_extend_runtime_deadline(self):
        clock, _adapter, _, coordinator = stack(run_budget=budget(max_runtime_seconds=1))
        original = coordinator.runs["run-1"].budget.deadline_monotonic_ns
        coordinator.pause_run("run-1")
        clock.advance_seconds(2)
        self.assertFalse(coordinator.resume_run("run-1"))
        self.assertEqual(original, coordinator.runs["run-1"].budget.deadline_monotonic_ns)

    def test_65_restart_recovery_does_not_grant_fresh_runtime_deadline(self):
        clock, _, store, first = stack(backend_epoch="one", run_budget=budget(max_runtime_seconds=1))
        original = first.runs["run-1"].budget.deadline_monotonic_ns
        clock.advance_seconds(2)
        second_adapter = FakeAdapter(clock)
        second = MutationCoordinator(second_adapter, store, clock, backend_epoch="two")
        recovered = second.recover_run("run-1")
        self.assertEqual(original, recovered.budget.deadline_monotonic_ns)
        self.assertGreaterEqual(clock.now_ns(), recovered.budget.deadline_monotonic_ns)


class PackageAAdditionalContractTests(unittest.TestCase):
    def test_contract_major_negotiation_fail_closed(self):
        self.assertEqual(1, negotiate_major(1, [1], contract_name="scenario"))
        with self.assertRaises(ValidationError):
            negotiate_major(1, [2], contract_name="scenario")

    def test_engine_contract_major_negotiation_fail_closed(self):
        clock, adapter, _, coordinator = stack(start_run=False)
        engine = ScenarioEngine(
            adapter=adapter,
            coordinator=coordinator,
            artifacts=ArtifactStore(),
            recorder=Recorder(clock, backend_epoch=coordinator.backend_epoch, adapter_id="fake", adapter_generation="g"),
            supported_contracts={"adapter": [1], "execution": [1], "scenario": [2], "artifact": [1]},
        )
        with self.assertRaises(ValidationError):
            engine.negotiate_contracts()

    def test_read_only_concurrency_requires_explicit_safe_fixture(self):
        clock = ManualClock()
        adapter = FakeAdapter(clock, concurrency_safe_reads=False)
        coordinator = MutationCoordinator(adapter, DeterministicDurableStore(), clock)
        coordinator.start_run("read-one", budget(), mutation_capable=False)
        with self.assertRaises(ValidationError):
            coordinator.start_run("read-two", budget(), mutation_capable=False)

    def test_jcs_utf16_property_order_vector(self):
        self.assertEqual('{"a":2,"b":1}', jcs_dumps({"b": 1, "a": 2}))

    def test_comparison_exact_match_and_mismatch(self):
        profile = ComparisonProfile("p", "1", (ProfileField("player.hp", ComparisonClass.EXACT),))
        pair = CheckpointPair("c", "r", "c")
        reference = {("r", "player.hp"): NormalizedObservation("player.hp", "c", ObservationStatus.OBSERVED, 100)}
        candidate = {("c", "player.hp"): NormalizedObservation("player.hp", "c", ObservationStatus.OBSERVED, 100)}
        match = compare_runs(
            comparison_id="x", profile=profile, reference_run_id="r", candidate_run_id="c",
            scenario_id="s", reference_scenario_hash="h", candidate_scenario_hash="h",
            checkpoint_pairs=[pair], reference_observations=reference, candidate_observations=candidate,
        )
        self.assertEqual(ComparisonStatus.PASS, match.status)
        candidate[("c", "player.hp")] = NormalizedObservation("player.hp", "c", ObservationStatus.OBSERVED, 99)
        mismatch = compare_runs(
            comparison_id="x2", profile=profile, reference_run_id="r", candidate_run_id="c",
            scenario_id="s", reference_scenario_hash="h", candidate_scenario_hash="h",
            checkpoint_pairs=[pair], reference_observations=reference, candidate_observations=candidate,
        )
        self.assertEqual(ComparisonStatus.FAIL, mismatch.status)

    def test_comparison_coverage_gap_not_failure(self):
        profile = ComparisonProfile("p", "1", (ProfileField("player.hp", ComparisonClass.EXACT),))
        result = compare_runs(
            comparison_id="x", profile=profile, reference_run_id="r", candidate_run_id="c",
            scenario_id="s", reference_scenario_hash="h", candidate_scenario_hash="h",
            checkpoint_pairs=[CheckpointPair("c", "r", "c")],
            reference_observations={
                ("r", "player.hp"): NormalizedObservation("player.hp", "c", ObservationStatus.UNKNOWN)
            },
            candidate_observations={
                ("c", "player.hp"): NormalizedObservation("player.hp", "c", ObservationStatus.OBSERVED, 99)
            },
        )
        self.assertEqual(ComparisonStatus.COVERAGE_INCOMPLETE, result.status)

    def test_comparison_order_set_tolerance_and_scenario_mismatch(self):
        profile = ComparisonProfile("p", "1", (
            ProfileField("conditions", ComparisonClass.SET_EQUIVALENT),
            ProfileField("containers", ComparisonClass.ORDERED_EQUIVALENT),
            ProfileField("latency", ComparisonClass.TOLERANCE, absolute_tolerance=5),
        ))
        pair = CheckpointPair("cp", "r", "c")
        reference = {
            ("r", "conditions"): NormalizedObservation("conditions", "cp", ObservationStatus.OBSERVED, ["a", "b"]),
            ("r", "containers"): NormalizedObservation("containers", "cp", ObservationStatus.OBSERVED, [1, 2]),
            ("r", "latency"): NormalizedObservation("latency", "cp", ObservationStatus.OBSERVED, 100),
        }
        candidate = {
            ("c", "conditions"): NormalizedObservation("conditions", "cp", ObservationStatus.OBSERVED, ["b", "a"]),
            ("c", "containers"): NormalizedObservation("containers", "cp", ObservationStatus.OBSERVED, [1, 2]),
            ("c", "latency"): NormalizedObservation("latency", "cp", ObservationStatus.OBSERVED, 104),
        }
        good = compare_runs(
            comparison_id="x", profile=profile, reference_run_id="r", candidate_run_id="c",
            scenario_id="s", reference_scenario_hash="h", candidate_scenario_hash="h",
            checkpoint_pairs=[pair], reference_observations=reference, candidate_observations=candidate,
        )
        self.assertEqual(ComparisonStatus.PASS, good.status)
        bad = compare_runs(
            comparison_id="y", profile=profile, reference_run_id="r", candidate_run_id="c",
            scenario_id="s", reference_scenario_hash="h1", candidate_scenario_hash="h2",
            checkpoint_pairs=[pair], reference_observations=reference, candidate_observations=candidate,
        )
        self.assertEqual(ComparisonStatus.INVALID_INPUT, bad.status)

    def test_artifact_report_contradiction_rejected(self):
        artifacts, recorder, run_id = artifact_fixture()
        artifacts.finalize(run_id, recorder=recorder, action_results={}, requested_status="PASS", final_control_generation=0, budget_summary={})
        with self.assertRaises(ValidationError):
            artifacts.validate_report_status(run_id, "FAIL")

    def test_artifact_supplement_cannot_rewrite_result(self):
        artifacts, recorder, run_id = artifact_fixture()
        artifacts.finalize(run_id, recorder=recorder, action_results={}, requested_status="PASS", final_control_generation=0, budget_summary={})
        with self.assertRaises(ValidationError):
            artifacts.add_supplement(run_id, "s1", {"result.json": b"{}"})

    def test_artifact_hashes_match_exact_final_bytes(self):
        artifacts, recorder, run_id = artifact_fixture()
        artifacts.finalize(run_id, recorder=recorder, action_results={}, requested_status="PASS", final_control_generation=0, budget_summary={})
        self.assertTrue(artifacts.validate_hashes(run_id))

    def test_policy_boundary_types_carry_no_authority_handle(self):
        fields = set(inspect.signature(PolicyActionProposal).parameters)
        self.assertEqual({"kind", "parameters", "timeout_ms", "requested_budget_ceiling"}, fields)
        self.assertFalse(any("authority" in field or "adapter" in field for field in fields))


if __name__ == "__main__":
    unittest.main()
