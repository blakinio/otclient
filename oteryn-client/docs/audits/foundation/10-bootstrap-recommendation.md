# Bootstrap Recommendation

## Decision

After this audit is accepted, the first implementation package should be:

> **WS-R01 — Rust workspace, toolchain, dependency-policy and architecture-check bootstrap.**

This is a repository/tooling package only. It must not create the game application, launcher, renderer, protocol adapters, domain, UI, asset runtime, audio or feature crates.

Evidence status: `SUPPORTED` by the complete foundation audit. Product areas still have protocol, asset, performance, dependency or cross-repository decisions that should not be frozen in the first code package.

## Suggested task

```text
Task: OTC-20260727-rust-workspace-bootstrap
Track: greenfield-rust
Workstream: WS-R01
Suggested branch: ci/OTC-20260727-rust-workspace-bootstrap
Risk: medium
```

The implementation agent must perform a fresh preflight and adapt the identifier to live repository state.

## Observable outcome

A minimal Rust workspace exists under `oteryn-client/` that can:

1. format, lint and test its own narrow policy tool on Windows;
2. verify workspace metadata and dependency policy;
3. enforce architecture invariants against synthetic fixture graphs;
4. run in path-scoped CI without compiling or changing the legacy client;
5. provide a stable base for later crates without pretending those crates already exist.

## Proposed owned paths

```text
oteryn-client/Cargo.toml
oteryn-client/Cargo.lock
oteryn-client/rust-toolchain.toml
oteryn-client/rustfmt.toml
oteryn-client/deny.toml
oteryn-client/tools/architecture-check/**
oteryn-client/tests/architecture-fixtures/**
oteryn-client/docs/operations/RUST_WORKSPACE.md
.github/workflows/<dedicated Rust-client workflow or approved reusable paths>
docs/agents/MODULE_CATALOG.md
docs/agents/BUILD_TEST_MATRIX.md
docs/agents/CHANGELOG.md
docs/agents/tasks/active/<task>.md
```

`.github/workflows/**` is a high-contention area. The task must inspect current CI ownership and either coordinate or split CI integration into a dependent WS-R01 PR. Existing legacy required checks must not be weakened or replaced.

## Initial workspace shape

```text
oteryn-client/
├── Cargo.toml
├── Cargo.lock
├── rust-toolchain.toml
├── rustfmt.toml
├── deny.toml
├── tools/
│   └── architecture-check/
│       ├── Cargo.toml
│       └── src/
└── tests/
    └── architecture-fixtures/
```

The only initial workspace member should be the architecture-policy tool or an equally narrow WS-R01 utility justified by evidence.

Do not create empty placeholders for:

```text
apps/client
apps/launcher
crates/renderer
crates/game-domain
crates/protocol-canary
crates/protocol-oteryn
crates/ui-core
crates/asset-runtime
features/*
```

Those paths are created by their first observable implementation package.

## Toolchain policy

The implementation task selects and pins a current stable Rust toolchain using official Rust documentation. This audit does not freeze a version.

Required policy:

- required target is 64-bit Windows MSVC;
- toolchain is pinned in `rust-toolchain.toml`;
- formatter and linter components are explicit;
- minimum-supported Rust policy is documented;
- `Cargo.lock` is committed;
- no nightly-only production requirement without a new evidence-backed ADR.

## Workspace lint policy

The task should configure supported current lints rather than copying a stale list. Baseline requirements:

- warnings fail required CI;
- unsafe code is forbidden by default;
- workspace-level Rust and Clippy lints are inherited;
- formatting is required;
- external-input paths avoid panic-prone shortcuts;
- secret-bearing types are not broadly printable or serializable;
- exceptions are narrow, documented and tested.

## Dependency and supply-chain policy

The bootstrap should use as few dependencies as practical. The architecture checker may use the standard library plus a narrowly justified metadata/parser dependency.

Required controls:

- approved license policy;
- advisory/vulnerability checks;
- duplicate-version visibility;
- sources restricted to approved registries and workspace-local paths;
- no unreviewed external git dependency;
- no native dynamic plugin mechanism;
- action and dependency versions pinned according to repository policy;
- dependency and license evidence visible without leaking private paths.

If the exact license allowlist has not been approved, record a bounded owner/legal blocker and split the affected policy step rather than weakening unrelated checks.

## Architecture checker scope

The first checker validates workspace metadata and declared dependency categories. It is not a second build system.

### Positive checks

- all workspace members are under `oteryn-client/`;
- package names follow the `oteryn-*` convention;
- shared dependencies follow workspace policy;
- every member has a documented category/owner mapping;
- no member references legacy runtime paths;
- no dependency cycle exists in fixture graphs;
- the real initial one-tool workspace passes.

