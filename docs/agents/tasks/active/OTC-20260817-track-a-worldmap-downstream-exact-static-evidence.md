---
task_id: OTC-20260817-track-a-worldmap-downstream-exact-static-evidence
status: implementing
agent: ChatGPT
session_id: chatgpt-worldmap-downstream-static-producer-20260817
session_role: researcher_producer_under_coordinator_dispatch
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: evidence_staging
phase: downstream-worldmap-exact-static-evidence
implementation_authorized: true
branch: research/OTC-20260817-track-a-worldmap-downstream-exact-static-evidence
base_branch: main
base_main: 55803133a5abe8b1e75e4660da1d2b84b154ab9a
live_main_at_claim: 55803133a5abe8b1e75e4660da1d2b84b154ab9a
risk: medium
updated: 2026-08-17T08:12:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-worldmap-downstream-exact-static-evidence.md
  - docs/agents/evidence/OTC-20260817-track-a-worldmap-downstream-exact-static-evidence/**
  - .github/scripts/tibia-official-client-re-worldmap-downstream-exact-static.py
  - .github/workflows/tibia-official-client-re-worldmap-downstream-exact-static.yml
modules_touched: []
reuses:
  - PR #367 / OTC-20260816-track-a-worldmap-extent-static-re as consumer only; do not modify its branch from this producer
  - PR #437 / OTC-20260816-track-a-worldmap-exact-static-evidence as accepted prior exact-static producer methodology and exact anchors
  - PR #437 source run 31972743782 artifact 9270235755 and hosted run 31972915689 artifact 9270276361 as provenance/reference only
  - docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_PARALLEL_RESEARCH_COORDINATION.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
depends_on:
  - exact retained official native-Linux client file matching 15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  - PR #367 consumer frontier at head a69179e5cf4681a9d41014a562a0bfd0d1cd9ffb
blocks:
  - PR #367 final downstream static patch/dependency graph
policy_version: 2
prompting_standard_version: 2.1
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: checkpoint_only
user_communication: low_noise
execution_mode: github-actions
execution_reason: GitHub-only producer with one bounded read-only exact-file staging step on synology-otclient-01 and disposable hosted decoding; no live client/runtime access
execution_class: github_hosted
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
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: false
owner_funded_ai_api_authorized: false
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
source_staging_exception:
  coordinator_approved: true
  reason: owner explicitly requested autonomous RUNTIME evidence production; PR #367 requires new exact-file downstream windows and current routing permits bounded read-only host-local source staging when the file is not available to hosted runners
  source_executor: synology-otclient-01
  source_access: read_only_file_only
  source_runtime_access: none
  source_candidates:
    - /home/runner/_work/_otclient_tibia_re_state/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client
    - /work/_otclient_tibia_re_state/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client
  canonical_state_access: forbidden
  client_process_access: forbidden
  process_memory_access: forbidden
  x11_vnc_access: forbidden
  login_session_access: forbidden
  gameplay_access: forbidden
  raw_client_upload: forbidden
  client_byte_mutation: forbidden
  allowed_output: bounded sanitized text/json evidence and bounded executable code windows only
  hosted_validation_executor: ubuntu-latest
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
feature_scope:
  type: contract_producer
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: partial_producer
consumer_contract:
  pr: 367
  task: OTC-20260816-track-a-worldmap-extent-static-re
  consumer_branch: research/OTC-20260816-track-a-worldmap-extent-static-re
  consumer_head_at_claim: a69179e5cf4681a9d41014a562a0bfd0d1cd9ffb
  requested_targets:
    storage_slot_12: 0x00cc6cd0
    storage_slot_12_input_pair: rsi+0x38
    render_provider: {typeinfo: 0x03089b70, vptr: 0x02f6c258}
    camera: {typeinfo: 0x03080500, vptr: 0x03083968}
    picker: {typeinfo: 0x03086888, vptr: 0x02f6b7c8}
  requested_questions:
    - caller/upstream producer that feeds TWorldMapStorage slot 12, especially QWORD argument rsi+0x38
    - RenderProvider non-destructor iteration, clipping and culling constraints
    - Camera non-meta projection, scale and viewport coupling
    - Picker non-destructor screen/world transform and bounds constraints
    - fixed allocations, loop bounds, masks, packing and hardcoded 18/14 or derived values tied to these paths
acceptance_inventory:
  - exact source fence re-proven before any read
  - no client process, process memory, canonical state, X11/VNC, login/gameplay or client-byte mutation
  - recover relocation-aware vtable slots for RenderProvider/Camera/Picker and stage non-trivial executable slots/callers rather than destructor/first-slot-only windows
  - recover direct xrefs/callers of Storage slot-12 function 0x00cc6cd0 and bounded caller windows sufficient to trace the source of its rsi+0x38 pair when statically possible
  - hosted disassembly/analysis over bounded sanitized windows only; raw client never uploaded
  - persist FACT/INFERENCE/UNKNOWN separately; do not infer missing immediate 18/14 writes
  - durable evidence usable by #367 without Synology access
  - exact-head governance/CI green for the producer Draft PR
researcher_delivery: draft_only
WORLD_MAP_DOWNSTREAM_STATIC_EVIDENCE_READY: false
programme_complete: false
invocation_started_at: 2026-08-17T08:12:00+02:00
last_progress_at: 2026-08-17T08:12:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: producer-initial
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
recovery_checkpoint:
  status: CLAIMED_BEFORE_FIRST_SOURCE_RUN
  fresh_overlap_check: no open downstream worldmap exact-static producer found; open worldmap PRs are consumer #367 and prior producer #437 only
  source_run_id: NOT_STARTED
  source_job_id: NOT_STARTED
  prohibited_repeat: do not repeat v7 GUI/client_window_missing; do not rescan exhausted retained inventory; do not depend on source-side objdump/llvm-objdump because prior producer proved both absent
next_action: open a Draft producer PR, implement a disassembler-free exact-ELF source sanitizer that stages non-trivial vtable/caller windows for Storage slot 12, RenderProvider, Camera and Picker, then hosted-disassemble and persist consumer-ready evidence for PR #367
---

# Track A world-map downstream exact static evidence producer

This task exists only to produce the new exact static input requested by consumer PR #367. It owns no consumer files and does not design or apply a client patch.
