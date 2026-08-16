---
task_id: OTC-20260816-track-a-mesa-glx-provider-inventory
status: implementing
agent: ChatGPT
session_id: chatgpt-mesa-glx-provider-inventory-20260816
session_role: runtime_infrastructure_observer
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: runtime_infrastructure_inventory
phase: contained-mesa-glx-provider-readonly
branch: diag/OTC-20260816-track-a-mesa-glx-provider-inventory
base_branch: main
base_main: d3f186414256151c9d5e03f34c5a9026b1fba500
risk: low
updated: 2026-08-16T20:45:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-mesa-glx-provider-inventory.md
  - docs/agents/evidence/OTC-20260816-track-a-mesa-glx-provider-inventory/**
  - .github/workflows/tibia-official-client-re-mesa-glx-provider-inventory.yml
modules_touched: []
reuses:
  - PR #416 contained-Xvfb capability evidence as unpromoted research input only
  - PR #417 explicit-GLX differential as unpromoted research input only
  - PR #418 modulepath rejection as unpromoted research input only
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: Xvfb contains GLX server code and contained libGL/libglx files, but default and explicit GLX launches advertise no GLX and Xvfb rejects -modulepath; the next bounded question is whether the fixed contained Mesa/GLVND/DRI provider stack needed for software GLX is complete and where its actual search roots are
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: read_only
runtime_owner_task: OTC-20260816-track-a-mesa-glx-provider-inventory
runtime_namespace: runner-support-mesa-glx-provider
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
physical_e2e_required: false
owner_funded_ai_api_authorized: false
observation_allowlist:
  - /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/** bounded to named GLVND/Mesa/DRI candidates and their direct ELF dependencies
  - /work/_otclient_tibia_re_state/toolroot/lib/x86_64-linux-gnu/** same bounded rule
  - /work/_otclient_tibia_re_state/toolroot/usr/lib/xorg/modules/extensions/libglx.so
  - fixed DRI directories below the contained toolroot
  - fixed GLVND vendor JSON directories below the contained toolroot
  - SHA-256, file size, ELF NEEDED/RPATH/RUNPATH and bounded provider/search-path strings
forbidden_observation:
  - official client package/files/processes
  - /proc process inventory
  - canonical runtime registration/lease/session directories
  - X11 display/window/VNC state
  - any X server execution
  - network/game/login state
  - credentials or environment secrets
  - Track B and historical PR #303 surfaces
acceptance:
  - fixed roots and named provider candidates are enumerated without ambient PATH discovery
  - exact presence/hash/ELF metadata recorded for libGL, libGLX, Mesa GLX, GLdispatch, EGL Mesa, GBM, DRM and swrast DRI candidates when present
  - direct dependencies are resolved against fixed contained roots and missing direct dependencies are explicit
  - DRI directory and swrast_dri.so exact path are proven when present
  - bounded strings identify any dri/search/provider hints from libglx.so, libGLX_mesa and swrast
  - no X server or official client is started
  - no canonical state access
  - one-shot workflow removed after capture
last_completed_step: PR #418 run 31965191048/job 95209182706 proved this Xvfb rejects -modulepath during argument parsing, eliminating explicit Xorg modulepath injection as a server correction
next_action: execute one read-only fixed-root Mesa/GLVND/DRI provider inventory; use the result to select at most one separately admitted Xvfb-only provider-search environment discriminator
---

# Track A contained Mesa/GLX provider inventory

Read-only support-filesystem evidence only. No X server or official client may be started and canonical runtime state must remain untouched.
