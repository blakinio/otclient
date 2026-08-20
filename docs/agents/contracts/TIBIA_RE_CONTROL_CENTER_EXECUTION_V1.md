# TIBIA RE Control Center Execution Contract v1

```yaml
contract_id: TIBIA-RE-CONTROL-CENTER-EXECUTION-V1
version: 1.4
major_version: 1
status: normative_design
producer_repository: blakinio/otclient
runtime_authority: external
runtime_access_of_this_document: none
scenario_semantics: docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_SCENARIO_V1.md
artifact_semantics: docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ARTIFACT_V1.md
```

## 1. Purpose

Define concurrency, dispatch, cancellation, idempotency, side-effect accounting, recorder, privacy, artifact and crash-recovery semantics for every Control Center implementation.

Normative separation:

```text
scenario validity
!= capability support
!= evidence maturity
!= observation freshness
!= mutation authority
```

No UI state, CLI option, scenario field, API credential, capability bit, cached authority status or prior preflight grants mutation authority.

For `OFFICIAL_TIBIA`, then-current trusted-base Track A lease/registration/Gate A/rebind/Gate B/target identity/GUI input lock/whole-lifetime supervisor remain the sole external mutation authority.

Scenario typing/hashing/effect bounds are defined by Scenario v1. Durable backend-global and per-run safety/artifact structure is defined by Artifact v1.

## 2. Core identities and backend activation

Every backend lifetime creates a fresh opaque unique `backend_epoch`.

Within one backend epoch, `control_generation` is a checked monotonic unsigned integer. STOP advances it; overflow fails closed.

Every adapter exposes `adapter_generation`. Mutation may also bind `runtime_instance_id` and `session_epoch`.

Changed required identity/fence invalidates pending mutation.

Before a backend may admit mutation-capable work, it must load Artifact-v1 ControlState and durably mark `active_backend_epoch=<current backend_epoch>`. If an existing record still names a different prior active backend, the prior lifetime is unclean: set/preserve `recovery_required=true` and keep mutation disabled until explicit recovery/reset. Failure to persist the current backend-active marker disables mutation.

This marker is not Track A authority; it only prevents a crash or failed STOP persistence from becoming an implicit safety reset on the next backend lifetime.

## 3. MutationCoordinator

Each adapter instance has exactly one local `MutationCoordinator`.

It owns only Control Center-local execution safety:

- mutation-run ownership;
- mutation dispatch serialization;
- ActionLedger idempotency;
- BudgetLedger;
- durable backend-global STOP/reset/recovery ControlState;
- backend/control-generation fencing;
- STOP/reset linearization;
- one-shot durable dispatch commit;
- action lifecycle bookkeeping.

It never becomes Track A authority.

## 4. MutationRunLease

A scenario is `mutation_capable=true` when validation finds at least one executable step requiring `MUTATION` authority or another invasive control transition.

For each adapter there is at most one active mutation-capable run lease:

```yaml
MutationRunLease:
  adapter_id: string
  run_id: string
  backend_epoch: string
  acquired_control_generation: integer
```

Rules:

- acquire before scheduling the first mutation-capable step;
- while held, a second mutation-capable run on the same adapter is refused with `REFUSED_MUTATION_RUN_CONFLICT` by default;
- do not automatically queue a second mutation run;
- read-only runs may coexist only when all involved sources are proven concurrency-safe;
- unknown read concurrency safety means serialize/refuse;
- lease grants no external authority;
- STOP/abort/terminal run releases only local run ownership after bounded cleanup/accounting;
- a dispatch-committed/ambiguous action remains represented in ledgers after lease release and may block overlapping side-effect domains;
- backend epoch/control generation changes invalidate stale lease ownership.

This prevents interleaving two mutation scenarios such as `A1 -> B1 -> A2`.

## 5. Dispatch gate

The coordinator has one small local `dispatch_gate` used only to linearize:

- final dispatch commit;
- STOP ALL;
- reset/generation transitions when required.

Do not hold it while waiting for external/Track A authority, GUI/input locks, captures, network I/O, sleeps or adapter discovery.

