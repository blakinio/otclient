---
task_id: OTC-20260816-linux-ci-hybrid
status: active
owner: current-agent
branch: ci/OTC-20260816-linux-postmerge-resilience
base_branch: main
related_pr: "331"
feature_scope: infrastructure
completion_claim: internal_only
ownership_released: false
owned_paths:
  - .github/workflows/ci.yml
  - .github/workflows/infrastructure-retry.yml
  - .github/workflows/reusable-build-linux.yml
  - .github/workflows/reusable-build-windows.yml
  - docs/agents/tasks/active/OTC-20260816-linux-ci-hybrid.md
  - docs/agents/tasks/archive/OTC-20260816-linux-ci-hybrid.md
  - docs/agents/tasks/active/OTC-20260712-client-test-foundation.md
  - docs/agents/tasks/archive/OTC-20260712-client-test-foundation.md
updated: 2026-08-16
---

# OTC-20260816 Linux CI hybrid

## Objective

Make the ordinary OTClient build/test path Linux-only on GitHub-hosted runners, including a bounded headless startup smoke of the built Linux client, while preserving Synology/self-hosted capacity exclusively for work that genuinely needs controlled runtime, LAN, real display/input, persistent sessions, or physical gameplay evidence.

## Current state

The primary implementation is already merged through PR #331 (`4c50f1d5843bfe067cca19519e25e4fa9dc7ccfe` -> merge commit `c4b1919e16fb2931c74f32cb310229703dbf893c`). Exact-head CI run `31935503532` passed both hosted Linux builds, unit/Lua/integration tests, the real release-artifact startup smoke and `CI / Required`.

The first post-merge `main` run `31937211914` did not expose an OTClient regression. Its Linux configure failed while vcpkg cold-built dependencies because the pinned freetype 2.14.3 source download from `gitlab.freedesktop.org` returned HTTP 504 through all three vcpkg attempts. A retry on the same merge SHA entered both hosted `Run CMake` jobs successfully but was later cancelled by the repository's intended `main` concurrency policy when newer documentation-only commits superseded that old `main` run.

This closeout slice therefore hardens only the reusable Linux build against that demonstrated transient external-source failure, then requires a fresh full Linux build/smoke on the exact repair head and on `main` after merge before this task may be archived.

## Coordination

- Windows general CI remains intentionally disabled; it must not be reintroduced.
- Dedicated Synology/Track A runtime workflows remain outside the changed runtime scope.
- PR #328 is closed as superseded.
- PR #280 remains a separate specialized Synology/runtime lane.
- Historical task `OTC-20260712-client-test-foundation` was discovered to retain stale ownership of `.github/workflows/reusable-build-linux.yml` even though PR #3 is merged. This slice archives that terminal historical task and releases its ownership before modifying the reusable Linux workflow.
- No open PR currently claims `reusable-build-linux.yml` or `OTC-20260816-linux-ci-hybrid`.

## Implemented primary scope

- Required Windows compile job replaced by the GitHub-hosted Linux reusable build.
- Ordinary scope detection, fast checks, Lua checks, required aggregation and Linux builds remain on GitHub-hosted Ubuntu runners.
- Required hosted Linux startup smoke:
  - downloads `linux-linux-release` from the same run;
  - verifies shared-library resolution with `ldd`;
  - runs the real `otclient` under `Xvfb`, software GL and null OpenAL;
  - isolates state with `--user-dir` under `RUNNER_TEMP`;
  - requires a bounded 20-second liveness window;
  - uploads startup/dependency logs.
- PR-close cancellation emits no normal build/test work and cancels obsolete CI in the same PR concurrency group.
- Superseded cancellations are not automatically treated as infrastructure failures.
- Reusable Windows build workflow is removed; current workflow inventory and code search contain no `build-windows`, `windows-2025` or `reusable-build-windows.yml` general-CI dependency.

## Post-merge resilience slice

- Release the stale merged test-foundation ownership record.
- Cache vcpkg source downloads on hosted Linux runners to reduce repeated external fetches.
- Give the CMake configure/build action one bounded retry after a failed first attempt. A deterministic code/configuration failure will still fail the second attempt; a transient source/network failure gets one additional chance without weakening the required gate.
- Require exact-head Linux release/tests + startup smoke + `CI / Required` before merge.
- Require a fresh compile-scope `main` run after merge before task archival.

