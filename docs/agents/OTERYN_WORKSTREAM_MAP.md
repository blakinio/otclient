# Oteryn OTClient Workstream and File Map

Status: normative routing guide  
Repository: `blakinio/otclient`  
Primary platform: Windows  
Last reviewed: 2026-07-25

Use this document to decide where a change belongs, which files may be owned by one task and which neighboring systems must be inspected. Live GitHub state, task records and source remain authoritative.

## 1. Start-of-task routing

Before editing:

1. Read `AGENTS.md` and `docs/agents/README.md`.
2. Inspect all open PRs and `docs/agents/tasks/active/**`.
3. Search `MODULE_CATALOG.md`, source and tests for an existing owner.
4. Identify the workstream below.
5. Claim the narrowest practical `owned_paths` in a task record.
6. Declare overlap, dependencies and any `OTS-*`/`CAN-*` coordination.
7. Create a branch and draft PR before substantial implementation.

Do not choose work from chat history alone. Verify the live branch, current `main`, open PRs, upstream delta and CI policy.

## 2. Repository structure

```text
blakinio/otclient/
├── AGENTS.md                         # highest-priority repository instructions
├── AGENT_HANDOFF.md                  # legacy detailed handoff; verify freshness
├── CMakeLists.txt
├── CMakePresets.json
├── init.lua
├── otclientrc.lua
├── src/
│   ├── client/                       # game state, protocol, map, things, services
│   ├── framework/                    # engine, UI primitives, Lua, resources, network
│   ├── protobuf/                     # generated/schema-related protocol support
│   └── main.cpp
├── modules/
│   ├── client_entergame/             # login, character list, Oteryn Identity
│   ├── client_assets/                # secure asset discovery/install
│   ├── client_options/               # current options UI/settings wiring
│   ├── game_interface/               # main in-game composition and panels
│   ├── game_actionbar/               # action bars, actions and cooldown presentation
│   ├── game_console/                 # channels, messages and console policy
│   ├── game_features/                # protocol/client feature selection
│   ├── game_inventory/               # inventory/equipment presentation
│   ├── game_minimap/                 # minimap UI and persistence
│   ├── game_wheel/                   # Wheel of Destiny and Gem Atelier
│   ├── game_forge/                   # Forge flows and timers
│   └── game_*/                       # other shipped feature owners
├── mods/                             # optional/custom behavior only
├── data/
│   ├── images/                       # runtime UI/game images
│   ├── styles/                       # shared OTUI styles
│   ├── fonts/
│   ├── things/<version>/             # runtime things assets
│   └── sounds/<version>/             # runtime sounds
├── bin/                              # expected runtime extras
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── lua/
│   ├── fixtures/
│   └── support/
├── docs/
│   ├── architecture/                 # stable target architecture
│   ├── agents/                       # operating memory, tasks, contracts and prompts
│   └── ui/                           # capability audits and UI parity plans
├── cmake/
├── vc18/                             # Visual Studio solution support
└── .github/workflows/                # primary and reusable CI workflows
```

Names shown for existing directories are navigational, not a guarantee that every module has identical internal files. Inspect the actual manifest before editing.

## 3. Planned first-party structure

Create these only in the milestone that needs them and only after confirming no equivalent already exists:

```text
modules/game_taskboard/
├── game_taskboard.otmod
├── game_taskboard.lua
├── controllers/
├── models/
├── views/
├── styles/
├── locale/
└── tests are placed under tests/, not inside the module

data/images/ui/oteryn/
├── common/
├── enter_game/
├── game_interface/
├── windows/
├── actionbar/
├── status/
├── console/
├── minimap/
├── inventory/
└── taskboard/

data/styles/oteryn/
├── palette.otui
├── typography.otui
├── controls.otui
├── windows.otui
├── miniwindows.otui
├── game_interface.otui
├── actionbar.otui
└── taskboard.otui

tests/
├── unit/client/protocol/              # protocol field/order/version fixtures
├── unit/framework/                    # engine/native behavior
├── integration/protocol/              # bounded loopback and cross-layer flows
├── integration/auth/                  # Oteryn login/session negative and positive flows
├── lua/modules/                       # module/controller contracts
└── fixtures/protocol/<version>/       # synthetic or legally captured fixtures
```

