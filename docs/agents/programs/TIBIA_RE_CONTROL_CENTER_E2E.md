# TIBIA RE Control Center / E2E Lab

```yaml
programme: TIBIA-RE-CONTROL-CENTER-E2E
repository: blakinio/otclient
track: official-client-re
status: hardened_design_baseline
version: 1.2
runtime_access_of_this_document: none
future_official_client_runtime: Track A canonical live runtime only
future_oteryn_runtime: separate adapter task in blakinio/Oteryn-v2
```

## 1. Purpose

Build one reusable research and E2E platform that can:

1. observe the official Tibia Linux client under existing Track A governance;
2. execute bounded semantic research actions only when current external mutation authority exists at the final dispatch boundary;
3. remain safe under STOP races, duplicate requests, lost responses, backend crashes and client/runtime generation changes;
4. correlate controlled stimuli with runtime state, network metadata, targeted traces and screenshots without confusing temporal ordering with causality;
5. produce deterministic, privacy-safe, machine-readable per-run evidence bundles;
6. expose identical domain semantics to browser and direct-machine CLI operation;
7. later run the same semantic scenarios against the Oteryn v2 Rust client through a separately governed adapter;
8. compare official-client and Oteryn outcomes at normalized semantic state-transition checkpoints.

The Control Center is a research/test harness. It is not the game client, not a protocol authority, not a Track A lease/registration authority and not an Oteryn server authority.

Normative separation:

```text
scenario validity
!= capability support
!= evidence maturity
!= observation freshness
!= mutation authority
```

No local configuration, UI state, CLI option, cached status, prior preflight or adapter capability can create mutation authority.

## 2. Normative document stack

Read these as one design package:

1. `docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md` — causal RE/evidence methodology;
2. `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md` — concurrency, dispatch commit, STOP, idempotency, budget, recorder, privacy and recovery semantics;
3. `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md` — semantic adapter data/API boundary;
4. this programme — product architecture/phasing;
5. `docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_MVP.md` — bounded implementation procedure.

For future official-client work, then-current trusted-base Track A admission/lease/registration/Gate A/rebind/Gate B/target-identity/GUI-lock/whole-lifetime-supervisor contracts take precedence over stale examples.

## 3. Existing systems to reuse

Do not replace:

- Track A canonical lease manager;
- authoritative runtime registration;
- Gate A, generation rebind and Gate B;
- canonical target-uniqueness proof;
- cancellation-safe whole-lifetime mutation supervisor/guard;
- shared GUI input lock/guard;
- shared activity heartbeat where applicable;
- `tools/tibia_runtime_bridge/**` for current identity/bridge behavior where its contract applies;
- Track A capability/evidence registries;
- Surveyor #592 outputs/interfaces after an exact accepted producer state exists;
- Oteryn v2's accepted native E2E architecture, currently owned by `docs/architecture/ADR-0007-native-end-to-end-test-platform.md` in `blakinio/Oteryn-v2`.

Control Center may normalize and reference these systems but must not become their second source of truth.

## 4. Product architecture

There is one backend domain path and two operator surfaces.

```text
                       TIBIA RE CONTROL CENTER

              Browser UI                 CLI
                   \                     /
                    \                   /
                     v                 v
                    Versioned Control API
                             |
                             v
                   Control Domain Service
                             |
                    +--------+---------+
                    |                  |
                 Run Manager        Read Models
                    |
                    v
                Scenario Engine
                    |
          +---------+---------+----------------+
          |                   |                |
       Recorder        MutationCoordinator   Artifact Store
          |                   |
          |             Safety Controller
          |                   |
          +-------------------+
                    |
                    v
               Adapter Contract
                 /          \
                /            \
       Official Tibia       Oteryn v2
          Adapter             Adapter
             |                   |
     current Track A       Oteryn QA-E2E
       infrastructure        integration
```

### 4.1 Hard invariants

- Browser and CLI never call adapters directly.
- Quick Actions are one-step scenarios, not a second mutation path.
- Scenario Engine never stores standing Track A mutation authority.
- MutationCoordinator owns local serialization/idempotency/generations/dispatch commit only.
- Safety Controller consumes external authority; it is not a new lease manager.
- Recorder preserves evidence but cannot grant capability/authority.
- Artifact Store owns per-run artifacts only; it cannot promote Track A evidence registries.
- Comparator compares normalized semantics only.

## 5. Backend epoch and local generations

Every backend process has a fresh opaque unique `backend_epoch`.

Within that epoch, `control_generation` is monotonic and advances on STOP.

