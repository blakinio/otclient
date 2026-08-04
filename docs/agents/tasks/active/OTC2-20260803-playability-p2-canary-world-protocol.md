---
task_id: OTC2-20260803-playability-p2-canary-world-protocol
status: validating
agent: "P2 Canary world protocol worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-canary-world-protocol
phase: unknown-nonplayer-appearance-terminal-ci
branch: feat/OTC2-20260804-canary-unknown-nonplayer-appearance
base_branch: main
created: 2026-08-03T02:04:00+02:00
updated: 2026-08-04T12:31:00+02:00
required_base_commit: "644df4c93a19840886cc7544b830df0de24f4524"
risk: high
related_prs: [188, 190, 191, 192, 193, 196, 198, 203, 204, 219, 220, 221, 222, 223, 224, 225, 227, 228, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 254, 256, 258, 261]
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
  - authoritative Current item-type metadata and complete AddItem branch contract
  - authoritative item-instance identity for generic removal and replacement
  - nonzero known-cache eviction, hidden-health, summon and extension branches
  - complete local-player appended map-strip reconciliation
  - product binding map and visible-world composition
  - controlled real M2 acceptance
invocation_started_at: 2026-08-03T19:01:00+02:00
last_progress_at: 2026-08-04T12:31:00+02:00
ci_checks_for_current_head: 3
ci_check_generation: unknown-nonplayer-appearance-final-exact-head
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 2
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Goal

Reconcile pinned Canary Current evidence with the Rust client while preserving fail-closed real admission. Implement only inbound protocol families whose complete byte layout, ordering, feature gates, bounds and semantic ownership are proven without inference.

# Terminal result of the completed phase

The post-merge Windows newline repair is terminal, the historical `Cargo.lock` lease is released, and the parent task now contains the following merged provenance-safe inbound slices:

```yaml
source_repository: blakinio/canary
source_revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
profile: ProtocolProfileId::Current
network_message_max_bytes: 65500
real_admission: RealAdmissionUnavailable
shared_path_lease: []
merged_slices:
  local_player_initialization_0x17: session_fenced_local_EntityHandle
  allow_bug_report_0x1A: fixed_0x00_order_only
  tibia_time_0xEF: two_u8_consumed_and_discarded
  pending_state_0x0A: GameEvent::BootstrapStarted
  enter_world_0x0F: order_only
  local_player_only_map_0x64: GameEvent::BootstrapCompleted
  absent_tile_update_0x69: GameEvent::TileCleared
  unknown_remote_player_add_0x6A: GameEvent::EntityAppeared
  session_end_0x18: GameEvent::SessionEnded
```

All accepted slices are bounded, session-fenced, reject trailing data, fail atomically and do not mutate simulation state. Canary-only capability, clock, appearance, health, direction, light, speed, icon, skull, party, guild, vocation, speech, inspection and walkability fields do not escape the adapter boundary.

# Unknown ordinary remote-player appearance

The completed phase proves and implements only this exact Current/non-legacy producer branch:

```yaml
opcode: 0x6A
position: [x_u16_le, y_u16_le, z_u8]
floor_bound: 0_through_15
stack_bound: 0_through_9
creature_marker_u16_le: 0x61
known_cache_eviction_id_u32_le: 0
entity_id: nonzero_and_distinct_from_local_player
entity_type: ordinary_player
name_bound_bytes: 30
icon_count_bound: 3
output: GameEventEnvelope::v1(GameEvent::EntityAppeared)
retained_fields: [entity_id, name, position, stack]
```

The implementation rejects known marker `0x62`, nonzero cache eviction, local identity reuse, hidden health, summon, monster, NPC, invisible/zero-looktype and OTCR extension branches. The fixture is original synthetic logical-message data and contains no credential, session key, private capture, deployed configuration, proprietary asset byte or copied producer implementation body.

# Inbound readiness matrix

