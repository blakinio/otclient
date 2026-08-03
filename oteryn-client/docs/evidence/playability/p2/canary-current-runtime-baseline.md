# Canary Current P2 Development Runtime Baseline

Status: alignment in progress on task `OTC2-20260803-playability-p2-canary-world-protocol`.  
Evidence cut: generated P1 artifact from `blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3`.  
Consumer boundary: `oteryn-client/crates/protocol-canary`.

## Claim boundary

This document aligns a **development source baseline** only. It does not prove that any deployed Identity, Gateway or Canary instance runs this revision, configuration, build, feature set, framing/security mode or gameplay ordering.

Real Canary admission remains fail-closed in the Rust client. No credential, session key, private packet capture, proprietary asset byte or producer implementation body is stored here.

An opcode, dispatch phase, method name and source anchor prove only source-level dispatch shape. They do not establish field layout. Unsupported layouts remain explicit `UNKNOWN` and must not be inferred from adjacent handlers.

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

## Revision reconciliation

The pre-P2 runtime descriptor named:

```yaml
previous_runtime_revision: 95b276db311cf6e9acd58b847f1fb0ca6697b137
historical_accepted_source_cut: 4b2d6f432d92628c42bde1d95daed6ae0d0eb88f
```

P2 changes the development descriptor revision to the generated P1 index revision and preserves both older values only as explicit historical evidence. No deployed-equality claim is created.

## Mechanical drift contract

The `protocol-canary` package tests include the versioned generated JSON as read-only compile-time test evidence and verify:

- schema, repository, revision, release, producer profile and client version;
- total and direction counts;
- the exact 16 enabled feature declarations;
- all seven exact source path/SHA-256 pairs;
- empty unresolved declarations;
- consistency between the JSON and the public non-secret `CURRENT_PROFILE` descriptor;
- continued fail-closed real admission.

A generator/artifact change must therefore update the descriptor, this evidence record and tests together in an explicitly reviewed task.

## Supported outbound M2 command subset

Exact producer dispatch at revision `bc0068ab…` establishes ten client-to-server gameplay-session commands with no payload:

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

`encode_current_development_command` consumes only a current session-fenced merged `GameCommandEnvelope`. It emits one byte for `Step`, `StopMovement` and `Logout`, rejects every unsupported semantic command explicitly, and performs no network I/O. Real transmission remains unauthorized while admission is fail-closed.

## Inbound gameplay layout readiness

Current P1 fixture classification provides no reusable provenance-safe complete post-admission transcript. Map, entity and bootstrap paths depend on nested tile, thing, appearance and profile logic that dispatch entries alone do not define.

Inbound bootstrap, map, entity and reconciliation layouts therefore remain `UNKNOWN` and unimplemented until complete bounded source contracts and original sanitized positive and negative fixtures prove ordering, gates and truncation behavior.

## Validation checkpoint

```yaml
status: focused_validation_passed
product_code_scope:
  - non-secret development descriptor metadata
  - generated-index drift tests
  - bounded source-evidenced movement, stop and logout command encoder
admission_lifecycle_changed: false
real_admission_state: fail_closed
credentials_or_private_payloads_added: false
gameplay_layouts_implemented:
  outbound: [step_8_directions, stop_movement, logout]
  inbound: []
focused_validation:
  cargo_fmt: PASS
  strict_clippy: PASS
  package_tests: PASS
  architecture: PASS
blockers:
  - complete provenance-safe inbound bootstrap, map, entity and reconciliation layouts
  - original sanitized positive and negative fixtures for each inbound family
next_action: Run retained exact-head repository CI, then protected-merge this bounded phase and release the lockfile lease before continuing inbound evidence normalization.
```
