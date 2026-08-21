---
task_id: OTC-20260821-tibia-re-control-center-package-a-p1-isolation-3
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
created: 2026-08-21T08:46:00+02:00
updated: 2026-08-21T08:52:00+02:00
initial_base_sha: 5707af6c413cd9949f6c33b17744801cedef6eaf
related_pr: 628
parent_task: OTC-20260820-tibia-re-control-center-package-a
predecessor_repair_task: OTC-20260821-tibia-re-control-center-package-a-p1-isolation-2
fresh_isolation_authorized_by_owner: true
fresh_isolation_authorized_at: 2026-08-21T08:46:00+02:00
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
execution_budget_reason: owner-authorized fresh isolation after exact-head Codex review b42b5449 opened five new P1 findings
invocation_started_at: 2026-08-21T08:46:00+02:00
last_progress_at: 2026-08-21T08:52:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: isolation3_repair_driver
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 0
stall_warnings: 0
validation_level: full
complete_user_facing_feature: false
owned_paths:
  - tools/tibia_re_control_center/execution.py
  - tools/tibia_re_control_center/artifact.py
  - tests/tools/tibia_re_control_center/test_codex_cycle2_repairs.py
  - tests/tools/tibia_re_control_center/audit_package_a_p1.py
  - docs/agents/tasks/active/OTC-20260821-tibia-re-control-center-package-a-p1-isolation-3.md
  - docs/agents/tasks/archive/OTC-20260821-tibia-re-control-center-package-a-p1-isolation-3.md
modules_touched:
  - tibia_re_control_center
reuses:
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ARTIFACT_V1.md
  - tests/tools/tibia_re_control_center/test_codex_cycle2_repairs.py
---

# Package A P1 isolation 3

Fresh bounded repair task opened after independent exact-head review of PR #628 at `b42b5449be2b57aa4e0908e0fef408a9da37ee8f` against `main@5707af6c413cd9949f6c33b17744801cedef6eaf`.

## Exact findings

1. `PRRT_kwDOTVmdjs6bD8WK` — enforce per-action `timeout_ms` at the final dispatch gate, independently of the run deadline.
2. `PRRT_kwDOTVmdjs6bD8WM` — recursively freeze/snapshot action parameters so adapter preflight cannot mutate semantics after hash/effect validation.
3. `PRRT_kwDOTVmdjs6bD8WO` — if STOP cancels a run after durable dispatch commit but before reconciliation, record a conservative cancelled-after-dispatch outcome rather than PASS.
4. `PRRT_kwDOTVmdjs6bD8WR` — structured staged content must be privacy-classified; JSON keys such as `password` cannot bypass string scanning.
5. `PRRT_kwDOTVmdjs6bD8WV` — supplement files must use the same fail-closed privacy admission as normal staged content.

## Authority

`runtime_access:none` permanently. No official-client process access, credentials, login, GUI/gameplay input, network listener, Track A mutation, transaction or unrelated refactor.

## Required gates

- focused deterministic regressions for all five findings;
- full Package A test suite;
- `audit_package_a.py` and `audit_package_a_p1.py` PASS;
- Ruff and `git diff --check` PASS;
- exact-current-main reconciliation;
- fresh independent exact-head review with zero P0/P1/material findings;
- Ready + squash merge only after all gates pass.
