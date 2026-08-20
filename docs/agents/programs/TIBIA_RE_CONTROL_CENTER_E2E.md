# TIBIA RE Control Center / E2E Lab

```yaml
programme: TIBIA-RE-CONTROL-CENTER-E2E
repository: blakinio/otclient
track: official-client-re
status: hardened_design_baseline
version: 2.1
runtime_access_of_this_document: none
future_official_client_runtime: Track A canonical live runtime only
future_oteryn_runtime: separate adapter task in blakinio/Oteryn-v2
```

## 1. Mission

Build one reusable research/E2E control plane that can:

1. observe the official native Linux Tibia client under current Track A governance;
2. execute bounded semantic actions only when current external mutation authority survives until the final irreversible dispatch boundary;
3. stay fail-closed under STOP races, duplicate requests, lost responses, client restarts and backend crashes;
4. correlate controlled stimuli with state/network/trace/screenshot evidence without confusing ingestion order with causality;
5. produce deterministic privacy-safe run artifacts;
6. expose exactly the same domain operations to browser and direct-machine CLI;
7. later run the same semantic scenarios against Oteryn v2 through its existing E2E architecture;
8. compare official-client and Oteryn results at normalized semantic checkpoints.

The Control Center is a research/test harness. It is not:

- a Tibia game client;
- a Track A lease/registration authority;
- a protocol authority;
- a credential/login authority;
- an Oteryn gameplay/server authority;
- a second Oteryn E2E framework.

## 2. Fundamental separation

```text
scenario validity
!= semantic capability support
!= semantic field-schema support
!= evidence maturity
!= observation freshness
!= mutation authority
```

No UI state, checkbox, CLI option, scenario field, semantic registry, API nonce, cached `MUTATION_ALLOWED`, successful preflight or adapter capability creates official-client mutation authority.

## 3. Normative contract stack

A competent implementation agent must read these together:

1. `docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md`
   - causal RE methodology, negative controls, R0-R4/A0-A4 evidence meaning;
2. `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_SCENARIO_V1.md`
   - bounded parser, immutable semantic-field registries, typed predicates/references/actions, canonical hashes, retry and `SideEffectBudget`/`EffectBound` semantics;
3. `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md`
   - backend epochs, MutationCoordinator, final dispatch commit, durable STOP/reset, idempotency, durability, budgets, privacy, recorder and crash recovery;
4. `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md`
   - semantic client adapter boundary, semantic-registry advertisement/projection and official/Oteryn invariants;
5. `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ARTIFACT_V1.md`
   - global RequestLedger/ControlState safety authority, per-run Action/Budget/Recovery state, artifact staging/finalization and retention;
6. `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_CONTROL_API_V1.md`
   - browser/CLI loopback transport, nonce/Host/Origin/anti-framing policy, crash-safe request admission, bounds/backpressure and shutdown;
7. `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_COMPARISON_V1.md`
   - versioned semantic comparison profiles, checkpoints, mismatch and coverage-gap semantics;
8. this programme;
9. `docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_MVP.md`.

The contracts above are mutually normative. If prose in this programme is less specific, the relevant versioned contract controls. For any future Official Tibia mutation, then-current trusted-base Track A contracts additionally override stale Track A examples in this package.

## 4. Existing infrastructure is authoritative

Control Center must REUSE/EXTEND, never replace:

- canonical Track A lease manager;
- authoritative canonical runtime registration;
- Gate A;
- generation rebind;
- Gate B;
- target/process/window/display uniqueness/identity proof;
- cancellation-safe whole-lifetime supervisor/guard;
- shared GUI input lock;
- activity heartbeat where applicable;
- `tools/tibia_runtime_bridge/**` where its current contract applies;
- Track A capability/evidence registries;
- Surveyor outputs only after an accepted exact producer/schema exists;
- Oteryn-v2 accepted `ADR-0007-native-end-to-end-test-platform.md`.

Per-run or global Control Center safety state may reference these authorities but never promote, overwrite or replace them.

## 5. Target architecture

