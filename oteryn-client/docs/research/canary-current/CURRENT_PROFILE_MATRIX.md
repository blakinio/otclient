# Canary Current profile matrix

Evidence revision: `blakinio/canary@87149c6b527f43025860c20cca0a440091ee8730`.

All rows describe producer source at the cited revision. `PROVEN` does not mean an unimplemented Rust consumer is compatible.

## Profile and transport

| Property | Current evidence | Status | Exact source |
|---|---|---|---|
| client protocol | `1525`, displayed as 15.25 | `PROVEN` | `src/core.hpp`; `protocol_profile.cpp::currentClientVersionLabel` |
| profile identity | `ProtocolProfileId::Current`, name `current` | `PROVEN` | `src/server/network/protocol/protocol_profile.{hpp,cpp}` |
| support state | enabled | `PROVEN` | `protocol_profile.cpp::currentProfile` |
| wire family | `CipsoftVanilla` | `PROVEN` | `protocol_profile.cpp::currentProfile` |
| RSA family | OpenTibia | `PROVEN` | `protocol_profile.cpp::currentProfile` |
| item mapper | not required | `PROVEN` | `protocol_profile.cpp::currentProfile` |
| initial game flow | server challenge before login | `PROVEN` | `protocol_profile.cpp::currentInitialBehavior` |
| challenge layout | Current login challenge | `PROVEN` | `protocol_profile.cpp::currentInitialBehavior` |
| current game transport | modern block count; modern padding byte; sequence checksum; official compression; compression signaled by sequence high bit | `PROVEN` | `protocol_profile.cpp::currentGameSequenceTransport`; `transport_codec.cpp` |
| current account-login response transport | modern block count; modern padding; Adler-32; no compression | `PROVEN` | `protocol_profile.cpp::currentLoginTransport`; `transport_codec.cpp` |
| malformed transport behavior | zero/incorrect sequence, checksum mismatch, malformed frame and decrypt failure are distinct rejected states | `PROVEN` | `src/server/network/protocol/transport_codec.{hpp,cpp}` |

## Login layouts

| Boundary | Current layout | Status | Exact source |
|---|---|---|---|
| account-login pre-RSA prefix | skip 17 bytes; no legacy asset signatures before RSA | `PROVEN` | `protocol_profile.cpp::currentAccountLoginLayout`; `protocollogin.cpp::resolveLoginLayout` |
| account character list | world-list layout with session key | `PROVEN` | `protocol_profile.{hpp,cpp}` |
| session-key response | enabled; emitted before character/world list | `PROVEN` | `protocol_profile.cpp`; `protocollogin.cpp::getCharacterList` |
| game-login version fields | numeric version, build/version string and asset-hash string present | `PROVEN` | `protocol_profile.cpp::currentGameLoginLayout` |
| game-login content revision | absent for Current | `PROVEN` | `protocol_profile.cpp::currentGameLoginLayout` |
| preview state | present | `PROVEN` | `protocol_profile.cpp::currentGameLoginLayout` |
| game authentication | session-key layout | `PROVEN` | `protocol_profile.{hpp,cpp}`; `protocolgame.cpp` |
| challenge response | present | `PROVEN` | `protocol_profile.cpp::currentGameLoginLayout` |
| OTCv8 probe | source expects the Current layout to account for this field | `PROVEN` | `protocol_profile.cpp::currentGameLoginLayout` |
| Oteryn native credential | existing Game Session credential is consumed through the session-key field, once, by one exact issuer process | `PROVEN` for maintained producer path; Rust consumer absent | Platform `docs/contracts/GAME_SESSION_CANARY_CONTRACT.md` at `285eb5f...`; Canary session manager/protocol source at `87149c...` |

## Current feature mask

The Current profile enables these source-level gates in `protocol_profile.cpp::currentProfile`:

| Feature | Producer evidence | Initial MPS relevance |
|---|---|---|
| `CurrentPayload` | enabled | baseline Current packet shapes |
| `LoginSpeedFormula` | enabled | session start/player movement initialization |
| `ModernLoginSideSystems` | enabled | login-side payloads; defer non-MPS extras unless required by fixture |
| `ResourceBalancePackets` | enabled | minimal stats/resources subset only |
| `CustomMonkPackets` | enabled | not required for generic first MPS unless selected character/runtime requires it |
| `MarketPackets` | enabled | defer from first MPS |
| `ImbuementWindow` | enabled | defer from first MPS |
| `MemorialPackets` | enabled | defer from first MPS |
| `PlayerDataLevelPercentU16` | enabled | player-data fixture must prove centesimal `u16` behavior |
| `GameEventPayload` | enabled | fixture exact event-selector shape before use |
| `OfficialTaskboardPackets` | enabled | defer from first MPS |
| `OfficialVocationSpecificPlayerData` | enabled | fixture selected vocation-specific branch before claiming login completion |
| `OfficialWeaponProficiencyPayload` | enabled | build-string-sensitive; defer unless required by selected login baseline |
| `GraphicalEffectSourceByte` | enabled | map/effect fixture must prove source-byte semantics before implementing that family |
| `OfficialSoulSealsPackets` | enabled | defer from first MPS |
| `OfficialSkillWheelPayload` | enabled | defer from first MPS |

