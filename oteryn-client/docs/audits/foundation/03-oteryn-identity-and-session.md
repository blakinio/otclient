# Oteryn Identity, Directory and Session Audit

Evidence cut:

- Oteryn Platform `main`: `348f483938fc8358132128fc79d229e38b98045b`;
- maintained client `main`: `5568cb6f5e2fd6162c78cde304deea5d32461e05`;
- authoritative cross-repository document: `blakinio/Oteryn-Platform/docs/contracts/GAME_SESSION_CANARY_CONTRACT.md`.

## Current proven flow

```text
Rust/maintained client
 -> system browser
 -> Oteryn Identity Authorization Code + PKCE
 -> Platform Game Login Ticket
 -> Oteryn Game Gateway
 -> authoritative ticket redeem
 -> Canary account + configured world context
 -> exact Canary issuer /internal/v1/game-sessions
 -> opaque one-use Canary Game Session credential
 -> client
 -> Canary GameSessionKey world-entry field
 -> ProtocolGame / IOLoginData admission
```

### Identity transaction

- `PROVEN` maintained deployment configuration expects Authorization, token, ticket and Gateway login endpoints plus a public native `clientId`.
- `PROVEN` Oteryn mode is disabled by default and production endpoints require HTTPS, with literal loopback HTTP allowed only for controlled development.
- `PROVEN` configured scope is currently `game:ticket`, callback timeout 120 seconds and maximum accepted game-ticket TTL 60 seconds in maintained client configuration.
- `PROVEN` the architecture requires system-browser Authorization Code + PKCE S256 and strict transaction `state`/callback generation validation.
- `PROVEN` the Oteryn profile does not silently fall back to main-password login.

Exact Identity endpoint schemas beyond the authoritative game-session contract must be revalidated in the WS-R03 implementation task. This audit does not freeze field names from legacy Lua into Rust APIs.

## Credential taxonomy

| Credential/state | Owner | Current evidence | Rust requirement |
|---|---|---|---|
| PKCE verifier, state, callback nonce | client Identity transaction | maintained native-auth flow | memory only, one attempt, stale/duplicate callback rejection |
| OAuth access/refresh material | Oteryn Identity/account session | Platform implementation | OS credential store where persistence is allowed; never exposed to features/extensions |
| Game Login Ticket | Oteryn Identity | ~60-second current policy, atomic single-use | separate type from game session; never logged/persisted |
| Gateway service credential to Platform | server-side only | hashed current/previous rotation contract | never enters client |
| Gateway service credential to Canary | server-side only | separate rotation contract | never enters client |
| Canary Game Session credential | exact Canary issuer process | opaque, 60-second TTL, atomic single-use | one connection attempt; clear after handoff; no reconnect replay |
| game-session/resume state | Canary game protocol | exact resume contract not established for Rust | separate from initial ticket; adapter-specific |

`REJECTED` using one generic string/token type for all credentials.

## Gateway -> Canary contract v1

Request:

```json
{
  "protocol_version": 1,
  "canary_account_id": 101,
  "world_id": 1,
  "login_attempt_id": "00112233445566778899aabbccddeeff"
}
```

Response returns protocol version and opaque credential/expiry.

Current semantics:

- `PROVEN` protocol version is exactly `1`;
- `PROVEN` account ID and Platform world context come from authoritative ticket redeem;
- `PROVEN` `login_attempt_id` is a server-generated 32-hex idempotency identifier, not a bearer secret;
- `PROVEN` one successful issuance is allowed per attempt/issuer/TTL;
- `PROVEN` Game Session credentials are stored as the existing SHA-256 representation and consumed atomically once;
- `PROVEN` wrong character/profile consumption burns the credential according to existing manager semantics;
- `PROVEN` issuer restart invalidates unconsumed process-local credentials;
- `PROVEN` current Game Session is bound to `ProtocolProfileId::Current` and the account's allowed character-name set;
- `PROVEN` normal Canary deletion, ban and admission checks remain authoritative after authentication.

## Proven E2E and production gate

Bounded E2E evidence:

- scenario `login/oteryn-native-auth`;
- behavior run `29988893301`;
- evidence run `29992417296`;
- Canary adapter revision `285dec6a034aa3620ae5ca12549fb9e8e1b35631`;
- maintained client revision `bb87346f6c516a19d19497d82bb01fb389334ff5`;
- Gateway revision `8006534108d835474dadd208b0ec934e4a12528b`;
- one successful `Knight 1` world entry, logout and replay rejection.

