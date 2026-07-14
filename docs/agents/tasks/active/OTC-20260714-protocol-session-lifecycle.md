---
task_id: OTC-20260714-protocol-session-lifecycle
coordination_id: OTS-20260714-protocol-session-lifecycle
status: in_progress
agent: ChatGPT
branch: fix/protocol-game-session-lifecycle
base_branch: main
created: 2026-07-14T07:04:45Z
updated: 2026-07-14T07:15:00Z
last_verified_commit: "b6c8533152d6c25a02a84f197adfd5b5ec41e118"
risk: medium
related_issue: "blakinio/canary#245"
related_pr: "blakinio/otclient#7"
depends_on: []
blocks:
  - blakinio/canary#245
owned_paths:
  - src/client/protocolgame.cpp
  - src/client/protocolgamecallbackguard.h
  - src/framework/net/protocol.cpp
  - tests/unit/protocol/**
  - docs/agents/tasks/active/OTC-20260714-protocol-session-lifecycle.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
modules_touched:
  - Game protocol lifecycle
  - Protocol callback dispatch
reuses:
  - existing Protocol weak ownership
  - existing GoogleTest protocol target
public_interfaces:
  - otclient::detail::runIfCurrentProtocolGame
cross_repo_tasks:
  - CAN-20260713-universal-agent-e2e-platform
---

# Goal

Prevent delayed callbacks from an obsolete `ProtocolGame` instance from disconnecting or mutating a newer active game session in the same OTClient process.

# Acceptance criteria

- [x] Connection errors validate the exact source `ProtocolGame` before entering global `Game` handling.
- [x] Obsolete source protocols cannot disconnect or reset the current protocol.
- [x] Current-protocol errors retain existing handling and disconnect behavior.
- [x] Deferred proxy/player callbacks retain safe ownership and do not capture raw `this` implicitly.
- [x] Deterministic regression tests cover stale/current/null/duplicate callbacks without sleeps.
- [ ] Relevant unit, protocol, integration and sanitizer validation completed or exact unavailable environment documented.
- [x] Module catalogue impact handled.
- [x] Documentation/changelog impact handled.
- [x] Cross-repository impact documented for Canary PR #245.
- [ ] Autonomous merge gate satisfied.

# Confirmed context

- `Game::loginWorld()` replaces `m_protocolGame` with a new shared `ProtocolGame`.
- Native `Protocol::connect()` protects callback lifetime with `weak_ptr`, but the old `ProtocolGame::onError()` discarded source identity before calling global `Game::processConnectionError()`.
- `Game::processConnectionError()` only checks `m_protocolGame != nullptr`; without an identity guard it can act on a replacement session.
- `Protocol::onProxyPacket()`, `onLocalDisconnected()` and `onPlayerPacket()` previously created a local shared owner but posted lambdas with `[&]`, so the queued callback itself retained only raw `this` access.
- Canary PR #245 needs two login/logout cycles in one physical-client process and must consume the fixed OTClient revision after merge.

# Existing work to reuse

| Module/task/PR | Reuse | Evidence/path | Why it fits |
|---|---|---|---|
| Client test foundation PR #3 | Existing GoogleTest targets, CTest labels and protocol test directory | `tests/unit/protocol/**`, `tests/CMakeLists.txt` | Avoids a parallel test harness. |
| Protocol weak ownership | `std::weak_ptr<Protocol>` error/connect callbacks | `src/framework/net/protocol.cpp` | Native transport lifetime protection remains valid; the fix adds missing session identity semantics. |

# Ownership and overlap check

- Open PRs inspected: none in `blakinio/otclient` at task start.
- Active tasks inspected: coordination index is stale; live PR state is authoritative.
- Overlaps: Canary PR #245 consumes OTClient but does not own OTClient source paths.
- Resolution: implement only in `blakinio/otclient`; Canary changes remain outside this PR.

# Current state

Implementation, deterministic tests, catalogue entry and changelog are present in PR #7. Final GitHub CI is running on the current branch head.

# Plan

1. Validate the source protocol at the `ProtocolGame::onError()` boundary before any global `Game` callback.
2. Retain explicit shared ownership in deferred proxy/player callbacks.
3. Exercise the exact identity guard deterministically through the existing protocol GoogleTest target.
4. Inspect final CI and diff, repair failures if required, update evidence, squash-merge, and hand off the merged OTClient revision to Canary PR #245.

# Work log

## 2026-07-14T07:04:45Z

- Changed: created branch and claimed lifecycle/test paths.
- Learned: no open OTClient PR overlaps this work.
- Failed/blocked: none.
- Result: implementation could proceed.

## 2026-07-14T07:15:00Z

- Changed: added `runIfCurrentProtocolGame`, guarded `ProtocolGame::onError()`, replaced deferred `[&]` captures with explicit shared `self`, and added three deterministic lifecycle regression tests.
- Learned: no `Game` signature change is necessary when stale callbacks are rejected before crossing into global `Game`; current callbacks still use the unchanged production path.
- Failed/blocked: local checkout/build is unavailable in this environment because outbound GitHub DNS is unavailable; repository CI is authoritative.
- Result: PR #7 is ready for final CI validation.

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| Compare exact shared `ProtocolGame` identity rather than add timers or relog flags | Fixes ownership semantics directly and is deterministic | none |
| Reject stale callbacks at the `ProtocolGame` → global `Game` boundary | Prevents every global side effect while preserving the existing current-session path and avoiding a broader `Game` API change | none |
| Capture `shared_ptr<Protocol>` explicitly in posted proxy/player lambdas | Ensures the queued operation owns the object it accesses; a local unused `self` did not provide that guarantee | none |
| Keep Canary unchanged in this PR | Root cause is client lifecycle; cross-repo rollout follows after merge | none |

# Files and interfaces

| Path/interface/config/schema | Purpose | Status |
|---|---|---|
| `src/client/protocolgamecallbackguard.h` | Exact shared-instance callback gate | implemented |
| `ProtocolGame::onError` | Reject obsolete source callbacks before global `Game` handling | implemented |
| deferred `Protocol` callbacks | Capture and dereference shared `self` explicitly | implemented |
| `protocol_game_lifecycle_test.cpp` | Stale/current/null/duplicate callback regression | implemented |
| protocol test CMake target | Register regression in existing `unit;protocol` target | implemented |

# Validation and CI

| Commit | Command/check/workflow | Result | Evidence/notes |
|---|---|---|---|
| `b6c8533152d6c25a02a84f197adfd5b5ec41e118` | PR #7 diff review | passed | Eight intended files; no Canary, workflow, asset or unrelated runtime changes. |
| `b6c8533152d6c25a02a84f197adfd5b5ec41e118` | GitHub CI run #33 | running | Final result pending. |
| environment | local configure/build/test | unavailable | Container cannot resolve `github.com`; no local repository checkout/toolchain available. |

Never write `passed` without verification.

# Failed approaches and dead ends

- Direct local clone was attempted but failed because the execution container could not resolve `github.com`; no test result is inferred from that failure.
- A broader `Game::processConnectionError(source, error)` API change was considered but was unnecessary once the exact source is rejected synchronously before global handling. The narrower boundary guard preserves existing current-session semantics.

# Risks and compatibility

- Runtime: lifecycle change affects error handling only; exact pointer equality preserves current-session failures and suppresses only obsolete sources.
- Data/migration: none.
- Security: eliminates stale asynchronous mutation and raw-lifetime callback risk.
- Backward compatibility: no wire-protocol, Lua API, asset or server behavior change.
- Cross-repo rollout: Canary physical E2E must update its controlled OTClient revision/image after merge and rerun the two-session scenario.
- Rollback: revert the single squash commit if regressions appear.

# Remaining work

1. Wait for final current-head CI, repair any failure, then update final evidence and merge PR #7.

# Handoff

## Start here

Use the final merged OTClient commit from PR #7 in Canary PR #245, then rerun the physical `login → safe logout → login → safe logout` scenario in one client process.

## Do not repeat

Do not add relog timers, retry loops, `isRelogging` flags, time-window suppression, or a second protocol callback guard.

## Required reads

- `AGENTS.md`
- `docs/agents/README.md`
- `docs/agents/MODULE_CATALOG.md`
- `src/client/protocolgame.cpp`
- `src/client/protocolgamecallbackguard.h`
- `src/framework/net/protocol.cpp`
- `tests/unit/protocol/protocol_game_lifecycle_test.cpp`

## Open questions

- Whether Canary PR #245 pins OTClient by commit, image tag, or workflow input must be confirmed in that repository after this PR merges.

# Completion

- Final status: in progress
- PR: https://github.com/blakinio/otclient/pull/7
- Merge commit:
- Catalogue updated: yes
- Changelog updated: yes
- Archived at:
