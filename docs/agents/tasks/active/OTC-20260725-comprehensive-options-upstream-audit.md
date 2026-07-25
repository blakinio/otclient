---
task_id: OTC-20260725-comprehensive-options-upstream-audit
coordination_id: ""
status: discovery
agent: "GPT-5.6 Thinking"
branch: docs/OTC-20260725-comprehensive-options-audit
base_branch: main
created: 2026-07-25T09:00:00+02:00
updated: 2026-07-25T09:00:00+02:00
last_verified_commit: 715ba210e870304f66b5d5496899c6ea3ca9599d
risk: high
related_issue: ""
related_pr: ""
depends_on: []
blocks:
  - Global-like client parity implementation roadmap
owned_paths:
  - docs/agents/tasks/active/OTC-20260725-comprehensive-options-upstream-audit.md
  - docs/ui/OTCLIENT_COMPREHENSIVE_AUDIT_AND_PLAN.md
modules_touched:
  - client options and GUI
  - protocol and game feature consumers
  - action bars and hotkeys
  - assets installer
  - platform/runtime framework
reuses:
  - docs/ui/TIBIA_GLOBAL_OPTIONS_PARITY.md
  - modules/client_options
  - modules/game_actionbar
  - modules/corelib/keybind.lua
  - modules/game_cooldown
  - Oteryn Identity native login
  - existing test infrastructure
public_interfaces: []
cross_repo_tasks: []
---

# Goal

Produce a comprehensive, source-grounded and runtime-aware audit of the current client, synchronize the exact 16 missing `opentibiabr/otclient` commits safely, review `solchanel/otclient-15` for selectively valuable Taskboard and protocol 15.22 work, and triage upstream issues/PRs without weakening Oteryn Identity, tests or security.

# Acceptance criteria

- [ ] Current client capabilities are classified as present, runtime-proven, source-only, partial, broken, missing or externally dependent.
- [ ] The exact 16 commits missing from `opentibiabr/otclient` are identified and dispositioned one by one.
- [ ] Selected upstream changes are integrated only into `blakinio/otclient` and validated.
- [ ] Valuable changes from `solchanel/otclient-15`, especially Taskboard and protocol 15.22, are reviewed and dispositioned.
- [ ] Open upstream issues and recent relevant pull requests are triaged against our current source.
- [ ] No write is made to `opentibiabr/otclient`, `solchanel/otclient-15` or any other external repository.
- [ ] Oteryn Identity, no-password-fallback behavior, one-shot session semantics, replay protections, shell-safe URL launching, tests and security fixes are preserved.
- [ ] Any selected code changes have focused tests and current-head CI evidence.
- [ ] A phased implementation plan includes dependencies, risks, compatibility, rollout and rollback.
- [ ] Full changed-file and diff review completed.
- [ ] Autonomous merge gate satisfied or a concrete blocker is recorded.

# Confirmed context

- Current `main` was verified at `715ba210e870304f66b5d5496899c6ea3ca9599d` at task start.
- `opentibiabr/otclient:main` is exactly 16 commits ahead and 21 commits behind our `main`; merge base is `bdea0b23b4a738809d698cb7e4f88a299dd6bffc`.
- Open PR #23 owns Oteryn enter-game presentation paths and must not be overwritten or duplicated.
- `opentibiabr/otclient` and `solchanel/otclient-15` are read-only sources for this task.
- User explicitly requested no pushes or writes to external repositories.
- The existing Global options audit is source-only and does not prove runtime behavior.

# Existing work to reuse

