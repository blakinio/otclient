# Current Parallel Agent Wave

Status: accepted launch plan after this plan and its separate task archive merge  
Wave ID: `OTERYN-W7-TECHNICAL-LOGIN`  
Evidence cut: `main` `1922ef0201cd476cad2fabd42e6f9622e52891f6`  
External source cut: Oteryn Platform/Gateway `8e613c00503c0874e69e2085c740f87f4a87e002`; Canary `4b2d6f432d92628c42bde1d95daed6ae0d0eb88f`

Live Git, active tasks, open PRs, reviews and exact checks remain authoritative. This plan authorizes no worker task, branch, PR or shared-path lease until the planning PR and its separate lifecycle archive merge and a fresh overlap check passes.

## 1. Objective and first milestone

Produce the first compilable Rust Oteryn client slice capable of a bounded technical Oteryn Identity -> Gateway -> one exact Canary issuer login flow:

1. compile the Windows executable on pinned Rust `1.94.0` for `x86_64-pc-windows-msvc`;
2. open the existing Rust application window;
3. start Authorization Code + PKCE `S256` through the system browser;
4. validate one callback and establish one client-side account-session generation;
5. obtain one fresh Game Login Ticket and exchange it through Gateway protocol v1;
6. validate one directory response and explicitly select one configured world plus one character belonging to it;
7. move one opaque one-shot Game Session credential into the Canary admission boundary;
8. complete the exact Current-profile challenge/login/admission preamble for the configured issuer;
9. report typed `SessionEntered` or typed recoverable `EntryFailure`;
10. disconnect safely and clear every session-scoped credential and replayable state.

The milestone excludes map rendering, map/world decoding after the admission marker, inventory, chat, combat, general-purpose native UI, channel switching, production assets, launcher/updater work, multi-world issuer routing and production-deployment readiness.

## 2. Live-state reconciliation

- PR #93 merged and its task archive merged through PR #95.
- W6 implementation PR #92/archive #94, closure PR #98 and closure archive PR #100 are merged; W1-W6 are completed and cannot be relaunched.
- PR #23 remains legacy OTUI/Lua presentation only and owns no Rust login path.
- PR #48 remains isolated operational non-merge work.
- PR #97 owns only `.github/workflows/client-assets-real-release-rehearsal.yml` and its legacy-client task; it owns no W7 Rust path or shared W7 integration document.
- No active Rust task or other open PR owns Identity, account session, world directory, game session, transport, `protocol-core`, `protocol-canary`, application-runtime login composition or login E2E paths.
- Every previous Cargo workspace, `Cargo.lock`, dependency-policy and shared-document lease is released.
- The architecture checker already recognizes `identity`, `account-session`, `world-directory`, `game-session`, `transport`, `protocol-core`, `protocol-canary`, `platform`, runtime and app categories. W7 does not pre-authorize checker-rule changes.

## 3. Topology and dependency graph

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

- `W7-ENTRY-CONTRACT` merges first.
- `W7-IDENTITY` and `W7-CANARY-ENTRY` may prepare private worktrees only after ENTRY merges; their shared-path integration is serialized by coordinator lease.
- `W7-LOGIN-E2E` may build only private fake-service adapters after ENTRY merges. It cannot finalize public composition or claim compatibility until required producer commits merge.
- A blocked real adapter does not authorize a substitute public contract. Unaffected deterministic/fake work may continue.

## 4. W7-C coordinator

Prompt: `prompts/COORDINATOR_AGENT.md`

Responsibilities:

- repeat current-main, active-task, open-PR, review and exact-CI reconciliation before each launch/merge;
- create no worker implementation while coordinating;
- enforce one task/branch/worktree/draft PR per lane;
- enforce one producer per public contract and reject substitute types;
- grant at most one shared-path lease at a time;
- order merges/restacks and prohibit manual `Cargo.lock` conflict resolution;
- preserve exact external revision evidence and all blocked claims;
- require separate archive PR for every merged worker;
- create a separate W7 closure PR, then a separate closure archive PR;
- record exactly one bounded next recommendation without implementing it.

