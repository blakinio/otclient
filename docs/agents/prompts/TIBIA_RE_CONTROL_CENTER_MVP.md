# TIBIA-RE-CONTROL-CENTER-MVP

Use this prompt only after the design PR containing this file is merged or an owner explicitly selects an exact unmerged head for implementation.

Repository:

```text
https://github.com/blakinio/otclient
```

Execution mode:

```text
AUTONOMOUS BOUNDED IMPLEMENTATION
```

## Mission

Implement the first usable `TIBIA RE Control Center / E2E Lab` without performing real official-client mutation in the initial implementation package.

The product must support both:

1. browser UI served from the Control Center backend;
2. direct-machine CLI using the same backend/domain operations.

The long-term target is the architecture in:

- `docs/agents/programs/TIBIA_RE_CONTROL_CENTER_E2E.md`;
- `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md`.

Do not reconstruct the design from chat history. Git is authoritative.

## Mandatory preflight

Before editing:

1. read root `AGENTS.md` and `docs/agents/README.md`;
2. read all current Track A admission/routing documents required by `docs/agents/README.md`;
3. inspect current `main`, all open PRs and `docs/agents/tasks/active/**`;
4. inspect `docs/agents/MODULE_CATALOG.md`, `REPOSITORY_MAP.md`, `KNOWN_RISKS.md`, `BUILD_TEST_MATRIX.md` and relevant cross-repo contracts;
5. inspect the exact current state of PR #592 and do not assume it merged;
6. search for an existing Control Center/scenario/adapter implementation before creating one;
7. identify shared-path ownership conflicts before editing;
8. create a dedicated task/branch/worktree and Draft PR before substantial implementation.

## Architecture constraint

The implementation must preserve this dependency direction:

```text
Web UI / CLI
      |
      v
Control API
      |
      v
Scenario Engine
      |
      +---- Recorder
      +---- Safety Controller
      |
      v
Adapter contract
      |
      v
Fake/read-only adapter first
```

The web UI must not call official-client tooling directly.

## Package split

Do not implement all phases in one PR.

### Package A — control-core

Implement the smallest reusable core and tests:

- typed/domain models corresponding to Adapter Contract v1;
- capability model;
- normalized runtime status;
- normalized snapshots;
- event envelope;
- scenario schema and validation;
- side-effect budgets;
- cancellation generation;
- one-step experiment representation;
- fake adapter;
- deterministic tests for validation, refusal, timeout, cancellation and event ordering.

No network listener. No official-client access. `runtime_access: none`.

Recommended future path after checking repository conventions:

```text
tools/tibia_re_control_center/
```

Do not create that path if another live PR/task already owns an equivalent abstraction.

### Package B — read-only browser + CLI

Consume merged Package A.

Implement:

- loopback-only Control API by default;
- browser UI;
- CLI;
- status/capabilities/scenario/run views;
- bounded live event view;
- run/artifact browser;
- `STOP ALL` and scenario cancellation;
- no official-client mutation.

UI baseline:

Top bar:

```text
RUNTIME | CLIENT | RECORDER | AUTHORITY | SESSION | STOP ALL | PAUSE
```

Tabs:

```text
Main Runtime Movement Healing Spells Consumables Combat Targeting
Inventory Containers Equipment Chat Conditions Scenarios Recorder
Network Experiments Compare Logger
```

Main layout:

- left: Quick Activator, Profile/Target, Session Info;
- center top: Character State, Conditions, Actions, Target Info;
- center middle: Quick Actions;
- center bottom: Engine Benchmark, Live Events, Active Scenario;
- right: Mini Map, Backpack, Battle List, Hotkeys.

For Package B, mutating Quick Actions are visible but disabled/refused unless backed only by the fake adapter. The UI must clearly show `READ_ONLY` for real Track A state.

Keep the browser implementation lightweight. Inspect repository dependency policy before adding any framework. Prefer a thin local UI over a new build ecosystem unless evidence justifies it.

### Package C — Surveyor integration

Only after PR #592 has an accepted exact state.

Consume Surveyor outputs/interfaces; do not copy its code.

Expose in Control Center:

- coverage summary;
- evidence/index status;
- read-only runtime snapshot;
- current-client fence/provenance;
- compact agent bundle link/status.

Any #592 API mismatch should be repaired by a bounded integration contract change, not by duplicating Surveyor internals.

### Package D — official Track A action adapter

