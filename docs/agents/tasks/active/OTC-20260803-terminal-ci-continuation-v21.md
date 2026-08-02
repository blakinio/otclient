---
task_id: OTC-20260803-terminal-ci-continuation-v21
status: validating
created: 2026-08-03T00:18:00+02:00
branch: docs/OTC-20260803-terminal-ci-continuation-v21
related_pr: 181
owned_paths:
  - AGENTS.override.md
  - docs/agents/AGENTS.md
  - docs/agents/ANTI_STALL_AND_EXECUTION_BUDGET.md
  - docs/agents/AUTONOMOUS_PROGRAM_CONTINUATION.md
  - docs/agents/GITHUB_ONLY_EXECUTION.md
  - docs/agents/tasks/active/OTC-20260803-terminal-ci-continuation-v21.md
modules_touched:
  - agent-governance
reuses:
  - anti-stall policy v2
  - autonomous programme continuation contract v2.2
  - GitHub-only execution policy v3
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
- eligible terminal observations use dedicated counters and do not consume the ordinary two-check counters;
- ordinary CI and all other external waiting retain the two-check fail-closed limit;
- protected auto-merge or merge-queue admission may occur only after the final head is frozen and all non-CI gates pass, with branch protection guaranteeing final exact-head checks before merge;
- direct or manual merge remains forbidden until every required exact-head check passes;
- protected auto-merge success leads directly to merge verification and required task archival when runtime remains;
- a repository-mandated archive PR is part of the same entry task rather than an additional READY task;
- exhausted time, check or runtime limits still require an exact WAITING or ROTATE checkpoint;
- root bootstrap, local agent routing, anti-stall, autonomous continuation and GitHub-only execution now state the same rule.

## Acceptance

- [x] define a bounded terminal-CI exception with an explicit wait budget, minimum polling interval and maximum checks;
- [x] distinguish a materially new required-check generation on the same SHA from repeated unchanged polling;
- [x] keep terminal observations separate from the ordinary two-check counters;
- [x] allow protected auto-merge observation and immediate post-merge lifecycle closeout in the same entry task;
- [x] preserve branch protection and forbid direct merge before exact-head PASS;
- [x] keep ordinary external waiting and non-terminal polling limited;
- [x] require WAITING or ROTATE after the terminal-CI budget is exhausted;
- [x] align every higher-priority routing document that previously forced an early stop;
- [ ] pass exact-head repository CI;
- [ ] complete a fresh contradiction/scope audit.

## Review findings already repaired

```yaml
TERMINAL-CI-001:
  severity: medium
  finding: dedicated terminal observations were not explicitly separated from ordinary unchanged-state counters
  disposition: repaired in anti-stall policy 2.1
TERMINAL-CI-002:
  severity: medium
  finding: root and local bootstrap still required auto-merge to wait for final CI, conflicting with protected pre-authorization of ready-state checks
  disposition: repaired while preserving direct-merge prohibition and branch protection
```

## Diff review

```yaml
implementation_head_before_checkpoint: 64e22a80287ea66c554fd426d099e61e6d238c2c
changed_paths: 6
unexpected_paths: 0
client_protocol_asset_workflow_changes: 0
ordinary_ci_limit_preserved: true
terminal_ci_wait_is_bounded: true
branch_protection_required: true
direct_merge_before_required_ci: forbidden
background_execution_claimed: false
```

## Checkpoint

```yaml
base: c911e0f6fa7ad6e8824dd5e0e44e154abbbdcbc1
status: validating
pr: 181
next_action: Perform a fresh exact-diff contradiction and scope audit, update the PR evidence, then mark PR #181 ready and validate the exact final head through repository CI.
```
