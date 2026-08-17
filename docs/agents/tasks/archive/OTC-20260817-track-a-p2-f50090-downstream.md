---
task_id: OTC-20260817-track-a-p2-f50090-downstream
status: completed
agent: ChatGPT
session_role: promotion_integration_coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: archived
base_branch: main
source_pr: 488
source_head: ebda1b1c01a801e749d3ec2ed5973705e8140969
source_final_state: closed_unmerged_after_promotion
previous_promotion_pr: 489
final_disposition: ACCEPT_WITH_EDITS_FINAL_SOURCE_HEAD_REPAIR
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
  f50090_second_argument: FACT:canonical_same_message
  f50090_decomposes_message_into_fields: FACT
  f50090_forwards_original_message_pointer_as_whole: DISPROVEN
  f50090_writer_member: FACT:this_plus_0x08
  f50090_writer_type: FACT:TIODeviceWriter
  f50090_writer_vtable_ap: FACT:0x2f69d48
  f50090_writer_rtti: FACT:0x3080718
  f50090_writer_qiodevice_pair: FACT:plus_0x08_plus_0x10
  f50090_writer_qdatastream_pair: FACT:plus_0x18_plus_0x20
  f50090_writer_qdatastream_object: FACT:plus_0x18
  writer_slot_0x58_guard_target: FACT:0xcb2960
  raw_payload_pointer: FACT:canonical_message_plus_0x10_value
  raw_payload_length: FACT:canonical_message_plus_0x18_value
  raw_payload_receiver: FACT:TIODeviceWriter_plus_0x18_QDataStream
  raw_payload_target: FACT:QDataStream_writeRawData_at_0x4dd250
  representation_boundary: FACT:STRUCTURED_MESSAGE_FIELDS_TO_TIODEVICEWRITER_QDATASTREAM
  f50090_direct_socket_sink: DISPROVEN
  f50090_is_proven_final_binary_egress: DISPROVEN
unknown:
  - current_tiodevice_concrete_type
  - final_binary_egress
  - final_socket_ownership
  - framing
  - sequence
  - compression
  - encryption
validation:
  generation_2_run: 32037248323
  generation_2_source_job: 95410048084
  generation_2_hosted_job: 95410072413
  generation_3_run: 32037533068
  generation_3_source_job: 95410828633
  generation_3_hosted_job: 95410901806
  final_source_head_governance_run: 32038034263
  final_source_head_governance_result: SUCCESS
  final_source_head_ci_run: 32038034467
  final_source_head_required_job: 95412354038
  final_source_head_required_result: SUCCESS
  source_changed_files: 3
  review_threads: 0
  one_shot_surfaces_removed: true
independent_support:
  canonical_type_report: docs/agents/evidence/OTC-20260813-official-client-re/20260814-final-write-reconciliation-generation-5.md
  pr308_artifact: 9251725866
  pr308_artifact_digest: sha256:f669df2ace3db0e269f60287d82c51b69eff11eaf7c7f5b932e049492632bd1e
  pr308_artifact_redownload_rehash: PASS
  qdatastream_write_raw_data: QDataStream::writeRawData(char_const_ptr,qint64)@0x4dd250
  constructor_artifact: 9290498273
  constructor_artifact_digest: sha256:4aa991a9912c3fb56cc08863ba94ac9e73e78a466a966c00353e85ce39a85323
  constructor_artifact_redownload_rehash: PASS
audit:
  result: PASS_BOUNDED
  material_findings_open: 0
e2e:
  result: NOT_APPLICABLE
  reason: static exact-file/disassembly evidence only
next_action: later invocation may resolve the concrete QIODevice shared-pair provenance supplied at b4b273 -> 0x1960340 and its first post-serialization consumer; do not infer final socket/framing/compression/encryption until proven
---

# P2 `0xf50090` downstream — archived final source-head reconciliation

Coordinator final disposition: `ACCEPT_WITH_EDITS` on source head `ebda1b1c01a801e749d3ec2ed5973705e8140969`.

The canonical same message reaches `0xf50090`, where it is decomposed into structured fields and serialized through an exact `TIODeviceWriter` whose QDataStream object is retained at `+0x18`. The raw payload path is concretely:

```text
message+0x10 data pointer
 + message+0x18 length
 -> TIODeviceWriter slot +0x58 / wrapper 0xcb2960
 -> TIODeviceWriter+0x18 QDataStream
 -> QDataStream::writeRawData(char const*, qint64) @ 0x4dd250
```

This positively classifies `0xf50090` as a serialization/QDataStream representation stage and disproves it as a direct socket sink or as a proven terminal binary-egress function. The concrete QIODevice bound to this writer, final binary egress/socket ownership, framing, sequence, compression and encryption remain unknown.
