---
task_id: OTC-20260725-agent-architecture
coordination_id: ""
status: validation
agent: "GPT-5.6 Thinking"
branch: docs/OTC-20260725-agent-architecture
base_branch: main
created: 2026-07-25T14:45:54+02:00
updated: 2026-07-25T14:55:11+02:00
last_verified_commit: "23729da8ed9336d55473d9ff5b97d92f94c4eda4"
risk: low
related_issue: ""
related_pr: "#28"
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

- [x] Target client architecture documents trust boundaries, subsystem responsibilities and dependency direction.
- [x] File/workstream map distinguishes current paths, planned paths and ownership/overlap rules.
- [x] New-agent prompt includes preflight, Windows-only validation, Oteryn security invariants, Canary contracts and autonomous delivery requirements.
- [x] Agent read order links all new documents.
- [x] No client runtime code, assets, protocol or external repositories are changed.
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
- `docs/agents/README.md` received only a narrow read-order/core-document update.
- `docs/agents/BUILD_TEST_MATRIX.md`, CI workflows, runtime modules and protocol files remain untouched.

# Current state

The architecture, workstream map and standalone prompt are complete. Full changed-file and diff review found only the five declared documentation paths. PR #28 is ready for documentation CI.

# Plan

1. Define target architecture and non-negotiable boundaries. — complete
2. Define repository structure, workstreams, ownership and acceptance gates. — complete
3. Provide a standalone prompt for future agents. — complete
4. Update the agent documentation read order. — complete
5. Observe final documentation CI and close the task. — in progress

# Work log

## 2026-07-25T14:45:54+02:00

- Changed: created the dedicated branch and task record.
- Learned: current documentation has strong governance and an audit roadmap, but no single target-architecture or workstream ownership document.
- Failed/blocked: none.
- Result: documentation can be added without touching active runtime work.

## 2026-07-25T14:55:11+02:00

- Changed: added the target architecture, detailed workstream/file map, copy-ready new-agent prompt and README read-order links.
- Learned: stable architecture must remain separate from the volatile audit; planned paths are explicitly labelled and source/manifests remain authoritative.
- Validation: reviewed all changed filenames and the complete PR diff; only declared documentation paths are present.
- Failed/blocked: documentation CI has not yet completed.
- Result: implementation is complete and ready for final CI.

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| Keep architecture separate from the mutable audit | Architecture defines stable boundaries; audit records current gaps and issue status. | none |
| Make the new-agent prompt reference repository sources of truth rather than embed volatile SHAs | Prevents immediate staleness. | none |
| Treat Windows-only as the active project policy while PR #27 remains the implementation dependency | Explicit owner decision; do not duplicate CI changes in this PR. | none |
| Label future directories as planned, not existing | Prevents agents from treating a target structure as implementation evidence. | none |

# Files and interfaces

| Path | Purpose | Status |
|---|---|---|
| `docs/architecture/OTERYN_CLIENT_ARCHITECTURE.md` | Target technical architecture and boundaries | complete |
| `docs/agents/OTERYN_WORKSTREAM_MAP.md` | File structure, ownership and work package routing | complete |
| `docs/agents/prompts/OTCLIENT_NEW_AGENT_PROMPT.md` | Copy-ready autonomous agent prompt | complete |
| `docs/agents/README.md` | Required read-order links | complete |

# Validation and CI

| Commit | Command/check/workflow | Result | Evidence/notes |
|---|---|---|---|
| `23729da8ed9336d55473d9ff5b97d92f94c4eda4` | Changed-file and complete PR diff review | passed | Five declared documentation paths only; no source, assets, CI or external-repository changes. |
| pending final head | GitHub `CI / Required` | not-run | PR must be marked ready to obtain final evidence. |

# Failed approaches and dead ends

None.

# Risks and compatibility

- Runtime: none; documentation only.
- Data/migration: none.
- Security: documents preserve Oteryn password/fallback/session/routing and asset-integrity boundaries.
- Backward compatibility: no shipped interfaces changed.
- Cross-repo rollout: none.
- Rollback: revert PR #28.

# Remaining work

1. Mark PR #28 ready, observe final required documentation checks and update completion state.

# Handoff

## Start here

Read `docs/architecture/OTERYN_CLIENT_ARCHITECTURE.md`, then `docs/agents/OTERYN_WORKSTREAM_MAP.md`. Use `docs/agents/prompts/OTCLIENT_NEW_AGENT_PROMPT.md` for a fresh agent.

## Do not repeat

Do not create a second architecture or agent prompt in another location. Extend these files and keep volatile project status in tasks/audits.

## Required reads

- `AGENTS.md`
- `docs/agents/README.md`
- `docs/architecture/OTERYN_CLIENT_ARCHITECTURE.md`
- `docs/agents/OTERYN_WORKSTREAM_MAP.md`
- `docs/agents/prompts/OTCLIENT_NEW_AGENT_PROMPT.md`

## Open questions

None.

# Completion

- Final status: validation
- PR: #28
- Merge commit: pending
- Catalogue updated: not applicable; no reusable runtime interface added
- Changelog updated: not required for documentation-only architecture
- Archived at: pending
