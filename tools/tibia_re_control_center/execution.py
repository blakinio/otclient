from __future__ import annotations

import copy
import threading
import uuid
from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Any

from .fake import FakeAdapter, ManualClock
from .model import (
    EFFECT_DIMENSIONS,
    MAX_U64,
    ActionLedgerRecord,
    ActionRequest,
    ActionResult,
    ActionStatus,
    Authority,
    BudgetDimension,
    BudgetLedger,
    Confirmation,
    ControlState,
    DispatchState,
    DurabilityError,
    DurabilityTimeout,
    LifecycleState,
    SideEffectBudget,
    SimulatedCrash,
    ValidationError,
    checked_add,
    checked_mul,
)
from .scenario import action_request_hash
from .store import DeterministicDurableStore

_MISSING = object()


def _freeze_semantic_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze_semantic_value(child) for key, child in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_semantic_value(child) for child in value)
    return value


@dataclass
class CancellationToken:
    cancelled: bool = False

    def cancel(self) -> None:
        self.cancelled = True


@dataclass
class RunState:
    run_id: str
    budget: BudgetLedger
    expected_adapter_generation: str
    expected_runtime_instance_id: str | None
    expected_session_epoch: str | None
    mutation_capable: bool
    paused: bool = False
    cancelled: bool = False


class _OneShotCommit:
    def __init__(self, commit: Callable[[], bool]) -> None:
        self._commit = commit
        self.called = False
        self.result = False

    def __call__(self) -> bool:
        if self.called:
            return False
        self.called = True
        self.result = self._commit()
        return self.result


