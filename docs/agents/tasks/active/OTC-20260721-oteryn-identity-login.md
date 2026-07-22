---
task_id: OTC-20260721-oteryn-identity-login
coordination_id: OTS-20260721-oteryn-identity-auth
status: validating
agent: ChatGPT
branch: feat/OTC-20260721-oteryn-identity-login
base_branch: main
created: 2026-07-21T21:00:00Z
updated: 2026-07-22T10:08:00Z
last_verified_commit: 1824991d2cd2af13838ee96e1581b9d4d4424ed9
risk: high
related_issue: ""
related_pr: "17"
depends_on:
  - Oteryn Platform game-auth architecture PR 117
  - Oteryn Platform native OAuth PKCE PR 119
  - Oteryn Platform Game Login Ticket API PR 121
  - Oteryn Platform Game Gateway MVP PR 122
blocks:
  - production cross-repository game-auth E2E
owned_paths:
  - modules/client_entergame/**
  - modules/corelib/http.lua
  - src/framework/net/server.*
  - src/framework/net/protocolhttp.h
  - src/framework/util/crypt.cpp
  - src/framework/luafunctions.cpp
  - tests/lua/contracts/oteryn_identity_core_test.lua
  - tests/lua/CMakeLists.txt
  - tests/integration/protocol/loopback_packet_test.cpp
  - init.lua
  - docs/agents/**
  - docs/auth/**
modules_touched:
  - client_entergame
  - corelib
reuses:
  - framework HTTP client
  - system browser via g_platform.openUrl
  - framework event dispatcher
  - existing GameSessionKey game-world transport
  - merged client test foundation
public_interfaces:
  - Services.oterynIdentity deployment configuration
  - server/profile authMode oteryn_identity
  - loopback OAuth callback listener
  - Server.createLoopbackHttp and Server.getLocalPort Lua bindings
  - Http.removeCustomHeader Lua binding
  - Game Gateway protocol v1 response normalization
  - one-shot GameSessionKey handoff
cross_repo_tasks:
  - OTS-20260721-oteryn-identity-auth
  - Oteryn Platform GAME_SESSION_CANARY_CONTRACT Phase 6 adapter selection
---

# Goal

Implement the OTClient consumer side of the current Oteryn game-auth architecture: system-browser Authorization Code + PKCE, loopback callback, short-lived OAuth bootstrap, separate Platform Game Login Ticket issuance, standalone Game Gateway login, authoritative world/character routing, and one-shot Game Session handoff to the existing `GameSessionKey` game-world protocol field without sending or persisting the user's Oteryn password.

# Acceptance criteria

- [x] `Sign in with Oteryn` is the preferred login action when the profile is explicitly configured for Oteryn Identity.
- [x] Native desktop flow uses system browser, PKCE S256, high-entropy state, bounded timeout, strict callback path/state validation, cancellation, and one-flow-at-a-time replay protection.
- [x] Oteryn flow never writes the primary password, OAuth token, Game Login Ticket, or Game Session credential to settings.
- [x] OAuth access token is used only for ticket issuance and the temporary Authorization header is removed from the shared HTTP header map immediately after the request is queued.
- [x] Game Login Ticket is retained only for the immediate Gateway request and is cleared after queueing.
- [x] Oteryn profile never silently falls back to legacy password login; legacy mode remains an explicit separate profile configuration.
- [x] OAuth code exchange, Platform ticket issuance, and Game Gateway login are separate protocol steps matching merged producer implementations.
- [x] Gateway worlds are authoritative and characters must reference an exact returned `world_id` before host/port are accepted.
- [x] Oteryn RSA selection is deferred until the exact Gateway-authoritative `worldHost` is known and is applied immediately before `g_game.loginWorld`.
- [x] Game Session credential is handed to the existing `GameSessionKey` path once and client auto-replay/reconnect fails closed.
- [x] `Game::loginWorld` -> `ProtocolGame::login` synchronously copies the Game Session credential into `ProtocolGame::m_sessionKey` before asynchronous connect begins.
- [x] Oteryn character-list UI does not invent a Free/Premium subscription classification when Gateway does not provide one.
- [x] Versioned client/Platform/Gateway contract and failure behavior are documented.
- [x] Cross-repository registry records the remaining Canary Game Session adapter gate without claiming implementation outside `blakinio/otclient`.
- [x] Loopback callback binds IPv4 loopback port `0` and reads the OS-assigned ephemeral port before opening the browser.
- [ ] Required desktop C++ builds complete on the final non-draft PR head.
- [x] Focused deterministic auth-contract tests are registered in the merged Lua test foundation and loopback ephemeral-port behavior is covered in the existing protocol integration target.
- [x] Original `init.lua` module-discovery/autoload/updater startup tail is preserved after adding Oteryn configuration.
- [x] Module catalogue, changelog, auth architecture and cross-repo contract docs updated.
- [ ] Autonomous merge gate satisfied or exact remaining blocker documented.

# Confirmed context

- `main` HEAD verified as `a6868920443dc285656bd016acdb2c1ea566e511` at task start and is the PR base.
- Existing PR #17 is the authoritative task branch; no duplicate auth PR was created.
- Legacy `entergame.lua` copies account/password into globals and persists encrypted credentials; legacy `ProtocolLogin` serializes password. Those paths remain only for explicitly configured legacy profiles.
- `ProtocolGame::sendLoginPacket` already has a `GameSessionKey` branch that sends session key + character name instead of account/password.
- `Game::loginWorld` creates `ProtocolGame` and calls `ProtocolGame::login(..., sessionKey)` synchronously; `ProtocolGame::login` assigns `m_sessionKey = sessionKey` before `connect(host, port)`.
- Current Platform OAuth scope is `game:ticket`, ticket issuance is `POST /api/v1/game-auth/tickets`, and the deployed Gateway accepts strict `POST /v1/login` JSON containing only `protocol_version` and `game_login_ticket`.
- Current Gateway returns `session.credential`, `session.expires_at`, authoritative `worlds` with `id/host/port`, and account-scoped `characters` with `world_id`.
- Oteryn no longer selects RSA from the local pre-Gateway profile host; selection uses the exact validated Gateway world host at world-entry handoff.
- The production Canary Game Session compatibility adapter remains unresolved in `GAME_SESSION_CANARY_CONTRACT.md`; this OTClient task cannot claim production world-entry E2E readiness.
- Client test foundation PR #3 is merged as `9733a8dd4b3b1fc4c3fd862fc32f1f2ea86f8a67` and is reused directly.
- Container network access cannot clone GitHub in this environment; GitHub connector state/files and GitHub Actions are the executable evidence source. No local build/runtime success is claimed.

# Current implemented flow

```text
system browser
-> Oteryn Identity Authorization Code + PKCE
-> short-lived OAuth access token
-> Platform POST /api/v1/game-auth/tickets
-> opaque one-time Game Login Ticket
-> standalone Game Gateway POST /v1/login
-> Game Session credential + authoritative worlds/characters
-> Gateway-authoritative world host selects RSA
-> selected world through existing OTClient GameSessionKey field
```

The loopback callback uses `Server.createLoopbackHttp()` to bind `127.0.0.1:0`; `Server.getLocalPort()` exposes the actual OS-assigned port to Lua. The Game Session credential is cleared from global Lua state after the first normal world-login handoff, while C++ has already copied it into `ProtocolGame`.

# Security and compatibility decisions

| Decision | Reason/evidence |
|---|---|
| System browser + Authorization Code + PKCE S256 | avoids embedded credential capture and matches Platform native-client contract. |
| IPv4 loopback `127.0.0.1:0` | OS owns ephemeral-port selection; listener is never wildcard/public. |
| OAuth token separate from Game Login Ticket | Platform Phase 3 requires bearer-authenticated ticket issuance. |
| Remove Authorization header after queueing | prevents credential or empty Authorization header from leaking to unrelated later HTTP requests. |
| Send only `protocol_version` + `game_login_ticket` to Gateway | deployed Gateway uses strict JSON decoding. |
| Gateway world routing and RSA host authoritative | client must not invent account/world routing or derive world crypto selection from stale local profile routing. |
| Reuse existing `GameSessionKey` only as client wire field | existing OTClient sends session key + character without account/password; production Canary adapter remains pending. |
| One-shot Game Session/no auto-replay | reconnect semantics are not approved by Phase 6 contract; fail closed. |
| No automatic password fallback | prevents local UI/config downgrade from bypassing first-party native auth. |
| Native auth disabled by default | one-sided deployments remain safe before exact-version cross-repo E2E. |

# Validation and CI

| Commit/run | Result | Evidence |
|---|---|---|
| `1f0358a6e34a53d9b47aae04a1ecad885126eafc`, run `29907489042` | PASS draft required gate | Lua syntax, workflow validation and informational analysis passed; platform builds skipped because PR was draft. |
| run `29908319555` | superseded/cancelled | concurrency cancellation after ready-for-review transition; not a code failure. |
| `392e8c05cc81e95e6b9548a2be8fdbb9b0a15aaf`, run `29908924661` | ACTION_REQUIRED, no jobs | bot-authored cleanup commit did not produce executable PR jobs. |
| `e9843b5c0f8863fcc906d73d63f92fb31534bfdd`, run `29909439825` | SUPERSEDED | full matrix started before the authoritative Gateway-world RSA correction; it is not the final merge gate. |
| `1824991d2cd2af13838ee96e1581b9d4d4424ed9` | runtime correction | removed local-profile RSA selection and moved it to validated Gateway `worldHost`; this checkpoint commit triggers authoritative final CI on identical runtime code. |

Never write `passed` without verification.

# Work log

## 2026-07-21

- Created the task branch and durable task record.
- Established that generic legacy login persists password material and cannot be reused for first-party Oteryn auth.

## 2026-07-22 — architecture correction

- Continued existing PR #17 rather than creating a duplicate.
- Corrected stale `OAuth token -> ticket -> login-server` design to current Platform ticket + standalone Game Gateway architecture.
- Added authoritative `world_id` routing and one-shot Game Session handoff.
- Revalidated producer contracts against Platform PRs #117/#119/#121/#122.

## 2026-07-22 — hardening

- Replaced client-side port probing with OS-assigned `127.0.0.1:0`.
- Added deterministic PKCE/callback/Gateway Lua tests and loopback integration coverage using merged test foundation.
- Restored an accidentally removed `init.lua` startup tail found during final diff review before merge.
- Proved `ProtocolGame::login` copies session credential before asynchronous connect.
- Changed Oteryn account UI to display neutral `Oteryn Account` and suppress unsupported premium upsell classification.
- Added explicit `Http.removeCustomHeader` and removed temporary Bearer Authorization from shared HTTP state after ticket request queueing.
- Moved Game Session consumption to the exact `g_game.loginWorld` handoff instead of an outer UI wrapper.
- Moved RSA selection from the local pre-Gateway profile host to the exact validated Gateway `worldHost` immediately before world login.

# Failed approaches and dead ends

- Generic wildcard `Server` for OAuth callback: rejected.
- Client-side pseudo-random ephemeral-port probing: replaced by OS-assigned port `0`.
- OAuth token endpoint returning the game ticket: rejected after producer revalidation.
- Sending ticket directly to legacy/login-server: rejected after Gateway MVP revalidation.
- Client-authoritative account/world identifiers or pre-Gateway world RSA selection: rejected.
- Blind Game Session auto-reconnect/replay: rejected until Phase 6 defines semantics.
- Merging before full diff review: rejected; review caught and repaired the accidental `init.lua` startup-tail deletion and later the stale pre-Gateway RSA selection.

# Remaining work

1. Wait for the full non-draft CI/build/CTest matrix triggered by this normal checkpoint commit.
2. Inspect and repair exact failure markers without weakening security semantics.
3. Perform final changed-file/security review and confirm no temporary workflows remain.
4. Mark this task `ready`, update exact workflow evidence, and squash-merge PR #17 only if all required/relevant checks are green.
5. Archive the task after merge.
6. Continue autonomously to the separately scoped Phase 6 Canary Game Session adapter; production E2E remains blocked until that adapter and Phase 7 are proven.

# Handoff

## Start here

Read this task and `docs/auth/oteryn-identity-login.md`, then inspect live PR #17 and its current CI run.

## Do not repeat

Do not reintroduce direct ticket-to-login-server flow, persistent Oteryn password storage, client-authoritative world routing, pre-Gateway local-host RSA selection, OAuth refresh-token use, client-side port probing, global retained Authorization headers, or automatic Game Session replay.

## Required reads

- `AGENTS.md`
- `docs/agents/ACTIVE_WORK.md`
- `docs/agents/MODULE_CATALOG.md`
- `docs/agents/CROSS_REPO_CONTRACTS.md`
- `docs/auth/oteryn-identity-login.md`
- current Platform OTClient/Game Gateway/Game Session contracts

# Completion

- Final status: validating
- PR: #17 ready for review
- Merge commit: pending
- Catalogue updated: yes
- Changelog updated: yes
- Archived at: pending
