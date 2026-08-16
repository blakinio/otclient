---
task_id: OTC-20260816-linux-ci-hybrid
status: active
owner: current-agent
branch: ci/OTC-20260816-linux-ci-hybrid
base_branch: main
related_pr: "331"
feature_scope: infrastructure
completion_claim: internal_only
ownership_released: false
owned_paths:
  - .github/workflows/ci.yml
  - .github/workflows/infrastructure-retry.yml
  - .github/workflows/reusable-build-windows.yml
  - docs/agents/tasks/active/OTC-20260816-linux-ci-hybrid.md
  - docs/agents/tasks/archive/OTC-20260816-linux-ci-hybrid.md
---

# OTC-20260816 Linux CI hybrid

## Objective

Make the ordinary OTClient build/test path Linux-only on GitHub-hosted runners, including a bounded headless startup smoke of the built Linux client, while preserving Synology/self-hosted capacity exclusively for work that genuinely needs controlled runtime, LAN, real display/input, persistent sessions, or physical gameplay evidence.

## Coordination

- Owner explicitly authorized disabling Windows builds because this OTClient deployment uses Linux only.
- Owner explicitly accepted the runner boundary: deterministic/static/build/startup validation on GitHub-hosted runners; physical gameplay control and persistent runtime evidence on Synology.
- PR #328 is closed as superseded; its safe hosted-runner queue reductions are carried forward where applicable without its Windows gate.
- Live validation exposed that PR #328's already-started Windows matrix kept consuming hosted runners after the PR was closed. General CI now listens for `pull_request.closed`; the new no-work run shares the PR concurrency group, so closing a PR cancels its older in-progress CI instead of leaving orphaned build demand.
- PR #280 remains a separate specialized Synology/runtime lane and its owned files are not modified by this task.
- Historical task `OTC-20260712-client-test-foundation` still lists `.github/workflows/reusable-build-linux.yml` as owned although its implementation PR #3 is already merged. This task does not modify that file; the startup smoke is deliberately implemented in `.github/workflows/ci.yml` after the existing Linux build artifact is produced.

## Implemented scope

- Replace the required Windows compile job in `.github/workflows/ci.yml` with the existing GitHub-hosted Linux reusable build.
- Keep ordinary scope detection, fast checks, Lua checks, required aggregation, and Linux builds on GitHub-hosted Ubuntu runners.
- Add a required GitHub-hosted Linux startup-smoke job for compile-relevant non-draft changes:
  - download the `linux-linux-release` artifact from the same Actions run;
  - check dynamic-library resolution with `ldd`;
  - run the real `otclient` binary under `Xvfb` with software GL and null OpenAL output;
  - isolate persisted state with `--user-dir` under `RUNNER_TEMP`;
  - require the client to remain alive for a bounded 20-second startup window;
  - upload startup and dependency logs as evidence.
- On PR close, create only a no-work CI run in the same concurrency group so any older build for that PR is cancelled without allocating new build/test runners.
- Avoid retrying intentionally cancelled superseded CI runs.
- Remove the reusable Windows build workflow after verifying that the ordinary CI caller is replaced and no active workflow file in the current workflow inventory names another Windows build entry point.
- Do not change the dedicated Synology/Track A runtime workflows.

## Runner boundary

### GitHub-hosted runners

Responsible for deterministic and disposable validation that does not require a durable game session:

- static analysis, workflow validation and Lua syntax;
- C++/Lua unit and bounded integration tests;
- Linux release/test compilation;
- Linux client artifact dependency validation;
- bounded headless client startup smoke under a virtual X display.

### Synology/self-hosted runtime

Responsible for evidence that depends on the real controlled environment:

- persistent OTClient session and canonical runtime registration;
- real display/input ownership;
- login and physical gameplay control such as walking/clicking;
- LAN/runtime integration requiring the Synology environment;
- long-lived observations and direct runtime evidence.

A GitHub headless startup smoke is not evidence of successful physical gameplay and must never replace Synology runtime E2E where that evidence is required.

## Acceptance inventory

- [x] `CI` has no `windows-2025`, `build-windows`, or `reusable-build-windows.yml` dependency on the implementation branch.
- [x] Compile-relevant PRs require `Build - Linux` via `.github/workflows/reusable-build-linux.yml`.
- [x] Documentation/task-only changes are scoped so unrelated fast/Lua/build/smoke jobs can be skipped.
- [x] Closed PRs have a concurrency-cancellation path that emits no normal build/test work.
- [ ] Generic CI jobs are observed on GitHub-hosted Ubuntu runners on the exact implementation head.
- [ ] Exact-head Actions proves the real Linux release artifact starts under `Xvfb` and survives the bounded 20-second smoke window.
- [ ] Startup smoke evidence artifact contains dependency/startup logs.
- [x] Dedicated Synology/runtime workflow files are outside this task's changed-file set.
- [x] Runner responsibility boundary is durably recorded and explicitly prevents hosted startup smoke from being treated as physical gameplay E2E.
- [x] Superseded `cancelled` CI runs are not automatically retried.
- [ ] Workflow validation/actionlint and exact-head required CI pass.
- [ ] Related PRs are terminal: #328 closed superseded; PR #331 merged when green; #280 intentionally remains separate if still active.

## Validation

1. Inspect the exact branch diff and workflow references.
2. Verify no Windows build dependency remains in general CI.
3. Inspect PR #331 exact-head Actions jobs/runner labels.
4. Require workflow syntax/actionlint, both Linux builds, hosted client startup smoke and `CI / Required` success.
5. Verify the smoke job uses the real release artifact, a virtual display, isolated user directory, bounded liveness and no Synology runner labels.
6. Verify closed-PR events skip normal jobs while sharing the same concurrency key used by the PR's active run.
7. Merge only on the exact validated head.
8. Verify post-merge `main` and its Actions outcome.
9. Archive this task and release ownership after post-merge verification.

## Runtime E2E

`SPLIT_BY_ENVIRONMENT`:

- GitHub-hosted environment outcome required here: real release artifact headless startup smoke.
- Physical gameplay/runtime E2E remains intentionally outside this infrastructure task and belongs to the dedicated Synology/Track A runtime lane. That lane must provide its own direct display/PID/session/gameplay evidence when a task requires it.

## Context checkpoint

```yaml
state: PROVEN
phase: validation
base_head: a27b9f3383b0555142b31216672e9f0143d2cd3d
implementation_pr: 331
superseded_pr: 328
specialized_runtime_pr: 280
historical_merged_pr_with_stale_task_claim: 3
observed_orphaned_run: 31934213173
changed_paths:
  - .github/workflows/ci.yml
  - .github/workflows/infrastructure-retry.yml
  - .github/workflows/reusable-build-windows.yml (removed)
  - docs/agents/tasks/active/OTC-20260816-linux-ci-hybrid.md
next_action: validate the new exact PR head through hosted Linux builds plus real client startup smoke, audit the final diff, then merge and archive if green
```
