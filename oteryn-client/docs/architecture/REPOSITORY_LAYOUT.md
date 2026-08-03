# Oteryn Client Repository Layout

Status: normative active layout. Directories are created only when their accepted workstream starts.

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
│   ├── renderer-resource/
│   ├── ui-core/
│   ├── ui-runtime/
│   ├── input/
│   ├── input-platform/
│   ├── audio/
│   ├── asset-types/
│   ├── asset-runtime/
│   ├── asset-decode/
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
│   │   └── auth/
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
| `app-runtime` | generation-checked top-level entry state, owned cancellable/joined worker composition, typed progress/result routing and terminal cleanup | packet parsing, concrete widgets, raw sockets, producer DTOs or credentials outside the one-shot lifecycle |
| `platform` | strict bounded producer-facing HTTP/DTO boundaries and concrete reviewed OS/network adapters | browser transaction state, game rules, feature state, Canary wire, UI or deployment defaults |
| `identity` | CSPRNG PKCE transaction, pre-bound loopback callback, system-browser launch and generation-safe Identity/ticket/Gateway orchestration | passwords, substitute ENTRY contracts, character/game mutation, Canary wire, UI or persistence |
| `account-session` | authenticated account lifetime | live game connection |
| `world-directory` | characters, worlds, gameplay-channel descriptors | physical node assumptions |
| `game-session` | one live game session lifecycle | wire-format details |
| `transport` | one bounded non-reconnecting TCP connection, explicit timeouts/cancellation, directional frame limits, partial I/O and stable transport errors | DNS policy, credentials, protocol constants, reconnect loops, domain events or UI |
| `protocol-core` | bounded checked binary reader/writer helpers, trailing-data policy and closed protocol errors | Canary/Oteryn constants, sockets, credentials or domain ownership |
| `protocol-canary` | exact-version Canary adapters consuming shared lifecycle/domain contracts; W7 currently exposes evidence-gated Current admission outcomes only | raw application sockets/credentials, UI, domain storage, gameplay/map decoding, reconnect or compatibility claims without exact evidence |
| `protocol-oteryn` | native Oteryn encode/decode | UI and domain storage |
| `game-domain` | typed commands, events, identifiers and pure rules | sockets, GPU, widgets |
| `game-simulation` | mutable session state and deterministic systems | rendering backend |
| `world-storage` | chunks, entities, arenas and spatial queries | protocol logic |
| `render-types` | backend-neutral extracted render data | game mutation |
| `renderer` | deterministic surface lifecycle, GPU instance/surface/adapter/device/queue ownership and bounded presentation | feature business logic, game rendering, UI or protocol |
| `renderer-resource` | checked immutable RGBA8 upload plans, process/device/asset-generation-fenced handles and bounded deterministic cache lifecycle | world state, draw ordering, protocol, input, UI, filesystem acquisition or CPU media decode |
| `ui-core` | primitives, layout, input routing, accessibility | inventory/chat specifics |
| `ui-runtime` | view-model binding, panel registry, persistence | protocol bytes |
| `input` | framework-neutral normalized physical events, contexts, bindings and semantic actions | native windowing types, global hooks, background capture or direct socket writes |
| `input-platform` | bounded Windows/winit physical-event normalization into the merged `input` contract | product keymaps, gameplay commands, UI actions, native identifier retention, global hooks or application composition |
| `audio` | devices, mixing and voices | game authority |
| `asset-types` | IDs, pack schemas and metadata | filesystem policy |
| `asset-runtime` | verified pack mounting and streaming | source conversion |
| `asset-decode` | checked synthetic-v1 RGBA8 CPU normalization from generation-fenced runtime handles into immutable owned bytes | filesystem paths, loose-file or production import, GPU upload, renderer caches, network, application composition or asset rights decisions |
| `settings` | typed schemas, scopes and migrations | credentials |
| `diagnostics` | metrics, tracing, redaction and replay hooks | authoritative game state |
| `extension-api` | stable capability-limited guest ABI | host implementation details |
| `extension-host` | WASM runtime, quotas and capability enforcement | native plugin loading |

