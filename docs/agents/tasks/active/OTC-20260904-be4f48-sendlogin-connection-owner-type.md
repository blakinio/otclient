---
task_id: OTC-20260904-be4f48-sendlogin-connection-owner-type
status: active
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: validate
branch: research/OTC-20260904-be4f48-sendlogin-connection-owner-type
base_branch: main
base_main: e94e6c5764851f9cb62691d90c55f42e9c6253a1
created: 2026-09-04T14:11:00+02:00
updated_at: 2026-09-04T14:17:00+02:00
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
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one bounded exact-current connection-owner type discriminator with one static analysis workflow
invocation_started_at: 2026-09-04T14:11:00+02:00
last_progress_at: 2026-09-04T14:17:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: green_candidate
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
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
  - closed source PR #884 only as consumed sanitized input; its direct-caller scan must not be repeated
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
green_implementation_commit: PENDING
source_head: PENDING
source_run: PENDING
source_job: PENDING
source_result: PENDING
scientific_terminal_result: PENDING
first_missing_boundary: PENDING
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
last_completed_step: repository-only TDD RED verified on run 33871893625 job 101019573417; WARP and all client-materialization steps were skipped
next_action: validate the smallest bounded in-FDE/one-edge owner-type analyzer on the exact client fence and consume only its sanitized result
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

# Starting facts

```text
CONNECTION_OWNER_FDE=0x7c6700..0x7cc933
CONNECTION_OWNER_ENTRY_OBJECT=ENTRY_ARG:rdi
SENDLOGIN_RECEIVER_PROVENANCE=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
sendlogin_connectimpl_callsite=0x7c6b9f
sendlogin_adapter_target=0xbd3050
```

# Search boundary

Allowed: selected owner FDE/object -> in-FDE identity evidence -> at most one unique identity-preserving vtable/RTTI/QMeta/type edge -> optional `+0x88` typing only if owner identity makes that route unique.

Forbidden: consumed #884 direct-caller scan, global constructor/caller census, global RTTI/QMeta/QObject/vtable census, global `+0x88` search, queue signal/QSlot/writer work, Track B mutation, runtime access, official-client execution, login, packet capture, OCR/Vision, official-service E2E, Field6 observation or guessing.

# TDD state

Repository-only RED is proven at `396849b2ce1ae818c3db42ced133f4e1ffca2674`: workflow run `33871893625`, job `101019573417`, failed in `Validate repository-only connection owner-type contract`. The WARP preparation, transient client materialization, analyzer, result validation and artifact upload steps were all skipped. The analyzer is therefore admitted for the GREEN phase without having touched client bytes during RED.
