---
task_id: OTC2-20260803-playability-p2-simulation-snapshot
status: validating
agent: "P2 simulation/snapshot worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-simulation-snapshot
phase: final-exact-head-ci
branch: feat/OTC2-20260803-playability-p2-simulation-snapshot
base_branch: main
created: 2026-08-03T01:36:30+02:00
updated: 2026-08-03T01:56:00+02:00
last_verified_commit: "6b7fbeac921770168568bbb77148eff96ced468c"
required_base_commit: "07cbc0445241e50f439996b59024ca869c1b16cd"
risk: high
related_pr: 186
owned_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-simulation-snapshot.md
  - oteryn-client/crates/simulation-core/**
shared_path_lease:
  holder: OTC2-20260803-playability-p2-simulation-snapshot
  granted_at: 2026-08-03T01:52:00+02:00
  paths:
    - oteryn-client/Cargo.toml
    - oteryn-client/Cargo.lock
  release_condition: exact-head integration validation and protected merge or explicit rollback
implementation_authorized: true
policy_version: 2.1
prompting_standard_version: 2.1
task_kind: implementation
execution_mode: github-only
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_pressure: high
decomposition_decision: phased
validation_level: heavy
complete_user_facing_feature: false
missing_layers:
  - Canary gameplay decoder/encoder
  - asset decode and renderer resources
  - platform input adapter and product binding map
  - visible-world app composition and controlled M2 E2E
invocation_started_at: 2026-08-03T01:36:30+02:00
last_progress_at: 2026-08-03T01:56:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: final-exact-head
terminal_ci_wait_started_at: 2026-08-03T01:56:00+02:00
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Goal

Implement the sole protocol-neutral deterministic single-writer gameplay simulation and immutable renderer-facing snapshot producer accepted by the archived P1 aggregation barrier and `WAVE_P2_MINIMUM_VISIBLE_WORLD.md`.

# Proven launch state

- P1 aggregation implementation #184 merged as `95d18ca4e97920d1418a41762b86d92b7cf9516d`;
- P1 aggregation archive #185 merged as `07cbc0445241e50f439996b59024ca869c1b16cd`;
- all P1 shared integration leases were released before this task;
- no open branch, PR or active task owned `oteryn-client/crates/simulation-core/**` or the granted shared paths;
- architecture category `game-simulation` already permits only `foundation` and `game-domain`;
- merged `game-domain` supplies ordered session-fenced handles, positions and the closed v1 `GameEventEnvelope` vocabulary.

# Acceptance

- [x] one session-scoped owner atomically applies ordered `GameEventEnvelope` values;
- [x] stale/wrong-session events and invalid lifecycle transitions fail with stable errors and no partial mutation;
- [x] bootstrap establishes the local player and explicit bounded world state;
- [x] floors, tiles, stacks, entities, items, containers and capacities are checked and deterministic;
- [x] movement/removal/tile clear/resources/container/session-end families update state correctly;
- [x] immutable generation-stable `RenderSnapshot` exposes only renderer-required semantic state;
- [x] equal event streams produce equal snapshots;
- [x] public API exposes no mutable storage, Canary, socket, winit/Win32/wgpu, asset, UI or app types;
- [x] focused manifest-path format, strict Clippy and complete package tests pass;
- [x] fresh API/determinism/allocation/lifecycle audit has no open material finding;
- [x] coordinator granted only the minimal `Cargo.toml`/`Cargo.lock` lease;
- [x] root workspace member and local lockfile package are integrated without registry-dependency changes;
- [x] integration metadata, format, strict package Clippy, package tests and architecture policy pass;
- [ ] final exact-head Windows workspace, architecture, Supply Chain and repository CI pass;
- [ ] implementation protected-merges, task archives separately and lease releases.

# Delivered contract

The new `oteryn-simulation-core` package:

- depends only on exact local `oteryn-foundation` and `oteryn-game-domain`;
- uses bounded `BTreeMap`/`BTreeSet` state for canonical ordering;
- applies each event to a cloned bounded candidate and commits only after lifecycle, consistency and capacity validation;
- publishes immutable ordered tiles with semantic entity/item entries;
- retains container state outside the renderer-facing snapshot;
- clears all session-owned state on terminal session events;
- imposes absolute ceilings in addition to configurable non-zero limits;
- rejects removal/clearing that would leave an active local-player handle dangling;
- implements `ItemChanged` and `ContainerSlotChanged` as replacement semantics at the canonical location.

# Audit findings

## `P2-SIM-LIMIT-001`

Initial configurable limits were non-zero but had no absolute ceiling, allowing impractically large clone/allocation bounds.

Disposition: repaired with hard ceilings and explicit `LimitTooLarge` errors/tests.

## `P2-SIM-LOCAL-PLAYER-001`

Initial `EntityRemoved` and `TileCleared` handling could leave `RenderSnapshot::local_player` referencing an entity removed from tracked world state.

Disposition: repaired with an active-state invariant and atomic rejection tests for both event paths.

## `P2-SIM-ITEM-REPLACE-001`

Initial item/slot change handling rejected a different item already occupying the canonical location, contradicting the merged replacement semantics.

Disposition: repaired with deterministic location replacement and tile/container tests.

# Validation evidence

```yaml
focused:
  initial:
    run: 30772745325
    job: 91562631422
    result: FAIL
    cause:
      - one unused test-only import
      - one deterministic collapsible-if Clippy finding
    disposition: causally repaired; failed run produced no source commit
  repaired:
    run: 30772923833
    job: 91563102861
    result: PASS
    gates: [pinned_rustfmt, strict_package_clippy_all_targets, complete_package_tests]
audit_repair:
  run: 30773091019
  job: 91563552653
  result: PASS
  gates: [pinned_rustfmt, strict_package_clippy_all_targets, complete_package_tests]
integration:
  stale_delayed_run:
    run: 30773209435
    job: 91563889192
    result: FAIL_CLOSED
    cause: stale expected-parent guard rejected the delayed workflow before mutation
  accepted_run:
    run: 30773209464
    job: 91563869866
    result: PASS
    gates:
      - exact current main and ancestor check
      - Cargo metadata and generated lockfile
      - pinned workspace format
      - strict package Clippy with locked dependencies
      - complete package tests with locked dependencies
      - architecture workspace policy
      - exact lockfile addition allowlist
integration_head: 6b7fbeac921770168568bbb77148eff96ced468c
changed_paths: 5
unexpected_paths: 0
temporary_workflows_retained: false
workspace_delta:
  members_added: [crates/simulation-core]
lockfile_delta:
  local_packages_added: [oteryn-simulation-core]
  registry_packages_added: []
  dependencies: [oteryn-foundation, oteryn-game-domain]
open_material_findings: 0
```

## Context checkpoint

```yaml
checkpoint_version: 3
updated_at: 2026-08-03T01:56:00+02:00
content_reviewed_head: 6b7fbeac921770168568bbb77148eff96ced468c
branch: feat/OTC2-20260803-playability-p2-simulation-snapshot
pr: 186
status: validating
phase: final-exact-head-ci
base:
  main: 07cbc0445241e50f439996b59024ca869c1b16cd
  behind_by: 0
proven:
  - Exclusive source/manifest passes pinned format, strict Clippy and all package tests.
  - Public API and dependency direction remain protocol/platform/renderer/asset/UI/app neutral.
  - Hard ceilings, local-player consistency, replacement semantics and capacity rollback are tested.
  - Root workspace and lockfile changes are minimal and generated under the recorded lease.
  - Integration architecture policy passes without category or policy edits.
shared_lease:
  holder: OTC2-20260803-playability-p2-simulation-snapshot
  paths: [oteryn-client/Cargo.toml, oteryn-client/Cargo.lock]
  state: held_until_protected_merge
unknown: []
conflicts: []
blockers: []
next_action: Observe the final exact-head Rust Client and repository CI under the bounded terminal policy; on PASS recheck paths, lockfile and review hygiene, mark ready, protected-merge and separately archive the task while releasing the shared lease.
```
