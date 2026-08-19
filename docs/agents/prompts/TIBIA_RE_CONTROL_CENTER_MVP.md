# TIBIA-RE-CONTROL-CENTER-MVP

Recommended reasoning effort: high / maximum.

Repository:

```text
https://github.com/blakinio/otclient
```

Execution mode:

```text
AUTONOMOUS BOUNDED IMPLEMENTATION
```

## Mission

Implement the first reusable `TIBIA RE Control Center / E2E Lab` from the current repository contracts without performing real official-client mutation in Package A or Package B.

Do not reconstruct architecture from chat history. Git is authoritative.

Normative design package:

- `docs/agents/programs/TIBIA_RE_CONTROL_CENTER_E2E.md`
- `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md`
- `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md`

This prompt controls implementation procedure; it does not override current Track A or Oteryn governance.

# HARD SAFETY BOUNDARY

For Package A:

```yaml
runtime_access: none
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
network_listener_allowed: false
official_client_access: false
```

Package A must be fully implementable and testable without Track A runtime, KasmVNC, official-client processes, credentials, login, GUI input or gameplay.

Package B remains read-only for the real official-client path.

Real official-client mutation belongs only to a separate Package D runtime-sensitive task with fresh current Track A admission.

# 1. Mandatory preflight

Before editing:

1. read root `AGENTS.md`, `docs/agents/README.md` and nearer applicable instructions;
2. fetch current `main` and verify exact head;
3. inspect all open PRs and `docs/agents/tasks/active/**` for overlapping Control Center/scenario/recorder/API/adapter work;
4. read the three normative design files in full;
5. read `docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md`;
6. read current Track A admission/routing/contracts required by `docs/agents/README.md`, even though Package A uses `runtime_access:none`;
7. inspect exact current #592 Surveyor state and do not assume merge/interface stability;
8. inspect `tools/tibia_runtime_bridge/**` and current test/runtime helpers for reuse;
9. inspect `MODULE_CATALOG.md`, `REPOSITORY_MAP.md`, `KNOWN_RISKS.md`, `BUILD_TEST_MATRIX.md`, `CROSS_REPO_CONTRACTS.md`;
10. search existing scenario, recorder, HTTP, CLI, artifact, cancellation, idempotency, persistence and fake/test infrastructure before creating abstractions;
11. create one dedicated task, branch/worktree and Draft PR before substantial implementation;
12. declare owned paths and resolve live overlap before shared-path edits.

If repository state supersedes an example here, follow current trusted-base contracts and record the discrepancy.

# 2. Architecture invariant

Preserve exactly one operator-to-adapter path:

```text
Browser UI ----\
                -> Versioned Control API/domain service
CLI -----------/              |
                              v
                         Run Manager
                              |
                              v
                       Scenario Engine
                              |
                    MutationCoordinator
                              |
                     Safety Controller
                              |
                              v
                       Adapter Contract
```

Recorder and Artifact Store observe/record this path; they do not create authority.

Forbidden:

```text
CLI -> direct adapter
Browser -> raw action endpoint
Quick Action -> raw keypress/tool
Scenario -> Track A lease/registration mutation
Recorder -> capability promotion
Artifact Store -> evidence-registry promotion
```

# 3. Package order

Do not collapse all phases into one PR.

## Package A — control-core

No network listener. No official client. No Surveyor dependency required for tests.

Recommended path only after checking live conventions:

```text
tools/tibia_re_control_center/
```

### A1. Typed domain models

Implement:

- adapter and execution contract version negotiation;
- generic capability support;
- official-client evidence extension types without requiring them for fake adapters;
- runtime status/freshness;
- normalized snapshots;
- `backend_epoch` and `control_generation`;
- dispatch fences;
- action request/result/lifecycle;
- event ordering/causal fields;
- typed predicates;
- side-effect ledgers;
- run/artifact states.

`backend_epoch` is a fresh opaque unique value for every backend process lifetime. `control_generation` is monotonic only within that epoch.

### A2. Deterministic Scenario Engine

Implement:

- `schema_version` validation;
- deterministic stable step IDs;
- typed preconditions/assertions/waits;
- explicit UNKNOWN semantics;
- deterministic timeout semantics;
- deterministic failure propagation;
- mutation retry default `0`;
- one-step experiment representation;
- pause/resume fencing;
- backend/control/adapter/runtime/session invalidation;
- no hidden retries.

### A3. MutationCoordinator

Exactly one coordinator per adapter instance.

It owns only local:

- mutation serialization;
- unique `backend_epoch`;
- monotonic `control_generation`;
- action idempotency ledger;
- budget reservation/accounting;
- dispatch lifecycle bookkeeping;
- tiny `dispatch_gate` linearization domain;
- STOP/reset semantics.

It does not own Track A authority.

Do **not** hold `dispatch_gate` while waiting for slow/external authority, I/O, Track A locks, capture or GUI resources.

### A4. Idempotency ledger

`action_id` is mandatory and stores a canonical normalized-request hash.

Rules:

- same ID + same request hash -> same logical state/result, no second dispatch;
- same ID + different request hash -> deterministic conflict refusal;
- duplicate caller/API attempt -> no second budget reservation;
- new explicit retry -> new ID and new budget admission;
- after possible dispatch, automatic retry is forbidden.

### A5. Side-effect reservation before dispatch

Per dimension track:

```text
limit
reserved
at_risk
committed
uncertain
```

Before final dispatch, reserve the maximum plausible effect.

If a hard budget cannot be safely bounded, refuse.

Use checked/overflow-safe arithmetic.

### A6. Preparation outside the dispatch gate

Preparation may:

- validate action/schema;
- resolve capability;
- reserve budget;
- run advisory preflight;
- await/acquire fake/external authority provider;
- prepare before-state.

All waits are bounded and cancellation-aware.

Preparation never authorizes final dispatch.

### A7. One-shot dispatch commit

Model the adapter execution context with a one-shot coordinator-owned operation equivalent to:

```text
commit_dispatch() -> COMMITTED | REFUSED
```

Immediately before the fake irreversible effect, `commit_dispatch()` acquires `dispatch_gate` and verifies:

1. action record is still dispatchable and not already committed;
2. request hash still matches;
3. expected backend epoch is current;
4. expected control generation is current;
5. STOP is not latched;
6. cancellation is not latched;
7. adapter generation matches;
8. runtime/session fences match;
9. budget reservation remains valid;
10. semantic capability remains supported;
11. current authority provider still permits the exact action.

Then it atomically/deterministically transitions the fake persistence model to:

```text
lifecycle_state=DISPATCH_COMMITTED
dispatch_state=POSSIBLY_DISPATCHED
budget reserved -> at_risk
```

Only after that commit succeeds may the fake adapter cross its irreversible test effect.

### A8. Dispatch durability model

Package A must implement a deterministic store abstraction that can simulate a durability barrier.

Required behavior:

```text
write-ahead commit/barrier fails -> no physical fake effect
write-ahead commit/barrier succeeds -> action is now possible-dispatch / no safe auto-retry
```

A crash after durable dispatch commit but before the fake physical effect recovers as `AMBIGUOUS` unless a deterministic reconciliation fixture proves no effect.

This conservative false-positive ambiguity is intentional.

### A9. STOP ALL

STOP and dispatch commit use the same tiny `dispatch_gate`.

Required linearizability:

```text
STOP acquires dispatch_gate first
  -> control_generation increments/latches STOP
  -> stale commit fails
  -> no physical mutation begins

commit_dispatch acquires dispatch_gate first
  -> possible-dispatch state is recorded
  -> STOP later sees already committed/in-flight work
  -> no fiction that STOP undid it
```

STOP then:

- cancels queued old-generation steps;
- signals active waits/captures/actions;
- rejects stale completions as control input;
- preserves them as evidence where useful;
- cleans harness-owned resources;
- requires explicit reset.

### A10. Reset

Reset is local only and never restores external authority from cache.

It must preserve safe handling of unresolved `AMBIGUOUS` side-effect domains.

### A11. Crash/restart recovery

On simulated backend restart:

- create a new unique `backend_epoch`;
- stale old-epoch callbacks cannot influence current execution;
- do not auto-resume mutation-capable scenarios;
- state before durable dispatch commit is `NOT_DISPATCHED`;
- durable `DISPATCH_COMMITTED` without authoritative terminal evidence becomes `AMBIGUOUS`;
- contradictory/corrupt/missing ledger fails closed;
- all authority is reacquired/revalidated.

### A12. Budget reconciliation

At durable dispatch commit, reservation moves to `at_risk` in the same logical transaction.

After outcome:

- proven no physical dispatch/effect -> release only with proof;
- measured confirmed effect -> move measured amount to `committed`, release proven remainder;
- dispatched but unmeasurable -> conservatively commit maximum plausible effect;
- timeout/failure/cancellation/ambiguity after dispatch commit -> move maximum plausible amount to `uncertain`;
- `uncertain` counts as consumed until safely reconciled.

### A13. Recorder core

`events.jsonl` order is ingestion order, not causal source order.

Preserve:

- ingest sequence;
- ingestion monotonic timestamp;
- source timestamp;
- source clock domain;
- source sequence/scope;
- ordering confidence;
- backend/control/adapter/runtime/session generations;
- run/step/stimulus identity;
- late flag;
- sensitivity.

Preserve causal fields from `OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md` when supplied/observable.

Never infer causality from timestamp proximity.

### A14. Privacy constructors

Secret classification occurs before normal Event/Error/Artifact construction.

Provide constructors/barriers so:

- arbitrary runtime/exception text is not implicitly safe;
- secret-shaped values cannot enter ordinary event payloads;
- `SECRET_REJECTED` contains category/reason only;
- environment values cannot be serialized accidentally;
- screenshot admission supports `SAFE`, `QUARANTINED`, `REJECTED` without persisting synthetic secret values;
- export-time redaction is only defense in depth.

### A15. Artifact lifecycle

Logical run state:

```text
ACTIVE -> CLOSING -> FINALIZED
```

Support:

- staging/incomplete state;
- deterministic flush/finalization;
- manifest with backend/control/fence/action/budget provenance;
- immutable finalized result;
- append-only supplement model;
- no synthesized PASS after crash.

### A16. Fake adapter

Use deterministic manual clock/state scheduling capable of injecting:

- read-only/mutation authority;
- capability present/missing;
- backend/control/adapter/runtime/session changes;
- success/refusal;
- before-dispatch failure;
- dispatch durability failure;
- crash after dispatch commit before effect;
- after-dispatch failure;
- ambiguous completion;
- timeout/cancellation;
- exact STOP-vs-dispatch-gate interleavings;
- duplicate action IDs;
- deterministic movement/consumable effects;
- multi-clock event sources;
- late events;
- secret-shaped rejected data;
- artifact crash/finalization.

Fake success never proves official-client capability.

## Package B — loopback Control API + browser + CLI

Consume merged Package A.

Before accepting operator mutation-capable requests even for fake adapters, the backend's selected persistent store must implement the execution contract's durable write-ahead dispatch commit. The storage technology is not prescribed, but durability/failure semantics are.

Implement:

- versioned loopback-only API, preferably `/v1`;
- browser UI;
- CLI as a client of exactly the same domain operations;
- status/capability/evidence/freshness views;
- scenario/run/action views;
- bounded live events/history/subscribers/backpressure;
- artifact browser/export;
- STOP/reset/pause/resume/abort;
- duplicate request/result retrieval;
- no official-client mutation.

Mutating UI controls may operate only against explicit fake adapters in Package B. For real Track A state they remain disabled/refused.

Remote/LAN binding is out of scope. Do not add a convenience unauthenticated remote-control switch.

## Package C — Surveyor/read-only integration

Only after #592 has an accepted exact producer state.

Pin:

```yaml
surveyor_schema_version:
producer_commit:
producer_interface:
```

Consume outputs; do not copy internals.

Expose:

- coverage summary;
- evidence/index status;
- read-only runtime snapshot;
- current-client fence/provenance;
- bundle reference/status.

Incompatible/missing Surveyor -> explicit `UNAVAILABLE/INCOMPATIBLE`, not fabricated data.

