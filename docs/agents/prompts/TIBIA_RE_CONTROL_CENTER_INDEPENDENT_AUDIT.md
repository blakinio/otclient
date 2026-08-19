# TIBIA-RE-CONTROL-CENTER-INDEPENDENT-AUDIT

Recommended reasoning effort: high / maximum.

Act as a **fresh independent read-only architecture, security and implementation-readiness auditor**.

Repository:

`https://github.com/blakinio/otclient`

Use the connected GitHub repository state as the source of truth.

Do **not** implement fixes during this task.

Do not modify files.  
Do not commit.  
Do not push.  
Do not merge.  
Do not create replacement architecture.  
Do not perform Track A runtime actions.  
Do not launch or control the Tibia client.  
Do not access credentials.  
Do not log in.  
Do not perform gameplay actions.  
Do not write to `blakinio/Oteryn-v2`.

## Audit target

Audit the complete design of:

`TIBIA RE Control Center / E2E Lab`

The design was introduced by PR:

`blakinio/otclient#600`

Known merge at the time this prompt was prepared:

`ada65af85a872e2df43469f5687418fc5647811a`

Lifecycle closeout:

`blakinio/otclient#601`

Known closeout merge:

`5817f1ad699c2d68dfb1a03886dc8c20dace67e7`

These values are **discovery hints only**.

Before relying on them:

1. fetch current `main`;
2. verify that #600 and #601 are actually merged;
3. verify their exact merge commits;
4. verify the current blobs of all audited files;
5. inspect current open PRs and active tasks for newer overlapping work;
6. if current repository evidence supersedes any value above, use the live repository state and explicitly report the discrepancy.

## Mandatory files

Read in full:

- `AGENTS.md`
- `docs/agents/README.md`
- `docs/agents/programs/TIBIA_RE_CONTROL_CENTER_E2E.md`
- `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md`
- `docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_MVP.md`
- `docs/agents/tasks/archive/OTC-20260819-tibia-re-control-center-e2e-design.md`

Also read the current relevant Track A governance and dependencies, including at minimum:

- `docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md`
- `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`
- `docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md`
- current canonical lease/registration/Gate A/Gate B/rebind/supervisor contracts referenced by repository instructions
- `docs/agents/MODULE_CATALOG.md`
- `docs/agents/REPOSITORY_MAP.md`
- `docs/agents/KNOWN_RISKS.md`
- `docs/agents/BUILD_TEST_MATRIX.md`
- `docs/agents/CROSS_REPO_CONTRACTS.md`

Inspect the current exact status and relevant content of:

- PR #592 `TIBIA-RE Surveyor`
- `tools/tibia_re_surveyor/**`, if now merged or otherwise present on current main
- `tools/tibia_runtime_bridge/**`
- existing Track A lease/input-lock/heartbeat/runtime-control helpers
- any existing scenario, recorder, E2E, HTTP, web UI, CLI or adapter infrastructure that could overlap with the proposed design

For the Oteryn side, inspect **read-only** current repository state in:

`https://github.com/blakinio/Oteryn-v2`

Read its current:

- `AGENTS.md`
- relevant architecture documents
- `apps/client`
- existing test-support/E2E/control interfaces
- security rules affecting a future test adapter

Do not assume historical `otclient/oteryn-client/**` is still canonical.

# PRIMARY OBJECTIVE

Determine whether the Control Center design is:

1. architecturally sound;
2. implementable without major redesign;
3. properly integrated with existing Track A infrastructure;
4. safely fail-closed;
5. suitable for both browser and direct-machine operation;
6. capable of becoming a reusable E2E platform;
7. suitable for later semantic differential testing against Oteryn v2;
8. sufficiently specified for another agent to begin Package A implementation.

Do not trust the conclusions of the agent that authored #600.

Independently falsify the design.

# AUDIT AREA A — REPOSITORY FIT AND DUPLICATION

Verify whether the design correctly reuses existing infrastructure rather than rebuilding it.

Check for duplication or conflict with:

- Surveyor;
- runtime bridge;
- canonical runtime lease manager;
- canonical registration;
- Gate A / rebind / Gate B;
- whole-lifetime supervisor;
- GUI input lock;
- activity heartbeat;
- evidence registries;
- existing client-test infrastructure;
- existing scenario/test helpers;
- existing HTTP/web/CLI infrastructure.

For every proposed component classify:

```text
REUSE_EXISTING
EXTEND_EXISTING
NEW_COMPONENT_JUSTIFIED
DUPLICATE_OR_CONFLICTING
UNKNOWN
```

Pay special attention to whether a new:

- Safety Controller,
- Recorder,
- Artifact Store,
- Scenario Engine,
- Adapter API

would accidentally become a second source of truth.