| Module/task/PR | Reuse | Evidence/path | Why it fits |
|---|---|---|---|
| Global options parity audit | Existing option matrix and known defects | `docs/ui/TIBIA_GLOBAL_OPTIONS_PARITY.md` | Baseline to extend with runtime evidence and wider client scope. |
| Oteryn Identity | OAuth Authorization Code + PKCE and one-shot game-session handoff | `modules/client_entergame/oteryn_identity*.lua`, session guard, platform URL fixes | Must be preserved through every upstream integration. |
| Action bars/keybinds | Existing Global-like controls and persistence | `modules/game_actionbar/**`, `modules/corelib/keybind.lua` | Strong existing parity; do not replace with older/incompatible code. |
| Test foundation | Existing C++/Lua fixtures and protocol loopback | `tests/**` and active/merged test work | Reuse for regression coverage. |

# Ownership and overlap check

- Open PRs inspected: #23 (`modules/client_entergame/**` presentation only).
- Overlap: possible upstream changes to enter-game, action-bar, assets, protocol and framework files.
- Resolution: do not edit PR #23-owned presentation paths; preserve current auth and security behavior; inspect all overlapping patches before integration.

# Current state

Discovery is in progress. No upstream source commit has been applied yet.

# Plan

1. Build exact per-commit disposition for the 16 upstream commits.
2. Triage open upstream issues and recent merged PRs by severity, reproducibility, affected paths and relevance.
3. Audit `solchanel/otclient-15` Taskboard and protocol 15.22 changes against current client and Canary contracts.
4. Expand the options audit into a complete client capability, wiring, persistence, test and dependency matrix.
5. Integrate only selected safe changes into a dedicated implementation branch/PR, preserving Oteryn-specific work.
6. Add focused tests and run proportional validation, then final current-head CI.
7. Publish the durable audit and phased repair roadmap.

# Work log

## 2026-07-25T09:00:00+02:00

- Changed: created a dedicated audit/synchronization branch and task record.
- Learned: upstream is exactly 16 commits ahead; the delta touches assets, action bars, NPC trade, reward wall, wheel, protocol parsing, input/platform and framework runtime.
- Failed/blocked: none yet.
- Result: discovery scope and safety boundaries recorded.

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| External repositories are read-only | Explicit user instruction and repository allowlist. | none |
| Do not bulk-merge upstream blindly | Our fork is 21 commits ahead with auth, tests and security changes; per-commit review is required. | none |
| Separate source presence from runtime proof | Existing audit did not compile or exercise the client. | none |

# Files and interfaces

| Path/interface/config/schema | Purpose | Status |
|---|---|---|
| `docs/ui/OTCLIENT_COMPREHENSIVE_AUDIT_AND_PLAN.md` | Complete matrix, upstream disposition and roadmap | planned |
| task record | Coordination, evidence and handoff | active |

# Validation and CI

| Commit | Command/check/workflow | Result | Evidence/notes |
|---|---|---|---|
| pending | Source/commit/issue/PR review | not-run | Discovery in progress. |

Never write `passed` without verification.

# Failed approaches and dead ends

# Risks and compatibility

- Runtime: high; upstream touches protocol, rendering, action bars and platform behavior.
- Data/migration: settings and assets selection may change.
- Security: auth/session/url-launch protections must not regress.
- Backward compatibility: protocol/version-specific changes require explicit gates.
- Cross-repo rollout: protocol payload changes may require exact Canary pairing.
- Rollback: each selected upstream change must be independently revertible or grouped by coherent dependency.

# Remaining work

1. Complete exact upstream commit and issue/PR triage.

# Handoff

## Start here

Read this task, `docs/ui/TIBIA_GLOBAL_OPTIONS_PARITY.md`, the 16-commit comparison, open PR #23 and current security/auth contracts.

## Do not repeat

Do not bulk-merge or overwrite Oteryn-specific files without patch-level comparison.

## Required reads

- `AGENTS.md`
- `docs/agents/BUILD_TEST_MATRIX.md`
- `docs/agents/CROSS_REPO_CONTRACTS.md`
- `docs/ui/TIBIA_GLOBAL_OPTIONS_PARITY.md`

## Open questions

- Final disposition of each upstream commit and each solchanel candidate.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Catalogue updated: pending determination
- Changelog updated: pending determination
- Archived at: pending
