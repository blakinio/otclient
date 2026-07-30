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
-> report typed SessionEntered or typed recoverable failure
-> disconnect and clear every session-scoped secret
```

`SessionEntered` is a technical admission result. W7 does not claim map rendering, gameplay readiness, production rollout or general protocol coverage.

## 2. Explicit exclusions

W7 does not implement:

- map, tile, creature, item, container, inventory, chat, combat or movement decoding;
- production asset packs or asset runtime mounting;
- a general native UI framework or final login presentation;
- multi-world issuer discovery, gameplay-channel switching or horizontal issuer replicas;
- updater, launcher, signing or deployment activation;
- legacy password fallback for an Oteryn Identity profile;
- official Tibia service automation, gameplay manipulation or anti-cheat evasion;
- BattlEye patching, disabling, hooking, impersonation, emulation or bypass;
- publication of private captures, credentials, proprietary artifacts or reusable abuse tooling.

Protocol research is permitted only as internal compatibility work for the project-owned Oteryn/Canary stack. Prefer Canary source, project-owned instances, local mocks and synthetic fixtures.

## 3. Exact producer evidence

The planning evidence cut must be revalidated by every implementation lane before compatibility is claimed.

### Oteryn Identity and Platform

- Native public OAuth Authorization Code + PKCE producer: Oteryn Platform PR #119, merge `27fa277c5def0e151d7ee013acef188dbfd6f463`.
- Registered redirect base: `http://127.0.0.1/callback`.
- Current producer tests prove a dynamic loopback port such as `http://127.0.0.1:49152/callback` is accepted for authorization and token exchange while a wrong path or non-loopback redirect fails closed.
- Initial scope: `game:ticket`.
- Game Login Ticket issue/redeem producer: Oteryn Platform PR #121, merge `cab00c140ce200e3cd51b7eafe2c1659842c2b90`.
- Public ticket issue endpoint: `POST /api/v1/game-auth/tickets`, protected by the OAuth bearer and `game:ticket` scope.

The registered no-port URI and the dynamic request port are not a conflict. The producer intentionally registers the loopback base while Passport validates an otherwise matching dynamic loopback port. The Rust client must still bind `127.0.0.1:0`, use the actual OS-assigned port in both authorization and token requests, and validate the exact callback path and state.

### Game Gateway

- Gateway protocol-v1 producer: Oteryn Platform PR #122, merge `8006534108d835474dadd208b0ec934e4a12528b`.
- Hardened Platform boundary: PR #124, merge recorded by current Canary contract evidence as `53158217a6c6017230301cf4daa783b04fcc13d5`.
- Client endpoint: `POST /v1/login`.
- Strict request JSON:

```json
{
  "protocol_version": 1,
  "game_login_ticket": "<opaque-one-time-ticket>"
}
```

- Unknown fields, trailing JSON, missing ticket, ticket longer than 1024 bytes or protocol version other than `1` fail closed.
- Success JSON contains `protocol_version`, `session`, authoritative `worlds` and account-scoped `characters`.
- `session` contains `credential` and `expires_at`.
- A world contains positive `id`, `slug`, `name`, `region`, `host` and `port`.
- A character contains positive `id`, `name`, `level`, `vocation` and `world_id`.
- Current error classes are `invalid_request`, `invalid_login` and `login_unavailable` with bounded HTTP status semantics.
- Sensitive responses are `no-store` / `no-cache`.

### Canary

