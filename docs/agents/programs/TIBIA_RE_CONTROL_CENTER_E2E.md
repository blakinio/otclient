# TIBIA RE Control Center / E2E Lab

```yaml
programme: TIBIA-RE-CONTROL-CENTER-E2E
repository: blakinio/otclient
track: official-client-re
status: hardened_design_baseline
version: 1.1
runtime_access_of_this_document: none
future_official_client_runtime: Track A canonical live runtime only
future_oteryn_runtime: separate adapter task in blakinio/Oteryn-v2
```

## 1. Purpose

Build one reusable research and E2E platform that can:

1. observe the official Tibia Linux client under existing Track A governance;
2. execute bounded semantic research actions only when current external mutation authority exists at the final dispatch boundary;
3. correlate controlled stimuli with runtime state, network metadata, targeted traces and screenshots without confusing temporal ordering with causality;
4. produce deterministic, privacy-safe, machine-readable per-run evidence bundles;
5. expose the same domain semantics to browser and direct-machine CLI operation;
6. later run the same semantic scenarios against the Oteryn v2 Rust client through a separately governed adapter;
7. compare official-client and Oteryn outcomes at normalized semantic state-transition checkpoints.

The Control Center is a research/test harness. It is not the game client, not a protocol authority, not a Track A lease/registration authority and not an Oteryn server authority.

Normative separation:

```text
scenario validity
!= capability support
!= evidence maturity
!= observation freshness
!= mutation authority
```

No local configuration, UI state, CLI option, cached status or prior preflight can create mutation authority.

## 2. Normative document stack

The implementation must read these as one design package:

1. `docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md` — causal RE/evidence methodology;
2. `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md` — normative concurrency, dispatch, STOP ALL, idempotency, budget, recorder, privacy and recovery semantics;
3. `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md` — semantic adapter data/API boundary;
4. this programme — product architecture and phasing;
5. `docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_MVP.md` — bounded implementation procedure.

When a future official-client implementation interacts with Track A, the current trusted-base Track A admission/lease/registration/Gate A/rebind/Gate B/target-identity/GUI-lock/whole-lifetime-supervisor contracts take precedence over any stale example in this programme.

## 3. Existing systems to reuse

Do not create replacements for:

- Track A canonical lease manager;
- authoritative runtime registration;
- Gate A, generation rebind and Gate B;
- canonical target-uniqueness proof;
- cancellation-safe whole-lifetime mutation supervisor/guard;
- shared GUI input lock/guard;
- shared activity heartbeat where applicable;
- `tools/tibia_runtime_bridge/**` for current runtime identity/bridge behavior where its contract applies;
- Track A evidence/capability registries;
- Surveyor #592 outputs/interfaces after an exact accepted producer state exists;
- Oteryn v2's accepted native E2E architecture, currently owned by `docs/architecture/ADR-0007-native-end-to-end-test-platform.md` in `blakinio/Oteryn-v2`.

Control Center may normalize and reference those systems. It must not become their second source of truth.

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

### 4.1 Hard architectural invariants

- Browser and CLI never call adapters directly.
- Quick Actions are one-step scenarios, not a second mutation path.
- The Scenario Engine never stores standing Track A mutation authority.
- The `MutationCoordinator` owns local serialization/idempotency/cancellation generations only; it does not own Track A authority.
- The Safety Controller is a consumer/facade over external authority and safety checks, not a new lease manager.
- The Recorder observes and preserves evidence but cannot grant capability or authority.
- The Artifact Store owns per-run evidence only; it does not promote Track A capability/evidence registries.
- The Comparator compares normalized semantics only.

## 5. Mutation dispatch architecture

Every adapter instance has one local `MutationCoordinator` as defined by `TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md`.

Mutation is admitted only through one final logical operation:

```text
atomic_dispatch(action, dispatch_fence, cancellation_token)
```

Immediately before crossing the irreversible adapter boundary it must revalidate:

- action idempotency ledger;
- current Control Center cancellation/control generation;
- runtime/session/adapter fences;
- side-effect budget reservation;
- capability support;
- current external authority;
- required input lock;
- all official-client Track A fences for `OFFICIAL_TIBIA`.

An earlier scenario check or adapter `preflight()` may reject work early but can never authorize final dispatch.

The official adapter must reuse the current Track A whole-lifetime guarded mutation boundary so authority validation and irreversible dispatch cannot be separated by an unguarded TOCTOU window.

## 6. STOP ALL and cancellation model

`STOP ALL` is a safety state transition, not a best-effort UI command.

Its linearization point is the increment/latch of the Control Center `control_generation` under the same local coordinator synchronization domain used to admit dispatch.

Required result:

```text
STOP linearizes before dispatch -> mutation does not start
Dispatch linearizes before STOP -> action is already-dispatched and handled conservatively
```

There is no valid state in which STOP linearizes first and a stale-generation mutation then begins.

`STOP ALL`:

- rejects new mutations;
- cancels queued old-generation work;
- signals cooperative cancellation to waits/captures/in-flight adapters;
- prevents not-yet-dispatched work from crossing the irreversible boundary;
- rejects stale completions as control input;
- emits terminal evidence;
- cleans only harness-owned resources;
- never kills the official client without separate current process-control authority.

STOP remains latched until explicit local reset and fresh status/authority revalidation.

## 7. Concurrency model

Default policy is conservative:

- one mutation-capable action per adapter at a time;
- no two operator surfaces can create parallel mutation implementations;
- concurrent read-only runs are permitted only where every involved source is proven concurrency-safe;
- unknown concurrency safety means serialize;
- scenarios never own permanent adapter authority;
- adapter restart/generation change invalidates pending mutation work.

## 8. Deployment modes

### 8.1 Direct-machine mode

The backend runs on the machine hosting the applicable test/runtime environment. CLI and local browser use the same backend/domain service.

### 8.2 Browser mode

The backend serves the same Control API plus thin web UI.

Initial API exposure is loopback-only. KasmVNC may provide remote visual access to the desktop without exposing a new Control API network surface.

A future non-loopback deployment requires a separate accepted security design covering authentication, authorization, TLS/transport, origins, Host policy, CSRF/replay concerns, bind policy, rate/bounds and shutdown. Remote exposure must not be enabled by a convenience `0.0.0.0` flag alone.

## 9. Control API

The domain API is versioned and transport-neutral. Package B should expose `/v1` or an equivalent explicit version.

Responsibilities:

- status and freshness;
- capabilities and evidence maturity;
- scenarios and validation;
- run lifecycle;
- one-step experiments;
- STOP/reset/pause/resume/abort;
- bounded event streaming/polling;
- run/artifact inspection and safe export.

Required properties:

- bounded request bodies and collections;
- bounded run/event history and subscribers;
- explicit idempotency key for mutation-capable requests;
- duplicate POST/result-replay semantics from the execution contract;
- deterministic malformed-input errors;
- no raw action/debug bypass endpoint;
- explicit shutdown behavior.

## 10. Scenario Engine

The engine owns deterministic scenario semantics, not external authority.

Responsibilities:

- parse/version/validate scenarios;
- assign deterministic stable step IDs;
- resolve required semantic capabilities;
- evaluate typed predicates/preconditions;
- reserve/check budgets;
- schedule one action through the coordinator;
- capture before/after checkpoints;
- perform bounded waits;
- evaluate assertions;
- enforce abort conditions;
- propagate failures deterministically;
- implement explicit pause/resume semantics;
- emit reproducible run/step states.

Unknown values never silently satisfy mutation-safety predicates.

Mutation retries default to zero. An action with possible external side effect that becomes `AMBIGUOUS` is never automatically retried.

## 11. Scenario model

Every scenario declares at minimum:

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

Typed predicate baseline:

```yaml
field: player.hp
op: LT
value: 100
unknown_policy: FAIL
```

Allowed operators and UNKNOWN behavior are normative in the execution contract.

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
  - field: player.hp_percent
    op: LT
    value: 90
    unknown_policy: FAIL
side_effect_budget:
  max_runtime_seconds: 60
  max_actions: 3
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
expected_result:
  - field: player.hp
    op: GT
    value_from_snapshot: before.player.hp
privacy_policy:
  secret_material: reject
```

## 12. Atomic semantic action catalogue

Scenario files express intent, never implementation details.

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

Adapters may implement these via GUI input, semantic bridge calls or other separately approved mechanisms, but coordinates, keycodes, QMeta IDs, function addresses, vtables, opcodes and wire layouts do not leak into common scenarios.

## 13. Side-effect budgets

Budgets are hard admission constraints, not decorative metadata.

Each run maintains a monotonic ledger per dimension:

```text
limit
reserved
committed
uncertain
```

Before dispatch the engine reserves the maximum plausible effect. After dispatch it releases, commits or moves the conservative maximum to `uncertain` according to the proven outcome.

A timeout/failure/cancellation after possible dispatch is treated as consumed/uncertain for future admission.

If a hard budget cannot be safely bounded or measured for an action, that scenario/action is refused.

Minimum dimensions:

- runtime;
- action attempts;
- movement tiles;
- spells;
- consumables;
- moved items/stack amount at risk;
- gold;
- Tibia Coins;
- irreversible changes.

TC and irreversible-change budgets default to zero for research scenarios unless separately and explicitly authorized.

## 14. Action lifecycle and restart behavior

The Control Center distinguishes at least:

```text
CREATED
VALIDATED
RESERVED
DISPATCHING
DISPATCHED
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

Backend restart never auto-resumes mutation.

If the backend cannot prove whether an action crossed the irreversible boundary, recovery classifies it `AMBIGUOUS` unless authoritative reconciliation proves the exact outcome. `AMBIGUOUS` is not retried automatically.

## 15. Recorder and causal evidence

The unified `events.jsonl` order is recorder ingestion order, not proof that independent sources share one clock.

Every event preserves:

- ingest sequence;
- ingestion monotonic timestamp;
- source timestamp when available;
- source clock domain;
- source-local sequence and scope when available;
- ordering confidence;
- run/experiment/step identity;
- runtime/session fences;
- sensitivity classification.

For causal Track A work it additionally preserves the fields required by `OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md`, including stimulus ID, direction, lane/message sequence/type, observable thread/handler/object identity, before/after state hashes, semantic delta and evidence reference.

Negative/no-stimulus controls remain mandatory where causal promotion requires them.

Correlation is not automatically causal proof.

## 16. Late events and finalization

Run state:

```text
ACTIVE -> CLOSING -> FINALIZED
```

After execution ends, a bounded drain records late source events and watermarks where available. Late events may enrich evidence but cannot rewrite a terminal action result or restart execution.

After finalization, later accepted evidence is append-only supplemental evidence referencing the original run; historical results are not silently rewritten.

## 17. Artifact Store

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

- stage then finalize atomically where supported;
- incomplete/crashed runs remain explicitly incomplete;
- `result.json`/manifest PASS is written only after ledgers/events are flushed;
- artifacts include schema versions, scenario hash, adapter identity/version, generation/fence summary, budget/action ledger summary and artifact hashes;
- large/raw evidence stays outside Git unless current policy explicitly permits it;
- Control Center does not overwrite Surveyor/Track A capability registries.

## 18. Privacy and secret exclusion

Mandatory invariant:

> Secret-class data never enters the normal Event, Artifact, Error, Report or AgentBundle object graph.

Redaction/classification happens before ordinary object creation. Export-time redaction is defense in depth only.

Never persist:

- email/password/2FA;
- auth/session tokens;
- cookies/tickets;
- encryption/RSA secret material;
- secret-bearing memory or packet payloads;
- environment-variable values;
- unnecessary private chat/personal data.

Arbitrary exception/debug/repr text is untrusted. Persistent errors use stable reason codes, reviewed static text and explicitly classified safe fields.

Screenshots are accepted only when capture context is known non-secret or after an explicit quarantine/sanitization path. Login/auth screens are not normal run artifacts.

## 19. Network capture

Default persistent network capture is metadata-only:

```text
direction
connection/session lane
source-local sequence when available
message type only when structurally known
size
correlation ID
payload_capture=NONE
```

There is no raw-payload fallback.

A future sanitized payload mode requires a separate approved policy proving that secret-class bytes are excluded before persistence.

## 20. UI information architecture

The UI is a dense desktop research console.

Always-visible status:

```text
RUNTIME | CLIENT | RECORDER | AUTHORITY | CAPABILITY | EVIDENCE | FRESHNESS | SESSION
STOP ALL | PAUSE
```

`AUTHORITY`, `CAPABILITY`, `EVIDENCE` and `FRESHNESS` are separate concepts and must not be collapsed into one green/red badge.

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

Unknown/unproven state renders as `UNKNOWN`, `UNSUPPORTED`, `NOT_PROVEN`, `STALE` or another truthful explicit state. Never render fabricated sample gameplay data as live state.

Quick Actions always create one-step experiments:

```text
snapshot before
-> semantic action
-> bounded wait/assertion
-> snapshot after
-> result
```

There are no unrecorded manual mutation shortcuts.

## 21. Official Tibia adapter

The official adapter is an `EXTEND_EXISTING` Track A consumer.

It may combine approved mechanisms from:

- `tools/tibia_runtime_bridge/**`;
- normal GUI input under the shared input lock;
- stable semantic bridge methods;
- bounded targeted instrumentation.

Each mechanism remains subject to its current proof/action maturity and current Track A authorization.

Official adapter capability reporting has two layers:

1. generic semantic `read_supported` / `action_supported`;
2. official-only RE maturity extension `R0-R4` / `A0-A4` plus evidence refs.

Read support never implies action support.

## 22. Surveyor boundary

Surveyor is integrated only after an exact accepted producer state exists.

Package C pins:

```text
surveyor_schema_version
producer_commit
producer_interface
```

Schema mismatch degrades Surveyor-dependent panels to explicit `INCOMPATIBLE/UNAVAILABLE`; it does not trigger copied internal logic or fabricated data.