```text
                            TIBIA RE CONTROL CENTER

             Browser UI                          CLI
                  |                               |
                  +---------- same origin/API ----+
                                  |
                          Control API v1
                                  |
                         Control Domain Service
                                  |
                 +----------------+----------------+
                 |                                 |
              Read Models                       Run Manager
                 |                                 |
      Semantic Field Registry                 Scenario Engine
                 |                                 |
                 +-------------------+-------------+-------------+
                                     |                           |
                                  Recorder                MutationCoordinator
                                     |                           |
                               Artifact Store              Safety Controller
                                     |                           |
                           Global Safety Store            Semantic Adapter v1
                                                                  /        \
                                                         Official Tibia   Oteryn v2
                                                             |               |
                                                       current Track A   ADR-0007
```

The logical storage split is:

```text
Global Safety Store
  -> RequestLedger
  -> ControlState / STOP latch

Per-run Safety/Artifact State
  -> ActionLedger
  -> BudgetLedger
  -> Recovery
  -> staging/finalized evidence
```

Presentation artifacts are never the authority for those safety records.

### 5.1 One-path invariant

Forbidden architectures:

```text
Browser -> raw adapter
CLI -> direct adapter
Quick Action -> xdotool/raw key/raw bridge
Scenario -> lease/registration edits
Scenario predicate -> arbitrary snapshot object traversal
Recorder -> capability promotion
Artifact/report -> safety-state authority
Oteryn adapter -> hidden server-authoritative mutation hook
```

## 6. Core components

### 6.1 Control Domain Service

One in-process domain surface used by every operator transport. It owns no concrete client manipulation.

### 6.2 Run Manager

Owns run lifecycle, scenario scheduling, run persistence references and recovery classification. It enforces the Scenario-v1 absolute monotonic run deadline.

### 6.3 Scenario Engine

Owns deterministic Scenario-v1 parsing/validation/execution semantics:

- bounded JSON/YAML parser;
- immutable semantic field-registry selection;
- canonical scenario/action hashes;
- stable step IDs;
- typed predicates and UNKNOWN policy;
- typed discriminated semantic references;
- exact `SideEffectBudget` and action `EffectBound` handling;
- preconditions/assertions/waits;
- explicit retries only after proven `NOT_DISPATCHED`;
- pause/resume fencing;
- failure propagation;
- one-step experiment representation.

It does not own external mutation authority.

### 6.4 Semantic Field Registry

The Scenario Engine owns `control-center.core@1.0.0`. Adapter extensions use the exact Scenario-v1 registry schema and Adapter-v1 descriptor/hash negotiation.

A path missing from the selected immutable registry is a validation error. A registered field may later be `UNKNOWN`/`STALE` at observation time, but an unregistered field may never be treated as a loosely typed runtime value.

Registry support, capability support, evidence maturity and mutation authority remain independent.

### 6.5 MutationCoordinator

Exactly one per adapter instance.

Owns local:

- mutation-run serialization;
- `backend_epoch`;
- `control_generation`;
- ActionLedger/idempotency;
- BudgetLedger;
- recovered durable ControlState/STOP latch;
- tiny `dispatch_gate`;
- STOP/reset linearization;
- one-shot durable dispatch commit.

It never becomes a Track A lease/registration authority.

### 6.6 Safety Controller

A facade/consumer over current external safety sources:

- current capability support;
- current runtime/session/adapter fences;
- current official Track A authority/identity when applicable;
- current GUI input lock state where applicable.

No local setting can weaken external gates.

### 6.7 Recorder

Owns normalized events, source/ingest clocks and causal metadata. Recorder cannot promote correlation to causal proof or capability evidence.

### 6.8 Global Safety Store

Owns only durable Control Center-local safety state that is not necessarily run-scoped:

- RequestLedger request/resource/transition identity;
- ControlState and STOP/reset recovery.

For protected POST operations, stable request/resource identity is durable before scheduling or domain/control transition according to Control API/Artifact v1.

A missing/corrupt/contradictory safety state fails closed; restart does not synthesize a reset or a new resource.

### 6.9 Artifact Store

Owns per-run safety/evidence staging/finalization plus presentation materialization:

- Action/Budget/Recovery safety state;
- staged normalized scenario/events/actions/snapshots/captures;
- immutable finalized results;
- append-only supplements.

Safety-critical state survives ordinary report/render failure and cannot be reconstructed optimistically from UI/report text.

### 6.10 Adapter

