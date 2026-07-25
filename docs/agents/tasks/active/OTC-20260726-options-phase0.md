---
task_id: OTC-20260726-options-phase0
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260726-options-phase0
base_branch: main
created: 2026-07-26T01:31:00+02:00
updated: 2026-07-26T01:47:00+02:00
last_verified_commit: "b39ea0c1c3e52de1546c4857f68971e20efa1a58"
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

Repair the deterministic Phase 0 option defects without adding unsupported product surface: correct action-bar reset wiring, event ownership and labels; hide controls that have no backend; and migrate the misspelled inventory-expiry key with backward-compatible dual read/write.

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

- `actionbars.otui` previously mapped Right Bar 3 to action bar 7 and duplicated `clearRightBar3` for the global reset button.
- `data_options.lua` guards inventory event removal with `showExpiryInContainers.event`; the adapter now owns the event around the unchanged legacy action and deduplicates legacy removal.
- `general.otui` has wrong setup-only labels; the backing actions already use correct labels, so the adapter normalizes the loaded widgets without rewriting the template.
- `interface.otui` exposes a disabled unused-item-expiry checkbox with no proven backing distinction; the adapter hides it.
- `HUD.otui` exposes two generic option checkboxes without IDs or matching option entries; the adapter recursively hides their panels by translated text.
- `showSpellGroupCooldowns` controls the complete cooldown window; the adapter labels it `Show Cooldown Bar` and gives it an accurate tooltip.
- Current stacked base: PR #35 head `70818ce8fd6b134d0708071fd8e9fd0f87acb21a`.

# Implementation

- `options_migration_core.lua` defines canonical/legacy keys and deterministic precedence.
- `options_phase0.lua` wraps `setOption/getOption`, dual-writes both keys, captures/cancels the inventory reload event and normalizes loaded widgets before user interaction.
- `actionbars.otui` contains the direct bar-9 and unique-ID fixes.
- `options_phase0_test.lua` verifies migration, static action-bar wiring, loaded widget state and rapid-toggle cleanup.

# Work log

## 2026-07-26T01:31:00+02:00

- Claimed deterministic option repairs on a stacked branch from PR #35.
- Confirmed unsupported controls must be hidden rather than enabled because no authoritative backing option/action exists.

## 2026-07-26T01:47:00+02:00

- Added the compatibility helper and adapter without replacing the 863-line `data_options.lua`.
- Corrected the action-bar OTUI directly.
- Added focused static and mock lifecycle tests.
- Updated the changelog.
- No local Lua interpreter is available in the sandbox; repository CI remains the validation source of truth.

# Validation and CI

| Commit | Check | Result |
|---|---|---|
| `b39ea0c1c3e52de1546c4857f68971e20efa1a58` | focused Lua/static tests | pending repository CTest |
| `b39ea0c1c3e52de1546c4857f68971e20efa1a58` | Lua Syntax | pending workflow publication |
| pending refreshed head | Windows CMake Tests / CTest | not-run |
| pending refreshed head | `CI / Required` | not-run |

# Risks and compatibility

- Existing consumers of the misspelled key remain supported through dual writes and canonical-to-legacy API mapping.
- The adapter changes only the module sandbox and loaded options widgets.
- Hidden controls can be reintroduced only with real backing behavior and acceptance tests.
- Rollback is a normal squash revert.

# Remaining work

1. Obtain draft lightweight CI on the current stacked head.
2. After PR #35 merges, refresh onto current `main`, inspect the isolated diff, mark ready and run full CTest/Windows CI.
3. Squash-merge and archive this task.

# Completion

- Final status: in progress
- PR: #36
- Merge commit: pending
- Catalogue updated: compatibility alias documented here; no catalogue entry required
- Changelog updated: yes
- Archived at: pending
