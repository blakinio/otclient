---
task_id: OTC-20260726-characterlist-recreation
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260726-characterlist-recreation
base_branch: main
created: 2026-07-26T00:46:58+02:00
updated: 2026-07-26T08:23:30+02:00
last_verified_commit: "ce4329ee13b39576915240605c2fe6657096c517"
risk: medium
related_issue: "opentibiabr/otclient#1775 (character-list relog subcase)"
related_pr: "#31"
depends_on: []
blocks:
  - action-bar cooldown lifecycle repair
owned_paths:
  - modules/client_entergame/entergame.otmod
  - modules/client_entergame/characterlist_lifecycle.lua
  - modules/client_entergame/characterlist_lifecycle_core.lua
  - tests/lua/unit/characterlist_lifecycle_test.lua
  - tests/lua/unit/characterlist_lifecycle_adapter_test.lua
  - tests/lua/CMakeLists.txt
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260726-characterlist-recreation.md
modules_touched:
  - client_entergame
reuses:
  - existing CharacterList controller and G.characters/G.characterAccount state
  - existing Lua test runner
public_interfaces: []
cross_repo_tasks: []
---

# Goal

Make the legacy and Oteryn character-list layouts safely reusable after the list window is destroyed, without duplicating login behavior or changing authentication/protocol semantics.

# Acceptance criteria

- [x] Character-list OTUI names are normalized to absolute `/client_entergame/*.otui` paths before deferred callbacks use them.
- [x] The last successfully selected layout is retained for recreation.
- [x] Destroy followed by `showAgain()` recreates the list from `G.characters` and `G.characterAccount`.
- [x] UI load failure is nil-safe and restores the enter-game window instead of indexing a nil widget.
- [x] Legacy `characterlist.otui` and Oteryn `oteryn_characterlist.otui` use the same controller path.
- [x] Focused Lua tests cover default, custom, absolute, missing-layout and repeated recreation decisions.
- [ ] Runtime-root Lua syntax and required CI pass on the exact final head.
- [ ] Full changed-file list and diff are reviewed before squash merge.

# Confirmed context

- PR #26 synchronization, PR #25 audit and archive PR #38 are merged into `main`.
- Current clean base: `ce4329ee13b39576915240605c2fe6657096c517`.
- The reported failure resolves relative `characterlist` as `/characterlist.otui` during a deferred login callback and then indexes a nil `charactersWindow`.
- `CharacterList.destroy()` removes the window and UI references; existing `showAgain()` only acts while the old list widget still exists.
- PR #23 owns enter-game presentation files and also edits `entergame.otmod`; this P1 lifecycle repair changes only one manifest line and will be reconciled into #23 after this repair reaches `main`.
- No Canary, login-server, credential or Oteryn Identity contract changes are required.

# Plan

1. Add a pure path/recreation decision helper with Lua tests.
2. Install a narrow lifecycle adapter after `characterlist.lua` loads.
3. Preserve the original CharacterList controller and wrap only create/destroy/hide/showAgain behavior.
4. Validate syntax, focused tests, complete diff and required CI.
5. Squash-merge and archive the task.

# Work log

## 2026-07-26T00:46:58+02:00

- Claimed the focused P1 lifecycle repair on a branch created from PR #26's exact reviewed tree.
- Determined that a module-local adapter is safer than rewriting the existing large controller.

## 2026-07-26T08:23:30+02:00

- Verified PR #25 merged and released the implementation queue.
- Created backup branch `backup/OTC-20260726-characterlist-recreation-pre-restack` at the original stacked head.
- Restacked PR #31 directly on current `main`, removing 35 unrelated historical files from the proposed diff.
- Created a second clean backup `backup/OTC-20260726-characterlist-recreation-clean-c01a7daa` before refreshing onto archive merge `ce4329ee...`.
- Recreated only the lifecycle helper, adapter, focused tests, manifest load order, CTest registration, changelog and task record.
- Preserved authentication, protocol, login population, sorting, outfits, pinning and reconnect behavior in the existing CharacterList controller.

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| Keep the existing CharacterList controller authoritative | Login, sorting, outfits, pinning and reconnect behavior already exist and must not be duplicated | none |
| Normalize only module-local OTUI names | Both shipped layouts live under `/client_entergame`; absolute paths remain accepted unchanged | none |
| Catch UI creation failures at the adapter boundary | Prevents the known nil dereference and returns the user to a usable login screen | none |
| Force-restack only after creating backup refs | Removes historical stack noise without risking loss of the reviewed implementation | none |

# Validation and CI

| Commit | Check | Result | Evidence |
|---|---|---|---|
| pending | Lua lifecycle unit tests | pending | focused CTest suite |
| pending | Runtime Lua syntax | pending | required CI |
| pending | `CI / Required` | pending | final merge gate |

# Risks and compatibility

- Authentication and protocol payloads are unchanged.
- The adapter preserves custom Oteryn layout selection from PR #23.
- No new assets, settings migration or persisted credentials are introduced.
- Backup branches preserve both the original stacked implementation and the first clean restack until merge completion.
- Rollback is a normal squash revert.

# Remaining work

1. Review the exact eight-file diff.
2. Mark PR #31 ready and pass exact-head required CI/CTest.
3. Squash-merge and archive this task.

# Handoff

## Start here

Open this task and PR #31, then inspect `characterlist_lifecycle*.lua`, `entergame.otmod` and the two focused Lua tests.

## Do not repeat

Do not duplicate `CharacterList` login/population logic or introduce a second character-list controller.

# Completion

- Final status: in progress
- PR: #31
- Merge commit: pending
- Catalogue updated: not applicable; no public reusable interface
- Changelog updated: yes
- Archived at: pending