Backend-start activation happens before mutation admission; clean-shutdown marker persistence happens after new mutation admission is closed. Those lifecycle writes therefore do not compete with an admitted action for dispatch linearization.

### 5.1 Narrow durability exceptions

The only I/O permitted while holding `dispatch_gate` is one of these bounded local safety transactions:

1. the dispatch write-ahead transaction that atomically records:

```text
DISPATCH_COMMITTED
POSSIBLY_DISPATCHED
budget AT_RISK
```

2. the backend-global ControlState transaction that durably latches STOP or durably clears STOP/recovery-required state during an explicit reset.

Both transactions have a finite deadline, no external network dependency and fail closed. Dispatch durability timeout/error means no physical dispatch. STOP durability timeout/error leaves the in-memory latch STOPPED and disables further mutation/reset progress until durable state is safely reconciled. Reset durability timeout/error leaves STOP/recovery-required state blocking mutation.

No arbitrary artifact/report/capture I/O is permitted under `dispatch_gate`.

## 6. Irreversible boundary

The physical irreversible boundary is the first external operation after which no-effect can no longer be proven.

The durable local dispatch commit occurs immediately before this boundary.

`DISPATCH_COMMITTED` means possible effect must be assumed, budget is at-risk and automatic retry is unsafe. It does not prove the effect occurred.

## 7. DispatchFence

```yaml
DispatchFence:
  action_id: string
  run_id: string
  step_id: string
  expected_backend_epoch: string
  expected_control_generation: integer
  expected_adapter_generation: string
  expected_runtime_instance_id: string | null
  expected_session_epoch: string | null
  required_capability: string
  required_authority: READ_ONLY | MUTATION
```

Official Track A authority/identity details remain current adapter-specific inputs, not generic scenario fields.

## 8. Action lifecycle

Non-terminal:

```text
CREATED
VALIDATED
RESERVED
WAITING_AUTHORITY
DISPATCH_COMMITTED
DISPATCHING
CONFIRMING
```

Terminal success:

```text
CONFIRMED
```

Terminal/exceptional:

```text
REFUSED
CANCELLED_BEFORE_DISPATCH
CANCELLED_AFTER_DISPATCH
FAILED_BEFORE_DISPATCH
FAILED_AFTER_DISPATCH
TIMED_OUT_BEFORE_DISPATCH
TIMED_OUT_AFTER_DISPATCH
AMBIGUOUS
```

`CONFIRMED` is the only successful terminal lifecycle state. An `ActionResult.status=PASS` is legal only when lifecycle state is `CONFIRMED` and the action's required confirmation/evidence policy is satisfied.

`AMBIGUOUS` means external effect cannot be proven either way and is never automatically retried. After `DISPATCH_COMMITTED`, cancellation/failure/timeout may use a more specific terminal state only when authoritative reconciliation establishes the required effect/no-effect semantics; otherwise the canonical terminal state is `AMBIGUOUS`.

Stale old-backend/generation/session/runtime callbacks may be evidence only, never current control input and never change a terminal lifecycle state.

## 9. Action idempotency

ActionLedger stores globally unique `action_id` plus Scenario-v1 canonical `action_request_hash`.

- same action ID/hash -> existing state/result, no second dispatch;
- same action ID/different hash -> `REFUSED_IDEMPOTENCY_CONFLICT`;
- duplicate submission -> no second budget reservation;
- explicit retry -> new action ID/attempt + fresh budget/fences/authority;
- auto-retry forbidden after dispatch commit or any possible-dispatch state.

Control API RequestLedger handles transport/domain request idempotency separately.

## 10. Preparation

Outside dispatch gate:

1. validate scenario/action;
2. resolve capability;
3. compute Scenario-v1 EffectBound and reserve external-effect budget;
4. verify the run monotonic runtime deadline has not expired;
5. run advisory preflight;
6. wait for/acquire external authority guard;
7. acquire required GUI/input lock;
8. prepare before-state evidence.

Every wait is bounded/cancellation-aware and cannot extend the run deadline. Preparation never grants standing dispatch permission.

