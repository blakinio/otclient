---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: blocked
agent: ChatGPT
session_id: chatgpt-runtime-v5-20260816-1734
session_role: runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: waiting-bounded-client-window-wait-fix
branch: ci/OTC-20260816-track-a-canonical-runtime-e2e-v5
base_branch: main
base_main: b69084067de24528b1f763ab9630f638e8bcf092
risk: high
updated: 2026-08-16T17:41:00+02:00
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
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-toolroot-layout-fix.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-runner-support-x11vnc-repair.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-runner-system-xkbcomp-repair.md
supersedes_pr: 386
depends_on:
  - OTC-20260816-track-a-canonical-client-window-wait-fix
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: v5 physical bootstrap passed trusted support preflight and acquired canonical lease generation 4 but hit the transition worker timeout; deterministic source review found the client-window wait can exceed the supervisor budget and must be repaired/promoted before another physical attempt
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
canonical_registration: ABSENT
canonical_lease_generation: 4
registration_lease_generation: NOT_APPLICABLE
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: REQUIRED_NOT_PROVEN
target_uniqueness: UNKNOWN
mutation_authorized: false
owner_funded_ai_api_authorized: false
live_runtime_authorization_source: owner instruction 2026-08-16 to finish the existing Track A tasks; v5 bootstrap used no account credentials or login input
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
excluded_runtime_surfaces:
  - Track B PR #284 namespace
  - historical closed PR #303 runtime surfaces
prior_fail_closed_attempts:
  - pr: 376
    run: 31952484701
    job: 95177998199
    acquired_lease_generation: 1
    result: XVFB_UNAVAILABLE_BEFORE_REGISTRATION
  - pr: 381
    run: 31953635875
    job: 95180815033
    acquired_lease_generation: 2
    result: TOOLROOT_UNAVAILABLE_BEFORE_WARP_X11_CLIENT
  - pr: 386
    run: 31954637565
    job: 95183271514
    acquired_lease_generation: 3
    result: XVFB_SOCKET_MISSING_BEFORE_CLIENT_REGISTRATION
  - pr: 393
    run: 31956030015
    job: 95186692121
    head: fc329b23fa8e30fb6110fb162e9c57ed2d3d4e5d
    pre_admission_lease_status: released
    pre_admission_lease_generation: 3
    acquired_lease_generation: 4
    support_root_preflight: PASS
    system_xkbcomp_preflight: PASS
    warp_profile_generated: true
    result: FAIL_CLOSED_WORKER_TIMEOUT
    registration_published: false
    gate_b_reached: false
    credentials_used: false
    login_attempted: false
    one_shot_workflow_removed: true
deterministic_root_cause:
  classification: BOUNDED_CLIENT_WINDOW_WAIT_DEFECT
  window_helper_max_seconds_approx: 30
  bootstrap_outer_attempts: 100
  bootstrap_nominal_missing_window_seconds_approx: 3025
  transition_worker_timeout_seconds: 300
  consequence: missing/slow client window path can be masked by supervisor worker_timeout before client_window_missing is emitted
  evidence: docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/20260816-v5-worker-timeout.md
safety:
  blind_bootstrap_retry_forbidden: true
  one_shot_bootstrap_workflow_removed: true
  registration_exists: false
  current_pid_session_claimed: false
acceptance:
  - hosted-only worker fix is independently tested/promoted to trusted main before any new physical bootstrap
  - client-window wait is bounded below transition worker timeout and preserves client_exited/client_window_missing failure classification
  - next RUNTIME attempt starts from the new current main with fresh admission and one bounded attempt
  - bootstrap still creates only one exact-fenced persistent X11/VNC/client runtime and immediate Gate B must pass before controller release
  - no credentials are used until a later separately admitted protected-login phase
last_completed_step: v5 physical run 31956030015/job 95186692121 passed support/xkbcomp preflight, acquired lease generation 4 and generated canonical WARP profile, then failed closed at worker_timeout; one-shot workflow removed and deterministic nested client-window wait defect persisted
next_action: implement/test/promote OTC-20260816-track-a-canonical-client-window-wait-fix on GitHub-hosted current main, then close this stale v5 PR and create one fresh-current-main RUNTIME redispatch
---

# Track A canonical physical runtime E2E v5 — blocked checkpoint

The runner support blockers are cleared, but the trusted worker's nested client-window polling can exceed the transition supervisor budget. No authoritative runtime registration exists from v5. Further physical bootstrap is disabled until the bounded-wait fix reaches trusted main.
