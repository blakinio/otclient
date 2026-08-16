---
task_id: OTC-20260816-track-a-qsg-glx-egl-rhi-discriminator
status: implementing
agent: ChatGPT
session_id: chatgpt-qsg-glx-egl-rhi-20260816
session_role: runtime_researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_discriminator
phase: isolated-qsg-backend-capture
branch: diag/OTC-20260816-track-a-qsg-glx-egl-rhi
base_branch: main
base_main: d7a2d4168816cb42267fc7b20aacb88ae1b13b8e
risk: high
updated: 2026-08-16T19:23:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-qsg-glx-egl-rhi-discriminator.md
  - docs/agents/evidence/OTC-20260816-track-a-qsg-glx-egl-rhi-discriminator/**
  - .github/workflows/tibia-official-client-re-qsg-glx-egl-rhi-discriminator.yml
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
execution_reason: canonical bootstrap mutation is governance-blocked; this separate task uses the previously accepted task-owned ephemeral-isolated startup harness only to capture bounded QSG_INFO/GLX/EGL/RHI evidence after the trusted graphics environment fix
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
mutation_authorized: true
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
source_harness:
  commit: cb557da12ebb41c597340909b2db717ee59cdfe1
  blob: 1616edcc982be50ef2c95b8077160ec8fe9291fe
  required_patches: 3
  patch_1: nounset-safe snapshot local declaration
  patch_2: replace source task id with this task id so namespace/marker ownership is current-task scoped
  patch_3: replace QT_XCB_GL_INTEGRATION=none with QSG_INFO=1 while preserving QT_QUICK_BACKEND=software
acceptance:
  - immutable source blob and exactly three patch sites are fenced before execution
  - task-owned isolated display/WARP/VNC/client namespace only
  - exact live client executable fence passes
  - bounded snapshots at 5/15/35 seconds are collected
  - bounded sanitized client log captures QSG_INFO plus GLX/EGL/RHI/scenegraph messages
  - no canonical lease/registration/session mutation occurs
  - cleanup completes for all task-owned state
  - exactly one semantic physical run; no retry on a new discriminator
last_completed_step: v7 proved the graphics source contract reached the physical runner but remained client_window_missing; current canonical bootstrap mutation is governance-blocked and did not expose client.log/QSG_INFO
next_action: run exactly one governance-compliant ephemeral-isolated QSG/GLX/EGL/RHI discriminator and persist its sanitized result
---

# Track A QSG / GLX / EGL / RHI discriminator

This task is diagnostic only. It must not create, reuse or modify the canonical runtime. It reproduces the accepted isolated startup surface after the graphics environment fix and captures only bounded non-secret graphics/backend evidence.