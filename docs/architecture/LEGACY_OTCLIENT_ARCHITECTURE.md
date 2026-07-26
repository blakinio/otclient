# Legacy OTClient Architecture Reference

Status: maintained legacy/reference architecture  
Scope: existing C++/Lua/OTUI client outside `oteryn-client/`  
Primary required platform: Windows  
Last reviewed: 2026-07-26

This document preserves the architecture required to maintain the existing OTClient while the greenfield Rust client is developed. It is not the target architecture for the new product.

The normative new-client architecture is under `oteryn-client/docs/architecture/**`.

## 1. Legacy purpose

The existing client remains buildable and supported during migration for:

- current gameplay and protocol compatibility;
- active legacy PR completion;
- exact Canary behavior evidence;
- protocol, asset and feature inventory for the Rust-client audit;
- fallback and product migration until a separately accepted retirement plan exists.

Legacy maintenance must use small, reversible changes. It must not add dependencies from the Rust client to C++/Lua/OTUI.

## 2. Legacy system context

```text
Oteryn Identity
  -> Authorization Code + PKCE
  -> Platform Game Login Ticket
  -> Game Gateway
  -> one-shot GameSessionKey
  -> existing C++ Game/Protocol core
  -> Lua/OTUI feature modules
  -> Canary
```

The Oteryn profile never collects or sends the main account password through the game-login path and never silently falls back to legacy password authentication.

## 3. Layer ownership

### Windows application/platform

Typical paths:

```text
src/main.cpp
src/framework/core/**
src/framework/platform/**
cmake/**
CMakePresets.json
vc18/**
.github/workflows/reusable-build-windows.yml
```

Owns startup/shutdown, process/window/filesystem/URL integration, user directory, Windows build and packaging.

Rules:

- Windows is the required compiled legacy platform in the current phase;
- dormant non-Windows sources do not imply compatibility;
- URL, path, process and archive inputs remain validated;
- updater/launcher changes are a separate trust boundary.

### Framework/engine

Typical paths:

```text
src/framework/**
data/styles/**
data/fonts/**
data/images/**
```

Owns rendering, textures, shaders, draw pools, UI primitives/layouts, Lua runtime/bindings, network primitives, resources, settings, crypto helpers, timers and dispatchers.

Rules:

- add framework abstractions only for proven cross-module needs;
- feature policy stays in the owning module;
- native Lua bindings require explicit lifetime/ownership;
- C++ framework changes require focused tests and Windows compilation.

### Game/protocol core

Typical paths:

```text
src/client/**
modules/game_features/**
tests/unit/client/**
tests/integration/protocol/**
```

Owns game connection, packet framing/parsing/encoding, feature/version gates, map, things, creatures, player and containers.

Rules:

- exact Canary source/commit is authoritative for protocol facts;
- another client fork is never sufficient proof;
- malformed/unknown messages fail boundedly without busy loops or uncontrolled allocation;
- protocol state is independent of widget visibility;
- protocol changes require fixtures, version gates and cross-repository coordination.

### Authentication/session boundary

Typical paths:

```text
modules/client_entergame/oteryn_identity*.lua
modules/client_entergame/oteryn_session_guard.lua
modules/client_entergame/**
src/framework/net/server.*
src/framework/util/crypt.*
init.lua
tests/**/auth*
```

Owns system-browser PKCE, loopback callback, Platform ticket, Game Gateway routing and one-shot game-session handoff.

Non-negotiable invariants:

1. main Oteryn password is not collected/stored/sent by the Oteryn profile;
2. no silent legacy-password fallback;
3. OAuth `state`, callback path, PKCE and endpoint validation remain strict;
4. server/Gateway routing is authoritative;
5. the game-session credential is consumed once and cleared after handoff;
6. reconnect does not replay the initial credential;
7. long-lived bearer credentials are not exposed to general Lua modules;
8. production compatibility requires an exact Canary pair and E2E evidence.

### Shipped feature modules

Typical structure:

```text
modules/<module>/
├── <module>.otmod
├── <module>.lua
├── controllers/
├── models/
├── widgets/ or styles/
├── *.otui / *.otml
└── locale/
```

A module owns feature state, controller lifecycle, event subscriptions, persistence and unsupported-server behavior.

Rules:

- controllers own widgets, timers, callbacks and event connections;
- terminate/logout/reload/destroy paths are idempotent;
- retain protocol state independently of visual visibility where needed;
- avoid new globals;
- required production fixes belong in `modules/`, not `mods/`.

### UI composition

Primary areas include:

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

Rules:

- visual work stays in Lua/OTUI/assets unless a proven engine primitive is missing;
- preserve widget IDs or provide migration;
- unsupported controls are hidden/disabled with a reason, never inert;
- validate representative 1080p, 1440p, 4K and ultrawide layouts when relevant;
- use only original or independently licensed artwork.

### Options/settings

Legacy options remain distributed across options and feature modules. New legacy controls require:

- one authoritative option key;
- real backing behavior;
- persistence scope and migration;
- safe import/export excluding secrets;
- observable apply callback;
- unsupported-state behavior;
- focused tests.

### Assets

Typical paths:

```text
modules/client_assets/**
data/things/<version>/**
data/sounds/<version>/**
bin/**
docs/client-assets-auto-install.md
```

Rules:

- strict SHA-256 validation stays enabled;
- final runtime paths remain standard;
- staging/cache is transient;
- requested version/tag selects the archive;
- no proprietary asset commits without rights;
- source/version/hash/license is recorded for new distributable material;
- hashing/extraction must not freeze UI without progress/cancellation.

## 4. Dependency direction

```text
Windows/platform
  -> framework primitives
  -> client/game/protocol core
  -> module-facing events/state
  -> feature controllers
  -> OTUI presentation
```

Forbidden:

- framework depending on a concrete feature module;
- protocol parser depending on widget visibility;
- UI inventing authoritative economy/progress values;
- Lua retaining long-lived auth secrets;
- login presentation duplicating OAuth/session flow;
- direct mutation of another module's internals;
- protocol assumptions copied without Canary proof.

## 5. State ownership

| State | Legacy owner | Lifetime |
|---|---|---|
| OAuth transaction/PKCE | Identity controller/native callback boundary | one auth attempt |
| Platform ticket | Identity flow | short exchange |
| Game Session credential | session guard/enter-game handoff | one world-login transfer |
| Protocol connection/parsed game state | `Game` / `ProtocolGame` | one game session |
| Feature payload cache | owning module/controller/model | session or explicit scope |
| Visual state | owning module/controller | widget/module lifetime |
| Options | settings/options owner | profile/character/user scope |
| Economy/task truth | Canary | server-authoritative lifetime |

Every async callback is tied to an exact source object, owner generation or cancellable handle. Global relog flags and arbitrary time windows are not identity validation.

## 6. Legacy test evidence

Use the existing test foundation under `tests/**`; do not create a parallel legacy harness.

| Change | Required evidence |
|---|---|
| Lua lifecycle | syntax, focused test, repeated init/terminate/login/logout |
| OTUI/layout | parse/load, interaction and relevant resolutions |
| C++ core | focused tests plus required Windows build matrix |
| Protocol | framed positive/malformed/truncated fixtures, gates and exact Canary pair |
| Authentication | PKCE/callback/Gateway/session positive and replay/fallback negatives |
| Assets/updater | hashes, paths, selection, rollback and clean install |
| Performance | before/after measurements and cancellation/UI-thread behavior |

Compilation proves build compatibility, not runtime/server compatibility.

## 7. Relationship to the Rust client

The legacy client may provide audited evidence such as:

- required observable behavior;
- exact Canary producer/consumer mappings;
- synthetic fixture semantics;
- legal asset metadata;
- benchmark scenario definitions;
- lifecycle regression cases.

It may not provide runtime linkage, copied architecture, Lua/OTUI compatibility requirements or unverified/proprietary content.
