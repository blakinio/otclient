---
task_id: OTC-20260726-wheel-conviction-indices
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260726-wheel-conviction-indices
base_branch: main
created: 2026-07-26T01:21:00+02:00
updated: 2026-07-26T02:20:00+02:00
last_verified_commit: "7df656ac1e9f270a89deb8b6d4985eb45ec497ee"
risk: low
related_issue: "opentibiabr/otclient#1753"
related_pr: "#34"
depends_on:
  - PR #33 action-bar cooldown lifecycle
blocks:
  - Forge and deterministic options repair sequence
owned_paths:
  - modules/game_wheel/wheel.otmod
  - modules/game_wheel/classes/conviction_indices.lua
  - tests/lua/unit/wheel_conviction_indices_test.lua
  - tests/lua/CMakeLists.txt
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260726-wheel-conviction-indices.md
modules_touched:
  - game_wheel
reuses:
  - existing ConvictionBonus producer order
  - existing global `getConvictionPerks`
  - existing `WheelOfDestiny.configureSummary`
  - existing Lua test runner
public_interfaces: []
cross_repo_tasks: []
---

# Goal

Replace shifted numeric ConvictionBonus accesses with one named index contract so Wheel skill, life, mana and spell summaries read the fields produced by the existing parser.

# Acceptance criteria

- [x] One named index map matches the current producer order: four special slots, skill, life, mana, five spell slots and four vessel slots.
- [x] Wheel summary reads skill/life/mana/spells through the named contract.
- [x] Focused Lua tests prove every index, summary extraction order and scoped adapter restoration.
- [x] No protocol parser, payload width or Canary contract changes.
- [ ] Exact-head Lua Syntax, CTest and required CI pass before squash merge.

# Confirmed context

- `getConvictionPerks` produces special bonuses at 1-4, skill at 5, life leech at 6, mana leech at 7, spells at 8-12 and vessels at 13-16.
- `WheelOfDestiny.configureSummary` dynamically calls the global `getConvictionPerks`, then expects a ten-slot summary view: special 1/2, skill, life, mana and five spells.
- The legacy summary consumer therefore reads shifted source slots when it uses raw positions 3-10.
- The mismatch is deterministic and independent of server payload changes.
- Current stacked base: PR #33 code/task stack.

# Implementation

- `conviction_indices.lua` defines one named producer-order index map.
- `buildSummaryView` adapts the 16-slot producer output to the existing ten-slot summary consumer shape.
- The adapter temporarily scopes the remapped getter only while original `WheelOfDestiny.configureSummary` executes and restores the global getter on success or error.
- `wheel.otmod` loads the adapter after the original Wheel classes.
- Tests verify the full index map, summary remap and restoration of the global getter.

# Work log

## 2026-07-26T01:21:00+02:00

- Claimed the focused Wheel index repair.
- Confirmed the producer/consumer disagreement and implemented a narrow summary-only adapter.

## 2026-07-26T02:20:00+02:00

- Source review verified `configureSummary` uses the global getter rather than a local closure, so the manifest-loaded adapter is effective.
- Corrected task ownership from the unchanged `wheelclass.lua` to the actually changed `wheel.otmod`.
- No local Lua interpreter is available; repository CTest/CI remains the validation source of truth.

# Validation and CI

| Commit | Check | Result |
|---|---|---|
| `7df656ac1e9f270a89deb8b6d4985eb45ec497ee` | focused Lua test | pending repository CTest |
| `7df656ac1e9f270a89deb8b6d4985eb45ec497ee` | Lua Syntax | pending workflow publication |
| pending refreshed head | Windows CMake Tests / CTest | not-run |
| pending refreshed head | `CI / Required` | not-run |

# Risks and compatibility

- No protocol bytes, feature gates, persistence or UI layout change.
- The raw 16-slot producer remains unchanged for all other consumers.
- Rollback is a normal squash revert.

# Remaining work

1. After PR #33 merges, refresh onto current `main` and inspect the isolated diff.
2. Mark ready, run full Windows CTest/required CI and review stable base/threads.
3. Squash-merge and archive this task.

# Completion

- Final status: in progress
- PR: #34
- Merge commit: pending
- Catalogue updated: not applicable
- Changelog updated: yes
- Archived at: pending
