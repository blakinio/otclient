---
task_id: OTC-20260724-shell-safe-open-url
coordination_id: OTS-20260721-oteryn-identity-auth
status: ready
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260724-shell-safe-open-url
base_branch: main
created: 2026-07-24T12:40:00+02:00
updated: 2026-07-24T15:49:00+02:00
last_verified_commit: a9c130da976ef42a75674c5743c53639ab7f430e
risk: medium
related_issue: ""
related_pr: "20"
depends_on:
  - "OTClient native identity merge bb87346f6c516a19d19497d82bb01fb389334ff5"
  - "Platform rehearsal merge b520cf78ac1b488a289b156b492539b2a047f299"
blocks: []
owned_paths:
  - docs/agents/tasks/active/OTC-20260724-shell-safe-open-url.md
  - src/framework/platform/unixplatform.cpp
  - tests/unit/framework/CMakeLists.txt
  - tests/unit/framework/platform_open_url_test.cpp
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
modules_touched:
  - Linux platform process launch
  - Oteryn system-browser OAuth boundary
reuses:
  - Platform::spawnProcess argv-based execv implementation
public_interfaces:
  - Platform::openUrl behavior on Unix desktop
cross_repo_tasks:
  - CAN-20260723-native-auth-ephemeral-cutover-rehearsal
  - OTERYN-20260723-native-auth-ephemeral-cutover-rehearsal
required_reads:
  - docs/agents/BUILD_TEST_MATRIX.md
  - docs/agents/CROSS_REPO_CONTRACTS.md
  - docs/agents/tasks/active/OTC-20260724-shell-safe-open-url.md
search_first:
  - src/framework/platform/unixplatform.cpp
  - tests/unit/framework/platform_open_url_test.cpp
  - docs/agents/MODULE_CATALOG.md
optional_reads:
  - modules/client_entergame/oteryn_identity.lua
---

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-07-24T15:49:00+02:00
head: a9c130da976ef42a75674c5743c53639ab7f430e
branch: fix/OTC-20260724-shell-safe-open-url
pr: 20
status: ready
context_routes:
  - agent-governance
  - cpp-runtime
  - cross-repo-native-auth
owned_paths:
  - src/framework/platform/unixplatform.cpp
  - tests/unit/framework/CMakeLists.txt
  - tests/unit/framework/platform_open_url_test.cpp
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260724-shell-safe-open-url.md
proven:
  - OTClient bb87346f generated a complete PKCE URL, while Unix Platform::openUrl passed it through system("xdg-open ...").
  - Platform rehearsal run 30085898466 received only client_id and correctly returned HTTP 400; artifact 8593807390 retained the redacted diagnosis.
  - PR 20 replaces shell parsing with argv-based spawnProcess and adds a one-argument URL regression test.
  - Draft CI run 30087234932 passed syntax, static analysis, Lua syntax and CI Required.
  - Full CI run 30087461815 on implementation head 9189d106 produced Linux release artifact 8595332324 with digest sha256:396e0e1fed38c14f43c88cba4e578997ecbd56c2f211ee8b398c712a10c44850 before later jobs were cancelled by subsequent pushes.
  - Current-head CI run 30091010071 passed on a9c130da976ef42a75674c5743c53639ab7f430e.
  - Platform rehearsal run 30095854266 completed successfully with exact OTClient source 9189d1063e968a0c2ffab11c5069db192e753397 and artifact 8595332324.
  - Retained rehearsal artifact 8597730728 has digest sha256:e7e908e9129658654054a96adf641757edc2c904fc2b01a5b9fc97e393d18009 and classification PRODUCTION_LIKE_PROVEN.
  - Platform PR 126 was squash-merged as b520cf78ac1b488a289b156b492539b2a047f299 after all current-head workflows passed.
  - PR 20 is open, mergeable and draft pending its final documentation-only checks.
derived:
  - The missing OAuth parameters were a Unix OTClient product defect, not a Platform or rehearsal-harness defect.
  - The shell-safe URL launch is physically proven through complete OAuth PKCE and successful world entry.
unknown: []
conflicts: []
first_failure:
  marker: none
  evidence: All implementation and cross-repository acceptance gates passed; only final documentation-only PR checks remain.
rejected_hypotheses:
  - OTClient module initialization omitted PKCE fields: source builds all required PKCE fields before openUrl.
  - capture-xdg-open.sh truncated the URL: it requires exactly one argument and writes that argument unchanged.
  - Platform authorization validation caused the defect: the fixed client delivered the full query and completed OAuth.
changed_paths:
  - src/framework/platform/unixplatform.cpp
  - tests/unit/framework/CMakeLists.txt
  - tests/unit/framework/platform_open_url_test.cpp
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260724-shell-safe-open-url.md
validation:
  - command: Platform rehearsal run 30085898466
    result: FAIL
    evidence: OAuth authorize request contained only client_id; artifact 8593807390.
  - command: OTClient CI run 30087234932
    result: PASS
    evidence: syntax, static analysis, Lua syntax and CI Required succeeded on draft head.
  - command: OTClient CI run 30087461815
    result: PARTIAL_PASS
    evidence: Linux release build succeeded and uploaded artifact 8595332324; remaining platform jobs were cancelled after subsequent documentation pushes.
  - command: OTClient CI run 30091010071
    result: PASS
    evidence: current-head CI succeeded on a9c130da976ef42a75674c5743c53639ab7f430e.
  - command: Platform rehearsal run 30095854266
    result: PASS
    evidence: Full physical OAuth PKCE, world entry, logout, replay rejection, rotation, rollback and final smoke succeeded.
  - command: Retained evidence artifact 8597730728
    result: PASS
    evidence: PRODUCTION_LIKE_PROVEN; digest sha256:e7e908e9129658654054a96adf641757edc2c904fc2b01a5b9fc97e393d18009.
blockers: []
next_action: Inspect checks triggered by the final documentation-only commits and, if green, mark PR 20 ready and squash-merge it.
```

# Goal

Launch Unix desktop URLs without shell interpretation so OAuth Authorization Code + PKCE reaches the system browser as one unchanged argument.

# Current implementation

- PR: `blakinio/otclient#20`
- Branch: `fix/OTC-20260724-shell-safe-open-url`
- Fixed implementation head: `9189d1063e968a0c2ffab11c5069db192e753397`
- Current verified documentation head: `a9c130da976ef42a75674c5743c53639ab7f430e`
- Linux release artifact: `8595332324`
- Artifact digest: `sha256:396e0e1fed38c14f43c88cba4e578997ecbd56c2f211ee8b398c712a10c44850`
- Rehearsal run: `30095854266`
- Retained evidence artifact: `8597730728`
- Platform rehearsal merge: `b520cf78ac1b488a289b156b492539b2a047f299`
- `Platform::openUrl` reuses `spawnProcess` for Unix desktop URL launch.
- The focused Linux regression substitutes `xdg-open` through `PATH` and asserts one exact URL argument.
- Catalogue and changelog entries are included.

# Acceptance criteria

- [x] Unix desktop URL launch no longer constructs a shell command.
- [x] Focused test covers a URL containing multiple `&` query separators.
- [x] Draft fast checks pass.
- [x] Exact Linux release artifact exists for the fixed implementation head.
- [x] Exact Linux artifact is pinned into Platform PR #126.
- [x] Physical production-like native-auth rehearsal passes.
- [x] PR remained unmerged until the cross-repository gate became green.

# Remaining work

1. Follow the checkpoint `next_action`.