| Family | Classification | Durable decision |
|---|---|---|
| session bootstrap | `PARTIAL` | Exact order through local identity, bug-report permission, Tibia time, pending-state, enter-world and one item-free local-player map is implemented. General map admission remains incomplete. |
| map description | `PARTIAL` | One complete item-free local-player-only `0x64` branch is implemented. General non-empty tiles require authoritative item metadata and broader creature/cache branches. |
| tile and stack updates | `PARTIAL` | The complete absent-tile `0x69 + position + 0x01 + 0xFF` branch emits `TileCleared`. Non-empty tile bodies and authoritative stack identity remain blocked. |
| creature/entity appearance | `PARTIAL` | Complete ordinary-player branches are merged. This phase stages the complete unknown zero-eviction visible monster/NPC `0x61` subfamily. Nonzero eviction, hidden, summon, invisible and OTCR branches remain unsupported. |
| movement and reconciliation | `PARTIAL` | The complete remote non-teleport `0x6D` layout is implemented behind a read-only caller-owned resolver that supplies the session-fenced entity and destination stack. Local-player movement and appended map strips remain blocked. |
| removal | `PARTIAL` | The complete remote-entity `0x6C` layout is implemented behind a read-only caller-owned resolver. Item removal and local-player teleport/map-reset branches remain unsupported. |
| session end/logout | `PARTIAL` | Exact `0x18` layout and values `0x00`/`0x02` are implemented; `0x01`/`0x03` remain rejected. |

No partial unsupported family is admitted. Unknown subfamilies fail closed.

# Caller-owned entity reconciliation continuation

The pinned producer proves two complete field layouts that can be normalized without owning world state when the caller supplies a read-only authoritative observation resolver:

```yaml
source_revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
branch: feat/OTC2-20260803-canary-entity-reconciliation
pr: 252
remote_entity_movement:
  opcode: 0x6D
  layout: [old_position_u16_u16_u8, old_stack_u8, new_position_u16_u16_u8]
  source_branch: non_local_non_teleport_creature_visible_at_old_and_new_position
  resolver_output: [session_fenced_entity_handle, destination_stack]
  event: GameEvent::EntityMoved
remote_entity_removal:
  opcode: 0x6C
  layout: [position_u16_u16_u8, stack_u8]
  accepted_object: caller_resolved_non_local_entity
  event: GameEvent::EntityRemoved
resolver_contract:
  ownership: caller
  access: read_only
  malformed_input_invocation: forbidden
  simulation_mutation: false
  unresolved_or_ambiguous: fail_closed
shared_path_lease: []
validation:
  exact_product_head: daa7e5b09c06551a6f4ad94a69d00cbf65319133
  rust_client_run: 30883311792
  windows_job: 91909062725
  supply_chain_job: 91909062730
  repository_ci_run: 30883312109
  repository_required_job: 91909281559
  result: PASS
```

Local-player movement is excluded because its producer branch appends map strips. Generic item removal is excluded because this phase does not own or infer item identity. General map and tile decoding remain blocked by authoritative item metadata.

# Known ordinary remote-player appearance continuation

The pinned Current producer proves a second complete ordinary-player `sendAddCreature` family that does not require item metadata or mutable cache ownership:

```yaml
source_revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
branch: feat/OTC2-20260804-canary-known-player-appearance
pr: 256
opcode: 0x6A
position: [x_u16_le, y_u16_le, z_u8]
stack_bound: 0_through_9
known_marker_u16_le: 0x62
entity_id: nonzero_and_distinct_from_local_player
known_header_omits: [cache_eviction_id, entity_type, name]
common_payload:
  health: 1_through_100
  direction: 0_through_7
  visible_outfit: required
  guild_emblem: omitted_for_known_branch
  final_entity_type: ordinary_player
output: GameEventEnvelope::v1(GameEvent::EntityAppeared)
output_name: null
cache_mutation: false
shared_path_lease: []
validation:
  product_head: e952aea38ce93d873b0303556164e3f7a118f1d5
  rust_client_run: 30894575347
  windows_job: 91944323324
  supply_chain_job: 91944323203
  repository_ci_run: 30894574150
  repository_required_job: 91944797163
  result: PASS
```

The adapter accepts the wire-carried session-fenced entity identity but does not create, mutate or infer the producer's known-creature cache. Hidden health, invisible outfits, summons, monsters, NPCs, nonzero eviction and OTCR extensions remain rejected.

# Unknown ordinary monster and NPC continuation

Pinned Current source proves a complete zero-eviction unknown non-player subfamily without item metadata or cache mutation:

```yaml
source_revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
branch: feat/OTC2-20260804-canary-unknown-nonplayer-appearance
pr: 261
opcode: 0x6A
marker_u16_le: 0x61
cache_eviction_u32_le: 0
accepted_header_types:
  monster: 1
  npc: 2
name_bound: protocol_neutral_NameText_64_bytes
health: 1_through_100
visible_outfit: required
final_type: must_equal_header_type
rejected_types: [player_0, summon_player_3, summon_others_4, hidden_5]
outputs:
  monster: GameEvent::EntityAppeared(EntityKind::Creature)
  npc: GameEvent::EntityAppeared(EntityKind::NonPlayerCharacter)
cache_mutation: false
shared_path_lease: []
validation:
  product_head: f913e5ff5e4813e7ec2590122fc2ee3224aa901f
  rust_client_run: 30899069326
  windows_job: 91958836539
  supply_chain_job: 91958836582
  repository_ci_run: 30899073315
  repository_required_job: 91959144109
  result: PASS
```

For monsters with a player master, the producer rewrites the final type to summon-player and appends a master id. Requiring final type equality rejects that branch atomically. Hidden health, zero outfit, nonzero eviction and extensions remain fail-closed.

# Exact blocker normalization

## Authoritative item metadata

`AddItem` is not a fixed-width wire family. Its complete Current layout branches on authoritative item-type and runtime instance metadata, including subtype/count, fluid or splash subtype, tier, animation phase, custom attributes and profile features. The protocol adapter does not own the producer's item catalogue. Decoding a general tile or map body without that authoritative dependency would require guessing message length or branch selection and is forbidden.

## Position/stack identity resolution

Merged PR `#252` now provides a read-only caller-owned resolver for complete remote entity movement and entity-only removal. It supplies session-fenced entity identity and destination ordering only after bounded parsing succeeds, without mutating simulation. Generic item removal remains blocked because no authoritative item-instance resolver exists, and local-player movement remains blocked because its producer branch appends map-strip payloads whose general tile/item families are incomplete.

## Remaining creature branches

The complete known ordinary-player appearance branch was merged in PR `#256`. Nonzero cache eviction, non-player types, hidden-health, summon, invisible outfit and OTCR extension branches are not normalized as complete accepted families. They remain `UNKNOWN` and unimplemented.

# Validation

```yaml
implementation_pr: 248
implementation_head: 70aeb1e2754a20b090422e435401ecb0b2f6e93e
implementation_merge: 26d5ed87552afe9b71245ba75fbb93fa66b2bc68
focused_windows:
  workflow: OTC2 Canary Unknown Player Appearance
  run: 30857020465
  job: 91830290527
  result: PASS
  rust: 1.94.0
  locked_metadata: PASS
  formatting: PASS
  strict_package_clippy: PASS
  protocol_canary_tests: 57_PASS
  architecture_tests: PASS
  architecture_workspace_policy: PASS
exact_head_rust_client:
  run: 30857235341
  windows_job: 91830984449
  supply_chain_job: 91830984426
  result: PASS
exact_head_repository_ci:
  run: 30857235601
  required_job: 91831301928
  result: PASS
cleanup_pr: 249
cleanup_head: be83f3caf7444293defc7cdeee8b8b11f3a747bc
cleanup_merge: 6b3efb75131f0ee1b9ce1779aa3ef7eaa1a536a2
cleanup_repository_ci:
  run: 30857557281
  required_job: 91832219075
  result: PASS
temporary_workflows_remaining: 0
temporary_scripts_remaining: 0
shared_path_lease: []
```

# Independent audit

```yaml
validator: fresh_exact_head_falsification_audit
review_id: 4848927049
reviewed_head: 70aeb1e2754a20b090422e435401ecb0b2f6e93e
critical_open: 0
high_open: 0
material_medium_open: 0
unresolved_review_threads: 0
fixture_provenance: PASS
fixture_sanitization: PASS
dependency_direction: PASS
negative_case_behavior: PASS
```

The cleanup PR received a separate workflow-only audit with zero material findings.

# PR hygiene

```yaml
188: merged
190: merged_terminal_newline_repair
240: merged_local_player_only_map
241: merged_then_removed_local_map_runner
242: merged_unknown_player_runner_registration
243: closed_unmerged_duplicate
244: closed_unmerged_superseded_after_restack
245: merged_guarded_restack_repair
246: merged_exit_and_identity_repair
247: closed_unmerged_duplicate
248: merged_unknown_player_implementation
249: merged_temporary_runner_cleanup
open_related_prs: 0
unresolved_review_threads: 0
```

