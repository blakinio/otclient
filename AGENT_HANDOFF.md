# OTS / OTClient - agent handoff

> Status: active
> Last verified: 2026-07-12 (Europe/Warsaw)
> Working repository: `blakinio/otclient`
> Default branch: `main`
> Local user path: `C:\Users\barte\Documents\New project`

## 1. Purpose

This file is the durable handoff for every agent working on the OTS project. Read it before changing code. It exists so another agent can continue safely when the current conversation becomes slow, loses context, or reaches its token limit.

At the beginning of every session, verify the live GitHub and local Git state. Snapshots below are historical evidence, not a substitute for verification. After every important PR, merge, CI repair, policy change, or newly discovered blocker, update both the current-state section and the changelog.

## 2. Project goal

Maintain a stable OTClient Redemption fork designed to work with Canary. The project should provide:

- predictable client behavior and protocol compatibility with Canary;
- secure, repeatable CI;
- unit, integration, contract, Lua, and regression tests;
- controlled upstream synchronization;
- small reviewable PRs;
- a base for future client, server, map, quest, NPC, monster, and content tooling;
- clear operating rules for humans and AI agents.

Long-term related repositories:

- working fork: `https://github.com/blakinio/otclient`
- OTClient upstream: `https://github.com/opentibiabr/otclient`
- Canary server: `https://github.com/opentibiabr/canary`
- Remere's Map Editor: `https://github.com/opentibiabr/remeres-map-editor`
- client-editor: `https://github.com/opentibiabr/client-editor`

Critical rule: ordinary PRs must target `blakinio/otclient:main`. Never open a PR to `opentibiabr/otclient` unless the user explicitly requests an upstream contribution. An accidental upstream PR happened earlier; it was closed without merge.

## 3. Current verified snapshot

Snapshot taken on 2026-07-12. Re-check before acting.

### 3.1 Main branch

Latest verified `main` commit:

```text
bdd83db12292bb646280372dfdf8ae5cd50e3072
fix(ci): restore runtime-scoped Lua syntax checks
```

Previous governance merge:

```text
208c64d336eef7c199fa022daf08d1ee95295575
Chore/repository governance (#1)
```

### 3.2 Open test-foundation PR

```text
PR: https://github.com/blakinio/otclient/pull/3
Title: test: establish client unit and integration test foundation
Base: main
Head: test/client-test-foundation
Verified head SHA: 92d29382e6a87cefb6453ac3b3d7b5224423fd3e
State at snapshot: open, not draft, mergeable
Commits: 9
Changed files: 43
Additions: 1936
Deletions: 14
CI at snapshot: in progress, run 7, run id 29186723650
```

Latest verified branch commit:

```text
92d29382e6a87cefb6453ac3b3d7b5224423fd3e
test: include client compile context in new tests
```

That commit added `#include <framework/pch.h>` to new C++ test sources and missing client type includes used by tile tests.

Live verification:

```powershell
gh pr view 3 --repo blakinio/otclient
gh pr checks 3 --repo blakinio/otclient
gh run list --repo blakinio/otclient --branch test/client-test-foundation
```

## 4. Completed work and decisions

### 4.1 Fork organization

- The fork was audited against upstream and was initially synchronized.
- OTClient Redemption was selected as the client base for Canary.
- Production behavior changes must not be mixed with governance or test-infrastructure changes.

### 4.2 Repository governance - PR #1

Branch: `chore/repository-governance`

Squash result:

```text
208c64d336eef7c199fa022daf08d1ee95295575
Chore/repository governance (#1)
```

The governance work added or improved:

- one stable required CI status;
- minimal GitHub Actions permissions;
- pinned external actions;
- safer privileged workflows;
- Dependabot configuration and safe automation;
- one retry only for infrastructure failures;
- CODEOWNERS;
- issue and PR templates;
- contribution and governance documentation;
- a repository-settings helper script.

Important files:

```text
.github/CODEOWNERS
.github/ISSUE_TEMPLATE/
.github/PULL_REQUEST_TEMPLATE.md
.github/dependabot.yml
.github/workflows/ci.yml
.github/workflows/reusable-tests-lua.yml
scripts/configure-github-repository.sh
```

A local branch once tracked `origin/main` incorrectly. It was repaired with:

```powershell
git branch --unset-upstream
git push -u origin chore/repository-governance
```

Always inspect `git branch -vv` after branch creation or first push.

### 4.3 Lua CI repair - PR #2

The first governance CI run failed because the blocking Lua job compiled every tracked `*.lua`, including files outside OTClient runtime roots. The failure propagated to `CI / Required`.

Repair branch: `fix/ci-lua-syntax`

Squash result:

```text
bdd83db12292bb646280372dfdf8ae5cd50e3072
fix(ci): restore runtime-scoped Lua syntax checks
```

The blocking Lua syntax scan now covers only:

```text
data/
modules/
mods/
```

Deterministic discovery:

```bash
find data modules mods -type f -name '*.lua' -print0 | sort -z
```

Real Lua syntax errors remain fatal. Do not restore `git ls-files '*.lua'` without a full impact analysis.

### 4.4 Pull-request settings

Verified repository settings:

- default branch: `main`;
- auto-merge: enabled;
- suggest/update PR branch: enabled;
- squash merge: enabled;
- merge commits: disabled;
- rebase merge: disabled;
- automatic head-branch deletion: enabled;
- web commit sign-off: disabled;
- commit comments: enabled.

Effective merge policy: squash only.

### 4.5 Main protection

Use one modern Branch Ruleset, not a simultaneous legacy Branch protection rule.

Active ruleset: `Protect main`

Effective rules:

```text
deletion
non_fast_forward
required_linear_history
pull_request
required_status_checks
```

Parameters:

- target: `~DEFAULT_BRANCH`;
- enforcement: active;
- required approvals: 0;
- code-owner review: off;
- last-push approval: off;
- review-thread resolution: required;
- allowed merge method: squash only;
- required check: `CI / Required`;
- branch must be current with `main`;
- force pushes and deletion blocked;
- CodeQL is not a required ruleset condition;
- repository administrator bypass exists for emergencies only.

The legacy endpoint correctly returns HTTP 404:

```powershell
gh api repos/blakinio/otclient/branches/main/protection
```

This means no legacy rule is active. It does not mean `main` is unprotected. Inspect modern rules with:

```powershell
gh api repos/blakinio/otclient/rules/branches/main
```

Verified effective summary:

```json
{
  "rules": [
    "deletion",
    "non_fast_forward",
    "required_linear_history",
    "pull_request",
    "required_status_checks"
  ],
  "merge_methods": ["squash"],
  "checks": ["CI / Required"]
}
```

Do not use admin bypass merely to avoid failing CI, unresolved discussions, or an outdated PR branch.

## 5. CI invariants

### 5.1 Stable required check

The ruleset requires exactly:

```text
CI / Required
```

Do not require dynamic matrix-job names or conditional platform checks directly. Some jobs can be skipped depending on path scope, while the aggregate must always run and correctly evaluate their results.

### 5.2 Path scope

Documentation-only changes may skip expensive builds, but they must still produce `CI / Required`. Avoid workflow-level path filters that prevent the required workflow from appearing at all.

### 5.3 Security

- Keep permissions minimal.
- Do not execute untrusted PR code with secrets.
- Use `pull_request_target` only with a proven safe model.
- Never check out PR code in a privileged workflow.
- Pin external actions to immutable SHAs.
- Dependabot metadata/automation must remain read-only and same-repository constrained.

### 5.4 Retry policy

Retry only clear infrastructure outcomes such as cancelled, timed out, or startup failure. Maximum one retry. Never retry or suppress genuine test failures to manufacture green CI.

### 5.5 Forbidden CI shortcuts

Do not introduce:

- `continue-on-error` on required tests;
- ignored exit codes;
- catch-all scripts returning zero;
- disabled tests without documented justification;
- weaker assertions merely because a test exposed a defect.

## 6. PR #3 - client test foundation

### 6.1 Purpose

Create the first deterministic client test foundation without changing production client behavior.

Before this PR there were about 23 discovered GoogleTest cases in three targets, concentrated mainly in map spectators, string encoding, and OTML aliases. Lua CI mostly compiled syntax. There was no shared message-builder layer, bounded protocol loopback integration test, cross-language resource contract suite, or organized regression backlog.

### 6.2 New structure and targets

Directories:

```text
tests/unit/
tests/integration/
tests/lua/
tests/fixtures/
tests/support/
```

New CMake targets:

```text
otclient_message_tests
otclient_test_support_tests
otclient_tile_order_tests
otclient_protocol_contract_tests
otclient_protocol_loopback_tests
```

Lua CTest registrations:

```text
otclient_lua_unit_tests
otclient_lua_contract_tests
otclient_lua_runner_failure_contract
```

Expected configured scope at the PR snapshot:

- 58 GoogleTest cases;
- 3 Lua CTest registrations;
- 7 positive Lua cases;
- 1 intentional runner-failure contract.

### 6.3 Covered areas

