# Oteryn Client Workstream Routing

Status: repository-wide routing index  
Last reviewed: 2026-07-26

## 1. Choose the correct track

### Greenfield Rust client

Any new product architecture, Rust engine, renderer, UI, protocol adapter, asset pack, launcher or first-party feature belongs under:

```text
oteryn-client/**
```

Read:

- `oteryn-client/AGENTS.md`;
- `oteryn-client/docs/architecture/**`;
- `oteryn-client/docs/agents/PROGRAM.md`;
- `oteryn-client/docs/agents/WORKSTREAMS.md`;
- `oteryn-client/docs/agents/AUDIT_PLAN.md`.

The foundation audit is the first required workstream. Production Rust workspace bootstrap is blocked until that gate is accepted.

### Legacy C++/Lua OTClient

Existing maintenance, open PR completion, behavior fixes and comparison evidence remain under:

```text
src/**
modules/**
mods/**
data/**
tests/**
CMake*/cmake/vc18
```

Legacy work follows the current owner module, exact Canary contract and root repository validation policy. It must not define the target architecture or add dependencies from `oteryn-client/` to legacy runtime code.

## 2. Greenfield workstreams

The complete ownership matrix is `oteryn-client/docs/agents/WORKSTREAMS.md`:

```text
WS-R00 foundation audit
WS-R01 workspace/governance/CI
WS-R02 platform/application runtime
WS-R03 Identity/account/directory and gameplay-channel selection
WS-R04 domain/simulation/world storage
WS-R05 transport/protocol core
WS-R06 Canary adapter
WS-R07 native Oteryn adapter
WS-R08 renderer
WS-R09 assets/tooling
WS-R10 UI core/runtime
WS-R11 input/settings
WS-R12 audio
WS-R13 first-party features
WS-R14 diagnostics/replay/benchmarks
WS-R15 launcher/updater/packaging
WS-R16 WebAssembly extension platform
```

Use that document for exact planned paths, boundaries and package sizing.

## 3. Legacy high-contention paths

Until the legacy client is retired, preserve existing ownership discipline:

- `src/client/protocolgameparse.cpp`: one active task per affected parser region;
- `modules/client_entergame/**`: separate presentation from authentication/session work;
- `modules/game_interface/**`: composition infrastructure, not a general feature-state owner;
- `modules/client_options/**`: option metadata/orchestration separate from feature behavior;
- `data/images/**`, `data/styles/**`: explicit namespace and provenance ownership;
- `.github/workflows/**`, CMake and presets: dedicated CI/build ownership.

Open PR and active task state is authoritative.

## 4. Shared cross-repository contracts

Identity, game tickets, character/world/gameplay-channel routing, protocol messages, identifiers, feature capabilities and asset compatibility require shared coordination IDs and exact producer/consumer evidence.

Canary is the first compatibility target for the Rust client. Oteryn is the target ecosystem. Neither wire format may leak into the game domain or feature UI.

## 5. Package sizing

Good:

- one audit output family;
- one Rust foundation crate and its tests;
- one synthetic renderer slice;
- one verified Canary message family;
- one first-party feature slice;
- one legacy behavior fix in its existing owner.

Bad:

- bootstrap every Rust crate at once;
- mix legacy fixes with greenfield architecture;
- protocol + feature UI + assets in one PR;
- copy legacy modules into Rust;
- weaken CI or security to unblock a feature.

## 6. Required task routing metadata

Every task identifies:

- track: `greenfield-rust` or `legacy-client`;
- workstream/owner;
- exact paths and public contracts;
- dependencies, blockers and overlaps;
- cross-repository tasks;
- validation and evidence requirements.

A task crossing both tracks should normally be split into independent audit/contract and implementation packages.
