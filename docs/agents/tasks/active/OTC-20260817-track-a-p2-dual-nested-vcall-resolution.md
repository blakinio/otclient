---
task_id: OTC-20260817-track-a-p2-dual-nested-vcall-resolution
status: ready
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: claim
branch: research/OTC-20260817-track-a-p2-dual-nested-vcall-resolution
base_branch: main
base_main: PENDING_PROMOTION_MERGE
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-p2-dual-nested-vcall-resolution.md
  - docs/agents/evidence/OTC-20260817-track-a-p2-dual-nested-vcall-resolution/**
modules_touched: []
depends_on:
  - coordinator promotion of OTC-20260817-track-a-p2-dual-precondition-egress
  - PR #450 merged canonical P2 chain
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: bounded exact-client static discriminator; no live runtime required
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: checkpoint_only
user_communication: low_noise
decomposition_decision: single
validation_level: focused
execution_class: github_hosted
source_staging_class: exact_fenced_file_only_nonsemantic_if_additional_bytes_are_required
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
  canonical_chain: persistent_QBuffer_to_TProtocolClientMessageProcessor_to_TGameserverNetworkPacketRawDataProcessor_to_same_message_to_TGameserverDualConnection_plus_0x80_plus_0x78
  nested_vcall_1: 0xb56c93
  nested_vcall_2: 0xb57042
  b40630_reachability: UNKNOWN
  final_binary_egress: UNKNOWN
next_action: after promotion dependency is on main, recover exact receiver provenance and concrete vtable +0x10 target for 0xb56c93 and 0xb57042 and test whether either exact edge reaches 0xb40630 while preserving the same-message argument
---

# Track A P2 — DualConnection nested virtual-call resolution

## Objective

Resolve the two still-untyped nested virtual calls at `0xb56c93` and `0xb57042` far enough to make one falsifiable reachability decision downstream of the canonical #450 same-message handoff.

The task must determine from exact-client evidence:

1. the receiver object provenance at each call;
2. the receiver vtable identity when recoverable;
3. the concrete target of vslot `+0x10` when recoverable;
4. whether either exact target is `0xb40630` or another exact function;
5. whether the original promoted same-message argument is preserved across that edge.

## Scope boundary

Do not infer a target from address proximity, vtable adjacency, class names or Qt semantics. Do not label any recovered target as framing, compression, encryption, sequence handling, socket ownership or final egress unless this bounded task directly proves that semantic property.

Do not revisit world-map/map evidence. Do not use OTClient/Canary/CrystalServer as official-client behavioral proof. No runtime/login/gameplay/process-memory work is authorized by this task.

## Acceptance inventory

- [ ] exact client size/SHA fenced before using any additional file bytes;
- [ ] both callsite receiver dataflows reconstructed from exact bytes;
- [ ] vtable/slot target resolved with relocation/object-construction evidence, or explicitly retained UNKNOWN with the failed discriminator recorded;
- [ ] exact test of `target == 0xb40630` for each call;
- [ ] same-message argument preservation classified FACT/DISPROVEN/UNKNOWN from register/dataflow evidence;
- [ ] no framing/compression/encryption/final-egress semantic overpromotion;
- [ ] one-shot staging surfaces removed after evidence capture;
- [ ] final researcher Draft CI/governance green before coordinator review.

## Stop condition

Stop this bounded task once both nested `+0x10` calls are classified to the strongest exact evidence available. If neither can be resolved, persist the narrow missing byte/object-construction evidence required; do not broaden into a generic network reverse-engineering sweep.
