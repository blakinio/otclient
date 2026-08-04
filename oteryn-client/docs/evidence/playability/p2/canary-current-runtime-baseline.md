# Canary Current P2 Development Runtime Baseline

Status: the bounded local identity, login side-preamble, item-free local-player map, absent-tile, unknown ordinary remote-player appearance and session-end slices are merged. The parent producer remains blocked on authoritative item metadata and stack-identity ownership.

Evidence cut: generated P1 artifact and exact source from `blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3`.

Consumer boundary: `oteryn-client/crates/protocol-canary`.

## Claim boundary

This evidence proves only a development source baseline for already decrypted and deframed logical messages. It does not prove that a deployed Identity, Gateway or Canary instance runs this revision, configuration, build, feature set, framing/security mode or gameplay order.

Real Canary admission remains `RealAdmissionUnavailable` before network I/O. No credential, session key, private packet capture, deployed configuration, proprietary asset byte or copied producer implementation body is stored here. The parser does not own transport, simulation mutation, rendering or application composition.

## Normalized source profile

```yaml
schema: oteryn-canary-source-index-v1
repository: blakinio/canary
revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
server_release: 3.6.1
client_version: 1525
profile: ProtocolProfileId::Current
network_message_max_bytes: 65500
```

## Supported outbound development subset

```yaml
logout: 0x14
step_north: 0x65
step_east: 0x66
step_south: 0x67
step_west: 0x68
stop_movement: 0x69
step_north_east: 0x6A
step_south_east: 0x6B
step_south_west: 0x6C
step_north_west: 0x6D
```

`encode_current_development_command` accepts only a Current session-fenced merged `GameCommandEnvelope`, emits one byte for this subset and performs no network I/O.

## Merged inbound development slices

```yaml
bootstrap_order:
  local_player_initialization_0x17:
    retained: session_fenced_EntityHandle
  allow_bug_report_0x1A:
    layout: [0x1A, 0x00]
    retained: none
  tibia_time_0xEF:
    layout: [0xEF, clock_component_u8, clock_component_u8]
    retained: none
  pending_state_0x0A:
    output: GameEvent::BootstrapStarted
  enter_world_0x0F:
    output: caller_owned_order_state_only
  local_player_only_map_0x64:
    output: GameEvent::BootstrapCompleted
post_bootstrap:
  absent_tile_update_0x69:
    output: GameEvent::TileCleared
  unknown_remote_player_add_0x6A:
    output: GameEvent::EntityAppeared
terminal:
  session_end_0x18:
    accepted_values: [0x00, 0x02]
    output: GameEvent::SessionEnded
```

Every accepted boundary is bounded, session-fenced, trailing-data rejecting and state-atomic. No parser mutates simulation state.

## Item-free local-player map branch

The pinned producer permits one complete source-reachable bootstrap map branch without item-catalogue decoding: an existing item-free tile containing only the ordinary local player.

```yaml
opcode: 0x64
position: [x_u16_le, y_u16_le, z_u8]
viewport: 18_by_14
surface_floor_order: [7, 6, 5, 4, 3, 2, 1, 0]
underground_floor_window: z_minus_2_through_z_plus_2_clamped
missing_tile_encoding: [skip_u8, 0xFF]
accepted_tiles: exactly_one_local_player_tile
accepted_items: none
accepted_creatures: exactly_one_unknown_ordinary_local_player
identity: must_match_0x17_local_identity
output: GameEvent::BootstrapCompleted
general_map_claim: false
```

Every item, extra tile or creature, known-creature marker, non-local identity, unsupported player branch, malformed skip marker, impossible order, truncation, oversize and trailing data fails closed.

## Absent-tile update branch

`sendUpdateTile` emits opcode `0x69`, canonical `Position`, absent-tile marker `0x01` and terminator `0xFF` without a nested writer.

