---
task_id: OTC-20260817-track-a-p2-sequence-provenance
status: completed
agent: ChatGPT
session_role: promotion_integration_coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: archived
base_branch: main
integration_base: 0aed48da9a51730c590d0ffe4688f149b359a170
source_pr: 495
source_head: 4a98632046936fba070653196d91e9f82e6b07e7
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
  sequence_field: FACT:DWORD_message_plus_0
  sequence_owner: FACT:TGameserverDualConnection_this_plus_0x9c
  sequence_update: FACT:store_current_then_increment_by_one
  sequence_initialization_or_reset_policy: UNKNOWN
  compression: UNKNOWN
  encryption: UNKNOWN
  final_binary_egress: PROVEN_AT_QT_QTCPSOCKET_BOUNDARY
  final_socket_owner: FACT:TGameserverTCPConnection
  final_os_socket_syscall: UNKNOWN
validation:
  exact_head_governance_run: 32045117129
  exact_head_governance_result: SUCCESS
  exact_head_ci_run: 32045117287
  exact_head_required_job: 95431242465
  exact_head_required_result: SUCCESS
  source_changed_files: 3
  reviews: 0
  threads: 0
audit:
  result: PASS_BOUNDED
  material_findings_open: 0
e2e:
  result: NOT_APPLICABLE
  reason: static exact-file/disassembly evidence only
next_action: resolve RawDataProcessor this+0x8/+0x10 member dynamic type and exact 0xb3ec30 transform semantics for encryption
---

# P2 outbound sequence — archived

Coordinator decision: `ACCEPT_WITH_EDITS`. The outbound field serialized at `f50107` is a direct per-`TGameserverDualConnection` 32-bit post-increment sequence counter for the exact qualifying message mode; nonmatching messages receive zero. Initialization/reset policy remains unproven and is not required for the accepted sequence-mechanism claim.
