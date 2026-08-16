---
task_id: OTC-20260816-track-a-xvfb-libgl-drivers-path
status: implementing
agent: ChatGPT
session_id: chatgpt-xvfb-libgl-drivers-path-20260816
session_role: runtime_infrastructure_researcher
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: runtime_discriminator
phase: isolated-xvfb-libgl-drivers-path
branch: diag/OTC-20260816-track-a-xvfb-libgl-drivers-path
base_branch: main
base_main: d3f186414256151c9d5e03f34c5a9026b1fba500
risk: medium
updated: 2026-08-16T20:49:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-xvfb-libgl-drivers-path.md
  - docs/agents/evidence/OTC-20260816-track-a-xvfb-libgl-drivers-path/**
  - .github/workflows/tibia-official-client-re-xvfb-libgl-drivers-path.yml
modules_touched: []
reuses:
  - PR #417 explicit-GLX differential as unpromoted research input only
  - PR #419 Mesa/GLVND/DRI provider inventory as unpromoted research input only
  - exact contained Xvfb and swrast provider fences from those tasks
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: the contained GLX provider stack is present with zero missing direct dependencies and Xorg libglx explicitly supports LIBGL_DRIVERS_PATH; default and explicit-GLX Xvfb launches still advertise GLX absent, so the next single-variable test binds the proven contained DRI provider directory
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260816-track-a-xvfb-libgl-drivers-path
runtime_namespace: track-a-xvfb-libgl-drivers-path-v1
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
  official_client_allowed: false
  vnc_allowed: false
  warp_allowed: false
  credentials_allowed: false
  login_allowed: false
  gameplay_allowed: false
  track_b_access: false
exact_support_fence:
  toolroot: /work/_otclient_tibia_re_state/toolroot
  xvfb: /work/_otclient_tibia_re_state/toolroot/usr/bin/Xvfb
  xvfb_sha256: 2c7f5a9534410fed5092d782a69ca7ffd9fce80e98b81ffe4944d703dd11d3b1
  dri_root: /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri
  swrast_resolved: /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri/libdril_dri.so
  swrast_sha256: c28638b02783ebc96a78bb982fe59ad0d54230bc1faf53305af33edab29cd388
  xkb_root: /work/_otclient_tibia_re_state/toolroot/usr/share/X11/xkb
  xkbcomp: /usr/bin/xkbcomp
  xkbcomp_sha256: 0967e7e7b03b077327cea74567726b265bd304b4fdf59f87bf7fdfe1074e7591
experiment:
  baseline_reference: PR #417 explicit +extension GLX case
  only_new_variable: LIBGL_DRIVERS_PATH=/work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri
  server_args: identical to #417 explicit-GLX Xvfb case including +extension GLX
  observation:
    - core-X11 GLX and RENDER extension state
    - bounded Xvfb stderr for GLX/AIGLX/swrast/renderer/dlopen/driver/provider lines
forbidden:
  - LIBGL_ALWAYS_SOFTWARE
  - GALLIUM_DRIVER
  - MESA_LOADER_DRIVER_OVERRIDE
  - official client/package access
  - VNC/WARP/proxy
  - canonical state access
  - credentials/login/gameplay
  - Track B and historical PR #303 surfaces
acceptance:
  - exact Xvfb/swrast/xkbcomp fences pass
  - task-owned isolated display only
  - LIBGL_DRIVERS_PATH is the only new provider variable relative to #417 explicit-GLX case
  - GLX/RENDER query and bounded provider stderr captured
  - no client/VNC/WARP/canonical state
  - cleanup complete
  - exactly one semantic physical workflow run; no retry after valid discriminator
last_completed_step: PR #419 run 31965397353/job 95209684373 proved the contained Mesa/GLVND/swrast stack is present and direct-dependency complete, and Xorg libglx contains the LIBGL_DRIVERS_PATH provider-search override
next_action: execute exactly one Xvfb-only explicit-GLX run with the proven contained LIBGL_DRIVERS_PATH, persist result, remove the one-shot workflow, return mutation_authorized=false, and hand the Draft to coordinator
---

# Track A Xvfb LIBGL_DRIVERS_PATH discriminator

One-variable support-process experiment only. No official client or canonical runtime access.
