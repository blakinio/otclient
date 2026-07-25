---
task_id: OTC-20260725-upstream-sync-16
coordination_id: ""
status: complete
agent: "GPT-5.6 Thinking"
branch: sync/OTC-20260725-opentibiabr-16-commits
base_branch: main
created: 2026-07-25T22:33:32+02:00
updated: 2026-07-26T00:55:42+02:00
last_verified_commit: "38ef14010cc01b16824dd646022c6f5d3ba93146"
risk: high
related_issue: ""
related_pr: "#26"
depends_on: []
blocks: []
owned_paths: []
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
- [x] Required checks passed on the exact final head.
- [x] Autonomous merge gate satisfied and squash SHA verified.

# Final state

PR #26 was squash-merged to `main` as `38ef14010cc01b16824dd646022c6f5d3ba93146` after the exact refreshed head `4f9958c5b834e911e06ffb5e10f1193400f545e7` passed CI run `30176493622`.

The accepted synchronization retained:

- NPC trade imbuement quantities and lifecycle cleanup;
- Stats pause/resume and manual-walk/bot helpers;
- animated outfit/mount phase fixes;
- `--user-dir`, pre-780 use-with and ground-border targeting;
- bounded unknown-opcode recovery;
- reviewed browser/WASM and Cocoa source fixes without making new dormant-platform support claims.

The following upstream effects remain deliberately excluded:

1. renderer/preload ordering that would reverse the framework-to-client dependency direction;
2. Reward Wall source-byte semantics without an exact Canary producer and shared `OTS-*` contract;
3. asset release-archive selection without release fixtures, final-path verification and runtime-load proof.

# Validation and CI

| Commit | Workflow/check | Result | Evidence |
|---|---|---|---|
| `f89b0299cad683045f809d7fafd969f376fb00bc` | CI `30170445507` | success | supporting pre-task evidence |
| `c9dba184328250b3550386565e3d15bf8f73ea49` | CI `30173862455` | success | first exact task-record head |
| `4f9958c5b834e911e06ffb5e10f1193400f545e7` | CI `30176493622` | success | refreshed exact merge head; five Windows variants, CTest, Fast Checks, Lua Syntax and `CI / Required` |
| `38ef14010cc01b16824dd646022c6f5d3ba93146` | PR #26 squash merge | verified | final `main` result |

# Risks and compatibility

- Several retained gameplay behaviors have compile/test evidence but no fresh interactive Windows gameplay evidence in this environment.
- Oteryn authentication, no-password fallback and one-shot Game Session paths were outside the synchronization diff.
- The three deferred effects remain fail-closed and require focused future tasks.
- Rollback is a normal revert of squash commit `38ef14010cc01b16824dd646022c6f5d3ba93146`.

# Handoff

- Continue from `main` at or after `38ef14010cc01b16824dd646022c6f5d3ba93146`.
- Do not re-import the excluded framework dependency reversal, Reward Wall payload change or unproven asset archive-selection change.
- The comprehensive audit and the character-list recreation repair may now treat the synchronization dependency as complete.

# Completion

- Final status: complete
- PR: #26
- Merge commit: `38ef14010cc01b16824dd646022c6f5d3ba93146`
- Catalogue updated: yes
- Changelog updated: yes
- Archived at: 2026-07-26T00:55:42+02:00
