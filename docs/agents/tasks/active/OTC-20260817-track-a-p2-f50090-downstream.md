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
  writer_guard_slot: FACT:+0x58
  writer_guard_exact_target: FACT:0xcb2960
  raw_payload_pointer: FACT:value_from_message_plus_0x10
  raw_payload_length: FACT:value_from_message_plus_0x18
  underlying_receiver: FACT:writer_plus_0x18_on_direct_guarded_branch
  raw_payload_target: FACT:0x4dd250
  cb2960_payload_pointer: FACT:subobject_plus_0x08
  cb2960_payload_length: FACT:subobject_plus_0x10
  cb2960_underlying_receiver: FACT:wrapper_plus_0x18
  cb2960_target: FACT:0x4dd250
  constructor_installed_vptr: FACT:0x2f69d48_in_constructor_0x1960340
  constructor_nested_object_member: FACT:this_plus_0x18_in_constructor_0x1960340
  constructor_owner_control_member: FACT:this_plus_0x20_in_constructor_0x1960340
  f50090_forwards_original_message_pointer_as_whole: DISPROVEN
  writer_exact_dynamic_type: UNKNOWN
  underlying_receiver_exact_dynamic_type: UNKNOWN
  semantic_role_of_0x4dd250: UNKNOWN
  final_binary_egress: UNKNOWN
  final_socket_ownership: UNKNOWN
  framing: UNKNOWN
  sequence: UNKNOWN
  compression: UNKNOWN
  encryption: UNKNOWN
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
  no_world_map_evidence: true
  no_runtime_access: true
  raw_client_uploaded: false
  final_exact_head_governance: PENDING
  final_exact_head_ci: PENDING
  review_hygiene: PENDING
anti_stall:
  invocation_started_at: 2026-08-17T15:50:00+02:00
  last_progress_at: 2026-08-17T16:04:00+02:00
  ci_checks_for_current_head: 0
  ci_check_generation: draft
  terminal_ci_wait_started_at: null
  terminal_ci_checks_for_current_generation: 0
  unchanged_state_checks: 0
  identical_failure_retries: 1
  repair_cycles_for_current_gate: 1
  context_reconstruction_attempts: 1
  stall_warnings: 0
next_action: verify final exact-head governance/CI/review hygiene, then coordinator independently review and promote the accepted bounded result; do not start another research frontier in this invocation
---

# Track A P2 — `0xf50090` downstream discriminator

## Terminal researcher result

The coordinator-promoted same message enters `0xf50090` in SysV `rsi`. Exact dataflow saves that pointer in `rbp`, decomposes the message into fields, and on the directly guarded writer path proves:

```text
canonical same message
 -> 0xf50090
 -> writer vslot +0x58 guard == 0xcb2960
 -> payload pointer from message+0x10
 -> payload length from message+0x18
 -> underlying receiver at writer+0x18
 -> exact target 0x4dd250
```

Generation 3 independently decodes `0xcb2960`, which repeats the same structural contract by extracting `subobject+0x08` as data pointer, `subobject+0x10` as length and forwarding through wrapper `this+0x18` to `0x4dd250`.

Constructor-like function `0x1960340` independently installs vptr `0x2f69d48` and binds a nested object at `this+0x18`, but this task does not overpromote that structural constructor into the exact current dynamic type without separate RTTI/vtable provenance.

The exact dynamic types, semantic role of `0x4dd250`, final binary egress, final socket ownership, framing, sequence, compression and encryption remain `UNKNOWN`.

Durable evidence:
- `docs/agents/evidence/OTC-20260817-track-a-p2-f50090-downstream/20260817-f50090-downstream-dataflow.md`
- `docs/agents/evidence/OTC-20260817-track-a-p2-f50090-downstream/result.json`

E2E: `NOT_APPLICABLE` — static exact-file/disassembly evidence only.
