# Oteryn Identity Native Login

## Status

`CLIENT IMPLEMENTATION VALIDATING — PLATFORM AND GAME GATEWAY PRODUCERS EXIST; PRODUCTION CANARY GAME SESSION ADAPTER IS NOT YET SELECTED`

This document describes the first-party Oteryn authentication path implemented by OTClient task `OTC-20260721-oteryn-identity-login` and coordinated as `OTS-20260721-oteryn-identity-auth`.

It does not authorize or claim a Canary-side Game Session adapter. The current client implementation remains disabled until deployment configuration provides the exact Identity, Platform ticket and Game Gateway endpoints plus the registered native OAuth client id.

## Verified producer baseline

The client contract was revalidated against `blakinio/Oteryn-Platform` after these merged phases:

- ADR/game-auth architecture: PR #117, merge `78bc9f839b98b96ff9e5e3fcf43680104a5e27fa`;
- game-auth domain foundation: PR #118, merge `fc6b70fa11f3bb9958b405fc76d8918c49381668`;
- native OAuth Authorization Code + PKCE: PR #119, merge `27fa277c5def0e151d7ee013acef188dbfd6f463`;
- Game Login Ticket issue/redeem API: PR #121, merge `cab00c140ce200e3cd51b7eafe2c1659842c2b90`;
- standalone Game Gateway MVP: PR #122, merge `8006534108d835474dadd208b0ec934e4a12528b`.

The authoritative cross-repository contracts remain the Platform documents:

- `docs/contracts/OTCLIENT_GAME_AUTH_CONTRACT.md`;
- `docs/contracts/GAME_GATEWAY_IDENTITY_CONTRACT.md`;
- `docs/contracts/GAME_SESSION_CANARY_CONTRACT.md`;
- `docs/contracts/WORLD_REGISTRY_CONTRACT.md`.

## Target flow implemented by this client

```text
OTClient
  -> system browser
  -> Oteryn Identity /oauth/authorize
  -> loopback callback with Authorization Code
  -> Oteryn Identity /oauth/token using PKCE verifier
  -> short-lived OAuth access token in process memory
  -> Oteryn Platform POST /api/v1/game-auth/tickets
  -> opaque one-time Game Login Ticket in process memory
  -> Oteryn Game Gateway POST /v1/login
  -> Game Session credential + authoritative worlds + characters
  -> selected Canary world using GameSessionKey protocol field
```

The user's Oteryn password, MFA secret/code, recovery code and OAuth refresh token are not inputs to the OTClient-native flow.

## Configuration

Global deployment configuration lives under `Services.oterynIdentity`:

```lua
oterynIdentity = {
    enabled = false,
    authorizationEndpoint = "https://<identity>/oauth/authorize",
    tokenEndpoint = "https://<identity>/oauth/token",
    ticketEndpoint = "https://<platform>/api/v1/game-auth/tickets",
    gatewayLoginEndpoint = "https://<game-gateway>/v1/login",
    clientId = "<registered-public-native-client-id>",
    scope = "game:ticket",
    callbackTimeoutMillis = 120000,
    maxGameTicketTtlSeconds = 60,
    allowInsecureLoopback = false
}
```

Production endpoints must use HTTPS. `allowInsecureLoopback` exists only for literal `http://127.0.0.1` development endpoints.

A server/profile opts into the first-party Oteryn flow explicitly:

```lua
authMode = "oteryn_identity"
legacyAuthEnabled = false
oterynIdentity = {
    enabled = true,
    protocolVersion = 1
}
```

World host and port are never authoritative from this local profile. After authentication they come from the Game Gateway response and are matched through exact `world_id` references.

## OAuth native-client behavior

The client:

1. creates a high-entropy `state` and PKCE `code_verifier` using CSPRNG-backed UUID material;
2. derives `code_challenge = BASE64URL(SHA256(code_verifier))`;
3. binds a desktop HTTP callback listener to IPv4 loopback only;
4. uses callback path `/callback` and an OS-assigned ephemeral port obtained by binding `127.0.0.1:0`;
5. opens the authorization URL in the operating system browser;
6. accepts only the configured callback path;
7. requires exact `state` equality;
8. rejects duplicate sensitive callback parameters;
9. closes the callback listener after terminal success/failure;
10. exchanges the code once using `code_verifier` and no client secret.

Only one Oteryn flow may be active at a time.

## Credential lifecycle

| Credential | OTClient handling | Destination |
|---|---|---|
| Oteryn password | never requested/stored by native flow | browser -> Identity only |
| PKCE verifier | process memory, cleared after code request is queued | OAuth token endpoint |
| Authorization code | process memory, cleared after code request is queued | OAuth token endpoint |
| OAuth access token | process memory, cleared after ticket request is queued | Platform ticket endpoint only |
| OAuth refresh token | ignored | none |
| Game Login Ticket | process memory, cleared after Gateway request is queued | Game Gateway only |
| Game Session credential | process memory until first actual world-login handoff | Canary game connection only |

No Oteryn password, OAuth token, ticket or Game Session credential is written to `g_settings`.

