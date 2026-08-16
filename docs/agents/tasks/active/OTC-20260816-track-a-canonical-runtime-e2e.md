---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: blocked
agent: ChatGPT
session_id: chatgpt-runtime-v4-20260816-1705
session_role: runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: waiting-isolated-xvfb-startup-discriminator
branch: ci/OTC-20260816-track-a-canonical-runtime-e2e-v4
base_branch: main
base_main: 917b8ab943fd9aa1fded50c9a0b8b4e1dfeb5cbb
risk: high
updated: 2026-08-16T17:10:00+02:00
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
  - docs/agents/tasks/archive/OTC-20260816-track-a-runner-support-layout-inventory.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-runner-support-x11vnc-repair.md
supersedes_pr: 381
depends_on:
  - OTC-20260816-track-a-isolated-xvfb-startup-discriminator
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: physical Synology bootstrap reached the trusted contained support root but Xvfb failed to create its socket; further client mutation is disabled pending a separate isolated support-process discriminator
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
canonical_lease_generation: 3
registration_lease_generation: NOT_APPLICABLE
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: REQUIRED_NOT_PROVEN
target_uniqueness: UNKNOWN
mutation_authorized: false
owner_funded_ai_api_authorized: false
live_runtime_authorization_source: owner instruction 2026-08-16 to finish existing Track A tasks, subject to current admission gates; no account credentials authorized/used in this phase
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
    remediation: toolroot worker #379/#380
  - pr: 381
    run: 31953635875
    job: 95180815033
    acquired_lease_generation: 2
    result: TOOLROOT_UNAVAILABLE_BEFORE_WARP_X11_CLIENT
    remediation: layout inventory #382/#383 plus contained x11vnc repair #384/#385
  - pr: 386
    run: 31954637565
    job: 95183271514
    runner: synology-otclient-01
    support_root_preflight: PASS
    pre_admission_lease_status: released
    pre_admission_lease_generation: 2
    acquired_lease_generation: 3
    trusted_worker_toolroot: /work/_otclient_tibia_re_state/toolroot
    warp_profile_generated: true
    result: FAIL_CLOSED_XVFB_SOCKET_MISSING
    stage: Xvfb startup before client launch and before registration
    registration_published: false
    gate_b_reached: false
    credentials_used: false
    login_attempted: false
    workflow_status: REMOVED_TO_PREVENT_RETRY
support_root_proof:
  root: /work/_otclient_tibia_re_state/toolroot
  completion_run: 31954295453
  completion_job: 95182427755
  x11vnc_sha256: 4954921ae9c4e2bf7061603eb6a2d52c2292a0973eb2da5d6f48a9bd49570ffc
  trusted_worker_contract_test: PASS_CONTAINED_TOOLROOT_COMPLETE
current_discriminator:
  failure: TRACK_A_CANONICAL_SESSION_ERROR=xvfb_socket_missing
  worker_stage: after canonical-owned WARP helper/profile setup, before X11 socket/client/VNC registration
  unknowns:
    - whether contained Xvfb exits immediately and exact stderr/exit reason
    - whether its library/XKB invocation is valid on the current runner
    - whether the selected display/socket directory itself is usable by the runner user
  safe_next_experiment: one bounded ephemeral Xvfb-only launch using the same exact contained binary/environment on an isolated free display, capturing exit code/stderr/socket result and cleaning it immediately; no canonical/client/runtime surface access
admission_governance:
  initial_run: 31954637529
  fresh_behavior_audit: SUCCESS
  deterministic_policy_audit: FAILED_TASK_METADATA_ONLY
  metadata_finding: pre-run descriptive gate values were outside the deterministic admission vocabulary
  correction: this checkpoint now uses canonical_bootstrap fail-closed vocabulary exactly: registration ABSENT, gate_a REQUIRED_NOT_PROVEN, generation_rebind NOT_APPLICABLE, gate_b NOT_APPLICABLE, bootstrap REQUIRED_NOT_PROVEN, mutation_authorized false
safety:
  one_shot_bootstrap_workflow_removed: true
  blind_bootstrap_retry_forbidden: true
  registration_exists: false
  current_pid_session_claimed: false
acceptance:
  - isolated Xvfb-only discriminator does not inspect or operate official-client/canonical registration/process/session/VNC/game/login surfaces
  - its exact result is persisted and any worker/package/environment fix is promoted before another bootstrap
  - next bootstrap, if justified, is a fresh-current-main task/PR with fresh admission and one bounded attempt
last_completed_step: physical bootstrap v4 proved the contained support-root preflight and lease acquisition generation 3, then failed closed at xvfb_socket_missing before client launch/registration; workflow removed and admission checkpoint normalized without retry
next_action: execute OTC-20260816-track-a-isolated-xvfb-startup-discriminator as a separate bounded support-process task; use exact stderr/exit/socket evidence to select a hosted worker fix, support-root repair or explicit external environment blocker
---

# Track A canonical physical runtime E2E v4 — blocked Xvfb startup checkpoint

The support filesystem is now complete and accepted by the trusted worker. The remaining bootstrap failure is specifically Xvfb startup: no X11 socket appeared. No canonical client was launched or registered. Further bootstrap attempts are disabled until a bounded isolated Xvfb-only test explains that failure.
