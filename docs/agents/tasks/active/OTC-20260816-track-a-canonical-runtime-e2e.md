---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: implementing
agent: ChatGPT
session_id: chatgpt-runtime-admission-reconcile-v2-20260816
session_role: governance_reconciliation_engineer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: hosted-bootstrap-admission-reconciliation-current-main
branch: fix/OTC-20260816-track-a-bootstrap-admission-reconcile-v2
base_branch: main
base_main: 0bdc82583417616ccd4a2ef52a9005bcc18eb660
risk: high
updated: 2026-08-16T22:43:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/**
  - .github/scripts/test_track_a_agent_runtime_governance.py
modules_touched:
  - Track A runtime admission validator
reuses:
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-bootstrap-implementation.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-xvfb-dri-path-fix.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-dri-repair-isolated-client-revalidation.md
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: trusted main contains the reviewed bootstrap/rebind/Gate-B implementation promoted by PR #371 and archived by #375, while the deterministic admission validator still carries a stale unconditional pre-#371 rejection of canonical_bootstrap mutation. This current-main replay reconciles the validator only. It also consumes the newer archived isolated client evidence from #431/#432/#434, which proves the DRI repair restores GLX but the exact client still has zero visible windows through 35 seconds; therefore merging this governance repair must not be treated as authority for a blind canonical bootstrap retry.
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
invocation_started_at: 2026-08-16T22:27:00+02:00
last_progress_at: 2026-08-16T22:43:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: current-main-replay
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 1
stall_warnings: 0
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
trusted_bootstrap_implementation:
  implementation_pr: 371
  implementation_merge_commit: d16091ca29ff7c9330115e9ce0fdbfb41646e0dc
  archive_pr: 375
  archive_merge_commit: 259e418b2c526f93bd697f07c42b73b1fd40a914
  status: PROMOTED_AND_ARCHIVED
  physical_authority_from_implementation_pr: false
trusted_xvfb_dri_repair:
  proof_pr: 427
  proof_archive_pr: 428
  implementation_pr: 429
  implementation_merge_commit: feb5c087eba70bd649602737742e4f2fe3e72bc3
  archive_pr: 430
  archive_merge_commit: fa5b66b697d42c60515c5de48ea5e30135eadd0e
  classification: PROVEN_LIBGL_DRIVERS_PATH_ALONE_ENABLES_GLX_UNDER_CURRENT_CANONICAL_XVFB_ARGUMENTS
latest_isolated_client_revalidation:
  source_pr: 431
  promotion_pr: 432
  archive_pr: 434
  archive_merge_commit: 0bdc82583417616ccd4a2ef52a9005bcc18eb660
  semantic_run: 31970703417
  semantic_job: 95222630271
  governance_run: 31970703290
  cleanup: COMPLETE
  canonical_state_access: NONE
  x11_glx_present: true
  x11_glx_opcode: 150
  client_alive_t05_t15_t35: true
  visible_window_count_t05_t15_t35: 0
  client_log_total_lines: 415
  client_log_allowlist_matches: 35
  prior_qxcb_neither_glx_nor_egl_line_present: false
  prior_qrhigles2_create_failure_line_present: false
  classification: PROVEN_DRI_PATH_RESTORES_XVFB_GLX_AND_REMOVES_PRIOR_ALLOWLISTED_QXCB_NO_GLX_EGL_FAILURE_BUT_EXACT_CLIENT_REMAINS_ALIVE_WITH_ZERO_VISIBLE_WINDOWS_THROUGH_35S
  remaining_no_window_root_cause: UNKNOWN_POST_GLX_PREREQUISITE
historical_canonical_runtime_checkpoint:
  last_physical_pr: 405
  last_physical_run: 31960965493
  last_physical_job: 95198777325
  last_lease_generation: 6
  authoritative_registration_published: false
  gate_b_reached: false
  result: FAIL_CLOSED_CLIENT_WINDOW_MISSING
  governance_result: FAILURE
  governance_discriminator: bootstrap is not currently implemented/authorized
admission_reconciliation_contract:
  purpose: allow a future explicit invocation of the already-reviewed bootstrap transaction only when trusted-base implementation proof and one-attempt owner authorization are both present; the transaction itself must still acquire current lease authority and prove under-lock authoritative absence/uniqueness before child creation
  bootstrap_mutation_true_requires:
    - canonical_registration ABSENT
    - canonical_lease_generation UNKNOWN at pre-run task checkpoint
    - registration_lease_generation NOT_APPLICABLE
    - gate_a REQUIRED_NOT_PROVEN at pre-run task checkpoint
    - generation_rebind NOT_APPLICABLE
    - gate_b NOT_APPLICABLE
    - bootstrap PASS
    - target_uniqueness UNKNOWN at pre-run task checkpoint
    - bootstrap_attempt_limit 1
    - non-empty live_runtime_authorization_source
    - credentials_allowed false
    - login_allowed false
    - gameplay_allowed false
  runtime_transaction_invariants:
    - reviewed transition acquires canonical coordination flock and validates the freshly acquired lease before decisive absence checks
    - registration absence and complete official-client candidate/session inventory are re-proven under the held flock immediately before launch
    - any failure before registration commit cleans only bootstrap-owned descendants and leaves no success registration
    - same-generation Gate B must pass before controller release
    - task-level mutation_authorized true authorizes only one invocation of the reviewed fail-closed transaction, not child creation outside its internal gates
source_reconciliation:
  source_pr: 433
  source_head: cb4a9283cd8c2ad8bcbb584f631619a9255c2ce0
  independent_validator_run: 31970995035
  independent_validator_job: 95223324421
  independent_validator_result: SUCCESS
  final_governance_run: 31971035068
  final_governance_result: SUCCESS
  pre_ready_ci_run: 31971035100
  pre_ready_required_ci_job: 95223592746
  pre_ready_required_ci_result: SUCCESS
  ready_ci_run: 31971119864
  ready_required_ci_job: 95223786044
  ready_required_ci_result: SUCCESS
  source_merge_ref_invalidated_by_main_move: true
  main_move_nonoverlap: PRs #432 and #434 changed only isolated DRI-revalidation task/evidence lifecycle paths
current_main_replay:
  replay_parent: 0bdc82583417616ccd4a2ef52a9005bcc18eb660
  source_merge_tree: 111ceb5311a2579f44455e902d8ec9e7fece778c
  replay_seed_commit: 62e9ed3640c1aff4380b61001ce6bd98870bb786
  source_code_rewritten: false
  metadata_update_only_after_replay: true
safety:
  blind_canonical_bootstrap_retry_forbidden: true
  reason: latest isolated full-client startup proves GLX is fixed yet no visible window appears through 35 seconds, so a canonical launch would currently repeat a known unsatisfied visible-window prerequisite rather than test a new causal fix
  credentials_allowed: false
  login_allowed: false
  gameplay_allowed: false
  track_b_access: false
forbidden:
  - physical Synology execution from this governance reconciliation branch
  - canonical lease/registration/session observation or mutation from this governance reconciliation branch
  - weakening exact client fence, canonical namespace, under-lock absence inventory, Gate B or cleanup invariants
  - credentials, login or gameplay authorization
  - blind canonical retry while the post-GLX visible-window prerequisite remains unresolved
  - Track B or historical PR #303 runtime access
  - owner-funded Codex/OpenAI API quota
acceptance:
  - deterministic validator still accepts existing none/read_only/ephemeral/canonical-reuse fail-closed cases
  - fail-closed bootstrap state with mutation_authorized false remains valid
  - canonical_bootstrap mutation_authorized true is accepted only for one explicitly authorized no-credential transaction with bootstrap PASS and pre-run transactional gate values
  - registration UNKNOWN cannot authorize bootstrap mutation
  - stale Gate A PASS/target uniqueness PROVEN preclaims cannot substitute for transaction-owned under-lock proof
  - missing owner authorization source, attempt limit other than 1, or credentials/login/gameplay permission rejects the bootstrap mutation claim
  - current-main replay preserves #432/#434 isolated revalidation evidence and archive
  - exact-head governance and repository CI pass against the current main
  - reconciliation merges before any later bootstrap admission could be considered
  - no canonical bootstrap is launched merely because governance is reconciled
last_completed_step: source reconciliation #433 was independently validated and reached green pre-ready/ready required CI, but strict branch protection correctly rejected merge after main advanced through independent #432/#434; the audited merge tree was replayed linearly onto current main 0bdc82583417616ccd4a2ef52a9005bcc18eb660 without code changes
next_action: validate and merge the current-main governance replay; then refresh this same entry task from trusted main and continue with the post-GLX/post-RHI no-visible-window investigation. Do not retry canonical bootstrap until a new causal fix makes a visible exact-client window plausible and a fresh canonical admission is separately authorized.
---

# Track A canonical runtime E2E — current-main bootstrap admission reconciliation

This phase is repository-only. It fixes the stale bootstrap admission validator while preserving the newer physical fact that GLX restoration did not create a visible official-client window. The next runtime work is therefore the post-GLX/post-RHI no-window discriminator, not a blind canonical bootstrap retry.
