---
task_id: OTC-20260727-multi-agent-orchestration
status: awaiting_ci
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: coordination
branch: docs/OTC-20260727-multi-agent-orchestration
base_branch: main
created: 2026-07-27T10:30:00+02:00
updated: 2026-07-27T11:05:00+02:00
last_verified_commit: "c5d1b3e68bedbdda70d001feee3a3fc9dde61b38"
risk: medium
related_pr: "#55"
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

- [x] One normative multi-agent execution protocol exists.
- [x] Coordinator and worker responsibilities are separate and explicit.
- [x] Shared workspace files have a single-owner reservation/integration protocol.
- [x] Contract-producer and consumer ordering prevents duplicate public APIs.
- [x] A dependency DAG and maximum initial concurrency are defined.
- [x] One safe first wave can start without overlapping implementation paths.
- [x] Copy-ready prompts exist for the coordinator and three independent research lanes.
- [x] The existing foundation implementation prompt remains the sole implementation prompt for the first wave.
- [x] Task metadata extension covers lane, shared-path lease, contract ownership and integration dependencies.
- [x] PROGRAM, WORKSTREAMS and shared agent discovery route to the new system.
- [x] No runtime code, Cargo metadata, protocol constants, workflows, assets or external repositories are changed.
- [x] Complete 12-file changed-path and content review found no out-of-scope path.
- [ ] Exact-head required CI passes.
- [ ] Autonomous merge gate is satisfied.

# Confirmed context

- Rust workspace bootstrap and its archive are merged on current `main`.
- Foundation implementation is already active as task `OTC-20260727-rust-foundation-primitives` and draft PR #54; the initial wave registers that live worker and explicitly forbids launching a duplicate.
- PR #54 owns the foundation crate, Cargo/lockfile, architecture category/fixtures and its required shared integration documents.
- This coordination PR does not edit any PR #54 implementation/shared integration path.
- Open PR #48 is an operational draft and remains outside this task.
- Open PRs #37 and #23 own legacy asset/login-shell paths only.
- Root governance already requires one branch/worktree per agent and advisory `owned_paths`; this task adds Rust-client-specific execution and integration rules rather than replacing root governance.

# Delivered package

## Normative protocol

`oteryn-client/docs/agents/MULTI_AGENT_EXECUTION.md` defines:

- coordinator, worker, contract-producer and research roles;
- initial concurrency limit of one coordinator plus at most four workers;
- lane states from proposed through archived;
- exclusive path ownership and one active producer per public contract;
- task-based shared-path leases without a global mutable lock table;
- serialized Cargo/lockfile/architecture/CI integration;
- producer/consumer base-commit and revalidation rules;
- merge ordering, stale-work handling and mandatory stops.

## Initial Wave 1

`INITIAL_PARALLEL_WAVE.md` defines:

- W1-C coordinator;
- existing W1-F foundation implementation task/PR #54;
- W1-CP Canary evidence lane;
- W1-AR asset input/provenance evidence lane;
- W1-PR Windows platform evidence lane;
- exclusive owned/forbidden paths and shared-path lease table;
- Wave 2 dependency envelope without authorizing premature implementation.

## Prompts and task metadata

- `COORDINATOR_AGENT.md`;
- `WORKER_AGENT_BASE.md`;
- `CANARY_EVIDENCE_AGENT.md`;
- `ASSET_RESEARCH_AGENT.md`;
- `PLATFORM_RESEARCH_AGENT.md`;
- existing `NEXT_FOUNDATION_AGENT.md` remains the sole W1-F implementation prompt;
- `templates/PARALLEL_TASK.md` adds lane state, lease, contract role, producer/consumer and required-base metadata.

## Routing

- PROGRAM links the parallel protocol, first wave, prompts and stop conditions.
- WORKSTREAMS distinguishes workstream ownership from shared integration leases and maps default contract producers.
- Shared `docs/agents/README.md` routes new sessions to the protocol and wave plan.

# Design decisions

- One coordinator plus at most four workers is the initial maximum.
- Only one implementation worker modifies the Rust workspace in Wave 1.
- Three additional workers are isolated docs-only evidence lanes.
- Shared integration paths are serialized through task/PR state, not a manually edited central table.
- Consumers never define temporary duplicate public APIs and validate only against merged producers.
- Research outputs cannot silently become accepted architecture or code contracts.
- Foundation PR #54 is registered as the existing W1-F lane rather than duplicated.

# Work log

## 2026-07-27T10:30:00+02:00

- Performed current-main/open-PR preflight and created task, branch and draft PR #55.
- Claimed documentation/coordination paths only.

## 2026-07-27T11:05:00+02:00

- Added the normative execution protocol, initial dependency wave, coordinator/worker/research prompts and parallel task metadata.
- Updated PROGRAM, WORKSTREAMS and shared discovery routing.
- A subsequent live PR search found foundation PR #54 created seconds before this coordination PR; updated the wave and coordinator prompt to register that existing task and explicitly forbid duplicate launch.
- Reviewed the 12 changed paths and all authored content for path ownership, link consistency, lane terminology, shared-path lease rules and non-goals.
- Confirmed no Cargo, lockfile, workflow, runtime, protocol, asset, binary, secret or external-repository change.

# Validation and CI

| Commit | Check | Result | Evidence |
|---|---|---|---|
| `55f73be78e040254975fafdc82da2e6b611e63a6` | base/preflight | PASS | workspace bootstrap archived; open legacy/operational PR ownership inspected |
| `c5d1b3e68bedbdda70d001feee3a3fc9dde61b38` | changed-file/content/path consistency review | PASS | 12 declared documentation/task paths only; live PR #54 incorporated without overlap |
| final task-record head | required docs/fast CI | pending | no C++ or Rust build claim for docs-only package |

# Non-goals

- no automatic agent spawning service;
- no GitHub bot or scheduler implementation;
- no shared branch or worktree;
- no runtime/client/renderer/protocol/UI/asset implementation;
- no server or cross-repository writes;
- no replacement of root task/PR governance;
- no claim that every planned lane may implement code immediately.

# Remaining work

1. Update PR #55 body with live foundation-lane state and delivered scope.
2. Pass exact-head required CI.
3. Mark ready, recheck reviews/mergeability/checks and squash-merge.
4. Archive this task separately.
5. Launch one coordinator and the three isolated research agents; register existing PR #54 as W1-F rather than launching another foundation worker.

# Handoff

## Start here

- `oteryn-client/docs/agents/MULTI_AGENT_EXECUTION.md`
- `oteryn-client/docs/agents/INITIAL_PARALLEL_WAVE.md`
- `oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md`

## First next action

After merge/archive, start the coordinator session and let it register live PR #54 plus launch only the unclaimed research lanes.

# Completion

- Final status: awaiting CI
- PR: #55
- Merge commit: pending
- Archived at: pending