Do not create duplicate shared style or test hierarchies merely to match this example. Extend current conventions when they already provide the required owner.

## 4. Workstream matrix

### WS-00 — Repository governance and Windows CI

Primary responsibilities:

- branch/PR/task rules;
- required-check graph;
- Windows presets, Visual Studio/CMake matrix and packaging policy;
- dependency/action pinning and minimal permissions.

Primary paths:

```text
AGENTS.md
docs/agents/**
.github/workflows/ci.yml
.github/workflows/reusable-checks.yml
.github/workflows/reusable-tests-lua.yml
.github/workflows/reusable-build-windows.yml
CMakePresets.json
cmake/**
vc18/**
```

Do not combine with feature behavior. Lightweight checks may run on Ubuntu, but current policy compiles only Windows.

Acceptance:

- actionlint/yamllint and emitted job graph are correct;
- `CI / Required` reflects the real Windows-only dependency graph;
- no required failure is silenced;
- non-Windows compatibility is not claimed.

### WS-01 — Oteryn Identity and game-session handoff

Primary responsibilities:

- browser Authorization Code + PKCE;
- loopback callback;
- Platform ticket and Gateway exchange;
- authoritative world routing;
- one-shot `GameSessionKey` lifecycle;
- negative cases: replay, fallback, stale callback and automatic reconnect.

Primary paths:

```text
modules/client_entergame/oteryn_identity*.lua
modules/client_entergame/oteryn_session_guard.lua
modules/client_entergame/** auth integration points
src/framework/net/server.*
src/framework/util/crypt.*
init.lua
tests/**/auth*
docs/agents/CROSS_REPO_CONTRACTS.md
```

Required neighboring inspection:

```text
src/client/game.*
src/client/protocolgame*
character-list/world-login controller
Oteryn Platform contract
selected Canary Game Session adapter
```

Hard stop:

- no password fallback;
- no long-lived token exposure to Lua;
- no production claim without exact Canary E2E.

### WS-02 — Enter-game and character-list presentation

Primary responsibilities:

- Oteryn login shell and legacy login presentation;
- character list layout, world/character status and error presentation;
- destroy/recreate/relogin lifecycle;
- visual responsiveness.

Primary paths:

```text
modules/client_entergame/*.lua
modules/client_entergame/*.otui
modules/client_entergame/*.otml
data/images/ui/oteryn/enter_game/**
data/styles/oteryn/**
```

Boundary:

- reuse WS-01 authentication APIs;
- presentation must not implement OAuth, ticket or session logic;
- retain legacy mode unless an explicit migration removes it.

Acceptance:

- Oteryn and legacy flows load the correct layout;
- repeated destroy/create and failed-login cycles are safe;
- missing layouts fail clearly;
- no credentials are logged or persisted.

### WS-03 — Main interface, skin and layout

Primary responsibilities:

- viewport composition;
- top/bottom panels, sidebars, status, console and action-bar placement;
- Oteryn palette, typography and widget states;
- dynamic layout tree and migration in later milestones.

Primary paths:

```text
modules/game_interface/**
modules/client_topmenu/**
modules/game_console/**
modules/game_inventory/**
modules/game_minimap/**
data/images/ui/oteryn/**
data/styles/oteryn/**
```

Boundary:

- do not rewrite rendering for a skin change;
- use framework changes only for missing primitives such as robust docking/drop preview/DPI behavior;
- no proprietary artwork.

Acceptance:

- representative Windows resolution and DPI evidence;
- no clipping of critical controls;
- stable IDs or migrations;
- layout state restores after restart and version migration where implemented.

### WS-04 — Options, controls and configuration

Primary responsibilities:

- metadata-driven option registry;
- basic/advanced filtering;
- General, Action Bar and Custom Hotkey sections;
- persistence, schema migration and safe import/export;
- console/interface/gameplay/screenshot policies.

Primary paths:

```text
modules/client_options/**
modules/game_hotkeys/** or current hotkey owner
modules/game_interface/** option hooks
modules/game_console/** option hooks
modules/game_actionbar/** option hooks
settings/config helpers
tests/lua/** options contracts
```

Boundary:

- option module owns metadata and orchestration;
- feature module owns the actual feature behavior;
- no inert controls;
- import/export excludes secrets and validates schema/size.

Initial repair set:

- Right Bar 3 reset/duplicate ID;
- inventory expiry event ownership;
- dead status-bar controls;
- disabled unused-item expiry option;
- incorrect walk-delay labels;
- misspelled key migration.

### WS-05 — Action bars, hotkeys and cooldown lifecycle

Primary responsibilities:

- nine action bars and their persistence;
- action types and hotkey resolution;
- spell/group/multi-use cooldown state;
- relog restoration and overlay lifecycle.

Primary paths:

```text
modules/game_actionbar/**
modules/game_hotkeys/** or current input owner
src/client/protocolgameparse.cpp cooldown parsing
src/client/game.* callback surface
tests/lua/** actionbar tests
tests/unit/client/** protocol cooldown fixtures
```

Boundary:

- protocol cooldown state exists independently of visible bars and visual-option toggles;
- module UI consumes state but does not define packet truth;
- session reset must be explicit and correctly timed.

Acceptance:

- packets received before widget creation are retained;
- relog and module reload do not lose valid cooldowns or leak old ones;
- individual/group cooldown chooses the greatest valid remaining duration;
- runes, spells and multi-actions follow one restoration policy.

### WS-06 — Modern protocol 15.2x and legacy regression compatibility

Primary responsibilities:

- 15.24/15.25 Monk, level percent, XP, resources, Wheel/Forge/store/reward payloads;
- selected older-protocol regressions such as VIP 10.98 and chargeable items 7.80–8.54;
- exact feature/version gates.

Primary paths:

```text
src/client/protocolgame*.cpp
src/client/protocolcodes.h or current definitions
src/client/game.*
modules/game_features/**
affected modules
tests/unit/client/protocol/**
tests/integration/protocol/**
docs/agents/CROSS_REPO_CONTRACTS.md
```

Boundary:

- every packet change is an `OTS-*` contract task;
- no blind cherry-pick from `solchanel/otclient-15`;
- parser compilation alone is not acceptance.

Required proof:

- exact Canary producer path and commit;
- order, widths, signedness, optional fields and gate;
- positive, malformed and truncated fixtures;
- unsupported client/server combination behavior;
- Windows runtime or loopback evidence.

### WS-07 — Taskboard

Primary responsibilities:

- server-driven bounty/weekly/preferred/shop/Soulseal/tracker feature;
- payload models, UI controller and original Oteryn assets.

Primary paths:

```text
src/client/** existing Taskboard parsers/definitions
modules/game_features/**
modules/game_taskboard/** planned
data/images/ui/oteryn/taskboard/** planned
data/styles/oteryn/taskboard.otui planned
tests/unit/client/protocol/**
tests/lua/modules/**
docs/agents/CROSS_REPO_CONTRACTS.md
```

Boundary:

- Canary owns prices, progress, rewards and eligibility;
- do not duplicate current parser entry points;
- do not copy external binary assets or a multi-thousand-line feature wholesale.

Implementation packages:

1. contract and fixtures;
2. parser/callback completion;
3. read-only UI model;
4. user actions and server errors;
5. persistence/tracker integration;
6. exact-version E2E and original art acceptance.

### WS-08 — Assets, updater and packaging

Primary responsibilities:

- version-correct asset acquisition;
- strict hashes and staging/final paths;
- updater responsiveness, cancellation and rollback;
- Windows distribution.

Primary paths:

```text
modules/client_assets/**
updater modules/services
src/framework/core/resourcemanager.*
data/things/**
data/sounds/**
bin/**
docs/client-assets-auto-install.md
```

Boundary:

- no weakened TLS/hash checks;
- no runtime use of staging/cache;
- no proprietary asset commit without rights;
- hashing/extraction must not block the UI without progress/cancellation.

Acceptance:

- clean install and repair on Windows;
- correct requested-version archive selection;
- tamper and mismatch failures;
- rollback/retry semantics;
- no credential or private path leakage in logs.

### WS-09 — Interaction and lifecycle defects

Primary responsibilities:

- containers and drop zones;
- miniwindow input focus;
- classic mouse chords and walking keys;
- use-with cursor cleanup;
- battle-list identity updates;
- Forge/Wheel timer and callback cleanup.

