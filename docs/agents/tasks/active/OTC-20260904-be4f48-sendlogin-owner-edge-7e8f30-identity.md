---
task_id: OTC-20260904-be4f48-sendlogin-owner-edge-7e8f30-identity
status: implementing
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: implement
branch: research/OTC-20260904-be4f48-sendlogin-owner-edge-7e8f30-identity
base_branch: main
base_main: 7e67c67783b19575ec7f378c7be49cb69d87f1ce
created: 2026-09-04T15:44:00+02:00
updated_at: 2026-09-04T15:44:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
runtime_access: none
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
physical_e2e_required: false
implementation_authorized: true
feature_scope:
  type: contract_producer
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one exact-current callee-local owner identity discriminator with one static analysis workflow
invocation_started_at: 2026-09-04T15:37:00+02:00
last_progress_at: 2026-09-04T15:44:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: red_contract
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
owned_paths:
  - .github/workflows/tibia-official-client-re-be4f48-sendlogin-owner-edge-7e8f30-identity.yml
  - tools/tibia_re_be4f48_sendlogin_owner_edge_7e8f30_identity/**
  - docs/agents/tasks/active/OTC-20260904-be4f48-sendlogin-owner-edge-7e8f30-identity.md
  - docs/agents/evidence/OTC-20260904-be4f48-sendlogin-owner-edge-7e8f30-identity/**
modules_touched: []
reuses:
  - coordinator promotion #891 / merge b4582b1e72d689b5d26fbd16c0ba2bbd20dca970
  - archive #892 / merge 58cc12558babcfcadaa89bbdc49ca19ee1e58e5e
  - alias registration #893 / main 7e67c67783b19575ec7f378c7be49cb69d87f1ce
  - closed source PR #889 only as consumed sanitized evidence and generic analyzer/workflow pattern; its owner-FDE scan is not repeated
depends_on: []
blocks:
  - clean coordinator promotion before any Track B decision
red_head: PENDING
red_run: PENDING
red_job: PENDING
red_result: PENDING
red_first_error: PENDING
tdd_red_verified: false
green_implementation_commit: PENDING
source_head: PENDING
source_run: PENDING
source_job: PENDING
source_result: PENDING
source_artifact_id: PENDING
source_artifact_digest: PENDING
scientific_terminal_result: PENDING
first_missing_boundary: PENDING
owner_edge_callsite: 0x7c67b8
owner_edge_callee: 0x7e8f30
owner_object_identity: UNKNOWN
owner_object_identity_proven: false
sendlogin_receiver_identity: UNKNOWN
sendlogin_receiver_identity_proven: false
complete_sender_receiver_pair_proven: false
sendlogin_causal_binding_proven: false
pre_success_send_sequence: UNKNOWN
field6_value: UNKNOWN
e2e_result: NOT_APPLICABLE
e2e_reason: source-only static discriminator; official-client execution and official-service E2E are explicitly forbidden
last_completed_step: claimed non-overlapping exact-callee source task from trusted main
next_action: publish repository-only RED contract and verify it fails because edge_identity.py is missing before any client materialization
recovery:
  policy_version: 1
  generation: 1
  session_id: chat-github-20260904T153700+0200
  session_started_at: 2026-09-04T15:37:00+02:00
  checkpointed_at: 2026-09-04T15:44:00+02:00
  last_progress_at: 2026-09-04T15:44:00+02:00
  phase: implement
  exact_head: PENDING
  pull_request: none
  active_operation: repository-only RED workflow preparation
  external_run_ids: []
  operation_started_at: null
  wait_deadline_at: null
  check_generation: red_contract
  checks_used: 0
  status: active
  safe_to_resume: true
  resume_condition: branch contains task record plus RED contract/workflow
  next_action: create RED contract and workflow, open Draft PR, then inspect first workflow run for the expected missing-analyzer failure
---

# Objective

Resolve only the exact identity semantics of the already-promoted owner-bound edge `0x7c67b8 -> 0x7e8f30`, carrying the same `ENTRY_ARG:rdi` owner object.

Analyze only the callee FDE and, if necessary, at most one unique internal identity-preserving edge. Do not repeat #884 caller discovery or #889 owner-FDE scanning and do not open a global constructor, RTTI, QMeta, QObject, vtable or `+0x88` census.

# Exact fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

# Starting evidence

```text
OWNER_EDGE_CALLSITE=0x7c67b8
OWNER_EDGE_CALLEE=0x7e8f30
OWNER_OBJECT=ENTRY_ARG:rdi
SENDLOGIN_RECEIVER_PROVENANCE=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
OWNER_OBJECT_IDENTITY=UNKNOWN
SENDLOGIN_RECEIVER_IDENTITY=UNKNOWN
FIRST_MISSING_BOUNDARY=UNIQUE_ENTRY_OBJECT_EDGE_TYPE_NOT_PROVEN
```

# Safety

Source-only static analysis. No official-client execution, login, credential/session/cookie/character/world access, process-memory access, packet capture, OCR/Vision, official-service E2E, runtime Field6 observation, queue/QSlot/writer work, Track B mutation, guessed Field6 value or guessed pre-success order.

# Acceptance

- repository-only RED is observed before any WARP/client materialization;
- exact fence is enforced before analysis;
- analysis begins at `0x7e8f30` and never rescans the owner FDE;
- at most one unique internal identity-preserving edge is followed;
- deterministic sanitized JSON records either `SENDLOGIN_OWNER_EDGE_IDENTITY_PROVEN` or `SOURCE_BLOCKER`;
- transient official-client bytes are deleted before artifact upload;
- Track B PR #284 remains untouched;
- fresh exact-head qualification and whole-diff falsification are recorded before coordinator handoff.