# AUDIT AREA B — AUTHORITY AND FAIL-CLOSED DESIGN

Attempt to find every way the proposed platform could accidentally execute an action without valid current Track A authority.

Audit:

- stale lease;
- expired lease;
- stale registration;
- mismatched lease generation;
- mismatched runtime generation;
- process restart;
- PID reuse;
- changed executable;
- changed boot ID;
- changed session epoch;
- different X11 window;
- different container;
- changed display;
- authority loss between scenario validation and dispatch;
- authority loss during a multi-step scenario;
- queued actions after authority loss;
- browser reconnect;
- duplicated HTTP request;
- repeated CLI request;
- race between STOP ALL and action dispatch;
- concurrent operators;
- concurrent scenarios;
- cancellation while waiting;
- cancellation during adapter dispatch.

Confirm that:

`scenario validity != mutation authority`

and that mutating authority is checked at the final possible point before dispatch.

Any path capable of turning:

`READ_ONLY -> mutation`

without external Track A authority is a critical finding.

# AUDIT AREA C — STOP ALL / CANCELLATION

Deeply audit the proposed `STOP ALL` semantics.

Determine whether the design adequately defines:

- cancellation generation;
- queued work rejection;
- active scenario cancellation;
- active adapter call cancellation;
- bounded wait cancellation;
- capture shutdown;
- local lock cleanup;
- stale completion rejection;
- post-cancellation events;
- restart after STOP;
- concurrent request races.

Look specifically for the classic race:

```text
preflight PASS
        |
        +---- STOP ALL
        |
dispatch mutation
```

The design must provide a concrete implementation strategy that prevents or fences this race.

Do not accept vague language such as `cancel active action` if the contract does not make the behavior implementable.

# AUDIT AREA D — SCENARIO ENGINE

Audit the scenario model for determinism and testability.

Check:

- validation;
- stable step IDs;
- preconditions;
- timeouts;
- assertions;
- waits;
- abort conditions;
- side-effect budgets;
- capability requirements;
- session/runtime fencing;
- retries;
- idempotency;
- partial completion;
- failure propagation;
- cancellation;
- reproducibility.

Determine whether the schema can represent at least:

- movement;
- turning;
- spell cast;
- potion use;
- food;
- rune use;
- target selection;
- attack/follow;
- inventory;
- containers;
- equipment;
- controlled chat;
- read-only observation;
- before/after checkpoints.

Identify any semantics that are underspecified enough that two agents could implement materially incompatible engines.

# AUDIT AREA E — SIDE-EFFECT BUDGETS

Verify that the proposed budget model is enforceable rather than decorative.

Audit at minimum:

- max runtime;
- max actions;
- max movement;
- spells;
- consumables;
- moved items;
- gold;
- Tibia Coins;
- irreversible changes.

Determine:

1. which budgets can be enforced before dispatch;
2. which require state confirmation;
3. how failed or ambiguous actions consume budget;
4. how duplicate dispatch is accounted for;
5. whether budget state survives retries/reconnects within one run.

Flag any budget that appears safe in YAML but cannot actually be measured reliably.

# AUDIT AREA F — RECORDER AND CAUSAL EVIDENCE

Compare the Control Center Recorder design against:

`OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md`

Verify preservation of:

- session epoch;
- monotonic timestamps;
- stimulus ID;
- direction;
- sequence/correlation data;
- runtime thread when observable;
- handler/object identity;
- before state;
- after state;
- semantic delta;
- negative/no-stimulus controls;
- evidence reference.

Check whether the proposed normalized `Event` envelope loses any information required for causal RE.

Verify that correlation is not incorrectly treated as causal proof.

Determine whether one unified event sequence across:

```text
ACTION
TRACE
NET
STATE
SCREEN
SNAPSHOT
ASSERTION
RESULT
```

can be implemented without lying about ordering across independent sources.

Require explicit handling of:

- source timestamp;
- ingestion timestamp;
- sequence scope;
- clock domain;
- unknown ordering.

# AUDIT AREA G — NETWORK CAPTURE

Audit the default metadata-only network design.

Check whether it provides enough information for:

- C2S/S2C discrimination;
- connection/session lane;
- message candidate correlation;
- packet/message sequence;
- packet size;
- semantic message type when actually known.

Verify that it does **not** persist sensitive:

- login credentials;
- auth tokens;
- session tokens;
- tickets;
- encryption material;
- secret-bearing payloads.

Find any field or artifact path where secrets could accidentally escape through:

- exceptions;
- repr/debug output;
- raw packet fallback;
- reports;
- screenshots;
- agent bundles.

# AUDIT AREA H — PRIVACY / REDACTION

Falsify the redaction model.

Test the design conceptually against:

- email;
- password;
- 2FA;
- auth/session tokens;
- cookies;
- tickets;
- RSA material;
- private chat;
- player identities;
- screenshots containing login UI;
- trace strings;
- environment variables;
- exception messages.

Determine whether redaction occurs:

```text
BEFORE event creation
```

or only at export time.

Preferred invariant:

> secret-class data never enters the normal event/artifact object graph.

Flag export-time-only redaction as a material weakness.

# AUDIT AREA I — CONTROL API

Audit the proposed browser/CLI Control API.

Check:

- one domain path for browser and CLI;
- no GUI bypass;
- no hidden raw-action endpoint;
- request bounds;
- action idempotency;
- replay protection;
- duplicate POST handling;
- event-stream bounds;
- run-history bounds;
- cancellation;
- shutdown;
- malformed inputs.

Initial implementation is intended to be loopback-only.

Verify that this is sufficient and clearly specified.

If future LAN exposure is discussed, confirm the current design does **not** accidentally make remote unauthenticated control easy to enable.

# AUDIT AREA J — WEB UI

Audit whether the dense proposed GUI is technically reasonable.

Required major surfaces:

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

Verify the design correctly separates:

- observation;
- configuration;
- action;
- evidence status;
- authority status.

Check that `MUTATION_ALLOWED` cannot be mistaken for a checkbox or local UI setting.

Verify that unknown state is rendered as `UNKNOWN` rather than fake/example data.

Audit whether manual Quick Actions correctly become one-step experiments instead of bypassing Recorder/Scenario Engine.

# AUDIT AREA K — DIRECT-MACHINE MODE

Verify that CLI/local operation and browser operation actually share the same backend semantics.

Find any reason they might drift into two execution implementations.

Preferred invariant:

```text
Browser
   \
    -> Control API/domain service -> Scenario Engine
   /
CLI
```

not:

```text
Browser -> API
CLI -> direct adapter calls
```

Treat a CLI bypass as a material architecture defect.

# AUDIT AREA L — OFFICIAL TIBIA ADAPTER

Determine whether Adapter Contract v1 is sufficient to hide implementation-specific details such as:

- GUI coordinates;
- raw key presses;
- QMeta IDs;
- function addresses;
- vtables;
- packet opcodes;
- wire layouts.

Scenarios should express semantic intent such as:

```text
move NORTH
cast_spell EXURA
use_consumable HEALTH_POTION
```

not runtime implementation details.

Verify independent read/action maturity remains representable:

```text
R0-R4
A0-A4
```

and that read support can never imply action support.

# AUDIT AREA M — OTERYN V2 E2E ADAPTER

Audit the proposed future cross-repository boundary against current `blakinio/Oteryn-v2`.

Verify that:

- Oteryn retains `protocol-oteryn`;
- Control Center does not require Tibia wire compatibility;
- semantic comparison is sufficient;
- server-authoritative Oteryn state remains authoritative;
- test hooks do not create an unauthenticated production control interface;
- adapter/test code can be excluded or locked down appropriately in production;
- cross-repo versioning can be managed.

Determine whether `TIBIA_RE_CONTROL_CENTER_ADAPTER_V1` is actually generic enough for Oteryn without polluting Oteryn architecture with Track A concepts.

Flag fields that should live in official-adapter-specific extensions rather than the generic contract.

# AUDIT AREA N — DIFFERENTIAL E2E

Falsify the proposed semantic comparison approach.

Check expected comparison semantics for:

- position;
- HP;
- mana;
- conditions;
- target state;
- inventory;
- containers;
- equipment;
- cooldowns;
- visual/game effects;
- timing.

Classify comparison fields as:

```text
EXACT
NORMALIZED_EXACT
SET_EQUIVALENT
ORDERED_EQUIVALENT
TOLERANCE
REFERENCE_ONLY
NOT_COMPARABLE
```

Check that the design does not imply official Tibia and Oteryn should use identical:

- protocol bytes;
- internal object structure;
- timing;
- renderer implementation.

Define what should constitute an E2E mismatch.

# AUDIT AREA O — TESTABILITY

Audit whether Package A can be implemented and validated with **zero Track A runtime access**.

It should be possible to test:

- schema parser;
- fake adapter;
- successful one-step scenario;
- capability refusal;
- read-only mutation refusal;
- authority change;
- runtime identity change;
- timeout;
- STOP ALL;
- budget exhaustion;
- event ordering;
- secret rejection;
- artifact generation.

Identify anything in Package A that unnecessarily depends on the official client.

# AUDIT AREA P — IMPLEMENTATION PHASING

Critically review:

```text
P0 Surveyor
P1 read-only Control Center
P2 Scenario Engine
P3 bounded Official actions
P4 Recorder expansion
P5 research suites
P6 Oteryn adapter
P7 differential E2E
```

