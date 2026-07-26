# Oteryn Rust Client Workstreams

Status: normative routing guide. Live tasks and open PRs remain authoritative.

## WS-R00 — Foundation audit

Owns:

- `docs/audits/**`;
- verified capability/feature/protocol/asset inventories;
- baseline benchmark/replay scene definitions;
- audit recommendations and blockers.

Does not own production crates. This is the first required workstream.

Acceptance: every conclusion links evidence or is marked unknown; no copied proprietary assets; one exact next implementation package is recommended.

## WS-R01 — Workspace, governance and CI

Planned paths:

```text
Cargo.toml
Cargo.lock
rust-toolchain.toml
rustfmt.toml
deny.toml
tools/architecture-check/**
CI paths dedicated to oteryn-client
```

Owns toolchain, workspace metadata, lints, dependency/license/security policy, architecture-edge checks and Windows Rust CI.

Boundary: no gameplay or renderer implementation.

## WS-R02 — Platform and application runtime

Planned paths:

```text
apps/client/**
crates/app-runtime/**
crates/platform/**
```

Owns Windows process/window/event integration, application state machine, cancellation, startup/shutdown and service composition.

Boundary: does not parse protocols or own feature UI.

## WS-R03 — Identity, account session and directory

Planned paths:

```text
crates/identity/**
crates/account-session/**
crates/world-directory/**
features/enter-game/**
features/character-selection/**
features/channel-selection/**
tests/security/auth*
```

Owns PKCE, account lifetime, characters/worlds/gameplay-channel models, selection flow and one-shot ticket acquisition.

Boundary: no main-password fallback, no game protocol implementation, no physical node assumptions.

## WS-R04 — Domain, simulation and world storage

Planned paths:

```text
crates/game-domain/**
crates/game-simulation/**
crates/world-storage/**
crates/render-types/**
tests/fixtures/domain/**
```

Owns typed IDs, commands/events, deterministic state, chunks/entities and render extraction contracts.

High-contention interfaces: `GameEvent`, `GameCommand`, snapshot structures and entity/chunk IDs. Only one active task may change each shared contract unless explicitly coordinated.

## WS-R05 — Transport and protocol core

Planned paths:

```text
crates/transport/**
crates/protocol-core/**
contracts/domain/**
```

Owns transport abstractions, adapter trait, common bounded validation types and session-independent protocol contracts.

Boundary: does not own Canary/Oteryn message constants.

## WS-R06 — Canary adapter

Planned paths:

```text
crates/protocol-canary/**
contracts/canary/**
tests/protocol/canary/**
```

Owns exact audit-selected Canary compatibility, golden/malformed fixtures and version/capability matrix.

Requires shared cross-repository coordination and exact producer evidence. No feature UI changes in adapter PRs.

## WS-R07 — Native Oteryn adapter

Planned paths:

```text
crates/protocol-oteryn/**
contracts/oteryn/**
tests/protocol/oteryn/**
```

Owns future native Oteryn transport/message/session mapping after the cross-repository contract and ADR exist.

Boundary: does not redesign domain/UI merely to mirror server schema.

## WS-R08 — Renderer

Planned paths:

```text
crates/renderer/**
benches/renderer/**
benches/scenes/**
tests/renderer/**
```

Owns `wgpu`, render graph, GPU resources, sprite/text/effect/UI passes, batching, culling, device recovery and renderer metrics.

Boundary: consumes `render-types`; does not mutate game state or depend on features.

## WS-R09 — Assets and tooling

Planned paths:

```text
crates/asset-types/**
crates/asset-runtime/**
tools/asset-compiler/**
assets/**
benches/assets/**
```

Owns normalized asset model, pack format, compiler, verification, streaming and budgets.

High-risk: licenses, signatures, hashes, archives and path handling. Importers remain build tools, not runtime engine dependencies.

## WS-R10 — UI core and runtime

Planned paths:

```text
crates/ui-core/**
crates/ui-runtime/**
tests/ui/**
```

Owns layout, widgets, focus, accessibility, text integration, docking, view-model binding and panel/action registries.

Boundary: no concrete inventory/chat/market business state in core crates.

## WS-R11 — Input and settings

Planned paths:

```text
crates/input/**
crates/settings/**
features/settings-ui/**
```

Owns devices, semantic actions, contexts, bindings, typed settings, scopes and migrations.

Boundary: gameplay actions go through application/domain commands, not sockets.

## WS-R12 — Audio

Planned paths:

```text
crates/audio/**
tests/audio/**
```

Owns devices, voice management, mixing, positional/UI categories and real-time-safe callback behavior.

Boundary: decoding/source conversion remains asset tooling/runtime workers.

## WS-R13 — First-party game features

One task/PR per narrow observable feature slice under `features/**`.

Each feature owns controller/view-model/UI/persistence for its domain but reuses shared domain/UI/application contracts. Feature crates do not depend directly on protocol adapters.

Shared game-interface/docking composition requires a stable WS-R10 API before parallel feature UI work.

## WS-R14 — Diagnostics, replay and benchmarks

Planned paths:

```text
crates/diagnostics/**
tools/protocol-recorder/**
tools/replay-runner/**
tools/benchmark-runner/**
benches/**
docs/performance/**
```

Owns tracing/redaction, metrics, sanitized replay, benchmark orchestration and support bundles.

Boundary: diagnostics cannot become required for correctness and cannot retain secrets.

## WS-R15 — Launcher, updater and packaging

Planned paths:

```text
apps/launcher/**
crates/updater-* if introduced
docs/operations/**
packaging/ or approved equivalent
```

Owns signed manifests, download/staging, atomic activation, rollback, clean install, repair and Windows packaging.

This is a separate trust boundary and high-risk workstream.

## WS-R16 — Extension platform

Planned paths:

```text
crates/extension-api/**
crates/extension-host/**
tests/security/extensions/**
```

Owns versioned WASM ABI, capabilities, quotas and host integration after the playable core.

Native dynamic plugins are out of scope.

## Shared path rules

### Domain contracts

One owner for affected events/commands/IDs at a time. Protocol and feature agents consume a reviewed version rather than editing adjacent shared contracts in parallel.

### UI registries

WS-R10 owns registry primitives. Feature work owns descriptors and surfaces. Do not add feature-specific behavior to `ui-core`.

### Asset schemas

WS-R09 owns format/schema. Renderer/features propose requirements through review rather than independently changing the pack model.

### Cargo workspace and CI

WS-R01 owns manifests, workspace dependency policy and Rust CI. Feature agents do not weaken lints/checks to merge.

### Cross-repository contracts

Protocol, identity, routing, gameplay-channel, identifier and asset changes require shared coordination IDs and exact producer/consumer evidence.

## Work package sizing

Good packages:

- add typed identifier crate and property tests;
- render one synthetic instanced map scene with metrics;
- parse one verified Canary message family with malformed fixtures;
- implement character/channel selection against a fake directory;
- add one UI virtualization primitive;
- compile and mount one synthetic signed asset pack.

Bad packages:

- bootstrap every crate at once;
- implement the complete protocol in one PR;
- renderer + UI skin + asset conversion together;
- copy the legacy client architecture into Rust;
- add all game features before a playable vertical slice;
- change client and server contracts without coordinated tasks.

## Required task metadata

Each Rust-client task declares:

```yaml
workstream:
owned_paths:
crates_touched:
features_touched:
contracts_touched:
reuses:
depends_on:
blocks:
cross_repo_tasks:
performance_evidence:
security_evidence:
```

The root task template remains mandatory; these fields extend it.
