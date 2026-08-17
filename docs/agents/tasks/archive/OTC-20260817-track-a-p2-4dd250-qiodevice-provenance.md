---
task_id: OTC-20260817-track-a-p2-4dd250-qiodevice-provenance
status: completed
agent: ChatGPT
session_role: promotion_integration_coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: archived
base_branch: main
integration_base: c1ddb0e0a8a6a1634668f025837aab72d20af64e
source_pr: 490
source_head: 6d6211b89c802600ab7e749d3b08ba3f7a60840f
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
  current_writer_type: FACT:TIODeviceWriter
  current_writer_vtable_ap: FACT:0x2f69d48
  current_qiodevice_type: FACT:QTcpSocket
  current_qiodevice_owner: FACT:TGameserverTCPConnection
  current_qiodevice_shared_pair: FACT:TGameserverTCPConnection_this_plus_0x10_plus_0x18
  target_0x4dd250_identity: FACT:QDataStream_writeRawData_char_const_ptr_qint64
  canonical_payload_pointer_to_0x4dd250: FACT
  canonical_payload_length_to_0x4dd250: FACT
  qdatastream_bound_device: FACT:QTcpSocket
  qt_qtcpsocket_bound_binary_boundary: PROVEN
  final_binary_egress: PROVEN_AT_QT_QTCPSOCKET_BOUNDARY
  final_socket_owner: FACT:TGameserverTCPConnection
  final_os_socket_syscall: UNKNOWN
  framing: UNKNOWN
  sequence: UNKNOWN
  compression: UNKNOWN
  encryption: UNKNOWN
validation:
  generation_1_run: 32038672531
  generation_1_source_job: 95413976848
  generation_1_hosted_job: 95414062445
  generation_2_run: 32038917855
  generation_2_source_job: 95414621259
  generation_2_hosted_job: 95414649302
  generation_2_bundle_digest: sha256:3fa3b3118c0a988000de6c77fc9c52514f9670f9f3d7b52f2d07f63ba53071b7
  generation_3_run: 32039061786
  generation_3_source_job: 95415015967
  generation_3_hosted_job: 95415041166
  generation_3_bridge_digest: sha256:4bc45e68bc7c1530579860dfb7769d48e162a82f80fad17a098d2a695760f596
  exact_head_governance_run: 32039404811
  exact_head_governance_result: SUCCESS
  exact_head_ci_run: 32039405213
  exact_head_required_job: 95416178014
  exact_head_required_result: SUCCESS
  source_changed_files: 3
  one_shot_surface_present: false
  coordinator_review_id: 4952339069
audit:
  result: PASS_BOUNDED
  material_findings_open: 0
e2e:
  result: NOT_APPLICABLE
  reason: static exact-file/disassembly evidence only
next_research_task_created: false
future_frontiers:
  - optional Qt/QTcpSocket to Linux syscall/kernel transition
  - framing
  - sequence
  - compression
  - encryption ordering before the proven QTcpSocket boundary
next_action: none in this invocation; the task is terminal after coordinator promotion and source Draft closeout
---

# P2 `0x4dd250` / QIODevice provenance — archived

Coordinator decision: `ACCEPT_WITH_EDITS`.

The canonical same-message binary payload is proven to reach `QDataStream::writeRawData(char const*, qint64)` on a QDataStream constructed on the concrete `TGameserverTCPConnection::QTcpSocket*`. The Qt QTcpSocket-bound binary boundary and final socket owner are canonical after promotion. A specific Linux socket syscall/kernel transition remains unknown, as do framing, sequence, compression and encryption.

No additional research task is created by this closeout because the current autonomous invocation has consumed its one permitted additional task.