## Runner boundary

### GitHub-hosted runners

Responsible for deterministic/disposable validation that does not require a durable game session: static/workflow/Lua checks, C++/Lua/integration tests, Linux release/test compilation, artifact dependency validation and bounded headless startup smoke.

### Synology/self-hosted runtime

Responsible for persistent OTClient sessions, canonical runtime registration, real display/input ownership, login/walking/clicking, LAN/runtime integration and direct physical gameplay evidence.

A GitHub headless startup smoke is not evidence of successful physical gameplay and must never replace Synology runtime E2E where that evidence is required.

## Acceptance inventory

- [x] General `CI` has no Windows build dependency.
- [x] Compile-relevant PRs require `Build - Linux` via `.github/workflows/reusable-build-linux.yml`.
- [x] Documentation/task-only changes skip unrelated fast/Lua/build/smoke jobs.
- [x] Closed PRs share the PR concurrency key and emit no normal build/test work.
- [x] Generic CI jobs were observed on GitHub-hosted Ubuntu runners on exact implementation head `4c50f1d...`.
- [x] Exact-head run `31935503532` proves the real Linux release artifact starts under `Xvfb` and survives the bounded 20-second smoke window.
- [x] Smoke artifact `9260979303` contains dependency/startup logs; smoke job `95140721575` completed successfully.
- [x] Exact-head Linux tests job `95137457639` and release job `95137457721` passed.
- [x] Exact-head `CI / Required` job `95140827090` passed.
- [x] Dedicated Synology/runtime workflow files remain outside this task's implementation changes.
- [x] Runner responsibility boundary is durably recorded.
- [x] PR #331 is merged; #328 is closed superseded; #280 remains separate.
- [x] Initial post-merge failure classified from direct job logs as external freetype HTTP 504, not an OTClient compile regression.
- [x] Historical merged task #3 stale ownership identified and released in this closeout slice.
- [ ] Resilience PR exact head passes actionlint/workflow validation, both Linux builds, tests, startup smoke and `CI / Required`.
- [ ] Resilience PR merged.
- [ ] Fresh compile-scope `main` CI after resilience merge passes both Linux builds, startup smoke and `CI / Required`.
- [ ] Task archived and ownership released.

## Validation contract

1. Keep Windows disabled and preserve the hosted/Synology responsibility split.
2. Validate the resilience diff through exact-head Actions.
3. Require both Linux matrix builds and the same real-artifact 20-second startup smoke.
4. Merge only the validated exact head.
5. Verify the resulting compile-scope `main` run, not a docs-only run.
6. Archive this task only after post-merge `main` success.

## Runtime E2E

`SPLIT_BY_ENVIRONMENT`:

- GitHub-hosted outcome required here: Linux release/tests plus real release-artifact headless startup smoke.
- Physical gameplay/runtime E2E remains intentionally outside this infrastructure task and belongs to the dedicated Synology/Track A runtime lane.

## Context checkpoint

```yaml
state: PROVEN_WITH_POSTMERGE_INFRASTRUCTURE_FOLLOWUP
phase: closeout_resilience
primary_implementation_pr: 331
primary_implementation_head: 4c50f1d5843bfe067cca19519e25e4fa9dc7ccfe
primary_merge_commit: c4b1919e16fb2931c74f32cb310229703dbf893c
exact_head_ci_run: 31935503532
exact_head_linux_tests_job: 95137457639
exact_head_linux_release_job: 95137457721
exact_head_smoke_job: 95140721575
exact_head_required_job: 95140827090
exact_head_smoke_artifact: 9260979303
initial_postmerge_run: 31937211914
initial_postmerge_failure: EXTERNAL_FREETYPE_HTTP_504
initial_postmerge_attempt: 1
postmerge_retry_attempt: 2
postmerge_retry_result: SUPERSEDED_BY_NEWER_MAIN_CONCURRENCY
resilience_branch: ci/OTC-20260816-linux-postmerge-resilience
stale_ownership_task_archived: OTC-20260712-client-test-foundation
next_action: harden reusable Linux dependency fetch resilience, validate exact head, merge, require fresh compile-scope main CI, then archive
```
