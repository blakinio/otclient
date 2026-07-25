# Oteryn OTClient Target Architecture

Status: normative project architecture  
Scope: `blakinio/otclient`  
Primary platform: Windows  
Last reviewed: 2026-07-25

This document defines stable technical boundaries for the Oteryn OTClient fork. It does not replace live source, `AGENTS.md`, open pull requests, task records, protocol contracts or the current capability audit. It explains where behavior belongs, which component owns state and which invariants may not be weakened.

## 1. Product objective

Build a first-party Windows client for the Oteryn ecosystem by evolving OTClient Redemption instead of rewriting the entire engine.

The client must provide:

- secure Oteryn Identity login through Authorization Code + PKCE;
- one-shot game-session handoff without sending the Oteryn account password to the game login path;
- exact, tested compatibility with selected Canary revisions;
- a modern Oteryn interface inspired by the ergonomics of Tibia Global without copying proprietary artwork;
- controlled upstream synchronization;
- deterministic lifecycle, protocol and regression tests;
- small, reviewable and reversible changes.

## 2. System context

```text
+------------------------+
| Oteryn Identity        |
| Authorization Endpoint |
+-----------+------------+
            | Authorization Code + PKCE
            v
+--------------------------------------------------+
| Oteryn OTClient for Windows                     |
|                                                  |
|  Enter Game / Identity Adapter                  |
|            |                                     |
|            v                                     |
|  Platform Ticket + Game Gateway Adapter         |
|            |                                     |
|            v                                     |
|  One-shot GameSessionKey                        |
|            |                                     |
|            v                                     |
|  C++ Game/Protocol Core <-> Lua/OTUI Modules    |
+-----------------------+--------------------------+
                        |
                        | selected character + one-shot session
                        v
+-----------------------+--------------------------+
| Canary / game-login acceptance adapter          |
| authoritative game state, tasks, economy, world |
+--------------------------------------------------+
```

Related repositories and services are external dependencies. Routine writes from an OTClient task are permitted only in `blakinio/otclient`.

## 3. Architectural layers

### 3.1 Windows application and platform layer

Primary paths:

```text
src/main.cpp
src/framework/core/**
src/framework/platform/**
cmake/**
CMakePresets.json
vc18/**
.github/workflows/reusable-build-windows.yml
```

Responsibilities:

- application startup and shutdown;
- process, window, filesystem and URL-launch integration;
- Windows build presets and packaging;
- resource discovery and writable user directory;
- native event loop and graphics backend selection.

Rules:

- Windows is the only compiled and required platform during the current project phase;
- non-Windows source may remain, but Windows work must not claim Linux, macOS, browser, Android or Docker compatibility;
- platform integration must not weaken URL, path, archive or process-argument safety;
- launcher/updater work is a separate trust boundary and must use signed or strictly hashed artifacts.

### 3.2 Framework and engine layer

Primary paths:

```text
src/framework/**
data/styles/**
data/fonts/**
data/images/**
```

Responsibilities:

- rendering, textures, shaders and draw pools;
- UI widget primitives and layouts;
- Lua runtime and C++ bindings;
- networking primitives, HTTP, sockets and loopback server support;
- resources, archives, settings and cryptographic helpers;
- reusable timers, events and dispatchers.

Rules:

- add a framework abstraction only when several modules need it or Lua/OTUI cannot correctly provide the behavior;
- framework changes require focused C++ tests and Windows compilation;
- do not move feature-specific policy into the framework;
- native code exposed to Lua must have explicit ownership and lifetime semantics.

### 3.3 Game and protocol core

Primary paths:

```text
src/client/**
modules/game_features/**
tests/unit/client/**
tests/integration/protocol/**
```

Responsibilities:

- game connection lifecycle;
- packet framing, parsing and encoding;
- feature/version gates;
- local player, creatures, map, items and containers;
- authoritative protocol state delivered to modules;
- bounded handling of malformed or unsupported data.

Rules:

- Canary and the exact selected protocol contract are the source of truth for field order, widths, signedness, optionals and opcode meaning;
- protocol behavior must not be inferred only from another client fork;
- every modern protocol change requires parser/output fixtures and a linked Canary commit or documented missing environment;
- unknown or malformed messages must fail boundedly without cursor rewind, busy loops or uncontrolled allocation;
- protocol state must not depend on whether a visual widget is currently open.

### 3.4 Authentication and session boundary

Primary paths:

```text
modules/client_entergame/oteryn_identity*.lua
modules/client_entergame/oteryn_session_guard.lua
modules/client_entergame/**
src/framework/net/server.*
src/framework/util/crypt.*
init.lua
tests/**/auth*
```

Responsibilities:

- launch the system browser;
- create PKCE verifier/challenge and state;
- receive the OS-assigned loopback callback;
- exchange the authorization result for a short-lived Platform Game Login Ticket;
- call the standalone Game Gateway;
- accept only server-authoritative world routing;
- transfer a one-shot `GameSessionKey` into the normal world-login path.

Non-negotiable invariants:

1. The Oteryn account password is never collected, stored or sent by the Oteryn profile.
2. Oteryn mode never silently falls back to legacy password authentication.
3. OAuth state, callback path, PKCE and endpoint validation remain strict.
4. Gateway `world_id` is the authoritative routing input.
5. The Game Session credential is consumed once and cleared after the normal handoff.
6. Automatic reconnect does not replay an Oteryn Game Session credential.
7. Long-lived bearer credentials are not exposed to Lua modules.
8. Production enablement requires a selected Canary Game Session adapter and exact-version E2E.

The enter-game presentation may change independently, but it must reuse this authentication boundary rather than duplicate it.

### 3.5 Shipped feature modules

Primary paths:

```text
modules/client_*/**
modules/game_*/**
```

A shipped feature normally owns:

```text
modules/<module>/
├── <module>.otmod        # dependencies, load order and startup
├── <module>.lua          # entry point and lifecycle
├── controllers/          # optional controller-owned behavior
├── models/               # optional payload/view models
├── widgets/ or styles/   # optional reusable local styles
├── *.otui / *.otml       # layout and style declarations
└── locale/               # localization when applicable
```

Responsibilities:

- feature-specific state and behavior;
- UI controller lifecycle;
- subscription to `g_game` and other module events;
- persistence scoped to the feature/profile/character as appropriate;
- graceful feature-off and unsupported-server behavior.

Rules:

- the module controller owns its widgets, timers, callbacks and event connections;
- `terminate`, logout, reload and destroy paths must be idempotent;
- event connections required to retain protocol state must exist independently of visual visibility;
- avoid new globals; use controller-owned state or an existing service;
- do not place required production fixes in `mods/**`.

### 3.6 UI composition and Oteryn skin

Primary/current paths:

```text
modules/game_interface/**
modules/client_topmenu/**
modules/client_entergame/**
modules/game_actionbar/**
modules/game_console/**
modules/game_inventory/**
modules/game_minimap/**
data/styles/**
data/images/ui/**
```

Planned Oteryn-owned assets and styles should use a dedicated namespace, following existing runtime conventions verified at implementation time:

```text
data/images/ui/oteryn/**
data/styles/oteryn/**
```

Responsibilities:

- main viewport composition;
- side panels, console, status displays and action bars;
- window appearance, spacing, typography and interaction states;
- responsive behavior at supported Windows resolutions and DPI settings;
- layout persistence and migration.

Rules:

- visual inspiration may follow modern game-client ergonomics, but artwork, icons, logos and frames must be original or independently licensed;
- presentation changes should remain in Lua/OTUI/assets unless an engine capability is genuinely missing;
- preserve stable widget IDs or provide a migration when controllers depend on them;
- unsupported controls must be hidden or disabled with a clear reason, never shown as inert UI;
- validate representative 1080p, 1440p, 4K and ultrawide layouts when a UI milestone is ready.

### 3.7 Options and user configuration

Current behavior is distributed across options modules, feature modules and settings. The target design is a metadata-driven registry.

Target option metadata:

```text
id
category
subgroup
label
tooltip
basic_or_advanced
default
value_type
constraints
dependency
availability_probe
unavailable_reason
persistence_scope
migration_version
apply_callback
```

Responsibilities:

- basic/advanced filtering;
- one authoritative option key per behavior;
- persistence and schema migration;
- import/export validation;
- observable application of every enabled control;
- explicit unsupported-state handling.

Rules:

- do not add a checkbox before defining its backing behavior, persistence and test;
- typo corrections in existing keys require backward-compatible migration;
- settings import must be schema-versioned and must not import secrets;
- minimap and layout data require separate validation and size limits.

### 3.8 Taskboard and modern server-driven features

Planned module:

```text
modules/game_taskboard/**
```

The Taskboard is not a client-side economy engine. Canary remains authoritative for:

- availability and rotation;
- task definitions and progress;
- difficulty and prices;
- balances and rewards;
- preferred/unwanted slots;
- weekly tasks, shop data and error codes.

Required implementation order:

1. shared `OTS-*` contract;
2. exact Canary producer identification;
3. C++ parser/output fixtures;
4. Lua callback contract tests;
5. controller-owned module and feature-off behavior;
6. original Oteryn assets;
7. exact-version Windows client + Canary E2E.

No Taskboard code or binary graphics from another fork may be copied wholesale.

### 3.9 Asset acquisition and distribution

Primary paths:

```text
modules/client_assets/**
data/things/<version>/**
data/sounds/<version>/**
bin/**
docs/client-assets-auto-install.md
```

Rules:

- strict manifest SHA-256 validation remains enabled;
- runtime final paths remain standard and staging/cache paths are transient;
- archive selection must match the requested client version/tag;
- never commit proprietary CipSoft assets without confirmed redistribution rights;
- new distributable assets need source, version, hash and license records;
- asset installation and updater hashing must not freeze the UI thread.

### 3.10 Test architecture

Primary paths:

```text
tests/unit/**
tests/integration/**
tests/lua/**
tests/fixtures/**
tests/support/**
```

Use the existing test foundation; do not create a parallel harness.

Minimum evidence by change type:

| Change | Required evidence |
|---|---|
| Documentation | Markdown/path/full-diff review and required docs checks |
| Lua lifecycle | Syntax, focused Lua test, repeated init/terminate and login/logout |
| OTUI/layout | Parse/load, interaction and supported-resolution evidence |
| C++ core | Focused tests plus final Windows build/test matrix |
| Protocol | framed fixture, malformed/truncated cases, version gates and exact Canary pair |
| Authentication | PKCE/callback/Gateway/session tests and replay/fallback negatives |
| Assets/updater | hash, path, archive-selection, rollback and clean-install evidence |
| Performance | before/after measurement, cancellation and UI-thread behavior |

Passing compilation proves build compatibility, not interactive or server compatibility.

## 4. Dependency direction

Allowed direction:

```text
Windows/platform
       v
framework primitives
       v
client/game/protocol core
       v
module-facing game events/state
       v
feature controllers
       v
OTUI presentation
```

External service direction:

```text
Oteryn Identity -> Platform Ticket -> Game Gateway -> OTClient handoff -> Canary
```

Forbidden patterns:

- framework depending on a specific game module;
- protocol parser depending on widget visibility;
- UI inventing server-authoritative economy or progress values;
- Lua holding long-lived authentication secrets;
- login presentation implementing a second OAuth/session flow;
- modules directly mutating unrelated module internals without a documented interface;
- copying protocol assumptions from a fork without Canary proof.

## 5. State ownership and lifecycle

| State | Owner | Lifetime |
|---|---|---|
| OAuth transaction state and PKCE verifier | Oteryn identity controller/native callback boundary | one authorization attempt |
| Platform ticket | Oteryn identity flow | short-lived exchange only |
| Game Session credential | session guard/enter-game handoff | one normal world-login transfer |
| Protocol connection and parsed game state | C++ `Game`/`ProtocolGame` | one game session |
| Feature payload cache | owning feature controller/model | session or explicit persistence scope |
| Visual widget state | owning module/controller | widget/module lifetime |
| User options | option registry/settings layer | user/profile/character scope with schema version |
| Server economy/task progress | Canary | authoritative server lifetime |

Every asynchronous callback must be tied to an owner generation, cancellable event handle or exact source object. Time windows and global relog flags are not acceptable substitutes for identity validation.

## 6. Current delivery sequence

The current roadmap is:

1. stabilize repository policy and Windows-only CI;
2. synchronize selected upstream changes while preserving Oteryn/security history;
3. repair deterministic lifecycle and existing-option defects;
4. establish exact 15.24/15.25 Canary compatibility;
5. implement metadata-driven options;
6. implement screenshot and dynamic-layout systems;
7. implement Taskboard under a shared server contract;
8. address interaction and measured performance backlog;
9. finish the original Oteryn skin and production acceptance.

Open PR and task state is authoritative. A new agent must not assume this sequence is unblocked without checking live dependencies.

## 7. Definition of done

A work package is complete only when:

- the correct owner layer contains the behavior;
- no security or compatibility invariant is weakened;
- lifecycle cleanup is deterministic;
- unsupported combinations fail clearly and safely;
- focused tests exist at the appropriate layer;
- final required Windows checks pass on the exact head;
- runtime or Canary behavior is claimed only when actually exercised;
- documentation, contracts, task state and PR description are current;
- the diff contains no unrelated files or unlicensed assets.