```yaml
logical_message: [0x69, x_u16_le, y_u16_le, z_u8, 0x01, 0xFF]
prerequisite: current_session_after_bootstrap_completed
output: GameEventEnvelope::v1(GameEvent::TileCleared)
```

Wrong opcode, marker, terminator, truncation, oversize, trailing data, stale/pre-bootstrap order and terminal state are rejected.

## Unknown ordinary remote-player appearance

Source classification: `PROVEN` for one narrow Current/non-legacy branch produced by `sendAddCreature` and `AddCreature` at the pinned revision.

```yaml
opcode: 0x6A
position: [x_u16_le, y_u16_le, z_u8]
floor_bound: 0_through_15
stack_bound: 0_through_9
unknown_creature_marker_u16_le: 0x61
known_cache_eviction_id_u32_le: 0
entity_id: nonzero_and_distinct_from_local_player
entity_type: ordinary_player
name_bound_bytes: 30
health_bound: 1_through_100
direction_bound: 0_through_7
icon_count_bound: 3
output: GameEventEnvelope::v1(GameEvent::EntityAppeared)
retained_fields: [entity_id, name, position, stack]
```

The parser consumes the complete ordinary Current player payload. Health, direction, outfit, mount, light, speed, icons, skull, party, guild, vocation, speech, inspection and walkability do not escape the adapter.

Known marker `0x62`, nonzero cache eviction, local identity reuse, hidden health, summon, monster, NPC, invisible/zero-looktype and OTCR extension branches remain unsupported and fail closed.

## Fixture provenance and sanitization

All hexadecimal fixtures under `oteryn-client/tests/integration/canary-world-protocol/fixtures/` are original synthetic already-decrypted logical messages. Coordinates, identities, names, appearance values, clock bytes and `synthetic://store` are invented test values.

The fixtures contain no credential, session key, private capture, deployed configuration, producer implementation body or proprietary asset. Positive, every-truncated-prefix, invalid-field, invalid-UTF-8, stale-session, pre-bootstrap, terminal-state, oversize and trailing-data cases are exercised for the remote-player slice.

## Terminal validation

```yaml
implementation_pr: 248
implementation_head: 70aeb1e2754a20b090422e435401ecb0b2f6e93e
implementation_merge: 26d5ed87552afe9b71245ba75fbb93fa66b2bc68
focused_windows:
  run: 30857020465
  job: 91830290527
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
fresh_audit:
  review_id: 4848927049
  critical_open: 0
  high_open: 0
  material_medium_open: 0
  unresolved_review_threads: 0
cleanup_pr: 249
cleanup_merge: 6b3efb75131f0ee1b9ce1779aa3ef7eaa1a536a2
cleanup_repository_ci:
  run: 30857557281
  required_job: 91832219075
  result: PASS
temporary_workflows_remaining: 0
temporary_scripts_remaining: 0
shared_path_lease: []
```

## Inbound readiness matrix

| Required family | Classification | Exact current evidence and missing contract |
|---|---|---|
| session bootstrap | `PARTIAL` | Exact order through local identity, bug-report permission, Tibia time, pending-state, enter-world and one complete item-free local-player map is implemented. General map admission remains incomplete. |
| map description | `PARTIAL` | One source-reachable item-free local-player-only `0x64` branch is implemented. General non-empty tiles require authoritative item metadata and broader creature/cache branches. |
| tile and stack updates | `PARTIAL` | The complete absent-tile `0x69 + position + 0x01 + 0xFF` branch is implemented as `TileCleared`. Non-empty tile descriptions and authoritative stack identity remain incomplete. |
| creature/entity appearance | `PARTIAL` | One complete post-bootstrap `0x6A` unknown ordinary remote-player branch with zero cache eviction is implemented as `EntityAppeared`. Broader creature branches remain unsupported. |
| movement and reconciliation | `BLOCKED` | Local steps append general map strips. Remote movement lacks an accepted caller-owned position/stack-to-domain-handle resolver. |
| removal | `BLOCKED` | Position plus stack index cannot be converted to an authoritative domain handle without caller-owned world state. |
| session end/logout | `PARTIAL` | Exact `0x18` layout and known values `0x00`/`0x02` are implemented; `0x01`/`0x03` remain rejected. |

