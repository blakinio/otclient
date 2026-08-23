# Control Center Package D Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a fail-closed real `OFFICIAL_TIBIA` Control Center adapter that reuses Track A canonical authority, can represent post-COMMIT ambiguity correctly, and promotes exactly one physical action only after fresh runtime proof.

**Architecture:** Keep `MutationCoordinator` as the Control Center-local safety owner and implement the Official adapter by duck-typing the existing adapter surface. External authority is acquired inside `execute_committed()` through one Track A guarded-dispatch transaction; `_final_commit()` then revalidates that exact active guarded session via `dispatch_guard()`. Extend the existing Track A canonical transition supervisor rather than creating a second lease/flock authority system, and add one canonical GUI/input `flock` used only as serialization, never authority.

**Tech Stack:** Python 3 standard library (`dataclasses`, `contextlib`, `fcntl`, `subprocess`, `json`, `hashlib`, `threading`), `unittest`, existing Control Center model/scenario/execution/store packages, existing Track A lease/guard/transition scripts, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-08-23-control-center-package-d-design.md`

## Global Constraints

- Runtime remains `runtime_access:none` until repository implementation/tests are green and the active task is freshly re-admitted.
- Exact current Official client fence remains version `15.32`, size `52109920`, SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`, `official_native_linux_only`.
- `turn` is the preferred first physical candidate; `move` is only a separately proved fallback.
- Exactly one action family may be promoted in the first runtime slice.
- Control Center `dispatch_gate` is never Track A authority and is never held while waiting for external Track A authority or GUI/input serialization.
- Track A canonical lease, registration, rebind, Gate B and whole-lifetime supervisor are reused, not copied.
- No ActionRequest/result/evidence object may expose raw key combinations, GUI coordinates, opcodes, QMeta IDs, addresses, pointers, PIDs, XIDs, display IDs, bridge handles, lease capabilities or credentials.
- A committed action with uncertain physical outcome must remain `POSSIBLY_DISPATCHED/AMBIGUOUS`; no blind retry.
- No bootstrap/login is performed merely to make Package D progress; physical work requires a separately legal current runtime state.
- Shared `MODULE_CATALOG.md`, `CHANGELOG.md` and normative contracts are edited only after fresh live ownership revalidation.

---

### Task 1: Make post-COMMIT outcomes conservative in `MutationCoordinator`

**Files:**
- Modify: `tools/tibia_re_control_center/execution.py`
- Test: `tests/tools/tibia_re_control_center/test_package_d_official_adapter.py`

**Interfaces:**
- Consumes: current adapter `execute_committed(request, commit_dispatch) -> mapping`.
- Produces: optional `outcome` field with exact values `confirmed` or `ambiguous`; omitted means `confirmed` for backward compatibility with `FakeAdapter`.

- [ ] **Step 1: Write the failing ambiguity test**

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


def test_committed_ambiguous_execution_never_becomes_pass():
    clock, store, adapter, coordinator, request = make_mutation_fixture(
        adapter_cls=CommittedAmbiguousAdapter,
        capability="turn",
        kind="turn",
        parameters={"direction": "NORTH"},
    )
    result = coordinator.execute_action(request)
    self.assertEqual(result.lifecycle_state, LifecycleState.AMBIGUOUS)
    self.assertEqual(result.status, ActionStatus.AMBIGUOUS)
    self.assertEqual(result.dispatch_state, DispatchState.POSSIBLY_DISPATCHED)
    self.assertNotEqual(result.authoritative_confirmation, Confirmation.PROVEN)
```

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```bash
PYTHONPATH=. python3 -m unittest \
  tests.tools.tibia_re_control_center.test_package_d_official_adapter.PackageDExecutionResultTests.test_committed_ambiguous_execution_never_becomes_pass -v
```

Expected: FAIL because current `MutationCoordinator` treats every `committed=True` result as confirmed PASS.

- [ ] **Step 3: Implement the minimal conservative branch**

Immediately after durable committed-state verification in `execute_action()`, normalize:

```python
execution_outcome = str(execution.get("outcome", "confirmed"))
if execution_outcome == "ambiguous":
    next_budget = self._reconcile_budget(run, request, outcome="ambiguous")
    ambiguous = durable.with_state(
        LifecycleState.AMBIGUOUS,
        self.clock.now_ns(),
        dispatch_state=DispatchState.POSSIBLY_DISPATCHED,
        authoritative_confirmation=Confirmation.UNKNOWN,
        reason_code=str(execution.get("reason_code") or "POST_DISPATCH_AMBIGUOUS"),
    )
    self.store.atomic_reconcile(ambiguous, next_budget)
    run.budget = next_budget
    result = self._make_result(
        request,
        LifecycleState.AMBIGUOUS,
        ActionStatus.AMBIGUOUS,
        DispatchState.POSSIBLY_DISPATCHED,
        confirmation=Confirmation.UNKNOWN,
        reason_code=ambiguous.reason_code,
    )
    self.results[request.action_id] = result
    return result
if execution_outcome != "confirmed":
    # Unknown post-COMMIT classifications are unsafe and therefore ambiguous.
    ...
```

Implement the unknown-outcome case with the same ambiguity path and reason `POST_DISPATCH_OUTCOME_INVALID`; do not throw a pre-dispatch exception after durable commit.

- [ ] **Step 4: Add regression tests**

Add tests proving:

```python
def test_legacy_fake_adapter_without_outcome_still_confirms(): ...
def test_invalid_post_commit_outcome_is_ambiguous(): ...
def test_ambiguous_reconciliation_moves_budget_from_at_risk_to_uncertain(): ...
```

- [ ] **Step 5: Run focused and full Control Center suites**

```bash
python3 -m compileall -q tools/tibia_re_control_center tests/tools/tibia_re_control_center
PYTHONPATH=. python3 -m unittest discover -s tests/tools/tibia_re_control_center -v
```

Expected: all tests PASS; existing FakeAdapter success semantics unchanged.

- [ ] **Step 6: Commit**

```bash
git add tools/tibia_re_control_center/execution.py tests/tools/tibia_re_control_center/test_package_d_official_adapter.py
git commit -m "fix(control-center): preserve post-dispatch ambiguity"
```

---

### Task 2: Implement the fail-closed semantic `OfficialTibiaAdapter`

**Files:**
- Create: `tools/tibia_re_control_center/official_adapter.py`
- Modify/Test: `tests/tools/tibia_re_control_center/test_package_d_official_adapter.py`

**Interfaces:**
- Consumes: `OfficialTibiaAdapterContract.map_action()`, `ActionRequest`, `AdapterIdentity`, `Capability`, `RuntimeStatus`, `default_effect_bound()`.
- Produces:

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
    outcome: str  # confirmed | ambiguous
    reason_code: str | None
    evidence_refs: tuple[str, ...]

class GuardedDispatchSession(Protocol):
    def current_view(self) -> GuardedRuntimeView: ...
    def cross_once_and_reconcile(self, request: ActionRequest) -> GuardedExecutionOutcome: ...

class TrackAAuthorityBridge(Protocol):
    def advisory_available(self, request: ActionRequest) -> bool: ...
    @contextmanager
    def guarded_dispatch(self, request: ActionRequest) -> Iterator[GuardedDispatchSession]: ...
    def emergency_stop(self, reason: str) -> None: ...
```

- [ ] **Step 1: Write failing default-deny tests**

```python
def test_official_adapter_is_non_actionable_without_promotion():
    adapter = make_official_adapter(promotions=())
    self.assertFalse(adapter.allow_mutation)
    self.assertFalse(adapter.capability("turn").action_supported)
    self.assertFalse(adapter.await_authority(make_turn_request()))


def test_promotion_must_match_current_build_and_adapter_generation():
    bad = OfficialCapabilityPromotion(
        action_kind="turn",
        client_sha256="0" * 64,
        read_gate="R2",
        action_gate="A2",
        semantic_path_id="turn-v1",
        confirmation_id="facing-direction-v1",
        requires_input_lock=True,
        evidence_refs=("evidence:test",),
        adapter_generation="official-generation-1",
    )
    adapter = make_official_adapter(promotions=(bad,))
    self.assertFalse(adapter.capability("turn").action_supported)
```

- [ ] **Step 2: Run and verify RED**

Expected: import/module failure because `official_adapter.py` does not exist.

- [ ] **Step 3: Implement types and constructor validation**

Implement `OfficialTibiaAdapter` so it:

```python
class OfficialTibiaAdapter:
    concurrency_safe_reads = False

    def __init__(self, identity, authority_bridge, promotions=()):
        if identity.adapter_kind is not AdapterKind.OFFICIAL_TIBIA:
            raise ValidationError("OFFICIAL_ADAPTER_IDENTITY_REQUIRED", ...)
        self._prep = OfficialTibiaAdapterContract(identity)
        self._bridge = authority_bridge
        self._active_session = threading.local()
        self._promotions = validate_promotions(promotions, identity)
```

`allow_mutation` returns `True` only when at least one valid current promotion exists; it never means current Track A authority.

- [ ] **Step 4: Implement capability/effect-bound/preflight methods**

Rules:

```python
def effect_bound(self, kind, parameters):
    normalized = validate_action_parameters(kind, parameters)
    return default_effect_bound(kind, normalized)


def capability(self, capability_id):
    promotion = self._promotions.get(capability_id)
    return Capability(
        capability_id=capability_id,
        read_supported=False,
        action_supported=promotion is not None,
        source="official-package-d-evidence-promotion" if promotion else "official-package-d-default-deny",
        notes=None if promotion else OFFICIAL_RUNTIME_NOT_ADMITTED,
    )
```

`preflight()` reuses exact PREP mapping and returns false unless a valid promotion exists and `authority_bridge.advisory_available()` is true. It never caches authority.

- [ ] **Step 5: Implement guarded-session coupling**

`execute_committed()` must acquire external authority before invoking the coordinator commit callback:

```python
def execute_committed(self, request, commit_dispatch):
    with self._bridge.guarded_dispatch(request) as session:
        self._active_session.value = session
        try:
            view = session.current_view()
            if not self._view_allows(request, view):
                return {"committed": False, "effect": None}
            committed = commit_dispatch()
            if not committed:
                return {"committed": False, "effect": None}
            outcome = session.cross_once_and_reconcile(request)
            return {
                "committed": True,
                "effect": None,
                "outcome": outcome.outcome,
                "reason_code": outcome.reason_code,
            }
        finally:
            self._active_session.value = None
```

`dispatch_guard()` must not acquire a second external guard. It only revalidates the already-active session and yields the current identity/capability/authority tuple expected by `_final_commit()`.

- [ ] **Step 6: Add race/safety tests**

Use an in-memory fake bridge/session to prove:

```python
def test_external_guard_is_entered_before_commit_callback(): ...
def test_dispatch_guard_revalidates_same_active_session(): ...
def test_input_lock_false_refuses_before_commit(): ...
def test_target_uniqueness_false_refuses_before_commit(): ...
def test_adapter_generation_change_refuses_before_commit(): ...
def test_commit_refusal_calls_zero_physical_effects(): ...
def test_commit_success_calls_cross_once_exactly_once(): ...
def test_public_result_contains_no_raw_runtime_handles(): ...
```

- [ ] **Step 7: Run focused/full suites and commit**

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
- Produces a context-managed exclusive `flock` for exactly `canonical-live-runtime/input.lock`.
- It grants no lease/runtime/mutation authority and carries no credentials.

- [ ] **Step 1: Write failing lock tests**

Tests must prove:

```python
def test_lock_file_is_mode_0600_regular_owned_file(): ...
def test_second_nonblocking_holder_is_refused(): ...
def test_lock_released_after_context_exit(): ...
def test_symlink_path_is_rejected(): ...
def test_replaced_inode_is_rejected(): ...
def test_lock_has_no_authority_or_runtime_api(): ...
```

