---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: blocked
agent: ChatGPT
session_id: chatgpt-runtime-v6-20260816
session_role: runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: waiting-client-window-ownership-discriminator
branch: ci/OTC-20260816-track-a-canonical-runtime-e2e-v6
base_branch: main
base_main: 9e3634c1d822ffc6e74d8e42da63a4e8c60ea3e1
risk: high
updated: 2026-08-16T18:07:00+02:00
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
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-client-window-wait-fix.md
depends_on:
  - OTC-20260816-track-a-client-window-ownership-discriminator
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: v6 physical bootstrap reached a live exact client after WARP/Xvfb/VNC success but failed closed at the bounded visible-window discriminator; a separate non-registering ephemeral-isolated diagnostic must resolve window/process ownership or startup state before another canonical bootstrap attempt
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
canonical_lease_generation: 5
registration_lease_generation: NOT_APPLICABLE
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: REQUIRED_NOT_PROVEN
target_uniqueness: UNKNOWN
mutation_authorized: false
owner_funded_ai_api_authorized: false
live_runtime_authorization_source: owner instruction 2026-08-16 to finish existing Track A tasks; no further canonical mutation is authorized from this branch after the v6 discriminator
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
    acquired_lease_generation: 4
    result: FAIL_CLOSED_WORKER_TIMEOUT
    registration_published: false
    gate_b_reached: false
  - pr: 397
    run: 31957502867
    job: 95190252936
    head: 29c750adfbfbf0ea4db64005698b456a5b9c92b0
    governance_run: 31957502830
    governance_result: SUCCESS
    pre_admission_lease_status: released
    pre_admission_lease_generation: 4
    acquired_lease_generation: 5
    trusted_worker_wait_contract: PASS
    support_root_preflight: PASS
    system_xkbcomp_preflight: PASS
    warp: PASS
    xvfb: PASS
    vnc: PASS
    client_start: REACHED
    client_liveness_during_window_wait: ALIVE
    bounded_window_wait_seconds_approx: 30
    result: FAIL_CLOSED_CLIENT_WINDOW_MISSING
    registration_published: false
    gate_b_reached: false
    credentials_used: false
    login_attempted: false
    one_shot_workflow_removed: true
current_discriminator:
  classification: CLIENT_ALIVE_NO_MATCHING_PID_OWNED_VISIBLE_TIBIA_WINDOW
  proven:
    - exact trusted base and bounded-window worker contract passed
    - support root and xkbcomp passed
    - canonical WARP egress passed
    - Xvfb socket/startup passed
    - localhost-only VNC listener startup passed
    - exact client launch stage was reached
    - launched exact client PID remained alive throughout the bounded 30-second window wait
    - no visible window matching ^Tibia$ owned by the launched PID was found within that budget
  unknown:
    - whether any visible client-related X11 window existed under another title
    - whether a relevant window was owned by an owned child/related process instead of the launched PID
    - whether the client remained blocked before window mapping and why
  evidence: docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/20260816-v6-client-window-missing.md
safety:
  blind_bootstrap_retry_forbidden: true
  one_shot_bootstrap_workflow_removed: true
  registration_exists: false
  current_pid_session_claimed: false
acceptance:
  - bounded ephemeral-isolated diagnostic determines visible X11 window title/class/PID ownership versus no mapped window
  - diagnostic may inspect only task-owned startup process tree/window metadata and bounded sanitized startup log with no credentials/login/canonical registration mutation
  - all diagnostic processes/display/WARP state are cleaned before exit
  - only after the discriminator is resolved may a hosted fix be promoted or a fresh canonical bootstrap be redispatched
last_completed_step: v6 run 31957502867/job 95190252936 acquired lease generation 5 and passed WARP/Xvfb/VNC/client-start stages, then failed closed after the correct 30-second wait at client_window_missing; one-shot workflow removed and sanitized evidence persisted
next_action: execute one separately admitted ephemeral-isolated client-window ownership/startup discriminator; do not retry canonical bootstrap until that evidence identifies the required fix or proves a safe window-owner matching rule
---

# Track A canonical physical runtime E2E v6 — blocked checkpoint

v6 eliminated the generic timeout and reached a live exact client process after all support stages passed. The remaining blocker is now precisely the lack of a visible `^Tibia$` window owned by the launched PID during the bounded 30-second wait. Canonical registration/Gate B remain unproven and no login occurred.
