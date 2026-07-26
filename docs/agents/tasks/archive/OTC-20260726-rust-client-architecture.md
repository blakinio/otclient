---
task_id: OTC-20260726-rust-client-architecture
coordination_id: ""
status: completed
agent: "GPT-5.6 Thinking"
branch: docs/OTC-20260726-rust-client-architecture
base_branch: main
created: 2026-07-26T23:30:22+02:00
updated: 2026-07-27T00:20:00+02:00
last_verified_commit: "4550437d9442d6c23176f5f3aaec41dfbd99faa3"
risk: high
related_issue: ""
related_pr: "#45"
depends_on: []
blocks: []
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

Define and deliver one complete, agent-ready greenfield Rust Oteryn client architecture in an isolated `oteryn-client/` directory while preserving the current C++/Lua/OTUI client as a separately documented legacy/reference track.

# Completion summary

- The target product is a new Rust client, not a line-by-line OTClient rewrite.
- Canary is the first compatibility adapter; Oteryn is the long-term target ecosystem.
- Gameplay channels are parallel world instances selected during login or relog, not network streams.
- Channel 1 -> Channel 2 changes close the current game session and use a fresh ticket/session.
- The architecture defines data-oriented world/simulation storage, a `wgpu` renderer, native Rust UI, input, audio, signed assets, diagnostics, launcher/updater and optional sandboxed WebAssembly extensions.
- Canary and future Oteryn wire formats are isolated behind typed `GameEvent`/`GameCommand` domain boundaries.
- Oteryn Identity uses system-browser Authorization Code + PKCE and one-shot game-session handoff without sending the main password to game nodes.
- A mandatory foundation audit blocks production Cargo/workspace bootstrap until exact Canary, asset, performance, hardware and dependency evidence is collected.
- The current C++/Lua/OTUI client remains buildable and its maintenance architecture/workstreams remain separately documented.

# Delivered documents

## Greenfield client

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

## ADRs

- `0001-greenfield-rust-client.md`
- `0002-data-oriented-wgpu-renderer.md`
- `0003-protocol-adapter-boundary.md`
- `0004-static-modules-wasm-extensions.md`
- `0005-gameplay-channel-relog.md`

## Agent program

- `oteryn-client/docs/agents/PROGRAM.md`
- `WORKSTREAMS.md`
- `AUDIT_PLAN.md`
- `prompts/FIRST_AUDIT_AGENT.md`
- `templates/TASK.md`

## Legacy preservation

- `docs/architecture/LEGACY_OTCLIENT_ARCHITECTURE.md`
- `docs/agents/LEGACY_OTCLIENT_WORKSTREAMS.md`

# Validation

| Commit/run | Result | Evidence |
|---|---|---|
| `4550437d9442d6c23176f5f3aaec41dfbd99faa3` | PASS | final 31-file documentation/governance diff reviewed; no runtime, workflow, binary, asset, secret or external-repository changes |
| CI run `30222662629` | PASS | Detect Build Scope, both Fast Checks, Lua Syntax and `CI / Required` succeeded; Windows build correctly skipped |
| CI run `30222745448` | PASS | ready-for-review-triggered exact-head rerun also passed all required jobs |
| PR review state | PASS | no comments or requested changes; mergeable before merge |

# Merge

- PR: #45
- Method: squash
- Merge commit: `8f4670668efb04040ef2de048e579de7df5f1a20`
- Merged: 2026-07-27

# Rejected approaches

- Keeping the greenfield design as an appendix to the C++ architecture.
- Moving legacy source into `legacy/` during this architecture package.
- Treating gameplay channels as network streams.
- Creating placeholder Cargo crates before the audit.
- Removing detailed legacy governance rather than preserving it as a separate track.

# Next action

Start the separate WS-R00 foundation-audit task using `oteryn-client/docs/agents/prompts/FIRST_AUDIT_AGENT.md`. Do not bootstrap Cargo or production crates before the audit gate is accepted.

# Completion

- Final status: completed
- PR: #45
- Merge commit: `8f4670668efb04040ef2de048e579de7df5f1a20`
- Catalogue updated: yes
- Changelog updated: yes
- Archived at: `docs/agents/tasks/archive/OTC-20260726-rust-client-architecture.md`
