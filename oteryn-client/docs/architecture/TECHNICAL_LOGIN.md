# W7 Technical Login Architecture

Status: proposed architecture slice for `OTERYN-W7-TECHNICAL-LOGIN`  
Runtime target: greenfield Rust Oteryn client on Windows  
Server target: project-owned Oteryn Platform / Game Gateway / Canary Current profile  
Scope limit: one configured world/issuer and one explicitly selected character

This document extends `ARCHITECTURE.md`, `CLIENT_LIFECYCLE.md`, `PROTOCOL_BOUNDARY.md` and `SECURITY_MODEL.md`. Those documents remain normative for the whole client. This file owns only the first technical-login slice.

## 1. Product outcome

The first W7 executable proves one bounded account-to-game path:

```text
start existing Rust executable
-> create existing Windows window and renderer
-> report LoggedOut
-> start Oteryn sign-in
-> open the system browser
-> receive and validate one loopback OAuth callback
-> exchange Authorization Code + PKCE S256
-> issue one Game Login Ticket
-> call Game Gateway protocol v1
-> receive authoritative worlds, characters and one fresh Game Session credential
-> select one character on one configured world
-> connect to Canary Current profile
-> submit the credential through the existing GameSessionKey world-login field
-> validate the admission prefix through enter-world 0x0F
-> report typed SessionEntered or typed recoverable failure
-> disconnect and clear every session-scoped secret
```

`SessionEntered` is a technical admission result. W7 does not claim map rendering, gameplay readiness, production rollout or general protocol coverage.

## 2. Explicit exclusions

W7 does not implement:

- map, tile, creature, item, container, inventory, chat, combat or movement decoding;
- production asset packs or asset runtime mounting;
- a general native UI framework or final login presentation;
- multi-world issuer discovery, gameplay-channel switching or issuer replicas;
- updater, launcher, signing or deployment activation;
- legacy password fallback for an Oteryn Identity profile;
- official Tibia service automation or gameplay manipulation;
- BattlEye patching, disabling, hooking, impersonation, emulation or bypass;
- publication of private captures, credentials, proprietary artifacts or reusable abuse tooling.

Protocol research is permitted only as internal compatibility work for the project-owned Oteryn/Canary stack. Prefer Canary source, project-owned instances, local mocks and synthetic fixtures.

## 3. Exact producer evidence

Every implementation lane must revalidate the producer revision before a compatibility claim.

### Oteryn Identity and Platform

- Native public OAuth producer: Platform PR #119, merge `27fa277c5def0e151d7ee013acef188dbfd6f463`.
- Game Login Ticket producer: PR #121, merge `cab00c140ce200e3cd51b7eafe2c1659842c2b90`.
- Registered redirect base: `http://127.0.0.1/callback`.
- Current producer tests prove that an otherwise matching dynamic loopback port, for example `http://127.0.0.1:49152/callback`, succeeds for authorization and token exchange; wrong path and non-loopback redirects fail closed.
- The Rust client binds `127.0.0.1:0`, uses the actual assigned port in authorization and token exchange, and never binds fixed port 80.
- Initial OAuth scope is `game:ticket`.
- Current ticket issuance revokes the associated access/refresh token family, so W7 owns one bounded bootstrap attempt rather than a reusable relog account session.

### Game Gateway

- Gateway protocol-v1 producer: Platform PR #122, merge `8006534108d835474dadd208b0ec934e4a12528b`.
- Current hardening evidence includes merge `53158217a6c6017230301cf4daa783b04fcc13d5`.
- Client endpoint: `POST /v1/login`.
- Strict request JSON:

```json
{
  "protocol_version": 1,
  "game_login_ticket": "<opaque-one-time-ticket>"
}
```

