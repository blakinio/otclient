---
task_id: OTC-20260714-protocol-session-reentrancy
coordination_id: OTS-20260714-protocol-session-lifecycle
status: in_progress
agent: ChatGPT
branch: fix/protocol-game-session-reentrancy
base_branch: main
created: 2026-07-14T08:45:00Z
updated: 2026-07-14T08:45:00Z
last_verified_commit: "3cb61bb40eded11dc1e7c2d6660a46772364f6d4"
risk: medium
related_issue: "blakinio/canary#245"
related_pr: ""
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
modules_touched:
  - Game protocol lifecycle
reuses:
  - protocol callback identity fix from PR #7
  - existing GoogleTest protocol target
public_interfaces: []
cross_repo_tasks:
  - CAN-20260713-universal-agent-e2e-platform
---

# Goal

Complete the protocol-session identity fix by carrying the source `ProtocolGame` through `Game::processConnectionError()` and `Game::processDisconnect()`, including identity revalidation after Lua callbacks.

# Acceptance criteria

- [ ] Stale protocols cannot enter global error handling or disconnect a replacement session.
- [ ] Source/current identity is checked again after `onConnectionError` and `onGameEnd` Lua callbacks.
- [ ] Explicit cancel/force logout disconnect only the protocol captured at operation start.
- [ ] Deterministic tests exercise stale/current/duplicate source handling.
- [ ] Required CI passes and PR is squash-merged.
- [ ] Canary handoff identifies the final superseding commit.

# Confirmed context

PR #7 rejects callbacks that are already stale before entering `Game`, but `Game::processConnectionError()` still operates on global `m_protocolGame` after invoking Lua. A Lua callback can synchronously clear the old protocol and begin another login before the outer handler resumes, allowing the outer `processDisconnect()` to act on the replacement. The source identity therefore must remain part of the complete call chain.

# Plan

1. Add source-aware overloads/signatures in `Game`.
2. Revalidate exact identity at entry and after Lua-reentrant boundaries.
3. Capture source protocol in explicit logout paths.
4. Replace helper-only tests with direct `Game` lifecycle tests.
5. Run full CI, merge, archive the task and update the Canary handoff.

# Validation and CI

| Commit | Check | Result | Notes |
|---|---|---|---|
| | GitHub CI | not-run | implementation pending |

# Risks and compatibility

- No wire-protocol or server change.
- Current-session errors and logouts must preserve existing behavior.
- The final Canary consumer commit will supersede `3cb61bb40eded11dc1e7c2d6660a46772364f6d4`.

# Completion

- Final status: in progress
- PR:
- Merge commit:
- Archived at:
