# Rust Workspace Operations

Status: active workspace policy after WS-R01 bootstrap  
Required compiled platform: Windows x86-64 MSVC

## Scope

The workspace contains six bounded members:

```text
apps/client
crates/foundation
crates/renderer
crates/diagnostics
crates/test-support
tools/architecture-check
```

`oteryn-client` is the bounded Windows application shell and composes one main-thread renderer surface owner. `oteryn-renderer` owns deterministic surface lifecycle plus the exact DX12 instance/surface/adapter/device/queue and one constant clear/present path. `oteryn-foundation` provides standard-library-only technical generations, monotonic time, explicit cancellation ownership and primitive-specific errors. `oteryn-diagnostics` provides bounded structured and redacted diagnostic contracts. `oteryn-test-support` is a test-only `tool` crate composing those merged contracts into deterministic timelines, technical contexts and classified event fixtures. `oteryn-architecture-check` validates workspace metadata and declared dependency categories. Protocol stack, domain/game rendering, product UI, asset runtime and extension host remain absent.

Product crates are created only by the first work package that delivers observable behavior in their owning workstream. Empty placeholder crates are prohibited.

## Toolchain

`rust-toolchain.toml` pins Rust `1.94.0`, released through the stable channel on 2026-07-02, with the minimal profile plus `clippy`, `rustfmt` and the `x86_64-pc-windows-msvc` target.

Policy:

- required CI uses the pinned toolchain;
- `Cargo.lock` is committed and required commands use `--locked` where supported;
- nightly-only production requirements need an evidence-backed ADR;
- changing the toolchain requires a focused task, release-note review and exact-head Windows validation;
- portability of source is not a compatibility claim for another platform.

## Normal commands

Run from `oteryn-client/`:

```text
cargo metadata --locked --format-version 1
cargo fmt --all --check
cargo clippy --workspace --all-targets --locked -- -D warnings
cargo test --workspace --all-targets --locked
cargo run --locked -p oteryn-architecture-check -- workspace .
cargo deny check
```

Local `cargo deny check` uses `deny.toml`. CI pins `EmbarkStudios/cargo-deny-action` at commit `3c6349835b2b7b196a839186cb8b78e02f7b5f25`, which contains cargo-deny `0.20.2`. Tool or action upgrades require current upstream release review and an exact immutable pin.

## Workspace package requirements

Every workspace package must:

- use the `oteryn-` package-name prefix;
- live under `oteryn-client/`;
- inherit workspace edition, Rust version, license/repository and lint policy where applicable;
- declare one architecture category:

```toml
[package.metadata.oteryn]
category = "foundation"
```

- use crates.io registry dependencies or reviewed workspace-local path dependencies only;
- avoid external git/path sources unless a later focused policy change explicitly approves them;
- avoid a dependency on legacy `src/`, `modules` or `mods` runtime code/content.

Known categories are defined by the architecture checker and follow the accepted architecture, including `app`, `foundation`, `tool`, `platform`, `game-domain`, protocol adapters, renderer/UI layers, assets, diagnostics and `feature`.

`foundation` is the bottom reusable category. It must not depend on application, platform, domain, protocol, renderer, UI, assets, diagnostics or feature crates. Lower product layers may depend on it only for generic primitives that do not encode product/server behavior.

`tool` packages may consume reviewed lower contracts for development/test/build purposes but must not become runtime service locators or bypass product dependency direction. The current `oteryn-test-support` tool depends only on `foundation` and `diagnostics`.

The current `app` package depends directly on foundation/diagnostics, exact `winit 0.30.13` and the Windows-only `oteryn-renderer` composition contract; `oteryn-test-support` is dev-only. GPU ownership remains inside `oteryn-renderer`; the app must not absorb protocol, feature, persistence or direct Win32 responsibilities.

Adding or changing a category is an architecture-policy change. Update the checker, synthetic positive/negative fixtures, architecture/workstream documentation and module catalogue in one focused PR.

## Architecture checker

Usage:

```text
cargo run --locked -p oteryn-architecture-check -- workspace .
cargo run --locked -p oteryn-architecture-check -- fixture tests/architecture-fixtures/valid_minimal_workspace.json
```

The workspace command runs locked Cargo metadata and validates:

- package naming and category metadata;
- workspace path containment;
- dependency source policy;
- workspace-local path dependency resolution;
- prohibited category edges;
- dependency cycles.

