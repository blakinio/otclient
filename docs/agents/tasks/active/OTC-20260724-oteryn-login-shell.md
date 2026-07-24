---
task_id: OTC-20260724-oteryn-login-shell
coordination_id: OTS-20260721-oteryn-identity-auth
status: awaiting_visual_review
agent: "GPT-5.6 Thinking"
branch: feat/OTC-20260724-oteryn-login-shell
base_branch: main
created: 2026-07-24T21:44:57Z
updated: 2026-07-24T21:58:34Z
last_verified_commit: 83203ca8521d414e274285e3aaa80aa5a7b1a139
risk: low
related_issue: ""
related_pr: "#23"
depends_on:
  - merged Oteryn native identity login PR #17
blocks:
  - runtime visual approval before merge
owned_paths:
  - modules/client_entergame/entergame.otui
  - modules/client_entergame/entergame.otmod
  - modules/client_entergame/oteryn_login_theme.lua
  - modules/client_entergame/oteryn_characterlist.otui
  - docs/agents/ACTIVE_WORK.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260724-oteryn-login-shell.md
modules_touched:
  - client_entergame
reuses:
  - existing Oteryn Identity Authorization Code + PKCE flow
  - existing CharacterList controller and login handoff
public_interfaces:
  - Oteryn-specific login shell and character-list OTUI surface
cross_repo_tasks: []
required_reads:
  - modules/client_entergame/entergame.otui
  - modules/client_entergame/oteryn_identity.lua
  - modules/client_entergame/characterlist.lua
search_first:
  - existing enter-game and character-list widget IDs and lifecycle
optional_reads: []
---

# Oteryn login shell prototype

## Goal

Create a reversible OTUI/Lua-only visual prototype for the existing secure Oteryn login flow, using the supplied dark navy, blue and antique-gold direction without changing authentication or protocol behavior.

## Acceptance criteria

- [x] Existing Oteryn OAuth/PKCE behavior remains unchanged.
- [x] Legacy server password login remains available and keeps every widget ID required by `entergame.lua`.
- [x] Oteryn mode presents a modern branded login shell and primary action.
- [x] Oteryn accounts use a dedicated modern character-list presentation while reusing `CharacterList` behavior.
- [x] No new proprietary or binary assets are committed.
- [x] Lua-focused CI and complete changed-file review are recorded.
- [ ] Runtime visual approval is recorded before merge.

## Current state

- Draft PR #23 contains the prototype implementation.
- The enter-game view is replaced by a large dark shell with a navy/blue/gold palette, an Oteryn-first action, separate legacy server mode and retained server/client selectors.
- `oteryn_login_theme.lua` decorates the existing dynamic identity button, keeps the identity controller untouched and selects `oteryn_characterlist.otui` only for Oteryn accounts.
- The dedicated character-list view reuses the existing character population, sorting, outfit, pinning, reconnect and game-entry logic.
- No main-password fallback was added to the Oteryn profile.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-07-24T21:58:34Z
head: 83203ca8521d414e274285e3aaa80aa5a7b1a139
branch: feat/OTC-20260724-oteryn-login-shell
pr: 23
status: awaiting_visual_review
context_routes:
  - client-entergame-ui
  - oteryn-identity
owned_paths:
  - modules/client_entergame/entergame.otui
  - modules/client_entergame/entergame.otmod
  - modules/client_entergame/oteryn_login_theme.lua
  - modules/client_entergame/oteryn_characterlist.otui
  - docs/agents/ACTIVE_WORK.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260724-oteryn-login-shell.md
proven:
  - Oteryn native authentication remains implemented by the existing identity controller; this task changes presentation only.
  - CharacterList.create accepts an optional OTUI name, allowing an Oteryn-specific view without duplicating game-login behavior.
  - All legacy widget IDs consumed by entergame.lua remain direct children of the enter-game root.
  - Module unload order disconnects the wrapped identity callback before restoring the original function reference.
  - CI run 180 completed successfully on code head 6112ad46f921243d20fd201249198050a10d2a8c, including Lua syntax and fast checks.
derived:
  - A small theme adapter is sufficient to select the Oteryn character view and style the dynamic Oteryn button without changing auth internals.
unknown:
  - Exact rendered spacing and font metrics until a built desktop client is launched with this branch.
conflicts: []
first_failure:
  marker: sandbox-runtime-unavailable
  evidence: the execution environment cannot resolve github.com for a local clone and does not contain a runnable Windows OTClient build
rejected_hypotheses:
  - Replacing the authentication controller is unnecessary because the merged flow already provides the required security behavior.
  - A hardcoded live service-status claim was rejected; the prototype displays only neutral client readiness text.
changed_paths:
  - docs/agents/ACTIVE_WORK.md
  - docs/agents/CHANGELOG.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/tasks/active/OTC-20260724-oteryn-login-shell.md
  - modules/client_entergame/entergame.otmod
  - modules/client_entergame/entergame.otui
  - modules/client_entergame/oteryn_characterlist.otui
  - modules/client_entergame/oteryn_login_theme.lua
validation:
  - command: repository and overlap preflight
    result: PASS
    evidence: task branch created from main 8f2b6a8878c9cbc243a29c8b2dad7c755ca7a260; no active runtime-UI overlap
  - command: changed-file and complete patch review
    result: PASS
    evidence: PR #23 contains only the declared OTUI/Lua/docs paths and no auth/protocol/binary changes
  - command: GitHub Actions CI run 180
    result: PASS
    evidence: completed success at 6112ad46f921243d20fd201249198050a10d2a8c; Lua Syntax and Fast Checks successful
blockers:
  - launch the branch in a desktop client and approve or adjust exact layout before merge
next_action: Build or run the Windows client from PR #23 and capture the actual enter-game and Oteryn character-list screens for visual review.
```

## Compatibility and rollback

- Authentication endpoints, credential lifecycle, Gateway response handling and Canary handoff are unchanged.
- Legacy server mode and Oteryn mode continue to share existing controllers.
- No new assets, stored credentials or configuration migrations are introduced.
- Rollback is a normal revert of draft PR #23.
