---
task_id: OTC-20260821-tibia-re-control-center-package-a-p1-isolation-2
status: completed
agent: ChatGPT
project_lane: otclient
lane: P1-CONTROL-CORE
track_id: official-client-re
task_kind: repair
phase: close
risk: medium
branch: feat/OTC-20260820-tibia-re-control-center-package-a
base_branch: main
created: 2026-08-21T07:58:00+02:00
updated: 2026-08-21T17:18:00+02:00
initial_base_sha: 73487b0746b898365c759dbfc193e914e619acfb
related_pr: 628
parent_task: OTC-20260820-tibia-re-control-center-package-a
predecessor_repair_task: OTC-20260820-tibia-re-control-center-package-a-p1-isolation
fresh_isolation_authorized_by_owner: true
fresh_isolation_authorized_at: 2026-08-21T07:52:00+02:00
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
network_listener_allowed: false
official_client_access: false
policy_version: 2
prompting_standard_version: 2.1
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
user_communication: terminal_only
execution_mode: github_connector_plus_codex
execution_budget_minutes: 120
execution_budget_reason: owner-authorized second fresh isolation after five new exact-head P1 findings exhausted the predecessor repair budget
invocation_started_at: 2026-08-21T07:58:00+02:00
last_progress_at: 2026-08-21T07:58:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: isolation2_implementation_pending
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
validation_level: full
complete_user_facing_feature: false
owned_paths:
  - tools/tibia_re_control_center/execution.py
  - tools/tibia_re_control_center/store.py
  - tools/tibia_re_control_center/artifact.py
  - tools/tibia_re_control_center/engine.py
  - tools/tibia_re_control_center/model.py
  - tests/tools/tibia_re_control_center/test_codex_cycle2_repairs.py
  - tests/tools/tibia_re_control_center/audit_package_a_p1.py
  - tests/tools/tibia_re_control_center/test_package_a.py
  - docs/agents/tasks/active/OTC-20260821-tibia-re-control-center-package-a-p1-isolation-2.md
  - docs/agents/tasks/archive/OTC-20260821-tibia-re-control-center-package-a-p1-isolation-2.md
  - _tmp_do_not_merge
  - tests/tools/tibia_re_control_center/test_cycle2_isolation.py
modules_touched:
  - tibia_re_control_center
reuses:
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ARTIFACT_V1.md
  - tests/tools/tibia_re_control_center/test_codex_cycle2_repairs.py
depends_on:
  - OTC-20260820-tibia-re-control-center-package-a
  - OTC-20260820-tibia-re-control-center-package-a-p1-isolation
blocks:
  - parent Package A closeout
cross_repository_tasks: []
ownership_released: true
---

# Package A second fresh isolated P1 repair

## Objective

Repair exactly the five P1 findings from the independent Codex review of `0701967323c9c26bdeff413bd6e3b147339606ea`, without expanding runtime authority, then return PR #628 to the normal terminal closeout path.

## Acceptance

- [ ] Recovered mutation runs cannot be rebased across STOP/restart and reacquire mutation after reset.
- [ ] `privacy_policy` is snapshotted and privacy-validated before artifact construction.
- [ ] Arbitrary staged artifact bytes cannot bypass the construction-time privacy boundary.
- [ ] Artifact safety precedence is scoped to action ledgers for the current `run_id` only.
- [ ] Dynamically constructed `ActionRequest.required_authority` is fail-closed to the `Authority` enum before capability/dispatch classification.
- [ ] Accidental `_tmp_do_not_merge` and `test_cycle2_isolation.py` files are removed.
- [ ] Focused regressions, full Package A suite, audits, Ruff and diff-check PASS.
- [ ] Fresh independent exact-head review has zero P0/P1/material findings.
- [ ] Parent PR #628 is Ready/merged only after this isolation task is terminally clean.

## Review evidence

Fresh exact-head review of `0701967323c9c26bdeff413bd6e3b147339606ea` opened:

- `PRRT_kwDOTVmdjs6bDF-5` — recovery generation/restart mutation rebase.
- `PRRT_kwDOTVmdjs6bDF_D` — unvalidated privacy policy snapshot.
- `PRRT_kwDOTVmdjs6bDF_K` — `write_stage()` privacy bypass.
- `PRRT_kwDOTVmdjs6bDF_W` — cross-run safety ledger contamination.
- `PRRT_kwDOTVmdjs6bDF_Z` — unvalidated dynamic required authority.

`runtime_access:none` remains permanent for this repair.

## Terminal Package A lifecycle closeout

Package A / `control-core` is terminally complete. Source PR #628 squash-merged as `13b3f02a07a176662d766352d9af39619775a73d` after exact-head validation and a fresh independent Codex Spark review of `d66b59724e9f1856a8007a4f57d9c644600a6134` returned no major/material findings. This record becomes authoritative when lifecycle closeout PR #649 merges.

```yaml
closeout:
  implementation_complete: true
  vertical_slice_complete: true
  delivery_classification: backend_only
  user_facing_feature_complete: false
  audit:
    result: PASS
    independent_validator: Codex Spark exact-head review
    audited_head: d66b59724e9f1856a8007a4f57d9c644600a6134
    material_findings_open: 0
  e2e:
    result: NOT_APPLICABLE
    reason: lifecycle closeout is documentation-only; Package A behavior was validated by the fake one-step non-UI E2E with runtime_access:none before source merge
  final_ci:
    head: d66b59724e9f1856a8007a4f57d9c644600a6134
    result: PASS
    required_checks:
      - TIBIA RE Control Center Package A run 32495289822 SUCCESS
      - Track A agent runtime governance run 32495289937 SUCCESS
      - repository CI run 32495290189 SUCCESS
  merge:
    pr: 628
    merge_commit: 13b3f02a07a176662d766352d9af39619775a73d
  pull_requests:
    open_related_prs: 0
    unresolved_review_threads: 0
    terminal_prs:
      - blakinio/otclient#628 merged as 13b3f02a07a176662d766352d9af39619775a73d
      - blakinio/otclient#649 merged lifecycle closeout (effective when this archive reaches main)
  task_status: completed
  task_archived: true
  ownership_released: true
  stale_branches_reconciled: true
```

No official Tibia runtime, credentials, login, GUI/gameplay input, network listener, local Ollama/model, or Track A mutation was used by this lifecycle closeout. Package B and later packages remain separate work and are not claimed complete here.
