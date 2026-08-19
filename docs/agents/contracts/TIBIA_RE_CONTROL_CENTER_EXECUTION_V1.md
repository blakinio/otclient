# TIBIA RE Control Center Execution Contract v1

```yaml
contract_id: TIBIA-RE-CONTROL-CENTER-EXECUTION-V1
version: 1.2
major_version: 1
status: normative_design
producer_repository: blakinio/otclient
runtime_authority: external
runtime_access_of_this_document: none
scenario_semantics: docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_SCENARIO_V1.md
```

## 1. Purpose

Define the concurrency, dispatch, cancellation, idempotency, side-effect accounting, recorder, privacy, artifact and crash-recovery semantics for every Control Center implementation.

Normative separation:

```text
scenario validity
!= capability support
!= evidence maturity
!= observation freshness
!= mutation authority
```

No UI state, CLI option, scenario field, capability bit, cached authority status or prior preflight grants mutation authority.

For `OFFICIAL_TIBIA`, the then-current trusted-base Track A lease/registration/Gate A/rebind/Gate B/target-identity/GUI-input-lock/whole-lifetime-supervisor contracts remain the sole external mutation authority. This contract consumes them; it never replaces them.

Scenario parsing, canonical semantic request hashing, action parameter types and EffectBound semantics are defined by `TIBIA_RE_CONTROL_CENTER_SCENARIO_V1.md`.

## 2. Core identities

### 2.1 Backend epoch

Each backend process creates a fresh opaque `backend_epoch` unique across restarts. UUIDv4 or an equivalently collision-resistant identifier is acceptable.

A backend epoch is never reused.

### 2.2 Control generation

Within one backend epoch, `control_generation` is a monotonic unsigned integer.

`STOP ALL` advances it and latches STOP.

A control generation is meaningful only together with its backend epoch.

### 2.3 Adapter generation

Every adapter exposes an opaque `adapter_generation` that changes whenever adapter process/binding state changes in a way that can invalidate queued assumptions.

### 2.4 Runtime/session fences

Mutation requests may bind `runtime_instance_id` and `session_epoch`. A mismatch invalidates stale pending mutation.

## 3. MutationCoordinator

Each adapter instance has exactly one local `MutationCoordinator`.

It owns only Control Center-local execution safety:

- mutation serialization;
- action idempotency ledger;
- side-effect budget reservation/accounting;
- backend/control-generation fencing;
- STOP/reset linearization;
- one-shot dispatch commit;
- action lifecycle bookkeeping.

It does **not** own Track A lease, registration, Gate A, rebind, Gate B, target identity or official-client process authority.

## 4. Dispatch gate

The coordinator exposes one small local synchronization domain called `dispatch_gate`.

It linearizes only transitions that must be ordered against final mutation admission:

- final dispatch commit;
- STOP ALL;
- reset/other generation transitions when required.

Do not hold `dispatch_gate` while waiting for:

- external/Track A authority acquisition;
- GUI/input lock acquisition;
- remote/network I/O;
- captures/traces;
- ordinary artifact writes;
- sleeps/waits;
- adapter discovery.

### 4.1 Narrow durability exception

The **only** I/O permitted while holding `dispatch_gate` is the bounded local write-ahead durability transaction required to make `DISPATCH_COMMITTED/POSSIBLY_DISPATCHED` and the matching budget `AT_RISK` state durable before physical mutation.

That durability operation must:

- use a local store owned by the Control Center;
- have an explicit finite deadline;
- not depend on external network services;
- fail closed on timeout/error;
- never dispatch if durability is not proven.

This exception is necessary so STOP cannot linearize between the recorded possible-dispatch state and the decision to permit the physical effect.

## 5. Irreversible boundary and dispatch commit

The physical irreversible boundary is the first external input/call/operation after which the platform cannot prove that no game/runtime side effect occurred.

The Control Center defines a local durable **dispatch commit** immediately before that boundary.

`DISPATCH_COMMITTED` means:

```text
possible external effect must be assumed
no safe automatic retry exists
budget is at-risk
```

It does **not** mean the effect is proven to have occurred.

