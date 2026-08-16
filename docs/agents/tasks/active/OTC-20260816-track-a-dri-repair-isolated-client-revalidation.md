---
task_id: OTC-20260816-track-a-dri-repair-isolated-client-revalidation
status: ready
agent: ChatGPT
session_id: chatgpt-dri-repair-isolated-client-revalidation-20260816-2219
session_role: runtime_researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_discriminator
phase: coordinator-promotion-ready
branch: diag/OTC-20260816-track-a-dri-repair-isolated-client-revalidation
base_branch: main
base_main: fa5b66b697d42c60515c5de48ea5e30135eadd0e
current_main: fa5b66b697d42c60515c5de48ea5e30135eadd0e
created: 2026-08-16T22:19:00+02:00
updated: 2026-08-16T22:32:00+02:00
risk: high
researcher_delivery: draft_only
implementation_authorized: true
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-dri-repair-isolated-client-revalidation.md
  - docs/agents/evidence/OTC-20260816-track-a-dri-repair-isolated-client-revalidation/**
modules_touched: []
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-xcbgl-runtime-trace.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-xvfb-dri-path-default-glx.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-xvfb-dri-path-fix.md
  - immutable isolated startup harness blob 1616edcc982be50ef2c95b8077160ec8fe9291fe
  - accepted XCB/GL transformer surface from semantic run 31964397523/job 95207211173
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: trusted-main DRI repair is merged and archived; one bounded non-canonical physical discriminator tested the exact official client against the repaired task-owned Xvfb GLX prerequisite
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: heavy
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260816-track-a-dri-repair-isolated-client-revalidation
runtime_namespace: track-a-dri-repair-client-revalidation-v1
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: false
persistent_session_role: none
physical_e2e_required: true
owner_funded_ai_api_authorized: false
canonical_boundary:
  read_or_write_canonical_lease: false
  read_or_write_canonical_registration: false
  publish_registration: false
  canonical_namespace_access: false
  credentials_allowed: false
  login_allowed: false
  gameplay_allowed: false
  track_b_access: false
  second_logged_in_global_session_allowed: false
exact_client_fence:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
preflight_attempts:
  - workflow_head: 1836f4109d21f4eb7448b6eaba2c170353357476
    governance_run: 31970617994
    governance_result: SUCCESS
    workflow_run: 31970618113
    workflow_job: 95222415652
    result: PRE_RUNTIME_TRANSFORMER_REFUSAL
    discriminator: DRI_REVALIDATION_REFUSED=XVFB_ENV_PATCH_SITE_COUNT:0
    runtime_mutation_started: false
    semantic_physical_run_consumed: false
  - workflow_head: 3882672fc0e96b2fdae9b84dd7be8772d4b8d83c
    governance_run: 31970677906
    governance_result: SUCCESS
    workflow_run: 31970677923
    workflow_job: 95222564029
    result: PRE_RUNTIME_TRANSFORMER_REFUSAL
    discriminator: DRI_REVALIDATION_REFUSED=XVFB_ENV_PATCH_SITE_COUNT:0
    runtime_mutation_started: false
    semantic_physical_run_consumed: false
  repair:
    cycle: 1
    repaired_head: c5e6328c697a2f02590bc99d082bb340e1405b8d
    change: replace the fragile two-line Xvfb environment anchor with the unique immutable-source XKB_CONFIG_ROOT token
    runtime_semantics_changed: false
semantic_execution:
  workflow_head: c5e6328c697a2f02590bc99d082bb340e1405b8d
  governance_run: 31970703290
  governance_result: SUCCESS
  workflow_run: 31970703417
  workflow_job: 95222630271
  workflow_result: SUCCESS
  semantic_physical_runs_completed: 1
  immutable_source_blob: 1616edcc982be50ef2c95b8077160ec8fe9291fe
  patch_count: 9
  canonical_state_access: NONE
  runtime_access: EPHEMERAL_ISOLATED
  support_fence: PASS
  exact_source_fence: PASS
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
    xcb_glx_metadata_found: true
    xcb_glx_key_found: true
    xcb_glx_library_loaded: true
    vulkan_library_loaded: true
    qrhi_vulkan_initialized: true
    prior_qxcb_neither_glx_nor_egl_line_in_allowlist: false
    prior_qrhigles2_failed_create_line_in_allowlist: false
  final_classification: CLIENT_ALIVE_NO_VISIBLE_WINDOWS_ON_ISOLATED_DISPLAY
  discriminator_result: PASS_DISCRIMINATOR_CAPTURED
  cleanup: COMPLETE
result:
  classification: PROVEN_DRI_PATH_RESTORES_XVFB_GLX_AND_REMOVES_PRIOR_ALLOWLISTED_QXCB_NO_GLX_EGL_FAILURE_BUT_EXACT_CLIENT_REMAINS_ALIVE_WITH_ZERO_VISIBLE_WINDOWS_THROUGH_35S
  dri_path_repairs_xvfb_glx_prerequisite: true
  prior_allowlisted_qxcb_no_glx_egl_failure_removed: true
  visible_official_client_window_proven: false
  remaining_no_window_root_cause: UNKNOWN_POST_GLX_PREREQUISITE
  canonical_bootstrap_retry_authorized: false
  client_backend_forcing_authorized: false
negative_evidence_boundary:
  statement: the complete 415-line task-owned client log was scanned locally with the configured XCB/GLX/EGL/QRhi/Vulkan allowlist; all 35 matches were emitted and none contained the prior QXcb neither-GLX-nor-EGL or QRhiGles2 create-failure signature
  does_not_prove:
    - every possible GL/EGL context operation succeeded
    - Vulkan RHI is the cause of the no-window state
    - the client can create a visible window on a canonical runtime
    - a canonical bootstrap is authorized
evidence:
  - docs/agents/evidence/OTC-20260816-track-a-dri-repair-isolated-client-revalidation/20260816-isolated-dri-repair-client-revalidation.md
one_shot_workflow_removed: true
audit:
  result: PASS_PENDING_EXACT_FINAL_HEAD_CHECKS
  material_findings_open: 0
acceptance:
  - task-owned ephemeral namespace and dynamic display/ports: PASS
  - exact source/client/support fences: PASS
  - contained DRI/swrast support contract: PASS
  - task-owned Xvfb receives only contained LIBGL_DRIVERS_PATH as the new provider input: PASS
  - Xvfb argument list unchanged and no +extension GLX: PASS
  - same-display GLX/RENDER capture: PASS
  - exact official client start without credentials/login/gameplay: PASS
  - no client LIBGL_DRIVERS_PATH leak and no backend forcing: PASS
  - 5/15/35 second liveness/window capture: PASS
  - complete allowlisted client-log scan: PASS
  - no canonical state access: PASS
  - cleanup: PASS
  - exactly one semantic physical run: PASS
final_validation:
  exact_final_head_track_a_governance: PENDING
  exact_final_head_repository_ci: PENDING
  review_threads_open: PENDING_COORDINATOR_CHECK
last_completed_step: semantic run 31970703417/job 95222630271 restored GLX on the task-owned Xvfb and removed the prior allowlisted QXcb GLX/EGL failure signature, while the exact client remained alive with zero visible windows through 35 seconds; cleanup completed and the one-shot workflow was removed before terminal evidence/task commits
next_action: obtain exact-final-head Track A governance and repository CI after workflow removal/evidence closeout; coordinator independently review the semantic logs and zero review threads, then promote/archive this durable evidence without any second physical run
---

# Track A isolated DRI-repair client revalidation — terminal candidate

The DRI repair is physically validated as a GLX prerequisite fix, but it does not resolve the bounded no-visible-window condition. The next investigation must move beyond GLX availability while preserving the non-canonical and no-second-login boundaries.