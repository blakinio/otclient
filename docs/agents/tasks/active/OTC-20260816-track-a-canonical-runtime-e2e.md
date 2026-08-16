---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: implementing
agent: ChatGPT
session_id: chatgpt-runtime-v3-20260816-1644
session_role: runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: canonical-bootstrap
branch: ci/OTC-20260816-track-a-canonical-runtime-e2e-v3
base_branch: main
base_main: 67e5dc88ff4d6c241d90a046527dac4aa9f831d8
risk: high
updated: 2026-08-16T16:44:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/**
  - .github/workflows/tibia-official-client-re-canonical-runtime-e2e-v3.yml
modules_touched: []
reuses:
  - .github/scripts/tibia-official-client-re-canonical-live-lease
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-bootstrap-implementation.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-toolroot-layout-fix.md
supersedes_pr: 376
depends_on: []
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: physical Synology operation is dispatched only through repository-controlled GitHub Actions using trusted-main transition/worker code
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
bootstrap: TRUSTED_MAIN_IMPLEMENTED_AND_TOOLROOT_FIXED
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
prior_attempt:
  pr: 376
  run: 31952484701
  job: 95177998199
  runner: synology-otclient-01
  acquired_lease_generation: 1
  result: FAIL_CLOSED_XVFB_UNAVAILABLE
  registration_published: false
  rollback_semantics: transition kills bootstrap process group and invokes worker rollback on any unsuccessful bootstrap; absence of bootstrap_rollback_failed means rollback completed
  remediation_pr: 379
  remediation_archive_pr: 380
acceptance:
  - fresh authoritative lease and registration state are observed before mutation
  - if registration already exists, workflow refuses bootstrap and returns for reclassification rather than creating a second runtime
  - canonical lease is acquired for this exact task/session before transition bootstrap
  - trusted-main bootstrap re-proves registration absence and all-official-client candidate absence under canonical coordination lock
  - exact client fence 15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe is proven
  - one persistent localhost-only X11/VNC/exact-client runtime is created using the trusted selected toolroot
  - authoritative registration is committed and immediate same-generation Gate B passes
  - controller lease is released while canonical desktop/VNC/client remain alive idle
  - no credentials are read or typed and no login is attempted in this phase
  - no second Track A official-client runtime and no Track B/old PR #303 surface is touched
last_completed_step: toolroot layout repair #379 and lifecycle archive #380 were promoted to trusted main after hardened hosted validation
next_action: run exactly one bootstrap-only Synology workflow from this fresh-main branch; persist sanitized registration evidence if Gate B passes, otherwise stop at the new fail-closed discriminator without blind retry
---

# Track A canonical physical runtime E2E v3

This is the fresh trusted-main continuation after the fail-closed #376 toolroot defect was repaired and archived. The physical phase remains intentionally limited to creating and registering one persistent exact-client X11/VNC runtime without account login or credential use.
