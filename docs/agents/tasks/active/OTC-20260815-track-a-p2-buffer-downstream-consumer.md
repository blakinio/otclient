---
task_id: OTC-20260815-track-a-p2-buffer-downstream-consumer
status: blocked
agent: unassigned
session_id: chatgpt-p2-hosted-resume-20260816-1317
session_role: researcher
session_rotation_count: 2
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: validation
phase: validate
branch: research/OTC-20260815-track-a-p2-buffer-downstream-consumer
base_branch: main
base_main: 0d7b2607912552599ae501891491aab439cfde7b
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-p2-buffer-downstream-consumer
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
related_pr: 310
created: 2026-08-15T21:40:00+02:00
updated: 2026-08-16T13:22:53+02:00
lease_expires_at: 2026-08-16T13:22:53+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-p2-buffer-downstream-consumer.md
  - docs/agents/evidence/OTC-20260815-track-a-p2-buffer-downstream-consumer/**
  - .github/workflows/tibia-official-client-re-p2-buffer-downstream-consumer.yml
  - .github/scripts/tibia-official-client-re-p2-buffer-downstream-consumer.py
modules_touched: []
reuses:
  - coordinator-promoted PR #308 exact retained QBuffer/QDataStream boundary
  - PR #310 run 31904696996 sanitized static artifact as historical discovery input only
  - PR #310 run 31904967728 exact-client failure log as historical discovery input only
depends_on:
  - main@0d7b2607912552599ae501891491aab439cfde7b
  - coordinator promotion of closed-unmerged PR #308 as pinned evidence only
blocks: []
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
track_a_runtime_agent_admission_version: 1
execution_mode: github-only
execution_reason: deterministic exact-build static ELF/disassembly validation on GitHub-hosted execution; no live client or retained Synology state is required or permitted
execution_class: github_hosted
runtime_access: none
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: false
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
owner_funded_ai_api_authorized: false
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: milestone_and_terminal
implementation_authorized: true
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_research_only
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one bounded P2 post-serialization chain question with one owned validator/workflow and no runtime dependency
validation_level: focused
invocation_started_at: 2026-08-16T13:07:00+02:00
last_progress_at: 2026-08-16T13:22:03+02:00
ci_checks_for_current_head: 0
ci_check_generation: blocked-checkpoint
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 1
stall_warnings: 0
heavy_validation_runs: 2
heavy_validation_result: blocked_before_semantic_validator
terminal_invocation_result: BLOCKED
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
historical_run_disposition:
  run_31904696996: sanitized_static_evidence_only_do_not_treat_as_current_execution
  run_31904967728: exact_client_static_failure_log_only_do_not_repeat_on_synology
  run_31944051248: QUARANTINED_ROUTING_VIOLATION_successful_static_synology_run_not_current_proof
  run_31944074222: HOSTED_INPUT_BLOCKED_download.tibia.com_DNS_unresolved
  run_31944119641: HOSTED_INPUT_BLOCKED_static.tibia.com_HTTP_403
  synology_static_rerun: FORBIDDEN_BY_CURRENT_ROUTING
known_validator_defect:
  marker: client_processor_ap_loaded
  failing_run: 31904967728
  first_actionable_error: GNU_objdump_rip_comment_contains_2f6a208_without_required_0x_prefix
  repair: accept the exact address token independent of the optional 0x presentation prefix
  repair_commit: 366085e6f6a65970b2132e491bd32bf6c05f51b7
hosted_input_policy:
  source: official Linux Tibia download endpoint only
  use: ephemeral read-only archive extraction and exact-fence static analysis
  execute_client: false
  persist_client_bytes: false
  upload_client_bytes: false
  exact_fence_required: true
  on_download_or_fence_mismatch: fail_closed_INPUT_BLOCKED_no_synology_fallback
hosted_attempts:
  count: 2
  exhausted_for_session: true
  first:
    run: 31944074222
    head: 85f6eee992ea8acc3d0dbe9e7088e156a64fdfcd
    job: 95157361223
    runner: github_hosted_ubuntu_24_04
    runtime_access: none
    result: INPUT_BLOCKED
    first_actionable_error: download.tibia.com_DNS_resolution_failed
    artifact: 9262801026
  second:
    run: 31944119641
    head: 61b84f4a770dfcb130511ca89e335f0e2f23fd2c
    job: 95157468020
    runner: github_hosted_ubuntu_24_04
    runtime_access: none
    result: INPUT_BLOCKED
    first_actionable_error: static.tibia.com_returned_HTTP_403
    artifact: 9262812558
    proprietary_input_cleanup: PASS
current_compliant_result:
  exact_binary_materialized: false
  semantic_validator_ran: false
  first_downstream_consumer: UNKNOWN
  protocol_stage_order: UNKNOWN
  framing: UNKNOWN
  sequence: UNKNOWN
  compression: UNKNOWN
  encryption: UNKNOWN
  final_binary_egress: UNKNOWN
blocker:
  type: INPUT_BLOCKED
  execution_class: github_hosted
  runtime_access: none
  validated_experiment_head: 61b84f4a770dfcb130511ca89e335f0e2f23fd2c
  run: 31944119641
  job: 95157468020
  exact_failure: official_native_Linux_archive_static.tibia.com_returned_HTTP_403_to_GitHub_hosted_runner
  previous_attempt: download.tibia.com_DNS_resolution_failed_on_GitHub_hosted_runner
  exact_binary_materialized: false
  semantic_validator_ran: false
  synology_fallback_allowed: false
  repair_budget_exhausted: true
e2e:
  result: NOT_APPLICABLE
  reason: static reverse-engineering validation only; no live/client runtime behavior changed or authorized
audit:
  result: NOT_TERMINAL_COMPLETION_AUDIT
  material_findings_open: 0
  notes:
    - compliant hosted attempts preserved runtime_access none and did not execute the client
    - exact client/package bytes were not uploaded by the compliant hosted attempts
    - run 31944051248 is explicitly quarantined and cannot be used as current routing-compliant proof
active_operation: stopped after the second permitted GitHub-hosted exact-input materialization attempt failed closed before semantic analysis
last_completed_step: second and final permitted hosted attempt 31944119641 passed the hosted/no-runtime boundary, received HTTP 403 while materializing the official Linux archive, removed any temporary proprietary input, and uploaded sanitized blocker artifact 9262812558
next_action: coordinator must provide or approve a legally and technically compliant GitHub-hosted-readable staging source for the exact fenced native-Linux client, without Synology execution or runtime access, then redispatch this same validator from current main
---

# Objective

Start from the coordinator-promoted P2 boundary:

```text
TProtocolClientMessageProcessor
  -> retained intermediate AP 0x2f69e30 / RTTI 0x3080748
  -> retained TProtocolWriter AP 0x2f69dd0 / RTTI 0x3080728
  -> retained helper 0x1960340 / TIODeviceWriter AP 0x2f69d48
  -> retained QDataStream serialization
  -> persistent QBuffer-backed QIODevice byte container
```

Recover the **first exact downstream consumer or transform** of that retained byte-container state toward framing/final binary egress. Distinguish concrete data flow from lifecycle adjacency.

This resumed dispatch is static-only and GitHub-hosted. It must not touch a running client, canonical runtime, VNC/display, login/session state, retained Synology package paths or Synology runner execution.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
execution_class: github_hosted
runtime_access: none
```

The hosted job may consume only an ephemeral official Linux download. It must verify size and SHA-256 before semantic analysis, must never execute the client, and must never upload client/package bytes. If the exact fenced build is not legally and technically obtainable on GitHub-hosted execution, the result is `INPUT_BLOCKED`; it is not permission to use Synology.

# Pinned promoted facts

- helper `0x1960340` binds supplied QIODevice shared pair to QDataStream and retains device at `+0x8/+0x10`, stream at `+0x18/+0x20`;
- persistent QBuffer pair is passed to that helper and helper is retained at `TProtocolWriter+0x18/+0x20`;
- retained writer is retained by intermediate, which is retained by `TProtocolClientMessageProcessor`;
- serializer slots `0xc10960` and `0xc20290` use the retained QDataStream;
- local QBuffer slot `0xc20c70` proves QBuffer-backed serialization/exposure;
- only local object lifecycle order was coordinator-promoted by predecessor #308.

# Historical #310 evidence boundary

Run `31904967728` directly verified the exact client fence and all checks through `client_processor_actual_object_pointer`, then failed on `client_processor_ap_loaded`. The validator required literal `0x2f6a208` in an objdump instruction line even though GNU objdump's RIP-relative comment target can emit the same exact address as `2f6a208` without a mandatory `0x` prefix. Commit `366085e6f6a65970b2132e491bd32bf6c05f51b7` repairs only that presentation-sensitive assertion.

Run `31944051248` subsequently completed the static validator under the stale pre-routing Synology workflow. Because current policy and owner direction require GitHub-hosted execution for this deterministic task, that success is quarantined as a routing violation and is not accepted as current proof.

The two compliant hosted attempts did not reach semantic analysis. Run `31944074222` failed closed because `download.tibia.com` could not be resolved; after one evidence-based endpoint repair, run `31944119641` reached `static.tibia.com` but received HTTP 403. The second attempt then removed temporary proprietary input and uploaded only sanitized blocker evidence. The session's two-full-attempt budget is exhausted.

# Acceptance boundary

A positive downstream claim requires exact type/member provenance plus a concrete read/call/data-flow edge from the retained QBuffer/helper/writer state into the candidate transform/consumer. A symbol-name hit, generic Qt/QBuffer census, vtable adjacency, unrelated local QBuffer use, historical final-socket observation, quarantined routing-violating execution, or passing workflow without the exact client fence is insufficient.

Until a routing-compliant hosted run materializes and verifies the exact fenced binary, the current task does not promote a new downstream semantic claim. Current compliant classifications remain:

```yaml
first_downstream_consumer: UNKNOWN
protocol_stage_order: UNKNOWN
framing: UNKNOWN
sequence: UNKNOWN
compression: UNKNOWN
encryption: UNKNOWN
final_binary_egress: UNKNOWN
```

# Forbidden shortcuts

Do not use:
- generic QIODevice/QBuffer/QByteArray callsite census as proof;
- vtable adjacency as temporal order;
- historical final-socket run `31825417040` as proof;
- stale/superseded sink models;
- unproven direct DualConnection writer ownership;
- live traffic, credentials, login, attach, gameplay or account state;
- Synology/self-hosted execution for this deterministic static task;
- a third full hosted attempt in this invocation after the two-attempt budget is exhausted;
- owner-funded Codex/OpenAI API capacity.

Research stays Draft-only; coordinator owns promotion.