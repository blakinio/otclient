# Current Parallel Agent Wave

Status: accepted launch plan after this plan and its separate task archive merge  
Wave ID: `OTERYN-W7-TECHNICAL-LOGIN`  
Evidence cut: `main` `1922ef0201cd476cad2fabd42e6f9622e52891f6`  
External source cut: Oteryn Platform/Gateway `8e613c00503c0874e69e2085c740f87f4a87e002`; Canary `4b2d6f432d92628c42bde1d95daed6ae0d0eb88f`

Live Git, active tasks, open PRs, reviews and exact checks remain authoritative. This plan authorizes no worker task, branch, PR or shared-path lease until the planning PR and its separate lifecycle archive merge and a fresh overlap check passes.

## 1. Objective and first milestone

Produce the first compilable Rust Oteryn client slice capable of one bounded technical Oteryn Identity -> Gateway -> one exact Canary issuer login flow:

1. compile the Windows executable on pinned Rust `1.94.0` for `x86_64-pc-windows-msvc`;
2. open the existing Rust application window and renderer;
3. report `LoggedOut`;
4. start Authorization Code + PKCE `S256` through the system browser;
5. bind `127.0.0.1:0`, use the actual OS-assigned callback port and validate one callback;
6. exchange the authorization code and issue one fresh Game Login Ticket;
7. exchange the ticket through Gateway protocol v1;
8. validate the authoritative world/character directory and explicitly select one character belonging to one configured world;
9. move one opaque one-shot Game Session credential into the Canary admission boundary;
10. complete the exact Current-profile challenge/login/admission prefix for the configured issuer;
11. report typed `SessionEntered` or typed recoverable `EntryFailure`;
12. disconnect safely and clear every session-scoped credential and replayable state.

The milestone excludes map rendering, map/world decoding after the admission marker, inventory, chat, combat, general-purpose native UI, channel switching, production assets, launcher/updater work, multi-world issuer routing and production-deployment readiness.

All packet/protocol work is internal Oteryn/Canary interoperability work. It must not be published or packaged as third-party gameplay manipulation, unauthorized-access or anti-cheat tooling.

## 2. Live-state reconciliation

- PR #93 merged and its task archive merged through PR #95.
- W6 implementation PR #92/archive #94, closure PR #98 and closure archive PR #100 are merged; W1-W6 are completed and cannot be relaunched.
- PR #23 remains legacy OTUI/Lua presentation only and owns no Rust login path.
- PR #48 remains isolated operational non-merge work.
- PR #97 owns only one legacy-client asset rehearsal workflow and task; it owns no W7 Rust path or shared W7 integration document.
- No active Rust task or other open PR owns Identity, account session, world directory, game session, transport, `protocol-core`, `protocol-canary`, application-runtime login composition or login E2E paths.
- Every previous Cargo workspace, `Cargo.lock`, dependency-policy and shared-document lease is released.
- The architecture checker already recognizes `identity`, `account-session`, `world-directory`, `game-session`, `transport`, `protocol-core`, `protocol-canary`, `platform`, runtime and app categories. W7 does not pre-authorize checker-rule changes.

## 3. Exact producer evidence

Implementation workers must revalidate every revision before a compatibility claim.

### Platform and Identity

- Native OAuth Authorization Code + PKCE producer: Platform PR #119, merge `27fa277c5def0e151d7ee013acef188dbfd6f463`.
- Game Login Ticket producer: Platform PR #121, merge `cab00c140ce200e3cd51b7eafe2c1659842c2b90`.
- The registered public-client redirect base is `http://127.0.0.1/callback`.
- Current producer tests explicitly prove authorization and token exchange with a matching dynamic loopback port such as `http://127.0.0.1:49152/callback` and reject a wrong callback path or non-loopback redirect.
- The Rust client therefore binds `127.0.0.1:0`; fixed port 80 is prohibited.
- Initial OAuth scope is `game:ticket`.
- Current ticket issuance revokes the associated access/refresh token family; W7 claims one bounded bootstrap attempt, not a reusable account session for relog/channel switching.

### Game Gateway

- Protocol-v1 producer: Platform PR #122, merge `8006534108d835474dadd208b0ec934e4a12528b`.
- Current hardening evidence includes Platform merge `53158217a6c6017230301cf4daa783b04fcc13d5`.
- Client endpoint: `POST /v1/login`.
- Request: strict `{"protocol_version":1,"game_login_ticket":"..."}`.
- Success: `protocol_version`, `session { credential, expires_at }`, `worlds[] { id, slug, name, region, host, port }`, `characters[] { id, name, level, vocation, world_id }`.
- Protocol v1 contains no directory revision, gameplay-channel ID, issuer directory or general multi-world routing contract.
- Unknown/trailing/oversized input and unsupported protocol version fail closed; sensitive responses are no-store/no-cache.

