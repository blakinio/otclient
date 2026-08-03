# Canary Current P2 Development Runtime Baseline

Status: local-player identity, pending-state, enter-world order and known session-end slices are merged; the parent producer remains blocked on complete map/world layouts and general identity resolution.  
Evidence cut: generated P1 artifact and exact source from `blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3`.  
Consumer boundary: `oteryn-client/crates/protocol-canary`.

## Claim boundary

This document aligns a **development source baseline** only. It does not prove that any deployed Identity, Gateway or Canary instance runs this revision, configuration, build, feature set, framing/security mode or gameplay ordering.

Real Canary admission remains fail-closed. No credential, session key, private packet capture, proprietary asset byte or copied producer implementation body is stored here. The parser consumes already decrypted and deframed logical messages only and does not own simulation, rendering, transport or application composition.

## Normalized source profile

```yaml
schema: oteryn-canary-source-index-v1
repository: blakinio/canary
revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
server_release: 3.6.1
client_version: 1525
profile: ProtocolProfileId::Current
enabled_feature_required_here: LoginSpeedFormula
network_message_max_bytes: 65500
```

Exact indexed source hashes remain recorded by the generated descriptor in `oteryn-protocol-canary`. Historical runtime revisions remain historical evidence only.

## Supported outbound development subset

Exact dispatch establishes ten no-payload client-to-server commands:

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

`encode_current_development_command` accepts only a Current session-fenced merged `GameCommandEnvelope`, emits exactly one byte for this subset and performs no network I/O.

## Proven local-player initialization

The exact Current/non-legacy local branch of `ProtocolGame::sendAddCreature` precedes pending-state, enter-world and map description. At client version 1525 with `LoginSpeedFormula` enabled, the logical message is:

```yaml
opcode_u8: 0x17
player_id_u32_le: non_zero
server_beat_u16_le: opaque
speed_formula_components: 3
each_speed_component:
  precision_u8: 3
  scaled_value_u32_le: opaque
pvp_framing_change_u8: 0
expert_mode_u8: 0
store_url: u16_length_plus_opaque_bytes
store_coin_packet_u16_le: opaque
exiva_enabled_u8: boolean
```

The decoder validates the complete structure but retains only:

```yaml
output: EntityHandle
session_fenced: true
raw_creature_id_escape: false
timing_or_speed_configuration_retained: false
store_configuration_retained: false
emitted_game_event: none
simulation_mutation: false
```

A zero player ID, stale session, duplicate/out-of-order message, wrong opcode, bad precision, non-zero fixed capability byte, invalid boolean, truncation, oversize and trailing data fail without changing state.

## Proven pending-state and enter-world order

```yaml
pending_state:
  producer: sendPendingStateEntered
  opcode: 0x0A
  payload_bytes: 0
  prerequisite: local_player_identity
  output: GameEventEnvelope::v1(GameEvent::BootstrapStarted)
enter_world:
  producer: sendEnterWorld
  opcode: 0x0F
  payload_bytes: 0
  prerequisites: [local_player_identity, pending_state]
  output: caller_owned_order_state_only
bootstrap_completed:
  emitted: false
  missing_required_value: validated_map_position
```

Every boundary is session-fenced, bounded, trailing-data rejecting and state-atomic. Enter-world cannot fabricate the `EntityHandle + Position` pair required by `GameEvent::BootstrapCompleted`.

## Proven session-end boundary

The exact producer emits opcode `0x18`, one `SessionEndInformations` byte and then disconnects. The inspected call sites prove:

```yaml
0x00: SESSION_END_LOGOUT
0x02: SESSION_END_FORCECLOSE
0x01: UNKNOWN
0x03: UNKNOWN
```

Only `0x00` and `0x02` are accepted. Both normalize conservatively to `GameEvent::SessionEnded { reason: ServerClosed }`; unknown values fail closed. The isolated decoder lacks caller-owned command history sufficient to prove `Requested`.

## Fixture provenance

