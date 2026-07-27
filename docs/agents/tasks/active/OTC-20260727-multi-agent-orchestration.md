---
task_id: OTC-20260727-multi-agent-orchestration
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: coordination
branch: docs/OTC-20260727-multi-agent-orchestration
base_branch: main
created: 2026-07-27T10:30:00+02:00
updated: 2026-07-27T10:30:00+02:00
last_verified_commit: "55f73be78e040254975fafdc82da2e6b611e63a6"
risk: medium
related_pr: "pending"
depends_on:
  - merged PR #50 Rust workspace bootstrap
  - merged PR #53 bootstrap task archival
blocks:
  - safe parallel launch of Rust-client worker agents
owned_paths:
  - oteryn-client/docs/agents/MULTI_AGENT_EXECUTION.md
  - oteryn-client/docs/agents/INITIAL_PARALLEL_WAVE.md
  - oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md
  - oteryn-client/docs/agents/prompts/WORKER_AGENT_BASE.md
  - oteryn-client/docs/agents/prompts/CANARY_EVIDENCE_AGENT.md
  - oteryn-client/docs/agents/prompts/ASSET_RESEARCH_AGENT.md
  - oteryn-client/docs/agents/prompts/PLATFORM_RESEARCH_AGENT.md
  - oteryn-client/docs/agents/templates/PARALLEL_TASK.md
  - oteryn-client/docs/agents/PROGRAM.md
  - oteryn-client/docs/agents/WORKSTREAMS.md
  - docs/agents/README.md
  - docs/agents/tasks/active/OTC-20260727-multi-agent-orchestration.md
crates_touched: []
features_touched: []
contracts_touched:
  - multi-agent ownership and merge protocol
modules_touched: []
reuses:
  - root multi-agent concurrency policy
  - Rust-client workstream ownership map
  - task records and live draft PRs as authoritative coordination state
public_interfaces:
  - agent lane states
  - shared-path reservation protocol
  - dependency and merge-order protocol
cross_repo_tasks: []
---

# Goal

Prepare a complete, repository-native system for several autonomous agents to work safely in parallel on the greenfield Rust Oteryn client. The package defines one coordinator role, worker-lane rules, shared-path reservations, dependency/merge ordering, an immediately safe first parallel wave and copy-ready prompts.

# Acceptance criteria

- [ ] One normative multi-agent execution protocol exists.
- [ ] Coordinator and worker responsibilities are separate and explicit.
- [ ] Shared workspace files have a single-owner reservation/integration protocol.
- [ ] Contract-producer and consumer ordering prevents duplicate public APIs.
- [ ] A dependency DAG and maximum initial concurrency are defined.
- [ ] One safe first wave can start without overlapping implementation paths.
- [ ] Copy-ready prompts exist for the coordinator and three independent research lanes.
- [ ] The existing foundation implementation prompt remains the sole implementation prompt for the first wave.
- [ ] Task metadata extension covers lane, shared-path lease, contract ownership and integration dependencies.
- [ ] PROGRAM, WORKSTREAMS and shared agent discovery route to the new system.
- [ ] No runtime code, Cargo metadata, protocol constants, workflows, assets or external repositories are changed.
- [ ] Complete diff and exact-head required CI pass.
- [ ] Autonomous merge gate is satisfied.

# Confirmed context

- Rust workspace bootstrap and its archive are merged on current `main`.
- No open Rust-client implementation PR currently owns foundation, renderer, protocol, asset or platform crate paths.
- Open PR #48 is an operational draft and remains outside this task.
- Open PRs #37 and #23 own legacy asset/login-shell paths only.
- Root governance already requires one branch/worktree per agent and advisory `owned_paths`; this task adds Rust-client-specific execution and integration rules rather than replacing root governance.

# Design constraints

- Start with one coordinator plus at most four worker agents.
- Do not allow two workers to edit `Cargo.toml`, `Cargo.lock`, architecture-check policy, Rust CI or the same shared contract simultaneously.
- Research lanes may run before their implementation gate only when they write isolated evidence documents and do not freeze unsupported code contracts.
- Implementation consumers wait for their contract producer to merge.
- Coordinator does not implement a large product module while coordinating.
- Live task records and open PRs remain authoritative; no manually edited global lock table is introduced.

# Plan

1. Define lane states, ownership, reservations and dependency protocol.
2. Define initial wave and later dependency DAG.
3. Add coordinator and worker prompts.
4. Add three safe docs-only research prompts that may run alongside foundation implementation.
5. Extend task metadata template for parallel work.
6. Link the protocol from PROGRAM, WORKSTREAMS and shared agent discovery.
7. Review full diff and pass exact-head checks.

# Validation and CI

| Commit | Check | Result | Evidence |
|---|---|---|---|
| `55f73be78e040254975fafdc82da2e6b611e63a6` | base/preflight | PASS | workspace bootstrap archived; open PR ownership inspected |
| pending | Markdown/path/full-diff review | not-run | |
| pending | required docs/fast CI | not-run | |

# Non-goals

- no automatic agent spawning service;
- no GitHub bot or scheduler implementation;
- no shared branch or worktree;
- no runtime/client/renderer/protocol/UI/asset implementation;
- no server or cross-repository writes;
- no replacement of root task/PR governance;
- no claim that every planned lane may implement code immediately.

# Remaining work

1. Open an early draft PR.
2. Add the protocol, first-wave plan, prompts and routing updates.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Archived at: pending