For Official Tibia, Track A guard remains continuously held through final current Track A checks, local commit and physical effect.

## 11. Final commit sequence

```text
prepare outside dispatch_gate
-> hold required external authority guard
-> enter dispatch_gate
-> revalidate all final fences including runtime deadline
-> atomically/durably transition ActionLedger + external-effect BudgetLedger to possible-dispatch/at-risk
-> durability barrier succeeds
-> exit dispatch_gate
-> with external authority guard still held, cross physical irreversible boundary exactly once
-> reconcile result/evidence/budget
```

Inside dispatch gate verify immediately before commit:

1. exact action/hash not already committed;
2. matching active mutation-run ownership where mutation-capable;
3. backend epoch;
4. control generation;
5. durable + in-memory STOP/recovery-required/cancellation state;
6. adapter generation;
7. runtime/session fences;
8. run runtime deadline not expired;
9. valid external-effect budget reservation;
10. current semantic capability;
11. current external authority;
12. current input lock where required;
13. all current Official Tibia Track A final identity/authority requirements under the existing guard.

Durable commit minimum:

```yaml
backend_epoch:
control_generation:
action_id:
action_request_hash:
lifecycle_state: DISPATCH_COMMITTED
dispatch_state: POSSIBLY_DISPATCHED
budget_state: AT_RISK
adapter_generation:
runtime_instance_id:
session_epoch:
```

Failure/timeout -> no physical dispatch.

## 12. One-shot adapter commit token

Adapter execution receives coordinator-owned:

```text
commit_dispatch() -> COMMITTED | REFUSED
```

It is one-shot. Adapter must not cross the physical mutation boundary unless this exact action returned COMMITTED.

Official Tibia external Track A guard remains continuously held through commit and physical effect.

## 13. Crash after commit

Crash after durable dispatch commit but before physical outcome is known recovers as:

```text
AMBIGUOUS
```

unless authoritative reconciliation proves exact effect/no-effect.

The backend-active marker additionally ensures that an unclean process lifetime itself forces recovery-required state on the next backend before mutation admission.

Prefer false-positive ambiguity/recovery blocking over duplicate mutation.

## 14. STOP ALL

STOP acquires the same dispatch gate and:

1. computes the next checked control generation;
2. latches STOPPED in memory before any later mutation may commit;
3. durably writes backend-global Artifact-v1 `ControlState(stop_latched=true, control_generation=<next>, recovery_required=<preserved>)` under the gate;
4. commits the new generation only with that durable STOP state; on durability failure, remains in-memory STOPPED and mutation-disabled rather than reopening dispatch;
5. releases the gate;
6. cancels queued/waiting old-generation work;
7. signals cooperative cancellation;
8. boundedly cleans harness-owned resources.

Race:

```text
STOP wins gate -> stale action cannot commit -> no physical effect
commit wins gate -> possible-dispatch/at-risk already durable -> STOP treats action as already committed
```

No third dispatch outcome exists.

If STOP persistence fails and the backend subsequently crashes, the already-durable Artifact-v1 `active_backend_epoch` from backend activation causes the next backend to classify the prior lifetime as unclean and enter recovery-required/mutation-disabled state. Thus a storage failure cannot turn process restart into an implicit reset.

STOP cannot promise rollback and grants no gameplay/process-control authority. Repeating STOP while already latched is idempotent with respect to external gameplay effects; Control API request replay semantics additionally bind a repeated transport request to its original transition identity/result.

## 15. Emergency-stop boundary

`adapter.emergency_stop()` may cancel/wake harness-owned waits, close harness-owned passive captures, release local resources and signal already-authorized helper cancellation.

It must not use STOP to initiate:

- gameplay stop/movement/action;
- keyboard/mouse injection;
- client kill/signal/restart;
- debugger/instrumentation attach/detach;
- network/proxy/client mutation.

Any compensating external action is a separate semantic action with fresh authority/idempotency/budget.

## 16. Reset and recovery release

STOP remains durably latched across backend restart until explicit reset.

