---
task_id: OTC-20260817-track-a-p2-dual-nested-vcall-resolution
status: completed
agent: ChatGPT
session_role: promotion_integration_coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: archived
base_branch: main
source_pr: 483
source_head: 349530d89051391998f1f88ce686bde59a2df2c8
source_final_state: close_unmerged_after_promotion
final_disposition: ACCEPT_WITH_EDITS
risk: medium
execution_class: github_hosted
runtime_access: none
physical_e2e_required: false
mutation_authorized: false
owner_funded_ai_api_authorized: false
ownership_released: true
owned_paths: []
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
accepted_result:
  b56c93_same_message_preserved: FACT
  outer_type: FACT:tibia::network::TGameserverNetworkPacketConnection
  outer_vtable_ap: FACT:0x3084ba8
  intermediate_type: FACT:tibia::network::TGameserverNetworkPacketProcessor
  intermediate_vtable_ap: FACT:0x30b7a68
  final_receiver_vtable_ap: FACT:0x2f741d8
  final_receiver_rtti_pointer: FACT:0x30b7548
  final_receiver_exact_dynamic_type: UNKNOWN
  b56c93_virtual_slot: FACT:+0x10
  b56c93_concrete_target: FACT:0xf50090
  b56c93_target_equals_b40630: DISPROVEN
  b57042_same_message_preserved: DISPROVEN
unknown:
  - dualconnection_to_binary_egress
  - final_binary_egress
  - final_socket_ownership
  - framing
  - sequence
  - compression
  - encryption
  - semantic_role_of_0xf50090
validation:
  generation_3_run: 32035436709
  source_job: 95404656415
  hosted_job: 95404893228
  final_artifact: 9290498273
  final_artifact_digest: sha256:4aa991a9912c3fb56cc08863ba94ac9e73e78a466a966c00353e85ce39a85323
  coordinator_redownload_rehash: PASS
  coordinator_primary_constructor_review: PASS
  coordinator_primary_vtable_review: PASS
  exact_head_governance_run: 32035805051
  exact_head_governance_result: SUCCESS
  exact_head_ci_run: 32035805264
  exact_head_required_job: 95405920582
  exact_head_required_result: SUCCESS
  source_changed_files: 3
  reviews: 0
  review_threads: 0
audit:
  result: PASS_BOUNDED
  material_findings_open: 0
e2e:
  result: NOT_APPLICABLE
  reason: static exact-file/disassembly evidence only
next_action: continue P2 with bounded exact-client disassembly/dataflow of 0xf50090 preserving the same second argument; do not infer framing/sequence/compression/encryption/final socket semantics
---

# P2 nested virtual-call resolution — archived

Coordinator decision: `ACCEPT_WITH_EDITS`.

The surviving same-message path from `TGameserverDualConnection +0x78` is structurally proven through `TGameserverNetworkPacketConnection`, `TGameserverNetworkPacketProcessor`, receiver vtable AP `0x2f741d8`, slot `+0x10`, to exact target `0xf50090`. The prior `0xb40630` reachability hypothesis is disproven for this path. Transport-layer semantics beyond `0xf50090` remain unknown.
