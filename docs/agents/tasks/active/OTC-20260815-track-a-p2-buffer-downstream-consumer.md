---
task_id: OTC-20260815-track-a-p2-buffer-downstream-consumer
status: investigating
agent: ChatGPT
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
updated: 2026-08-16T13:17:33+02:00
lease_expires_at: 2026-08-16T14:02:33+02:00
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
last_progress_at: 2026-08-16T13:17:33+02:00
ci_checks_for_current_head: 0
ci_check_generation: hosted-redispatch
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
heavy_validation_runs: 0
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
historical_run_disposition:
  run_31904696996: sanitized_static_evidence_only_do_not_treat_as_current_execution
  run_31904967728: exact_client_static_failure_log_only_do_not_repeat_on_synology
  synology_static_rerun: FORBIDDEN_BY_CURRENT_ROUTING
known_validator_defect:
  marker: client_processor_ap_loaded
  failing_run: 31904967728
  first_actionable_error: GNU_objdump_rip_comment_contains_2f6a208_without_required_0x_prefix
  repair: accept the exact address token independent of the optional 0x presentation prefix
hosted_input_policy:
  source: official Linux Tibia download endpoint only
  use: ephemeral read-only archive extraction and exact-fence static analysis
  execute_client: false
  persist_client_bytes: false
  upload_client_bytes: false
  exact_fence_required: true
  on_download_or_fence_mismatch: fail_closed_INPUT_BLOCKED_no_synology_fallback
active_operation: refresh the stale P2 Draft to current hosted/no-runtime routing, repair the proven validator formatting defect, and rerun the exact static discriminator without touching canonical or Synology runtime state
next_action: replace the stale Synology workflow with an ubuntu-latest fail-closed official-artifact static validator, repair client_processor_ap_loaded matching, run once, and classify the first downstream consumer/transform without promoting framing or egress beyond evidence
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

The hosted job may consume only an ephemeral official Linux download. It must verify size and SHA-256 before semantic analysis, must never execute the client, and must never upload client/package bytes. If the exact fenced build is no longer obtainable from the official public endpoint, the result is `INPUT_BLOCKED`; it is not permission to use Synology.

# Pinned promoted facts

- helper `0x1960340` binds supplied QIODevice shared pair to QDataStream and retains device at `+0x8/+0x10`, stream at `+0x18/+0x20`;
- persistent QBuffer pair is passed to that helper and helper is retained at `TProtocolWriter+0x18/+0x20`;
- retained writer is retained by intermediate, which is retained by `TProtocolClientMessageProcessor`;
- serializer slots `0xc10960` and `0xc20290` use the retained QDataStream;
- local QBuffer slot `0xc20c70` proves QBuffer-backed serialization/exposure;
- only local object lifecycle order was coordinator-promoted by predecessor #308.

# Historical #310 evidence boundary

Run `31904967728` directly verified the exact client fence and all checks through `client_processor_actual_object_pointer`, then failed on `client_processor_ap_loaded`. The validator required literal `0x2f6a208` in an objdump instruction line even though the established GNU objdump RIP-relative comment form emits the same address as `2f6a208` without a mandatory `0x` prefix. This resume may repair only that presentation-sensitive assertion and must rerun before claiming any later marker as proven.

Run `31904696996` provides sanitized prior disassembly useful for hypothesis selection. It does not by itself upgrade its prior `CANDIDATE` first-consumer classification.

# Acceptance boundary

A positive downstream claim requires exact type/member provenance plus a concrete read/call/data-flow edge from the retained QBuffer/helper/writer state into the candidate transform/consumer. A symbol-name hit, generic Qt/QBuffer census, vtable adjacency, unrelated local QBuffer use, historical final-socket observation, or passing workflow without the exact client fence is insufficient.

Classify separately:

```yaml
first_downstream_consumer: PROVEN | CANDIDATE | UNKNOWN
protocol_stage_order: PROVEN_PARTIAL | UNKNOWN
framing: PROVEN | CANDIDATE | UNKNOWN
sequence: PROVEN | CANDIDATE | UNKNOWN
compression: PROVEN | CANDIDATE | UNKNOWN
encryption: PROVEN | CANDIDATE | UNKNOWN
final_binary_egress: PROVEN | CANDIDATE | UNKNOWN
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
- owner-funded Codex/OpenAI API capacity.

Research stays Draft-only; coordinator owns promotion.