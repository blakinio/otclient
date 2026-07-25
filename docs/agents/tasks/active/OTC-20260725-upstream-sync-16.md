---
task_id: OTC-20260725-upstream-sync-16
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
branch: sync/OTC-20260725-opentibiabr-16-commits
base_branch: main
created: 2026-07-25T22:33:32+02:00
updated: 2026-07-25T22:33:32+02:00
last_verified_commit: "f89b0299cad683045f809d7fafd969f376fb00bc"
risk: high
related_issue: ""
related_pr: "#26"
depends_on: []
blocks:
  - OTC-20260725-comprehensive-options-upstream-audit
owned_paths:
  - Dockerfile.browser
  - docs/agents/CHANGELOG.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/tasks/active/OTC-20260725-upstream-sync-16.md
  - mods/game_bot/default_configs/cavebot_1.3/targetbot/target.lua
  - modules/game_actionbar/logics/MultiActionLogic.lua
  - modules/game_interface/gameinterface.lua
  - modules/game_npctrade/**
  - modules/game_shaders/shaders/fragment/text_glow.frag
  - modules/game_walk/walk.lua
  - modules/game_wheel/classes/**
  - src/CMakeLists.txt
  - src/client/creature.cpp
  - src/client/game.cpp
  - src/client/game.h
  - src/client/luafunctions.cpp
  - src/client/protocolgameparse.cpp
  - src/client/tile.cpp
  - src/framework/core/resourcemanager.cpp
  - src/framework/core/resourcemanager.h
  - src/framework/luafunctions.cpp
  - src/framework/platform/cocoawindow.mm
  - src/framework/util/stats.cpp
  - src/framework/util/stats.h
  - src/main.cpp
modules_touched:
  - game_actionbar
  - game_interface
  - game_npctrade
  - game_walk
  - game_wheel
reuses:
  - existing InputMessage body-size and EOF contracts
  - existing Oteryn Identity and one-shot session guards
  - existing Windows-only CI graph
public_interfaces:
  - g_stats.pause
  - g_stats.resume
  - g_game.getLastManualWalk
  - TargetBot.Danger
cross_repo_tasks: []
---

# Goal

Synchronize the reviewed net effects of the exact 16 upstream commits through `465b7a217e87502bb7f9980bf6e099718d0a9a49` without weakening Oteryn architecture, authentication, protocol or asset-installation gates.

# Acceptance criteria

- [x] Exact upstream merge base, head and 16-commit range recorded.
- [x] Full net diff against current `main` reviewed.
- [x] Framework-to-client dependency reversal excluded.
- [x] Reward Wall payload change excluded pending an exact Canary producer and `OTS-*` contract.
- [x] Asset archive-selection change excluded pending fixtures and runtime-path evidence.
- [x] Oteryn Identity, no-password-fallback and one-shot Game Session behavior preserved.
- [x] Module catalogue and changelog updated for retained interfaces and behavior.
- [ ] Required checks pass on the exact final head after this task record is added.
- [ ] Autonomous merge gate satisfied and task archived with squash SHA.

# Confirmed context

- Current `main`: `85bfac8825607a73b475f1267cb3a798da1e717d`.
- Reviewed upstream head: `465b7a217e87502bb7f9980bf6e099718d0a9a49`.
- Recorded common ancestor: `bdea0b23b4a738809d698cb7e4f88a299dd6bffc`.
- Prior reviewed PR head: `f89b0299cad683045f809d7fafd969f376fb00bc`.
- Current comparison is diverged by one documentation-only `main` commit, but the authoritative tree comparison contains no net difference for that archived task file; the 30-file feature net diff remains unchanged.
- Repository settings permit squash merge only.
- Windows is the only compiled and required target.

# Existing work to reuse

| Module/task/PR | Reuse | Evidence/path | Why it fits |
|---|---|---|---|
| PR #26 reviewed synchronization | Existing 30-file net diff | live PR and `main...head` comparison | Avoids repeating the 16-commit review. |
| InputMessage tests | body-size/EOF invariants | existing test foundation | Covers bounded skip-to-EOF behavior without duplicating the harness. |
| Oteryn auth implementation | fail-closed identity/session boundary | `modules/client_entergame/oteryn_identity*.lua`, session guard | Must remain untouched by synchronization. |

# Ownership and overlap check

- Open PRs inspected: #23, #25, #26.
- Active task evidence inspected: live PR task references and current task paths.
- Overlaps: #23 owns `modules/client_entergame/**`; #25 owns audit documentation; neither owns this runtime diff.
- Resolution: this task owns only the synchronization paths listed above and blocks the final audit update until merge state is known.

# Current state

PR #26 is open, non-draft, mergeable and has no review threads or submitted reviews. Its prior exact head passed workflow run `30170445507`, but this task-record commit intentionally creates a new final head so required CI is re-evaluated after the latest `main` state was verified.

# Plan

1. Add this durable task record and let CI validate the resulting exact head.
2. Review the final changed-file list, workflow jobs and any logs.
3. Repair root causes without weakening checks.
4. Squash-merge only after the full gate passes.
5. Archive this task in a separate post-merge PR recording the squash SHA and upstream baseline.

# Work log

## 2026-07-25T22:33:32+02:00

- Changed: created a dedicated task record for PR #26.
- Learned: current `main` is one commit ahead in ancestry, but no current-main file content is missing from the PR tree; the net synchronization diff remains exactly 30 files before this task file.
- Failed/blocked: connector does not expose a branch-update merge operation; no content conflict exists and GitHub reports the PR mergeable.
- Result: new exact head will receive a fresh CI run.

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| Keep the three deferred upstream effects excluded | Each violates an explicit architecture or evidence gate | none |
| Use squash merge | Repository allows squash only and `AGENTS.md` requires repository policy | none |
| Do not create duplicate unknown-opcode tests | Existing tests already prove body size and skip-to-EOF contracts | none |

# Files and interfaces

| Path/interface/config/schema | Purpose | Status |
|---|---|---|
| 30-file reviewed net synchronization diff | Retain accepted upstream behavior | implemented |
| `docs/agents/tasks/active/OTC-20260725-upstream-sync-16.md` | Ownership, evidence and handoff | implemented |
| `g_stats.pause/resume` and Lua bindings | Stats lifecycle control | implemented |
| `--user-dir` | Explicit writable user directory selection | implemented |
| bounded unknown-opcode recovery | End malformed/unsupported packet handling without looping | implemented |

# Validation and CI

| Commit | Command/check/workflow | Result | Evidence/notes |
|---|---|---|---|
| `f89b0299cad683045f809d7fafd969f376fb00bc` | CI run `30170445507` | success | Supporting evidence only; predates this task-record commit. |
| pending | `CI / Required` on exact final head | not-run | Required merge gate. |

Never write `passed` without verification.

# Failed approaches and dead ends

- A local clone was attempted for an independent worktree preflight, but the sandbox has no DNS access to GitHub. Live GitHub connector state is used instead.
- The connector has no merge-base/update-branch mutation and GitHub rejects commit SHAs where tree-object SHAs are required. No force update or fabricated tree was used.

# Risks and compatibility

- Runtime: several retained behaviors have compile coverage but no fresh interactive Windows gameplay evidence in this environment.
- Data/migration: `--user-dir` changes resource-location behavior only when explicitly supplied.
- Security: Oteryn authentication and one-shot session paths are outside the diff; deferred asset/Reward Wall effects remain fail-closed.
- Backward compatibility: pre-780 use-with and ground-border targeting are intentionally retained from reviewed upstream behavior.
- Cross-repo rollout: no Canary contract is changed by accepted effects; Reward Wall remains deferred because the exact producer is unknown.
- Rollback: squash revert of PR #26 restores the pre-sync fork state.

# Remaining work

1. Inspect and satisfy required CI on the new exact head.

# Handoff

## Start here

Open PR #26, verify the current head created by this task file, inspect all jobs and compare it against current `main`.

## Do not repeat

Do not re-import the excluded framework dependency reversal, Reward Wall payload change or unproven asset archive-selection change.

## Required reads

- `AGENTS.md`
- `docs/agents/README.md`
- `docs/architecture/OTERYN_CLIENT_ARCHITECTURE.md`
- `docs/agents/OTERYN_WORKSTREAM_MAP.md`
- `docs/agents/BUILD_TEST_MATRIX.md`
- PR #26 full diff and checks

## Open questions

- None for the accepted synchronization package.

# Completion

- Final status: in progress
- PR: #26
- Merge commit: pending
- Catalogue updated: yes
- Changelog updated: yes
- Archived at: pending
