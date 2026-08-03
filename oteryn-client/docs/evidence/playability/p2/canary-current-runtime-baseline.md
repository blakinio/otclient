# Canary Current P2 Development Runtime Baseline

Status: bounded session-end inbound implementation is validating on task `OTC2-20260803-playability-p2-canary-world-protocol`.  
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
| session bootstrap | `PARTIAL` | `sendPendingStateEntered` is `PROVEN` and implemented. `sendEnterWorld` is a proven one-byte `0x0F` layout at line 8512, but it carries neither local-player identity nor position required by `GameEvent::BootstrapCompleted`; semantic completion remains `BLOCKED` rather than guessed. |
| map description | `UNKNOWN` | `sendMapDescription` delegates to `GetMapDescription`, floor/tile iteration, skip markers and nested item/creature writers. Complete Current branches, terminators, collection bounds and appearance dependencies have not been normalized into one accepted layout. |
| tile and stack updates | `PARTIAL` | Outer opcodes/positions for update/add/remove paths are visible, but tile descriptions contain nested variable writers and stack-only operations do not prove a domain item/entity handle without authoritative state. |
| creature/entity appearance | `UNKNOWN` | `sendAddCreature`, `sendUpdateTileCreature` and `AddCreature` depend on known-creature cache branches, removals, outfit/light/skull/type/feature fields and nested bounds not yet proven as one complete Current layout. |
| movement and reconciliation | `PARTIAL` | `sendMoveCreature` has local-player, teleport, floor-transition, map-strip, remote-visible and remove/add branches. Direct `0x6D` movement identifies the source by position/stack rather than a domain handle, so complete deterministic normalization requires an accepted identity-resolution contract and every branch layout. |
| removal | `PARTIAL` | remove-tile messages expose position and stack index, not a protocol-neutral item/entity handle. Mapping without authoritative state would guess identity and is forbidden. |
| session end/logout | `PARTIAL` | Exact `0x18` layout and known values `0x00`/`0x02` are `PROVEN` and implemented; source values `0x01`/`0x03` remain explicitly `UNKNOWN` and rejected. |

No map, tile, entity, movement or removal payload is implemented from this matrix. Partial decoding cannot mutate simulation state.

## Validation checkpoint

```yaml
status: exact_head_validation_pending
branch: feat/OTC2-20260803-canary-session-end-inbound
pr: 196
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
  truncated: pending
  unknown_opcode: pending
  trailing_data: pending
  oversized: pending
  unknown_reason: pending
  invalid_order_or_duplicate: pending
  stale_session: pending
audit:
  result: pending_exact_final_diff
blockers:
  - complete provenance-safe map/entity/movement/removal layouts and identity-resolution contracts
next_action: Complete focused and exact-head validation and fresh audit for PR 196, then merge the bounded family and persist the remaining provenance blocker.
```
