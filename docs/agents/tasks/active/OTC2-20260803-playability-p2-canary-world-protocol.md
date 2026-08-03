---
task_id: OTC2-20260803-playability-p2-canary-world-protocol
status: validating
agent: "P2 Canary world protocol worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-canary-world-protocol
phase: unknown-player-appearance
branch: feat/OTC2-20260803-canary-unknown-player-appearance
base_branch: main
created: 2026-08-03T02:04:00+02:00
updated: 2026-08-03T23:30:00+02:00
required_base_commit: "ed355c66c305a4f7a42962bcc692194145626371"
risk: high
related_prs: [188, 190, 191, 192, 193, 196, 198, 203, 204, 219, 220, 221, 222, 223, 224, 225, 227, 228, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244]
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
invocation_started_at: 2026-08-03T19:01:00+02:00
last_progress_at: 2026-08-03T23:30:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: unknown-player-appearance-focused
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Goal

Reconcile pinned Canary Current evidence with the Rust client while preserving fail-closed real admission. Implement only protocol families whose complete byte layout, feature gates, order and semantic ownership are proven without inference.

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
    layout: [opcode_0x1A, fixed_permission_0x00]
    output: caller_owned_order_state_only
  tibia_time_0xEF:
    layout: [opcode_0xEF, clock_component_u8, clock_component_u8]
    output: caller_owned_order_state_only
  pending_state_0x0A:
    prerequisites: [local_player_identity, allow_bug_report, tibia_time]
    output: GameEvent::BootstrapStarted
  enter_world_0x0F:
    prerequisites: [local_player_identity, pending_state]
    output: caller_owned_order_state_only
  bootstrap_completed_emitted: true
unknown_remote_player_appearance_0x6A:
  prerequisite: completed_current_bootstrap
  accepted_branch: unknown_ordinary_player_with_zero_cache_eviction
  bounds: [floor_0_through_15, stack_0_through_9, name_max_30, icons_max_3]
  output: GameEvent::EntityAppeared
  retained_wire_fields: [entity_id, name, position, stack]
session_end_0x18:
  accepted_values: [0x00, 0x02]
  unknown_values_rejected: [0x01, 0x03]
empty_tile_update_0x69:
  layout: [opcode_u8, x_u16_le, y_u16_le, z_u8, marker_0x01, terminator_0xFF]
  prerequisite: current_session_after_bootstrap_completed
  output: GameEvent::TileCleared
  caller_state_mutation: false
```

All accepted boundaries are bounded, session-fenced, trailing-data rejecting and state-atomic. Raw producer creature IDs, clock values, store configuration and capability values do not escape the adapter. No parser mutates simulation state.

# Completed login side-preamble phase

The pinned Current local-player producer calls the following complete messages before pending-state:

```yaml
order:
  - local_player_initialization_0x17
  - allow_bug_report_0x1A_0x00
  - tibia_time_0xEF_two_u8
  - pending_state_0x0A
  - enter_world_0x0F
new_decoders:
  - decode_current_allow_bug_report
  - decode_current_tibia_time
retained_protocol_values: none
emitted_game_events: none
simulation_mutation: false
```

The fixed bug-report payload must be `0x00`. The two clock bytes are structurally consumed and deliberately discarded because protocol-canary does not own world-light simulation. Wrong order, wrong opcode, wrong fixed byte, truncation, oversize, stale session, duplicate use, terminal state and trailing data fail without advancing state.

# Phase integration

```yaml
registration_pr: 233
registration_merge: 4fefec3ab3a1b6401cd3b89b6e0bb1dbcb2ce2a7
historical_product_pr: 234
historical_product_head: 292755649226bd36422bf941afba5281a6713af7
runner_repair_pr: 235
runner_repair_merge: 29bc427a6f5c43218c8e2b1d6542cebb8499e5ad
restacked_product_pr: 236
restacked_product_head: 524c99598e49120fab7c6eff3fb00634e0a5d8b8
implementation_merge: 03cf57fca8f251e4b47fc1aefd56c67b6a788110
cleanup_pr: 237
cleanup_merge: 2f9ddc7fe9747740a42eebfaac677a1a49599f3c
changed_product_paths: 8
temporary_workflows_remaining: 0
temporary_scripts_remaining: 0
shared_path_lease: []
```

PR #234 was closed without merge after focused validation because its historical merge base exposed the temporary workflow in the product diff. PR #236 restacked the exact validated task/product/evidence/fixture blobs on current main and contained no workflow or patch-script change. PR #237 removed the one temporary runner.

# Validation and audit

```yaml
focused_windows_validation:
  run: 30837572720
  job: 91766409598
  rust: 1.94.0
  locked_metadata: PASS
  formatting: PASS
  strict_package_clippy: PASS
  protocol_canary_tests: 48_PASS
  architecture_tests: PASS
  architecture_workspace_policy: PASS
restacked_exact_head_validation:
  head: 524c99598e49120fab7c6eff3fb00634e0a5d8b8
  rust_client_run: 30837930784
  windows_job: 91767570065
  supply_chain_job: 91767570180
  repository_ready_ci_run: 30838016884
  repository_required_job: 91768642943
  result: PASS
cleanup_validation:
  repository_ci_run: 30838418308
  repository_required_job: 91769507878
  result: PASS
fresh_audit:
  review_id: 4847048515
  critical_open: 0
  high_open: 0
  material_medium_open: 0
unresolved_review_threads: 0
e2e:
  result: NOT_APPLICABLE
  reason: The isolated decoder consumes already decrypted and deframed logical messages and has no reachable real transport, simulation composition or user journey.
