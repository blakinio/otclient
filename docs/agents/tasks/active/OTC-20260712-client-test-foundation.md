---
task_id: OTC-20260712-client-test-foundation
coordination_id: ""
status: review
agent: Codex
branch: test/client-test-foundation
base_branch: main
created: 2026-07-12T08:10:03Z
updated: 2026-07-13T00:10:00Z
last_verified_commit: ab942241c5824645b97663420172c993ed6e1b08
risk: medium
related_issue: ""
related_pr: "https://github.com/blakinio/otclient/pull/3"
depends_on: []
blocks: []
owned_paths:
  - tests/**
  - docs/testing-strategy.md
  - docs/regression-test-backlog.md
  - CMakePresets.json
  - .github/workflows/reusable-build-linux.yml
  - .github/workflows/reusable-build-windows.yml
  - .github/workflows/test-analysis.yml
modules_touched: []
reuses:
  - existing otclient_add_gtest CMake helper
  - existing GoogleTest and CTest infrastructure
  - existing OTML and spectator tests
public_interfaces:
  - test-only CMake targets and CTest labels
  - tests/support builders, assertions, fakes, and TestEnvironment
  - tests/lua lightweight runner and stubs
cross_repo_tasks: []
---

# Goal

Establish deterministic unit, integration, contract, Lua, and regression-test foundations for OTClient Redemption without changing production client behavior.

# Acceptance criteria

- [x] Shared C++ test support has representative real uses and lifecycle coverage.
- [x] InputMessage and OutputMessage semantics have deterministic unit coverage.
- [x] Representative tile, OTML, protocol-contract, Lua, and loopback integration tests exist.
- [x] Tests are selectable with CTest labels and supported presets.
- [x] Linux, Windows, and macOS CI pass on the current implementation commit.
- [x] Module catalogue and testing documentation describe the reusable foundation.
- [x] Cross-repository impact is recorded as none; no Canary runtime dependency was added.
- [ ] Architectural review completed; merge is intentionally outside this task per user instruction.

# Confirmed context

- PR #3 targets `blakinio/otclient:main` from `blakinio/otclient:test/client-test-foundation`.
- The branch was created directly from `origin/main` and later fast-forwarded to merge commit `ab942241c`, which synchronizes current `main` into the task branch.
- `upstream` points to `opentibiabr/otclient` and was not mutated.
- The final implementation diff contains no `src/**`, runtime asset, branch-protection, Ruleset, or repository-setting changes.
- Client-assets installation and runtime paths were not modified.

# Existing work to reuse

| Module/task/PR | Reuse | Evidence/path | Why it fits |
|---|---|---|---|
| Existing GoogleTest support | `otclient_add_gtest` and stable targets | `tests/CMakeLists.txt` | Preserves the repository test model and target names. |
| Existing map/OTML tests | Kept in place and extended additively | `tests/map`, `tests/otml` | Avoids a risky mechanical migration. |
| Client test foundation PR #3 | Builders, assertions, fakes, environment, Lua runner | `tests/support/**`, `tests/lua/**` | Canonical reusable support introduced by this task. |

# Ownership and overlap check

- Open PRs inspected: #3 and documentation-only #6.
- Active tasks inspected: no task file existed before this handoff record.
- Overlaps: PR #6 changes coordination rules but not this unique task file or test implementation.
- Resolution: leave `ACTIVE_WORK.md` unchanged because it already lists PR #3; add only the task-owned handoff file.

# Current state

Implementation is complete and PR #3 is ready for architectural review. CI run 15 completed successfully on implementation commit `ab942241c`.

# Plan

1. Commit and push this task handoff record.
2. Confirm the documentation-only head check succeeds.
3. Update the PR body with exact final results and stop without merging.

# Work log

## 2026-07-12 to 2026-07-13

- Changed: added additive C++/Lua test organization, shared support, message/tile/OTML/contracts/loopback tests, labels, presets, CI, analysis jobs, strategy, and regression backlog.
- Learned: parser reads in function arguments must not rely on evaluation order; creature fixtures require initialized texture globals; Windows tests require `NOMINMAX` and the supported `x64-windows` triplet.
- Failed/blocked: local full C++ build was unavailable because this host lacks the repository vcpkg toolchain; repository CI supplied the full supported build environment.
- Result: CI run 15 passed on all emitted required jobs and supported desktop platforms.

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| Keep existing test directories and targets; add the new hierarchy alongside them. | Minimizes diff risk and preserves target stability. | Documented in `docs/testing-strategy.md`. |
| Use a bounded local loopback integration test instead of Canary. | Deterministic, offline, and exercises packet framing without a full login flow. | Documented in `docs/testing-strategy.md`. |
| Do not change production behavior for discovered fragment-name or gameplay cases. | Foundation PR must not bundle unrelated fixes; cases are recorded in the regression backlog. | None. |

# Files and interfaces

| Path/interface/config/schema | Purpose | Status |
|---|---|---|
| `tests/support/**` | Shared deterministic builders, assertions, fakes, and environment | complete |
| `tests/unit/**` | Message, tile, contract, and support unit tests | complete |
| `tests/integration/protocol/**` | Bounded local packet loopback | complete |
| `tests/lua/**` | Lightweight runner, stubs, unit and contract tests | complete |
| `CMakePresets.json`, test CMake files | Labels and supported test/analysis presets | complete |
| `.github/workflows/**` | Required labeled tests and optional analysis | complete |
| Testing documentation | Strategy and regression backlog | complete |

# Validation and CI

| Commit | Command/check/workflow | Result | Evidence/notes |
|---|---|---|---|
| `ab942241c` | CI run 15 / Linux unit label | passed | 56/56, 0.97 seconds real. |
| `ab942241c` | CI run 15 / Lua label | passed | 3/3 CTest registrations, 0.02 seconds; registrations execute 7 positive cases plus the failure contract. |
| `ab942241c` | CI run 15 / integration label | passed | 1/1 loopback test, 0.03 seconds. |
| `ab942241c` | CI run 15 / Windows CMake Tests | passed | Dedicated Windows configure, build, and CTest job. |
| `ab942241c` | CI run 15 / Linux release, Windows variants, macOS, Docker, Required | passed | All emitted non-skipped jobs succeeded. |
| working branch | Local preset JSON, Lua bytecode, runner failure, YAML, diff checks | passed | Full C++ validation delegated to CI due missing local vcpkg toolchain. |
| `ab942241c` | ASAN and coverage | not-run | Optional manual workflow; no threshold is required in this foundation PR. |

# Failed approaches and dead ends

- A custom Windows debug triplet exposed an unsupported Abseil header configuration; the supported `x64-windows` preset is used instead.
- Unsequenced packet reads reversed values on compilers with a different argument evaluation order; reads are now explicit sequential statements.
- Initial synthetic creature fixtures lacked required global texture initialization; `TestEnvironment` now owns that test-only lifecycle.

# Risks and compatibility

- Runtime: no production runtime code changed.
- Data/migration: none.
- Security: asset hash and fallback defaults remain untouched.
- Backward compatibility: existing test target names and directories remain available.
- Cross-repo rollout: none; Canary is not a required dependency.
- Rollback: revert the test/CI/docs commits; no runtime state migration exists.

# Remaining work

1. Obtain architectural review; do not merge automatically.
2. Run optional ASAN/coverage manually in a follow-up if reviewers request evidence.
3. Implement backlog regressions in focused future PRs with any required production fixes.

# Handoff

## Start here

- PR #3 body and checks.
- `docs/testing-strategy.md`.
- `docs/regression-test-backlog.md`.
- `tests/support/**` for reusable test utilities.

## Do not repeat

- Do not recreate the test branch from governance work; its ancestry and current main synchronization are already verified.
- Do not retry the discarded custom Windows debug triplet.
- Do not turn Canary into a normal unit-test dependency.

## Required reads

- `AGENTS.md`
- `docs/agents/ACTIVE_WORK.md`
- `docs/agents/MODULE_CATALOG.md`
- `docs/testing-strategy.md`
- `docs/regression-test-backlog.md`

## Open questions

- Whether optional ASAN/coverage should become scheduled after the foundation is reviewed.
- Which regression-backlog item should be the first focused production-fix PR.

# Completion

- Final status: ready for architectural review; no automatic merge per explicit user instruction.
- PR: https://github.com/blakinio/otclient/pull/3
- Merge commit: none
- Catalogue updated: yes, on synchronized main documentation.
- Changelog updated: yes, on synchronized main documentation.
- Archived at: not archived while PR remains open.