## 5. Lane W7-ENTRY-CONTRACT

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

- `AccountSessionId`
- `CharacterId`
- `WorldId`
- `GameplayChannelId`
- `DirectoryRevision`
- `GameEntryRequest`
- `GameEntryCredential`
- `EntryFailure`
- entry lifecycle states
- `SessionEntered`

Required contract semantics:

- `AccountSessionId` is a client-local opaque generation/correlation identity, not an Oteryn identity ID, Canary account ID or bearer token.
- `CharacterId` and `WorldId` preserve the current Gateway JSON integer width and reject invalid narrowing.
- `DirectoryRevision` is a client-local monotonic validated-response generation; current Gateway protocol v1 exposes no server directory revision.
- `GameplayChannelId` is an opaque shared type reserved by architecture but remains unpopulated and unserialized in this one-exact-issuer milestone.
- `GameEntryCredential` owns secret bytes, is non-`Clone`, redacts `Debug`/`Display`, supports one move into admission and clears on terminal paths.
- `EntryFailure` is closed, typed, stable, recoverable where appropriate and contains no raw backend/OS text or secret.
- stale generations, duplicate callbacks, duplicate credential handoff, invalid world/character relationships, terminal reuse and disconnect cleanup are deterministic state transitions.

No Platform/Gateway/Canary raw DTO or protocol opcode is produced by this lane.

## 6. Lane W7-IDENTITY

Prompt: `prompts/W7_IDENTITY_AGENT.md`  
Contract role: consumer  
Initial state after ENTRY merge: deterministic/fake portion launchable; real callback adapter externally blocked

Exclusive owned paths:

```text
oteryn-client/crates/platform/**
oteryn-client/crates/identity/**
oteryn-client/docs/research/technical-login/W7_IDENTITY_EVIDENCE.md
```

Consumes without substitutes:

- all relevant merged W7-ENTRY-CONTRACT types;
- exact current Platform native OAuth/ticket source at `8e613c00503c0874e69e2085c740f87f4a87e002`;
- exact Gateway protocol v1 request/response/error/cache contract at that revision.

Required deterministic/fake scope:

- Authorization Code + PKCE `S256` transaction generation;
- system-browser launch request abstraction without embedded credentials;
- exact state, callback path, origin, active-generation, stale and duplicate validation;
- single-use authorization code exchange boundary;
- strict bounded JSON for Game Login Ticket issue and Gateway `POST /v1/login`;
- exact protocol version `1`, no unknown response assumptions, no-store policy verification where observable;
- validation that selected `Character.world_id` matches the selected world;
- access/refresh-token and Game Login Ticket clearing at their exact terminal boundaries;
- no Oteryn password UI or Canary password fallback;
- stable redacted failures and no retry that can duplicate ticket/session issuance.

Current exact Gateway v1 response fields are `protocol_version`, `session { credential, expires_at }`, `worlds[] { id, slug, name, region, host, port }` and `characters[] { id, name, level, vocation, world_id }`. There is no directory revision, gameplay-channel ID, general issuer directory or multi-world issuer routing contract.

External blocker `W7-BLOCK-IDENTITY-REDIRECT`:

- current Platform source requires native redirect URI exactly `http://127.0.0.1/callback` and rejects any explicit port;
- the normative Rust security model requires an OS-assigned loopback port;
- the worker must not bind fixed port 80, weaken the security invariant or invent dynamic redirect registration;
- the real browser/listener adapter and real Identity compatibility claim remain blocked until exact producer or accepted architecture evidence reconciles the conflict;
- pure transaction/state-machine and fake HTTP/browser adapters may merge with the blocker preserved.

The current producer revokes the native access token and associated refresh token after issuing one Game Login Ticket. W7 therefore claims only one bounded bootstrap account-session attempt, not a reusable long-lived relog session.

## 7. Lane W7-CANARY-ENTRY

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

- merged W7-ENTRY-CONTRACT request/credential/result types;
- exact Canary Current-profile source at `4b2d6f432d92628c42bde1d95daed6ae0d0eb88f`;
- the configured `World.host`, `World.port`, selected character name and one moved credential.