```

# Bounded map-source findings

The pinned producer establishes these outer boundaries:

```yaml
sendMapDescription:
  opcode: 0x64
  prefix: local_player_position_u16le_u16le_u8
  viewport: 18_by_14
GetMapDescription:
  surface_floors: 7_down_to_0
  underground_floor_window: z_minus_2_through_z_plus_2_clamped
  empty_run_encoding: [skip_u8, 0xFF]
```

A completely empty initial viewport is not source-reachable: the local player has already been placed on a tile before `sendMapDescription`, and `GetTileDescription` serializes creatures. The smallest reachable bootstrap map therefore still depends on `GetTileDescription` and `AddCreature`. Implementing a synthetic all-empty bootstrap decoder would accept a state the pinned producer cannot emit and is forbidden.

The complete non-empty family still delegates to:

```yaml
- GetFloorDescription
- GetTileDescription
- AddItem
- AddCreature
- knownCreatureSet eviction and known/unknown branches
- outfit, light, skull, type and feature-gated fields
- item subtype, tier, animation and custom-attribute branches
```

Local movement also appends map strips through `GetMapDescription`; remote movement and removal expose positions and stack indices but do not by themselves prove protocol-neutral domain handles.

# Inbound readiness matrix

| Family | Classification | Durable decision |
|---|---|---|
| session bootstrap | `PARTIAL` | Exact order through local identity, bug-report permission, Tibia time, pending-state and enter-world plus one complete item-free local-player map emits `BootstrapCompleted`; general map admission remains incomplete. |
| map description | `PARTIAL` | One complete item-free local-player-only `0x64` branch is implemented. General non-empty tiles remain blocked by authoritative item metadata and broader creature/cache branches. |
| tile and stack updates | `PARTIAL` | The complete absent-tile `0x69 + position + 0x01 + 0xFF` branch emits `TileCleared`. Non-empty tile bodies and authoritative stack identity remain blocked. |
| creature/entity appearance | `PARTIAL` | One complete post-bootstrap `0x6A` unknown ordinary remote-player branch with zero cache eviction emits `EntityAppeared`. Known/cache-eviction, hidden, summon, monster, NPC, invisible and OTCR branches remain unsupported. |
| movement and reconciliation | `PARTIAL` | Local steps append map strips; remote `0x6D` and remove/add branches still require authoritative identity and stack ownership. |
| removal | `PARTIAL` | Position plus stack index cannot be converted to a protocol-neutral item/entity handle without caller-owned world state. |
| session end/logout | `PARTIAL` | Exact `0x18` layout and values `0x00`/`0x02` are implemented; `0x01`/`0x03` remain rejected. |

Real admission remains `RealAdmissionUnavailable` before network I/O. No map-body, creature, item, movement or removal parser is partially admitted.


# Active local-player-only map bootstrap

The pinned source permits one complete initial-map branch without item-catalogue
decoding: an existing item-free tile containing only the ordinary local player.
The branch consumes the complete unknown-player payload, exact `18 x 14`
surface traversal and all skip markers.

```yaml
opcode: 0x64
position: [x_u16_le, y_u16_le, z_u8]
accepted_floor: source_valid_0_through_15
accepted_tiles: exactly_one_local_player_tile
accepted_items: none
accepted_creatures: exactly_one_unknown_ordinary_local_player
identity: must_match_session_local_player_from_0x17
output: GameEvent::BootstrapCompleted
simulation_mutation: false
general_map_claim: false
```

Other tiles, every item branch, known creatures, non-player creature types,
health-hidden players, zero-looktype outfits and extra contents remain rejected.


# Unknown ordinary remote-player appearance

The exact pinned `sendAddCreature` and `AddCreature` source proves one bounded
post-bootstrap entity branch that does not require ownership of the producer's
known-creature cache: opcode `0x6A`, canonical position, stack below ten,
unknown marker `0x61`, zero eviction id, a distinct non-zero player id and the
complete Current ordinary-player payload.

```yaml
accepted_opcode: 0x6A
accepted_marker: 0x61
accepted_cache_eviction: 0
accepted_entity_type: player
accepted_stack: 0_through_9
accepted_floor: 0_through_15
output: GameEvent::EntityAppeared
simulation_mutation: false
unsupported: [known_0x62, nonzero_eviction, hidden, summon, monster, npc, invisible, otcr]
```

The original synthetic fixture contains no capture, secret or proprietary asset
byte. Canary-only status and appearance fields are consumed but do not escape
the adapter.

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

The parent Canary producer remains incomplete, retains exclusive ownership of `protocol-canary` and holds no shared-path lease. Visible World Integration cannot start until the Canary producer is genuinely complete and separately archived.

# Durable checkpoint

```yaml
checkpoint_version: 24
updated_at: 2026-08-03T23:30:00+02:00
observed_main: ed355c66c305a4f7a42962bcc692194145626371
status: validating
phase: unknown-player-appearance
implemented_bootstrap_order: [local_player_0x17, allow_bug_report_0x1A, tibia_time_0xEF, pending_state_0x0A, enter_world_0x0F, local_player_only_map_0x64]
active_branch: feat/OTC2-20260803-canary-unknown-player-appearance
active_layout: unknown_ordinary_remote_player_add_0x6A
validation: focused_workflow_running
shared_path_lease: []
ownership:
  protocol_canary: retained_by_active_parent_task
  shared_paths: released
blocker: General AddItem decoding requires authoritative item-type branch metadata; movement and removal provide position/stack without an accepted protocol-neutral handle resolver; known/cache-eviction and non-player creature branches remain incomplete.
next_action: Validate and merge the unknown ordinary remote-player appearance, then terminally normalize the remaining item-catalogue and position/stack identity blockers without inference.
```
