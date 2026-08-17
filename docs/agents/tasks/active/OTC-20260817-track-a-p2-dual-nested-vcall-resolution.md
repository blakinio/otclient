---
task_id: OTC-20260817-track-a-p2-dual-nested-vcall-resolution
status: investigating
agent: ChatGPT
session_role: draft_researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: investigate
branch: research/OTC-20260817-track-a-p2-dual-nested-vcall-resolution
base_branch: main
base_main: 2ba207cef6d53dc847542b33ec94e7b53fd35b1f
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-p2-dual-nested-vcall-resolution.md
  - docs/agents/evidence/OTC-20260817-track-a-p2-dual-nested-vcall-resolution/**
  - .github/scripts/tibia-official-client-re-p2-dual-nested-vcall-resolution.py
  - .github/workflows/tibia-official-client-re-p2-dual-nested-vcall-resolution.yml
modules_touched: []
depends_on:
  - PR #481 merged as 2ba207cef6d53dc847542b33ec94e7b53fd35b1f
  - PR #450 merged canonical P2 chain
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: exact-fenced bounded static discriminator with file-only source staging and GitHub-hosted semantic analysis
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
research_output: IN_PROGRESS_NOT_PROMOTED
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
additional_evidence_required: true
next_action: run one exact-fenced bounded source generation that mechanically recovers candidate vtable/RTTI/address-point evidence and bounded constructor xref windows for the surviving 0xb56c93 receiver, then resolve its exact +0x10 target on GitHub-hosted infrastructure
---

# Track A P2 — DualConnection nested virtual-call resolution

## Objective

Resolve the remaining same-message reachability edge downstream of the canonical #450 chain. The task is not terminal while `0xb56c93` still has an unresolved concrete `+0x10` target and a safe bounded exact-client discriminator remains available.

## Reused exact-artifact result

Independent re-download/re-hash of accepted exact-fenced artifact `9283858910` proved:

- `0xb56c93` preserves the original `0xb56970` second SysV argument in `r14`, restores it to `rsi`, and calls receiver vslot `+0x10`; canonical #450 therefore makes same-message preservation to this call a FACT;
- the `0xb56c93` receiver is reached as `current=[r12] -> +0x20 -> +0x20`, with exact guard targets `outer vslot +0x98 -> 0xb3eda0` and `intermediate vslot +0x60 -> 0xf45cf0`;
- `0xb57042` is not a same-message continuation: its direct taken path has `rsi=0x100000001` at the call, so that candidate is DISPROVEN as the same-message edge to `0xb40630`.

The accepted #310 exact-SHA artifact was also checked and does not contain the surviving receiver vtable identity. Reusing only old artifacts cannot resolve the final edge.

## Bounded evidence generation

One temporary exact-fenced producer is authorized within this task. Source-side execution on the retained exact regular file may only perform deterministic file-byte mapping and structural indexing; it may not disassemble or semantically classify. It will stage only:

1. small exact code windows around the `0xb56c93` guarded chain and the relevant exact function targets `0xb3eda0`, `0xf45cf0`, `0xb40630` and `0xb57470`;
2. exact file-backed occurrences of those target pointers;
3. mechanically derived candidate vtable address-point windows from the callsite-tested slot offsets (`+0x98`, `+0x60`, `+0x10`, `+0x80`);
4. bounded RTTI/name bytes reached from those candidate tables;
5. bounded executable raw-byte windows around structural RIP-relative references to candidate address points, for hosted decoding only.

No raw ELF/package is uploaded. All instruction decoding, type interpretation, constructor/object-provenance reasoning and final semantic classification occur on GitHub-hosted Ubuntu. The one-shot workflow/script must be removed immediately after evidence consumption.

## Acceptance inventory

- [ ] exact client size/SHA fenced before new bytes are staged;
- [x] both nested callsite dataflows reconstructed from exact-fenced bytes;
- [x] `0xb56c93` same-message preservation = FACT;
- [x] `0xb57042` same-message preservation = DISPROVEN;
- [ ] surviving `0xb56c93` receiver vtable/object-construction provenance resolved to strongest exact evidence;
- [ ] `0xb56c93` concrete vslot `+0x10` target resolved, or retained UNKNOWN only after the new discriminator is exhausted;
- [ ] exact test `b56c93 target == 0xb40630`;
- [ ] final `DUALCONNECTION_TO_BINARY_EGRESS` classification updated without inventing a replacement sink;
- [ ] framing/sequence/compression/encryption/final-socket properties kept independently PROVEN/UNKNOWN as evidence warrants;
- [ ] temporary workflow/script removed after the single evidence generation;
- [ ] durable Markdown + JSON evidence persisted;
- [ ] final exact-head governance/CI and review hygiene green before coordinator promotion.

## Scope boundary

Do not infer targets from address proximity, vtable adjacency, class names alone or Qt semantics. Do not revisit world-map/map evidence. No runtime/login/gameplay/process-memory work is authorized. No owner-funded AI/API use is authorized.

## Stop condition

Stop only after the surviving `0xb56c93` exact target is resolved to the strongest evidence available from the bounded producer and the task has completed researcher validation/cleanup. If the bounded constructor/vtable evidence cannot bind the receiver, record the exact exhausted discriminator as `UNKNOWN` rather than broadening into generic network reverse engineering.
