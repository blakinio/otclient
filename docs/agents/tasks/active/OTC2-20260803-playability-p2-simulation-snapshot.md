---
task_id: OTC2-20260803-playability-p2-simulation-snapshot
status: integration_ready
agent: "P2 simulation/snapshot worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-simulation-snapshot
phase: shared-integration
branch: feat/OTC2-20260803-playability-p2-simulation-snapshot
base_branch: main
created: 2026-08-03T01:36:30+02:00
updated: 2026-08-03T01:52:00+02:00
last_verified_commit: "f4f8affd5c415dc906142cdd1219ace4b23f0ac6"
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
last_progress_at: 2026-08-03T01:52:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: shared-integration
terminal_ci_wait_started_at: null
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
- all P1 shared integration leases are released;
- no open branch, PR or active task owns `oteryn-client/crates/simulation-core/**`;
- architecture category `game-simulation` already permits only the required lower-layer dependency direction;
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
- [x] focused manifest-path format, strict Clippy and complete package tests pass before any shared lease;
- [x] fresh API/determinism/allocation/lifecycle audit has no open material finding;
- [x] coordinator grants only the minimal Cargo.toml/Cargo.lock lease after exclusive validation;
- [ ] root workspace member and local lockfile package are integrated without registry-dependency changes;
- [ ] exact-head workspace, architecture, Supply Chain and repository CI pass;
- [ ] implementation protected-merges, task archives separately and lease releases.

# Exclusive implementation result

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

Initial configurable limits were non-zero but had no absolute ceiling, allowing a caller to select impractically large clone/allocation bounds.

Disposition: repaired with hard ceilings and explicit `LimitTooLarge` errors/tests.

## `P2-SIM-LOCAL-PLAYER-001`

Initial `EntityRemoved` and `TileCleared` handling could leave `RenderSnapshot::local_player` referencing an entity removed from tracked world state.

Disposition: repaired with an active-state invariant and atomic rejection tests for both event paths.

## `P2-SIM-ITEM-REPLACE-001`

Initial item/slot change handling inserted the new handle but rejected a different item already occupying the canonical location, contradicting the merged event replacement semantics.

Disposition: repaired with deterministic location replacement and tile/container tests.

# Focused validation

```yaml
initial_focused:
  run: 30772745325
  job: 91562631422
  result: FAIL
  cause:
    - one unused test-only import
    - one deterministic collapsible-if Clippy finding
  disposition: causally repaired without source commit from the failed run
repaired_focused:
  run: 30772923833
  job: 91563102861
  result: PASS
  gates:
    - pinned Rust 1.94 rustfmt
    - strict package Clippy with all targets
    - complete package tests
audit_repair:
  run: 30773091019
  job: 91563552653
  result: PASS
  gates:
    - pinned Rust 1.94 rustfmt
    - strict package Clippy with all targets
    - complete package tests
exclusive_head: f4f8affd5c415dc906142cdd1219ace4b23f0ac6
exclusive_changed_paths: 3
unexpected_paths: 0
temporary_workflows_retained: false
open_material_findings: 0
```

## Context checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-03T01:52:00+02:00
head: f4f8affd5c415dc906142cdd1219ace4b23f0ac6
branch: feat/OTC2-20260803-playability-p2-simulation-snapshot
pr: 186
status: integration_ready
phase: shared-integration
base:
  main: 07cbc0445241e50f439996b59024ca869c1b16cd
  behind_by: 0
proven:
  - Exclusive source/manifest package passes pinned format, strict Clippy and all package tests.
  - Public API and dependency direction remain protocol/platform/renderer/asset/UI/app neutral.
  - Hard ceilings, local-player consistency, item replacement and capacity rollback are explicitly tested.
  - Final exclusive diff contains only the task and simulation-core package.
shared_lease:
  holder: OTC2-20260803-playability-p2-simulation-snapshot
  paths:
    - oteryn-client/Cargo.toml
    - oteryn-client/Cargo.lock
  conflict_check: PASS
unknown: []
conflicts: []
blockers: []
next_action: Add one workspace member and generate the minimal local-package lockfile delta under the granted lease, then run exact-head Rust Client and repository CI and perform final changed-path/lockfile/review audit.
```