All action fences, results, events and run provenance include both values.

A backend restart:

- creates a new backend epoch;
- invalidates stale old-backend callbacks as control input;
- never automatically resumes mutation;
- requires fresh external status/authority.

This prevents a restarted process from accidentally reusing an old numeric generation value as if it belonged to the same control lifetime.

## 6. MutationCoordinator and dispatch gate

Every adapter instance has one local `MutationCoordinator`.

It owns:

- one-action mutation serialization;
- action idempotency ledger;
- side-effect budget admission;
- backend/control-generation fencing;
- a tiny `dispatch_gate` used to linearize final dispatch commit versus STOP;
- local run/action state transitions.

It does not own external Track A authority.

The `dispatch_gate` must not be held while waiting for slow/external authority, I/O, Track A locks, captures or GUI resources.

## 7. Two-stage mutation path

### 7.1 Preparation

Outside `dispatch_gate`, the engine/adapter may:

- validate schema/action;
- resolve capabilities;
- reserve maximum plausible side effects;
- run advisory preflight;
- await/acquire adapter-specific external authority;
- acquire required shared input lock;
- capture before-state.

Preparation is bounded/cancellable and never creates standing authority.

### 7.2 Final dispatch commit

Immediately before the physical irreversible effect:

```text
hold current adapter-specific external authority/Track A guard
-> enter local dispatch_gate
-> revalidate backend/control/adapter/runtime/session/idempotency/budget/cancellation fences
-> revalidate exact current external authority
-> durably write DISPATCH_COMMITTED / POSSIBLY_DISPATCHED + AT_RISK budget state
-> durability barrier succeeds
-> exit dispatch_gate
-> while external authority guard remains continuously held, perform physical effect once
-> reconcile result/evidence/budget
```

If durable dispatch commit fails, physical mutation must not occur.

For `OFFICIAL_TIBIA`, the current canonical Track A guard/supervisor remains continuously held across the final authority checks, local `commit_dispatch()` and physical mutation. Control Center does not create a second Track A authority lock.

A prior `preflight=PASS` is diagnostic only and never sufficient to authorize dispatch.

## 8. Write-ahead safety

Before Package B accepts mutation-capable fake requests, and before any future real Package D mutation, selected storage must support a durable write-ahead dispatch commit.

The persisted point-of-no-safe-auto-retry records at minimum:

```text
backend epoch
control generation
action ID
normalized request hash
DISPATCH_COMMITTED
POSSIBLY_DISPATCHED
AT_RISK budget state
runtime/session/adapter fence summary
```

Crash after this commit but before physical effect is conservatively `AMBIGUOUS` unless authoritative reconciliation proves no effect.

This intentionally prefers ambiguity over duplicate mutation.

## 9. STOP ALL and cancellation

STOP is a state transition, not a best-effort UI request.

STOP and `commit_dispatch()` race on the same tiny `dispatch_gate`.

```text
STOP wins dispatch_gate
  -> control generation increments/latches STOP
  -> stale action cannot dispatch-commit
  -> physical mutation does not begin

Action commit wins dispatch_gate
  -> possible-dispatch state is durable
  -> STOP later classifies it already committed/in-flight
  -> no claim that STOP reversed it
```

There is no third outcome.

STOP then:

- rejects new mutation admission;
- cancels queued old-generation steps;
- signals active waits/captures/actions;
- rejects stale completion as control input;
- preserves useful stale/late evidence;
- performs bounded harness-owned cleanup;
- remains latched until explicit reset.

STOP does not kill the official client unless separate current process-control authority permits that exact effect.

## 10. Concurrency model

Default:

- one mutation-capable action per adapter at a time;
- no separate browser/CLI mutation implementations;
- concurrent read-only runs only where every source is proven concurrency-safe;
- unknown concurrency safety -> serialize;
- pending action invalidated by backend/control/adapter/runtime/session fence changes.

## 11. Deployment modes

### 11.1 Direct-machine

Backend runs on the machine hosting the applicable environment. CLI and local browser use the same backend/domain service.

### 11.2 Browser

Backend serves the same Control API plus thin web UI.

Initial Control API exposure is loopback-only. Existing KasmVNC may provide remote visual access without exposing a new control service.

Non-loopback control requires a separate accepted security design covering authentication, authorization, TLS/transport, origins, Host/CSRF/replay policy, rate/bounds and shutdown. A convenience `0.0.0.0` switch is not sufficient authorization.

## 12. Control API

Package B uses an explicit API major version, recommended `/v1`.

