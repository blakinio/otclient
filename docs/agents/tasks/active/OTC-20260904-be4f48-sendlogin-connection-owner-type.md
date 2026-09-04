---
task_id: OTC-20260904-be4f48-sendlogin-connection-owner-type
status: ready
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: integrate
branch: research/OTC-20260904-be4f48-sendlogin-connection-owner-type
base_branch: main
base_main: e94e6c5764851f9cb62691d90c55f42e9c6253a1
created: 2026-09-04T14:11:00+02:00
updated_at: 2026-09-04T14:23:00+02:00
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
context_score: 8
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one bounded exact-current connection-owner type discriminator with one static analysis workflow
invocation_started_at: 2026-09-04T14:11:00+02:00
last_progress_at: 2026-09-04T14:23:00+02:00
ci_checks_for_current_head: 14
ci_check_generation: source_terminal
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 14
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
owned_paths:
  - .github/workflows/tibia-official-client-re-be4f48-sendlogin-connection-owner-type.yml
  - tools/tibia_re_be4f48_sendlogin_connection_owner_type/**
  - docs/agents/tasks/active/OTC-20260904-be4f48-sendlogin-connection-owner-type.md
  - docs/agents/evidence/OTC-20260904-be4f48-sendlogin-connection-owner-type/**
modules_touched: []
reuses:
  - coordinator promotion #886 / merge 4ca7f33386a3e9d602a942105626150b2359960b
  - archive #887 / merge 6ab922152d288e56112b162518512859552f06e6
  - alias registration #888 / main e94e6c5764851f9cb62691d90c55f42e9c6253a1
  - closed source PR #884 only as consumed sanitized input; its direct-caller scan was not repeated
  - closed source PR #885 only through promoted coordinator facts; queue/QSlot scope is excluded
depends_on: []
blocks:
  - clean coordinator promotion before any Track B decision
red_head: 396849b2ce1ae818c3db42ced133f4e1ffca2674
red_run: 33871893625
red_job: 101019573417
red_result: expected_failure_before_client_materialization
red_first_error: "AssertionError: owner_type.py is missing: expected RED before client materialization"
tdd_red_verified: true
green_implementation_commit: 903b7e6c5f9452d9be545d698355bcb151c62aec
source_head: 903b7e6c5f9452d9be545d698355bcb151c62aec
source_merge_ref_sha: 51a4410e24ee75ed6218e30b5b0e613b00e33792
source_run: 33872240794
source_job: 101020701224
source_result: success
source_artifact_id: 9936389943
source_artifact_digest: sha256:f4fcfd66b409c31ddaf7b06c471eccd33a638d7ff6cdaeeae9c4f47bef147636
source_ci_run: 33872241316
source_ci_result: success
source_governance_run: 33872241004
source_governance_result: success
source_self_hosted_boundary_run: 33872240809
source_self_hosted_boundary_result: success
scientific_terminal_result: SOURCE_BLOCKER
first_missing_boundary: UNIQUE_ENTRY_OBJECT_EDGE_TYPE_NOT_PROVEN
connection_owner_identity: UNKNOWN
connection_owner_identity_proven: false
sendlogin_receiver_identity: UNKNOWN
sendlogin_receiver_identity_proven: false
complete_sender_receiver_pair_proven: false
sendlogin_causal_binding_proven: false
pre_success_send_sequence: UNKNOWN
field6_value: UNKNOWN
e2e_result: NOT_APPLICABLE
e2e_reason: source-only static discriminator; official-client execution and official-service E2E are explicitly forbidden
audit_result: PENDING
audit_independent: false
audit_material_findings_open: PENDING
audit_evidence: PENDING
last_completed_step: exact-current source workflow succeeded and stopped fail-closed after the single admitted owner identity edge did not prove one exact type
next_action: perform fresh whole-diff falsification and exact-head qualification; then clean coordinator promotion may consume this SOURCE_BLOCKER
---

# Objective

Resolve only the exact class/type identity of the object entering connection-owner FDE `0x7c6700..0x7cc933` through `ENTRY_ARG:rdi` using bounded in-FDE identity evidence and at most one unique identity-preserving vtable/RTTI/QMeta/type edge.

Only if that owner identity is proven and the object layout gives one unique identity-preserving route to `+0x88` may the receiver field/type be classified.

# Exact fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

# Terminal source result

```text
EXACT_CLIENT_FENCE_PROVEN=true
CONNECTION_OWNER_FDE=0x7c6700..0x7cc933
CONNECTION_OWNER_ENTRY_OBJECT=ENTRY_ARG:rdi
CONNECTION_OWNER_IDENTITY=UNKNOWN
CONNECTION_OWNER_IDENTITY_PROVEN=false
SENDLOGIN_RECEIVER_PROVENANCE=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
SENDLOGIN_RECEIVER_IDENTITY=UNKNOWN
SENDLOGIN_RECEIVER_IDENTITY_PROVEN=false
COMPLETE_SENDER_RECEIVER_PAIR_PROVEN=false
SENDLOGIN_CAUSAL_BINDING_PROVEN=false
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=UNIQUE_ENTRY_OBJECT_EDGE_TYPE_NOT_PROVEN
NEXT_ACTION=one newly admitted bounded step only if coordinator authorizes it
```

No typed vptr/RTTI event was bound to `ENTRY_ARG:rdi` inside the selected owner FDE. Exactly one owner-bound adjacent edge was admitted and followed: `0x7c67b8 -> 0x7e8f30`. That edge did not prove one exact type, so the task stops without widening the search.

# Evidence

Sanitized exact-current result: `docs/agents/evidence/OTC-20260904-be4f48-sendlogin-connection-owner-type/result.json`.

Source report: `docs/agents/evidence/OTC-20260904-be4f48-sendlogin-connection-owner-type/20260904-source-result.md`.

# Safety

Source-only static analysis. No official-client execution, login, credential/session/cookie/character/world access, process-memory access, packet capture, OCR/Vision, official-service E2E, runtime Field6 observation, queue/QSlot/writer work, Track B mutation, guessed Field6 value or guessed pre-success order.

# Lifecycle

This source task is scientifically terminal and ready for falsification/qualification and then clean coordinator consumption. PR #889 remains Draft and must not self-merge. Track B PR #284 remains untouched.
