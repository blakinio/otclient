# TIBIA RE Control Center Execution Contract v1

```yaml
contract_id: TIBIA-RE-CONTROL-CENTER-EXECUTION-V1
version: 1.1
major_version: 1
status: normative_design
producer_repository: blakinio/otclient
runtime_authority: external
runtime_access_of_this_document: none
```

## 1. Purpose

This contract defines the concurrency, dispatch, cancellation, idempotency, budget, recorder, privacy, artifact and crash-recovery semantics that every Control Center implementation must obey.

It closes the gap between a valid semantic scenario and actual authority to perform a mutation.

Normative separation:

```text
scenario validity
!= capability support
!= evidence maturity
!= observation freshness
!= mutation authority
```

A scenario may be valid while its action is unsupported or unauthorized. No local UI, CLI flag, scenario field, cached status, prior preflight or adapter capability may create Track A mutation authority.

For `OFFICIAL_TIBIA`, current trusted-base Track A lease/registration/Gate A/rebind/Gate B/target-identity/GUI-lock/whole-lifetime-supervisor contracts remain the sole mutation authority. This contract consumes them; it never replaces them.

## 2. Core terms

### 2.1 Backend epoch

Every Control Center backend process creates a fresh opaque `backend_epoch` that is unique across restarts. UUIDv4 or an equivalently collision-resistant identifier is acceptable.

`backend_epoch` is never reused after restart.

### 2.2 Control generation

Within one `backend_epoch`, the backend owns a monotonic integer `control_generation`.

`STOP ALL` increments it and latches STOP.

A `control_generation` is meaningful only together with its `backend_epoch`.

### 2.3 MutationCoordinator

Each adapter instance has exactly one local `MutationCoordinator` responsible for:

- mutation serialization;
- action idempotency ledger;
- side-effect budget admission/reservation;
- `backend_epoch` / `control_generation` fencing;
- STOP/reset linearization;
- final local dispatch commit.

It does **not** own external Track A authority.

### 2.4 Dispatch gate

The coordinator exposes one very small local `dispatch_gate` synchronization domain used only to linearize:

- final dispatch commit;
- STOP ALL;
- other transitions that must be ordered against those operations.

Do not hold `dispatch_gate` while waiting for slow/external authority, I/O, capture, GUI locks or Track A coordination. This prevents STOP from being blocked behind unrelated waiting work.

### 2.5 Irreversible boundary

The physical irreversible boundary is the first external call/input/operation after which the platform cannot prove that no game/runtime side effect occurred.

The Control Center defines a **dispatch commit** immediately before this boundary.

## 3. Execution ownership and concurrency

Rules:

1. at most one mutation-capable action per adapter may cross dispatch commit at a time;
2. multiple read-only runs may execute concurrently only when every involved source is independently proven safe for concurrent use;
3. a mutating run never acquires standing authority for its lifetime; every mutation is independently re-authorized at final dispatch;
4. browser, CLI, scheduler and one-step experiments submit work through the same coordinator;
5. no operator-facing surface may call adapter mutation directly;
6. local locks/tokens are never substitutes for Track A authority;
7. unknown concurrency safety means serialize.

## 4. Immutable dispatch fence

Every validated action binds:

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

For the official adapter, final dispatch additionally checks every current Track A identity/authority fence required by trusted base. Those Track A fields stay adapter-specific and must not be copied into the generic scenario schema.

Changed backend epoch, control generation, adapter generation, runtime instance, session epoch or required Track A identity/authority fact invalidates pending mutation work.

## 5. Action ledger and lifecycle

Every action has one logical record keyed by `action_id`.

Required lifecycle states:

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

`DISPATCH_COMMITTED` is the local point of no safe automatic retry. It means the action has been durably classified `POSSIBLY_DISPATCHED` immediately before the physical irreversible boundary.

A crash after `DISPATCH_COMMITTED` but before the physical external call is conservatively recovered as `AMBIGUOUS` unless authoritative reconciliation proves no effect occurred.

`AMBIGUOUS` is never automatically retried.

A terminal callback from an older backend epoch, control generation, adapter generation, runtime instance or session epoch may be retained as evidence but cannot advance/resume current execution.

## 6. Idempotency and replay

`action_id` is a mandatory globally unique idempotency key for one logical action attempt within the Control Center artifact namespace.

The ledger also stores a canonical hash of the normalized semantic request.

Duplicate rules:

- same `action_id` + same normalized request hash -> return/replay existing logical state/result; never create another dispatch;
- same `action_id` + different normalized request hash -> `REFUSED_IDEMPOTENCY_CONFLICT`;
- duplicate transport/API submission never creates a second budget reservation;
- browser reload, CLI retry, repeated HTTP POST or connection loss do not create a new attempt if `action_id` is unchanged;
- a new explicit retry uses a new `action_id` and new budget admission;
- automatic retry after `DISPATCH_COMMITTED`, `DISPATCHING`, `AMBIGUOUS`, `FAILED_AFTER_DISPATCH`, `TIMED_OUT_AFTER_DISPATCH` or `CANCELLED_AFTER_DISPATCH` is forbidden.

The Control API must permit retrieval of existing action/run state by ID after transport loss.

## 7. Preparation phase

Before final dispatch commit the engine/coordinator may perform work outside `dispatch_gate`:

1. validate scenario/action schema;
2. resolve semantic capability;
3. reserve maximum plausible side effects;
4. evaluate advisory preflight;
5. wait for/acquire adapter-specific external authority guards;
6. obtain shared GUI/input lock when required;
7. prepare normalized before-state evidence.

All blocking waits must be cancellation-aware and bounded.

Preparation never grants standing dispatch authority.

For `OFFICIAL_TIBIA`, Track A guard/supervisor acquisition may occur here, but the guard must remain held across final dispatch commit and physical irreversible dispatch.

## 8. Final dispatch commit

The race-safe sequence is normative.

For a mutating action:

```text
prepare outside dispatch_gate
-> hold adapter-specific external authority/Track A guard if required
-> enter local dispatch_gate
-> revalidate all final fences
-> durably write DISPATCH_COMMITTED / POSSIBLY_DISPATCHED + at-risk budget state
-> durability barrier succeeds
-> exit local dispatch_gate
-> while external authority guard is still continuously held, cross physical irreversible boundary once
-> reconcile result/evidence
```

Inside `dispatch_gate`, immediately before durable dispatch commit, verify:

1. action ledger is still dispatchable and not previously committed;
2. request hash matches ledger identity;
3. expected `backend_epoch` equals current backend epoch;
4. expected `control_generation` equals current generation;
5. STOP is not latched;
6. cancellation token is not cancelled;
7. adapter generation matches;
8. runtime instance/session epoch match;
9. budget reservation remains valid;
10. capability remains supported;
11. required external authority is currently held/valid;
12. for `OFFICIAL_TIBIA`, current Track A authority/identity checks pass while the existing canonical guarded mutation boundary remains continuously held;
13. required GUI/input lock is held when applicable.

Then the coordinator performs the dispatch write-ahead commit.

### 8.1 Write-ahead requirement

Before physical irreversible dispatch, persistent Package B+ implementations must durably record at least:

```yaml
backend_epoch:
control_generation:
action_id:
request_hash:
lifecycle_state: DISPATCH_COMMITTED
dispatch_state: POSSIBLY_DISPATCHED
budget_state: AT_RISK
runtime/session/adapter fence summary:
```

and complete the storage durability barrier appropriate to the chosen store.

If this persistence/barrier fails, **do not dispatch**.

Package A may use a deterministic in-memory durability model, but its tests must exercise barrier success/failure and restart recovery semantics.

### 8.2 Physical dispatch after commit

Once `DISPATCH_COMMITTED` succeeds, the external side-effect call happens exactly once and as immediately as practicable while the same external Track A/adapter authority guard remains held.

If the process crashes between commit and physical call, recovery remains conservative: `AMBIGUOUS` unless authoritative reconciliation proves no effect occurred.

This intentionally prefers possible false-positive ambiguity over unsafe duplicate mutation.

## 9. STOP ALL linearization

`STOP ALL` linearizes by acquiring the same local `dispatch_gate`, then:

1. increment `control_generation`;
2. latch `stop_state=STOPPED`;
3. persist/record the new STOP state as required by the current storage model;
4. release `dispatch_gate`;
5. cancel queued old-generation work;
6. signal cooperative cancellation to active waits/captures/actions;
7. cleanup harness-owned resources within bounded limits.

Required race result:

```text
STOP acquires dispatch_gate first
  -> generation increments
  -> stale action cannot DISPATCH_COMMIT
  -> physical mutation does not begin

Action DISPATCH_COMMIT acquires dispatch_gate first
  -> action becomes POSSIBLY_DISPATCHED durably
  -> STOP later classifies it as already committed/in-flight
  -> no automatic retry or fiction that STOP undid it
```

