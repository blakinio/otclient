# TIBIA RE Control Center Execution Contract v1

```yaml
contract_id: TIBIA-RE-CONTROL-CENTER-EXECUTION-V1
version: 1
status: normative_design
producer_repository: blakinio/otclient
runtime_authority: external
runtime_access_of_this_document: none
```

## 1. Purpose

This contract defines the concurrency, dispatch, cancellation, idempotency, budget, recorder, privacy and crash-recovery semantics that every Control Center implementation must obey.

It closes the gap between a valid semantic scenario and actual authority to perform a mutation.

Normative invariant:

```text
scenario validity != capability evidence != mutation authority
```

A scenario may be valid while its action is unsupported or unauthorized. No local UI, CLI flag, scenario field, cached status, prior preflight or adapter capability may create Track A mutation authority.

For `OFFICIAL_TIBIA`, current Track A trusted-base lease/registration/Gate A/rebind/Gate B/target-identity/GUI-lock/whole-lifetime-supervisor contracts remain the sole mutation authority. This contract consumes them; it never replaces them.

## 2. Execution ownership and concurrency

Each adapter instance has exactly one `MutationCoordinator`.

Rules:

1. at most one mutation-capable action may cross the adapter's irreversible dispatch boundary at a time;
2. multiple read-only runs may execute concurrently only when every involved observation source is independently safe for concurrent use;
3. a mutating run does not acquire standing authority for its lifetime; every mutation is authorized independently at dispatch;
4. browser, CLI, internal scheduler and one-step experiments submit work to the same coordinator;
5. no adapter method callable by an operator surface may bypass the coordinator;
6. local process locks are never substitutes for Track A authority.

If concurrency safety is not explicitly proven for an operation, serialize it.

## 3. Generations and immutable fences

The backend owns a monotonic `control_generation` persisted for the current backend lifetime. `STOP ALL` increments it.

Every validated action binds immutable expected fences:

```yaml
DispatchFence:
  action_id: string
  run_id: string
  step_id: string
  expected_control_generation: integer
  expected_runtime_instance_id: string | null
  expected_session_epoch: string | null
  expected_adapter_generation: string
  required_capability: string
  required_authority: READ_ONLY | MUTATION
```

For the official adapter, the final dispatch implementation also binds every current Track A identity/authority fence required by trusted base. Those Track A fields are adapter-specific and must not be copied into the generic scenario schema.

A changed runtime instance, session epoch, adapter generation, control generation or required Track A identity/authority fact invalidates the action.

## 4. Action lifecycle

Every action has exactly one durable logical lifecycle:

```text
CREATED
  -> VALIDATED
  -> RESERVED
  -> DISPATCHING
  -> DISPATCHED
  -> CONFIRMING
  -> CONFIRMED

or terminal:

REFUSED
CANCELLED_BEFORE_DISPATCH
CANCELLED_AFTER_DISPATCH
FAILED_BEFORE_DISPATCH
FAILED_AFTER_DISPATCH
TIMED_OUT_BEFORE_DISPATCH
TIMED_OUT_AFTER_DISPATCH
AMBIGUOUS
```

`AMBIGUOUS` means the platform cannot prove whether the external side effect occurred. `AMBIGUOUS` is never automatically retried.

Terminal completion from an older `control_generation`, runtime instance or session epoch may be recorded as evidence but must not advance or resume a newer run.

## 5. Idempotency and replay

`action_id` is a mandatory globally unique idempotency key for one logical action attempt within the artifact namespace.

The coordinator maintains an action ledger keyed by `action_id`.

Duplicate submission rules:

- same `action_id` + byte-equivalent normalized semantic request -> return/replay the existing logical action state/result; never dispatch again;
- same `action_id` + different normalized request -> `REFUSED_IDEMPOTENCY_CONFLICT`;
- new `action_id` after a prior `AMBIGUOUS`, `DISPATCHED`, `FAILED_AFTER_DISPATCH` or `TIMED_OUT_AFTER_DISPATCH` action is a new side-effect attempt and requires an explicit scenario policy; mutation retries default to forbidden;
- transport retry, browser reload, CLI retry or repeated HTTP POST never creates a second logical action when the idempotency key is unchanged.