## 6. Immutable DispatchFence

Every mutation-capable action binds:

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

Official Track A authority/identity details remain official-adapter internals and are freshly evaluated from trusted-base sources at final dispatch. They do not become generic scenario fields.

Any changed required fence invalidates the pending action.

## 7. Action lifecycle

Every `action_id` has one durable logical record.

Non-terminal lifecycle:

```text
CREATED
VALIDATED
RESERVED
WAITING_AUTHORITY
DISPATCH_COMMITTED
DISPATCHING
CONFIRMING
CONFIRMED
```

Terminal/exceptional states:

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

`AMBIGUOUS` means the platform cannot prove whether the external effect occurred.

`AMBIGUOUS` is never automatically retried.

A callback/result from an older backend epoch, control generation, adapter generation, runtime instance or session epoch may be retained as evidence but cannot advance current execution.

## 8. Action idempotency

`action_id` is globally unique within the Control Center artifact namespace for one logical action attempt.

The ActionLedger stores the canonical `action_request_hash` defined by Scenario v1.

Rules:

- same action ID + same request hash -> return existing logical state/result; never dispatch again;
- same action ID + different request hash -> `REFUSED_IDEMPOTENCY_CONFLICT`;
- duplicate caller/API submission creates no second budget reservation;
- browser reload/CLI retry/HTTP retry does not create a second action when action ID is unchanged;
- a new explicit retry uses a new action ID and attempt index and requires new budget/fences/authority;
- automatic retry is forbidden after `DISPATCH_COMMITTED`, `DISPATCHING`, `CANCELLED_AFTER_DISPATCH`, `FAILED_AFTER_DISPATCH`, `TIMED_OUT_AFTER_DISPATCH` or `AMBIGUOUS`.

Transport/domain-request idempotency is additionally governed by `TIBIA_RE_CONTROL_CENTER_CONTROL_API_V1.md` for Package B.

## 9. Preparation phase

Preparation occurs outside `dispatch_gate` and may:

1. validate scenario/action;
2. resolve capabilities;
3. compute EffectBound and reserve budgets;
4. execute advisory preflight;
5. wait for/acquire adapter-specific external authority guard;
6. acquire shared GUI/input lock where required;
7. prepare before-state evidence.

Every wait is bounded and cancellation-aware.

Preparation never creates standing authority.

For `OFFICIAL_TIBIA`, any required Track A guard/supervisor is obtained here and remains continuously held across final Track A checks, local dispatch commit and physical mutation.

## 10. Final dispatch commit sequence

For mutation:

```text
prepare outside dispatch_gate
-> hold required external authority guard
-> enter local dispatch_gate
-> revalidate all local and external final fences
-> durably transition ActionLedger + BudgetLedger to possible-dispatch/at-risk
-> durability barrier succeeds
-> exit dispatch_gate
-> while external authority guard remains continuously held, cross physical irreversible boundary exactly once
-> reconcile result/evidence/budget
```

Inside `dispatch_gate`, verify immediately before the durable commit:

1. ActionLedger says this exact action/request is not previously committed;
2. expected backend epoch is current;
3. expected control generation is current;
4. STOP is not latched;
5. cancellation token is not cancelled;
6. adapter generation matches;
7. runtime/session fences match;
8. budget reservation is present and still valid;
9. semantic capability remains supported;
10. required external authority remains currently held/valid;
11. required GUI/input lock remains held when applicable;
12. for `OFFICIAL_TIBIA`, all current Track A final authority/identity requirements pass under the existing canonical guarded mutation boundary.

Then perform one atomic logical durability transaction containing at least:

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

If the transaction or durability barrier fails/times out, do not dispatch.

## 11. Adapter one-shot commit token

The adapter execution context exposes a one-shot coordinator-owned primitive conceptually equivalent to:

```text
commit_dispatch() -> COMMITTED | REFUSED
```

The adapter must not cross a mutation boundary unless this returns `COMMITTED` for that exact action.

A second invocation cannot produce another commit/effect authorization.

For Official Tibia, the external Track A guard remains continuously held through `commit_dispatch()` and the subsequent physical effect.

