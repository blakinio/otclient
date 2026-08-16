---
task_id: OTC-20260816-track-a-xres-window-identity
status: ready
agent: ChatGPT
session_id: chatgpt-xres-window-identity-v2-20260816
session_role: runtime_identity_researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_discriminator
phase: coordinator-promotion-ready-helper-unavailable
branch: diag/OTC-20260816-track-a-xres-window-identity-v2
base_branch: main
base_main: 845adabba5f6d2bfecb6d54bc13834c47cc61c94
risk: high
updated: 2026-08-16T23:30:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-xres-window-identity.md
  - docs/agents/evidence/OTC-20260816-track-a-xres-window-identity/**
modules_touched: []
reuses:
  - PR #438 post-RHI raw-X11 evidence as unpromoted research input only
  - X-Resource protocol v1.2 / QueryClientIds(LocalClientPid) identity model
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: a physical XRes identity discriminator did launch once on replacement PR #442 under the pre-hardening gate and reached a valid new result plus cleanup before a newer hardening generation cancelled it during post-job handling. The observer proved libxcb and libX11 were available but libxcb-res.so.0 was unavailable in the bounded fixed library allowlist, so XRes PID identity could not be queried. The task is now terminal, fail-closed and must not launch the client again. One-shot workflow and both patchers have been removed.
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: heavy
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260816-track-a-xres-window-identity
runtime_namespace: track-a-xres-window-identity-v1
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
source_evidence:
  pr: 438
  run: 31972261899
  job: 95226396914
  classification: PROVEN_RAW_X11_TREE_HAS_VIEWABLE_1920X1080_NAMELESS_PIDLESS_WINDOW_FROM_T15_WHILE_XDOTOOL_NAMED_VISIBLE_SEARCH_RETURNS_ZERO_AND_EXACT_CLIENT_REMAINS_ALIVE_POST_GLX
source_xres_draft:
  pr: 440
  stale_base_physical_job: 95229185679
  stale_base_result: REFUSED_BEFORE_CLIENT_LAUNCH
  refusal: XRES_REFUSED_BASE_MOVED
  client_launch: false
replacement_pr:
  pr: 442
  base: 845adabba5f6d2bfecb6d54bc13834c47cc61c94
  semantic_run: 31973388722
  semantic_job: 95229260820
  runtime_admission: PASS
  exact_base_fence: PASS
  source_transform_fence: PASS
  support_fence: PASS
  exact_client_launch: true
  exact_client_launch_count_for_task: 1
  canonical_state_access: NONE
  cleanup: COMPLETE
  cancellation_after_result_cleanup: true
  generated_result: PASS_DISCRIMINATOR_CAPTURED
xres_result:
  helper_t05: libxcb_true_libxcb_res_false_libX11_true
  helper_t15: libxcb_true_libxcb_res_false_libX11_true
  helper_t35: libxcb_true_libxcb_res_false_libX11_true
  query_client_ids_executed: false
  viewable_xid_pid_identity: UNKNOWN
  final_classification: XRES_IDENTITY_UNRESOLVED
  bounded_classification: PROVEN_XRES_IDENTITY_UNRESOLVED_BECAUSE_LIBXCB_RES_HELPER_UNAVAILABLE_ON_RUNNER_FIXED_ALLOWLIST
raw_x11_reconfirmation:
  viewable_1920x1080_window_present: true
  exact_client_alive_through_t35: true
  xdotool_named_visible_count: 0
  exact_client_ownership_of_viewable_xid: UNKNOWN
safety_hardening:
  unsafe_pr_body_substring_gate_identified: true
  replacement_gate: authorized_branch_suffix
  cancel_in_progress_enabled: true
  hardening_commit: c4613fa3b5e4e4547f5d378a2ea3f7c1a4401987
  hardening_workflow_run: 31973490169
  hosted_preflight: SUCCESS
  physical_job: SKIPPED
  one_shot_workflow_removed: true
  patchers_removed: true
  second_client_launch_authorized: false
forbidden:
  - any second exact-client launch from this task
  - canonical bootstrap retry
  - canonical worker window-identity relaxation
  - canonical lease/registration/session access
  - credentials, login or gameplay
  - Track B and historical PR #303 runtime surfaces
acceptance:
  - one physical XRes discriminator captured: PASS
  - helper availability classified without inference: PASS
  - viewable-window ownership remains explicitly UNKNOWN: PASS
  - cleanup complete: PASS
  - hardened follow-up physical job skipped: PASS
  - workflow and patchers removed: PASS
  - mutation authorization returned false: PASS
  - no second run: PASS
evidence:
  - docs/agents/evidence/OTC-20260816-track-a-xres-window-identity/20260816-xres-helper-unavailable.md
last_completed_step: replacement #442 run 31973388722 / job 95229260820 launched the exact isolated client once, reproduced the raw viewable window and proved the selected XRes helper could not resolve libxcb-res.so.0; discriminator result and cleanup completed before cancellation during post-job hardening; later hardened run 31973490169 skipped physical execution and all one-shot files were removed
next_action: coordinator-promote/archive this bounded helper-unavailable evidence. Separately admit a support-only read-only library/protocol capability inventory for libxcb-res.so*, libXRes.so* and raw X-Resource protocol feasibility. Do not launch the official client again until a new helper path is statically proven.
---

# Track A XRes window identity — terminal source

The ownership question remains open because the convenience XCB RES helper library was unavailable. The next step is support-only capability discovery, not another client launch.