Use a temporary state directory and a subprocess for true `flock` contention.

- [ ] **Step 2: Run RED**

```bash
PYTHONPATH=. python3 .github/scripts/test_tibia_official_client_re_input_lock.py -v
```

Expected: module/path missing.

- [ ] **Step 3: Implement the lock helper**

Core API:

```python
class InputLockError(RuntimeError):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


@contextmanager
def hold_input_lock(state_dir: Path, *, blocking: bool = True):
    state_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    path = state_dir / "input.lock"
    fd = os.open(path, os.O_RDWR | os.O_CREAT | os.O_CLOEXEC | os.O_NOFOLLOW, 0o600)
    try:
        st_fd = os.fstat(fd)
        st_path = path.lstat()
        if not stat.S_ISREG(st_fd.st_mode) or st_fd.st_ino != st_path.st_ino:
            raise InputLockError("input_lock_identity_invalid")
        if hasattr(os, "getuid") and st_fd.st_uid != os.getuid():
            raise InputLockError("input_lock_owner_invalid")
        os.fchmod(fd, 0o600)
        flags = fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB)
        fcntl.flock(fd, flags)
        yield
    finally:
        os.close(fd)
```

Translate `BlockingIOError` to `InputLockError("input_lock_busy")` and all unsafe path/identity conditions to typed fail-closed errors.

- [ ] **Step 4: Run tests and commit**

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
- Inputs: current task/session/token, current authoritative probe, task-private worker command/IPC endpoint.
- Output: safe status/reason only; raw runtime identity stays inside the transaction.

- [ ] **Step 1: Write failing supervisor tests**

Add deterministic tests proving:

```python
def test_guarded_dispatch_requires_current_registration_and_generation(): ...
def test_guarded_dispatch_holds_canonical_flock_and_input_lock_before_ready(): ...
def test_guarded_dispatch_revalidates_gate_b_after_input_lock(): ...
def test_abort_before_commit_runs_zero_effects(): ...
def test_commit_runs_worker_effect_at_most_once(): ...
def test_lease_generation_change_before_commit_refuses(): ...
def test_worker_descendant_keeps_serialization_until_exit(): ...
def test_cancellation_before_commit_runs_zero_effects(): ...
def test_unknown_worker_outcome_is_ambiguous_not_retryable(): ...
```

Use only fake probe/worker scripts and temporary state. No Official client access.

- [ ] **Step 2: Run RED**

```bash
PYTHONPATH=. python3 .github/scripts/test_tibia_official_client_re_canonical_live_transition.py -v
```

Expected: new operation absent.

- [ ] **Step 3: Load the input-lock helper without duplicating it**

Use `importlib.util.spec_from_file_location()` exactly as the transition script already loads the canonical guard. Add a helper `_input_lock()` returning the module.

- [ ] **Step 4: Implement `_guarded_dispatch()` inside the existing supervisor**

Ordering inside the already flock-owning `_child()` transaction:

```text
current lease validated by _child
-> _probe_reg(... old=False) / current Gate B
-> acquire canonical input lock
-> _probe_reg(... old=False) again after input lock
-> start task-private semantic worker in READY-only mode
-> verify worker READY envelope binds action hash + fence digest
-> wait for COMMIT/ABORT from Control Center-side bridge
-> on ABORT: worker exits with zero effect
-> on COMMIT: revalidate lease + registration identity once more
-> allow exactly one worker effect
-> collect immediate reconciliation classification
-> wait for worker and descendants to exit
-> release input lock
-> existing supervisor releases canonical flock
```

Do not pass the lease token, flock fd or input-lock fd to the worker (`close_fds=True`).

- [ ] **Step 5: Make parser explicit and fail closed**

Add `guarded-dispatch` to the parser but require explicit worker/probe/IPC arguments. The transition script must not discover arbitrary worker commands from environment variables.