# E2E disposition

```yaml
result: NOT_APPLICABLE
reason: This package is an isolated producer adapter over already decrypted and deframed synthetic logical messages. It owns no real transport, admission, simulation mutation, renderer or reachable user journey.
```

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

The parent Canary task remains active and blocked. It retains exclusive `protocol-canary` ownership, holds no shared-path lease and cannot claim general Canary compatibility, M2 completion or visible-world completion.

# Durable checkpoint

```yaml
checkpoint_version: 36
updated_at: 2026-08-04T12:31:00+02:00
observed_main: 644df4c93a19840886cc7544b830df0de24f4524
status: validating
phase: unknown-nonplayer-appearance-terminal-ci
active_branch: feat/OTC2-20260804-canary-unknown-nonplayer-appearance
pr: 261
base: 644df4c93a19840886cc7544b830df0de24f4524
validated_product_head: f913e5ff5e4813e7ec2590122fc2ee3224aa901f
changed_paths:
  - oteryn-client/crates/protocol-canary/src/lib.rs
  - oteryn-client/crates/protocol-canary/src/non_player.rs
  - oteryn-client/crates/protocol-canary/src/non_player/tests.rs
  - oteryn-client/tests/integration/canary-world-protocol/fixtures/unknown-monster-appearance.hex
  - oteryn-client/tests/integration/canary-world-protocol/fixtures/unknown-npc-appearance.hex
  - oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
implementation:
  unknown_monster_appearance_0x6A_0x61_type_1: complete
  unknown_npc_appearance_0x6A_0x61_type_2: complete
  cache_eviction: zero_only
  cache_mutation: false
validation:
  rust_client:
    run: 30899069326
    windows_job: 91958836539
    supply_chain_job: 91958836582
    locked_metadata: PASS
    formatting: PASS
    strict_workspace_clippy: PASS
    workspace_tests: PASS
    architecture: PASS
    supply_chain: PASS
  repository_ci:
    run: 30899073315
    required_job: 91959144109
    result: PASS
fresh_audit:
  exact_head: f913e5ff5e4813e7ec2590122fc2ee3224aa901f
  comment_id: 5177542802
  result: PASS
  critical_open: 0
  high_open: 0
  material_medium_open: 0
  unresolved_review_threads: 0
e2e:
  result: NOT_APPLICABLE
  reason: Isolated producer adapter over already decrypted and deframed logical messages; no real transport, admission, simulation mutation, renderer or reachable user journey.
temporary_workflows_remaining: 0
temporary_scripts_remaining: 0
shared_path_lease: []
ownership:
  protocol_canary: retained
  shared_paths: released
remaining_blocker: General AddItem/non-empty map decoding still requires authoritative Current item metadata; local-player movement requires complete map strips; nonzero eviction, hidden/invisible, summon and extension branches remain incomplete.
next_action: Run final exact-head CI for the validation checkpoint, mark PR 261 ready, protected-merge it, then persist the active blocked parent state and continue to the next complete source-proven family.
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 3
  session_id: OTC2-20260804T1043+0200-nonplayer
  session_started_at: 2026-08-04T12:10:00+02:00
  checkpointed_at: 2026-08-04T12:31:00+02:00
  last_progress_at: 2026-08-04T12:31:00+02:00
  phase: unknown-nonplayer-appearance-terminal-ci
  exact_head: f913e5ff5e4813e7ec2590122fc2ee3224aa901f
  pull_request: 261
  active_operation: final exact-head CI, protected merge and blocked-parent reconciliation
  external_run_ids:
    - 30899069326
    - 30899073315
  operation_started_at: 2026-08-04T12:31:00+02:00
  wait_deadline_at: 2026-08-04T13:16:00+02:00
  check_generation: unknown-nonplayer-appearance-final-exact-head
  checks_used: 2
  status: ready
  safe_to_resume: true
  resume_condition: Merge PR 261 only after the validation-record head passes all exact-head required checks; otherwise preserve the precise failure.
  next_action: Reconcile PR 261 terminal state, then continue the parent task from its remaining item, summon and hidden/extension blockers.
```
