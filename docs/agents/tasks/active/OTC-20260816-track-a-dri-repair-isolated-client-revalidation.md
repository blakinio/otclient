---
task_id: OTC-20260816-track-a-dri-repair-isolated-client-revalidation
status: ready
agent: ChatGPT
session_id: chatgpt-coord-dri-repair-revalidation-20260816-2235
session_role: promotion_integration_coordinator
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_discriminator
phase: coordinator-promotion-ready
branch: docs/OTC-20260816-track-a-dri-repair-isolated-client-revalidation-promote
base_branch: main
base_main: fa5b66b697d42c60515c5de48ea5e30135eadd0e
current_main: fa5b66b697d42c60515c5de48ea5e30135eadd0e
created: 2026-08-16T22:19:00+02:00
updated: 2026-08-16T22:35:00+02:00
risk: high
researcher_delivery: draft_only
implementation_authorized: true
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-dri-repair-isolated-client-revalidation.md
  - docs/agents/evidence/OTC-20260816-track-a-dri-repair-isolated-client-revalidation/**
modules_touched: []
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: coordinator promotion consumes already-completed durable physical evidence; no runtime process or physical mutation occurs in this promotion session
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
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
physical_e2e_reason: physical discriminator already completed exactly once in the accepted source package
owner_funded_ai_api_authorized: false
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
  canonical_bootstrap_authorized: false
source_research:
  pr: 431
  final_head: 17e09be20643ddd13e8f2ca24bd510e8e99e6e03
  task_blob: 779a760cc77c198357fde809d5683374caaa9708
  evidence_blob: aebf57694ccf257f47a6452e124ead120398a46f
  coordinator_decision: ACCEPT
  material_findings_open: 0
  review_threads_open: 0
  one_shot_workflow_removed: true
  preflight_nonsemantic_runs:
    - {run: 31970618113, job: 95222415652, result: PRE_RUNTIME_TRANSFORMER_REFUSAL, runtime_mutation: false}
    - {run: 31970677923, job: 95222564029, result: PRE_RUNTIME_TRANSFORMER_REFUSAL, runtime_mutation: false}
  final_track_a_governance_run: 31970849706
  final_track_a_governance_result: SUCCESS
  final_repository_ci_run: 31970849838
  final_repository_ci_result: SUCCESS
  final_required_ci_job: 95222998232
  final_required_ci_result: SUCCESS
physical_evidence:
  semantic_head: c5e6328c697a2f02590bc99d082bb340e1405b8d
  governance_run: 31970703290
  governance_result: SUCCESS
  semantic_run: 31970703417
  semantic_job: 95222630271
  semantic_result: SUCCESS
  runner: synology-otclient-01
  runtime_access: ephemeral_isolated
  canonical_state_access: NONE
  cleanup: COMPLETE
  exact_client:
    version: 15.32.df7b29
    size: 51965216
    sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  contained_dri_path: /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri
  swrast_real: /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri/libdril_dri.so
  explicit_glx_flag: false
  client_receives_libgl_drivers_path: false
  client_backend_forcing: false
  historical_ephemeral_values_only:
    display: ':231'
    vnc_port: 6200
    client_pid: 26972
    client_pgid: 26972
  x11:
    extension_count: 23
    glx_present: true
    glx_major_opcode: 150
    render_present: true
    render_major_opcode: 139
  snapshots:
    t05: {client_alive: true, state: D, visible_window_count: 0}
    t15: {client_alive: true, state: R, visible_window_count: 0}
    t35: {client_alive: true, state: S, visible_window_count: 0}
  client_log:
    total_lines: 415
    allowlist_matches: 35
    xcb_platform_library_loaded: true
    xcbglintegrations_directory_scanned: true
    xcb_glx_library_loaded: true
    vulkan_library_loaded: true
    qrhi_vulkan_initialized: true
    prior_qxcb_neither_glx_nor_egl_line_in_allowlist: false
    prior_qrhigles2_failed_create_line_in_allowlist: false
result:
  classification: PROVEN_DRI_PATH_RESTORES_XVFB_GLX_AND_REMOVES_PRIOR_ALLOWLISTED_QXCB_NO_GLX_EGL_FAILURE_BUT_EXACT_CLIENT_REMAINS_ALIVE_WITH_ZERO_VISIBLE_WINDOWS_THROUGH_35S
  dri_path_repairs_xvfb_glx_prerequisite: true
  visible_official_client_window_proven: false
  remaining_no_window_root_cause: UNKNOWN_POST_GLX_PREREQUISITE
  canonical_bootstrap_retry_authorized: false
negative_evidence_boundary:
  statement: the complete 415-line task-owned client log was scanned with the configured graphics allowlist; all 35 matches were emitted and none contained the prior QXcb neither-GLX-nor-EGL or QRhiGles2 create-failure signature
  does_not_prove:
    - every possible GL/EGL context operation succeeded
    - Vulkan RHI causes the no-window state
    - a canonical runtime can create a visible client window
promotion:
  pr: 432
  source_pr: 431
  initial_replay_head: eee37fc9fb71a338f8a525cd2f0e133a356c446a
  replay_method: exact final source task/evidence blobs onto current main without temporary-workflow history; task then rewritten only for coordinator promotion state
  physical_run_repeated: false
validation:
  source_exact_head_track_a_governance: SUCCESS
  source_exact_head_repository_ci: SUCCESS
  source_exact_head_required_ci: SUCCESS
  coordinator_log_cross_check: PASS
  promotion_exact_head_track_a_governance: PENDING
  promotion_exact_head_repository_ci: PENDING
  review_threads_open: 0
  physical_e2e: PASS_SOURCE_RUN_31970703417_JOB_95222630271
audit:
  result: PASS
  material_findings_open: 0
acceptance:
  - exactly one semantic physical run: PASS
  - trusted contained DRI path restores GLX: PASS
  - prior configured QXcb no-GLX/EGL failure signature removed: PASS
  - exact client still alive with zero visible windows through 35 seconds: PASS
  - no credentials/login/gameplay/canonical state/backend forcing/Track B: PASS
  - cleanup complete: PASS
  - no second physical run in promotion: PASS
  - conclusion does not overstate remaining root cause: PASS
last_completed_step: coordinator independently reviewed the semantic job log, final source task/evidence, exact-final-head governance/CI and zero review threads, accepted Draft #431, and replayed its durable package onto current main as Draft #432 without temporary-workflow history
next_action: obtain exact-head Track A governance and repository CI for this coordinator checkpoint; if green and main remains compatible, close source #431 superseded, mark #432 ready, merge after ready-state protection gates, then archive the task and release ownership without any further physical run
---

# Track A isolated DRI-repair client revalidation — coordinator promotion

The DRI repair is physically validated as a GLX prerequisite fix, but the bounded official-client no-visible-window condition remains. This evidence grants no canonical runtime authority.