There is no third outcome.

`STOP ALL` may request cancellation of already-committed work, but cannot promise reversal of an external effect.

`STOP ALL` never kills the official client unless separate current process-control authority explicitly permits that exact effect.

## 10. Reset after STOP

STOP is latched.

A reset is local Control Center state only; it does not create external authority.

Reset requires:

- no stale callback is capable of being accepted into the new generation;
- fresh runtime/adapter status;
- explicit new current control generation state;
- no unresolved ambiguous action whose side-effect domain would make subsequent requested actions unsafe;
- fresh external authority at every future mutation dispatch.

An old `AMBIGUOUS` action may block overlapping side-effect domains until authoritative reconciliation or explicit safe disposition.

## 11. Pause and resume

Pause stops scheduling new scenario steps. It does not suspend:

- lease expiry;
- session/runtime/adapter generation changes;
- external clocks;
- an action already beyond dispatch commit;
- adapter deadlines unless the adapter explicitly supports pausable deadlines.

Resume revalidates:

- backend epoch;
- control generation;
- adapter generation;
- runtime instance;
- session epoch;
- scenario predicates marked `revalidate_on_resume`;
- all subsequent mutation authority at final dispatch.

Changed runtime instance or session epoch invalidates pending mutation steps by default.

Scenario-engine owned waits use documented monotonic active-run time; external deadlines use their own monotonic clock policy.

## 12. Backend restart and crash recovery

On every backend restart:

- create a new unique `backend_epoch`;
- initialize a fresh local control-generation scope;
- do not accept callbacks/tokens from the old backend epoch as control input;
- do not automatically resume mutation-capable scenarios;
- reacquire/revalidate all external authority from current sources.

Durable action state must distinguish:

```text
NOT_DISPATCHED
POSSIBLY_DISPATCHED
CONFIRMED
```

Recovery rules:

- state before durable dispatch commit -> `NOT_DISPATCHED`; action may only be reconsidered after explicit run recovery policy and fresh validation;
- durable `DISPATCH_COMMITTED`/`POSSIBLY_DISPATCHED` without authoritative terminal proof -> `AMBIGUOUS`;
- `AMBIGUOUS` -> no automatic retry;
- confirmed authoritative result -> recover terminal result;
- missing/corrupt ledger or contradictory evidence -> fail closed, never synthesize PASS.

## 13. Side-effect budget ledger

Every run has a ledger per budget dimension:

```yaml
BudgetDimension:
  limit: integer
  reserved: integer
  at_risk: integer
  committed: integer
  uncertain: integer
```

Admission uses:

```text
available = limit - reserved - at_risk - committed - uncertain
```

with checked/overflow-safe arithmetic.

### 13.1 Reservation

Before dispatch preparation completes, reserve the action's maximum plausible effect for every applicable dimension.

If a safe maximum cannot be derived for a hard budget, refuse the action.

### 13.2 Dispatch commit accounting

At durable dispatch commit, move the relevant reservation from `reserved` to `at_risk` in the same durable logical transaction as `DISPATCH_COMMITTED`.

This ensures a backend crash cannot forget an action that may have produced a side effect.

### 13.3 Reconciliation

- proven no physical dispatch/effect -> release `at_risk` only with authoritative/proven no-effect evidence;
- confirmed measured effect -> move measured amount to `committed`, release proven unused remainder;
- physical dispatch but exact effect not measurable -> conservatively move maximum plausible amount to `committed`;
- timeout/failure/cancellation/uncertain result after dispatch commit -> move maximum plausible amount to `uncertain`;
- duplicate same `action_id` -> no second reservation/accounting;
- explicit new retry action -> new reservation.

`uncertain` counts as consumed for future admission until safely reconciled.

### 13.4 Minimum dimensions

```text
max_runtime_seconds       bounded deadline policy
max_actions               maximum one logical dispatch attempt per action ID
max_movement_tiles        maximum possible requested displacement
max_spells                1 per spell dispatch unless action contract proves otherwise
max_consumables           maximum units one action may consume
max_items_moved           maximum count/stack amount at risk
max_gold                  must have safe maximum delta or refuse
max_tibia_coins           hard default 0
max_irreversible_changes  hard default 0; any irreversible operation reserves >=1
```

Budgets are safety gates, not reporting decoration.

## 14. Typed scenario semantics

Every scenario has `schema_version`.

Stable step IDs are deterministic from normalized scenario identity + ordinal/declared identity and never depend on runtime timing.

Typed predicate baseline:

```yaml
Predicate:
  field: string
  op: EQ | NE | LT | LTE | GT | GTE | EXISTS | NOT_EXISTS | CHANGED | UNCHANGED | IN_SET | CONTAINS
  value: scalar | list | null
  unknown_policy: FAIL | WAIT | ACCEPT
```

Rules:

- unknown never silently compares equal to a concrete value;
- mutation preconditions default `FAIL` on unknown;
- assertions default `FAIL` on unknown;
- waits may use `WAIT` until timeout;
- `ACCEPT` is explicit and forbidden for mutation-authority/safety predicates;
- mutation retries default to `0`;
- failure propagation is deterministic and terminal unless an explicitly safe continuation path exists.

## 15. Recorder clocks and ordering

A unified event stream is an **ingestion sequence**, not a universal causal clock.

Every event preserves:

```yaml
EventOrdering:
  ingest_seq: integer
  ingested_monotonic_ns: integer
  source_timestamp: integer | string | null
  source_clock_domain: string | null
  source_sequence: integer | null
  source_sequence_scope: string | null
  ordering_confidence: KNOWN | PARTIAL | UNKNOWN
```

`ingest_seq` orders persistence inside one recorder instance only.

For causal RE preserve when observable:

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

Timestamp correlation alone never auto-promotes causal proof.

## 16. Late events and run finalization

Run lifecycle:

```text
ACTIVE -> CLOSING -> FINALIZED
```

At logical completion the recorder enters bounded `CLOSING`, drains sources where possible and records source watermarks.

Events arriving after logical terminal state carry `late=true` and terminal-run context.

Late events may enrich evidence but cannot:

- change terminal action result;
- resume execution;
- authorize retry;
- rewrite finalized historical result.

After `FINALIZED`, later admitted evidence is an append-only supplement referencing the original run.

## 17. Secret exclusion before object creation

Mandatory invariant:

> Secret-class data never enters the normal Event, Artifact, Error, Report or AgentBundle object graph.

Every ingestion boundary classifies before constructing ordinary persistent objects.

Required controls:

- arbitrary exception/repr/debug text is untrusted and cannot directly become `safe_message`;
- persistent errors use stable reason codes, reviewed static messages and explicitly classified safe fields;
- environment-variable values are never enumerated into artifacts;
- auth/login packet payloads are structurally excluded from normal capture;
- trace strings are filtered before Event creation;
- private chat is omitted/redacted before Event creation unless deliberately generated test text is permitted;
- screenshots are admitted only when capture context is known non-secret or enter quarantine outside normal run artifacts until sanitized/approved;
- `SECRET_REJECTED` may contain category/reason only, never the secret value, hash or reversible derivative.

Export-time redaction is defense in depth only.

## 18. Network metadata policy

Default persistent network event:

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

Any future sanitized/non-secret payload mode requires separate explicit capture-policy approval proving secret exclusion before persistence.

## 19. Control API idempotency and bounds

Browser and CLI use the same domain service. Neither calls adapters directly.

Package B exposes one explicit API major version, recommended `/v1`, with:

- bounded request bodies/collections;
- bounded run/event history;
- bounded subscribers/backpressure;
- `action_id`/idempotency on mutation-capable requests;
- deterministic duplicate semantics;
- retrieval of existing action/run state;
- deterministic malformed-input errors;
- explicit shutdown behavior;
- no raw/debug mutation endpoint;
- loopback bind by default;
- fail-closed refusal of remote exposure without an independently approved remote-security profile.

A convenience `0.0.0.0` switch must not silently enable unauthenticated control.

## 20. Capability model separation

Generic adapters expose:

```yaml
GenericCapability:
  capability_id: string
  read_supported: bool
  action_supported: bool
  semantic_version: string
  source: string
  notes: string | null
```

Official Tibia additionally exposes:

```yaml
OfficialEvidenceExtension:
  read_gate: NONE | R0 | R1 | R2 | R3 | R4
  action_gate: NONE | A0 | A1 | A2 | A3 | A4
  evidence_refs: [string]
```

Oteryn/fake adapters do not claim Track A evidence grades.

Read support never implies action support.

## 21. Surveyor integration boundary

Surveyor is a producer dependency, not logic to copy.

Package C pins:

```yaml
surveyor_schema_version:
producer_commit:
producer_interface:
```

Unknown/incompatible schema -> explicit `SURVEYOR_UNAVAILABLE/INCOMPATIBLE`.