- Success JSON contains `protocol_version`, `session { credential, expires_at }`, authoritative `worlds[] { id, slug, name, region, host, port }` and account-scoped `characters[] { id, name, level, vocation, world_id }`.
- Unknown fields, trailing JSON, invalid protocol version, invalid/missing ticket and oversized data fail closed.
- Sensitive responses are no-store/no-cache.

### Canary

- Game Session issuer producer: Canary PR #722, merge `b8a88f073b2609b444fa15370aae30ac9f80b908`.
- Gateway service-credential rotation: Canary PR #807, merge `981c82f5ebb6bc22c867312c2b274a71f6aeeb3e`.
- Planning cut: Canary `4b2d6f432d92628c42bde1d95daed6ae0d0eb88f`; the worker must pin current revision, release/build and exact source paths again.
- Initial supported profile: `ProtocolProfileId::Current`.
- The opaque Game Session credential is process-local, hashed at rest, expires after 60 seconds and is consumed atomically once.
- Wrong character/profile may burn a matching credential; restart invalidates outstanding credentials.
- Protocol v1 supports one Platform world mapped to one exact Canary issuer process. Platform `world_id` is not a gameplay-channel ID.
- The game wire remains the existing Current-profile `GameSessionKey` path; no new game opcode is introduced.

Legacy OTClient PR #17 / merge `bb87346f6c516a19d19497d82bb01fb389334ff5` is read-only behavioral evidence only and never a Rust runtime dependency.

## 4. Runtime ownership

| Owner | Category | Responsibility | Must not own |
|---|---|---|---|
| `oteryn-account-session` | `account-session` | Account-auth generation, authenticated-context lifetime and cancellation ownership without bearer storage | HTTP, browser, world routing, game wire |
| `oteryn-world-directory` | `world-directory` | Validated authoritative worlds/characters and explicit selection | OAuth, sockets, credential storage |
| `oteryn-game-session` | `game-session` | One-shot credential lifetime, selected entry request, admission result and disconnect lifecycle | OAuth, JSON, TCP framing, Canary byte layout |
| `oteryn-platform` | `platform` | Strict bounded Platform ticket and Gateway-v1 DTO/HTTP boundary | browser state, game wire, UI |
| `oteryn-identity` | `identity` | Authorization Code + PKCE transaction, callback validation and conversion into entry contracts | UI, game wire, renderer, persistent passwords/tokens |
| `oteryn-protocol-core` | `protocol-core` | Bounded wire primitives, frame/parser contracts and protocol-neutral errors | socket ownership, Canary domain mapping |
| `oteryn-transport` | `transport` | Bounded TCP connection/read/write/framing lifetime and cancellation | account policy, selection, raw UI events |
| `oteryn-protocol-canary` | `protocol-canary` | Exact Current-profile challenge/world-login/admission mapping | Identity HTTP, gameplay domain beyond admission |
| `oteryn-app-runtime` | `app-runtime` | Typed progress/result/cancellation orchestration | duplicate backend contracts |
| `apps/client` | `app` | Compose existing shell/renderer with merged services | raw backend DTOs, secret persistence, duplicate contracts |

## 5. Dependency direction

```text
oteryn-foundation
  <- oteryn-account-session
  <- oteryn-protocol-core

oteryn-account-session
  <- oteryn-world-directory
  <- oteryn-game-session

oteryn-world-directory
  <- oteryn-game-session

oteryn-account-session + oteryn-world-directory + oteryn-game-session
  <- oteryn-platform
  <- oteryn-identity

oteryn-foundation + oteryn-protocol-core
  <- oteryn-transport

oteryn-world-directory + oteryn-game-session + oteryn-protocol-core + oteryn-transport
  <- oteryn-protocol-canary
merged W7 services
  <- oteryn-app-runtime
existing shell/renderer/diagnostics + app-runtime
  <- apps/client
```

No lower crate depends on `apps/client`, renderer, UI, a legacy runtime path or a producer repository.

## 6. Public contract model

Exact names may be refined only by the sole ENTRY producer. Consumers must not create substitutes.

