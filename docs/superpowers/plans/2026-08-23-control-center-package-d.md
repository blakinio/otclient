# Control Center Package D Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a fail-closed real `OFFICIAL_TIBIA` Control Center adapter that reuses Track A canonical authority, preserves post-COMMIT ambiguity, and promotes exactly one physical action only after fresh runtime proof.

**Architecture:** Keep `MutationCoordinator` as the Control Center-local safety owner. `OfficialTibiaAdapter` acquires one external Track A guarded-dispatch session inside `execute_committed()`; the coordinator's `_final_commit()` then revalidates that exact already-active session through `dispatch_guard()` before durable commit. Extend the existing canonical transition supervisor rather than creating a second lease/flock authority system, and add one canonical GUI/input `flock` that serializes input actors but grants no authority.

**Tech Stack:** Python 3 standard library (`contextlib`, `dataclasses`, `fcntl`, `hashlib`, `importlib`, `json`, `os`, `stat`, `subprocess`, `threading`), `unittest`, existing Control Center packages, existing Track A lease/guard/transition scripts, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-08-23-control-center-package-d-design.md`

## Global Constraints

- Runtime remains `runtime_access:none` until repository implementation/tests are green and the active task is freshly re-admitted.
- Exact current Official client fence is version `15.32`, size `52109920`, SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`, platform `official_native_linux_only`.
- `turn` is the preferred first physical candidate; `move` is only a separately proved fallback.
- Exactly one action family may be promoted in the first runtime slice.
- Control Center `dispatch_gate` is never Track A authority and is never held while waiting for Track A authority or GUI/input serialization.
- Track A canonical lease, registration, rebind, Gate B and whole-lifetime supervisor are reused, not copied.
- ActionRequest/result/evidence objects must not expose raw key combinations, GUI coordinates, opcodes, QMeta IDs, addresses, pointers, PIDs, XIDs, display IDs, bridge handles, lease capabilities or credentials.
- A committed action with uncertain physical outcome remains `POSSIBLY_DISPATCHED/AMBIGUOUS`; automatic retry is forbidden.
- Package D does not bootstrap/login merely to manufacture action evidence.
- Shared `MODULE_CATALOG.md`, `CHANGELOG.md` and normative contracts are edited only after fresh live ownership revalidation.

---

## Shared test fixture for Tasks 1, 2 and 5

Create `tests/tools/tibia_re_control_center/test_package_d_official_adapter.py` with these concrete helpers before the first test:

```python
from __future__ import annotations

import unittest
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any

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


def request_for_adapter(coordinator: MutationCoordinator, adapter: Any) -> ActionRequest:
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
        schema_version=1,
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
```

This fixture uses the real Scenario-v1 hash/effect-bound path and never accesses Official Tibia.

---

### Task 1: Make post-COMMIT outcomes conservative in `MutationCoordinator`

**Files:**
- Create: `tests/tools/tibia_re_control_center/test_package_d_official_adapter.py`
- Modify: `tools/tibia_re_control_center/execution.py`

**Interfaces:**
- Consumes existing adapter `execute_committed(request, commit_dispatch) -> mapping`.
- Produces optional execution field `outcome` with exact values `confirmed` or `ambiguous`; omitted means `confirmed` for backward compatibility with `FakeAdapter`.

- [ ] **Step 1: Add a concrete ambiguous fake adapter and failing test**

```python
class CommittedAmbiguousAdapter(FakeAdapter):
    def execute_committed(self, request, commit_dispatch):
        committed = commit_dispatch()
        return {
            "committed": committed,
            "effect": None,
            "outcome": "ambiguous" if committed else None,
            "reason_code": "OFFICIAL_CONFIRMATION_UNAVAILABLE",
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
        self.assertEqual(ledger.dimensions["max_actions"].at_risk, 0)
        self.assertEqual(ledger.dimensions["max_actions"].uncertain, 1)
```

- [ ] **Step 2: Run the single test and verify RED**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.tools.tibia_re_control_center.test_package_d_official_adapter.PackageDExecutionResultTests.test_committed_ambiguous_execution_never_becomes_pass -v
```

Expected: FAIL because current `MutationCoordinator` turns every `committed=True` execution into `CONFIRMED/PASS`.

- [ ] **Step 3: Add one helper for committed ambiguity in `MutationCoordinator`**

Add a private helper directly beside `_reconcile_budget()`:

```python
def _terminalize_committed_ambiguous(
    self,
    run: RunState,
    request: ActionRequest,
    durable: ActionLedgerRecord,
    reason_code: str,
) -> ActionResult:
    next_budget = self._reconcile_budget(run, request, outcome="ambiguous")
    terminal = durable.with_state(
        LifecycleState.AMBIGUOUS,
        self.clock.now_ns(),
        dispatch_state=DispatchState.POSSIBLY_DISPATCHED,
        authoritative_confirmation=Confirmation.UNKNOWN,
        reason_code=reason_code,
    )
    try:
        self.store.atomic_reconcile(terminal, next_budget)
        run.budget = next_budget
    except (DurabilityError, DurabilityTimeout):
        self.mutation_disabled = True
        reason_code = "RESULT_DURABILITY_FAILED"
    result = self._make_result(
        request,
        LifecycleState.AMBIGUOUS,
        ActionStatus.AMBIGUOUS,
        DispatchState.POSSIBLY_DISPATCHED,
        confirmation=Confirmation.UNKNOWN,
        reason_code=reason_code,
    )
    self.results[request.action_id] = result
    return result