## 12. Crash between commit and effect

If the backend crashes after durable dispatch commit but before the physical effect can be proven:

```text
recovery = AMBIGUOUS
```

unless authoritative reconciliation proves either exact effect or exact no-effect.

This intentionally accepts false-positive ambiguity rather than risking duplicate mutation.

## 13. STOP ALL linearization

`STOP ALL` acquires the same `dispatch_gate` and:

1. increments `control_generation` with checked overflow handling;
2. latches `stop_state=STOPPED`;
3. records/persists the STOP transition according to the active storage model;
4. releases `dispatch_gate`;
5. cancels queued old-generation work;
6. signals cooperative cancellation to active waits/captures/actions;
7. performs bounded cleanup of harness-owned resources.

Required race semantics:

```text
STOP wins dispatch_gate
  -> generation changes before action commit
  -> stale commit is refused
  -> no physical mutation begins

Action commit wins dispatch_gate
  -> action is durably POSSIBLY_DISPATCHED / budget AT_RISK
  -> STOP later sees already-committed work
  -> no automatic retry and no claim that STOP reversed it
```

There is no valid third outcome.

STOP may request cancellation of an already-committed adapter operation but cannot promise rollback of an external effect.

STOP does not itself grant process-control/gameplay authority.

## 14. Adapter emergency-stop boundary

`adapter.emergency_stop()` is **not** a second mutation path.

It may only:

- cancel/wake harness-owned waits;
- close harness-owned passive capture streams/resources;
- release harness-owned local locks/tokens;
- signal cancellation to adapter-owned helper work that was already authorized.

It must not, merely because STOP was pressed:

- send a new gameplay movement/stop command;
- inject keyboard/mouse input;
- signal/kill/restart the official client;
- attach/detach a debugger/instrumentor;
- mutate network/proxy/client state;
- perform any new external action requiring authority.

If an external compensating action is desired, it is a separate semantic action with its own fresh authority, idempotency and side-effect budget. STOP itself never authorizes it.

## 15. Reset after STOP

STOP remains latched until explicit reset.

Reset is local state only and grants no external authority.

Reset requires:

- fresh backend/control state;
- fresh adapter/runtime status;
- stale callbacks fenced by backend/control generation;
- no unresolved ambiguity in an overlapping side-effect domain that would make the requested next action unsafe;
- fresh authority at every subsequent mutation commit.

Control-generation overflow fails closed; do not wrap/reuse a generation inside one backend epoch.

## 16. Pause/resume

Pause stops scheduling new steps.

Pause does not suspend:

- external lease expiry;
- backend/control/adapter/runtime/session changes;
- external clocks;
- an action already dispatch-committed;
- adapter deadlines unless explicitly supported.

Resume revalidates backend epoch, control generation, adapter generation, runtime instance, session epoch and all predicates marked `revalidate_on_resume`.

Changed runtime instance/session epoch invalidates pending mutations by default.

Every subsequent mutation is still freshly authorized at final commit.

## 17. Backend restart and recovery

Every backend restart creates a fresh backend epoch.

On restart:

- old-epoch callbacks/tokens cannot control new execution;
- mutation-capable runs do not auto-resume;
- external authority is reacquired/revalidated from current sources;
- durable action state is recovered before considering new work.

Durable dispatch classes:

```text
NOT_DISPATCHED
POSSIBLY_DISPATCHED
CONFIRMED
```

Recovery:

- no durable dispatch commit -> `NOT_DISPATCHED`; reconsider only via explicit recovery policy + fresh validation;
- durable possible-dispatch without terminal authoritative proof -> `AMBIGUOUS`;
- confirmed terminal authoritative result -> recover it;
- missing/corrupt/contradictory safety ledger -> fail closed, never synthesize PASS or silently recreate mutation.

## 18. Side-effect budget ledger

Each run tracks every hard dimension:

```yaml
BudgetDimension:
  limit: integer
  reserved: integer
  at_risk: integer
  committed: integer
  uncertain: integer
```

Availability:

```text
available = limit - reserved - at_risk - committed - uncertain
```