- [ ] **Step 6: Run transition/guard/lease regression suites**

```bash
PYTHONPATH=. python3 .github/scripts/test_tibia_official_client_re_canonical_live_transition.py -v
PYTHONPATH=. python3 .github/scripts/test_tibia_official_client_re_canonical_live_guard.py -v
PYTHONPATH=. python3 .github/scripts/test_tibia_official_client_re_canonical_live_lease.py -v
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add .github/scripts/tibia-official-client-re-canonical-live-transition.py \
        .github/scripts/test_tibia_official_client_re_canonical_live_transition.py
git commit -m "feat(track-a): add guarded Control Center dispatch transaction"
```

---

### Task 5: Bind the semantic adapter to the Track A guarded transaction without raw-handle leakage

**Files:**
- Modify: `tools/tibia_re_control_center/official_adapter.py`
- Modify/Test: `tests/tools/tibia_re_control_center/test_package_d_official_adapter.py`
- Create only if needed after repository search: `tools/tibia_re_control_center/track_a_authority_bridge.py`

**Interfaces:**
- Produces `CanonicalTrackAAuthorityBridge` implementing `TrackAAuthorityBridge`.
- Bridge launches only the repository-owned transition operation and exchanges a strict JSONL handshake over private local pipes/Unix socket.

- [ ] **Step 1: Write failing transport-boundary tests**

```python
def test_bridge_command_is_fixed_repository_transition_entrypoint(): ...
def test_bridge_never_serializes_token_contents(): ...
def test_ready_envelope_contains_only_action_hash_and_fence_digest(): ...
def test_result_envelope_rejects_unknown_fields_and_raw_handle_names(): ...
def test_bridge_timeout_before_commit_is_not_dispatched(): ...
def test_bridge_timeout_after_commit_is_ambiguous(): ...
```

- [ ] **Step 2: Implement strict envelopes**

Use exact schemas:

```python
READY_KEYS = {"type", "action_hash", "fence_digest"}
RESULT_KEYS = {"type", "outcome", "reason_code", "evidence_refs"}
ALLOWED_OUTCOMES = {"confirmed", "ambiguous"}
```

Reject extra fields and reject keys containing `pid`, `xid`, `display`, `token`, `coordinate`, `address`, `pointer`, `opcode`, `keycode`, `window`.

- [ ] **Step 3: Implement fixed command construction**

The bridge accepts token *path* but never reads token contents. Build the transition command from repository-owned script path plus explicit task/session/token-file/probe/worker/IPC arguments. No `shell=True`.

- [ ] **Step 4: Run fake E2E through `MutationCoordinator`**

Construct:

```text
ActionRequest(turn)
-> coordinator reserve
-> OfficialTibiaAdapter advisory preflight
-> fake CanonicalTrackAAuthorityBridge guarded session
-> READY
-> coordinator commit_dispatch
-> exactly one fake effect
-> confirmed reconciliation
-> ActionResult CONFIRMED/PASS
```

Then repeat with ambiguous reconciliation and STOP between READY and commit.

- [ ] **Step 5: Full test/audit pass**

```bash
python3 -m compileall -q tools/tibia_re_control_center tests/tools/tibia_re_control_center .github/scripts
PYTHONPATH=. python3 -m unittest discover -s tests/tools/tibia_re_control_center -v
PYTHONPATH=. python3 tests/tools/tibia_re_control_center/audit_package_a.py
PYTHONPATH=. python3 tests/tools/tibia_re_control_center/audit_package_a_p1.py
ruff check tools/tibia_re_control_center
```

Expected: current Package A regressions remain green; new Package D tests prove zero physical runtime access.

- [ ] **Step 6: Commit**

```bash
git add tools/tibia_re_control_center tests/tools/tibia_re_control_center
git commit -m "feat(control-center): bridge Official adapter to Track A guard"
```

---

### Task 6: Revalidate shared governance and make the input lock normative