- Game Session issuer producer: Canary PR #722, merge `b8a88f073b2609b444fa15370aae30ac9f80b908`.
- Gateway-to-Canary credential rotation: Canary PR #807, merge `981c82f5ebb6bc22c867312c2b274a71f6aeeb3e`.
- Current planning source cut: Canary `4b2d6f432d92628c42bde1d95daed6ae0d0eb88f`; the implementation worker must pin the exact current revision and build/profile evidence again.
- Supported initial profile: `ProtocolProfileId::Current`.
- The opaque Game Session credential is stored process-locally as a SHA-256 representation, expires after 60 seconds and is consumed atomically once.
- Wrong character or profile burns a matching credential.
- Process restart invalidates unconsumed credentials.
- Existing `ProtocolGame` and `IOLoginData` ownership, deletion, ban and runtime admission checks remain authoritative.
- Protocol v1 supports one Platform world mapped to one exact Canary issuer process. Platform `world_id` is not Canary gameplay-channel ID.
- The game wire remains the existing Current-profile `GameSessionKey` world-login path; the Gateway contract introduces no new game opcode.

### Maintained legacy consumer evidence

Legacy OTClient PR #17, merge `bb87346f6c516a19d19497d82bb01fb389334ff5`, is read-only behavioral evidence for:

- system-browser OAuth with PKCE and OS-assigned loopback port;
- ticket issue followed by Gateway `/v1/login`;
- authoritative world/character validation;
- opaque credential handoff through `GameSessionKey`;
- no Oteryn password fallback;
- clearing the credential after the real world-login handoff and refusing automatic replay.

The legacy client is never a Rust runtime dependency.

## 4. Runtime ownership

W7 introduces or completes these bounded owners.

| Owner | Category | Responsibility | Must not own |
|---|---|---|---|
| `oteryn-account-session` | `account-session` | Account-auth generation, authenticated account-context lifetime and cancellation ownership without bearer storage | HTTP, browser, world routing, game wire |
| `oteryn-world-directory` | `world-directory` | Validated server-authoritative worlds/characters and explicit selection | OAuth, sockets, game credential storage |
| `oteryn-game-session` | `game-session` | One-shot credential lifetime, selected entry request, admission result and disconnect lifecycle | OAuth, JSON, TCP framing, Canary byte layout |
| `oteryn-identity` | `identity` | Blocking, injected Authorization Code + PKCE transaction; token exchange; ticket issue; Gateway-v1 consumption | UI, game wire, renderer, persistent passwords/tokens |
| `oteryn-protocol-core` | `protocol-core` | Bounded wire primitives, frame/parser contracts and protocol-neutral errors | socket ownership, Canary domain mapping |
| `oteryn-transport` | `transport` | Bounded TCP connection/read/write/framing lifetime and cancellation | account policy, character selection, raw UI events |
| `oteryn-protocol-canary` | `protocol-canary` | Exact Current-profile challenge/world-login/admission mapping | Identity HTTP, game domain beyond admission, official-service bypass logic |
| `apps/client` | `app` | Compose the existing shell/renderer with the merged services and expose public phases/results | duplicate contracts, raw backend payloads, secret persistence |

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
  <- oteryn-identity

oteryn-foundation + oteryn-protocol-core
  <- oteryn-transport

oteryn-world-directory + oteryn-game-session + oteryn-protocol-core + oteryn-transport
  <- oteryn-protocol-canary
all merged W7 services + existing shell/renderer/diagnostics
  <- apps/client
