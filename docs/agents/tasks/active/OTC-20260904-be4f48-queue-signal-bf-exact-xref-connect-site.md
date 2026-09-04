---
task_id: OTC-20260904-be4f48-queue-signal-bf-exact-xref-connect-site
alias: OTC-BE4F48-QUEUE-SIGNAL-BF-EXACT-XREF-CONNECT-SITE
status: investigating
agent: ChatGPT
session_id: chatgpt-20260904T1649+0200
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: investigate
branch: ai/OTC-20260904-be4f48-queue-signal-bf-exact-xref-connect-site
base_branch: main
base_main: 73bf55043e1a46732b30fd0be537742b0ac6fed9
created: 2026-09-04T16:57:00+02:00
updated_at: 2026-09-04T16:57:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
execution_reason: exact-current source-only signal-reference discriminator; GitHub-hosted static analysis is sufficient and no live runtime is authorized
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
policy_version: 2
context_pressure: medium
context_growth: stable
context_score: 9
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one bounded exact-signal discriminator followed by at most one causally linked connect site and one endpoint identity edge
feature_scope:
  type: contract_producer
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
invocation_started_at: 2026-09-04T16:49:00+02:00
last_progress_at: 2026-09-04T16:57:00+02:00
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
  - .github/workflows/tibia-official-client-re-be4f48-queue-signal-bf-exact-xref-connect-site.yml
  - tools/tibia_re_be4f48_queue_signal_bf_exact_xref_connect_site/**
  - docs/agents/tasks/active/OTC-20260904-be4f48-queue-signal-bf-exact-xref-connect-site.md
  - docs/agents/evidence/OTC-20260904-be4f48-queue-signal-bf-exact-xref-connect-site/**
reuses:
  - coordinator promotion PR #896 / merge 71e1af0db234a4011689e51bdbcc0ee7d9ee97c8
  - archive PR #897 / merge 5bedd83b38b276f5b7691f7efe2ef5f91611f42f
  - alias registration PR #898 / main 73bf55043e1a46732b30fd0be537742b0ac6fed9
  - source PR #880 only for exact signal-body/metaobject derivation patterns
  - source PR #895 only for promoted queue receiver/self-relay facts and hidden-sret connectImpl ABI
consumes_parallel_task: false
depends_on: []
blocks:
  - clean coordinator promotion before any Track B protocol decision
last_completed_step: fresh-main authority, governance, promotion, ownership and no-overlap preflight completed
next_action: produce repository-only RED contract/workflow before adding the exact-signal analyzer
---

# Objective

Resolve the exact-current downstream `clientMessageReadyToProcess(0xbf)` connect site, if and only if an exact-signal-only reference discriminator proves exactly one causal `QObject::connectImpl` setup and at most one endpoint identity edge.

This task starts from the promoted signal identity/body and the already-proven `tibia::protocol::TProtocolMessageQueue` self-relay. It must not repeat constructor-local enumeration and must not become a generic QObject/connect/socket/writer census.

# Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

# Promoted starting facts

```text
QUEUE_SIGNAL=clientMessageReadyToProcess
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_BODY=0xbd2190
QUEUE_SIGNAL_ARGV1_IDENTITY=exact GameclientMessage shared pair
QUEUE_SIGNAL_RECEIVER_IDENTITY=tibia::protocol::TProtocolMessageQueue
QUEUE_SIGNAL_CONNECTION_ROLE=SIGNAL_RELAY
SELF_RELAY_CONNECTIMPL_CALLSITE=0xbe2eee
QSLOT_FUNCTION_TARGET=0xbd2190
QUEUE_CONSTRUCTOR_FDE=0xbe2a50..0xbe3086
DIRECT_CONNECTIMPL_CALLS_IN_CONSTRUCTOR=0xbe2e54,0xbe2eee
AFTER_SELF_RELAY_CONNECT_COUNT=0
ADDITIONAL_EXACT_SIGNAL_CANDIDATES_IN_CONSTRUCTOR=0
NEXT_UNIQUE_RELAY_EDGE=UNKNOWN
NEXT_ENDPOINT_IDENTITY=UNKNOWN
FINAL_WRITER_CONTRACT=UNKNOWN
FIELD6_VALUE=UNKNOWN
```

# Admission and safety

```yaml
track_id: official-client-re
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
```

Forbidden for this task: official-client execution, login, credentials/session use, process-memory access, packet capture, OCR/Vision, official-service E2E, runtime Field6 observation, Track B PR #284 mutation, generic executable-wide connect/QObject/QSlot/socket/writer census, and guessing endpoint/writer/Field6 semantics.

# TDD contract

1. Persist this ownership/admission record before material implementation.
2. Create a repository-only contract test and hosted workflow while the analyzer is absent.
3. Observe the expected RED failure before any exact-client materialization.
4. Add the smallest exact-signal-only analyzer that derives any static metaobject identity from the exact binary instead of assuming an analyzer constant.
5. Enforce the exact version/size/SHA fence, delete transient raw client bytes, and persist/upload only deterministic sanitized JSON.
6. Stop positive only on one uniquely proven downstream connect site and endpoint; otherwise preserve the first precise source blocker.

# Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 1
  session_id: chatgpt-20260904T1649+0200
  session_started_at: 2026-09-04T16:49:00+02:00
  checkpointed_at: 2026-09-04T16:57:00+02:00
  last_progress_at: 2026-09-04T16:57:00+02:00
  phase: investigate
  exact_head: task-record-commit-pending-resolution
  pull_request: none
  active_operation: none
  external_run_ids: []
  operation_started_at: null
  wait_deadline_at: null
  check_generation: draft
  checks_used: 0
  status: active
  safe_to_resume: true
  resume_condition: dedicated branch remains owned and no overlapping exact alias PR exists
  next_action: create repository-only RED contract/workflow without the production analyzer
```
