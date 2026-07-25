---
task_id: OTC-20260726-wheel-conviction-indices
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260726-wheel-conviction-indices
base_branch: main
created: 2026-07-26T01:21:00+02:00
updated: 2026-07-26T01:21:00+02:00
last_verified_commit: "68b3826611e3a6d535bc6614bdf6a132a53396d4"
risk: low
related_issue: "opentibiabr/otclient#1753"
related_pr: ""
depends_on:
  - PR #33 action-bar cooldown lifecycle
blocks:
  - Forge and deterministic options repair sequence
owned_paths:
  - modules/game_wheel/classes/conviction_indices.lua
  - modules/game_wheel/classes/wheelclass.lua
  - tests/lua/unit/wheel_conviction_indices_test.lua
  - tests/lua/CMakeLists.txt
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260726-wheel-conviction-indices.md
modules_touched:
  - game_wheel
reuses:
  - existing ConvictionBonus parser shape
  - existing wheel summary widgets
  - existing Lua test runner
public_interfaces: []
cross_repo_tasks: []
---

# Goal

Replace shifted numeric ConvictionBonus accesses with one named index contract so Wheel skill, life, mana and spell summaries read the fields produced by the existing parser.

# Acceptance criteria

- [ ] One named index map matches the current parser order: four special slots, skill, life, mana and five spell slots.
- [ ] Wheel summary reads skill/life/mana/spells through the named contract.
- [ ] Focused Lua tests prove every index and summary extraction order.
- [ ] No protocol parser, payload width or Canary contract changes.
- [ ] Exact-head Lua Syntax, CTest and required CI pass before squash merge.

# Confirmed context

- `bonus.lua` populates ConvictionBonus indices 1-4 as special bonuses, 5 as skill, 6 as life, 7 as mana and 8-12 as spells.
- `wheelclass.lua` currently reads skill at 3, life at 4, mana at 5 and spells at 6-10.
- The mismatch is deterministic and independent of server payload changes.
- Current stacked base: PR #33 head `68b3826611e3a6d535bc6614bdf6a132a53396d4`.

# Plan

1. Add a pure named index/extraction helper.
2. Replace numeric summary accesses without changing parser production.
3. Add focused Lua tests.
4. Validate the isolated diff after dependencies reach `main`.

# Work log

## 2026-07-26T01:21:00+02:00

- Changed: claimed the focused Wheel index repair.
- Learned: the producer and consumer disagree by exactly two slots because the consumer omits the first four special-bonus fields from its numeric assumptions.

# Validation and CI

| Commit | Check | Result |
|---|---|---|
| pending | focused Lua test | not-run |
| pending | Lua Syntax | not-run |
| pending | Windows CMake Tests / CTest | not-run |
| pending | `CI / Required` | not-run |

# Risks and compatibility

- No protocol bytes, feature gates, persistence or UI layout change.
- Rollback is a normal squash revert.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Catalogue updated: not applicable
- Changelog updated: pending
- Archived at: pending
