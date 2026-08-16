---
task_id: OTC-20260816-track-a-p2-hosted-evidence-replay
status: investigating
agent: ChatGPT
session_id: chatgpt-p2-replay-20260816-1424
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: validation
phase: investigate
branch: research/OTC-20260816-track-a-p2-hosted-evidence-replay
base_branch: main
base_main: c932236af63069e36c71f43e47b2435532171180
risk: low
related_pr: 368
updated: 2026-08-16T14:48:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-p2-hosted-evidence-replay.md
  - docs/agents/evidence/OTC-20260816-track-a-p2-hosted-evidence-replay/**
  - .github/workflows/tibia-official-client-re-p2-hosted-evidence-replay.yml
  - .github/scripts/tibia-official-client-re-p2-hosted-evidence-replay.py
modules_touched: []
reuses:
  - PR #310 historical P2 evidence only
  - run 31944051248 / job 95157306712 / artifact 9262800114
  - run 31904696996 / artifact 9252025461
  - artifact 9229609330 exact setup/construction provenance
  - artifact 9228087310 transport RTTI/vtables
  - artifact 9228207514 stream owner pairs
  - artifact 9228275973 outbound owner vtables
  - artifact 9226966960 direct QIODevice::write(QByteArray) census
  - artifact 9229441999 remaining write sinks
  - artifact 9231716774 TCP/network-packet connection RTTI/vtables
depends_on:
  - historical exact-client evidence fenced to 15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: deterministic replay/correlation of sanitized historical exact-build evidence requires no official-client binary, self-hosted runner or runtime state
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: milestone_and_terminal
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
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
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_research_only
provenance_boundary:
  source_run_31944051248: historical_exact_binary_evidence_quarantined_for_execution_routing
  source_artifact_zip_sha256: 30bd87d94088019b42fcf8504dfb6082af53b447547c544fec816e35b86407f3
  current_hosted_replay_may_upgrade_exact_binary_provenance: false
  client_binary_in_fixture: false
hosted_replay:
  first_green_run: 31947198080
  execution_class: github_hosted
  runtime_access: none
  exact_binary_reexecution: false
  result: PROVEN_CONSISTENCY_ONLY
historical_exact_chain:
  persistent_qbuffer_direct_readall: PROVEN
  first_downstream_consumer: PROVEN:TProtocolClientMessageProcessor+0x10@0xc2df80
  first_downstream_transform: PROVEN:TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
  same_message_handoff_to_dualconnection: PROVEN
  protocol_stage_order: PROVEN_PARTIAL
current_classification:
  framing: PROVEN_PARTIAL
  sequence: UNKNOWN
  compression: UNKNOWN
  encryption: UNKNOWN
  direct_qiodevice_qbytearray_final_egress: DISPROVEN
  final_binary_egress: UNKNOWN
framing_result:
  processor: TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
  prepend_one_byte: PROVEN
  modulo_8_padding_loop: PROVEN
  first_byte_post_loop_delta_store: PROVEN
  exact_header_semantic_name: UNKNOWN
  pad_byte_generator: 0x1832b90
  pad_byte_semantics: UNKNOWN
raw_processor_retained_pair:
  actual_this_plus_8_10_source: '[outer+0xa20] object +0xc0/+0xc8 shared pair'
  source_guard: 'outer+0xa20 virtual +0x20 == 0xe0d890 fast path'
  concrete_dynamic_type: UNKNOWN
  prior_unencrypted_stream_mapping: CORRECTED_FALSE
  actual_this_plus_18_20: shared::TCompressionHelper / shared::TZlibInflateWrapper retained pair
direct_write_census:
  symbol: QIODevice::write(QByteArray const&)
  callsites_total: 5
  final_binary_gameplay_sinks: 0
  disposition:
    0x7dd563: internal TUnencryptedRawMessageStream/QBuffer reverse-path write
    0xb4066b: internal TUnencryptedRawMessageStream self-write
    0xb46c75: TGameserverTCPConnection text line write; not binary gameplay
    0xc4a848: QNetworkReply to QFileDevice download path
    0xd08642: QFile path
  result: ALL_DIRECT_QBYTEARRAY_WRITES_DISPROVEN_AS_FINAL_BINARY_GAMEPLAY_EGRESS
transport_types:
  TUnencryptedRawMessageStream: AP 0x3084c58 / RTTI 0x3080660 / QBuffer-derived
  TGameserverNetworkPacketSequenceFlowProcessor: AP 0x3084d68 / RTTI 0x3080678 / temporal position UNKNOWN
  TGameserverTCPConnection: AP 0x3084b38 / RTTI 0x3080630
  TGameserverNetworkPacketConnection: AP 0x3084ba8 / RTTI 0x3080648
reverse_path:
  raw_processor_virtual_plus_0x18: 0xb46cd0
  inverse_optional_dispatch: retained this+0x8 object virtual +0x30
  structural_unframing: first-byte consume plus QByteArray mid slicing
  forward_inverse_pair: HIGH_CONFIDENCE_INFERENCE_ONLY
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
e2e:
  result: NOT_APPLICABLE
  reason: static evidence replay/correlation only; no live client behavior or physical runtime authorized
active_operation: trace final binary egress below DualConnection through TGameserverNetworkPacketConnection/TGameserverTCPConnection indirect or virtual transport methods and identify outer+0xa20 retained transform source by exact vtable signature
last_completed_step: exhausted all five direct QIODevice::write(QByteArray const&) callsites and disproved every one as final binary gameplay egress while preserving final_binary_egress UNKNOWN
next_action: correlate TGameserverNetworkPacketConnection/TCPConnection vtable methods with DualConnection post-raw calls; search non-QByteArray direct mechanisms (other overload, virtual writeData, QAbstractSocket/QTcpSocket virtual path or lower-level socket API), and identify the outer+0xa20 object whose virtual +0x20 equals 0xe0d890
---

# P2 hosted evidence replay and egress narrowing

This lane validates and correlates only sanitized historical exact-build evidence on GitHub-hosted execution. It does not execute or download the official client and does not upgrade the historical self-hosted exact-binary run into current hosted exact-binary provenance.

The post-serialization chain is now stable enough for bounded downstream analysis. `TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130` performs a proven partial framing operation: it prepends one byte, appends bytes until an 8-byte alignment condition clears, and stores a post-loop size/state delta in the first byte. Exact protocol meaning of that byte and the padding-byte generator remain unresolved.

A complete census of direct `QIODevice::write(QByteArray const&)` callsites found five sites and excluded all five as final binary gameplay egress. The final sink must therefore be sought through another overload, an indirect/virtual write path, or another lower-level transport API. No socket-egress claim may be made until concrete payload provenance and owning transport object are both proven.
