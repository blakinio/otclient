---
task_id: OTC-20260724-validation-cost-policy
coordination_id: OTS-20260724-validation-cost-policy
status: implementing
branch: dudantas/validation-cost-policy
base_branch: main
created: 2026-07-24
updated: 2026-07-24
related_pr: ""
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

Make local and CI validation proportional to changed paths and risk, avoiding compilation for clearly non-build-affecting changes while retaining relevant builds for C++, build-system, dependency and platform work.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-07-24T08:00:00+02:00
branch: dudantas/validation-cost-policy
status: implementing
proven:
  - BUILD_TEST_MATRIX.md is mandatory startup context for OTClient agents.
derived:
  - Updating that matrix is sufficient to make the validation policy authoritative without broad root-governance edits.
unknown: []
conflicts: []
changed_paths:
  - docs/agents/tasks/active/OTC-20260724-validation-cost-policy.md
validation: []
blockers: []
next_action: Update BUILD_TEST_MATRIX.md and inspect the branch diff.
```
