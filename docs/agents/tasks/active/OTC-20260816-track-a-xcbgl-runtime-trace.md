---
task_id: OTC-20260816-track-a-xcbgl-runtime-trace
status: implementing
agent: ChatGPT
session_id: chatgpt-xcbgl-runtime-trace-20260816
session_role: runtime_researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_discriminator
phase: isolated-xcbgl-loader-trace
branch: diag/OTC-20260816-track-a-xcbgl-runtime-trace
base_branch: main
base_main: d3f186414256151c9d5e03f34c5a9026b1fba500
risk: high
updated: 2026-08-16T20:14:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-xcbgl-runtime-trace.md
  - docs/agents/evidence/OTC-20260816-track-a-xcbgl-runtime-trace/**
  - .github/workflows/tibia-official-client-re-xcbgl-runtime-trace.yml
modules_touched: []
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-xcbgl-log-extract.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-qt-debug-plugins-discriminator.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: the completed hosted extraction of #410 proved the retained Actions log cannot classify xcbglintegrations discovery/load/init; the next accepted discriminator is one narrow ephemeral-isolated runtime trace plus read-only extension inventory on the same task-owned Xvfb display
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: heavy
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260816-track-a-xcbgl-runtime-trace
runtime_namespace: track-a-xcbgl-runtime-trace-v1
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
  required_patches: 6
  patch_1: nounset-safe snapshot local declaration
  patch_2: replace source task id with current task id
  patch_3: replace QT_XCB_GL_INTEGRATION=none with QSG_INFO=1 plus QT_DEBUG_PLUGINS=1 while preserving QT_QUICK_BACKEND=software
  patch_4: add read-only core-X11 extension inventory after task-owned Xvfb socket proof
  patch_5: filter the complete task-owned client log to xcbglintegrations/QXcbIntegration/GLX/EGL/QRhi/load lines before emission
  patch_6: emit exact filtered-match count alongside total client-log line count
observation_scope:
  - same task-owned isolated Xvfb display created by the accepted immutable harness
  - X11 core ListExtensions plus QueryExtension for GLX and RENDER only
  - complete client.log scanned locally but only allowlisted sanitized graphics/plugin lines emitted
  - bounded 5/15/35 second client/window snapshots retained from the accepted harness
forbidden:
  - canonical bootstrap or canonical lease/registration/session access
  - backend forcing including QSG_RHI_BACKEND or QT_XCB_GL_INTEGRATION override
  - account credentials, login or gameplay
  - Track B or historical PR #303 runtime surfaces
  - arbitrary process inventory or proprietary binary upload
acceptance:
  - immutable source blob and every patch site fenced before execution
  - task-owned isolated display/WARP/VNC/client namespace only
  - exact live client executable fence passes
  - read-only X11 extension inventory proves whether GLX is advertised on the exact task-owned display
  - complete client log is scanned and only compact sanitized xcbglintegration/GLX/EGL/QRhi/load lines are emitted
  - no graphics backend is forced and canonical state is untouched
  - cleanup completes
  - exactly one semantic physical run; no retry on a new discriminator
last_completed_step: #412/#413 exhausted the retained #410 Actions log and proved xcbglintegration discovery/load/init remains unknown without a new physical observation
next_action: execute exactly one governance-compliant isolated XCB GL loader trace plus same-display X11 extension inventory, persist the sanitized result, remove the one-shot workflow, return mutation_authorized=false, and hand the Draft to the coordinator
---

# Track A XCB GL runtime trace discriminator

This is a narrow non-canonical physical diagnostic. It must not create, inspect or mutate the canonical runtime and must not force GLX, EGL, Vulkan, OpenGL or another renderer/backend.