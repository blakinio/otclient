---
task_id: OTC-20260817-track-a-p2-clientprocessor-sanitized-evidence
status: ready
agent: unassigned
session_id: chatgpt-p2-clientprocessor-sanitized-evidence-20260817
session_role: researcher_producer_under_coordinator_dispatch
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: evidence_staging
phase: coordinator-review-ready
branch: research/OTC-20260817-track-a-p2-clientprocessor-sanitized-evidence
base_branch: main
base_main: 8c9486e2c6109a7a39b564804c8acd707659b5e0
risk: medium
created: 2026-08-17T09:10:00+02:00
updated: 2026-08-17T09:20:00+02:00
producer_pr: 449
consumer_pr: 310
consumer_task: OTC-20260815-track-a-p2-buffer-downstream-consumer
consumer_head_at_claim: 9b99b6b4bda2cf01e8fadcd8a00a6827de35d825
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-p2-clientprocessor-sanitized-evidence.md
  - docs/agents/evidence/OTC-20260817-track-a-p2-clientprocessor-sanitized-evidence/**
  - .github/scripts/tibia-official-client-re-p2-clientprocessor-sanitized-evidence.py
  - .github/workflows/tibia-official-client-re-p2-clientprocessor-sanitized-evidence.yml
modules_touched: []
reuses:
  - PR #308 artifact 9251725866 for the already-promoted persistent-QBuffer boundary
  - PR #310 artifact 9252025461 for prior targeted processor observations only
  - current-main final-write reconciliation for canonical TGameserverDualConnection owner-field typing
  - PR #446 bounded file-only source-sanitize -> hosted-decode method
policy_version: 2
prompting_standard_version: 2.1
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: checkpoint_only
user_communication: low_noise
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
source_staging_exception:
  coordinator_approved: true
  owner_continuation_authorized: true
  source_executor: synology-otclient-01
  source_access: read_only_file_only
  source_runtime_access: none
  source_static_analysis: forbidden
  source_disassembly: forbidden
  source_semantic_classification: forbidden
  canonical_state_access: forbidden
  client_process_access: forbidden
  process_memory_access: forbidden
  x11_vnc_access: forbidden
  login_session_access: forbidden
  gameplay_access: forbidden
  raw_client_upload: forbidden
  client_byte_mutation: forbidden
  allowed_output: exact fence metadata plus bounded hex-encoded file windows only
  hosted_validation_executor: ubuntu-latest
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
feature_scope:
  type: contract_producer
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: partial_producer
validation:
  evidence_run: 32005141186
  evidence_result: SUCCESS
  evidence_head: 1b615736726049e70c902a88d0fde5004044e7e0
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
  final_task_only_head: 5064af2222bd1f8830cb656270f488eca45b052e
  final_task_only_head_checks: PENDING
independent_coordinator_review:
  result: PASS_BOUNDED
  artifact_result_json_trusted_as_summary: false
  source_bundle_redecoded_independently: true
  exact_fence_reverified: true
  file_boundary_reverified: true
  setup_identity_gap_closed: true
  persistent_qbuffer_to_clientprocessor_this_plus_0x18: PROVEN
  clientprocessor_vslot_plus_0x10: PROVEN_0x00c2df80
  qiodevice_readall_from_same_member: PROVEN
  same_stack_message_to_rawprocessor: PROVEN
  rawprocessor_vslot_plus_0x10: PROVEN_0x00b47130
  rawprocessor_inplace_qbytearray_transform: PROVEN
  same_stack_message_to_owner_c18_slots_plus_0x80_plus_0x78: PROVEN
  dualconnection_typing_source: current-main canonical final-write reconciliation
  protocol_stage_order: PROVEN_PARTIAL
  framing: UNKNOWN
  sequence: UNKNOWN
  compression: UNKNOWN
  encryption: UNKNOWN
  final_binary_egress: UNKNOWN
  final_socket_ownership: UNKNOWN
negative_controls:
  generic_qt_census_used_as_proof: false
  vtable_adjacency_used_as_temporal_order: false
  quarantined_run_31944051248_used_as_proof: false
  historical_final_socket_evidence_used_as_proof: false
  rawprocessor_labeled_framing_compression_or_encryption: false
  dual_slots_labeled_final_egress: false
findings_closed:
  - TACOORD-310-20260817-001
  - TACOORD-310-20260817-002
e2e:
  result: NOT_APPLICABLE
  reason: static exact-client evidence producer only; no runtime behavior or client state changed
last_completed_step: independently re-decoded artifact 9279753620 and cross-checked artifact 9279759553 against accepted #308 and current-main canonical network ownership evidence; the missing #310 object-identity gap is closed
next_action: coordinator should classify #310 ACCEPT_WITH_EDITS, promote only the bounded evidence on current main without the obsolete #310 staging workflow, then close/archive #310 and this producer intentionally
---

# Track A P2 ClientMessageProcessor sanitized exact-client evidence

The producer closed only the object-identity evidence gap for consumer PR #310. Framing, sequence, compression, encryption, final binary egress and socket ownership remain unknown.
