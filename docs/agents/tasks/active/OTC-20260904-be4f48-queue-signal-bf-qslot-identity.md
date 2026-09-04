---
task_id: OTC-20260904-be4f48-queue-signal-bf-qslot-identity
status: implementing
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: implement
branch: research/OTC-20260904-be4f48-queue-signal-bf-qslot-identity
base_branch: main
base_main: e24462d72942d8381e1a468de84f16b60f1aa8c9
created: 2026-09-04T13:00:00+02:00
updated_at: 2026-09-04T13:00:00+02:00
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
persistent_session_role: none
physical_e2e_required: false
implementation_authorized: true
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one bounded static QSlot producer/function discriminator tied to one promoted connectImpl FDE
feature_scope:
  type: contract_producer
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
invocation_started_at: 2026-09-04T12:53:00+02:00
last_progress_at: 2026-09-04T13:00:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
owned_paths:
  - .github/workflows/tibia-official-client-re-be4f48-queue-signal-bf-qslot-identity.yml
  - tools/tibia_re_be4f48_queue_signal_bf_qslot_identity/**
  - docs/agents/tasks/active/OTC-20260904-be4f48-queue-signal-bf-qslot-identity.md
  - docs/agents/evidence/OTC-20260904-be4f48-queue-signal-bf-qslot-identity/**
reuses:
  - coordinator promotion #881 / merge 2023254a4c6f0bac3a5ac4e8b06426d9dfed0862
  - registration #883 / main e24462d72942d8381e1a468de84f16b60f1aa8c9
  - closed source PR #880 only as discovery input, never as promotion authority
depends_on: []
blocks:
  - clean coordinator promotion before any Track B decision
last_completed_step: claimed isolated source-only task from current main; overlap preflight found parallel #884 on disjoint paths
next_action: add repository-only RED contract and focused pull-request workflow with qslot_identity.py intentionally absent
---

# Objective

Resolve only the exact QSlot object/function construction for the promoted queue signal connection:

```text
TProtocolMessageQueue::clientMessageReadyToProcess (signal 0xbf)
  -> QObject::connectImpl @ 0xbe2eee
  -> QSlot object passed as r9
  -> producer/call-return boundary 0xbe2eb1
  -> exact QSlot function target / slot identity
  -> at most one uniquely identity-preserving downstream writer edge
```

# Exact fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

# Promoted starting facts

```text
queue_sender_identity=tibia::protocol::TProtocolMessageQueue
queue_signal_name=clientMessageReadyToProcess
queue_signal_index=0xbf
queue_signal_body=0xbd2190
queue_signal_connectimpl_callsite=0xbe2eee
queue_signal_connectimpl_fde=0xbe2a50..0xbe3086
queue_signal_receiver_provenance=ENTRY_ARG:rdi
qslot_object_argument=r9 <- rax after call-return boundary 0xbe2eb1
queue_signal_qslot_function=UNKNOWN
queue_signal_writer_identity=UNKNOWN
FIRST_MISSING_BOUNDARY=QUEUE_SIGNAL_BF_QSLOT_FUNCTION_NOT_UNIQUELY_PROVEN
```

# Acceptance / bounded stop rule

Start only from FDE `0xbe2a50..0xbe3086` and producer boundary `0xbe2eb1`. Follow the smallest identity-preserving construction chain needed to identify the exact QSlot function. If and only if one unique slot target is proven, follow at most one additional uniquely identity-preserving writer edge. Stop at the first non-unique producer/type/writer edge and emit `SOURCE_BLOCKER` rather than widening to a global Qt/socket/writer census.

Required terminal outcomes are exactly `QUEUE_SIGNAL_BF_QSLOT_IDENTITY_PROVEN`, `FINAL_WRITER_EDGE_PROVEN`, or `SOURCE_BLOCKER`.

# Safety

Static source-only analysis with `runtime_access: none`. No official-client execution, login, credentials, process memory, packet capture, OCR/Vision, official-service E2E, runtime Field6 observation, Track B PR #284 mutation, protocol rewrite, or parallel sendLogin receiver-field-owner analysis.
