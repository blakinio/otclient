---
task_id: OTC-20260904-be4f48-sendlogin-owner-edge-7e8f30-identity
status: ready
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: integrate
branch: research/OTC-20260904-be4f48-sendlogin-owner-edge-7e8f30-identity
base_branch: main
base_main: 7e67c67783b19575ec7f378c7be49cb69d87f1ce
created: 2026-09-04T15:44:00+02:00
updated_at: 2026-09-04T16:01:00+02:00
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
context_score: 7
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one exact-current callee-local owner identity discriminator with one static analysis workflow
owned_paths:
  - .github/workflows/tibia-official-client-re-be4f48-sendlogin-owner-edge-7e8f30-identity.yml
  - tools/tibia_re_be4f48_sendlogin_owner_edge_7e8f30_identity/**
  - docs/agents/tasks/active/OTC-20260904-be4f48-sendlogin-owner-edge-7e8f30-identity.md
  - docs/agents/evidence/OTC-20260904-be4f48-sendlogin-owner-edge-7e8f30-identity/**
modules_touched: []
reuses:
  - coordinator promotion #891 / merge b4582b1e72d689b5d26fbd16c0ba2bbd20dca970
  - archive #892 / merge 58cc12558babcfcadaa89bbdc49ca19ee1e58e5e
  - alias registration #893 / main 7e67c67783b19575ec7f378c7be49cb69d87f1ce
  - closed source PR #889 only as consumed sanitized evidence and generic analyzer/workflow pattern; its owner-FDE scan is not repeated
depends_on: []
blocks:
  - clean coordinator consumption before any newly admitted Track A step or Track B decision
red_head: 684e301ada1feef6590fc59b3375a19c547f16a8
red_run: 33879930241
red_job: 101045813815
red_result: expected_failure_before_client_materialization
red_first_error: "AssertionError: edge_identity.py is missing: expected RED before client materialization"
tdd_red_verified: true
green_implementation_commit: 9c68d92657100b054c6d5006ab46ddc5303112ee
source_head: 9c68d92657100b054c6d5006ab46ddc5303112ee
source_run: 33880393758
source_job: 101047349555
source_result: success
source_artifact_id: 9939610461
source_artifact_digest: sha256:ae15b1091e72ca4a4ae5eb970fe91695189f2248582a6519286660a03d646877
scientific_terminal_result: SOURCE_BLOCKER
first_missing_boundary: CALLEE_INTERNAL_IDENTITY_EDGE_NOT_FOUND
owner_edge_callsite: 0x7c67b8
owner_edge_callee: 0x7e8f30
owner_edge_callee_fde: 0x7e8f30..0x7f06d6
owner_object_identity: UNKNOWN
owner_object_identity_proven: false
owner_identity_proof_classes: []
sendlogin_receiver_identity: UNKNOWN
sendlogin_receiver_identity_proven: false
complete_sender_receiver_pair_proven: false
sendlogin_causal_binding_proven: false
pre_success_send_sequence: UNKNOWN
field6_value: UNKNOWN
e2e_result: NOT_APPLICABLE
e2e_reason: source-only static discriminator; official-client execution and official-service E2E are explicitly forbidden
audit_result: pass
audit_independent: false
audit_material_findings_open: 0
audit_evidence: docs/agents/evidence/OTC-20260904-be4f48-sendlogin-owner-edge-7e8f30-identity/20260904-whole-diff-falsification.md
qualification_head: e1cb7e3f981a4176048ea0d67f021745dc63c8f3
qualification_source_run: 33880858875
qualification_source_job: 101048892758
qualification_source_artifact_id: 9939805366
qualification_source_artifact_digest: sha256:dc2fe4c16fd7241ad21e996beeb392055db81e49c1ce1158bfadbcfd163b657b
qualification_ci_run: 33880859518
qualification_governance_run: 33880858844
qualification_self_hosted_boundary_run: 33880859027
qualification_result: pass
review_threads_open: 0
last_completed_step: exact-head qualification on e1cb7e3f981a4176048ea0d67f021745dc63c8f3 passed task-specific source, CI, Track A governance and self-hosted boundary and reproduced the same terminal SOURCE_BLOCKER
next_action: clean coordinator consumption of this terminal negative evidence; do not widen this worker
recovery:
  policy_version: 1
  generation: 5
  session_id: chat-github-20260904T153700+0200
  session_started_at: 2026-09-04T15:37:00+02:00
  checkpointed_at: 2026-09-04T16:01:00+02:00
  last_progress_at: 2026-09-04T16:01:00+02:00
  phase: integrate
  exact_head: HEAD_CONTAINS_QUALIFICATION_METADATA_ONLY
  pull_request: 894
  active_operation: none
  external_run_ids: [33880858875, 33880859518, 33880858844, 33880859027]
  operation_started_at: null
  wait_deadline_at: null
  check_generation: qualification_metadata_only
  checks_used: 0
  status: ready
  safe_to_resume: true
  resume_condition: clean coordinator is ready to consume PR #894 evidence
  next_action: consume the terminal SOURCE_BLOCKER in a clean coordinator; any further source step requires a newly admitted bounded task
---

# Objective

Resolve only the exact identity semantics of the promoted owner-bound edge `0x7c67b8 -> 0x7e8f30`, carrying the same `ENTRY_ARG:rdi` owner object. Analysis is restricted to the callee FDE and at most one unique identity-preserving internal edge; #884 caller discovery, #889 owner-FDE scanning and global constructor/RTTI/QMeta/QObject/vtable/`+0x88` censuses are forbidden.

# Exact fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

# Terminal scientific result

```text
EXACT_CLIENT_FENCE_PROVEN=true
OWNER_EDGE_CALLSITE=0x7c67b8
OWNER_EDGE_CALLEE=0x7e8f30
OWNER_EDGE_CALLEE_FDE=0x7e8f30..0x7f06d6
OWNER_OBJECT_IDENTITY=UNKNOWN
OWNER_OBJECT_IDENTITY_PROVEN=false
OWNER_IDENTITY_PROOF_CLASSES=[]
SENDLOGIN_RECEIVER_PROVENANCE=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
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
FIRST_MISSING_BOUNDARY=CALLEE_INTERNAL_IDENTITY_EDGE_NOT_FOUND
```

Inside only `0x7e8f30..0x7f06d6`, no vptr/Itanium RTTI event was tied to the carried `ENTRY_ARG:rdi`, no same-object external constructor/metaobject call was present, and no admissible same-object direct internal edge candidate existed. Therefore no internal edge was followed and the owner identity remains fail-closed `UNKNOWN`.

# Validation

Repository-only RED: head `684e301ada1feef6590fc59b3375a19c547f16a8`, run `33879930241`, job `101045813815`; failed exactly because `edge_identity.py` was absent, with all WARP/client-materialization steps skipped.

Scientific GREEN/source evidence: head `9c68d92657100b054c6d5006ab46ddc5303112ee`, run `33880393758`, job `101047349555`, artifact `9939610461`, digest `sha256:ae15b1091e72ca4a4ae5eb970fe91695189f2248582a6519286660a03d646877`.

Exact-head qualification on `e1cb7e3f981a4176048ea0d67f021745dc63c8f3`:

```text
TASK_SOURCE_RUN=33880858875 PASS
CI_RUN=33880859518 PASS
TRACK_A_GOVERNANCE_RUN=33880858844 PASS
SELF_HOSTED_BOUNDARY_RUN=33880859027 PASS
QUALIFICATION_ARTIFACT=9939805366
QUALIFICATION_ARTIFACT_DIGEST=sha256:dc2fe4c16fd7241ad21e996beeb392055db81e49c1ce1158bfadbcfd163b657b
```

The qualification source run reproduced the same `SOURCE_BLOCKER`, exact fence PASS, sanitized result PASS and `RAW_CLIENT_RETAINED=false`.

The subsequent qualification-metadata compaction was rejected once by Track A governance because mandatory `runtime_access: none` admission companion fields were omitted. This checkpoint restores those exact static/no-runtime fields; no analyzer, workflow or scientific evidence changed in that repair.

# Audit and safety

Whole-diff falsification at `docs/agents/evidence/OTC-20260904-be4f48-sendlogin-owner-edge-7e8f30-identity/20260904-whole-diff-falsification.md` is `PASS` with zero material findings. It is not coordinator promotion.

No official-client execution, login, credential/session access, process-memory access, packet capture, OCR/Vision, official-service E2E, runtime Field6 observation, queue/QSlot/writer work or Track B #284 mutation occurred. Field6 and pre-success order remain `UNKNOWN`.

# Terminal disposition

The exact callee identity question is scientifically terminal as `SOURCE_BLOCKER`. PR #894 remains Draft intentionally for clean coordinator consumption and must not self-merge. Any continuation beyond this boundary requires a newly admitted bounded task from that coordinator.
