---
task_id: OTC-20260904-be4f48-sendlogin-receiver-field-88-use-semantics
status: ready
agent: ChatGPT
session_id: chat-github-20260904T165603+0200
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: integrate
branch: ai/OTC-20260904-be4f48-sendlogin-receiver-field-88-use-semantics
base_branch: main
base_main: 73bf55043e1a46732b30fd0be537742b0ac6fed9
created: 2026-09-04T16:56:03+02:00
updated_at: 2026-09-04T17:13:30+02:00
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
last_progress_at: 2026-09-04T17:13:30+02:00
ci_checks_for_current_head: 0
ci_check_generation: final-exact-head-qualification-pending
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
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
red_head: f0d94c0e6a16dff41e8135bbd4a2700c70172cd6
red_run: 33886750137
red_job: 101068292328
red_result: expected_failure_before_client_materialization
red_first_error: "AssertionError: receiver_field_use_semantics.py is missing: expected RED before client materialization"
tdd_red_verified: true
first_green_head: 4c309fd088257d9f94fc6a0ecdaa316be0445030
first_green_run: 33887133223
first_green_job: 101069574567
first_green_result: rejected_by_self_falsification
first_green_rejection: generic ABI-register candidate admission falsely treated stale receiver in rcx at operator new(unsigned long)@0x7c6b5e as object-tied
regression_red_head: 0573a784ce3554345ea1c9730f664f95b17d5cd2
regression_red_run: 33887477954
regression_red_job: 101070712173
regression_red_result: expected_failure_before_client_materialization
regression_red_first_error: "AssertionError: missing receiver-field-use contract token: OBJECT_TIED_THIS_REGISTER = \"rdi\""
source_head: 9397bb9eb44c7566a789f6a310e20c0da7845923
source_run: 33887723682
source_job: 101071529772
source_result: success
source_artifact_id: 9942554299
source_artifact_digest: sha256:b9da2ed976d0fb93dcd84f337c71e8e2a5a963124abd61ae62e18cb4215e19ef
source_ci_run: 33887724009
source_ci_result: success
source_governance_run: 33887723710
source_governance_result: success
source_self_hosted_boundary_run: 33887723792
source_self_hosted_boundary_result: success
scientific_terminal_result: SOURCE_BLOCKER
first_missing_boundary: NO_UNIQUE_OBJECT_TIED_TYPE_EDGE_IN_EXACT_FIELD_VALUE_LIFETIME
receiver_field_load_site: 0x7c6b18
receiver_field_value_use: QOBJECT_CONNECTIMPL_RECEIVER_ARGUMENT
receiver_field_value_use_proven: true
sendlogin_receiver_identity: UNKNOWN
sendlogin_receiver_identity_proven: false
complete_sender_receiver_pair_proven: false
sendlogin_causal_binding_proven: false
pre_success_send_sequence: UNKNOWN
field6_value: UNKNOWN
e2e_result: NOT_APPLICABLE
e2e_reason: source-only static discriminator; the exact task contract forbids official-client execution and official-service E2E
audit_result: SELF_FALSIFICATION_PASS
audit_independent: false
audit_material_findings_open: 0
audit_evidence: docs/agents/evidence/OTC-20260904-be4f48-sendlogin-receiver-field-88-use-semantics/20260904-whole-diff-falsification.md
qualification_pre_audit_head: bb3f61b5739100578699cfa589e05990fb944261
last_completed_step: fresh whole-diff falsification found zero material findings, retained the proven receiver-use claim, and confirmed fail-closed identity at the first missing object-tied type edge
next_action: exact-head qualify this final source-task audit/checkpoint head; then clean coordinator promotion may consume PR #899 without widening this source lane
---

# Objective

Starting only from the promoted `sendLogin` connection at `QObject::connectImpl@0x7c6b9f` and receiver provenance `OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]`, determine whether the exact loaded field value has uniquely provable immediate use semantics and, at most, one uniquely object-tied type/QMeta/vptr edge.

