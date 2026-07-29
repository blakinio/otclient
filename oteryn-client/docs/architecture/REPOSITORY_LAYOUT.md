# Oteryn Client Repository Layout

Status: normative planned layout. Directories are created only when their workstream starts after the foundation audit.

## 1. Coexistence in the current repository

```text
otclient/
├── oteryn-client/                 # new Rust product
├── src/                           # legacy C++ client
├── modules/                       # legacy Lua/OTUI features
├── mods/                          # legacy optional scripts
├── data/                          # legacy runtime assets
├── tests/                         # legacy client tests
└── docs/agents/                   # repository-wide coordination
```

The legacy tree is not moved during greenfield development. Moving or retiring it requires a later dedicated migration task.

## 2. Planned Rust tree

```text
oteryn-client/
├── AGENTS.md
├── README.md
├── Cargo.toml
├── Cargo.lock
├── rust-toolchain.toml
├── rustfmt.toml
├── deny.toml
├── apps/
│   ├── client/
│   │   ├── Cargo.toml
│   │   └── src/
│   │       ├── lib.rs
│   │       └── main.rs
│   └── launcher/
│       ├── Cargo.toml
│       └── src/main.rs
├── crates/
│   ├── foundation/
│   ├── test-support/
│   ├── app-runtime/
│   ├── platform/
│   ├── identity/
│   ├── account-session/
│   ├── world-directory/
│   ├── game-session/
│   ├── transport/
│   ├── protocol-core/
│   ├── protocol-canary/
│   ├── protocol-oteryn/
│   ├── game-domain/
│   ├── game-simulation/
│   ├── world-storage/
│   ├── render-types/
│   ├── renderer/
│   ├── ui-core/
│   ├── ui-runtime/
│   ├── input/
│   ├── audio/
│   ├── asset-types/
│   ├── asset-runtime/
│   ├── settings/
│   ├── diagnostics/
│   ├── extension-api/
│   └── extension-host/
├── features/
│   ├── enter-game/
│   ├── character-selection/
│   ├── channel-selection/
│   ├── game-interface/
│   ├── inventory/
│   ├── containers/
│   ├── chat/
│   ├── battle-list/
│   ├── minimap/
│   ├── action-bars/
│   ├── market/
│   └── settings-ui/
├── tools/
│   ├── asset-compiler/
│   ├── protocol-recorder/
│   ├── replay-runner/
│   ├── benchmark-runner/
│   └── architecture-check/
├── contracts/
│   ├── domain/
│   ├── canary/
│   └── oteryn/
├── assets/
│   ├── source/
│   ├── manifests/
│   ├── schemas/
│   └── test-fixtures/
├── tests/
│   ├── integration/
│   ├── protocol/
│   ├── ui/
│   ├── renderer/
│   ├── security/
│   └── fixtures/
├── benches/
│   ├── scenes/
│   ├── domain/
│   ├── renderer/
│   └── assets/
└── docs/
    ├── architecture/
    ├── agents/
    ├── audits/
    ├── compatibility/
    ├── performance/
    └── operations/
```

## 3. Crate responsibilities

| Crate | Owns | Must not own |
|---|---|---|
| `foundation` | generic technical generations, monotonic time, explicit cancellation and primitive-specific errors | product lifecycle policy, domain IDs, protocol, platform services, async runtime or global event bus |
| `test-support` | deterministic test-owned timelines/context and classified diagnostic-event fixtures using merged lower contracts | another clock abstraction, sleep/scheduler/executor, global fixture registry, product services or external fixture loading |
| `app-runtime` | top-level state machine, service composition, error routing | packet parsing, concrete widgets |
| `platform` | OS abstractions | game rules or feature state |
| `identity` | PKCE orchestration and safe callback boundary | character/game state |
| `account-session` | authenticated account lifetime | live game connection |
| `world-directory` | characters, worlds, gameplay-channel descriptors | physical node assumptions |
| `game-session` | one live game session lifecycle | wire-format details |
| `transport` | bytes, connection health, framing primitives | domain events or UI |
| `protocol-core` | adapter interfaces and validated shared types | Canary/Oteryn constants |
| `protocol-canary` | exact Canary encode/decode | UI and domain storage |
| `protocol-oteryn` | native Oteryn encode/decode | UI and domain storage |
| `game-domain` | typed commands, events, identifiers and pure rules | sockets, GPU, widgets |
| `game-simulation` | mutable session state and deterministic systems | rendering backend |
| `world-storage` | chunks, entities, arenas and spatial queries | protocol logic |
| `render-types` | backend-neutral extracted render data | game mutation |
| `renderer` | deterministic surface lifecycle, GPU instance/surface/adapter/device/queue ownership and bounded presentation | feature business logic, game rendering, UI or protocol |
| `ui-core` | primitives, layout, input routing, accessibility | inventory/chat specifics |
| `ui-runtime` | view-model binding, panel registry, persistence | protocol bytes |
| `input` | devices, bindings, contexts and semantic actions | direct socket writes |
| `audio` | devices, mixing and voices | game authority |
| `asset-types` | IDs, pack schemas and metadata | filesystem policy |
| `asset-runtime` | verified pack mounting and streaming | source conversion |
| `settings` | typed schemas, scopes and migrations | credentials |
| `diagnostics` | metrics, tracing, redaction and replay hooks | authoritative game state |
| `extension-api` | stable capability-limited guest ABI | host implementation details |
| `extension-host` | WASM runtime, quotas and capability enforcement | native plugin loading |

