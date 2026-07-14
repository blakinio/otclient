---
task_id: OTC-20260714-protocol-session-reentrancy
coordination_id: OTS-20260714-protocol-session-lifecycle
status: in_progress
agent: ChatGPT
branch: fix/protocol-game-session-reentrancy
base_branch: main
created: 2026-07-14T08:45:00Z
updated: 2026-07-14T10:00:00Z
last_verified_commit: "afbaee5b9086b43e641a1eb5ff1c4be357278d45"
risk: medium
related_issue: "blakinio/canary#245"
related_pr: "blakinio/otclient#9"
depends_on:
  - blakinio/otclient#7
blocks:
  - blakinio/canary#245
owned_paths:
  - src/client/game.cpp
  - src/client/game.h
  - src/client/protocolgame.cpp
  - src/client/protocolgamecallbackguard.h
  - tests/unit/protocol/**
  - docs/agents/tasks/active/OTC-20260714-protocol-session-reentrancy.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - docs/agents/CROSS_REPO_CONTRACTS.md
modules_touched:
  - Game protocol lifecycle
reuses:
  - protocol callback identity fix from PR #7
  - existing GoogleTest protocol target
public_interfaces:
  - otclient::detail::isCurrentProtocolGame
  - otclient::detail::runWhileCurrentProtocolGame
cross_repo_tasks:
  - CAN-20260713-universal-agent-e2e-platform
---

# Goal

Complete the protocol-session identity fix by carrying the source `ProtocolGame` through `Game::processConnectionError()`, game-end cleanup and disconnect handling, including identity revalidation after Lua callbacks.

# Acceptance criteria

- [x] Stale protocols cannot enter global error handling or disconnect a replacement session.
- [x] Source/current identity is checked again after `onConnectionError`, `onGameEnd` and `onConnectionFailing` Lua callbacks.
- [x] Explicit cancel, force logout and safe logout operate on the protocol captured at operation start.
- [x] State-reset callback boundaries stop cleanup when the source protocol has been replaced.
- [x] Deterministic tests exercise stale/current/null/replacement source handling through the production `Game` lifecycle methods and guard helpers.
- [x] Module catalogue, changelog and cross-repository rollout contract are updated.
- [ ] Required CI passes on the final current head.
- [ ] PR is squash-merged and the final Canary handoff identifies the superseding commit.

# Confirmed context

PR #7 rejects callbacks that are already stale before entering `Game`, but its implementation discarded source identity inside `Game::processConnectionError()`. That function invoked Lua and then called a no-argument `processDisconnect()` against global `m_protocolGame`. A synchronous Lua callback could therefore clear protocol A, start replacement protocol B and let the outer handler disconnect B.

The same global lookup existed after `onGameEnd` and in explicit logout paths. The complete fix must retain one captured `ProtocolGamePtr` through the operation and re-check exact shared-instance identity after every relevant reentrant boundary.

# Existing work reused

| Work | Reuse | Evidence |
|---|---|---|
| OTClient PR #7 | Exact pointer guard and deferred callback ownership fix | `src/client/protocolgamecallbackguard.h`, `src/framework/net/protocol.cpp` |
| Client test foundation | Existing `otclient_protocol_contract_tests` target and `unit;protocol` labels | `tests/unit/protocol/CMakeLists.txt` |

# Implementation

- `ProtocolGame::onError()` passes its exact shared instance into `Game` instead of performing only an outer guard.
- `Game::processConnectionError()`, `processDisconnect()` and `processGameEnd()` require the captured source protocol.
- `runWhileCurrentProtocolGame()` validates identity both before and after a callback.
- Game-end and connection-error Lua callbacks cannot resume cleanup against a replacement session.
- `resetGameStates(source)` snapshots containers and stops after callback-capable close/cancel operations when the source is no longer current.
- `cancelLogin()`, `forceLogout()` and `safeLogout()` capture `m_protocolGame` once and never switch to a later global protocol during the operation.

# Decisions

| Decision | Reason |
|---|---|
| Carry `ProtocolGamePtr`, not a boolean relog flag or timestamp | Exact ownership identity addresses the race without timing assumptions. |
| Revalidate after Lua callbacks | Lua can synchronously call lifecycle methods and begin another login before the outer C++ stack resumes. |
| Keep the wire protocol and Canary server unchanged | The defect is entirely in client-side lifecycle ownership. |
| Extend the merged guard instead of adding another lifecycle framework | Avoids duplicate abstractions and preserves PR #7 ownership fixes. |

# Work log

## 2026-07-14T08:45:00Z

- Created draft PR #9 after post-merge review of PR #7 found the Lua-reentrancy gap.
- Claimed the game/protocol lifecycle and existing protocol-test paths.

## 2026-07-14T10:00:00Z

- Carried source identity through connection-error, game-end and disconnect handling.
- Added before/after callback validation and source-aware state cleanup.
- Captured source protocol in all explicit logout operations.
- Replaced helper-only coverage with direct deterministic `Game` lifecycle tests plus callback-replacement guard coverage.
- Updated catalogue, changelog and the Canary rollout contract.
- A temporary read-only source-export workflow was used to obtain a complete source snapshot in the restricted execution environment; it is removed by the implementation commit and is not part of the intended final diff.

# Validation and CI

| Commit | Check | Result | Notes |
|---|---|---|---|
| `afbaee5b9086b43e641a1eb5ff1c4be357278d45` | Base review | passed | PR #8 archived the prior lifecycle task; no overlapping open OTClient PR exists. |
| implementation staging | Source call-site inventory | passed | All `processConnectionError`, `processDisconnect` and `processGameEnd` call sites now carry the captured source. |
| implementation staging | Deterministic test review | passed | Tests cover stale/current disconnect, stale/current EOF handling, stale game end and callback replacement. |
| final PR head | GitHub CI | pending | Required Linux/Windows builds and test jobs must pass before merge. |
| environment | Local configure/build/test | unavailable | The execution container cannot resolve GitHub/vcpkg dependencies; no local build result is claimed. GitHub CI is authoritative. |

# Risks and compatibility

- Runtime: current-session errors and explicit logout retain their existing visible behavior; only operations whose source is obsolete are suppressed.
- Reentrancy: cleanup aborts instead of touching a replacement session when Lua or close/cancel callbacks change the current protocol.
- Protocol: no opcode, field, feature flag, protobuf, authentication payload or version-gate change.
- Server: Canary requires no server code change for this fix.
- Rollout: client-first-safe; Canary PR #245 must consume the final merged OTClient commit/image before the two-session physical proof.
- Rollback: revert the final squash commit; no migration or persisted data change exists.

# Remaining work

1. Push the implementation and remove the temporary source-export workflow.
2. Inspect the complete PR diff and current-head CI.
3. Repair any real CI failure, then mark ready and squash-merge.
4. Archive this task with the final merge SHA and give Canary PR #245 the final consumer handoff.

# Handoff

## Start here

After PR #9 merges, use its squash commit rather than PR #7 commit `3cb61bb40eded11dc1e7c2d6660a46772364f6d4` in Canary PR #245.

## Required physical proof

Run one client process through:

`login A -> stable marker -> safe logout -> persistence ready -> login B -> stable marker -> safe logout`

Retain client logs, server logs, packet records and the E2E result artifact. Confirm that delayed callbacks from A do not emit connection/game-end effects for B and do not clear B's active protocol.

## Do not repeat

Do not add relog delays, retry windows, `isRelogging`, timer suppression, server-side disconnect workarounds or another callback guard.

# Completion

- Final status: in progress
- PR: https://github.com/blakinio/otclient/pull/9
- Merge commit:
- Catalogue updated: yes
- Changelog updated: yes
- Cross-repo contract updated: yes
- Archived at:
