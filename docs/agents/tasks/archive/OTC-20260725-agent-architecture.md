---
task_id: OTC-20260725-agent-architecture
coordination_id: ""
status: complete
agent: "GPT-5.6 Thinking"
branch: docs/OTC-20260725-agent-architecture
base_branch: main
created: 2026-07-25T14:45:54+02:00
updated: 2026-07-25T15:00:56+02:00
last_verified_commit: "fde5b0699663c4d1845beeb60d5e785ae27fd30b"
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
- [x] Documentation CI succeeds.

# Delivered

| Path | Purpose |
|---|---|
| `docs/architecture/OTERYN_CLIENT_ARCHITECTURE.md` | Stable target architecture, trust boundaries, dependency direction, state ownership and definition of done. |
| `docs/agents/OTERYN_WORKSTREAM_MAP.md` | Existing/planned repository structure, ten workstreams, shared-path ownership and package routing. |
| `docs/agents/prompts/OTCLIENT_NEW_AGENT_PROMPT.md` | Standalone autonomous prompt with preflight, Windows-only policy, Oteryn invariants, Canary rules and delivery loop. |
| `docs/agents/README.md` | Required read order and links to the new sources of truth. |

# Confirmed decisions

- Stable architecture remains separate from the mutable capability/upstream audit.
- Planned directories are explicitly labelled and are not implementation evidence.
- Windows is the only compiled/required target for the current project phase; this PR does not duplicate PR #27's CI implementation.
- Oteryn Identity, no-password fallback, authoritative `world_id`, one-shot Game Session and strict asset/protocol boundaries are normative.
- New agents must choose the highest-priority unblocked, non-overlapping work package from live state rather than chat history.

# Validation

| Commit | Check | Result |
|---|---|---|
| `23729da8ed9336d55473d9ff5b97d92f94c4eda4` | Complete changed-file and PR diff review | passed; only declared documentation paths |
| `fde5b0699663c4d1845beeb60d5e785ae27fd30b` | GitHub Actions run `30158807085` | passed |
| same | Fast Checks / Syntax and workflow validation | success |
| same | Fast Checks / Informational static analysis | success |
| same | Lua Syntax | success |
| same | `CI / Required` | success |
| same | Platform builds | correctly skipped for documentation-only scope |

# Risks and compatibility

- No runtime, protocol, asset, authentication or CI workflow behavior changed.
- No external repository was modified.
- Rollback is a revert of PR #28.

# Handoff

A new agent starts with:

1. `AGENTS.md`;
2. `docs/agents/README.md`;
3. `docs/architecture/OTERYN_CLIENT_ARCHITECTURE.md`;
4. `docs/agents/OTERYN_WORKSTREAM_MAP.md`;
5. `docs/agents/prompts/OTCLIENT_NEW_AGENT_PROMPT.md`.

Do not create parallel architecture, prompt, protocol model, authentication flow or test harness documentation. Extend the established owner.

# Completion

- Final status: complete
- PR: #28
- Merge commit: pending PR merge
- Catalogue updated: not applicable; no runtime interface added
- Changelog updated: not required for documentation-only architecture
- Archived at: 2026-07-25T15:00:56+02:00