```

- [ ] **Step 4: Normalize execution outcome after durable commit**

Immediately after loading the durable committed record, add:

```python
execution_outcome = str(execution.get("outcome", "confirmed"))
if execution_outcome == "ambiguous":
    return self._terminalize_committed_ambiguous(
        run,
        request,
        durable,
        str(execution.get("reason_code") or "POST_DISPATCH_AMBIGUOUS"),
    )
if execution_outcome != "confirmed":
    return self._terminalize_committed_ambiguous(
        run,
        request,
        durable,
        "POST_DISPATCH_OUTCOME_INVALID",
    )
```

Keep the existing confirmed branch unchanged after this guard.

- [ ] **Step 5: Add two concrete regression tests**

Add `InvalidOutcomeAdapter` returning `{"committed": True, "effect": None, "outcome": "unexpected"}` after a successful commit and assert `AMBIGUOUS/POSSIBLY_DISPATCHED/POST_DISPATCH_OUTCOME_INVALID`. Add a normal `FakeAdapter` test and assert its omitted `outcome` still yields `CONFIRMED/PASS/DISPATCHED/PROVEN`.

- [ ] **Step 6: Run focused and full suites**

```bash
python3 -m compileall -q tools/tibia_re_control_center tests/tools/tibia_re_control_center
PYTHONPATH=. python3 -m unittest tests.tools.tibia_re_control_center.test_package_d_official_adapter -v
PYTHONPATH=. python3 -m unittest discover -s tests/tools/tibia_re_control_center -v
```

Expected: all tests PASS.

- [ ] **Step 7: Commit**

```bash
git add tools/tibia_re_control_center/execution.py tests/tools/tibia_re_control_center/test_package_d_official_adapter.py
git commit -m "fix(control-center): preserve post-dispatch ambiguity"
```

---

### Task 2: Implement the fail-closed semantic `OfficialTibiaAdapter`

**Files:**
- Create: `tools/tibia_re_control_center/official_adapter.py`
- Modify: `tests/tools/tibia_re_control_center/test_package_d_official_adapter.py`

**Interfaces:**

Production types:

```python
@dataclass(frozen=True)
class OfficialCapabilityPromotion:
    action_kind: str
    client_sha256: str
    read_gate: str
    action_gate: str
    semantic_path_id: str
    confirmation_id: str
    requires_input_lock: bool
    evidence_refs: tuple[str, ...]
    adapter_generation: str


@dataclass(frozen=True)
class GuardedRuntimeView:
    adapter_generation: str
    runtime_instance_id: str
    session_epoch: str | None
    client_state: str
    authority_current: bool
    target_unique: bool
    input_lock_held: bool
    fence_digest: str


@dataclass(frozen=True)
class GuardedExecutionOutcome:
    outcome: str
    reason_code: str | None
    evidence_refs: tuple[str, ...]


class GuardedDispatchSession(Protocol):
    def current_view(self) -> GuardedRuntimeView:
        raise NotImplementedError

    def cross_once_and_reconcile(self, request: ActionRequest) -> GuardedExecutionOutcome:
        raise NotImplementedError


class TrackAAuthorityBridge(Protocol):
    def advisory_available(self, request: ActionRequest) -> bool:
        raise NotImplementedError

    @contextmanager
    def guarded_dispatch(self, request: ActionRequest) -> Iterator[GuardedDispatchSession]:
        raise NotImplementedError

    def emergency_stop(self, reason: str) -> None:
        raise NotImplementedError
```

- [ ] **Step 1: Write a failing default-deny test**

```python
class DenyBridge:
    def advisory_available(self, request):
        return False

    @contextmanager
    def guarded_dispatch(self, request):
        raise AssertionError("default-deny adapter must not enter guarded dispatch")
        yield

    def emergency_stop(self, reason):
        return None


