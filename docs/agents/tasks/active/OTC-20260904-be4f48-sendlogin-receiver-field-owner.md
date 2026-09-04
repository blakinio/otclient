---
task_id: OTC-20260904-be4f48-sendlogin-receiver-field-owner
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: investigate
branch: research/OTC-20260904-be4f48-sendlogin-receiver-field-owner
base_branch: main
base_main: e24462d72942d8381e1a468de84f16b60f1aa8c9
created: 2026-09-04T12:52:00+02:00
updated_at: 2026-09-04T12:52:00+02:00
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
last_completed_step: claimed isolated source-only task from trusted main
next_action: add repository-only RED contract and draft PR before any exact-client materialization
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

# Safety

Source-only static analysis. No official-client execution, login, credentials, process memory, packet capture, OCR/Vision, official-service E2E, runtime Field6 observation, Track B PR #284 mutation, or protocol rewrite.

# Acceptance / stop rule

Follow only the smallest identity-preserving owner/caller/constructor chain needed to reach the defining `+0x88` store. Stop at the first non-unique initializer/constructor edge and emit a precise `SOURCE_BLOCKER` rather than opening another analyzer family.
