---
task_id: OTC-20260727-rust-foundation-primitives
status: validating
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R01
branch: feat/OTC-20260727-rust-foundation-primitives
base_branch: main
created: 2026-07-27T10:46:08+02:00
updated: 2026-07-27T11:20:00+02:00
last_verified_commit: "2d41f85e040655650eb6ecc36c9ec615a177a9ff"
risk: medium
related_pr: "#54"
depends_on:
  - merged PR #50 Rust workspace bootstrap
  - merged PR #53 WS-R01 lifecycle archive
blocks:
  - later application/domain/platform packages requiring generic generations, monotonic time or cancellation
owned_paths:
  - oteryn-client/crates/foundation/**
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/tools/architecture-check/**
  - oteryn-client/tests/architecture-fixtures/**
  - oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
  - oteryn-client/docs/agents/WORKSTREAMS.md
  - oteryn-client/docs/operations/RUST_WORKSPACE.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260727-rust-foundation-primitives.md
crates_touched:
  - oteryn-foundation
  - oteryn-architecture-check
features_touched: []
contracts_touched: []
modules_touched: []
reuses:
  - merged foundation audit and Gate 1 program
  - WS-R01 workspace lint, lockfile, architecture and supply-chain policy
  - std::time::Instant, std::time::Duration and std::sync atomics/Arc/RwLock
public_interfaces:
  - typed process/session/task generations
  - monotonic moment/deadline and clock interfaces
  - explicit cancellation source/token ownership
  - primitive-specific non-secret errors
cross_repo_tasks: []
performance_evidence:
  - no product performance claim; focused deterministic primitive tests only
security_evidence:
  - standard-library-only runtime implementation
  - no unsafe, FFI, secrets, external text in errors or global mutable runtime
---

# Goal

Add exactly one standard-library-only `oteryn-foundation` crate containing generic technical generations, deterministic monotonic time, explicit cancellation ownership and narrow non-secret errors. Add the missing `foundation` architecture category and enforce that it cannot depend upward into product categories.

# Fresh preflight

Base: `main` `55f73be78e040254975fafdc82da2e6b611e63a6`.

Read and reconciled:

- root and nested `AGENTS.md`;
- Oteryn client README and normative architecture, layout, lifecycle, security and performance/testing documents;
- Gate program/workstreams;
- merged foundation audit risk/gap/bootstrap documents;
- Rust workspace operations;
- archived WS-R01 task and merged PR #50;
- all live open PRs, their changed paths, active task records, comments, reviews and review threads.

Live overlap result:

- PR #48 owns only one operational workflow and its task record;
- PR #37 owns legacy client-assets Lua/tests/docs plus `docs/agents/CHANGELOG.md`;
- PR #23 owns legacy enter-game OTUI/Lua plus shared catalogue/changelog paths and is awaiting manual visual review;
- none owns `oteryn-client/crates/foundation/**`, workspace manifests, architecture-check category policy, foundation fixtures or the foundation public contracts;
- shared documentation edits must be reconciled against current `main` immediately before merge.

Environment limitation:

- the execution sandbox cannot resolve `github.com`, so a local clone/worktree and local Cargo commands are unavailable;
- all repository writes use this dedicated branch through the authenticated GitHub connector;
- exact build/lint/test/supply-chain evidence comes from repository CI on the exact PR head.

# Implemented design

- `ProcessGeneration`, `SessionGeneration` and `TaskGeneration` are distinct `u64` newtypes with `ZERO`, `MAX`, explicit construction, ordering and `checked_next`; exhaustion returns `GenerationError` and never wraps.
- A compile-fail public API example and direct `TypeId` unit test prove the three generation types are non-interchangeable.
- `Moment` and `Deadline` carry explicit `Duration` values from a clock-specific monotonic origin.
- `SystemClock` owns one `std::time::Instant` origin and never reads wall-clock time.
- Thread-safe `ManualClock` shares deterministic state through `Arc<RwLock<_>>`; `advance` is checked and `try_set` explicitly rejects backwards movement.
- `CancellationSource` is the unique cancellation authority; cloneable `CancellationToken` only observes an `AtomicBool` state.
- Cancellation is idempotent and visible across threads. Dropping a token has no effect. Dropping an uncancelled source does not implicitly cancel surviving tokens. Final source/token drop releases the shared state and starts no hidden work.
- `GenerationError` and `TimeError` are closed enums containing only primitive technical data; `Display` and derived `Debug` cannot include arbitrary external text or secrets.
- The crate has zero external dependencies and no unsafe, async runtime, executor, scheduler, event bus, hidden thread, network, protocol, renderer, UI, asset or legacy dependency.
- Architecture-check recognizes `foundation`, permits product layers to depend downward on it, and reports `E005_FORBIDDEN_EDGE` when foundation depends upward.

# Acceptance criteria

- [x] Workspace contains one additional crate only: `oteryn-foundation`.
- [x] `foundation` is normative in repository layout and recognized by architecture-check.
- [x] A valid foundation fixture passes by policy and a foundation-upward fixture expects `E005_FORBIDDEN_EDGE`.
- [x] Process/session/task generations are distinct and checked without wraparound.
- [x] Production and manual monotonic clocks implement deterministic origin/deadline behavior.
- [x] Cancellation is explicit, idempotent, clone-visible and thread-safe without hidden threads.
- [x] Drop semantics and repeated create/cancel/drop resource release are tested.
- [x] Display/Debug output for primitive errors is deterministic and secret-free by construction.
- [x] No game/domain/protocol/platform identity, events, commands, channels, assets or legacy runtime coupling is added.
- [ ] Workspace metadata, format, Clippy, tests, real architecture check and cargo-deny pass on the final exact head.
- [ ] Rust Client / Windows, Rust Client / Supply Chain, repository CI / Required and all current required checks pass on the final exact head.
- [ ] Full changed-file list, complete diff, comments, reviews and unresolved threads are inspected on the final head.
- [x] Task, module catalogue, Rust workspace operations, workstreams, repository layout and changelog are current for validation.
- [ ] Merge occurs only through the autonomous merge gate.
- [ ] Completed task is archived in a separate lifecycle PR.

# Validation checkpoint

- Diagnostic head `e4d615f3d77dfa23906b6a98b194cfbeb7764450`: locked workspace metadata passed; rustfmt identified formatting-only changes.
- Diagnostic head `9b8feefabcde7e8b11c2f48f7c9ac13eb4ed8818`: `Rust Client / Supply Chain` passed, including cargo-deny advisories, licenses, bans and sources.
- Current validation head begins after implementation checkpoint `2d41f85e040655650eb6ecc36c9ec615a177a9ff`; exact-head Windows, repository-required and full supply-chain evidence is pending.
- No runtime, server, protocol, GPU, performance or non-Windows compatibility claim is made.

# Stop conditions

Stop and record a blocker if live path ownership changes, a primitive requires unresolved Platform/Canary identifiers, a dependency needs incomplete security/license evidence, a global runtime/executor/event bus becomes necessary, or workspace/CI policy would need weakening.

# Next package recommendation

Implement one bounded Gate 1 structured diagnostics and secret-redaction contract package after a fresh dependency/security/license preflight; do not add product tracing integration or runtime services in this foundation PR.

# Handoff

Next action: complete exact-head CI, inspect the final diff/review state, and enter the autonomous merge gate only if every required check is green.
