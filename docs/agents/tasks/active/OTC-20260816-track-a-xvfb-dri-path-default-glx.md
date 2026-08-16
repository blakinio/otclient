---
task_id: OTC-20260816-track-a-xvfb-dri-path-default-glx
status: implementing
agent: ChatGPT
session_id: chatgpt-xvfb-dri-path-default-glx-20260816
session_role: runtime_infrastructure_researcher
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: runtime_discriminator
phase: isolated-xvfb-dri-path-default-extension-state
branch: diag/OTC-20260816-track-a-xvfb-dri-path-default-glx
base_branch: main
base_main: d3f186414256151c9d5e03f34c5a9026b1fba500
risk: medium
updated: 2026-08-16T20:54:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-xvfb-dri-path-default-glx.md
  - docs/agents/evidence/OTC-20260816-track-a-xvfb-dri-path-default-glx/**
  - .github/workflows/tibia-official-client-re-xvfb-dri-path-default-glx.yml
modules_touched: []
reuses:
  - PR #417 default/explicit GLX Xvfb differential as unpromoted research input only
  - PR #420 LIBGL_DRIVERS_PATH causal proof as unpromoted research input only
  - exact contained Xvfb/swrast/xkbcomp fences from those tasks
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: PR #420 proved LIBGL_DRIVERS_PATH enables GLX when +extension GLX is present; the current canonical worker has neither setting, so one final isolated support-process discriminator must determine whether the DRI path alone enables GLX under the worker's existing default Xvfb arguments
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260816-track-a-xvfb-dri-path-default-glx
runtime_namespace: track-a-xvfb-dri-path-default-glx-v1
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
  xvfb: /work/_otclient_tibia_re_state/toolroot/usr/bin/Xvfb
  xvfb_sha256: 2c7f5a9534410fed5092d782a69ca7ffd9fce80e98b81ffe4944d703dd11d3b1
  dri_root: /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri
  swrast_sha256: c28638b02783ebc96a78bb982fe59ad0d54230bc1faf53305af33edab29cd388
  xkbcomp_sha256: 0967e7e7b03b077327cea74567726b265bd304b4fdf59f87bf7fdfe1074e7591
experiment:
  baseline: current canonical worker Xvfb arguments and environment
  only_new_variable: LIBGL_DRIVERS_PATH=/work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri
  explicit_glx_flag: false
  forbidden_provider_overrides:
    - LIBGL_ALWAYS_SOFTWARE
    - GALLIUM_DRIVER
    - MESA_LOADER_DRIVER_OVERRIDE
acceptance:
  - exact support fences pass
  - task-owned isolated display only
  - server arguments match current canonical worker Xvfb arguments exactly
  - LIBGL_DRIVERS_PATH is the only new graphics/provider variable
  - core-X11 GLX/RENDER state captured
  - bounded provider stderr captured
  - no official client/VNC/WARP/canonical state
  - cleanup complete
  - exactly one semantic physical workflow run
last_completed_step: PR #420 proved LIBGL_DRIVERS_PATH plus explicit +extension GLX changes the exact contained Xvfb from GLX absent to GLX present
next_action: execute one Xvfb-only run with the DRI path but without +extension GLX; if GLX is present, the hosted worker repair needs only LIBGL_DRIVERS_PATH; otherwise it needs both the environment variable and explicit extension flag
---

# Track A default-Xvfb DRI-path discriminator

This task resolves the final minimality question before changing the canonical worker.