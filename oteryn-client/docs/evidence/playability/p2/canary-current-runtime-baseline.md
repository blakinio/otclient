# Canary Current P2 Development Runtime Baseline

Status: local-player identity and enter-world bootstrap normalization are under exact-head validation; pending-state and known session-end families remain merged.  
Evidence cut: generated P1 artifact and exact source from `blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3`.  
Consumer boundary: `oteryn-client/crates/protocol-canary`.

## Claim boundary

This document aligns a **development source baseline** only. It does not prove that any deployed Identity, Gateway or Canary instance runs this revision, configuration, build, feature set, framing/security mode or gameplay ordering.

Real Canary admission remains fail-closed in the Rust client. No credential, session key, private packet capture, proprietary asset byte or producer implementation body is stored here.

An opcode, dispatch phase, method name and source anchor prove only source-level dispatch shape unless the exact producer body, nested writers, gates and relevant call sites are also inspected. Unsupported layouts remain explicit `UNKNOWN` and are never inferred from adjacent handlers.

## Normalized generated-index evidence

```yaml
schema: oteryn-canary-source-index-v1
repository: blakinio/canary
revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
server_release: 3.6.1
client_version: 1525
producer_profile: ProtocolProfileId::Current
runtime_profile_identifier: current
entries:
  total: 347
  client_to_server: 159
  server_to_client: 188
unresolved_declarations: 0
```

Enabled feature declarations:

```text
CurrentPayload
CustomMonkPackets
GameEventPayload
GraphicalEffectSourceByte
ImbuementWindow
LoginSpeedFormula
MarketPackets
MemorialPackets
ModernLoginSideSystems
OfficialSkillWheelPayload
OfficialSoulSealsPackets
OfficialTaskboardPackets
OfficialVocationSpecificPlayerData
OfficialWeaponProficiencyPayload
PlayerDataLevelPercentU16
ResourceBalancePackets
```

Exact indexed source hashes:

```yaml
src/core.hpp: 6e665eb99b62049c78b84d142eea070913b74699c2c40448d1473e3bcd211ce6
src/server/network/protocol/protocol_port_utils.hpp: 3a39e0693cdea574f6decc5a061c715b3b1573e82791696cd681b46243e70505
src/server/network/protocol/protocol_profile.cpp: 69d2d4193e721b83805031108825a5f3bf30ae4e5e46c27729ea5493ea6d33df
src/server/network/protocol/protocol_profile.hpp: 7cbb7ac6d16b6f7eb74201d00fc60ccd6d098e862814164efa45596392ff4a58
src/server/network/protocol/protocol_session_hint.hpp: 3b84362af14d7909b37c6b8adf61d941987cb59729090c295841866488a2d2db
src/server/network/protocol/protocolgame.cpp: af7484cd0c4e1e4e5812ea3b6f1813031687331696001fb74de0be9bd21d5efc
src/server/network/protocol/protocolgame.hpp: 33a97f6c54baa6138555164995c0125141407bd7d7a4e71dd7c0561c0f246beb
```

The pre-P2 runtime descriptor named revision `95b276db311cf6e9acd58b847f1fb0ca6697b137` and historical accepted source cut `4b2d6f432d92628c42bde1d95daed6ae0d0eb88f`. They remain historical evidence only. PR #190 enforces LF checkout for generated JSON so drift evidence is byte-stable on Windows and Linux.

## Supported outbound M2 command subset

Exact producer dispatch establishes ten client-to-server gameplay-session commands with no payload:

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

`encode_current_development_command` consumes only a Current session-fenced merged `GameCommandEnvelope`. It emits one byte for the supported subset, rejects unsupported semantic commands explicitly and performs no network I/O.

## Proven local-player identity and enter-world boundaries

The exact Current/non-legacy local-player branch of `sendAddCreature` precedes
`sendPendingStateEntered`, `sendEnterWorld` and `sendMapDescription`. At client
version 1525 with `LoginSpeedFormula` enabled, its first logical message has the
complete structural layout:

```yaml
local_player_initialization:
  opcode_u8: 0x17
  player_id_u32_le: non_zero
  server_beat_u16_le: opaque_timing_value
  speed_formula_components: 3
  each_speed_component:
    precision_u8: 3
    scaled_value_u32_le: opaque_tuning_value
  pvp_framing_change_u8: 0
  expert_mode_u8: 0
  store_url: u16_length_plus_opaque_bytes
  store_coin_packet_u16_le: opaque_configuration_value
  exiva_enabled_u8: boolean
semantic_normalization:
  retained: session_fenced_EntityHandle
  discarded: timing_speed_store_and_capability_values
  emitted_event: none
```

`sendEnterWorld` is exactly one byte `0x0F`. The caller-owned bootstrap state
accepts it only after local-player identity and pending-state entry. It records
order but emits no `BootstrapCompleted`, because position remains absent until a
complete map-description family is validated. This closes local identity
ownership without partially mutating simulation or exposing Canary-specific
configuration fields.

Original synthetic fixtures use invented field values and a synthetic store URL;
no producer body, private capture, credential or deployed configuration is copied.

## Proven inbound pending-state boundary

The generated index and exact producer body establish:

```yaml
method: sendPendingStateEntered
source: src/server/network/protocol/protocolgame.cpp:8502
opcode: 0x0A
logical_message_bytes: [0x0A]
payload_bytes: 0
producer_method_gates:
  - player exists
  - oldProtocol is false
```

The exact login call site orders it after `sendTibiaTime` and before `sendEnterWorld` and `sendMapDescription` for `version >= 980`. The Current development profile is client version `1525` and non-legacy.

`decode_current_pending_state_entered` consumes one already decrypted and deframed logical message through a caller-owned state fenced to one `SessionToken`. It rejects empty, wrong-opcode, trailing, oversized, duplicate/out-of-order and stale-session input. On success it advances only that session-owned state and emits `GameEventEnvelope::v1(GameEvent::BootstrapStarted)`.

## Proven inbound session-end boundary

The generated index records `sendSessionEndInformation` as a server-to-client bootstrap-family send at `src/server/network/protocol/protocolgame.cpp:2932`, opcode `0x18`, with no profile or build gate. The exact producer body establishes the complete layout and terminal effect:

```yaml
logical_message:
  opcode_u8: 0x18
  information_u8: SessionEndInformations
post_send_effect: disconnect
legacy_gate: oldProtocol must be false
```

The pinned `SessionEndInformations : uint8_t` definition proves numeric values `0x00`, `0x01`, `0x02`, `0x03`. Exact call sites prove only these named values are emitted by the inspected producer path:

```yaml
0x00:
  source_name: SESSION_END_LOGOUT
  proven_callers:
    - client gameplay opcode 0x14 -> logout(display_effect=true, forced=false)
    - livestream-viewer logout path
0x02:
  source_name: SESSION_END_FORCECLOSE
  proven_caller:
    - logout(..., forced=true)
0x01: UNKNOWN
0x03: UNKNOWN
```

The adapter accepts only `0x00` and `0x02`; unknown values fail closed. Both accepted codes normalize conservatively to `GameEvent::SessionEnded { reason: ServerClosed }`, because this isolated producer has no caller-owned outbound-command history sufficient to prove `Requested` at decode time. No raw Canary reason byte escapes the adapter boundary.

The terminal message may be accepted before or after pending-state entry, but only once for the current session. Success prevents later bootstrap advancement. Truncation, wrong opcode, trailing data, oversize, unknown reason, duplicate end and stale session all fail without changing state.

Original synthetic hexadecimal fixtures live under `oteryn-client/tests/integration/canary-world-protocol/fixtures/`. They are already-decrypted logical messages, carry exact source provenance and contain no credential, session key, private capture, proprietary asset byte or copied producer body.

## Inbound M2 readiness matrix

