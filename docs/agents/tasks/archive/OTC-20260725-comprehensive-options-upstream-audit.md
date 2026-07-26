---
task_id: OTC-20260725-comprehensive-options-upstream-audit
coordination_id: ""
status: completed
agent: "GPT-5.6 Thinking"
branch: docs/OTC-20260725-comprehensive-options-audit
base_branch: main
created: 2026-07-25T09:00:00+02:00
updated: 2026-07-26T08:23:30+02:00
last_verified_commit: "6e30c340c26f3d1fdb1ffacb17cc30a172392dca"
risk: high
related_issue: ""
related_pr: "#25"
depends_on: []
blocks: []
owned_paths:
  - docs/agents/tasks/archive/OTC-20260725-comprehensive-options-upstream-audit.md
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

Produce a source-grounded and runtime-aware audit of the current client, disposition the exact 16 reviewed `opentibiabr/otclient` commits safely, review `solchanel/otclient-15` selectively, and define the next implementation sequence without weakening Oteryn Identity, tests, security or the current Windows validation policy.

# Acceptance criteria

- [x] Current capabilities classified as runtime-proven, CI-proven, source-only, partial, broken, missing or externally dependent.
- [x] Exact 16-commit upstream range identified and dispositioned.
- [x] Valuable `solchanel/otclient-15` clues reviewed without bulk integration.
- [x] Relevant upstream issues and PRs triaged against current source.
- [x] External repositories remained read-only.
- [x] Oteryn Identity, no-password fallback, one-shot session semantics, replay protections, shell-safe URL launching, tests and strict asset gates recorded as preservation boundaries.
- [x] Phased implementation plan records dependencies, risks, compatibility, rollout and rollback.
- [x] PR #26 final net diff, exact-head CI and squash result verified.
- [x] PR #25 current-base docs diff passed required CI and was squash-merged.
- [x] Task archived with the PR #25 squash SHA.

# Confirmed final synchronization state

- Task-start `main`: `715ba210e870304f66b5d5496899c6ea3ca9599d`.
- Reviewed upstream head: `465b7a217e87502bb7f9980bf6e099718d0a9a49`.
- Recorded common ancestor: `bdea0b23b4a738809d698cb7e4f88a299dd6bffc`.
- Exact reviewed upstream-only range: 16 commits.
- PR #26 refreshed exact head: `4f9958c5b834e911e06ffb5e10f1193400f545e7`.
- PR #26 exact-head CI: run `30176493622`, success.
- PR #26 squash merge: `38ef14010cc01b16824dd646022c6f5d3ba93146`.
- PR #25 exact-head CI: run `30178833942`, success.
- PR #25 squash merge: `6e30c340c26f3d1fdb1ffacb17cc30a172392dca`.
- Repository policy: squash merge only.
- Required compilation: five-job Windows matrix; Fast Checks and Lua Syntax remain required.

# Accepted and deferred upstream effects

Accepted effects include NPC trade imbuement quantities/lifecycle cleanup, Stats pause/resume, `--user-dir`, manual-walk/bot coordination, bounded unknown-opcode recovery, pre-780 use-with, ground-border targeting, mount animation, reviewed browser/WASM compatibility and Cocoa mouse delta handling.

Three effects remain deliberately excluded:

1. renderer/preload ordering that imported `client/game.h` into framework core and reversed the required dependency direction;
2. Reward Wall source-byte semantics without an exact Canary producer, shared `OTS-*` contract, compatibility matrix and paired tests;
3. production asset release-archive compatibility without a real clean-directory download/runtime rehearsal.

# Capability conclusions

- Oteryn Identity exists with Authorization Code + PKCE, loopback callback, Platform Game Login Ticket, Gateway normalization and one-shot Game Session handoff. Production enablement remains blocked on an exact Canary adapter/E2E pair.
- Legacy account/password login remains present for non-Oteryn profiles; the Oteryn profile has no password fallback.
- Action bars, hotkey sets, multi-actions, graphical cooldowns and option surfaces exist but contain deterministic lifecycle and persistence defects tracked in follow-up PRs.
- Existing Taskboard parser/feature hooks must be reused. A complete Taskboard remains externally dependent on an exact Canary payload contract and original/provenance-safe assets.
- Dormant browser/macOS/Android paths have source or historical evidence only; no new compatibility claim is made.
- Client-assets installation retains strict hash/path gates. Archive-selection code is handled separately and production claims still require runtime rehearsal.

# Priority execution sequence