class PackageDOfficialAdapterTests(unittest.TestCase):
    def test_official_adapter_is_non_actionable_without_promotion(self):
        identity = AdapterIdentity(
            adapter_id="official",
            adapter_kind=AdapterKind.OFFICIAL_TIBIA,
            adapter_version="1.0",
            adapter_generation="official-generation-1",
            runtime_instance_id="runtime-1",
            session_epoch="session-1",
        )
        adapter = OfficialTibiaAdapter(identity, DenyBridge(), promotions=())
        capability = adapter.capability("turn")
        self.assertIsNotNone(capability)
        self.assertFalse(adapter.allow_mutation)
        self.assertFalse(capability.action_supported)
```

- [ ] **Step 2: Run RED**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.tools.tibia_re_control_center.test_package_d_official_adapter.PackageDOfficialAdapterTests.test_official_adapter_is_non_actionable_without_promotion -v
```

Expected: import failure because `official_adapter.py` does not exist.

- [ ] **Step 3: Implement constructor, promotion validation and capability projection**

Exact rules:

```python
CURRENT_CLIENT_SHA256 = "ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8"
ALLOWED_READ_GATES = {"R0", "R1", "R2", "R3", "R4"}
ALLOWED_ACTION_GATES = {"A0", "A1", "A2", "A3", "A4"}


def _promotion_is_current(promotion, identity):
    return bool(
        promotion.client_sha256 == CURRENT_CLIENT_SHA256
        and promotion.adapter_generation == identity.adapter_generation
        and promotion.read_gate in ALLOWED_READ_GATES
        and promotion.action_gate in ALLOWED_ACTION_GATES
        and promotion.requires_input_lock
        and promotion.semantic_path_id
        and promotion.confirmation_id
        and promotion.evidence_refs
    )
```

`OfficialTibiaAdapter` rejects non-Official identity, reuses `OfficialTibiaAdapterContract`, stores only current promotions, sets `concurrency_safe_reads=False`, and reports `allow_mutation=True` only when at least one current promotion exists. This boolean remains local capability enablement, not Track A authority.

- [ ] **Step 4: Implement exact semantic methods**

```python
def effect_bound(self, kind, parameters):
    normalized = validate_action_parameters(kind, parameters)
    return default_effect_bound(kind, normalized)


def preflight(self, request):
    self._prep.map_action(request)
    capability = self.capability(request.required_capability)
    return bool(
        capability is not None
        and capability.action_supported
        and self._bridge.advisory_available(request)
    )
```

`await_authority()` performs only bounded advisory availability and never caches authority. `current_authority(READ_ONLY)` returns false for this first mutation-only slice; `current_authority(MUTATION)` returns true only while an active guarded session exists and its current view is authority-current, target-unique and input-lock-held.

- [ ] **Step 5: Implement guarded-session coupling**

Use thread-local storage because `_final_commit()` calls back into `dispatch_guard()` synchronously on the same execution thread:

```python
def execute_committed(self, request, commit_dispatch):
    with self._bridge.guarded_dispatch(request) as session:
        self._active_session.value = session
        try:
            view = session.current_view()
            if not self._view_allows(request, view):
                return {"committed": False, "effect": None}
            if not commit_dispatch():
                return {"committed": False, "effect": None}
            outcome = session.cross_once_and_reconcile(request)
            normalized = outcome.outcome if outcome.outcome in {"confirmed", "ambiguous"} else "ambiguous"
            return {
                "committed": True,
                "effect": None,
                "outcome": normalized,
                "reason_code": outcome.reason_code,
            }
        finally:
            self._active_session.value = None
```

`dispatch_guard()` must assert an active session exists, call `session.current_view()` again, verify current promotion and current view, then yield `(self.identity(), capability, authority_current)`. It must not call `guarded_dispatch()` itself.

- [ ] **Step 6: Add a concrete in-memory guarded session fixture**

```python
@dataclass
class FakeGuardedSession:
    view: GuardedRuntimeView
    outcome: GuardedExecutionOutcome
    cross_calls: int = 0

    def current_view(self):
        return self.view

    def cross_once_and_reconcile(self, request):
        self.cross_calls += 1
        if self.cross_calls != 1:
            raise AssertionError("physical boundary crossed more than once")
        return self.outcome


class FakeAuthorityBridge:
    def __init__(self, session, advisory=True):
        self.session = session
        self.advisory = advisory
        self.guard_entries = 0

    def advisory_available(self, request):
        return self.advisory

    @contextmanager
    def guarded_dispatch(self, request):
        self.guard_entries += 1
        yield self.session

    def emergency_stop(self, reason):
        return None
```

- [ ] **Step 7: Add exact safety tests**

Use the fake session/bridge to assert all of these:

| Test | Exact assertion |
| --- | --- |
| `test_promotion_wrong_build_is_not_actionable` | `capability("turn").action_supported is False` |
| `test_promotion_wrong_generation_is_not_actionable` | same false result |
| `test_input_lock_false_refuses_before_commit` | coordinator result `REFUSED/NOT_DISPATCHED`, `cross_calls == 0` |
| `test_target_not_unique_refuses_before_commit` | same zero-effect result |
| `test_commit_refusal_crosses_zero_effects` | bridge entered once, `cross_calls == 0` |
| `test_commit_success_crosses_once` | result `CONFIRMED/PASS`, `cross_calls == 1` |
| `test_ambiguous_reconciliation_remains_ambiguous` | result `AMBIGUOUS/POSSIBLY_DISPATCHED` |
| `test_emergency_stop_delegates_cleanup_only` | bridge cleanup called; no new session/effect created |

- [ ] **Step 8: Run focused/full suites and commit**

```bash
PYTHONPATH=. python3 -m unittest tests.tools.tibia_re_control_center.test_package_d_official_adapter -v
PYTHONPATH=. python3 -m unittest discover -s tests/tools/tibia_re_control_center -v
ruff check tools/tibia_re_control_center
```

Commit:

```bash
git add tools/tibia_re_control_center/official_adapter.py tests/tools/tibia_re_control_center/test_package_d_official_adapter.py
git commit -m "feat(control-center): add fail-closed Official Tibia adapter"
```

---

### Task 3: Add canonical GUI/input serialization primitive

**Files:**
- Create: `.github/scripts/tibia-official-client-re-input-lock.py`
- Create: `.github/scripts/test_tibia_official_client_re_input_lock.py`

**Interfaces:**
- `hold_input_lock(state_dir: Path, blocking: bool = True)` yields only while the exact `input.lock` inode is exclusively flocked.
- The module has no lease, registration, login, runtime discovery or mutation API.

- [ ] **Step 1: Write the failing lock test module**

Use `importlib.util` to load the hyphenated production script. Include a test class that creates `TemporaryDirectory()` and checks mode, ownership, contention and symlink refusal. The primary contention test must fork/spawn a second Python process that opens the same path and verifies nonblocking acquisition exits with the typed `input_lock_busy` error.

Concrete identity assertion:

```python
with module.hold_input_lock(state_dir):
    st = (state_dir / "input.lock").lstat()
    self.assertTrue(stat.S_ISREG(st.st_mode))
    self.assertEqual(stat.S_IMODE(st.st_mode), 0o600)
    if hasattr(os, "getuid"):
        self.assertEqual(st.st_uid, os.getuid())
```

Concrete symlink assertion:

```python
target = state_dir / "target"
target.write_text("x", encoding="utf-8")
(state_dir / "input.lock").symlink_to(target)
with self.assertRaises(module.InputLockError) as caught:
    with module.hold_input_lock(state_dir):
        self.fail("symlink must never be admitted")
self.assertEqual(caught.exception.code, "input_lock_path_unsafe")
```

- [ ] **Step 2: Run RED**

```bash
PYTHONPATH=. python3 .github/scripts/test_tibia_official_client_re_input_lock.py -v
```

Expected: production module missing.

- [ ] **Step 3: Implement the lock helper**

```python
class InputLockError(RuntimeError):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


@contextmanager
def hold_input_lock(state_dir: Path, *, blocking: bool = True):
    state_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    path = state_dir / "input.lock"
    if path.is_symlink():
        raise InputLockError("input_lock_path_unsafe")
    flags = os.O_RDWR | os.O_CREAT | os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(path, flags, 0o600)
    except OSError as exc:
        raise InputLockError("input_lock_path_unsafe") from exc
    try:
        os.fchmod(fd, 0o600)
        st_fd = os.fstat(fd)
        st_path = path.lstat()
        if not stat.S_ISREG(st_fd.st_mode):
            raise InputLockError("input_lock_not_regular")
        if (st_fd.st_dev, st_fd.st_ino) != (st_path.st_dev, st_path.st_ino):
            raise InputLockError("input_lock_identity_invalid")
        if hasattr(os, "getuid") and st_fd.st_uid != os.getuid():
            raise InputLockError("input_lock_owner_invalid")
        operation = fcntl.LOCK_EX if blocking else fcntl.LOCK_EX | fcntl.LOCK_NB
        try:
            fcntl.flock(fd, operation)
        except BlockingIOError as exc:
            raise InputLockError("input_lock_busy") from exc
        after = path.lstat()
        if (st_fd.st_dev, st_fd.st_ino) != (after.st_dev, after.st_ino):
            raise InputLockError("input_lock_identity_changed")
        yield
    finally:
        os.close(fd)
```

- [ ] **Step 4: Add exact regression cases**

