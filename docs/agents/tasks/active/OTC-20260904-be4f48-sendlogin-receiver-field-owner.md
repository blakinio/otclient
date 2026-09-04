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
updated_at: 2026-09-04T13:10:00+02:00
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
decomposition_reason: one bounded static field-owner discriminator with one exact-current analysis workflow
invocation_started_at: 2026-09-04T12:52:00+02:00
last_progress_at: 2026-09-04T13:10:00+02:00
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
green_implementation_commit: bb39f99c8188ec5166eb95b868cfcecfcd9951bf
source_head: 29d30b7de6a59bfa0a40c619abfbf3f3061692e1
source_merge_ref_sha: d239e42d62b1a778873cd4e2df58b7478528307c
source_run: 33866338005
source_job: 101001945445
source_result: success
source_artifact_id: 9934120718
source_artifact_digest: sha256:2a8313249628076f1daef8766ac07ae6adf4fdc72e5f232f6b955ceaa4b62614
source_ci_run: 33866338387
source_ci_result: success
source_governance_run: 33866337998
source_governance_result: success
source_self_hosted_boundary_run: 33866338017
source_self_hosted_boundary_result: success
scientific_terminal_result: SOURCE_BLOCKER
first_missing_boundary: CONNECTION_OWNER_FDE_DIRECT_CALLER_NOT_UNIQUE
receiver_field_definition_site: UNKNOWN
receiver_owner_chain: UNKNOWN
receiver_endpoint_identity: UNKNOWN
receiver_identity_proven: false
complete_sender_receiver_pair_proven: false
sendlogin_causal_binding_proven: false
pre_success_send_sequence: UNKNOWN
field6_value: UNKNOWN
e2e_result: NOT_APPLICABLE
e2e_reason: source-only static discriminator; official-client execution and official-service E2E are explicitly forbidden
audit_result: pending
last_completed_step: exact-current source run completed on the admitted analyzer and returned SOURCE_BLOCKER because the bounded direct-caller edge from connection-owner FDE 0x7c6700..0x7cc933 has zero candidates; sanitized terminal evidence is now being persisted
next_action: perform fresh whole-diff falsification and exact-head validation on the terminal-evidence head; if clean, mark this source task ready for coordinator promotion without broadening scope
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

# TDD

Repository-only RED is verified on head `e9e20394fc28bb5caa4332b0baf4458ef1445c9a`: workflow run `33865752388`, job `101000116304`, failed in the first contract step because `receiver_field_owner.py` was deliberately absent. WARP preparation, exact-client materialization, analysis and artifact upload were all skipped. Only after that expected RED was observed, the bounded analyzer was added in commit `bb39f99c8188ec5166eb95b868cfcecfcd9951bf`.

# Terminal source result

Exact-current source head `29d30b7de6a59bfa0a40c619abfbf3f3061692e1` completed the bounded analyzer:

```text
EXACT_CLIENT_FENCE_PROVEN=true
SENDLOGIN_RECEIVER_PROVENANCE=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
SENDLOGIN_RECEIVER_FIELD_DEFINITION=UNKNOWN
SENDLOGIN_RECEIVER_OWNER_CHAIN=UNKNOWN
SENDLOGIN_RECEIVER_IDENTITY=UNKNOWN
COMPLETE_SENDER_RECEIVER_PAIR_PROVEN=false
SENDLOGIN_CAUSAL_BINDING_PROVEN=false
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=CONNECTION_OWNER_FDE_DIRECT_CALLER_NOT_UNIQUE
```

The target-specific direct-caller xref for the promoted connection-owner FDE produced zero candidates. Under the bounded search rule, that is a terminal fail-closed boundary: this task does not widen into a global constructor, RTTI, QMeta, QObject, or `+0x88` census to manufacture an owner identity.

Exact run evidence:

```text
SOURCE_RUN=33866338005 success
SOURCE_JOB=101001945445 success
ARTIFACT_ID=9934120718
ARTIFACT_DIGEST=sha256:2a8313249628076f1daef8766ac07ae6adf4fdc72e5f232f6b955ceaa4b62614
CI_RUN=33866338387 success
GOVERNANCE_RUN=33866337998 success
SELF_HOSTED_BOUNDARY_RUN=33866338017 success
RAW_CLIENT_RETAINED=false
```

Durable evidence:

- `docs/agents/evidence/OTC-20260904-be4f48-sendlogin-receiver-field-owner/result.json`
- `docs/agents/evidence/OTC-20260904-be4f48-sendlogin-receiver-field-owner/20260904-source-result.md`

# Safety

Source-only static analysis. No official-client execution, login, credentials, process memory, packet capture, OCR/Vision, official-service E2E, runtime Field6 observation, Track B PR #284 mutation, or protocol rewrite.

# Acceptance / stop rule

The field-owner question is scientifically terminal at the first exact non-unique owner edge. Remaining work is only fresh whole-diff falsification, exact-head qualification, and clean coordinator promotion after the independent parallel QSlot lane has its own terminal durable result. This source task must not consume that lane's scope.