Sole produced interface:

- one bounded transport connection/admission interface used by W7;
- exact Current-profile challenge/login encoder and bounded admission-prefix decoder;
- no general gameplay protocol/domain types.

Exact source boundary at the evidence cut:

- Canary release is `3.6.1`; Current client protocol is `1525`;
- Current profile uses OpenTibia RSA, server challenge before login, modern block-count framing, modern padding byte, sequence checksum after login and official compression signaling;
- Current login layout includes OS `u16`, protocol `u16`, client version `u32`, client-version string, asset-hash string, preview-state byte, RSA-encrypted XTEA key/GM/session-key/character/challenge response and optional OTCv8 probe;
- the one-shot Game Session is consumed against character name and Current profile;
- successful placement emits login opcode `0x17`, then bounded pre-world packets including `0x1A`, Tibia time `0xEF`, pending-state `0x0A` and enter-world `0x0F` before map description;
- `SessionEntered` may be emitted only after the ordered validated admission prefix reaches `0x0F`; the lane stops before map-description decoding and disconnects cleanly.

Required tests include bounded/truncated/oversized frames, challenge mismatch, checksum/sequence mismatch, padding, compression output limits, RSA/XTEA boundary vectors, wrong profile/version, wrong character, expired/replayed credential, unexpected opcode order, partial write/read, timeout, disconnect and redacted errors.

Dependency selection for HTTPS-independent TCP admission crypto/compression must be narrowly evidenced against Rust `1.94.0`, current licenses/advisories and cargo-deny. No dependency version is pre-approved by this plan. Policy weakening is prohibited.

Reference physical E2E from Canary PR #815 used legacy OTClient and older exact producer revisions. It is evidence that the external architecture can work, not proof that the Rust consumer is compatible.

## 8. Lane W7-LOGIN-E2E

Prompt: `prompts/W7_LOGIN_E2E_AGENT.md`  
Contract role: final consumer/composition owner  
Initial state after ENTRY merge: private fake harness only; final integration blocked on required producers

Exclusive owned paths before final integration:

```text
oteryn-client/crates/app-runtime/**
oteryn-client/tests/integration/technical-login/**
oteryn-client/docs/research/technical-login/W7_LOGIN_E2E_EVIDENCE.md
```

Final integration lease adds:

```text
oteryn-client/apps/client/**
```

Consumes merged producer APIs and may not redefine public entry, identity, transport or protocol types.

Required composition:

- preserve the existing Windows `winit` window and renderer lifecycle;
- one explicit technical configuration surface for issuer authorization/token endpoints, Gateway base URL, expected world identity/host/port and selected character; no hidden production defaults;
- keep blocking browser/HTTP/TCP work outside the window event thread;
- deliver typed progress/result events back to app runtime;
- report `SessionEntered` or typed recoverable `EntryFailure` without adding a general native UI framework;
- on close/failure/success-disconnect clear callback state, code verifier, authorization code, access/refresh token, Game Login Ticket, Game Session credential, transport keys and session-scoped buffers.

The fake-service E2E must prove stale callback rejection, duplicate callback rejection, state mismatch, one successful ticket/session handoff, duplicate/late credential rejection, world-character validation, secret redaction, terminal cleanup and requirement for a fresh credential on a second attempt.

## 9. Shared-path lease

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
2. non-holder workers keep shared paths read-only and may work only in exclusive crates;
3. a worker that finished exclusive work marks `parallel_lane_state: integration_ready` and waits;
4. holder integrates generated Cargo metadata/lockfile and shared docs, validates exact head, merges and archives;
5. next worker restacks on current `main`, regenerates resolution and claims the released lease;
6. manual `Cargo.lock` conflict resolution, copied lockfile fragments and concurrent shared-document edits are prohibited.

Recommended lease/merge order:

1. `W7-ENTRY-CONTRACT`
2. `W7-CANARY-ENTRY` and `W7-IDENTITY`, ordered by downstream readiness; the blocked real Identity adapter must not delay merge of a clearly bounded deterministic/fake package
3. `W7-LOGIN-E2E`
4. separate archive PR for every merged worker
5. separate W7 closure PR
6. separate archive PR for W7 closure

