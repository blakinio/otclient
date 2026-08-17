---
task_id: OTC-20260817-track-a-p2-f50090-framing
status: completed
agent: ChatGPT
session_role: promotion_integration_coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: archived
base_branch: main
integration_base: c1adcf491580e28d40f215356a9e559af2ccadc4
source_pr: 493
source_head: 6d01a7eb22548256e0d4f5aff9a6d13f95f84c19
source_final_state: close_unmerged_after_promotion
final_disposition: ACCEPT_WITH_EDITS
risk: medium
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
ownership_released: true
owned_paths: []
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
accepted_result:
  dualconnection_to_binary_egress: PROVEN
  final_binary_egress: PROVEN_AT_QT_QTCPSOCKET_BOUNDARY
  final_socket_owner: FACT:TGameserverTCPConnection
  final_os_socket_syscall: UNKNOWN
  framing: PROVEN
  sequence: UNKNOWN
  compression: UNKNOWN
  encryption: UNKNOWN
  scalar_a_source: FACT:low16_ceil_payload_length_div_8
  scalar_b_source: FACT:DWORD_message_plus_0
  scalar_b_semantics: UNKNOWN
  rawdataprocessor_alignment_envelope: PROVEN
validation:
  exact_head_governance_run: 32042849047
  exact_head_governance_result: SUCCESS
  exact_head_ci_run: 32042849245
  exact_head_ci_result: SUCCESS_AFTER_ONE_INFRASTRUCTURE_RETRY
  exact_head_required_job: 95429351299
  exact_head_required_result: SUCCESS
  source_changed_files: 3
  reviews_before_disposition: 0
  threads_before_disposition: 0
audit:
  result: PASS_BOUNDED
  material_findings_open: 0
e2e:
  result: NOT_APPLICABLE
  reason: static exact-file/disassembly evidence only
next_action: continue P2 with exact producer/update provenance of DWORD(message+0) at f50107; test sequence semantics without inference from width or position
---

# P2 outbound framing — archived

Coordinator decision: `ACCEPT_WITH_EDITS`.

The canonical outbound chain now proves deterministic scalar framing before the raw payload on the already-proven `TIODeviceWriter -> QDataStream -> TGameserverTCPConnection-owned QTcpSocket` path. The exact semantic identity of `DWORD(message+0)`, sequence, compression, encryption and the optional Linux syscall boundary remain separate frontiers.
