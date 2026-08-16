---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: implementing
agent: ChatGPT
session_id: chatgpt-runtime-admission-reconcile-20260816
session_role: governance_reconciliation_engineer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: hosted-bootstrap-admission-reconciliation
branch: fix/OTC-20260816-track-a-bootstrap-admission-reconcile
base_branch: main
base_main: fa5b66b697d42c60515c5de48ea5e30135eadd0e
risk: high
updated: 2026-08-16T22:31:00+02:00
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
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: trusted main already contains the reviewed bootstrap/rebind/Gate-B implementation promoted by PR #371 and archived by #375, and the minimal Xvfb DRI-provider repair promoted by #429 and archived by #430; the remaining blocker is the deterministic admission validator's stale unconditional rejection of canonical_bootstrap mutation. This hosted phase reconciles that validator only. The current unmerged governance change cannot authorize its own physical runtime use; physical mutation remains forbidden until the reconciliation is merged to trusted main and this task is freshly re-admitted from that new main.
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
last_progress_at: 2026-08-16T22:31:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
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
  implementation_path: .github/scripts/tibia-official-client-re-canonical-live-transition.py
  worker_path: .github/scripts/tibia-official-client-re-canonical-live-session.sh
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
historical_runtime_checkpoint:
  last_physical_pr: 405
  last_physical_run: 31960965493
  last_physical_job: 95198777325
  last_lease_generation: 6
  authoritative_registration_published: false
  gate_b_reached: false
  last_physical_result: FAIL_CLOSED_CLIENT_WINDOW_MISSING
  last_governance_result: FAILURE
  last_governance_discriminator: bootstrap is not currently implemented/authorized
  credentials_used: false
  login_attempted: false
  gameplay_attempted: false
resolved_noncanonical_diagnostics:
  xcb_gl_trace_pr: 425
  xcb_gl_trace_archive_pr: 426
  dri_path_minimality_pr: 427
  dri_path_minimality_archive_pr: 428
  proven_before_repair: task-owned Xvfb did not advertise GLX and Qt loaded xcb_glx then failed context creation
  proven_after_dri_path: exact canonical-shaped Xvfb arguments advertise GLX with only contained LIBGL_DRIVERS_PATH; no +extension GLX required
admission_reconciliation_contract:
  purpose: authorize invocation of the already-reviewed bootstrap transaction only when explicit attempt metadata is present; the transaction itself must still acquire current lease authority and prove under-lock absence/uniqueness before child creation
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
forbidden:
  - physical Synology execution from this reconciliation branch
  - canonical lease/registration/session observation or mutation from this reconciliation branch
  - weakening exact client fence, canonical namespace, under-lock absence inventory, Gate B or cleanup invariants
  - credentials, login or gameplay authorization
  - Track B or historical PR #303 runtime access
  - owner-funded Codex/OpenAI API quota
acceptance:
  - deterministic validator still accepts existing none/read_only/ephemeral/canonical-reuse fail-closed cases
  - fail-closed bootstrap state with mutation_authorized false remains valid
  - canonical_bootstrap mutation_authorized true is accepted only for one explicitly authorized no-credential transaction with bootstrap PASS and pre-run transactional gate values
  - registration UNKNOWN cannot authorize bootstrap mutation
  - stale Gate A PASS/target uniqueness PROVEN preclaims cannot substitute for transaction-owned under-lock proof
  - missing owner authorization source, attempt limit other than 1, or credentials/login/gameplay permission rejects the bootstrap mutation claim
  - canonical rebind behavior remains unchanged in this phase
  - fresh independent positive/negative validator passes
  - standard Track A governance and repository CI pass on exact final head
  - reconciliation merges before any physical task re-admission
last_completed_step: trusted-main inspection proved #371/#375 already promoted and archived the bootstrap/rebind/Gate-B implementation, while current admission code still unconditionally rejects canonical_bootstrap mutation; #429/#430 have already promoted and archived the DRI provider repair
next_action: reconcile the deterministic bootstrap admission validator on this hosted-only branch, run independent positive/negative validation, obtain exact-head governance/CI and merge; only then re-admit this same task from the new trusted main for exactly one physical bootstrap/Gate-B attempt
---

# Track A canonical runtime E2E — hosted admission reconciliation

This checkpoint intentionally has `runtime_access: none`. It cannot authorize or execute the official client. It exists solely to reconcile the deterministic admission validator with the already-promoted bootstrap implementation before a fresh physical re-admission.