## Ticket issuance

After a successful OAuth token exchange, OTClient sends:

```http
POST /api/v1/game-auth/tickets
Authorization: Bearer <short-lived-oauth-access-token>
Content-Type: application/json

{"protocol_version":1}
```

Expected response:

```json
{
  "protocol_version": 1,
  "ticket": "<opaque-ticket>",
  "expires_in": 60
}
```

The access token is not sent to Game Gateway or Canary. The bearer header exists only while the HTTP layer synchronously copies it into the queued ticket request; the temporary `Authorization` entry is removed from shared HTTP header state immediately afterwards.

## Game Gateway login

The current implemented Gateway endpoint accepts exactly:

```json
{
  "protocol_version": 1,
  "game_login_ticket": "<opaque-ticket>"
}
```

Unknown request fields are intentionally not sent because the deployed Gateway uses strict JSON decoding.

A successful Gateway response is normalized only when:

- `protocol_version == 1`;
- `session.credential` is a non-empty bounded string;
- `session.expires_at` is present;
- at least one valid world exists;
- every world has a unique positive id, non-empty name/host and valid TCP port;
- every character references an exact returned `world_id`;
- every character has a non-empty name.

The client uses the returned world `host` and `port` for the selected character. Locally edited account/world ownership data is not accepted as authority.

## Game Session handoff

The current OTClient game protocol already supports `GameSessionKey`. When that feature is enabled, `ProtocolGame::sendLoginPacket` serializes the session key and selected character name instead of account/password.

For the Oteryn path:

- `G.account`, `G.password` and `G.authenticatorToken` are empty;
- `G.sessionKey` temporarily contains only the Gateway-issued Game Session credential;
- the character list contains only Gateway-authoritative world routing;
- `CharacterList.tryLogin` calls `g_game.loginWorld` first; C++ synchronously copies the session credential through `Game::loginWorld` into `ProtocolGame::m_sessionKey` before `connect()` begins;
- only after that actual handoff returns does Lua clear `G.sessionKey` and mark the Oteryn Game Session consumed;
- a second attempt or auto-reconnect fails closed and requires a fresh `Sign in with Oteryn` flow;
- lack of subscription information from Gateway is shown neutrally as `Oteryn Account`, without inventing Free/Premium status or showing premium upsell based on missing data.

This client-side handoff does not prove that production Canary accepts the credential. The exact Game Session adapter remains governed by `GAME_SESSION_CANARY_CONTRACT.md` and requires a separate Phase 6 implementation/evidence gate.

## Legacy migration behavior

The first-party Oteryn profile never silently falls back to password authentication.

When `authMode = "oteryn_identity"`:

- the primary action is `Sign in with Oteryn`;
- account/password-related controls are hidden;
- pressing the normal login action is redirected into Oteryn native auth;
- failure returns to signed-out UI rather than calling the legacy password flow.

Legacy password behavior remains available only for profiles explicitly configured with `authMode = "legacy"`. Existing encrypted legacy settings are not removed by this phase because generic/custom-server compatibility remains a migration requirement.

## Error and retry policy

The client does not blindly retry:

- authorization-code exchange;
- Game Login Ticket issuance;
- Game Gateway ticket redemption;
- Game Session world entry.

An invalid/expired/reused ticket is presented to the user as a requirement to sign in again. Gateway and Platform internals are not exposed through detailed probing messages.

Cancellation or timeout closes the listener, cancels the active HTTP operation when possible and clears state/verifier/code/access-token/ticket references.

## Current security boundaries

- callback listener is desktop-only and binds IPv4 loopback;
- production service endpoints require HTTPS;
- no confidential OAuth client secret is embedded in OTClient;
- no bearer credential is put in a URL/query string;
- temporary bearer HTTP state is removed after the one ticket request is queued;
- ticket and Game Session values are never intentionally logged;
- world routing is server-authoritative;
- unsupported protocol versions fail closed;
- native auth is disabled by default.

## Remaining production blockers

1. The final production Canary Game Session adapter is not selected/implemented in this OTClient task.
2. Cross-repository E2E must prove browser -> Identity -> ticket -> Gateway -> Game Session -> selected Canary world.
3. Exact production endpoint URLs and native OAuth client id must be injected by deployment configuration.
4. Legacy Oteryn password paths may only be disabled/removed after the authoritative cross-repository cutover gate.

## Required validation before production enablement

Client-side/CI evidence must cover at minimum:

- Lua syntax and static checks;
- desktop C++ build for loopback/CSPRNG changes;
- state mismatch and duplicate callback rejection;
- PKCE S256 derivation;
- callback path rejection;
- loopback-only listener behavior;
- cancellation/timeout cleanup;
- no Oteryn credential persistence;
- exact Platform ticket request shape;
- exact Gateway request/response shape;
- unknown world reference fail-closed;
- one-shot Game Session handoff/no auto-replay;
- no password-based `ProtocolLogin` or HTTP login on the Oteryn profile.

Cross-repository production evidence additionally requires the exact Platform, Gateway and Canary/session-adapter versions used in the test.