### Account session

The account-session contract carries:

- a client-local opaque session generation/correlation identity;
- public lifecycle state required to reject stale completions;
- cancellation/termination ownership;
- a non-secret authenticated-context marker.

It does not persist OAuth access or refresh tokens. W7 uses the access token only for immediate ticket issuance and discards the refresh token.

### World directory

The directory contract carries:

- positive signed-64-compatible `WorldId` and `CharacterId`;
- validated host and non-zero TCP port;
- immutable authoritative world and character descriptors;
- client-local `DirectoryRevision` bound to the active account generation;
- explicit selection proving the character references the selected world;
- an opaque reserved `GameplayChannelId` that remains unused/unserialized in W7.

Protocol v1 rejects duplicate IDs, unknown world references, invalid strings/ports, unsupported routing and local route overrides.

### Game entry and session

The game-session contract carries:

- opaque `GameEntryCredential` with redacted formatting, explicit expiry and no ordinary clone/serialization surface;
- a one-shot holder permitting exactly one take/handoff;
- `GameEntryRequest` binding account generation, directory snapshot, selection, Current profile and authoritative route;
- typed phases and `SessionEntered`;
- typed recoverable failures and recommended actions;
- no automatic reconnect after credential handoff.

Wrong-character/profile rejection, uncertain post-write failure or lost success response requires a fresh Gateway login and credential.

## 7. Public application phases

```text
LoggedOut
Authenticating
AwaitingBrowserCallback
ExchangingAuthorizationCode
RequestingGameTicket
RequestingGameEntry
AccountReady
SelectingCharacter
ConnectingGame
AwaitingGameChallenge
AwaitingAdmission
SessionEntered
Disconnecting
RecoverableFailure
FatalFailure
```

Every worker completion carries the originating generation. Obsolete completions are ignored and disposed. Application close cancels the active generation, closes listeners/sockets, joins workers and clears secrets before window/renderer destruction.

## 8. Identity transaction

Required injected capabilities:

- cryptographically secure random bytes;
- monotonic deadline and cancellation;
- system-browser launch;
- IPv4 loopback listener bound to `127.0.0.1:0`;
- bounded HTTPS client with certificate/hostname validation;
- explicit Platform/Gateway URLs, public client ID and callback path.

Required behavior:

1. generate high-entropy state and verifier;
2. derive PKCE S256 challenge using base64url without padding;
3. bind loopback before browser launch and use the actual assigned port;
4. accept one bounded request only on the exact path from loopback;
5. reject missing/duplicate code/state, wrong state/path/peer, OAuth error, oversize, timeout, cancellation and stale generation;
6. exchange the code with the same redirect URI and verifier;
7. use the access token only for ticket issuance and discard the refresh token in W7;
8. clear the ticket after the Gateway request is committed;
9. parse strict Gateway protocol v1 and validate directory relations;
10. return public account/directory state plus one fresh one-shot credential.

Non-loopback Platform/Gateway URLs require HTTPS. Loopback fakes may use HTTP. Sensitive redirects are rejected unless a future exact contract requires them.

## 9. Canary admission transaction

The adapter is pinned to one exact Current-profile revision/build and implements only the messages needed to determine admission.

Required behavior:

1. connect only to the authoritative validated route;
2. apply exact source-proven framing, checksum/sequence, encryption and challenge behavior;
3. generate client cryptographic material using a CSPRNG;
4. submit the opaque credential unchanged in `GameSessionKey` with the selected character;
5. never send an Oteryn password or invented account descriptor;
6. decode bounded challenge, rejection/wait/advice and admission prefix;
7. emit `SessionEntered` only after ordered enter-world `0x0F` for the active generation;
8. stop before map description and disconnect deterministically;
9. clear credential, XTEA/session keys and buffers on every terminal path;
10. never replay a credential after socket handoff.