Maps semantic intent to one client-specific implementation while hiding raw implementation details.

Adapter-v1 semantic-field projection is observational metadata/read behavior and cannot create action support or mutation authority.

## 7. Backend epoch, ControlState and stale-work fencing

Every backend start creates a fresh unique `backend_epoch`.

Within it, `control_generation` is monotonic and scoped to that epoch.

All runs/actions/events/results include these fences where applicable.

Before mutation admission, backend recovery must process Artifact-v1 safety state including ControlState.

Backend restart:

- never reuses old epoch;
- never accepts old-epoch callbacks as control input;
- never auto-resumes mutation-capable work;
- never treats restart as STOP reset;
- carries a valid durable `stop_latched=true` into the new backend as STOPPED;
- fails closed on missing/corrupt/contradictory safety state when prior state may exist;
- reacquires external authority fresh.

## 8. Mutation preparation versus final commit

### 8.1 Preparation

Outside local `dispatch_gate`:

- validate scenario/action and semantic registry;
- compute conservative EffectBound;
- verify remaining SideEffectBudget and total action/run deadlines;
- reserve applicable non-time budget;
- run advisory preflight;
- acquire external/Track A guard;
- acquire GUI input lock where required;
- capture before-state.

All waits are bounded/cancellable. Preflight and registry/capability state grant no standing authority.

### 8.2 Final commit

While required external authority guard remains held:

```text
enter dispatch_gate
-> revalidate action/hash/run ownership/backend/control/STOP/adapter/runtime/session
-> revalidate budget/capability/current external authority/input lock/current Track A identity
-> durably write DISPATCH_COMMITTED + POSSIBLY_DISPATCHED + applicable non-time budget AT_RISK
-> local durability barrier succeeds
-> leave dispatch_gate
-> while external guard remains continuously held, cross physical irreversible boundary exactly once
-> reconcile terminal result/evidence/budget
```

The only I/O allowed while holding `dispatch_gate` is one bounded local safety-store transaction of an Execution-v1 allowed kind:

```text
DISPATCH_COMMIT
STOP_TRANSITION
RESET_TRANSITION
```

Each has a finite local deadline and no external network dependency.

Dispatch durability failure/timeout -> no dispatch.

## 9. Official Track A dispatch

For Official Tibia:

1. obtain current Track A authority using existing trusted-base mechanisms;
2. do not hold local `dispatch_gate` while waiting for Track A locks/guard;
3. when Track A guard is held, revalidate current Track A identity/authority;
4. retain the required GUI/input lock;
5. invoke local one-shot `commit_dispatch()`;
6. after COMMITTED, perform exactly one physical effect while Track A guard remains continuously held;
7. preserve whole-lifetime supervisor behavior for mutation descendants.

The Control Center never implements a second lease manager, registration path or alternative Track A guard.

## 10. STOP ALL and reset

STOP is a durable linearizable safety transition.

```text
STOP wins dispatch_gate
  -> durable STOP_TRANSITION writes stop_latched=true + new generation
  -> stale action cannot commit
  -> no physical effect begins

Action commit wins dispatch_gate
  -> action is durably possible-dispatched/at-risk
  -> later STOP durably latches a newer generation
  -> no claim that STOP reversed the committed action
```

STOP additionally rejects new mutation admission, cancels queued/waiting old-generation work, wakes waits, requests cooperative cancellation and closes harness-owned passive resources.

STOP durability failure leaves the current backend fail-closed. Crash/restart with uncertain/corrupt ControlState remains fail-closed.

STOP does **not** grant authority to send gameplay stop input, kill/restart the client or perform compensating mutation.

Reset is explicit, local and durable. It advances control generation and clears only the STOP latch after Execution-v1 reset preconditions and durability barrier succeed. Reset never clears unresolved ambiguous Action/Budget state and never restores cached Track A authority. Reset failure leaves STOP latched.

## 11. Idempotency hierarchy

Two distinct IDs exist:

```text
request_id  -> transport/domain request dedupe (Control API v1)
action_id   -> semantic action-attempt dedupe (Execution/Scenario v1)
```

For protected POST requests:

```text
validate/hash
-> allocate stable resource/transition identity
-> durably atomically record RequestLedger INTENT_DURABLE + minimum resource/control record
-> only then schedule/transition
```

