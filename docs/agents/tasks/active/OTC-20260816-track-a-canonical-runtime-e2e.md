---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: ready
agent: ChatGPT
session_id: chatgpt-post-rhi-window-state-20260816
session_role: runtime_discriminator_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: coordinator-promotion-ready-post-rhi-window-state
branch: diag/OTC-20260816-track-a-post-rhi-window-state
base_branch: main
base_main: b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4
risk: high
updated: 2026-08-16T23:10:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/**
modules_touched: []
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-dri-repair-isolated-client-revalidation.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-xvfb-dri-path-fix.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: one separately admitted isolated physical discriminator completed successfully and proved that raw X11 has a full-display viewable window after GLX/RHI initialization even though the canonical xdotool PID/title identity path sees no usable named window. This source Draft is now terminal and fail-closed; no second physical run is authorized on it. The next causal action is a separate X-Resource client-identity discriminator plus hosted/static investigation of the QQmlEngine/render-thread warning.
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
validation_level: heavy
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260816-track-a-canonical-runtime-e2e
runtime_namespace: track-a-post-rhi-window-state-v1
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
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
semantic_run:
  workflow_run: 31972261899
  hosted_preflight_job: 95226378236
  hosted_preflight_result: SUCCESS
  physical_job: 95226396914
  physical_result: SUCCESS
  runner: synology-otclient-01
  semantic_head: 8e9cc81011383922cf6bad75ca7207deb749fffb
  admission_immediately_before_runtime: PASS
  exact_base_fence: PASS
  source_blob_fence: PASS
  support_fence: PASS
  canonical_state_access: NONE
  cleanup: COMPLETE
  one_shot_workflow_removed: true
  temporary_transformers_removed: true
  second_run_authorized: false
x11_result:
  extension_count: 23
  glx_present: true
  glx_opcode: 150
  render_present: true
  render_opcode: 139
  t05:
    client_alive: true
    nonroot_windows: 1
    viewable: 0
    unmapped: 1
    notable_xid: 0x00c00005_UNMAPPED_3x3
  t15:
    client_alive: true
    nonroot_windows: 3
    viewable: 1
    unmapped: 2
    notable_xid: 0x00c00011_VIEWABLE_1920x1080
  t35:
    client_alive: true
    nonroot_windows: 3
    viewable: 1
    unmapped: 2
    notable_xid: 0x00c00011_VIEWABLE_1920x1080
  xdotool_named_visible_count_t05_t15_t35: 0
  xdotool_pid_name_class_binding_for_viewable_xid: ABSENT
  raw_viewable_window_fact: PROVEN
  exact_client_ownership_of_viewable_xid: UNKNOWN
thread_result:
  t05_count: 3
  t15_count: 32
  t35_count: 38
  observed_classes:
    - QXcbEventQueue
    - llvmpipe-0..3
    - QQmlThread
    - QSGSoftwareRend
    - QNetworkAccessM
    - QQuickPixmapRea
client_log:
  total_lines: 415
  broader_filter_matches: 121
  opengl_context_created: true
  opengl_renderer: Mesa_llvmpipe
  qrhi_vulkan_initialized: true
  qtquick_window_loaded: true
  cross_thread_qobject_warning: true
  warning_parent: QQmlEngine
  warning_current_thread: QSGSoftwareRenderThread
  warning_causal_to_window_identity: UNKNOWN
classification:
  primary: PROVEN_RAW_X11_TREE_HAS_VIEWABLE_1920X1080_NAMELESS_PIDLESS_WINDOW_FROM_T15_WHILE_XDOTOOL_NAMED_VISIBLE_SEARCH_RETURNS_ZERO_AND_EXACT_CLIENT_REMAINS_ALIVE_POST_GLX
  generated: NONROOT_X11_WINDOWS_PRESENT_NONE_TASK_PID_BOUND
  prior_zero_visible_window_claim_corrected: true
inference_boundary:
  xid_resource_base_inference: observed XIDs 0x00c00005, 0x00c00011, 0x00c00013 share 0x00c00000 region and are consistent with one X client connection
  xid_resource_base_is_process_identity_proof: false
  xres_client_pid_needed: true
external_primary_source_checkpoint:
  xres_1_2_query_client_ids_supports_resource_xid_selection: true
  xres_local_client_pid_mask_exists: true
  qt_qobject_parent_child_same_thread_required: true
  qt_scenegraph_may_use_dedicated_render_thread: true
forbidden:
  - any second semantic run from this Draft
  - canonical bootstrap retry from this Draft
  - relaxing canonical window identity to any viewable fullscreen XID without resource/client identity proof
  - canonical lease/registration/session access
  - credentials, login or gameplay
  - Track B and historical PR #303 runtime surfaces
acceptance:
  - same-generation hosted preflight: PASS
  - same-generation runtime admission: PASS
  - exact base/source/support fences: PASS
  - GLX/RENDER state captured: PASS
  - raw X11 map-state tree captured t05/t15/t35: PASS
  - bounded task-owned thread state captured: PASS
  - broader complete-log filter captured: PASS
  - cleanup complete: PASS
  - one-shot workflow removed: PASS
  - temporary transformers removed: PASS
  - no second physical run: PASS
  - new causal frontier identified: PASS
evidence:
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/20260816-post-rhi-window-state.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/20260816-post-rhi-semantic-authorization.md
last_completed_step: semantic run 31972261899 / job 95226396914 proved a raw VIEWABLE 1920x1080 X11 window exists from t15 while xdotool PID/title identity remains unavailable; exact client remains alive with OpenGL llvmpipe, QRhi Vulkan and QtQuick.Window initialized; cleanup completed and all one-shot runtime files were removed
next_action: coordinator-promote/archive this bounded evidence. Independently, the next separately admitted runtime discriminator should use X-Resource v1.2 QueryClientIds on the observed raw XID class to prove or refute exact-client PID ownership; in parallel, hosted/static work may classify the QQmlEngine/QSGSoftwareRenderThread warning. Do not relax the canonical worker or retry canonical bootstrap before identity proof.
---

# Track A canonical runtime E2E — post-RHI window-state terminal source

This Draft proves that a raw viewable X11 window exists after the graphics repair and corrects the earlier named-window observation. It deliberately does not claim that the window belongs to the official-client PID until X-Resource identity evidence is captured.