- `PROVEN` bounded pre-hardening E2E exists.
- `BLOCKED` this is not proof of the final hardened production boundary.
- `BLOCKED` production activation still requires deployed private network/ingress, TLS hostname validation, secret-manager injection/rotation, exact deployed revisions and hardened E2E.

The Rust client must not claim production native-auth readiness from repository tests alone.

## Account session versus game session

- `PROVEN` Game Login Ticket and Canary Game Session are separate, atomic one-use credentials.
- `PROVEN` the accepted client architecture separates the account session from each game session.
- `SUPPORTED` a valid account session can support repeated game-entry transactions without repeated password entry.
- `UNKNOWN` exact Oteryn account-session refresh/expiry/error schemas for the Rust client; WS-R03 needs fake-service contracts and exact Platform fixtures.

## Directory contract

The new client needs one server-authoritative model:

```text
AccountDirectoryRevision
Characters[]
Worlds[]
GameplayChannels[]
compatibility requirements
availability / queue / recommendation when provided
```

Current evidence:

- `PROVEN` Canary login can expose one world entry per gameplay channel and repeat character rows per channel.
- `PROVEN` Gateway v1 accepts a Platform `world_id` for one exact issuer configuration.
- `UNKNOWN` a current Oteryn Platform client-facing directory endpoint that returns explicit `CharacterId`, `WorldId`, `WorldChannelId`, population/status and compatibility metadata.
- `BLOCKED` the desired explicit channel-scoped one-shot ticket is not defined by Gateway -> Canary protocol v1.

The Rust client may not synthesize authoritative channel availability from local configuration.

## Gameplay-channel relog

Required product lifecycle:

```text
InGame(Channel 1)
 -> request normal logout
 -> receive committed game end or explicit recoverable outcome
 -> discard all session-scoped state
 -> preserve valid account session and user preferences
 -> select Channel 2
 -> request a fresh channel-scoped game-entry transaction
 -> connect and create a new game session
```

Audit result:

- `PROVEN` Canary exposes channels through the login world list.
- `PROVEN` initial Game Session credential cannot be replayed or transferred.
- `PROVEN` accepted client ADR requires a fresh session for channel change.
- `SUPPORTED` classic Canary login can implement relog to another channel today.
- `BLOCKED` Oteryn-native channel selection/ticket routing and exact old-session closure fencing require a new cross-repository contract.

## Reconnect

- `PROVEN` automatic reconnect must not replay the original Oteryn Game Session credential.
- `UNKNOWN` whether the initial Rust Canary adapter will support session resume or only return to selection after loss.
- `INFERRED` first MPS should prefer a simple fail-closed return-to-selection path unless exact Canary resume evidence is selected and tested.

Reconnect and relog remain separate state-machine branches.

## Required client error taxonomy

The following external outcomes need stable internal actions, independent of legacy text:

| Condition | Required action |
|---|---|
| stale/mismatched OAuth callback | reject transaction; remain/return logged out |
| account session expired | `AuthenticateAgain` |
| directory revision stale | `RefreshDirectory` |
| selected channel unavailable/full | `ChooseAnotherChannel` or queue when contract exists |
| ticket issue/redeem failure | retry only under exact idempotency rules or start fresh attempt |
| game credential expired/consumed | request fresh game-entry transaction |
| protocol/client/asset mismatch | `UpdateOrRepair` |
| game logout denied | remain in current session with explicit reason |
| connection lost and no resume contract | `ReturnToSelection` after safe cleanup |

## Required WS-R03 fixtures

- PKCE success and state mismatch;
- stale callback after a newer auth transaction;
- duplicate callback;
- token/ticket response with excessive TTL;
- account-session expiry during selection;
- duplicate game-ticket use;
- Gateway route for wrong world/channel;
- credential consumed once;
- reconnect path proving no initial-ticket replay;
- relog Channel 1 -> Channel 2 with two fresh game-entry transactions;
- selected channel disappears between directory and ticket request;
- secret/log/crash/replay redaction.

## Cross-repository decisions required

1. explicit client-facing typed directory schema;
2. stable mapping among Platform world, product gameplay channel, Canary login-list world ID and process `channel_id`;
3. channel-aware issuer selection and ticket scope;
4. old-session closure/fencing required before another channel admission;
5. queue/full/maintenance/error semantics;
6. session resume support or explicit non-support;
7. hardened exact-revision E2E including two-channel relog.
