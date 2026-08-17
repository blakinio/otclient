---
task_id: OTC-20260817-track-a-p2-clientprocessor-sanitized-evidence
status: completed
agent: ChatGPT
session_role: promotion_integration_coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: evidence_staging
phase: archived
base_branch: main
base_main: 8c9486e2c6109a7a39b564804c8acd707659b5e0
risk: medium
updated: 2026-08-17T09:34:00+02:00
execution_class: github_hosted
runtime_access: none
persistent_session_role: consumer_of_runtime_evidence
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
ownership_released: true
owned_paths: []
consumer:
  task: OTC-20260815-track-a-p2-buffer-downstream-consumer
  pr: 310
  final_state: closed_unmerged
producer_pr:
  number: 449
  final_state: closed_unmerged
  final_disposition: ACCEPT
  evidence_head: 1b615736726049e70c902a88d0fde5004044e7e0
  final_source_pr_head: dbd75c152957ae945804f81313f485430b6cb768
  terminal_comment: 5313150277
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
source_boundary:
  source_executor: synology-otclient-01
  source_access: read_only_exact_file_bounded_byte_slicing
  source_runtime_access: none
  source_static_analysis: false
  source_disassembly: false
  source_semantic_classification: false
  client_process_access: false
  process_memory_access: false
  canonical_state_access: false
  x11_vnc_access: false
  login_session_access: false
  gameplay_access: false
  raw_client_upload: false
  client_byte_mutation: false
  hosted_validation_executor: ubuntu-latest
validation:
  evidence_run: 32005141186
  evidence_result: SUCCESS
  source_job: 95312954329
  source_job_result: SUCCESS
  source_artifact: 9279753620
  source_artifact_digest: sha256:6c970c23aa95856698eb71024937ed847502fb1f040701ce04c632da32c38d32
  hosted_job: 95313213503
  hosted_job_result: SUCCESS
  final_artifact: 9279759553
  final_artifact_digest: sha256:8228d6c281cf99f45f5c880b76e7a2817130156fde4cc892a402eccf4af10528
  evidence_head_track_a_governance_run: 32005159534
  evidence_head_track_a_governance_result: SUCCESS
  evidence_head_repository_ci_run: 32005159706
  evidence_head_repository_ci_result: SUCCESS
  closeout_governance_failure_run: 32005722504
  closeout_governance_failure_reason: task-only checkpoint omitted mandatory runtime_access:none admission fields
  repair_cycles: 1
  final_source_pr_track_a_governance_run: 32006193081
  final_source_pr_track_a_governance_result: SUCCESS
  final_source_pr_repository_ci_run: 32006193202
  final_source_pr_repository_ci_result: SUCCESS
  custom_evidence_generations: 1
independent_audit:
  result: PASS_BOUNDED
  generated_result_json_used_as_primary_proof: false
  source_artifact_redecoded_independently: true
  material_findings_open: 0
accepted_output:
  persistent_qbuffer_to_clientprocessor_this_plus_0x18: PROVEN
  clientprocessor_vslot_plus_0x10: PROVEN:0xc2df80
  qiodevice_readall_from_same_member: PROVEN
  same_message_to_rawprocessor: PROVEN
  rawprocessor_vslot_plus_0x10: PROVEN:0xb47130
  rawprocessor_inplace_qbytearray_transform: PROVEN
  protocol_stage_order_support: PROVEN_PARTIAL
unknown:
  - framing
  - sequence
  - compression
  - encryption
  - final_binary_egress
  - final_socket_ownership
cleanup:
  source_pr_closed_unmerged: true
  one_shot_workflow_merged: false
  producer_script_merged: false
  evidence_promoted_by_pr: 450
  ownership_released: true
e2e:
  result: NOT_APPLICABLE
  reason: static exact-client evidence producer only; no runtime behavior changed
last_completed_step: one exact-fenced bounded source slice was decoded on GitHub-hosted infrastructure, independently audited by the coordinator, then the producer PR was closed unmerged after its metadata-only exact-head governance/CI passed
next_action: none for this producer after PR #450 merge
---

# P2 ClientMessageProcessor sanitized evidence producer — archived

This one-shot producer existed only to close the object-identity gap on #310. Its workflow and script are intentionally not promoted to `main`; the accepted evidence is carried by coordinator PR #450.
