---
task_id: OTC-20260817-track-a-p2-raw-transform-semantics
status: ready
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: review
branch: research/OTC-20260817-track-a-p2-raw-transform-semantics
base_branch: main
base_main: 8a5fcfd72f2554261eef91a2129c9cc076e730ea
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-p2-raw-transform-semantics.md
  - docs/agents/evidence/OTC-20260817-track-a-p2-raw-transform-semantics/**
modules_touched: []
reuses:
  - PR #496 canonical sequence promotion
  - PR #494 canonical framing promotion
  - docs/agents/evidence/OTC-20260815-track-a-p2-buffer-downstream-consumer/20260817-coordinator-accepted-downstream-chain.json
  - run 32046592885 concrete TXteaHelper transform and RTTI
  - run 32046849472 bounded backend trace
  - run 32059752436 outbound transform census
depends_on:
  - main@8a5fcfd72f2554261eef91a2129c9cc076e730ea
blocks: []
policy_version: 2
prompting_standard_version: 2.1
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
decomposition_decision: single
validation_level: focused
execution_class: github_hosted
source_staging_class: exact_fenced_file_only_nonsemantic
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
  integration_required: true
  e2e_required: false
  completion_claim: internal_only
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
accepted_input:
  framing: PROVEN
  sequence: PROVEN
  compression: UNKNOWN
  encryption: UNKNOWN
  persistent_qbuffer_to_clientprocessor: PROVEN
  same_message_downstream_to_qtcpsocket: PROVEN
result:
  framing: PROVEN
  sequence: PROVEN
  encryption: PROVEN
  encryption_receiver: FACT:shared::TXteaHelper
  encryption_vtable_ap: FACT:0x2f63148
  encryption_slot_plus_0x28: FACT:0xf861e0
  compression: DISPROVEN_ON_PROVEN_OUTBOUND_PATH
  compression_outside_proven_outbound_path: UNKNOWN
  final_binary_egress: PROVEN_AT_QT_QTCPSOCKET_BOUNDARY
  final_socket_owner: FACT:TGameserverTCPConnection
  linux_socket_syscall: UNKNOWN_OPTIONAL
promotion_status: DRAFT_READY_FOR_COORDINATOR_REVIEW
next_action: coordinator independently falsifies exact run evidence and final diff, then promotes only accepted encryption and scoped compression claims; Linux syscall is optional and not required for protocol reconstruction
---

# Track A P2 — RawDataProcessor transform semantics

## Objective

Resolve the last protocol-semantic byte-transform frontier before the already-proven framing/sequence/QTcpSocket boundary, while classifying encryption and compression independently.

## Researcher conclusion

```text
persistent QBuffer
 -> TProtocolClientMessageProcessor+0x10 @ 0xc2df80
 -> TGameserverNetworkPacketRawDataProcessor+0x10 @ 0xb47130
 -> prefix + padding
 -> conditional shared::TXteaHelper transform when message+0x28 == 2
 -> canonical same-message downstream chain
 -> framing / sequence
 -> QDataStream::writeRawData
 -> QTcpSocket
```

Classification:

```text
FRAMING=PROVEN
SEQUENCE=PROVEN
ENCRYPTION=PROVEN
COMPRESSION=DISPROVEN_ON_PROVEN_OUTBOUND_PATH
FINAL_BINARY_EGRESS=PROVEN_AT_QT_QTCPSOCKET_BOUNDARY
LINUX_SOCKET_SYSCALL=UNKNOWN_OPTIONAL
```

The compression result is strictly scoped to the canonical outbound path from the persistent QBuffer to QTcpSocket. It is not a claim about inbound traffic or unrelated client code.

## Exact evidence

### Concrete encryption receiver

Run `32046592885`:

- source job `95435821666`;
- hosted job `95435860761`;
- transform `0xf861e0..0xf864c0`, SHA-256 `f45afa6aaf3337850d4d892692d533140f896444e4a1342c83f73cb7053de3be`;
- vtable AP `0x2f63148`, typeinfo `0x3077800`;
- RTTI `N6shared11TXteaHelperE`;
- vslot `+0x20 = 0xf85eb0`;
- vslot `+0x28 = 0xf861e0`.

The encryption verdict uses concrete byte-container input/output dataflow plus exact receiver type. RTTI naming or 8-byte alignment alone is not used as proof. Exact XTEA round-core reconstruction remains outside the promoted claim.

### Compression falsification

Run `32059752436`:

- source job `95478101478`;
- hosted job `95478152304`;
- `0xc2df80..0xc2e500`, SHA-256 `00cea4d539c6f4ac8695ae908535b88af7af849f27f4f69578e20cc6f49557b9`;
- `0xb47130..0xb47440`, SHA-256 `d0cd15d635e9452788f628f0d61d26025665d859eb6315b1c188a97d6795f993`.

The client-processor body reads/copies persistent-QBuffer bytes into the message and selects mode metadata. The complete RawDataProcessor byte-changing sequence is prefix insertion, 8-byte padding, padding-count store, optional concrete TXteaHelper transform and assignment back to the same message. Canonical downstream evidence preserves that message through framing and QTcpSocket. No separate compression transform exists on this proven path.

## Acceptance

- [x] source runner only exact-fenced and copied bounded file-backed bytes;
- [x] semantic disassembly and classification were GitHub-hosted;
- [x] concrete RawDataProcessor conditional transform was resolved by exact vtable/RTTI and byte-container dataflow;
- [x] `0xf85eb0` is separated from the main transform and used by the padding path;
- [x] `ENCRYPTION=PROVEN` is supported by direct transform evidence rather than naming alone;
- [x] `COMPRESSION=DISPROVEN_ON_PROVEN_OUTBOUND_PATH` is independently bounded and scope-guarded;
- [x] canonical `FRAMING=PROVEN`, `SEQUENCE=PROVEN` and QTcpSocket boundary are preserved;
- [x] no runtime/login/world-map/process-memory/full executable upload/owner-funded AI;
- [x] researcher does not self-promote.

Durable evidence:

- `docs/agents/evidence/OTC-20260817-track-a-p2-raw-transform-semantics/result.json`
- `docs/agents/evidence/OTC-20260817-track-a-p2-raw-transform-semantics/20260817-outbound-transform-semantics.md`