Reset acquires `dispatch_gate`, verifies the currently loaded durable STOP/recovery state, Action/Budget/RequestLedger recovery, unresolved ambiguity/budget restrictions and checked next control generation, then durably writes Artifact-v1 ControlState before exposing RUNNING or admitting new mutation.

A reset may clear `recovery_required` only when local persistent safety state is internally consistent and every unresolved possible-dispatch/ambiguous overlapping effect remains conservatively represented/blocked. It is not a data-loss escape hatch. If recovery cannot establish those invariants, reset refuses and mutation remains disabled.

Reset durability timeout/error leaves STOP/recovery-required state blocking mutation and returns a typed failure.

Reset grants no external authority, cannot reuse stale callbacks and must preserve unresolved ambiguous overlapping side-effect blocks. It does not clear ActionLedger/BudgetLedger uncertainty and cannot be used to bypass Track A authority.

Generation overflow or missing/corrupt contradictory ControlState fails closed as STOPPED/recovery-required/mutation-disabled.

## 17. Pause/resume

Pause stops scheduling new steps but does not suspend external authority expiry, identities, clocks or an already committed action. It also does not pause or extend the run's monotonic runtime deadline.

Resume revalidates backend/control/adapter/runtime/session fences, run deadline and declared predicates. Changed runtime/session or expired deadline invalidates pending mutation by default.

Every later mutation is freshly authorized at final commit.

## 18. Backend restart/recovery

Every restart creates a fresh backend epoch, rejects old-epoch callbacks as control input, does not auto-resume mutation runs and reacquires all external authority.

Startup order before mutation admission:

1. load/validate backend-global Artifact-v1 ControlState and RequestLedger plus relevant per-run safety state;
2. if the loaded `active_backend_epoch` names a prior backend, classify that prior lifetime as unclean and set/preserve `recovery_required=true`;
3. durably write current `active_backend_epoch=<new backend_epoch>` while preserving STOP/recovery truth;
4. recover Action/Budget/RequestLedger state conservatively, including the original run activation/deadline rather than granting fresh runtime time;
5. only when `stop_latched=false`, `recovery_required=false`, safety state is consistent, the run deadline is valid for any considered pending work and all other local/external gates pass may mutation admission become possible.

A durable `stop_latched=true` survives the new backend epoch and remains STOPPED until explicit reset. Restart is never an implicit reset. A prior unclean backend also blocks mutation until explicit recovery/reset. A previously initialized store with missing/corrupt/contradictory ControlState fails closed. A brand-new store must durably create its initial current-backend-active ControlState before mutation can be admitted.

Durable dispatch classes:

```text
NOT_DISPATCHED
POSSIBLY_DISPATCHED
CONFIRMED
```

- no durable commit -> NOT_DISPATCHED; reconsider only via explicit recovery + fresh validation and within the original run deadline;
- durable possible-dispatch without terminal proof -> AMBIGUOUS;
- confirmed terminal authoritative result -> recover `CONFIRMED` without redispatch;
- missing/corrupt/contradictory safety state -> fail closed.

Artifact-v1 safety-state precedence applies. Recovery never weakens STOP/recovery-required state, never extends the original runtime budget and never auto-resumes a mutation run.

### 18.1 Clean shutdown marker

After new mutation admission is closed and all required global/per-run safety state is durably flushed, a graceful shutdown may durably write `active_backend_epoch=null`. It must preserve `stop_latched` and `recovery_required` values. Failure to persist the clean-shutdown marker is safe: the next backend treats the prior lifetime as unclean and requires recovery rather than assuming clean state.

## 19. Runtime deadline and external-effect BudgetLedger

Scenario-v1 `max_runtime_seconds` is enforced as one monotonic run deadline:

```text
runtime_deadline = checked_add(run_started_monotonic, max_runtime_seconds)
```

Rules:

- derive the deadline once at run activation; overflow fails closed;
- every wait is capped by the earlier of its own timeout and the run deadline;
- pause, backend restart and external-authority waiting do not freeze or extend the deadline;
- deadline expiry stops new scheduling/dispatch and produces the scenario/run timeout path;
- elapsed runtime is not moved through `reserved/at_risk/committed/uncertain`, because time passage is not an ambiguous external effect;
- crash/recovery preserves the original run activation/deadline for any recovery decision; it never grants a fresh runtime window.

