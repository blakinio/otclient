---
task_id: OTC-20260816-track-a-canonical-client-window-wait-fix
status: completed
agent: ChatGPT
session_id: chatgpt-coord-window-wait-fix-20260816-1746
session_role: runtime_infrastructure_maintainer
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: runtime_worker_repair
phase: archived
base_branch: main
base_main: ffe954be315ee29825c726b996a30fea8475a0f3
implementation_pr: 395
implementation_head: 160a16ae87c60ae9eeff7cf683fbb8e393b2f31f
implementation_merge_commit: c160e6776344429058a0bb97db0b411202e3e82e
risk: medium
updated: 2026-08-16T18:01:00+02:00
policy_version: 2
prompting_standard_version: 2.1
execution_class: github_hosted
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
owner_funded_ai_api_authorized: false
source_failure:
  runtime_pr: 393
  run: 31956030015
  job: 95186692121
  result: FAIL_CLOSED_WORKER_TIMEOUT
  lease_generation: 4
  registration_published: false
  gate_b_reached: false
root_cause:
  classification: DETERMINISTIC_BOUNDED_WAIT_DEFECT
  old_window_helper_budget_seconds: 30
  old_bootstrap_outer_attempts: 100
  old_compounded_budget_seconds_approx: 3025
  transition_worker_timeout_seconds: 300
implementation:
  production_window_wait_attempts: 120
  production_window_wait_delay_seconds: 0.25
  production_window_wait_budget_seconds: 30
  nested_outer_wait_removed: true
  client_liveness_checked_per_poll: true
  failure_classes: [client_exited, client_window_missing, client_window_probe_failed]
  bootstrap_probe_share_bounded_helper: true
  non_secret_stage_markers_added: true
semantic_validation:
  head: f82c35cba98690d30676fa34997895ba6daf0c82
  run: 31956997604
  job: 95189035137
  result: SUCCESS
  session_tests: 10_PASS
  transition_tests: 9_PASS
  guard_tests: 3_PASS
  lease_tests: 14_PASS
  behavioral_cases: [found_window, exited_client, live_client_missing_window, wait_budget_invariant]
  runtime_access: none
  physical_e2e: false
final_validation:
  final_head: 160a16ae87c60ae9eeff7cf683fbb8e393b2f31f
  track_a_governance_run: 31957132608
  track_a_governance_result: SUCCESS
  repository_ci_run: 31957132867
  repository_ci_required_result: SUCCESS
  ready_state_repository_ci_run: 31957227393
  ready_state_repository_ci_required_result: SUCCESS
  review_threads_open: 0
coordinator_review:
  disposition: ACCEPT
  review_id: 4946586170
audit:
  result: PASS
  material_findings_open: 0
  superseded_prs:
    - 394
evidence_path: docs/agents/evidence/OTC-20260816-track-a-canonical-client-window-wait-fix/20260816-hosted-validation.md
runtime_nonclaims_at_completion:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
ownership: released
next_action: resume the existing blocked OTC-20260816-track-a-canonical-runtime-e2e task from current trusted main with a fresh RUNTIME admission and exactly one bounded physical bootstrap/Gate-B attempt; do not recreate this fix task
---

# Canonical client-window bounded-wait fix — terminal archive

The deterministic nested client-window wait that masked the intended runtime discriminator behind the 300-second supervisor timeout is repaired on trusted `main`. The production wait budget is now approximately 30 seconds, client liveness remains distinguishable from a missing window, and bootstrap/probe share the same bounded helper. Hosted behavioral and dependent canonical contract tests passed; the temporary validator was removed before promotion.

No physical runtime was accessed by this fix. Current runtime identity remains unregistered until the RUNTIME owner performs a fresh admitted bootstrap after this archive.