Repeated same request ID/hash returns/reconstructs the same logical resource/transition. Same ID with different normalized request hash conflicts.

Possible-dispatch action is never auto-retried. Surviving request intent after backend restart never auto-resumes mutation work.

## 12. Side-effect budgets and runtime deadline

Scenario v1 provides one required `SideEffectBudget`:

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

The runtime dimension is an absolute monotonic run deadline and also constrains every action's total attempt timeout. It is never extended by pause, ambiguity or retry.

Non-time hard dimensions use the Execution-v1 ledger state:

```text
limit
reserved
at_risk
committed
uncertain
```

Action effects are bounded before dispatch using Scenario-v1 EffectBound. At dispatch commit applicable non-time reserved effect moves atomically to at-risk. Uncertain/ambiguous effect counts as consumed until authoritative reconciliation.

Hard budget with no safe finite bound -> refuse before dispatch. Tibia Coins and irreversible changes default to zero unless explicitly separately admitted.

## 13. Crash/restart semantics

Durable action dispatch classes:

```text
NOT_DISPATCHED
POSSIBLY_DISPATCHED
CONFIRMED
```

Crash after durable dispatch commit but before physical outcome is known -> `AMBIGUOUS` unless authoritative reconciliation proves exact effect/no-effect.

`CONFIRMED` is the successful terminal action lifecycle state. Late callbacks/events cannot rewrite it as another control outcome.

Missing/corrupt/contradictory Action/Budget/Control/Request safety state -> fail closed.

No automatic mutation resume or retry after restart.

## 14. Scenario semantics

Scenario v1 defines:

- bounded safe YAML/JSON parsing;
- duplicate-key/custom-tag/alias controls;
- JCS/SHA-256 canonical scenario/action hashes;
- stable step IDs;
- immutable semantic field registry identity/version and typed field descriptors;
- typed predicates without implicit coercion;
- discriminated entity/item/destination references;
- action schemas for movement, turn, spells, consumables, runes, targeting/combat, inventory/containers, equipment, UI panels and logout;
- total action-attempt deadlines and retry only after proven `NOT_DISPATCHED`;
- SideEffectBudget/EffectBound;
- capture policy;
- abort/privacy policy.

`login_request`/`enter_game_request` remain non-executable capability placeholders until a separate accepted auth/session execution contract exists.

## 15. Capture boundary

Capture configuration is not authority.

Passive capture operations may start only producers already admitted as read-only/passive.

If enabling capture requires attach/injection/input/process/network mutation, the passive capture request refuses. The invasive transition must be modeled as a separately governed semantic action/contract through normal mutation authority/dispatch semantics.

Screenshot states:

```text
SAFE
QUARANTINED
REJECTED
```

Unknown login/auth content does not enter normal run artifacts.

## 16. Recorder/causal evidence

Unified `events.jsonl` is ingestion order only.

Every event preserves where applicable:

- ingest sequence;
- ingestion monotonic time;
- source timestamp;
- source clock domain;
- source-local sequence/scope;
- ordering confidence;
- backend/control/adapter/runtime/session fences;
- run/experiment/step/stimulus identity;
- late flag;
- sensitivity.

Track A causal fields preserve stimulus/BACKGROUND, direction, message sequence/type/lane, thread, handler/runtime object/object epoch, before/after hashes, semantic delta and evidence ref when observable.

Negative/no-stimulus controls remain required where causal promotion depends on them. Correlation/ingestion order is never automatic causal proof.

## 17. Privacy invariant

> Secret-class data never enters normal Event, Artifact, Error, Report or AgentBundle objects.

Classification/redaction/rejection occurs before ordinary object construction.

Never persist:

- account email/password/2FA;
- session/auth tokens;
- cookies/tickets;
- encryption/RSA secret material;
- secret-bearing packet/memory material;
- environment variable values;
- arbitrary unsanitized exception/debug/repr text;
- unnecessary private chat/personal data;
- unapproved login/auth screenshots;
- Control API nonce.

`SECRET_REJECTED` contains category/reason only, not value/hash/reversible derivative. Export-time redaction is defense in depth only.

## 18. Network capture

Default persistent capture is metadata-only:

```text
direction
connection/session lane
source-local sequence when known
structurally known message type
size
correlation ID
payload_capture=NONE
```

No raw-payload fallback. Future sanitized payload capture is a separate explicit security/capture-policy task.

## 19. Run/artifact lifecycle

```text
ACTIVE -> CLOSING -> FINALIZED
```

CLOSING performs a bounded source drain/watermark where possible.

Late events cannot rewrite terminal action/run result, resume execution or authorize retry.

Finalized history is immutable; later accepted evidence is an append-only supplement.

Crash before finalization leaves explicit incomplete state, never synthesized PASS.

Safety-state authority remains in Artifact-v1 global/per-run safety records independent of presentation finalization.

## 20. Browser/CLI Control API

Control API v1 is local-only and same-backend.

Security baseline:

- exact `127.0.0.1` default bind;
- wildcard/non-loopback forbidden;
- fresh >=256-bit `control_nonce` per backend epoch;
- nonce in custom header, never URL/query/fragment/log/artifact;
- exact Host allowlist to resist DNS rebinding;
- exact same-origin browser Origin policy;
- mandatory CSP `frame-ancestors 'none'` for the initial UI;
- no permissive CORS/cookie ambient auth;
- every `/v1/*` request authenticated with current nonce;
- global durable `request_id` ledger for every POST;
- durable request/resource intent before protected scheduling/control transition;
- bounded bodies/pages/events/subscribers/backpressure;
- no raw/debug/adapter bypass endpoints;
- remote/LAN unsupported in v1;
- graceful shutdown flushes required safety state and invalidates nonce.

The API nonce grants local Control API access only; it never grants Track A mutation authority.

## 21. UI information architecture

Always-visible status separates:

```text
RUNTIME | CLIENT | RECORDER | AUTHORITY | CAPABILITY | EVIDENCE | FRESHNESS | SESSION
STOP ALL | PAUSE
```

Required major tabs:

```text
Main
Runtime
Movement
Healing
Spells
Consumables
Combat
Targeting
Inventory
Containers
Equipment
Chat
Conditions
Scenarios
Recorder
Network
Experiments
Compare
Logger
```

Unknown/unproven/stale data renders truthfully as `UNKNOWN`, `UNSUPPORTED`, `NOT_PROVEN`, `STALE` or another explicit state.

`MUTATION_ALLOWED` is a status label, never a checkbox or grant.

Every Quick Action becomes exactly one validated one-step experiment through Scenario Engine.

## 22. Official adapter

Official Tibia adapter is `EXTEND_EXISTING` over current Track A infrastructure.

It may use approved current mechanisms such as:

- `tools/tibia_runtime_bridge/**`;
- GUI input under current shared input lock;
- stable semantic bridge methods;
- bounded instrumentation where separately admitted.

Generic semantic support:

```text
read_supported
action_supported
```

Official-only research maturity:

```text
R0-R4
A0-A4
evidence refs
```

Read support, semantic-registry support and action support are independent.

## 23. Surveyor integration

Package C only after an accepted exact Surveyor producer state exists.

Pin:

```text
surveyor_schema_version
producer_commit
producer_interface
```

Mismatch -> explicit `UNAVAILABLE/INCOMPATIBLE`, not copied logic/fabricated data.

Control Center does not silently promote Surveyor-owned coverage/evidence state.

## 24. Oteryn v2 adapter

Canonical implementation lives in `blakinio/Oteryn-v2` under a separate task/branch/PR.

It integrates with current accepted ADR-0007 or an explicit versioned cross-repo semantic boundary.

Requirements:

- retain `protocol-oteryn`;
- client sends semantic intent;
- server remains authoritative;
- no Tibia wire compatibility shortcut;
- no hidden authoritative client mutation hook;
- no unauthenticated production test-control surface;
- test-only hooks excluded/locked down by Oteryn production policy;
- generic semantic capability model, not Track A R/A grades.

## 25. Differential E2E

Versioned comparison classes:

```text
EXACT
NORMALIZED_EXACT
SET_EQUIVALENT
ORDERED_EQUIVALENT
TOLERANCE
REFERENCE_ONLY
NOT_COMPARABLE
```

Default field baseline:

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

