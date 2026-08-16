---
task_id: OTC-20260816-track-a-xvfb-glx-enable-probe
status: implementing
agent: ChatGPT
session_id: chatgpt-xvfb-glx-enable-20260816
session_role: runtime_infrastructure_researcher
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: runtime_discriminator
phase: isolated-xvfb-glx-enable
branch: diag/OTC-20260816-track-a-xvfb-glx-enable-probe
base_branch: main
base_main: d3f186414256151c9d5e03f34c5a9026b1fba500
risk: medium
updated: 2026-08-16T20:35:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-xvfb-glx-enable-probe.md
  - docs/agents/evidence/OTC-20260816-track-a-xvfb-glx-enable-probe/**
  - .github/workflows/tibia-official-client-re-xvfb-glx-enable-probe.yml
modules_touched: []
reuses:
  - PR #416 contained-Xvfb capability evidence as unpromoted research input only
  - exact contained Xvfb SHA 2c7f5a9534410fed5092d782a69ca7ffd9fce80e98b81ffe4944d703dd11d3b1
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: read-only capability inventory proved the exact contained Xvfb has GLX server code, contained libGL dependency and libglx.so module while the prior isolated display advertised no GLX; one isolated Xvfb-only differential is required to test whether explicit +extension GLX changes the server extension state
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260816-track-a-xvfb-glx-enable-probe
runtime_namespace: track-a-xvfb-glx-enable-probe-v1
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
  official_client_allowed: false
  vnc_allowed: false
  warp_allowed: false
  track_b_access: false
exact_support_fence:
  toolroot: /work/_otclient_tibia_re_state/toolroot
  xvfb: /work/_otclient_tibia_re_state/toolroot/usr/bin/Xvfb
  xvfb_sha256: 2c7f5a9534410fed5092d782a69ca7ffd9fce80e98b81ffe4944d703dd11d3b1
  xkb_root: /work/_otclient_tibia_re_state/toolroot/usr/share/X11/xkb
  system_xkbcomp: /usr/bin/xkbcomp
  system_xkbcomp_sha256: 0967e7e7b03b077327cea74567726b265bd304b4fdf59f87bf7fdfe1074e7591
experiment:
  - start one task-owned default Xvfb with the accepted support environment and capture stderr plus core-X11 extension state
  - tear it down with ownership verification
  - start one task-owned Xvfb with the same environment plus exactly `+extension GLX`
  - capture stderr plus core-X11 extension state
  - tear it down completely
  - compare GLX and RENDER presence between the two subruns
forbidden:
  - official client launch or package access
  - VNC/WARP/proxy setup
  - canonical lease/registration/session access
  - arbitrary process inventory
  - credentials/login/gameplay
  - Track B and historical PR #303 surfaces
acceptance:
  - exact Xvfb and xkbcomp fences pass before launch
  - both displays are freshly selected and task-owned
  - default and explicit-GLX server use identical environment/args except `+extension GLX`
  - core-X11 ListExtensions/QueryExtension records GLX and RENDER for each subrun
  - bounded sanitized Xvfb stderr records GLX provider/init diagnostics
  - no official client/VNC/WARP/canonical state access
  - cleanup completes for both subruns
  - exactly one semantic physical workflow run; no retry after a valid discriminator
last_completed_step: PR #416 run 31964879003/job 95208403843 proved the contained Xvfb binary includes GLX code/options, contained libGL.so.1 and contained libglx.so/libglamoregl.so with direct dependencies resolved
next_action: execute exactly one isolated Xvfb-only default-vs-+extension-GLX differential, persist the sanitized result, remove the one-shot workflow, return mutation_authorized=false and hand the Draft to the coordinator
---

# Track A Xvfb GLX enable probe

Support-process discriminator only. No official Tibia client or canonical runtime surface may be touched.