No partial unsupported family is admitted.

## Remaining blockers

### Authoritative item catalogue

The producer's general `AddItem` layout branches on authoritative item-type and runtime instance metadata, including subtype/count, fluid or splash subtype, tier, animation phase, custom attributes and profile features. That catalogue is not owned by the protocol adapter. Inferring a branch or message length would be unsafe.

### Stack identity ownership

Movement and removal messages provide positions and stack indices while the merged domain contracts require session-fenced handles. No accepted caller-owned resolver currently maps these observations to authoritative item or entity handles without permitting partial decoding to mutate world state.

### Broader creature/cache branches

Known-creature cache transitions, nonzero eviction, hidden-health, summon, monster, NPC, invisible outfit and OTCR extension branches remain incomplete and unimplemented.

## E2E disposition

```yaml
result: NOT_APPLICABLE
reason: The package is an isolated producer adapter over already decrypted and deframed synthetic logical messages. It owns no real transport, admission, simulation mutation, renderer or reachable user journey.
```

## P2 barrier

```yaml
simulation_snapshot: archived
asset_decode: archived
renderer_resource: archived
input_platform: archived
canary_world_protocol: blocked_not_archived
visible_world_integration: not_ready
controlled_m2_acceptance: not_ready
```

The next safe action is to merge an accepted authoritative item-decoding dependency and caller-owned stack-identity resolver contract. Until then the parent task retains exclusive `protocol-canary` ownership, holds no shared lease and remains blocked rather than archived.


## Read-only entity reconciliation slice

Status: entity reconciliation slice merged as `d41a8155547d197ee18f9f390091f32ee3e64af6`; parent protocol task remains blocked on authoritative item metadata and local-player map strips.

Pinned producer revision `bc0068ab80bbf003e128fce0589b4cc89d2682d3` proves:

- remote non-teleport creature movement uses `0x6D + old Position + old stack u8 + new Position` when the creature is not the local player and both positions are visible;
- `RemoveTileThing` emits `0x6C + Position + stack u8` only for stack positions below ten;
- local-player movement appends map-strip payloads and is not part of this slice;
- `0x6C` remains generic at the producer, so this slice admits only a non-local entity resolved by caller-owned authoritative state.

The adapter introduces a read-only resolver contract using only protocol-neutral `TilePosition`, `StackIndex` and session-fenced `EntityHandle` values. Resolution happens after full bounded parsing and trailing-data rejection. Unknown, ambiguous, local-player, stale-session and invalid destination-stack outcomes fail closed. No resolver method may mutate simulation, and no Canary appearance, cache, item or map-strip field crosses the adapter boundary.

Original synthetic fixtures cover positive movement/removal, every truncated prefix, trailing movement data and an invalid removal stack. They contain no credentials, private captures, deployed configuration, proprietary assets or copied producer implementation bodies.


## Entity reconciliation validation

```yaml
product_head: daa7e5b09c06551a6f4ad94a69d00cbf65319133
rust_client:
  run: 30883311792
  windows_job: 91909062725
  supply_chain_job: 91909062730
  locked_metadata: PASS
  formatting: PASS
  strict_workspace_clippy: PASS
  workspace_tests: PASS
  architecture: PASS
  supply_chain: PASS
repository_ci:
  run: 30883312109
  required_job: 91909281559
  result: PASS
fresh_audit:
  comment_id: 5175281373
  result: PASS
  critical_high_material_medium_open: 0
e2e:
  result: NOT_APPLICABLE
  reason: Isolated producer adapter over already decrypted and deframed logical messages; no real transport, admission, simulation mutation, renderer or reachable user journey.
```


## Entity reconciliation post-merge closeout

