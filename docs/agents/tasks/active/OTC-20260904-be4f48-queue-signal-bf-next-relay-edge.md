---
task_id: OTC-20260904-be4f48-queue-signal-bf-next-relay-edge
status: implementing
agent: ChatGPT
session_id: chatgpt-20260904T1537+0200
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: implement
branch: ai/OTC-20260904-be4f48-queue-signal-bf-next-relay-edge
base_branch: main
base_main: 7e67c67783b19575ec7f378c7be49cb69d87f1ce
created: 2026-09-04T15:37:00+02:00
updated_at: 2026-09-04T15:37:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
execution_reason: bounded exact-current static source discriminator; GitHub-only execution is sufficient and no live runtime is authorized
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
decomposition_reason: one bounded exact-current identity-preserving relay-edge discriminator from the promoted self-relay boundary
feature_scope:
  type: contract_producer
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
invocation_started_at: 2026-09-04T15:37:00+02:00
last_progress_at: 2026-09-04T15:37:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: initial_red
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
owned_paths:
  - .github/workflows/tibia-official-client-re-be4f48-queue-signal-bf-next-relay-edge.yml
  - tools/tibia_re_be4f48_queue_signal_bf_next_relay_edge/**
  - docs/agents/tasks/active/OTC-20260904-be4f48-queue-signal-bf-next-relay-edge.md
  - docs/agents/evidence/OTC-20260904-be4f48-queue-signal-bf-next-relay-edge/**
reuses:
  - promotion PR #891 / merge b4582b1e72d689b5d26fbd16c0ba2bbd20dca970
  - alias registration PR #893 / main 7e67c67783b19575ec7f378c7be49cb69d87f1ce
  - source PR #890 only for promoted receiver identity, SIGNAL_RELAY role, exact GameclientMessage pair and hosted workflow pattern
depends_on: []
blocks:
  - clean coordinator promotion before any Track B decision
last_completed_step: trusted-base preflight complete; no overlapping branch or open PR found; static no-runtime admission persisted
next_action: create repository-only RED contract and draft PR before implementing the analyzer
---

# Objective

Resolve exactly one next identity-preserving `clientMessageReadyToProcess` relay edge after the promoted self-relay. Start only from the already-promoted `tibia::protocol::TProtocolMessageQueue` sender/receiver identity, `SIGNAL_RELAY` classification, QSlot callable `0xbd2190`, and exact `GameclientMessage` shared pair.

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
QUEUE_SIGNAL_BODY=0xbd2190
QUEUE_SIGNAL_CONNECTIMPL_CALLSITE=0xbe2eee
QUEUE_SIGNAL_CONNECTIMPL_FDE=0xbe2a50..0xbe3086
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
```

Do not re-prove receiver RTTI/type from #890 or QSlot construction from #885.

# Bounded evidence rule

Allowed path only:

```text
promoted self-relay at connectImpl@0xbe2eee
  -> exact clientMessageReadyToProcess / GameclientMessage shared pair
  -> queue constructor/metaobject/connect context causally tied to that exact signal/pair
  -> at most one next unique identity-preserving relay edge
  -> exact endpoint type/callable if uniquely proven
```

Stop when the next relay edge or endpoint ceases to be unique. No global QObject/connect/QSlot/socket/TCP/writer census, no broad whole-executable generic xref discovery, no Track B mutation.

# TDD contract

The repository-only contract must fail before exact-client materialization while the analyzer is absent. After observing that RED, add the smallest bounded analyzer that can produce deterministic sanitized JSON. Raw official-client bytes remain transient and must be deleted before artifact upload.

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

# Required terminal schema

```text
EXACT_CLIENT_FENCE_PROVEN=true|false
QUEUE_SIGNAL=clientMessageReadyToProcess
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_RECEIVER_IDENTITY=tibia::protocol::TProtocolMessageQueue
QUEUE_SIGNAL_CONNECTION_ROLE=SIGNAL_RELAY
QSLOT_FUNCTION_TARGET=0xbd2190
NEXT_UNIQUE_RELAY_EDGE=<exact edge|UNKNOWN>
NEXT_ENDPOINT_IDENTITY=<exact type/callable|UNKNOWN>
NEXT_RELAY_IDENTITY_PRESERVED=true|false
QUEUE_SIGNAL_WRITER_IDENTITY=<value|UNKNOWN>
FINAL_QUEUE_WRITER_IDENTIFIED=true|false
FINAL_TCP_WRITER_IDENTIFIED=true|false
FINAL_WRITER_CONTRACT=<value|UNKNOWN>
FIELD6_VALUE=UNKNOWN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
terminal_result=<QUEUE_SIGNAL_BF_NEXT_RELAY_EDGE_PROVEN|SOURCE_BLOCKER>
FIRST_MISSING_BOUNDARY=<none|precise boundary>
NEXT_ACTION=<clean coordinator promotion or one newly admitted bounded source step>
```
