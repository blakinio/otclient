# Canary Current P2 Development Runtime Baseline

Status: local-player identity, login side-preamble, session-end and absent-tile slices are merged; one source-reachable item-free local-player map bootstrap is under exact validation.

Evidence cut: generated P1 artifact and exact source from `blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3`.

Consumer boundary: `oteryn-client/crates/protocol-canary`.

## Claim boundary

This document aligns a development source baseline only. It does not prove that a deployed Identity, Gateway or Canary instance runs this revision, configuration, build, feature set, framing/security mode or gameplay order.

Real Canary admission remains fail-closed. No credential, session key, private packet capture, proprietary asset byte or copied producer implementation body is stored here. The parser consumes already decrypted and deframed logical messages and does not own transport, simulation, rendering or application composition.

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

## Proven bootstrap identity and order

The exact Current/non-legacy local branch of `ProtocolGame::sendAddCreature` now has this normalized logical-message order:

```yaml
local_player_initialization:
  opcode: 0x17
  retained: session_fenced_EntityHandle
  discarded: [server_beat, speed_formula, capability_bytes, store_url, store_coin_packet, exiva_flag]
allow_bug_report:
  producer: sendAllowBugReport
  layout: [0x1A, 0x00]
  retained: none
tibia_time:
  producer: sendTibiaTime
  layout: [0xEF, clock_component_u8, clock_component_u8]
  retained: none
pending_state:
  opcode: 0x0A
  prerequisites: [local_player_identity, allow_bug_report, tibia_time]
  output: GameEvent::BootstrapStarted
enter_world:
  opcode: 0x0F
  prerequisites: [local_player_identity, pending_state]
  output: caller_owned_order_state_only
bootstrap_completed:
  emitted: false
  missing_required_value: validated_map_position_and_body
```

The fixed bug-report byte must be `0x00`. The clock components are consumed structurally and intentionally discarded because protocol-canary does not own world-light simulation. Every boundary is bounded, session-fenced, trailing-data rejecting and state-atomic.

Invalid precision, fixed fields, boolean, zero identity, wrong order, wrong opcode, truncation, oversize, stale session, duplicate use, terminal state and trailing data fail closed.

## Proven session-end boundary

The producer emits opcode `0x18`, one `SessionEndInformations` byte and disconnects.

```yaml
0x00: SESSION_END_LOGOUT
0x02: SESSION_END_FORCECLOSE
0x01: UNKNOWN_REJECTED
0x03: UNKNOWN_REJECTED
semantic_output: GameEvent::SessionEnded(ServerClosed)
```

The conservative semantic reason is required because this isolated decoder has no caller-owned outbound-command history sufficient to prove `Requested`.

## Proven absent-tile update branch

`ProtocolGame::sendUpdateTile` writes opcode `0x69` and calls `NetworkMessage::addPosition`, whose exact layout is `x:u16le`, `y:u16le`, `z:u8`. When the tile pointer is absent, the producer writes fixed marker `0x01` followed by terminator `0xFF` and does not call a nested writer.

```yaml
logical_message:
  opcode_u8: 0x69
  x_u16_le: canonical_tile_x
  y_u16_le: canonical_tile_y
  z_u8: canonical_floor
  absent_tile_marker_u8: 0x01
  terminator_u8: 0xFF
prerequisite: current_session_after_bootstrap_completed
output: GameEventEnvelope::v1(GameEvent::TileCleared)
caller_state_mutation: false
nested_writer_dependency: none
```

The decoder rejects every truncated prefix, wrong opcode, wrong marker, wrong terminator, oversize, trailing data, stale/pre-enter-world state and a terminal session.

## Bounded map-description findings

The pinned producer establishes the complete outer traversal structure:

```yaml
sendMapDescription:
  opcode: 0x64
  prefix: player_position_x_u16le_y_u16le_z_u8
  viewport_width: 18
  viewport_height: 14
GetMapDescription:
  surface_floor_order: [7, 6, 5, 4, 3, 2, 1, 0]
  underground_floor_window: z_minus_2_through_z_plus_2_clamped
  floor_offsets: z_minus_serialized_floor
GetFloorDescription:
  traversal: x_major_then_y_minor
  missing_tile_run_encoding: [skip_u8, 0xFF]
  max_run_chunk: 256_tiles_encoded_as_FF_FF
```

A fully empty initial viewport is not source-reachable. The local player has already been placed before `sendMapDescription`, and `GetTileDescription` serializes creatures from that tile. Therefore a synthetic all-empty bootstrap decoder would accept a state the pinned producer cannot emit and is not implemented.

The smallest reachable bootstrap map still requires the complete nested writer family:

```yaml
GetTileDescription:
  dependencies: [ground_item, top_items, creatures, down_items]
  client_stack_limit: 10
AddItem:
  dependencies: [item_type, subtype, tier, animation, attributes, profile_features]
AddCreature:
  dependencies: [known_creature_cache, removed_known_id, outfit, light, speed, skull, shield, type, feature_fields]
knownCreatureSet:
  semantic_effect: controls_known_vs_unknown_wire_branch
  ownership_requirement: session_scoped_protocol_identity_registry
```

Local-player movement cannot be isolated from this family because ordinary steps append directional map strips through `GetMapDescription`; teleport and floor transitions also request complete map bodies. Remote movement/removal packets expose position and stack index but do not independently prove protocol-neutral item/entity handles.


## Active item-free local-player map validation

The pinned source permits an existing tile to contain a creature list without
ground or items. `GetTileDescription` then emits the ordinary unknown-player
branch. For an initial surface map at synthetic position `(0x1234, 0x5678, 7)`,
the local tile is ordinal 118 in the first `18 x 14` floor and the complete
message has deterministic leading and trailing skip runs.

```yaml
opcode: 0x64
viewport: 18_by_14
surface_floors: 7_down_to_0
leading_missing_tiles: 118
leading_marker: [0x75, 0xFF]
tile_contents:
  ground: none
  items: none
  creatures: [ordinary_unknown_local_player]
unknown_player:
  marker_u16_le: 0x61
  removed_known_u32_le: 0
  id: must_match_0x17_local_identity
  bounded_name: consumed_not_exposed
  outfit_branch: non_zero_looktype
  icon_count_max: 3
  final_fixed_fields: [mark_0xFF, inspection_0x00]
trailing_missing_tiles: 1897
trailing_markers: [seven_FF_FF_pairs, 0x69_0xFF]
output: GameEvent::BootstrapCompleted
general_map_or_item_support: false
```

The decoder rejects every item, extra tile/creature, known-creature marker,
non-local identity, unsupported player branch, malformed RLE marker, impossible
order, truncation, oversize and trailing data.

## Fixture provenance

All hexadecimal fixtures under `oteryn-client/tests/integration/canary-world-protocol/fixtures/` are original synthetic already-decrypted logical messages. Coordinates, identity values, clock bytes and `synthetic://store` are invented test values. Fixtures contain no credential, session key, private capture, deployed configuration, producer body or proprietary asset.

New side-preamble fixtures:

```yaml
allow-bug-report.hex: "1A 00"
tibia-time.hex: "EF 0C 22"
```

The clock bytes are synthetic and are not retained by the decoder.

## Login side-preamble terminal validation

```yaml
focused_product_head: 292755649226bd36422bf941afba5281a6713af7
focused_run: 30837572720
focused_job: 91766409598
focused_result: PASS
protocol_canary_tests: 48_PASS
strict_package_clippy: PASS
locked_metadata: PASS
formatting: PASS
architecture: PASS
historical_product_pr: 234
runner_registration_pr: 233
runner_registration_merge: 4fefec3ab3a1b6401cd3b89b6e0bb1dbcb2ce2a7
runner_repair_pr: 235
runner_repair_merge: 29bc427a6f5c43218c8e2b1d6542cebb8499e5ad
restacked_head: 524c99598e49120fab7c6eff3fb00634e0a5d8b8
implementation_pr: 236
implementation_merge: 03cf57fca8f251e4b47fc1aefd56c67b6a788110
rust_client_run: 30837930784
windows_job: 91767570065
supply_chain_job: 91767570180
repository_ready_ci_run: 30838016884
repository_required_job: 91768642943
restacked_validation: PASS
fresh_audit_review: 4847048515
open_critical_high_material_medium: 0
cleanup_pr: 237
cleanup_merge: 2f9ddc7fe9747740a42eebfaac677a1a49599f3c
cleanup_repository_ci_run: 30838418308
cleanup_required_job: 91769507878
cleanup_validation: PASS
temporary_workflows_remaining: 0
temporary_scripts_remaining: 0
shared_path_lease: []
e2e:
  result: NOT_APPLICABLE
  reason: Isolated logical-message decoding has no reachable real transport, simulation composition or user journey.
```

## Inbound readiness matrix

| Required family | Classification | Exact current evidence and missing contract |
|---|---|---|
| session bootstrap | `PARTIAL` | Local identity `0x17`, bug-report permission `0x1A`, Tibia time `0xEF`, pending-state `0x0A` and enter-world `0x0F` are implemented in exact producer order. A complete reachable map body remains required before `BootstrapCompleted`. |
| map description | `UNKNOWN` | Outer opcode, position, viewport, floor traversal and skip encoding are proven. Reachable bootstrap still depends on complete nested item/creature writers and known-creature state. |
| tile and stack updates | `PARTIAL` | The complete absent-tile `0x69 + position + 0x01 + 0xFF` branch is implemented as `TileCleared`. Non-empty tile descriptions and stack identity remain incomplete. |
| creature/entity appearance | `UNKNOWN` | Known/unknown cache branches, eviction, outfit/light/skull/type fields, feature gates and collection bounds remain incomplete as one accepted family. |
| movement and reconciliation | `PARTIAL` | Local steps append map strips; teleport/floor transitions require map bodies; remote movement still lacks an accepted general identity-resolution owner. |
| removal | `PARTIAL` | Position plus stack index cannot be converted to a protocol-neutral handle without authoritative caller-owned world state. |
| session end/logout | `PARTIAL` | Exact `0x18` layout and known values `0x00`/`0x02` are implemented; `0x01`/`0x03` remain rejected. |

No partial non-empty map, item, creature, movement or removal decoder is admitted. No parser mutates simulation state.

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

## Remaining blocker

Complete provenance-safe Current non-empty map/tile/item/creature layouts, remaining movement/removal branches and an accepted general position/stack-to-domain-handle identity-resolution ownership contract remain unavailable after bounded normalization of the pinned revision.

The next safe phase is the complete `GetMapDescription -> GetFloorDescription -> GetTileDescription -> AddItem/AddCreature` family, including every Current feature gate, collection bound, skip terminator, known-creature cache transition and authoritative identity owner. Missing fields or ownership must not be inferred.


## Unknown ordinary remote-player appearance

Source classification: `PROVEN` for one narrow Current/non-legacy branch at
`blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3`.

The producer emits `0x6A + Position + stack_u8` for a non-local creature below
stack index ten. `AddCreature` then emits unknown marker `0x61`, an optional
known-cache eviction id, entity id, type/name and the complete appearance/status
tail. The implemented branch requires eviction id zero and ordinary player type,
consumes the full payload and emits only `GameEvent::EntityAppeared` with a
session-fenced handle, bounded name, position and stack.

Known marker `0x62`, nonzero eviction, hidden health, summon, monster, NPC,
invisible/zero-looktype and OTCR branches remain `UNKNOWN` and fail closed. The
fixture is original synthetic data without credentials, captures or assets.
