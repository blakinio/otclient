---
task_id: OTC-20260904-be4f48-sendlogin-receiver-field-88-use-semantics
status: implementing
agent: ChatGPT
session_id: chat-github-20260904T165603+0200
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: implement
branch: ai/OTC-20260904-be4f48-sendlogin-receiver-field-88-use-semantics
base_branch: main
base_main: 73bf55043e1a46732b30fd0be537742b0ac6fed9
created: 2026-09-04T16:56:03+02:00
updated_at: 2026-09-04T16:56:03+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
execution_reason: user declined Work handoff; trusted-main GITHUB_ONLY_EXECUTION permits GitHub connector plus GitHub-hosted Actions for deterministic static Track A analysis
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
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
decomposition_reason: one exact-current receiver-field-value use/type discriminator with one bounded source-analysis workflow
invocation_started_at: 2026-09-04T16:49:00+02:00
last_progress_at: 2026-09-04T16:56:03+02:00
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
  - .github/workflows/tibia-official-client-re-be4f48-sendlogin-receiver-field-88-use-semantics.yml
  - tools/tibia_re_be4f48_sendlogin_receiver_field_88_use_semantics/**
  - docs/agents/tasks/active/OTC-20260904-be4f48-sendlogin-receiver-field-88-use-semantics.md
  - docs/agents/evidence/OTC-20260904-be4f48-sendlogin-receiver-field-88-use-semantics/**
modules_touched: []
reuses:
  - coordinator promotion #896 / merge 71e1af0db234a4011689e51bdbcc0ee7d9ee97c8
  - archive #897 / merge 5bedd83b38b276f5b7691f7efe2ef5f91611f42f
  - alias registration #898 / main 73bf55043e1a46732b30fd0be537742b0ac6fed9
  - closed source PR #879 only as consumed stack-aware connectImpl receiver-provenance evidence and generic workflow pattern; no predecessor owner/caller/type scan is repeated
depends_on: []
blocks:
  - clean coordinator promotion after this source discriminator becomes scientifically terminal
cross_repository_task_ids: []
e2e_result: NOT_APPLICABLE
e2e_reason: source-only static discriminator; the exact task contract forbids official-client execution and official-service E2E
last_completed_step: trusted-main authority, exact alias, no-overlap state, source-only runtime admission and bounded predecessor evidence were refreshed
next_action: commit repository-only contract test and workflow without the analyzer, open Draft PR, and verify expected RED before any client materialization
---

# Objective

Starting only from the promoted `sendLogin` connection at `QObject::connectImpl@0x7c6b9f` and receiver provenance `OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]`, determine whether the exact loaded field value has uniquely provable immediate use semantics and, at most, one uniquely object-tied type/QMeta/vptr edge.

# Exact fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

# Promoted starting facts

```text
SENDLOGIN_SENDER_IDENTITY=tibia::authentication::TLoginProtocolMessageHandler
SENDLOGIN_SIGNAL=sendLoginMessage
SENDLOGIN_CONNECTIMPL_CALLSITE=0x7c6b9f
SENDLOGIN_ADAPTER_TARGET=0xbd3050
SENDLOGIN_RECEIVER_PROVENANCE=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
SENDLOGIN_RECEIVER_IDENTITY=UNKNOWN
SENDLOGIN_CAUSAL_BINDING_PROVEN=false
OWNER_EDGE=0x7c67b8->0x7e8f30
OWNER_OBJECT_IDENTITY=UNKNOWN
OWNER/CALLEE_IDENTITY_PATHS_EXHAUSTED=true
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
```

# Bounded implementation contract

Admitted path only:

```text
sendLogin connectImpl@0x7c6b9f
  -> exact stack-aware receiver argument handoff
  -> exact receiver field value loaded from [entry-rdi-derived-rbx+0x88]
  -> immediate field-value use semantics
  -> at most one unique object-tied type/QMeta/vptr edge
```

Stop at the first non-unique field-value use or type edge. Do not redo PR #884 caller discovery, PR #889 owner-FDE type analysis or PR #894 `0x7e8f30` identity analysis. Do not perform a global `+0x88`, RTTI, QMeta, QObject or vtable census. Do not enter queue/QSlot/writer scope or mutate Track B PR #284.

# TDD state

Repository-only RED is required before the analyzer exists or any exact client bytes are materialized. The RED workflow must fail on the missing analyzer in its first repository-only step; every WARP/package/client step must therefore be skipped. Only after that failure is observed may the minimal analyzer be added.

# Required terminal report

```text
EXACT_CLIENT_FENCE_PROVEN=true|false
SENDLOGIN_CONNECTIMPL_CALLSITE=0x7c6b9f
SENDLOGIN_RECEIVER_PROVENANCE=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
RECEIVER_FIELD_VALUE_USE=<exact bounded description|UNKNOWN>
RECEIVER_FIELD_VALUE_USE_PROVEN=true|false
SENDLOGIN_RECEIVER_IDENTITY=<value|UNKNOWN>
SENDLOGIN_RECEIVER_IDENTITY_PROVEN=true|false
COMPLETE_SENDER_RECEIVER_PAIR_PROVEN=true|false
SENDLOGIN_CAUSAL_BINDING_PROVEN=true|false
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
terminal_result=<SENDLOGIN_RECEIVER_FIELD_USE_IDENTITY_PROVEN|SOURCE_BLOCKER>
FIRST_MISSING_BOUNDARY=<none|precise boundary>
NEXT_ACTION=<clean coordinator promotion or one newly admitted bounded step>
```

# Safety

No official-client execution, login, credential/session/cookie/character/world access, process-memory access, packet capture, OCR/Vision, official-service E2E, runtime Field6 observation or Track B mutation. Static deterministic analysis runs on GitHub-hosted infrastructure with transient exact client bytes deleted before the sanitized result artifact is uploaded.