Add tests for lock release after context exit, replacement inode rejection, owner mismatch using patched `os.getuid`, and absence of exported names containing `lease`, `gate_b`, `login`, `credential`, `runtime_registration` or `mutation_authorized`.

- [ ] **Step 5: Run tests and commit**

```bash
PYTHONPATH=. python3 .github/scripts/test_tibia_official_client_re_input_lock.py -v
python3 -m compileall -q .github/scripts/tibia-official-client-re-input-lock.py .github/scripts/test_tibia_official_client_re_input_lock.py
```

Commit:

```bash
git add .github/scripts/tibia-official-client-re-input-lock.py .github/scripts/test_tibia_official_client_re_input_lock.py
git commit -m "feat(track-a): add canonical GUI input lock"
```

---

### Task 4: Extend canonical transition supervisor with `guarded-dispatch`

**Files:**
- Modify: `.github/scripts/tibia-official-client-re-canonical-live-transition.py`
- Modify: `.github/scripts/test_tibia_official_client_re_canonical_live_transition.py`
- Reuse: `.github/scripts/tibia-official-client-re-input-lock.py`

**Interfaces:**
- New transition operation: `guarded-dispatch`.
- Fixed worker protocol: private line-delimited JSON over inherited pipes created by the transition supervisor; lease/input-lock fds use `CLOEXEC` and are never inherited.
- Control messages are exactly `READY`, `COMMIT`, `ABORT`, `RESULT`.

- [ ] **Step 1: Add exact protocol constants/tests before implementation**

In transition tests create a fake worker that reports one READY record, waits for one control record, increments a task-private counter only for COMMIT, then returns a RESULT. Add tests with these assertions:

| Test | Required assertion |
| --- | --- |
| missing registration | transition rc nonzero, counter stays `0` |
| stale registration generation | rc nonzero, counter `0` |
| input lock held before READY | fake worker's attempt to acquire the same lock nonblocking reports busy |
| Gate B identity changes after input lock | rc nonzero, counter `0` |
| ABORT | rc zero or typed abort result, counter `0` |
| COMMIT | counter exactly `1` |
| second COMMIT record | protocol rejected; counter never exceeds `1` |
| lease generation drift before COMMIT | typed refusal; counter `0` |
| supervisor cancellation before COMMIT | counter `0` |
| child descendant outlives primary | canonical coordination and input lock remain busy until descendant exits |

- [ ] **Step 2: Run RED**

```bash
PYTHONPATH=. python3 .github/scripts/test_tibia_official_client_re_canonical_live_transition.py -v
```

Expected: `guarded-dispatch` parser/implementation absent.

- [ ] **Step 3: Load input-lock module exactly once**

Add:

```python
INPUT_LOCK_PATH = Path(__file__).with_name("tibia-official-client-re-input-lock.py")


def _input_lock():
    spec = importlib.util.spec_from_file_location("track_a_input_lock", INPUT_LOCK_PATH)
    if spec is None or spec.loader is None:
        raise E("input_lock_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module
```

- [ ] **Step 4: Implement strict JSON record parsing**

Use exact-key validation:

```python
def _json_record(line: str, required: set[str]) -> dict[str, Any]:
    try:
        value = json.loads(line)
    except json.JSONDecodeError as exc:
        raise E("guarded_dispatch_protocol_invalid") from exc
    if not isinstance(value, dict) or set(value) != required:
        raise E("guarded_dispatch_protocol_invalid")
    return value
```

READY keys: `type`, `action_hash`, `fence_digest`. RESULT keys: `type`, `outcome`, `reason_code`, `evidence_refs`. Allowed outcomes: `confirmed`, `ambiguous`.

- [ ] **Step 5: Implement `_guarded_dispatch()` ordering inside the already flock-owning `_child()`**

The code sequence must be:

```text
_child validates current lease while holding coordination.lock
-> _probe_reg(... old=False)
-> acquire hold_input_lock(STATE)
-> _probe_reg(... old=False) again
-> launch fixed worker with close_fds=True and dedicated stdin/stdout pipes
-> receive/validate READY and exact caller-supplied action hash
-> receive exactly one COMMIT or ABORT from the bridge-side channel
-> ABORT: send ABORT to worker and wait for all descendants; zero effect
-> COMMIT: _probe_reg(... old=False) and _lease(... generation) again
-> send COMMIT once
-> receive RESULT once
-> wait for worker and all adopted/orphaned descendants
-> release input lock
-> existing supervisor later releases coordination.lock
```

Do not serialize raw registration fields into READY/RESULT.

- [ ] **Step 6: Add parser arguments with fixed semantics**

`guarded-dispatch` requires: `--task-id`, `--session-id`, `--token-file`, `--probe`, `--worker`, `--action-hash`, `--control-fd`, and bounded worker timeout. Reject shell command strings and environment-selected workers.

