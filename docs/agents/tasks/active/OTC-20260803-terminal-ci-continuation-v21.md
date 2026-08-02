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
- [x] complete a fresh contradiction/scope audit.

## Fresh contradiction and scope audit

```yaml
validator_role: fresh-governance-falsification
primary_inputs:
  - task acceptance criteria
  - complete live PR 181 diff
  - root and local agent routing hierarchy
  - anti-stall and GitHub-only merge constraints
audited_policy_head: ba22376ca111972b882c4f87f64e1f4dbb951b0e
result: PASS_WITH_REPAIRS
open_material_findings: 0
scope:
  changed_paths: 6
  unexpected_paths: 0
  client_code: 0
  protocol_or_assets: 0
  workflows_or_branch_protection: 0
  production_or_external_state: 0
invariants:
  ordinary_two_check_limit_preserved: true
  terminal_wait_time_bounded: true
  minimum_interval_required: true
  per_generation_check_cap_required: true
  time_budget_not_reset_between_generations: true
  dedicated_terminal_counters: true
  branch_protection_required: true
  direct_merge_before_required_ci: forbidden
  hidden_background_execution: forbidden
  archive_closeout_is_same_entry_task: true
```

## Findings repaired

```yaml
TERMINAL-CI-001:
  severity: medium
  finding: dedicated terminal observations were not explicitly separated from ordinary unchanged-state counters
  disposition: repaired in anti-stall policy 2.1
TERMINAL-CI-002:
  severity: medium
  finding: root and local bootstrap still required auto-merge to wait for final CI, conflicting with protected pre-authorization of ready-state checks
  disposition: repaired while preserving direct-merge prohibition and branch protection
TERMINAL-CI-003:
  severity: medium
  finding: GitHub-only purpose text could conflate configuring protected auto-merge with the actual merge gate
  disposition: repaired by separating pre-CI protected auto-merge admission from post-CI actual merge authority
```

## Validation classification

```yaml
e2e:
  result: NOT_APPLICABLE
  reason: documentation-only agent-governance change with no executable client, protocol, asset, workflow or production behavior
review_threads: 0
requested_changes: 0
related_open_prs:
  - blakinio/otclient#181
```

## Checkpoint

```yaml
base: c911e0f6fa7ad6e8824dd5e0e44e154abbbdcbc1
status: validating
pr: 181
audit: PASS_WITH_REPAIRS
open_material_findings: 0
next_action: Mark PR #181 ready, validate repository-required CI on the exact final head, then use protected auto-merge only after the trusted-base merge gates permit it.
```
