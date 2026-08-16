---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: implementing
agent: ChatGPT
session_id: chatgpt-runtime-v5-20260816-1734
session_role: runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: canonical-bootstrap
branch: ci/OTC-20260816-track-a-canonical-runtime-e2e-v5
base_branch: main
base_main: b69084067de24528b1f763ab9630f638e8bcf092
risk: high
updated: 2026-08-16T17:34:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/**
  - .github/workflows/tibia-official-client-re-canonical-runtime-e2e-v5.yml
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
depends_on: []
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: one serialized physical bootstrap is dispatched through repository-controlled GitHub Actions using only current trusted-main transition/worker code after the isolated Xvfb/xkbcomp blocker was repaired and promoted
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
canonical_lease_generation: UNKNOWN
registration_lease_generation: NOT_APPLICABLE
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: REQUIRED_NOT_PROVEN
target_uniqueness: UNKNOWN
mutation_authorized: false
owner_funded_ai_api_authorized: false
live_runtime_authorization_source: owner instruction 2026-08-16 to finish the existing Track A tasks; this phase authorizes only gate-controlled canonical bootstrap/Gate-B and uses no account credentials or login input
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
    remediation: trusted toolroot resolver repair #379/#380
  - pr: 381
    run: 31953635875
    job: 95180815033
    acquired_lease_generation: 2
    result: TOOLROOT_UNAVAILABLE_BEFORE_WARP_X11_CLIENT
    remediation: layout inventory #382/#383 plus x11vnc repair #384/#385
  - pr: 386
    run: 31954637565
    job: 95183271514
    acquired_lease_generation: 3
    result: XVFB_SOCKET_MISSING_BEFORE_CLIENT_REGISTRATION
    registration_published: false
    gate_b_reached: false
    credentials_used: false
    remediation: isolated discriminator #387, inventory #388 and system xkbcomp repair #389/#391
resolved_support_proof:
  toolroot: /work/_otclient_tibia_re_state/toolroot
  contained_x11vnc_sha256: 4954921ae9c4e2bf7061603eb6a2d52c2292a0973eb2da5d6f48a9bd49570ffc
  system_xkbcomp_path: /usr/bin/xkbcomp
  system_xkbcomp_sha256: 0967e7e7b03b077327cea74567726b265bd304b4fdf59f87bf7fdfe1074e7591
  system_xkbcomp_repair_run: 31955642775
  isolated_xvfb_socket_result: PASS
  isolated_xvfb_display: ':199'
bootstrap_phase_boundary:
  credentials_allowed: false
  login_allowed: false
  create_second_runtime_if_registration_exists: false
  exact_client_version: 15.32.df7b29
  exact_client_size: 51965216
  exact_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
acceptance:
  - current trusted main/base is fenced before physical work
  - fixed support-root preflight passes and the trusted worker resolves the contained root
  - fresh authoritative lease and registration state are observed before mutation
  - existing registration or unregistered canonical session root fails closed rather than creating a second runtime
  - canonical lease is acquired for this exact task/session before transition bootstrap
  - trusted-main bootstrap re-proves registration absence and all-official-client candidate absence under the canonical coordination lock
  - exact client fence is proven before publication
  - one persistent localhost-only X11/VNC/exact-client runtime is created and authoritative registration is atomically committed
  - immediate same-generation Gate B passes before controller release
  - controller lease is released while the registered desktop/VNC/client remain alive idle
  - no account credentials are consumed and no login is attempted in this phase
  - any new fail-closed discriminator stops this phase and the one-shot workflow is removed before further work
last_completed_step: closed stale runtime PR #386 after xkbcomp repair #389 was promoted/archived; claimed one fresh current-main v5 canonical-bootstrap phase with fail-closed admission and no credential authority
next_action: dispatch exactly one repository-controlled bootstrap/Gate-B attempt on synology-otclient-01; on PASS persist sanitized registration/lease evidence and stop before login, on any new discriminator remove the one-shot workflow and persist the blocker without blind retry
---

# Track A canonical physical runtime E2E v5

This is the sole fresh RUNTIME claim after the Xvfb absolute-helper blocker was repaired. The phase may create the canonical idle runtime only through trusted-main bootstrap and immediate Gate B. It does not authorize login or credentials.