Responsibilities:

- status/freshness;
- capabilities/evidence maturity;
- scenarios/validation;
- run/action lifecycle;
- one-step experiments;
- STOP/reset/pause/resume/abort;
- bounded events;
- artifact inspection/export.

Required:

- bounded bodies/collections/history/subscribers;
- mutation idempotency keys;
- duplicate POST/result replay;
- action/result retrieval after connection loss;
- deterministic malformed-input errors;
- no raw action/debug bypass;
- explicit shutdown semantics;
- loopback fail-closed default.

## 13. Scenario Engine

Responsibilities:

- version/validate scenario;
- deterministic stable step IDs;
- typed predicates/preconditions/assertions/waits;
- explicit UNKNOWN semantics;
- capabilities;
- budget reservation;
- run/action lifecycle;
- one-step experiments;
- pause/resume fencing;
- bounded waits/timeouts;
- deterministic failure propagation;
- no hidden mutation retries.

Mutation retry defaults to zero.

A possible-dispatch/AMBIGUOUS action never automatically retries.

## 14. Scenario model

Every scenario includes at minimum:

```yaml
schema_version: 1
id:
name:
adapter_requirements:
preconditions:
side_effect_budget:
capture_policy:
steps:
abort_conditions:
expected_result:
privacy_policy:
```

Predicate baseline:

```yaml
field: player.hp
op: LT
value: 100
unknown_policy: FAIL
```

Unknown never silently satisfies a mutation-safety condition.

Example:

```yaml
schema_version: 1
id: healing-basic-001
name: Basic healing experiment
adapter_requirements:
  read: [player_state]
  actions: [cast_spell]
preconditions:
  - field: client_state
    op: EQ
    value: IN_GAME
    unknown_policy: FAIL
side_effect_budget:
  max_runtime_seconds: 60
  max_actions: 2
  max_spells: 1
  max_consumables: 0
  max_gold: 0
  max_tibia_coins: 0
  max_irreversible_changes: 0
capture_policy:
  state: true
  events: true
  screenshots: before_after
  network: metadata
  traces: targeted
steps:
  - snapshot:
      name: before
  - action:
      kind: cast_spell
      parameters:
        spell: exura
      timeout_ms: 3000
  - wait:
      condition:
        field: player.hp
        op: CHANGED
        unknown_policy: WAIT
      timeout_ms: 3000
  - snapshot:
      name: after
abort_conditions:
  - authority_lost
  - target_identity_changed
  - client_not_in_game
  - timeout
privacy_policy:
  secret_material: reject
```

## 15. Semantic action catalogue

Common scenarios express intent only:

```text
SYSTEM
wait
checkpoint

SESSION
login_request         capability only; credentials stay outside scenario payload
enter_game_request    capability only
logout

MOVEMENT
move
turn
stop_movement

CHAT
say_controlled_text

HEALING / SPELLS
cast_spell

CONSUMABLES
use_consumable
eat_food
use_rune

COMBAT
select_target
attack
cancel_attack
follow
cancel_follow

INVENTORY / CONTAINERS
open_container
close_container
use_item
look_item
move_item
equip
unequip

UI
open_panel
close_panel
```

Coordinates, raw keys, QMeta IDs, function addresses, vtables, opcodes and wire layouts do not leak into common scenario files.

## 16. Action lifecycle

Required states include:

```text
CREATED
VALIDATED
RESERVED
WAITING_AUTHORITY
DISPATCH_COMMITTED
DISPATCHING
CONFIRMING
CONFIRMED
REFUSED
CANCELLED_BEFORE_DISPATCH
CANCELLED_AFTER_DISPATCH
FAILED_BEFORE_DISPATCH
FAILED_AFTER_DISPATCH
TIMED_OUT_BEFORE_DISPATCH
TIMED_OUT_AFTER_DISPATCH
AMBIGUOUS
```

`DISPATCH_COMMITTED` is the local point of no safe automatic retry.

## 17. Side-effect budgets

Each run tracks per dimension:

```text
limit
reserved
at_risk
committed
uncertain
```

Before dispatch, reserve maximum plausible effect.

At durable dispatch commit, atomically move reservation to `at_risk`.

After outcome:

- proven no effect -> release only with proof;
- measured confirmed effect -> commit measured amount;
- dispatched but unmeasurable -> conservatively commit maximum plausible effect;
- timeout/failure/cancel/ambiguity after commit -> move maximum plausible effect to `uncertain`;
- uncertain counts as consumed until reconciled.