`test-support` is physically under `crates/` because it is a reusable library package, but it declares architecture category `tool`. It may consume reviewed lower contracts for tests and must never become a runtime service locator.

`apps/client` is the concrete `app` package. Its current W5 boundary composes deterministic shell state with the single `oteryn-renderer` surface owner on the main thread. Protocol, game/domain rendering, feature composition, assets, UI and persistence remain absent.

## 4. Feature crate contract

Each first-party feature follows a predictable structure:

```text
features/inventory/
├── Cargo.toml
├── src/
│   ├── lib.rs
│   ├── model.rs
│   ├── controller.rs
│   ├── view_model.rs
│   ├── commands.rs
│   └── registration.rs
└── tests/
```

A feature may depend on domain/application/UI contracts. It must not depend on protocol adapters, renderer internals or another feature's private modules.

Feature-to-feature integration uses published application contracts. Circular feature dependencies are forbidden.

## 5. Dependency direction

```text
apps
├── app-runtime
├── first-party features
└── concrete platform/renderer/protocol composition

features
├── application contracts
├── game-domain read/command APIs
├── ui-runtime/ui-core
└── foundation when a generic primitive is required

application services
├── game-domain
├── protocol-core traits
├── engine primitives
└── foundation

game-domain / simulation / world-storage / render-types
└── foundation

protocol-canary / protocol-oteryn
├── protocol-core
├── game-domain contracts
└── foundation when a generic primitive is required

renderer
├── render-types
├── asset-runtime
├── platform/GPU dependencies
└── foundation when a generic primitive is required

test-support (tool category)
├── diagnostics
└── foundation

foundation
└── Rust standard library and separately reviewed non-product dependencies only
```

`foundation` must not depend on application, platform, domain, protocol, renderer, UI, assets, diagnostics or feature crates. `game-domain`, `world-storage` and `render-types` must remain usable in tests without launching a window, GPU, network or async runtime. `test-support` may compose lower contracts only for deterministic tests and must not be linked as a product service. The current `apps/client` shell depends on foundation/diagnostics, the exact windowing library and the bounded `renderer` crate for concrete Windows composition. Renderer depends only on foundation plus its exact GPU dependencies and owns no feature, protocol, asset or UI service.

## 6. Cargo workspace policy

After the audit gate:

- use one workspace-level dependency policy;
- pin the Rust toolchain through `rust-toolchain.toml`;
- commit `Cargo.lock` for applications;
- deny unknown licenses and duplicate/risky dependencies through `cargo-deny` policy;
- use workspace lints and forbid unsafe code by default;
- allow `unsafe` only in explicitly reviewed low-level modules with documented invariants;
- keep default feature sets minimal and deterministic;
- avoid giant facade crates that hide dependency direction.

Crate names use the `oteryn-` package prefix while directory names remain concise, for example directory `game-domain` and package `oteryn-game-domain`.

## 7. Contracts

`contracts/` stores source-of-truth schemas and compatibility records, not generated runtime business logic.

```text
contracts/domain/      stable event/command schema documentation
contracts/canary/      exact supported versions, packet evidence and fixtures
contracts/oteryn/      future native protocol/session contracts
```

Generated code belongs in the owning crate's build output or generated-source path and must be reproducible.

## 8. Test placement

- crate-local unit/property tests stay near the source;
- reusable deterministic Rust test helpers live in `crates/test-support/` and remain test-owned;
- cross-crate integration tests live under top-level `tests/`;
- protocol fixtures are versioned and provenance-documented;
- renderer scenes and expected metrics live under `benches/scenes/`;
- UI snapshot/reference data contains only original or licensed material;
- security negative cases are first-class tests, not comments.

## 9. Documentation ownership

- stable architecture: `docs/architecture/`;
- durable decisions: `docs/architecture/decisions/`;
- audit evidence: `docs/audits/`;
- current agent program and prompts: `docs/agents/`;
- exact client/server pairs: `docs/compatibility/`;
- measured benchmark results: `docs/performance/`.

A task must update the nearest owning document rather than adding a competing document with similar scope.

## 10. Creation sequence

Do not create all directories empty. Create only the slice required by the active milestone:

1. audit documents and fixtures inventory;
2. workspace/toolchain and architecture check;
3. foundation and deterministic test-support crates, then application shell;
4. renderer vertical slice;
5. domain and synthetic replay slice;
6. Canary adapter and minimum playable connection;
7. first-party features;
8. launcher/updater and release hardening;
9. optional extension host.
