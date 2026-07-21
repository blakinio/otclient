---
task_id: OTC-20260721-oteryn-identity-login
coordination_id: OTS-20260721-oteryn-identity-auth
status: in_progress
agent: ChatGPT
branch: feat/OTC-20260721-oteryn-identity-login
base_branch: main
created: 2026-07-21T21:00:00Z
updated: 2026-07-21T21:00:00Z
last_verified_commit: a6868920443dc285656bd016acdb2c1ea566e511
risk: high
related_issue: ""
related_pr: ""
depends_on: []
blocks: []
owned_paths:
  - modules/client_entergame/**
  - modules/gamelib/protocollogin.lua
  - modules/client_serverlist/serverlist.lua
  - src/framework/net/**
  - src/framework/util/crypt.*
  - src/framework/luafunctions.cpp
  - src/CMakeLists.txt
  - init.lua
  - docs/agents/**
  - docs/auth/**
modules_touched:
  - client_entergame
  - client_serverlist
  - gamelib
reuses:
  - framework HTTP client
  - system browser via g_platform.openUrl
  - framework event dispatcher
  - existing ProtocolLogin transport
public_interfaces:
  - Oteryn Identity client configuration
  - loopback OAuth callback listener
  - ProtocolLogin oteryn_identity auth mode
cross_repo_tasks:
  - OTERYN-20260721-otclient-identity-contract
  - LOGIN-20260721-game-ticket-contract
  - CAN-20260721-game-ticket-consumer-validation
---

# Goal

Add a client-first, migration-safe Oteryn Identity login integration using system-browser Authorization Code + PKCE, a loopback callback, an ephemeral game-login ticket, and an explicitly versioned login-server auth contract without persisting the user's primary password.

# Acceptance criteria

- [ ] `Sign in with Oteryn` is the preferred login action when configured.
- [ ] Native desktop flow uses system browser, PKCE S256, state, bounded timeout, strict loopback callback matching, cancellation, and one-flow-at-a-time replay protection.
- [ ] Oteryn flow never writes the primary password or game ticket to settings.
- [ ] Game ticket is cleared after handoff/error as soon as practical.
- [ ] Legacy password flow remains explicitly configurable and can be disabled.
- [ ] Ticket is sent only when server configuration declares versioned Oteryn ticket support.
- [ ] Versioned client/login-server contract and failure behavior are documented.
- [ ] Cross-repository Platform/login-server/Canary handoffs are durable and contain no implementation outside `blakinio/otclient`.
- [ ] Relevant static/build/test checks completed or exact unavailable environment documented.
- [ ] Module catalogue, changelog, ADR/architecture docs updated.
- [ ] Autonomous merge gate satisfied or blocker documented.

# Confirmed context

- `main` HEAD verified as `a6868920443dc285656bd016acdb2c1ea566e511` at task start.
- Live GitHub had no open PRs at task start; `docs/agents/ACTIVE_WORK.md` was stale and still referenced old PR #3/#4.
- Current `modules/client_entergame/entergame.lua` copies account/password into globals, persists encrypted account/password, and passes the password to both HTTP login and `ProtocolLogin`.
- Current `modules/client_serverlist/serverlist.lua` persists password using `g_crypt.encrypt`.
- Current `modules/gamelib/protocollogin.lua` serializes the account password in the login packet.
- Existing generic `Server` binds IPv4 wildcard and does not expose a loopback-only ephemeral-port OAuth callback abstraction, so it is not suitable as-is for RFC 8252 loopback redirect handling.
- Container network access cannot clone GitHub in this environment; GitHub connector state/files are used for repository inspection and writes. No local build/runtime result will be claimed without evidence.

# Existing work to reuse

| Module/task/PR | Reuse | Evidence/path | Why it fits |
|---|---|---|---|
| Framework HTTP | token/ticket endpoint POSTs and cancellation | `modules/corelib/http.lua`, `src/framework/net/protocolhttp.cpp` | Supports form-urlencoded POST and bounded timeout. |
| Platform URL open | system-browser authorization | `g_platform.openUrl` binding | Avoids embedded WebView. |
| ProtocolLogin | legacy transport and migration gate | `modules/gamelib/protocollogin.lua` | Existing login-server connection lifecycle can carry a versioned alternative credential. |
| Event dispatcher | timeout/cancellation cleanup | framework Lua event APIs | Existing lifecycle primitive. |

# Ownership and overlap check

- Open PRs inspected: none live at task start.
- Active tasks inspected: coordination index is stale; no live PR overlap found.
- Overlaps: login/protocol paths are cross-repository coupled by policy.
- Resolution: client-only implementation plus durable handoffs; no writes to Platform, login-server, Canary, or upstream OTClient.

# Current state

Preflight and source analysis complete. Branch/task claimed. Implementation in progress.

# Plan

1. Add standards-based crypto helpers and loopback callback primitive needed by native desktop OAuth.
2. Add Oteryn Identity Lua controller and preferred login UX with strict migration gates.
3. Add versioned ticket login contract to `ProtocolLogin` while retaining legacy behavior.
4. Remove Oteryn-flow dependence on persistent password storage and document legacy limitation.
5. Add focused tests where current repository harness permits; otherwise add deterministic pure-Lua contract tests and document unavailable runtime coverage.
6. Add ADR, architecture/threat model, cross-repo handoffs, catalogue/changelog entries.
7. Review diff, inspect CI, repair failures, and merge only if autonomous gate is satisfied.

# Work log

## 2026-07-21T21:00:00Z

- Changed: created task branch and durable task record.
- Learned: current auth persists encrypted passwords and uses `G.password`; generic `Server` is not loopback-only.
- Failed/blocked: direct local clone/build unavailable because sandbox DNS cannot resolve GitHub.
- Result: proceed through repository connector; validation claims will distinguish CI from unavailable local runtime.

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| Use system browser + Authorization Code + PKCE S256 | Native-app best practice; avoids embedded credential capture | planned |
| Use IPv4 loopback `127.0.0.1` on OS-assigned ephemeral port | Appropriate desktop redirect model; callback can be bound only to loopback | planned |
| Keep ticket validation server-authoritative | Client cannot establish ticket validity/single-use itself | planned |
| Gate ticket wire format by explicit server capability/config | Prevents sending new credential to legacy servers | planned |

# Files and interfaces

| Path/interface/config/schema | Purpose | Status |
|---|---|---|
| `docs/auth/oteryn-identity-login.md` | architecture, lifecycle, threat model, contracts | planned |
| loopback callback primitive | strict native callback receiver | planned |
| Oteryn Identity controller | browser/PKCE/token/ticket lifecycle | planned |
| `ProtocolLogin` auth mode v1 | ticket handoff to declared-capable login server | planned |

# Validation and CI

| Commit | Command/check/workflow | Result | Evidence/notes |
|---|---|---|---|
| a6868920443dc285656bd016acdb2c1ea566e511 | local git/build preflight | unavailable | sandbox DNS cannot resolve github.com; connector preflight completed |

Never write `passed` without verification.

# Failed approaches and dead ends

- Reusing generic `Server` directly for OAuth callback rejected because it binds `0.0.0.0` and does not expose an OS-assigned port to Lua.

# Risks and compatibility

- Runtime: new loopback callback code is desktop-only; browser/mobile must fail closed until a platform-specific redirect mechanism is designed.
- Data/migration: legacy encrypted password settings remain readable only for legacy fallback during migration; Oteryn flow must not create/update them.
- Security: high-risk auth surface; no secrets may enter logs/settings/query parameters beyond short-lived authorization code returned by standard redirect.
- Backward compatibility: legacy mode remains explicit; Oteryn ticket must never be sent unless declared supported.
- Cross-repo rollout: Platform and login-server changes are required before end-to-end production enablement; client code must default disabled/fail closed.
- Rollback: disable `oteryn_identity` configuration and retain explicit legacy auth mode during migration.

# Remaining work

1. Implement the client-side loopback/PKCE/Oteryn flow and versioned ticket handoff.

# Handoff

## Start here

Read this task, then `docs/auth/oteryn-identity-login.md` once created, and inspect the live PR/CI state.

## Do not repeat

Do not reintroduce persistent password storage for Oteryn autologin and do not invent server-side ticket validation semantics in this repository.

## Required reads

- `AGENTS.md`
- `docs/agents/ACTIVE_WORK.md`
- `docs/agents/MODULE_CATALOG.md`
- `docs/agents/CROSS_REPO_CONTRACTS.md`
- `modules/client_entergame/entergame.lua`
- `modules/gamelib/protocollogin.lua`
- `modules/client_serverlist/serverlist.lua`

## Open questions

- Exact production Oteryn Identity endpoint URLs/client ID are external deployment configuration and must not be hard-coded here.
- Exact login-server capability advertisement mechanism requires server-side agreement; client will use an explicit configuration gate until contract producer is implemented.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Catalogue updated: pending
- Changelog updated: pending
- Archived at: pending
