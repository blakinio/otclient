---
task_id: OTC-20260726-rust-client-architecture
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
branch: docs/OTC-20260726-rust-client-architecture
base_branch: main
created: 2026-07-26T23:30:22+02:00
updated: 2026-07-26T23:30:22+02:00
last_verified_commit: "24452895ca44c4e9a98853d69fcc863b62bc089f"
risk: high
related_issue: ""
related_pr: "pending"
depends_on: []
blocks:
  - greenfield Rust client foundation audit
  - Rust workspace bootstrap
  - renderer, protocol, UI and asset workstreams
owned_paths:
  - AGENTS.md
  - docs/architecture/OTERYN_CLIENT_ARCHITECTURE.md
  - docs/architecture/OTERYN_CLIENT_REPOSITORY_LAYOUT.md
  - docs/architecture/OTERYN_CLIENT_SECURITY_MODEL.md
  - docs/architecture/decisions/ADR-001-greenfield-rust-client.md
  - docs/architecture/decisions/ADR-002-renderer-and-data-model.md
  - docs/architecture/decisions/ADR-003-protocol-adapter-boundary.md
  - docs/architecture/decisions/ADR-004-module-model.md
  - docs/architecture/decisions/ADR-005-client-lifecycle-and-world-channels.md
  - docs/agents/README.md
  - docs/agents/OTERYN_WORKSTREAM_MAP.md
  - docs/agents/REPOSITORY_MAP.md
  - docs/agents/KNOWN_RISKS.md
  - docs/agents/BUILD_TEST_MATRIX.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - docs/agents/programs/OTERYN_RUST_CLIENT_PROGRAM.md
  - docs/agents/prompts/OTERYN_RUST_CLIENT_AUDIT_AGENT_PROMPT.md
  - docs/agents/tasks/active/OTC-20260726-rust-client-architecture.md
modules_touched: []
reuses:
  - existing repository governance and task/PR workflow
  - existing C++ client only as behavior/protocol/asset evidence during audit
  - existing Canary and Oteryn Identity contracts where independently verified
public_interfaces:
  - target Rust workspace boundaries
  - client state machine and world-channel selection contract
  - agent workstream ownership model
cross_repo_tasks: []
---

# Goal

Replace the current evolutionary C++ target architecture with a complete, agent-ready greenfield Rust client architecture that treats Canary as the first compatibility adapter and Oteryn as the target ecosystem, including repository layout, security boundaries, module rules, performance budgets, world-channel login/relog behavior and an audit-first implementation program.

# Acceptance criteria

- [ ] Normative architecture explicitly defines a new Rust client rather than a line-by-line OTClient rewrite.
- [ ] Current C++/Lua/OTUI code is classified as legacy/reference evidence and does not constrain the target design.
- [ ] Repository layout and crate dependency direction are complete enough for independent agents to claim non-overlapping work.
- [ ] Canary and future Oteryn protocol implementations are isolated behind one domain adapter boundary.
- [ ] Account session, character/world/channel selection, game session and relog state machines are explicit.
- [ ] World channels mean parallel gameplay channels selected at login or relog, not network stream multiplexing.
- [ ] Renderer, world storage, UI, assets, audio, input, launcher/updater, diagnostics and extension boundaries are defined.
- [ ] Security model covers identity, one-shot game tickets, untrusted server data, updater/assets and extension sandboxing.
- [ ] Performance budgets and benchmark gates are documented as targets requiring measurement.
- [ ] A standalone first-agent audit prompt and ordered program backlog are ready.
- [ ] Existing open PR ownership is not overwritten.
- [ ] Documentation/full-diff checks and autonomous merge gate are completed.

# Confirmed context

- The current normative architecture on `main` says to evolve OTClient Redemption in C++/Lua/OTUI; this conflicts with the repository owner's new greenfield Rust direction.
- The requested client is written from scratch and should choose architecture for performance, safety and maintainability rather than compatibility with OTClient internals.
- Canary is the first server compatibility target; Oteryn is the long-term target.
- A world exposes multiple gameplay channels. The user selects a channel during login and may change it by relogging; no seamless in-game channel transfer is required.
- Open PRs inspected: #37 assets, #36 options Phase 0 and #23 legacy Oteryn login-shell prototype.
- None of those PRs owns the architecture/program paths claimed here.
- Current `main` observed at `24452895ca44c4e9a98853d69fcc863b62bc089f`.

# Existing work to reuse

