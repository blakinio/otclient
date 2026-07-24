---
task_id: OTC-20260724-validation-cost-policy
coordination_id: OTS-20260724-validation-cost-policy
status: validating
branch: dudantas/validation-cost-policy
base_branch: main
created: 2026-07-24
updated: 2026-07-24
related_pr: "19"
owned_paths:
  - docs/agents/tasks/active/OTC-20260724-validation-cost-policy.md
  - docs/agents/BUILD_TEST_MATRIX.md
modules_touched:
  - agent-governance
depends_on: []
blocks: []
cross_repo_tasks:
  - CAN-20260724-validation-cost-policy
  - OTH-20260724-validation-cost-policy
  - OTERYN-20260724-validation-cost-policy
---

# Risk-based validation policy

## Goal

Make local and CI validation proportional to changed paths, risk and coherent milestones. Agents perform focused checks during individual steps, defer compilation until the feature or phase is reviewable as a whole, and still build early for CMake, dependency, ABI, platform or blocking-risk changes.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-07-24T08:52:00+02:00
branch: dudantas/validation-cost-policy
pr: 19
status: validating
proven:
  - BUILD_TEST_MATRIX.md is mandatory startup context for OTClient agents.
  - The matrix now requires cheap focused validation during multi-step work and defers heavy compilation to coherent milestone completion.
  - Documentation, task records, Lua-only and OTUI-only commits explicitly avoid C++ builds unless compiled integration changed.
  - CMake, dependency, toolchain, public-header/ABI and platform changes still require early or affected-platform compilation.
derived:
  - OTClient agents no longer need to rebuild after every small commit while final build evidence remains mandatory for compiled changes.
unknown:
  - Exact current-head required-check conclusions until PR 19 is marked ready and workflows complete.
conflicts: []
changed_paths:
  - docs/agents/BUILD_TEST_MATRIX.md
  - docs/agents/tasks/active/OTC-20260724-validation-cost-policy.md
validation:
  - command: exact PR patch and changed-file audit
    result: PASS
    evidence: PR 19 changes only the authoritative build/test matrix and its task record; no runtime, build-system or asset path changed.
blockers: []
next_action: Mark PR 19 ready, inspect the exact-head required checks and merge only after the documentation/governance gates pass.
```