- [ ] **Step 7: Run transition/guard/lease regressions**

```bash
PYTHONPATH=. python3 .github/scripts/test_tibia_official_client_re_canonical_live_transition.py -v
PYTHONPATH=. python3 .github/scripts/test_tibia_official_client_re_canonical_live_guard.py -v
PYTHONPATH=. python3 .github/scripts/test_tibia_official_client_re_canonical_live_lease.py -v
```

- [ ] **Step 8: Commit**

```bash
git add .github/scripts/tibia-official-client-re-canonical-live-transition.py \
        .github/scripts/test_tibia_official_client_re_canonical_live_transition.py
git commit -m "feat(track-a): add guarded Control Center dispatch transaction"
```

---

### Task 5: Implement the fixed Track A bridge and fake full-path E2E

**Files:**
- Create: `tools/tibia_re_control_center/track_a_authority_bridge.py`
- Modify: `tools/tibia_re_control_center/official_adapter.py`
- Modify: `tests/tools/tibia_re_control_center/test_package_d_official_adapter.py`

**Interfaces:**
- `CanonicalTrackAAuthorityBridge` implements the Task-2 `TrackAAuthorityBridge` protocol.
- Constructor accepts repository root, task ID, session ID, token *path*, probe path and worker path. It never reads token contents.
- Public/sanitized envelopes expose only action hash, fence digest, outcome, reason code and evidence refs.

- [ ] **Step 1: Add strict envelope tests**

Use exact assertions:

```python
FORBIDDEN_PUBLIC_KEY_PARTS = {
    "pid", "xid", "display", "window", "token", "coordinate",
    "address", "pointer", "opcode", "keycode", "lease_capability",
}


def assert_sanitized_mapping(testcase, value):
    for key in value:
        lowered = key.lower()
        testcase.assertFalse(any(part in lowered for part in FORBIDDEN_PUBLIC_KEY_PARTS))
```

Tests must reject READY/RESULT records with any extra key, reject invalid outcome values, and prove `token_file.read_text` is never called by patching it to raise `AssertionError`.

- [ ] **Step 2: Implement strict transport types**

```python
READY_KEYS = frozenset({"type", "action_hash", "fence_digest"})
RESULT_KEYS = frozenset({"type", "outcome", "reason_code", "evidence_refs"})
ALLOWED_OUTCOMES = frozenset({"confirmed", "ambiguous"})


def require_exact_record(value, keys):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValidationError("TRACK_A_BRIDGE_PROTOCOL_INVALID", "unexpected guarded-dispatch record")
    return value
```

- [ ] **Step 3: Implement fixed command construction without `shell=True`**

Command executable is `sys.executable`; script is repository-owned `.github/scripts/tibia-official-client-re-canonical-live-transition.py`; operation is exactly `guarded-dispatch`. Pass token path, not contents. All other paths are constructor-bound and resolved beneath the repository root or exact canonical task state location.

- [ ] **Step 4: Implement bridge/session lifecycle**

`guarded_dispatch()` starts the transition process with private pipes, waits for READY, creates a session object whose `current_view()` is a sanitized current fence view, and whose `cross_once_and_reconcile()` sends COMMIT once then consumes RESULT once. Context exit before COMMIT sends ABORT. Process timeout after COMMIT returns `GuardedExecutionOutcome("ambiguous", "TRACK_A_RESULT_TIMEOUT", ())` rather than a pre-dispatch failure.

- [ ] **Step 5: Add complete fake Control Center E2E tests**

Use a fake transition process fixture, not the Official client. Required cases:

| Case | Required final result |
| --- | --- |
| confirmed turn | `CONFIRMED/PASS/DISPATCHED/PROVEN`, fake effect count `1` |
| STOP between READY and commit | `REFUSED` or `CANCELLED_BEFORE_DISPATCH`, fake effect count `0` |
| control generation drift | `NOT_DISPATCHED`, fake effect count `0` |
| ambiguous RESULT after COMMIT | `AMBIGUOUS/POSSIBLY_DISPATCHED`, fake effect count `1` maximum |
| bridge timeout before READY | pre-dispatch failure/refusal, fake effect count `0` |
| bridge timeout after COMMIT | ambiguous, no automatic second dispatch |

- [ ] **Step 6: Run full repository-only validation**

```bash
python3 -m compileall -q tools/tibia_re_control_center tests/tools/tibia_re_control_center .github/scripts
PYTHONPATH=. python3 -m unittest discover -s tests/tools/tibia_re_control_center -v
PYTHONPATH=. python3 tests/tools/tibia_re_control_center/audit_package_a.py
PYTHONPATH=. python3 tests/tools/tibia_re_control_center/audit_package_a_p1.py
ruff check tools/tibia_re_control_center
```

