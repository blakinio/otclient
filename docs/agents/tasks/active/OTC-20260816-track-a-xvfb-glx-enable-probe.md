---
task_id: OTC-20260816-track-a-xvfb-glx-enable-probe
status: ready
agent: ChatGPT
session_id: chatgpt-xvfb-glx-enable-20260816
session_role: runtime_infrastructure_researcher
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: runtime_discriminator
phase: coordinator-promotion-ready
branch: diag/OTC-20260816-track-a-xvfb-glx-enable-probe
base_branch: main
base_main: d3f186414256151c9d5e03f34c5a9026b1fba500
risk: medium
updated: 2026-08-16T20:39:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-xvfb-glx-enable-probe.md
  - docs/agents/evidence/OTC-20260816-track-a-xvfb-glx-enable-probe/**
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
execution_reason: read-only capability inventory proved the exact contained Xvfb has GLX server code, contained libGL dependency and libglx.so module while the prior isolated display advertised no GLX; one isolated Xvfb-only differential tested whether explicit +extension GLX changes the server extension state
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
execution:
  pr: 417
  dispatch_head: 6ade6bf38131a325935686c9766f1545afd196d9
  governance_run: 31965041248
  governance_result: SUCCESS
  semantic_run: 31965041300
  semantic_job: 95208804449
  semantic_result: SUCCESS
  canonical_state_access: NONE
  client_started: false
  vnc_started: false
  warp_started: false
  cleanup: COMPLETE
result:
  classification: PROVEN_EXPLICIT_GLX_FLAG_DOES_NOT_ENABLE_GLX_ON_CURRENT_CONTAINED_XVFB_ENVIRONMENT
  default_server_started: true
  default_extension_count: 22
  default_glx_present: false
  default_render_present: true
  explicit_glx_server_started: true
  explicit_glx_extension_count: 22
  explicit_glx_present: false
  explicit_glx_render_present: true
  extension_lists_identical: true
  explicit_glx_provider_log_present: false
  explicit_glx_hypothesis_disproven: true
one_shot_workflow_removed: true
evidence:
  - docs/agents/evidence/OTC-20260816-track-a-xvfb-glx-enable-probe/20260816-default-vs-explicit-glx.md
audit:
  result: PASS_PENDING_EXACT_FINAL_HEAD_CHECKS
  material_findings_open: 0
  notes:
    - dispatch-head fresh admission behavior and deterministic policy audits both passed
    - exactly one semantic physical workflow run executed
    - official client/VNC/WARP/canonical state were excluded
    - one-shot workflow removed before terminal evidence/task commits
acceptance:
  - exact Xvfb and xkbcomp fences: PASS
  - default and explicit GLX Xvfb subruns captured: PASS
  - core-X11 GLX/RENDER comparison: PASS
  - bounded server stderr: PASS
  - no client/VNC/WARP/canonical state: PASS
  - cleanup: PASS
  - exactly one semantic workflow run: PASS
last_completed_step: run 31965041300/job 95208804449 proved explicit +extension GLX does not change the contained Xvfb extension list: both default and explicit cases advertise 22 extensions with GLX absent and RENDER present
next_action: coordinator-promote/archive this Draft after exact-final-head checks; separately admit one Xvfb-only contained-modulepath discriminator using `-modulepath /work/_otclient_tibia_re_state/toolroot/usr/lib/xorg/modules +extension GLX`, without official client/VNC/WARP or canonical state access
---

# Track A Xvfb GLX enable probe — terminal candidate

The command-line extension flag is not sufficient. The next variable is explicit binding of Xvfb to the contained Xorg module tree that contains `libglx.so`.