**Files:**
- Revalidate before editing: `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`
- Revalidate before editing: `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md`
- Revalidate before editing: `docs/agents/MODULE_CATALOG.md`
- Revalidate before editing: `docs/agents/CHANGELOG.md`
- Modify: `docs/agents/tasks/active/OTC-20260823-tibia-re-control-center-package-d.md`

**Interfaces:**
- Produces current governance text stating that canonical GUI mutation must hold the reviewed canonical input lock in addition to, but distinct from, Track A mutation authority.

- [ ] **Step 1: Re-query open PR changed files and active ownership for all four shared paths**

If any path has an unresolved current owner, do not edit it; record `DEFERRED_EXISTING_OWNER_<PR/TASK>` in the active task and keep physical dispatch blocked if the missing normative change is required for safety.

- [ ] **Step 2: If unowned, update Track A admission contract narrowly**

Add the input-lock requirement only to canonical GUI mutation semantics; explicitly state:

```text
input.lock serializes GUI/input actors but grants no lease, registration, Gate B,
mutation, login, credential or gameplay authority. Failure to acquire it is a
mutation refusal. It must be held by the external Track A supervisor through
final target validation, commit, physical effect and immediate reconciliation.
```

- [ ] **Step 3: Update Adapter v1 narrowly**

Reference the concrete canonical input lock and `guarded-dispatch` transaction without exposing their raw path/handles through semantic APIs.

- [ ] **Step 4: Update catalogue/changelog only if live ownership permits**

Record reusable `OfficialTibiaAdapter`, canonical input lock and guarded-dispatch transaction.

- [ ] **Step 5: Update task checkpoint**

Record exact implementation heads/tests and preserve:

```yaml
runtime_access: none
mutation_authorized: false
first_action_status: NOT_YET_PHYSICALLY_PROVEN
```

- [ ] **Step 6: Commit docs/governance changes**

Use `docs(...)` conventional commit and do not mix unrelated shared-file cleanup.

---

### Task 7: Exact-head repository validation before any runtime admission

**Files:** no new production files unless a validation repair is necessary.

- [ ] **Step 1: Review complete PR diff and changed-file list**

Verify there are no unrelated files, raw runtime handles, credentials, secret-bearing evidence, proprietary assets or unexpected workflow changes.

- [ ] **Step 2: Run/observe exact-head GitHub checks**

Required at minimum:

```text
CI
TIBIA RE Control Center Package A / Package A deterministic core
TIBIA RE Control Center Package A / Fresh Package A falsification audit
Track A agent runtime governance
Track A canonical-live governance when triggered by Track A script changes
```

- [ ] **Step 3: Inspect failures by job/step/log and repair root cause**

Do not rerun identical deterministic failures without a code/governance change.

- [ ] **Step 4: Keep PR Draft after repository green**

Repository green is not runtime authority and does not promote any action.

---

### Task 8: Fresh Track A runtime admission and conditional first-slice proof

**Files:**
- Modify first: `docs/agents/tasks/active/OTC-20260823-tibia-re-control-center-package-d.md`
- Evidence only after legal runtime access: `docs/agents/evidence/OTC-20260823-tibia-re-control-center-package-d/**`

**Interfaces:**
- Consumes current live Track A lease/registration/rebind/Gate B/runtime ownership.
- Produces either a fresh legal `canonical_reuse_or_mutation` admission or a precise fail-closed blocker.

- [ ] **Step 1: Re-read current trusted `main`, admission contract and all open Track A runtime owners**

Do not reuse the design-start SHA. Re-evaluate PR #475 or any successor current owner; Package D must not observe/mutate another task's runtime surface.

- [ ] **Step 2: Persist the complete current admission record before live observation**

Required shape:

```yaml
track_id: official-client-re
runtime_access: canonical_reuse_or_mutation | canonical_rebind | canonical_bootstrap | none
runtime_owner_task: OTC-20260823-tibia-re-control-center-package-d | NOT_APPLICABLE
runtime_namespace: canonical-live-runtime | NOT_APPLICABLE
canonical_registration: PRESENT | ABSENT | UNKNOWN
canonical_lease_generation: <integer | UNKNOWN>
registration_lease_generation: <integer | UNKNOWN>
gate_a: PASS | REQUIRED_NOT_PROVEN | NOT_APPLICABLE
generation_rebind: PASS | REQUIRED_UNAVAILABLE | REQUIRED_NOT_PROVEN | NOT_APPLICABLE
gate_b: PASS | REQUIRED_NOT_PROVEN | NOT_APPLICABLE
bootstrap: PASS | REQUIRED_UNIMPLEMENTED | REQUIRED_NOT_PROVEN | NOT_APPLICABLE
target_uniqueness: PROVEN | UNKNOWN | NOT_APPLICABLE
mutation_authorized: true | false
```

Any required UNKNOWN/REQUIRED_* value means no mutation.

- [ ] **Step 3: If current runtime is not legally reusable, stop physical work without weakening gates**

Valid terminal blocker examples:

```text
BLOCKED_RUNTIME_OWNED_BY_OTHER_TASK
BLOCKED_NO_CURRENT_REGISTERED_RUNTIME
BLOCKED_REBIND_REQUIRED
BLOCKED_GATE_B_NOT_PROVEN
BLOCKED_INPUT_LOCK_NOT_NORMATIVE
BLOCKED_NO_CURRENT_ACTIVE_WORLD_SEMANTIC_PROOF
```

Continue only repository/static evidence work that does not touch the runtime.

- [ ] **Step 4: If admission is legal, prove `turn` semantics before promotion**

Require current evidence for exact semantic path, reference UI parity, one-effect bound, no movement side effect, required input lock and authoritative facing-direction confirmation. Do not infer these from Package D PREP.

- [ ] **Step 5: Promote exactly `turn` only if all proof is current**

Persist one `OfficialCapabilityPromotion`-equivalent sanitized evidence record. `move` remains unsupported.

- [ ] **Step 6: Execute exactly one Control Center physical E2E**

Use the real domain path:

```text
ActionRequest(turn)
-> budget reserve
-> external Track A guarded-dispatch
-> input lock
-> final current Gate B/identity
-> READY
-> commit_dispatch COMMITTED
-> one physical turn
-> authoritative facing-direction reconciliation
-> CONFIRMED/PASS
```

No manual key press/direct worker invocation counts as E2E.

- [ ] **Step 7: If post-COMMIT confirmation is uncertain, record AMBIGUOUS and stop**

Do not retry the action automatically and do not promote a successful first slice from ambiguous evidence.

---

### Task 9: Closeout, review and merge

**Files:**
- Create/update: `docs/agents/evidence/OTC-20260823-tibia-re-control-center-package-d/**`
- Archive: `docs/agents/tasks/archive/OTC-20260823-tibia-re-control-center-package-d.md`
- Delete after archive commit: `docs/agents/tasks/active/OTC-20260823-tibia-re-control-center-package-d.md`

- [ ] **Step 1: Record exact validation/runtime result**

The evidence must distinguish one of:

```text
PHYSICAL_SLICE=CONFIRMED_PASS
PHYSICAL_SLICE=BLOCKED_WITH_REASON
PHYSICAL_SLICE=AMBIGUOUS_NO_RETRY
```

Never claim physical compatibility from fake E2E.

- [ ] **Step 2: Run fresh independent validation required by repository policy**

Inspect exact-head CI, deterministic falsification, review comments/threads and any central Spark advisory result that the repository automation actually produced. Do not invoke direct Codex/Spark from this task unless separate current-task authorization is added.

- [ ] **Step 3: Mark Ready only when all merge gates are satisfied**

A repository-complete but runtime-blocked Package D may merge only if its behavior is explicitly fail-closed and the task acceptance allows a blocked physical slice; it must not advertise an action as supported.

- [ ] **Step 4: Squash merge, archive task and verify final main**

Record implementation head, merge SHA, checks, findings, runtime admission/result and remaining next action.