## 23. Oteryn v2 adapter boundary

Canonical Oteryn code is in `blakinio/Oteryn-v2`.

A future Oteryn adapter is implemented through a separate Oteryn task/branch/PR and must integrate with that repository's accepted native E2E architecture (`ADR-0007`) or a deliberately versioned cross-repository semantic boundary.

It must not:

- add Tibia wire compatibility to satisfy this harness;
- create a second Oteryn E2E scenario authority;
- create authentication/session authority;
- mutate server-authoritative state through hidden client hooks;
- expose unauthenticated production control.

Oteryn retains `protocol-oteryn`; client sends intent; server remains authoritative.

## 24. Differential E2E

Comparison profiles are explicit and versioned.

Default classifications:

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

A mismatch exists only if both sides support/observe the same normalized field at the same semantic checkpoint, neither value is UNKNOWN and the candidate violates the selected equivalence/tolerance rule.

Missing official observation is a coverage gap, not proof of Oteryn failure.

## 25. Implementation phases

The previous P1-before-P2 UI ordering is superseded. Core semantics and recorder primitives precede operator UI and all real actions.

### P0 — Contracts and falsification baseline

- hardened architecture;
- execution safety contract;
- semantic adapter contract;
- implementation prompt;
- independent audit prompt.

### P1 — Package A control-core

No network listener and `runtime_access: none`.

Deliver:

- typed models;
- scenario parser/validator;
- deterministic predicates/step IDs;
- run/action lifecycle;
- MutationCoordinator;
- cancellation generation/STOP semantics;
- idempotency ledger;
- budget ledger;
- Recorder primitives and multi-clock event model;
- privacy constructors;
- artifact staging/finalization model;
- deterministic fake adapter/manual clock;
- complete race/restart/privacy tests.

### P2 — Package B loopback Control API + browser + CLI

Consume merged Package A. Browser and CLI are thin clients over one backend. No official-client mutation.

### P3 — Package C Surveyor/read-only integration

Only after an accepted exact Surveyor schema/interface exists. Add read-only Track A/survey views and evidence references.

### P4 — Package D official Track A mutation adapter

Separate runtime-sensitive task. Integrate only the smallest already-proven action surface through current Track A authority/guard infrastructure.

### P5 — Recorder/capture expansion

Add bounded network metadata, targeted traces and screenshot checkpoints for real actions. Recorder core already exists from P1; this phase adds runtime-specific producers, not the first recorder semantics.

### P6 — Research suites

Add feature families only as read/action evidence exists.

### P7 — Package E Oteryn v2 adapter

Separate Oteryn-v2 repository task/PR aligned with ADR-0007.

### P8 — Differential E2E

Run the same semantic scenarios against official reference and Oteryn and emit versioned mismatch/coverage reports.

## 26. Package A implementation-readiness gate

Package A may start only when a fresh independent audit can answer YES to:

> Can a competent implementation agent implement Package A solely from repository documentation without inventing concurrency, authority, cancellation, retry, budget, privacy, event-ordering, artifact or recovery semantics?

Minimum required falsification coverage is normative in `TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md` and the independent-audit prompt.

## 27. First useful operator release

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
STOP ALL / bounded cancellation       YES
Artifact/run browser                  YES
agent_bundle.json                     YES
real official-client mutation         NO until Package D separately admitted
Oteryn adapter                        NO until separate Oteryn task
```

## 28. Non-goals

Control Center must not:

- replace Track A admission/lease/registration/supervisor systems;
- infer authority from a visible process/window;
- persist credentials or secret-bearing auth/session data;
- expose unauthenticated remote control by default;
- turn UI toggles into authority;
- create a raw gameplay automation bypass around Scenario Engine/Recorder;
- implement a second Tibia protocol stack for the harness;
- claim byte-level official-vs-Oteryn parity;
- claim causal RE proof from timestamp correlation alone;
- make historical `oteryn-client/**` canonical;
- create a second Oteryn E2E platform.

## 29. Implementation language guidance

Python remains the preferred first orchestration language on the official Track A side because current Surveyor/runtime tooling is Python and reuse minimizes bridge duplication.

The web UI should remain thin HTML/CSS/JavaScript unless current repository evidence justifies another existing stack.

This is guidance only. Every dependency remains subject to current repository dependency/test policy.

## 30. Required package split

Do not collapse the programme into one PR.

```text
Package A  control-core + Recorder primitives + fake adapter + deterministic tests
Package B  loopback Control API + browser + CLI
Package C  accepted Surveyor/read-only integration
Package D  separately admitted official Track A mutation adapter
Package E  separately governed Oteryn-v2 adapter
```

Shared public contracts have one producer at a time. Later workers consume merged contracts rather than redefining them.