The backend API must support retrieving the existing run/action result after connection loss.

## 6. Atomic dispatch boundary

A mutating action may cross the irreversible adapter boundary only through a single coordinator operation logically equivalent to:

```text
atomic_dispatch(action, expected_control_generation, cancellation_token)
```

The following must be evaluated within one serialization/authority critical section immediately before irreversible dispatch:

1. action ledger still permits first dispatch;
2. expected `control_generation` equals current generation;
3. cancellation token is not cancelled;
4. runtime/session/adapter fences still match;
5. side-effect reservation is still valid;
6. capability is currently supported;
7. for `OFFICIAL_TIBIA`, the current Track A authority/identity chain passes inside the existing canonical guarded mutation boundary;
8. required shared GUI/input lock is held when applicable;
9. then, and only then, the implementation crosses the irreversible mutation boundary exactly once.

A separate earlier `preflight()` is advisory/diagnostic and may reject early, but it can never authorize dispatch. `execute()` must revalidate the final dispatch fence itself or delegate to a primitive that does.

For the official adapter, preferred integration is to place the final fence check and irreversible action under the current Track A whole-lifetime guard/supervisor rather than implementing a second authority lock.

## 7. STOP ALL linearization

`STOP ALL` has one linearization point: increment/latch the global `control_generation` under the same `MutationCoordinator` synchronization domain used by dispatch admission.

Required behavior:

1. increment `control_generation`;
2. latch `stop_state=STOPPED`;
3. reject all new mutation admissions until explicitly reset;
4. cancel queued old-generation steps;
5. signal cooperative cancellation to active waits/captures/actions;
6. prevent any action that has not yet crossed the irreversible boundary from doing so;
7. classify already-dispatched work conservatively;
8. reject stale old-generation completion as control input;
9. emit terminal cancellation/evidence events;
10. perform bounded cleanup of harness-owned resources only.

The following race must be impossible:

```text
preflight PASS
STOP ALL linearizes
mutation dispatch starts
```

Either dispatch linearizes first and the action is classified as already dispatched, or STOP ALL linearizes first and dispatch is refused. There is no third outcome.

`STOP ALL` does not kill the official client unless a separate current process-control authority explicitly authorizes that exact effect.

## 8. Reset after STOP

STOP is latched. A new run requires an explicit local reset operation that:

- creates/accepts the new current `control_generation`;
- proves there is no unresolved harness-owned action whose state could be mistaken for the new run;
- obtains a fresh runtime status;
- never restores prior Track A mutation authority from cache.

If an older action remains `AMBIGUOUS`, the reset may permit unrelated actions only when their side-effect domains cannot compound that ambiguity. Otherwise fail closed.

## 9. Pause and resume

Pause stops scheduling new steps but does not suspend external time, lease expiry, session generation, runtime identity or action deadlines already beyond the irreversible boundary.

On resume the engine must revalidate:

- current `control_generation`;
- adapter generation;
- runtime instance;
- session epoch;
- scenario preconditions that were declared `revalidate_on_resume`;
- every subsequent mutation's current authority at dispatch.

A changed session epoch or runtime instance invalidates pending mutation steps by default. Resume never reuses an old successful authority check.

Scenario timeouts use a documented clock policy. Package A default is monotonic active-run time for engine-owned waits, while adapter/external deadlines continue according to their own monotonic clocks and cannot be extended by pause unless the adapter contract explicitly supports it.

## 10. Backend restart and crash recovery

Package A may use an in-memory fake store, but the logical recovery semantics are normative from day one.

Before Package B accepts operator requests, durable run/action state must distinguish at least:

```text
NOT_DISPATCHED
POSSIBLY_DISPATCHED
CONFIRMED
```

On backend restart:

- `NOT_DISPATCHED` work may be reconsidered only after fresh validation;
- `POSSIBLY_DISPATCHED` mutation becomes `AMBIGUOUS` unless authoritative reconciliation proves the exact outcome;
- `AMBIGUOUS` mutation is never auto-retried;
- no active scenario automatically resumes mutation after restart;
- a new backend control generation is created;
- all authority is reacquired/revalidated from external sources.

## 11. Side-effect budget ledger

Budgets are enforced by a per-run ledger with `limit`, `reserved`, `committed` and `uncertain` values per dimension.

Before dispatch the engine must reserve the maximum plausible effect of the action for every applicable budget dimension.

After outcome:

- proven no-dispatch -> release reservation;
- proven dispatched with authoritative measured effect -> commit measured effect and release unused reservation;
- dispatched but effect cannot be measured exactly -> commit the conservative maximum plausible effect;
- timeout/failure/cancellation after possible dispatch -> move the conservative maximum plausible effect to `uncertain` and treat it as consumed for further admission;
- duplicate request with same `action_id` -> no second reservation;
- a new retry action -> new reservation.

Budget arithmetic must be monotonic and overflow-safe.

A scenario is refused before dispatch if the platform cannot derive a safe maximum plausible effect for any declared hard budget.

### 11.1 Minimum budget semantics

```text
max_runtime_seconds       pre-dispatch + runtime deadline
max_actions               reserve 1 per mutation attempt that may dispatch
max_movement_tiles        reserve maximum requested/possible tile displacement
max_spells                reserve 1 per spell dispatch
max_consumables           reserve maximum consumables one action can consume
max_items_moved           reserve maximum item count/stack amount at risk
max_gold                  require measurable/bounded maximum delta; otherwise refuse
max_tibia_coins           hard default 0; mutation requiring TC is refused unless separately authorized and measurable
max_irreversible_changes  hard default 0; any action classified irreversible reserves at least 1
```

Budgets are safety bounds, not after-the-fact reporting fields.

## 12. Typed scenario semantics

Every scenario has `schema_version` and every step receives a deterministic `step_id` derived from validated scenario identity plus ordinal, not from runtime timing.

Conditions use an explicit typed predicate form:

```yaml
Predicate:
  field: string
  op: EQ | NE | LT | LTE | GT | GTE | EXISTS | NOT_EXISTS | CHANGED | UNCHANGED | IN_SET | CONTAINS
  value: scalar | list | null
  unknown_policy: FAIL | WAIT | ACCEPT
```

Rules:

- unknown values never silently compare equal to concrete values;
- mutation preconditions default `unknown_policy=FAIL`;
- assertions default `unknown_policy=FAIL`;
- waits may use `WAIT` until timeout;
- `ACCEPT` must be explicit and is forbidden for mutation-authority or safety predicates;
- retries are explicit scenario policy; mutation action retries default to `0`;
- failure propagation is deterministic and terminal unless the scenario explicitly declares a safe continuation path.

## 13. Recorder clocks and ordering

A unified event file is an ingestion sequence, not proof of a single causal clock.

Every event records:

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

`ingest_seq` is unique and monotonic inside one recorder process and orders persistence only.

The recorder must not claim source causality from ingestion order alone.

For causal RE, the normalized event model must preserve, when observable:

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

Negative/no-stimulus controls remain experiment-level evidence requirements; the Control Center must not auto-promote a correlation to causal proof.

## 14. Late events and run finalization

A run has:

```text
ACTIVE -> CLOSING -> FINALIZED
```

When execution ends, the recorder enters `CLOSING` for a bounded drain interval and records a source watermark for each active source where available.

Events arriving after logical step/run termination carry `late=true` and the observed terminal run state. They may enrich evidence but cannot change the already-decided action outcome or restart execution.

After `FINALIZED`, mutable run files are closed. Later evidence, if accepted, is stored as an explicit append-only supplement referencing the original run rather than rewriting history.

## 15. Secret exclusion before object creation

Preferred invariant is mandatory:

> Secret-class data never enters the normal Event, Artifact, Error, Report or AgentBundle object graph.

