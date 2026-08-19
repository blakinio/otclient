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

Package B remains read-only with respect to the real official-client path.

Real official-client mutation belongs only to a separate Package D runtime-sensitive task with fresh current Track A admission.

# 1. Mandatory preflight

Before editing:

1. read root `AGENTS.md`, `docs/agents/README.md` and any nearer applicable instructions;
2. fetch current `main` and verify exact head;
3. inspect all open PRs and `docs/agents/tasks/active/**` for overlapping Control Center/scenario/recorder/API/adapter work;
4. read in full the three normative design files listed above;
5. read `docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md`;
6. read current Track A admission/routing/contracts required by `docs/agents/README.md`, even though Package A itself uses `runtime_access:none`;
7. inspect current #592 Surveyor state and do not assume merge/interface stability;
8. inspect `tools/tibia_runtime_bridge/**` and existing test/runtime helpers for reuse;
9. inspect `docs/agents/MODULE_CATALOG.md`, `REPOSITORY_MAP.md`, `KNOWN_RISKS.md`, `BUILD_TEST_MATRIX.md`, `CROSS_REPO_CONTRACTS.md`;
10. search for existing scenario, recorder, HTTP, CLI, artifact, cancellation, idempotency and fake-adapter infrastructure before creating new abstractions;
11. create one dedicated task, branch/worktree and Draft PR before substantial implementation;
12. declare owned paths and resolve live overlap before editing shared paths.

