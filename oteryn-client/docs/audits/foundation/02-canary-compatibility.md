# Canary Compatibility Audit

Evidence cut: Canary `main` at `1408aaa886240034a90fc33873e9b9e0fa47cab6`.

## Candidate baseline

### Current profile

- `PROVEN` Canary defines `CLIENT_VERSION = 1525` in `src/core.hpp`.
- `PROVEN` the modern game port resolves to `ProtocolProfileId::Current` in `src/server/network/protocol/protocolgame.cpp`.
- `PROVEN` the profile registry distinguishes `Current`, `Tibia1100` and several 8.60/OTCv8 profiles in `protocol_profile.hpp`.
- `PROVEN` the Current profile uses a version/feature model that includes modern login, resources, market, Monk, Taskboard, Soul Seals, skill wheel and other payload gates.
- `PROVEN` some 15.25 payload shapes are build-string-specific. Weapon-proficiency detail-list output currently recognizes prefixes `15.25.794c2e` and `15.25.d96c64`; unknown 15.25 builds use the shorter shape.

### Audit selection

`SUPPORTED` the initial Rust Canary adapter should target **Canary `ProtocolProfileId::Current`, client protocol 15.25**, using the exact Canary revision selected by the adapter task.

This audit does not freeze the adapter to Canary audit-head `1408aaa...`. The implementation task must:

1. revalidate current `main` and open protocol PRs;
2. select an exact Canary commit;
3. record the exact current profile/feature mask and known build string;
4. create shared `OTS-*`, `CAN-*` and `OTC-*` tasks;
5. prove fixtures and E2E against that pair.

`REJECTED` supporting all legacy profiles in the first Rust adapter. Additional profiles are independent later packages.

## Protocol architecture evidence

Canary already separates several concerns useful to the new adapter:

| Evidence | Status | Client implication |
|---|---|---|
| `ProtocolProfileId` and `ProtocolFeature` registry | `PROVEN` | Rust adapter needs explicit version/capability inputs rather than ad hoc version conditionals across features |
| `TransportProfile` with outer length, encryption, checksum and compression layouts | `PROVEN` | transport/framing behavior must stay below normalized game events |
| `AccountLoginLayout` and `GameLoginLayout` | `PROVEN` | login/world-list and game-entry parsing are distinct contracts |
| Current game login uses session-key authentication layout | `PROVEN` | Oteryn Game Session can enter through the maintained field without main-password transport |
| malformed/unsupported profile states exist | `PROVEN` | unsupported combinations must fail before gameplay |
| modern payloads have feature/build gates | `PROVEN` | one numeric version is insufficient to describe compatibility |

## Multi-channel evidence

### Shipped Canary behavior

`PROVEN` Canary's multi-channel architecture defines:

- one Canary process per gameplay channel;
- process identity from `--channel-id`, `CANARY_CHANNEL_ID`, then safe fallback channel `1`;
- one shared account/character/economy model;
- per-channel runtime map, players, monsters, NPCs, spawns, local party/trade/chat and physical map state;
- a channel registry and login gateway;
- modern login world-list entries `(worldId, name, ip, port)`;
- the same character repeated for each available channel, carrying that channel's `worldId`;
- a disabled-by-default multi-channel gate and runtime availability/heartbeat model.

Evidence:

- `docs/multichannel/ARCHITECTURE.md`;
- `src/game/multichannel/channel_context.hpp`;
- `src/server/network/protocol/protocolgame.cpp`.

### Client consequence

- `PROVEN` a Canary-compatible client can select a gameplay channel through the existing character/world list; no new gameplay packet is required for that classic path.
- `PROVEN` the new client must represent this value as `WorldChannelId` even when the Canary adapter receives it through a field called `worldId`.
- `REJECTED` equating Platform `game_worlds.id`, Canary login-list `worldId`, and Canary `ChannelContext::channel_id` without an explicit mapping contract.

## Native-auth compatibility evidence

The authoritative Platform contract records:

- Oteryn Platform/Gateway protocol v1 merged at `8006534108d835474dadd208b0ec934e4a12528b` with later hardening;
- Canary game-session issuer introduced at `b8a88f073b2609b444fa15370aae30ac9f80b908` with later credential-rotation hardening;
- maintained OTClient consumer merged at `bb87346f6c516a19d19497d82bb01fb389334ff5`;
- a bounded E2E baseline using Canary `285dec6a034aa3620ae5ca12549fb9e8e1b35631`, maintained client `bb87346...` and Gateway `800653...`;
- one successful world entry and replay rejection.

`PROVEN` the native-auth credential is consumed through the existing Game Session key path and the user's Oteryn password is not used at Gateway -> Canary admission.

`BLOCKED` production activation remains gated on exact hardened revisions, network/TLS/secret injection and hardened E2E evidence.

## Critical multi-channel/native-auth gap

Current Gateway -> Canary protocol v1 explicitly limits itself to:

- one configured Platform world;
- one exact Canary process/issuer;
- one process-local Game Session store;
- `ProtocolProfileId::Current`.

It explicitly does **not** claim:

- multi-world issuer selection;
- same-world replicas without exact sticky/process routing;
- shared Game Session storage across processes.

It also states Platform `game_worlds.id` is not Canary `ChannelContext::channel_id`.

Therefore:

- `BLOCKED` the desired Oteryn-native request `character + world + gameplay channel -> ticket` is not covered by protocol v1.
- `SUPPORTED` an initial controlled Rust-client E2E may target one exact channel/issuer using protocol v1.
- `INFERRED` channel-aware native auth requires either a channel-aware Gateway issuer mapping or an authoritative route returned after selecting a channel. The exact server design is outside this client audit and requires a cross-repository contract.

## Minimum-playable message families

The adapter task must inventory exact fields/opcodes for these families against the selected Canary commit:

| Family | Direction | Audit status |
|---|---|---|
| game challenge/login/session admission | both | `SUPPORTED`; architecture and layouts proven, exact byte fixtures still required |
| session start/end/errors | server -> client | `SUPPORTED`; normalized lifecycle cases need fixtures |
| map description/region/tile updates | server -> client | `SUPPORTED`; existing parser/producer code, exact MPS fixture inventory incomplete |
| creature known/unknown, movement and removal | server -> client | `SUPPORTED` |
| local movement/turn/stop commands | client -> server | `SUPPORTED` |
| item serialization and tile/container references | server -> client | `SUPPORTED`; subtype/version mapping needs exact review |
| inventory/equipment/container updates | both | `SUPPORTED` |
| basic player stats/resources | server -> client | `SUPPORTED`; select minimal Current-profile subset |
| attack/follow/use/use-with/move-item | client -> server | `SUPPORTED` |
| text/system/local chat | both | `SUPPORTED` |
| ping/heartbeat/connection health | both | `SUPPORTED` |
| logout | client -> server and result | `SUPPORTED` |

No opcode or field shape is frozen by this audit. The table defines work packages, not packet truth.

## Fixture requirements

For each selected family:

- positive encoded/decoded fixture;
- smallest valid payload;
- maximum bounded collection/string case;
- truncated input at each variable-length boundary;
- invalid count/length/enum;
- wrong profile/feature gate;
- out-of-order state transition;
- round-trip output inspection where semantically stable;
- fuzz entry point and minimized regression corpus;
- exact Canary producer path and commit in fixture metadata.

Fixtures committed to this repository must be synthetic or explicitly proven redistributable. Live credentials and private packet captures are forbidden.

## Compatibility matrix

| Rust client | Canary | Expected outcome | Status |
|---|---|---|---|
| no adapter | any | no game connection | `PROVEN` current architecture phase |
| future Current-profile adapter | exact selected 15.25 Canary commit | MPS target | `SUPPORTED`, not implemented |
| future Current-profile adapter | arbitrary later Current profile | fail unless capability/version compatibility is proven | `PROVEN` required policy |
| future Current-profile adapter | Tibia 11.00 / 8.60 profiles | unsupported | `PROVEN` initial non-goal |
| Oteryn native auth v1 | one exact configured Canary issuer | supported after exact E2E/activation gates | `SUPPORTED` |
| Oteryn native auth v1 | arbitrary channel chosen from a multi-channel cluster | unsupported by current contract | `BLOCKED` |

## Required next cross-repository tasks

Before channel-aware native gameplay:

1. define a shared identifier mapping for Platform world, product gameplay channel, Canary login-list world ID and `ChannelContext::channel_id`;
2. define channel-aware issuer selection/routing and one-shot credential scope;
3. define supported failure behavior when the selected channel becomes unavailable;
4. prove one-character, two-channel relog with two fresh credentials and no session overlap;
5. update Platform, Canary and Rust-client compatibility matrices.
