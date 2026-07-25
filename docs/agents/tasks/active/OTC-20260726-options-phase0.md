---
task_id: OTC-20260726-options-phase0
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260726-options-phase0
base_branch: main
created: 2026-07-26T01:31:00+02:00
updated: 2026-07-26T01:31:00+02:00
last_verified_commit: "70818ce8fd6b134d0708071fd8e9fd0f87acb21a"
risk: medium
related_issue: ""
related_pr: ""
depends_on:
  - PR #35 Forge scheduled-event lifecycle
blocks:
  - options architecture phase one
owned_paths:
  - modules/client_options/options.otmod
  - modules/client_options/options_migration_core.lua
  - modules/client_options/options_phase0.lua
  - modules/client_options/data_options.lua
  - modules/client_options/styles/interface/actionbars.otui
  - modules/client_options/styles/interface/interface.otui
  - modules/client_options/styles/interface/HUD.otui
  - modules/client_options/styles/controls/general.otui
  - tests/lua/unit/options_phase0_test.lua
  - tests/lua/CMakeLists.txt
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260726-options-phase0.md
modules_touched:
  - client_options
reuses:
  - existing option controller and settings store
  - existing action-bar reset API
  - existing inventory/container reload actions
  - existing Lua test runner
public_interfaces:
  - showExpiryInInventory
  - legacy alias showExpiryInInvetory
cross_repo_tasks: []
---

# Goal

Repair the deterministic Phase 0 option defects without adding unsupported product surface: correct action-bar reset wiring, event ownership and labels; hide controls that have no backend; and migrate the misspelled inventory-expiry key with backward-compatible dual read/write.

# Acceptance criteria

- [ ] Clear Right Bar 3 calls `resetAction(9)`.
- [ ] The global reset button has a unique widget ID.
- [ ] Inventory expiry cancels its own pending event.
- [ ] Teleport and floor-change sliders display their own labels in setup callbacks.
- [ ] Unsupported unused-item expiry and status-bar controls are not user-visible.
- [ ] Cooldown-window wording matches actual behavior.
- [ ] Canonical `showExpiryInInventory` reads a legacy stored value when needed and writes both keys for existing consumers.
- [ ] Focused Lua/static tests cover all changed controls and migration decisions.
- [ ] No new backend claim is made for hidden unsupported controls.
- [ ] Exact-head Lua Syntax, CTest and required CI pass before squash merge.

# Confirmed context

- `actionbars.otui` maps Right Bar 3 to action bar 7 and duplicates `clearRightBar3` for the global reset button.
- `data_options.lua` guards inventory event removal with `showExpiryInContainers.event`.
- `general.otui` displays the turn-delay label for teleport and floor-change setup callbacks.
- `interface.otui` exposes a disabled unused-item-expiry checkbox with no proven backing distinction.
- `HUD.otui` exposes two generic option checkboxes without IDs or matching option entries.
- `showSpellGroupCooldowns` controls the complete cooldown window, so the visible label should describe a cooldown bar/window rather than only group internals.
- Current stacked base: PR #35 head `70818ce8fd6b134d0708071fd8e9fd0f87acb21a`.

# Plan

1. Add a pure compatibility helper for the inventory-expiry key.
2. Install a narrow post-options adapter that performs migration and dual writes.
3. Apply the five static OTUI/Lua repairs.
4. Add focused static/migration tests.
5. Validate the isolated diff after dependencies merge.

# Work log

## 2026-07-26T01:31:00+02:00

- Changed: claimed deterministic option repairs on a stacked branch from PR #35.
- Learned: unsupported controls should be hidden rather than enabled because no authoritative backing option/action exists.
- Safety: no new protocol, platform, authentication or rendering behavior is introduced.

# Validation and CI

| Commit | Check | Result |
|---|---|---|
| pending | focused Lua/static tests | not-run |
| pending | Lua Syntax | not-run |
| pending | Windows CMake Tests / CTest | not-run |
| pending | `CI / Required` | not-run |

# Risks and compatibility

- Existing consumers of the misspelled key remain supported through dual writes.
- Hidden controls can be reintroduced only with real backing behavior and acceptance tests.
- Rollback is a normal squash revert.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Catalogue updated: yes, compatibility alias documented in task
- Changelog updated: pending
- Archived at: pending