Every ingestion boundary must classify data before construction of ordinary persistent objects.

Required controls:

- arbitrary exception/repr/debug text is untrusted and cannot become `safe_message` without sanitization;
- errors use stable reason codes and reviewed static messages plus explicitly classified safe fields;
- environment-variable values are never enumerated into artifacts;
- auth/login packet payloads are structurally excluded from capture;
- trace strings are filtered before Event creation;
- private chat text is omitted/redacted before Event creation unless explicitly test-generated and permitted;
- screenshots are admitted only when capture context is known non-secret, or enter a quarantine path that is not part of normal run artifacts until sanitized/approved;
- a rejected secret may create a metadata-only `SECRET_REJECTED` event containing category/reason, never the value/hash/reversible derivative.

Export-time redaction is defense in depth only, never the primary protection.

## 16. Network metadata policy

Default network persistence is metadata only:

```yaml
direction: CLIENT_TO_SERVER | SERVER_TO_CLIENT
lane: string | null
source_sequence: integer | null
message_type: string | null
size: integer
correlation_id: string | null
payload_capture: NONE
```

`message_type` is populated only when structurally known. Unknown remains `null`/`UNKNOWN`; no guessed semantic type is allowed.

Raw payload fallback is forbidden. A future `SANITIZED` or `APPROVED_NON_SECRET` payload path requires a separate explicit capture policy proving secret exclusion before persistence.

## 17. Control API idempotency and bounds

Browser and CLI call the same domain service. Neither may call adapters directly.

Package B must expose a versioned loopback API, recommended `/v1`, with:

- explicit request-body bounds;
- bounded event stream and run-history pagination;
- `action_id`/request idempotency key on every mutation-capable command;
- duplicate POST semantics from section 5;
- bounded subscriber count/backpressure behavior;
- deterministic malformed-input errors;
- explicit shutdown behavior;
- no raw action/debug endpoint;
- loopback bind by default and fail closed if configuration requests remote exposure without an independently approved remote-security profile.

Remote/LAN exposure is not enabled merely by a convenience bind flag.

## 18. Capability model separation

Generic adapters expose semantic support separately from implementation-specific evidence maturity:

```yaml
GenericCapability:
  capability_id: string
  read_supported: bool
  action_supported: bool
  semantic_version: string
  source: string
  notes: string | null
```

`OFFICIAL_TIBIA` additionally exposes Track A RE maturity:

```yaml
OfficialEvidenceExtension:
  read_gate: NONE | R0 | R1 | R2 | R3 | R4
  action_gate: NONE | A0 | A1 | A2 | A3 | A4
  evidence_refs: [string]
```

Oteryn and fake adapters must not be forced to claim Track A R/A evidence grades.

Read support never implies action support.

## 19. Surveyor integration boundary

Surveyor is a producer dependency, not an implementation library to copy.

Package C may integrate only after an exact accepted Surveyor state is identified and must pin:

```yaml
surveyor_schema_version:
producer_commit:
producer_interface:
```

Unknown or incompatible schema fails closed to `SURVEYOR_UNAVAILABLE/INCOMPATIBLE` while the rest of Control Center remains usable where independent data sources permit it.

Surveyor capability/evidence registries remain the source of truth for their owned coverage data. Control Center per-run artifacts may reference them but must not silently promote or overwrite them.

## 20. Oteryn v2 boundary

Current Oteryn v2 architecture owns its own shared E2E platform under accepted `docs/architecture/ADR-0007-native-end-to-end-test-platform.md`.

Therefore a future Control Center Oteryn adapter must integrate with that platform or an explicitly versioned cross-repository semantic boundary. It must not create a second Oteryn scenario authority, authentication authority or server-mutation authority.

The Oteryn adapter:

- retains `protocol-oteryn`;
- sends semantic client intent through supported product/test boundaries;
- treats server-authoritative state as authoritative;
- keeps test-only hooks excluded from production-default builds or otherwise cryptographically/operationally unreachable in production according to Oteryn governance;
- exposes normalized observations/actions without Track A-specific authority fields in the generic schema;
- uses separate Oteryn repository task/branch/PR and shared coordination ID for any cross-repository contract change.

