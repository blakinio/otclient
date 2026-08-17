---
task_id: OTC-20260816-track-a-qsg-glx-egl-rhi-discriminator
status: completed
agent: ChatGPT
session_role: runtime_researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_discriminator
phase: archived
implementation_pr: 406
implementation_head: 45e19e5a2893b811693b926ff646f4afa0e5701d
implementation_merge_commit: da0ff6feb34e4ce3106ed0a799d5bb660d995b17
updated: 2026-08-16T19:30:00+02:00
owned_paths: []
ownership_released: true
runtime_access: ephemeral_isolated
runtime_namespace: track-a-qsg-glx-egl-rhi-discriminator-v1
mutation_authorized: false
owner_funded_ai_api_authorized: false
canonical_state_access: NONE
credentials_login_gameplay: NONE
semantic_run:
  run: 31961555061
  job: 95200193452
  governance_run: 31961554989
  result: SUCCESS
  cleanup: COMPLETE
result:
  classification: PROVEN_VULKAN_LLVMPIPE_INITIALIZES_WHILE_XCB_GLX_EGL_UNAVAILABLE_AND_NO_VISIBLE_WINDOW
  qrhi_vulkan_backend: INITIALIZED
  vulkan_physical_device: llvmpipe LLVM 20.1.2 128 bits
  mesa_version: 25.2.8
  vulkan_api: 1.4.318
  vk_khr_xcb_surface: ENABLED
  qt_quick_backend: software
  xcb_glx_egl_platform_context: UNAVAILABLE
  visible_x11_window: NONE_THROUGH_35S
final_validation:
  exact_head_governance_run: 31961726183
  exact_head_governance_result: SUCCESS
  exact_head_ci_run: 31961726285
  exact_head_ci_result: SUCCESS
  ready_state_ci_run: 31961762406
  ready_state_ci_result: SUCCESS
  review_threads_open: 0
evidence:
  - docs/agents/evidence/OTC-20260816-track-a-qsg-glx-egl-rhi-discriminator/20260816-qsg-glx-egl-rhi-result.md
runtime_nonclaims:
  canonical_registration: ABSENT
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
next_action: inventory exact-client/toolroot xcbglintegrations plugin files, Qt plugin search paths and dynamic dependencies before any backend forcing or canonical bootstrap
---

# QSG / GLX / EGL / RHI discriminator — terminal archive

The task proved that QRhi Vulkan initializes on llvmpipe while XCB platform GLX/EGL contexts remain unavailable and no visible client window maps. The isolated runtime was fully cleaned and canonical state was untouched. Ownership is released.