# Exact fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

# Terminal source result

```text
EXACT_CLIENT_FENCE_PROVEN=true
SENDLOGIN_CONNECTIMPL_CALLSITE=0x7c6b9f
SENDLOGIN_RECEIVER_PROVENANCE=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
RECEIVER_FIELD_VALUE_USE=QOBJECT_CONNECTIMPL_RECEIVER_ARGUMENT
RECEIVER_FIELD_VALUE_USE_PROVEN=true
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
FIRST_MISSING_BOUNDARY=NO_UNIQUE_OBJECT_TIED_TYPE_EDGE_IN_EXACT_FIELD_VALUE_LIFETIME
```

The exact field value is loaded at `0x7c6b18`, preserved through the bounded stack-aware slice, and supplied in formal receiver register `rcx` to `QObject::connectImpl@0x7c6b9f`. The immediate use is therefore proven. After the regression repair, the exact field-value lifetime from `0x7c6b18` to `0x7c6b9f` contains zero admitted object-tied `this` or primary-vptr edges, so receiver class identity remains `UNKNOWN` and this source task stops at that first bounded missing edge.

# TDD and repair evidence

Initial RED:

```text
RED_HEAD=f0d94c0e6a16dff41e8135bbd4a2700c70172cd6
RED_RUN=33886750137
RED_JOB=101068292328
RESULT=expected failure before client materialization
```

The first implemented head `4c309fd088257d9f94fc6a0ecdaa316be0445030` / run `33887133223` / job `101069574567` completed technically but was scientifically rejected by self-falsification because generic ABI-register candidate admission manufactured an object-tied edge from stale `rcx` at `operator new(unsigned long)@0x7c6b5e`.

Regression RED:

```text
REGRESSION_RED_HEAD=0573a784ce3554345ea1c9730f664f95b17d5cd2
REGRESSION_RED_RUN=33887477954
REGRESSION_RED_JOB=101070712173
RESULT=expected failure before client materialization
```

Accepted repaired source evidence:

```text
SOURCE_HEAD=9397bb9eb44c7566a789f6a310e20c0da7845923
SOURCE_RUN=33887723682 success
SOURCE_JOB=101071529772 success
ARTIFACT_ID=9942554299
ARTIFACT_DIGEST=sha256:b9da2ed976d0fb93dcd84f337c71e8e2a5a963124abd61ae62e18cb4215e19ef
CI_RUN=33887724009 success
GOVERNANCE_RUN=33887723710 success
SELF_HOSTED_BOUNDARY_RUN=33887723792 success
RAW_CLIENT_RETAINED=false
```

Durable sanitized result: `docs/agents/evidence/OTC-20260904-be4f48-sendlogin-receiver-field-88-use-semantics/result.json`.
Run/repair narrative: `docs/agents/evidence/OTC-20260904-be4f48-sendlogin-receiver-field-88-use-semantics/source-qualification.md`.
Fresh whole-diff falsification: `docs/agents/evidence/OTC-20260904-be4f48-sendlogin-receiver-field-88-use-semantics/20260904-whole-diff-falsification.md` = `SELF_FALSIFICATION_PASS`, zero material findings. It is explicitly not represented as an independent closeout audit; independent lifecycle review belongs to the clean coordinator promotion.

# Safety

Source-only static analysis. No official-client execution, login, credentials, session/cookie/character/world access, process memory, packet capture, OCR/Vision, official-service E2E, runtime Field6 observation, Track B PR #284 mutation, or protocol rewrite. Exact client bytes were transient and removed before sanitized artifact upload.

# Lifecycle

This source lane is scientifically terminal and ready for coordinator consumption, not complete/archived. PR #899 remains Draft and must not self-merge. After exact-head qualification, the clean coordinator may promote only the sanitized terminal facts, then close this source PR unmerged as consumed. Track B remains unchanged.
