---
task_id: OTC-20260816-track-a-qlibrary-linux-resolution-hosted
status: ready
agent: ChatGPT
session_id: chatgpt-qlibrary-v3-20260816-1615
session_role: researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: discovery
phase: coordinator-promotion-ready
branch: docs/OTC-20260816-track-a-qlibrary-linux-resolution-hosted-v3
base_branch: main
base_main: 259e418b2c526f93bd697f07c42b73b1fd40a914
current_main: 259e418b2c526f93bd697f07c42b73b1fd40a914
risk: low
updated: 2026-08-16T16:15:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-qlibrary-linux-resolution-hosted.md
  - docs/agents/reports/OTCLIENT-20260816-qlibrary-linux-resolution-source-correlated.md
modules_touched: []
reuses:
  - docs/agents/reports/OTCLIENT-20260816-filesystem-helper-resolver-static.md
  - historical exact-binary inventory from closed PR #354 only
  - accepted source-correlation report from PR #373
  - official qt/qtbase v6.9.3 source
supersedes_pr: 373
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
result:
  classification: OFFICIAL_QT_6_9_3_SOURCE_CORRELATED
  haswell_false_potential_candidates: [<APPDIR>/BattlEye/BEClient, <APPDIR>/BattlEye/BEClient.so, <APPDIR>/BattlEye/libBEClient, <APPDIR>/BattlEye/libBEClient.so]
  haswell_true_BEClient_so_index: 3
  actual_attempt_rule: actual dlopen attempts are a prefix of the applicable potential list and stop at first success or after a failed existing absolute candidate
  BEClient_so_generated: true
  BEClient_so_actually_attempted: UNKNOWN_RUNTIME_CONDITIONAL
  successful_mapping: UNKNOWN
provenance:
  old_validator_pr: 356
  old_validator_disposition: CLOSED_VALIDATOR_DEFECT
  accepted_replacement_pr: 373
  accepted_replacement_head: 9933e0d4aa5cdd6dddde30517c7716a5dbb3aaaa
  accepted_replacement_ready_ci_run: 31951967861
  accepted_replacement_required_job: 95176747410
  accepted_replacement_required_result: SUCCESS
  replacement_merge_blocker: branch protection required current-main exact-head required check after main advanced through bootstrap archive
validation:
  semantic_validator_run: 31950672119
  semantic_validator_result: SUCCESS
  accepted_source_final_governance_run: 31950786981
  accepted_source_final_governance_result: SUCCESS
  accepted_source_final_repository_ci_run: 31950787080
  accepted_source_final_repository_ci_result: SUCCESS
  accepted_source_checkpoint_governance_run: 31951871755
  accepted_source_checkpoint_governance_result: SUCCESS
  accepted_source_checkpoint_repository_ci_run: 31951871821
  accepted_source_checkpoint_repository_ci_result: SUCCESS
  accepted_source_ready_required_job: 95176747410
  accepted_source_ready_required_result: SUCCESS
  current_main_exact_replay_report_blob: byte-for-byte semantic report replay from #373
  current_head_track_a_governance: PENDING
  current_head_repository_ci: PENDING
  review_threads_open: 0
  e2e: NOT_APPLICABLE_WITH_REASON
  e2e_reason: public-source static semantic correlation only
audit:
  result: PASS
  material_findings_open: 0
last_completed_step: replayed the accepted two-file QLibrary result directly on current main after branch protection correctly refused the behind-by-two source PR despite green checks
next_action: open current-main PR, close PR #373 superseded, obtain exact-head governance/CI, coordinator review, mark ready and merge; archive task after merge
---

# Qt 6.9.3 QLibrary source-correlation current-main promotion

This branch contains the accepted public-source QLibrary report on the exact current trusted main. It exists only because branch protection correctly required the promotion head to include the two later non-overlapping bootstrap/archive commits. No semantic claim changed from accepted PR #373.
