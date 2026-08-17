---
task_id: OTC-20260817-track-a-p2-4dd250-qiodevice-provenance
status: ready
agent: ChatGPT
session_role: draft_researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: validate
branch: research/OTC-20260817-track-a-p2-4dd250-qiodevice-provenance
base_branch: main
base_main: 5068b220aef571805a72c4d8f9293dcaa43ee90c
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-p2-4dd250-qiodevice-provenance.md
  - docs/agents/evidence/OTC-20260817-track-a-p2-4dd250-qiodevice-provenance/**
modules_touched: []
depends_on:
  - PR #489 merged as 5068b220aef571805a72c4d8f9293dcaa43ee90c
  - PR #308 accepted exact-SHA QDataStream/QIODevice structural evidence
  - PR #299 merged canonical TCPConnection/QTcpSocket member evidence
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
research_output: DRAFT_NOT_PROMOTED_READY_FOR_COORDINATOR_REVIEW_AFTER_FINAL_CI
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
research_result:
  current_writer_exact_dynamic_type: FACT:TIODeviceWriter
  current_writer_vtable_ap: FACT:0x2f69d48
  current_writer_qiodevice_shared_pair: FACT:TGameserverTCPConnection_this_plus_0x10_plus_0x18
  current_writer_qiodevice_concrete_type: FACT:QTcpSocket
  current_writer_qiodevice_owner: FACT:TGameserverTCPConnection
  current_writer_qdatastream_member: FACT:TIODeviceWriter_plus_0x18
  target_0x4dd250_identity: FACT:QDataStream_writeRawData_char_const_ptr_qint64
  canonical_payload_pointer_to_0x4dd250: FACT
  canonical_payload_length_to_0x4dd250: FACT
  qdatastream_bound_device: FACT:QTcpSocket
  qt_qtcpsocket_bound_binary_serialization_boundary: PROVEN
  final_binary_egress_at_qt_qtcpsocket_boundary: PROVEN
  final_socket_owner: FACT:TGameserverTCPConnection
  final_os_socket_syscall: UNKNOWN
  framing: UNKNOWN
  sequence: UNKNOWN
  compression: UNKNOWN
  encryption: UNKNOWN
accepted_crosschecks:
  pr308_artifact: 9251725866
  pr308_digest: sha256:f669df2ace3db0e269f60287d82c51b69eff11eaf7c7f5b932e049492632bd1e
  pr299_merge: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
generations:
  - run: 32038672531
    source_job: 95413976848
    hosted_job: 95414062445
    result: SUCCESS
    direct_calls_to_b4aea0: [0x1970285, 0x1970608]
  - run: 32038917855
    source_job: 95414621259
    hosted_job: 95414649302
    result: SUCCESS
    bundle_digest: sha256:3fa3b3118c0a988000de6c77fc9c52514f9670f9f3d7b52f2d07f63ba53071b7
    tcp_vtable_ap: 0x3084b38
    tcp_rtti: 0x3080630
  - run: 32039061786
    source_job: 95415015967
    hosted_job: 95415041166
    result: SUCCESS
    bridge_window: 0xb4ae90..0xb4b290
    bridge_digest: sha256:4bc45e68bc7c1530579860dfb7769d48e162a82f80fad17a098d2a695760f596
cleanup:
  one_shot_workflow_removed: true
validation:
  exact_source_fences: PASS
  hosted_primary_decode: PASS
  pr308_crosscheck: PASS
  pr299_crosscheck: PASS
  no_world_map_evidence: true
  no_runtime_access: true
  raw_client_uploaded: false
  final_exact_head_governance: PENDING
  final_exact_head_ci: PENDING
  review_hygiene: PENDING
next_action: verify final exact-head governance/CI/review hygiene, then coordinator independently promote the proven Qt QTcpSocket-bound binary boundary and archive this task; do not start another research task in this invocation
---

# Track A P2 — `0x4dd250` / QIODevice provenance

## Terminal researcher result

The canonical binary gameplay payload is now statically bound to a concrete `QTcpSocket` through exact object/member provenance.

Exact chain:

```text
canonical same message
 -> 0xf50090 field decomposition
 -> raw payload pointer/length
 -> current TIODeviceWriter
 -> QDataStream at writer+0x18
 -> QDataStream::writeRawData@0x4dd250
 -> QDataStream constructed on TGameserverTCPConnection::QTcpSocket*
```

The decisive ownership edge is instruction-proven:

```text
b4b1ee  source object = TGameserverTCPConnection
b4b1f2  source+0x10 = QTcpSocket pointer
b4b1f6  source+0x18 = shared control
b4b230..b4b26f rebuild that exact shared pair
b4b273  pair passed to TIODeviceWriter helper 0x1960340
```

Merged #299 independently proves `TGameserverTCPConnection this+0x10` is the concrete `QTcpSocket` constructed in both exact constructor paths. Accepted #308 independently proves helper `0x1960340` constructs `TIODeviceWriter`, stores the supplied QIODevice pair, constructs `QDataStream(QIODevice*)`, and resolves `0x4dd250` as `QDataStream::writeRawData(char const*, qint64)`.

Therefore the final binary path is **PROVEN at the Qt QTcpSocket abstraction boundary**, and final socket ownership is `TGameserverTCPConnection`.

What remains explicitly unproven:

```text
FINAL_OS_SOCKET_SYSCALL=UNKNOWN
FRAMING=UNKNOWN
SEQUENCE=UNKNOWN
COMPRESSION=UNKNOWN
ENCRYPTION=UNKNOWN
```

Do not reinterpret `PROVEN at Qt QTcpSocket boundary` as proof of a specific Linux `send/write` syscall or kernel descriptor transition.

Durable evidence:
- `docs/agents/evidence/OTC-20260817-track-a-p2-4dd250-qiodevice-provenance/20260817-qtcpsocket-boundary.md`
- `docs/agents/evidence/OTC-20260817-track-a-p2-4dd250-qiodevice-provenance/result.json`

E2E: `NOT_APPLICABLE` — static exact-file/disassembly evidence only.
