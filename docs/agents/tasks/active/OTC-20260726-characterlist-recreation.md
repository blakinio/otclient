---
task_id: OTC-20260726-characterlist-recreation
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260726-characterlist-recreation
base_branch: main
created: 2026-07-26T00:46:58+02:00
updated: 2026-07-26T08:55:00+02:00
last_verified_commit: "841031a129c3148e425de819abe907d8bc3f2e32"
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
- [x] Focused Lua tests cover default, custom, absolute, root-resolving, missing-layout and repeated recreation decisions.
- [ ] Runtime-root Lua syntax and required CI pass on the exact final head.
- [x] Full changed-file list and diff are reviewed before squash merge.

# Confirmed context

- PR #26 synchronization, PR #25 audit and archive PR #38 are merged into `main`.
- Current clean base: `ce4329ee13b39576915240605c2fe6657096c517`.
- The reported failure resolves relative `characterlist` as `/characterlist.otui` during a deferred login callback and then indexes a nil `charactersWindow`.
- `CharacterList.destroy()` removes the window and UI references; existing `showAgain()` only acts while the old list widget still exists.
- PR #23 owns enter-game presentation files and also edits `entergame.otmod`; this P1 lifecycle repair changes only one manifest line and will be reconciled into #23 after this repair reaches `main`.
- No Canary, login-server, credential or Oteryn Identity contract changes are required.

# Implementation

- Relative layout requests are validated from the caller-provided module-local name and always anchored under `/client_entergame/`.
- An absolute path returned by `guessFilePath` for a relative request is never trusted as the resource root; this directly covers the observed `/characterlist.otui` failure.
- Explicit absolute layouts remain supported after traversal validation.
- The adapter preserves the last successful layout and recreates through the existing CharacterList controller.

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

## 2026-07-26T08:55:00+02:00

- Source review reproduced the important resolver behavior: a relative request may be returned as `/characterlist.otui`.
- Corrected normalization so relative requests are anchored from their validated module-local name rather than trusting a root-level resolver result.
- Added focused coverage for both legacy and Oteryn layouts when the resolver returns root-level paths.

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| Keep the existing CharacterList controller authoritative | Login, sorting, outfits, pinning and reconnect behavior already exist and must not be duplicated | none |
| Anchor relative requests from the validated request name | The resource resolver may return `/characterlist.otui`, which is exactly the failing path | none |
| Preserve explicit absolute layouts | PR #23 and future module callers may already pass a fully qualified shipped layout | none |
| Catch UI creation failures at the adapter boundary | Prevents the known nil dereference and returns the user to a usable login screen | none |
| Force-restack only after creating backup refs | Removes historical stack noise without risking loss of the reviewed implementation | none |

# Validation and CI

| Commit | Check | Result | Evidence |
|---|---|---|---|
| `841031a129c3148e425de819abe907d8bc3f2e32` | root-resolving layout regression | pending | focused CTest suite |
| pending final head | Runtime Lua syntax | pending | required CI |
| pending final head | Windows CMake Tests / CTest | pending | required CI |
| pending final head | `CI / Required` | pending | final merge gate |

# Risks and compatibility

- Authentication and protocol payloads are unchanged.
- The adapter preserves custom Oteryn layout selection from PR #23.
- No new assets, settings migration or persisted credentials are introduced.
- Backup branches preserve both the original stacked implementation and the first clean restack until merge completion.
- Rollback is a normal squash revert.

# Remaining work

1. Pass exact-head required CI/CTest.
2. Verify reviews and stable base, then squash-merge.
3. Archive this task.

# Handoff

Open this task and PR #31, then inspect `characterlist_lifecycle*.lua`, `entergame.otmod` and both focused Lua tests. Do not duplicate CharacterList login/population logic or introduce a second controller.

# Completion

- Final status: in progress
- PR: #31
- Merge commit: pending
- Catalogue updated: not applicable; no public reusable interface
- Changelog updated: yes
- Archived at: pending