Stable rule codes:

| Code | Meaning |
|---|---|
| `E001_PACKAGE_NAME` | package does not use the `oteryn-` prefix |
| `E002_UNKNOWN_CATEGORY` | package category is not recognized |
| `E003_OUTSIDE_WORKSPACE` | package or path dependency escapes `oteryn-client/` |
| `E004_UNAPPROVED_SOURCE` | dependency uses an unapproved registry/git source |
| `E005_FORBIDDEN_EDGE` | category dependency violates architecture direction |
| `E006_DEPENDENCY_CYCLE` | workspace dependency graph contains a cycle |
| `E008_UNKNOWN_WORKSPACE_DEP` | workspace path dependency cannot be resolved |
| `E009_DUPLICATE_PACKAGE` | graph contains duplicate package names |

The checker intentionally validates metadata/graph policy only. It does not replace Cargo, Clippy, source review, security review, protocol tests or runtime validation.

## Synthetic fixtures

`tests/architecture-fixtures/` contains original metadata-only graphs:

- one valid minimal tool workspace;
- one valid lower-layer dependency on `foundation`;
- one invalid `foundation` dependency upward into a product layer;
- legacy path dependency;
- game-domain -> Canary adapter;
- renderer -> concrete feature;
- UI core -> concrete feature;
- dependency cycle;
- unapproved source dependency.

Fixtures contain no game source, protocol bytes, credentials or assets. New architecture rules require both a valid example and a focused invalid fixture.

## Foundation crate contract

`oteryn-foundation` is standard-library-only and owns:

- `ProcessGeneration`, `SessionGeneration` and `TaskGeneration` as distinct checked `u64` newtypes;
- `Moment`, `Deadline`, `MonotonicClock`, `SystemClock` and deterministic thread-safe `ManualClock`;
- `CancellationSource` as the unique cancellation authority and cloneable observation-only `CancellationToken`;
- closed `GenerationError` and `TimeError` enums containing no arbitrary external text.

Cancellation is always explicit. Dropping an observer has no effect; dropping an uncancelled source does not implicitly cancel its surviving tokens. The final source/token drop releases shared state and starts no background work.

The crate contains no Character/World/Channel identifiers, Identity/session implementation, async runtime, scheduler, executor, global event bus, hidden thread, network, GPU, UI, asset, tracing, serialization, FFI or legacy runtime dependency.

## Diagnostics crate contract

`oteryn-diagnostics` owns stable bounded diagnostic contracts only:

- severity, category and code values;
- reviewed static safe text and lower-snake-case field keys;
- explicit sensitive classifications redacted at creation without retaining input text;
- technical context using foundation moments/generations and a diagnostic correlation ID;
- at most 16 unique fields in deterministic insertion order.

It installs no global logger/subscriber or sink and performs no file, network, telemetry, crash-report, support-bundle, replay, async-runtime or product-service work.

## Deterministic test-support contract

`oteryn-test-support` is a test-only `tool` package and owns:

- `TestTimeline`, which directly owns/clones the shared `ManualClock`, advances or sets it explicitly and builds exact technical context;
- `DiagnosticEventFixture`, which validates reviewed static message/key literals and accepts only already-classified `DiagnosticValue` values;
- `TestSupportError`, which wraps only closed static-text and bounded-event failures.

It defines no second clock trait/implementation, wall-clock source, sleep, polling loop, timer wheel, async runtime, executor, scheduler, hidden production thread, global registry, environment mutation, logger/sink, product service or external fixture loader. Thread tests use explicit barriers only to prove shared manual-clock observation.

## Windows application-shell contract

`oteryn-client` currently owns only:

- deterministic `ShellState`, phase, command, error and window-snapshot contracts;
- bounded lifecycle diagnostics using reviewed diagnostics values;
- one main-thread `winit::ApplicationHandler` that creates one resizable window;
- one named one-shot proxy-wake thread joined after the event loop returns;
- explicit shell runtime-evidence blockers in `docs/research/windows-platform/W4_RUNTIME_EVIDENCE.md`.

It owns no GPU resources directly, direct Win32/FFI, unsafe code, async runtime, protocol, identity, networking, assets, audio, feature UI, persistence or updater. It composes `oteryn-renderer`, releases renderer resources before the window and routes fatal renderer errors through the existing close path. Compilation on a hosted Windows runner is not an interactive compatibility claim.