| Module/task/PR | Reuse | Evidence/path | Why it fits |
|---|---|---|---|
| Repository agent governance | Branch/task/PR lifecycle and safety rules | `AGENTS.md`, `docs/agents/**` | Avoids inventing a parallel coordination system. |
| Current OTClient | Audit evidence only | `src/**`, `modules/**`, `data/**`, tests | Contains protocol, asset and gameplay behavior that must be inventoried, but is not the target architecture. |
| Oteryn Identity contract | Security requirements only | `docs/agents/CROSS_REPO_CONTRACTS.md` and verified external contract | Preserves Authorization Code + PKCE and one-shot game-session intent without retaining Lua implementation. |
| PR #3 test foundation | Legacy-client testing only | `tests/**` on PR #3 | Useful for comparison/audit; the Rust workspace will require its own native Cargo test structure rather than embedding C++ harness assumptions. |

# Ownership and overlap check

- Open PRs inspected: #37, #36, #23.
- Active tasks inspected: their task records on corresponding head branches.
- Overlaps: none on claimed architecture/program paths. PR #23 and #36 are legacy-client product work whose long-term priority may change after this architecture is accepted.
- Resolution: do not edit their owned paths or close/retarget their PRs in this task.

# Current state

Preflight complete. The repository already contains architecture and workstream documents, but they are oriented around incremental C++/Lua evolution and must be replaced rather than duplicated.

# Plan

1. Publish this task and a draft PR.
2. Replace the normative architecture and routing map.
3. Add repository layout, security model and durable ADRs.
4. Add the audit-first program and standalone audit-agent prompt.
5. Update governance discovery documents and changelog.
6. Review the complete diff and documentation consistency.

# Work log

## 2026-07-26T23:30:22+02:00

- Changed: created a dedicated architecture branch and claimed only governance/architecture paths.
- Learned: the existing normative documents explicitly require evolving the current C++ client, which contradicts the newly confirmed product direction.
- Failed/blocked: no blocker.
- Result: ready to publish the draft PR and architecture package.

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| Build a greenfield Rust client | Explicit repository-owner direction; avoids inheriting C++/Lua/OTUI constraints | ADR-001 |
| Audit before implementation | Compatibility facts and legal asset constraints remain incomplete | ADR-001 / program audit gate |
| Keep Canary/Oteryn outside the domain core | Enables compatibility now and protocol replacement later | ADR-003 |

# Files and interfaces

| Path/interface/config/schema | Purpose | Status |
|---|---|---|
| `docs/architecture/OTERYN_CLIENT_ARCHITECTURE.md` | Normative target architecture | planned |
| `docs/architecture/OTERYN_CLIENT_REPOSITORY_LAYOUT.md` | Concrete workspace/crate/file structure | planned |
| `docs/architecture/OTERYN_CLIENT_SECURITY_MODEL.md` | Trust boundaries and security invariants | planned |
| `docs/agents/OTERYN_WORKSTREAM_MAP.md` | Agent ownership and sequencing | planned |
| `docs/agents/programs/OTERYN_RUST_CLIENT_PROGRAM.md` | Ordered implementation program | planned |
| `docs/agents/prompts/OTERYN_RUST_CLIENT_AUDIT_AGENT_PROMPT.md` | First-agent standalone prompt | planned |

# Validation and CI

| Commit | Command/check/workflow | Result | Evidence/notes |
|---|---|---|---|
| pending | complete changed-file and Markdown/path review | not-run | Documentation-only task; no C++ or Rust build required. |
| pending | repository required documentation/fast checks | not-run | Run on final head. |

# Failed approaches and dead ends

- Extending the current architecture with another parallel “Rust option” was rejected because agents need one normative target.
- Treating world channels as network transport channels was rejected; they are parallel gameplay instances selected during login/relog.

# Risks and compatibility

- Runtime: no runtime code changes in this task.
- Data/migration: architecture must define coexistence without moving current C++ files yet.
- Security: no weakening of existing identity or asset invariants; new model must preserve or strengthen them.
- Backward compatibility: current client remains buildable until a separately gated retirement task.
- Cross-repo rollout: Canary and Oteryn work requires separate exact contracts; this task defines client boundaries only.
- Rollback: normal documentation PR revert.

# Remaining work

1. Open the draft PR and commit the full architecture package.

# Handoff

## Start here

Read the final architecture, program and audit prompt introduced by this task.

## Do not repeat

Do not create a second greenfield architecture or bootstrap Rust code before the audit gate is completed.

## Required reads

- `AGENTS.md`
- `docs/architecture/OTERYN_CLIENT_ARCHITECTURE.md`
- `docs/architecture/OTERYN_CLIENT_REPOSITORY_LAYOUT.md`
- `docs/architecture/OTERYN_CLIENT_SECURITY_MODEL.md`
- `docs/agents/OTERYN_WORKSTREAM_MAP.md`
- `docs/agents/programs/OTERYN_RUST_CLIENT_PROGRAM.md`

## Open questions

- Exact initial Canary revision and protocol fixture set remain audit outputs.
- Exact production Oteryn transport remains a cross-repository decision; the client architecture is transport-agnostic.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Catalogue updated: pending
- Changelog updated: pending
- Archived at: pending
