---
task_id: OTC-20260816-track-a-xvfb-modulepath-glx-probe
status: implementing
agent: ChatGPT
session_id: chatgpt-xvfb-modulepath-glx-20260816
session_role: runtime_infrastructure_researcher
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: runtime_discriminator
phase: isolated-xvfb-modulepath-glx
branch: diag/OTC-20260816-track-a-xvfb-modulepath-glx-probe
base_branch: main
base_main: d3f186414256151c9d5e03f34c5a9026b1fba500
risk: medium
updated: 2026-08-16T20:40:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-xvfb-modulepath-glx-probe.md
  - docs/agents/evidence/OTC-20260816-track-a-xvfb-modulepath-glx-probe/**
  - .github/workflows/tibia-official-client-re-xvfb-modulepath-glx-probe.yml
modules_touched: []
reuses:
  - PR #416 contained-Xvfb capability evidence as unpromoted research input only
  - PR #417 explicit-GLX differential as unpromoted research input only
  - exact contained Xvfb/libglx/module-root fences from those tasks
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: the exact contained Xvfb has GLX code and a contained libglx.so module, but default and explicit +extension GLX launches both advertise GLX absent; the accepted launch surface never binds Xvfb to the contained Xorg module tree, so one isolated modulepath discriminator is the next single-variable test
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260816-track-a-xvfb-modulepath-glx-probe
runtime_namespace: track-a-xvfb-modulepath-glx-probe-v1
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
  modulepath: /work/_otclient_tibia_re_state/toolroot/usr/lib/xorg/modules
  libglx: /work/_otclient_tibia_re_state/toolroot/usr/lib/xorg/modules/extensions/libglx.so
  libglx_sha256: 373b75559ee9a17449dfb84871bb7e5e306da7bd3aecd3282c7f03831ccf961a
  xkb_root: /work/_otclient_tibia_re_state/toolroot/usr/share/X11/xkb
  xkbcomp: /usr/bin/xkbcomp
  xkbcomp_sha256: 0967e7e7b03b077327cea74567726b265bd304b4fdf59f87bf7fdfe1074e7591
experiment:
  - start exactly one task-owned isolated Xvfb with the accepted environment
  - add exactly `-modulepath /work/_otclient_tibia_re_state/toolroot/usr/lib/xorg/modules` and `+extension GLX`
  - query core X11 extension list, GLX and RENDER presence
  - capture bounded Xvfb stderr for module/GLX/provider diagnostics
  - tear down and clean the task namespace
forbidden:
  - official client/package access
  - VNC/WARP/proxy
  - canonical lease/registration/session access
  - arbitrary process inventory
  - credentials/login/gameplay
  - Track B and historical PR #303 surfaces
acceptance:
  - exact Xvfb/libglx/xkbcomp fences pass before launch
  - selected display is free and task-owned
  - server args differ from #417 explicit-GLX case only by contained `-modulepath`
  - core-X11 query records GLX and RENDER
  - bounded stderr records module/GLX/provider diagnostics
  - cleanup completes
  - exactly one semantic physical workflow run; no retry after a valid discriminator
last_completed_step: PR #417 run 31965041300/job 95208804449 proved +extension GLX alone leaves GLX absent with an otherwise healthy Xvfb and RENDER extension
next_action: execute exactly one isolated contained-modulepath + GLX Xvfb probe, persist the sanitized result, remove the one-shot workflow, return mutation_authorized=false and hand the Draft to the coordinator
---

# Track A Xvfb modulepath GLX probe

Support-process-only discriminator. It must not launch the official client or touch canonical runtime state.
