from __future__ import annotations

from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def replace_between(text: str, start: str, end: str, replacement: str, label: str) -> str:
    start_at = text.find(start)
    if start_at < 0:
        raise SystemExit(f"{label}: start marker missing")
    end_at = text.find(end, start_at + len(start))
    if end_at < 0:
        raise SystemExit(f"{label}: end marker missing")
    return text[:start_at] + replacement.rstrip() + "\n\n" + text[end_at:]


execution_path = Path("tools/tibia_re_control_center/execution.py")
execution = execution_path.read_text(encoding="utf-8")

execution = replace_once(
    execution,
    "from .store import DeterministicDurableStore\n",
    "from .store import DeterministicDurableStore\n\n\n_MISSING = object()\n",
    "callback sentinel",
)
execution = replace_once(
    execution,
    """        self.dispatch_gate = threading.RLock()\n        self.mutation_execution_lock = threading.Lock()\n        self.runs: dict[str, RunState] = {}\n""",
    """        self.dispatch_gate = threading.RLock()\n        self.control_transition_lock = threading.RLock()\n        self.mutation_execution_lock = threading.Lock()\n        self.runs: dict[str, RunState] = {}\n""",
    "control transition lock",
)
execution = replace_once(
    execution,
    """        self.in_memory_stop = False\n        self.mutation_disabled = False\n        self.activation_error: str | None = None\n""",
    """        self.in_memory_stop = False\n        self.mutation_disabled = False\n        self.stop_durability_unresolved = False\n        self.activation_error: str | None = None\n""",
    "failed STOP latch state",
)
execution = replace_once(
    execution,
    """    def _final_commit(self, run: RunState, request: ActionRequest, token: CancellationToken | None) -> bool:\n""",
    """    def _final_commit(\n        self,\n        run: RunState,\n        request: ActionRequest,\n        token: CancellationToken | None,\n        final_commit_check: Callable[[], bool] | None,\n    ) -> bool:\n""",
    "final commit signature",
)
execution = replace_once(
    execution,
    """            if request.action_id not in run.budget.reservations:\n                return False\n            next_budget = self._move_reserved_to_at_risk(run.budget, request.action_id)\n""",
    """            if request.action_id not in run.budget.reservations:\n                return False\n            if final_commit_check is not None:\n                try:\n                    final_check_passed = final_commit_check()\n                except Exception:\n                    return False\n                if final_check_passed is not True:\n                    return False\n            next_budget = self._move_reserved_to_at_risk(run.budget, request.action_id)\n""",
    "final safety predicate gate",
)
execution = replace_once(
    execution,
    """    def execute_action(self, request: ActionRequest, *, token: CancellationToken | None = None) -> ActionResult:\n""",
    """    def execute_action(\n        self,\n        request: ActionRequest,\n        *,\n        token: CancellationToken | None = None,\n        final_commit_check: Callable[[], bool] | None = None,\n    ) -> ActionResult:\n""",
    "execute action signature",
)
execution = replace_once(
    execution,
    """            one_shot = _OneShotCommit(lambda: self._final_commit(run, request, token))\n""",
    """            one_shot = _OneShotCommit(\n                lambda: self._final_commit(run, request, token, final_commit_check)\n            )\n""",
    "one-shot final guard",
)

stop_method = '''    def stop_all(self, *, transition_id: str | None = None, reason_code: str = "STOP_ALL") -> bool:
        with self.control_transition_lock:
            with self.dispatch_gate:
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
                self.in_memory_stop = True
                next_state = self._new_control_state(
                    stop_latched=True,
                    recovery_required=self.control_state.recovery_required,
                    generation=next_generation,
                    transition_id=transition_id or f"stop:{self.backend_epoch}:{next_generation}",
                    reason_code=reason_code,
                    active_backend_epoch=self.backend_epoch,
                )
                try:
                    self.store.write_control_state(next_state, operation="stop")
                except (DurabilityError, DurabilityTimeout):
                    self.stop_durability_unresolved = True
                    self.mutation_disabled = True
                    return False
                self.control_state = next_state
                self.stop_durability_unresolved = False
                self.mutation_disabled = True
        for run in self.runs.values():
            run.cancelled = True
        self.adapter.emergency_stop(reason_code)
        return True'''
execution = replace_between(execution, "    def stop_all(", "    def reset_stop(", stop_method, "STOP method")

reset_method = '''    def reset_stop(self, *, transition_id: str | None = None, reason_code: str = "EXPLICIT_RESET") -> bool:
        with self.control_transition_lock:
            with self.dispatch_gate:
                if self.stop_durability_unresolved:
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
                for run in self.runs.values():
                    run.cancelled = False
                return True'''
execution = replace_between(execution, "    def reset_stop(", "    def pause_run(", reset_method, "reset method")

callback_method = '''    def accept_callback(
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
        return True'''
execution = replace_between(
    execution,
    "    def accept_callback(",
    "    def clean_shutdown(",
    callback_method,
    "callback method",
)

clean_shutdown_method = '''    def clean_shutdown(self) -> bool:
        self.mutation_disabled = True
        if not self.mutation_execution_lock.acquire(blocking=False):
            return False
        try:
            with self.control_transition_lock:
                if self.activation_error is not None or self.stop_durability_unresolved:
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
            self.mutation_execution_lock.release()'''
clean_start = execution.find("    def clean_shutdown(")
if clean_start < 0:
    raise SystemExit("clean shutdown: start marker missing")
execution = execution[:clean_start] + clean_shutdown_method.rstrip() + "\n"
execution_path.write_text(execution, encoding="utf-8", newline="\n")

engine_path = Path("tools/tibia_re_control_center/engine.py")
engine = engine_path.read_text(encoding="utf-8")
engine = replace_once(
    engine,
    '''                    elif step.step_type == "action":\n                        request = self._action_request(run_id, step)\n                        result = self.coordinator.execute_action(request)\n''',
    '''                    elif step.step_type == "action":\n                        request = self._action_request(run_id, step)\n\n                        def final_commit_check(\n                            bound_scenario: ValidatedScenario = scenario,\n                        ) -> bool:\n                            observed = self._snapshot_mapping(self.adapter.snapshot())\n                            return self._abort_reason(bound_scenario, observed) is None\n\n                        result = self.coordinator.execute_action(\n                            request,\n                            final_commit_check=final_commit_check,\n                        )\n''',
    "engine final abort guard",
)
engine_path.write_text(engine, encoding="utf-8", newline="\n")

workflow_path = Path(".github/workflows/tibia-re-control-center-core.yml")
workflow = workflow_path.read_text(encoding="utf-8")
workflow = replace_once(
    workflow,
    "          PYTHONPATH=. python3 tests/tools/tibia_re_control_center/audit_package_a.py\n",
    "          PYTHONPATH=. python3 tests/tools/tibia_re_control_center/audit_package_a.py\n"
    "          PYTHONPATH=. python3 tests/tools/tibia_re_control_center/audit_package_a_p1.py\n",
    "fresh audit P1 extension",
)
workflow_path.write_text(workflow, encoding="utf-8", newline="\n")

print("PACKAGE_A_P1_REPAIR_APPLIED=YES")
