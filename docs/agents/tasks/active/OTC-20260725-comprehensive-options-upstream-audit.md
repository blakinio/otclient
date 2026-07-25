---
task_id: OTC-20260725-comprehensive-options-upstream-audit
coordination_id: ""
status: implementation-gate
agent: "GPT-5.6 Thinking"
branch: docs/OTC-20260725-comprehensive-options-audit
base_branch: main
created: 2026-07-25T09:00:00+02:00
updated: 2026-07-25T20:46:00+02:00
last_verified_commit: 3efc9a95ff91f48cc753af3dad024bd45d5137ce
risk: high
related_issue: ""
related_pr: "25"
depends_on:
  - PR 26 final Windows CI and squash merge
blocks:
  - Global-like client parity implementation roadmap
  - deterministic lifecycle repair milestones
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
  - merged client test infrastructure
public_interfaces: []
cross_repo_tasks: []
---

# Goal

Produce a source-grounded and runtime-aware audit of the current client, disposition the exact 16 reviewed `opentibiabr/otclient` commits safely, review `solchanel/otclient-15` selectively, and define the next implementation sequence without weakening Oteryn Identity, tests, security or current Windows-only validation policy.

# Acceptance criteria

- [x] Current client capabilities are classified as present, runtime-proven, CI-proven, source-only, partial, broken, missing or externally dependent.
- [x] The exact 16 reviewed upstream commits are identified and dispositioned one by one.
- [x] Valuable `solchanel/otclient-15` changes, especially Taskboard and protocol 15.22 clues, are reviewed without bulk integration.
- [x] Open upstream issues and recent relevant PRs are triaged against current source.
- [x] External repositories remained read-only.
- [x] Oteryn Identity, no-password fallback, one-shot session semantics, replay protections, shell-safe URL launching, tests and strict asset gates are explicit preservation boundaries.
- [x] A phased implementation plan records dependencies, risks, compatibility, rollout and rollback.
- [x] PR #26 final net changed-file list and full diff were reviewed against current `main`.
- [ ] PR #26 exact-head Windows CI and `CI / Required` succeed.
- [ ] PR #26 squash-merges through branch protection and its squash SHA is recorded.
- [ ] PR #25 is updated to the synchronization result, rebased/current, validated and merged.

# Confirmed context

- Task-start `main`: `715ba210e870304f66b5d5496899c6ea3ca9599d`.
- Reviewed upstream head: `465b7a217e87502bb7f9980bf6e099718d0a9a49`.
- Recorded merge base: `bdea0b23b4a738809d698cb7e4f88a299dd6bffc`.
- The reviewed upstream-only range contains exactly 16 commits.
- Current `main`: `b352c3c5769f8e778085174fb82cb289bcebdd59` after PR #27 and archive PR #29.
- PR #27 established Windows-only required compilation and merged as `fd283c1a6d99dd870f09ee45fdf591541a6f71e9` after CI #210 passed all five Windows jobs and `CI / Required`.
- PR #29 archived the Windows-only task and merged as `b352c3c5769f8e778085174fb82cb289bcebdd59`.
- Open PR #23 owns Oteryn enter-game presentation paths; PR #26 has no net overlap with those paths.
- PR #26 current head is `3efc9a95ff91f48cc753af3dad024bd45d5137ce`, exactly current with `main` (`behind_by: 0`).
- The authoritative `main...head` comparison contains 29 net changed files.
- GitHub's PR file endpoint also lists nine files already present on `main` because explicit base-update merge commits remain in branch history; those files have zero net difference and were reviewed separately.
- Repository settings allow squash merge only. `AGENTS.md` requires repository-supported squash merge, so upstream ancestry will not be used as the durable synchronization mechanism.
- Future synchronization must use the recorded upstream head and per-commit disposition, not assume reviewed upstream SHAs exist in `main` ancestry.

# Existing work to reuse

| Module/task/PR | Reuse | Evidence/path | Why it fits |
|---|---|---|---|
| Global options parity audit | Existing option matrix and known defects | `docs/ui/TIBIA_GLOBAL_OPTIONS_PARITY.md` | Baseline extended rather than duplicated. |
| Oteryn Identity | OAuth Authorization Code + PKCE and one-shot Game Session handoff | `modules/client_entergame/oteryn_identity*.lua`, session guard | Mandatory non-regression boundary. |
| Action bars/keybinds | Existing controls, profiles and persistence | `modules/game_actionbar/**`, `modules/corelib/keybind.lua` | Lifecycle repair is preferred over replacement. |
| Test foundation | C++/Lua fixtures, InputMessage contracts and loopback | `tests/**` | Existing coverage is reused before creating new harnesses. |
| Taskboard parser hooks | `GameTaskboard`, opcode 91 and parser entry points | `src/client/**`, `modules/game_features/**` | Avoids a second protocol model. |
| Windows CI policy | Required Windows build/test matrix | `.github/workflows/ci.yml`, `docs/agents/BUILD_TEST_MATRIX.md` | Final PR #26 gate follows current policy. |

