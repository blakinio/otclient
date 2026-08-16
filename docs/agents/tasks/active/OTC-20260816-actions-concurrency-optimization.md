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
  - docs/agents/tasks/active/OTC-20260816-actions-concurrency-optimization.md
  - docs/agents/tasks/archive/OTC-20260816-actions-concurrency-optimization.md
---

# OTC-20260816 Actions concurrency optimization

## Objective

Reduce avoidable GitHub-hosted runner occupancy and queue amplification without weakening repository-required validation: documentation/task-only changes must not fan out into unrelated Lua/static-analysis jobs, compile-relevant changes must retain the existing Windows build gate, and intentionally cancelled superseded CI runs must not be automatically retried.

## Ownership and coordination

Reuses:
- existing `dorny/paths-filter` scope classifier in `.github/workflows/ci.yml`;
- existing `CI / Required` aggregate gate;
- existing one-shot infrastructure retry classifier.

Dependencies: none.

Cross-repository coordination:
- `blakinio/Otheryn`: separate CI-concurrency optimization task in PR #417; no shared branch or file ownership;
- `blakinio/Oteryn-Platform`: audited separately; current Edge Security workflow already ignores `docs/agents/**` and cancels superseded runs;
- `blakinio/freqtrade`: audited separately; live CI load is dominated by active governance PR #1563 and its risk-aware component graph.

## Live evidence at claim

- GitHub Pro concurrency pressure was observed across the owner's repositories; current repository state at 2026-08-16 showed queued CI/retry runs while other repositories occupied many GitHub-hosted runners.
- `CI` already uses per-PR/ref concurrency with `cancel-in-progress: true`.
- Every ordinary PR currently starts `Detect Build Scope`, two jobs inside `Fast Checks`, and `Lua Syntax` before `CI / Required`, even for documentation-only changes.
- `.github/workflows/infrastructure-retry.yml` treated `cancelled` as retryable when it did not find a newer run, despite intentional cancellation being part of the CI concurrency design.
- Open PR #280 owns only the dedicated Synology runner stack/migration workflow and does not overlap `.github/workflows/ci.yml` or `.github/workflows/infrastructure-retry.yml`.

## Implemented change

- `CI` now emits explicit `compile`, `fast`, and `lua` path-scope outputs.
- Documentation/task-only changes leave both `fast` and `lua` false, so reusable Fast Checks and Lua Syntax are skipped rather than allocating hosted runners.
- Compile paths are deliberately duplicated into both `fast` and `lua` filters; `CI / Required` fails closed if `compile=true` is ever inconsistent with those scopes.
- Manual dispatch and merge-queue validation force all scopes true.
- The aggregate required job validates each scope against the actual job conclusion and continues to require Windows success for a non-draft compile-scope run.
- Infrastructure retry no longer treats `cancelled` as retryable; timeout and proven startup-failure handling remain.

## Acceptance inventory

- [ ] Documentation/task-only PRs run only the scope detector plus the aggregate required gate from the general `CI` workflow; unrelated Fast Checks, Lua Syntax and Windows build are skipped.
- [x] Code/config/workflow changes still run the relevant Fast Checks and Lua gate according to explicit path scope.
- [x] Every compile-relevant path remains a subset of both fast-check and Lua-validation scope so the existing Windows build dependency cannot silently bypass those gates.
- [x] `workflow_dispatch` and merge-queue validation force the full validation scope.
- [x] `CI / Required` validates scope/result consistency and fails closed if a required scoped job is skipped or a non-required scoped job unexpectedly runs.
- [x] Windows compilation remains required for non-draft compile-scope changes.
- [x] Automatic retry remains available for `timed_out` and proven `startup_failure` infrastructure failures, but not for intentional `cancelled` conclusions.
- [ ] Workflow syntax/actionlint and exact-head required CI pass on the implementation head.
- [ ] A post-merge docs-only closeout PR proves the reduced emitted job graph on the optimized `main` before archival is merged.
- [x] No owner-funded AI/Codex/OpenAI quota is used.

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
phase: validation
owner: current-agent
branch: ci/OTC-20260816-actions-concurrency-optimization
pr: 328
head: pending-live-refresh
owned_paths:
  - .github/workflows/ci.yml
  - .github/workflows/infrastructure-retry.yml
  - docs/agents/tasks/active/OTC-20260816-actions-concurrency-optimization.md
proven:
  - scoped general CI fanout implemented
  - cancelled conclusions removed from automatic retry eligibility
  - PR #280 path ownership does not overlap this task
  - active task now carries required YAML front matter after deterministic governance audit identified the omission
next_action: inspect PR #328 exact-head emitted checks after the front-matter fix; promote from draft only after workflow validation is green
```
