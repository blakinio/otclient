---
task_id: OTC-20260817-track-a-p2-raw-transform-semantics
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: investigate
branch: research/OTC-20260817-track-a-p2-raw-transform-semantics
base_branch: main
base_main: 8a5fcfd72f2554261eef91a2129c9cc076e730ea
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-p2-raw-transform-semantics.md
  - docs/agents/evidence/OTC-20260817-track-a-p2-raw-transform-semantics/**
  - .github/workflows/tibia-official-client-re-p2-raw-transform-semantics.yml
modules_touched: []
reuses:
  - PR #496 canonical sequence promotion
  - PR #494 canonical framing promotion
  - run 32005141186 accepted RawDataProcessor/setup evidence
depends_on:
  - main@8a5fcfd72f2554261eef91a2129c9cc076e730ea
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
  sequence: PROVEN
  compression: UNKNOWN
  encryption: UNKNOWN
  rawdataprocessor_member_pair: FACT:copied_from_outer_plus_a20_object_plus_c0
  rawdataprocessor_member_vslot_plus_0x20_fast_target: FACT:0xf85eb0
  rawdataprocessor_member_vslot_plus_0x28_fast_target: FACT:0xb3ec30
  conditional_transform_gate: FACT:message_plus_0x28_equals_2
hypotheses:
  h1: 0xb3ec30_is_the_in_place_binary_encryption_transform
  h2: 0xf85eb0_supplies_padding_bytes_only_and_is_not_the_primary_transform
  h3: compression_is_independent_and_remains_UNKNOWN_unless_directly_observed
next_action: exact-fence and stage bounded windows for 0xb3ec30, 0xf85eb0 and the setup/owner construction around 0x196f000..0x1972200; decode only on GitHub-hosted Linux and bind transform input/output plus dynamic object provenance
---

# Track A P2 — RawDataProcessor transform semantics

## Objective

Resolve the smallest remaining byte-transform frontier before the already-proven framing/sequence/QTcpSocket boundary:

```text
RawDataProcessor this+0x8/+0x10 member
 -> padding vslot +0x20 / 0xf85eb0
 -> conditional vslot +0x28 / 0xb3ec30 when message+0x28 == 2
```

Classify encryption and compression independently from exact dataflow. Do not infer either from names, 8-byte alignment or known Tibia protocol expectations.

## Acceptance

- [ ] source runner only exact-fences and copies bounded file-backed bytes;
- [ ] semantic disassembly and classification are GitHub-hosted;
- [ ] identify exact `0xb3ec30` function boundary and its byte-container input/output effect;
- [ ] bind its receiver to the RawDataProcessor member object, and resolve dynamic type/provenance where exact evidence permits;
- [ ] identify `0xf85eb0` concrete effect sufficiently to distinguish padding-byte generation from the main transform;
- [ ] classify `ENCRYPTION=PROVEN|DISPROVEN|UNKNOWN` only from direct transform evidence;
- [ ] classify `COMPRESSION=PROVEN|DISPROVEN|UNKNOWN` separately;
- [ ] preserve canonical `FRAMING=PROVEN`, `SEQUENCE=PROVEN` and QTcpSocket boundary;
- [ ] no runtime/login/world-map/process-memory/full executable upload/owner-funded AI.
