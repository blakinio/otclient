---
task_id: OTC-20260816-track-a-qlibrary-linux-resolution-hosted
status: ready
agent: ChatGPT
session_id: chatgpt-qlibrary-v2-20260816-1544
session_role: researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: discovery
phase: coordinator-promotion-ready
branch: docs/OTC-20260816-track-a-qlibrary-linux-resolution-hosted-v2
base_branch: main
base_main: dbd9520e2f8cc5a26f556bffaae2a83e139615f9
current_main: 259e418b2c526f93bd697f07c42b73b1fd40a914
risk: low
updated: 2026-08-16T16:08:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-qlibrary-linux-resolution-hosted.md
  - docs/agents/reports/OTCLIENT-20260816-qlibrary-linux-resolution-source-correlated.md
modules_touched: []
reuses:
  - docs/agents/reports/OTCLIENT-20260816-filesystem-helper-resolver-static.md
  - historical exact-binary inventory from closed PR #354 only
  - official qt/qtbase v6.9.3 source
supersedes_pr: 356
depends_on: []
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_class: github_hosted
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
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
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
historical_exact_qtcore_inventory:
  source_run: 31942882982
  source_job: 95154489699
  execution_class: historical_synology_inventory_only_no_repeat
  retained_path: bin/lib/libQt6Core.so.6
  size: 8789520
  sha256: 03ac3e4eb8730c2f6cbe6e3db9eb06c03477846eb3ac46ca2ebf19423270ffc5
  soname: libQt6Core.so.6
  static_version_string_set: [6.9.3]
source_pr_failure:
  pr: 356
  disposition: CLOSED_SUPERSEDED_BY_373
  run: 31943243252
  job: 95155325324
  classification: VALIDATOR_DEFECT
  failed_expectation: append-style .so spelling not used by Qt 6.9.3
primary_source:
  qt_tag: v6.9.3
  qlibrary_unix_git_blob: afa96679a0db38f8f08ee9244175368e78c8d349
  qlibrary_unix_sha256: 9b9495f491b71e0fda0a9eff972298b118eb6f68488bb5da73f6e56c450f1a7e
  qlibrary_p_git_blob: ebc7c91d26e7af84262fe13900ffa2432335dc05
  qlibrary_p_sha256: 32d89e6dee9cbaab5777f98b0bc4dea8da45fffcb058604fdf35daa55efdc24e
result:
  classification: OFFICIAL_QT_6_9_3_SOURCE_CORRELATED
  haswell_false_potential_candidates: [<APPDIR>/BattlEye/BEClient, <APPDIR>/BattlEye/BEClient.so, <APPDIR>/BattlEye/libBEClient, <APPDIR>/BattlEye/libBEClient.so]
  haswell_true_BEClient_so_index: 3
  actual_attempt_rule: actual dlopen attempts are a prefix of the applicable potential list and stop at first success or after a failed existing absolute candidate
  BEClient_so_generated: true
  BEClient_so_actually_attempted: UNKNOWN_RUNTIME_CONDITIONAL
  successful_mapping: UNKNOWN
main_freshness_after_validation:
  from: dbd9520e2f8cc5a26f556bffaae2a83e139615f9
  to: 259e418b2c526f93bd697f07c42b73b1fd40a914
  compare_status: NON_OVERLAPPING
  files:
    - .github/scripts/test_tibia_official_client_re_canonical_live_transition.py
    - .github/scripts/tibia-official-client-re-canonical-live-session.sh
    - .github/scripts/tibia-official-client-re-canonical-live-transition.py
    - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-bootstrap-implementation.md
validation:
  semantic_validator_head: 74f1f95d1547fdd10acba207b52132d4757b0633
  hosted_source_validator_run: 31950672119
  hosted_source_validator_result: SUCCESS
  semantic_head_track_a_governance_run: 31950672049
  semantic_head_track_a_governance_result: SUCCESS
  semantic_head_repository_ci_run: 31950672278
  semantic_head_repository_ci_result: SUCCESS
  temporary_validator_workflow: REMOVED
  accepted_final_head: 91c493e4346760ccaf1cdd13ed21fc5d85271136
  accepted_final_track_a_governance_run: 31950786981
  accepted_final_track_a_governance_result: SUCCESS
  accepted_final_repository_ci_run: 31950787080
  accepted_final_repository_ci_result: SUCCESS
  final_checkpoint_head: PENDING_AFTER_THIS_TASK_ONLY_UPDATE
  final_checkpoint_track_a_governance: PENDING
  final_checkpoint_repository_ci: PENDING
  review_threads_open: 0
  e2e: NOT_APPLICABLE_WITH_REASON
  e2e_reason: public-source static semantic correlation only
audit:
  result: PASS
  material_findings_open: 0
  notes:
    - old PR #356 failure is classified as a validator defect, not negative semantic evidence
    - exact-client facts, historical QtCore inventory, official-source correlation and runtime unknowns remain explicitly separated
last_completed_step: verified corrected source-correlated report, successful semantic validator and exact final-head governance/CI, closed PR #356 superseded, and proved later trusted-main advance is non-overlapping runtime-infrastructure work
next_action: obtain final exact-head governance/CI after this task-only checkpoint update, then coordinator mark ready and squash-merge PR #373; archive and release ownership after merge
---

# Qt 6.9.3 QLibrary source-correlation task

This replacement corrects the old #356 validator defect while keeping generated potential QLibrary names separate from runtime-conditional actual `dlopen` attempts. No physical runtime, proprietary semantic probe, login/session state or anti-cheat internals are part of this task.