Primary paths depend on the owning module. Do not create a generic interaction module unless several owners require a proven reusable primitive.

Acceptance:

- exact reproduction first;
- deterministic input/lifecycle tests where feasible;
- repeated init/terminate, login/logout and widget destroy/create;
- no unrelated control behavior regressions.

### WS-10 — Performance and diagnostics

Primary responsibilities:

- startup profiling;
- stats collection policy;
- outfit preview/render performance;
- text flicker investigation;
- updater checksum work;
- actionable diagnostic logs without secret leakage.

Primary paths:

```text
src/framework/**
src/client/**
affected modules
profiling/diagnostic settings
tests/performance or focused benchmarks when introduced
```

Boundary:

- measure before changing;
- do not reduce correctness checks for speed;
- expensive work needs cancellation/lifetime handling;
- logging must not expose auth tokens, tickets, session keys or personal paths.

## 5. Shared-path ownership rules

### `src/client/protocolgameparse.cpp`

High-contention path. One active protocol task should own the affected parser region. Other agents must coordinate rather than edit adjacent opcodes in parallel.

### `modules/client_entergame/**`

Separate presentation work from authentication/session work. A task must declare which boundary it owns and inspect the other open PR before editing.

### `modules/game_interface/**`

Treat as composition infrastructure. Feature-specific state belongs in the feature module; main-interface changes should expose a narrow docking/panel API.

### `modules/client_options/**`

The options task owns metadata and controls. Feature tasks own callbacks and observable behavior. Agree on option IDs and migration before parallel edits.

### `data/images/**` and `data/styles/**`

Declare namespace ownership. Never overwrite another feature's assets or silently replace existing resources. Record provenance for every new distributable asset.

### `tests/support/**`

Shared infrastructure only. New helpers require catalogue review and broad utility. Feature fixtures/tests belong under the closest unit/integration/Lua area.

### `.github/workflows/**`, CMake and presets

Owned by a dedicated build/CI task. Feature tasks should not opportunistically modify the matrix to obtain green checks.

## 6. Work package sizing

Prefer one PR for one observable behavior:

Good packages:

- restore cooldowns through relog with focused tests;
- recreate character-list layouts safely;
- normalize one protocol field under an exact feature gate;
- add Taskboard parser fixtures without UI;
- add one options registry slice and migrations;
- add the Oteryn action-bar skin without changing action logic.

Bad packages:

- “implement all Global options”;
- “merge all 15.22 changes”;
- Taskboard + protocol + assets + updater in one PR;
- broad renderer refactor mixed with a UI skin;
- CI weakening bundled with a feature fix.

Split when a package crosses two trust boundaries, two protocol contracts, or independent rollback units.

## 7. Required task metadata

Every active task must declare:

```yaml
owned_paths:
modules_touched:
reuses:
depends_on:
blocks:
cross_repo_tasks:
```

For protocol/auth/assets also record:

```text
exact producer and consumer
feature/version gate
supported and unsupported pairs
security/failure behavior
fixture or runtime evidence
rollout order
```

## 8. Current priority order

Verify live state before using this list:

1. merge/establish Windows-only CI policy;
2. finish safe upstream synchronization and update stale platform-specific acceptance text;
3. deterministic P0/P1 lifecycle and option repairs;
4. exact 15.24/15.25 protocol compatibility;
5. options registry and missing controls;
6. screenshot/layout systems;
7. Taskboard contract and implementation;
8. interaction/performance backlog;
9. production Oteryn visual acceptance and release hardening.

A blocked higher-priority package does not justify editing its owned paths. Choose the highest unblocked package with non-overlapping ownership.

## 9. Completion checklist

Before marking a PR ready:

- inspect the complete diff and changed-file list;
- verify every file belongs to the declared workstream;
- confirm Oteryn security invariants are unchanged or explicitly tested;
- confirm exact Canary pairing for protocol-dependent work;
- run focused validation and final required Windows checks on the exact head;
- remove unsupported claims about other platforms;
- update task, contracts, module catalogue and docs where applicable;
- ensure no proprietary assets, secrets or external-repository writes;
- leave one concrete next action in the task handoff.
