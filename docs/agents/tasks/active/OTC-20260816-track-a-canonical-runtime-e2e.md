---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: blocked
agent: ChatGPT
session_id: chatgpt-runtime-v3-20260816-1644
session_role: runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: waiting-runner-support-layout-inventory
branch: ci/OTC-20260816-track-a-canonical-runtime-e2e-v3
base_branch: main
base_main: 67e5dc88ff4d6c241d90a046527dac4aa9f831d8
risk: high
updated: 2026-08-16T16:48:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/**
modules_touched: []
reuses:
  - .github/scripts/tibia-official-client-re-canonical-live-lease
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-bootstrap-implementation.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-toolroot-layout-fix.md
supersedes_pr: 376
depends_on:
  - OTC-20260816-track-a-runner-support-layout-inventory
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
canonical_registration: ABSENT_AT_RUN_31953635875_PRECHECK
canonical_lease_generation: 2_RELEASE_EXPECTED_AFTER_FAILED_WORKFLOW
registration_lease_generation: NOT_APPLICABLE
gate_a: ACQUIRED_GENERATION_2_THEN_RELEASE_PATH_EXECUTED
generation_rebind: NOT_APPLICABLE
gate_b: NOT_REACHED
bootstrap: FAIL_CLOSED_BEFORE_WARP_X11_CLIENT
target_uniqueness: NOT_REACHED_THIS_ATTEMPT
mutation_authorized: false
owner_funded_ai_api_authorized: false
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
physical_attempts:
  - pr: 376
    run: 31952484701
    job: 95177998199
    acquired_lease_generation: 1
    result: FAIL_CLOSED_XVFB_UNAVAILABLE
    registration_published: false
    remediation: PR 379/380
  - pr: 381
    run: 31953635875
    job: 95180815033
    runner: synology-otclient-01
    pre_admission_lease_status: released
    pre_admission_lease_generation: 1
    acquired_lease_generation: 2
    result: FAIL_CLOSED_TOOLROOT_UNAVAILABLE
    stage: support-root-resolution-before-WARP-X11-client
    registration_published: false
    session_root_precheck: ABSENT
    credentials_used: false
    login_attempted: false
    workflow_status: REMOVED_TO_PREVENT_RETRY
root_cause_frontier:
  trusted_worker_fixed_candidates:
    - /home/runner/_work/_otclient_tibia_re_state/toolroot
    - /work/_otclient_tibia_re_state/toolroot
  result: neither candidate satisfied the hardened same-root completeness/containment contract on the current physical runner
  static_runner_stack_finding: PR 280 proposed image installs xvfb, xdotool and proxychains4 as system packages but does not list x11vnc; that branch is not trusted-current deployment proof
  unknowns:
    - actual current system paths and versions for Xvfb/x11vnc/xdotool/XKB/libproxychains on synology-otclient-01
    - which fixed support components, if any, are missing from each historical toolroot
    - whether current runner image already has x11vnc outside the historical roots
safety:
  one_shot_bootstrap_workflow_removed: true
  blind_physical_retry_forbidden: true
  next_physical_work_must_be_read_only_support_inventory: true
acceptance:
  - bounded read-only runner support-layout inventory proves exact realpaths/existence/version metadata for only required support tools/data
  - inventory does not inspect official-client processes, registration, X11/VNC sessions, network/game state or credentials
  - any resolver/image repair is implemented and promoted on GitHub-hosted before another bootstrap attempt
  - next bootstrap is a fresh-current-main redispatch with fresh admission and one bounded attempt
last_completed_step: fresh trusted-main physical run 31953635875 acquired generation 2 but failed closed at toolroot_unavailable before WARP/X11/client; one-shot workflow was removed and static PR280 inspection exposed a likely system-package/x11vnc mismatch requiring exact runner inventory
next_action: execute OTC-20260816-track-a-runner-support-layout-inventory as a separate bounded read-only Synology infrastructure observation; use its sanitized result to choose a hosted resolver/image fix or declare an external deployment blocker
---

# Track A canonical physical runtime E2E v3 — blocked support-layout checkpoint

The runner is reachable and canonical admission is functioning, but the current physical support filesystem does not satisfy the hardened trusted-worker root contract. No registered runtime exists and no client/login was started. Further bootstrap attempts are disabled until a minimal support-layout inventory identifies the actual runner tool placement without observing the official client/runtime surface.