### Forbidden-edge checks

Synthetic fixtures must prove rejection of:

```text
game-domain -> protocol-canary
game-domain -> protocol-oteryn
renderer -> concrete feature
ui-core -> concrete feature
platform -> game feature
asset-types -> identity
feature A -> private feature B implementation
Rust package -> legacy src/** library
Rust package -> modules/** or mods/** runtime content
native dynamic plugin category inside the core graph
```

Failures must identify the source package, target package and violated rule.

### Deferred from this package

- full Rust source import analysis;
- domain-event schema validation;
- protocol, asset or UI semantics;
- binary-size and performance gates;
- application dependency selection;
- complete unsafe-block analysis beyond compiler/lint policy.

## Synthetic architecture fixtures

```text
valid_minimal_workspace
invalid_legacy_path_dependency
invalid_domain_to_canary_edge
invalid_renderer_to_feature_edge
invalid_ui_core_to_feature_edge
invalid_feature_cycle
invalid_unapproved_source_dependency
```

Fixtures contain no game code, assets, secrets or copied legacy manifests.

## CI recommendation

Rust jobs should be selected for `oteryn-client/**`, their workflow files and explicitly listed shared Rust-client governance paths.

Required bootstrap checks:

- install pinned toolchain;
- formatting check;
- locked workspace metadata validation;
- architecture checker tests and fixtures;
- workspace linting;
- workspace tests on Windows;
- approved dependency/license/advisory checks;
- final required-check integration without weakening legacy jobs.

A non-Windows metadata job may be additive if repository policy permits it, but required compiled evidence remains Windows.

Caching is an optimization only. Cache keys must include relevant toolchain/lockfile inputs, corruption must have a clean retry path and cached/generated data is never source of truth.

## Acceptance criteria

- [ ] Current stable Rust toolchain is selected from official documentation and pinned.
- [ ] Workspace contains only the narrow WS-R01 tool member; no product placeholders.
- [ ] `Cargo.lock` is committed and reproducible on Windows.
- [ ] Formatting, lint and tests pass on exact final head.
- [ ] Unsafe code is denied by default.
- [ ] Valid architecture fixture passes and every required invalid fixture fails for the expected rule.
- [ ] A dependency on legacy `src/`, `modules/` or `mods/` cannot pass policy.
- [ ] Dependency source/license/advisory policy is enforced or an exact blocker is separated without weakening other checks.
- [ ] Rust CI is path-scoped, additive and leaves legacy required checks intact.
- [ ] Required Windows job passes on exact head.
- [ ] Full diff contains no product implementation, protocol constant, asset or secret.
- [ ] Catalogue, build/test matrix, task record and workspace operations document are current.
- [ ] Autonomous merge gate passes.

## Expected validation commands

The task records exact commands for the selected tool versions. They should include equivalents of:

```text
cargo metadata --locked --format-version 1
cargo fmt --all --check
cargo clippy --workspace --all-targets --locked -- -D warnings
cargo test --workspace --all-targets --locked
cargo run --locked -p oteryn-architecture-check -- <policy input>
```

The approved dependency/license/advisory command is added after live policy/tool review.

## Explicit non-goals

The package does not:

- open a window or initialize a GPU;
- add `wgpu`, windowing, async, HTTP/TLS, audio, text or WASM dependencies;
- define game/domain identifiers, events or commands;
- implement Identity, account session or directory logic;
- parse or encode Canary/Oteryn messages;
- create asset pack schemas/importers;
- add UI/features;
- copy legacy source/tests/assets;
- claim product performance or server compatibility;
- resolve channel-aware native authentication.

## Dependencies and blockers

Prerequisites:

- this audit merged and archived;
- current PR/task/CI overlap inspected;
- current official Rust/tool documentation accessible;
- repository license policy available or an exact blocker recorded.

The task does not require Canary runtime, Oteryn deployment, game assets, GPU hardware, native channel-ticket contract or UI decisions.

## Risks and mitigation

- overbuilding the checker: keep it metadata/graph focused;
- selecting product dependencies early: initial member is tooling only;
- CI overlap: coordinate or split workflow work;
- stale lint/tool configuration: use current official docs and exact CI proof;
- broad required-job impact: use path scope and preserve existing evaluator behavior;
- weakening license/security gates: record blockers instead.

## Rollback

A normal squash revert removes this tooling/workspace package. No product runtime, persistent user data or migration exists.

## Handoff after bootstrap

The bootstrap PR recommends one next bounded package from live evidence, likely one of:

- typed foundation IDs/clocks/errors/test support;
- synthetic asset schema/compiler slice;
- minimal Windows window/surface spike.

It must not implement that next package inside the bootstrap PR.
