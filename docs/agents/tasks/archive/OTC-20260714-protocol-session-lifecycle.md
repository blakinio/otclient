---
task_id: OTC-20260714-protocol-session-lifecycle
coordination_id: OTS-20260714-protocol-session-lifecycle
status: completed
agent: ChatGPT
branch: fix/protocol-game-session-lifecycle
base_branch: main
created: 2026-07-14T07:04:45Z
updated: 2026-07-14T08:32:22Z
last_verified_commit: "3cb61bb40eded11dc1e7c2d6660a46772364f6d4"
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
- [x] Required unit, protocol, Lua, integration and platform CI passed.
- [x] Optional ASAN/UBSAN status documented accurately.
- [x] Module catalogue and changelog updated.
- [x] Cross-repository impact documented for Canary PR #245.
- [x] Autonomous merge gate satisfied.

# Root cause

Native connection callbacks retained protocol lifetime with a weak reference, but `ProtocolGame::onError()` discarded the identity of the callback's source before entering global `Game::processConnectionError()`. That global handler only checked whether any `m_protocolGame` existed and then disconnected whichever instance was current. A delayed callback from protocol A could therefore disconnect replacement protocol B.

The proxy and packet-player paths also created a local shared `self` but posted lambdas using `[&]`. The queued callbacks did not capture that owner and accessed protocol members through raw `this`.

# Implemented solution

- Added `otclient::detail::runIfCurrentProtocolGame()` to compare exact shared protocol identity.
- `ProtocolGame::onError()` now enters global `Game` handling only when its source instance is still `g_game.getProtocolGame()`.
- Current-session errors preserve the existing global error/disconnect path.
- Every source protocol still disconnects its own connection after error handling.
- `Protocol::onProxyPacket()`, `onLocalDisconnected()` and `onPlayerPacket()` now explicitly capture and dereference shared `self` in posted callbacks.
- No timers, retries, relog flags, time-window suppression or Canary workaround were added.

# Files and interfaces

| Path/interface | Purpose |
|---|---|
| `src/client/protocolgamecallbackguard.h` | Exact source/current shared-instance callback gate. |
| `ProtocolGame::onError` | Reject obsolete callbacks before global game-state handling. |
| `src/framework/net/protocol.cpp` deferred callbacks | Retain explicit shared ownership for queued proxy/player work. |
| `tests/unit/protocol/protocol_game_lifecycle_test.cpp` | Deterministic stale/current/null/duplicate regression coverage. |
| `tests/unit/protocol/CMakeLists.txt` | Registers cases in the existing `unit;protocol` target. |

# Validation and CI

Final PR head: `d19068e574e8e6b3a0299b3b117a24d0952a53ab`.

GitHub CI run #34 completed successfully:

- build-scope detection;
- syntax/workflow validation;
- informational static analysis;
- Lua syntax;
- Linux `linux-tests` configure/build;
- C++ unit tests;
- Lua tests;
- integration tests;
- Linux release;
- Windows CMake release;
- Windows CMake tests and CTest;
- Windows solution variants;
- browser bundle;
- Docker image;
- final required gate.

The full diff contained eight intended files and no Canary, workflow, asset, wire-protocol or unrelated runtime changes. No review threads or requested changes were outstanding.

ASAN/UBSAN were not run. They are optional manual workflows and were not part of the required PR CI. A local checkout/build was unavailable because the execution container could not resolve `github.com`; no local pass was claimed.

# Decisions

| Decision | Reason |
|---|---|
| Reject stale callbacks at the `ProtocolGame` to global `Game` boundary | Prevents every global side effect while preserving the existing current-session API and behavior. |
| Compare exact shared pointer identity | Provides deterministic session ownership without timing heuristics. |
| Capture shared `self` in queued protocol callbacks | Ensures asynchronous work owns the object it accesses. |
| Keep Canary unchanged in this PR | The defect was in OTClient lifecycle semantics; Canary only needs to consume the fixed client revision. |

# Risks and compatibility

- No wire-protocol, Lua API, asset or server behavior changed.
- Exact pointer equality suppresses only callbacks from obsolete sessions.
- Existing single-session error handling remains active for the current protocol.
- Rollback is the single squash commit from PR #7.

# Canary handoff

Canary PR #245 must consume OTClient commit `3cb61bb40eded11dc1e7c2d6660a46772364f6d4` or an image built from it and rerun the physical scenario:

`login → stable marker → safe logout → persistence ready → second login in the same client process → stable marker → safe logout`.

Do not add relog timers, retry windows, `isRelogging` flags or server-side disconnect workarounds. If the scenario still fails, capture the exact callback/error source, client log, server session identifiers/timestamps and packet-record boundary.

# Completion

- Final status: completed
- PR: https://github.com/blakinio/otclient/pull/7
- Squash commit: `3cb61bb40eded11dc1e7c2d6660a46772364f6d4`
- CI: run #34 passed
- Catalogue updated: yes
- Changelog updated: yes
- Archived at: `docs/agents/tasks/archive/OTC-20260714-protocol-session-lifecycle.md`