```yaml
implementation_pr: 252
implementation_head: 41cfd39b847911d708429b8e23d4d17f9c1dc417
implementation_merge: d41a8155547d197ee18f9f390091f32ee3e64af6
closeout_pr: 254
final_exact_head_validation:
  rust_client_run: 30883672329
  windows_job: 91910151945
  supply_chain_job: 91910151992
  repository_ci_run: 30883672401
  repository_required_job: 91910412579
  result: PASS
ready_state_validation:
  repository_ci_run: 30883947811
  repository_required_job: 91911322995
  result: PASS
fresh_audit:
  comment_id: 5175281373
  result: PASS
  material_findings_open: 0
temporary_workflows_remaining: 0
temporary_scripts_remaining: 0
shared_path_lease: []
parent_task_status: blocked
remaining_blockers:
  - authoritative Current item-type and runtime AddItem branch metadata
  - complete local-player appended map-strip decoding
  - complete known/cache-eviction and non-player creature branches
```


## Closeout restack on current governance base

```yaml
closeout_pr: 254
restacked_base: 14e2718b7ff046b0620d5c838429cef81aa6d340
pre_checkpoint_head: 52942db86c6172974b4e5e80009c662f51ebb058
changed_runtime_paths: []
changed_closeout_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
  - oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md
product_validation_reused_from_exact_implementation_heads: true
final_closeout_exact_head_ci:
  head: 9d82234af1c23c2748984f613e8eab2fa89396da
  rust_client_run: 30885320351
  repository_ci_run: 30885320455
  result: PASS
```


## Known ordinary remote-player appearance

Status: known ordinary remote-player appearance merged as `804f793bac199f1d9c4ca2d5f7ade984801984ee`; the parent task remains active and blocked on item metadata, local map strips and remaining creature branches.

Pinned producer revision `bc0068ab80bbf003e128fce0589b4cc89d2682d3` proves that the known `AddCreature` branch writes marker `0x62` and the creature id, then the common appearance payload. Unlike the unknown branch, it writes no cache-eviction id, entity type or name in the header and omits guild emblem from the common payload.

The staged decoder accepts only a visible ordinary remote player with health `1..=100`, direction `0..=7`, nonzero outfit, at most three icons, final player type, unmarked state, no inspection and a closed walkthrough flag. It emits `EntityAppeared` with the wire-carried session-fenced entity and `name: None`. It never mutates or infers the producer cache.

The synthetic fixture and negative mutations cover every truncated prefix, wrong marker, hidden health, invalid direction, wrong final type, local/zero identity, stale/pre-bootstrap state and trailing data. No credential, private capture, proprietary asset or deployed configuration is included.


## Known ordinary remote-player appearance validation

```yaml
product_head: e952aea38ce93d873b0303556164e3f7a118f1d5
rust_client:
  run: 30894575347
  windows_job: 91944323324
  supply_chain_job: 91944323203
  locked_metadata: PASS
  formatting: PASS
  strict_workspace_clippy: PASS
  workspace_tests: PASS
  architecture: PASS
  supply_chain: PASS
repository_ci:
  run: 30894574150
  required_job: 91944797163
  result: PASS
fresh_audit:
  comment_id: 5176900934
  result: PASS
  critical_high_material_medium_open: 0
e2e:
  result: NOT_APPLICABLE
  reason: Isolated producer adapter over already decrypted and deframed logical messages; no real transport, admission, simulation mutation, renderer or reachable user journey.
```


## Known ordinary remote-player post-merge closeout

```yaml
implementation_pr: 256
implementation_head: 1128242ffd225c8e3c3db3e6da447817d02baa55
implementation_merge: 804f793bac199f1d9c4ca2d5f7ade984801984ee
closeout_pr: 258
exact_final_head_validation:
  rust_client_run: 30895233392
  windows_job: 91946458850
  supply_chain_job: 91946458966
  repository_ci_run: 30895233866
  repository_required_job: 91946738204
  result: PASS
ready_state_validation:
  repository_ci_run: 30895644663
  repository_required_job: 91948000133
  result: PASS
fresh_audit:
  comment_id: 5176900934
  result: PASS
  material_findings_open: 0
temporary_workflows_remaining: 0
temporary_scripts_remaining: 0
shared_path_lease: []
parent_task_status: blocked
remaining_blockers:
  - authoritative Current item-type and runtime AddItem branch metadata
  - authoritative item-instance identity for generic removal and replacement
  - complete local-player appended map strips
  - nonzero cache eviction, hidden/invisible and non-player creature appearance branches
```


## Known-player closeout current-main restack

```yaml
closeout_pr: 258
restacked_base: 9a0bd3c4da8f9f503c3cfafb9a2ca0d722a83638
pre_checkpoint_head: a4bef4989878d99e13805caa4d1d8575d803ba79
changed_runtime_paths: []
changed_closeout_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
  - oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md
exact_head_validation: pending
```


## Known-player closeout final current-main replay

```yaml
closeout_pr: 258
base: 33da70afd159d9b9963e6e9d80398c298b26ff5d
final_diff_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
  - oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md
exact_head_validation: pending
```


## Unknown ordinary monster and NPC appearance

Status: exact product validation passed on `f913e5ff5e4813e7ec2590122fc2ee3224aa901f` / PR `#261`; final validation-record CI pending.

Pinned producer revision `bc0068ab80bbf003e128fce0589b4cc89d2682d3` defines creature types player `0`, monster `1`, NPC `2`, player summon `3`, other summon `4` and hidden `5`. The unknown `AddCreature` header carries type and name after marker `0x61`, eviction id and entity id. The Current common payload writes a second final type; a monster with a player master is rewritten to summon-player and gains a master id.

The staged decoder accepts only zero eviction, visible health, nonzero outfit, header/final type equality for monster or NPC, at most three icons and the closed Current tail. It emits a session-fenced `EntityAppeared` as `Creature` or `NonPlayerCharacter`, retains a domain-bounded name and never mutates the producer cache.

Synthetic monster and NPC fixtures plus negative mutations cover every truncated prefix, known marker, nonzero eviction, player header, hidden health, invalid direction, invisible outfit, summon rewrite, local/zero identity, empty name, invalid floor/stack, stale/pre-bootstrap state and trailing data. No credential, private capture, proprietary asset or deployed configuration is included.


## Unknown ordinary monster and NPC validation

```yaml
product_head: f913e5ff5e4813e7ec2590122fc2ee3224aa901f
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
  comment_id: 5177542802
  result: PASS
  critical_high_material_medium_open: 0
e2e:
  result: NOT_APPLICABLE
  reason: Isolated producer adapter over already decrypted and deframed logical messages; no real transport, admission, simulation mutation, renderer or reachable user journey.
```


## Unknown non-player current-main restack

```yaml
pr: 261
current_base: 133388d61b787fb1829d740d0a1db581dccc3c4e
validated_product_head: f913e5ff5e4813e7ec2590122fc2ee3224aa901f
restack_head_before_metadata: 3253268c94ff1e05ff8bbcba12b3713c7336d28e
new_governance_read:
  - oteryn-client/AGENTS.md
  - oteryn-client/docs/architecture/ARCHITECTURE.md
  - oteryn-client/docs/architecture/decisions/ADR-001-dual-protocol-selection-and-async-transport.md
  - oteryn-client/docs/architecture/PROTOCOL_BOUNDARY.md
  - oteryn-client/docs/architecture/DUAL_PROTOCOL_EXECUTION_PLAN.md
  - oteryn-client/docs/agents/PROGRAM.md
  - oteryn-client/docs/agents/WORKSTREAMS.md
adapter_isolation: PASS
changed_runtime_semantics_after_product_validation: false
final_exact_head_ci: pending
```