External-effect dimensions use:

```text
limit
reserved
at_risk
committed
uncertain
```

```text
available = limit - reserved - at_risk - committed - uncertain
```

Use checked non-negative arithmetic.

Reserve Scenario-v1 maximum plausible EffectBound before dispatch.

At dispatch commit, move reservation -> at-risk in the same atomic local safety transaction.

Reconciliation:

- authoritative/proven no effect -> release at-risk;
- measured confirmed effect -> commit measured, release proven remainder;
- dispatched but unmeasurable -> commit conservative maximum;
- timeout/fail/cancel/ambiguity after commit -> maximum -> uncertain;
- uncertain counts as consumed until reconciled;
- duplicate same action ID -> no additional accounting;
- retry action -> fresh reservation.

Core v1 external-effect dimensions:

```text
max_actions
max_movement_tiles
max_spells
max_consumables
max_items_moved
max_gold
max_tibia_coins
max_irreversible_changes
```

`max_actions` counts semantic actions that can cross an external-effect boundary, as defined by Scenario-v1 EffectBound; it is not a count of parser/refusal attempts. TC/irreversible default zero. Unbounded hard external effect -> refuse.

## 20. Capture-control boundary

Ordinary snapshot/wait/capture operations are observational only.

Passive capture may start only an already admitted passive producer.

If enabling capture requires attach/injection/input/process/network mutation, passive `capture_start()` refuses with a typed requirement. Invasive enablement must be a separately declared semantic control action/contract through the normal mutation path.

Capture cleanup may close harness-owned resources but cannot introduce a new invasive action.

## 21. Scenario semantics

Scenario-v1 parser limits, hashes, stable IDs, predicates, semantic selectors, action parameter schemas, retries, EffectBound and capture/privacy policies are normative.

Unknown authority/safety predicates fail closed. Mutation retry is allowed only after proven NOT_DISPATCHED and always uses a new action ID.

## 22. Recorder ordering/causal evidence

Every event preserves:

```yaml
ingest_seq: integer
ingested_monotonic_ns: integer
source_timestamp: integer | string | null
source_clock_domain: string | null
source_sequence: integer | null
source_sequence_scope: string | null
ordering_confidence: KNOWN | PARTIAL | UNKNOWN
```

Ingestion order is persistence order only.

For Track A causal RE preserve when observable:

```text
stimulus_id/BACKGROUND
message direction/sequence/type/lane
thread
handler/runtime object/object epoch
before/after state hash
semantic delta
evidence ref
```

Negative/no-stimulus controls remain experiment requirements. Timing correlation never auto-promotes causal proof.

## 23. Late events/finalization

```text
ACTIVE -> CLOSING -> FINALIZED
```

Bounded CLOSING drains sources/watermarks where possible.

Late events cannot change terminal action result, resume execution, authorize retry or rewrite finalized history.

Later accepted evidence is append-only supplement.

## 24. Secret exclusion

Mandatory:

> Secret-class data never enters normal Event, Artifact, Error, Report or AgentBundle objects.

Classification/redaction/rejection happens before ordinary persistent-object construction.

No raw arbitrary exception/repr/debug text, environment values, auth payloads, secret trace text, unapproved private chat, login/auth screenshot pixels or Control API nonce may enter ordinary artifacts.

`SECRET_REJECTED` contains category/reason only, never secret/hash/reversible derivative.

Export-time redaction is defense in depth only.

## 25. Network metadata

Default persistent network capture:

```text
direction
lane
source sequence when known
message type only when structurally known
size
correlation ID
payload_capture=NONE
```

No raw-payload fallback. Future payload mode requires separate approved sanitization policy before persistence.

## 26. Artifact durability

Artifact v1 defines backend-global ControlState/RequestLedger plus per-run Action/Budget/Recovery ledgers, manifest, event/action evidence, staging/finalization, screenshot quarantine, supplements and hashes.

