---
task_id: OTC2-20260803-playability-p2-simulation-snapshot
status: completed
agent: "P2 simulation/snapshot worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-simulation-snapshot
phase: archived
branch: feat/OTC2-20260803-playability-p2-simulation-snapshot
base_branch: main
created: 2026-08-03T01:36:30+02:00
completed: 2026-08-03T02:01:06+02:00
archived: 2026-08-03T02:02:00+02:00
implementation_head: "7c523270ab3892c3b6c9dda5e0132ec8b941fc11"
required_base_commit: "07cbc0445241e50f439996b59024ca869c1b16cd"
merge_commit: "4c83e61293317346947de09ac4265e09b36f13a8"
risk: high
related_pr: 186
implementation_authorized: true
policy_version: 2.1
prompting_standard_version: 2.1
task_kind: implementation
execution_mode: github-only
validation_level: heavy
complete_user_facing_feature: false
missing_layers:
  - Canary gameplay decoder/encoder
  - asset decode and renderer resources
  - platform input adapter and product binding map
  - visible-world app composition and controlled M2 E2E
shared_path_lease:
  state: released
  granted_at: 2026-08-03T01:52:00+02:00
  released_by_merge: "4c83e61293317346947de09ac4265e09b36f13a8"
  paths:
    - oteryn-client/Cargo.toml
    - oteryn-client/Cargo.lock
---

# Result

Implemented and protected-merged the sole protocol-neutral deterministic single-writer simulation and immutable renderer-facing snapshot producer for the P2 minimum-visible-world wave.

The new `oteryn-simulation-core` package:

- depends only on exact local `oteryn-foundation` and `oteryn-game-domain`;
- applies session-fenced v1 `GameEventEnvelope` values atomically through a bounded candidate state;
- stores canonical bounded entity/item/container state in deterministic ordered maps;
- publishes immutable generation-stable `RenderSnapshot` values containing renderer-required semantic tiles, entities, items, local-player/resources and terminal state;
- enforces lifecycle, consistency, stack/location, capacity and hard-ceiling invariants;
- exposes no Canary, socket, platform, renderer/GPU, asset, UI or app-composition type;
- adds one workspace member and one local lockfile package with no registry dependency delta.

This is a `partial_producer`, not a playable feature and not M2. Runtime E2E is not applicable until later protocol, renderer, input and app-composition consumers exist.

# Final acceptance

- [x] one session-scoped owner atomically applies ordered gameplay events;
- [x] stale/wrong-session and invalid lifecycle input fails with stable errors and no partial mutation;
- [x] bootstrap establishes a valid active local player and bounded world state;
- [x] tiles/stacks/entities/items/containers/capacities are deterministic and bounded;
- [x] movement, removal, tile clear, resources, containers and session end are implemented;
- [x] immutable snapshots are canonically ordered and equal event streams yield equal snapshots;
- [x] public API is protocol/platform/renderer/asset/UI/app neutral;
- [x] focused and full exact-head validation pass;
- [x] fresh API, determinism, allocation and lifecycle audit has zero open material finding;
- [x] workspace/lockfile integration is minimal and architecture-compliant;
- [x] implementation PR #186 merged through protected auto-merge;
- [x] shared integration lease is released;
- [x] lifecycle record moved from active to archive in a separate closeout PR.

# Audit findings

## `P2-SIM-LIMIT-001`

Configurable non-zero limits initially lacked absolute ceilings.

Disposition: repaired with hard ceilings and explicit `LimitTooLarge` tests.

## `P2-SIM-LOCAL-PLAYER-001`

Initial entity removal/tile clear could leave a dangling active local-player reference.

Disposition: repaired with an active-state invariant and atomic rejection tests.

## `P2-SIM-ITEM-REPLACE-001`

Initial item/slot change rejected a different item at the canonical location instead of implementing merged replacement semantics.

Disposition: repaired with deterministic tile/container replacement tests.

# Final evidence

```yaml
implementation:
  pr: 186
  head: 7c523270ab3892c3b6c9dda5e0132ec8b941fc11
  exact_base: 07cbc0445241e50f439996b59024ca869c1b16cd
  merge: 4c83e61293317346947de09ac4265e09b36f13a8
  changed_paths: 5
  unexpected_paths: 0
  temporary_workflows_retained: false
workspace:
  member_added: crates/simulation-core
  lockfile_local_package: oteryn-simulation-core
  registry_packages_added: []
  dependencies: [oteryn-foundation, oteryn-game-domain]
validation:
  focused_initial:
    run: 30772745325
    job: 91562631422
    result: deterministic_clippy_failure_repaired_without_source_commit
  focused_repaired:
    run: 30772923833
    job: 91563102861
    result: PASS
  audit_repair:
    run: 30773091019
    job: 91563552653
    result: PASS
  integration_stale_delayed:
    run: 30773209435
    job: 91563889192
    result: fail_closed_on_expected_parent_before_mutation
  integration_accepted:
    run: 30773209464
    job: 91563869866
    result: PASS
  rust_client:
    run: 30773280849
    windows_job: 91564064410
    supply_chain_job: 91564064434
    result: PASS
  repository_ci:
    run: 30773280916
    required_job: 91564169956
    result: PASS
  ready_state_ci:
    run: 30773414335
    required_job: 91564557710
    result: PASS
  review_hygiene:
    comments: 0
    reviews: 0
    review_threads: 0
  audit:
    open_material_findings: 0
blockers: []
```

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-03T02:02:00+02:00
head: 4c83e61293317346947de09ac4265e09b36f13a8
branch: main
pr: 186
status: completed
phase: archived
proven:
  - The sole P2 simulation/snapshot producer is merged and validated.
  - Its public contract consumes only merged game-domain events and publishes immutable semantic snapshots.
  - Workspace and lockfile integration are minimal and exact-head green.
  - The serialized shared integration lease is released.
blockers: []
next_action: After this archive PR merges, open the P2 CANARY-WORLD-PROTOCOL task from exact current main. First align the development runtime descriptor mechanically with the generated bc0068ab source index while preserving real admission fail-closed; do not implement or guess unsupported layouts before exact evidence exists.
```
