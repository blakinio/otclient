# Legacy OTClient Workstreams

Status: maintained routing for the existing C++/Lua/OTUI client  
Last reviewed: 2026-07-26

This document applies only to existing legacy paths. The target Rust-client workstreams are under `oteryn-client/docs/agents/WORKSTREAMS.md`.

Before editing, inspect current `main`, all open PRs, active task records, the module catalogue, exact owner source/tests and cross-repository contracts.

## WS-L00 — Repository governance and Windows CI

Owns:

- root/legacy agent rules and task coordination;
- required-check graph;
- CMake/Visual Studio presets and Windows packaging policy;
- dependency/action pinning and minimal permissions.

Typical paths:

```text
AGENTS.md
docs/agents/**
.github/workflows/**
CMakePresets.json
cmake/**
vc18/**
```

Boundary: do not combine governance/CI changes with feature behavior. Do not weaken checks to merge.

## WS-L01 — Oteryn Identity and game-session handoff

Owns:

- system-browser Authorization Code + PKCE;
- loopback callback;
- Platform ticket and Gateway exchange;
- authoritative world routing;
- one-shot `GameSessionKey` lifecycle;
- replay/fallback/stale-callback/reconnect negatives.

Typical paths:

```text
modules/client_entergame/oteryn_identity*.lua
modules/client_entergame/oteryn_session_guard.lua
modules/client_entergame/** auth integration
src/framework/net/server.*
src/framework/util/crypt.*
init.lua
tests/**/auth*
docs/agents/CROSS_REPO_CONTRACTS.md
```

Inspect neighboring `src/client/game.*`, `protocolgame*`, character/world-login flow, Platform contract and selected Canary adapter.

Hard stops: no password fallback, no long-lived token exposure to general Lua, no production claim without exact Canary E2E.

## WS-L02 — Enter-game and character-list presentation

Owns login shell, character list layout/status/errors, destroy/recreate/relogin lifecycle and responsive presentation.

Typical paths:

```text
modules/client_entergame/*.lua
modules/client_entergame/*.otui
modules/client_entergame/*.otml
data/images/ui/oteryn/enter_game/**
data/styles/oteryn/**
```

Boundary: reuse WS-L01 auth APIs; presentation never implements a second OAuth/ticket flow. Preserve legacy mode unless a deliberate migration removes it.

## WS-L03 — Main interface, skin and layout

Owns viewport composition, top/bottom panels, sidebars, status, console/action-bar placement, palette/typography/widget states and layout persistence.

Typical paths:

```text
modules/game_interface/**
modules/client_topmenu/**
modules/game_console/**
modules/game_inventory/**
modules/game_minimap/**
data/images/ui/oteryn/**
data/styles/oteryn/**
```

Boundary: do not rewrite rendering for skin work; framework changes require a proven missing primitive. Use original/licensed art and validate relevant Windows resolutions/DPI.

## WS-L04 — Options, controls and configuration

Owns metadata/orchestration, basic/advanced grouping, persistence, schema migration, safe import/export and option-facing policy.

Typical paths:

```text
modules/client_options/**
modules/game_hotkeys/** or current owner
modules/game_interface/** option hooks
modules/game_console/** option hooks
modules/game_actionbar/** option hooks
settings/config helpers
tests/lua/** option contracts
```

Boundary: option owner defines metadata; feature owner defines real behavior. No inert controls. Imported state excludes secrets and validates schema/size.

## WS-L05 — Action bars, hotkeys and cooldown lifecycle

Owns action bars/persistence, action types/hotkey resolution, spell/group/multi-use cooldown state, relog restoration and overlay lifecycle.

Typical paths:

```text
modules/game_actionbar/**
modules/game_hotkeys/** or current owner
src/client/protocolgameparse.cpp affected cooldown region
src/client/game.* callbacks
tests/lua/** actionbar tests
tests/unit/client/** protocol fixtures
```

Protocol cooldown truth exists independently of visible bars/options. Session reset is explicit; module UI consumes rather than defines packet state.

## WS-L06 — Canary protocol compatibility

Owns exact supported modern and selected legacy protocol behavior, feature/version gates and parser/output compatibility.

Typical paths:

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

Every packet change requires a shared coordination contract, exact Canary producer path/commit, field order/width/signedness/optionals, gates, positive/malformed/truncated fixtures and unsupported-pair behavior. Parser compilation alone is not acceptance.

