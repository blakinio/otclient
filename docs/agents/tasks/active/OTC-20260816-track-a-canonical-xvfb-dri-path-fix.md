---
task_id: OTC-20260816-track-a-canonical-xvfb-dri-path-fix
status: ready
agent: ChatGPT
session_id: chatgpt-coord-canonical-xvfb-dri-fix-20260816-2127
session_role: promotion_integration_coordinator
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: implementation
phase: coordinator-promotion-ready
branch: fix/OTC-20260816-track-a-canonical-xvfb-dri-path-v2
base_branch: main
base_main: acbc05866b6abec471425822a57c3bcf47c0edd5
current_main: acbc05866b6abec471425822a57c3bcf47c0edd5
risk: high
updated: 2026-08-16T21:27:00+02:00
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/test_tibia_official_client_re_canonical_live_session.py
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-xvfb-dri-path-fix.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-xvfb-dri-path-fix/**
modules_touched:
  - canonical Track A runtime session worker
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: coordinator exact-blob replay and validation of the already-hosted repair; this promotion performs no physical runtime operation
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: heavy
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
persistent_session_role: none
physical_e2e_required: false
owner_funded_ai_api_authorized: false
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
promoted_dependency:
  task: OTC-20260816-track-a-xvfb-dri-path-default-glx
  proof_pr: 427
  archive_pr: 428
  proof_merge: d9a91554dfa1da9232bbef89f818c71d6c2dca7d
  archive_merge: acbc05866b6abec471425822a57c3bcf47c0edd5
  classification: PROVEN_LIBGL_DRIVERS_PATH_ALONE_ENABLES_GLX_UNDER_CURRENT_CANONICAL_XVFB_ARGUMENTS
  minimal_worker_change: LIBGL_DRIVERS_PATH_ONLY
source_implementation:
  pr: 423
  final_head: 1496fc83ee92326ebd2a1f9da06a926d50f7d040
  coordinator_decision: ACCEPT
  material_findings_open: 0
  changed_paths:
    - .github/scripts/tibia-official-client-re-canonical-live-session.sh
    - .github/scripts/test_tibia_official_client_re_canonical_live_session.py
    - docs/agents/evidence/OTC-20260816-track-a-canonical-xvfb-dri-path-fix/20260816-hosted-validation.md
    - docs/agents/tasks/active/OTC-20260816-track-a-canonical-xvfb-dri-path-fix.md
  source_blobs:
    worker: f87c3d3f3e2e095fd0f7de48b1ec6de947446029
    tests: d786447fcb474874e870e71791ed03a0f9ec9c3c
    evidence: 9d206a3b3d123fe7f97d0e7c25e38cc2fa3e5ea2
implementation:
  contained_dri_root_helper: added
  toolroot_requires_contained_dri_provider: true
  swrast_must_resolve_below_dri_and_toolroot: true
  resolved_provider_must_be_regular_file: true
  bootstrap_derives_dri_from_selected_toolroot: true
  xvfb_environment_LIBGL_DRIVERS_PATH: '$dri'
  xvfb_argument_change: none
  client_environment_change: none
  explicit_glx_flag_added: false
hosted_validation:
  implementation_head_with_validator: cf9f361389972dcfe3f8c29db2ecd1c4c147c3ab
  validator_run: 31966128631
  validator_job: 95211462614
  result: SUCCESS
  shell_syntax: PASS
  canonical_session_tests: 14_of_14_PASS
  canonical_transition_tests: 9_of_9_PASS
  canonical_guard_tests: 3_of_3_PASS
  canonical_lease_tests: 14_of_14_PASS
  minimal_xvfb_dri_source_contract: PASS
  temporary_validator_removed: true
source_final_validation:
  governance_run: 31966417003
  governance_result: SUCCESS
  repository_ci_run: 31966417334
  repository_ci_result: SUCCESS
  required_ci_job: 95212359032
  required_ci_result: SUCCESS
  review_threads_open: 0
promotion:
  pr: 429
  source_pr: 423
  initial_replay_head: ed5900bd246db27bc92d09e868c041d25b37c669
  final_checkpoint_head: PENDING_AFTER_THIS_UPDATE
  replay_method: exact audited source blobs onto current main; no source branch merge/rebase
  current_main_source_worker_blob: 2707015cdc441d8b32d7c40daa54fc3141c4ca6b
  source_merge_base_worker_blob: 2707015cdc441d8b32d7c40daa54fc3141c4ca6b
  current_main_source_test_blob: e701e510a78392b81b665f187ff2901c8ea843a3
  source_merge_base_test_blob: e701e510a78392b81b665f187ff2901c8ea843a3
  intervening_overlap: false
final_validation:
  promotion_exact_head_governance: PENDING
  promotion_exact_head_repository_ci: PENDING
  physical_e2e: NOT_APPLICABLE
  physical_e2e_reason: repository repair only; physical official-client revalidation requires a separately admitted RUNTIME task after trusted-main promotion and archive
audit:
  result: PASS
  material_findings_open: 0
  notes:
    - coordinator independently reviewed the implementation patch and containment behavior
    - the DRI provider may be a symlink only when its resolved regular-file target remains inside the same contained DRI directory/toolroot
    - only the Xvfb environment receives LIBGL_DRIVERS_PATH
    - no +extension GLX or client-side provider override is introduced
acceptance:
  - promoted physical causal dependency: PASS
  - worker syntax and targeted contract suites: PASS
  - fail-closed DRI/swrast containment: PASS
  - Xvfb-only provider environment: PASS
  - unchanged Xvfb arguments: PASS
  - no client env leakage: PASS
  - no temporary workflow retained: PASS
  - source exact-head governance and CI: PASS
last_completed_step: coordinator promoted and archived the causal DRI-path proof, independently audited #423, verified current-main source/test blobs still equal #423 merge-base blobs, and replayed the exact audited repair onto current main as #429
next_action: obtain exact-head governance/CI on #429, close source #423 superseded, mark #429 ready and merge after branch-protection gates, then archive/release this repair before any fresh physical RUNTIME revalidation
---

# Track A canonical Xvfb DRI-path repair — coordinator promotion

This is a repository-only promotion. It establishes the fail-closed worker repair but makes no claim that a canonical runtime exists or that an official-client window has been physically revalidated after the repair.
