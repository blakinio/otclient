---
task_id: OTC-20260726-options-phase0
coordination_id: ""
status: completed
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260726-options-phase0
base_branch: main
created: 2026-07-26T01:31:00+02:00
updated: 2026-07-27T08:55:00+02:00
last_verified_commit: "8f1f03bcf506d7846c3e344dc25df9b7c7a305a7"
risk: medium
related_issue: ""
related_pr: "#36"
depends_on:
  - merged PR #35 Forge scheduled-event lifecycle
blocks: []
owned_paths:
  - modules/client_options/options.otmod
  - modules/client_options/options_migration_core.lua
  - modules/client_options/options_phase0.lua
  - modules/client_options/styles/interface/actionbars.otui
  - tests/lua/unit/options_phase0_test.lua
  - tests/lua/CMakeLists.txt
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/archive/OTC-20260726-options-phase0.md
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

# Completion summary

PR #36 delivered the bounded eight-file Phase 0 repair:

- Right Bar 3 now resets action bar 9 and the global reset button has a unique widget ID;
- inventory-expiry reload scheduling is owned and cancelled independently;
- teleport, floor-change and cooldown labels are normalized;
- unsupported controls remain hidden;
- canonical `showExpiryInInventory` preserves dual-read/write compatibility with `showExpiryInInvetory`;
- focused Lua/static coverage is registered in the existing CTest suite.

No authentication, protocol, renderer, Canary, login-server or server behavior changed.

# Final scope

Exactly eight feature files were merged:

1. `docs/agents/CHANGELOG.md`
2. `docs/agents/tasks/active/OTC-20260726-options-phase0.md`
3. `modules/client_options/options.otmod`
4. `modules/client_options/options_migration_core.lua`
5. `modules/client_options/options_phase0.lua`
6. `modules/client_options/styles/interface/actionbars.otui`
7. `tests/lua/CMakeLists.txt`
8. `tests/lua/unit/options_phase0_test.lua`

Historical stack and unrelated files remained excluded.

# Validation

| Evidence | Result |
|---|---|
| final feature head `8f1f03bcf506d7846c3e344dc25df9b7c7a305a7` | verified |
| exact-head CI run `30225228971` | PASS |
| Lua Syntax and both Fast Checks | PASS |
| Windows CMake Release | PASS |
| Windows CMake Tests / CTest | PASS |
| Windows Solution Debug | PASS |
| Windows Solution OpenGL | PASS |
| Windows Solution DirectX | PASS |
| `CI / Required` | PASS |
| changed-file/full-diff review | exactly eight files |
| unresolved review threads | none |

Earlier runs, including `30210789849` and `30223541591`, were superseded by restacks and were not used as final merge evidence.

# Restack evidence

Backups retained before force-restacks:

- `backup/OTC-20260726-options-phase0-pre-final-restack`
- `backup/OTC-20260726-options-phase0-pre-20260727-restack`
- `backup/OTC-20260726-options-phase0-pre-20260727-restack-2`

The final clean base was `3c7d1a75d294fce027c1f45f963f4aac4970b2fc`.

# Merge

- PR: #36
- Method: squash
- Feature head: `8f1f03bcf506d7846c3e344dc25df9b7c7a305a7`
- Exact-head CI run: `30225228971`
- Squash merge commit: `99ad5de5a19179f21e2e21e961c1ef121a30d08e`
- Merged: 2026-07-27

# Risks and compatibility

- Existing consumers of the misspelled key remain supported through dual writes and canonical-to-legacy API mapping.
- The adapter changes only the module sandbox and loaded options widgets.
- Hidden controls can be reintroduced only with real backing behavior and acceptance tests.
- Rollback is a normal squash revert.

# Completion

- Final status: completed
- PR: #36
- Merge commit: `99ad5de5a19179f21e2e21e961c1ef121a30d08e`
- Catalogue updated: compatibility alias documented here; no catalogue entry required
- Changelog updated: yes
- Archived at: `docs/agents/tasks/archive/OTC-20260726-options-phase0.md`