| Required family | Classification | Exact current evidence and missing contract |
|---|---|---|
| session bootstrap | `PARTIAL` | Current local-player `0x17` identity, pending-state `0x0A` and enter-world `0x0F` are `PROVEN` and normalized in exact source order. The map-description position and complete nested map body remain required before `GameEvent::BootstrapCompleted`; semantic completion is `BLOCKED`. |
| map description | `UNKNOWN` | `sendMapDescription` delegates to `GetMapDescription`, floor/tile iteration, skip markers and nested item/creature writers. Complete Current branches, terminators, collection bounds and appearance dependencies have not been normalized into one accepted layout. |
| tile and stack updates | `PARTIAL` | Outer opcodes/positions for update/add/remove paths are visible, but tile descriptions contain nested variable writers and stack-only operations do not prove a domain item/entity handle without authoritative state. |
| creature/entity appearance | `UNKNOWN` | `sendAddCreature`, `sendUpdateTileCreature` and `AddCreature` depend on known-creature cache branches, removals, outfit/light/skull/type/feature fields and nested bounds not yet proven as one complete Current layout. |
| movement and reconciliation | `PARTIAL` | `sendMoveCreature` has local-player, teleport, floor-transition, map-strip, remote-visible and remove/add branches. Direct `0x6D` movement identifies the source by position/stack rather than a domain handle, so complete deterministic normalization requires an accepted identity-resolution contract and every branch layout. |
| removal | `PARTIAL` | Remove-tile messages expose position and stack index, not a protocol-neutral item/entity handle. Mapping without authoritative state would guess identity and is forbidden. |
| session end/logout | `PARTIAL` | Exact `0x18` layout and known values `0x00`/`0x02` are `PROVEN` and implemented; source values `0x01`/`0x03` remain explicitly `UNKNOWN` and rejected. |

No map, tile, entity, movement or removal payload is implemented from this matrix. Partial decoding cannot mutate simulation state.

## Active bootstrap identity validation phase

```yaml
phase: bootstrap-identity-and-enter-world-normalization
branch: feat/OTC2-20260803-canary-bootstrap-identity
base: c91a5872a66cd9a31add2f3f1efc79ceefe7d150
new_layouts:
  - current_local_player_initialization_0x17
  - enter_world_0x0F_order_boundary
identity_contract:
  owner: caller_owned_CanaryInboundBootstrapState
  mapping: nonzero_Canary_creature_id_to_session_fenced_EntityHandle
  raw_id_escape: false
  map_stack_identity: unresolved
simulation_mutation: false
real_admission_changed: false
validation: running
```

## Terminal validation checkpoint

```yaml
status: bounded_family_merged_parent_blocked
implementation_pr: 196
implementation_head: a2ea69ea3801df0bbba20caaf6ab7d8677b52bb7
merge_commit: ceb24e22fc19305cb10c7ea29f7f16928def2a04
product_code_scope:
  - bounded session-fenced logical-message parsing
  - original sanitized positive and negative fixtures
admission_lifecycle_changed: false
real_admission_state: fail_closed
credentials_or_private_payloads_added: false
gameplay_layouts_implemented:
  outbound: [step_8_directions, stop_movement, logout]
  inbound: [pending_state_entered, session_end_known_codes]
session_end_negative_matrix:
  truncated: PASS
  unknown_opcode: PASS
  trailing_data: PASS
  oversized: PASS
  unknown_reason: PASS
  invalid_order_or_duplicate: PASS
  stale_session: PASS
validation:
  repaired_format_generation:
    rust_client_run: 30798587290
    windows_job: 91637729025
    result: REPAIRED
  exact_head_rust_client_run: 30798845230
  exact_head_windows_job: 91638521494
  exact_head_supply_chain_job: 91638521428
  locked_metadata: PASS
  formatting: PASS
  clippy: PASS
  workspace_tests: PASS
  architecture: PASS
  supply_chain: PASS
  repository_ci_run: 30798845350
  repository_required_job: 91638983873
  repository_ci: PASS
  ready_state_ci_run: 30799161107
  ready_state_required_job: 91639989636
  ready_state_ci: PASS
audit:
  result: PASS
  validator: fresh_connector_audit_role
  review_id: 4842339967
  open_critical_high_material_medium: 0
e2e:
  result: NOT_APPLICABLE
  reason: The isolated producer consumes already decrypted and deframed logical messages and has no reachable application or real transport composition.
shared_path_lease: []
blocker: Complete provenance-safe Current map/entity/movement/removal layouts and an accepted position/stack-to-domain-handle identity-resolution ownership contract are unavailable at the pinned revision after bounded evidence normalization.
next_action: Obtain and accept one complete pinned remaining-family layout plus its identity-resolution contract, then resume the same parent task without inferring missing fields or ownership.
```
