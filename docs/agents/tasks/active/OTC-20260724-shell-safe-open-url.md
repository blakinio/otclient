---
task_id: OTC-20260724-shell-safe-open-url
coordination_id: OTS-20260721-oteryn-identity-auth
status: validating
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260724-shell-safe-open-url
base_branch: main
created: 2026-07-24T12:40:00+02:00
updated: 2026-07-24T13:03:00+02:00
last_verified_commit: 9189d1063e968a0c2ffab11c5069db192e753397
risk: medium
related_issue: ""
related_pr: "20"
depends_on:
  - "OTClient native identity merge bb87346f6c516a19d19497d82bb01fb389334ff5"
  - "Platform rehearsal PR blakinio/Oteryn-Platform#126"
blocks:
  - "physical system-browser OAuth PKCE validation in Oteryn production-like rehearsal"
owned_paths:
  - docs/agents/tasks/active/OTC-20260724-shell-safe-open-url.md
  - src/framework/platform/unixplatform.cpp
  - tests/integration/framework/CMakeLists.txt
  - tests/integration/framework/platform_open_url_test.cpp
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
  - tests/integration/framework/platform_open_url_test.cpp
  - docs/agents/MODULE_CATALOG.md
optional_reads:
  - modules/client_entergame/oteryn_identity.lua
---

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-07-24T13:03:00+02:00
head: 9189d1063e968a0c2ffab11c5069db192e753397
branch: fix/OTC-20260724-shell-safe-open-url
pr: 20
status: validating
context_routes:
  - agent-governance
  - cpp-runtime
  - cross-repo-native-auth
owned_paths:
  - src/framework/platform/unixplatform.cpp
  - tests/integration/framework/CMakeLists.txt
  - tests/integration/framework/platform_open_url_test.cpp
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260724-shell-safe-open-url.md
proven:
  - OTClient bb87346f generated a complete PKCE URL, while Unix Platform::openUrl passed it through system("xdg-open ...").
  - Platform rehearsal run 30085898466 received only client_id and correctly returned HTTP 400; artifact 8593807390 retained the redacted diagnosis.
  - PR 20 replaces shell parsing with argv-based spawnProcess and adds a one-argument URL regression test.
  - Draft CI run 30087234932 passed syntax, static analysis, Lua syntax and CI Required.
  - PR 20 is open, mergeable and restored to draft.
derived:
  - The missing OAuth parameters are a real Unix OTClient product defect, not a Platform or rehearsal-harness defect.
  - A new exact Linux OTClient artifact must replace bb87346f in Platform PR 126 before the rehearsal can prove physical OAuth and malformed-Gateway handling.
unknown:
  - Final result of full OTClient CI run 30087461815.
  - Linux release artifact ID and digest for the fixed OTClient head.
  - Final cross-repository rehearsal result after repinning the fixed binary.
conflicts:
  - none
first_failure:
  marker: none
  evidence: First unmet gate is incomplete full CI run 30087461815 on implementation head 9189d1063e968a0c2ffab11c5069db192e753397.
rejected_hypotheses:
  - OTClient module initialization omitted PKCE fields: source builds all required PKCE fields before openUrl.
  - capture-xdg-open.sh truncated the URL: it requires exactly one argument and writes that argument unchanged.
  - Platform authorization validation caused the defect: HTTP 400 was correct for the shell-truncated request.
changed_paths:
  - src/framework/platform/unixplatform.cpp
  - tests/integration/framework/CMakeLists.txt
  - tests/integration/framework/platform_open_url_test.cpp
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
    result: NOT_RUN
    evidence: full Linux/Windows/macOS/Android/Docker/Browser matrix was still queued or in progress at handoff.
  - command: python tools/agents/checkpoint.py docs/agents/tasks/active/OTC-20260724-shell-safe-open-url.md --require-checkpoint
    result: PASS
    evidence: compact checkpoint validated before resume generation.
blockers:
  - Full OTClient CI run 30087461815 has not reached a final conclusion.
  - Platform PR 126 cannot repin an exact fixed OTClient binary until the Linux release artifact exists.
next_action: Inspect the final result of OTClient CI run 30087461815 and record either its first failed job or the Linux release artifact identifiers.
```

# Goal

Launch Unix desktop URLs without shell interpretation so OAuth Authorization Code + PKCE reaches the system browser as one unchanged argument.

# Current implementation

- PR: `blakinio/otclient#20`
- Branch: `fix/OTC-20260724-shell-safe-open-url`
- Implementation head under full CI: `9189d1063e968a0c2ffab11c5069db192e753397`
- `Platform::openUrl` reuses `spawnProcess` for Unix desktop URL launch.
- The focused Linux regression substitutes `xdg-open` through `PATH` and asserts one exact URL argument.
- Catalogue and changelog entries are included.
- PR remains draft and must not merge before exact-binary cross-repository rehearsal evidence is green.

# Acceptance criteria

- [x] Unix desktop URL launch no longer constructs a shell command.
- [x] Focused test covers a URL containing multiple `&` query separators.
- [x] Draft fast checks pass.
- [ ] Full affected-platform CI passes.
- [ ] Exact Linux artifact is pinned into Platform PR #126.
- [ ] Physical production-like native-auth rehearsal passes.
- [ ] PR remains unmerged until the cross-repository gate is green.

# Remaining work

1. Follow the checkpoint `next_action`.
