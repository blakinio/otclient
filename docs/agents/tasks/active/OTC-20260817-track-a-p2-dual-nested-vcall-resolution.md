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
research_result:
  b56c93_same_message_preserved: FACT
  outer_type: FACT:tibia::network::TGameserverNetworkPacketConnection
  outer_vtable_ap: FACT:0x3084ba8
  intermediate_type: FACT:tibia::network::TGameserverNetworkPacketProcessor
  intermediate_vtable_ap: FACT:0x30b7a68
  final_receiver_vtable_ap: FACT:0x2f741d8
  final_receiver_rtti_pointer: FACT:0x30b7548
  final_receiver_exact_dynamic_type: UNKNOWN
  b56c93_virtual_slot: FACT:+0x10
  b56c93_concrete_target: FACT:0xf50090
  b56c93_target_equals_b40630: DISPROVEN
  b57042_same_message_preserved: DISPROVEN
  dualconnection_to_binary_egress: UNKNOWN
  final_binary_egress: UNKNOWN
  final_socket_ownership: UNKNOWN
  framing: UNKNOWN
  sequence: UNKNOWN
  compression: UNKNOWN
  encryption: UNKNOWN
generations:
  - run: 32033753449
    source_job: 95399308395
    hosted_job: 95400245919
    source_artifact: 9289952632
    source_digest: sha256:176a174bafd8f77fb82ff8ea3737b0850be5b0327dc2ba6065e0d9bf51574e5a
    final_artifact: 9289961937
    final_digest: sha256:fa1cddd5410454d9f5b717afe0d625d404a7750fb82ffb4b8a9d288cbc9ac64a
    result: SUCCESS
  - run: 32034648596
    source_job: 95402114226
    hosted_job: 95402454465
    source_artifact: 9290206232
    source_digest: sha256:27e946c3a864aac6257675e3ff6403eec93476223efed400bd72907cdb10f1a4
    final_artifact: 9290395475
    final_digest: sha256:a0b396081570a1729e964bf8c57ad726ab95d91e3cf54f6857ebb43248afdebf
    result: SUCCESS
  - run: 32035436709
    source_job: 95404656415
    hosted_job: 95404893228
    source_artifact: 9290490800
    source_digest: sha256:f70f2f1ecc4e4af15323c6bee8998938cc79c25c454d72101672c1d9a0a68fa6
    final_artifact: 9290498273
    final_digest: sha256:4aa991a9912c3fb56cc08863ba94ac9e73e78a466a966c00353e85ce39a85323
    result: SUCCESS
cleanup:
  one_shot_workflows_removed: true
  one_shot_scripts_removed: true
validation:
  source_exact_fences: PASS
  hosted_primary_review: PASS
  artifact_redownload_rehash: PASS
  no_world_map_evidence: true
  no_runtime_access: true
  raw_client_uploaded: false
  final_exact_head_governance: PENDING
  final_exact_head_ci: PENDING
  review_hygiene: PENDING
next_action: coordinator independently review artifacts and durable evidence, promote accepted result, then continue P2 at exact target 0xf50090
---

# Track A P2 — DualConnection nested virtual-call resolution

## Terminal researcher result

The two nested `+0x10` candidates downstream of the canonical #450 chain are now resolved to the strongest exact evidence required by this task.

For `TGameserverDualConnection +0x78@0xb56970`, the original second argument is preserved to `0xb56c93`. Exact vtable/RTTI and constructor evidence binds the receiver chain:

```text
same post-RawDataProcessor message
 -> TGameserverDualConnection +0x78
 -> tibia::network::TGameserverNetworkPacketConnection
 -> tibia::network::TGameserverNetworkPacketProcessor
 -> receiver vtable AP 0x2f741d8
 -> slot +0x10
 -> 0xf50090
```

The concrete slot target is therefore `FACT:0xf50090`; the historical/current candidate `target == 0xb40630` is `DISPROVEN` for this surviving same-message branch.

For `0xb57042`, the exact visible taken branch retains `rsi=0x100000001`, so same-message preservation is `DISPROVEN` and it is not used as a continuation edge.

No final-egress or layer semantic is invented:

```yaml
DUALCONNECTION_TO_BINARY_EGRESS: UNKNOWN
FINAL_BINARY_EGRESS: UNKNOWN
FINAL_SOCKET_OWNER: UNKNOWN
FRAMING: UNKNOWN
SEQUENCE: UNKNOWN
COMPRESSION: UNKNOWN
ENCRYPTION: UNKNOWN
```

## Evidence / validation

Three exact-fenced bounded generations completed successfully. Source stages performed file-only deterministic byte mapping; semantic decode occurred on GitHub-hosted Ubuntu. Downloaded artifacts were independently re-hashed against GitHub digests. No raw executable/package, live client, process memory, login/gameplay, world-map evidence or owner-funded AI/API was used.

Durable evidence:

- `docs/agents/evidence/OTC-20260817-track-a-p2-dual-nested-vcall-resolution/20260817-nested-vcall-dataflow.md`
- `docs/agents/evidence/OTC-20260817-track-a-p2-dual-nested-vcall-resolution/result.json`

All temporary workflows/scripts were removed after evidence consumption.

## Acceptance inventory

- [x] exact client size/SHA fenced for all new source generations;
- [x] `0xb56c93` same-message preservation proven;
- [x] outer/intermediate vtable identities proven with RTTI and exact slots;
- [x] final receiver bound through constructor object/member provenance;
- [x] final receiver vtable AP `0x2f741d8` proven;
- [x] concrete `+0x10` target `0xf50090` proven;
- [x] exact `target == 0xb40630` test resolved `DISPROVEN`;
- [x] `0xb57042` same-message continuation disproven;
- [x] framing/sequence/compression/encryption/final egress/socket ownership retained independently as `UNKNOWN`;
- [x] temporary staging surfaces removed;
- [x] durable Markdown/JSON persisted;
- [ ] final exact-head Track A governance/CI and review hygiene verified.

## Handover

Researcher status: `DRAFT_NOT_PROMOTED / READY_FOR_COORDINATOR_REVIEW`.

Next smallest P2 discriminator after coordinator promotion is exact bounded disassembly/dataflow of `0xf50090`, preserving the same second argument and identifying either a concrete binary-write sink or the next exact transform/forward target.
