---
task_id: OTC-20260905-fast-login-serializer
status: ready
agent: Codex
session_id: astra-fast-login-20260905
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: implementation
phase: design
branch: ai/OTC-20260905-fast-login-serializer
base_branch: main
base_main: bca9df65c4cf42f02216402dc12ade84548c5858
policy_version: 2
prompting_standard_version: 2.1
execution_mode: codex
execution_reason: bounded source analysis and local synthetic tests, hosted exact-client qualification
execution_class: github_hosted
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
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one type-owned serializer-to-buffer discriminator
foreground_runtime_budget_minutes: 120
foreground_budget_reason: bounded source qualification and independently reviewed promotion/archive
max_new_static_source_tasks: 3
static_source_tasks_used: 0
static_source_budget_reason: explicit owner FAST TRACK invocation; registration is not a scientific source task
ci_checks_for_current_head: 0
ci_check_generation: registration
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
owned_paths:
  - docs/agents/tasks/active/OTC-20260905-fast-login-serializer.md
  - tools/tibia_re_fast_login_serializer/**
  - .github/workflows/track-a-fast-login-serializer.yml
  - docs/agents/evidence/OTC-20260905-fast-login-serializer/**
modules_touched: []
reuses:
  - source711 type-specific generated-message evidence as historical discovery only
  - source729 enclosing GameclientMessage evidence as historical discovery only
  - promoted source865 current producer provenance
  - promoted source874 exact queued GameclientMessage pair
depends_on: []
blocks: []
cross_repository_task_ids: []
next_action: independently validate and merge this docs-only registration, then create isolated source Draft with repository-only RED
---

# Exact-current login serializer plan

Owner FAST TRACK invocation authorizes at most three new high-value static source tasks,
sequentially, with clean promotion and separate archive between tasks. Stop early on an
implementable promoted wire delta. No fourth source. Runtime remains separately forbidden.

## Live evidence basis

Protected main bca9df65c4cf42f02216402dc12ade84548c5858 includes promotion952
b8c66514c542c22f332b408ac0c5d4327f69347c and the separate source951 archive.
Source951 final 0c8ab343124727c99224ad3050a5eb29d1a2f10f is closed unmerged;
its disqualified generations and repaired bounded CFG record are preserved.
Sources939/919 remain independently blocked with released ownership.
TrackB284 is open Draft at 62383aded3acbeb5f405a12fe1f93849cd8e35f9.
No TrackB changes or reruns are part of this source.

Fence: official native Linux 15.32.be4f48, size52105824,
SHA256552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1,
from docs/agents/contracts/TRACK_A_CURRENT_CLIENT_FENCE_V1.json.
Historical75d4a0 serializer facts are not current proof.

## Information-gain comparison

Recommendation scores are judgments, not measured results. Higher is preferable for
directness (D), information gain (I), boundedness (B), failure value (F), anti-loop (A).
E is estimated unproven intermediate edges; C is expected cost (low/medium/high).
Four independent proof options are scored; Qt is a supporting comparator.

| Option | D | I | E | B | F | C | A |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Serializer-first, two selected generated types to first buffer | 5 | 5 | 2-3 | 5 | 5 | medium | 5 |
| Writer-first, known frame consumer backward to selected payload | 5 | 4 | 3-5 | 3 | 4 | high | 4 |
| Field6 producer input, exact caller/owner | 5 | 4 | 2-4 | 4 | 4 | high | 3 |
| Concrete pre-success builder/send ordering | 4 | 3 | 3-5 | 3 | 4 | high | 4 |
| Qt frontier continuation (support only) | 1 | 1 | unknown | 4 | 2 | medium | 1 |

Choose serializer-first: the two exact type identities supply a bounded discriminator,
and even failure identifies whether generated output or downstream buffer ownership is
the first missing edge. Do not continue951's tail targets in this task.

## Bounded design and acceptance

Question: can the selected generated GameclientMessageLogin and enclosing
GameclientMessage serializers be independently resolved on the current fence and tied
to their first concrete serialized output buffer/length?

Reuse type-specific RTTI/vtable discovery, independently checked ByteSize and
serialization behavior. Restrict body analysis to the two selected types and a uniquely
selected immediate serialization helper/callsite. No protobuf-wide census, broad socket
sweep, Qt internal succession, historical-offset promotion, or full subsystem framework.

Positive facts require exact owner and buffer/length dataflow. A shared object pointer
or class name alone is not proof that bytes have been serialized. Unsupported control,
ABI, alias, partial-register or memory effects stop semantic propagation and retain
UNKNOWN. Never infer return from a call, trap fallthrough or object identity from adjacency.

## Execution sequence

- [ ] Merge independently audited docs-only registration with exact-head checks.
- [ ] Fresh live authority/overlap read; isolated source branch and early Draft.
- [ ] Repository-only RED for exact type selection, unique mapping, bounded decode,
      serializer input/output provenance and ambiguity rejection; no client acquisition.
- [ ] Minimal GREEN analyzer; inherited code only after its assumptions are audited.
- [ ] Hosted strict-fence qualification, deterministic sanitized JSON, raw cleanup.
- [ ] For any material analyzer defect: disqualify, regression RED, repair GREEN,
      fresh qualification. Maximum three repair cycles per gate.
- [ ] Independent exact whole-diff and scientific falsification; focused CI,
      governance and self-hosted boundary checks on the final source head.
- [ ] Source remains Draft/unmerged. Clean docs-only promotion from fresh main,
      exact checks, expected-head squash, close source unmerged consumed.
- [ ] Separate archive/release; publish matrix and rescore next source.

## Initial matrix and non-claims

LOGIN_SERIALIZER=UNKNOWN (current exact requalification pending)
SERIALIZER_OUTPUT=UNKNOWN
FRAME_CONTRACT=UNKNOWN (historical transport facts do not transfer)
FINAL_QUEUE_WRITER=UNKNOWN
FINAL_TCP_WRITER=UNKNOWN
FINAL_WRITER_CONTRACT=UNKNOWN
FIELD6_VALUE=UNKNOWN
FIELD6_SEMANTICS=UNKNOWN
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
TRACK_B_AUTHORIZED=false

runtime_access=none; official_client_executed=false; login_performed=false;
credentials_used=false; process_memory_access=false; packet_capture=false;
ocr_vision_used=false; official_service_e2e_count=0.
E2E=NOT_APPLICABLE for this static source; no login compatibility claimed.
