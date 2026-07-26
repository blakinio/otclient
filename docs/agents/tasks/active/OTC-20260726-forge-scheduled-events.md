---
task_id: OTC-20260726-forge-scheduled-events
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260726-forge-scheduled-events
base_branch: main
created: 2026-07-26T01:25:00+02:00
updated: 2026-07-26T14:30:15+02:00
last_verified_commit: "1dd02f88defde9a307d8d101608dedb0d19c7ba1"
risk: medium
related_issue: "opentibiabr/otclient#1691"
related_pr: "#35"
depends_on:
  - PR #34 Wheel conviction index repair
blocks:
  - deterministic options repair sequence
owned_paths:
  - modules/game_forge/game_forge.otmod
  - modules/game_forge/forge_event_lifecycle.lua
  - modules/game_forge/forge_event_lifecycle_core.lua
  - tests/lua/unit/forge_event_lifecycle_test.lua
  - tests/lua/unit/forge_event_lifecycle_adapter_test.lua
  - tests/lua/CMakeLists.txt
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260726-forge-scheduled-events.md
modules_touched:
  - game_forge
reuses:
  - existing ForgeController callbacks and controller lifecycle
  - existing global event removal API
  - existing Lua test runner
public_interfaces: []
cross_repo_tasks: []
---

# Goal

Prevent Forge scheduled callbacks from outliving their controller generation by tracking every module-owned event handle, cancelling pending handles before callback tables are cleared and ignoring stale-generation callbacks.

# Acceptance criteria

- [x] Every Forge callback scheduled through the module adapter has a retained event handle.
- [x] Successful callback execution removes its own handle from tracking.
- [x] Hide, game end and terminate cancel pending handles before callback closures are cleared.
- [x] Stale-generation callbacks are no-ops even if the underlying queue races cancellation.
- [x] Reopening Forge starts a fresh generation without inheriting old timers.
- [x] Focused Lua tests cover execution, cancellation, stale generations and repeated lifecycle cycles.
- [x] No Forge protocol or economy payload changes.
- [ ] Exact-head Lua Syntax, CTest and required CI pass before squash merge.

# Confirmed context

- Issue #1691 identifies six delayed callbacks: unloadModule, updateBonusButton, timeoutCallback, clearRightItem, continueAnimation and startResultAnimation.
- Current `terminate()` clears `ForgeController.callbacks` but does not retain/cancel all `scheduleEvent` handles.
- C++ may therefore retain a Lua function after the Lua closure table is released.
- PR #34 and its task archive are merged into `main`.
- Current clean base: `59d0a11e17b6fbc213f56bdb6ea3e381102e70d8`.

# Implementation

- `forge_event_lifecycle_core.lua` owns generation state and tracked handles without retaining completed or cancelled callback references.
- `forge_event_lifecycle.lua` wraps the Forge sandbox scheduler, removes completed handles and cancels/invalidate all pending handles at hide, game end, game start and terminate boundaries.
- Generation checks keep a raced callback harmless after cancellation or a reopened Forge session.
- The existing Forge controller and its callback table remain authoritative.

# Work log

## 2026-07-26T01:25:00+02:00

- Changed: claimed the focused Forge scheduled-event repair.
- Learned: cancellation alone is insufficient for a queue race; cancellation and generation validation are required together.

## 2026-07-26T14:30:15+02:00

- Created backup branch `backup/OTC-20260726-forge-scheduled-events-pre-autonomous-restack-70818ce8` at the original stacked head.
- Restacked the eight Forge task commits directly onto current `main`, removing the historical Wheel/action-bar/character-list/upstream stack from the PR diff.
- Full diff review found that `retiredCallbacks` accumulated every manually removed or lifecycle-cancelled closure forever.
- Verified from `modules/corelib/globals.lua` and `src/framework/core/event.cpp` that existing event cancellation clears both the Lua `_callback` reference and C++ callback, so the extra retention was unnecessary.
- Removed the unbounded callback list and added a 100-cycle regression proving that tracked handles return to zero without an accumulating callback collection.
- Passed all nine focused core/adapter tests with the repository Windows vcpkg LuaJIT.

# Validation and CI

| Commit | Check | Result |
|---|---|---|
| `1dd02f88defde9a307d8d101608dedb0d19c7ba1` | `luajit tests/lua/helpers/runner.lua tests/lua/unit/forge_event_lifecycle_test.lua tests/lua/unit/forge_event_lifecycle_adapter_test.lua` | passed, 9 tests and 0 failed with repository Windows vcpkg LuaJIT |
| `1dd02f88defde9a307d8d101608dedb0d19c7ba1` | `git diff --check origin/main...HEAD` | passed |
| pending | Windows CMake Tests / CTest | not-run |
| pending | `CI / Required` | not-run |

# Risks and compatibility

- Forge packets, prices, convergence rules and animation timings remain unchanged.
- Adapter must not capture unrelated module timers.
- Rollback is a normal squash revert.

# Remaining work

1. Publish the refreshed head and mark PR #35 ready.
2. Pass exact-head Windows CTest/required CI and verify review threads and stable base.
3. Squash-merge and archive the task.

# Completion

- Final status: in progress
- PR: #35
- Merge commit: pending
- Catalogue updated: not applicable
- Changelog updated: yes
- Archived at: pending
