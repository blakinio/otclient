---
task_id: OTC-20260725-comprehensive-options-upstream-audit
coordination_id: ""
status: implementation-gate
agent: "GPT-5.6 Thinking"
branch: docs/OTC-20260725-comprehensive-options-audit
base_branch: main
created: 2026-07-25T09:00:00+02:00
updated: 2026-07-25T10:05:00+02:00
last_verified_commit: 943428f0ef2c2791355f6a408c3fbc9d2abf6afb
risk: high
related_issue: ""
related_pr: "25"
depends_on:
  - PR 26 upstream synchronization validation
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

Produce a comprehensive, source-grounded and runtime-aware audit of the current client, synchronize the exact 16 missing `opentibiabr/otclient` commits safely, review `solchanel/otclient-15` for selectively valuable Taskboard and protocol 15.22 work, and triage upstream issues/PRs without weakening Oteryn Identity, tests or security.

# Acceptance criteria

- [x] Current client capabilities are classified as present, runtime-proven, source-only, partial, broken, missing or externally dependent.
- [x] The exact 16 commits missing from `opentibiabr/otclient` are identified and dispositioned one by one.
- [ ] Selected upstream changes are integrated only into `blakinio/otclient` and validated.
- [x] Valuable changes from `solchanel/otclient-15`, especially Taskboard and protocol 15.22, are reviewed and dispositioned.
- [x] Open upstream issues and recent relevant pull requests are triaged against current source.
- [x] No write was made to `opentibiabr/otclient`, `solchanel/otclient-15` or any other external repository.
- [x] Oteryn Identity, no-password-fallback behavior, one-shot session semantics, replay protections, shell-safe URL launching, tests and security fixes are explicit preservation gates.
- [ ] Selected code changes have current-head CI evidence; focused regression tests remain scheduled in the repair phases.
- [x] A phased implementation plan includes dependencies, risks, compatibility, rollout and rollback.
- [ ] Full changed-file and diff review completed for the final synchronization head.
- [ ] Autonomous merge gate satisfied or a concrete blocker is recorded.

# Confirmed context

- Current `main` was verified at `715ba210e870304f66b5d5496899c6ea3ca9599d` at task start.
- `opentibiabr/otclient:main` is exactly 16 commits ahead and 21 commits behind our starting `main`; merge base is `bdea0b23b4a738809d698cb7e4f88a299dd6bffc`.
- Open PR #23 owns Oteryn enter-game presentation paths and is not modified by the synchronization candidate.
- `opentibiabr/otclient` and `solchanel/otclient-15` were used read-only.
- The previous Global options audit was source-only and did not prove runtime behavior.
- Merged PR #3 supplies the deterministic C++/Lua/protocol test foundation; catalogue references calling it active are stale.
- Merged PR #17 supplies Oteryn Identity and no-password-fallback behavior.
- PR #26 is a local merge candidate in `blakinio/otclient` containing current `main` plus the exact 16 upstream commits.

# Existing work to reuse

| Module/task/PR | Reuse | Evidence/path | Why it fits |
|---|---|---|---|
| Global options parity audit | Existing option matrix and known defects | `docs/ui/TIBIA_GLOBAL_OPTIONS_PARITY.md` | Baseline extended by the comprehensive report. |
| Oteryn Identity | OAuth Authorization Code + PKCE and one-shot Game Session handoff | `modules/client_entergame/oteryn_identity*.lua`, session guard, platform URL fixes | Mandatory non-regression boundary. |
| Action bars/keybinds | Existing Global-like controls and persistence | `modules/game_actionbar/**`, `modules/corelib/keybind.lua` | Reused; lifecycle repaired rather than replaced. |
| Test foundation | C++/Lua fixtures and protocol loopback | `tests/**` | Required for follow-up regressions. |
| Existing Taskboard parser hooks | `GameTaskboard`, opcode 91 and `parseTaskBoard*` declarations/callbacks | `src/client/**`, `modules/game_features/**` | Avoids creating a second protocol model. |

# Ownership and overlap check

- Open PRs inspected: #23, #25 and #26.
- PR #23 overlap: none in the PR #26 changed-file list; its enter-game presentation paths remain untouched.
- PR #25 owns audit documentation only.
- PR #26 owns the exact synchronization candidate and is not merged until full builds and review complete.

# Current state

The comprehensive report is complete in `docs/ui/OTCLIENT_COMPREHENSIVE_AUDIT_AND_PLAN.md`. It records current capability evidence, known deterministic defects, all 16 upstream dispositions, selective solchanel decisions, upstream issue triage, security invariants, test gates and a six-phase delivery roadmap.

The exact upstream merge candidate is PR #26 at `7bcf57bb3eae419db8ac462d7053ce5cd43e264e`. It changes 31 files, does not touch Oteryn authentication/session/security files, is mergeable and is running full ready-for-review CI. The earlier draft runs passed fast checks but intentionally skipped builds and are not sufficient evidence.

# Plan

1. Observe full CI run on PR #26 and inspect any failed job/log.
2. Review PR #26 full diff and final changed-file list after CI stabilizes.
3. Merge PR #26 only when all required build/test gates pass.
4. Rebase/update PR #25 if required, finalize audit validation and merge the durable report.
5. Start focused repair PRs in this order: character-list recreation, action-bar cooldown lifecycle, Wheel/Forge/options deterministic defects, then modern 15.24/15.25 protocol contracts.
6. Begin Taskboard only after parser/Canary contracts and asset provenance are closed.

# Work log

## 2026-07-25T09:00:00+02:00

- Changed: created a dedicated audit/synchronization branch and task record.
- Learned: upstream is exactly 16 commits ahead; the delta touches assets, action bars, NPC trade, reward wall, wheel, protocol parsing, input/platform and framework runtime.
- Failed/blocked: none.
- Result: discovery scope and safety boundaries recorded.

## 2026-07-25T09:35:00+02:00

- Changed: opened draft audit PR #25 and local-only synchronization candidate PR #26.
- Learned: the 16-commit diff does not touch Oteryn login, session guards, auth tests or shell-safe URL implementation.
- Failed/blocked: draft CI skipped builds by design.
- Result: candidate was marked ready only after source/change review so full platform builds would run.

## 2026-07-25T10:05:00+02:00

- Changed: added the comprehensive audit and phased roadmap.
- Learned: current client already has Taskboard protocol identifiers/parsers and modern client-event screenshot parsing, but lacks complete user-facing modules/services. Solchanel protocol commits are partially superseded and contain unsafe examples, including a double-read risk; Taskboard cannot be bulk-ported with its binary assets and hard-coded economy values.
- Learned: deterministic defects include character-list relative OTUI recreation, action-bar cooldown lifecycle, Wheel conviction indices, Forge timer lifetime and previous option wiring defects.
- Failed/blocked: PR #26 full CI is still running.
- Result: audit acceptance criteria are complete except synchronization integration/final validation.

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| External repositories remain read-only | Explicit user instruction and repository allowlist. | none |
| Synchronize through a local merge candidate, not branch replacement | Our fork contains 21 unique commits with auth/tests/security work. | none |
| Accept the 16 upstream commits as a coherent candidate, subject to full CI and contract-specific follow-ups | Per-commit review found no direct auth/security overwrite; changes are focused and useful. | none |
| Do not bulk-merge `solchanel/otclient-15` | It diverges heavily, includes binary assets, hard-coded contracts and at least one parser double-read risk. | none |
| Reuse existing Taskboard parser hooks | Current source already declares Taskboard opcode/feature/parser entry points. | none |
| Separate deterministic fixes from modern protocol work | Lifecycle/UI defects can be tested client-side; payload changes require exact Canary pairs. | none |

# Files and interfaces

| Path/interface/config/schema | Purpose | Status |
|---|---|---|
| `docs/ui/OTCLIENT_COMPREHENSIVE_AUDIT_AND_PLAN.md` | Complete matrix, upstream disposition and roadmap | complete |
| task record | Coordination, evidence and handoff | active |
| PR #26 changed files | Exact upstream synchronization | validation in progress |

# Validation and CI

| Commit | Command/check/workflow | Result | Evidence/notes |
|---|---|---|---|
| `943428f0ef2c2791355f6a408c3fbc9d2abf6afb` | Audit source/path/issue/commit review | PASS | Report includes evidence levels and avoids runtime claims without proof. |
| `7bcf57bb3eae419db8ac462d7053ce5cd43e264e` | Draft CI runs | PASS, insufficient | Fast checks/Lua passed; builds skipped because PR was draft. |
| `7bcf57bb3eae419db8ac462d7053ce5cd43e264e` | Ready-for-review full CI | running | Linux/tests, Windows variants, macOS, browser and Docker required according to changed paths. |

Never write `passed` without verification.

# Failed approaches and dead ends

- Direct container cloning remains unavailable because DNS cannot resolve GitHub; connector-backed source and CI are authoritative.
- An initial branch directly at upstream head caused draft scope checks to be misleading. The branch was moved to GitHub's local merge candidate containing our `main` and upstream, then marked ready to trigger real builds.
- Solchanel `0053457` and `c3f3d14` cannot be cherry-picked safely: current code already supersedes several changes, while the patches include no-op parsing, hard-coded gates and a Cyclopedia field double-read risk.

# Risks and compatibility

- Runtime: high; upstream touches protocol, rendering, action bars and platform behavior.
- Data/migration: settings and asset archive selection may change.
- Security: auth/session/url-launch and strict asset hash protections are mandatory invariants.
- Backward compatibility: pre-780 use-with and modern Taskboard/Reward Wall require version-specific tests.
- Cross-repo rollout: Reward Wall and all 15.24/15.25 payload changes require exact Canary pairing.
- Asset licensing: Taskboard graphics from third-party forks are not accepted without provenance; original Oteryn assets are required.
- Rollback: PR #26 is one coherent upstream synchronization; subsequent defect fixes remain narrow and independently revertible.

# Remaining work

1. Complete PR #26 full CI and merge gate.
2. Finalize and merge PR #25 documentation after the synchronization result is known.
3. Execute the immediate repair sequence recorded in the report.

# Handoff

## Start here

1. Inspect PR #26 workflow run on head `7bcf57bb3eae419db8ac462d7053ce5cd43e264e`.
2. On failure, inspect the exact job log and repair only in `blakinio/otclient`.
3. On success, review changed files/full diff, merge PR #26, then update this report/task with the squash SHA.

## Do not repeat

- Do not bulk-merge solchanel.
- Do not copy Taskboard/CipSoft-like binary assets.
- Do not infer protocol correctness from a parser compiling.
- Do not treat draft CI with skipped builds as final validation.
- Do not overwrite PR #23 enter-game presentation work.

## Required reads

- `AGENTS.md`
- `docs/agents/BUILD_TEST_MATRIX.md`
- `docs/agents/CROSS_REPO_CONTRACTS.md`
- `docs/ui/TIBIA_GLOBAL_OPTIONS_PARITY.md`
- `docs/ui/OTCLIENT_COMPREHENSIVE_AUDIT_AND_PLAN.md`
- PR #26 diff and CI

## Open questions

- Final CI and merge result of PR #26.
- Exact Canary revision for the modern protocol milestone.

# Completion

- Final status: in progress; synchronization CI gate pending
- Audit PR: `blakinio/otclient#25`
- Synchronization PR: `blakinio/otclient#26`
- Merge commit: pending
- Catalogue updated: pending synchronization completion/stale-state cleanup
- Changelog updated: pending synchronization completion
- Archived at: pending