`test-support` is physically under `crates/` because it is a reusable library package, but it declares architecture category `tool`. It may consume reviewed lower contracts for tests and must never become a runtime service locator.

The W7 Identity implementation keeps producer-specific DTOs inside `platform`. `identity` consumes that boundary plus the merged `account-session`, `world-directory` and `game-session` contracts. Raw OAuth, ticket and Gateway values never become new public domain types. The synchronous service is designed to run on an application-owned worker thread; it does not own a runtime thread or async executor.

The W7 Canary entry implementation keeps generic bounded TCP ownership in `transport`, generic checked binary helpers in `protocol-core`, and exact source facts/outcome mapping in `protocol-canary`. It consumes the merged `game-session` and `world-directory` contracts; the production Current wire path is disabled before network and credential handoff until approved transcript/RSA/deployment evidence exists. Synthetic fixtures are deliberately not Canary bytes.

`apps/client` is the concrete `app` package. It preserves deterministic shell state and the single `oteryn-renderer` surface owner on the main thread, and now composes W7 technical login through typed `winit` user events. Browser, callback, HTTP and admission execute only in application-owned workers; explicit environment configuration is opt-in and contains no credentials or production defaults. Game/domain rendering, feature UI, assets and persistence remain absent.

The W7 application runtime consumes the exact merged Identity and Canary interfaces plus producer-owned ENTRY lifecycle. It owns no replacement transport, protocol or session contract. The integration-test package composes original fake browser/listener/HTTP/admission services and cannot establish real Canary or deployment compatibility.

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

identity
├── platform
├── account-session
├── world-directory
├── game-session
└── foundation

platform
├── account-session
├── world-directory
├── game-session
└── foundation

game-domain / simulation / world-storage / render-types
└── foundation

protocol-canary
├── transport
├── protocol-core
├── game-session/world-directory entry contracts
└── foundation when a generic primitive is required

protocol-oteryn
├── protocol-core
├── game-domain contracts
└── foundation when a generic primitive is required

asset-decode
├── asset-runtime
└── asset-types

renderer
├── render-types
├── asset-runtime
├── platform/GPU dependencies
└── foundation when a generic primitive is required

renderer-resource
├── asset-decode
├── asset-runtime
└── foundation

input-platform
└── input

test-support (tool category)
├── diagnostics
└── foundation

foundation
└── Rust standard library and separately reviewed non-product dependencies only
```

`foundation` must not depend on application, platform, domain, protocol, renderer, UI, assets, diagnostics or feature crates. `game-domain`, `world-storage` and `render-types` must remain usable in tests without launching a window, GPU, network or async runtime. `test-support` may compose lower contracts only for deterministic tests and must not be linked as a product service. `identity` may depend on the strict `platform` producer boundary and merged ENTRY contracts, but those lower crates must never depend back on Identity. The current `apps/client` shell depends on foundation/diagnostics, the exact windowing library and the bounded `renderer` crate for concrete Windows composition. Renderer depends only on foundation plus its exact GPU dependencies and owns no feature, protocol, asset or UI service. `renderer-resource` is a backend-neutral renderer-category producer over `asset-decode`, `asset-runtime` and foundation; it owns no device, world or draw policy. `input-platform` is an input-category producer over the merged framework-neutral `input` contract and owns no product keymap, command, UI action or application lifecycle. `asset-decode` is a dedicated bounded decode category and depends only on the merged asset runtime and schema crates in production; its compiler dependency is test-only.

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
- W7 Identity fake browser/listener/HTTP and security negatives live in `tests/security/auth/`;
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
5. account/directory/game-entry contracts and bounded Identity/Platform bootstrap;
6. Canary adapter and minimum playable connection;
7. first-party features;
8. launcher/updater and release hardening;
9. optional extension host.
