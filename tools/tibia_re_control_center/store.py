from __future__ import annotations

import copy
from typing import Any

from .model import (
    ActionLedgerRecord,
    BudgetLedger,
    ControlState,
    DurabilityError,
    DurabilityTimeout,
    ValidationError,
)


class DeterministicDurableStore:
    """In-memory Package A durability model with deterministic fault injection."""

    def __init__(self) -> None:
        self.initialized = False
        self.control_state: ControlState | None = None
        self.action_ledgers: dict[str, ActionLedgerRecord] = {}
        self.budget_ledgers: dict[str, BudgetLedger] = {}
        self.run_activation: dict[str, tuple[int, int]] = {}
        self.recovery_records: dict[str, dict[str, Any]] = {}
        self._faults: dict[str, list[str]] = {}
        self.safety_flush_count = 0

    def inject_fault(self, operation: str, kind: str = "error", *, count: int = 1) -> None:
        if kind not in {"error", "timeout"} or count < 1:
            raise ValueError("fault kind must be error/timeout and count >= 1")
        self._faults.setdefault(operation, []).extend([kind] * count)

    def clear_faults(self) -> None:
        self._faults.clear()

    def _before_write(self, operation: str) -> None:
        queue = self._faults.get(operation)
        if not queue:
            return
        kind = queue.pop(0)
        if not queue:
            self._faults.pop(operation, None)
        if kind == "timeout":
            raise DurabilityTimeout(f"durability timeout during {operation}")
        raise DurabilityError(f"durability failure during {operation}")

    def load_control_state(self) -> ControlState | None:
        if self.initialized and self.control_state is None:
            raise ValidationError("CONTROL_STATE_MISSING", "initialized store is missing authoritative ControlState")
        return copy.deepcopy(self.control_state)

    def write_control_state(self, state: ControlState, *, operation: str = "control_state") -> None:
        self._before_write(operation)
        self.control_state = copy.deepcopy(state)
        self.initialized = True

    def load_action(self, action_id: str) -> ActionLedgerRecord | None:
        return copy.deepcopy(self.action_ledgers.get(action_id))

    def write_action(self, record: ActionLedgerRecord, *, operation: str = "action") -> None:
        self._before_write(operation)
        existing = self.action_ledgers.get(record.action_id)
        if existing and existing.action_request_hash != record.action_request_hash:
            raise ValidationError("IDEMPOTENCY_CONFLICT", "action_id already exists with a different request hash")
        self.action_ledgers[record.action_id] = copy.deepcopy(record)

    def load_budget(self, run_id: str) -> BudgetLedger | None:
        value = self.budget_ledgers.get(run_id)
        return None if value is None else value.clone()

    def write_budget(self, ledger: BudgetLedger, *, operation: str = "budget") -> None:
        self._before_write(operation)
        self.budget_ledgers[ledger.run_id] = ledger.clone()

    def persist_run_activation(self, run_id: str, started_ns: int, deadline_ns: int) -> None:
        self._before_write("run_activation")
        existing = self.run_activation.get(run_id)
        if existing is not None and existing != (started_ns, deadline_ns):
            raise ValidationError("RUN_ACTIVATION_CONFLICT", "run activation/deadline is immutable")
        self.run_activation[run_id] = (started_ns, deadline_ns)

    def load_run_activation(self, run_id: str) -> tuple[int, int] | None:
        return self.run_activation.get(run_id)

    def atomic_dispatch_commit(self, record: ActionLedgerRecord, ledger: BudgetLedger) -> None:
        self._before_write("dispatch_commit")
        existing = self.action_ledgers.get(record.action_id)
        if existing and existing.action_request_hash != record.action_request_hash:
            raise ValidationError("IDEMPOTENCY_CONFLICT", "action_id already exists with a different request hash")
        self.action_ledgers[record.action_id] = copy.deepcopy(record)
        self.budget_ledgers[ledger.run_id] = ledger.clone()

    def atomic_reconcile(self, record: ActionLedgerRecord, ledger: BudgetLedger) -> None:
        self._before_write("reconcile")
        existing = self.action_ledgers.get(record.action_id)
        if existing is None:
            raise ValidationError("ACTION_LEDGER_MISSING", "cannot reconcile an unknown action")
        self.action_ledgers[record.action_id] = copy.deepcopy(record)
        self.budget_ledgers[ledger.run_id] = ledger.clone()

    def write_recovery(self, run_id: str, record: dict[str, Any]) -> None:
        self._before_write("recovery")
        self.recovery_records[run_id] = copy.deepcopy(record)

    def flush_safety_state(self) -> None:
        self._before_write("safety_flush")
        self.safety_flush_count += 1

    def corrupt_control_state(self) -> None:
        self.initialized = True
        self.control_state = None

    def snapshot(self) -> dict[str, Any]:
        return {
            "initialized": self.initialized,
            "control_state": copy.deepcopy(self.control_state),
            "actions": copy.deepcopy(self.action_ledgers),
            "budgets": {key: value.clone() for key, value in self.budget_ledgers.items()},
            "run_activation": dict(self.run_activation),
            "recovery": copy.deepcopy(self.recovery_records),
        }
