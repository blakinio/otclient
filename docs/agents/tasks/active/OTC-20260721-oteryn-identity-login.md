---
task_id: OTC-20260721-oteryn-identity-login
coordination_id: OTS-20260721-oteryn-identity-auth
status: ready
agent: ChatGPT
branch: main
base_branch: main
created: 2026-07-21T21:00:00Z
updated: 2026-07-22T11:47:00Z
last_verified_commit: bb87346f6c516a19d19497d82bb01fb389334ff5
risk: high
related_issue: ""
related_pr: "17"
depends_on:
  - Oteryn Platform game-auth architecture PR 117
  - Oteryn Platform native OAuth PKCE PR 119
  - Oteryn Platform Game Login Ticket API PR 121
  - Oteryn Platform Game Gateway MVP PR 122
blocks:
  - production cross-repository game-auth E2E until Game Session -> Canary adapter and Phase 7 E2E are proven
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
required_reads:
  - docs/auth/oteryn-identity-login.md
  - docs/agents/CROSS_REPO_CONTRACTS.md
search_first:
  - live Oteryn-Platform Phase 6 Game Session adapter task and PR overlap
  - current GAME_SESSION_CANARY_CONTRACT.md and current Canary auth/session implementation
optional_reads:
  - current Canary LoginSessionManager and account_sessions sources only when Phase 6 implementation begins
---

# Goal

Deliver the OTClient side of Oteryn native game authentication:

`system browser -> Oteryn Identity Authorization Code + PKCE -> Platform Game Login Ticket -> standalone Game Gateway -> one-shot Game Session -> Canary world connection`

The first-party Oteryn flow must not send or persist the user's Oteryn password and must not silently fall back to legacy password authentication.

# Completion

- PR #17 was squash-merged to `main` as `bb87346f6c516a19d19497d82bb01fb389334ff5`.
- Exact final pre-merge head `4e951defadaf796fe931c06beeb75efec40787fe` passed CI run `29910774034`.
- Production world-entry readiness is not claimed; the Game Session -> Canary compatibility adapter remains the next cross-repository gate.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-07-22T11:47:00Z
head: bb87346f6c516a19d19497d82bb01fb389334ff5
branch: main
pr: 17
status: ready
context_routes:
  - auth-identity
  - canary-integration
  - testing
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
proven:
  - PR #17 was squash-merged to main as bb87346f6c516a19d19497d82bb01fb389334ff5.
  - Exact final pre-merge head 4e951defadaf796fe931c06beeb75efec40787fe passed GitHub Actions CI run 29910774034.
  - Linux linux-tests completed CMake, C++ unit tests, Lua tests and integration tests successfully in run 29910774034.
  - The final workflow conclusion was success and included successful Linux release, Windows builds, macOS build, Docker image and browser bundle jobs.
  - PR #17 had no review threads or submitted reviews blocking merge and was mergeable immediately before squash merge.
  - OTClient now uses system-browser Authorization Code + PKCE, Platform ticket issuance, strict Gateway /v1/login, authoritative world_id routing and one-shot GameSessionKey handoff.
  - Oteryn RSA selection occurs only after the Gateway-authoritative worldHost is known, immediately before g_game.loginWorld.
  - The Oteryn flow does not persist the Oteryn password, OAuth token, Game Login Ticket or Game Session credential and does not silently fall back to legacy password auth.
  - The production Game Session -> Canary compatibility adapter remains unresolved and production cross-repository E2E is not proven by this task.
derived:
  - OTClient Phase 5 consumer implementation is complete at merge commit bb87346f6c516a19d19497d82bb01fb389334ff5.
  - Further authentication delivery work belongs to the separately scoped Oteryn Platform/Canary Game Session adapter boundary rather than additional OTClient protocol changes unless new contract evidence requires them.
unknown:
  - The selected production Game Session -> Canary adapter and its exact replay, revocation and world-scoping semantics.
  - Exact production end-to-end readiness across Identity, Gateway, session adapter, Canary and deployed OTClient.
conflicts:
  - none
first_failure:
  marker: none
  evidence: Final exact-head CI run 29910774034 passed and PR #17 merged successfully; no unresolved failure remains in this task.
rejected_hypotheses:
  - Direct ticket-to-login-server flow: current producer contracts require Platform ticket issuance followed by standalone Game Gateway login.
  - Client-authoritative world routing or pre-Gateway RSA selection: Gateway world_id and worldHost are authoritative.
  - Automatic Game Session replay/reconnect: Phase 6 replay semantics remain unresolved, so the OTClient handoff fails closed after first use.
changed_paths:
  - docs/agents/CHANGELOG.md
  - docs/agents/CROSS_REPO_CONTRACTS.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/tasks/active/OTC-20260721-oteryn-identity-login.md
  - docs/auth/oteryn-identity-login.md
  - init.lua
  - modules/client_entergame/characterlist.lua
  - modules/client_entergame/entergame.otmod
  - modules/client_entergame/oteryn_identity.lua
  - modules/client_entergame/oteryn_identity_core.lua
  - modules/corelib/http.lua
  - src/framework/luafunctions.cpp
  - src/framework/net/protocolhttp.h
  - src/framework/net/server.cpp
  - src/framework/net/server.h
  - src/framework/util/crypt.cpp
  - tests/integration/protocol/loopback_packet_test.cpp
  - tests/lua/CMakeLists.txt
  - tests/lua/contracts/oteryn_identity_core_test.lua
validation:
  - command: GitHub Actions CI run 29910774034 on 4e951defadaf796fe931c06beeb75efec40787fe
    result: PASS
    evidence: Workflow completed with conclusion success; linux-tests passed C++ unit, Lua and integration tests and the full platform matrix completed successfully.
  - command: PR #17 autonomous merge gate
    result: PASS
    evidence: PR was mergeable with no review threads or blocking reviews and squash-merged as bb87346f6c516a19d19497d82bb01fb389334ff5.
  - command: python tools/agents/checkpoint.py docs/agents/tasks/active/OTC-20260721-oteryn-identity-login.md --require-checkpoint
    result: PASS
    evidence: Compact checkpoint validation completed successfully before closeout handoff generation.
blockers:
  - none for the completed OTClient task
next_action: Start the separately scoped Oteryn Platform Phase 6 Game Session adapter task from current Platform main after a live overlap and contract preflight.
```
