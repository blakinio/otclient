---
task_id: OTC-20260816-track-a-xvfb-dri-path-default-glx
status: ready
agent: ChatGPT
session_id: chatgpt-coord-xvfb-dri-proof-20260816-2120
session_role: promotion_integration_coordinator
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: runtime_discriminator
phase: coordinator-promotion-ready
branch: docs/OTC-20260816-track-a-xvfb-dri-path-default-glx-promote
base_branch: main
base_main: e398337d887a7b498f13859bc17f989f74a81d22
current_main: e398337d887a7b498f13859bc17f989f74a81d22
risk: medium
updated: 2026-08-16T21:20:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-xvfb-dri-path-default-glx.md
  - docs/agents/evidence/OTC-20260816-track-a-xvfb-dri-path-default-glx/**
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: coordinator promotion replays already-produced durable Xvfb-only evidence; no runtime process is started by this session
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: false
owner_funded_ai_api_authorized: false
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
source_research:
  pr: 421
  final_head: a359ab908772e95e1dbae850f6ef4de1738cbf05
  dispatch_head: 082be738559dcb16ba342086cfc48fcc8c2d724d
  coordinator_decision: ACCEPT
  material_findings_open: 0
physical_evidence:
  runtime_access: ephemeral_isolated
  namespace: track-a-xvfb-dri-path-default-glx-v1
  runner: synology-otclient-01
  governance_run: 31965779562
  governance_result: SUCCESS
  semantic_run: 31965779546
  semantic_job: 95210624747
  semantic_result: SUCCESS
  client_started: false
  vnc_started: false
  warp_started: false
  canonical_state_access: NONE
  cleanup: COMPLETE
  support_fence: PASS
  explicit_glx_flag: false
  libgl_drivers_path: /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri
  server_started: true
  extension_count: 23
  glx_present: true
  glx_major_opcode: 150
  render_present: true
  render_major_opcode: 139
  server_log_lines: 19
  server_log_material_errors: 0
result:
  classification: PROVEN_LIBGL_DRIVERS_PATH_ALONE_ENABLES_GLX_UNDER_CURRENT_CANONICAL_XVFB_ARGUMENTS
  baseline_without_dri_path_extension_count: 22
  baseline_without_dri_path_glx_present: false
  minimal_worker_change: LIBGL_DRIVERS_PATH_ONLY
  add_explicit_extension_flag: false
  official_client_success_claimed: false
evidence:
  - docs/agents/evidence/OTC-20260816-track-a-xvfb-dri-path-default-glx/20260816-dri-path-alone-enables-glx.md
promotion:
  pr: 427
  source_pr: 421
  replay_method: exact source task/evidence blobs onto current main without source branch history
  initial_replay_head: 0652e9f342faa13bf21e5d02721b1ce470120c7a
  final_checkpoint_head: PENDING_AFTER_THIS_UPDATE
validation:
  source_track_a_governance_run: 31965851223
  source_track_a_governance_result: SUCCESS
  source_repository_ci_run: 31965851220
  source_repository_ci_result: SUCCESS
  source_required_ci_job: 95210823079
  source_required_ci_result: SUCCESS
  coordinator_log_cross_check: PASS
  promotion_exact_head_track_a_governance: PENDING
  promotion_exact_head_repository_ci: PENDING
  review_threads_open: 0
  physical_e2e: PASS
  physical_e2e_evidence: run 31965779546 / job 95210624747
audit:
  result: PASS
  material_findings_open: 0
acceptance:
  - current-worker-shaped Xvfb arguments preserved: PASS
  - only LIBGL_DRIVERS_PATH added: PASS
  - no explicit GLX flag: PASS
  - GLX present with opcode 150: PASS
  - RENDER preserved: PASS
  - no official client/VNC/WARP/canonical state: PASS
  - cleanup: PASS
  - conclusion limited to Xvfb capability, not client success: PASS
last_completed_step: coordinator independently inspected semantic job 95210624747 and confirmed that the exact contained Xvfb advertised GLX only after adding the contained LIBGL_DRIVERS_PATH while preserving the canonical argument list and starting no official client
next_action: obtain exact-head governance/CI for PR #427, close source #421 superseded, merge #427 after branch-protection gates, archive this task, then review the separate hosted implementation Draft #423 against the promoted proof and current main
---

# Track A Xvfb DRI-path minimality proof — coordinator promotion

This promotion consumes durable support-only evidence. It grants no canonical runtime authority and does not authorize an official-client bootstrap retry by itself.