Safety ledgers/control state have precedence over report/presentation. Presentation failure cannot downgrade STOP/recovery-required, possible-dispatch or at-risk state.

PASS is forbidden for unresolved ambiguous required mutation or incomplete required finalization/privacy/cleanup state.

## 27. Control API relationship

Package B transport semantics are normative in Control API v1.

Browser/CLI cannot bypass domain safety to concrete adapters.

## 28. Capability separation

Generic adapters expose `read_supported` and `action_supported` independently.

Official Tibia additionally exposes Track A R0-R4/A0-A4 evidence maturity with refs.

Oteryn/fake adapters do not claim Track A grades.

## 29. Surveyor/Oteryn boundaries

Surveyor integration pins schema + producer commit + interface and does not overwrite Surveyor-owned evidence.

Oteryn adapter integrates with current accepted Oteryn ADR-0007 or explicit versioned cross-repo semantics, retains `protocol-oteryn`, client intent/server authority and production test-hook isolation.

## 30. Differential comparison

`TIBIA_RE_CONTROL_CENTER_COMPARISON_V1.md` defines versioned field-level semantic comparison, coverage-gap semantics and mismatch rules.

No default byte-level protocol/internal-layout/renderer parity is required.

## 31. Package A fake requirements

Use deterministic manual clock/state scheduler and deterministic durability store capable of injecting:

- authority/capability states;
- backend/control/adapter/runtime/session changes;
- second mutation-run conflict;
- pre-commit/durability/post-commit failures;
- crash before/after effect;
- exact STOP-vs-commit interleavings;
- STOP persistence/restart/reset durability failures;
- backend-active marker write/clean-shutdown failures;
- unclean backend recovery-required semantics;
- runtime deadline expiry/overflow and pause/restart non-extension;
- STOP while waiting for authority;
- duplicate actions;
- external-effect budgets;
- passive/invasive capture distinction;
- multi-clock/late events;
- secret rejection;
- artifact incomplete/finalized state.

Fake success never proves official capability.

## 32. Required Package A execution tests

At minimum:

1. second active mutation-capable run on same adapter is refused;
2. read-only concurrency only when explicitly safe;
3. stale backend/control/adapter/runtime/session fences refuse commit;
4. duplicate action ID/hash dispatches once;
5. conflicting action hash refuses;
6. STOP wins gate -> no effect;
7. commit wins gate -> possible-dispatch/at-risk before STOP;
8. STOP linearizes while another action waits for external authority;
9. dispatch-journal failure/timeout -> no effect;
10. crash after durable commit -> AMBIGUOUS/no retry;
11. external-effect budget reserve/at-risk/commit/uncertain semantics;
12. arithmetic overflow fails closed;
13. runtime deadline expires while waiting and prevents later dispatch;
14. pause does not extend runtime deadline;
15. restart/recovery does not grant a fresh runtime deadline;
16. pause/resume stale identity refusal;
17. restart fresh epoch/stale callback refusal;
18. durable STOP latch survives restart and still refuses mutation;
19. reset durability failure leaves STOP/recovery blocking mutation;
20. missing/corrupt initialized ControlState fails closed;
21. backend activation marker must be durable before mutation admission;
22. crash with prior active-backend marker makes next backend recovery-required;
23. STOP persistence failure followed by crash cannot reopen mutation;
24. clean-shutdown marker failure causes conservative recovery-required next start;
25. invasive capture hidden in read path refused;
26. emergency-stop mutation attempt refused;
27. multi-clock ordering truthfulness;
28. late event cannot rewrite terminal result;
29. secret construction barriers;
30. artifact safety-state precedence/finalization;
31. `CONFIRMED` is terminal and duplicate callbacks cannot redispatch or rewrite it.

Scenario/Artifact/Control API contracts add their own deterministic acceptance tests.

## 33. Compatibility

Execution major version 1 is additive-only.

Changing mutation-run ownership, dispatch ordering, STOP linearization/durability, backend activation/recovery markers, runtime-deadline semantics, durability-before-effect, idempotency, external-effect budget ambiguity, secret construction boundary or restart fencing requires a new major version or separately reviewed compatible extension.