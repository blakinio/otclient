---
task_id: OTC-20260816-track-a-qt-debug-plugins-discriminator
status: implementing
agent: ChatGPT
session_id: chatgpt-qt-debug-plugins-20260816
session_role: runtime_researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_discriminator
phase: isolated-qt-plugin-discovery
branch: diag/OTC-20260816-track-a-qt-debug-plugins
base_branch: main
base_main: a1bab5e7197aba484ac72a4dbcb2d8fddeaeacc2
risk: high
updated: 2026-08-16T19:43:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-qt-debug-plugins-discriminator.md
  - docs/agents/evidence/OTC-20260816-track-a-qt-debug-plugins-discriminator/**
  - .github/workflows/tibia-official-client-re-qt-debug-plugins-discriminator.yml
modules_touched: []
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-qsg-glx-egl-rhi-discriminator.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-xcbgl-plugin-inventory.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: terminal inventory proved package/toolroot XCB GL plugins exist and have zero missing dependencies under canonical LD_LIBRARY_PATH; one isolated runtime capture with QT_DEBUG_PLUGINS=1 is required to classify discovery/load/initialization without forcing a backend or touching canonical state
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: heavy
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260816-track-a-qt-debug-plugins-discriminator
runtime_namespace: track-a-qt-debug-plugins-discriminator-v1
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
  patch_2: replace source task id with current task id
  patch_3: replace QT_XCB_GL_INTEGRATION=none with QSG_INFO=1 plus QT_DEBUG_PLUGINS=1 while preserving QT_QUICK_BACKEND=software
acceptance:
  - immutable source blob and exact patch sites fenced before execution
  - task-owned isolated display/WARP/VNC/client namespace only
  - exact live client executable fence passes
  - bounded snapshots at 5/15/35 seconds collected
  - sanitized client log captures QT_DEBUG_PLUGINS discovery/load/init output and QSG/GLX/EGL/RHI messages
  - no backend forced and no canonical state access
  - cleanup completes
  - exactly one semantic physical run; no retry on a new discriminator
last_completed_step: XCB GL plugin inventory #408/#409 proved plugin files exist with zero missing dependencies under canonical LD_LIBRARY_PATH
next_action: execute exactly one governance-compliant isolated QT_DEBUG_PLUGINS discriminator and persist sanitized discovery/load/initialization evidence
---

# Track A Qt plugin discovery discriminator

Diagnostic only. It must not create, reuse or mutate the canonical runtime and must not force GLX, EGL, Vulkan, OpenGL or another renderer/backend.