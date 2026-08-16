---
task_id: OTC-20260816-track-a-xvfb-dri-path-default-glx
status: ready
agent: ChatGPT
session_id: chatgpt-xvfb-dri-path-default-glx-20260816
session_role: runtime_infrastructure_researcher
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: runtime_discriminator
phase: coordinator-promotion-ready
branch: diag/OTC-20260816-track-a-xvfb-dri-path-default-glx
base_branch: main
base_main: d3f186414256151c9d5e03f34c5a9026b1fba500
risk: medium
updated: 2026-08-16T20:57:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-xvfb-dri-path-default-glx.md
  - docs/agents/evidence/OTC-20260816-track-a-xvfb-dri-path-default-glx/**
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
execution_reason: PR #420 proved LIBGL_DRIVERS_PATH enables GLX with explicit +extension GLX; this final isolated support-process discriminator proved the DRI path alone enables GLX under the current canonical worker's existing Xvfb argument surface
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
  pr: 421
  dispatch_head: 082be738559dcb16ba342086cfc48fcc8c2d724d
  governance_run: 31965779562
  governance_result: SUCCESS
  semantic_run: 31965779546
  semantic_job: 95210624747
  semantic_result: SUCCESS
  canonical_state_access: NONE
  client_started: false
  vnc_started: false
  warp_started: false
  cleanup: COMPLETE
result:
  classification: PROVEN_LIBGL_DRIVERS_PATH_ALONE_ENABLES_GLX_UNDER_CURRENT_CANONICAL_XVFB_ARGUMENTS
  explicit_glx_flag: false
  libgl_drivers_path: /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri
  server_started: true
  extension_count: 23
  glx_present: true
  glx_major_opcode: 150
  render_present: true
  render_major_opcode: 139
  baseline_without_dri_path_extension_count: 22
  baseline_without_dri_path_glx_present: false
  minimal_worker_change: LIBGL_DRIVERS_PATH_ONLY
  add_explicit_extension_flag: false
one_shot_workflow_removed: true
evidence:
  - docs/agents/evidence/OTC-20260816-track-a-xvfb-dri-path-default-glx/20260816-dri-path-alone-enables-glx.md
audit:
  result: PASS_PENDING_EXACT_FINAL_HEAD_CHECKS
  material_findings_open: 0
  notes:
    - dispatch-head governance passed
    - the experiment preserved current canonical worker Xvfb arguments and added only LIBGL_DRIVERS_PATH
    - no official client/VNC/WARP/canonical state was touched
    - one-shot workflow removed before terminal evidence/task commits
acceptance:
  - exact support fences: PASS
  - current-worker-shaped Xvfb args: PASS
  - single provider variable: PASS
  - GLX/RENDER capture: PASS
  - no client/VNC/WARP/canonical state: PASS
  - cleanup: PASS
  - exactly one semantic physical workflow run: PASS
last_completed_step: run 31965779546/job 95210624747 proved LIBGL_DRIVERS_PATH alone, with no +extension GLX, enables GLX under the exact current canonical worker Xvfb arguments
next_action: coordinator-promote/archive this Draft after exact-final-head checks; implement/test a minimal GitHub-hosted canonical-worker repair that fail-closed validates the selected toolroot DRI directory/swrast and exports only LIBGL_DRIVERS_PATH to Xvfb without adding +extension GLX
---

# Track A default-Xvfb DRI-path proof — terminal candidate

The minimal production change is now exact: bind the selected contained DRI directory into the Xvfb environment; do not change the Xvfb argument list.