---
task_id: OTC-20260721-oteryn-identity-login
coordination_id: OTS-20260721-oteryn-identity-auth
status: in_progress
agent: ChatGPT
branch: feat/OTC-20260721-oteryn-identity-login
base_branch: main
created: 2026-07-21T21:00:00Z
updated: 2026-07-22T09:25:00Z
last_verified_commit: 1f0358a6e34a53d9b47aae04a1ecad885126eafc
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
  - src/framework/net/server.*
  - src/framework/util/crypt.*
  - init.lua
  - docs/agents/**
  - docs/auth/**
modules_touched:
  - client_entergame
reuses:
  - framework HTTP client
  - system browser via g_platform.openUrl
  - framework event dispatcher
  - existing GameSessionKey game-world transport
public_interfaces:
  - Services.oterynIdentity deployment configuration
  - server/profile authMode oteryn_identity
  - loopback OAuth callback listener
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
- [x] OAuth access token and Game Login Ticket are cleared immediately after their one intended HTTP handoff is queued.
- [x] Oteryn profile never silently falls back to legacy password login; legacy mode remains an explicit separate profile configuration.
- [x] OAuth code exchange, Platform ticket issuance, and Game Gateway login are separate protocol steps matching the currently merged producer implementations.
- [x] Gateway worlds are authoritative and characters must reference an exact returned `world_id` before host/port are accepted.
- [x] Game Session credential is handed to the existing `GameSessionKey` path once and client auto-replay/reconnect fails closed.
- [x] Versioned client/Platform/Gateway contract and failure behavior are documented.
- [x] Cross-repository registry records the remaining Canary Game Session adapter gate without claiming implementation outside `blakinio/otclient`.
- [ ] Loopback callback uses an OS-assigned ephemeral port rather than bounded client-side port probing.
- [ ] Required desktop C++ builds complete on the final non-draft PR head.
- [ ] Focused deterministic auth-contract tests are added using existing test infrastructure where available, without creating a parallel harness.
- [x] Module catalogue, changelog, auth architecture and cross-repo contract docs updated.
- [ ] Autonomous merge gate satisfied or exact remaining blocker documented.

# Confirmed context

- `main` HEAD verified as `a6868920443dc285656bd016acdb2c1ea566e511` at task start and remained the PR base during the 2026-07-22 revalidation.
- Live work revalidation found existing draft PR #17 for this exact task; it is being continued rather than duplicated.
- Current legacy `entergame.lua` copies account/password into globals and persists encrypted credentials; legacy `ProtocolLogin` serializes password. Those paths remain only for explicitly configured legacy profiles.
- `ProtocolGame::sendLoginPacket` already has a `GameSessionKey` branch that sends session key + character name instead of account/password.
- Current Platform OAuth scope is `game:ticket`, ticket issuance is `POST /api/v1/game-auth/tickets`, and the deployed Gateway accepts strict `POST /v1/login` JSON containing only `protocol_version` and `game_login_ticket`.
- Current Gateway returns `session.credential`, `session.expires_at`, authoritative `worlds` with `id/host/port`, and account-scoped `characters` with `world_id`.
- The production Canary Game Session compatibility adapter remains unresolved in `GAME_SESSION_CANARY_CONTRACT.md`; this OTClient task cannot claim world-entry E2E readiness.
- Container network access cannot clone GitHub in this environment; GitHub connector state/files and GitHub Actions are the executable evidence source. No local build/runtime success is claimed.

# Existing work to reuse

| Module/task/PR | Reuse | Evidence/path | Why it fits |
|---|---|---|---|
| Framework HTTP | OAuth form POST, JSON ticket/Gateway POST, cancellation | `modules/corelib/http.lua`, `src/framework/net/protocolhttp.cpp` | Existing bounded asynchronous transport; bearer is exposed only during synchronous request queueing then overwritten. |
| Platform URL open | system-browser authorization | `g_platform.openUrl` binding | Avoids embedded credential WebView. |
| GameSessionKey | final client -> world credential field | `src/client/protocolgamesend.cpp` | Existing protocol branch sends session key + character instead of account/password. |
| Event dispatcher | timeout/cancellation cleanup | framework Lua event APIs | Existing bounded lifecycle primitive. |
| Client test foundation | future focused deterministic tests | active PR #3 | Must be reused when available; no second harness. |

# Ownership and overlap check

- Existing draft PR #17 is the authoritative OTClient task branch.
- No second OTClient auth PR was created.
- Platform producer phases were revalidated against merged PRs #117/#119/#121/#122.
- No Canary writes are performed in this task; Phase 6 Game Session adapter remains cross-repository work.
- Legacy protocol files are intentionally not modified because the Oteryn first-party path bypasses password-based login-server authentication rather than adding a new credential to `ProtocolLogin`.

# Current state

The original PR #17 concept was corrected from a stale `OAuth token endpoint -> ticket -> login-server` model to the currently deployed architecture:

```text
browser Identity
-> Authorization Code + PKCE
-> OAuth access token
-> Platform Game Login Ticket endpoint
-> standalone Game Gateway /v1/login
-> Game Session + authoritative worlds/characters
-> existing OTClient GameSessionKey world-entry field
```

Current Lua syntax, workflow validation, informational static analysis and required CI passed on run `29907489042`. Platform builds were skipped because PR #17 is still draft; final desktop C++ compilation remains required before merge.

# Plan

1. Replace client-side loopback port probing with an OS-assigned IPv4 loopback ephemeral port and expose the bound port safely to Lua.
2. Add focused pure auth-contract tests through the existing repository test foundation if available on the current base; otherwise record the exact test-infrastructure dependency without inventing a second harness.
3. Review final diff for credential/logging/persistence regressions and exact Gateway JSON compatibility.
4. Update PR description/checkpoint, mark PR ready to force scoped desktop builds, repair failures, and merge only when the autonomous gate is satisfied.
5. Leave production Canary Game Session adapter and cross-repository end-to-end proof to the separately scoped Phase 6/7 work.

# Work log

## 2026-07-21T21:00:00Z

- Changed: created task branch and durable task record.
- Learned: current auth persists encrypted passwords and generic `Server` was not loopback-only.
- Failed/blocked: direct local clone/build unavailable because sandbox DNS cannot resolve GitHub.
- Result: proceed through repository connector and GitHub Actions.

## 2026-07-22T09:25:00Z

- Changed: continued existing PR #17; corrected OAuth scope/callback path/config; split OAuth token exchange from Platform ticket issuance; replaced stale login-server ticket exchange with strict Game Gateway `/v1/login`; normalized authoritative `world_id` routing; added one-shot Game Session guard; added durable auth/cross-repo/catalogue/changelog documentation.
- Learned: deployed Gateway rejects unknown JSON fields and returns `session.credential` rather than legacy `sessionkey`; production Canary adapter is still intentionally unresolved.
- Validation: CI run `29907489042` passed Lua syntax, fast checks, informational static analysis and required gate; builds skipped while draft.
- Remaining: OS-assigned loopback ephemeral port, focused tests, non-draft C++ builds and final merge gate.

# Decisions

| Decision | Reason/evidence | ADR/contract |
|---|---|---|
| Use system browser + Authorization Code + PKCE S256 | first-party native-app contract; avoids embedded credential capture | Platform ADR 0009 / OTCLIENT_GAME_AUTH_CONTRACT |
| Use IPv4 loopback callback with exact `/callback` path | matches current Platform native redirect contract | OTCLIENT_GAME_AUTH_CONTRACT |
| Keep OAuth access token separate from Game Login Ticket | deployed Platform Phase 3 requires bearer-authenticated ticket issuance | GAME_GATEWAY_IDENTITY_CONTRACT |
| Send only `protocol_version` + `game_login_ticket` to Gateway | current Gateway uses strict JSON decoding | deployed Gateway MVP |
| Treat Gateway world routing as authoritative | client must not invent account/world ownership | OTCLIENT_GAME_AUTH_CONTRACT |
| Reuse existing `GameSessionKey` only as the client wire field | current OTClient already sends session key + character without password | GAME_SESSION_CANARY_CONTRACT; final adapter still pending |
| Clear Game Session after one client handoff and reject replay | retry/reconnect semantics are not yet approved; fail closed | GAME_SESSION_CANARY_CONTRACT |
| Never silently invoke legacy password fallback from Oteryn mode | prevents local configuration/UI downgrade from bypassing native auth | rollout/security contract |

# Files and interfaces

| Path/interface/config/schema | Purpose | Status |
|---|---|---|
| `docs/auth/oteryn-identity-login.md` | architecture, lifecycle, threat model and producer contracts | implemented |
| `modules/client_entergame/oteryn_identity_core.lua` | PKCE/callback/Gateway validation primitives | implemented |
| `modules/client_entergame/oteryn_identity.lua` | browser -> OAuth -> ticket -> Gateway orchestration | implemented |
| `modules/client_entergame/oteryn_session_guard.lua` | one-shot Game Session handoff/replay guard | implemented |
| `src/framework/net/server.*` | loopback-only callback HTTP primitive | implemented; OS-assigned port refinement pending |
| `src/framework/util/crypt.cpp` | CSPRNG-backed UUID material | implemented |
| `Services.oterynIdentity` | deployment-owned Identity/Platform/Gateway endpoints and public client id | implemented, disabled by default |

# Validation and CI

| Commit | Command/check/workflow | Result | Evidence/notes |
|---|---|---|---|
| a6868920443dc285656bd016acdb2c1ea566e511 | local git/build preflight | unavailable | sandbox DNS cannot resolve github.com; connector preflight completed |
| 1f0358a6e34a53d9b47aae04a1ecad885126eafc | GitHub Actions CI run 29907489042 | PASS for required draft gate | Lua syntax, workflow validation and informational analysis passed; builds skipped because PR is draft |

Never write `passed` without verification.

# Failed approaches and dead ends

- Reusing generic wildcard `Server` directly for OAuth callback was rejected.
- Treating OAuth token endpoint response as a Game Login Ticket was rejected after revalidation against merged Platform Phase 3.
- Sending ticket directly to a legacy/login-server HTTP contract was rejected after revalidation against standalone Game Gateway MVP.
- Adding client-selected account/world ownership data to Gateway requests is rejected.
- Blind auto-reconnect with a reusable Game Session is rejected until the selected Canary adapter defines exact replay/reconnect semantics.

# Risks and compatibility

- Runtime: loopback callback code is desktop-only; browser/mobile fail closed until platform-specific redirect work exists.
- Data/migration: encrypted legacy password settings remain only for generic/legacy profiles; Oteryn flow does not create/update them.
- Security: bearer credentials must not enter logs/settings/URLs; authorization code appears only in the standard loopback callback query.
- Backward compatibility: native auth is disabled by default and explicitly profile-gated.
- Session compatibility: current client can populate the existing `GameSessionKey` field, but production Canary acceptance/storage/revocation remains a separate adapter decision.
- Rollback: disable `Services.oterynIdentity.enabled` or configure the profile as explicit `legacy`; no automatic downgrade occurs inside the Oteryn flow.

# Remaining work

1. Implement OS-assigned loopback ephemeral port.
2. Add/attach focused deterministic auth tests through existing test infrastructure.
3. Run non-draft scoped builds and repair failures.
4. Final review, ready-for-review transition and autonomous merge if all gates are green.

# Handoff

## Start here

Read this task, `docs/auth/oteryn-identity-login.md`, then inspect live PR #17 and current GitHub Actions state.

## Do not repeat

Do not reintroduce direct ticket-to-login-server flow, persistent Oteryn password storage, client-authoritative world routing, OAuth refresh-token use, or automatic Game Session replay.

## Required reads

- `AGENTS.md`
- `docs/agents/ACTIVE_WORK.md`
- `docs/agents/MODULE_CATALOG.md`
- `docs/agents/CROSS_REPO_CONTRACTS.md`
- `docs/auth/oteryn-identity-login.md`
- current Platform OTClient/Game Gateway/Game Session contracts

## Open questions

- Exact production Identity/Platform/Gateway endpoint URLs and registered native client id are deployment configuration and must not be hard-coded.
- Exact production Canary Game Session adapter, TTL, revocation and reconnect semantics remain Phase 6 decisions.

# Completion

- Final status: in progress
- PR: #17 draft
- Merge commit: pending
- Catalogue updated: yes
- Changelog updated: yes
- Archived at: pending