Control Center per-run artifacts may reference but not promote/overwrite Surveyor-owned evidence/coverage state.

## Package D — official Track A action adapter

Separate runtime-sensitive task. This prompt does not authorize it.

Before any real action:

1. read then-current trusted-base Track A governance;
2. create a current runtime task and obtain current runtime access class;
3. satisfy canonical lease/registration/Gate A/rebind/Gate B/target uniqueness/whole-lifetime supervisor requirements;
4. use the shared GUI input lock when applicable;
5. prove action evidence/parity gate;
6. define safe maximum plausible effect/budget;
7. acquire current Track A guarded mutation boundary **without holding the local dispatch gate while waiting**;
8. while Track A guard remains continuously held, run final current Track A identity/authority checks;
9. immediately before physical effect call coordinator `commit_dispatch()`;
10. if durable local commit succeeds, cross physical irreversible boundary exactly once while Track A guard remains held;
11. reconcile action/budget/evidence conservatively.

Never implement a second lease manager, registration source or authority lock inside Control Center.

## Package E — Oteryn v2 adapter

Separate task/branch/PR in:

```text
blakinio/Oteryn-v2
```

Read current Oteryn governance and accepted `docs/architecture/ADR-0007-native-end-to-end-test-platform.md`.

Integrate with Oteryn's existing shared E2E architecture or an explicitly versioned cross-repo semantic contract. Do not create a second Oteryn E2E platform.

Requirements:

- keep `protocol-oteryn`;
- client sends semantic intent;
- server remains authoritative;
- no hidden authoritative mutation hook;
- no unauthenticated production test-control interface;
- test-only hooks excluded/locked down under Oteryn policy;
- generic semantic capability model, not Track A R/A grades.

# 4. UI requirements

Always-visible state separates:

```text
RUNTIME | CLIENT | RECORDER | AUTHORITY | CAPABILITY | EVIDENCE | FRESHNESS | SESSION
STOP ALL | PAUSE
```

Required tabs:

```text
Main Runtime Movement Healing Spells Consumables Combat Targeting
Inventory Containers Equipment Chat Conditions Scenarios Recorder
Network Experiments Compare Logger
```

Never present `MUTATION_ALLOWED` as a checkbox/local preference.

Unknown/unproven/stale fields render explicitly as `UNKNOWN`, `UNSUPPORTED`, `NOT_PROVEN`, `STALE` or equivalent.

Every manual Quick Action becomes exactly one validated one-step experiment through Scenario Engine.

# 5. Differential comparison rules

Use explicit versioned comparison profiles.

Baseline:

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

Do not report mismatch when the reference field is unobservable/UNKNOWN. Report coverage state.

# 6. Package A mandatory deterministic tests

Package A is not complete until all pass with `runtime_access:none`:

1. scenario schema accept/reject;
2. deterministic stable step IDs;
3. typed predicate UNKNOWN behavior;
4. unsupported capability refusal;
5. read-only mutation refusal;
6. stale backend epoch refusal;
7. authority expires exactly at final dispatch commit;
8. runtime instance changes at final dispatch commit;
9. session epoch changes at final dispatch commit;
10. adapter generation changes at final dispatch commit;
11. two concurrent mutation requests serialize;
12. same action ID/same request dispatches at most once;
13. same action ID/different request is refused;
14. duplicate request creates no second reservation;
15. STOP wins dispatch gate -> no commit/no effect;
16. commit wins dispatch gate -> STOP sees possible-dispatch/already committed;
17. stale old-generation completion cannot resume/advance run;
18. explicit reset does not restore cached authority;
19. pause/resume after runtime/session change refuses pending mutation;
20. engine timeout;
21. cancellation while waiting;
22. cancellation before commit;
23. after-commit cancellation classification;
24. budget reservation/exhaustion;
25. dispatch commit moves reservation to at-risk atomically;
26. durability barrier failure -> no effect;
27. crash after durable commit before effect -> AMBIGUOUS/no retry;
28. ambiguous consumable action conservatively consumes budget;
29. ambiguous action is not automatically retried;
30. backend restart creates a fresh backend epoch;
31. stale old-backend callback rejected as control input;
32. source/ingest clocks from different domains remain distinguishable;
33. ingestion sequence never masquerades as causal proof;
34. late event cannot rewrite terminal result;
35. causal fields preserve supplied stimulus/direction/lane/sequence/handler/object/delta/evidence refs;
36. secret-shaped event input rejected before ordinary event construction;
37. exception/repr secret-shaped text does not reach `safe_message`;
38. screenshot risk path is quarantined/rejected;
39. artifact crash remains incomplete, never PASS;
40. finalized artifact is stable except explicit supplement;
41. fake one-step scenario succeeds deterministically;
42. no browser/CLI-facing domain interface can call adapter directly.

