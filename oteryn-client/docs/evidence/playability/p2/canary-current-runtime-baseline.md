# Canary Current P2 Development Runtime Baseline

Status: bounded pending-state inbound implementation in progress on task `OTC2-20260803-playability-p2-canary-world-protocol`.  
Evidence cut: generated P1 artifact and exact source from `blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3`.  
Consumer boundary: `oteryn-client/crates/protocol-canary`.

## Claim boundary

This document aligns a **development source baseline** only. It does not prove that any deployed Identity, Gateway or Canary instance runs this revision, configuration, build, feature set, framing/security mode or gameplay ordering.

Real Canary admission remains fail-closed in the Rust client. No credential, session key, private packet capture, proprietary asset byte or producer implementation body is stored here.

An opcode, dispatch phase, method name and source anchor prove only source-level dispatch shape unless an exact producer body and call site are also inspected. Unsupported layouts remain explicit `UNKNOWN` and are never inferred from adjacent handlers.

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

## Revision and checkout contracts

The pre-P2 runtime descriptor named:

```yaml
previous_runtime_revision: 95b276db311cf6e9acd58b847f1fb0ca6697b137
historical_accepted_source_cut: 4b2d6f432d92628c42bde1d95daed6ae0d0eb88f
```

P2 changes the development descriptor revision to the generated P1 index revision and preserves both older values only as historical evidence. PR #190 enforces LF checkout for the generated JSON so compile-time drift evidence is byte-stable on Windows and Linux.

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

`encode_current_development_command` consumes only a current session-fenced merged `GameCommandEnvelope`. It emits one byte for the supported subset, rejects unsupported semantic commands explicitly, and performs no network I/O.

## Supported inbound pending-state boundary

The generated index records this exact producer entry:

```yaml
direction: server-to-client
dispatch_phase: server-send
family: bootstrap
method: sendPendingStateEntered
opcode: 0x0A
source:
  path: src/server/network/protocol/protocolgame.cpp
  line: 8502
```

The exact producer method establishes the complete logical-message layout:

```yaml
bytes: [0x0A]
payload_bytes: 0
producer_method_gates:
  - player exists
  - oldProtocol is false
```

The exact login call site establishes the bounded ordering and version gate:

```yaml
version_gate: version >= 980
order:
  after: sendTibiaTime
  before:
    - sendEnterWorld
    - sendMapDescription
```

The Current development profile is client version `1525` and non-legacy. `decode_current_pending_state_entered` therefore consumes one already decrypted and deframed logical message only when the caller explicitly owns `AwaitingPendingStateEntered`. It rejects empty, wrong-opcode, trailing, oversized, duplicate/out-of-order and stale-session input. On success it advances the caller-owned order state and emits a current-session `GameEventEnvelope::v1(GameEvent::BootstrapStarted)`.

The semantic event is a domain interpretation of the exact producer pending-state boundary. It does not claim that a deployed runtime matches this source or that the adjacent enter-world/map layouts are known.

## Remaining inbound readiness

`sendEnterWorld`, map description, entity appearance, movement reconciliation and every other inbound family remain `UNKNOWN`. They require their own complete source layouts, feature/build gates, ordering evidence and original sanitized positive/negative fixtures before implementation.

## Validation checkpoint

```yaml
status: implementation_pending_validation
product_code_scope:
  - non-secret development descriptor metadata
  - generated-index drift tests
  - bounded movement, stop and logout command encoder
  - bounded pending-state-entered decoder
admission_lifecycle_changed: false
real_admission_state: fail_closed
credentials_or_private_payloads_added: false
gameplay_layouts_implemented:
  outbound: [step_8_directions, stop_movement, logout]
  inbound: [pending_state_entered]
pending_state_negative_matrix:
  - truncated
  - unknown_opcode
  - trailing_data
  - oversized
  - invalid_order_or_duplicate
  - stale_session
blockers:
  - complete provenance-safe layouts and fixtures for all remaining inbound families
next_action: Run pinned format, strict package Clippy, package tests and architecture validation, then perform a fresh exact-diff audit and exact-head Windows CI before merge.
```