1. Character-list recreation after destroy/relog — PR #31.
2. Action-bar authoritative cooldown cache/subscription lifecycle — PR #33.
3. Wheel conviction index alignment — PR #34.
4. Forge scheduled-event cancellation/lifetime repair — PR #35.
5. Deterministic options Phase 0 — PR #36.
6. Focused asset archive selection — PR #37, with production rehearsal still gated.
7. Modern protocol 15.24/15.25 and Taskboard only with exact Canary pairs and fail-closed unsupported combinations.
8. Reconcile the Oteryn presentation prototype PR #23 after manual Windows visual approval.

# Work log

## 2026-07-25

- Created audit PR #25 and synchronization PR #26.
- Reviewed the exact 16-commit upstream range and current fork-specific Oteryn/security/test behavior.
- Triaged `solchanel/otclient-15` selectively; rejected bulk integration because of divergence, binary/provenance risk, hard-coded contracts and parser hazards.
- Excluded renderer dependency reversal, unpaired Reward Wall semantics and unproven production asset archive compatibility.
- Reused existing InputMessage body-size/EOF tests rather than adding a redundant harness.
- Corrected a temporary ranged-read truncation on the synchronization branch by restoring the exact prior blob before applying intended edits. Never replace a complete file from a ranged fetch.
- Confirmed repository merge policy is squash-only and refreshed strict-base heads rather than bypassing protection.

## 2026-07-26

- Verified PR #26 exact head `4f9958c5...` passed five Windows variants, CTest, Fast Checks, Lua Syntax and `CI / Required` in run `30176493622`.
- Verified PR #26 squash-merged as `38ef14010cc01b16824dd646022c6f5d3ba93146`.
- Started P1 character-list recreation as draft PR #31.
- Opened and merged post-merge task archive PR #32.
- Refreshed the audit to terminal synchronization facts.
- Verified PR #25 exact-head CI run `30178833942` completed successfully.
- Verified PR #25 squash-merged as `6e30c340c26f3d1fdb1ffacb17cc30a172392dca`.
- Archived this task and released its implementation blockers.

# Decisions

| Decision | Reason/evidence |
|---|---|
| External repositories remain read-only | Repository allowlist and cross-repository safety policy. |
| Synchronize reviewed net effects rather than replace the fork | The fork contains unique Oteryn, security, tests and governance behavior. |
| Record upstream head and per-commit disposition | Squash merge intentionally does not preserve upstream ancestry. |
| Separate deterministic client repairs from protocol work | Lifecycle/options defects can be proven locally; payload changes require exact Canary pairs. |
| Preserve strict asset gates | Production download compatibility requires final-path, hash and runtime-load proof. |
| Reuse existing Taskboard and action-bar infrastructure | Avoids duplicate controllers and incompatible persisted/protocol models. |

# Validation

| Commit/run | Check | Result |
|---|---|---|
| `943428f0ef2c2791355f6a408c3fbc9d2abf6afb` | initial audit source/path/issue review | success |
| `7bcf57bb3eae419db8ac462d7053ce5cd43e264e` | historical cross-platform synchronization evidence | success; supporting only |
| `fd283c1a6d99dd870f09ee45fdf591541a6f71e9` | Windows-only CI policy PR #27 | success |
| `c9dba184328250b3550386565e3d15bf8f73ea49` | first exact task-record CI #230 | success |
| `4f9958c5b834e911e06ffb5e10f1193400f545e7` | refreshed exact-head CI `30176493622` | success |
| `38ef14010cc01b16824dd646022c6f5d3ba93146` | PR #26 squash result | verified |
| `99655274358c80ef2a0c4f585c30cb74d965d63f` | PR #25 exact-head CI `30178833942` | success |
| `6e30c340c26f3d1fdb1ffacb17cc30a172392dca` | PR #25 squash result | verified |

# Risks and compatibility

- User-facing OTUI and gameplay repairs still require representative Windows interaction evidence before claims of visual/runtime parity.
- Protocol 15.x/Taskboard work remains blocked until exact producer fixtures and fail-closed compatibility gates exist.
- Asset production compatibility remains blocked on provenance, hash, install-path and runtime-load rehearsal evidence.
- Browser/macOS/Android remain non-required dormant targets.
- Rollback of the audit is a documentation revert; implementation tasks retain independent rollback commits.

# Handoff

- Start from the comprehensive report and the active implementation task records.
- Do not re-review the exact 16-commit range unless the upstream baseline changes.
- Do not bulk-import `solchanel/otclient-15`.
- Do not weaken Oteryn, strict assets, branch protection or exact Canary pairing to accelerate later phases.

# Completion

- Final status: completed
- PR: #25
- Merge commit: `6e30c340c26f3d1fdb1ffacb17cc30a172392dca`
- Catalogue updated: not applicable; audit only
- Changelog updated: not applicable; audit only
- Archived at: 2026-07-26T08:23:30+02:00
