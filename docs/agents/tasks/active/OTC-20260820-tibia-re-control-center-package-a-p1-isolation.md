---
task_id: OTC-20260820-tibia-re-control-center-package-a-p1-isolation
status: implementing
agent: ChatGPT
project_lane: otclient
lane: P1-CONTROL-CORE
track_id: official-client-re
task_kind: repair
phase: implement
risk: medium
branch: feat/OTC-20260820-tibia-re-control-center-package-a
base_branch: main
created: 2026-08-20T21:37:00+02:00
updated: 2026-08-20T21:37:00+02:00
initial_base_sha: 9376ad6ff13924628749a186f2586d438f2c60bd
related_pr: 628
parent_task: OTC-20260820-tibia-re-control-center-package-a
fresh_isolation_authorized_by_owner: true
fresh_isolation_authorized_at: 2026-08-20T21:37:00+02:00
runtime_access: none
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
network_listener_allowed: false
official_client_access: false
policy_version: 2
prompting_standard_version: 2.1run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
user_communication: terminal_only
execution_mode: remote_desktop_plus_github
execution_budget_minutes: 120
execution_budget_reason: owner-authorized fresh isolation after parent task exhausted three audit repair cycles
invocation_started_at: 2026-08-20T21:37:00+02:00
last_progress_at: 2026-08-20T21:37:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: isolation_implementation
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
  - tools/tibia_re_control_center/artifact.py
  - tests/tools/tibia_re_control_center/test_codex_review_repairs.py
  - tests/tools/tibia_re_control_center/audit_package_a_p1.py
  - docs/agents/tasks/active/OTC-20260820-tibia-re-control-center-package-a-p1-isolation.md
  - docs/agents/tasks/archive/OTC-20260820-tibia-re-control-center-package-a-p1-isolation.mdmodules_touched:
  - tibia_re_control_center
reuses:
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ARTIFACT_V1.md
  - tests/tools/tibia_re_control_center/test_codex_review_repairs.py
depends_on:
  - OTC-20260820-tibia-re-control-center-package-a
blocks:
  - parent Package A closeout
cross_repository_tasks: []
---

# Package A fresh isolated P1 repair

## Objective

Repair exactly four fresh P1 findings from Codex review of the repaired Package A code without expanding runtime authority: STOP cleanup/reset overlap, post-final-hook dispatch-fence revalidation, canonical ActionRequest hash verification before deduplication, and privacy scanning of serialized adapter/runtime/session artifact metadata.

## Acceptance

- [ ] STOP cleanup-in-progress state blocks reset and mutation admission until bounded harness cleanup completes.
- [ ] Final safety hook is followed by a fresh fail-closed recheck of dispatch fences and safety state before durable commit.
- [ ] Canonical ActionRequest hash is recomputed from request semantics before any ledger deduplication/result reuse.
- [ ] All serialized adapter/runtime/session identity metadata is privacy-scanned before RunArtifact construction.
- [ ] Focused regressions, full Package A tests, audits, Ruff and diff-check PASS.
- [ ] Fresh independent exact-head audit has zero material findings.
- [ ] Parent PR #628 is returned to Ready only after this isolation task is terminally clean.