Add deterministic interleaving/property tests where they make race semantics clearer.

# 7. Package B mandatory tests

At minimum:

- loopback bind default;
- non-loopback config fails closed absent approved profile;
- request/body/collection bounds;
- bounded history/subscribers/backpressure;
- malformed API requests;
- duplicate POST idempotency/result retrieval;
- durable dispatch journal barrier failure path;
- backend restart with committed fake action -> AMBIGUOUS/no retry;
- browser/CLI semantic parity;
- authority/capability/evidence/freshness rendered separately;
- disabled/refused real mutation under read-only/unknown/stale authority;
- STOP/reset visible state;
- browser reload does not duplicate active run/action;
- shutdown leaves truthful terminal/incomplete state.

# 8. Security/privacy acceptance

Fail implementation if ordinary persistent/loggable objects can contain:

- email/password/2FA;
- auth/session tokens;
- cookies/tickets;
- encryption/RSA secret material;
- raw secret-bearing network payload;
- environment variable value;
- arbitrary unsanitized adapter exception text;
- unapproved private chat text;
- unreviewed login/auth screenshot.

Use stable reason codes and explicitly classified safe fields.

# 9. Validation procedure

For each package PR:

1. inspect full changed-file list and diff;
2. run focused deterministic tests;
3. select commands from current `BUILD_TEST_MATRIX.md`; do not invent presets;
4. run required exact-head CI;
5. perform full self-review against normative contracts;
6. obtain independent review when current risk policy requires it;
7. re-run affected race/idempotency/durability/privacy tests after related changes;
8. update task with exact commands/outcomes/SHA;
9. update catalogue/changelog when required and not blocked by live ownership;
10. merge only through current repository policy after all gates pass.

# 10. Mandatory non-claims

Never claim:

- official mutation capability from fake tests;
- Track A authority from Control Center state;
- runtime compatibility from repository-only tests;
- causal proof from timestamp correlation;
- exact source ordering across different clocks without evidence;
- no side effect merely because an after-commit call timed out/failed;
- safe retry after dispatch commit without authoritative no-effect proof;
- Oteryn parity before separate Oteryn adapter;
- Oteryn mismatch when official reference is unobservable;
- remote/LAN security before separate exposure design;
- safe secret handling from export-time redaction alone.

# 11. Package A terminal acceptance

Package A may be called implementation-ready only when:

```text
runtime_access=none
network_listener=none
real_official_client_access=none
all mandatory deterministic tests=PASS
backend_epoch fencing=PASS
dispatch gate linearizability=PASS
durable write-ahead commit model=PASS
STOP race model=PASS
idempotency/replay=PASS
budget at-risk/uncertain accounting=PASS
multi-clock recorder=PASS
construction-time secret rejection=PASS
artifact crash/finalization=PASS
no adapter bypass=PASS
self-review=no material findings
required independent review=PASS when applicable
exact-head CI=PASS
```

A fresh agent must be able to continue from Git/task/PR alone without this chat.

# 12. Desired first operator result

After Packages A-C the operator can:

- start Control Center locally;
- use browser or CLI against the same backend;
- inspect truthful read-only Track A/Surveyor status;
- see authority/capability/evidence/freshness separately;
- browse scenarios/runs/actions/events/artifacts;
- execute deterministic fake-adapter one-step experiments;
- prove STOP/idempotency/durability/cancellation behavior;
- export privacy-safe `agent_bundle.json`;

while every real official-client mutation remains fail-closed until Package D receives separate current Track A authority and runtime evidence.