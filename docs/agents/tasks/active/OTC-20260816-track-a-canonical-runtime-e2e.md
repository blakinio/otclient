---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: implementing
agent: ChatGPT
session_id: chatgpt-runtime-v6-20260816
session_role: runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: canonical-bootstrap
branch: ci/OTC-20260816-track-a-canonical-runtime-e2e-v6
base_branch: main
base_main: 9e3634c1d822ffc6e74d8e42da63a4e8c60ea3e1
risk: high
updated: 2026-08-16T18:03:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/**
  - .github/workflows/tibia-official-client-re-canonical-runtime-e2e-v6.yml
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
depends_on: []
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: one serialized physical bootstrap/Gate-B attempt is routed through repository-controlled GitHub Actions after every previously observed support/wait blocker reached trusted-main terminal state
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
live_runtime_authorization_source: owner instruction 2026-08-16 to finish existing Track A tasks; authority remains conditional on fresh lease/registration/uniqueness checks and trusted-main transition gates; no account credentials/login are authorized in this phase
fresh_revalidation_required_before_mutation: true
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
    support_root_preflight: PASS
    system_xkbcomp_preflight: PASS
    result: FAIL_CLOSED_WORKER_TIMEOUT
    registration_published: false
    gate_b_reached: false
    credentials_used: false
    login_attempted: false
resolved_prerequisites:
  canonical_bootstrap_transition:
    implementation_merge: d16091ca29ff7c9330115e9ce0fdbfb41646e0dc
  support_toolroot:
    path: /work/_otclient_tibia_re_state/toolroot
  contained_x11vnc:
    sha256: 4954921ae9c4e2bf7061603eb6a2d52c2292a0973eb2da5d6f48a9bd49570ffc
  system_xkbcomp:
    path: /usr/bin/xkbcomp
    sha256: 0967e7e7b03b077327cea74567726b265bd304b4fdf59f87bf7fdfe1074e7591
    isolated_xvfb_socket_validation: PASS
  bounded_client_window_wait:
    implementation_merge: c160e6776344429058a0bb97db0b411202e3e82e
    archive_merge: 9e3634c1d822ffc6e74d8e42da63a4e8c60ea3e1
    production_wait_budget_seconds: 30
    transition_worker_timeout_seconds: 300
    semantic_validation_run: 31956997604
    semantic_validation_result: SUCCESS
bootstrap_phase_boundary:
  credentials_allowed: false
  login_allowed: false
  create_second_runtime_if_registration_exists: false
  exact_client_version: 15.32.df7b29
  exact_client_size: 51965216
  exact_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
acceptance:
  - workflow head/base and trusted-main worker/transition are fenced before physical work
  - support toolroot and exact current /usr/bin/xkbcomp are re-proven before mutation
  - fresh authoritative lease and registration state are read before mutation; any existing registration/session forces reclassification rather than duplicate creation
  - canonical lease is acquired for this exact task/session before transition bootstrap
  - trusted-main transition re-proves registration absence and candidate uniqueness under the canonical lock
  - one persistent exact-fenced client + X11 + localhost-only VNC + canonical-owned WARP runtime is created
  - authoritative registration is atomically committed only after bootstrap proof and immediate same-generation Gate B passes
  - controller authority is released while the canonical desktop/VNC/client remain alive idle on success
  - no account credentials/login are consumed in this phase
  - any new fail-closed discriminator stops this phase; no blind retry is permitted
last_completed_step: bounded client-window wait defect was promoted and archived on trusted main through PR #395/#396; existing RUNTIME task is re-claimed from current main for one fresh v6 bootstrap/Gate-B attempt
next_action: dispatch exactly one repository-controlled v6 bootstrap/Gate-B attempt on synology-otclient-01; on PASS persist sanitized authoritative registration and leave runtime idle, on any new discriminator remove the one-shot workflow and persist the exact blocker without retry
---

# Track A canonical physical runtime E2E v6

All previously observed deterministic support and wait-budget blockers are now terminal on trusted `main`. This phase performs one fresh canonical bootstrap/Gate-B attempt without login credentials. Current PID/session/display/VNC remain unclaimed until the workflow proves and persists them.