class MutationCoordinator:
    def __init__(
        self,
        adapter: FakeAdapter,
        store: DeterministicDurableStore,
        clock: ManualClock,
        *,
        backend_epoch: str | None = None,
    ) -> None:
        self.adapter = adapter
        self.store = store
        self.clock = clock
        self.backend_epoch = backend_epoch or f"backend-{uuid.uuid4().hex}"
        self.dispatch_gate = threading.RLock()
        self.control_transition_lock = threading.RLock()
        self.run_admission_lock = threading.RLock()
        self.mutation_execution_lock = threading.Lock()
        self.stop_operation_lock = threading.RLock()
        self.runs: dict[str, RunState] = {}
        self.results: dict[str, ActionResult] = {}
        self.active_mutation_run_id: str | None = None
        self.in_memory_stop = False
        self.mutation_disabled = False
        self.stop_durability_unresolved = False
        self.stop_cleanup_in_progress = False
        self.activation_error: str | None = None
        self.control_state = self._activate_backend()

    def _new_control_state(
        self,
        *,
        stop_latched: bool,
        recovery_required: bool,
        generation: int,
        transition_id: str,
        reason_code: str,
        active_backend_epoch: str | None,
    ) -> ControlState:
        return ControlState(
            stop_latched=stop_latched,
            recovery_required=recovery_required,
            control_generation=generation,
            transition_id=transition_id,
            active_backend_epoch=active_backend_epoch,
            written_by_backend_epoch=self.backend_epoch,
            reason_code=reason_code,
            updated_monotonic_ns=self.clock.now_ns(),
        )

    def _activate_backend(self) -> ControlState:
        try:
            prior = self.store.load_control_state()
        except ValidationError:
            self.in_memory_stop = True
            self.mutation_disabled = True
            raise
        if prior is None:
            next_state = self._new_control_state(
                stop_latched=False,
                recovery_required=False,
                generation=0,
                transition_id=f"backend-start:{self.backend_epoch}",
                reason_code="BACKEND_INITIALIZED",
                active_backend_epoch=self.backend_epoch,
            )
        else:
            unclean = prior.active_backend_epoch is not None and prior.active_backend_epoch != self.backend_epoch
            next_state = self._new_control_state(
                stop_latched=prior.stop_latched,
                recovery_required=prior.recovery_required or unclean,
                generation=0,
                transition_id=f"backend-start:{self.backend_epoch}",
                reason_code="UNCLEAN_BACKEND_RECOVERY_REQUIRED" if unclean else "BACKEND_STARTED",
                active_backend_epoch=self.backend_epoch,
            )
        try:
            self.store.write_control_state(next_state, operation="backend_activate")
        except (DurabilityError, DurabilityTimeout) as exc:
            self.activation_error = type(exc).__name__
            self.in_memory_stop = True
            self.mutation_disabled = True
            return replace(
                next_state,
                stop_latched=True,
                recovery_required=True,
                reason_code="BACKEND_ACTIVE_MARKER_DURABILITY_FAILED",
            )
        self.in_memory_stop = next_state.stop_latched
        self.mutation_disabled = bool(next_state.stop_latched or next_state.recovery_required)
        return next_state

    @property
    def control_generation(self) -> int:
        return self.control_state.control_generation

    def mutation_admission_allowed(self) -> bool:
        return not (
            self.mutation_disabled
            or self.in_memory_stop
            or self.stop_cleanup_in_progress
            or self.control_state.stop_latched
            or self.control_state.recovery_required
        )

    def _derive_deadline(self, started_ns: int, max_runtime_seconds: int) -> int:
        duration = checked_mul(
            max_runtime_seconds,
            1_000_000_000,
            maximum=MAX_U64,
            field_name="runtime_deadline",
        )
        return checked_add(started_ns, duration, maximum=MAX_U64, field_name="runtime_deadline")

    def start_run(self, run_id: str, budget: SideEffectBudget, *, mutation_capable: bool = True) -> RunState:
        with self.run_admission_lock:
            if run_id in self.runs:
                return self.runs[run_id]
            if mutation_capable:
                if not self.mutation_admission_allowed():
                    raise ValidationError("MUTATION_LOCALLY_BLOCKED", "STOP/recovery/activation state blocks mutation admission")
                if self.active_mutation_run_id is not None:
                    raise ValidationError("REFUSED_MUTATION_RUN_CONFLICT", "another mutation-capable run owns this adapter")
            elif self.runs and not self.adapter.concurrency_safe_reads:
                raise ValidationError("READ_CONCURRENCY_UNPROVEN", "read-only concurrency is not proven safe")
            started = self.clock.now_ns()
            deadline = self._derive_deadline(started, budget.max_runtime_seconds)
            self.store.persist_run_activation(run_id, started, deadline)
            ledger = BudgetLedger(
                run_id=run_id,
                limit_seconds=budget.max_runtime_seconds,
                started_monotonic_ns=started,
                deadline_monotonic_ns=deadline,
                dimensions={name: BudgetDimension(limit=value) for name, value in budget.effect_limits().items()},
                updated_monotonic_ns=started,
            )
            self.store.write_budget(ledger, operation="budget_init")
            identity = self.adapter.identity()
            self.store.write_recovery(
                run_id,
                {
                    "backend_epoch": self.backend_epoch,
                    "control_generation": self.control_generation,
                    "adapter_generation": identity.adapter_generation,
                    "runtime_instance_id": identity.runtime_instance_id,
                    "session_epoch": identity.session_epoch,
                    "mutation_capable": mutation_capable,
                },
            )
            run = RunState(run_id, ledger, identity.adapter_generation, identity.runtime_instance_id, identity.session_epoch, mutation_capable)
            self.runs[run_id] = run
            if mutation_capable:
                self.active_mutation_run_id = run_id
            return run

    def recover_run(self, run_id: str, *, mutation_capable: bool = True) -> RunState:
        with self.run_admission_lock:
            activation = self.store.load_run_activation(run_id)
            ledger = self.store.load_budget(run_id)
            recovery = self.store.load_recovery(run_id)
            if activation is None or ledger is None or recovery is None:
                raise ValidationError("RECOVERY_STATE_MISSING", "run recovery requires original activation, budget, and recovery fences")
            if (ledger.started_monotonic_ns, ledger.deadline_monotonic_ns) != activation:
                raise ValidationError("RECOVERY_STATE_CONTRADICTORY", "runtime activation/deadline contradict durable budget state")
            if bool(recovery.get("mutation_capable")) != mutation_capable:
                raise ValidationError("RECOVERY_AUTHORITY_CONTRADICTION", "run recovery cannot change mutation capability")
            identity = self.adapter.identity()
            origin_matches = (
                recovery.get("backend_epoch") == self.backend_epoch
                and recovery.get("control_generation") == self.control_generation
                and recovery.get("adapter_generation") == identity.adapter_generation
                and recovery.get("runtime_instance_id") == identity.runtime_instance_id
                and recovery.get("session_epoch") == identity.session_epoch
            )
            run = RunState(
                run_id,
                ledger,
                str(recovery.get("adapter_generation")),
                recovery.get("runtime_instance_id"),
                recovery.get("session_epoch"),
                mutation_capable,
                cancelled=bool(mutation_capable and (not origin_matches or not self.mutation_admission_allowed())),
            )
            self.runs[run_id] = run
            return run
    def finish_run(self, run_id: str) -> None:
        with self.run_admission_lock:
            if self.active_mutation_run_id == run_id:
                self.active_mutation_run_id = None
            self.runs.pop(run_id, None)

    def _run(self, run_id: str) -> RunState:
        try:
            return self.runs[run_id]
        except KeyError as exc:
            raise ValidationError("RUN_NOT_ACTIVE", "run is not active in this backend") from exc

    def _deadline_expired(self, run: RunState) -> bool:
        expired = self.clock.now_ns() >= run.budget.deadline_monotonic_ns
        if expired and not run.budget.expired:
            run.budget.expired = True
            run.budget.updated_monotonic_ns = self.clock.now_ns()
            self.store.write_budget(run.budget, operation="budget_expiry")
        return expired

    def acquire_mutation_run(self, run_id: str) -> None:
        with self.run_admission_lock:
            run = self._run(run_id)
            if not run.mutation_capable:
                raise ValidationError("RUN_READ_ONLY", "read-only run cannot acquire mutation ownership")
            if run.cancelled:
                raise ValidationError("RUN_CANCELLED", "cancelled/recovered mutation run cannot reacquire ownership")
            identity = self.adapter.identity()
            if (
                identity.adapter_generation != run.expected_adapter_generation
                or identity.runtime_instance_id != run.expected_runtime_instance_id
                or identity.session_epoch != run.expected_session_epoch
            ):
                raise ValidationError("RUN_IDENTITY_FENCE_MISMATCH", "run identity fence no longer matches the adapter")
            if not self.mutation_admission_allowed():
                raise ValidationError("MUTATION_LOCALLY_BLOCKED", "local safety state blocks mutation ownership")
            if self.active_mutation_run_id not in {None, run_id}:
                raise ValidationError("REFUSED_MUTATION_RUN_CONFLICT", "another mutation run owns this adapter")
            self.active_mutation_run_id = run_id

    def _check_reservation_fit(self, ledger: BudgetLedger, request: ActionRequest) -> None:
        for name in EFFECT_DIMENSIONS:
            amount = getattr(request.effect_bound, name)
            if amount > ledger.dimensions[name].available():
                raise ValidationError("BUDGET_EXHAUSTED", f"external-effect budget exhausted for {name}", name)

    def _reserve(self, run: RunState, request: ActionRequest) -> ActionLedgerRecord:
        existing = self.store.load_action(request.action_id)
        if existing is not None:
            if existing.action_request_hash != request.action_request_hash:
                raise ValidationError("REFUSED_IDEMPOTENCY_CONFLICT", "same action_id was submitted with a different semantic hash")
            return existing
        self._check_reservation_fit(run.budget, request)
        previous_budget = run.budget.clone()
        next_budget = run.budget.clone()
        for name in EFFECT_DIMENSIONS:
            amount = getattr(request.effect_bound, name)
            dimension = next_budget.dimensions[name]
            dimension.reserved = checked_add(dimension.reserved, amount, maximum=dimension.limit, field_name=name)
        next_budget.reservations[request.action_id] = request.effect_bound
        next_budget.updated_monotonic_ns = self.clock.now_ns()
        record = ActionLedgerRecord(
            action_id=request.action_id,
            action_request_hash=request.action_request_hash,
            run_id=request.run_id,
            step_id=request.step_id,
            attempt_index=request.attempt_index,
            lifecycle_state=LifecycleState.RESERVED,
            dispatch_state=DispatchState.NOT_DISPATCHED,
            backend_epoch=self.backend_epoch,
            control_generation=self.control_generation,
            adapter_id=self.adapter.identity().adapter_id,
            adapter_generation=request.dispatch_fence.expected_adapter_generation,
            runtime_instance_id=request.dispatch_fence.expected_runtime_instance_id,
            session_epoch=request.dispatch_fence.expected_session_epoch,
            effect_bound=request.effect_bound,
            created_monotonic_ns=self.clock.now_ns(),
            updated_monotonic_ns=self.clock.now_ns(),
        )
        durable_record, durable_budget, accepted = self.store.atomic_reserve_action(
            record,
            previous_budget,
            next_budget,
        )
        run.budget = durable_budget
        return record if accepted else durable_record

    def _release_reservation(self, run: RunState, request: ActionRequest) -> None:
        if request.action_id not in run.budget.reservations:
            return
        next_budget = run.budget.clone()
        bound = next_budget.reservations.pop(request.action_id)
        for name in EFFECT_DIMENSIONS:
            amount = getattr(bound, name)
            dimension = next_budget.dimensions[name]
            if amount > dimension.reserved:
                raise ValidationError("BUDGET_CONTRADICTION", "reservation release exceeds reserved budget")
            dimension.reserved -= amount
        next_budget.updated_monotonic_ns = self.clock.now_ns()
        self.store.write_budget(next_budget, operation="budget_release")
        run.budget = next_budget

    def _move_reserved_to_at_risk(self, ledger: BudgetLedger, action_id: str) -> BudgetLedger:
        if action_id not in ledger.reservations:
            raise ValidationError("RESERVATION_MISSING", "dispatch commit requires a current budget reservation")
        next_budget = ledger.clone()
        bound = next_budget.reservations.pop(action_id)
        for name in EFFECT_DIMENSIONS:
            amount = getattr(bound, name)
            dimension = next_budget.dimensions[name]
            if amount > dimension.reserved:
                raise ValidationError("BUDGET_CONTRADICTION", "dispatch reservation contradicts budget ledger")
            dimension.reserved -= amount
            dimension.at_risk = checked_add(dimension.at_risk, amount, maximum=dimension.limit, field_name=name)
        next_budget.updated_monotonic_ns = self.clock.now_ns()
        return next_budget

    def _reconcile_budget(self, run: RunState, request: ActionRequest, *, outcome: str) -> BudgetLedger:
        next_budget = run.budget.clone()
        for name in EFFECT_DIMENSIONS:
            amount = getattr(request.effect_bound, name)
            dimension = next_budget.dimensions[name]
            if amount > dimension.at_risk:
                raise ValidationError("BUDGET_CONTRADICTION", "reconciliation exceeds at-risk budget")
            dimension.at_risk -= amount
            if outcome == "confirmed":
                dimension.committed = checked_add(dimension.committed, amount, maximum=dimension.limit, field_name=name)
            elif outcome == "ambiguous":
                dimension.uncertain = checked_add(dimension.uncertain, amount, maximum=dimension.limit, field_name=name)
            elif outcome != "no_effect":
                raise ValueError("unsupported reconciliation outcome")
        next_budget.updated_monotonic_ns = self.clock.now_ns()
        return next_budget

    def _make_result(
        self,
        request: ActionRequest,
        state: LifecycleState,
        status: ActionStatus,
        dispatch: DispatchState,
        *,
        confirmation: Confirmation = Confirmation.UNKNOWN,
        reason_code: str | None = None,
    ) -> ActionResult:
        identity = self.adapter.identity()
        return ActionResult(
            action_id=request.action_id,
            lifecycle_state=state,
            status=status,
            dispatch_state=dispatch,
            authoritative_confirmation=confirmation,
            backend_epoch=self.backend_epoch,
            control_generation=self.control_generation,
            adapter_generation=identity.adapter_generation,
            runtime_instance_id=identity.runtime_instance_id,
            session_epoch=identity.session_epoch,
            monotonic_started_ns=self.clock.now_ns(),
            monotonic_finished_ns=self.clock.now_ns(),
            budget_effect=request.effect_bound.as_dict(),
            reason_code=reason_code,
        )

    def _terminalize_pre_dispatch(
        self,
        run: RunState,
        request: ActionRequest,
        state: LifecycleState,
        status: ActionStatus,
        reason: str,
    ) -> ActionResult:
        try:
            self._release_reservation(run, request)
        except (DurabilityError, DurabilityTimeout):
            self.mutation_disabled = True
            reason = "BUDGET_RELEASE_DURABILITY_FAILED"
        current = self.store.load_action(request.action_id)
        if current is not None and not current.terminal:
            terminal = current.with_state(state, self.clock.now_ns(), reason_code=reason)
            try:
                self.store.write_action(terminal, operation="action_terminal")
            except (DurabilityError, DurabilityTimeout):
                self.mutation_disabled = True
        result = self._make_result(request, state, status, DispatchState.NOT_DISPATCHED, reason_code=reason)
        self.results[request.action_id] = result
        return result

    def _final_commit(
        self,
        run: RunState,
        request: ActionRequest,
        token: CancellationToken | None,
        final_commit_check: Callable[[], str | None] | None,
        final_commit_refusal_reason: list[str | None],
        action_deadline_ns: int,
    ) -> bool:
        with self.control_transition_lock, self.dispatch_gate:
            record = self.store.load_action(request.action_id)
            if record is None or record.action_request_hash != request.action_request_hash:
                return False
            if record.dispatch_state != DispatchState.NOT_DISPATCHED:
                return False
            if self.active_mutation_run_id != request.run_id:
                return False
            if token is not None and token.cancelled:
                return False
            if run.cancelled or run.paused:
                return False
            fence = request.dispatch_fence
            if fence.expected_backend_epoch != self.backend_epoch or fence.expected_control_generation != self.control_generation:
                return False
            if self.in_memory_stop or self.control_state.stop_latched or self.control_state.recovery_required or self.mutation_disabled:
                return False
            identity = self.adapter.identity()
            if identity.adapter_generation != fence.expected_adapter_generation:
                return False
            if identity.runtime_instance_id != fence.expected_runtime_instance_id:
                return False
            if identity.session_epoch != fence.expected_session_epoch:
                return False
            if self.clock.now_ns() >= action_deadline_ns:
                final_commit_refusal_reason[0] = "ACTION_TIMEOUT_EXPIRED"
                return False
            if self._deadline_expired(run):
                return False
            capability = self.adapter.capability(request.required_capability)
            if capability is None:
                return False
            if request.required_authority == Authority.MUTATION and not capability.action_supported:
                return False
            if request.required_authority == Authority.READ_ONLY and not capability.read_supported:
                return False
            if not self.adapter.current_authority(request.required_authority):
                return False
            if request.action_id not in run.budget.reservations:
                return False
            if final_commit_check is not None:
                try:
                    final_reason = final_commit_check()
                except Exception:  # noqa: BLE001 -- fail closed on any safety-hook failure
                    final_commit_refusal_reason[0] = "FINAL_COMMIT_SAFETY_CHECK_FAILED"
                    return False
                if final_reason is not None:
                    final_commit_refusal_reason[0] = final_reason
                    return False
            if self.clock.now_ns() >= action_deadline_ns:
                final_commit_refusal_reason[0] = "ACTION_TIMEOUT_EXPIRED"
                return False
            record = self.store.load_action(request.action_id)
            if record is None or record.action_request_hash != request.action_request_hash:
                return False
            if record.dispatch_state != DispatchState.NOT_DISPATCHED:
                return False
            if self.active_mutation_run_id != request.run_id:
                return False
            if token is not None and token.cancelled:
                return False
            if run.cancelled or run.paused:
                return False
            if fence.expected_backend_epoch != self.backend_epoch or fence.expected_control_generation != self.control_generation:
                return False
            if self.in_memory_stop or self.stop_cleanup_in_progress or self.control_state.stop_latched or self.control_state.recovery_required or self.mutation_disabled:
                return False
            with self.adapter.dispatch_guard(request) as (identity, capability, authority_current):
                if identity.adapter_generation != fence.expected_adapter_generation:
                    return False
                if identity.runtime_instance_id != fence.expected_runtime_instance_id:
                    return False
                if identity.session_epoch != fence.expected_session_epoch:
                    return False
                if request.required_authority != Authority.MUTATION:
                    return False
                if capability is None or not capability.action_supported or not authority_current:
                    return False
                if self._deadline_expired(run):
                    return False
                if request.action_id not in run.budget.reservations:
                    return False
                if self.clock.now_ns() >= action_deadline_ns:
                    final_commit_refusal_reason[0] = "ACTION_TIMEOUT_EXPIRED"
                    return False
                next_budget = self._move_reserved_to_at_risk(run.budget, request.action_id)
                committed = record.with_state(
                    LifecycleState.DISPATCH_COMMITTED,
                    self.clock.now_ns(),
                    dispatch_state=DispatchState.POSSIBLY_DISPATCHED,
                    backend_epoch=self.backend_epoch,
                    control_generation=self.control_generation,
                    adapter_generation=identity.adapter_generation,
                    runtime_instance_id=identity.runtime_instance_id,
                    session_epoch=identity.session_epoch,
                )
                try:
                    if not self.store.atomic_dispatch_commit(committed, next_budget):
                        return False
                except (DurabilityError, DurabilityTimeout):
                    return False
                run.budget = next_budget
                return True

    def execute_action(
        self,
        request: ActionRequest,
        *,
        token: CancellationToken | None = None,
        final_commit_check: Callable[[], str | None] | None = None,
    ) -> ActionResult:
        parameters_snapshot = copy.deepcopy(dict(request.parameters))
        request = replace(request, parameters=_freeze_semantic_value(parameters_snapshot))
        action_started_ns = self.clock.now_ns()
        action_timeout_ns = checked_mul(
            request.timeout_ms,
            1_000_000,
            maximum=MAX_U64,
            field_name="action_timeout_ns",
        )
        action_deadline_ns = checked_add(
            action_started_ns,
            action_timeout_ns,
            maximum=MAX_U64,
            field_name="action_deadline_ns",
        )
        run = self._run(request.run_id)
        canonical_request_hash = action_request_hash(
            schema_version=request.schema_version,
            run_id=request.run_id,
            step_id=request.step_id,
            attempt_index=request.attempt_index,
            kind=request.kind,
            parameters=request.parameters,
            timeout_ms=request.timeout_ms,
            required_capability=request.required_capability,
            required_authority=request.required_authority,
        )
        if canonical_request_hash != request.action_request_hash:
            return self._make_result(
                request,
                LifecycleState.REFUSED,
                ActionStatus.REFUSED,
                DispatchState.NOT_DISPATCHED,
                reason_code="REFUSED_IDEMPOTENCY_CONFLICT",
            )
        with self.mutation_execution_lock:
            existing = self.store.load_action(request.action_id)
            if existing is not None:
                if existing.action_request_hash != request.action_request_hash:
                    return self._make_result(
                        request,
                        LifecycleState.REFUSED,
                        ActionStatus.REFUSED,
                        DispatchState.NOT_DISPATCHED,
                        reason_code="REFUSED_IDEMPOTENCY_CONFLICT",
                    )
                if request.action_id in self.results:
                    return self.results[request.action_id]
                if existing.lifecycle_state == LifecycleState.CONFIRMED:
                    result = self._make_result(
                        request,
                        LifecycleState.CONFIRMED,
                        ActionStatus.PASS,
                        existing.dispatch_state,
                        confirmation=existing.authoritative_confirmation,
                    )
                    self.results[request.action_id] = result
                    return result
                if existing.dispatch_state != DispatchState.NOT_DISPATCHED:
                    result = self._make_result(
                        request,
                        LifecycleState.AMBIGUOUS,
                        ActionStatus.AMBIGUOUS,
                        DispatchState.POSSIBLY_DISPATCHED,
                        reason_code="RECOVERED_POSSIBLE_DISPATCH",
                    )
                    self.results[request.action_id] = result
                    return result
                if existing.terminal:
                    result = self._make_result(
                        request,
                        existing.lifecycle_state,
                        ActionStatus.REFUSED,
                        DispatchState.NOT_DISPATCHED,
                        reason_code=existing.reason_code,
                    )
                    self.results[request.action_id] = result
                    return result
            if request.required_authority != Authority.MUTATION:
                return self._make_result(
                    request,
                    LifecycleState.REFUSED,
                    ActionStatus.REFUSED,
                    DispatchState.NOT_DISPATCHED,
                    reason_code="MUTATION_AUTHORITY_REQUIRED",
                )
            if not self.adapter.allow_mutation:
                return self._make_result(
                    request,
                    LifecycleState.REFUSED,
                    ActionStatus.REFUSED,
                    DispatchState.NOT_DISPATCHED,
                    reason_code="READ_ONLY_MUTATION_REFUSED",
                )
            capability = self.adapter.capability(request.required_capability)
            if capability is None or (
                request.required_authority == Authority.MUTATION and not capability.action_supported
            ) or (
                request.required_authority == Authority.READ_ONLY and not capability.read_supported
            ):
                return self._make_result(
                    request,
                    LifecycleState.REFUSED,
                    ActionStatus.REFUSED,
                    DispatchState.NOT_DISPATCHED,
                    reason_code="CAPABILITY_UNSUPPORTED",
                )
            try:
                expected_bound = self.adapter.effect_bound(request.kind, request.parameters)
                if expected_bound != request.effect_bound:
                    raise ValidationError("EFFECT_BOUND_MISMATCH", "ActionRequest EffectBound does not match deterministic adapter bound")
                self._reserve(run, request)
            except ValidationError as exc:
                return self._make_result(
                    request,
                    LifecycleState.REFUSED,
                    ActionStatus.REFUSED,
                    DispatchState.NOT_DISPATCHED,
                    reason_code=exc.code,
                )
            except (DurabilityError, DurabilityTimeout):
                self.mutation_disabled = True
                return self._make_result(
                    request,
                    LifecycleState.FAILED_BEFORE_DISPATCH,
                    ActionStatus.FAIL,
                    DispatchState.NOT_DISPATCHED,
                    reason_code="RESERVATION_DURABILITY_FAILED",
                )
            if token is not None and token.cancelled:
                return self._terminalize_pre_dispatch(
                    run, request, LifecycleState.CANCELLED_BEFORE_DISPATCH,
                    ActionStatus.CANCELLED, "CANCELLED_BEFORE_DISPATCH",
                )
            if self._deadline_expired(run):
                return self._terminalize_pre_dispatch(
                    run, request, LifecycleState.TIMED_OUT_BEFORE_DISPATCH,
                    ActionStatus.TIMEOUT, "RUN_DEADLINE_EXPIRED",
                )
            try:
                authority_available = self.adapter.await_authority(request)
            except Exception:  # noqa: BLE001 -- this adapter phase is before the one-shot dispatch fence
                return self._terminalize_pre_dispatch(
                    run, request, LifecycleState.FAILED_BEFORE_DISPATCH,
                    ActionStatus.FAIL, "AUTHORITY_WAIT_FAILED_BEFORE_DISPATCH",
                )
            if not authority_available:
                return self._terminalize_pre_dispatch(
                    run, request, LifecycleState.REFUSED,
                    ActionStatus.REFUSED, "AUTHORITY_UNAVAILABLE",
                )
            try:
                preflight_allowed = self.adapter.preflight(request)
            except ValidationError as exc:
                return self._terminalize_pre_dispatch(
                    run, request, LifecycleState.REFUSED,
                    ActionStatus.REFUSED, exc.code,
                )
            if not preflight_allowed:
                return self._terminalize_pre_dispatch(
                    run, request, LifecycleState.REFUSED,
                    ActionStatus.REFUSED, "PREFLIGHT_REFUSED",
                )
            final_commit_refusal_reason: list[str | None] = [None]
            one_shot = _OneShotCommit(
                lambda: self._final_commit(
                    run,
                    request,
                    token,
                    final_commit_check,
                    final_commit_refusal_reason,
                    action_deadline_ns,
                )
            )
            try:
                execution = self.adapter.execute_committed(request, one_shot)
            except SimulatedCrash:
                durable = self.store.load_action(request.action_id)
                if durable is not None and durable.dispatch_state != DispatchState.NOT_DISPATCHED:
                    next_budget = self._reconcile_budget(run, request, outcome="ambiguous")
                    ambiguous = durable.with_state(
                        LifecycleState.AMBIGUOUS,
                        self.clock.now_ns(),
                        reason_code="CRASH_AFTER_DISPATCH_COMMIT",
                    )
                    try:
                        self.store.atomic_reconcile(ambiguous, next_budget)
                        run.budget = next_budget
                    except (DurabilityError, DurabilityTimeout):
                        self.mutation_disabled = True
                    result = self._make_result(
                        request,
                        LifecycleState.AMBIGUOUS,
                        ActionStatus.AMBIGUOUS,
                        DispatchState.POSSIBLY_DISPATCHED,
                        reason_code="CRASH_AFTER_DISPATCH_COMMIT",
                    )
                    self.results[request.action_id] = result
                    return result
                return self._terminalize_pre_dispatch(
                    run, request, LifecycleState.FAILED_BEFORE_DISPATCH,
                    ActionStatus.FAIL, "CRASH_BEFORE_DISPATCH",
                )
            if not execution.get("committed"):
                durable = self.store.load_action(request.action_id)
                if durable is not None and durable.dispatch_state != DispatchState.NOT_DISPATCHED:
                    return self._make_result(
                        request,
                        LifecycleState.AMBIGUOUS,
                        ActionStatus.AMBIGUOUS,
                        DispatchState.POSSIBLY_DISPATCHED,
                        reason_code="COMMIT_RESULT_CONTRADICTION",
                    )
                refusal_reason = final_commit_refusal_reason[0] or "FINAL_COMMIT_REFUSED"
                if refusal_reason == "ACTION_TIMEOUT_EXPIRED":
                    return self._terminalize_pre_dispatch(
                        run, request, LifecycleState.TIMED_OUT_BEFORE_DISPATCH,
                        ActionStatus.TIMEOUT, refusal_reason,
                    )
                return self._terminalize_pre_dispatch(
                    run, request, LifecycleState.REFUSED,
                    ActionStatus.REFUSED, refusal_reason,
                )
            durable = self.store.load_action(request.action_id)
            if durable is None or durable.dispatch_state == DispatchState.NOT_DISPATCHED:
                self.mutation_disabled = True
                return self._make_result(
                    request,
                    LifecycleState.AMBIGUOUS,
                    ActionStatus.AMBIGUOUS,
                    DispatchState.POSSIBLY_DISPATCHED,
                    reason_code="DURABLE_DISPATCH_STATE_MISSING",
                )
            execution_outcome = str(execution.get("outcome", "confirmed"))
            if execution_outcome != "confirmed":
                reason = (
                    str(execution.get("reason_code") or "POST_DISPATCH_AMBIGUOUS")
                    if execution_outcome == "ambiguous"
                    else "POST_DISPATCH_OUTCOME_INVALID"
                )
                next_budget = self._reconcile_budget(run, request, outcome="ambiguous")
                terminal = durable.with_state(
                    LifecycleState.AMBIGUOUS,
                    self.clock.now_ns(),
                    dispatch_state=DispatchState.POSSIBLY_DISPATCHED,
                    authoritative_confirmation=Confirmation.UNKNOWN,
                    reason_code=reason,
                )
                try:
                    self.store.atomic_reconcile(terminal, next_budget)
                    run.budget = next_budget
                except (DurabilityError, DurabilityTimeout):
                    self.mutation_disabled = True
                    reason = "RESULT_DURABILITY_FAILED"
                result = self._make_result(
                    request,
                    LifecycleState.AMBIGUOUS,
                    ActionStatus.AMBIGUOUS,
                    DispatchState.POSSIBLY_DISPATCHED,
                    confirmation=Confirmation.UNKNOWN,
                    reason_code=reason,
                )
                self.results[request.action_id] = result
                return result
            next_budget = self._reconcile_budget(run, request, outcome="confirmed")
            if run.cancelled or (token is not None and token.cancelled):
                terminal_state = LifecycleState.CANCELLED_AFTER_DISPATCH
                terminal_status = ActionStatus.CANCELLED
                reason = "CANCELLED_AFTER_DISPATCH"
            else:
                terminal_state = LifecycleState.CONFIRMED
                terminal_status = ActionStatus.PASS
                reason = None
            terminal = durable.with_state(
                terminal_state,
                self.clock.now_ns(),
                dispatch_state=DispatchState.DISPATCHED,
                authoritative_confirmation=Confirmation.PROVEN,
                reason_code=reason,
            )
            try:
                self.store.atomic_reconcile(terminal, next_budget)
                run.budget = next_budget
            except (DurabilityError, DurabilityTimeout):
                self.mutation_disabled = True
                result = self._make_result(
                    request,
                    LifecycleState.AMBIGUOUS,
                    ActionStatus.AMBIGUOUS,
                    DispatchState.POSSIBLY_DISPATCHED,
                    reason_code="RESULT_DURABILITY_FAILED",
                )
                self.results[request.action_id] = result
                return result
            result = self._make_result(
                request,
                terminal_state,
                terminal_status,
                DispatchState.DISPATCHED,
                confirmation=Confirmation.PROVEN,
                reason_code=reason,
            )
            self.results[request.action_id] = result
            return result

    def stop_all(
        self,
        *,
        transition_id: str | None = None,
        reason_code: str = "STOP_ALL",
        state_persister: Callable[[ControlState], None] | None = None,
    ) -> bool:
        with self.stop_operation_lock:
            persisted = False
            with self.run_admission_lock, self.control_transition_lock, self.dispatch_gate:
                self.in_memory_stop = True
                self.mutation_disabled = True
                self.stop_cleanup_in_progress = True
                try:
                    next_generation = checked_add(
                        self.control_generation, 1, maximum=MAX_U64, field_name="control_generation"
                    )
                except ValidationError:
                    self.stop_durability_unresolved = True
                else:
                    next_state = self._new_control_state(
                        stop_latched=True,
                        recovery_required=self.control_state.recovery_required,
                        generation=next_generation,
                        transition_id=transition_id or f"stop:{self.backend_epoch}:{next_generation}",
                        reason_code=reason_code,
                        active_backend_epoch=self.backend_epoch,
                    )
                    try:
                        if state_persister is None:
                            self.store.write_control_state(next_state, operation="stop")
                        else:
                            state_persister(next_state)
                    except (DurabilityError, DurabilityTimeout):
                        self.stop_durability_unresolved = True
                    else:
                        self.control_state = next_state
                        self.stop_durability_unresolved = False
                        persisted = True
                for run in self.runs.values():
                    run.cancelled = True
            try:
                self.adapter.emergency_stop(reason_code)
            except Exception:  # noqa: BLE001 -- failed cleanup must keep STOP fail-closed
                return False
            with self.control_transition_lock:
                self.stop_cleanup_in_progress = False
            return persisted
    def reset_stop(self, *, transition_id: str | None = None, reason_code: str = "EXPLICIT_RESET") -> bool:
        with self.control_transition_lock, self.dispatch_gate:
                if self.stop_cleanup_in_progress or self.stop_durability_unresolved:
                    return False
                for ledger in self.store.budget_ledgers.values():
                    if any(
                        dimension.uncertain > 0 or dimension.at_risk > 0
                        for dimension in ledger.dimensions.values()
                    ):
                        return False
                if any(
                    record.lifecycle_state == LifecycleState.AMBIGUOUS
                    for record in self.store.action_ledgers.values()
                ):
                    return False
                try:
                    next_generation = checked_add(
                        self.control_generation,
                        1,
                        maximum=MAX_U64,
                        field_name="control_generation",
                    )
                except ValidationError:
                    self.in_memory_stop = True
                    self.mutation_disabled = True
                    return False
                next_state = self._new_control_state(
                    stop_latched=False,
                    recovery_required=False,
                    generation=next_generation,
                    transition_id=transition_id or f"reset:{self.backend_epoch}:{next_generation}",
                    reason_code=reason_code,
                    active_backend_epoch=self.backend_epoch,
                )
                try:
                    self.store.write_control_state(next_state, operation="reset")
                except (DurabilityError, DurabilityTimeout):
                    self.in_memory_stop = True
                    self.mutation_disabled = True
                    return False
                self.control_state = next_state
                self.in_memory_stop = False
                self.mutation_disabled = False
                return True

    def pause_run(self, run_id: str, *, durable_hook: Callable[[], None] | None = None) -> None:
        with self.control_transition_lock, self.dispatch_gate:
            run = self._run(run_id)
            if durable_hook is not None:
                durable_hook()
            run.paused = True

    def resume_run(self, run_id: str) -> bool:
        run = self._run(run_id)
        if run.cancelled:
            return False
        if self._deadline_expired(run):
            return False
        identity = self.adapter.identity()
        if identity.adapter_generation != run.expected_adapter_generation:
            return False
        if identity.runtime_instance_id != run.expected_runtime_instance_id:
            return False
        if identity.session_epoch != run.expected_session_epoch:
            return False
        if self.in_memory_stop or self.control_state.stop_latched or self.control_state.recovery_required:
            return False
        run.paused = False
        return True

    def wait_until(
        self,
        run_id: str,
        predicate: Callable[[], bool],
        *,
        timeout_ms: int,
        token: CancellationToken | None = None,
        poll_ms: int = 1,
    ) -> str:
        run = self._run(run_id)
        local_deadline = min(
            run.budget.deadline_monotonic_ns,
            checked_add(
                self.clock.now_ns(),
                checked_mul(timeout_ms, 1_000_000, maximum=MAX_U64, field_name="wait_timeout"),
                maximum=MAX_U64,
                field_name="wait_timeout",
            ),
        )
        while self.clock.now_ns() < local_deadline:
            if token is not None and token.cancelled:
                return "CANCELLED"
            if run.cancelled or self.in_memory_stop:
                return "CANCELLED"
            if predicate():
                return "READY"
            self.clock.advance_ms(poll_ms)
        self._deadline_expired(run)
        return "TIMEOUT"

    def retry_action(
        self,
        old_action_id: str,
        new_request: ActionRequest,
        *,
        token: CancellationToken | None = None,
    ) -> ActionResult:
        old = self.store.load_action(old_action_id)
        if old is None:
            return self._make_result(
                new_request,
                LifecycleState.REFUSED,
                ActionStatus.REFUSED,
                DispatchState.NOT_DISPATCHED,
                reason_code="RETRY_SOURCE_MISSING",
            )
        if old.dispatch_state != DispatchState.NOT_DISPATCHED or old.lifecycle_state not in {
            LifecycleState.REFUSED,
            LifecycleState.FAILED_BEFORE_DISPATCH,
            LifecycleState.TIMED_OUT_BEFORE_DISPATCH,
            LifecycleState.CANCELLED_BEFORE_DISPATCH,
        }:
            return self._make_result(
                new_request,
                LifecycleState.REFUSED,
                ActionStatus.REFUSED,
                DispatchState.NOT_DISPATCHED,
                reason_code="RETRY_NOT_PROVEN_NOT_DISPATCHED",
            )
        if new_request.action_id == old_action_id or new_request.attempt_index <= old.attempt_index:
            return self._make_result(
                new_request,
                LifecycleState.REFUSED,
                ActionStatus.REFUSED,
                DispatchState.NOT_DISPATCHED,
                reason_code="RETRY_IDENTITY_INVALID",
            )
        return self.execute_action(new_request, token=token)

    def accept_callback(
        self,
        action_id: str,
        *,
        backend_epoch: str,
        control_generation: int,
        lifecycle_state: LifecycleState,
        adapter_generation: str | object = _MISSING,
        runtime_instance_id: str | None | object = _MISSING,
        session_epoch: str | None | object = _MISSING,
        authoritative_confirmation: Confirmation = Confirmation.UNKNOWN,
    ) -> bool:
        if not self.mutation_execution_lock.acquire(blocking=False):
            return False
        try:
            return self._accept_callback_unlocked(
                action_id,
                backend_epoch=backend_epoch,
                control_generation=control_generation,
                lifecycle_state=lifecycle_state,
                adapter_generation=adapter_generation,
                runtime_instance_id=runtime_instance_id,
                session_epoch=session_epoch,
                authoritative_confirmation=authoritative_confirmation,
            )
        finally:
            self.mutation_execution_lock.release()

    def _accept_callback_unlocked(
        self,
        action_id: str,
        *,
        backend_epoch: str,
        control_generation: int,
        lifecycle_state: LifecycleState,
        adapter_generation: str | object = _MISSING,
        runtime_instance_id: str | None | object = _MISSING,
        session_epoch: str | None | object = _MISSING,
        authoritative_confirmation: Confirmation = Confirmation.UNKNOWN,
    ) -> bool:
        record = self.store.load_action(action_id)
        if record is None or record.terminal:
            return False
        if (
            adapter_generation is _MISSING
            or runtime_instance_id is _MISSING
            or session_epoch is _MISSING
        ):
            return False
        if (
            backend_epoch != self.backend_epoch
            or backend_epoch != record.backend_epoch
            or control_generation != self.control_generation
            or control_generation != record.control_generation
        ):
            return False
        identity = self.adapter.identity()
        if identity.adapter_id != record.adapter_id:
            return False
        if (
            adapter_generation != record.adapter_generation
            or identity.adapter_generation != record.adapter_generation
            or runtime_instance_id != record.runtime_instance_id
            or identity.runtime_instance_id != record.runtime_instance_id
            or session_epoch != record.session_epoch
            or identity.session_epoch != record.session_epoch
        ):
            return False
        if authoritative_confirmation != Confirmation.UNKNOWN:
            return False
        if record.dispatch_state == DispatchState.NOT_DISPATCHED:
            return False
        allowed_transitions = {
            LifecycleState.DISPATCH_COMMITTED: {
                LifecycleState.DISPATCHING,
                LifecycleState.CONFIRMING,
            },
            LifecycleState.DISPATCHING: {LifecycleState.CONFIRMING},
        }
        if lifecycle_state not in allowed_transitions.get(record.lifecycle_state, set()):
            return False
        try:
            updated = record.with_state(lifecycle_state, self.clock.now_ns())
            self.store.write_action(updated, operation="callback")
        except (ValidationError, DurabilityError, DurabilityTimeout):
            return False
        return True

    def clean_shutdown(self) -> bool:
        self.mutation_disabled = True
        if not self.mutation_execution_lock.acquire(blocking=False):
            return False
        try:
            with self.control_transition_lock:
                if self.activation_error is not None or self.stop_durability_unresolved or self.stop_cleanup_in_progress:
                    return False
                if any(
                    record.dispatch_state != DispatchState.NOT_DISPATCHED and not record.terminal
                    for record in self.store.action_ledgers.values()
                ):
                    return False
                if any(
                    dimension.at_risk > 0
                    for ledger in self.store.budget_ledgers.values()
                    for dimension in ledger.dimensions.values()
                ):
                    return False
                try:
                    self.store.flush_safety_state()
                except (DurabilityError, DurabilityTimeout):
                    return False
                next_state = self._new_control_state(
                    stop_latched=self.control_state.stop_latched,
                    recovery_required=self.control_state.recovery_required,
                    generation=self.control_generation,
                    transition_id=f"backend-clean-shutdown:{self.backend_epoch}",
                    reason_code="BACKEND_CLEAN_SHUTDOWN",
                    active_backend_epoch=None,
                )
                try:
                    self.store.write_control_state(next_state, operation="clean_shutdown")
                except (DurabilityError, DurabilityTimeout):
                    return False
                self.control_state = next_state
                return True
        finally:
            self.mutation_execution_lock.release()