### Canary

- Game Session producer: Canary PR #722, merge `b8a88f073b2609b444fa15370aae30ac9f80b908`.
- Service-credential rotation: Canary PR #807, merge `981c82f5ebb6bc22c867312c2b274a71f6aeeb3e`.
- Initial planning cut: Canary `4b2d6f432d92628c42bde1d95daed6ae0d0eb88f`; worker must pin current revision, release/build and exact source paths again.
- Initial supported profile: `ProtocolProfileId::Current`.
- Game Session credential is opaque, process-local, 60-second, hashed at rest and atomically single-use; wrong character/profile can burn it and process restart invalidates it.
- Protocol v1 maps one Platform world to one exact issuer process. Platform `world_id` is not a Canary gameplay-channel ID.
- The game wire remains the existing Current-profile `GameSessionKey` path; no new game opcode is introduced.

Legacy OTClient PR #17 / merge `bb87346f6c516a19d19497d82bb01fb389334ff5` is read-only behavioral evidence only and is never a Rust runtime dependency or Rust compatibility proof.

## 4. Topology and dependency graph

```text
1 coordinator: W7-C
4 workers maximum

W7-ENTRY-CONTRACT
        |
        +-----------------> W7-IDENTITY
        |
        +-----------------> W7-CANARY-ENTRY
        |
        +-----------------> W7-LOGIN-E2E private fake harness
                                  ^
                                  |
                     merged W7-IDENTITY + W7-CANARY-ENTRY
                                  |
                                  +--> final app composition
```

Rules:

- `W7-ENTRY-CONTRACT` merges and archives first.
- `W7-IDENTITY` and `W7-CANARY-ENTRY` restack on the exact ENTRY merge. Their shared-path integration is serialized by coordinator lease.
- `W7-LOGIN-E2E` may prepare only private fake-service work after ENTRY merges. Final composition waits for both required consumers.
- Missing deployment evidence blocks only the affected real-path claim; it does not authorize substitute public contracts or a security downgrade.

## 5. W7-C coordinator

Prompt: `prompts/COORDINATOR_AGENT.md`

Responsibilities:

- repeat current-main, active-task, open-PR, review and exact-CI reconciliation before each launch and merge;
- create no worker implementation while coordinating;
- enforce one task/branch/worktree/draft PR per lane;
- enforce one producer per public contract and reject substitute types;
- grant at most one shared-path lease at a time;
- order merges/restacks and prohibit manual `Cargo.lock` conflict resolution;
- preserve exact external revision evidence and all blocked claims;
- require a separate archive PR for every merged worker;
- create a separate W7 closure PR and separate closure archive PR;
- record exactly one bounded next recommendation without implementing it.

## 6. Lane W7-ENTRY-CONTRACT

Prompt: `prompts/W7_ENTRY_CONTRACT_AGENT.md`  
Contract role: sole producer  
Initial state after plan archive: launchable

Exclusive owned paths:

```text
oteryn-client/crates/account-session/**
oteryn-client/crates/world-directory/**
oteryn-client/crates/game-session/**
oteryn-client/docs/research/technical-login/W7_ENTRY_CONTRACT_EVIDENCE.md
```

Only this lane produces:

- `AccountSessionId`;
- `CharacterId`;
- `WorldId`;
- `GameplayChannelId`;
- `DirectoryRevision`;
- `GameEntryRequest`;
- `GameEntryCredential`;
- `EntryFailure`;
- entry lifecycle states;
- `SessionEntered`.

Required semantics:

- `AccountSessionId` is client-local opaque generation/correlation identity, not an external account ID or bearer.
- `CharacterId` and `WorldId` preserve Gateway signed 64-bit JSON identifiers and reject invalid narrowing.
- `DirectoryRevision` is a client-local validated-response generation because Gateway v1 exposes no server revision.
- `GameplayChannelId` is reserved but unpopulated/unserialized in W7.
- `GameEntryCredential` owns secret bytes, is non-`Clone`, redacts formatting, cannot be serialized/persisted and supports one move into admission.
- `EntryFailure` is closed, typed, stable and contains no raw backend/OS text or secret.
- stale generations, invalid world/character relationships, duplicate handoff, terminal reuse and disconnect cleanup are deterministic.

This lane produces no raw Platform/Gateway DTO, HTTP boundary, transport trait or Canary opcode.

## 7. Lane W7-IDENTITY

Prompt: `prompts/W7_IDENTITY_AGENT.md`  
Contract role: consumer  
Initial state after ENTRY merge: launchable

