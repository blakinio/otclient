---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: blocked
agent: ChatGPT
session_id: chatgpt-runtime-v2-20260816-1601
session_role: runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: waiting-trusted-toolroot-fix
branch: ci/OTC-20260816-track-a-canonical-runtime-e2e-v2
base_branch: main
base_main: 259e418b2c526f93bd697f07c42b73b1fd40a914
risk: high
updated: 2026-08-16T16:27:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/**
modules_touched: []
reuses:
  - .github/scripts/tibia-official-client-re-canonical-live-lease
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-bootstrap-implementation.md
supersedes_pr: 358
depends_on:
  - OTC-20260816-track-a-canonical-toolroot-layout-fix
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: heavy
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
persistent_session_role: canonical_runtime_owner
physical_e2e_required: true
runtime_access: canonical_bootstrap
runtime_owner_task: OTC-20260816-track-a-canonical-runtime-e2e
runtime_namespace: canonical-live-runtime
canonical_registration: RECHECK_REQUIRED
canonical_lease_generation: RECHECK_REQUIRED
registration_lease_generation: NOT_APPLICABLE_UNTIL_REGISTRATION_EXISTS
gate_a: REQUIRED_RECHECK_AFTER_DEPENDENCY_PROMOTION
generation_rebind: NOT_APPLICABLE_IF_REGISTRATION_REMAINS_ABSENT
gate_b: REQUIRED_AFTER_BOOTSTRAP
bootstrap: TRUSTED_MAIN_IMPLEMENTED_PR_371_BUT_PHYSICAL_TOOLROOT_LAYOUT_DEFECT_FOUND
target_uniqueness: REPROVE_UNDER_LOCK
mutation_authorized: false
owner_funded_ai_api_authorized: false
live_runtime_authorization_source: owner current instruction 2026-08-16 to finish existing Track A tasks, subject to all current admission gates
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
excluded_runtime_surfaces:
  - Track B PR #284 namespace
  - historical closed PR #303 runtime surfaces
physical_attempts:
  - run: 31951672293
    job: 95175957281
    head: d46d53bf1d71a630308666e97bfc04793649b478
    result: NOT_STARTED_SELECTOR_MISMATCH
    runner_id: 0
    requested_selector: [self-hosted, Linux, X64, otclient, tibia-re, synology]
    repair_basis: last successful canonical job 95157691875 used runner synology-otclient-01 with selector [otclient, synology]
  - run: 31952484701
    job: 95177998199
    head: 3d48284f0d07a6c1f4b71cd5f9db30774eb7dde3
    runner: synology-otclient-01
    runner_id: 21
    selector: [otclient, synology]
    pre_admission_lease_status: absent
    pre_admission_lease_generation: 0
    acquired_lease_generation: 1
    result: FAIL_CLOSED
    failure: TRACK_A_CANONICAL_SESSION_ERROR=xvfb_unavailable
    stage: bootstrap_before_x11_client_registration
    registration_published: false
    credentials_read_or_typed: false
    client_login_attempted: false
    note: worker downloaded/verified canonical WARP tools then failed before Xvfb selection; transition returned bootstrap_worker_failed and workflow cleanup released controller authority
root_cause:
  classification: TRUSTED_MAIN_RUNTIME_LAYOUT_DEFECT
  canonical_session_toolroot: /home/runner/_work/_otclient_tibia_re_state/toolroot
  historically_proven_runner_toolroot: /work/_otclient_tibia_re_state/toolroot
  evidence: closed PR #303 runtime workflow explicitly required /work/_otclient_tibia_re_state/toolroot/usr/bin and the physical run could not resolve Xvfb through the trusted-main TOOL path
  required_fix: hosted-only fail-closed toolroot layout resolution promoted to trusted main before any new physical bootstrap
workflow_status: REMOVED_TO_PREVENT_RETRY
admission_governance:
  run: 31952484718
  fresh_behavior_audit: SUCCESS
  deterministic_policy_audit: FAILED_TASK_METADATA_ONLY
  finding: mutation_authorized was previously a descriptive string; corrected here to boolean false while blocked
acceptance:
  - dependency fix is independently validated/promoted to trusted main without physical runtime mutation
  - this RUNTIME task is then redispatched/refreshed from the new trusted main
  - fresh lease/admission and under-lock registration/candidate absence are re-proven before mutation
  - bootstrap creates one exact-fenced persistent X11/VNC/client runtime and immediate Gate B passes
  - no credentials are used until a later separately re-admitted protected-login phase
last_completed_step: corrected the runner selector, obtained a real synology-otclient-01 physical bootstrap attempt, classified xvfb_unavailable as a trusted-main toolroot-layout defect, removed the one-shot workflow to prevent retries, and restored fail-closed mutation_authorized=false
next_action: implement/test/promote OTC-20260816-track-a-canonical-toolroot-layout-fix on GitHub-hosted current main; then create a fresh-current-main RUNTIME redispatch and repeat admission/bootstrap exactly once
---

# Track A canonical physical runtime E2E v2 — blocked checkpoint

The canonical runner is reachable. The first correctly routed physical bootstrap acquired lease generation 1 but stopped fail-closed before X11/client registration because the trusted session worker resolves support tools from a path that does not match the proven dedicated-runner layout. No login or credential use occurred. Further physical mutation is disabled until the support-toolroot resolver is repaired, tested and promoted to trusted main.