```

No lower crate depends on `apps/client`, renderer, UI, a legacy runtime path or a producer repository.

## 6. Public contract model

Exact names may be refined only by the sole contract producer, but consumers must not create substitutes.

### Account session

The account-session contract carries:

- a process-local session generation derived from the existing foundation generation primitives;
- public lifecycle state required to reject stale completions;
- cancellation/termination ownership;
- a non-secret authenticated-context marker.

It does not persist an OAuth access token or refresh token. W7 consumes the access token only for immediate Game Login Ticket issuance, then clears it. A future durable account session requires a separate credential-store contract.

### World directory

The directory contract carries strongly validated:

- `WorldId` and `CharacterId` with positive integer semantics;
- `WorldRoute` containing one validated host and non-zero TCP port;
- `WorldDescriptor` containing id, slug, name, region and route;
- `CharacterDescriptor` containing id, name, level, vocation and world id;
- immutable `DirectorySnapshot` bound to the active account-session generation;
- explicit `CharacterSelection` that proves the character references the selected authoritative world.

Protocol v1 rejects duplicate IDs, unknown world references, empty/bounded-string violations, invalid ports, unsupported additional selected issuers and any local route override.

### Game entry and game session

The game-session contract carries:

- an opaque `GameEntryCredential` with redacted `Debug`/`Display`, explicit expiry and no cloning or serialization surface;
- a pending one-shot holder that permits exactly one credential take/handoff;
- `GameEntryRequest` binding account generation, directory snapshot, character selection, Current profile and authoritative route;
- public session phases from `Connecting` through `SessionEntered`, `Disconnecting` and `Ended`;
- typed recoverable failures and recommended actions;
- no automatic reconnect after a credential was handed off or consumed.

A wrong-character/profile rejection, uncertain post-write transport failure or lost success response requires a fresh Gateway login and a new credential.

## 7. Public application phases

The composition owner exposes stable, non-secret phases:

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

Every asynchronous or worker-thread completion carries the originating generation. A completion from an obsolete generation is ignored and safely disposed. Closing the application cancels the active generation, closes listeners/sockets, joins owned threads and clears secrets before renderer/window destruction.

## 8. Identity transaction

`oteryn-identity` provides a blocking transaction driven by injected ports so deterministic tests do not require a browser or external service.

Required ports/capabilities:

- cryptographically secure random bytes;
- monotonic deadline/cancellation;
- system-browser launch;
- IPv4 loopback callback listener bound to `127.0.0.1:0`;
- bounded HTTPS client with normal certificate and hostname validation;
- configuration containing exact Platform/Gateway base URLs, public client ID and callback path.

Required behavior:

1. generate a high-entropy state and PKCE verifier;
2. derive S256 challenge with base64url without padding;
3. bind loopback before browser launch and use its actual port;
4. accept one bounded HTTP request only on the exact callback path;
5. reject missing/duplicate code/state, wrong state, OAuth error, wrong path, non-loopback peer, oversized input, timeout, cancellation and stale generation;
6. exchange code with the same redirect URI and verifier;
7. accept only bounded expected token fields, use the access token only for ticket issuance and discard the refresh token in W7;
8. issue one Game Login Ticket, remove the bearer immediately after the request completes and clear the ticket after the Gateway request is committed;
9. consume strict Gateway protocol v1 and validate all directory relations;
10. return public account/directory state plus one fresh one-shot Game Entry credential.

Non-loopback Platform/Gateway URLs require HTTPS. Loopback fakes may use HTTP. Redirects on sensitive API calls are rejected unless an exact producer contract later proves a safe requirement.

## 9. Canary admission transaction

The Canary adapter is pinned to one exact Current-profile producer revision and build string. It implements only the minimum messages needed to determine admission.

Required behavior:

1. connect only to the validated Gateway-authoritative host/port;
2. apply exact Current-profile transport framing, checksum/sequence, encryption and challenge behavior proven from pinned Canary source and sanitized synthetic fixtures;
3. generate any client-side cryptographic material through a CSPRNG;
4. submit the opaque Game Session credential unchanged in the existing `GameSessionKey` world-login field with the selected character;
5. never send an Oteryn password, authenticator or locally invented account descriptor;
6. decode bounded login challenge, explicit login rejection/wait/advice and the minimum success/admission message required to emit `SessionEntered`;
7. stop before map/gameplay decoding;
8. disconnect deterministically and clear session-scoped key material;
9. treat malformed, truncated, oversized, wrong-profile, unexpected and unknown-required messages as typed fail-closed errors;
10. never replay a credential after it was handed to the socket path.

Official Tibia 15.30 protobuf/BattlEye findings are not this adapter contract. W7 targets the project-owned Canary Current profile and existing GameSessionKey path only.

## 10. Failure model

Raw server text, HTTP bodies and parser diagnostics never become authoritative UI copy. Each layer returns stable code, reviewed safe message and recommended action.

Minimum actions:

- `RetryAuthentication` — before a Game Entry credential is issued;
- `StartFreshGameEntry` — credential expired, consumed, burned or may have reached Canary;
- `SelectCharacterAgain` — selection invalidated by a new directory snapshot;
- `CheckConfiguration` — unsupported base URL, client ID, world mapping or profile;
- `RetryConnection` — only when the credential has provably not been handed off;
- `UpdateClient` — exact producer profile/build is unsupported;
- `CloseApplication` — unrecoverable shell/runtime failure.

No error path silently falls back to legacy password authentication.

## 11. Security and privacy invariants

- Passwords never enter the Rust native-auth path.
- OAuth code, verifier, access token, refresh token, Game Login Ticket, Game Session credential, XTEA/session keys and raw sensitive frames never enter logs, diagnostics, window title, panic text, screenshots, task records, fixtures or Git.
- Secret-bearing types do not derive or expose ordinary `Clone`, `Debug`, `Display`, serialization or equality that reveals bytes.
- HTTP and protocol inputs are bounded before allocation.
- Host/port/world/character routing is accepted only from the validated Gateway response.
- A generation change invalidates callback, HTTP and socket completions.
- One-shot credentials are cleared on handoff, error, cancellation, timeout and shutdown.
- Local fixtures are synthetic and provenance-documented. Private captures remain outside Git and are reduced to sanitized facts before use.
- Internal packet work supports only Oteryn/Canary interoperability and is not packaged or published as third-party gameplay manipulation or anti-cheat tooling.

## 12. Test and evidence matrix

### Automated repository evidence

- contract constructor/validation tests for IDs, directory relations, expiry and one-shot consume;
- compile-time or API-surface tests proving secret values cannot be formatted/serialized through ordinary paths;
- PKCE known vector plus CSPRNG/state uniqueness tests;
- loopback tests for OS-assigned port, exact path/state, timeout, cancellation, stale callback and one active flow;
- fake Platform/Gateway positive and bounded negative HTTP cases;
- synthetic Canary golden login/challenge/admission fixtures pinned to exact source revision;
- malformed/truncated/trailing/oversized/wrong-profile/unknown-message tests;
- local TCP E2E: challenge -> login -> admission -> disconnect;
- application composition E2E covering public phases, close/cancel and no credential replay;
- Windows workspace metadata/fmt/Clippy/tests/architecture checks and cargo-deny on exact head.

### Interactive or deployment evidence

These remain explicit until genuinely observed:

- real system-browser launch and return on supported Windows versions;
- firewall/browser behavior for an OS-assigned loopback port;
- exact deployed Platform/Gateway TLS, DNS and certificate validation;
- approved secret-manager and private-network state on server-side dependencies;
- exact-version Rust client -> Gateway -> Canary admission in a project-owned controlled environment;
- clean disconnect and server-side exactly-one entry/replay rejection metrics.

Repository tests do not prove production deployment state.

## 13. Merge and rollout order

1. Merge and separately archive the W7 planning task.
2. Merge and archive `W7-ENTRY-CONTRACT` as the sole public lifecycle/selection/credential producer.
3. Restack consumers on the exact producer merge.
4. Merge and archive `W7-IDENTITY`.
5. Merge and archive `W7-CANARY-ENTRY`.
6. Restack and merge `W7-LOGIN-E2E` on all exact producer/consumer merges.
7. Close W7 in a separate coordination task.

Identity and Canary-entry workers may prepare isolated private implementation after the entry producer merges, but only one lane holds the Cargo/lockfile/shared-document lease at a time. No manual `Cargo.lock` conflict resolution is allowed.

## 14. Continuation after W7

After technical admission is proven, a separate accepted wave may introduce normalized server events for initial world snapshot, player position, map tiles, creatures and basic statistics against project-owned Canary. W7 creates no map/UI/gameplay contract and does not pre-authorize that work.
