# TIBIA RE Control Center / E2E Lab

```yaml
programme: TIBIA-RE-CONTROL-CENTER-E2E
repository: blakinio/otclient
track: official-client-re
status: design_baseline
version: 1.0
runtime_access_of_this_document: none
future_official_client_runtime: Track A canonical live runtime only
future_oteryn_runtime: separate adapter task in blakinio/Oteryn-v2
```

## 1. Purpose

Build one reusable research and E2E platform that can:

1. observe the official Tibia Linux client under the existing Track A governance model;
2. execute bounded, explicitly declared research actions when current mutation authority exists;
3. correlate actions with runtime state, network metadata, targeted traces and screenshots;
4. produce compact machine-readable evidence bundles for later agents;
5. later run the same semantic scenarios against the Oteryn v2 Rust client through a separate adapter;
6. compare official-client and Oteryn outcomes at the semantic state-transition level.

The platform is a research/test harness. It is not the game client, does not become a protocol authority, and does not grant itself runtime, login, credential or mutation permissions.

## 2. Existing systems to reuse

Do not create replacements for these systems:

- `docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md` — normative experiment/evidence methodology;
- Track A canonical lease, registration, Gate A/Gate B, target-uniqueness and whole-lifetime supervision contracts;
- `tools/tibia_runtime_bridge/**` — runtime identity/bridge work where its current contract applies;
- open Draft PR #592 `tools/tibia_re_surveyor/**` — evidence/coverage/runtime-snapshot Surveyor, if and when it is merged or otherwise explicitly consumed from an accepted exact head;
- shared GUI-input lock and heartbeat contracts already defined by Track A.

PR #592 is currently an open Draft and is not treated as merged capability by this design.

## 3. Product shape

The project has one backend and two operator surfaces.

```text
                 TIBIA RE CONTROL CENTER
                          |
            +-------------+-------------+
            |                           |
        Browser UI                    CLI
            |                           |
            +-------------+-------------+
                          |
                     Control API
                          |
          +---------------+----------------+
          |               |                |
     Scenario Engine   Recorder       Safety Controller
          |               |                |
          +---------------+----------------+
                          |
                     Adapter API
                 +--------+--------+
                 |                 |
         Official Tibia         Oteryn v2
            Adapter              Adapter
                 |                 |
          Track A runtime      Rust client
```

The GUI and CLI never talk directly to the official client. Every operation flows through the Scenario Engine and Safety Controller.

## 4. Deployment modes

### 4.1 Direct-machine mode

Run the backend on the machine hosting the Track A environment. The operator may use:

- CLI for deterministic scripted runs;
- the browser UI opened locally on the same desktop/KasmVNC session.

The initial implementation should prefer loopback-only Control API binding. A LAN/public bind is a separate security-sensitive task and must not be enabled by convenience defaults.

### 4.2 Browser mode

The same web UI is served by the Control Center backend. For the first Track A implementation, remote visual access may use the existing KasmVNC desktop rather than exposing a new network service.

If a later task exposes the Control API beyond loopback, it must define authentication, TLS/transport, origin policy, bind-address policy, rate/bounds and shutdown behavior before deployment.

## 5. UI information architecture

The approved visual direction is a dense desktop research console optimized for high information density rather than a consumer dashboard.

### 5.1 Always-visible top status bar

```text
TIBIA RE CONTROL CENTER
RUNTIME | CLIENT | RECORDER | AUTHORITY | SESSION       STOP ALL | PAUSE
```

Required states:

- `RUNTIME`: OFFLINE / DEGRADED / ONLINE;
- `CLIENT`: NOT_FOUND / LOGIN_SCREEN / CHARACTER_SELECTION / IN_GAME / UNKNOWN;
- `RECORDER`: STOPPED / RECORDING / ERROR;
- `AUTHORITY`: READ_ONLY / MUTATION_ALLOWED / EXPIRED / UNKNOWN;
- `SESSION`: elapsed research-session time and session epoch.

`AUTHORITY` must be visually prominent. A stale or unknown authority state disables every mutating control.

`STOP ALL` is always visible. It cancels queued/in-flight harness actions and capture tasks. It must not kill the official client unless separate current process-control authority explicitly permits that effect.

### 5.2 Main tabs

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

Tabs may be hidden only when their capability is structurally unavailable; unavailable research support should normally remain visible as `UNSUPPORTED`, `NOT_PROVEN` or `READ_ONLY`, not silently disappear.

### 5.3 Main screen layout

Left column:

- Quick Activator: Recorder, Runtime Trace, Network Capture, State Capture, Screenshots;
- research suite toggles: Movement, Healing, Combat, Inventory, Containers, Equipment, Chat;
- Profile/Target;
- Session Info.

Center top:

- Character State: HP, MP, soul, capacity, stamina, level, speed, position and only other values with a declared source/confidence;
- Conditions;
- Current Actions;
- Target Info.

Center middle:

- Quick Actions row. Every button creates a one-step experiment; there are no unrecorded manual mutation shortcuts.

Initial visible actions:

```text
Move N/E/S/W
Turn N/E/S/W
Cast selected healing spell
Cast selected offensive spell
Use selected potion
Eat selected food
Open selected container
Say controlled test text
Attack selected target
Follow selected target
Look at selected object
```

Center bottom:

- Engine Benchmark;
- Live Events with filters;
- Active Scenario with step list, status, duration and progress;
- actions: Pause Scenario / Abort Scenario.

Right column:

- Mini Map observation panel;
- Backpack/container observation panel;
- Battle List/target observation panel;
- Shortcuts/Hotkeys configured as research actions rather than raw keyboard macros.

### 5.4 Read-only behavior

When authority is `READ_ONLY`, `EXPIRED` or `UNKNOWN`:

- observation/capture controls remain available only if current read authority permits them;
- all action buttons are disabled;
- scenario runs containing mutations are rejected before dispatch;
- the UI shows the exact failing gate/category;
- no UI state may imply that checking a box created authority.

## 6. Core components

### 6.1 Control API

Responsibilities:

- expose current normalized status;
- start/stop/pause/resume scenario runs;
- submit one-step experiments;
- stream normalized events;
- enumerate capabilities/scenarios/runs;
- request safe artifact export;
- expose emergency-stop state.

The API is transport-neutral at the domain layer. The browser transport is an implementation detail.

### 6.2 Scenario Engine

Responsibilities:

- validate schema;
- evaluate preconditions;
- resolve adapter capabilities;
- acquire/validate required authority through Safety Controller;
- enforce side-effect budgets and action counts;
- execute one action at a time;
- capture before/after snapshots;
- wait for bounded conditions;
- evaluate assertions;
- apply abort conditions;
- emit deterministic run/step results.

A GUI button such as `Exura` is represented as a single-step scenario, not a separate execution path.

### 6.3 Safety Controller

Responsibilities:

- treat Track A admission as external authority, never as a UI preference;
- validate current authority immediately before every mutating step;
- preserve lease/generation/registration/target-identity fences required by the current Track A contracts;
- use the shared GUI input lock where input is involved;
- stop mutation on generation change, target identity change, unknown state or authority expiry;
- enforce scenario effect budgets;
- implement emergency cancellation and deterministic cleanup.

No scenario configuration may weaken a Track A gate.

### 6.4 Recorder

Normalized event classes:

```text
SYSTEM
AUTHORITY
ACTION
TRACE
NET
STATE
SCREEN
SNAPSHOT
ASSERTION
RESULT
ERROR
```

All events share:

- research session epoch;
- monotonic timestamp;
- sequence number;
- run ID;
- experiment/step ID when applicable;
- source adapter;
- sensitivity classification.

The recorder must preserve the causal-recorder requirements of `OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md`.

### 6.5 Artifact Store

Canonical per-run logical layout:

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

Large/raw artifacts remain outside Git unless existing evidence policy explicitly permits them. Git evidence contains normalized results, hashes, exact provenance and minimum necessary excerpts.

### 6.6 Comparator

The comparator operates on semantic snapshots and normalized transitions rather than raw protocol byte equality.

Examples:

```text
movement position delta       EXACT
HP/mana transition            EXACT or declared tolerance
condition transition          EXACT
container contents            semantic set/order policy
cooldown timing               bounded tolerance
visual effect                 structural/semantic observation
protocol bytes                NOT a cross-client parity requirement
```

This is required because Oteryn v2 owns `protocol-oteryn` and is not expected to reproduce third-party wire bytes.

## 7. Scenario model

Every scenario declares at minimum:

```yaml
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

Example:

```yaml
id: healing-basic-001
name: Basic healing experiment
adapter_requirements:
  actions: [cast_spell, use_consumable]
preconditions:
  client_state: IN_GAME
  hp_percent_below: 90
side_effect_budget:
  max_runtime_seconds: 60
  max_actions: 10
  max_spells: 3
  max_consumables: 2
  max_gold: 0
  max_tibia_coins: 0
capture_policy:
  state: true
  events: true
  screenshots: before_after
  network: metadata
  traces: targeted
steps:
  - snapshot: before
  - action:
      kind: cast_spell
      spell: exura
  - wait:
      condition: hp_changed
      timeout_ms: 3000
  - snapshot: after_spell
abort_conditions:
  - authority_lost
  - target_identity_changed
  - client_not_in_game
  - timeout
expected_result:
  hp_delta: positive
privacy_policy:
  secret_material: reject
```

A scenario may intentionally be read-only. Mutation is not implied by the presence of an action name in the catalogue.

## 8. Atomic action catalogue

The common semantic catalogue should start with:

```text
SYSTEM
wait
checkpoint

SESSION
login_request         capability only; credentials handled outside scenario payload
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

Actions are semantic intents. Adapters decide how they map to their client without leaking implementation-specific call addresses, UI coordinates or protocol bytes into scenario files.

## 9. Capture and privacy policy

Default capture policy is minimum necessary:

- state: normalized semantic fields;
- network: direction/type/size/sequence/correlation metadata by default;
- trace: only declared targets;
- screenshots: bounded checkpoints;
- message text: redact or omit unless deliberately generated test text is required;
- identities: anonymize/hash when identity is not the hypothesis;
- credentials/session/auth secrets: never persist.

