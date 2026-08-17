---
task_id: OTC-20260817-track-a-p2-f50090-downstream
status: ready
agent: ChatGPT
session_role: draft_researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: validate
branch: research/OTC-20260817-track-a-p2-f50090-downstream
base_branch: main
base_main: 696db6ce34acd23a3d0081b9b1b94e1eabbe1cbe
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-p2-f50090-downstream.md
  - docs/agents/evidence/OTC-20260817-track-a-p2-f50090-downstream/**
modules_touched: []
depends_on:
  - PR #487 merged as 696db6ce34acd23a3d0081b9b1b94e1eabbe1cbe
  - PR #481 canonical P2 chain
blocks: []
policy_version: 2
prompting_standard_version: 2.1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_mode: github-only
execution_reason: bounded exact-client static dataflow discriminator; no live runtime required
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
decomposition_decision: single
validation_level: focused
execution_class: github_hosted
source_staging_class: coordinator_approved_exact_fenced_file_only_nonsemantic_bridge
source_staging_runner: synology-otclient-01
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
accepted_input:
  same_message_to_f50090: FACT
  target: 0xf50090
research_result:
  f50090_function_entry: FACT:0xf50090
  f50090_second_argument: FACT:canonical_same_message
  f50090_saved_message_pointer: FACT:rbp
  f50090_decomposes_message_into_fields: FACT
  f50090_forwards_original_message_pointer_as_whole: DISPROVEN
  writer_member: FACT:this_plus_0x08
  writer_type: FACT:TIODeviceWriter
  writer_vtable_ap: FACT:0x2f69d48
  writer_rtti: FACT:0x3080718
  writer_qiodevice_pair: FACT:plus_0x08_plus_0x10
  writer_qdatastream_pair: FACT:plus_0x18_plus_0x20
  writer_qdatastream_object: FACT:plus_0x18
  writer_slot_0x30_guard_target: FACT:0xcb2930
  writer_slot_0x38_guard_target: FACT:0xcb2940
  writer_slot_0x58_guard_target: FACT:0xcb2960
  raw_payload_pointer: FACT:value_from_message_plus_0x10
  raw_payload_length: FACT:value_from_message_plus_0x18
  raw_payload_receiver: FACT:TIODeviceWriter_plus_0x18_QDataStream
  raw_payload_target: FACT:QDataStream_writeRawData_at_0x4dd250
  representation_boundary: FACT:STRUCTURED_MESSAGE_FIELDS_TO_TIODEVICEWRITER_QDATASTREAM
  f50090_direct_socket_sink: DISPROVEN
  f50090_is_proven_final_binary_egress: DISPROVEN
  current_tiodevice_concrete_type: UNKNOWN
  final_binary_egress: UNKNOWN
  final_socket_ownership: UNKNOWN
  framing: UNKNOWN
  sequence: UNKNOWN
  compression: UNKNOWN
  encryption: UNKNOWN
accepted_predecessor_crosscheck:
  pr: 308
  artifact: 9251725866
  artifact_digest: sha256:f669df2ace3db0e269f60287d82c51b69eff11eaf7c7f5b932e049492632bd1e
  helper: 0x1960340
  tiodevicewriter_ap: 0x2f69d48
  tiodevicewriter_rtti: 0x3080718
  qdatastream_member: plus_0x18
  qdatastream_write_raw_data: 0x4dd250
generations:
  - producer_head: ea8113028a07ef84518f4a8b705bcecd97604376
    run: 32037248323
    source_job: 95410048084
    hosted_job: 95410072413
    main_window: 0xf50040..0xf50480
    main_sha256: 1d14d72f683455daa3ab065bd48c3588f8755798ce63e70b838569353c3e2cea
    result: SUCCESS
  - producer_head: 8642b419ca8ef3034ba747f689a14e24cf9a0152
    run: 32037533068
    source_job: 95410828633
    hosted_job: 95410901806
    main_window: 0xf50040..0xf50480
    main_sha256: 1d14d72f683455daa3ab065bd48c3588f8755798ce63e70b838569353c3e2cea
    ctor_window: 0x1960300..0x1960600
    ctor_sha256: bc03c482e3ae04c0f9a91288d5f79612b2f0f08680ef10ffecdf9a927ec0371f
    vcall_window: 0xcb2900..0xcb29c0
    vcall_sha256: dc04038b7740f39095ed6ab599bc10048c368fab9eff126c3d0853930c62af14
    result: SUCCESS
cleanup:
  one_shot_workflow_removed: true
  one_shot_script_removed: true
validation:
  exact_source_fence: PASS
  hosted_primary_decode: PASS
  accepted_pr308_crosscheck: PASS
  no_world_map_evidence: true
  no_runtime_access: true
  raw_client_uploaded: false
  final_exact_head_governance: PENDING
  final_exact_head_ci: PENDING
  review_hygiene: PENDING
anti_stall:
  invocation_started_at: 2026-08-17T15:50:00+02:00
  last_progress_at: 2026-08-17T16:08:00+02:00
  ci_checks_for_current_head: 0
  ci_check_generation: draft
  terminal_ci_wait_started_at: null
  terminal_ci_checks_for_current_generation: 0
  unchanged_state_checks: 0
  identical_failure_retries: 1
  repair_cycles_for_current_gate: 1
  context_reconstruction_attempts: 1
  stall_warnings: 0
next_action: verify final exact-head governance/CI/review hygiene, then coordinator independently review and promote the bounded TIODeviceWriter/QDataStream result; do not start another research frontier before this task is terminal
---

# Track A P2 — `0xf50090` downstream discriminator

## Terminal researcher result

The coordinator-promoted same message enters `0xf50090` in SysV `rsi`. Exact dataflow saves that pointer in `rbp`, decomposes it into structured fields and sends those fields through a constructor-bound `TIODeviceWriter`.

The writer identity is exact:

```text
f50090 this+0x08
 -> object initialized by helper 0x1960340
 -> TIODeviceWriter AP 0x2f69d48 / RTTI 0x3080718
 -> QDataStream object at TIODeviceWriter+0x18
```

The strongest raw-payload edge is:

```text
canonical same message
 -> 0xf50090
 -> payload pointer copied from message+0x10
 -> payload length copied from message+0x18
 -> TIODeviceWriter slot +0x58 / wrapper 0xcb2960
 -> TIODeviceWriter+0x18 QDataStream
 -> QDataStream::writeRawData(char const*, qint64) @ 0x4dd250
```

The scalar paths through slots `+0x30/+0x38` also forward to the same QDataStream object. The exact overload names of the two scalar PLT calls are not promoted in this task.

This positively classifies `0xf50090` as a structured-field/QDataStream serialization stage. It is not a direct socket sink and is not proven final binary egress. The exact concrete QIODevice bound to this particular writer, final egress/socket ownership, framing, sequence, compression and encryption remain `UNKNOWN`.

Durable evidence:
- `docs/agents/evidence/OTC-20260817-track-a-p2-f50090-downstream/20260817-f50090-downstream-dataflow.md`
- `docs/agents/evidence/OTC-20260817-track-a-p2-f50090-downstream/result.json`

Next smallest frontier after coordinator promotion: resolve the exact QIODevice shared-pair provenance supplied to the current TIODeviceWriter at `b4b273 -> 0x1960340`, then follow its first post-serialization consumer without generic Qt/socket census.

E2E: `NOT_APPLICABLE` — static exact-file/disassembly evidence only.
