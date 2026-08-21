---
task_id: OTC-20260820-tibia-re-control-center-package-a-p1-isolation
status: validating
agent: ChatGPT
project_lane: otclient
lane: P1-CONTROL-CORE
track_id: official-client-re
task_kind: repair
phase: validate
risk: medium
branch: feat/OTC-20260820-tibia-re-control-center-package-a
base_branch: main
created: 2026-08-20T21:37:00+02:00
updated: 2026-08-21T07:40:00+02:00
initial_base_sha: 9376ad6ff13924628749a186f2586d438f2c60bd
related_pr: 628
parent_task: OTC-20260820-tibia-re-control-center-package-a
fresh_isolation_authorized_by_owner: true
fresh_isolation_authorized_at: 2026-08-20T21:37:00+02:00
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
execution_budget_reason: owner-authorized fresh isolation after parent task exhausted three audit repair cycles
invocation_started_at: 2026-08-20T21:37:00+02:00
last_progress_at: 2026-08-21T07:40:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: isolation_cycle3_candidate_pending_ci
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 3
context_reconstruction_attempts: 0
stall_warnings: 0
validation_level: full
complete_user_facing_feature: false
owned_paths:
  - tools/tibia_re_control_center/execution.py
  - tools/tibia_re_control_center/engine.py
  - tools/tibia_re_control_center/artifact.py
  - tools/tibia_re_control_center/recorder.py
  - tests/tools/tibia_re_control_center/test_codex_review_repairs.py
  - tests/tools/tibia_re_control_center/test_codex_cycle2_repairs.py
  - tests/tools/tibia_re_control_center/audit_package_a_p1.py
  - .github/workflows/tibia-re-control-center-core.yml
  - .github/workflows/tibia-re-control-center-cycle3-repair.yml
  - docs/agents/tasks/active/OTC-20260820-tibia-re-control-center-package-a-p1-isolation.md
  - docs/agents/tasks/archive/OTC-20260820-tibia-re-control-center-package-a-p1-isolation.md
modules_touched:
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

Repair the owner-authorized Package A isolation findings without expanding runtime authority. Initial isolation covered STOP cleanup/reset overlap, post-final-hook dispatch-fence revalidation, canonical ActionRequest hash verification before deduplication, and privacy scanning of serialized adapter/runtime/session metadata. Fresh exact-head review then added setup lease cleanup, STOP/admission linearization, terminal STOP cancellation, event-metadata privacy, concrete result reason preservation, and immutable semantic/metadata snapshots.

## Acceptance

- [x] STOP cleanup-in-progress state blocks reset and mutation admission until bounded harness cleanup completes.
- [x] Final safety hook is followed by a fresh fail-closed recheck of dispatch fences and safety state before durable commit.
- [x] Canonical ActionRequest hash is recomputed from request semantics before any ledger deduplication/result reuse.
- [x] All serialized adapter/runtime/session identity metadata is privacy-scanned before RunArtifact construction.
- [x] Artifact-construction rejection always releases the admitted mutation-run lease.
- [x] Run admission linearizes with STOP and STOP-cancelled runs remain terminal after reset.
- [x] All serialized event metadata is privacy-scanned before Event construction.
- [x] Result-v1 preserves concrete failure reason codes.
- [x] Action semantics and artifact metadata are snapshotted before hash/privacy validation and reused through dispatch/persistence.
- [x] Focused regressions, full Package A tests, audits, Ruff and diff-check PASS on the new exact head.
- [ ] Fresh independent exact-head audit has zero material findings.
- [ ] Parent PR #628 is returned to Ready only after this isolation task is terminally clean.

## Validation evidence

- Predecessor `bed5d3d4f11170fe2aa6c4bc3436b608ea1a563c`: 88/88 focused tests PASS; compileall PASS; `audit_package_a.py` PASS; expanded `audit_package_a_p1.py` PASS; Ruff PASS; `git diff --check` PASS; all four GitHub workflow generations PASS.
- Fresh review of that predecessor reported six P1 plus one P2 material findings now assigned to this isolation task for repair cycle 3.
- `runtime_access:none` remains unchanged; no official-client runtime, credentials, login, gameplay or network listener is authorized.

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 2
  session_id: package-a-p1-isolation-20260821-github
  session_started_at: 2026-08-21T07:35:00+02:00
  checkpointed_at: 2026-08-21T07:40:00+02:00
  last_progress_at: 2026-08-21T07:40:00+02:00
  phase: validate
  exact_head: bed5d3d4f11170fe2aa6c4bc3436b608ea1a563c
  pull_request: 628
  active_operation: publish exact-head cycle-3 candidate, then run exact-head CI and fresh independent review
  external_run_ids: []
  operation_started_at: 2026-08-21T07:40:00+02:00
  wait_deadline_at: null
  check_generation: isolation_cycle3_candidate_pending_ci
  checks_used: 0
  status: active
  safe_to_resume: true
  resume_condition: PR #628 remains Draft and this isolation task remains sole writer for delegated repair paths
  next_action: trigger exact-head CI and fresh independent Codex review; close isolation only if both are clean
```