If a hard budget cannot be safely bounded, refuse before dispatch.

Minimum dimensions:

- runtime;
- action attempts;
- movement tiles;
- spells;
- consumables;
- moved items/stack amount;
- gold;
- Tibia Coins;
- irreversible changes.

TC and irreversible-change budgets default to zero unless separately authorized.

## 18. Recorder and causal evidence

Unified `events.jsonl` is ingestion order, not universal causal order.

Every event preserves:

- ingest sequence;
- ingestion monotonic time;
- source timestamp;
- source clock domain;
- source-local sequence/scope;
- ordering confidence;
- backend/control/adapter/runtime/session generations;
- run/step/stimulus identity;
- late flag;
- sensitivity.

For Track A causal RE preserve, when observable, stimulus ID, direction, lane/message sequence/type, runtime thread, handler/runtime-object/object-instance identity, before/after hashes, semantic delta and evidence ref.

Negative/no-stimulus controls remain mandatory where causal promotion requires them.

Timestamp correlation is not causal proof.

## 19. Late events and finalization

```text
ACTIVE -> CLOSING -> FINALIZED
```

During bounded CLOSING, drain sources/watermarks where possible.

Late events may enrich evidence but cannot rewrite terminal action result, resume execution or authorize retry.

After FINALIZED, later admitted evidence is append-only supplemental evidence referencing the original run.

## 20. Artifact Store

Per-run logical layout:

```text
runs/<run-id>/
  manifest.json
  scenario.yaml
  events.jsonl
  actions.jsonl
  state/
  network/
  traces/
  screenshots/
  result.json
  report.md
  agent_bundle.json
```

Rules:

- staging/incomplete before finalization;
- durable dispatch journal/action ledger must be flushed before physical mutation where Package B+ uses persistent fake/real dispatch;
- PASS manifest/result only after required ledgers/events are flushed;
- crash before finalization -> incomplete, never synthesized PASS;
- finalized result immutable except explicit supplement;
- provenance includes schema/scenario hash/adapter/backend epoch/control generation/runtime/session fences/budget/action summaries/artifact hashes;
- per-run store cannot overwrite Surveyor/Track A evidence registries.

## 21. Privacy and secret exclusion

Mandatory invariant:

> Secret-class data never enters normal Event, Artifact, Error, Report or AgentBundle objects.

Classification/redaction/rejection occurs before normal object creation. Export-time redaction is only defense in depth.

Never persist:

- email/password/2FA;
- auth/session tokens;
- cookies/tickets;
- encryption/RSA secret material;
- secret-bearing memory/packet payloads;
- environment-variable values;
- unnecessary private chat/personal data.

Arbitrary exception/debug/repr text is untrusted.

Screenshots are admitted only when known non-secret or through quarantine/sanitization; login/auth screens are not normal run artifacts.

## 22. Network capture

Default persistence is metadata only:

```text
direction
connection/session lane
source-local sequence when available
message type only when structurally known
size
correlation ID
payload_capture=NONE
```

No raw-payload fallback.

Future sanitized payload capture requires separate approved policy proving pre-persistence secret exclusion.

## 23. UI information architecture

Always-visible status separates:

```text
RUNTIME | CLIENT | RECORDER | AUTHORITY | CAPABILITY | EVIDENCE | FRESHNESS | SESSION
STOP ALL | PAUSE
```

Required tabs:

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

Unknown/unproven data renders as `UNKNOWN`, `UNSUPPORTED`, `NOT_PROVEN`, `STALE` or equivalent.

Quick Actions always become:

```text
snapshot before
-> semantic action
-> bounded wait/assertion
-> snapshot after
-> result
```

No unrecorded manual mutation shortcuts.

## 24. Official Tibia adapter

Official adapter is `EXTEND_EXISTING` Track A integration.

It may use approved mechanisms from:

- `tools/tibia_runtime_bridge/**`;
- normal GUI input under shared lock;
- stable semantic bridge methods;
- bounded targeted instrumentation.

Each mechanism remains subject to its current action/read evidence and Track A authority.

Capability reporting separates generic:

```text
read_supported
action_supported
```

from official-only:

```text
R0-R4
A0-A4
evidence refs
```

Read support never implies action support.

## 25. Surveyor boundary

Package C integrates only after an exact accepted Surveyor producer state exists and pins:

```text
surveyor_schema_version
producer_commit
producer_interface
```

Schema mismatch -> explicit `INCOMPATIBLE/UNAVAILABLE`; never copied internal logic or fabricated data.

## 26. Oteryn v2 boundary

