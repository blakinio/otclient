---
task_id: OTC-20260904-be4f48-sendlogin-receiver-field-owner
status: validating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: validate
branch: research/OTC-20260904-be4f48-sendlogin-receiver-field-owner
base_branch: main
base_main: e24462d72942d8381e1a468de84f16b60f1aa8c9
created: 2026-09-04T12:52:00+02:00
updated_at: 2026-09-04T13:05:00+02:00
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
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one bounded static field-owner discriminator with one exact-current analysis workflow
invocation_started_at: 2026-09-04T12:52:00+02:00
last_progress_at: 2026-09-04T13:05:00+02:00
ci_checks_for_current_head: 1
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 1
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
owned_paths:
  - .github/workflows/tibia-official-client-re-be4f48-sendlogin-receiver-field-owner.yml
  - tools/tibia_re_be4f48_sendlogin_receiver_field_owner/**
  - docs/agents/tasks/active/OTC-20260904-be4f48-sendlogin-receiver-field-owner.md
  - docs/agents/evidence/OTC-20260904-be4f48-sendlogin-receiver-field-owner/**
modules_touched: []
reuses:
  - coordinator promotion #881 / merge 2023254a4c6f0bac3a5ac4e8b06426d9dfed0862
  - registration #883 / main e24462d72942d8381e1a468de84f16b60f1aa8c9
  - closed source PR #879 only as discovery input, never as promotion authority
depends_on: []
blocks:
  - clean coordinator promotion before any Track B decision
red_head: e9e20394fc28bb5caa4332b0baf4458ef1445c9a
red_run: 33865752388
red_job: 101000116304
red_result: expected_failure_before_client_materialization
red_first_error: "AssertionError: receiver_field_owner.py is missing: expected RED before client materialization"
tdd_red_verified: true
green_attempt_head: bb39f99c8188ec5166eb95b868cfcecfcd9951bf
last_completed_step: verified repository-only RED from job 101000116304, then added the minimal bounded exact-current field-owner analyzer
next_action: inspect the focused source workflow on the current GREEN-attempt head; use its sanitized exact-current result to terminalize or make one evidence-based analyzer repair
---

# Objective

Resolve only the exact definition/ownership/type chain for the promoted sendLogin receiver field:

```text
entry-rdi-derived owner object
  -> field +0x88
  -> initializer/member store defining the receiver pointer
  -> exact receiver object/class identity
```

If and only if the receiver class identity is independently proven, reconcile it with the promoted `TLoginProtocolMessageHandler::sendLoginMessage -> QObject::connectImpl@0x7c6b9f -> QSlot(adapter 0xbd3050)` connection and state whether complete sender/receiver causality is proven or rejected.

# Exact fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

# Promoted starting facts

```text
receiver_field_provenance=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
selected_connection_owner_fde=0x7c6700..0x7cc933
receiver_field_reads_in_selected_fde=165
receiver_field_writes_in_selected_fde=0
receiver_endpoint_identity=UNKNOWN
FIRST_MISSING_BOUNDARY=RECEIVER_FIELD_DEFINITION_OUTSIDE_SELECTED_CONNECTION_OWNER_FDE
```

# TDD state

Repository-only RED is verified on head `e9e20394fc28bb5caa4332b0baf4458ef1445c9a`: workflow run `33865752388`, job `101000116304`, failed in the first contract step because `receiver_field_owner.py` was deliberately absent. WARP preparation, exact-client materialization, analysis and artifact upload were all skipped. Only after that expected RED was observed, the bounded analyzer was added on head `bb39f99c8188ec5166eb95b868cfcecfcd9951bf`.

The GREEN attempt performs only the target-specific direct-caller xref for the promoted connection-owner FDE, inspects only the resulting unique caller FDE, binds a `+0x88` member store to the exact owner argument, and follows only constructor calls fed by that exact stored object. A positive identity requires both a unique bound field-store/constructor chain and matching primary-vptr Itanium RTTI.

# Safety

Source-only static analysis. No official-client execution, login, credentials, process memory, packet capture, OCR/Vision, official-service E2E, runtime Field6 observation, Track B PR #284 mutation, or protocol rewrite.

# Acceptance / stop rule

Follow only the smallest identity-preserving owner/caller/constructor chain needed to reach the defining `+0x88` store. Stop at the first non-unique initializer/constructor edge and emit a precise `SOURCE_BLOCKER` rather than opening another analyzer family.
