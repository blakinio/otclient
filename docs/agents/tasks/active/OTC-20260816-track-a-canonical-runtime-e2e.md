---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: ready
agent: ChatGPT
session_id: chatgpt-coord-xres-child-archive-20260817
session_role: promotion_integration_coordinator
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: raw-xres-helper-hosted-ready
branch: docs/OTC-20260817-track-a-xres-child-archive
base_branch: main
base_main: 7540a679420689c388d9d11125c9fd8846956a10
risk: high
updated: 2026-08-17T08:32:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/**
modules_touched: []
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-bootstrap-implementation.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-xvfb-dri-path-fix.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-dri-repair-isolated-client-revalidation.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-xres-window-identity.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-xres-support-inventory.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: coordinator promotion #444 merged the independently audited post-RHI raw-X11, XRes helper-unavailable and corrected XRes support evidence. Source Drafts #438/#442/#443 are closed superseded. The two bounded XRes child tasks are archived and ownership-released by this lifecycle branch. The remaining canonical task now has one causal next step: a GitHub-hosted raw-XRes encoder/parser derived from the promoted observed XResproto wire layout, without Xvfb/client/canonical state access. Physical identity retry remains forbidden until that helper is validated and separately admitted.
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
promotion_chain:
  coordinator_promotion_pr: 444
  coordinator_promotion_head: 32b7cca056c875429db4f2a167385f7b95335b81
  coordinator_promotion_merge: 7540a679420689c388d9d11125c9fd8846956a10
  source_pr_438: CLOSED_SUPERSEDED_ACCEPTED
  source_pr_442: CLOSED_SUPERSEDED_ACCEPTED
  source_pr_443: CLOSED_SUPERSEDED_ACCEPTED_WITH_EDITS
  promotion_governance_run: 32000325932
  pre_ready_ci_run: 32000326108
  pre_ready_required_ci_job: 95299301299
  ready_ci_run: 32000366565
  ready_required_ci_job: 95299428625
  promotion_review_threads_open: 0
promoted_window_identity_frontier:
  glx_present: true
  raw_viewable_full_display_xid_present: true
  raw_viewable_xid: 0x00c00011
  raw_viewable_geometry: 1920x1080
  xdotool_named_visible_count: 0
  exact_client_pid_ownership_of_viewable_xid: UNKNOWN
  convenience_libxcb_res_present: false
  convenience_libXRes_present: false
  contained_XResproto_present: true
  observed_query_client_ids_minor_opcode: 4
  observed_local_client_pid_mask: 0x02
  observed_query_client_ids_request_fixed_size: 8
  observed_query_client_ids_reply_fixed_size: 32
  raw_xres_helper_implementation_validated: false
safety:
  canonical_bootstrap_retry_authorized: false
  canonical_window_identity_relaxation_authorized: false
  physical_identity_retry_authorized: false
  credentials_allowed: false
  login_allowed: false
  gameplay_allowed: false
  track_b_access: false
forbidden:
  - any physical Synology/Xvfb/official-client execution before host-side raw-XRes helper validation and fresh separate admission
  - canonical lease/registration/session observation or mutation during hosted helper work
  - accepting a viewable XID as official-client-owned without direct resource/PID identity proof
  - canonical bootstrap retry
  - canonical window identity relaxation
  - credentials, login or gameplay
  - Track B and historical PR #303 runtime surfaces
acceptance_for_next_phase:
  - implement pure hosted/static QueryVersion request encoder and reply parser from promoted observed wire constants
  - implement pure hosted/static QueryClientIds request encoder for one resource XID and LocalClientPid mask
  - implement bounded QueryClientIds reply parser with strict lengths/counts/mask validation
  - include deterministic positive/negative/truncated/oversized/wrong-version fixtures
  - no network/X server/client/canonical runtime access in helper validation
  - pass exact-head Track A governance and repository CI
  - only then create a separately admitted physical identity discriminator
last_completed_step: coordinator promotion #444 merged as 7540a679420689c388d9d11125c9fd8846956a10; source Drafts #438/#442/#443 were closed superseded; child task archive/release is staged on the current lifecycle branch
next_action: merge the child-task archive/release PR, then continue this same canonical task by implementing and validating a GitHub-hosted raw-XRes QueryVersion/QueryClientIds encoder-parser with deterministic fixtures and no physical runtime access.
---

# Track A canonical runtime E2E — raw-XRes helper frontier

The remaining unknown is exact resource-to-PID ownership of the proven viewable X11 window. The next phase is purely hosted protocol-helper validation; another physical client run remains forbidden until that helper passes.
