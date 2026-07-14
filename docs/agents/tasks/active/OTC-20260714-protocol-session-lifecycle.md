---
task_id: OTC-20260714-protocol-session-lifecycle
coordination_id: OTS-20260714-protocol-session-lifecycle
status: in_progress
agent: ChatGPT
branch: fix/protocol-game-session-lifecycle
base_branch: main
created: 2026-07-14T07:04:45Z
updated: 2026-07-14T07:04:45Z
last_verified_commit: ""
risk: medium
related_issue: "blakinio/canary#245"
related_pr: ""
depends_on: []
blocks:
  - blakinio/canary#245
owned_paths:
  - src/client/game.cpp
  - src/client/game.h
  - src/client/protocolgame.cpp
  - src/framework/net/protocol.cpp
  - tests/unit/protocol/**
  - docs/agents/tasks/active/OTC-20260714-protocol-session-lifecycle.md
  - docs/agents/CHANGELOG.md
modules_touched:
  - Game protocol lifecycle
  - Protocol callback dispatch
reuses:
  - existing Protocol weak ownership
  - existing GoogleTest protocol target
public_interfaces: []
cross_repo_tasks:
  - CAN-20260713-universal-agent-e2e-platform
---

# Goal

Prevent delayed callbacks from an obsolete `ProtocolGame` instance from disconnecting or mutating a newer active game session in the same OTClient process.

# Acceptance criteria

- [ ] Connection errors carry the source `ProtocolGame` identity into `Game`.
- [ ] Obsolete source protocols cannot disconnect or reset the current protocol.
- [ ] Current-protocol errors and explicit logout paths retain existing behavior.
- [ ] Deferred proxy/player callbacks retain safe ownership and do not capture raw `this` implicitly.
- [ ] Deterministic regression tests cover stale/current callbacks without sleeps.
- [ ] Relevant unit, protocol, integration and sanitizer validation completed or exact unavailable environment documented.
- [ ] Module catalogue impact handled or none.
- [ ] Documentation/changelog impact handled or none.
- [ ] Cross-repository impact documented for Canary PR #245.
- [ ] Autonomous merge gate satisfied.

# Confirmed context

- `Game::loginWorld()` replaces `m_protocolGame` with a new shared `ProtocolGame`.
- Native `Protocol::connect()` protects callback lifetime with `weak_ptr`, but `ProtocolGame::onError()` discards the source identity before calling global `Game::processConnectionError()`.
- Current `Game::processConnectionError()` only checks `m_protocolGame != nullptr`; `processDisconnect()` therefore acts on whichever protocol is current when a delayed callback runs.
- `Protocol::onProxyPacket()`, `onLocalDisconnected()` and `onPlayerPacket()` create a local shared owner but post lambdas with `[&]`, leaving asynchronous work able to use raw `this`.
- Canary PR #245 needs two login/logout cycles in one physical-client process and must consume the fixed OTClient revision after merge.

# Existing work to reuse

| Module/task/PR | Reuse | Evidence/path | Why it fits |
|---|---|---|---|
| Client test foundation PR #3 | Existing GoogleTest targets, CTest labels and protocol test directory | `tests/unit/protocol/**`, `tests/CMakeLists.txt` | Avoids a parallel test harness. |
| Protocol weak ownership | `std::weak_ptr<Protocol>` error/connect callbacks | `src/framework/net/protocol.cpp` | Lifetime protection remains valid; only session identity propagation is missing. |

# Ownership and overlap check

- Open PRs inspected: none in `blakinio/otclient` at task start.
- Active tasks inspected: coordination index is stale; live PR state is authoritative.
- Overlaps: Canary PR #245 consumes OTClient but does not own OTClient source paths.
- Resolution: implement only in `blakinio/otclient`; Canary changes remain outside this PR.

# Current state

Branch and task record created. Source and test changes pending.

# Plan

1. Propagate source protocol identity through error/disconnect handling.
2. Make disconnect/reset operations identity-safe across Lua reentrancy.
3. Fix deferred proxy/player callback ownership.
4. Add deterministic lifecycle regression tests using the existing protocol test target.
5. Run CI, repair failures, document results, merge, and hand off the OTClient commit to Canary PR #245.

# Work log

## 2026-07-14T07:04:45Z

- Changed: created branch and claimed lifecycle/test paths.
- Learned: no open OTClient PR overlaps this work.
- Failed/blocked: none.
- Result: implementation can proceed.

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| Compare exact `ProtocolGamePtr` identity rather than add timers or relog flags | Fixes ownership semantics directly and is deterministic | none |
| Re-check identity after Lua callbacks | Lua callbacks can synchronously re-enter game lifecycle | none |
| Keep Canary unchanged in this PR | Root cause is client lifecycle; cross-repo rollout follows after merge | none |

# Files and interfaces

| Path/interface/config/schema | Purpose | Status |
|---|---|---|
| `Game::processConnectionError` | Add source-protocol identity validation | planned |
| `Game::processDisconnect` | Reset only the matching active protocol | planned |
| `ProtocolGame::onError` | Pass the exact source protocol | planned |
| deferred `Protocol` callbacks | Capture shared self explicitly | planned |
| protocol lifecycle test | Deterministic stale/current callback regression | planned |

# Validation and CI

| Commit | Command/check/workflow | Result | Evidence/notes |
|---|---|---|---|
| | GitHub CI | not-run | implementation pending |

Never write `passed` without verification.

# Failed approaches and dead ends

None.

# Risks and compatibility

- Runtime: lifecycle change affects error/logout handling; identity checks must not suppress current-session failures.
- Data/migration: none.
- Security: eliminates stale asynchronous mutation and raw-lifetime callback risk.
- Backward compatibility: no wire-protocol change; single-session login behavior must remain unchanged.
- Cross-repo rollout: Canary physical E2E must update its controlled OTClient revision/image after merge.
- Rollback: revert the single squash commit if regressions appear.

# Remaining work

1. Implement source identity propagation and regression tests.

# Handoff

## Start here

Read the confirmed call chain and inspect the final PR diff/CI before updating Canary PR #245.

## Do not repeat

Do not add relog timers, retry loops, `isRelogging` flags, or time-window suppression.

## Required reads

- `AGENTS.md`
- `docs/agents/README.md`
- `docs/agents/MODULE_CATALOG.md`
- `src/client/game.{h,cpp}`
- `src/client/protocolgame.cpp`
- `src/framework/net/protocol.cpp`
- existing protocol tests

## Open questions

- Whether Canary PR #245 pins OTClient by commit, image tag, or workflow input must be confirmed in that repository after this PR merges.

# Completion

- Final status: in progress
- PR:
- Merge commit:
- Catalogue updated: not required unless a reusable public interface is added
- Changelog updated: pending
- Archived at:
