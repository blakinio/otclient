---
task_id: OTC-20260817-track-a-p2-f50090-downstream
status: ready
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: claim
branch: research/OTC-20260817-track-a-p2-f50090-downstream
base_branch: main
base_main: PENDING_PROMOTION_MERGE
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-p2-f50090-downstream.md
  - docs/agents/evidence/OTC-20260817-track-a-p2-f50090-downstream/**
modules_touched: []
depends_on:
  - coordinator promotion of OTC-20260817-track-a-p2-dual-nested-vcall-resolution
  - PR #481 canonical P2 chain
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: bounded exact-client static dataflow discriminator; no live runtime required
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
decomposition_decision: single
validation_level: focused
execution_class: github_hosted
source_staging_class: exact_fenced_file_only_nonsemantic_if_additional_bytes_required
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
  same_message_to_f50090: PROVEN_AFTER_COORDINATOR_PROMOTION
  target: 0xf50090
  final_binary_egress: UNKNOWN
  final_socket_ownership: UNKNOWN
  framing: UNKNOWN
  sequence: UNKNOWN
  compression: UNKNOWN
  encryption: UNKNOWN
next_action: after promotion reaches main, disassemble a bounded exact-client window for 0xf50090 and track the preserved same second argument to a concrete binary-write sink or the next exact transform/forward target
---

# Track A P2 — `0xf50090` downstream discriminator

## Objective

Continue only the newly proven same-message branch:

```text
... -> TGameserverDualConnection +0x78
 -> TGameserverNetworkPacketConnection
 -> TGameserverNetworkPacketProcessor
 -> receiver vtable 0x2f741d8 +0x10
 -> 0xf50090
```

Recover the smallest exact downstream edge from `0xf50090` while preserving the same input argument.

## Acceptance inventory

- [ ] exact client size/SHA fenced before any new bytes are consumed;
- [ ] function boundary and SysV input dataflow for `0xf50090` reconstructed from exact bytes;
- [ ] relationship of the canonical same message to `0xf50090` arguments classified FACT/DISPROVEN/UNKNOWN;
- [ ] first downstream concrete call/virtual target carrying that message resolved when exact evidence permits;
- [ ] if a direct binary-write sink is present, receiver/payload ownership proven from dataflow rather than names;
- [ ] if no sink is present, next exact transform/forward target identified without semantic guessing;
- [ ] framing/sequence/compression/encryption/final socket ownership remain UNKNOWN unless independently proven;
- [ ] no world-map evidence, live runtime, process memory, login/gameplay, OTClient/Canary/CrystalServer behavioral proof or owner-funded AI used;
- [ ] one-shot staging surfaces removed after evidence capture;
- [ ] final Draft exact-head governance/CI/review hygiene green before coordinator review.

## Stop condition

Stop once the same-message path through `0xf50090` has one exact falsifiable downstream classification. Do not broaden into a generic Qt/network census.