Use checked/overflow-safe arithmetic.

### 18.1 Reservation

Before dispatch preparation completes, obtain the Scenario-v1 `EffectBound` and reserve its maximum plausible effect.

If a hard effect cannot be safely bounded, refuse before dispatch.

### 18.2 Dispatch commit

In the same atomic logical transaction as `DISPATCH_COMMITTED`, move the relevant reservation from `reserved` to `at_risk`.

### 18.3 Reconciliation

- authoritative/proven no physical effect -> release at-risk amount;
- confirmed measured effect -> move measured amount to `committed`, release proven unused remainder;
- dispatched but exact effect unmeasurable -> conservatively commit maximum plausible bound;
- timeout/failure/cancel/ambiguity after commit -> move maximum plausible amount to `uncertain`;
- duplicate same action ID -> no new reservation/accounting;
- new explicit retry action -> new reservation.

`uncertain` counts as consumed until safely reconciled.

### 18.4 Minimum dimensions

```text
max_runtime_seconds
max_actions
max_movement_tiles
max_spells
max_consumables
max_items_moved
max_gold
max_tibia_coins
max_irreversible_changes
```

Tibia Coins and irreversible changes default to zero unless explicitly and separately authorized/bounded.

## 19. Capture-control boundary

Observation/capture configuration is not authority.

Normal read/capture operations may only start producers already proven passive under the current adapter/read authority.

If a requested capture requires any of:

- process attach/injection;
- debugger/instrumentation attach;
- GUI input/window activation that changes behavior;
- client/network/proxy mutation;
- process signals/restart;
- another invasive state transition;

then passive `capture_start()` must refuse with a typed requirement. The invasive enablement must be represented by a separately declared semantic control action/contract and pass the full MutationCoordinator/dispatch-commit/external-authority path.

Capture cleanup may close/release harness-owned resources but cannot create a new invasive operation.

## 20. Scenario determinism

The typed scenario language, parser limits, stable step IDs, predicate semantics, action parameter schemas, retries, semantic references, EffectBound and capture-policy shape are normative in `TIBIA_RE_CONTROL_CENTER_SCENARIO_V1.md`.

Execution-specific rules additionally require:

- unknown authority/safety predicates fail closed;
- mutation retries are only allowed after proven `NOT_DISPATCHED` and create a new action ID;
- no hidden retries;
- deterministic failure propagation unless an explicitly declared safe continuation exists.

## 21. Recorder ordering

One persisted event stream is an ingestion sequence, not a universal causal clock.

Every Event records:

```yaml
ingest_seq: integer
ingested_monotonic_ns: integer
source_timestamp: integer | string | null
source_clock_domain: string | null
source_sequence: integer | null
source_sequence_scope: string | null
ordering_confidence: KNOWN | PARTIAL | UNKNOWN
```

`ingest_seq` orders persistence inside one recorder instance only.

For Track A causal RE preserve, when observable:

```yaml
stimulus_id: string | BACKGROUND | null
message_direction: CLIENT_TO_SERVER | SERVER_TO_CLIENT | LOCAL | null
message_sequence: integer | null
message_type: string | null
connection_lane: string | null
thread_id: string | integer | null
handler: string | null
runtime_object: string | null
object_instance_epoch: string | null
before_state_hash: string | null
after_state_hash: string | null
semantic_delta: object | null
evidence_ref: string | null
```

Negative/no-stimulus controls remain experiment-level requirements.

Timestamp/ingestion correlation never auto-promotes causal proof.

## 22. Late events and finalization

Run lifecycle:

```text
ACTIVE -> CLOSING -> FINALIZED
```

On logical completion, enter bounded CLOSING and drain source watermarks where available.

Late events carry `late=true` and terminal-run context.

Late events may enrich evidence but cannot:

- change terminal action result;
- resume execution;
- authorize retry;
- rewrite finalized history.

After FINALIZED, later admitted evidence is append-only supplemental evidence referencing the original run.

## 23. Secret exclusion before object creation

Mandatory invariant:

> Secret-class data never enters the normal Event, Artifact, Error, Report or AgentBundle object graph.

