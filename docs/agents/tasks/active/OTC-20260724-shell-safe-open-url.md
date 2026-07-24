---
task_id: OTC-20260724-shell-safe-open-url
coordination_id: OTS-20260721-oteryn-identity-auth
status: implementing
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260724-shell-safe-open-url
base_branch: main
created: 2026-07-24T12:40:00+02:00
updated: 2026-07-24T12:40:00+02:00
last_verified_commit: b3bcea2a95959bb4e92cc0b80cd49f36b63699b2
risk: medium
related_issue: ""
related_pr: ""
depends_on:
  - "OTClient native identity merge bb87346f6c516a19d19497d82bb01fb389334ff5"
  - "Platform rehearsal PR blakinio/Oteryn-Platform#126"
blocks:
  - "physical system-browser OAuth PKCE validation in Oteryn production-like rehearsal"
owned_paths:
  - docs/agents/tasks/active/OTC-20260724-shell-safe-open-url.md
  - src/framework/platform/unixplatform.cpp
  - tests/**/platform*open*url*
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
---

# Goal

Launch Unix desktop URLs without a shell so an OAuth authorization URL containing `&` reaches the system browser as one unchanged argument.

# Acceptance criteria

- [ ] `Platform::openUrl` does not use shell command construction on Unix desktop.
- [ ] A URL containing multiple query parameters is passed as one exact process argument.
- [ ] Existing asynchronous `now` behavior remains compatible.
- [ ] Required C++ build/tests and repository CI pass.
- [ ] The Platform-hosted native-auth rehearsal reaches the malformed Gateway boundary with the rebuilt exact OTClient binary.
- [ ] Module catalogue impact is recorded; no protocol or Canary wire contract changes.
- [ ] Changelog records the behavior-level security fix.
- [ ] Autonomous merge is held until cross-repository rehearsal evidence is green.

# Confirmed context

- Exact OTClient `bb87346f6c516a19d19497d82bb01fb389334ff5` builds a complete OAuth Authorization Code + PKCE URL in `modules/client_entergame/oteryn_identity.lua`.
- Unix `Platform::openUrl` currently executes `system(fmt::format("xdg-open {}", url).c_str())`.
- Platform rehearsal run `30085898466` retained only `client_id` at `/oauth/authorize`; all parameters after the first `&` were absent and Platform correctly returned HTTP 400.
- `capture-xdg-open.sh` accepts one quoted argument and therefore is not the truncation source.
- `Platform::spawnProcess` already provides argv-based `fork`/`execv` without shell interpretation.

# Existing work to reuse

| Module/task/PR | Reuse | Evidence/path | Why it fits |
|---|---|---|---|
| Platform process launch | `spawnProcess(process, args)` | `src/framework/platform/unixplatform.cpp` | Existing exact argv boundary; avoids new abstraction. |
| Oteryn identity flow | Existing PKCE URL construction | `modules/client_entergame/oteryn_identity.lua`, merged PR #17 | Confirms product URL is correct before platform launch. |
| Client test foundation | Existing C++ test presets/support | `tests/**`, docs/agents/BUILD_TEST_MATRIX.md | Add focused regression without parallel infrastructure. |

# Ownership and overlap check

- Open PRs inspected: none currently returned by live repository PR search.
- Active tasks inspected: repository coordination snapshot and Oteryn identity catalogue entry.
- Overlaps: none found for `src/framework/platform/unixplatform.cpp` or Unix URL launch.
- Resolution: dedicated narrow fix branch/PR; no edits to upstream or unrelated platform code.

# Current state

Task claimed; implementation and focused test discovery pending.

# Plan

1. Reuse `spawnProcess` for Unix URL launch and add a focused argv-preservation regression.
2. Open a draft PR and run required CI/build tests.
3. Build an exact Linux OTClient binary and pin it into Platform rehearsal PR #126.
4. Hold merge until cross-repository physical OAuth/malformed-Gateway evidence is green.

# Work log

## 2026-07-24T12:40:00+02:00

- Changed: created task and branch.
- Learned: shell interpretation truncates OAuth URLs at the first `&`.
- Failed/blocked: current exact OTClient cannot physically reach the fake Gateway in the rehearsal.
- Result: root cause assigned to Unix platform launch boundary.

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| Reuse `spawnProcess` instead of quoting a shell command | argv preserves the URL exactly and avoids shell metacharacter/security ambiguity | not needed; local implementation choice |

# Files and interfaces

| Path/interface/config/schema | Purpose | Status |
|---|---|---|
| `src/framework/platform/unixplatform.cpp` | Shell-safe system-browser launch | planned |
| focused platform regression test | Preserve full query URL as one argv element | discovery |

# Validation and CI

| Commit | Command/check/workflow | Result | Evidence/notes |
|---|---|---|---|
| b3bcea2a95959bb4e92cc0b80cd49f36b63699b2 | source/rehearsal root-cause inspection | passed | complete PKCE generated in Lua; Unix shell command truncates at `&` |

# Failed approaches and dead ends

- Waiting for more OTClient module globals did not change the malformed-helper failure.
- Accepting Lua timeout evidence was rejected because the fake Gateway access log remained empty.

# Risks and compatibility

- Runtime: process launch path changes on Unix desktop only.
- Data/migration: none.
- Security: removes shell interpretation of externally constructed URLs.
- Backward compatibility: same browser command and asynchronous scheduling semantics; URL becomes exact rather than shell-parsed.
- Cross-repo rollout: client-first-safe; old server components are unaffected.
- Rollback: revert the narrow platform commit and binary pin.

# Remaining work

1. Discover existing platform test seam and implement the smallest regression-backed fix.

# Handoff

## Start here

Inspect current platform tests and `Platform::spawnProcess`; do not alter OAuth URL construction.

## Do not repeat

Do not weaken Platform OAuth validation or the fake Gateway access-log proof.

## Required reads

- `AGENTS.md`
- `docs/agents/BUILD_TEST_MATRIX.md`
- `docs/agents/CROSS_REPO_CONTRACTS.md`
- `src/framework/platform/unixplatform.cpp`
- `modules/client_entergame/oteryn_identity.lua`

## Open questions

- Whether current merged tests expose a direct process-launch seam or require a minimal helper extraction.

# Completion

- Final status: implementing
- PR:
- Merge commit:
- Catalogue updated: pending
- Changelog updated: pending
- Archived at:
