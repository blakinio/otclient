---
task_id: OTC-20260816-track-a-qsg-glx-egl-rhi-discriminator
status: ready
agent: ChatGPT
session_id: chatgpt-qsg-glx-egl-rhi-20260816
session_role: runtime_researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_discriminator
phase: coordinator-promotion-ready
branch: diag/OTC-20260816-track-a-qsg-glx-egl-rhi
base_branch: main
base_main: d7a2d4168816cb42267fc7b20aacb88ae1b13b8e
risk: high
updated: 2026-08-16T19:28:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-qsg-glx-egl-rhi-discriminator.md
  - docs/agents/evidence/OTC-20260816-track-a-qsg-glx-egl-rhi-discriminator/**
modules_touched: []
reuses:
  - docs/agents/evidence/OTC-20260816-track-a-client-window-ownership-discriminator/20260816-final-no-visible-window-gl-context.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/20260816-v7-governance-invalid-client-window-missing.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: one governance-compliant ephemeral-isolated run captured the missing QSG/GLX/EGL/RHI evidence without canonical state access; the task is now terminal and further mutation is disabled
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: heavy
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260816-track-a-qsg-glx-egl-rhi-discriminator
runtime_namespace: track-a-qsg-glx-egl-rhi-discriminator-v1
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
exact_client_fence:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
semantic_run:
  run: 31961555061
  job: 95200193452
  governance_run: 31961554989
  governance_result: SUCCESS
  result: SUCCESS
  source_blob: 1616edcc982be50ef2c95b8077160ec8fe9291fe
  patch_count: 3
  canonical_state_access: NONE
  display: ':231'
  vnc_port: 6200
  warp: PASS
  xvfb: PASS
  vnc: PASS
  client_pid: 24554
  client_pgid: 24554
  client_alive_t05: true
  client_alive_t15: true
  client_alive_t35: true
  visible_windows_t05: 0
  visible_windows_t15: 0
  visible_windows_t35: 0
  cleanup: COMPLETE
graphics_result:
  classification: PROVEN_VULKAN_LLVMPIPE_INITIALIZES_WHILE_XCB_GLX_EGL_UNAVAILABLE_AND_NO_VISIBLE_WINDOW
  qrhi_vulkan_backend: INITIALIZED
  vulkan_physical_device: llvmpipe LLVM 20.1.2 128 bits
  mesa_version: 25.2.8
  vulkan_api: 1.4.318
  vk_khr_xcb_surface: ENABLED
  qt_quick_backend: software
  xcb_glx_egl_platform_context: UNAVAILABLE
  qrhi_gles2_context: FAILED
  visible_x11_window: NONE_THROUGH_35S
  asset_loading: COMPLETE
  tibia_https_via_task_proxy: PASS
falsified:
  - removing QT_XCB_GL_INTEGRATION=none alone is sufficient to map the client window
  - general Vulkan/GPU unavailability is the blocker
unknown:
  - whether xcb_glx/xcb_egl integration plugins are absent, undiscoverable or fail initialization
  - whether XCB GL integration failure alone causes the missing visible window
  - exact safe graphics correction
one_shot_workflow_removed: true
evidence:
  - docs/agents/evidence/OTC-20260816-track-a-qsg-glx-egl-rhi-discriminator/20260816-qsg-glx-egl-rhi-result.md
audit:
  result: PASS
  material_findings_open: 0
acceptance:
  - semantic graphics/backend discriminator captured: PASS
  - exact client remained alive through bounded observation: PASS
  - task-owned cleanup: PASS
  - canonical state untouched: PASS
  - credentials/login/gameplay absent: PASS
  - no further physical retry from this task
last_completed_step: run 31961555061/job 95200193452 proved QRhi Vulkan initializes on llvmpipe while XCB still has neither GLX nor EGL and the display remains windowless through 35 seconds; cleanup completed
next_action: coordinator-promote/archive this discriminator, then inventory exact-client/toolroot xcbglintegrations plugin files, Qt plugin search paths and dynamic dependencies before any backend forcing or canonical bootstrap
---

# Track A QSG / GLX / EGL / RHI discriminator — terminal candidate

The isolated diagnostic is complete. Vulkan via llvmpipe initializes successfully, Qt Quick loads the software backend, but XCB still cannot provide GLX/EGL platform contexts and no visible window maps. This selects plugin/discovery/dependency inventory as the next non-canonical boundary.