---
task_id: OTC-20260726-wheel-conviction-indices
coordination_id: ""
status: complete
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260726-wheel-conviction-indices
base_branch: main
created: 2026-07-26T01:21:00+02:00
updated: 2026-07-26T14:22:11+02:00
last_verified_commit: "7931762c75c03d80ef183b10374b6e43ef44874a"
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
- [x] Exact-head Lua Syntax, CTest and required CI pass before squash merge.

# Confirmed context

- `getConvictionPerks` produces special bonuses at 1-4, skill at 5, life leech at 6, mana leech at 7, spells at 8-12 and vessels at 13-16.
- `WheelOfDestiny.configureSummary` dynamically calls the global `getConvictionPerks`, then expects a ten-slot summary view: special 1/2, skill, life, mana and five spells.
- The legacy summary consumer therefore reads shifted source slots when it uses raw positions 3-10.
- The mismatch is deterministic and independent of server payload changes.
- PR #33 and its task archive are merged into `main`.
- Current clean base: `fc6a40fcca18b403b5936ac59f5f938b56bc5148`.

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

## 2026-07-26T13:12:34+02:00

- Created backup branch `backup/OTC-20260726-wheel-conviction-indices-pre-autonomous-restack-543c81bf` at the original stacked head.
- Restacked the seven Wheel task commits directly onto current `main`, removing the historical action-bar, character-list and upstream-synchronization stack from the PR diff.
- Reviewed the isolated six-file diff and the existing producer/summary consumer; confirmed the change does not touch protocol parsing, feature gates, authentication or assets.
- Located the repository Windows vcpkg LuaJIT and passed all three focused index/adapter tests.

# Validation and CI

| Commit | Check | Result |
|---|---|---|
| `baa2a252d255bb61bef11cb85078b8822f180ef9` | `luajit tests/lua/helpers/runner.lua tests/lua/unit/wheel_conviction_indices_test.lua` | passed, 3 tests and 0 failed with repository Windows vcpkg LuaJIT |
| `baa2a252d255bb61bef11cb85078b8822f180ef9` | `git diff --check origin/main...HEAD` | passed |
| `7931762c75c03d80ef183b10374b6e43ef44874a` | Runtime Lua syntax | passed in run `30199720339` |
| `7931762c75c03d80ef183b10374b6e43ef44874a` | Windows CMake Tests / CTest | passed in run `30199720339` |
| `7931762c75c03d80ef183b10374b6e43ef44874a` | required Windows build matrix | passed in run `30199720339`: CMake Release, CMake Tests, Solution DirectX, Solution OpenGL and Solution Debug |
| `7931762c75c03d80ef183b10374b6e43ef44874a` | `CI / Required` | passed, exact-head aggregate in run `30199720339` |

# Risks and compatibility

- No protocol bytes, feature gates, persistence or UI layout change.
- The raw 16-slot producer remains unchanged for all other consumers.
- Rollback is a normal squash revert.

# Remaining work

None.

# Completion

- Final status: complete
- PR: #34
- Merge commit: `218e1339cb6644a2f0db9ea03d59a63d7553d44d`
- Catalogue updated: not applicable
- Changelog updated: yes
- Archived at: 2026-07-26T14:22:11+02:00
