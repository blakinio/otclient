---
task_id: OTC-20260726-actionbar-cooldown-lifecycle
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260726-actionbar-cooldown-lifecycle
base_branch: main
created: 2026-07-26T01:09:00+02:00
updated: 2026-07-26T02:14:00+02:00
last_verified_commit: "a219d0c5cf2705958d0756d4f3ad2c226c12bbd0"
risk: medium
related_issue: "opentibiabr/otclient#1776"
related_pr: "#33"
depends_on:
  - PR #31 character-list lifecycle repair
blocks:
  - Wheel, Forge and deterministic options repair sequence
owned_paths:
  - modules/game_actionbar/game_actionbar.otmod
  - modules/game_actionbar/cooldown_lifecycle.lua
  - modules/game_actionbar/cooldown_lifecycle_core.lua
  - tests/lua/unit/actionbar_cooldown_lifecycle_test.lua
  - tests/lua/unit/actionbar_cooldown_adapter_test.lua
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

- [x] Cooldown protocol callbacks are subscribed for the module lifetime, not only after visible action bars are built.
- [x] New session boundaries reset individual and group caches synchronously before new packets.
- [x] Cooldown packets update caches even when visual cooldown options are disabled.
- [x] Rebuilding an action button clears stale widget timers before restoration, not after it.
- [x] Restoration uses the maximum remaining individual/primary/secondary group cooldown.
- [x] Text spells, simple rune buttons and multi-actions use the same authoritative remaining-time decision.
- [x] Unload/logout disconnects module-owned subscriptions and clears session caches.
- [x] Focused Lua tests cover cache-first handling, max remaining selection, session reset, pre-UI packets, reentrant start and relog restoration.
- [ ] Exact-head required CI and focused CTest pass before squash merge.

# Confirmed context

- Current stacked base: PR #31 head `8baa23d6fda45fa4a8083d0a7753c9d503d98063`.
- Legacy listeners connect only after action bars become active, allowing early protocol packets to be missed.
- Legacy callbacks return before caching when both visual options are disabled.
- Legacy `setupActionBar` can stop an overlay after `updateButton` restores it.
- Simple runes were not consistently routed through the same individual/group calculation.
- No protocol or Canary payload change is required.

# Implementation

- `cooldown_lifecycle_core.lua` owns session transitions, cache records/copies/merges and maximum remaining-time calculation.
- `cooldown_lifecycle.lua` installs module-lifetime event subscriptions, records protocol truth before visual decisions and restores all supported action types after rebuild.
- Existing `ActionBarController`, mappings and widgets remain authoritative.
- Reentrant callbacks received while the original `onGameStart` rebuild is running are merged back by latest expiration, preventing a temporary cache table from discarding them.

# Work log

## 2026-07-26T01:09:00+02:00

- Claimed the repair on a stacked branch from PR #31.
- Separated authoritative protocol state from presentation preferences.

## 2026-07-26T02:14:00+02:00

- Completed helper, adapter, manifest load order, lifecycle tests and changelog.
- Source review found a second race: a callback received reentrantly during original `onGameStart` could land in a temporary cache and be overwritten. Added cache merging by latest expiration and a mock reentrant-start test.
- No local Lua interpreter is available; repository CTest/CI remains the source of truth.

# Decisions

| Decision | Reason/evidence |
|---|---|
| Keep existing ActionBarController and persisted mappings | The defect is lifecycle/cache ordering, not missing feature architecture. |
| Add a module-local adapter and pure helper | Minimizes risk in large legacy files and makes state transitions testable. |
| Treat maximum remaining cooldown as authoritative | An action cannot be available before either its individual or any group cooldown expires. |
| Preserve caches when visuals are disabled | Preferences control presentation only, not protocol truth. |
| Merge rebuild-time caches by latest expiration | Reentrant packets must not be overwritten by deferred UI setup. |

# Validation and CI

| Commit | Check | Result |
|---|---|---|
| `a219d0c5cf2705958d0756d4f3ad2c226c12bbd0` | focused Lua tests | pending repository CTest |
| `a219d0c5cf2705958d0756d4f3ad2c226c12bbd0` | Lua Syntax | pending workflow publication |
| pending refreshed head | Windows CMake Tests / CTest | not-run |
| pending refreshed head | `CI / Required` | not-run |

# Risks and compatibility

- Protocol payloads and feature gates are unchanged.
- Adapter replaces the legacy subscription toggle with one idempotent module-lifetime subscription set.
- Persisted action mappings/hotkeys remain untouched.
- Rollback is a normal squash revert.

# Remaining work

1. After PR #31 merges, refresh onto current `main` and inspect the isolated diff.
2. Mark ready, run full Windows CTest/required CI, review threads and stable base.
3. Squash-merge and archive the task.

# Completion

- Final status: in progress
- PR: #33
- Merge commit: pending
- Catalogue updated: not applicable; no new public interface
- Changelog updated: yes
- Archived at: pending
