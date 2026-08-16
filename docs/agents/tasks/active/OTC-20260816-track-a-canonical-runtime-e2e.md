---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: implementing
agent: ChatGPT
session_id: chatgpt-runtime-v2-20260816-1601
session_role: runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: canonical-bootstrap
branch: ci/OTC-20260816-track-a-canonical-runtime-e2e-v2
base_branch: main
base_main: 259e418b2c526f93bd697f07c42b73b1fd40a914
risk: high
updated: 2026-08-16T16:03:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/**
  - .github/workflows/tibia-official-client-re-canonical-runtime-e2e-v2.yml
modules_touched: []
reuses:
  - .github/scripts/tibia-official-client-re-canonical-live-lease
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-bootstrap-implementation.md
supersedes_pr: 358
depends_on: []
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: physical Synology runtime is controlled only through repository GitHub Actions and trusted-main canonical transition primitives
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
context_pressure: high
context_growth: stable
context_score: 10
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: establish canonical persistent X11/VNC/exact-client first without credentials, then re-evaluate admission before any protected login or in-game E2E
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
canonical_registration: ABSENT_FROM_LAST_FRESH_RECONCILIATION_RECHECK_IN_WORKFLOW
canonical_lease_generation: RECHECK_IN_WORKFLOW
registration_lease_generation: NOT_APPLICABLE_BEFORE_BOOTSTRAP
gate_a: REQUIRED_RECHECK_IN_WORKFLOW
generation_rebind: NOT_APPLICABLE_IF_REGISTRATION_REMAINS_ABSENT
gate_b: REQUIRED_AFTER_BOOTSTRAP
bootstrap: TRUSTED_MAIN_IMPLEMENTED_PR_371
bootstrap_implementation_main: d16091ca29ff7c9330115e9ce0fdbfb41646e0dc
bootstrap_archive_main: 259e418b2c526f93bd697f07c42b73b1fd40a914
target_uniqueness: REPROVE_UNDER_LOCK
mutation_authorized: canonical_bootstrap_only_after_fresh_lease_and_under_lock_absence_inventory
owner_funded_ai_api_authorized: false
live_runtime_authorization_source: owner current instruction 2026-08-16 to finish the existing Track A tasks; this phase performs bootstrap without account credentials or login
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
excluded_runtime_surfaces:
  - Track B PR #284 namespace
  - historical closed PR #303 runtime surfaces
acceptance:
  - fresh authoritative lease status is read before mutation and current controller lease is acquired for this exact task/session
  - trusted-main bootstrap supervisor re-proves authoritative registration absence and complete all-official-client candidate absence while holding canonical coordination flock
  - exact client fence 15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe is proven by bootstrap
  - one persistent canonical X11 display and localhost-only VNC endpoint are created and bound to the exact registered client
  - canonical registration is atomically committed and immediate Gate B passes under the creation lease
  - controller lease is released while canonical X11/VNC/client remain alive idle
  - no credentials are read or typed during this bootstrap phase
  - no second official-client session or Track B/old PR #303 runtime is touched
  - subsequent protected login is attempted only after a fresh admission/rebind/Gate-B phase and credential authorization boundary is re-evaluated
last_completed_step: canonical bootstrap/rebind/Gate-B implementation was promoted and archived on trusted main through PR #371/#375
next_action: run the one-shot Synology bootstrap workflow from this fresh-main branch; if canonical bootstrap plus immediate Gate B pass, remove the workflow, persist sanitized registration evidence, close stale PR #358 superseded and reclassify the next RUNTIME phase
---

# Track A canonical physical runtime E2E v2

This is the fresh-main continuation of the stale read-only RUNTIME PR #358. The trusted base now contains the reviewed canonical bootstrap/rebind/Gate-B implementation and its terminal archive. The first physical mutation is intentionally limited to canonical bootstrap without account login: create one persistent private X11/VNC/exact-client runtime, publish the authoritative registration, prove immediate Gate B, release controller authority, and leave the registered runtime idle for the next admitted phase.