Original synthetic hexadecimal fixtures under `oteryn-client/tests/integration/canary-world-protocol/fixtures/` represent already decrypted logical messages. The local-player values and `synthetic://store` string are invented test values. Fixtures contain no credential, session key, private capture, deployed store configuration, proprietary asset byte or producer body.

Positive/negative coverage includes:

```yaml
local_player_initialization: PASS
bad_login_precision: PASS
zero_identity: PASS
trailing_identity_data: PASS
enter_world: PASS
pending_without_identity: PASS_REJECTED
wrong_opcode: PASS_REJECTED
truncation: PASS_REJECTED
oversize: PASS_REJECTED
stale_session: PASS_REJECTED
duplicate_or_impossible_order: PASS_REJECTED
known_session_end: PASS
unknown_session_end: PASS_REJECTED
```

## Inbound readiness matrix

| Required family | Classification | Exact current evidence and missing contract |
|---|---|---|
| session bootstrap | `PARTIAL` | Local identity `0x17`, pending-state `0x0A` and enter-world `0x0F` are proven and implemented in exact order. Complete map-description position/body remains required before `BootstrapCompleted`. |
| map description | `UNKNOWN` | `GetMapDescription` delegates to floor/tile iteration, skip markers and nested item/creature writers. Complete Current branches, terminators, bounds and appearance dependencies are not normalized as one accepted layout. |
| tile and stack updates | `PARTIAL` | Outer opcodes/positions are visible, but nested tile descriptions and stack-only identity ownership remain incomplete. |
| creature/entity appearance | `UNKNOWN` | Known-creature cache branches, removals, outfit/light/skull/type/feature fields and nested bounds remain incomplete. |
| movement and reconciliation | `PARTIAL` | Local-player, teleport, floor-transition, map-strip, remote-visible and remove/add branches are incomplete. Position plus stack does not prove a domain handle. |
| removal | `PARTIAL` | Remove-tile messages expose position and stack index, not a protocol-neutral item/entity handle. Mapping without authoritative state would guess identity. |
| session end/logout | `PARTIAL` | Exact `0x18` layout and known values `0x00`/`0x02` are implemented; `0x01`/`0x03` remain explicitly unknown and rejected. |

No partial map, tile, entity, movement or removal decoder is implemented. No parser mutates simulation state.

## Terminal bootstrap identity validation

```yaml
focused_product_head: ec34134aee42fd687f4f195025362189e49c9dbc
focused_run: 30820529534
focused_job: 91709031623
focused_result: PASS
protocol_canary_tests: 39_PASS
restacked_head: 0690084045c5dc70b6632a424c9c6ede2cc20b62
implementation_pr: 220
implementation_merge: 1c820ff6b87f8459bc300e5baeed0e395b6147c8
restacked_rust_client_run: 30821884378
restacked_windows_job: 91713561582
restacked_supply_chain_job: 91713561705
restacked_repository_ci_run: 30821887730
restacked_repository_required_job: 91713897019
restacked_validation: PASS
fresh_product_audit_review: 4844933812
fresh_restack_audit_review: 4845040720
open_critical_high_material_medium: 0
temporary_runner_cleanup_pr: 221
temporary_runner_cleanup_merge: d6ac5c89a378d58ef4bdbd7ba0e5a61f686e4e0a
cleanup_repository_ci_run: 30822271162
cleanup_required_job: 91715246698
cleanup_validation: PASS
temporary_workflows_remaining: 0
shared_path_lease: []
e2e:
  result: NOT_APPLICABLE
  reason: Isolated logical-message decoding has no reachable real transport, simulation composition or user journey.
```

## Remaining blocker

Complete provenance-safe Current map/tile/item/creature layouts, remaining movement/removal branches and an accepted general position/stack-to-domain-handle identity-resolution ownership contract are unavailable after bounded normalization of the pinned revision.

The next safe phase is one complete pinned map-description layout including nested writer gates, bounds and authoritative identity ownership. Missing fields or ownership must not be inferred.