- InputMessage numeric reads, strings, positions, cursor, unread bytes, EOF, skipping, empty bodies, bounds, and reserved-header offset behavior.
- OutputMessage encoding, byte order, positions, size, append preservation, and reset.
- TestEnvironment lifecycle, deterministic fake resources, fake game/local-player state, and callback order.
- Synthetic Tile, ThingType, Item, and Creature builders; tile ordering, selection, overlap, add/remove, and empty-tile rules.
- Selected opcode range and uniqueness contracts.
- C++/Lua ResourceTypes and feature-name contracts, including fragment identifiers 84/85 and prevention of invalid `BANK_BALANCE` aliases.
- A bounded local protocol loopback test on an ephemeral port for one world-light packet.
- OTML nesting, comments, aliases, empty values, deterministic reload, and invalid indentation.
- A minimal Lua runner with assertions, named reporting, nonzero failure status, client-global stubs, gamelib formatting tests, and ResourceTypes contracts.

### 6.4 Local and CI validation

Local commands for Linux:

```bash
cmake --preset linux-tests
cmake --build --preset linux-tests
ctest --preset linux-tests
ctest --test-dir build/linux-tests -L unit --output-on-failure
ctest --test-dir build/linux-tests -L lua --output-on-failure
ctest --test-dir build/linux-tests -L integration --output-on-failure
```

Equivalent presets: `windows-tests`, `macos-tests`.
Optional manual presets: `linux-asan-tests`, `linux-coverage-tests`.

Reported local validation before PR:

- CMake preset JSON parsed;
- Lua unit cases 4/4 passed;
- Lua resource contracts 3/3 passed;
- intentional Lua runner failure contract passed;
- new Lua sources compiled to LuaJIT bytecode;
- modified workflows passed yamllint;
- `git diff --check` passed.

Full C++/CTest validation was delegated to CI because the local Windows checkout lacked the repository vcpkg toolchain. Never claim those tests passed locally unless they were actually run.

### 6.5 Deliberately excluded from PR #3

Keep these for focused follow-up PRs:

- full Forge, Wheel, Gem Atelier, Prey, or Market coverage;
- full login flow;
- headless startup;
- every parser opcode dispatch seam;
- complete mock client globals;
- Canary end-to-end tests;
- production behavior changes;
- repository settings, ruleset, or branch-protection changes.

The observed Wheel plural-fragment-name issue belongs in a later regression/fix PR.

### 6.6 Client assets

PR #3 must not change client-assets installation or loading. Expected runtime locations remain:

```text
data/things/<version>/
data/sounds/<version>/
bin/*
```

Do not weaken manifest SHA-256 validation or secure fallback defaults. Never commit secrets, private server data, leaked files, or proprietary CipSoft assets.

## 7. Immediate continuation plan

Priority 1: finish PR #3.

1. Verify PR metadata and all checks.
2. Confirm the head is `test/client-test-foundation` and base is `blakinio/otclient:main`.
3. If CI fails, inspect the exact job and log; repair the cause on the same branch.
4. Do not disable the failing test, weaken CI, or add `continue-on-error` to obtain green status.
5. Before merge, require green `CI / Required`, an up-to-date branch, and no unresolved review threads.
6. Confirm the PR is test/support/docs/CI only and does not alter production behavior.
7. Merge with squash only.
8. After merge, synchronize local `main`, prune remotes, and update this handoff with final SHA, test counts, CI duration, and follow-ups.

Useful commands:

```powershell
git status -sb
git diff --check
git push
gh pr checks 3 --repo blakinio/otclient --watch
```

Recommended follow-up order after test foundation:

1. protocol parser contracts;
2. login/character-list seams;
3. Forge contracts;
4. Wheel contracts;
5. Gem Atelier contracts;
6. Prey;
7. Market;
8. Canary client/server E2E;
9. headless client smoke test;
10. map/content tooling integration.

Each topic belongs in its own branch and PR.

## 8. Standard operating procedure

### 8.1 Session start

```powershell
cd "C:\Users\barte\Documents\New project"
git status -sb
git remote -v
git fetch --all --prune
git branch -vv
git log --oneline --decorate -10 origin/main
gh auth status
gh pr list --repo blakinio/otclient
```

Expected remotes:

```text
origin   -> https://github.com/blakinio/otclient.git
upstream -> https://github.com/opentibiabr/otclient.git
```

Verify before adding or changing a remote.

### 8.2 New branches

Create new work from current `origin/main` unless the user explicitly selects another base:

```powershell
git fetch origin
git checkout -B <branch-name> origin/main
```

Do not base new work on `chore/repository-governance` or another stale task branch.

Use prefixes such as `feat/`, `fix/`, `test/`, `ci/`, `docs/`, `chore/`, and `refactor/`.

### 8.3 Commits and PRs

Use logical Conventional Commits. Before committing:

```powershell
git status --short
git diff --check
git diff --stat
```

Every important PR should explain goal, before/after state, scope, production impact, tests actually run, tests not run, risks, follow-ups, and any client-assets implications.

Never push directly to `main`. Target `blakinio/otclient:main` and merge with squash.

### 8.4 Missing GitHub CLI

The user's Windows machine has GitHub CLI 2.96.0 authenticated as `blakinio` over HTTPS. A container agent may not have `gh`. Missing `gh` is not a reason to stop implementation, commits, local tests, or normal `git push`; PR creation and monitoring can be completed later through an available GitHub integration or browser.

### 8.5 PowerShell and jq

Windows PowerShell can misinterpret complex `gh --jq` expressions. Prefer:

```powershell
$rules = gh api repos/blakinio/otclient/rules/branches/main | ConvertFrom-Json
```

Then inspect with native PowerShell objects.

## 9. Truthfulness requirements

Always distinguish:

- executed locally;
- executed in CI;
- not executed;
- impossible because of a missing toolchain or environment limitation.

Never state that all tests passed when only Lua, YAML, or CMake JSON checks were run.

For protocol changes, verify protocol version, feature flags, opcode on both sides, field order, numeric widths, version gates, C++/Lua agreement, unknown-opcode behavior, and regressions on older protocols.

Production behavior fixes require a separate PR with a reproducing test, before/after behavior, Canary comparison, and legal observation of the official client's behavior when needed.

## 10. Required reading

On `main` or the active branch:

```text
.github/PULL_REQUEST_TEMPLATE.md
.github/CODEOWNERS
.github/workflows/ci.yml
.github/workflows/reusable-tests-lua.yml
.github/dependabot.yml
scripts/configure-github-repository.sh
```

On `test/client-test-foundation`:

```text
docs/testing-strategy.md
docs/regression-test-backlog.md
tests/
CMakePresets.json
```

Read the complete CI dependency chain and `CI / Required` aggregation before editing workflows.

## 11. Handoff update format

After each major step, add a changelog entry:

```markdown
### YYYY-MM-DD - short title

- Branch:
- PR:
- Base SHA:
- Head SHA:
- Changes:
- Reason:
- Local tests:
- CI result:
- Merge SHA:
- Known issues:
- Next step:
```

Preserve historical decisions. When a decision changes, retain the old entry, record the new decision and reason, and update the current-state section.

## 12. Changelog

### 2026-07-12 - handoff document created

- Recorded project goals, repository roles, governance, CI invariants, ruleset, PR #3 state, operating procedure, known traps, and continuation plan.

### 2026-07-12 - PR #3 opened

- Branch: `test/client-test-foundation`
- Base: `main`
- Scope: unit, integration, contract, Lua, and regression-test foundation.
- Production behavior must remain unchanged.
- CI was still running at the snapshot.

### 2026-07-12 - compile-context repair on PR #3

- Commit: `92d29382e6a87cefb6453ac3b3d7b5224423fd3e`
- Added required PCH and missing client-type includes to new tests.

### 2026-07-12 - Protect main ruleset finalized

- One active Branch Ruleset.
- Squash only.
- Required `CI / Required`.
- Up-to-date branch and resolved discussions required.
- Zero approvals for the sole-maintainer workflow.
- Deletion and force push blocked.
- Legacy branch protection and required CodeQL rule removed.

### 2026-07-11 - Lua CI repair merged

- PR #2 merged.
- Commit: `bdd83db12292bb646280372dfdf8ae5cd50e3072`
- Blocking Lua scan limited to `data`, `modules`, and `mods`.

### 2026-07-11 - repository governance merged

- PR #1 merged.
- Commit: `208c64d336eef7c199fa022daf08d1ee95295575`
- Added governance, stable CI aggregation, Dependabot, templates, CODEOWNERS, and documentation.

## 13. New-agent checklist

```text
[ ] Read AGENT_HANDOFF.md.
[ ] Check git status, remotes, branches, and current origin/main.
[ ] Fetch and prune.
[ ] Inspect open PRs and live CI.
[ ] Confirm target repository is blakinio/otclient.
[ ] Confirm the correct task branch and base.
[ ] Do not work from the old governance branch.
[ ] Do not change rulesets or repository settings without instruction.
[ ] Do not weaken CI.
[ ] Do not mix production changes into test foundation.
[ ] Report only tests actually executed.
[ ] Update this file before handing work to another agent.
```

## 14. One-line continuation instruction

Continue from current `origin/main`; first bring PR #3 `test/client-test-foundation` to a fully green `CI / Required`, do not weaken CI or repository protection, keep production behavior changes separate, and record every significant result in this handoff.
