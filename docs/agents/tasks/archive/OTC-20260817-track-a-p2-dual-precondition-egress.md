---
task_id: OTC-20260817-track-a-p2-dual-precondition-egress
status: completed
agent: ChatGPT
session_role: promotion_integration_coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: archived
base_branch: main
base_main: 83034227280dc3bfdf589a991f0fdbbabab7dc87
risk: medium
execution_class: github_hosted
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
mutation_authorized: false
owner_funded_ai_api_authorized: false
ownership_released: true
owned_paths: []
source_pr:
  number: 458
  head: c3a3d8339a9fb769847011ffb76662688d91f06c
  final_disposition: ACCEPT_WITH_EDITS
  terminal_state_after_promotion: close_unmerged
  exact_head_track_a_governance_run: 32018496831
  exact_head_track_a_governance_result: SUCCESS
  exact_head_repository_ci_run: 32018496866
  exact_head_repository_ci_result: SUCCESS
evidence_generation:
  run: 32016842999
  source_job: 95348018877
  hosted_job: 95348295109
  source_artifact: 9283851546
  source_artifact_digest: sha256:7e03ed66bff463e288b5f2414bad8190a27bf421161ba1218c2a74d7342baeab
  final_artifact: 9283858910
  final_artifact_digest: sha256:2df8405269431397f3da0601ef24d9a9a8787dc33f3b5fdd43774f1eca36922c
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
accepted_result:
  b4066b_inside_b40370_plus_0x90_function: DISPROVEN
  b40630_distinct_function_entry: FACT
  b4066b_qiodevice_write_callsite: FACT
  b4066b_receiver: FACT:b40630_this_rbx_QBuffer_QIODevice_compatible
  b4066b_receiver_exact_concrete_dynamic_type: UNKNOWN
  b4066b_payload: FACT:original_b40630_second_argument_rsi
  b4066b_direct_qtcpsocket_sink: DISPROVEN
  payload_relationship_to_promoted_same_message: UNKNOWN
  b40630_reachability_from_promoted_dualconnection_plus_0x78_or_plus_0x80: UNKNOWN
unknown:
  - framing
  - sequence
  - compression
  - encryption
  - final_binary_egress
  - final_socket_ownership
  - complete_transport_stage_order_beyond_promoted_chain
  - b40630_receiver_exact_concrete_dynamic_type
  - payload_relationship_to_promoted_same_message
  - b40630_reachability_from_promoted_dualconnection_plus_0x78_or_plus_0x80
next_task: OTC-20260817-track-a-p2-dual-nested-vcall-resolution
audit:
  result: PASS_BOUNDED
  material_findings_open: 0
e2e:
  result: NOT_APPLICABLE
  reason: static exact-file/disassembly evidence only
next_action: none for this bounded task after coordinator promotion; continue in OTC-20260817-track-a-p2-dual-nested-vcall-resolution
---

# P2 DualConnection egress discriminator — archived

Coordinator decision: `ACCEPT_WITH_EDITS`. The bounded negative result is accepted without promoting `0xb4066b` as a final socket egress. The next task resolves only the two still-untyped nested `+0x10` virtual calls at `0xb56c93` and `0xb57042`.
