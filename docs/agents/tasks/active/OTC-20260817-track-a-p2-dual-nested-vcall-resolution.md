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
  - .github/scripts/tibia-official-client-re-p2-dual-nested-vcall-bridge.py
  - .github/workflows/tibia-official-client-re-p2-dual-nested-vcall-bridge.yml
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
accepted_input:
  canonical_chain: persistent_QBuffer_to_TProtocolClientMessageProcessor_to_TGameserverNetworkPacketRawDataProcessor_to_same_message_to_TGameserverDualConnection_plus_0x80_plus_0x78
  nested_vcall_1: 0xb56c93
  nested_vcall_2: 0xb57042
  b40630_reachability: UNKNOWN
  final_binary_egress: UNKNOWN
research_result:
  b56c93_receiver_provenance: FACT:nested_pointer_chain_current_entry_plus_0x20_plus_0x20
  b56c93_outer_guard_vslot_plus_0x98_target: FACT:0xb3eda0
  b56c93_outer_guard_type: FACT:tibia::network::TGameserverNetworkPacketConnection
  b56c93_outer_guard_vtable_ap: FACT:0x3084ba8
  b56c93_intermediate_guard_vslot_plus_0x60_target: FACT:0xf45cf0
  b56c93_intermediate_type: FACT:tibia::network::TGameserverNetworkPacketProcessor
  b56c93_intermediate_vtable_ap: FACT:0x30b7a68
  b56c93_intermediate_plus0x20_source: FACT:constructor_stack_local_rbp_minus_0xc0
  b56c93_receiver_exact_dynamic_type: UNKNOWN
  b56c93_virtual_slot: FACT:+0x10
  b56c93_concrete_target: UNKNOWN
  b56c93_second_argument: FACT:original_b56970_second_argument_rsi
  b56c93_same_message_preserved: FACT
  b56c93_target_equals_b40630: UNKNOWN
  b57042_same_message_preserved: DISPROVEN
  b57042_is_same_message_edge_to_b40630: DISPROVEN
generation_1:
  run: 32033753449
  source_job: 95399308395
  hosted_job: 95400245919
  source_artifact: 9289952632
  source_artifact_digest: sha256:176a174bafd8f77fb82ff8ea3737b0850be5b0327dc2ba6065e0d9bf51574e5a
  final_artifact: 9289961937
  final_artifact_digest: sha256:fa1cddd5410454d9f5b717afe0d625d404a7750fb82ffb4b8a9d288cbc9ac64a
  result: SUCCESS
additional_evidence_required: true
next_action: stage only exact file bytes 0xb4aea0..0xb4b800 and decode hosted to resolve the source and concrete vtable of constructor local [rbp-0xc0], which is the final b56c93 receiver
---

# Track A P2 — DualConnection nested virtual-call resolution

## Objective

Resolve the remaining exact same-message reachability edge after the canonical #450 handoff. The surviving call is `0xb56c93`; `0xb57042` is already disproven as a same-message continuation.

## Generation 1 result

Run `32033753449` fenced the exact client and completed source job `95399308395` plus hosted job `95400245919`, both `SUCCESS`. Source artifact `9289952632` and final artifact `9289961937` were independently re-hashed to the GitHub-recorded digests.

Hosted decoding recovered valid Itanium-style vtable/RTTI identities rather than relying on address adjacency:

- outer guard address point `0x3084ba8`, RTTI `tibia::network::TGameserverNetworkPacketConnection`; its slot `+0x98 = 0xb3eda0`;
- intermediate address point `0x30b7a68`, RTTI `tibia::network::TGameserverNetworkPacketProcessor`; its slot `+0x60 = 0xf45cf0`.

The exact forwarding methods are:

```text
0xb3eda0: this+0x20 -> check processor +0x60 == 0xf45cf0 -> this+0x20 -> call receiver +0x10
0xf45cf0: this+0x20 -> jmp receiver +0x10
```

Constructor evidence around `0xb4aea0` installs the outer vptr, allocates/constructs the processor object at `r15+0x10`, installs `0x30b7a68`, stores that processor object into outer `+0x20`, and writes:

```text
[r15+0x30] = [rbp-0xc0]
```

Because the processor object begins at `r15+0x10`, `r15+0x30` is exactly processor `this+0x20`, i.e. exactly the final receiver dereferenced by `0xf45cf0` / `0xb56c93`.

The first generated xref windows do not cover the assignment that produced `[rbp-0xc0]`. Therefore the only remaining object-provenance gap is one stack local in one constructor.

## Generation 2 bound

The follow-up generation is limited to the single file-backed executable window `0xb4aea0..0xb4b800`. Source-side operation is exact-fenced byte copying only; source-side disassembly/semantics remain forbidden. Hosted Ubuntu alone disassembles the window. No raw executable/package, client process, process memory, runtime, login or gameplay is involved.

## Acceptance inventory

- [x] exact client size/SHA fenced for generation 1;
- [x] both nested callsite dataflows reconstructed;
- [x] `0xb56c93` same-message preservation = FACT;
- [x] `0xb57042` same-message preservation = DISPROVEN;
- [x] outer receiver type/vtable = `TGameserverNetworkPacketConnection` / `0x3084ba8`;
- [x] intermediate type/vtable = `TGameserverNetworkPacketProcessor` / `0x30b7a68`;
- [x] final receiver source reduced to constructor local `[rbp-0xc0]`;
- [ ] resolve `[rbp-0xc0]` source and receiver vtable;
- [ ] resolve `0xb56c93` concrete `+0x10` target;
- [ ] exact test `target == 0xb40630`;
- [ ] final reachability/layer classifications persisted without semantic overpromotion;
- [ ] temporary producer surfaces removed;
- [ ] final Draft governance/CI and review hygiene green before coordinator promotion.

## Scope boundary

No world-map evidence. No target inference from adjacency/class names alone. No runtime/login/process-memory work. No owner-funded AI/API.