Canonical Oteryn code is `blakinio/Oteryn-v2`.

Future adapter is a separate Oteryn task/branch/PR and integrates with accepted ADR-0007 or an explicitly versioned cross-repo semantic boundary.

It must not:

- add Tibia wire compatibility merely for the harness;
- create second Oteryn E2E/scenario authority;
- create authentication/session authority;
- mutate server-authoritative state through hidden client hooks;
- expose unauthenticated production control.

Oteryn retains `protocol-oteryn`; client sends intent; server remains authoritative.

## 27. Differential E2E

Default comparison classes:

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

Mismatch requires both sides to observe/support the field at the same normalized checkpoint, neither UNKNOWN, and candidate violation of the selected rule.

Missing official observation is a coverage gap, not an Oteryn failure.

## 28. Implementation phases

The original UI-before-core phase order is superseded.

### P0 — contracts/falsification baseline

- architecture;
- execution contract;
- adapter contract;
- implementation prompt;
- independent audit prompt.

### P1 — Package A control-core

`runtime_access:none`, no network listener.

Deliver:

- typed models;
- backend epoch/control generation;
- scenario parser/validator;
- predicates/step IDs;
- MutationCoordinator/dispatch gate;
- idempotency ledger;
- side-effect ledger;
- deterministic write-ahead dispatch durability model;
- STOP/reset;
- Recorder primitives/multi-clock model;
- privacy constructors;
- artifact staging/finalization;
- deterministic fake adapter/manual clock;
- race/restart/privacy tests.

### P2 — Package B loopback API + browser + CLI

Consume merged Package A. Use a persistent store implementing durable dispatch-commit semantics for mutation-capable fake requests. No official mutation.

### P3 — Package C Surveyor/read-only integration

Only after accepted exact Surveyor schema/interface.

### P4 — Package D official Track A mutation adapter

Separate runtime-sensitive task. Acquire external Track A guard without holding local dispatch gate; while guard remains held, run final Track A checks, local durable `commit_dispatch()`, then physical effect once.

### P5 — runtime capture-producer expansion

Add network metadata, targeted traces and screenshot producers. Recorder core already exists from P1.

### P6 — research suites

Add families only as capability evidence exists.

### P7 — Package E Oteryn adapter

Separate Oteryn-v2 task/PR aligned with ADR-0007.

### P8 — differential E2E

Run same semantic scenarios and emit versioned mismatch/coverage reports.

## 29. Package A readiness gate

Package A may start only when fresh independent audit answers YES:

> Can a competent implementation agent implement Package A solely from repository documentation without inventing concurrency, dispatch, STOP, idempotency, durability, budget, privacy, event-ordering, artifact or restart semantics?

## 30. First useful operator release

Expected after Packages A-C:

```text
Browser GUI                          YES
CLI                                  YES
Loopback versioned Control API       YES
Read-only runtime status             YES
Capability/evidence/freshness views  YES
Live normalized event stream         YES
Scenario catalogue/browser           YES
Fake one-step experiments             YES
STOP / idempotency / restart safety   YES
Artifact/run browser                  YES
agent_bundle.json                     YES
real official-client mutation         NO until Package D separately admitted
Oteryn adapter                        NO until separate Oteryn task
```

## 31. Non-goals

Control Center must not:

- replace Track A admission/lease/registration/supervisor;
- infer authority from visible process/window;
- persist credentials/secret-bearing auth/session data;
- expose unauthenticated remote control by default;
- turn UI toggles into authority;
- create raw automation bypass around Scenario Engine/Recorder;
- implement second Tibia protocol stack for harness;
- claim byte-level official-vs-Oteryn parity;
- claim causal proof from timestamp correlation;
- make historical `oteryn-client/**` canonical;
- create second Oteryn E2E platform.

## 32. Implementation language guidance

Python remains preferred initial orchestration language on official Track A side because current Surveyor/runtime tooling is Python and reuse minimizes duplication.

Web UI should remain thin HTML/CSS/JavaScript unless current repository evidence justifies another existing stack.

This is guidance only; dependencies remain governed by current repository policy.

## 33. Required package split

```text
Package A  control-core + Recorder primitives + fake adapter + deterministic durability/race tests
Package B  loopback Control API + browser + CLI + persistent run/action store
Package C  accepted Surveyor/read-only integration
Package D  separately admitted official Track A mutation adapter
Package E  separately governed Oteryn-v2 adapter
```

Shared public contracts have one producer at a time. Later workers consume merged contracts instead of redefining them.