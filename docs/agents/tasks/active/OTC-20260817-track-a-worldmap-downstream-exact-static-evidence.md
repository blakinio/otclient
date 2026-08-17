---
task_id: OTC-20260817-track-a-worldmap-downstream-exact-static-evidence
status: validating
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
updated: 2026-08-17T08:52:00+02:00
producer_pr: 446
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-worldmap-downstream-exact-static-evidence.md
  - docs/agents/evidence/OTC-20260817-track-a-worldmap-downstream-exact-static-evidence/**
  - .github/scripts/tibia-official-client-re-worldmap-downstream-exact-static.py
  - .github/workflows/tibia-official-client-re-worldmap-downstream-exact-static.yml
  - .github/scripts/tibia-official-client-re-worldmap-downstream-targeted-static.py
  - .github/workflows/tibia-official-client-re-worldmap-downstream-targeted-static.yml
  - .github/scripts/tibia-official-client-re-worldmap-camera-neighborhood.py
  - .github/workflows/tibia-official-client-re-worldmap-camera-neighborhood.yml
modules_touched: []
reuses:
  - PR #367 / OTC-20260816-track-a-worldmap-extent-static-re as consumer only; producer never modifies its branch
  - PR #437 / OTC-20260816-track-a-worldmap-exact-static-evidence as accepted prior exact-static producer methodology and exact identity anchors
  - docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_PARALLEL_RESEARCH_COORDINATION.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
depends_on:
  - exact retained official native-Linux client file matching 15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  - PR #367 consumer frontier at head a69179e5cf4681a9d41014a562a0bfd0d1cd9ffb
blocks:
  - PR #367 downstream static patch/dependency reconciliation until this evidence is consumed
policy_version: 2
prompting_standard_version: 2.1
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: checkpoint_only
user_communication: low_noise
execution_mode: github-actions
execution_reason: GitHub-only producer with bounded read-only exact-file staging on synology-otclient-01 and disposable hosted decoding; no live client/runtime access
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
  reason: owner explicitly requested autonomous RUNTIME evidence production; PR #367 required new exact-file downstream windows and current routing permits bounded read-only host-local source staging when the file is not available to hosted runners
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
acceptance_inventory:
  - exact source fence re-proven before every physical read
  - no client process, process memory, canonical state, X11/VNC, login/gameplay or client-byte mutation
  - upstream Storage slot-12 pair source recovered
  - RenderProvider clipping/culling/indexing/iteration constraints recovered
  - Picker screen/world 32-cell transform constraints recovered
  - Camera exact layout/coownership recovered and all exact-vptr neighborhoods bounded-disassembled
  - fixed allocation/mask/packing dependencies recovered without broad false-positive promotion
  - durable evidence usable by #367 without Synology access
  - exact-head governance/CI required before handoff completion
researcher_delivery: draft_only
WORLD_MAP_DOWNSTREAM_STATIC_EVIDENCE_READY: true
programme_complete: false
invocation_started_at: 2026-08-17T08:12:00+02:00
last_progress_at: 2026-08-17T08:52:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: camera-supplement-consumer-ready
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 0
stall_warnings: 0
validation_state:
  broad_run: 32001356705
  broad_source_job: 95302168871
  broad_source_result: SUCCESS
  broad_source_artifact: 9278519216
  broad_source_digest: e10347435bece4cbedc7fca54b782cea76f9f1dab3b042082fe3bcc15f7c0728
  broad_hosted_job: 95302411849
  broad_hosted_result: SUCCESS
  broad_final_artifact: 9278527206
  broad_final_digest: af12b2af9c725ca402224876c3cbd0c01306f47b37e717548c5817310dd3bc9b
  broad_code_windows: 236
  broad_code_raw_bytes: 532736
  targeted_run: 32002326947
  targeted_source_job: 95304896213
  targeted_source_result: SUCCESS
  targeted_source_artifact: 9278827774
  targeted_source_digest: 8f6a9feaea607475f6f9d25d200d858f52714f9384561bd4010405d26a78009a
  targeted_hosted_job: 95305039463
  targeted_hosted_result: SUCCESS
  targeted_final_artifact: 9278833445
  targeted_final_digest: 7505aeae6e79e8829adf60261e1a3b50f27e0514f50136161e5f715a27124218
  targeted_code_windows: 15
  targeted_code_raw_bytes: 38400
  camera_run: 32003150333
  camera_source_job: 95307268007
  camera_source_result: SUCCESS
  camera_source_artifact: 9279105537
  camera_source_digest: 9b44a39558c50ce86243dece3b3fac19bb1f7619112e913fa45b647878d9e28d
  camera_hosted_job: 95307487191
  camera_hosted_result: SUCCESS
  camera_final_artifact: 9279111731
  camera_final_digest: 81620b3fd866e2203b2ed0a39a1a0979ba52b5e3af41b47ac7e247b09082effa
  camera_vptr_xrefs: 11
  camera_code_windows: 11
  camera_code_raw_bytes: 225280
  camera_unique_instruction_records: 37325
  primary_vtable_boundaries_curated:
    render_provider: slots_0_through_21
    camera: slots_0_through_4
    picker: slots_0_through_7
  durable_evidence:
    - docs/agents/evidence/OTC-20260817-track-a-worldmap-downstream-exact-static-evidence/20260817-worldmap-downstream-exact-static-evidence.md
    - docs/agents/evidence/OTC-20260817-track-a-worldmap-downstream-exact-static-evidence/20260817-worldmap-downstream-exact-static-evidence.json
    - docs/agents/evidence/OTC-20260817-track-a-worldmap-downstream-exact-static-evidence/20260817-worldmap-camera-neighborhood-evidence.md
    - docs/agents/evidence/OTC-20260817-track-a-worldmap-downstream-exact-static-evidence/20260817-worldmap-camera-neighborhood-evidence.json
recovery_checkpoint:
  status: ALL_REQUESTED_DOWNSTREAM_BOUNDED_EVIDENCE_CURATED_AWAITING_EXACT_HEAD_CI
  fresh_overlap_check: no competing downstream worldmap exact-static producer existed at claim time
  exact_source_candidate_index: 1
  proven_upstream_chain: static 18/14 literal at 0x01cdd958 -> Handler+0xb0/+0xb4 -> snapshot+0x38 via 0x00bc6350 -> Handler+0x10 exact TWorldMapStorage slot12 -> Storage+0x48/+0x4c
  fixed_default_classification: Handler and Viewport constructors use static 18/14; Storage constructor uses zero and Storage slot12 copies mutable snapshot state
  later_handler_master_writer_census: UNKNOWN
  render_provider_result: direct 32-cell clipping/culling/indexing/iteration dependencies recovered
  picker_result: direct fixed-32 screen/world conversion and bounds dependencies recovered
  camera_result: exact layout plus higher-level Camera/Viewport coownership recovered; all 11 exact Camera-vptr neighborhoods staged; no direct Camera-field -> Storage/master-18x14 edge recovered in the bounded neighborhoods; no preidentified Camera mutation site
  prohibited_repeat: do not repeat broad generic [vtable+0x60] scans as semantic proof; do not repeat v7 GUI/client_window_missing; do not rescan exhausted retained inventory; do not repeat Camera neighborhoods without a new discriminator
next_action: obtain exact-head Track A governance and repository CI for PR #446; then consume the durable evidence in #367 and finish the static dependency graph without client-byte mutation
---

# Track A world-map downstream exact static evidence producer

All requested downstream exact-static producer evidence is now durable and curated. The producer remains Draft-only and never modified #367. The remaining step is exact-head validation followed by consumer integration.
