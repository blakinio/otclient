---
task_id: OTC-20260817-track-a-p2-clientprocessor-sanitized-evidence
status: ready
agent: unassigned
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
updated: 2026-08-17T09:22:00+02:00
producer_pr: 449
consumer_pr: 310
consumer_task: OTC-20260815-track-a-p2-buffer-downstream-consumer
consumer_head_at_claim: 9b99b6b4bda2cf01e8fadcd8a00a6827de35d825
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-p2-clientprocessor-sanitized-evidence.md
  - docs/agents/evidence/OTC-20260817-track-a-p2-clientprocessor-sanitized-evidence/**
  - .github/scripts/tibia-official-client-re-p2-clientprocessor-sanitized-evidence.py
  - .github/workflows/tibia-official-client-re-p2-clientprocessor-sanitized-evidence.yml
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
  hosted_validation_executor: ubuntu-latest
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
validation:
  evidence_run: 32005141186
  evidence_result: SUCCESS
  evidence_head: 1b615736726049e70c902a88d0fde5004044e7e0
  source_job: 95312954329
  source_artifact: 9279753620
  source_artifact_digest: sha256:6c970c23aa95856698eb71024937ed847502fb1f040701ce04c632da32c38d32
  hosted_job: 95313213503
  final_artifact: 9279759553
  final_artifact_digest: sha256:8228d6c281cf99f45f5c880b76e7a2817130156fde4cc892a402eccf4af10528
  evidence_head_track_a_governance_run: 32005159534
  evidence_head_track_a_governance_result: SUCCESS
  evidence_head_repository_ci_run: 32005159706
  evidence_head_repository_ci_result: SUCCESS
independent_coordinator_review:
  result: PASS_BOUNDED
  source_bundle_redecoded_independently: true
  exact_fence_reverified: true
  source_file_boundary_reverified: true
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
last_completed_step: source artifact independently re-decoded; missing #310 object-identity evidence gap closed
next_action: coordinator should classify #310 ACCEPT_WITH_EDITS and promote only the bounded evidence from current main; obsolete #310 staging workflow must remain unmerged
---

# Track A P2 ClientMessageProcessor sanitized exact-client evidence

Transport semantics beyond the proven partial stage order remain unknown.