Exclusive owned paths:

```text
oteryn-client/crates/platform/**
oteryn-client/crates/identity/**
oteryn-client/docs/research/technical-login/W7_IDENTITY_EVIDENCE.md
```

Consumes without substitutes:

- merged W7-ENTRY-CONTRACT types;
- exact current Platform native OAuth/ticket producer;
- exact Gateway protocol-v1 request/response/error/cache contract.

Required scope:

- PKCE `S256`, cryptographically secure state/verifier and injected system-browser launch;
- bind IPv4 `127.0.0.1:0` before launch and use the actual port in authorization and token requests;
- exact callback path, loopback peer, state, active-generation, stale and duplicate validation;
- bounded token exchange, Game Login Ticket issue and strict Gateway `/v1/login`;
- validation of IDs, ports, duplicate relations and `Character.world_id` membership;
- conversion only into ENTRY domain types;
- clearing verifier/code/access/refresh/ticket secrets at exact terminal boundaries;
- no password collection, no password fallback and no duplicated one-shot issuance retry.

No directory revision, gameplay-channel ID, issuer directory or multi-world routing is inferred from Gateway v1.

## 8. Lane W7-CANARY-ENTRY

Prompt: `prompts/W7_CANARY_ENTRY_AGENT.md`  
Contract role: consumer plus sole initial transport/protocol-admission interface producer  
Initial state after ENTRY merge: launchable

Exclusive owned paths:

```text
oteryn-client/crates/transport/**
oteryn-client/crates/protocol-core/**
oteryn-client/crates/protocol-canary/**
oteryn-client/contracts/canary/current-entry/**
oteryn-client/docs/research/technical-login/W7_CANARY_ENTRY_EVIDENCE.md
```

Consumes without substitutes:

- merged W7-ENTRY request/credential/result types;
- exact pinned Canary Current-profile source;
- validated authoritative host/port, selected character and one moved credential.

Sole produced interface:

- one bounded transport connection/admission interface for W7;
- exact Current-profile challenge/login encoder and bounded admission-prefix decoder;
- no general gameplay protocol/domain enum.

Initial source evidence to revalidate:

- release `3.6.1`, protocol/client `1525`, Current profile and OpenTibia RSA;
- server challenge before login;
- modern framing/padding, sequence checksum after login and bounded compression signaling;
- login layout: OS `u16`, protocol `u16`, client version `u32`, version string, asset-hash string, preview byte, RSA block with XTEA key/GM/session key/character/challenge and optional OTCv8 probe;
- one-shot session key consumed against character and Current profile;
- successful placement emits self-login `0x17`, pre-world messages including `0x1A` and time, pending-state `0x0A`, then enter-world `0x0F`; map description follows.

`SessionEntered` is emitted only after ordered validated `0x0F`. The lane stops before map-description decoding and disconnects cleanly.

## 9. Lane W7-LOGIN-E2E

Prompt: `prompts/W7_LOGIN_E2E_AGENT.md`  
Contract role: final consumer/composition owner  
Initial state after ENTRY merge: private fake harness only; final integration waits for required merges

Exclusive paths before final integration:

```text
oteryn-client/crates/app-runtime/**
oteryn-client/tests/integration/technical-login/**
oteryn-client/docs/research/technical-login/W7_LOGIN_E2E_EVIDENCE.md
```

Final integration lease additionally owns:

```text
oteryn-client/apps/client/**
```

Required composition:

- preserve existing `winit` window, renderer and close lifecycle;
- keep browser/listener/HTTP/TCP work off the event-loop thread in cancellable joined workers;
- deliver typed progress/result events with generation checks;
- expose one explicit technical configuration surface with no hidden production defaults or credentials;
- report `SessionEntered` or typed recoverable `EntryFailure` without a general native UI framework;
- clear every callback/OAuth/ticket/credential/transport secret on close, failure and disconnect.

Fake-service E2E proves dynamic-port callback, stale/duplicate/mismatch rejection, strict Gateway parsing, world-character validation, one credential handoff, fresh second attempt, ordered Canary admission through `0x0F`, terminal cleanup and secret redaction.

## 10. Shared-path lease

Only one active task may hold this lease set at a time:

```text
oteryn-client/Cargo.toml
oteryn-client/Cargo.lock
oteryn-client/deny.toml
docs/agents/MODULE_CATALOG.md
docs/agents/BUILD_TEST_MATRIX.md
docs/agents/CHANGELOG.md
oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
oteryn-client/docs/operations/RUST_WORKSPACE.md
oteryn-client/apps/client/** when final composition begins
```

Lease protocol:

1. coordinator records holder and exact base/head in the active task and PR;
2. non-holder workers keep shared paths read-only and work only in exclusive paths;
3. exclusive work may reach `integration_ready` while waiting;
4. holder integrates generated Cargo metadata/lockfile/shared docs, validates exact head, merges and archives;
5. next worker restacks on current `main`, regenerates resolution and claims the released lease;
6. manual `Cargo.lock` conflict resolution, copied lockfile fragments and concurrent shared-document edits are prohibited.

Recommended lease/merge order:

1. `W7-ENTRY-CONTRACT`;
2. `W7-IDENTITY` and `W7-CANARY-ENTRY`, serialized and restacked;
3. `W7-LOGIN-E2E`;
4. separate archive PR after every worker;
5. separate W7 closure PR;
6. separate W7 closure archive PR.

## 11. Evidence matrix

| Requirement | Automated evidence | Interactive/external evidence |
|---|---|---|
| workspace/executable | locked metadata, Windows target build, fmt, strict Clippy, tests, architecture check, cargo-deny, repository CI | launch exact Windows executable and observe existing window |
| entry contract | lifecycle/generation/property tests; invalid relationship/replay tests; secret formatting barriers | none required |
| Identity | PKCE vector; fake browser/listener/HTTP; OS-assigned loopback port; stale/duplicate/path/peer/state rejection; strict JSON and cleanup | real browser launch/return against named exact Platform revision when configured |
| Gateway | bounded fake server proves protocol-v1 request/response/error/cache contract and one-shot handoff | named deployed Gateway revision/TLS/configuration or explicit blocker |
| Canary admission | source-derived synthetic challenge/login/admission fixtures; malformed/timeout/replay/crypto/framing tests | named exact Canary revision/build/issuer and one controlled Rust admission/disconnect, or explicit blocker |
| full flow | fake executable E2E proves one success plus required rejection/cleanup cases | named exact Identity -> Gateway -> Canary path or explicit blocker |
| production readiness | repository tests prove code properties only | TLS, DNS, firewall, secret manager, issuer mapping and deployed revisions remain external/out of scope |

## 12. Explicit blocked items

### `W7-BLOCK-REAL-RUST-E2E`

No Rust consumer has yet completed the real path. Repository/fake tests and legacy OTClient evidence cannot satisfy this. Final real-path acceptance requires named exact Identity, Gateway and Canary revisions plus controlled evidence; otherwise the real path remains blocked without a compatibility claim.

### `W7-BLOCK-DEPLOYMENT-EVIDENCE`

Repository access does not prove deployed TLS, hostname validation, firewall reachability, OAuth client configuration, runtime issuer mapping, secret injection or revision identity. No production claim.

### `W7-BLOCK-MULTIWORLD-CHANNEL`

Gateway v1 has no general gameplay-channel or multi-issuer directory/routing contract. `GameplayChannelId` remains unused; one exact configured world/issuer only.

### `W7-BLOCK-ACCOUNT-SESSION-REUSE`

Current ticket issuance revokes the native access/refresh token family. W7 cannot claim reusable account-session relog/channel switching.

### `W7-BLOCK-EXACT-CANARY-CUT`

The implementation worker must re-pin exact current Canary revision, release/build/profile source and sanitized fixture provenance before a compatibility claim. The planning cut is evidence for design, not permanent support policy.

## 13. Exact acceptance criteria

The W7 implementation wave succeeds only when:

- every lane has unique task, branch/worktree and draft/ready/merge/archive history;
- no overlapping public producer or shared-path lease exists;
- `W7-ENTRY-CONTRACT` is the sole producer of all named entry/shared identity types;
- `W7-CANARY-ENTRY` is the sole initial transport/protocol-admission interface producer;
- final executable compiles on pinned Rust `1.94.0` for Windows and opens the existing window;
- exact-head locked metadata, formatting, strict Clippy, all tests, architecture checks, cargo-deny and repository required CI pass;
- fake-service E2E proves dynamic callback, stale/duplicate rejection, one-shot credential handling, fresh-second-attempt behavior, terminal cleanup and secret redaction;
- explicit configuration selects one world/issuer and one matching character;
- one moved Game Session credential is never logged, cloned, persisted or replayed;
- Current-profile source-derived admission reaches ordered self-login -> pending `0x0A` -> enter-world `0x0F` semantics without map decoding;
- app reports typed `SessionEntered` or typed recoverable `EntryFailure`, disconnects and clears session-scoped credentials;
- exact named real Rust evidence proves the configured path, or the real path remains explicitly blocked without a compatibility/production claim;
- no unresolved review threads, ownership conflicts, stale bases or unarchived merged tasks remain;
- a separate W7 closure records exactly one next bounded recommendation and implements none of it.
