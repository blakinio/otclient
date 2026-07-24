---
task_id: OTC-20260724-oteryn-login-shell
coordination_id: OTS-20260721-oteryn-identity-auth
status: implementing
agent: "GPT-5.6 Thinking"
branch: feat/OTC-20260724-oteryn-login-shell
base_branch: main
created: 2026-07-24T21:44:57Z
updated: 2026-07-24T21:44:57Z
last_verified_commit: 8f2b6a8878c9cbc243a29c8b2dad7c755ca7a260
risk: low
related_issue: ""
related_pr: ""
depends_on:
  - merged Oteryn native identity login PR #17
blocks:
  - visual approval before merge
owned_paths:
  - modules/client_entergame/entergame.otui
  - modules/client_entergame/entergame.otmod
  - modules/client_entergame/oteryn_login_theme.lua
  - modules/client_entergame/oteryn_characterlist.otui
  - modules/client_entergame/characterlist.lua
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

- [ ] Existing Oteryn OAuth/PKCE behavior remains unchanged.
- [ ] Legacy password login remains available and keeps every widget ID required by `entergame.lua`.
- [ ] Oteryn mode presents a modern branded login shell and primary action.
- [ ] Oteryn accounts use a dedicated modern character-list presentation while reusing `CharacterList` behavior.
- [ ] No new proprietary or binary assets are committed.
- [ ] Lua/OTUI-focused validation and complete diff review are recorded.
- [ ] Prototype remains a draft until visual review.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-07-24T21:44:57Z
head: 8f2b6a8878c9cbc243a29c8b2dad7c755ca7a260
branch: feat/OTC-20260724-oteryn-login-shell
pr: none
status: implementing
context_routes:
  - client-entergame-ui
  - oteryn-identity
owned_paths:
  - modules/client_entergame/entergame.otui
  - modules/client_entergame/entergame.otmod
  - modules/client_entergame/oteryn_login_theme.lua
  - modules/client_entergame/oteryn_characterlist.otui
  - modules/client_entergame/characterlist.lua
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260724-oteryn-login-shell.md
proven:
  - Oteryn native authentication is already implemented and merged; this task changes presentation only.
  - CharacterList.create accepts an optional OTUI name, allowing an Oteryn-specific view without duplicating login behavior.
  - The current enter-game Lua controller addresses legacy controls by stable widget IDs that must be preserved.
derived:
  - A small theme adapter can select the dedicated Oteryn character list and style the existing dynamic Oteryn button without modifying auth internals.
unknown:
  - Exact runtime appearance until a built client is launched with the prototype branch.
conflicts: []
first_failure:
  marker: none
  evidence: none
rejected_hypotheses:
  - Replacing the authentication controller is unnecessary because the merged flow already provides the required security behavior.
changed_paths:
  - docs/agents/tasks/active/OTC-20260724-oteryn-login-shell.md
validation:
  - command: repository and overlap preflight
    result: PASS
    evidence: main 8f2b6a8878c9cbc243a29c8b2dad7c755ca7a260; only open PR #22 is documentation-only and does not own login UI paths
blockers:
  - visual approval before merge
next_action: Publish the draft PR, then implement the OTUI shell and theme adapter on its task branch.
```

## Compatibility and rollback

- Authentication endpoints, credential lifecycle, Gateway response handling and Canary handoff are unchanged.
- Legacy and Oteryn modes continue to share existing controllers.
- Rollback is a normal revert of this prototype PR.
