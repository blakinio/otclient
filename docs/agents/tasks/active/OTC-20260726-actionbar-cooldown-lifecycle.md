---
task_id: OTC-20260726-actionbar-cooldown-lifecycle
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260726-actionbar-cooldown-lifecycle
base_branch: main
created: 2026-07-26T01:09:00+02:00
updated: 2026-07-26T01:09:00+02:00
last_verified_commit: "8baa23d6fda45fa4a8083d0a7753c9d503d98063"
risk: medium
related_issue: "opentibiabr/otclient#1776"
related_pr: ""
depends_on:
  - PR #31 character-list lifecycle repair
blocks:
  - Wheel, Forge and deterministic options repair sequence
owned_paths:
  - modules/game_actionbar/game_actionbar.otmod
  - modules/game_actionbar/cooldown_lifecycle.lua
  - modules/game_actionbar/cooldown_lifecycle_core.lua
  - tests/lua/unit/actionbar_cooldown_lifecycle_test.lua
  - tests/lua/CMakeLists.txt
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260726-actionbar-cooldown-lifecycle.md
modules_touched:
  - game_actionbar
reuses:
  - existing action bars, cooldown widgets and protocol callbacks
  - existing spell and spell-group cooldown caches
  - existing MultiActionLogic cooldown restoration helpers
  - existing Lua test runner
public_interfaces: []
cross_repo_tasks: []
---

# Goal

Keep action-bar cooldown protocol state authoritative across login/logout/reload, subscribe before packets can arrive, and restore the longest applicable individual/group cooldown for spells, runes and multi-actions.

# Acceptance criteria

- [ ] Cooldown protocol callbacks are subscribed for the module lifetime, not only after visible action bars are built.
- [ ] New session boundaries reset individual and group caches synchronously before new packets.
- [ ] Cooldown packets update caches even when visual cooldown options are disabled.
- [ ] Rebuilding an action button clears stale widget timers before restoration, not after it.
- [ ] Restoration uses the maximum remaining individual/primary/secondary group cooldown.
- [ ] Text spells, simple rune buttons and multi-actions use the same authoritative remaining-time decision.
- [ ] Unload/logout cancels module-owned scheduled events and clears session caches.
- [ ] Focused Lua tests cover cache-first handling, max remaining selection, session reset and relog restoration.
- [ ] Exact-head required CI and focused CTest pass before squash merge.

# Confirmed context

- Current stacked base: PR #31 head `8baa23d6fda45fa4a8083d0a7753c9d503d98063`.
- `game_actionbar.lua` currently connects cooldown listeners only when action bars are active.
- Its deferred `onGameStart` reset can erase packets that arrived before UI construction.
- `onSpellCooldown` and group callbacks return before caching when both visual options are disabled.
- `setupActionBar` can call `updateButton` and then stop the newly restored overlay.
- Simple rune restoration is not consistently routed through the same individual/group calculation.
- No protocol or Canary payload change is required.

# Plan

1. Add a pure session/cache/remaining-time helper with focused Lua tests.
2. Install a narrow adapter after existing action-bar logic loads.
3. Subscribe at module lifetime and keep session cache updates independent of visual preferences.
4. Wrap button rebuild/restoration without replacing persisted mappings or the action-bar controller.
5. Validate exact diff, lifecycle tests and required Windows gate after the dependency stack reaches current `main`.

# Work log

## 2026-07-26T01:09:00+02:00

- Changed: claimed the cooldown lifecycle repair on a stacked branch from PR #31.
- Learned: the authoritative protocol state and presentation overlay must be separated; visual options may suppress rendering but must not suppress cache updates.
- Dependency: PR #25 audit and PR #31 lifecycle repair are still progressing through their own protected gates.

# Decisions

| Decision | Reason/evidence |
|---|---|
| Keep existing ActionBarController and persisted mappings | The defect is lifecycle/cache ordering, not missing feature architecture. |
| Add a module-local adapter and pure helper | Minimizes risk in large legacy files and makes state transitions testable. |
| Treat maximum remaining cooldown as authoritative | An action cannot be available before either its individual or any group cooldown expires. |
| Preserve caches when visuals are disabled | Preferences control presentation only, not protocol truth. |

# Validation and CI

| Commit | Check | Result |
|---|---|---|
| pending | focused Lua tests | not-run |
| pending | Lua Syntax | not-run |
| pending | Windows CMake Tests / CTest | not-run |
| pending | `CI / Required` | not-run |

# Risks and compatibility

- Protocol payloads and feature gates remain unchanged.
- The adapter must avoid duplicate event subscriptions with legacy `connecting()` logic.
- Persisted action mappings/hotkeys must remain untouched.
- Rollback is a normal squash revert.

# Remaining work

1. Implement helper, adapter, tests and manifest load order.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Catalogue updated: not applicable; no new public interface
- Changelog updated: pending
- Archived at: pending
