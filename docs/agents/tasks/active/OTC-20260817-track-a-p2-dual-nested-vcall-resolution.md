---
task_id: OTC-20260817-track-a-p2-dual-nested-vcall-resolution
status: ready
agent: ChatGPT
session_role: draft_researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: validate
branch: research/OTC-20260817-track-a-p2-dual-nested-vcall-resolution
base_branch: main
base_main: 2ba207cef6d53dc847542b33ec94e7b53fd35b1f
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-p2-dual-nested-vcall-resolution.md
  - docs/agents/evidence/OTC-20260817-track-a-p2-dual-nested-vcall-resolution/**
modules_touched: []
depends_on:
  - PR #481 merged as 2ba207cef6d53dc847542b33ec94e7b53fd35b1f
  - PR #450 merged canonical P2 chain
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: bounded exact-client static discriminator reusing an independently rehashed exact-fenced predecessor artifact; no live runtime required
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: checkpoint_only
user_communication: low_noise
decomposition_decision: single
validation_level: focused
execution_class: github_hosted
source_staging_class: none_new_reused_exact_fenced_sanitized_artifact
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
input_artifact:
  source_run: 32016842999
  hosted_job: 95348295109
  artifact: 9283858910
  artifact_sha256: 2df8405269431397f3da0601ef24d9a9a8787dc33f3b5fdd43774f1eca36922c
  independent_redownload_rehash: PASS
accepted_input:
  canonical_chain: persistent_QBuffer_to_TProtocolClientMessageProcessor_to_TGameserverNetworkPacketRawDataProcessor_to_same_message_to_TGameserverDualConnection_plus_0x80_plus_0x78
  nested_vcall_1: 0xb56c93
  nested_vcall_2: 0xb57042
  b40630_reachability: UNKNOWN
  final_binary_egress: UNKNOWN
research_result:
  b56c93_receiver_provenance: FACT:nested_pointer_chain_current_entry_plus_0x20_plus_0x20
  b56c93_outer_guard_vslot_plus_0x98_target: FACT:0xb3eda0
  b56c93_intermediate_guard_vslot_plus_0x60_target: FACT:0xf45cf0
  b56c93_receiver_exact_dynamic_type: UNKNOWN
  b56c93_virtual_slot: FACT:+0x10
  b56c93_concrete_target: UNKNOWN
  b56c93_second_argument: FACT:original_b56970_second_argument_rsi
  b56c93_same_message_preserved: FACT
  b56c93_target_equals_b40630: UNKNOWN
  b57042_receiver_provenance: FACT:internal_rbx_object_selected_from_plus_0x80_path
  b57042_receiver_exact_dynamic_type: UNKNOWN
  b57042_virtual_slot: FACT:+0x10
  b57042_concrete_target: UNKNOWN
  b57042_rsi_on_taken_branch: FACT:0x100000001
  b57042_same_message_preserved: DISPROVEN
  b57042_is_same_message_edge_to_b40630: DISPROVEN
unknown:
  - b56c93_receiver_exact_dynamic_type
  - b56c93_concrete_target
  - b56c93_target_equals_b40630
  - b57042_receiver_exact_dynamic_type
  - b57042_concrete_target
  - framing
  - sequence
  - compression
  - encryption
  - final_binary_egress
  - final_socket_ownership
  - complete_transport_stage_order_beyond_promoted_chain
validation:
  exact_artifact_redownload_rehash: PASS
  exact_dataflow_b56c93: PASS
  exact_dataflow_b57042: PASS
  no_world_map_evidence: true
  no_vtable_adjacency_as_target_proof: true
  no_runtime_access: true
  new_staging_surfaces: 0
  final_exact_head_ci: PENDING
  final_exact_head_governance: PENDING
  review_threads_open: PENDING
next_action: coordinator independently review the exact artifact-backed dataflow, then if accepted resolve only the b56c93 nested receiver vtable +0x10 concrete target after the 0xb3eda0/0xf45cf0 guarded chain and test target == 0xb40630; do not broaden into generic network RE
---

# Track A P2 — DualConnection nested virtual-call resolution

## Objective and current result

This bounded task reduced the two still-untyped nested `+0x10` calls downstream of the canonical #450 same-message handoff.

Exact artifact-backed dataflow proves:

- `0xb56c93` receives the original `0xb56970` second argument, so the canonical same post-RawDataProcessor message is preserved to this unresolved nested vslot;
- the receiver is reached through the exact nested chain `current=[r12] -> +0x20 -> +0x20`, guarded by concrete virtual-target comparisons `+0x98 -> 0xb3eda0` and `+0x60 -> 0xf45cf0`;
- the receiver's exact dynamic type and its `+0x10` concrete target remain `UNKNOWN`, so `target == 0xb40630` remains `UNKNOWN`;
- `0xb57042` is not the same-message continuation: on the direct taken branch `rsi` remains `0x100000001`, so the same-message edge to `0xb40630` is `DISPROVEN` for that call.

No framing, sequence, compression, encryption, final egress or socket-ownership semantic is promoted.

## Acceptance inventory

- [x] exact sanitized predecessor artifact independently re-downloaded and re-hashed;
- [x] both nested callsite receiver/dataflow paths reconstructed from exact-fenced bytes;
- [x] `0xb56c93` same-message preservation classified `FACT`;
- [x] `0xb57042` same-message preservation classified `DISPROVEN`;
- [x] unresolved concrete vtable targets retained as `UNKNOWN` rather than guessed;
- [x] no world-map/map evidence used;
- [x] no runtime/login/gameplay/process-memory work;
- [x] no new one-shot staging workflow/script required;
- [ ] final exact-head governance/CI and review hygiene verified.

## Stop condition / handover

The two-call discriminator is complete to the strongest evidence available in the reused exact artifact. The only live same-message reachability candidate is now `0xb56c93`. The next smallest discriminator is to recover the exact receiver vtable/object-construction provenance for that call and resolve only its `+0x10` target, testing whether it is exactly `0xb40630`.
