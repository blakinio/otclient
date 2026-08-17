---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: ready
agent: ChatGPT
session_id: chatgpt-coord-window-xres-promotion-20260817
session_role: promotion_integration_coordinator
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: coordinator-promotion-post-rhi-xres-chain
branch: docs/OTC-20260817-track-a-window-xres-promotion
base_branch: main
base_main: 845adabba5f6d2bfecb6d54bc13834c47cc61c94
risk: high
updated: 2026-08-17T08:20:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/**
modules_touched: []
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-bootstrap-implementation.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-xvfb-dri-path-fix.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-dri-repair-isolated-client-revalidation.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - source Draft #438 post-RHI window-state evidence
  - source Draft #442 XRes identity helper-unavailable evidence
  - source Draft #443 XRes support inventory evidence
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: coordinator review independently re-read the raw physical/support job logs for Drafts #438, #442 and #443. #438 and #442 are ACCEPT. #443 is ACCEPT_WITH_EDITS because its source Markdown contained two library hashes inconsistent with the raw job and an unsupported header digest; the promoted evidence corrects those fields without changing the helper-availability classification. Current work is promotion-only and grants no physical runtime authority. The next causal phase is a hosted/static raw-XRes encoder/parser before any new client launch.
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
validation_level: heavy
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
runner: github-hosted
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
persistent_session_role: none
physical_e2e_required: true
owner_funded_ai_api_authorized: false
runtime_nonclaims:
  current_canonical_display: UNKNOWN
  current_canonical_vnc_endpoint: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
  canonical_registration_authority: ABSENT_OR_UNPROVEN
promoted_bootstrap_governance:
  bootstrap_implementation_pr: 371
  bootstrap_archive_pr: 375
  admission_reconciliation_pr: 436
  admission_reconciliation_merge: b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4
  status: IMPLEMENTED_AND_GOVERNABLE
  blind_bootstrap_retry_authorized: false
promoted_graphics_prerequisite:
  dri_repair_pr: 429
  dri_repair_archive_pr: 430
  isolated_revalidation_source_pr: 431
  isolated_revalidation_promotion_pr: 432
  isolated_revalidation_archive_pr: 434
  x11_glx_present: true
  prior_qxcb_no_glx_egl_failure_removed: true
post_rhi_window_evidence:
  source_pr: 438
  coordinator_decision: ACCEPT
  final_source_head: 171fbfa679c8c75dc9722fe39c19141962282f01
  semantic_run: 31972261899
  semantic_job: 95226396914
  cleanup: COMPLETE
  canonical_state_access: NONE
  glx_present: true
  glx_opcode: 150
  render_present: true
  render_opcode: 139
  exact_client_alive_t05_t15_t35: true
  raw_viewable_window_t15_t35: true
  viewable_xid: 0x00c00011
  viewable_geometry: 1920x1080
  xdotool_named_visible_count_t05_t15_t35: 0
  xdotool_pid_name_class_binding: ABSENT
  exact_client_ownership_of_viewable_xid: UNKNOWN
  opengl_context_created: true
  opengl_renderer: Mesa_llvmpipe
  qrhi_vulkan_initialized: true
  qtquick_window_loaded: true
  qobject_cross_thread_warning_present: true
  qobject_cross_thread_warning_causal: UNKNOWN
  classification: PROVEN_RAW_X11_TREE_HAS_VIEWABLE_1920X1080_NAMELESS_PIDLESS_WINDOW_FROM_T15_WHILE_XDOTOOL_NAMED_VISIBLE_SEARCH_RETURNS_ZERO_AND_EXACT_CLIENT_REMAINS_ALIVE_POST_GLX
xres_identity_evidence:
  source_pr: 442
  coordinator_decision: ACCEPT
  final_source_head: 80bd75a1352ef1ffe84c3dcc34bf51a0cf0a7c54
  semantic_run: 31973388722
  semantic_job: 95229260820
  runtime_admission: PASS
  exact_client_launch_count: 1
  cleanup: COMPLETE
  helper_t05_t15_t35: libxcb_true_libxcb_res_false_libX11_true
  query_client_ids_executed: false
  exact_client_ownership_of_viewable_xid: UNKNOWN
  classification: PROVEN_XRES_IDENTITY_UNRESOLVED_BECAUSE_LIBXCB_RES_HELPER_UNAVAILABLE_ON_RUNNER_FIXED_ALLOWLIST
  hardened_followup_run: 31973490169
  hardened_followup_physical_job: SKIPPED
xres_support_evidence:
  source_pr: 443
  coordinator_decision: ACCEPT_WITH_EDITS
  final_source_head: 02c63797b0835ea745a08362c12874307129a9d1
  support_run: 31973740033
  support_job: 95230007324
  runtime_access: read_only
  xserver_started: false
  client_started: false
  canonical_state_access: NONE
  libxcb_res_present: false
  libXRes_present: false
  contained_libxcb_present: true
  contained_libX11_present: true
  XResproto_header_present: true
  xcb_res_generated_header_present: false
  XRes_public_header_present: false
  pkgconfig_present: false
  observed_query_client_ids_minor_opcode: 4
  observed_local_client_pid_mask: 0x02
  observed_query_client_ids_request_fixed_size: 8
  observed_query_client_ids_reply_fixed_size: 32
  promoted_libxcb_sha256: 7958a0136b121bdc4c708968569ad152a9ed208ab026e2537b1005dde64ca440
  promoted_libX11_sha256: c5b5d782bd9cab3420a62df88f5c991507edf3331a89f98464ddbc538c37b879
  XResproto_sha256: NOT_CAPTURED
  classification: HEADERS_PROTOCOL_BASIS_PRESENT_NO_HELPER_LIBRARY
coordinator_review:
  evidence_file: docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/20260817-window-xres-coordinator-review.md
  material_findings_open: 0
  corrected_source_claims:
    - Draft #443 libxcb hash corrected to raw job value
    - Draft #443 libX11 hash corrected to raw job value
    - unsupported XResproto header digest removed
    - system/core library path wording corrected to avoid false contained-path resolution claim
safety:
  canonical_bootstrap_retry_authorized: false
  canonical_window_identity_relaxation_authorized: false
  second_xres_client_launch_authorized: false
  credentials_allowed: false
  login_allowed: false
  gameplay_allowed: false
  track_b_access: false
forbidden:
  - physical Synology execution from the coordinator promotion branch
  - canonical lease/registration/session observation or mutation from the coordinator promotion branch
  - accepting any viewable 1920x1080 XID as the official client without direct resource/PID identity proof
  - another official-client launch before a raw-XRes helper is validated host-side and separately admitted
  - credentials, login or gameplay
  - Track B or historical PR #303 runtime surfaces
acceptance:
  - source #438 raw job independently cross-checked and bounded classification accepted
  - source #442 raw job independently cross-checked and bounded helper-unavailable classification accepted
  - source #443 raw job independently cross-checked and source evidence inconsistencies corrected
  - promoted evidence contains no temporary workflow/runtime code
  - exact current-main promotion branch owns only task/evidence paths
  - Track A governance and repository CI pass on exact promotion head
  - source Drafts become intentionally terminal after accepted promotion
  - child tasks #442/#443 are archived and ownership released after promotion merge
  - canonical task remains active and fail-closed for the next causal phase
last_completed_step: coordinator independently falsified source Draft #438/#442/#443 claims against raw jobs 95226396914, 95229260820 and 95230007324, accepted #438/#442, accepted #443 with evidence corrections, and staged a docs/evidence-only current-main promotion bundle
next_action: validate and merge the coordinator promotion bundle; close source Drafts #438/#442/#443 superseded by the promotion; archive/release the two bounded child tasks; then continue this canonical task with a hosted/static raw-XRes QueryVersion/QueryClientIds encoder-parser validation before any new physical identity run.
---

# Track A canonical runtime E2E — window/XRes promotion checkpoint

The current blocker is identity, not basic graphics initialization. A raw full-display X11 window is proven, but its exact client PID ownership remains unresolved because convenience XRes client libraries are absent. The contained protocol header provides the next hosted/static path; no canonical or physical retry is authorized from this checkpoint.
