---
task_id: OTC-20260726-forge-scheduled-events
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260726-forge-scheduled-events
base_branch: main
created: 2026-07-26T01:25:00+02:00
updated: 2026-07-26T01:25:00+02:00
last_verified_commit: "7df656ac1e9f270a89deb8b6d4985eb45ec497ee"
risk: medium
related_issue: "opentibiabr/otclient#1691"
related_pr: ""
depends_on:
  - PR #34 Wheel conviction index repair
blocks:
  - deterministic options repair sequence
owned_paths:
  - modules/game_forge/game_forge.otmod
  - modules/game_forge/forge_event_lifecycle.lua
  - modules/game_forge/forge_event_lifecycle_core.lua
  - tests/lua/unit/forge_event_lifecycle_test.lua
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

- [ ] Every Forge callback scheduled through the module adapter has a retained event handle.
- [ ] Successful callback execution removes its own handle from tracking.
- [ ] Hide, game end and terminate cancel pending handles before callback closures are cleared.
- [ ] Stale-generation callbacks are no-ops even if the underlying queue races cancellation.
- [ ] Reopening Forge starts a fresh generation without inheriting old timers.
- [ ] Focused Lua tests cover execution, cancellation, stale generations and repeated lifecycle cycles.
- [ ] No Forge protocol or economy payload changes.
- [ ] Exact-head Lua Syntax, CTest and required CI pass before squash merge.

# Confirmed context

- Issue #1691 identifies six delayed callbacks: unloadModule, updateBonusButton, timeoutCallback, clearRightItem, continueAnimation and startResultAnimation.
- Current `terminate()` clears `ForgeController.callbacks` but does not retain/cancel all `scheduleEvent` handles.
- C++ may therefore retain a Lua function after the Lua closure table is released.
- Current stacked base: PR #34 head `7df656ac1e9f270a89deb8b6d4985eb45ec497ee`.

# Plan

1. Add a pure generation/handle registry.
2. Install a Forge-local scheduler wrapper before controller initialization.
3. Cancel and invalidate on hide, game end and terminate.
4. Add focused Lua tests and validate the isolated diff after dependencies merge.

# Work log

## 2026-07-26T01:25:00+02:00

- Changed: claimed the focused Forge scheduled-event repair.
- Learned: cancellation alone is insufficient for a queue race; cancellation and generation validation are required together.

# Validation and CI

| Commit | Check | Result |
|---|---|---|
| pending | focused Lua test | not-run |
| pending | Lua Syntax | not-run |
| pending | Windows CMake Tests / CTest | not-run |
| pending | `CI / Required` | not-run |

# Risks and compatibility

- Forge packets, prices, convergence rules and animation timings remain unchanged.
- Adapter must not capture unrelated module timers.
- Rollback is a normal squash revert.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Catalogue updated: not applicable
- Changelog updated: pending
- Archived at: pending
