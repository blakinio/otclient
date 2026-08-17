---
task_id: OTC-20260817-track-a-p2-sequence-provenance
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: investigate
branch: research/OTC-20260817-track-a-p2-sequence-provenance
base_branch: main
base_main: 0aed48da9a51730c590d0ffe4688f149b359a170
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-p2-sequence-provenance.md
  - docs/agents/evidence/OTC-20260817-track-a-p2-sequence-provenance/**
  - .github/workflows/tibia-official-client-re-p2-sequence-provenance.yml
modules_touched: []
reuses:
  - PR #494 canonical framing promotion
  - PR #492 canonical QTcpSocket-bound binary boundary
  - run 32005141186 accepted same-message processor chain
  - run 32037533068 exact f50090 framing bytes
depends_on:
  - main@0aed48da9a51730c590d0ffe4688f149b359a170
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
  sequence: UNKNOWN
  sequence_candidate_field: FACT:DWORD_message_plus_0_written_before_raw_payload_at_f50107
  clientprocessor_initial_message_qword_0: FACT:0x0000000100000000_at_c2dff2
  rawdataprocessor_modifies_message_plus_0: NOT_OBSERVED_IN_ACCEPTED_BOUNDED_BODY
  dualconnection_plus_0x80_runs_before_plus_0x78: PROVEN
hypothesis:
  h1: TGameserverDualConnection_plus_0x80_or_one_exact_nested_callee_updates_message_plus_0_before_plus_0x78_send_path
  h2: if_updated_value_is_connection_scoped_monotonic_then_sequence_semantics_may_be_PROVEN
next_action: exact-fence and stage only 0xb56d60..0xb57280 for hosted disassembly; trace every write/call carrying the same message and classify the message+0 producer edge without semantic guessing
---

# Track A P2 — sequence provenance

## Objective

Trace only the producer/update provenance of the canonical 32-bit `message+0` field serialized at `f50107` before the raw payload.

Canonical order before this task:

```text
ClientMessageProcessor
 -> RawDataProcessor
 -> DualConnection +0x80
 -> DualConnection +0x78
 -> NetworkPacketConnection/Processor
 -> 0xf50090
 -> scalar A framing field
 -> DWORD(message+0), semantics UNKNOWN
 -> raw payload
 -> QDataStream/QTcpSocket boundary
```

The exact ClientMessageProcessor initializes message qword `+0` to `0x0000000100000000`, so low DWORD `message+0` begins as zero. The accepted RawDataProcessor body operates on the QByteArray beginning at `message+0x8` and does not by itself prove a low-DWORD update. Therefore the first bounded discriminator is the already-proven intervening `DualConnection +0x80` call.

## Acceptance

- [ ] source-side work is exact-fenced byte copying only; semantic decode is GitHub-hosted;
- [ ] trace the same `rsi=message` argument through the exact `+0x80@0xb56d60` body;
- [ ] identify every direct write to message `+0` or exact nested call receiving the same message;
- [ ] if a concrete producer is found, prove value provenance and update rule;
- [ ] call it `sequence` only if connection-scoped monotonic/update semantics are directly evidenced;
- [ ] otherwise retain `SEQUENCE=UNKNOWN` and leave one smaller concrete callee/frontier;
- [ ] do not alter `FRAMING=PROVEN`, QTcpSocket egress, compression or encryption classifications without direct new evidence;
- [ ] no runtime/login/world-map/full executable upload/owner-funded AI.
