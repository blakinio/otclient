# OTC-20260816-actions-concurrency-optimization

status: active
branch: ci/OTC-20260816-actions-concurrency-optimization
base: main
pr: pending
feature_scope: infrastructure
completion_claim: internal_only

## Objective

Reduce avoidable GitHub-hosted runner occupancy and queue amplification without weakening repository-required validation: documentation/task-only changes must not fan out into unrelated Lua/static-analysis jobs, compile-relevant changes must retain the existing Windows build gate, and intentionally cancelled superseded CI runs must not be automatically retried.

## Ownership

owned_paths:
- .github/workflows/ci.yml
- .github/workflows/infrastructure-retry.yml
- docs/agents/tasks/active/OTC-20260816-actions-concurrency-optimization.md
- docs/agents/tasks/archive/OTC-20260816-actions-concurrency-optimization.md

reuses:
- existing `dorny/paths-filter` scope classifier in `.github/workflows/ci.yml`
- existing `CI / Required` aggregate gate
- existing one-shot infrastructure retry classifier

depends_on: []
blocks: []
cross_repository_tasks:
- `blakinio/Otheryn`: separate CI-concurrency optimization task; no shared branch or file ownership
- `blakinio/Oteryn-Platform`: separate CI-concurrency optimization task if live evidence warrants it
- `blakinio/freqtrade`: separate CI-concurrency optimization task if live evidence warrants it

## Live evidence at claim

- GitHub Pro concurrency pressure was observed across the owner's repositories; current repository state at 2026-08-16 showed queued CI/retry runs while other repositories occupied many GitHub-hosted runners.
- `CI` already uses per-PR/ref concurrency with `cancel-in-progress: true`.
- Every ordinary PR currently starts `Detect Build Scope`, two jobs inside `Fast Checks`, and `Lua Syntax` before `CI / Required`, even for documentation-only changes.
- `.github/workflows/infrastructure-retry.yml` treats `cancelled` as retryable when it does not find a newer run, despite intentional cancellation being part of the CI concurrency design.
- Open PR #280 owns only the dedicated Synology runner stack/migration workflow and does not overlap `.github/workflows/ci.yml` or `.github/workflows/infrastructure-retry.yml`.

## Acceptance inventory

- [ ] Documentation/task-only PRs run only the scope detector plus the aggregate required gate from the general `CI` workflow; unrelated Fast Checks, Lua Syntax and Windows build are skipped.
- [ ] Code/config/workflow changes still run the relevant Fast Checks and Lua gate according to explicit path scope.
- [ ] Every compile-relevant path remains a subset of both fast-check and Lua-validation scope so the existing Windows build dependency cannot silently bypass those gates.
- [ ] `workflow_dispatch` and merge-queue validation force the full validation scope.
- [ ] `CI / Required` validates scope/result consistency and fails closed if a required scoped job is skipped or a non-required scoped job unexpectedly runs.
- [ ] Windows compilation remains required for non-draft compile-scope changes.
- [ ] Automatic retry remains available for `timed_out` and proven `startup_failure` infrastructure failures, but not for intentional `cancelled` conclusions.
- [ ] Workflow syntax/actionlint and exact-head required CI pass on the implementation head.
- [ ] A post-merge docs-only closeout PR proves the reduced emitted job graph on the optimized `main` before archival is merged.
- [ ] No owner-funded AI/Codex/OpenAI quota is used.

## Validation plan

1. Inspect the exact workflow diff and path-set relationships.
2. Let the repository workflow validation/actionlint run on the implementation PR.
3. Verify exact-head required CI and review state.
4. Merge only when the repository merge gate is satisfied.
5. Move this task to archive in a separate documentation-only closeout PR.
6. Inspect that closeout run's emitted jobs and require `Detect Build Scope` + `CI / Required` success with unrelated general-CI jobs skipped.

## Context checkpoint

```yaml
state: PROVEN
phase: implementation
owner: current-agent
branch: ci/OTC-20260816-actions-concurrency-optimization
pr: pending
owned_paths:
  - .github/workflows/ci.yml
  - .github/workflows/infrastructure-retry.yml
  - docs/agents/tasks/active/OTC-20260816-actions-concurrency-optimization.md
next_action: open an early draft PR, then implement scoped CI fanout and cancellation-retry suppression
```