## WS-L07 — Server-driven features

Owns one bounded server-driven feature at a time, such as Taskboard, including exact payload models, parser/callback surface, controller/UI, original assets and server errors.

Typical paths depend on the feature:

```text
src/client/** exact parser/definitions
modules/game_features/**
modules/game_<feature>/**
data/images/ui/oteryn/<feature>/**
data/styles/oteryn/**
tests/unit/client/protocol/**
tests/lua/modules/**
docs/agents/CROSS_REPO_CONTRACTS.md
```

Implementation order:

1. shared contract and producer evidence;
2. fixtures;
3. parser/callback completion;
4. read-only model/UI;
5. actions/errors;
6. persistence/integration;
7. exact-version E2E and original art acceptance.

The server owns prices, progress, eligibility, rewards and other authoritative values.

## WS-L08 — Assets, updater and packaging

Owns version-correct acquisition, strict hashes, staging/final paths, cancellation/rollback and Windows distribution.

Typical paths:

```text
modules/client_assets/**
legacy updater services
src/framework/core/resourcemanager.*
data/things/**
data/sounds/**
bin/**
docs/client-assets-auto-install.md
```

Boundary: no weakened TLS/hash validation, no runtime staging/cache source, no proprietary asset commit without rights, no UI-thread hashing/extraction without progress/cancellation.

## WS-L09 — Interaction and lifecycle defects

Owns narrow bugs in the actual feature owner, including containers/drop zones, input focus, mouse/keyboard behavior, use-with cleanup, battle-list identity and scheduled callback cleanup.

Do not create a generic interaction module unless multiple owners need a proven primitive.

Acceptance includes exact reproduction, focused deterministic tests where feasible, repeated init/terminate/login/logout/widget recreation and no unrelated control regressions.

## WS-L10 — Performance and diagnostics

Owns measured startup/render/UI/profiling issues, diagnostics policy and actionable redacted logs.

Typical paths:

```text
src/framework/**
src/client/**
affected modules
profiling/diagnostic settings
tests/performance or focused benchmarks
```

Measure before changing. Do not reduce correctness/security checks for speed. Expensive work needs cancellation/lifetime ownership. Logs exclude auth tokens, tickets, session keys and private paths.

## Shared legacy path ownership

### `src/client/protocolgameparse.cpp`

One active task owns the affected parser region. Adjacent opcode work coordinates rather than editing in parallel.

### `modules/client_entergame/**`

Authentication/session and presentation are separate ownership boundaries. Inspect both active task/PR sets.

### `modules/game_interface/**`

Composition infrastructure. Feature-specific state belongs in the feature module; expose narrow panel/docking APIs.

### `modules/client_options/**`

Options owns metadata/orchestration. Features own apply behavior. Agree on IDs and migrations before parallel edits.

### `data/images/**` and `data/styles/**`

Declare namespace ownership and provenance. Never silently replace another feature's resources.

### `tests/support/**`

Shared legacy infrastructure only. New helpers require broad utility/catalogue review; feature tests belong near the owning area.

### Workflows/CMake/presets

Dedicated CI/build task ownership. Feature tasks do not opportunistically modify the matrix.

## Package sizing

Good:

- restore one lifecycle behavior through relog with tests;
- safely recreate one character-list presentation;
- normalize one protocol field family under an exact gate;
- add parser fixtures separately from feature UI;
- add one option slice and migration;
- apply one visual skin slice without changing behavior.

Bad:

- implement all options/features in one PR;
- merge a broad protocol-version delta blindly;
- protocol + UI + assets + updater in one package;
- renderer refactor mixed with skin work;
- CI weakening bundled with a feature.

Split when a package crosses independent trust boundaries, protocol contracts or rollback units.

## Required legacy task evidence

Every task declares `owned_paths`, `modules_touched`, reuse, dependencies, blockers and cross-repository tasks.

Protocol/auth/assets tasks also record exact producer/consumer, gate, supported/unsupported pairs, failure behavior, fixtures/runtime evidence and rollout order.

Before readiness: inspect complete diff/files, verify ownership, preserve Oteryn security invariants, confirm exact Canary pairing, run required Windows checks on exact head, update task/contracts/catalogue/docs and leave one concrete next action.
