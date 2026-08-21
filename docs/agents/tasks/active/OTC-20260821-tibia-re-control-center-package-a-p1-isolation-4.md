---
task_id: OTC-20260821-tibia-re-control-center-package-a-p1-isolation-4
status: in_progress
agent: ChatGPT
project_lane: otclient
lane: P1-CONTROL-CORE
track_id: official-client-re
task_kind: repair
phase: implement
risk: medium
branch: feat/OTC-20260820-tibia-re-control-center-package-a
base_branch: main
created: 2026-08-21T11:45:00+02:00
updated: 2026-08-21T11:52:00+02:00
initial_base_sha: 5707af6c413cd9949f6c33b17744801cedef6eaf
related_pr: 628
parent_task: OTC-20260820-tibia-re-control-center-package-a
predecessor_repair_task: OTC-20260821-tibia-re-control-center-package-a-p1-isolation-3
fresh_isolation_authorized_by_owner: true
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
execution_mode: github_connector_plus_actions
execution_budget_minutes: 120
repair_cycles_for_current_gate: 1
validation_level: full
complete_user_facing_feature: false
owned_paths:
  - tools/tibia_re_control_center/execution.py
  - tools/tibia_re_control_center/artifact.py
  - tools/tibia_re_control_center/recorder.py
  - tests/tools/tibia_re_control_center/test_isolation4_repairs.py
  - tests/tools/tibia_re_control_center/test_package_a.py
  - docs/agents/tasks/active/OTC-20260821-tibia-re-control-center-package-a-p1-isolation-4.md
  - docs/agents/tasks/archive/OTC-20260821-tibia-re-control-center-package-a-p1-isolation-4.md
---

# Package A P1 isolation 4

Fresh bounded repair task opened after independent exact-head review of PR #628 at `ba458260865f9dde5510823ef8682e6d9f5ed4b5` against `main@5707af6c413cd9949f6c33b17744801cedef6eaf`.

## Exact findings

1. `PRRT_kwDOTVmdjs6bHJpx` — recheck action-local deadline after `final_commit_check` and immediately before durable dispatch.
2. `PRRT_kwDOTVmdjs6bHJp2` — serialize `recover_run()` admission/publication with STOP using the run-admission linearization lock.
3. `PRRT_kwDOTVmdjs6bHJp7` — reject duplicate JSON keys before privacy classification so overwritten secret values cannot survive in persisted bytes.
4. `PRRT_kwDOTVmdjs6bHJqA` — include `source_sequence` in event privacy admission before constructing the serialized Event.

## Authority

`runtime_access:none` permanently. No official-client process access, credentials, login, GUI/gameplay input, network listener, Track A mutation, transaction or unrelated refactor.

## Validation checkpoint

Isolation-4 implementation was published only after the corrected one-shot driver completed the full Package A suite, both audits, Ruff and diff-check. The remaining transient gate failure was governance-only: this task record initially omitted the explicit NOT_APPLICABLE runtime-none admission fields. Those fields are now present.

## Required gates

Focused deterministic regressions for all four findings; full Package A suite; both audits; Ruff; diff-check; exact-current-main; fresh independent exact-head review with zero P0/P1/material findings; Ready + squash merge only after all gates pass.