Login/auth capture is structural only. Email, password, 2FA, cookies, tickets, session tokens, secret-bearing memory and secret-bearing packet material must not enter run artifacts.

## 10. Official Tibia adapter

The official-client adapter is a Track A consumer. It may provide:

```text
runtime_status
snapshot
capabilities
execute semantic action
wait_for condition
authority_status
start/stop capture
emergency_stop
```

Implementation may combine approved mechanisms such as runtime bridge, normal GUI input, semantic bridge methods or targeted instrumentation, but each mechanism remains subject to its own current evidence gate and Track A authorization.

The adapter must report capability maturity separately for observation and action. A static or read capability does not imply mutation support.

## 11. Oteryn v2 adapter boundary

The canonical Rust client is in `blakinio/Oteryn-v2`, not the historical `otclient/oteryn-client` subtree.

A future separate Oteryn-v2 task should implement the same semantic adapter contract through test-owned interfaces in that repository. It must not add Tibia protocol compatibility merely to satisfy this harness.

Expected integration model:

```text
blakinio/otclient
  Control Center / scenario definitions / official reference evidence
          |
          | semantic E2E adapter contract
          v
blakinio/Oteryn-v2
  apps/client + test-control adapter
```

Cross-repository changes require separate tasks/branches/PRs and a shared coordination ID under each repository's current governance.

## 12. Engine benchmark

The Main UI records per-run timings when available:

```text
state read
screen capture
network correlation
runtime trace
adapter dispatch
state confirmation
total step latency
```

These values are diagnostics, not correctness proof. No fixed performance claim may be made without a named runtime and evidence.

## 13. MVP phases

### P0 — Surveyor foundation

Consume #592 only after its exact accepted state is known. Do not copy its implementation.

### P1 — Read-only Control Center

Deliver:

- backend process;
- loopback Control API;
- browser UI matching the dense approved layout;
- CLI status/session/run inspection;
- live normalized event stream;
- read-only runtime/survey data;
- artifact browser/export;
- no mutating action dispatch.

### P2 — Scenario Engine and one-step experiments

Deliver:

- scenario schema/validator;
- preconditions/assertions/timeouts/budgets;
- Manual Quick Action -> one-step experiment mapping;
- cancellation/STOP ALL;
- fake adapter and deterministic tests;
- still no real official-client mutation until P3 authority integration is proven.

### P3 — Official-client bounded actions

Integrate current Track A authority and begin with the smallest proven action set such as turn/move or another already-supported semantic action. Every action requires reference-path parity and the applicable action evidence gate.

### P4 — Recorder expansion

Add bounded network correlation, targeted traces, state/screenshot checkpoints and compact agent bundles.

### P5 — Research suites

Add suites only as capability evidence exists:

- movement;
- healing/spells/consumables;
- inventory/containers;
- combat/targeting;
- chat;
- equipment/conditions.

### P6 — Oteryn v2 adapter

Separate repository task/PR in `blakinio/Oteryn-v2`; no implementation in the frozen historical Rust subtree here.

### P7 — Differential E2E

Run the same semantic scenario against official reference and Oteryn, compare normalized outcomes, and produce machine-readable mismatch reports usable by Oteryn CI/release gates where that repository explicitly adopts them.

## 14. MVP acceptance target

The first useful operator release should support:

```text
Browser GUI                          YES
CLI                                  YES
Read-only runtime status             YES
Live normalized event stream         YES
Scenario catalogue/browser           YES
One-step experiment model            YES
STOP ALL / bounded cancellation       YES
Artifact/run browser                  YES
agent_bundle.json                     YES
real official-client mutation         NO until P3 gates are separately proven
Oteryn adapter                        NO until P6 separate repo task
```

## 15. Non-goals

The Control Center must not:

- replace Track A admission/lease/registration mechanisms;
- infer authority from a visible process/window;
- persist credentials or secret-bearing auth/session data;
- expose an unauthenticated remote-control service by default;
- turn UI toggles into permission grants;
- implement a second Tibia game protocol stack as part of the harness;
- make the historical `oteryn-client/**` subtree canonical again;
- claim official-vs-Oteryn byte-level protocol parity;
- automatically promote RE coverage from correlation alone.

## 16. Implementation language guidance

For the official Track A side, Python is the preferred initial orchestration language because the Surveyor/runtime tooling is already Python and this minimizes bridge duplication. The web UI should remain a thin browser client using ordinary HTML/CSS/JavaScript unless repository inspection proves an existing approved frontend stack should be reused.

This is guidance, not permission to add dependencies. The implementation task must inspect current dependency/test policy and justify every new runtime dependency.

## 17. Required first implementation split

Do not implement P1-P7 in one PR. The recommended first implementation package is:

```text
Task A: control-core contracts + fake adapter + deterministic tests
Task B: read-only HTTP/UI/CLI consuming Task A
Task C: Surveyor integration after #592 accepted state is known
Task D: Track A mutation adapter only after a current runtime/action admission task exists
Task E: Oteryn-v2 adapter as a separate cross-repository task
```

Shared public contracts have one producer at a time. Later workers consume the merged producer rather than redefining it.
