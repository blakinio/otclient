---
task_id: OTC-20260816-track-a-canonical-client-window-wait-fix
status: validating
agent: ChatGPT
session_id: chatgpt-coord-window-wait-fix-20260816-1746
session_role: runtime_infrastructure_maintainer
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: runtime_worker_repair
phase: remove-temporary-validator-and-finalize
branch: fix/OTC-20260816-track-a-canonical-client-window-wait-fix
base_branch: main
base_main: ffe954be315ee29825c726b996a30fea8475a0f3
risk: medium
updated: 2026-08-16T17:55:00+02:00
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/test_tibia_official_client_re_canonical_live_session.py
  - .github/workflows/tibia-official-client-re-canonical-window-wait-fix-v2.yml
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-client-window-wait-fix.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-client-window-wait-fix/**
modules_touched: []
reuses:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/20260816-v5-worker-timeout.md
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: deterministic worker wait-budget defect is fully testable without physical runtime; no Synology execution is required or authorized for this repair
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
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
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
source_failure:
  runtime_pr: 393
  run: 31956030015
  job: 95186692121
  result: FAIL_CLOSED_WORKER_TIMEOUT
  lease_generation: 4
  registration_published: false
  gate_b_reached: false
implementation:
  production_window_wait_attempts: 120
  production_window_wait_delay_seconds: 0.25
  production_window_wait_budget_seconds: 30
  transition_worker_timeout_seconds: 300
  nested_outer_wait_removed: true
  client_liveness_checked_per_poll: true
  failure_classes: [client_exited, client_window_missing, client_window_probe_failed]
  bootstrap_probe_share_bounded_helper: true
  non_secret_stage_markers_added: true
validation:
  semantic_head: f82c35cba98690d30676fa34997895ba6daf0c82
  semantic_run: 31956997604
  semantic_job: 95189035137
  semantic_result: SUCCESS
  session_tests: 10_PASS
  transition_tests: 9_PASS
  guard_tests: 3_PASS
  lease_tests: 14_PASS
  behavioral_cases: [found_window, exited_client, live_client_missing_window, wait_budget_invariant]
  runtime_access: none
  physical_e2e: false
  final_governance: PENDING
  final_repository_ci: PENDING
acceptance:
  - production client-window discovery uses one bounded wait budget comfortably below the transition worker timeout of 300 seconds
  - no nested outer loop multiplies the window helper wait budget
  - client liveness is checked during the window wait and preserves distinct client_exited versus client_window_missing classification
  - deterministic hosted tests exercise found-window, exited-client and missing-window behavior plus production wait-budget/invocation shape
  - existing canonical transition/guard/lease tests remain green
  - no physical runtime, login, credentials, VNC, Synology or client execution is used by validation
  - temporary validator workflow is removed before promotion
  - exact-head Track A governance and repository CI pass before promotion
last_completed_step: dedicated GitHub-hosted validator 31956997604/job 95189035137 passed 10 session, 9 transition, 3 guard and 14 lease tests on fresh-main PR #395 with runtime_access:none
next_action: persist sanitized validator evidence, remove the temporary workflow, then obtain final exact-head governance/CI and coordinator promotion
---

# Track A canonical client window wait fix

The fresh-main worker repair replaces the compounded window wait with one 30-second production budget, preserves explicit liveness classifications and adds sanitized stage markers. Hosted semantic validation is green; no physical runtime was touched.
