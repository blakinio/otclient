---
task_id: OTC-20260726-characterlist-recreation
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260726-characterlist-recreation
base_branch: main
created: 2026-07-26T00:46:58+02:00
updated: 2026-07-26T00:46:58+02:00
last_verified_commit: "4f9958c5b834e911e06ffb5e10f1193400f545e7"
risk: medium
related_issue: "opentibiabr/otclient#1775 (character-list relog subcase)"
related_pr: ""
depends_on:
  - PR #26 synchronization merge
blocks:
  - action-bar cooldown lifecycle repair
owned_paths:
  - modules/client_entergame/entergame.otmod
  - modules/client_entergame/characterlist_lifecycle.lua
  - modules/client_entergame/characterlist_lifecycle_core.lua
  - tests/lua/unit/characterlist_lifecycle_test.lua
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

- [ ] Character-list OTUI names are normalized to absolute `/client_entergame/*.otui` paths before deferred callbacks use them.
- [ ] The last successfully selected layout is retained for recreation.
- [ ] Destroy followed by `showAgain()` recreates the list from `G.characters` and `G.characterAccount`.
- [ ] UI load failure is nil-safe and restores the enter-game window instead of indexing a nil widget.
- [ ] Legacy `characterlist.otui` and Oteryn `oteryn_characterlist.otui` use the same controller path.
- [ ] Focused Lua tests cover default, custom, absolute and repeated recreation decisions.
- [ ] Runtime-root Lua syntax and required CI pass on the exact final head.
- [ ] Full changed-file list and diff are reviewed before squash merge.

# Confirmed context

- Current dependency head: PR #26 exact tree `4f9958c5b834e911e06ffb5e10f1193400f545e7`.
- The reported failure resolves relative `characterlist` as `/characterlist.otui` during a deferred login callback and then indexes a nil `charactersWindow`.
- `CharacterList.destroy()` removes the window and UI references; existing `showAgain()` only acts while the old list widget still exists.
- PR #23 owns enter-game presentation files and also edits `entergame.otmod`; this P1 lifecycle repair changes only one manifest line and will be reconciled into #23 after this repair reaches `main`.
- No Canary, login-server, credential or Oteryn Identity contract changes are required.

# Plan

1. Add a pure path/recreation decision helper with Lua tests.
2. Install a narrow lifecycle adapter after `characterlist.lua` loads.
3. Preserve the original CharacterList controller and wrap only create/destroy/hide/showAgain behavior.
4. Validate syntax, focused tests, complete diff and required CI.
5. Squash-merge after PR #26 is terminal and this branch is current with `main`.

# Work log

## 2026-07-26T00:46:58+02:00

- Changed: claimed the focused P1 lifecycle repair on a branch created from PR #26's exact reviewed tree.
- Learned: the smallest safe implementation is a module-local adapter; rewriting the 1,100-line controller is unnecessary and would increase regression risk.
- Dependency: PR #26 remains under required exact-head CI with auto-merge enabled.

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| Keep the existing CharacterList controller authoritative | Login, sorting, outfits, pinning and reconnect behavior already exist and must not be duplicated | none |
| Normalize only module-local OTUI names | Both shipped layouts live under `/client_entergame`; absolute paths remain accepted unchanged | none |
| Catch UI creation failures at the adapter boundary | Prevents the known nil dereference and returns the user to a usable login screen | none |

# Validation and CI

| Commit | Check | Result | Evidence |
|---|---|---|---|
| pending | Lua lifecycle unit tests | not-run | focused CTest suite |
| pending | Runtime Lua syntax | not-run | required CI |
| pending | `CI / Required` | not-run | final merge gate |

# Risks and compatibility

- Authentication and protocol payloads are unchanged.
- The adapter must preserve custom Oteryn layout selection from PR #23.
- No new assets, settings migration or persisted credentials are introduced.
- Rollback is a normal squash revert.

# Remaining work

1. Implement helper, adapter, tests and manifest load order.

# Handoff

## Start here

Open this task and the draft PR, then inspect `characterlist_lifecycle*.lua`, `entergame.otmod` and the focused Lua test.

## Do not repeat

Do not duplicate `CharacterList` login/population logic or introduce a second character-list controller.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Catalogue updated: not applicable; no public reusable interface
- Changelog updated: pending
- Archived at: pending
