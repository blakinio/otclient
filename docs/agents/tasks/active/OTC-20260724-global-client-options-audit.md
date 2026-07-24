---
task_id: OTC-20260724-global-client-options-audit
coordination_id: ""
status: ready
agent: ChatGPT
branch: docs/OTC-20260724-global-client-options-audit
base_branch: main
created: 2026-07-24T21:37:49Z
updated: 2026-07-24T21:48:48Z
last_verified_commit: 2e15b1ff0ac7e47b769c71065d6577f94ceba28e
risk: low
related_issue: ""
related_pr: "22"
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

- [x] Every visible option group in the supplied screenshots is classified with source evidence.
- [x] Publicly documented Global client capabilities relevant to the screenshots are recorded without claiming undocumented completeness.
- [x] Existing defects discovered during the audit are listed with exact paths/identifiers.
- [x] A phased implementation backlog distinguishes UI-only, engine, protocol/server and platform-specific work.
- [x] Relevant checks completed.
- [x] Module catalogue impact handled: no reusable interface changed.
- [x] Documentation/changelog impact handled: durable audit added; runtime changelog not required.
- [x] Cross-repository impact handled: future Canary-dependent options are identified, but this audit changes no contract.
- [ ] Autonomous merge gate satisfied.

# Confirmed context

- `main` was verified at `8f2b6a8878c9cbc243a29c8b2dad7c755ca7a260` when the task started.
- No open pull requests were returned for `blakinio/otclient` at task start.
- The supplied screenshots show Tibia Global option pages for Controls, Interface, Console, Action Bars and Misc/Screenshots.
- Official Tibia documentation explains the feature groups but does not publish a complete, versioned inventory of every current checkbox.
- Proprietary CipSoft assets are out of scope; this task records behavior and option parity only.
- PR #22 contains only the audit report and this task record.

# Existing work to reuse

| Module/task/PR | Reuse | Evidence/path | Why it fits |
|---|---|---|---|
| Client options | option registry, category UI and settings persistence | `modules/client_options/**` | Primary source of current option exposure and behavior. |
| Action bars | visibility, reset, hotkeys and visual settings | `modules/game_actionbar/**` | Implements most action-bar options visible in the screenshots. |
| Cooldown bar | cooldown window visibility and spell/group rendering | `modules/game_cooldown/**` | Provides the Global-like cooldown bar behavior under a different option name. |

# Ownership and overlap check

- Open PRs inspected: none returned by live GitHub search before PR #22 was opened.
- Active tasks inspected: `ACTIVE_WORK.md` is stale; no live PR overlap was found.
- Overlaps: none identified for this docs-only audit.
- Resolution: completed on a dedicated documentation branch and draft PR #22.

# Current state

The audit is complete. Of 58 screenshot-derived option groups, 25 are implemented, 7 are partial, 24 are missing and 2 are broken. The report also records seven concrete source defects and a six-phase delivery plan.

# Plan

1. Inspect checks on the final documentation head.
2. Mark PR #22 ready when required checks are green.
3. Squash-merge PR #22.
4. Archive the task after the merge commit is known.

# Work log

## 2026-07-24T21:37:49Z

- Changed: created the task branch and claimed documentation paths.
- Learned: the current options module already mirrors several Tibia Global categories but some labels do not match the actual behavior.
- Failed/blocked: local repository clone is unavailable because the execution container cannot resolve GitHub; GitHub connector reads are the source evidence.
- Result: audit branch ready for the durable report.

## 2026-07-24T21:48:48Z

- Changed: added `docs/ui/TIBIA_GLOBAL_OPTIONS_PARITY.md` with the complete matrix, defects and phased backlog.
- Learned: action bars and console filtering have strong parity; the largest gaps are advanced filtering, input semantics, Misc gameplay, screenshots and import/export.
- Failed/blocked: no runtime client was built or exercised because this task is documentation-only and the repository policy does not require compilation for documentation changes.
- Result: source/path and full-diff review completed; task is ready for PR checks.

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| Keep this task documentation-only | The user asked whether options exist; implementation scope depends on the completed parity matrix. | none |
| Do not copy CipSoft UI assets | Repository policy forbids proprietary assets without redistribution rights. | none |
| Treat screenshots as the exact visible-option baseline | Official documentation describes capabilities but is not a complete versioned checkbox inventory. | none |

# Files and interfaces

| Path/interface/config/schema | Purpose | Status |
|---|---|---|
| `docs/ui/TIBIA_GLOBAL_OPTIONS_PARITY.md` | Durable audit and implementation backlog | complete |
| task record | Coordination and evidence | ready |

# Validation and CI

| Commit | Command/check/workflow | Result | Evidence/notes |
|---|---|---|---|
| `2e15b1ff0ac7e47b769c71065d6577f94ceba28e` | Source/path review | PASS | Report references inspected current paths and separates unverified runtime behavior. |
| `2e15b1ff0ac7e47b769c71065d6577f94ceba28e` | PR changed-file review | PASS | Only the task record and `docs/ui/TIBIA_GLOBAL_OPTIONS_PARITY.md` are changed. |
| `2e15b1ff0ac7e47b769c71065d6577f94ceba28e` | Full unified diff review | PASS | Tables, headings, source paths and scope limitations were manually reviewed. |
| final head | GitHub Actions | pending | Observe checks after this task update. |

Never write `passed` without verification.

# Failed approaches and dead ends

- Direct `git clone` failed because the container could not resolve `github.com`; source inspection continued through the GitHub connector.
- Repository code search returned no results for known strings, so exact known paths were read directly.

# Risks and compatibility

- Runtime: none; documentation-only task.
- Data/migration: none.
- Security: no credentials or private data are included; quick-login recommendations explicitly preserve the Oteryn security boundary.
- Backward compatibility: none.
- Cross-repo rollout: none for the audit; future inspect/quick-loot behavior may require Canary support.
- Rollback: revert the documentation commit.

# Remaining work

1. Complete the PR merge gate and archive the task.

# Handoff

## Start here

Read `docs/ui/TIBIA_GLOBAL_OPTIONS_PARITY.md`, then implement Phase 0 before adding new option surface.

## Do not repeat

Do not infer checkbox functionality from the OTUI label alone; inspect the option action and owning module.

## Required reads

- `AGENTS.md`
- `docs/agents/BUILD_TEST_MATRIX.md`
- `docs/ui/TIBIA_GLOBAL_OPTIONS_PARITY.md`
- `modules/client_options/**`
- `modules/game_actionbar/**`
- `modules/game_cooldown/**`

## Open questions

- The first implementation milestone should be selected from Phase 0 after this audit is merged.

# Completion

- Final status: ready, pending PR checks and merge
- PR: `blakinio/otclient#22`
- Merge commit: pending
- Catalogue updated: not required; no reusable interface changed
- Changelog updated: not required; no runtime behavior changed
- Archived at: pending
