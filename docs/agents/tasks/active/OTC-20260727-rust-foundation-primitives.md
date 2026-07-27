---
task_id: OTC-20260727-rust-foundation-primitives
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R01
branch: feat/OTC-20260727-rust-foundation-primitives
base_branch: main
created: 2026-07-27T12:00:00+02:00
updated: 2026-07-27T12:00:00+02:00
last_verified_commit: "55f73be78e040254975fafdc82da2e6b611e63a6"
risk: medium
related_pr: pending
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
  - std::time::Instant, std::time::Duration and std::sync atomics/Arc
public_interfaces:
  - typed process/session/task generations
  - monotonic instant/deadline and clock interfaces
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

Add exactly one standard-library-first `oteryn-foundation` crate containing generic technical generations, deterministic monotonic time, explicit cancellation ownership and narrow non-secret errors. Add the missing `foundation` architecture category and enforce that it cannot depend upward into product categories.

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
- shared documentation edits will be rebased/resolved narrowly from current `main` before merge.

Environment limitation:

- the execution sandbox cannot resolve `github.com`, so a local clone/worktree and local Cargo commands are unavailable;
- all repository writes use this dedicated branch through the authenticated GitHub connector;
- exact build/lint/test/supply-chain evidence must come from the repository CI on the exact PR head.

# Design decisions

- Add `ProcessGeneration`, `SessionGeneration` and `TaskGeneration` because the committed next-agent contract explicitly authorizes these non-interchangeable technical generations and lifecycle architecture requires owner/session/task fencing.
- Back generations with `u64`, expose zero/checked construction, ordering and `checked_next`; exhaustion returns a typed error and never wraps.
- Use a crate-owned monotonic `Moment`/`Deadline` measured from clock origin, with checked `Duration` arithmetic.
- Production `SystemClock` is created with one `std::time::Instant` origin and never uses wall-clock time.
- `ManualClock` advances only through explicit checked forward operations; no backwards setter is exposed.
- `CancellationSource` owns cancellation authority; cloneable `CancellationToken` only observes shared atomic state.
- Dropping a token has no effect. Dropping an uncancelled source does not implicitly cancel; cancellation is always explicit. This avoids hidden lifecycle actions and is tested/documented.
- Errors are closed enums containing only deterministic primitive data and no arbitrary external strings.
- No external dependency is required.

# Acceptance criteria

- [ ] Workspace contains one additional crate only: `oteryn-foundation`.
- [ ] `foundation` is normative in repository layout and recognized by architecture-check.
- [ ] A valid foundation fixture passes and a foundation-upward dependency fixture fails with `E005_FORBIDDEN_EDGE`.
- [ ] Process/session/task generations are distinct and checked without wraparound.
- [ ] Production and manual monotonic clocks satisfy deterministic origin/deadline behavior.
- [ ] Cancellation is explicit, idempotent, clone-visible and thread-safe without hidden threads.
- [ ] Drop semantics and repeated create/cancel/drop resource release are tested.
- [ ] Display/Debug output for primitive errors is deterministic and secret-free by construction.
- [ ] No game/domain/protocol/platform identity, events, commands, channels, assets or legacy runtime coupling is added.
- [ ] Workspace metadata, format, Clippy, tests, real architecture check and cargo-deny pass on exact head.
- [ ] Rust Client / Windows, Rust Client / Supply Chain, repository CI / Required and all current required checks pass.
- [ ] Full changed-file list, complete diff, comments, reviews and unresolved threads are inspected before merge.
- [ ] Task, module catalogue, Rust workspace operations and changelog are current.
- [ ] Merge occurs only through the autonomous merge gate.
- [ ] Completed task is archived in a separate lifecycle PR.

# Validation

Pending implementation and exact-head CI.

# Stop conditions

Stop and record a blocker if live path ownership changes, a primitive requires unresolved Platform/Canary identifiers, a dependency needs incomplete security/license evidence, a global runtime/executor/event bus becomes necessary, or workspace/CI policy would need weakening.

# Handoff

Next action: implement the smallest public API and focused tests on this branch, then use exact-head CI as the unavailable local Cargo validation substitute.