## 10. Evidence matrix

| Requirement | Automated evidence | Interactive/external evidence |
|---|---|---|
| workspace/executable | locked metadata, Windows target build, exact `cargo fmt`, Clippy, tests, architecture check, cargo-deny, repository CI | launch exact Windows executable and observe existing Oteryn window |
| entry contract | deterministic lifecycle/generation/property tests; secret-debug/redaction tests | none required |
| Identity core | fake browser/listener/HTTP tests for PKCE, callback validation, stale/duplicate rejection, strict JSON, cache policy, cleanup | real system-browser callback only after `W7-BLOCK-IDENTITY-REDIRECT` is resolved |
| Gateway | bounded fake server proves protocol v1 request/response/error shapes and one-shot handoff | exact configured deployed Gateway revision/TLS evidence, otherwise blocked |
| Canary admission | synthetic source-derived challenge/login/admission transcripts, malformed/timeout/replay tests | named exact Canary revision/build/configured issuer; one Rust entry and safe disconnect, otherwise explicitly blocked |
| full flow | fake-service executable E2E proves one success plus all mandated rejection/cleanup cases | real configured Identity -> Gateway -> Canary flow only after all producer/deployment blockers clear |
| production readiness | repository tests may prove only code properties | TLS certificates/hostnames, secret manager, firewall, deployed revisions and production observability remain external and out of scope |

## 11. Explicit blocked items

### `W7-BLOCK-IDENTITY-REDIRECT`

Fixed no-port Platform redirect conflicts with the OS-assigned-port Rust security invariant. Real callback integration is blocked; no speculative API or security downgrade.

### `W7-BLOCK-REAL-RUST-E2E`

No Rust consumer has yet completed the real path. Repository/fake tests and legacy OTClient evidence cannot satisfy this. Final real-path acceptance requires named exact Identity, Gateway and Canary revisions plus interactive evidence; otherwise the plan records the real path as blocked.

### `W7-BLOCK-DEPLOYMENT-EVIDENCE`

Repository access does not prove deployed TLS, hostname validation, firewall reachability, runtime issuer mapping, secret injection or revision identity. No production claim.

### `W7-BLOCK-MULTIWORLD-CHANNEL`

Gateway v1 has no general gameplay-channel or multi-issuer directory/routing contract. `GameplayChannelId` remains unused; one exact configured world/issuer only.

### `W7-BLOCK-ACCOUNT-SESSION-REUSE`

Current native OAuth producer revokes access and refresh tokens after one Game Login Ticket. The first milestone cannot claim reusable account-session relog/channel switching.

## 12. Exact acceptance criteria

The W7 implementation wave succeeds only when:

- every lane has unique task, branch/worktree and draft/ready/merge/archive history;
- no overlapping public producer or shared-path lease exists;
- `W7-ENTRY-CONTRACT` is the sole producer of all named entry/shared identity types;
- `W7-CANARY-ENTRY` is the sole initial transport/protocol-admission interface producer;
- final executable compiles on pinned Rust `1.94.0` for Windows and opens the existing window;
- exact-head locked metadata, formatting, Clippy, all tests, architecture checks, cargo-deny and repository required CI pass;
- fake-service E2E proves stale callback rejection, duplicate callback rejection, one-shot credential handling, fresh-second-attempt behavior, terminal cleanup and secret redaction;
- explicit configuration selects one world/issuer and one matching character;
- one moved Game Session credential is never logged, cloned, persisted or replayed;
- Current-profile source-derived admission reaches ordered `0x17` -> `0x0A` -> `0x0F` semantics without decoding the map payload;
- the app reports typed `SessionEntered` or typed recoverable `EntryFailure`, safely disconnects and clears session-scoped credentials;
- exact named real Rust evidence proves the configured Canary admission path, or the real path remains explicitly blocked without a compatibility claim;
- no unresolved review threads, ownership conflicts, stale bases or unarchived merged tasks remain;
- a separate W7 closure records exactly one next bounded recommendation and implements none of it.
