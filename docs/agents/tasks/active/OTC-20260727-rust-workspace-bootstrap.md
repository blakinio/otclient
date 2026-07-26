---
task_id: OTC-20260727-rust-workspace-bootstrap
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R01
branch: ci/OTC-20260727-rust-workspace-bootstrap
base_branch: main
created: 2026-07-27T01:20:00+02:00
updated: 2026-07-27T01:20:00+02:00
last_verified_commit: "a10c6c7620d5b28b7d68060dd8427e4766f63cc2"
risk: medium
related_pr: "pending"
depends_on:
  - merged PR #47 foundation audit
  - merged PR #49 audit task archival
blocks:
  - Rust foundation crates
  - renderer/domain/asset/protocol workstreams
owned_paths:
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/rust-toolchain.toml
  - oteryn-client/rustfmt.toml
  - oteryn-client/deny.toml
  - oteryn-client/tools/architecture-check/**
  - oteryn-client/tests/architecture-fixtures/**
  - oteryn-client/docs/operations/RUST_WORKSPACE.md
  - .github/workflows/rust-client.yml
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/BUILD_TEST_MATRIX.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260727-rust-workspace-bootstrap.md
crates_touched:
  - oteryn-architecture-check
features_touched: []
contracts_touched: []
modules_touched: []
reuses:
  - foundation audit bootstrap recommendation
  - existing repository required-check and Windows-only policy
public_interfaces:
  - Rust workspace metadata policy
  - architecture category and dependency-edge policy
  - path-scoped Rust CI entry point
cross_repo_tasks: []
---

# Goal

Create the smallest production-quality Rust workspace foundation for the greenfield Oteryn client: one architecture-policy tool, synthetic dependency-graph fixtures, pinned stable toolchain, lint/supply-chain policy and additive Windows CI. Do not add any product application or engine crate.

# Acceptance criteria

- [ ] Current stable Rust toolchain is selected from official Rust metadata and pinned.
- [ ] Workspace contains exactly one member: `oteryn-architecture-check`.
- [ ] No placeholder application, renderer, protocol, domain, UI, asset, audio or feature crate exists.
- [ ] `Cargo.lock` is committed and all required commands use `--locked` where applicable.
- [ ] Unsafe Rust is forbidden by default through workspace/package policy.
- [ ] Architecture checker validates the real workspace and synthetic policy graphs.
- [ ] Valid fixture passes and every required invalid fixture fails for the expected rule.
- [ ] Legacy `src/`, `modules/` and `mods/` runtime dependencies are rejected.
- [ ] Dependency cycle and forbidden category edges are rejected with actionable errors.
- [ ] Dependency/license/advisory policy is documented and enforced without weakening unrelated checks.
- [ ] Rust CI is additive, path-scoped and does not replace or weaken existing legacy checks.
- [ ] Required Windows Rust build/lint/test succeeds on exact head.
- [ ] Full changed-file/diff review contains no product implementation, protocol constants, assets or secrets.
- [ ] Catalogue, build/test matrix, changelog and task record are current.
- [ ] Autonomous merge gate is satisfied.

# Confirmed context

- Foundation audit and archive are merged on current `main`.
- Audit authorizes this package only; product implementation remains out of scope.
- Official stable channel metadata reports Rust `1.94.0` dated 2026-07-02. The task will pin this exact toolchain after validating Windows availability through CI.
- Open PR #48 owns only agent documentation under `oteryn-client/docs/agents/**` and does not overlap this task.
- Other live PRs inspected are legacy asset/options/docs work and do not own these Rust workspace paths.
- `.github/workflows/**` remains high contention; this task claims one new dedicated `rust-client.yml` workflow only and will not edit existing workflow files unless a proven required-check integration issue forces a separately documented change.

# Plan

1. Read current CI/action conventions and official Rust/cargo-deny documentation.
2. Add one-member workspace and pinned toolchain/lint metadata.
3. Implement a dependency-policy checker using a small versioned text policy/fixture format with no product dependencies.
4. Add valid and forbidden synthetic fixture graphs.
5. Add supply-chain policy and workspace operations documentation.
6. Add an additive Windows workflow scoped to Rust-client/tooling paths.
7. Run/inspect exact-head CI, repair root causes and review the complete diff.
8. Merge only when all required checks pass.

# Explicit non-goals

- no client or launcher executable;
- no `wgpu`, windowing, async, HTTP/TLS, text, audio or WASM dependencies;
- no game/domain identifiers, events or commands;
- no Canary/Oteryn parsing or protocol constants;
- no asset schema or importer;
- no native UI or feature code;
- no legacy C++/Lua/OTUI dependency;
- no performance or runtime/server compatibility claim.

# Validation and CI

| Commit | Check | Result | Evidence |
|---|---|---|---|
| `a10c6c7620d5b28b7d68060dd8427e4766f63cc2` | base/preflight | PASS | audit/archive merged; no overlapping owned paths found |
| pending | Rust metadata/fmt/clippy/test/architecture/license/advisory | not-run | |

# Risks and compatibility

- Workflow overlap: one new workflow file only; preserve current required-check graph.
- Tool drift: pin Rust and action/tool versions based on current primary sources.
- License policy: use a narrow explicit allowlist suitable for the initial dependency tree; do not broaden merely for green CI.
- Architecture checker scope: metadata/graph policy only, not a second build system.
- Rollback: normal squash revert; no runtime or persistent user data.

# Remaining work

1. Open the early draft PR.
2. Inspect current workflow conventions and implement the one-member workspace.

# Handoff

## Start here

- `oteryn-client/docs/audits/foundation/10-bootstrap-recommendation.md`
- `oteryn-client/docs/agents/WORKSTREAMS.md`
- `.github/workflows/ci.yml`

## Do not repeat

Do not create product placeholder crates or add application dependencies.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Catalogue updated: pending
- Changelog updated: pending
- Archived at: pending
