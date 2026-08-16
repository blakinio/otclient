---
task_id: OTC-20260816-actions-concurrency-optimization
status: active
owner: current-agent
branch: ci/OTC-20260816-actions-concurrency-optimization
base_branch: main
related_pr: "328"
feature_scope: infrastructure
completion_claim: internal_only
ownership_released: false
owned_paths:
  - .github/workflows/ci.yml
  - .github/workflows/infrastructure-retry.yml
  - .github/workflows/reusable-build-windows.yml
  - docs/agents/tasks/active/OTC-20260816-actions-concurrency-optimization.md
  - docs/agents/tasks/archive/OTC-20260816-actions-concurrency-optimization.md
---

# OTC-20260816 Actions concurrency optimization

## Objective

Reduce avoidable GitHub-hosted runner occupancy and queue amplification without weakening repository-required validation: documentation/task-only changes must not fan out into unrelated Lua/static-analysis jobs, compile-relevant changes must retain the Windows build gate, superseded cancellations must not self-amplify through retry, and duplicated Windows solution setup must not consume three hosted runners when one can validate the same configurations.

## Ownership and coordination

Reuses:
- existing `dorny/paths-filter` scope classifier in `.github/workflows/ci.yml`;
- existing `CI / Required` aggregate gate;
- existing one-shot infrastructure retry classifier;
- existing Windows artifacts and CMake presets.

Dependencies: none.

Cross-repository coordination:
- `blakinio/Otheryn`: separate CI-concurrency optimization task in PR #417; no shared branch or file ownership;
- `blakinio/Oteryn-Platform`: audited separately; current live work represents applicable acceptance validation rather than proven task-only fanout;
- `blakinio/freqtrade`: audited separately; current live work represents applicable develop/governance CI rather than proven task-only fanout.

## Live evidence at claim

- GitHub Pro concurrency pressure was observed across the owner's repositories; `otclient` queued while other repositories occupied hosted runners.
- `CI` already uses per-PR/ref concurrency with `cancel-in-progress: true`.
- Ordinary documentation/task-only PRs previously started `Detect Build Scope`, two Fast Checks jobs, and Lua Syntax before `CI / Required`, even when compilation was irrelevant.
- `.github/workflows/infrastructure-retry.yml` treated `cancelled` as retryable despite intentional cancellation being part of the CI concurrency design.
- The ready-for-review validation of PR #328 proved all three Solution matrix jobs (`Debug`, `OpenGL`, `DirectX`) independently repeated `Install VS 2026 Build Tools (v145 toolset)` and occupied three Windows runners at once.
- Search of open PRs found no other active owner of `.github/workflows/reusable-build-windows.yml`.
- Open PR #280 owns only the dedicated Synology runner stack/migration workflow and does not overlap this task.

## Implemented change

- `CI` emits explicit `compile`, `fast`, and `lua` path-scope outputs.
- Documentation/task-only changes leave `fast` and `lua` false, so reusable Fast Checks and Lua Syntax are skipped instead of allocating hosted runners.
- Compile paths are duplicated into both `fast` and `lua` filters; `CI / Required` fails closed if `compile=true` is inconsistent with either prerequisite scope.
- Manual dispatch and merge-queue validation force all scopes true.
- `CI / Required` validates every scope against the actual job result and still requires Windows success for a non-draft compile-scope run.
- Infrastructure retry no longer treats `cancelled` as retryable; timeout and proven startup-failure handling remain.
- The Windows build matrix is reduced from five hosted jobs to three without removing a build target: CMake Release and CMake Tests remain separate, while Solution Debug/OpenGL/DirectX run sequentially in one Solution job after one VS/v145 + vcpkg setup.
- Solution artifact names remain `windows-solution-debug`, `windows-solution-opengl`, and `windows-solution-directx`.

## Acceptance inventory

- [ ] Documentation/task-only PRs run only the scope detector plus aggregate `CI / Required` from the general CI workflow; unrelated Fast Checks, Lua Syntax and Windows build are skipped.
- [x] Code/config/workflow changes still run relevant Fast Checks and Lua according to explicit path scope.
- [x] Every compile-relevant path remains a subset of fast-check and Lua-validation scope.
- [x] `workflow_dispatch` and merge-queue validation force full validation scope.
- [x] `CI / Required` fails closed on scope/result inconsistency.
- [x] Windows compilation remains required for non-draft compile-scope changes.
- [x] Automatic retry remains available for `timed_out` and proven `startup_failure`, but not intentional `cancelled` conclusions.
- [x] All five former Windows build targets remain covered: CMake Release, CMake Tests, Solution Debug, Solution OpenGL, Solution DirectX.
- [x] The three Solution configurations share one hosted runner/setup and preserve their three artifact names.
- [ ] Workflow syntax/actionlint and exact-head required CI pass after the consolidated Windows matrix change.
- [ ] Exact-head non-draft Windows validation proves the emitted Windows matrix contains three jobs, and all three jobs pass.
- [ ] A post-merge docs-only closeout PR proves the reduced docs-only emitted graph on optimized `main` before archival is merged.
- [x] No owner-funded AI/Codex/OpenAI quota is used.

## Validation plan

1. Inspect exact workflow diff and path-set relationships.
2. Require yamllint/actionlint on exact implementation head.
3. Require ready-for-review CI on the exact final head and verify the Windows matrix is exactly CMake Release + CMake Tests + combined Solution configurations.
4. Verify all CMake and all three MSBuild configurations succeed, with all expected artifacts retained.
5. Verify review/thread state and merge only when required CI is green.
6. Move this task to archive in a separate documentation-only closeout PR.
7. Inspect closeout emitted jobs and require only `Detect Build Scope` + `CI / Required` from general CI, with Fast Checks, Lua and Windows skipped.

## Context checkpoint

```yaml
state: PROVEN
phase: validation
owner: current-agent
branch: ci/OTC-20260816-actions-concurrency-optimization
pr: 328
head: pending-live-refresh
owned_paths:
  - .github/workflows/ci.yml
  - .github/workflows/infrastructure-retry.yml
  - .github/workflows/reusable-build-windows.yml
  - docs/agents/tasks/active/OTC-20260816-actions-concurrency-optimization.md
proven:
  - scoped general CI fanout implemented
  - cancelled conclusions removed from automatic retry eligibility
  - prior exact head passed yamllint, actionlint, Lua, Fast Checks and Track A governance
  - live non-draft run exposed duplicated VS/v145 setup across three Solution jobs
  - Windows solution configurations consolidated without dropping configuration coverage or artifact names
  - PR #280 path ownership does not overlap this task
next_action: verify the new exact head emits three Windows jobs, all pass, and aggregate CI remains green; then merge and run docs-only closeout proof
```
