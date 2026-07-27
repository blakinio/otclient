# Rust Workspace Operations

Status: active workspace policy after WS-R01 bootstrap  
Required compiled platform: Windows x86-64 MSVC

## Scope

The workspace contains two bounded members:

```text
crates/foundation
tools/architecture-check
```

`oteryn-foundation` provides standard-library-only technical generations, monotonic time, explicit cancellation ownership and primitive-specific errors. `oteryn-architecture-check` validates workspace metadata and declared dependency categories. Neither is the client, launcher, renderer, protocol stack, domain, UI, asset runtime or extension host.

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

Known categories are defined by the architecture checker and follow the accepted architecture, including `foundation`, `tool`, `platform`, `game-domain`, protocol adapters, renderer/UI layers, assets, diagnostics and `feature`.

`foundation` is the bottom reusable category. It must not depend on application, platform, domain, protocol, renderer, UI, assets, diagnostics or feature crates. Lower product layers may depend on it only for generic primitives that do not encode product/server behavior.

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

## Lint and unsafe policy

Workspace Rust policy:

- unsafe Rust is forbidden by default;
- standard Rust/Clippy warnings fail required CI;
- `unwrap`, `expect`, `panic`, `todo`, `unimplemented` and debug macros are denied by policy;
- exceptions require a narrow owning package, documented reason and tests rather than a workspace-wide allowance;
- external-input parsers need explicit bounded error handling in their later workstreams.

The current workspace crates contain no unsafe code and no native/FFI dependency.

## Supply-chain policy

`deny.toml` applies to the required Windows dependency target and currently:

- denies known advisories and yanked releases;
- denies wildcard dependencies;
- denies duplicate dependency versions;
- permits the explicit initial license set only;
- denies unknown registries and git sources;
- permits crates.io as the external registry.

Do not broaden license/source policy merely to make CI green. Investigate the exact dependency and either reject it, replace it or update policy through a reviewed task with legal/security rationale.

The workspace pins only `serde_json` for the architecture tool's Cargo metadata and synthetic JSON fixtures. `oteryn-foundation` has zero external dependencies. Application dependencies such as GPU, windowing, async, HTTP/TLS, text, audio or WebAssembly runtimes remain outside this package.

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

The expected next package is selected after live preflight. It must not be folded into a completed foundation-primitives PR.

## Rollback

The foundation primitives have no runtime or user-data migration. A normal squash revert removes the crate/category change. Generated Cargo build output and caches are transient and are never repository or release truth.
