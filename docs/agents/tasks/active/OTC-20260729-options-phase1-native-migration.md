---
task_id: OTC-20260729-options-phase1-native-migration
status: in_progress
agent: "GPT-5.6 Thinking"
track: legacy-client
branch: refactor/OTC-20260729-options-phase1-native-migration
base_branch: main
created: 2026-07-29T23:34:00+02:00
updated: 2026-07-30T00:28:00+02:00
last_verified_commit: ""
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
  - docs/agents/tasks/active/OTC-20260729-options-phase1-native-migration.md
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

# Goal

Harden the merged Phase 0 compatibility adapter by removing its temporary global `scheduleEvent`/`removeEvent` interception and giving inventory-expiry state and reload scheduling explicit adapter ownership.

# Delivered implementation

- canonical and legacy inventory-expiry keys now resolve to one adapter-owned boolean;
- both settings keys remain dual-written for compatibility;
- inventory reload is scheduled directly through the captured scheduler, without replacing global functions or invoking the defective legacy action;
- a generation guard prevents a raced stale callback from reloading inventory;
- rapid changes and module termination cancel only the adapter-owned handle;
- widget normalization, corrected labels and hidden unsupported controls remain unchanged;
- the focused Lua harness verifies global function identity, stale callback suppression, unrelated event isolation, dual-key behavior and termination cleanup;
- the options test is registered as its own CTest target so affected Windows validation executes it directly;
- the branch was rebuilt on current `main` commit `4e09e32032e64831c30d6f7aeb31a2ebd4d4520a` after PR #94 archived the W6 asset task.

# Acceptance criteria

- [x] Canonical and legacy keys expose one adapter-owned value.
- [x] Setting either key dual-writes both settings keys.
- [x] Rapid changes cancel only the preceding inventory reload owned by the adapter.
- [x] The adapter never replaces global `scheduleEvent` or `removeEvent`.
- [x] Unrelated scheduled events and removals remain untouched.
- [x] Startup migration, widget normalization and termination cleanup remain covered.
- [x] `docs/agents/CHANGELOG.md` was reconciled only after PR #92 released its explicit shared-path lease.
- [ ] Focused CTest and final exact-head required CI pass.

# Coordination

PR #92 released the changelog lease and PR #94 completed its separate task archive. PR #93 is rebuilt on exact current `main` commit `4e09e32032e64831c30d6f7aeb31a2ebd4d4520a`; the five-file diff does not overlap the #94 archive paths.

# Validation

- Head `b0b6a58ed2823e89e12299535e8bde10be7a85b2`, CI run `30493481912`: Lua Syntax, both Fast Checks and `CI / Required` passed; Windows was skipped by draft path detection, so this was not focused CTest evidence.
- Pre-reconciliation head `9127e9c535bebc5115beb4a94ba0728303d5cbd1`, run `30493781885`, and head `15c5e196100f703b4c10638a5838fed63a0ffbc5`, run `30495518738`, became non-final after `main` advanced and were intentionally superseded.
- Final exact-head validation is pending on the branch rebuilt from `4e09e32032e64831c30d6f7aeb31a2ebd4d4520a`.

# Completion

- Final status: in progress
- PR: #93
- Merge commit: pending
- Archived at: pending
