---
task_id: OTC-20260724-global-client-options-audit
coordination_id: ""
status: auditing
agent: ChatGPT
branch: docs/OTC-20260724-global-client-options-audit
base_branch: main
created: 2026-07-24T21:37:49Z
updated: 2026-07-24T21:37:49Z
last_verified_commit: 8f2b6a8878c9cbc243a29c8b2dad7c755ca7a260
risk: low
related_issue: ""
related_pr: ""
depends_on: []
blocks:
  - implementation plan for Global-like options parity
owned_paths:
  - docs/ui/TIBIA_GLOBAL_OPTIONS_PARITY.md
  - docs/agents/tasks/active/OTC-20260724-global-client-options-audit.md
modules_touched: []
reuses:
  - modules/client_options
  - modules/game_actionbar
  - modules/game_cooldown
public_interfaces: []
cross_repo_tasks: []
---

# Goal

Produce a source-grounded audit of the current OTClient option surface against the supplied Tibia Global screenshots and official public Tibia client documentation, separating implemented, partial, missing, broken and server-dependent behavior.

# Acceptance criteria

- [ ] Every visible option in the supplied screenshots is classified with source evidence.
- [ ] Publicly documented Global client capabilities relevant to the screenshots are recorded without claiming undocumented completeness.
- [ ] Existing defects discovered during the audit are listed with exact paths/identifiers.
- [ ] A phased implementation backlog distinguishes UI-only, engine, protocol/server and platform-specific work.
- [ ] Relevant checks completed.
- [ ] Module catalogue impact handled or none.
- [ ] Documentation/changelog impact handled or none.
- [ ] Cross-repository impact handled or none.
- [ ] Autonomous merge gate satisfied.

# Confirmed context

- `main` was verified at `8f2b6a8878c9cbc243a29c8b2dad7c755ca7a260` when the task started.
- No open pull requests were returned for `blakinio/otclient` at task start.
- The supplied screenshots show Tibia Global option pages for Controls, Interface, Console, Action Bars and Misc/Screenshots.
- Official Tibia documentation explains the feature groups but does not publish a complete, versioned inventory of every current checkbox.
- Proprietary CipSoft assets are out of scope; this task records behavior and option parity only.

# Existing work to reuse

| Module/task/PR | Reuse | Evidence/path | Why it fits |
|---|---|---|---|
| Client options | option registry, category UI and settings persistence | `modules/client_options/**` | Primary source of current option exposure and behavior. |
| Action bars | visibility, reset and visual settings | `modules/game_actionbar/**` | Implements most action-bar options visible in the screenshots. |
| Cooldown bar | cooldown window visibility and spell/group rendering | `modules/game_cooldown/**` | Provides the Global-like cooldown bar behavior under a different option name. |

# Ownership and overlap check

- Open PRs inspected: none returned by live GitHub search.
- Active tasks inspected: `ACTIVE_WORK.md` is stale; no live PR overlap was found.
- Overlaps: none identified for this docs-only audit.
- Resolution: proceed on a dedicated documentation branch.

# Current state

The audit is in progress. Initial review confirms substantial parity in mouse controls, console filters, action-bar visibility/overlays and item expiry display, with missing or incomplete behavior in advanced-option filtering, keyboard delay semantics, rotation modifiers, screenshots, gameplay confirmations and several current Global controls.

# Plan

1. Complete the option-by-option source audit.
2. Record exact defects and semantic mismatches.
3. Write the parity matrix and phased backlog.
4. Validate Markdown and review the full diff.
5. Update the task, mark the PR ready and merge if repository checks permit.

# Work log

## 2026-07-24T21:37:49Z

- Changed: created the task branch and claimed documentation paths.
- Learned: the current options module already mirrors several Tibia Global categories but some labels do not match the actual behavior.
- Failed/blocked: local repository clone is unavailable because the execution container cannot resolve GitHub; GitHub connector reads are the source evidence.
- Result: audit branch ready for the durable report.

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| Keep this task documentation-only | The user asked whether options exist; implementation scope depends on the completed parity matrix. | none |
| Do not copy CipSoft UI assets | Repository policy forbids proprietary assets without redistribution rights. | none |

# Files and interfaces

| Path/interface/config/schema | Purpose | Status |
|---|---|---|
| `docs/ui/TIBIA_GLOBAL_OPTIONS_PARITY.md` | Durable audit and implementation backlog | planned |
| task record | Coordination and evidence | active |

# Validation and CI

| Commit | Command/check/workflow | Result | Evidence/notes |
|---|---|---|---|
| pending | Markdown/path review | not-run | Documentation not complete yet. |

Never write `passed` without verification.

# Failed approaches and dead ends

- Direct `git clone` failed because the container could not resolve `github.com`; source inspection continues through the GitHub connector.
- Repository code search returned no results for known strings, so exact known paths are being read directly.

# Risks and compatibility

- Runtime: none; documentation-only task.
- Data/migration: none.
- Security: no credentials or private data are included.
- Backward compatibility: none.
- Cross-repo rollout: none for the audit; some future options may require Canary or Platform support.
- Rollback: revert the documentation commit.

# Remaining work

1. Finish the parity matrix and implementation backlog.

# Handoff

## Start here

Read the parity report once created, then verify any implementation target against the exact source path listed there.

## Do not repeat

Do not infer checkbox functionality from the OTUI label alone; inspect the option action and owning module.

## Required reads

- `AGENTS.md`
- `docs/agents/ACTIVE_WORK.md`
- `docs/agents/MODULE_CATALOG.md`
- `modules/client_options/**`
- `modules/game_actionbar/**`
- `modules/game_cooldown/**`

## Open questions

- Which missing option group should become the first implementation milestone after the audit?

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Catalogue updated: not required unless implementation changes interfaces
- Changelog updated: not required for audit-only documentation
- Archived at: pending