Initial source evidence includes self-login `0x17`, bug-report/time messages, pending `0x0A`, enter-world `0x0F`, then map description. Exact order/optionality must be pinned by worker evidence.

Official Tibia 15.30 protobuf/BattlEye findings are not this adapter contract. W7 targets project-owned Canary Current profile and its existing `GameSessionKey` path only.

## 10. Failure model

Raw HTTP bodies, server text and parser diagnostics never become authoritative UI copy. Each layer returns stable code, safe message and recommended action.

Minimum actions:

- `RetryAuthentication` before credential issuance;
- `StartFreshGameEntry` when credential expired, consumed, burned or may have reached Canary;
- `SelectCharacterAgain` after directory invalidation;
- `CheckConfiguration` for unsupported URL/client/world/profile configuration;
- `RetryConnection` only when credential handoff provably did not occur;
- `UpdateClient` for unsupported exact profile/build;
- `CloseApplication` for unrecoverable shell/runtime failure.

No error path silently falls back to legacy password authentication.

## 11. Security and privacy invariants

- Passwords never enter the Rust native-auth path.
- OAuth code/verifier/tokens, Game Login Ticket, Game Session credential, XTEA/session keys and sensitive frames never enter logs, diagnostics, titles, panic text, screenshots, fixtures or Git.
- Secret-bearing types do not expose ordinary formatting, cloning or serialization that reveals bytes.
- HTTP and protocol inputs are bounded before allocation.
- Routing is accepted only from the validated Gateway response and explicit expected-world configuration.
- Generation change invalidates callback, HTTP and socket completions.
- One-shot credentials clear on handoff, error, cancellation, timeout and shutdown.
- Local fixtures are synthetic and provenance-documented. Private captures stay outside Git and are reduced to sanitized facts.
- Internal packet work supports only Oteryn/Canary interoperability and is not published as third-party gameplay or anti-cheat tooling.

## 12. Test and evidence matrix

### Automated repository evidence

- contract validation/property tests for IDs, relations, expiry and one-shot consumption;
- API-surface/redaction tests for secret types;
- PKCE known vector and CSPRNG/state uniqueness tests;
- loopback tests for OS-assigned port, path/state/peer, timeout, cancellation, stale and duplicate callback;
- fake Platform/Gateway positive and bounded negative cases;
- synthetic source-derived Canary challenge/login/admission fixtures pinned to an exact revision;
- malformed/truncated/trailing/oversized/wrong-profile/unknown-message tests;
- local TCP E2E: challenge -> login -> admission `0x0F` -> disconnect;
- app composition E2E covering public phases, close/cancel and no replay;
- exact-head Windows build, locked metadata, fmt, strict Clippy, all tests, architecture checks and cargo-deny.

### Interactive or deployment evidence

- real system-browser launch/return on supported Windows;
- firewall/browser behavior for an OS-assigned loopback port;
- exact deployed Platform/Gateway TLS, DNS and certificate state;
- approved server-side secret/private-network state;
- exact-version Rust client -> Gateway -> Canary admission in a project-owned controlled environment;
- clean disconnect and server-side exactly-one entry/replay-rejection evidence.

Repository tests do not prove production deployment state.

## 13. Merge and rollout order

1. merge and separately archive the W7 planning task;
2. merge/archive `W7-ENTRY-CONTRACT` as sole public contract producer;
3. restack consumers on the exact producer merge;
4. merge/archive `W7-IDENTITY` and `W7-CANARY-ENTRY` under serialized shared-path lease;
5. restack/merge/archive `W7-LOGIN-E2E` on exact required merges;
6. close W7 in a separate coordination task and archive it separately.

No manual `Cargo.lock` conflict resolution is allowed.

## 14. Continuation after W7

After technical admission is proven, a separate accepted wave may introduce normalized server events for initial world snapshot, player position, map tiles, creatures and basic statistics against project-owned Canary. W7 creates no map/UI/gameplay contract and does not pre-authorize that work.
