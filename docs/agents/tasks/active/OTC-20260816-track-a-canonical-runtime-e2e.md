---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: implementing
agent: ChatGPT
session_id: chatgpt-runtime-v4-20260816-1705
session_role: runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: canonical-bootstrap
branch: ci/OTC-20260816-track-a-canonical-runtime-e2e-v4
base_branch: main
base_main: 917b8ab943fd9aa1fded50c9a0b8b4e1dfeb5cbb
risk: high
updated: 2026-08-16T17:05:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/**
  - .github/workflows/tibia-official-client-re-canonical-runtime-e2e-v4.yml
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
depends_on: []
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: physical Synology operation is dispatched only through repository-controlled GitHub Actions using current trusted-main transition/worker code and the now-complete persistent contained toolroot
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
canonical_registration: RECHECK_IN_WORKFLOW
canonical_lease_generation: RECHECK_IN_WORKFLOW
registration_lease_generation: NOT_APPLICABLE_IF_REGISTRATION_ABSENT
gate_a: REQUIRED_FRESH_IN_WORKFLOW
generation_rebind: NOT_APPLICABLE_IF_REGISTRATION_ABSENT
gate_b: REQUIRED_AFTER_BOOTSTRAP
bootstrap: TRUSTED_MAIN_IMPLEMENTED_AND_SUPPORT_ROOT_COMPLETE
target_uniqueness: REPROVE_UNDER_LOCK
mutation_authorized: false
owner_funded_ai_api_authorized: false
live_runtime_authorization_source: owner instruction 2026-08-16 to finish existing Track A tasks, subject to current admission gates; this phase performs bootstrap only and does not use account credentials
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
    remediation: layout inventory #382/#383 plus contained x11vnc support repair #384/#385
support_root_proof:
  root: /work/_otclient_tibia_re_state/toolroot
  completion_run: 31954295453
  completion_job: 95182427755
  x11vnc_sha256: 4954921ae9c4e2bf7061603eb6a2d52c2292a0973eb2da5d6f48a9bd49570ffc
  trusted_worker_contract_test: PASS_CONTAINED_TOOLROOT_COMPLETE
acceptance:
  - fresh authoritative lease and registration state are observed before mutation
  - registration/session prechecks fail closed rather than creating a second runtime
  - canonical lease is acquired for this exact task/session before transition bootstrap
  - trusted-main bootstrap re-proves registration absence and complete all-official-client candidate absence under canonical coordination lock
  - exact client fence 15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe is proven
  - trusted worker resolves the persistent complete contained support root before WARP/X11/client creation
  - one persistent localhost-only X11/VNC/exact-client runtime is created and authoritative registration is atomically committed
  - immediate same-generation Gate B passes before controller release
  - controller lease is released while canonical desktop/VNC/client remain alive idle
  - no account credentials are read or typed and no login is attempted in this phase
  - no second Track A official-client runtime and no Track B/old PR #303 surface is touched
  - any new fail-closed discriminator stops the physical phase; no blind retry
last_completed_step: contained x11vnc support repair #384 merged and archived via #385; trusted worker contract-test now accepts the persistent /work toolroot as complete
next_action: run exactly one bootstrap-only Synology workflow from this fresh-main branch; if registration plus immediate Gate B pass, remove workflow and persist sanitized registration/runtime identity evidence, otherwise stop at the new discriminator
---

# Track A canonical physical runtime E2E v4

This is the fresh trusted-main canonical bootstrap after both worker hardening and physical runner-support completion. The phase is deliberately limited to creating and registering one persistent exact-client X11/VNC runtime without account login or credential use.