## Renderer surface contract

`oteryn-renderer` owns:

- typed `SurfaceState`, `SurfaceEvent`, `SurfaceDecision` and closed `RendererError` contracts keyed by `ProcessGeneration`;
- transactional CPU-side unconfigured/configured/suspended/lost/closing transitions, zero-size suspension, bounded recovery, checked counters and idempotent close;
- on Windows, one exact DX12 wgpu instance/surface/adapter/device/queue owner and one constant original clear/present path;
- one synchronous main-thread `pollster::block_on` bootstrap and event-driven redraw only.

It owns no game/map/entity rendering, assets, textures, shader modules or pipelines, render graph, UI, protocol, identity, network, audio, persistence, extension runtime, global singleton, background service, scheduler or new worker thread. Hosted Windows CI proves compilation and deterministic tests only; interactive presentation, real resize/minimize/suspend/resume, surface/device loss, driver/hardware and performance remain blocked in `docs/research/renderer/W5_RUNTIME_EVIDENCE.md`.

## Lint and unsafe policy

Workspace Rust policy:

- unsafe Rust is forbidden by default;
- standard Rust/Clippy warnings fail required CI;
- `unwrap`, `expect`, `panic`, `todo`, `unimplemented` and debug macros are denied by policy;
- exceptions require a narrow owning package, documented reason and tests rather than a workspace-wide allowance;
- external-input parsers need explicit bounded error handling in their later workstreams.

Workspace source contains no unsafe code or direct native/FFI dependency. The exact `wgpu` DX12 graph owns reviewed transitive platform bindings; application and renderer source do not call them directly.

## Supply-chain policy

`deny.toml` applies to the required Windows dependency target and currently:

- denies known advisories and yanked releases;
- denies wildcard dependencies;
- denies duplicate dependency versions except documented exact graph branches;
- permits the explicit reviewed license set only;
- denies unknown registries and git sources;
- permits crates.io as the external registry.

Do not broaden license/source policy merely to make CI green. Investigate the exact dependency and either reject it, replace it or update policy through a reviewed task with legal/security rationale.

The workspace pins `serde_json` for the architecture tool, exact `winit 0.30.13` for the Windows application shell, exact `wgpu 30.0.0` with defaults disabled plus `std`/`dx12`, and exact `pollster 1.0.1` for one synchronous main-thread bootstrap. `oteryn-foundation`, `oteryn-diagnostics` and `oteryn-test-support` add no external dependency. `deny.toml` explicitly permits the OSI-approved ISC and Zlib licenses required by the fixed wgpu graph and narrowly skips only its unavoidable `hashbrown 0.16.1` and `syn 3.0.3` duplicate branches. HTTP/TLS, text, audio and WebAssembly runtimes remain absent.

## CI behavior

`.github/workflows/rust-client.yml` is additive and path-scoped. It does not edit or replace the legacy C++/Lua workflow graph.

The Windows job validates:

- pinned toolchain availability/version;
- locked metadata;
- formatting;
- Clippy with warnings denied;
- tests, including crate unit/doctests and architecture fixtures;
- the real workspace architecture policy.

A separate Ubuntu job runs the immutable official cargo-deny action against `oteryn-client/Cargo.toml` and the colocated `deny.toml` for advisories, licenses, bans and sources. Supply-chain execution on Ubuntu does not replace the required Windows compilation/test evidence.

A successful Rust workflow proves only the workspace packages compiled and tested on the stated revision. It does not prove client runtime, GPU, server, protocol, assets or non-Windows product compatibility.

## Adding the next crate

Before adding a crate:

1. perform the full repository/task preflight;
2. identify the audit finding and accepted workstream gate;
3. claim exact paths and any shared public contract;
4. create only the crate(s) needed for the bounded observable result;
5. choose dependencies from current primary sources and record license/unsafe/maintenance review;
6. declare category metadata;
7. update architecture fixtures if a new edge/category appears;
8. run all workspace and owning-workstream validation;
9. update the module catalogue and architecture/ADR when public boundaries change.

The expected next package is selected after live preflight. It must not be folded into a completed package or reuse an expired shared-path lease.

## Rollback

The current foundation, diagnostics, test-support, renderer and application-shell packages have no user-data migration. A normal squash revert of the owning package removes its crate/workspace/documentation change. Generated Cargo build output and caches are transient and are never repository or release truth.
