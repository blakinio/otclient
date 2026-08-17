---
task_id: OTC-20260817-track-a-p2-4dd250-qiodevice-provenance
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: investigate
branch: research/OTC-20260817-track-a-p2-4dd250-qiodevice-provenance
base_branch: main
base_main: 5068b220aef571805a72c4d8f9293dcaa43ee90c
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-p2-4dd250-qiodevice-provenance.md
  - docs/agents/evidence/OTC-20260817-track-a-p2-4dd250-qiodevice-provenance/**
  - .github/workflows/tibia-official-client-re-p2-4dd250-qiodevice-provenance.yml
modules_touched: []
depends_on:
  - PR #489 merged as 5068b220aef571805a72c4d8f9293dcaa43ee90c
  - PR #308 accepted exact-SHA QDataStream/QIODevice structural evidence
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: bounded exact-client static provenance discriminator; no live runtime required
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
decomposition_decision: single
validation_level: focused
execution_class: github_hosted
source_staging_class: exact_fenced_file_only_nonsemantic_if_additional_bytes_required
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
promotion_authority: coordinator_only
feature_scope:
  type: protocol
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: partial_producer
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
accepted_input:
  canonical_message_to_f50090: FACT
  f50090_decomposes_message: FACT
  raw_payload_pointer: FACT:canonical_message_plus_0x10_value
  raw_payload_length: FACT:canonical_message_plus_0x18_value
  writer_slot_0x58_target: FACT:0xcb2960
  underlying_receiver: FACT:writer_plus_0x18
  exact_target: FACT:0x4dd250
  semantic_role_of_0x4dd250: UNKNOWN
  writer_exact_dynamic_type: UNKNOWN
  underlying_receiver_exact_dynamic_type: UNKNOWN
  final_binary_egress: UNKNOWN
  final_socket_ownership: UNKNOWN
hypotheses:
  h1_4dd250_identity: accepted_exact_sha_PR308_may_resolve_0x4dd250_as_QDataStream_writeRawData
  h2_current_writer_identity: constructor_binding_plus_PR308_may_resolve_current_writer_as_TIODeviceWriter
  h3_bound_qiodevice: current_writer_input_pair_may_resolve_to_TGameserverTCPConnection_QTcpSocket_or_another_QIODevice
next_action: independently bind the current f50090 writer to constructor 0x1960340, resolve exact identity of 0x4dd250, then trace the QIODevice shared pair passed at b4b273 back through TGameserverNetworkPacketConnection construction; prove or disprove QTcpSocket ownership without generic Qt census
---

# Track A P2 — `0x4dd250` / QIODevice provenance

## Objective

Continue the canonical #489 path only:

```text
same message
 -> 0xf50090 field decomposition
 -> writer +0x58 / wrapper 0xcb2960
 -> payload pointer/length preserved
 -> writer+0x18
 -> 0x4dd250
```

Resolve three bounded questions:

1. exact semantic identity of `0x4dd250` from exact-SHA accepted evidence;
2. exact type of the current writer object used by `0xf50090`;
3. exact concrete QIODevice provenance supplied to that writer, specifically testing whether it is the already-known `TGameserverTCPConnection` / `QTcpSocket` path or a different QIODevice.

## Acceptance inventory

- [ ] no researcher summary treated as proof; primary exact bytes/artifacts independently checked;
- [ ] current `f50090 this+0x08` writer bound to its exact construction site or retained UNKNOWN;
- [ ] `0x4dd250` exact identity classified FACT/UNKNOWN from exact-SHA evidence;
- [ ] helper `0x1960340` writer type and QIODevice/QDataStream member contract classified FACT/UNKNOWN;
- [ ] current QIODevice input pair traced to an exact object/member provenance;
- [ ] QTcpSocket hypothesis classified PROVEN/DISPROVEN/UNKNOWN without class-name or adjacency inference;
- [ ] if a concrete socket path is proven, distinguish QDataStream serialization call from final OS/network egress;
- [ ] framing/sequence/compression/encryption remain UNKNOWN unless direct evidence proves them;
- [ ] no world-map, runtime/login/process-memory or owner-funded AI;
- [ ] temporary source-staging workflow removed after evidence capture;
- [ ] final Draft exact-head governance/CI/review hygiene green before coordinator review.

## Stop condition

Stop after the concrete QIODevice provenance and the role of `0x4dd250` are classified to the strongest exact evidence available. Do not broaden into a generic Qt/socket census or unrelated protocol semantics.
