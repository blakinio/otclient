---
task_id: OTC-20260904-be4f48-queue-signal-bf-relay-receiver-type
status: validating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: validate
branch: research/OTC-20260904-be4f48-queue-signal-bf-relay-receiver-type
base_branch: main
base_main: e94e6c5764851f9cb62691d90c55f42e9c6253a1
created: 2026-09-04T14:18:00+02:00
updated_at: 2026-09-04T14:34:00+02:00
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
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one bounded exact-current receiver-type discriminator at connectImpl@0xbe2eee with at most one uniquely identity-preserving relay edge
feature_scope:
  type: contract_producer
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
invocation_started_at: 2026-09-04T14:11:00+02:00
last_progress_at: 2026-09-04T14:34:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: terminal_evidence_pending_exact_head_checks
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 0
stall_warnings: 0
source_run: 33873246506
source_job: 101024010911
source_head: 7dab5a0cb60f9f971ff0623aa0d5b9922bbbcd65
source_artifact: 9936796961
source_artifact_digest: sha256:9dd2bb0d11af5240b5f0275df89f8b4bccabb3af8d19461642619883ebcc3879
owned_paths:
  - .github/workflows/tibia-official-client-re-be4f48-queue-signal-bf-relay-receiver-type.yml
  - tools/tibia_re_be4f48_queue_signal_bf_relay_receiver_type/**
  - docs/agents/tasks/active/OTC-20260904-be4f48-queue-signal-bf-relay-receiver-type.md
  - docs/agents/evidence/OTC-20260904-be4f48-queue-signal-bf-relay-receiver-type/**
reuses:
  - promotion PR #886 / merge 4ca7f33386a3e9d602a942105626150b2359960b
  - registration PR #888 / main e94e6c5764851f9cb62691d90c55f42e9c6253a1
  - source PR #885 only for already-promoted QSlot facts and workflow pattern
  - source PR #880 only for already-promoted receiver provenance ENTRY_ARG:rdi
depends_on: []
blocks:
  - clean coordinator promotion before any Track B decision
last_completed_step: exact-current receiver identity tibia::protocol::TProtocolMessageQueue and SIGNAL_RELAY role proven on source head 7dab5a0cb60f9f971ff0623aa0d5b9922bbbcd65; sanitized result and proof boundary persisted
next_action: run exact-head terminal checks on the evidence-bearing PR head, then stop for clean coordinator promotion
---

# Objective

Resolve only the exact object/class identity of the receiver passed to the promoted unique `QObject::connectImpl@0xbe2eee`, starting from receiver provenance `ENTRY_ARG:rdi`, then classify that exact connection as `SIGNAL_RELAY`, `WRITER_EDGE`, `OTHER`, or `UNKNOWN`. Follow at most one next `clientMessageReadyToProcess` edge only if receiver identity and relay role are uniquely proven.

# Exact fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

# Promoted inputs

```text
QUEUE_SIGNAL=clientMessageReadyToProcess
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_ARGV1_IDENTITY=exact GameclientMessage shared pair
QUEUE_SIGNAL_CONNECTIMPL_CALLSITE=0xbe2eee
QUEUE_SIGNAL_CONNECTIMPL_FDE=0xbe2a50..0xbe3086
QUEUE_SIGNAL_RECEIVER_PROVENANCE=ENTRY_ARG:rdi
QSLOT_FUNCTION_TARGET=0xbd2190
QSLOT_IDENTITY_PROVEN=true
FINAL_QUEUE_WRITER_IDENTIFIED=false
FINAL_TCP_WRITER_IDENTIFIED=false
FINAL_WRITER_CONTRACT=UNKNOWN
FIELD6_VALUE=UNKNOWN
```

Do not repeat the consumed QSlot construction analysis from #885. Do not reinterpret dispatcher `0xbe4df0` as the callable target.

# Bounded evidence rule

Allowed path only:

```text
connectImpl@0xbe2eee
  -> receiver ENTRY_ARG:rdi
  -> exact receiver type via object-tied vptr/vtable/typeinfo, QMeta/static-metaobject, or one unique constructor/member provenance edge
  -> classify exact connection role
  -> optionally one next unique identity-preserving relay edge
```

Stop at the first non-unique type or relay boundary. No global QObject/QSlot/socket/writer census, no broad whole-executable generic xref scan, no parallel sendLogin owner task, no Track B mutation.

# TDD and scientific state

```text
initial_red_run=33872253528
initial_red_job=101020741944
repair_red_run=33872908681
scientific_green_run=33873246506
scientific_green_job=101024010911
scientific_green_head=7dab5a0cb60f9f971ff0623aa0d5b9922bbbcd65
sanitized_artifact=9936796961
sanitized_artifact_digest=sha256:9dd2bb0d11af5240b5f0275df89f8b4bccabb3af8d19461642619883ebcc3879
```

Initial RED failed before any exact-client materialization because the analyzer was absent. The first implementation exposed a false source blocker caused by re-proving the already-promoted `ENTRY_ARG:rdi` receiver provenance across unrelated caller-saved-register clobbers. Repair RED required explicit promoted-provenance consumption. Repair GREEN proved the receiver from the bounded constructor-tied primary vptr/RTTI path without widening the admitted source scope.

# Source result

```text
EXACT_CLIENT_FENCE_PROVEN=true
QUEUE_SIGNAL=clientMessageReadyToProcess
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_ARGV1_IDENTITY=exact GameclientMessage shared pair
QUEUE_SIGNAL_CONNECTIMPL_CALLSITE=0xbe2eee
QUEUE_SIGNAL_RECEIVER_PROVENANCE=ENTRY_ARG:rdi
QUEUE_SIGNAL_RECEIVER_IDENTITY=tibia::protocol::TProtocolMessageQueue
QUEUE_SIGNAL_RECEIVER_IDENTITY_PROVEN=true
QSLOT_FUNCTION_TARGET=0xbd2190
QUEUE_SIGNAL_CONNECTION_ROLE=SIGNAL_RELAY
NEXT_UNIQUE_RELAY_EDGE=UNKNOWN
NEXT_ENDPOINT_IDENTITY=UNKNOWN
FINAL_QUEUE_WRITER_IDENTIFIED=false
FINAL_TCP_WRITER_IDENTIFIED=false
FINAL_WRITER_CONTRACT=UNKNOWN
FIELD6_VALUE=UNKNOWN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
terminal_result=QUEUE_SIGNAL_BF_RELAY_RECEIVER_TYPE_PROVEN
FIRST_MISSING_BOUNDARY=NEXT_RELAY_EDGE_NOT_UNIQUELY_PROVEN_WITHIN_BOUNDED_RECEIVER_TYPE_PROOF
NEXT_ACTION=clean coordinator promotion before any Track B decision
```

Key bounded type evidence:

```text
QObject::QObject(QObject*) call=0xbe2a6d
entry-object root vptr store=0xbe2a85
base_register=rbx
object_offset=0x0
vptr=0x30ed588
typeinfo=0x30ed548
typeinfo_name_ptr=0x1d77cc0
typeinfo_raw_name=N5tibia8protocol21TProtocolMessageQueueE
demangled_type=tibia::protocol::TProtocolMessageQueue
```

The next relay edge is deliberately left `UNKNOWN`: no further unique identity-preserving edge was established inside this admitted receiver-type proof.

# Safety

```text
runtime_access=none
official_client_execution=false
login=false
credentials=false
process_memory=false
packet_capture=false
ocr_vision=false
official_service_e2e=false
track_b_pr_284_modified=false
```

# Terminal schema

```text
EXACT_CLIENT_FENCE_PROVEN=true|false
QUEUE_SIGNAL=clientMessageReadyToProcess
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_ARGV1_IDENTITY=exact GameclientMessage shared pair
QUEUE_SIGNAL_CONNECTIMPL_CALLSITE=0xbe2eee
QUEUE_SIGNAL_RECEIVER_PROVENANCE=ENTRY_ARG:rdi
QUEUE_SIGNAL_RECEIVER_IDENTITY=<value|UNKNOWN>
QUEUE_SIGNAL_RECEIVER_IDENTITY_PROVEN=true|false
QSLOT_FUNCTION_TARGET=0xbd2190
QUEUE_SIGNAL_CONNECTION_ROLE=<SIGNAL_RELAY|WRITER_EDGE|OTHER|UNKNOWN>
NEXT_UNIQUE_RELAY_EDGE=<value|UNKNOWN>
NEXT_ENDPOINT_IDENTITY=<value|UNKNOWN>
FINAL_QUEUE_WRITER_IDENTIFIED=true|false
FINAL_TCP_WRITER_IDENTIFIED=true|false
FINAL_WRITER_CONTRACT=<value|UNKNOWN>
FIELD6_VALUE=UNKNOWN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
terminal_result=<QUEUE_SIGNAL_BF_RELAY_RECEIVER_TYPE_PROVEN|NEXT_RELAY_EDGE_PROVEN|SOURCE_BLOCKER>
FIRST_MISSING_BOUNDARY=<none|precise boundary>
NEXT_ACTION=<clean coordinator promotion or one newly admitted bounded step>
```