Every ingestion boundary classifies before ordinary persistent-object construction.

Requirements:

- arbitrary exception/repr/debug text is untrusted and never directly becomes `safe_message`;
- persistent errors use stable reason codes, reviewed static messages and explicitly classified safe fields;
- environment-variable values are never enumerated/copied into evidence;
- auth/login packet payloads are structurally excluded from normal capture;
- trace strings are filtered before Event creation;
- private chat is omitted/redacted before Event creation unless explicitly test-generated and permitted;
- screenshots are admitted only when known non-secret or placed in quarantine outside normal run artifacts until sanitized/approved;
- `SECRET_REJECTED` contains category/reason only, never value/hash/reversible derivative.

Export-time redaction is defense in depth only.

## 24. Network metadata

Default persistent network capture:

```yaml
direction: CLIENT_TO_SERVER | SERVER_TO_CLIENT
lane: string | null
source_sequence: integer | null
message_type: string | null
size: integer
correlation_id: string | null
payload_capture: NONE
```

`message_type` is populated only when structurally known.

Raw payload fallback is forbidden.

Any future sanitized payload mode requires a separately approved capture policy proving secret exclusion before persistence.

## 25. Artifact durability

Per-run artifacts use staging/incomplete state followed by explicit finalization.

Minimum manifest provenance includes:

- schema versions;
- scenario hash;
- adapter identity/version;
- backend epoch/control generation;
- runtime/session/adapter fences;
- action ledger summary;
- budget ledger summary;
- privacy policy;
- artifact hashes;
- terminal/incomplete state.

The safety-critical dispatch journal/ActionLedger/BudgetLedger durability state is authoritative for duplicate-effect prevention and must not be erased or downgraded merely because report/event finalization fails.

PASS manifest/result is written only after required ledgers/events are flushed under the selected store guarantees.

Crash before finalization -> explicit incomplete run, never synthesized PASS.

Finalized historical result is immutable except explicit append-only supplements.

## 26. Control API relationship

Package B browser/CLI transport semantics, local nonce, Host/Origin policy, RequestLedger idempotency, request bounds, backpressure and shutdown are normative in `TIBIA_RE_CONTROL_CENTER_CONTROL_API_V1.md`.

Neither browser nor CLI may bypass this domain safety architecture by calling concrete adapters directly.

## 27. Generic versus official capability evidence

Generic adapters expose semantic support independently:

```yaml
GenericCapability:
  capability_id: string
  read_supported: bool
  action_supported: bool
  semantic_version: string
  source: string
  notes: string | null
```

Official Tibia additionally exposes Track A research maturity:

```yaml
OfficialEvidenceExtension:
  read_gate: NONE | R0 | R1 | R2 | R3 | R4
  action_gate: NONE | A0 | A1 | A2 | A3 | A4
  evidence_refs: [string]
```

Oteryn/fake adapters do not claim Track A evidence grades.

Read support never implies action support.

## 28. Surveyor integration

Surveyor is a producer dependency, not logic to copy.

Package C pins:

```yaml
surveyor_schema_version:
producer_commit:
producer_interface:
```

Unknown/incompatible producer -> explicit `SURVEYOR_UNAVAILABLE/INCOMPATIBLE`.

Control Center may reference Surveyor evidence/coverage but cannot silently promote/overwrite its source-of-truth records.

## 29. Oteryn v2 boundary

Oteryn v2 owns its shared native E2E architecture under accepted `docs/architecture/ADR-0007-native-end-to-end-test-platform.md`.

A future Oteryn adapter integrates with that platform or an explicitly versioned cross-repository semantic boundary. It must not create a second Oteryn scenario/authentication/server-mutation authority.

It retains `protocol-oteryn`; client sends semantic intent; server remains authoritative; test-only hooks remain excluded/locked down in production according to current Oteryn governance.

## 30. Differential comparison baseline

Comparison classes:

```text
EXACT
NORMALIZED_EXACT
SET_EQUIVALENT
ORDERED_EQUIVALENT
TOLERANCE
REFERENCE_ONLY
NOT_COMPARABLE
```

Default fields:

```text
position                 NORMALIZED_EXACT
hp                       NORMALIZED_EXACT
mana                     NORMALIZED_EXACT
conditions               SET_EQUIVALENT or profile NORMALIZED_EXACT
target_state              NORMALIZED_EXACT
inventory                 NORMALIZED_EXACT
containers                ORDERED_EQUIVALENT when order/index is semantic
equipment                 NORMALIZED_EXACT
cooldown_state            NORMALIZED_EXACT
cooldown_timing           TOLERANCE
visual_effect_semantics   REFERENCE_ONLY unless both expose stable semantics
pixel/frame output        NOT_COMPARABLE by default
latency                   TOLERANCE or REFERENCE_ONLY
protocol bytes            NOT_COMPARABLE
internal object layout    NOT_COMPARABLE
renderer implementation  NOT_COMPARABLE
```

Mismatch requires both sides to support/observe the field at the same normalized checkpoint, neither UNKNOWN, and candidate violation of the selected rule.

Missing reference observation is a coverage gap, not candidate failure.

## 31. Fake adapter normative behavior

Package A fake adapter uses deterministic manual clock/state scheduling and a deterministic durability store abstraction.

It must inject:

- read-only/mutation authority;
- capability support/refusal;
- backend/control/adapter/runtime/session generation changes;
- success/refusal;
- before-commit failure;
- dispatch-journal durability failure/timeout;
- crash after durable commit before effect;
- after-effect failure;
- ambiguity;
- timeout/cancellation;
- exact STOP-vs-dispatch-gate interleavings;
- STOP while waiting for external/fake authority;
- duplicate action IDs;
- deterministic side effects;
- multi-clock event sources;
- late events;
- secret-shaped rejected inputs;
- passive versus invasive capture classification;
- artifact incomplete/finalized states.

Fake success never proves official-client capability.

## 32. Package A acceptance matrix

Package A is valid only with `runtime_access:none`, no network listener and no official-client access.

Required deterministic tests include at minimum:

1. bounded scenario parser accept/reject, duplicate-key and unsafe-YAML rejection;
2. canonical scenario/action hashing and stable step IDs;
3. typed predicate UNKNOWN/type-mismatch semantics;
4. action-specific parameter validation;
5. unsupported capability refusal;
6. read-only mutation refusal;
7. stale backend epoch refusal;
8. authority loss exactly before commit;
9. runtime/session/adapter generation change before commit;
10. two mutation requests serialize;
11. same action ID/same request dispatches at most once;
12. same ID/different request conflict;
13. STOP wins dispatch gate -> no commit/effect;
14. commit wins dispatch gate -> durable possible-dispatch/at-risk before STOP;
15. STOP can linearize while another action waits for external authority because dispatch gate is not held;
16. dispatch-journal barrier failure/timeout -> no physical effect;
17. crash after durable commit before effect -> AMBIGUOUS/no retry;
18. backend restart -> fresh epoch and stale callback rejection;
19. pause/resume after runtime/session change refuses pending mutation;
20. engine timeout and cancellation while waiting;
21. before-commit versus after-commit cancellation classification;
22. budget reservation/exhaustion/overflow handling;
23. commit atomically moves budget reserved -> at-risk;
24. ambiguity conservatively consumes budget;
25. duplicate action creates no second budget reservation;
26. invasive capture request under read-only path is refused;
27. emergency-stop cannot create new gameplay/process mutation;
28. multi-clock events keep source/ingest ordering distinct;
29. late event cannot rewrite terminal result;
30. causal fields preserve supplied Track A evidence metadata;
31. secret-shaped event/error/trace rejected before normal construction;
32. screenshot risk path quarantined/refused;
33. artifact crash remains incomplete;
34. finalized artifact cannot be silently rewritten;
35. fake one-step experiment succeeds deterministically;
36. no operator-facing adapter bypass exists.

## 33. Compatibility

Execution major version 1 is additive-only.

Changing dispatch-commit ordering, STOP linearization, durability-before-effect, idempotency, budget ambiguity, secret-construction boundary or restart fencing requires a new major version or separately reviewed compatible extension.