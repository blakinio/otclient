---
task_id: OTC-20260726-options-phase0
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260726-options-phase0
base_branch: main
created: 2026-07-26T01:31:00+02:00
updated: 2026-07-26T18:35:00+02:00
last_verified_commit: "afdcdd774c35603feab705206c3ab0dada9745d1"
risk: medium
related_issue: ""
related_pr: "#36"
depends_on:
  - PR #35 Forge scheduled-event lifecycle
blocks:
  - options architecture phase one
owned_paths:
  - modules/client_options/options.otmod
  - modules/client_options/options_migration_core.lua
  - modules/client_options/options_phase0.lua
  - modules/client_options/styles/interface/actionbars.otui
  - tests/lua/unit/options_phase0_test.lua
  - tests/lua/CMakeLists.txt
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260726-options-phase0.md
modules_touched:
  - client_options
reuses:
  - existing option controller and settings store
  - existing action-bar reset API
  - existing inventory/container reload action
  - existing loaded panel/widget tree
  - existing Lua test runner
public_interfaces:
  - showExpiryInInventory
  - legacy alias showExpiryInInvetory
cross_repo_tasks: []
---

# Goal

Repair deterministic Phase 0 option defects without adding unsupported product surface: correct action-bar reset wiring, event ownership and labels; hide controls that have no backend; and migrate the misspelled inventory-expiry key with backward-compatible dual read/write.

# Acceptance criteria

- [x] Clear Right Bar 3 calls `resetAction(9)`.
- [x] The global reset button has a unique widget ID.
- [x] Inventory expiry owns and cancels its pending reload event independently from the container option.
- [x] Teleport and floor-change sliders display their own labels after panel load and on later option changes.
- [x] Unsupported unused-item expiry and status-bar controls are not user-visible.
- [x] Cooldown-window wording matches actual behavior.
- [x] Canonical `showExpiryInInventory` reads a legacy stored value when needed and writes both keys for existing consumers.
- [x] Focused Lua/static tests cover action-bar wiring, migration, loaded-panel normalization and rapid event cancellation.
- [x] No new backend claim is made for hidden unsupported controls.
- [ ] Exact-head Lua Syntax, CTest and required CI pass before squash merge.

# Confirmed context

- `actionbars.otui` mapped Right Bar 3 to action bar 7 and duplicated `clearRightBar3` for the global reset button.
- `data_options.lua` guards inventory event removal with `showExpiryInContainers.event`; the adapter owns the inventory event around the unchanged legacy action and deduplicates legacy removal.
- The backing teleport/floor-change actions already update correct labels; the adapter normalizes the initially loaded widgets.
- Unsupported unused-item-expiry and status-bar controls have no authoritative backend and remain hidden.
- `showSpellGroupCooldowns` controls the complete cooldown window.
- PR #35 and archive PR #42 are merged.
- Current clean base: `ca78b71397cd2196ab841144c27275d0462902d7`.

# Implementation

- `options_migration_core.lua` defines canonical/legacy keys and deterministic precedence.
- `options_phase0.lua` wraps `setOption/getOption`, dual-writes both keys, captures/cancels the inventory reload event and normalizes loaded widgets before user interaction.
- `actionbars.otui` contains the direct bar-9 and unique-ID fixes.
- `options_phase0_test.lua` verifies migration, static action-bar wiring, loaded widget state and rapid-toggle cleanup.

# Work log

## 2026-07-26T01:31:00+02:00

- Claimed deterministic option repairs on a stacked branch from PR #35.
- Confirmed unsupported controls must be hidden rather than enabled because no authoritative backing option/action exists.

## 2026-07-26T18:35:00+02:00

- Created backup branch `backup/OTC-20260726-options-phase0-pre-final-restack` at the original stacked head `ce81b2df4e9f0cc1c6c0c00aa896553883029ef0`.
- Restacked PR #36 directly onto current `main`, removing the historical 60-file gameplay/upstream stack.
- Recreated only the two option helpers, one manifest line, the two action-bar OTUI corrections, focused test registration/test, changelog and this task record.
- Re-reviewed the adapter against current `data_options.lua`; no protocol, auth, renderer or backend capability changes are introduced.

# Validation and CI

| Commit | Check | Result |
|---|---|---|
| `afdcdd774c35603feab705206c3ab0dada9745d1` | exact changed-file review | pending final compare after task commit |
| pending final head | Runtime Lua syntax | pending required CI |
| pending final head | Windows CMake Tests / CTest | pending required CI |
| pending final head | required Windows matrix and `CI / Required` | pending |

# Risks and compatibility

- Existing consumers of the misspelled key remain supported through dual writes and canonical-to-legacy API mapping.
- The adapter changes only the module sandbox and loaded options widgets.
- Hidden controls can be reintroduced only with real backing behavior and acceptance tests.
- Rollback is a normal squash revert.

# Remaining work

1. Review the isolated diff and focused test behavior.
2. Reopen/refresh PR #36, mark ready and pass exact-head required CI.
3. Squash-merge and archive this task.

# Completion

- Final status: in progress
- PR: #36
- Merge commit: pending
- Catalogue updated: compatibility alias documented here; no catalogue entry required
- Changelog updated: yes
- Archived at: pending
