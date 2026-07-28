# Canary channel and native-session gaps

Evidence cuts:

- `blakinio/canary@87149c6b527f43025860c20cca0a440091ee8730`
- `blakinio/Oteryn-Platform@285eb5f89b8f83752fa4d5798bb242136b7b9ae6`
- `blakinio/otclient@9b5c86dff694aa65f4b264683f9c5ce3bf000035`

## Identifier separation

| Concept | Current owner/shape | Proven semantics | Must not be assumed |
|---|---|---|---|
| Platform world ID | Platform `game_worlds.id`; Gateway v1 request `world_id` | selects the configured Platform world mapped to one exact Canary issuer | equal to a Canary process/channel ID |
| Canary database channel ID | `channels.id` in the multi-channel registry | persistent configuration identity for a channel row | equal to the response-local modern login-list index in every response |
| Canary process channel ID | signed `int32_t` held by `ChannelContext`; CLI `--channel-id`, then `CANARY_CHANNEL_ID`, then fallback `1` | identifies the channel represented by one Canary process | equal to Platform `game_worlds.id`; suitable as the product's public ID without a mapping contract |
| modern Canary login-list world ID | one-byte zero-based index generated while serializing the selected response world table | links each character row to a world entry in that same login response | globally stable across channel ordering/configuration changes; equal to `channels.id` |
| legacy Canary channel selection | per-character row includes endpoint/name; one row per `(character, channel)` | chooses one channel without a separate world table | same wire shape as Current |
| product `WorldChannelId` | stable typed domain identifier required by Rust architecture | must survive presentation and wire-adapter naming differences | derivable from a transient response index without an authoritative mapping/stability policy |

Evidence:

- Canary `docs/multichannel/ARCHITECTURE.md` and `src/game/multichannel/channel_context.hpp` define process/channel ownership.
- Canary `src/server/network/protocol/protocollogin.cpp::getCharacterList` serializes the modern response-local world table and repeated character rows.
- Platform `docs/contracts/GAME_SESSION_CANARY_CONTRACT.md` explicitly states Platform `game_worlds.id` is not Canary `ChannelContext::channel_id`.
- Oteryn architecture requires a server-provided stable `WorldChannelId` and prohibits inferring physical topology.

## Classic Canary path

`PROVEN` current classic login can expose multiple channels without a new gameplay packet:

1. a designated login-gateway process loads available login-list channels;
2. the modern response serializes one world-table entry per available channel;
3. each account character is repeated for each serialized world-table index;
4. selecting a row chooses that channel's endpoint;
5. a game login creates a normal session in that exact process.

This path is useful compatibility evidence, but it does not establish the desired Oteryn-native directory contract. The encoded modern `worldId` is response-local; the Rust adapter must not leak that storage/width/name into the domain.

`SUPPORTED` initial compatibility approach: normalize the selected response entry into an adapter-owned channel descriptor carrying all producer-provided fields plus explicit provenance. The domain-facing stable ID remains blocked until an accepted mapping/stability contract exists.

## Gateway native-auth v1 path

`PROVEN` current native-auth flow:

```text
Identity OAuth + PKCE
  -> one-time Platform Game Login Ticket
  -> Game Gateway redeem
  -> POST one exact Canary issuer /internal/v1/game-sessions
  -> opaque single-use 60-second process-local Game Session
  -> existing GameSessionKey field
  -> Canary admission
```

The contract is intentionally bounded to:

- one configured Platform world;
- one exact Canary process/listener;
- `ProtocolProfileId::Current`;
- one process-local `LoginSessionManager` store.

It does not claim:

- channel-aware issuer selection;
- multi-world issuer selection;
- same-world replicas without exact sticky/process routing;
- shared Game Session storage between processes;
- transparent credential replay after a lost issuer response;
- active-session revocation from later Identity security events.

## Required contracts before channel-aware native login

### 1. Stable identifier mapping

A cross-repository contract must define:

- authoritative product `WorldId` and `WorldChannelId` types;
- mapping from Platform directory descriptors to a selected Canary issuer/channel;
- whether Canary `channels.id` is exposed, transformed or kept internal;
- whether a classic login-list response index is ephemeral only;
- uniqueness scope, width, signedness, lifecycle and reuse rules;
- behavior when channel ordering changes or a channel is removed/recreated.

### 2. Authoritative route and ticket scope

The producer must define whether channel selection returns:

- an authenticated route to one exact issuer; or
- an opaque route key resolved by Gateway; or
- another reviewed mechanism.

The one-shot credential scope must include the exact selected account/character/world/channel context according to the producer contract. The client must never infer a physical node address.

### 3. Availability and failure behavior

Required one-sided outcomes:

- selected channel disappears before ticket issue;
- issuer becomes unavailable after ticket issue but before consumption;
- Gateway receives a successful issuer response but loses its own response;
- channel enters maintenance/draining/offline state;
- stale directory data names a removed or reordered channel;
- relog selects a new channel while the old game session is closing;
- old credential is replayed against another issuer, character or profile.

Every unsupported or ambiguous combination must fail closed with a typed, non-secret client action.

### 4. Relog lifecycle proof

Required exact-pair E2E:

1. authenticate account once;
2. select one character and Channel A;
3. obtain and consume credential A once;
4. close game session A while preserving only the valid account session;
5. destroy all session-A state and generations;
6. select Channel B;
7. obtain a fresh credential B scoped to Channel B;
8. prove credential A is rejected and no old session state mutates session B;
9. prove exactly one active game session and one successful entry per credential.

## Current disposition

| Claim | Status | Reason |
|---|---|---|
| classic Current login-list channel selection exists | `PROVEN` | current Canary source |
| Current Rust adapter can parse it | `BLOCKED` | no adapter or fixture corpus |
| response-local `worldId` is a stable product channel ID | `REJECTED` | serializer uses response index; no stability contract |
| native auth can enter one exact configured issuer | `SUPPORTED` | producer implementation and bounded older E2E exist; hardened production E2E remains gated |
| native auth can select arbitrary channel | `BLOCKED` | protocol v1 capability boundary excludes it |
| seamless in-game channel migration | `REJECTED` initial architecture | channel change is relog |

## First implementation recommendation

Do not combine channel-aware native routing with the first parser package. First implement and verify isolated Current transport/login parsing against synthetic fixtures. Channel-aware Identity/Gateway/Canary work begins only after a dedicated shared contract and exact producer tasks exist.
