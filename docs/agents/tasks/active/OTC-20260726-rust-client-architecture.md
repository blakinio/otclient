---
task_id: OTC-20260726-rust-client-architecture
coordination_id: ""
status: awaiting_final_ci
agent: "GPT-5.6 Thinking"
branch: docs/OTC-20260726-rust-client-architecture
base_branch: main
created: 2026-07-26T23:30:22+02:00
updated: 2026-07-27T00:12:00+02:00
last_verified_commit: "33183027cc8c65e75d4b4911d3e8c5f0914a0add"
risk: high
related_issue: ""
related_pr: "#45"
depends_on: []
blocks:
  - greenfield Rust client foundation audit
  - Rust workspace bootstrap
  - renderer, protocol, UI and asset workstreams
owned_paths:
  - oteryn-client/README.md
  - oteryn-client/AGENTS.md
  - oteryn-client/docs/architecture/**
  - oteryn-client/docs/agents/**
  - docs/architecture/OTERYN_CLIENT_ARCHITECTURE.md
  - docs/architecture/LEGACY_OTCLIENT_ARCHITECTURE.md
  - docs/agents/README.md
  - docs/agents/OTERYN_WORKSTREAM_MAP.md
  - docs/agents/LEGACY_OTCLIENT_WORKSTREAMS.md
  - docs/agents/REPOSITORY_MAP.md
  - docs/agents/KNOWN_RISKS.md
  - docs/agents/BUILD_TEST_MATRIX.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260726-rust-client-architecture.md
modules_touched: []
reuses:
  - existing repository governance and task/PR workflow
  - current C++ client only as behavior/protocol/asset evidence during audit
  - existing Canary and Oteryn Identity contracts where independently verified
public_interfaces:
  - target Rust workspace boundaries
  - client state machine and gameplay-channel login/relog contract
  - protocol adapter boundary
  - agent workstream ownership model
cross_repo_tasks: []
---

# Goal

Define one complete, agent-ready greenfield Rust client architecture in an isolated `oteryn-client/` directory. Canary is the first compatibility adapter and Oteryn is the target ecosystem. Include repository layout, module and protocol boundaries, security, performance, assets, gameplay-channel login/relog behavior and an audit-first implementation program.

# Acceptance criteria

- [x] New client is a greenfield Rust product, not a line-by-line OTClient rewrite.
- [x] Legacy C++/Lua/OTUI remains buildable and is reference evidence only for the Rust track.
- [x] New-client architecture and agent documents are isolated under `oteryn-client/`.
- [x] Workspace layout, crates, dependency direction and non-overlapping workstreams are defined.
- [x] Canary and future Oteryn wire formats are isolated behind typed domain adapters.
- [x] Account session, selection, game session, reconnect and channel-relog lifecycles are explicit.
- [x] Gameplay channels are parallel world instances, not network streams.
- [x] Renderer, world, UI, input, audio, assets, diagnostics, updater and extension boundaries are defined.
- [x] Identity, one-shot ticket, parser, updater, assets and WASM security invariants are documented.
- [x] Performance budgets are targets requiring reproducible percentile measurements.
- [x] Mandatory foundation audit, workstream map and copy-ready first-agent prompt exist.
- [x] Five ADRs preserve the core decisions.
- [x] Detailed legacy architecture/workstream knowledge remains available.
- [x] Complete changed-file/full-patch consistency review was performed and findings repaired.
- [x] Required checks passed on implementation head `33183027cc8c65e75d4b4911d3e8c5f0914a0add`.
- [ ] Required checks pass on this final task-record head.
- [ ] Autonomous merge gate is satisfied.

# Confirmed context

- Previous target documentation prescribed incremental C++/Lua evolution and conflicted with the confirmed greenfield direction.
- Canary is the initial compatibility target; Oteryn is the long-term ecosystem.
- Channel changes use relog with a fresh game-entry transaction; seamless transfer is out of scope.
- Open PRs #37, #36 and #23 were inspected and do not own these architecture paths.
- PR #45 was opened from `main` at `24452895ca44c4e9a98853d69fcc863b62bc089f`.

# Delivered package

## Greenfield entry and architecture

- `oteryn-client/README.md`
- `oteryn-client/AGENTS.md`
- `oteryn-client/docs/architecture/ARCHITECTURE.md`
- `REPOSITORY_LAYOUT.md`
- `CLIENT_LIFECYCLE.md`
- `MODULE_MODEL.md`
- `PROTOCOL_BOUNDARY.md`
- `SECURITY_MODEL.md`
- `PERFORMANCE_AND_TESTING.md`
- `ASSET_PIPELINE.md`

## Durable decisions

- ADR-0001 greenfield Rust client and isolated directory;
- ADR-0002 data-oriented runtime and `wgpu` renderer;
- ADR-0003 protocol adapter boundary;
- ADR-0004 static first-party modules and WASM extensions;
- ADR-0005 gameplay-channel login/relog semantics.

## Agent program

- `oteryn-client/docs/agents/PROGRAM.md`
- `WORKSTREAMS.md`
- `AUDIT_PLAN.md`
- `prompts/FIRST_AUDIT_AGENT.md`
- `templates/TASK.md`

## Legacy preservation

- `docs/architecture/LEGACY_OTCLIENT_ARCHITECTURE.md`
- `docs/agents/LEGACY_OTCLIENT_WORKSTREAMS.md`

# Key decisions

| Decision | Reason | ADR |
|---|---|---|
| New product under `oteryn-client/` | isolates dependencies and CI while legacy remains operational | 0001 |
| Audit before Cargo bootstrap | exact Canary, asset, hardware and dependency facts remain to verify | 0001 |
| Data-oriented runtime and `wgpu` | locality, predictable frame time and modern GPU abstraction | 0002 |
| Wire adapters outside domain | Canary now and Oteryn later without another client rewrite | 0003 |
| Static first-party crates and sandboxed WASM | performance, reviewability and containment | 0004 |
| Gameplay-channel changes through relog | confirmed product behavior and deterministic session ownership | 0005 |

# Work log

## 2026-07-26T23:30:22+02:00

- Created task branch and draft PR #45 after overlap inspection.

## 2026-07-26T23:52:03+02:00

- Added the isolated architecture, workspace plan, security/performance/asset models, workstreams, audit and ADRs.
- Added no production crates, legacy runtime changes, assets, secrets or external-repository writes.

## 2026-07-27T00:02:00+02:00

- Full patch review found that initial routing edits removed too much legacy maintenance knowledge.
- Restored it in explicitly scoped legacy architecture/workstream documents and restored catalogue/discovery detail.
- Aligned audit wording with accepted `wgpu` ADR.

## 2026-07-27T00:12:00+02:00

- Exact-head run `30222552414` completed successfully on `33183027cc8c65e75d4b4911d3e8c5f0914a0add`.
- `Detect Build Scope`, `Fast Checks / Syntax and workflow validation`, `Fast Checks / Informational static analysis`, `Lua Syntax / Check Lua Syntax` and `CI / Required` succeeded.
- Windows build was correctly skipped for the documentation-only scope.
- No PR comments or review-change requests are open; PR was mergeable before this final task-record commit.

# Validation and CI

| Commit | Check | Result | Evidence |
|---|---|---|---|
| `7ee647f79bd2f4a61bf7d04831a3fbcb66ccd0fb` | complete changed-file and patch review | PASS | initial governance-loss issue found and repaired |
| `33183027cc8c65e75d4b4911d3e8c5f0914a0add` | workflow run `30222552414` | PASS | all required documentation-scope jobs succeeded; Windows build skipped by path scope |
| final task-record head | required CI | pending | must pass before readiness/merge |

# Failed approaches and dead ends

- A greenfield appendix inside the old architecture was rejected because agents need one normative target.
- Moving legacy source to `legacy/` now was rejected as a huge unrelated/conflicting diff.
- Treating gameplay channels as transport streams was rejected.
- Creating placeholder Cargo crates before the audit was rejected.
- Removing detailed legacy governance was detected during review and repaired.

# Risks and compatibility

- Documentation only; no runtime or build behavior changed.
- Existing client and active PR ownership remain intact.
- Exact Canary/Oteryn implementation still requires coordinated tasks and evidence.
- Rollback is a normal squash revert.

# Remaining work

1. Pass required CI on this final task-record head.
2. Mark PR #45 ready, recheck mergeability/checks/diff/reviews and squash-merge.
3. Start the separate foundation-audit task from the committed copy-ready prompt; do not bootstrap Cargo first.

# Handoff

## Start here

- `oteryn-client/README.md`
- `oteryn-client/AGENTS.md`
- `oteryn-client/docs/architecture/ARCHITECTURE.md`
- `oteryn-client/docs/agents/AUDIT_PLAN.md`

## Do not repeat

Do not create another Rust architecture, move legacy source or create production crates before the audit gate.

## Audit-owned open questions

- exact initial Canary revision and fixtures;
- legally usable asset sources;
- concrete Windows hardware tiers;
- exact dependency packages/versions;
- native Oteryn transport/schema/resume design.

# Completion

- Final status: awaiting final CI
- PR: #45
- Merge commit: pending
- Catalogue updated: yes
- Changelog updated: yes
- Archived at: pending
