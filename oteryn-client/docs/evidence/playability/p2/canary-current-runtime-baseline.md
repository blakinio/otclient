# Canary Current P2 Development Runtime Baseline

Status: local-player identity, known session-end and absent-tile slices are merged; exact login side-preamble order is under validation while the parent remains blocked on non-empty map/world layouts and general identity resolution.

Evidence cut: generated P1 artifact and exact source from `blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3`.

Consumer boundary: `oteryn-client/crates/protocol-canary`.

## Claim boundary

This document aligns a development source baseline only. It does not prove that a deployed Identity, Gateway or Canary instance runs this revision, configuration, build, feature set, framing/security mode or gameplay order.

Real Canary admission remains fail-closed. No credential, session key, private packet capture, proprietary asset byte or copied producer implementation body is stored here. The parser consumes already decrypted and deframed logical messages and does not own simulation, rendering, transport or application composition.

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

Exact indexed source hashes remain published by the immutable Current profile descriptor in `oteryn-protocol-canary`.

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


## Proven login side-preamble order

The pinned Current local-player producer calls these complete logical messages
between local identity and pending-state:

```yaml
allow_bug_report:
  producer: sendAllowBugReport
  logical_message: [0x1A, 0x00]
  retained_output: none
tibia_time:
  producer: sendTibiaTime
  logical_message: [0xEF, hour_component_u8, minute_component_u8]
  retained_output: none
ordering:
  after: local_player_initialization_0x17
  before: pending_state_0x0A
state_mutation: caller_owned_order_only
simulation_mutation: false
```

Clock components are structurally validated and intentionally discarded because
the protocol adapter does not own world-light simulation. Wrong order, fixed
permission byte, opcode, truncation, oversize and trailing data fail atomically.

## Proven pending-state and enter-world order

The exact Current/non-legacy local branch of `ProtocolGame::sendAddCreature` provides the complete `0x17` local-player initialization layout. The decoder validates all fixed and profile-gated fields but retains only a non-zero producer creature ID normalized to a session-fenced `EntityHandle`.

```yaml
local_player_initialization:
  opcode: 0x17
  retained: session_fenced_EntityHandle
  discarded: [server_beat, speed_formula, capability_bytes, store_url, store_coin_packet, exiva_flag]
pending_state:
  opcode: 0x0A
  prerequisites: [local_player_identity, allow_bug_report, tibia_time]
  output: GameEventEnvelope::v1(GameEvent::BootstrapStarted)
enter_world:
  opcode: 0x0F
  prerequisites: [local_player_identity, pending_state]
  output: caller_owned_order_state_only
bootstrap_completed:
  emitted: false
  missing_required_value: validated_map_position
```

These boundaries are bounded, session-fenced, trailing-data rejecting and state-atomic. Invalid precision, fixed fields, boolean, zero identity, truncation, oversize, stale session, duplicates and impossible order fail closed.

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

`ProtocolGame::sendUpdateTile` writes opcode `0x69` and calls `NetworkMessage::addPosition`, whose exact layout is `x:u16le`, `y:u16le`, `z:u8`. When the tile pointer is absent, the producer writes fixed marker `0x01` followed by terminator `0xFF` and does not call any nested writer.

```yaml
logical_message:
  opcode_u8: 0x69
  x_u16_le: canonical_tile_x
  y_u16_le: canonical_tile_y
  z_u8: canonical_floor
  absent_tile_marker_u8: 0x01
  terminator_u8: 0xFF
prerequisite: current_session_after_enter_world
output: GameEventEnvelope::v1(GameEvent::TileCleared)
caller_state_mutation: false
nested_writer_dependency: none
```

`decode_current_empty_tile_update` rejects:

```yaml
- every truncated prefix
- wrong opcode
- wrong absent-tile marker
- wrong terminator
- oversized input
- trailing data
- stale session
- pre-enter-world order
- terminal session
```

The non-empty branch is not partially parsed because it invokes `GetTileDescription`, `AddItem`, `AddCreature` and feature-dependent variable writers.

## Fixture provenance

All hexadecimal fixtures under `oteryn-client/tests/integration/canary-world-protocol/fixtures/` are original synthetic already-decrypted logical messages. Coordinates, identity values and `synthetic://store` are invented test values. Fixtures contain no credential, session key, private capture, deployed configuration, producer body or proprietary asset.

## Inbound readiness matrix

| Required family | Classification | Exact current evidence and missing contract |
|---|---|---|
| session bootstrap | `PARTIAL` | Local identity `0x17`, pending-state `0x0A` and enter-world `0x0F` are implemented in exact order. A complete map-description position/body remains required before `BootstrapCompleted`. |
| map description | `UNKNOWN` | `GetMapDescription` delegates to floor/tile iteration, skip markers and nested item/creature writers. Complete Current branches, terminators, bounds and appearance dependencies are not normalized as one accepted layout. |
| tile and stack updates | `PARTIAL` | The complete absent-tile `0x69 + position + 0x01 + 0xFF` branch is implemented as `TileCleared`. Non-empty tile descriptions and stack-only identity ownership remain incomplete. |
| creature/entity appearance | `UNKNOWN` | Known-creature cache branches, removals, outfit/light/skull/type/feature fields and nested bounds remain incomplete. |
| movement and reconciliation | `PARTIAL` | Local-player, teleport, floor-transition, map-strip, remote-visible and remove/add branches are incomplete. Position plus stack does not prove a domain handle. |
| removal | `PARTIAL` | Remove-tile messages expose position and stack index, not a protocol-neutral item/entity handle. Mapping without authoritative state would guess identity. |
| session end/logout | `PARTIAL` | Exact `0x18` layout and known values `0x00`/`0x02` are implemented; `0x01`/`0x03` remain explicitly unknown and rejected. |

No partial non-empty map, entity, movement or removal decoder is implemented. The tile decoder accepts only the complete absent-tile branch. No parser mutates simulation state.

## Empty-tile terminal validation

```yaml
focused_product_head: 6bfaea45187176e7b956cb49aefbcf16523cc045
focused_run: 30831813507
focused_job: 91747353789
focused_result: PASS
focused_protocol_canary_tests: 45_PASS
superseded_product_pr: 224
restacked_head: 8c6436aa8d87eead0a0f6f6d8592cd0ba3043aaf
implementation_pr: 230
implementation_merge: fe0e74bb1df56ad10aac39eef93c9132c09e2407
rust_client_run: 30832279785
windows_job: 91748896392
supply_chain_job: 91748896261
repository_ci_run: 30832280429
repository_required_job: 91749201719
restacked_validation: PASS
fresh_audit_review: 4846369910
open_critical: 0
open_high: 0
open_material_medium: 0
unresolved_review_threads: 0
cleanup_pr: 231
cleanup_merge: f88a6ac21b078dc1d79cdcddfc1f05ffa1589235
cleanup_repository_ci_run: 30832756476
cleanup_required_job: 91750747579
cleanup_validation: PASS
temporary_workflows_remaining: 0
temporary_scripts_remaining: 0
shared_path_lease: []
e2e:
  result: NOT_APPLICABLE
  reason: Isolated logical-message decoding has no reachable real transport, simulation composition or user journey.
```

## Remaining blocker

Complete provenance-safe Current non-empty map/tile/item/creature layouts, remaining movement/removal branches and an accepted general position/stack-to-domain-handle identity-resolution ownership contract remain unavailable after bounded normalization.

The next safe phase must normalize `GetMapDescription -> GetFloorDescription -> GetTileDescription -> AddItem/AddCreature` as one complete Current family, including feature gates, collection bounds, skip terminators and authoritative identity ownership. Missing fields or ownership must not be inferred.

## Active login side-preamble validation

```yaml
branch: feat/OTC2-20260803-canary-login-preamble
base: 4fefec3ab3a1b6401cd3b89b6e0bb1dbcb2ce2a7
registration_pr: 233
source_revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
source_methods: [sendAllowBugReport, sendTibiaTime]
new_decoders: [decode_current_allow_bug_report, decode_current_tibia_time]
validation: focused_workflow_running
```