Mismatch exists only when both sides support/observe the field at the same normalized checkpoint, neither is UNKNOWN and the candidate violates the selected rule.

Missing official observation is a coverage gap, not Oteryn failure.

## 26. Implementation phases

### P0 — hardened contract/falsification baseline

- programme;
- Scenario v1;
- Execution v1;
- Adapter v1;
- Artifact v1;
- Control API v1;
- Comparison v1;
- MVP prompt;
- independent audit prompt.

### P1 — Package A control-core

`runtime_access:none`, no network listener, no official client.

Deliver:

- typed contract models including semantic registry descriptors/projections;
- bounded Scenario v1 parser/hash/validator;
- deterministic fake adapter/manual clock;
- MutationCoordinator and dispatch gate;
- Action/Budget ledgers and durable ControlState abstraction;
- deterministic durability store abstraction;
- STOP/reset/restart semantics;
- Recorder/causal event model;
- construction-time privacy boundaries;
- Artifact staging/finalization;
- pure Comparison profile/result types/tests where implemented;
- full deterministic falsification suite.

### P2 — Package B local Control API + browser + CLI

Consume merged A.

Deliver persistent local store for global RequestLedger + ControlState + Action/Budget dispatch journal, Control API v1, thin browser/CLI clients, run/event/artifact views and fake-adapter operations.

No official-client mutation.

### P3 — Package C accepted Surveyor/read-only integration

Pin exact accepted producer/schema/interface.

### P4 — Package D Official Track A mutation adapter

Separate runtime-sensitive task. Start with one smallest already-proven semantic action through then-current Track A authority + durable local commit.

### P5 — runtime capture producers

Add only bounded passive/currently authorized network metadata, trace and screenshot producers; invasive enablement remains separately governed.

### P6 — research suites

Add feature families only as capability evidence exists.

### P7 — Package E Oteryn v2 adapter

Separate Oteryn task/PR aligned with ADR-0007.

### P8 — differential E2E

Run identical semantic scenarios/checkpoints and emit versioned mismatch/coverage reports.

## 27. Package A implementation readiness

Package A may start only after a fresh independent auditor answers YES:

> Can a competent implementation agent implement Package A solely from current repository documentation without inventing scenario types, semantic registry, concurrency, dispatch, STOP, retry, durability, budget, privacy, event-ordering, artifact or restart semantics?

All safety-critical falsification cases in the independent-audit prompt must be `SAFE_DEFINED`.

## 28. First useful operator release

After Packages A-C:

```text
Browser GUI                           YES
CLI                                   YES
Secure local Control API v1           YES
Read-only runtime status              YES
Capability/evidence/freshness views   YES
Live normalized event stream          YES
Scenario catalogue/browser            YES
Fake one-step experiments              YES
STOP/idempotency/restart safety        YES
Artifact/run browser                   YES
privacy-safe agent_bundle.json         YES
real official-client mutation          NO until separately admitted Package D
Oteryn adapter                         NO until separate Oteryn task
```

## 29. Non-goals

Control Center must not:

- replace Track A authority/registration/supervisor;
- infer authority from visible process/window;
- persist credentials/secret auth material;
- expose unauthenticated remote control;
- turn UI/API/semantic-registry state into authority;
- create a raw automation bypass;
- implement a second Tibia protocol stack;
- claim byte-level Official-vs-Oteryn parity;
- claim causality from timing alone;
- make historical `oteryn-client/**` canonical;
- create a second Oteryn E2E platform.

## 30. Implementation language guidance

Python remains the preferred initial official-side orchestration language because existing Surveyor/runtime tooling is Python and reuse minimizes duplication.

Browser UI should remain thin HTML/CSS/JavaScript unless current repository evidence justifies an existing approved frontend stack.

This is guidance only; current repository dependency/test policy remains authoritative.

## 31. Required package split

```text
Package A  control-core + Scenario/Execution/Recorder/Artifact/fake durability tests
Package B  Control API v1 + browser + CLI + global RequestLedger/persistent safety store
Package C  accepted Surveyor/read-only integration
Package D  separately admitted official Track A mutation adapter
Package E  separately governed Oteryn-v2 adapter
```

Shared public contracts have one producer at a time. Later workers consume merged contracts rather than redefining them.