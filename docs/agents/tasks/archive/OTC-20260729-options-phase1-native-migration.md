---
task_id: OTC-20260729-options-phase1-native-migration
status: completed
agent: "GPT-5.6 Thinking"
track: legacy-client
branch: refactor/OTC-20260729-options-phase1-native-migration
base_branch: main
created: 2026-07-29T23:34:00+02:00
updated: 2026-07-30T11:01:00+02:00
last_verified_commit: "cce607fe4b7555879347dd7ba6cc8a0abded71cb"
required_base_commit: "4e09e32032e64831c30d6f7aeb31a2ebd4d4520a"
risk: medium
related_pr: "#93"
depends_on:
  - merged PR #36 options Phase 0
  - archive PR #51
  - merged PR #92 shared-path lease release
  - archive PR #94 current-main synchronization
owned_paths:
  - modules/client_options/options_phase0.lua
  - tests/lua/CMakeLists.txt
  - tests/lua/unit/options_phase0_test.lua
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/archive/OTC-20260729-options-phase1-native-migration.md
modules_touched:
  - client_options
reuses:
  - existing options migration core
  - existing module lifecycle hook
  - existing Lua test runner
public_interfaces:
  - showExpiryInInventory
  - legacy alias showExpiryInInvetory
cross_repo_tasks: []
---

# Result

PR #93 completed the bounded continuation of merged PR #36. The compatibility adapter now owns the canonical/legacy inventory-expiry value and its reload scheduling without replacing global scheduler functions.

The merged implementation:

- resolves `showExpiryInInventory` and `showExpiryInInvetory` to one adapter-owned boolean;
- dual-writes both settings keys for compatibility;
- schedules inventory reload directly through the captured scheduler;
- cancels only its own preceding reload handle;
- uses a generation guard so a raced stale callback cannot reload inventory;
- preserves startup migration, widget normalization, corrected labels and hidden unsupported controls;
- proves unrelated scheduled events and removals remain untouched;
- registers the focused options Lua test as its own CTest target.

# Acceptance criteria

- [x] Canonical and legacy keys expose one adapter-owned value.
- [x] Setting either key dual-writes both settings keys.
- [x] Rapid changes cancel only the preceding inventory reload owned by the adapter.
- [x] The adapter never replaces global `scheduleEvent` or `removeEvent`.
- [x] Unrelated scheduled events and removals remain untouched.
- [x] Startup migration, widget normalization and termination cleanup remain covered.
- [x] The agent changelog was reconciled after the shared-path lease was released.
- [x] Focused CTest and final exact-head required CI passed.

# Validation and merge evidence

| Evidence | Result |
|---|---|
| stable base | `4e09e32032e64831c30d6f7aeb31a2ebd4d4520a` |
| final feature head | `cce607fe4b7555879347dd7ba6cc8a0abded71cb` |
| exact-head CI run | `30496430978`: PASS after one infrastructure-only failed-job retry |
| initial CMake Tests job | `90727208189`: external `freetype` download failure from GitLab before CTest |
| retry CMake Tests job | `90813266723`: PASS, including `Run CMake` and `Run CTest` |
| Lua Syntax | PASS |
| Fast Checks / static analysis | PASS |
| Fast Checks / syntax and workflow validation | PASS |
| CMake Release | PASS |
| Solution OpenGL | PASS |
| Solution DirectX | PASS |
| Solution Debug | PASS |
| `CI / Required` | PASS |
| comments, reviews and unresolved threads | none |
| feature PR | #93 |
| squash merge | `bdb73eea3c862f31e87fca81317ab3511c3a85a0` |

The failed first CMake Tests attempt was inspected before retry. It failed while vcpkg downloaded `freetype` from GitLab and did not execute CTest. The single failed-job retry used the unchanged final head and completed the required focused test evidence.

# Boundaries preserved

- no authentication, protocol, renderer, Canary, server or greenfield Rust runtime changes;
- no proprietary or downloaded assets;
- no global scheduler interception;
- no unrelated event cancellation;
- rollback is a normal squash revert of PR #93.

# Completion

- Final status: completed
- PR: #93
- Merge commit: `bdb73eea3c862f31e87fca81317ab3511c3a85a0`
- Changelog updated: yes
- Archived at: `docs/agents/tasks/archive/OTC-20260729-options-phase1-native-migration.md`
- Shared-path lease: released