and the implementation prompt's:

```text
Package A control-core
Package B browser/CLI
Package C Surveyor integration
Package D Track A mutation adapter
Package E Oteryn adapter
```

Determine whether dependencies are ordered correctly.

Look for work that should move earlier/later.

Especially verify whether:

- Scenario Engine should precede browser UI;
- fake adapter exists before official adapter;
- Recorder primitives should exist before real actions;
- Surveyor integration should wait for #592;
- official action support remains separated from UI implementation.

# AUDIT AREA Q — IMPLEMENTATION READINESS

Answer:

> Could a fresh competent implementation agent now implement Package A solely from repository documentation without needing this chat?

If NO, list exactly what contract/specification is missing.

Examples:

- ambiguous type;
- missing lifecycle;
- missing error semantics;
- missing storage location;
- missing concurrency model;
- missing version negotiation;
- missing cancellation rule;
- missing fake-adapter behavior;
- missing test acceptance criterion.

# REQUIRED FALSIFICATION TESTS

Attempt to construct at least these failure scenarios:

1. authority expires one nanosecond before action dispatch;
2. client restarts between preflight and action;
3. two browser tabs start scenarios simultaneously;
4. CLI and browser trigger the same Quick Action simultaneously;
5. STOP ALL races with action dispatch;
6. network recorder reports after scenario already ended;
7. screenshot contains login credentials;
8. adapter throws exception containing secret material;
9. event sequence receives timestamps from different clock domains;
10. a failed potion dispatch is retried and consumes two potions;
11. Oteryn adapter reports a field official Tibia cannot observe;
12. official adapter reports A4 while read path is only R1;
13. Surveyor #592 changes its output format;
14. HTTP client repeats POST after connection loss;
15. runtime authority changes while a scenario is paused;
16. stale scenario resumes after a new session epoch;
17. operator reloads the browser during an active run;
18. backend process restarts with an action possibly in-flight.

For each, state whether the current design already defines safe behavior.

# REQUIRED OUTPUT

Return exactly this structure:

```text
REVIEW_TYPE=TIBIA_RE_CONTROL_CENTER_INDEPENDENT_AUDIT

REPOSITORY=
CURRENT_MAIN=
DESIGN_PR=
DESIGN_MERGE=
CLOSEOUT_PR=
CLOSEOUT_MERGE=
AUDITED_FILES=
SURVEYOR_STATE=
OTERYN_V2_HEAD=

RESULT=PASS | PASS_WITH_FINDINGS | FAIL

SUMMARY:
<short factual summary>

P0_FINDINGS:
- ...

P1_FINDINGS:
- ...

P2_FINDINGS:
- ...

P3_FINDINGS:
- ...

ARCHITECTURE_VERDICT:
...

TRACK_A_AUTHORITY_VERDICT:
...

STOP_ALL_CONCURRENCY_VERDICT:
...

SCENARIO_ENGINE_VERDICT:
...

RECORDER_CAUSAL_EVIDENCE_VERDICT:
...

SECURITY_PRIVACY_VERDICT:
...

BROWSER_CLI_VERDICT:
...

OFFICIAL_ADAPTER_VERDICT:
...

OTERYN_V2_ADAPTER_VERDICT:
...

DIFFERENTIAL_E2E_VERDICT:
...

PACKAGE_A_IMPLEMENTATION_READY=YES | NO

PACKAGE_A_MISSING_REQUIREMENTS:
- ...

DUPLICATION_OR_OVERLAP:
- ...

FALSIFICATION_RESULTS:
1. ...
2. ...
...
18. ...

RECOMMENDED_CHANGES_BEFORE_IMPLEMENTATION:
1. ...
2. ...

RECOMMENDED_IMPLEMENTATION_ORDER:
1. ...
2. ...

EVIDENCE:
- exact repository paths
- exact PRs
- exact SHAs
- exact workflow/check results when relevant

FINAL_DECISION:
...
```

## Severity definition

`P0` — design can cause unsafe authority/security behavior, secret exposure, irreversible effects, or invalidates the architecture.

`P1` — material flaw likely to require redesign or make the initial implementation unsafe/unreliable.

`P2` — meaningful correctness, maintainability, testability or specification gap that should be fixed before/while implementing the affected phase.

`P3` — non-blocking improvement.

Do not create findings merely to produce output.

A clean section must say:

`NONE`

## Decision criteria

Return `PASS` only if there are no P0/P1 findings and Package A is sufficiently specified for implementation.

Return `PASS_WITH_FINDINGS` when no P0/P1 exists but meaningful P2/P3 improvements remain.

Return `FAIL` if any P0/P1 finding exists or Package A cannot safely start without material redesign.

This is an **independent audit**, not an implementation task.
