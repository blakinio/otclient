---
task_id: OTC-20260904-be4f48-post904-promotion
status: validating
agent: Codex
session_id: login-closure-20260904-ae070f034ee4
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: validate
branch: docs/OTC-20260904-be4f48-post904-promotion
base_branch: main
base_main: 04a4ca71b658dcc374aaf40dbb8135de43d49cb7
created: 2026-09-04T22:06:00Z
updated_at: 2026-09-04T22:25:59Z
invocation_started_at: 2026-09-04T22:06:00Z
last_progress_at: 2026-09-04T22:25:59Z
policy_version: 2
prompting_standard_version: 2.1
execution_mode: codex
execution_reason: isolated checkout and deterministic local tests; exact client qualification on GitHub-hosted runner
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
implementation_authorized: false
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
decomposition_reason: one connection construction and one adapter/member boundary
foreground_runtime_budget_minutes: 120
foreground_budget_reason: explicit sequential source qualification and clean promotion/archive programme
ci_checks_for_current_head: 0
ci_check_generation: final_source_qualification
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
owned_paths:
  - docs/agents/evidence/OTC-20260904-be4f48-post904-promotion/**
  - docs/agents/tasks/active/OTC-20260904-be4f48-post904-promotion.md
modules_touched: []
reuses:
  - docs/agents/prompts/OTC_BE4F48_SENDLOGIN_ADAPTER_BD3050_RECEIVER_SEMANTICS.md
  - docs/agents/evidence/OTC-20260904-be4f48-post899-900-promotion/result.json
  - PR 899 transient hosted qualification pattern (not its consumed type scan)
depends_on: []
blocks:
  - clean coordinator consumption of this exact source result
cross_repository_task_ids: []
ownership_released: false
next_action: exact-head CI/governance and independent whole-diff review, expected-head squash, source close unmerged, separate archive
---

# Coordinator promotion of source PR #904

Trusted main: 04a4ca71b658dcc374aaf40dbb8135de43d49cb7. Protected main ruleset18840974 active; squash-only, CI / Required, resolved threads, no bypass.

Source PR904 head 191a8ff86f1b354d313a95e6901e9c7abcd389d8; analyzer/tests/workflow scientific head4d7669970b4dc54829e29887ae6d60c76b73579b. Exact fence15.32.be4f48 /52105824 /552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1 requalified on final head.

## FACT

Selected connection at0x7c6b9f constructs QSlot dispatcher0x7c4f10 with member pair{0xbd3050,0}. Given operation edi=1 and the constructed slot in rsi, entry rdx reaches adapter rdi unchanged, and [entry rcx+8] reaches adapter rsi. This is conditional invocation ABI, not evidence of external Qt's receiver argument selection.

Under the analyzer's modeled normal returning paths, adapter0xbd3050 reaches its first same-entry-receiver edge at0xbd31e4, target load64(add(load64(arg:rdi),0x68)). No concrete dynamic vptr or member implementation is identified.

The selected QObject::connectImpl symbol is an undefined dynamic import in this executable. This does not establish absence of all Qt implementation code.

## INFERENCE

Connecting this conditional invocation to the proven +0x88 registered receiver requires an exact deployed-Qt registration-to-invocation proof. A generic/historical Qt ABI description is insufficient. A resolved vptr/member also requires a distinct identity-preserving proof.

## UNKNOWN

Receiver class/identity, complete sender-receiver pair and causal binding remain unproven. Queue endpoint, final queue/TCP writer, writer contract, Field6 value and pre-success ordering remain UNKNOWN. TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN; PR284 unchanged at62383aded3acbeb5f405a12fe1f93849cd8e35f9. No implementation or E2E unlocked.

terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=CURRENT_QT_REGISTERED_RECEIVER_TO_QSLOT_ENTRY_RDX_NOT_PROVEN

## Independent coordinator falsification

Coordinator independently read the complete analyzer, result and diff; rejected equating the imported connection receiver with the conditional QSlot input, equating vptr+0x68 with a concrete writer, and treating analysis incompleteness as a scientific blocker. Independent Codex reviewer /root/adapter_review reproduced and rechecked five regressions: width/partial writes, call memory/SIMD clobbers, unsupported loops, all-path coverage, signed-immediate comparisons. All resolved;18 synthetic tests pass. Exact final evidence-head independent review PASS,0 material findings. No raw official bytes retained.

Final source qualification: focused33925815752/job101193970658; CI33925815918; governance33925815751; boundary33925815793, all SUCCESS. Persisted source JSON exactly matches the final qualification output, reviewed without JS numeric reserialization. Earlier scientific artifact9956642316 digest sha256:d3038c3a89f4490c3a9d37f0dd6109ce810cb09d81783bada18c153c83199ae3.

## Lifecycle and continuation

Source PR904 remains Draft until this clean docs-only promotion merges, then closes unmerged as consumed. Its active record lives only on its source branch; archive closeout must import an explicitly labelled historical source record, not pretend it existed on main. This coordinator active task is moved to archive in a separate PR with ownership_released:true. No source analyzer/workflow is promoted.

After archive, execute existing canonical alias OTC-BE4F48-QUEUE-SIGNAL-BF-QMETA-INDEX-CONNECTION sequentially. No duplication of consumed adapter or body/name scans. SOURCE_BLOCKER is task-local and does not exhaust static proof classes or end the login programme.

runtime_access=none; official_client_executed=false; login_performed=false; credentials_used=false; process_memory_access=false; packet_capture=false; ocr_vision_used=false; official_service_e2e_count=0; track_b_pr_284_modified=false.