This is a separate runtime-sensitive task and is NOT authorized by this prompt merely because Packages A-C exist.

Before any real action:

- create a current Track A runtime task;
- obtain the applicable runtime access class;
- satisfy current canonical registration/lease/Gate A/rebind/Gate B/target-uniqueness/supervisor requirements;
- prove current action capability/evidence gate;
- use the shared GUI input lock when applicable;
- define effect budget and abort behavior;
- preserve reference-path parity evidence.

Start with the smallest already-proven action surface. Do not batch many gameplay families into the first mutation PR.

### Package E — Oteryn v2 adapter

Separate repository task/branch/PR in:

```text
blakinio/Oteryn-v2
```

Read that repository's current governance before acting.

Do not implement new Rust product code under historical `blakinio/otclient/oteryn-client/**`.

The Oteryn adapter exposes semantic snapshots/actions for E2E comparison. It must not add Tibia wire compatibility as a test shortcut.

## Required UI behavior

### Authority

The top status bar always shows one of:

```text
READ_ONLY
MUTATION_ALLOWED
EXPIRED
DENIED
UNKNOWN
```

Unknown/stale/expired authority disables mutation.

### Quick Actions

Every manual action is internally a validated one-step scenario:

```text
snapshot before
-> action
-> bounded wait/assertion
-> snapshot after
-> result
```

No separate unrecorded manual mutation path.

### STOP ALL

`STOP ALL` must:

- latch harness cancellation;
- reject new mutation requests;
- cancel queued steps;
- request bounded cancellation of active work;
- release harness-owned local locks/resources;
- emit a terminal event;
- never kill the official client without separate current process-control authority.

### Unknown data

Render unknown/unproven fields as unknown. Do not fabricate HP, position, inventory, battle list, minimap or capability values to make the UI look complete.

## Recorder requirements

Use one normalized event envelope and monotonic ordering.

Required event kinds:

```text
SYSTEM AUTHORITY ACTION TRACE NET STATE SCREEN SNAPSHOT ASSERTION RESULT ERROR
```

Default network capture is metadata-only.

Never persist:

- email/password/2FA;
- auth/session tokens;
- cookies/tickets;
- secret-bearing process memory;
- secret-bearing packet payloads;
- unnecessary private chat text/personal data.

## Artifact requirements

Per run:

```text
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

Store large/raw captures outside Git unless current evidence policy explicitly permits them. Git stores normalized evidence, hashes and minimal necessary excerpts.

## Testing

Package A must have deterministic unit tests for at least:

- schema acceptance/rejection;
- unsupported capability refusal;
- mutation refusal under read-only authority;
- budget exhaustion;
- runtime/session identity change;
- timeout;
- cancellation/STOP ALL;
- monotonic event ordering;
- secret-class event rejection/redaction;
- fake-adapter successful one-step experiment.

Package B must test:

- loopback default bind;
- API refusal paths;
- UI rendering of authority states;
- disabled mutating controls under read-only state;
- browser/CLI parity for shared backend operations;
- bounded event/run history.

Select exact commands from current `BUILD_TEST_MATRIX.md`; do not invent preset names.

## Completion boundaries

A package is not complete because the UI renders.

For each PR:

- inspect full diff and changed-file set;
- run focused tests;
- run exact-head required CI;
- perform mandatory self-review;
- obtain independent review when current risk policy requires it;
- record exact evidence in the task/PR;
- update module catalogue/changelog when the reusable implementation is actually added;
- merge only through current repository policy.

Do not claim:

- real official-client action capability from fake tests;
- real runtime compatibility from repository-only tests;
- Oteryn parity before a separate Oteryn-v2 adapter exists;
- remote/LAN security before a dedicated exposure design is tested;
- protocol semantic proof from timestamp correlation alone.

## Owner-funded AI

Do not invoke Codex/OpenAI API/other owner-funded AI merely because this prompt exists. Follow current repository authorization rules exactly. Central Spark advisory review, if eligible, remains separate from implementation authority.

## Desired first terminal result

After Packages A-C, the operator should be able to launch the Control Center locally, open the dense browser UI or CLI, inspect read-only Track A/Surveyor state, browse scenarios/runs/events, execute deterministic fake-adapter one-step experiments, cancel them safely and export `agent_bundle.json` — while all real official-client mutation remains fail-closed until Package D receives its own current runtime admission.