## 21. Differential comparison profile

Comparisons are field-profile driven:

```text
position                 NORMALIZED_EXACT
hp                       NORMALIZED_EXACT
mana                     NORMALIZED_EXACT
conditions               SET_EQUIVALENT or profile-declared NORMALIZED_EXACT
target_state              NORMALIZED_EXACT
inventory                 NORMALIZED_EXACT
containers                ORDERED_EQUIVALENT when index/order is semantic
equipment                 NORMALIZED_EXACT
cooldown_state            NORMALIZED_EXACT
cooldown_timing           TOLERANCE
visual_effect_semantics   REFERENCE_ONLY unless both expose a stable semantic event
pixel/frame output        NOT_COMPARABLE by default
latency                   TOLERANCE or REFERENCE_ONLY
protocol_bytes            NOT_COMPARABLE
internal_object_layout    NOT_COMPARABLE
renderer_implementation   NOT_COMPARABLE
```

A mismatch exists only when:

1. both sides declare the field observable/supported for the selected comparison profile;
2. both observations refer to the same normalized scenario checkpoint/semantic transition;
3. neither side is `UNKNOWN` for the compared field;
4. the candidate violates the declared equivalence/tolerance rule.

Missing official observation is a coverage gap, not an Oteryn failure.

Recommended non-mismatch classifications include:

```text
NOT_OBSERVABLE_REFERENCE
NOT_SUPPORTED_CANDIDATE
UNKNOWN_REFERENCE
UNKNOWN_CANDIDATE
NOT_COMPARABLE
```

## 22. Artifact atomicity

Each run is written through a staging directory and finalized atomically where the filesystem permits it.

Minimum manifest fields include schema versions, scenario hash, adapter identity/version, control generation, runtime/session fences, start/end state, action ledger summary, budget ledger summary, privacy policy and artifact hashes.

`result.json`/manifest final state is written only after action ledger and event stream are flushed. A crash before finalization leaves an explicit incomplete run; recovery must not synthesize PASS.

## 23. Fake adapter normative behavior

Package A fake adapter uses a deterministic manual clock and seeded state machine.

It must support fixtures for:

- read-only and mutation-capable authority states;
- capability presence/absence;
- runtime/session generation changes;
- delayed waits;
- action success/refusal;
- before-dispatch failure;
- after-dispatch failure;
- ambiguous completion;
- cancellation before dispatch;
- STOP ALL racing at the dispatch boundary;
- duplicate action IDs;
- deterministic side-effect consumption;
- secret-shaped input rejection;
- multi-source event clocks and late events.

Fake success is never evidence of official-client capability.

## 24. Package A acceptance

Package A is implementation-ready only when all semantics above can be validated with `runtime_access: none` and no network listener.

Required deterministic tests include at minimum:

1. schema accept/reject and stable step IDs;
2. unsupported capability refusal;
3. read-only mutation refusal;
4. authority loss immediately before dispatch;
5. runtime/session identity change immediately before dispatch;
6. two concurrent mutation requests serialize;
7. duplicate `action_id` dispatches once;
8. duplicate id with conflicting body is refused;
9. STOP ALL before dispatch prevents mutation;
10. dispatch-before-STOP is classified as already dispatched and never silently undone;
11. stale completion from old control generation cannot resume run;
12. pause/resume after session change refuses pending mutation;
13. budget reservation/exhaustion;
14. ambiguous consumable action conservatively consumes budget and is not retried;
15. backend-recovery model converts possibly-dispatched mutation to AMBIGUOUS;
16. cross-clock events preserve source/ingest metadata without false total-order claim;
17. late event cannot rewrite terminal result;
18. secret-shaped event/error/trace input is rejected before normal object creation;
19. screenshot secret-risk path is quarantined/refused;
20. artifact incomplete/finalized states are deterministic;
21. fake one-step experiment success;
22. no adapter bypass exists from browser/CLI-facing domain interfaces.