`PROVEN` build-string branch: `protocolgame.cpp::supportsWeaponProficiencyDetailList` recognizes prefixes `15.25.794c2e` and `15.25.d96c64`. Unknown `15.25.*` builds use the shorter shape and log a diagnostic. A later adapter task must select and record the exact build string; `15.25` alone is insufficient.

## Minimum-playable family inventory

The following table scopes fixture acquisition. It intentionally does not reproduce opcode values or freeze field layouts.

| Family | Direction | Current producer/parser owners | Evidence state | Required before implementation claim |
|---|---|---|---|---|
| initial challenge, game login and session admission | both | `protocol_profile.{hpp,cpp}`, `protocolgame.{hpp,cpp}`, `security/login_session_manager.*`, `io/iologindata*` | `SUPPORTED` | full first-message fixtures, challenge mismatch, invalid/expired/replayed session, wrong profile/character and state-transition negatives |
| session start/end/errors | server -> client; logout client -> server | `protocolgame.{hpp,cpp}` (`sendSessionEndInformation`, login/logout/leave-game state), `game/game.*` | `SUPPORTED` | successful login baseline, each selected terminal state, duplicate/out-of-order logout and stale-session cases |
| map description, floor/region and tile updates | server -> client | `protocolgame.{hpp,cpp}`, map/tile/position helpers | `SUPPORTED` | synthetic smallest map, boundary floors/coordinates, stack limit, unknown/removed tile objects, truncation at every variable section |
| known/unknown creature, add/move/remove | server -> client | `protocolgame.{hpp,cpp}` (`checkCreatureAsKnown`, visibility and creature send helpers) | `SUPPORTED` | known-set transition corpus, removed-known reuse, movement visibility edges and malformed appearance data |
| local movement, turn and stop | client -> server | `protocolgame.cpp::parsePacket*`, movement parse methods and `game/game.*` commands | `SUPPORTED` | each direction, auto-walk bounds, illegal enum, too-long path, out-of-order/pre-login command |
| item serialization and references | server -> client | `protocolgame.cpp::AddItem`, item/type serialization helpers | `SUPPORTED` | subtype/count/tier variants used by MPS, unknown type, invalid references and bounded collection cases |
| inventory/equipment/container updates | both | `protocolgame.{hpp,cpp}` container/inventory send and parse methods | `SUPPORTED` | open/close/add/update/remove, nested/reference boundaries, invalid slot/index/count and state ordering |
| player stats/resources | server -> client | `protocolgame.{hpp,cpp}` player-data/stat/resource functions | `SUPPORTED` | one minimal Current subset; `PlayerDataLevelPercentU16`; width/boundary cases for every selected field |
| attack/follow/use/use-with/move-item | client -> server | `protocolgame.{hpp,cpp}` parse methods; `game/game.*` action dispatch | `SUPPORTED` | valid command shapes, invalid position/stack/target/id, stale target and pre-login/out-of-order cases |
| text/system/local chat | both | `protocolgame.{hpp,cpp}`, chat/speech owners | `SUPPORTED` | selected speech classes, bounded UTF-8/string lengths, invalid class/channel, private-content exclusion from retained fixture metadata |
| ping/heartbeat/connection health | both | `protocolgame.{hpp,cpp}`, protocol/connection owners | `SUPPORTED` | request/response, duplicate/out-of-order, timeout and disconnect state transitions |
| logout | both | `protocolgame.{hpp,cpp}` leave-game state machine and `game/game.*` | `SUPPORTED` | normal, denied, forced, duplicate, raced disconnect and session cleanup cases |

## Compatibility statement

| Consumer | Producer | Expected result | Status |
|---|---|---|---|
| current repository with no Rust adapter | any Canary | no Rust game connection | `PROVEN` |
| future Rust Current adapter | `87149c6...` without fixtures | not claimable | `BLOCKED` |
| future Rust Current adapter | exact selected Canary revision + exact build string + reviewed fixture corpus | candidate MPS pair | `SUPPORTED`, future task only |
| future Rust Current adapter | later arbitrary Current revision | fail closed until material profile/layout changes are reviewed | required policy |
| first Rust adapter | Tibia 11.00 or any 8.60/OTCv8 profile | unsupported | `PROVEN` non-goal |

## Source inventory

All Canary paths below are pinned to `87149c6b527f43025860c20cca0a440091ee8730`:

- `src/core.hpp`
- `src/server/network/protocol/protocol_profile.hpp`
- `src/server/network/protocol/protocol_profile.cpp`
- `src/server/network/protocol/transport_codec.hpp`
- `src/server/network/protocol/transport_codec.cpp`
- `src/server/network/protocol/protocollogin.hpp`
- `src/server/network/protocol/protocollogin.cpp`
- `src/server/network/protocol/protocolgame.hpp`
- `src/server/network/protocol/protocolgame.cpp`
- `src/security/login_session_manager.hpp`
- `src/security/login_session_manager.cpp`
- `src/io/iologindata.hpp` and owned implementation files
- `src/game/game.hpp` and `src/game/game.cpp`

A future task must narrow this broad producer inventory to exact functions and fixture hashes before adding Rust constants or parsers.
