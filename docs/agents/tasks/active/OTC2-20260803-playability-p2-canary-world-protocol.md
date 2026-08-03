---
task_id: OTC2-20260803-playability-p2-canary-world-protocol
status: validating
agent: "P2 Canary world protocol worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-canary-world-protocol
phase: login-side-preamble-normalization
branch: feat/OTC2-20260803-canary-login-preamble
base_branch: main
created: 2026-08-03T02:04:00+02:00
updated: 2026-08-03T19:20:00+02:00
required_base_commit: "4fefec3ab3a1b6401cd3b89b6e0bb1dbcb2ce2a7"
risk: high
related_prs: [188, 190, 191, 192, 193, 196, 198, 203, 204, 219, 220, 221, 222, 223, 224, 225, 227, 228, 230, 231, 232, 233]
owned_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
  - oteryn-client/crates/protocol-canary/**
  - oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md
  - oteryn-client/tests/integration/canary-world-protocol/**
shared_path_lease: []
implementation_authorized: true
policy_version: 2.1
prompting_standard_version: 2.1
task_kind: implementation
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: terminal_only
context_pressure: high
decomposition_decision: phased
validation_level: heavy
complete_user_facing_feature: false
missing_layers:
  - complete provenance-safe Current non-empty map/tile/item/creature layouts
  - complete movement/removal branch layouts
  - accepted general position/stack-to-domain-handle identity-resolution ownership contract
  - product binding map and visible-world composition
  - controlled real M2 acceptance
invocation_started_at: 2026-08-03T10:16:00+02:00
last_progress_at: 2026-08-03T19:20:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: login-preamble-focused
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Goal

Reconcile pinned Canary Current evidence with the Rust client while preserving fail-closed real admission. Implement only gameplay mappings whose complete byte layout, feature gates, order and semantic ownership are proven without inference.

# Merged bounded protocol slices

```yaml
source_repository: blakinio/canary
source_revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
outbound_commands:
  logout: 0x14
  step_8_directions: [0x65, 0x66, 0x67, 0x68, 0x6A, 0x6B, 0x6C, 0x6D]
  stop_movement: 0x69
inbound_bootstrap_order:
  local_player_initialization_0x17:
    output: session_fenced_EntityHandle
  allow_bug_report_0x1A:
    fixed_payload: 0x00
    output: caller_owned_order_state_only
  tibia_time_0xEF:
    payload: [opaque_u8, opaque_u8]
    output: caller_owned_order_state_only
  pending_state_0x0A:
    prerequisites: [local_player_identity, allow_bug_report, tibia_time]
    output: GameEvent::BootstrapStarted
  enter_world_0x0F:
    prerequisites: [local_player_identity, pending_state]
    output: caller_owned_order_state_only
  bootstrap_completed_emitted: false
session_end_0x18:
  accepted_values: [0x00, 0x02]
  unknown_values_rejected: [0x01, 0x03]
empty_tile_update_0x69:
  layout: [opcode_u8, x_u16_le, y_u16_le, z_u8, marker_0x01, terminator_0xFF]
  prerequisite: current_session_after_enter_world
  output: GameEvent::TileCleared
  caller_state_mutation: false
```

The empty-tile branch is complete and independent of `GetTileDescription`, `AddItem`, `AddCreature` and position/stack identity resolution. The non-empty branch remains unsupported because it invokes variable nested writers.

# Empty-tile phase integration

```yaml
focused_product_head: 6bfaea45187176e7b956cb49aefbcf16523cc045
superseded_product_pr: 224
restacked_head: 8c6436aa8d87eead0a0f6f6d8592cd0ba3043aaf
implementation_pr: 230
implementation_merge: fe0e74bb1df56ad10aac39eef93c9132c09e2407
cleanup_pr: 231
cleanup_merge: f88a6ac21b078dc1d79cdcddfc1f05ffa1589235
changed_product_paths: 9
temporary_workflows_remaining: 0
temporary_scripts_remaining: 0
shared_path_lease: []
```

PR #224 was closed without merge after focused validation because its historical merge base exposed the temporary workflow in the diff. PR #230 restacked the exact product blobs on current `main` and contained only the nine allowed task/product/evidence/fixture paths. PR #231 removed the temporary runner.

# Validation and audit

```yaml
focused_validation:
  run: 30831813507
  job: 91747353789
  locked_metadata: PASS
  formatting: PASS
  strict_package_clippy: PASS
  protocol_canary_tests: 45_PASS
  architecture: PASS
restacked_exact_head_validation:
  head: 8c6436aa8d87eead0a0f6f6d8592cd0ba3043aaf
  rust_client_run: 30832279785
  windows_job: 91748896392
  supply_chain_job: 91748896261
  repository_ci_run: 30832280429
  repository_required_job: 91749201719
  result: PASS
cleanup_validation:
  repository_ci_run: 30832756476
  repository_required_job: 91750747579
  result: PASS
fresh_audit:
  review_id: 4846369910
  critical_open: 0
  high_open: 0
  material_medium_open: 0
unresolved_review_threads: 0
e2e:
  result: NOT_APPLICABLE
  reason: The isolated decoder consumes already decrypted and deframed logical messages and has no reachable real transport, simulation composition or user journey.
```

# Inbound readiness matrix

| Family | Classification | Durable decision |
|---|---|---|
| session bootstrap | `PARTIAL` | Local identity `0x17`, pending-state `0x0A` and enter-world `0x0F` are implemented in exact order. A complete map description remains required before `BootstrapCompleted`. |
| map description | `UNKNOWN` | Floor/tile iteration and skip markers are visible, but complete nested item/creature writers, bounds and feature branches are not normalized as one accepted Current layout. |
| tile and stack updates | `PARTIAL` | The complete absent-tile `0x69 + position + 0x01 + 0xFF` branch is implemented as `TileCleared`. The non-empty branch and stack identity remain blocked. |
| creature/entity appearance | `UNKNOWN` | Known-creature cache branches, removals, appearance fields, gates and nested bounds remain incomplete. |
| movement and reconciliation | `PARTIAL` | Local/remote/teleport/floor/map-strip branches remain incomplete; position plus stack does not prove a domain handle. |
| removal | `PARTIAL` | Position plus stack index cannot be converted to a protocol-neutral handle without authoritative state ownership. |
| session end/logout | `PARTIAL` | Exact `0x18` layout and values `0x00`/`0x02` are implemented; `0x01`/`0x03` remain unknown and rejected. |

No partial non-empty map, entity, movement or removal decoder is implemented. No parser mutates simulation state. Real admission remains `RealAdmissionUnavailable` before network I/O.


# Active login side-preamble phase

The complete Current producer order immediately following local identity is:

```yaml
local_player_initialization: 0x17
allow_bug_report: [0x1A, 0x00]
tibia_time: [0xEF, hour_component_u8, minute_component_u8]
pending_state: 0x0A
enter_world: 0x0F
```

This phase adds no gameplay event, world-clock state, simulation mutation,
transport framing, admission change or map claim. It only rejects bootstrap
sequences that omit or reorder the two proven logical messages.

# P2 barrier

```yaml
simulation_snapshot: archived
asset_decode: archived
renderer_resource: archived
input_platform: archived
canary_world_protocol: blocked_not_archived
visible_world_integration: not_ready
controlled_m2_acceptance: not_ready
```

The Visible World Integration task requires all five prerequisite producers to be merged and separately archived. This parent Canary producer remains incomplete, retains exclusive `protocol-canary` ownership and holds no shared-path lease.

# Durable checkpoint

```yaml
checkpoint_version: 21
updated_at: 2026-08-03T19:20:00+02:00
observed_main: 4fefec3ab3a1b6401cd3b89b6e0bb1dbcb2ce2a7
status: validating
phase: login-side-preamble-normalization
active_branch: feat/OTC2-20260803-canary-login-preamble
active_layouts: [allow_bug_report_0x1A, tibia_time_0xEF]
registration_pr: 233
validation: focused_workflow_running
implemented_bootstrap_order: [local_player_0x17, allow_bug_report_0x1A, tibia_time_0xEF, pending_state_0x0A, enter_world_0x0F]
shared_path_lease: []
ownership:
  protocol_canary: retained_by_active_parent_task
  shared_paths: released
blocker: Complete provenance-safe Current non-empty map/tile/item/creature layouts, remaining movement/removal branches and an accepted general position/stack-to-domain-handle identity-resolution ownership contract remain unavailable.
next_action: Validate and merge exact login side-preamble order, remove its temporary runner, then continue complete nested map writer normalization without inferring fields or ownership.
```