Control Center may reference Surveyor-owned evidence/coverage state but does not silently promote or overwrite it.

## 22. Oteryn v2 boundary

Oteryn v2 owns its shared E2E platform under accepted `docs/architecture/ADR-0007-native-end-to-end-test-platform.md`.

A future Control Center Oteryn adapter integrates with that platform or an explicitly versioned cross-repository semantic boundary. It must not create a second Oteryn scenario authority, authentication authority or server-mutation authority.

Requirements:

- retain `protocol-oteryn`;
- client sends semantic intent;
- server remains authoritative;
- test-control hooks do not become unauthenticated production surfaces;
- production-default builds exclude/disable test-only control according to Oteryn governance;
- generic semantic capability fields are used without Track A-specific authority/evidence pollution;
- separate Oteryn task/branch/PR and coordination ID for writes.

## 23. Differential comparison profile

Default field classes:

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

A mismatch exists only when:

1. both sides support/observe the field for the selected profile;
2. both refer to the same normalized scenario checkpoint/transition;
3. neither side is UNKNOWN;
4. the candidate violates the declared equivalence/tolerance rule.

Coverage states include:

```text
NOT_OBSERVABLE_REFERENCE
NOT_SUPPORTED_CANDIDATE
UNKNOWN_REFERENCE
UNKNOWN_CANDIDATE
NOT_COMPARABLE
```

Missing reference observation is a coverage gap, not candidate failure.

## 24. Artifact atomicity and durability

Each run uses a staging/incomplete state and explicit finalization.

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
- terminal/incomplete status.

`result.json`/manifest PASS is written only after required action ledger/events are flushed according to the chosen storage guarantees.

Crash before finalization -> explicit incomplete run, never synthesized PASS.

Finalized historical result is immutable except explicit append-only supplemental evidence.

## 25. Fake adapter normative behavior

Package A fake adapter uses deterministic manual clock/state scheduling.

It must inject/test:

- read-only/mutation authority;
- capability support/refusal;
- backend/control/adapter/runtime/session generation changes;
- success/refusal;
- before-dispatch failure;
- dispatch-commit durability failure;
- crash after dispatch commit before physical fake effect;
- after-dispatch failure;
- ambiguous completion;
- timeout;
- cancellation;
- exact STOP-vs-dispatch-gate interleavings;
- duplicate action IDs;
- deterministic side-effect consumption;
- multi-clock event sources;
- late events;
- secret-shaped rejected inputs;
- artifact incomplete/finalized states.

Fake success never proves official-client capability.

## 26. Package A acceptance

Package A is implementation-ready only when all semantics above can be validated with `runtime_access:none` and no network listener.

Required deterministic tests include at minimum:

1. schema accept/reject and stable step IDs;
2. typed UNKNOWN predicate semantics;
3. unsupported capability refusal;
4. read-only mutation refusal;
5. stale backend epoch refusal;
6. authority loss immediately before dispatch commit;
7. runtime/session/adapter identity change immediately before dispatch commit;
8. two concurrent mutation requests serialize;
9. duplicate same-ID/same-request dispatches once;
10. same-ID/different-request conflict refusal;
11. STOP wins dispatch gate -> no commit/no mutation;
12. dispatch commit wins -> STOP classifies action at risk/already committed;
13. stale old-generation completion cannot advance run;
14. reset does not restore cached authority;
15. pause/resume after session/runtime change refuses pending mutation;
16. engine timeout and wait cancellation;
17. side-effect reservation/exhaustion;
18. dispatch commit atomically moves budget to at-risk;
19. duplicate request creates no second reservation;
20. ambiguous consumable action conservatively consumes budget and is not retried;
21. durability failure before dispatch commit -> no physical dispatch;
22. crash after durable dispatch commit but before fake effect -> AMBIGUOUS/no retry;
23. backend restart creates new backend epoch;
24. stale old-backend callback rejected as control input;
25. source/ingest clocks stay distinct;
26. ingest ordering never implies causal ordering;
27. late event cannot rewrite terminal result;
28. causal fields preserve supplied stimulus/direction/lane/sequence/handler/object/delta/evidence refs;
29. secret-shaped event/error/trace rejected before normal object creation;
30. screenshot risk path quarantined/refused;
31. artifact crash remains incomplete;
32. finalized artifact cannot be silently rewritten;
33. fake one-step experiment succeeds deterministically;
34. no operator-facing adapter bypass exists.
