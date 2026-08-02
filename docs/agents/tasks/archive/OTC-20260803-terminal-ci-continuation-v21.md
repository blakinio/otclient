---
task_id: OTC-20260803-terminal-ci-continuation-v21
status: completed
related_pr: 181
implementation_head: 77d6dae8ab405e2faafac74019524081845ecfcb
merge_commit: b689e18006c08765716822775cd0f0e310104d9c
archive_pr: 182
completed: 2026-08-03T00:31:00+02:00
owned_paths: []
---

# Bounded terminal CI continuation

## Terminal result

PR #181 merged the bounded terminal-CI continuation contract to `main` as `b689e18006c08765716822775cd0f0e310104d9c`.

The merged governance now:

- preserves the ordinary two-check limit for non-terminal CI and unchanged external state;
- permits eligible final required exact-head CI, protected auto-merge and merge-queue completion to remain in one foreground invocation for at most 45 minutes;
- requires at least three minutes between unchanged terminal-CI observations and caps them at 12 per materially new required-check generation;
- keeps terminal-CI counters separate from ordinary CI and unchanged-state counters;
- does not reset the total terminal wait budget across draft, ready-state or merge-queue generations on the same head;
- keeps direct or manual merge forbidden until all required exact-head checks pass;
- treats mandatory post-merge archival and ownership release as part of the same entry task;
- continues to forbid hidden background execution and unbounded polling.

## Closeout evidence

```yaml
implementation_complete: true
scope:
  type: documentation_and_agent_governance
  changed_paths: 6
  client_protocol_asset_workflow_changes: 0
audit:
  result: PASS_WITH_REPAIRS
  material_findings_open: 0
  repaired_findings:
    - TERMINAL-CI-001 dedicated terminal counter isolation
    - TERMINAL-CI-002 bootstrap protected-auto-merge contradiction
    - TERMINAL-CI-003 protected-auto-merge admission versus actual merge wording
e2e:
  result: NOT_APPLICABLE
  reason: documentation-only agent-governance change with no executable client, protocol, asset, workflow or production behavior
final_ci:
  head: 77d6dae8ab405e2faafac74019524081845ecfcb
  result: PASS
  runs:
    - CI 30770169421
pull_requests:
  terminal_prs:
    - blakinio/otclient#181 merged as b689e18006c08765716822775cd0f0e310104d9c
  archive_pr: blakinio/otclient#182
  unresolved_review_threads: 0
task_archived_or_terminal: true
ownership_released: true
blocker: none
```

No material finding or blocker remains. PR #182 is the lifecycle-only archive PR and becomes terminal when merged.
