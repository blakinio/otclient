---
task_id: OTC-20260904-be4f48-sendlogin-owner-edge-7e8f30-identity
status: validating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: validate
branch: research/OTC-20260904-be4f48-sendlogin-owner-edge-7e8f30-identity
base_branch: main
base_main: 7e67c67783b19575ec7f378c7be49cb69d87f1ce
created: 2026-09-04T15:44:00+02:00
updated_at: 2026-09-04T15:52:00+02:00
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
last_progress_at: 2026-09-04T15:52:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: source_checkpoint
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
red_head: 684e301ada1feef6590fc59b3375a19c547f16a8
red_run: 33879930241
red_job: 101045813815
red_result: expected_failure_before_client_materialization
red_first_error: "AssertionError: edge_identity.py is missing: expected RED before client materialization"
tdd_red_verified: true
green_implementation_commit: 9c68d92657100b054c6d5006ab46ddc5303112ee
source_head: 9c68d92657100b054c6d5006ab46ddc5303112ee
source_run: 33880393758
source_job: 101047349555
source_result: RUNNING
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
last_completed_step: verified repository-only RED at head 684e301ada1feef6590fc59b3375a19c547f16a8 and added the minimal callee-only analyzer at 9c68d92657100b054c6d5006ab46ddc5303112ee
next_action: inspect the terminal scientific source run 33880393758 and persist its sanitized exact-current result, then perform whole-diff falsification and exact-head qualification
recovery:
  policy_version: 1
  generation: 2
  session_id: chat-github-20260904T153700+0200
  session_started_at: 2026-09-04T15:37:00+02:00
  checkpointed_at: 2026-09-04T15:52:00+02:00
  last_progress_at: 2026-09-04T15:52:00+02:00
  phase: validate
  exact_head: PENDING_TASK_CHECKPOINT_COMMIT
  pull_request: 894
  active_operation: scientific source workflow run 33880393758 on 9c68d92657100b054c6d5006ab46ddc5303112ee
  external_run_ids: [33880393758, 33880394037, 33880393831, 33880394167]
  operation_started_at: 2026-09-04T15:50:00+02:00
  wait_deadline_at: null
  check_generation: source_checkpoint
  checks_used: 0
  status: active
  safe_to_resume: true
  resume_condition: scientific source workflow 33880393758 reaches terminal conclusion
  next_action: inspect run 33880393758, retrieve sanitized result artifact/log evidence, and persist the scientific boundary without widening scope
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

# TDD RED evidence

At exact head `684e301ada1feef6590fc59b3375a19c547f16a8`, workflow run `33879930241`, job `101045813815` failed exactly at the repository-only contract with:

```text
AssertionError: edge_identity.py is missing: expected RED before client materialization
```

The subsequent WARP, client materialization, result validation and artifact steps were all skipped. This satisfies the required RED-before-client boundary.

# GREEN implementation boundary

The implementation at `9c68d92657100b054c6d5006ab46ddc5303112ee`:

- starts only from callee `0x7e8f30` and its containing FDE;
- binds type evidence only to the same `ENTRY_ARG:rdi` object;
- accepts exact Itanium RTTI only when tied to an object vptr store;
- if callee-local proof is absent, enumerates only same-object direct internal calls inside that callee and follows one only when exactly one candidate exists;
- follows no second internal edge;
- does not rediscover callers, rescan the connection-owner FDE, or open a global type census;
- leaves the `+0x88` receiver identity `UNKNOWN` unless the bounded owner proof itself uniquely implies more.

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
