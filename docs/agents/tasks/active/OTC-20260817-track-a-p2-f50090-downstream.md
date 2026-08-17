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
research_output: DRAFT_NOT_PROMOTED_READY_FOR_COORDINATOR_REVIEW
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
  next_aligned_function_entry: FACT:0xf501e0
  f50090_second_argument: FACT:canonical_same_message
  f50090_saved_message_pointer: FACT:rbp
  f50090_decomposes_message_into_fields: FACT
  target_0x4dc3d0: FACT:length_derived_scalar_from_message_plus_0x18
  target_0x4daaf0: FACT:scalar_from_message_plus_0x00
  raw_payload_target: FACT:0x4dd250
  raw_payload_rsi: FACT:value_from_message_plus_0x10
  raw_payload_rdx: FACT:value_from_message_plus_0x18
  raw_payload_receiver_provenance: FACT:f50090_this_plus_0x08_then_plus_0x18
  f50090_forwards_original_message_pointer_as_whole: DISPROVEN
  semantic_role_of_0x4dd250: UNKNOWN
  final_binary_egress: UNKNOWN
  final_socket_ownership: UNKNOWN
  framing: UNKNOWN
  sequence: UNKNOWN
  compression: UNKNOWN
  encryption: UNKNOWN
generation:
  producer_head: ea8113028a07ef84518f4a8b705bcecd97604376
  run: 32037248323
  source_job: 95410048084
  hosted_job: 95410072413
  code_window: 0xf50040..0xf50480
  code_length: 1088
  code_sha256: 1d14d72f683455daa3ab065bd48c3588f8755798ce63e70b838569353c3e2cea
  source_candidate_index: 1
  result: SUCCESS
cleanup:
  one_shot_workflow_removal: PENDING
  one_shot_script_removal: PENDING
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
  last_progress_at: 2026-08-17T15:58:00+02:00
  ci_checks_for_current_head: 0
  ci_check_generation: draft
  terminal_ci_wait_started_at: null
  terminal_ci_checks_for_current_generation: 0
  unchanged_state_checks: 0
  identical_failure_retries: 1
  repair_cycles_for_current_gate: 1
  context_reconstruction_attempts: 1
  stall_warnings: 0
next_action: remove the one-shot producer workflow/script, then verify final exact-head governance/CI/review hygiene and hand the Draft to coordinator promotion
---

# Track A P2 — `0xf50090` downstream discriminator

## Terminal researcher result

The coordinator-promoted same message enters `0xf50090` in SysV `rsi`; exact entry dataflow saves that pointer in `rbp` and then decomposes the message into fields rather than forwarding the whole object.

The strongest exact downstream payload edge is:

```text
canonical message
 -> 0xf50090
 -> message+0x10 value as rsi
 -> message+0x18 value as rdx
 -> nested receiver from this+0x08 then +0x18
 -> call 0x4dd250
```

Earlier concrete calls receive only message-derived scalar values: `0x4dc3d0` receives a length-derived scalar and `0x4daaf0` receives `message+0x00` as a scalar. No downstream call in the bounded function receives the original saved message pointer as a whole.

The exact semantic identity of `0x4dd250`, its receiver dynamic type, final binary egress, final socket ownership, framing, sequence, compression and encryption remain `UNKNOWN`. No semantic is inferred from calling convention alone.

Durable evidence:

- `docs/agents/evidence/OTC-20260817-track-a-p2-f50090-downstream/20260817-f50090-downstream-dataflow.md`
- `docs/agents/evidence/OTC-20260817-track-a-p2-f50090-downstream/result.json`

E2E: `NOT_APPLICABLE` — static exact-file/disassembly evidence only.