# Ownership and overlap check

- Open relevant PRs inspected: #23, #25 and #26.
- PR #23 overlap: none in the 29-file net diff.
- PR #25 owns audit/task documentation only.
- PR #26 owns the synchronization implementation and local safety adaptations.
- No external repository writes were made.

# Current state

The comprehensive audit report exists in `docs/ui/OTCLIENT_COMPREHENSIVE_AUDIT_AND_PLAN.md` and needs a final factual refresh after PR #26 reaches a terminal state.

PR #26 currently contains the reviewed net effects of the upstream range plus local safety adaptations. Its exact current head is `3efc9a95ff91f48cc753af3dad024bd45d5137ce`. CI #224 (`30170044203`) has passed path detection, workflow/static checks and Lua syntax; the five-job Windows matrix is running.

Three upstream effects are deliberately absent from the final net diff:

1. `src/framework/core/graphicalapplication.cpp` rendering/preload change is deferred because it imported `client/game.h` into framework core, reversing the required dependency direction. Reimplement through `ApplicationDrawEvents` in a focused task.
2. `modules/game_rewardwall/game_rewardwall.lua` source-byte change is deferred because no exact Canary producer commit, shared `OTS-*` contract, compatibility matrix or paired tests were established.
3. `modules/client_assets/client_assets.lua` archive-selection change is deferred because the mandatory installer gate requires release metadata fixtures, install-path proof and runtime-load verification.

Retained changes include NPC trade imbuement quantities and presentation, Stats pause/resume, `--user-dir`, manual-walk/bot coordination, bounded unknown-opcode recovery, pre-780 use-with, ground-border targeting, mount animation, Lua/WebGL compatibility and Cocoa mouse delta. Interactive compatibility is not claimed where it was not exercised.

# Plan

1. Observe CI #224 on exact PR #26 head and inspect any failure before retrying.
2. Reconfirm current-base net diff, comments, reviews and inline threads.
3. Squash-merge PR #26 with an explicit message recording the upstream head, exact 16-commit reviewed range and three excluded effects.
4. Update this task and the comprehensive report with the PR #26 squash SHA and verified final evidence.
5. Update PR #25 to current `main`, mark ready, validate docs-only CI and merge.
6. Archive this task in a focused post-merge documentation PR.
7. Start the highest-priority unblocked repair: character-list recreation, then action-bar cooldown lifecycle, then Wheel/Forge/options repairs.

# Work log

## 2026-07-25T09:00:00+02:00

- Changed: created the audit/synchronization task and dedicated branches.
- Learned: upstream had an exact 16-commit reviewed range touching assets, action bars, NPC trade, reward wall, wheel, protocol, input/platform and framework runtime.
- Result: safety boundaries and read-only external policy recorded.

## 2026-07-25T09:35:00+02:00

- Changed: opened audit PR #25 and local synchronization PR #26.
- Learned: the original range did not overwrite Oteryn login/session/security paths.
- Result: full builds were triggered only after the candidate left draft state.

## 2026-07-25T10:05:00+02:00

- Changed: completed the initial comprehensive audit and phased roadmap.
- Learned: existing Taskboard hooks must be reused; solchanel patches include hard-coded contracts, binary assets and a parser double-read risk.
- Result: deterministic lifecycle/options defects and protocol milestones were prioritized.

## 2026-07-25T20:32:00+02:00

- Changed: PR #27 merged after strict-base refresh and full Windows CI #210; PR #29 then archived its task.
- Learned: a green historical run was insufficient while the branch was behind `main`; strict protection required a current branch and a new exact-head run.
- Result: Windows-only compilation is active on `main`; lightweight Ubuntu checks remain required.

## 2026-07-25T20:40:00+02:00

- Changed: completed patch-level review of PR #26 and added local safety follow-ups.
- Learned: rendering/preload violated framework dependency direction; Reward Wall lacked a paired Canary contract; asset archive selection lacked mandatory installer proof.
- Result: all three net effects were excluded while the reviewed range remained fully documented.

## 2026-07-25T20:42:00+02:00

- Changed: added NPC trader cleanup on module termination and game-session end; catalogued `g_stats.pause/resume`, `--user-dir`, `TargetBot.Danger()` and `lastManualWalk`.
- Learned: tracker cleanup only on NPC close events was insufficient for reload/logout lifecycle.
- Result: current net diff includes idempotent lifecycle cleanup and current public-interface documentation.

## 2026-07-25T20:43:00+02:00

- Failed: a partial-range file read was mistakenly used as complete replacement content for `game_npctrader.lua`, temporarily truncating the branch file.
- Recovery: immediately restored the exact previous blob with a non-forced follow-up commit, then applied the two intended cleanup lines to the verified complete file.
- Result: final net diff contains only eight intended additions and no lost content. Never repeat a full-file update from a ranged fetch.

## 2026-07-25T20:44:00+02:00

- Changed: added then removed a redundant unknown-opcode integration test.
- Learned: existing `tests/unit/framework/inputmessage_test.cpp` already proves reserved-header/body-size semantics and `skipBytes()` reaching EOF.
- Result: parser fix reuses existing contracts; no duplicate harness or redundant test remains.

## 2026-07-25T20:45:00+02:00

- Changed: refreshed PR #26 twice through non-forced synthetic merge commits until `behind_by: 0` against `b352c3c...`.
- Learned: GitHub's PR file endpoint retains nine base-history paths, while authoritative current-base comparison shows 29 net files.
- Result: both views were reviewed and documented.

## 2026-07-25T20:46:00+02:00

- Changed: corrected merge strategy from merge commit to squash.
- Learned: repository settings have `allow_merge_commit=false`, `allow_rebase_merge=false`, `allow_squash_merge=true`; root `AGENTS.md` requires repository-supported squash merge.
- Result: exact upstream head and per-commit disposition become the durable synchronization baseline instead of `main` ancestry.

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| External repositories remain read-only | Highest-priority repository allowlist. | none |
| Synchronize reviewed net effects, not replace the fork branch | Fork contains unique Oteryn, tests, security and governance history. | none |
| Use squash merge for PR #26 | Current repository settings and `AGENTS.md` permit squash only. | none |
| Record upstream head/per-commit disposition as synchronization baseline | Squash does not preserve upstream ancestry in `main`. | none |
| Exclude rendering/preload net effect | Upstream implementation reverses framework → client dependency direction. | none |
| Exclude Reward Wall source-byte net effect | Exact Canary producer/consumer contract and paired tests are missing. | none |
| Exclude asset archive-selection net effect | Mandatory installer fixtures, path and runtime-load evidence are missing. | none |
| Retain bounded unknown-opcode recovery | Existing InputMessage tests prove the framing primitive; final Windows tests cover compiled integration. | none |
| Do not bulk-merge `solchanel/otclient-15` | Heavy divergence, binary assets, hard-coded contracts and parser risk. | none |
| Separate deterministic repairs from modern protocol work | Client lifecycle defects can be tested locally; payload changes require exact Canary pairs. | none |

# Files and interfaces

| Path/interface/config/schema | Purpose | Status |
|---|---|---|
| `docs/ui/OTCLIENT_COMPREHENSIVE_AUDIT_AND_PLAN.md` | Capability matrix, upstream disposition and delivery roadmap | refresh pending PR #26 terminal result |
| task record | Coordination, failures, decisions and handoff | current |
| PR #26 29-file net diff | Reviewed synchronization result | exact-head CI running |
| `g_stats.pause()` / `g_stats.resume()` | Lua-visible Stats collection controls | catalogued in PR #26 |
| `--user-dir=<path>` | Persisted-state directory override | catalogued in PR #26 |
| `TargetBot.Danger()` / `lastManualWalk` | Optional bot/manual-input coordination | catalogued in PR #26 |

# Validation and CI

| Commit/run | Check | Result | Evidence/notes |
|---|---|---|---|
| `943428f0ef2c2791355f6a408c3fbc9d2abf6afb` | Initial audit source/path/issue review | PASS | Evidence levels avoid unsupported runtime claims. |
| `7bcf57bb3eae419db8ac462d7053ce5cd43e264e` | Historical full cross-platform CI | PASS | Supporting evidence for unchanged retained upstream effects; not final merge gate. |
| `fd283c1a6d99dd870f09ee45fdf591541a6f71e9` | PR #27 Windows-only policy | PASS | CI #210: five Windows jobs and `CI / Required` succeeded. |
| `b352c3c5769f8e778085174fb82cb289bcebdd59` | PR #29 task archive | PASS | Docs-only CI #221 and Required succeeded. |
| `3efc9a95ff91f48cc753af3dad024bd45d5137ce` | Current-base compare/full diff | PASS | 29 net files; three deferred files absent; no Oteryn auth/session paths. |
| same | PR comments/reviews/threads | PASS at last inspection | No comments, reviews or unresolved inline threads. Recheck before merge. |
| CI #224 / `30170044203` | Fast checks and Lua syntax | PASS | Windows matrix running. |
| CI #224 / `30170044203` | Five Windows jobs and Required | RUNNING | Do not mark passed until terminal success. |

# Failed approaches and dead ends

- Direct container cloning was unavailable because GitHub DNS resolution failed; connector-backed source and CI remain authoritative.
- Draft CI with skipped builds was not accepted as final evidence.
- The first PR #27 merge attempt failed because the branch was behind strict `main`; updating the branch and rerunning exact-head CI resolved it.
- A ranged fetch was incorrectly treated as a complete file during one NPC trader update; the exact blob was restored immediately. Never use ranged content for full replacement.
- A redundant integration test was removed after existing unit contracts were found.
- Merge-commit preservation of upstream ancestry is impossible under current repository settings and is not permitted as an excuse to bypass squash policy.
- Solchanel `0053457` and `c3f3d14` remain unsafe wholesale due superseded changes, hard-coded gates and parser double-read risk.

# Risks and compatibility

- Runtime: high; retained changes touch protocol, NPC trade, Wheel, action bars, platform and diagnostics.
- Data/migration: `--user-dir` changes persisted-state location only when explicitly supplied.
- Security: Oteryn auth/session/url-launch and strict asset behavior remain mandatory invariants.
- Backward compatibility: pre-780 use-with needs focused old-protocol runtime/fixture follow-up.
- Protocol: Reward Wall remains unchanged until exact Canary pairing exists.
- Assets: archive selection remains unchanged until mandatory installer evidence exists.
- Architecture: renderer/preload ordering remains unchanged until dependency-safe implementation exists.
- Platform: current final gate compiles Windows only; historical browser/macOS evidence is supporting, not a current compatibility claim.
- Rollback: PR #26 squash is one revertible synchronization commit; deferred effects remain separate future tasks.

# Remaining work

1. Complete CI #224 and PR #26 squash merge gate.
2. Finalize and merge PR #25 documentation with exact PR #26 result.
3. Archive this task after PR #25 merge.
4. Execute character-list recreation repair.
5. Execute action-bar cooldown lifecycle repair.
6. Execute Wheel/Forge/options deterministic repairs.
7. Start modern 15.24/15.25 contracts only with exact Canary pairs.

# Handoff

## Start here

1. Inspect PR #26 exact head `3efc9a95ff91f48cc753af3dad024bd45d5137ce` and CI #224 (`30170044203`).
2. On failure, inspect the exact job log and repair only in `blakinio/otclient`.
3. On success, recheck the authoritative 29-file `main...head` diff, PR comments/reviews/threads and mergeability.
4. Squash-merge PR #26 with expected head SHA and a message naming upstream head `465b7a217e87502bb7f9980bf6e099718d0a9a49`, the exact 16-commit reviewed range and the three excluded effects.
5. Update this task/report with the squash SHA before finalizing PR #25.

## Do not repeat

- Do not bulk-merge solchanel.
- Do not copy Taskboard/CipSoft-like binary assets.
- Do not infer protocol correctness from compilation.
- Do not restore the three deferred effects without their specific gates.
- Do not treat GitHub's historical 38-file PR view as the net squash diff; compare current `main...head`.
- Do not use ranged fetch output as complete replacement file content.
- Do not bypass squash-only repository policy.

## Required reads

- `AGENTS.md`
- `docs/agents/BUILD_TEST_MATRIX.md`
- `docs/agents/CROSS_REPO_CONTRACTS.md`
- `docs/ui/TIBIA_GLOBAL_OPTIONS_PARITY.md`
- `docs/ui/OTCLIENT_COMPREHENSIVE_AUDIT_AND_PLAN.md`
- PR #26 current-base compare, full diff and CI #224

## Open questions

- Final CI and squash SHA of PR #26.
- Exact Canary revision for the modern protocol milestone.
- Exact Canary producer/consumer contract for Reward Wall source semantics.

# Completion

- Final status: in progress; PR #26 exact-head Windows CI running
- Audit PR: `blakinio/otclient#25`
- Synchronization PR: `blakinio/otclient#26`
- Synchronization squash commit: pending
- Catalogue updated: yes in PR #26
- Changelog updated: pending final synchronization documentation
- Archived at: pending PR #25 merge
