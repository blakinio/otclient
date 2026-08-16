---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: implementing
agent: ChatGPT
session_id: chatgpt-runtime-v7-20260816
session_role: runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: fresh-canonical-bootstrap-after-graphics-fix
branch: ci/OTC-20260816-track-a-canonical-runtime-e2e-v7
base_branch: main
base_main: 778e13306d93297025abf8e4e970e91ac9830a36
risk: high
updated: 2026-08-16T19:11:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/**
  - .github/workflows/tibia-official-client-re-canonical-runtime-e2e-v7.yml
modules_touched: []
reuses:
  - .github/scripts/tibia-official-client-re-canonical-live-lease
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-client-window-ownership-discriminator.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-graphics-integration-fix.md
depends_on: []
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: v6 and the isolated discriminator proved the exact client stayed alive with zero visible X11 windows while Qt reported that neither GLX nor EGL was enabled; hosted fix #402 removed the worker's explicit QT_XCB_GL_INTEGRATION=none self-disable, preserved QT_QUICK_BACKEND=software and added QSG_INFO=1, and is now trusted on main; exactly one fresh canonical bootstrap/Gate-B attempt is therefore authorized
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
mutation_authorized: true
owner_funded_ai_api_authorized: false
live_runtime_authorization_source: owner instruction 2026-08-16 to finish the existing Track A task; authorization is limited to exactly one fresh no-login canonical bootstrap/Gate-B attempt from trusted main after graphics fix #402
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
    acquired_lease_generation: 1
    result: XVFB_UNAVAILABLE_BEFORE_REGISTRATION
  - pr: 381
    acquired_lease_generation: 2
    result: TOOLROOT_UNAVAILABLE_BEFORE_WARP_X11_CLIENT
  - pr: 386
    acquired_lease_generation: 3
    result: XVFB_SOCKET_MISSING_BEFORE_CLIENT_REGISTRATION
  - pr: 393
    acquired_lease_generation: 4
    result: FAIL_CLOSED_WORKER_TIMEOUT
  - pr: 397
    run: 31957502867
    job: 95190252936
    acquired_lease_generation: 5
    result: FAIL_CLOSED_CLIENT_WINDOW_MISSING
    registration_published: false
    gate_b_reached: false
resolved_discriminator:
  pr: 398
  run: 31958546334
  job: 95192878995
  classification: PROVEN_CLIENT_ALIVE_ZERO_VISIBLE_WINDOWS_WITH_QT_GL_CONTEXT_FAILURES
  client_alive_through_seconds: 35
  visible_windows_t05: 0
  visible_windows_t15: 0
  visible_windows_t35: 0
  cleanup: COMPLETE
resolved_graphics_fix:
  implementation_pr: 402
  implementation_merge_commit: 8b04ffd0c2a9c25b3a8fba942b55ccb6ca450044
  archive_merge_commit: 778e13306d93297025abf8e4e970e91ac9830a36
  removed_environment_assignment: QT_XCB_GL_INTEGRATION=none
  preserved_environment_assignment: QT_QUICK_BACKEND=software
  added_nonsecret_diagnostic_assignment: QSG_INFO=1
  forced_specific_gl_backend: false
  hosted_session_tests: 11_PASS
  hosted_transition_tests: 9_PASS
  hosted_guard_tests: 3_PASS
  hosted_lease_tests: 14_PASS
  graphics_contract: PASS
safety:
  blind_bootstrap_retry_forbidden: true
  max_physical_attempts_this_phase: 1
  registration_exists_prestate: false
  current_pid_session_claimed: false
  credentials_allowed: false
  login_allowed: false
  gameplay_allowed: false
  track_b_access: false
acceptance:
  - exact trusted base is 778e13306d93297025abf8e4e970e91ac9830a36
  - worker graphics contract proves QT_XCB_GL_INTEGRATION=none absent, QT_QUICK_BACKEND=software present and QSG_INFO=1 present before mutation
  - fresh lease/admission precheck refuses pre-existing registration or unregistered canonical session root
  - exactly one canonical bootstrap is attempted
  - immediate same-generation Gate B must pass before controller release and success claim
  - successful registration must preserve exact client version/size/SHA and loopback VNC mapping
  - on any new failure, stop fail-closed, publish no registration claim and do not retry
  - no account credentials, login or gameplay input are used
last_completed_step: discriminator #398 and hosted graphics fix #402/#404 are terminal on trusted main; no authoritative canonical registration currently exists
next_action: execute exactly one fresh v7 physical bootstrap and immediate same-generation Gate B; persist sanitized QSG/GLX/EGL/runtime evidence and then remove the one-shot workflow
---

# Track A canonical physical runtime E2E v7

Fresh one-shot canonical bootstrap after the trusted Qt XCB graphics integration repair. Success requires authoritative registration plus immediate same-generation Gate B. Any new discriminator terminates this phase without retry.