If repository state supersedes examples in this prompt, follow current trusted-base contracts and record the discrepancy.

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
Scenario -> Track A lease mutation
Recorder -> capability promotion
```

# 3. Package order

Implement in this order. Do not collapse all packages into one PR.

## Package A — control-core

No network listener. No official client. No Surveyor dependency required for tests.

Recommended path after verifying live repository conventions:

```text
tools/tibia_re_control_center/
```

Package A must implement:

### A1. Typed contract models

- adapter identity/version negotiation;
- generic capability support;
- official-client evidence extension types without requiring them for fake adapters;
- normalized runtime status/freshness;
- normalized snapshots;
- dispatch fences;
- action request/result/lifecycle;
- normalized event ordering/causal fields;
- typed predicates;
- side-effect budgets/ledgers;
- run/action/artifact states.

### A2. Deterministic Scenario Engine

- `schema_version` validation;
- deterministic stable step IDs;
- typed preconditions/assertions/waits;
- explicit UNKNOWN semantics;
- explicit timeout semantics;
- deterministic failure propagation;
- mutation retry default `0`;
- one-step experiment representation;
- pause/resume fencing;
- runtime/session/adapter-generation invalidation;
- no hidden retries.

### A3. MutationCoordinator

Implement one coordinator per adapter instance.

It owns only local:

- mutation serialization;
- `control_generation`;
- action idempotency ledger;
- budget reservation/admission;
- dispatch lifecycle bookkeeping;
- STOP ALL linearization.

It does not own Track A authority.

### A4. Atomic dispatch semantics

A mutation-capable action crosses the irreversible boundary only through the execution contract's logical `atomic_dispatch` operation.

Immediately before dispatch verify inside one local coordinator critical section:

1. action has not already dispatched;
2. idempotency request matches existing ledger state;
3. expected `control_generation` is current;
4. cancellation is not latched;
5. adapter generation matches;
6. runtime/session fences match;
7. budget reservation remains valid;
8. capability remains supported;
9. required authority provider says the action is currently allowed;
10. then dispatch exactly once.

For Package A the authority provider is fake/deterministic. Package A must not implement or simulate success from real Track A state.

### A5. STOP ALL

STOP must linearize under the same coordinator synchronization domain as dispatch admission.

Required invariant:

```text
STOP before dispatch -> no dispatch
Dispatch before STOP -> already-dispatched classification
```

Required behavior:

- increment/latch `control_generation`;
- reject new mutation admissions;
- cancel queued old-generation steps;
- signal active waits/captures/actions;
- prevent not-yet-dispatched mutation;
- reject stale completion as control input;
- preserve late/stale evidence;
- cleanup harness-owned resources;
- require explicit reset before future mutation-capable runs.

### A6. Idempotency and replay

`action_id` is mandatory.

Rules:

- same `action_id` + same normalized request -> existing logical state/result, no second dispatch;
- same `action_id` + different normalized request -> deterministic conflict refusal;
- connection loss or caller retry cannot create a second dispatch;
- `AMBIGUOUS`, `DISPATCHED`, `FAILED_AFTER_DISPATCH`, `TIMED_OUT_AFTER_DISPATCH` are never automatically retried;
- a new explicit retry uses a new `action_id` and a new budget reservation.

### A7. Side-effect budget ledger

Per dimension track:

```text
limit
reserved
committed
uncertain
```

Reserve maximum plausible effect before dispatch.

After outcome:

- proven no-dispatch -> release reservation;
- confirmed measured effect -> commit measured amount;
- dispatched but not exactly measurable -> commit conservative maximum;
- possible dispatch + timeout/failure/cancellation -> move conservative maximum to `uncertain` and treat as consumed for future admission.

If a hard budget cannot be safely bounded, refuse the action before dispatch.

### A8. Recorder core

`events.jsonl` ordering is ingestion order, not causal clock order.

Each event must preserve:

- `ingest_seq`;
- ingestion monotonic timestamp;
- source timestamp;
- source clock domain;
- source sequence/scope;
- ordering confidence;
- run/step/stimulus identity;
- control/runtime/session/adapter generations;
- late flag;
- sensitivity classification.

Preserve causal fields required by `OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md` when observable.

Do not infer causality from timestamp proximity.

### A9. Privacy constructors

Secret classification happens before ordinary Event/Error/Artifact object creation.

Package A must provide safe construction boundaries so:

- arbitrary runtime/exception text is not implicitly safe;
- secret-shaped fields cannot enter normal event payloads;
- a `SECRET_REJECTED` event contains category/reason only;
- environment values cannot be serialized accidentally;
- screenshot admission can represent `SAFE`, `QUARANTINED`, `REJECTED` without persisting test secret material;
- export-time redaction is not the primary control.

### A10. Artifact lifecycle

Logical run state:

```text
ACTIVE -> CLOSING -> FINALIZED
```

Artifact state supports:

- staging/incomplete;
- deterministic flush/finalization;
- immutable finalized result;
- append-only late supplement where later evidence is explicitly admitted;
- no synthesized PASS after crash.

Package A may use a temporary directory in tests; production path decisions follow current repository conventions.

### A11. Fake adapter

The fake adapter is normative test infrastructure, not a toy stub.

Use a deterministic manual clock/state machine capable of injecting:

- read-only/mutation authority;
- capability present/missing;
- runtime generation change;
- session epoch change;
- adapter generation change;
- success/refusal;
- before-dispatch failure;
- after-dispatch failure;
- ambiguous dispatch;
- timeout;
- cancellation;
- exact STOP-vs-dispatch race scheduling;
- duplicate action IDs;
- deterministic consumable/movement effects;
- multi-clock event sources;
- late events;
- secret-shaped rejected data.

Fake adapter tests never prove official-client action support.

## Package B — loopback Control API + browser + CLI

Consume merged Package A.

Implement:

- versioned loopback-only API, preferably `/v1`;
- browser UI;
- CLI as a client of the same backend/domain operations;
- status/capability/evidence/freshness views;
- scenario/run/action views;
- bounded live events;
- artifact browser/export;
- STOP/reset/pause/resume/abort;
- duplicate request/result retrieval;
- bounded history/subscribers/backpressure;
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

Consume Surveyor outputs; do not copy internals.

Expose:

- coverage summary;
- evidence/index status;
- read-only runtime snapshot;
- current-client fence/provenance;
- bundle reference/status.

Incompatible/missing Surveyor becomes explicit `UNAVAILABLE/INCOMPATIBLE`, not fabricated data.

Control Center per-run artifacts reference Surveyor/evidence registries but do not silently promote or overwrite them.

## Package D — official Track A action adapter

Separate runtime-sensitive task. This prompt does not authorize it.

Before any real action:

- read then-current trusted-base Track A governance;
- create a current runtime task;
- obtain current runtime access class;
- satisfy current canonical lease/registration/Gate A/rebind/Gate B/target uniqueness/whole-lifetime supervisor requirements;
- use current shared GUI input lock when applicable;
- prove action evidence/parity gate;
- define action-specific maximum plausible effect/budget;
- integrate final `atomic_dispatch` check inside the existing Track A guarded mutation boundary;
- start with one smallest already-proven semantic action.

Never implement a second lease manager, registration source of truth or authority lock inside Control Center.

## Package E — Oteryn v2 adapter

Separate task/branch/PR in:

```text
blakinio/Oteryn-v2
```

Read current Oteryn governance and accepted `docs/architecture/ADR-0007-native-end-to-end-test-platform.md`.

The adapter must integrate with Oteryn's existing shared E2E architecture or an explicitly versioned cross-repo semantic contract. Do not create a second Oteryn E2E platform.

Requirements:

- keep `protocol-oteryn`;
- client sends semantic intent;
- server remains authoritative;
- no hidden authoritative mutation hook;
- no unauthenticated production test-control interface;
- test-only hooks excluded/locked down under Oteryn policy;
- generic semantic capability model, not fake Track A R/A grades.

# 4. UI requirements

Always-visible state should separate:

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

Never present `MUTATION_ALLOWED` as a checkbox or local preference.

Unknown/unproven/stale fields render truthfully as `UNKNOWN`, `UNSUPPORTED`, `NOT_PROVEN`, `STALE` or equivalent.

Every manual Quick Action becomes exactly one validated one-step experiment through the normal Scenario Engine path.

# 5. Differential comparison rules

Use explicit comparison profiles.

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

Do not report an E2E mismatch when the reference field is unobservable/UNKNOWN. Report coverage state instead.

# 6. Package A mandatory deterministic tests

Package A is not complete until all of these pass without Track A runtime access:

1. scenario schema accept/reject;
2. deterministic stable step IDs;
3. typed predicate UNKNOWN behavior;
4. unsupported capability refusal;
5. mutation refusal under read-only authority;
6. authority expires exactly at final dispatch admission;
7. runtime instance changes exactly at final dispatch admission;
8. session epoch changes exactly at final dispatch admission;
9. adapter generation changes exactly at final dispatch admission;
10. two concurrent mutation requests serialize;
11. browser/CLI-equivalent duplicate logical request model dispatches once;
12. same `action_id` + same request returns existing result;
13. same `action_id` + different request is refused;
14. STOP linearizes before dispatch and prevents it;
15. dispatch linearizes before STOP and is classified already-dispatched;
16. stale completion from old control generation cannot resume/advance run;
17. queued old-generation action is rejected after STOP;
18. explicit reset creates fresh control generation and does not restore cached authority;
19. pause/resume after runtime/session change refuses pending mutation;
20. engine timeout;
21. cancellation while waiting;
22. cancellation before dispatch;
23. after-dispatch cancellation classification;
24. budget reservation and exhaustion;
25. duplicate request creates no second reservation;
26. ambiguous potion/consumable action conservatively consumes budget;
27. ambiguous action is not automatically retried;
28. possibly-dispatched crash recovery becomes `AMBIGUOUS`;
29. not-dispatched crash recovery does not silently execute;
30. source/ingest clocks from different domains remain distinguishable;
31. ingestion sequence never masquerades as causal proof;
32. late event cannot rewrite terminal result;
33. causal fields preserve stimulus/direction/lane/sequence/handler/object/delta/evidence refs when provided;
34. secret-shaped event input rejected before ordinary event construction;
35. exception/repr secret-shaped text does not reach `safe_message`;
36. screenshot secret-risk path is quarantined/rejected;
37. artifact crash remains incomplete, never PASS;
38. finalized artifact is stable/immutable except explicit supplement;
39. fake one-step scenario succeeds deterministically;
40. no browser/CLI-facing domain interface can call adapter directly.

Add focused property/race tests where deterministic interleavings are easier to express parametrically.

# 7. Package B mandatory tests

At minimum:

- loopback bind default;
- non-loopback request/config fails closed absent separate approved profile;
- request/body/collection bounds;
- bounded event history/subscriber/backpressure behavior;
- malformed API requests;
- duplicate POST idempotency/result retrieval;
- browser/CLI semantic parity for shared domain operations;
- authority/capability/evidence/freshness rendered separately;
- disabled/refused real mutation under read-only/unknown/stale authority;
- STOP/reset visible state;
- browser reload does not duplicate active run/action;
- shutdown leaves truthful terminal/incomplete state.

# 8. Security/privacy acceptance

Fail the implementation if any ordinary persistent/loggable object can accidentally contain:

- email/password/2FA;
- auth/session tokens;
- cookies/tickets;
- encryption/RSA secret material;
- raw secret-bearing network payload;
- environment variable value;
- arbitrary unsanitized adapter exception text;
- unapproved private chat text;
- unreviewed login/auth screenshot.

Use stable reason codes and explicitly safe fields.

# 9. Validation procedure

For every package PR:

1. inspect full changed-file list and full diff;
2. run focused deterministic tests;
3. select exact commands from current `BUILD_TEST_MATRIX.md`; do not invent presets;
4. run required exact-head CI;
5. perform full self-review against the normative architecture/contracts;
6. perform or obtain independent review when current repository risk policy requires it;
7. specifically re-run affected race/idempotency/privacy tests after any concurrency or error-path change;
8. update task/checkpoint with exact commands/outcomes/SHA;
9. update module catalogue/changelog when required and not blocked by current path ownership;
10. merge only through current repository policy after all gates pass.

# 10. Mandatory non-claims

Never claim:

- official mutation capability from fake tests;
- Track A authority from Control Center state;
- runtime compatibility from repository-only tests;
- causal proof from timestamp correlation;
- exact source ordering across different clock domains without evidence;
- no side effect merely because an after-dispatch call timed out;
- Oteryn parity before its separate adapter exists;
- Oteryn failure when official reference state is unobservable;
- remote/LAN security before a separate exposure design is accepted;
- safe secret handling from export-time redaction alone.

# 11. Package A terminal acceptance

Package A may be called implementation-ready only when all are true:

```text
runtime_access=none
network_listener=none
real_official_client_access=none
all mandatory deterministic tests=PASS
no adapter bypass=PASS
atomic dispatch model=PASS
STOP race model=PASS
idempotency/replay=PASS
budget ambiguity handling=PASS
multi-clock recorder=PASS
construction-time secret rejection=PASS
artifact crash/finalization=PASS
self-review=no material findings
required independent review=PASS when applicable
exact-head CI=PASS
```

A fresh agent must be able to continue from Git/task/PR alone without this chat.

# 12. Desired first operator result

After Packages A-C the operator should be able to:

- start the Control Center locally;
- use browser or CLI against the same backend;
- inspect truthful read-only Track A/Surveyor status;
- see authority/capability/evidence/freshness separately;
- browse scenarios/runs/actions/events/artifacts;
- execute deterministic fake-adapter one-step experiments;
- prove STOP ALL/idempotency/cancellation behavior;
- export privacy-safe `agent_bundle.json`;

while every real official-client mutation remains fail-closed until Package D receives its own current Track A authority and runtime evidence.