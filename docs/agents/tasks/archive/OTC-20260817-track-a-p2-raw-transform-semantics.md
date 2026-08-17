---
task_id: OTC-20260817-track-a-p2-raw-transform-semantics
status: completed
agent: ChatGPT
session_role: promotion_integration_coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: archived
base_branch: main
integration_base: 8a5fcfd72f2554261eef91a2129c9cc076e730ea
source_pr: 497
source_head: b2a3f6ee9cbc785c20df429b5a482d6ffc92b0d9
source_final_state: close_unmerged_after_promotion
final_disposition: ACCEPT_WITH_EDITS
risk: medium
execution_class: github_hosted
runtime_access: none
persistent_session_role: none
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
  framing: PROVEN
  sequence: PROVEN
  encryption: PROVEN
  encryption_receiver: FACT:shared::TXteaHelper
  encryption_vtable_ap: FACT:0x2f63148
  encryption_transform_slot: FACT:vslot_plus_0x28_at_0xf861e0
  xtea_round_core: UNKNOWN_NOT_REQUIRED_FOR_ENCRYPTION_ROLE_CLASSIFICATION
  compression: DISPROVEN_ON_PROVEN_OUTBOUND_PATH
  compression_outside_proven_outbound_path: UNKNOWN
  final_binary_egress: PROVEN_AT_QT_QTCPSOCKET_BOUNDARY
  final_socket_owner: FACT:TGameserverTCPConnection
  final_os_socket_syscall: UNKNOWN_OPTIONAL
validation:
  exact_head_governance_run: 32060048976
  exact_head_governance_result: SUCCESS
  exact_head_ci_run: 32060049189
  exact_head_required_job: 95479139576
  exact_head_required_result: SUCCESS
  source_changed_files: 3
  reviews: 0
  threads: 0
generation:
  txtea_transform_run: 32046592885
  txtea_transform_source_job: 95435821666
  txtea_transform_hosted_job: 95435860761
  txtea_transform_window: 0xf861e0..0xf864c0
  txtea_transform_sha256: f45afa6aaf3337850d4d892692d533140f896444e4a1342c83f73cb7053de3be
  outbound_census_run: 32059752436
  outbound_census_source_job: 95478101478
  outbound_census_hosted_job: 95478152304
  protocol_window_sha256: 00cea4d539c6f4ac8695ae908535b88af7af849f27f4f69578e20cc6f49557b9
  raw_window_sha256: d0cd15d635e9452788f628f0d61d26025665d859eb6315b1c188a97d6795f993
audit:
  result: PASS_BOUNDED
  material_findings_open: 0
e2e:
  result: NOT_APPLICABLE
  reason: static exact-file/disassembly evidence only
completion:
  p2_outbound_protocol_reconstruction_at_qt_boundary: COMPLETE
  remaining_non_optional_p2_semantic_frontiers: 0
  optional_lower_boundary: Linux_socket_syscall_below_Qt_QTcpSocket
next_action: none for non-optional P2 outbound protocol semantics; optional Linux syscall tracing may be done separately if lower-than-Qt transport provenance is ever required
---

# P2 outbound transform semantics — archived

Coordinator decision: `ACCEPT_WITH_EDITS`.

The canonical official-Linux outbound path now has framing, sequence and encryption proven from bounded exact-client evidence. The concrete encryption receiver is `shared::TXteaHelper`; the conditional transform is its vslot `+0x28@0xf861e0`. Compression is independently falsified on the proven persistent-QBuffer-to-QTcpSocket outbound path, with no claim beyond that path.

No non-optional P2 outbound protocol-semantic frontier remains below the application-layer reconstruction goal. The Linux syscall beneath the already-proven Qt/QTcpSocket boundary remains intentionally optional.