Expected: Package A regressions remain green; all Package D tests use fake Track A transport only.

- [ ] **Step 7: Commit**

```bash
git add tools/tibia_re_control_center/official_adapter.py \
        tools/tibia_re_control_center/track_a_authority_bridge.py \
        tests/tools/tibia_re_control_center/test_package_d_official_adapter.py
git commit -m "feat(control-center): bridge Official adapter to Track A guard"
```

---

### Task 6: Revalidate shared governance and make the input lock normative

**Files:**
- Revalidate before edit: `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`
- Revalidate before edit: `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md`
- Revalidate before edit: `docs/agents/MODULE_CATALOG.md`
- Revalidate before edit: `docs/agents/CHANGELOG.md`
- Modify: `docs/agents/tasks/active/OTC-20260823-tibia-re-control-center-package-d.md`

- [ ] **Step 1: Re-query open PR changed files and task ownership for all four shared paths**

If a path has an unresolved current owner, do not edit it. Record the exact owner PR/task in the active Package D record. If the missing normative edit is required for physical safety, keep physical dispatch blocked until ownership is serialized.

- [ ] **Step 2: If the Track A admission contract is unowned, add this exact semantic rule**

```text
Canonical GUI/input mutation additionally requires the reviewed canonical
input.lock held by the existing external Track A supervisor. input.lock only
serializes GUI/input actors; it grants no lease, registration, Gate B,
mutation, login, credential, gameplay or session authority. Failure to acquire
or revalidate it refuses mutation. The same lock remains held through final
target validation, Control Center commit, the one physical effect and immediate
reconciliation.
```

- [ ] **Step 3: If Adapter v1 is unowned, bind it to the concrete guarded transaction**

State that Official `execute()` uses the current canonical Track A guarded-dispatch supervisor plus canonical input lock, while raw lock paths/fds and runtime handles remain adapter-private.

- [ ] **Step 4: Update catalogue/changelog only when ownership is free**

Add entries for `OfficialTibiaAdapter`, `CanonicalTrackAAuthorityBridge`, canonical input lock and guarded-dispatch transition. Do not edit unrelated entries.

- [ ] **Step 5: Update the active task checkpoint**

Set `phase: implement`, list all actually owned implementation paths, add the implementation plan path, and preserve these exact facts until runtime admission begins:

```yaml
runtime_access: none
mutation_authorized: false
official_client_access: false
first_action_status: NOT_YET_PHYSICALLY_PROVEN
```

- [ ] **Step 6: Commit governance/docs changes separately**

```bash
git add docs/agents/contracts docs/agents/MODULE_CATALOG.md docs/agents/CHANGELOG.md \
        docs/agents/tasks/active/OTC-20260823-tibia-re-control-center-package-d.md
git commit -m "docs(track-a): define Package D guarded input boundary"
```

Stage only files whose ownership was actually granted; omit deferred shared files from `git add`.

---

### Task 7: Exact-head repository validation before any runtime admission

**Files:** no new production files unless a deterministic validation failure requires a task-owned repair.

- [ ] **Step 1: Review the complete PR changed-file list and diff**

Reject unrelated files, credentials, secret-bearing evidence, proprietary assets, raw runtime handles and unexpected workflow changes.

- [ ] **Step 2: Verify exact-head checks**

Required when triggered:

```text
CI
TIBIA RE Control Center Package A / Package A deterministic core
TIBIA RE Control Center Package A / Fresh Package A falsification audit
Track A agent runtime governance
Track A canonical-live governance
```

- [ ] **Step 3: Inspect failed job logs before any rerun**

Fix deterministic failures in task-owned scope. A second identical failure is investigated rather than rerun unchanged.

- [ ] **Step 4: Keep PR #670 Draft after repository green**

Repository green does not grant runtime authority or action capability.

---

### Task 8: Fresh Track A runtime admission and conditional first-slice proof

**Files:**
- Modify before live access: `docs/agents/tasks/active/OTC-20260823-tibia-re-control-center-package-d.md`
- Create after legal live evidence exists: `docs/agents/evidence/OTC-20260823-tibia-re-control-center-package-d/runtime-admission.md`
- Create only after a current semantic path is proved: `.github/scripts/tibia-official-client-re-control-center-turn-worker.py`
- Create with that worker: `.github/scripts/test_tibia_official_client_re_control_center_turn_worker.py`

- [ ] **Step 1: Re-read then-current trusted `main`, admission contract and every open Track A runtime owner**

PR #475 or any successor current runtime owner is a hard ownership input. Package D must not observe or mutate another task's runtime surface.

- [ ] **Step 2: Persist the complete current admission record before any live operation**

Populate every field from then-current controller/runtime state. Legal classes are `canonical_reuse_or_mutation`, `canonical_rebind`, `canonical_bootstrap`, or `none`. Any required `UNKNOWN`, `REQUIRED_NOT_PROVEN`, `REQUIRED_UNAVAILABLE` or `REQUIRED_UNIMPLEMENTED` value keeps `mutation_authorized:false` and forbids the operation.

- [ ] **Step 3: Stop physical work on any current ownership/admission blocker**

Use one exact durable blocker code chosen from the observed condition:

```text
BLOCKED_RUNTIME_OWNED_BY_OTHER_TASK
BLOCKED_NO_CURRENT_REGISTERED_RUNTIME
BLOCKED_REBIND_REQUIRED
BLOCKED_GATE_B_NOT_PROVEN
BLOCKED_INPUT_LOCK_NOT_NORMATIVE
BLOCKED_NO_CURRENT_ACTIVE_WORLD_SEMANTIC_PROOF
BLOCKED_TARGET_UNIQUENESS_NOT_PROVEN
```

No gate is weakened to avoid a blocker.

- [ ] **Step 4: If current runtime is legally reusable, prove `turn` before writing a physical worker**

Current evidence must establish all six facts: semantic physical path, reference UI parity, exactly one turn effect, no movement side effect, canonical input lock requirement, and authoritative facing-direction before/after confirmation. Historical Package D PREP evidence is not sufficient.

- [ ] **Step 5: Create the first-slice worker only after Step 4 passes**

The worker file name is fixed above. It accepts only the sanitized semantic `turn` envelope and the already-supervisor-bound runtime context. The newly proved raw input mapping remains private inside this worker and its sanitized evidence; it is never added to ActionRequest, API schema or public result objects. If Step 4 does not establish a safe mapping, do not create the worker.

- [ ] **Step 6: TDD the worker against a fake X11/input target before real use**

Tests must prove one COMMIT causes exactly one turn command, ABORT causes zero commands, malformed direction is refused, second COMMIT is refused, and result reports only `confirmed` or `ambiguous` with sanitized evidence refs.

- [ ] **Step 7: Promote exactly `turn` only after current proof and worker tests pass**

Persist a sanitized promotion record containing current client SHA, exact R/A grades justified by current evidence, semantic path ID, confirmation ID, input-lock requirement, evidence refs and current adapter generation. `move` remains unsupported.

- [ ] **Step 8: Execute exactly one real Control Center physical E2E**

Required order:

```text
ActionRequest(turn)
-> Scenario validation + exact EffectBound
-> budget reservation
-> external Track A guarded-dispatch
-> canonical input lock
-> final current Gate B / identity / target uniqueness
-> READY
-> Control Center commit_dispatch() = COMMITTED
-> exactly one physical turn
-> authoritative facing-direction reconciliation
-> CONFIRMED/PASS
```

A direct worker call or manual input does not count as Package D E2E.

- [ ] **Step 9: On post-COMMIT uncertainty, record ambiguity and stop**

The only legal uncertain terminal result is `AMBIGUOUS/POSSIBLY_DISPATCHED`; do not automatically retry or claim first-slice success.

---

### Task 9: Closeout, independent validation and merge

**Files:**
- Create/update: `docs/agents/evidence/OTC-20260823-tibia-re-control-center-package-d/package-d-result.md`
- Create: `docs/agents/tasks/archive/OTC-20260823-tibia-re-control-center-package-d.md`
- Delete after archive content is durable: `docs/agents/tasks/active/OTC-20260823-tibia-re-control-center-package-d.md`

- [ ] **Step 1: Record one exact physical disposition**

Use exactly one:

```text
PHYSICAL_SLICE=CONFIRMED_PASS
PHYSICAL_SLICE=BLOCKED_WITH_REASON
PHYSICAL_SLICE=AMBIGUOUS_NO_RETRY
```

Fake E2E is never described as physical compatibility.

- [ ] **Step 2: Run fresh independent validation required by repository policy**

Inspect exact-head CI, deterministic falsification, all review threads/comments and any central Spark advisory that the repository automation actually produced. Do not invoke direct Codex/Spark from this Package D task unless a separate current-task authorization is added to repository authority.

- [ ] **Step 3: Mark Ready only when merge gates are satisfied**

A runtime-blocked implementation may be ready only if it remains fail-closed, advertises no unproved action support, records the blocker precisely, and repository acceptance permits the blocked physical disposition.

- [ ] **Step 4: Squash merge and verify final `main`**

Record exact implementation head, merge SHA, check run/job IDs, findings, runtime admission/disposition and the single remaining next action in the archive/evidence.
