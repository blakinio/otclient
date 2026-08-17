---
task_id: OTC-20260817-track-a-p2-sequence-provenance
status: ready
agent: ChatGPT
session_role: draft_researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: review
branch: research/OTC-20260817-track-a-p2-sequence-provenance
base_branch: main
base_main: 0aed48da9a51730c590d0ffe4688f149b359a170
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-p2-sequence-provenance.md
  - docs/agents/evidence/OTC-20260817-track-a-p2-sequence-provenance/**
modules_touched: []
reuses:
  - PR #494 canonical framing promotion
  - PR #492 canonical QTcpSocket-bound binary boundary
  - run 32005141186 accepted same-message processor chain
  - run 32037533068 exact f50090 framing bytes
depends_on:
  - main@0aed48da9a51730c590d0ffe4688f149b359a170
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
research_output: DRAFT_NOT_PROMOTED_READY_FOR_COORDINATOR_REVIEW
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
research_result:
  framing: PROVEN
  sequence: PROVEN
  compression: UNKNOWN
  encryption: UNKNOWN
  final_binary_egress: PROVEN_AT_QT_QTCPSOCKET_BOUNDARY
  final_socket_owner: FACT:TGameserverTCPConnection
  final_os_socket_syscall: UNKNOWN
  sequence_field: FACT:DWORD_message_plus_0
  sequence_owner: FACT:TGameserverDualConnection_this_plus_0x9c
  sequence_mode: FACT:message_plus_0x34_equals_3
  sequence_update: FACT:store_current_then_increment_by_one
  sequence_nonmatching_mode: FACT:message_plus_0_zero
  sequence_initialization_or_reset_policy: UNKNOWN
generation:
  run: 32044825898
  source_job: 95430326316
  hosted_job: 95430351866
  result: SUCCESS
  window: 0xb56d60..0xb57280
  window_digest: sha256:e5cf009bb1aec3065da4ff0dd3231268af1255cffa50fbb48f8817777907d557
cleanup:
  one_shot_workflow_removed: pending
validation:
  source_exact_fence: PASS
  hosted_decode: PASS
  no_runtime_access: true
  no_world_map_evidence: true
  raw_client_uploaded: false
  final_exact_head_governance: PENDING
  final_exact_head_ci: PENDING
  review_hygiene: PENDING
next_action: remove the one-shot workflow, obtain final exact-head governance/CI/review hygiene, then coordinator independently promote SEQUENCE=PROVEN; afterwards resolve RawDataProcessor member transform 0xb3ec30 for encryption
---

# Track A P2 — outbound sequence provenance

## Terminal researcher result

The canonical pre-payload `DWORD(message+0)` is directly produced by `TGameserverDualConnection+0x80@0xb56d60`.

For `message+0x34 == 3`:

```text
b57058  eax = DWORD[DualConnection this+0x9c]
b5705f  DWORD[message+0] = eax
b57061  eax += 1
b57064  DWORD[DualConnection this+0x9c] = eax
```

For the nonmatching branch, `b56f5a` explicitly writes zero to `DWORD(message+0)`.

The same message is saved at entry (`b56d75`) and restored before this update (`b56f46`). Canonical framing PR #494 independently proves that exact field is serialized before the raw payload. Therefore the outbound sequence-number mechanism is instruction/dataflow-proven rather than inferred from field width or location.

```text
FRAMING=PROVEN
SEQUENCE=PROVEN
COMPRESSION=UNKNOWN
ENCRYPTION=UNKNOWN
```

Durable evidence:
- `docs/agents/evidence/OTC-20260817-track-a-p2-sequence-provenance/20260817-sequence-provenance.md`
- `docs/agents/evidence/OTC-20260817-track-a-p2-sequence-provenance/result.json`

Promotion authority remains coordinator-only. E2E: `NOT_APPLICABLE` — static exact-file/disassembly evidence only.
