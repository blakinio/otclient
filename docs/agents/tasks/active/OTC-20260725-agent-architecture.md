---
task_id: OTC-20260725-agent-architecture
coordination_id: ""
status: implementation
agent: "GPT-5.6 Thinking"
branch: docs/OTC-20260725-agent-architecture
base_branch: main
created: 2026-07-25T14:45:54+02:00
updated: 2026-07-25T14:45:54+02:00
last_verified_commit: ""
risk: low
related_issue: ""
related_pr: ""
depends_on:
  - "PR #27 Windows-only CI policy"
blocks: []
owned_paths:
  - docs/architecture/OTERYN_CLIENT_ARCHITECTURE.md
  - docs/agents/OTERYN_WORKSTREAM_MAP.md
  - docs/agents/prompts/OTCLIENT_NEW_AGENT_PROMPT.md
  - docs/agents/README.md
  - docs/agents/tasks/active/OTC-20260725-agent-architecture.md
modules_touched:
  - agent governance
  - architecture documentation
reuses:
  - AGENTS.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/REPOSITORY_MAP.md
  - docs/agents/KNOWN_RISKS.md
  - docs/agents/CROSS_REPO_CONTRACTS.md
  - docs/ui/OTCLIENT_COMPREHENSIVE_AUDIT_AND_PLAN.md from PR #25
public_interfaces: []
cross_repo_tasks: []
---

# Goal

Create a durable target architecture, repository/file ownership map and copy-ready startup prompt so a new agent can safely continue OTClient/Oteryn work without relying on chat history.

# Acceptance criteria

- [ ] Target client architecture documents trust boundaries, subsystem responsibilities and dependency direction.
- [ ] File/workstream map distinguishes current paths, planned paths and ownership/overlap rules.
- [ ] New-agent prompt includes preflight, Windows-only validation, Oteryn security invariants, Canary contracts and autonomous delivery requirements.
- [ ] Agent read order links all new documents.
- [ ] No client runtime code, assets, protocol or external repositories are changed.
- [ ] Documentation CI succeeds.

# Confirmed context

- Working and writable repository: `blakinio/otclient` only.
- `opentibiabr/otclient`, `solchanel/otclient-15` and Canary repositories are read-only unless a separately authorized task changes that rule.
- PR #23 owns the Oteryn enter-game presentation prototype.
- PR #25 owns the comprehensive capability/upstream audit.
- PR #26 owns the exact 16-commit upstream synchronization candidate.
- PR #27 owns the temporary Windows-only CI implementation.
- Oteryn Identity, no-password fallback, one-shot Game Session behavior and strict world routing must remain unchanged.

# Existing work to reuse

| Document/system | Reuse | Evidence/path | Why it fits |
|---|---|---|---|
| Root operating policy | Repository and delivery rules | `AGENTS.md` | Highest-priority local instructions. |
| Agent catalogue/map/risks | Existing discovery and safety model | `docs/agents/**` | Extend rather than replace governance. |
| Cross-repo registry | Canary/OTClient coupling | `docs/agents/CROSS_REPO_CONTRACTS.md` | Required protocol and login contract format. |
| Comprehensive audit | Roadmap, defects and parity evidence | PR #25 `docs/ui/OTCLIENT_COMPREHENSIVE_AUDIT_AND_PLAN.md` | Source for workstreams and priorities. |

# Ownership and overlap check

- Open PRs inspected: #23, #25, #26 and #27.
- No open PR owns the three new documentation paths.
- `docs/agents/README.md` will receive only a narrow read-order update.
- `docs/agents/BUILD_TEST_MATRIX.md`, CI workflows, runtime modules and protocol files remain untouched.

# Current state

Branch and task record created. Architecture documents are being authored.

# Plan

1. Define target architecture and non-negotiable boundaries.
2. Define repository structure, workstreams, ownership and acceptance gates.
3. Provide a standalone prompt for future agents.
4. Update the agent documentation read order.
5. Review the full diff and observe documentation CI.

# Work log

## 2026-07-25T14:45:54+02:00

- Changed: created the dedicated branch and task record.
- Learned: current documentation has strong governance and an audit roadmap, but no single target-architecture or workstream ownership document.
- Failed/blocked: none.
- Result: documentation can be added without touching active runtime work.

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| Keep architecture separate from the mutable audit | Architecture defines stable boundaries; audit records current gaps and issue status. | none |
| Make the new-agent prompt reference repository sources of truth rather than embed volatile SHAs | Prevents immediate staleness. | none |
| Treat Windows-only as the active project policy while PR #27 remains the implementation dependency | Explicit owner decision; do not duplicate CI changes in this PR. | none |

# Files and interfaces

| Path | Purpose | Status |
|---|---|---|
| `docs/architecture/OTERYN_CLIENT_ARCHITECTURE.md` | Target technical architecture and boundaries | planned |
| `docs/agents/OTERYN_WORKSTREAM_MAP.md` | File structure, ownership and work package routing | planned |
| `docs/agents/prompts/OTCLIENT_NEW_AGENT_PROMPT.md` | Copy-ready autonomous agent prompt | planned |
| `docs/agents/README.md` | Required read-order links | planned |

# Validation and CI

| Commit | Command/check/workflow | Result | Evidence/notes |
|---|---|---|---|
| pending | Markdown/path/full-diff review | not-run | Documentation-only; no client compilation required. |
| pending | GitHub `CI / Required` | not-run | Must pass on final head. |

# Failed approaches and dead ends

None.

# Risks and compatibility

- Runtime: none; documentation only.
- Data/migration: none.
- Security: inaccurate boundaries could mislead future agents; documents must preserve current Oteryn invariants.
- Backward compatibility: no shipped interfaces changed.
- Cross-repo rollout: none.
- Rollback: revert the documentation PR.

# Remaining work

1. Author the architecture, workstream map and new-agent prompt.

# Handoff

## Start here

Read this task, then the three new documents when present.

## Do not repeat

Do not create a second architecture or agent prompt in another location. Extend these files.

## Required reads

- `AGENTS.md`
- `docs/agents/README.md`
- `docs/agents/MODULE_CATALOG.md`
- `docs/agents/REPOSITORY_MAP.md`
- `docs/agents/KNOWN_RISKS.md`
- `docs/agents/CROSS_REPO_CONTRACTS.md`
- PR #25 audit

## Open questions

None.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Catalogue updated: not applicable
- Changelog updated: not required for documentation-only architecture
- Archived at: pending
