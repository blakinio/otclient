---
task_id: OTC-20260816-track-a-xvfb-libgl-drivers-path
status: ready
agent: ChatGPT
session_id: chatgpt-xvfb-libgl-drivers-path-20260816
session_role: runtime_infrastructure_researcher
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: runtime_discriminator
phase: coordinator-promotion-ready
branch: diag/OTC-20260816-track-a-xvfb-libgl-drivers-path
base_branch: main
base_main: d3f186414256151c9d5e03f34c5a9026b1fba500
risk: medium
updated: 2026-08-16T20:52:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-xvfb-libgl-drivers-path.md
  - docs/agents/evidence/OTC-20260816-track-a-xvfb-libgl-drivers-path/**
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
execution_reason: the contained GLX provider stack is present and Xorg libglx supports LIBGL_DRIVERS_PATH; this single-variable Xvfb-only experiment directly proved binding the contained DRI directory changes GLX from absent to present
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
mutation_authorized: false
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
execution:
  pr: 420
  dispatch_head: 74650474e73f4418681a52c46bf524ba878a3080
  governance_run: 31965565693
  governance_result: SUCCESS
  semantic_run: 31965565953
  semantic_job: 95210097816
  semantic_result: SUCCESS
  canonical_state_access: NONE
  client_started: false
  vnc_started: false
  warp_started: false
  cleanup: COMPLETE
result:
  classification: PROVEN_CONTAINED_LIBGL_DRIVERS_PATH_CAUSALLY_ENABLES_GLX_ON_EXACT_XVFB
  baseline_pr417_glx_present: false
  baseline_pr417_extension_count: 22
  libgl_drivers_path: /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri
  swrast_resolved: /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri/libdril_dri.so
  server_started: true
  extension_count: 23
  glx_present: true
  glx_major_opcode: 150
  render_present: true
  render_major_opcode: 139
  causal_variable: LIBGL_DRIVERS_PATH
  canonical_bootstrap_retry_authorized: false
one_shot_workflow_removed: true
evidence:
  - docs/agents/evidence/OTC-20260816-track-a-xvfb-libgl-drivers-path/20260816-libgl-drivers-path-enables-glx.md
audit:
  result: PASS_PENDING_EXACT_FINAL_HEAD_CHECKS
  material_findings_open: 0
  notes:
    - dispatch-head governance passed both admission audits
    - the experiment changed one provider variable relative to the #417 explicit-GLX case
    - no official client/VNC/WARP/canonical state was touched
    - one-shot workflow removed before terminal evidence/task commits
acceptance:
  - exact Xvfb/swrast/xkbcomp fences: PASS
  - task-owned isolated display: PASS
  - single provider variable: PASS
  - core-X11 GLX/RENDER capture: PASS
  - no client/VNC/WARP/canonical state: PASS
  - cleanup: PASS
  - exactly one semantic physical workflow run: PASS
last_completed_step: run 31965565953/job 95210097816 directly proved the contained LIBGL_DRIVERS_PATH increases Xvfb extension count 22 to 23 and enables GLX with opcode 150 while preserving RENDER
next_action: coordinator-promote/archive this Draft after exact-final-head checks; separately implement/test a minimal GitHub-hosted canonical-worker repair that derives and validates the contained DRI root from the selected toolroot and exports it as LIBGL_DRIVERS_PATH to Xvfb, with no physical runtime execution in the implementation PR
---

# Track A Xvfb LIBGL_DRIVERS_PATH proof — terminal candidate

The missing GLX prerequisite now has a direct causal repair. The next step is a hosted-only worker change, not another physical runtime experiment.