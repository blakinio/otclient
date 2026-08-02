---
task_id: OTC-20260803-terminal-ci-continuation-v21
status: implementing
created: 2026-08-03T00:18:00+02:00
branch: docs/OTC-20260803-terminal-ci-continuation-v21
owned_paths:
  - docs/agents/ANTI_STALL_AND_EXECUTION_BUDGET.md
  - docs/agents/AUTONOMOUS_PROGRAM_CONTINUATION.md
  - docs/agents/tasks/active/OTC-20260803-terminal-ci-continuation-v21.md
modules_touched:
  - agent-governance
reuses:
  - anti-stall policy v2
  - autonomous programme continuation contract v2.2
depends_on: []
blocks: []
complete_user_facing_feature: false
---

# Bounded terminal CI continuation

## Purpose

Permit one foreground owner invocation to remain active through final required exact-head CI, protected auto-merge and mandatory post-merge task closeout without allowing indefinite polling.

## Problem

The current contract requires a stop after two CI checks for one exact head even when implementation is complete, auto-merge is enabled and a new ready-state required check is the only remaining gate. This forces repeated owner messages before merge and archive closeout.

## Scope

Governance documentation only. No client code, protocol, assets, workflows, branch protection, production state or external repository mutation.

## Acceptance

- define a bounded terminal-CI exception with an explicit wait budget, minimum polling interval and maximum checks;
- distinguish a materially new required-check generation on the same SHA from repeated unchanged polling;
- allow protected auto-merge observation and immediate post-merge lifecycle closeout in the same entry task;
- keep ordinary external waiting and non-terminal polling limited;
- require WAITING or ROTATE after the terminal-CI budget is exhausted;
- update both governing contracts consistently;
- pass exact-head repository CI and a fresh contradiction/scope audit.

## Checkpoint

```yaml
base: c911e0f6fa7ad6e8824dd5e0e44e154abbbdcbc1
status: implementing
next_action: Update the two governance contracts with the bounded terminal-CI continuation exception, review the exact diff, then validate through the draft PR.
```
