---
task_id: OTC-20260816-linux-ci-hybrid
status: active
owner: current-agent
branch: ci/OTC-20260816-linux-ci-hybrid
base_branch: main
related_pr: null
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

Make the ordinary OTClient build/test path Linux-only on GitHub-hosted runners while preserving Synology/self-hosted capacity exclusively for work that genuinely needs controlled runtime, LAN, display, or persistent-environment evidence.

## Coordination

- Owner explicitly authorized disabling Windows builds because this OTClient deployment uses Linux only.
- PR #328 is closed as superseded; its safe hosted-runner queue reductions are carried forward where applicable without its Windows gate.
- PR #280 remains a separate specialized Synology/runtime lane and its owned files are not modified by this task.

## Implemented scope

- Replace the required Windows compile job in `.github/workflows/ci.yml` with the existing GitHub-hosted Linux reusable build.
- Keep ordinary scope detection, fast checks, Lua checks, required aggregation, and Linux builds on GitHub-hosted Ubuntu runners.
- Avoid retrying intentionally cancelled superseded CI runs.
- Remove the reusable Windows build workflow after verifying that the ordinary CI caller is replaced and no active workflow file in the current workflow inventory names another Windows build entry point.
- Do not change the dedicated Synology/Track A runtime workflows.

## Acceptance inventory

- [ ] `CI` has no `windows-2025`, `build-windows`, or `reusable-build-windows.yml` dependency.
- [ ] Compile-relevant PRs require `Build - Linux` via `.github/workflows/reusable-build-linux.yml`.
- [ ] Documentation/task-only changes do not allocate unrelated fast/Lua/build runners.
- [ ] Generic CI jobs use GitHub-hosted Ubuntu runners.
- [ ] Dedicated Synology/runtime workflow files remain unchanged.
- [ ] Superseded `cancelled` CI runs are not automatically retried.
- [ ] Workflow validation/actionlint and exact-head required CI pass.
- [ ] Related PRs are terminal: #328 closed superseded; implementation PR merged when green; #280 intentionally remains separate if still active.

## Validation

1. Inspect the exact branch diff and workflow references.
2. Verify no Windows build dependency remains in general CI.
3. Open a PR and inspect exact-head Actions jobs/runner labels.
4. Require workflow syntax/actionlint and `CI / Required` success.
5. Merge only on the exact validated head.
6. Archive this task and release ownership after post-merge verification.

## Runtime E2E

`NOT_APPLICABLE_WITH_REASON`: this task changes CI routing rather than product runtime behavior. The real GitHub Actions run on the implementation head is the environment/outcome verification. The dedicated Synology runtime lane remains responsible for runtime/display/LAN evidence.

## Context checkpoint

```yaml
state: PROVEN
phase: implementation
base_head: a27b9f3383b0555142b31216672e9f0143d2cd3d
superseded_pr: 328
specialized_runtime_pr: 280
next_action: remove the Windows reusable build, inspect the exact diff, open the implementation PR, and validate exact-head Actions
```
