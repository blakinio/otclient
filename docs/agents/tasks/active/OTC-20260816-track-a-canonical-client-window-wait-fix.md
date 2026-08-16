---
task_id: OTC-20260816-track-a-canonical-client-window-wait-fix
status: ready
agent: ChatGPT
session_id: chatgpt-window-wait-fix-20260816-1742
session_role: runtime_infrastructure_maintainer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_infrastructure_fix
phase: coordinator-promotion-ready
branch: fix/OTC-20260816-track-a-canonical-client-window-wait
base_branch: main
base_main: b69084067de24528b1f763ab9630f638e8bcf092
risk: medium
updated: 2026-08-16T17:51:00+02:00
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/test_tibia_official_client_re_canonical_live_session.py
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-client-window-wait-fix.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-client-window-wait-fix/**
modules_touched: []
reuses:
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/20260816-v5-worker-timeout.md
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/test_tibia_official_client_re_canonical_live_session.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_transition.py
depends_on: []
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: deterministic trusted-worker bounded-wait defect was repaired and validated without physical runtime access
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
runner: github-hosted
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
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
owner_funded_ai_api_authorized: false
source_failure:
  runtime_pr: 393
  run: 31956030015
  job: 95186692121
  acquired_lease_generation: 4
  result: worker_timeout
  registration_published: false
  gate_b_reached: false
  credentials_used: false
root_cause:
  window_helper_attempts: 120
  window_helper_sleep_seconds: 0.25
  window_helper_max_seconds_approx: 30
  bootstrap_outer_attempts: 100
  compounded_max_seconds_approx: 3025
  transition_worker_timeout_seconds: 300
  classification: DETERMINISTIC_BOUNDED_WAIT_DEFECT
implementation:
  window_dead_pid_return_code: 2
  bootstrap_window_calls: 1
  nested_outer_wait_removed: true
  non_secret_stage_markers_added: true
  probe_failure_classification_aligned: true
validation:
  source_validated_head: 7cc7c64aa40b6662973dbc2f059a099a89a184c6
  hosted_validator_run: 31956703737
  hosted_validator_job: 95188323165
  hosted_validator_result: SUCCESS
  session_tests: 9_PASS
  transition_tests: 9_PASS
  guard_tests: 3_PASS
  lease_tests: 14_PASS
  bounded_window_validator: PASS
  validation_merge_base_main: ffe954be315ee29825c726b996a30fea8475a0f3
  temporary_validator_workflow: REMOVED
  final_head_governance: PENDING
  final_head_repository_ci: PENDING
  review_threads_open: 0
evidence_path: docs/agents/evidence/OTC-20260816-track-a-canonical-client-window-wait-fix/20260816-hosted-validation.md
audit:
  result: PASS
  material_findings_open: 0
  notes:
    - source branch was created from parent b6908406 while v5 terminal checkpoint #393 landed concurrently as ffe954be
    - hosted validator checked the pull-request merge ref combining current main ffe954be with the fix source head
    - changed executable paths do not overlap the terminal v5 task/evidence paths added by ffe954be
acceptance:
  - bootstrap invokes the already-bounded client-window helper exactly once
  - dead client during the bounded wait is classified as client_exited
  - live client with no visible Tibia window after the bounded wait is classified as client_window_missing
  - no production test-only knobs can reduce runtime identity or authority checks
  - deterministic tests prove the nested 100x wait is absent and the two failure classes are preserved
  - existing toolroot/session/transition/guard/lease tests pass on GitHub-hosted execution
  - temporary validator is removed before promotion
  - no Synology, client, X11/VNC, WARP, credentials, login or canonical registration was accessed
last_completed_step: hosted validator 31956703737/job 95188323165 passed all session/transition/guard/lease and bounded-wait checks against a merge ref containing current main ffe954be; one-shot validator removed and independent diff audit found zero material findings
next_action: obtain final exact-head Track A governance/repository CI, coordinator-promote this fix, archive ownership, then redispatch the blocked canonical RUNTIME task from the resulting trusted main
---

# Canonical client-window bounded-wait fix

The trusted worker now uses one bounded window search rather than multiplying it inside another 100-iteration loop. Hosted regression tests preserve `client_exited` versus `client_window_missing`; this task changes no physical runtime state.
