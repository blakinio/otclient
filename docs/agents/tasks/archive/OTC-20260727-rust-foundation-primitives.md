---
task_id: OTC-20260727-rust-foundation-primitives
status: completed
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R01
parallel_wave: OTERYN-W1-FOUNDATION-EVIDENCE
parallel_lane: W1-F
parallel_lane_state: archived
coordinator_task: OTC-20260727-multi-agent-orchestration
branch: feat/OTC-20260727-rust-foundation-primitives
base_branch: main
created: 2026-07-27T10:46:08+02:00
updated: 2026-07-27T12:20:00+02:00
last_verified_commit: "b8445f280b048fdabc2753b91d1f1906825e24d9"
required_base_commit: "cc2f3a6d2531aeb22c680b292345f9a51246864b"
risk: medium
related_pr: "#54"
depends_on:
  - merged PR #50 Rust workspace bootstrap
  - merged PR #53 WS-R01 lifecycle archive
  - merged PR #55 parallel execution protocol
  - merged PR #57 orchestration lifecycle archive
integration_after:
  - "cc2f3a6d2531aeb22c680b292345f9a51246864b"
blocks: []
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
shared_path_lease: []
contract_role: producer
contracts_produced:
  - typed process/session/task technical generations
  - monotonic clock, moment and deadline primitives
  - explicit cancellation source/token ownership semantics
  - primitive-specific non-secret error contracts
  - foundation architecture category and downward-only dependency rule
contracts_consumed: []
crates_touched:
  - oteryn-foundation
  - oteryn-architecture-check
features_touched: []
contracts_touched:
  - foundation public primitive API
  - foundation architecture dependency category
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

# Completion summary

Merged PR #54 delivered:

- distinct `ProcessGeneration`, `SessionGeneration` and `TaskGeneration` newtypes with explicit construction, ordering and checked non-wrapping increment;
- `Moment`, `Deadline` and the `MonotonicClock` interface;
- `SystemClock` backed only by `std::time::Instant`;
- deterministic thread-safe `ManualClock` with checked advance and explicit backward-movement rejection;
- explicit non-cloneable `CancellationSource` and cloneable observation-only `CancellationToken`;
- documented and tested Drop semantics: observer drop has no effect, source drop does not implicitly cancel, final drop releases shared state and starts no background work;
- deterministic concurrent cancellation-race coverage;
- closed `GenerationError` and `TimeError` values containing no arbitrary external text;
- package `oteryn-foundation` with zero external dependencies;
- the normative `foundation` repository category;
- architecture policy allowing product layers to depend downward on foundation while rejecting foundation dependencies into product categories;
- positive and negative architecture fixtures;
- workspace, lockfile, layout, operations, catalogue and changelog integration.

# Validation

| Evidence | Result |
|---|---|
| complete 16-file changed-path and full patch review on `b8445f280b048fdabc2753b91d1f1906825e24d9` | PASS |
| `cargo metadata --locked --format-version 1` | PASS on Windows exact head |
| `cargo fmt --all --check` | PASS on Windows exact head |
| `cargo clippy --workspace --all-targets --locked -- -D warnings` | PASS on Windows exact head |
| `cargo test --workspace --all-targets --locked` | PASS on Windows exact head |
| `cargo run --locked -p oteryn-architecture-check -- workspace .` | PASS on Windows exact head |
| Rust Client run `30256718479` | PASS: Windows and Supply Chain |
| repository CI run `30256719038` | PASS: scope, Lua, both Fast Checks and `CI / Required` |
| ready-for-review CI run `30257019625` | PASS on the same exact head |
| pinned Cargo 1.94.0 lockfile regeneration | PASS: zero `Cargo.lock` diff |
| PR comments, submitted reviews and unresolved threads | none |

# Merge

- PR: #54
- Method: squash
- Exact validated head: `b8445f280b048fdabc2753b91d1f1906825e24d9`
- Merge commit: `7a68f6e7d92eb6b05078bb001e4881d78544a82b`
- Merged: 2026-07-27

# Boundaries preserved

- no `CharacterId`, `WorldId` or `WorldChannelId`;
- no Platform or Canary mapping/assumption;
- no Identity, account session, game session, ticket or world-channel implementation;
- no `GameEvent`, `GameCommand`, map, entity or product lifecycle policy;
- no async runtime, executor, scheduler, global event bus or hidden thread;
- no network, HTTP/TLS, GPU, windowing, UI, assets, serialization, tracing, audio or WASM dependency;
- no unsafe, FFI, secret-bearing error or arbitrary external error text;
- no legacy C++/Lua/OTUI runtime coupling;
- no runtime, server, protocol, GPU, performance or non-Windows product compatibility claim.

# Acceptance criteria

- [x] One additional crate only: `oteryn-foundation`.
- [x] Foundation category documented and enforced by architecture-check.
- [x] Typed generations are non-interchangeable and cannot wrap during increment.
- [x] Production/manual monotonic time and explicit deadlines are tested.
- [x] Explicit cancellation, idempotence, clone visibility, Drop behavior, resource release and a thread race are tested.
- [x] Primitive errors are deterministic and secret-free by construction.
- [x] Foundation has zero external dependencies and no upward product dependency.
- [x] Locked metadata, formatting, Clippy, all workspace tests, real architecture-check and cargo-deny are green.
- [x] `Rust Client / Windows`, `Rust Client / Supply Chain`, `CI / Required` and all emitted required checks are green.
- [x] Full files, full diff, comments, reviews and unresolved threads were inspected.
- [x] Task, module catalogue, Rust workspace operations, repository layout and changelog were updated.
- [x] Merge occurred only through the autonomous merge gate.
- [x] Shared-path lease is released and lane W1-F is archived in this separate lifecycle PR.

# Next package recommendation

Implement one bounded Gate 1 structured diagnostics and secret-redaction contract package after a fresh dependency/security/license preflight; do not add product tracing integration or runtime services to foundation.

# Completion

- Final status: completed
- PR: #54
- Merge commit: `7a68f6e7d92eb6b05078bb001e4881d78544a82b`
- Archived at: `docs/agents/tasks/archive/OTC-20260727-rust-foundation-primitives.md`
