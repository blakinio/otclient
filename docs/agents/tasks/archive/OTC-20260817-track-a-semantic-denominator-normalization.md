---
task_id: OTC-20260817-track-a-semantic-denominator-normalization
status: completed_on_merge
agent: ChatGPT
session_role: coverage_integration_coordinator
project_lane: otclient
lane: COVERAGE-AUDIT
track_id: official-client-re
task_kind: implementation
phase: archived
base_branch: main
base_main: f8e628a255a18ec92839bbb45ef0e3b40bef8605
pr: 460
execution_class: github_hosted
runtime_access: none
mutation_authorized: false
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: false
owner_funded_ai_api_authorized: false
ownership_released: true
owned_paths: []
source_registry:
  canonical_pr: 454
  source_baseline_pr: 304
  source_baseline_head: 43a60bd96cc644b656b200c9edbfb75578b330b6
  exact_client_version: 15.32.df7b29
  exact_client_size: 51965216
  exact_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
generation:
  source_run: 32017799293
  source_job: 95350885329
  artifact: 9284175545
  artifact_digest: sha256:cf2fb874e39af2465de76445347a118077893d9bbf213b69809b793ed4d7f577
  result: SUCCESS
  e51_denominator: 349
  e52_denominator: 642
  p0_item_denominator: 180
  p1_item_denominator: 28
  qmeta_source_run: 31790507112
  qmeta_source_job: 94736106350
  denominator_complete_is_not_semantic_complete: true
independent_artifact_audit:
  digest_match: true
  e51_unique_ids: 349
  e51_direction_split: 189_server_to_client_160_client_to_server
  e51_direct_qmeta_links: 27
  e51_semantic_support: UNKNOWN_349
  e52_unique_type_names: 642
  e52_unique_qmeta_records: 642
  e52_semantic_support: UNKNOWN_642
  p0_unique_items: 180
  p1_unique_items: 28
component_validation:
  run: 32018548728
  job: 95353113344
  result: SUCCESS
  canonical_marker: CANONICAL_COVERAGE_REGISTRY_VALIDATION_PASS
  baseline_blob_fence: PASS
  validated_denominator_payload_unchanged_after_run: true
fresh_audit:
  result: PASS
  record: docs/agents/evidence/OTC-20260817-track-a-semantic-denominator-normalization/20260817-final-audit.md
  material_findings_open_for_task: 0
current_main_drift_reconciliation:
  merged_main: f8e628a255a18ec92839bbb45ef0e3b40bef8605
  denominator_counts_changed: false
  consumed_merges:
    - worldmap physical validation/archive through #466; NO_HANDLER_CANARY_OBSERVED_BOUNDED; causal propagation unproven
    - raw XRes physical resource-to-exact-client PID evidence through #457/#459
    - raw XRes client-base helper correction through #461
    - canonical raw XRes window-identity integration #465 at f8e628a255a18ec92839bbb45ef0e3b40bef8605
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
  canonical_gate_b: NOT_PROVEN
  current_structural_in_game: NOT_PROVEN
result:
  AUD-COV-002: RESOLVED_AS_DENOMINATOR_COMPLETENESS
  protocol_denominator: 349
  protocol_semantic_support: UNKNOWN_349
  full_tibia_qmeta_denominator: 642
  full_tibia_qmeta_semantic_support: UNKNOWN_642
  p0_item_denominator: 180
  p0_live_semantics: UNKNOWN_180
  p1_item_denominator: 28
  p1_live_semantics: UNKNOWN_28
  programme_complete: false
remaining_findings:
  - AUD-COV-003 MEDIUM action/QMeta 612-vs-1004 denominator definition conflict
  - AUD-COV-004 HIGH current canonical live semantic/restart proof unavailable
  - AUD-COV-007 MEDIUM durable global coordinator checkpoint stale
e2e:
  result: NOT_APPLICABLE
  reason: deterministic repository coverage/denominator integration; no client/runtime/user-facing behavior changed
closeout:
  temporary_generator_terminal_tree: absent
  temporary_workflow_terminal_tree: absent
  active_task_terminal_tree: absent
  exact_terminal_head_repository_ci_required: true
  ready_state_required_ci_required: true
  review_threads_required_zero: true
last_completed_step: four finite canonical denominator registries materialized, integrated validator and fresh audit passed, and current-main runtime/worldmap drift through f8e628a was reconciled without changing denominator membership
next_action: run exact-head required CI and review hygiene on the refreshed PR #460 head, then merge if main remains compatible
---

# Track A semantic denominator normalization — archived

This task resolves `AUD-COV-002` as denominator completeness only. It deliberately leaves semantic numerators unknown wherever evidence is not sufficient.
