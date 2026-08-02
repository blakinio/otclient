---
task_id: OTC-20260803-terminal-ci-continuation-v21
status: validating
created: 2026-08-03T00:18:00+02:00
branch: docs/OTC-20260803-terminal-ci-continuation-v21
related_pr: 181
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

The previous contract required a stop after two CI checks for one exact head even when implementation was complete, auto-merge was enabled and a new ready-state required check was the only remaining gate. This forced repeated owner messages before merge and archive closeout.

## Scope

Governance documentation only. No client code, protocol, assets, workflows, branch protection, production state or external repository mutation.

## Implemented contract

- anti-stall policy version `2.1` adds a terminal-CI wait budget of 45 minutes;
- unchanged terminal-CI checks require at least a three-minute interval and are capped at 12 per required-check generation;
- draft, ready-state and merge-queue checks on one SHA are separate generations only when GitHub creates a materially new required-check set;
- the terminal wait budget does not reset across generations on the same head;
- ordinary CI and all other external waiting retain the two-check fail-closed limit;
- protected auto-merge success leads directly to merge verification and required task archival when runtime remains;
- a repository-mandated archive PR is part of the same entry task rather than an additional READY task;
- exhausted time, check or runtime limits still require an exact WAITING or ROTATE checkpoint.

## Acceptance

- [x] define a bounded terminal-CI exception with an explicit wait budget, minimum polling interval and maximum checks;
- [x] distinguish a materially new required-check generation on the same SHA from repeated unchanged polling;
- [x] allow protected auto-merge observation and immediate post-merge lifecycle closeout in the same entry task;
- [x] keep ordinary external waiting and non-terminal polling limited;
- [x] require WAITING or ROTATE after the terminal-CI budget is exhausted;
- [x] update both governing contracts consistently;
- [ ] pass exact-head repository CI;
- [ ] complete a fresh contradiction/scope audit.

## Diff review

```yaml
implementation_head_before_checkpoint: 57e508e468287210fcfede2a41ceaf569ec16727
changed_paths: 3
unexpected_paths: 0
client_protocol_asset_workflow_changes: 0
ordinary_ci_limit_preserved: true
terminal_ci_wait_is_bounded: true
background_execution_claimed: false
```

## Checkpoint

```yaml
base: c911e0f6fa7ad6e8824dd5e0e44e154abbbdcbc1
status: validating
pr: 181
next_action: Validate the final exact head through repository CI, audit the three-path diff for contradictions and unsafe polling expansion, then mark the PR ready only when all gates pass.
```
