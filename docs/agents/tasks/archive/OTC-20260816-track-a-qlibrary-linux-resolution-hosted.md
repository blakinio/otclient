---
task_id: OTC-20260816-track-a-qlibrary-linux-resolution-hosted
status: completed
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: discovery
phase: closeout
base_branch: main
implementation_pr: 377
superseded_prs: [356, 373]
implementation_merge_commit: 0da52e479c0fb9c3c6b1063d1cb516c71bacb31b
risk: low
updated: 2026-08-16T16:20:00+02:00
execution_mode: github-only
execution_class: github_hosted
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
mutation_authorized: false
owner_funded_ai_api_authorized: false
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
result:
  classification: OFFICIAL_QT_6_9_3_SOURCE_CORRELATED
  client_generated_input: <APPDIR>/BattlEye/BEClient
  client_appends_so: false
  BEClient_so_generated_by_qt: true
  haswell_false_BEClient_so_index: 1
  haswell_true_BEClient_so_index: 3
  actual_attempt_rule: actual dlopen attempts are a prefix of the applicable potential list and stop at first success or after a failed existing absolute candidate
  BEClient_so_actually_attempted: UNKNOWN_RUNTIME_CONDITIONAL
  successful_mapping: UNKNOWN
  exact_final_mapped_filesystem_object: UNKNOWN
validation:
  semantic_validator_run: 31950672119
  semantic_validator_result: SUCCESS
  accepted_source_final_governance_run: 31950786981
  accepted_source_final_governance_result: SUCCESS
  accepted_source_final_repository_ci_run: 31950787080
  accepted_source_final_repository_ci_result: SUCCESS
  current_main_replay_head: d1bdea86fab8ba0068e329209622e0a7180f2ba0
  current_main_replay_governance_run: 31952255823
  current_main_replay_governance_result: SUCCESS
  current_main_replay_repository_ci_run: 31952255885
  current_main_replay_repository_ci_result: SUCCESS
  ready_state_repository_ci_run: 31952308436
  ready_state_required_job: 95177585542
  ready_state_required_result: SUCCESS
  coordinator_review_id: 4946380413
  review_threads_open: 0
audit:
  result: PASS
  material_findings_open: 0
  notes:
    - PR 356 failure was a validator defect, not negative semantic evidence
    - PR 373 carried the accepted semantic result but became behind trusted main and was closed superseded rather than bypass branch protection
    - PR 377 replayed the accepted report directly on exact current main before promotion
    - exact-client facts, historical QtCore inventory, public Qt source correlation and runtime unknowns remain separated
e2e:
  result: NOT_APPLICABLE_WITH_REASON
  reason: public-source static semantic correlation only
ownership_released: true
next_action: none
---

# Qt 6.9.3 QLibrary source-correlation — terminal closeout

PR #377 promoted the corrected public-source QLibrary correlation to trusted `main`. The accepted exact-client predecessor still ends in extensionless `BattlEye/BEClient`; Qt 6.9.3 source generates decorated candidate names including `BEClient.so`, while the actual runtime attempt sequence and successful mapped object remain explicitly unknown until separate physical evidence exists.
