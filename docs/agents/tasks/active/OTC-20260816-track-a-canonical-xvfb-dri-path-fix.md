---
task_id: OTC-20260816-track-a-canonical-xvfb-dri-path-fix
status: ready
agent: ChatGPT
session_id: chatgpt-canonical-xvfb-dri-path-fix-20260816
session_role: implementation_engineer
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: implementation
phase: coordinator-promotion-ready
branch: fix/OTC-20260816-track-a-canonical-xvfb-dri-path
base_branch: main
base_main: d3f186414256151c9d5e03f34c5a9026b1fba500
risk: high
updated: 2026-08-16T21:01:00+02:00
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/test_tibia_official_client_re_canonical_live_session.py
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-xvfb-dri-path-fix.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-xvfb-dri-path-fix/**
modules_touched:
  - canonical Track A runtime session worker
reuses:
  - PR #420 causal LIBGL_DRIVERS_PATH proof as unpromoted research input only
  - PR #421 minimality proof as unpromoted research input only
  - current trusted main canonical session worker and tests
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: physical research isolated the missing canonical Xvfb GLX prerequisite to the contained DRI provider search path; implementation and validation are hosted-only and must reach trusted main before any fresh physical runtime redispatch
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: heavy
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
runner: github-hosted
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
persistent_session_role: none
physical_e2e_required: false
owner_funded_ai_api_authorized: false
implementation:
  worker:
    contained_dri_root_helper: added
    toolroot_requires_contained_dri_provider: true
    bootstrap_derives_dri_from_selected_toolroot: true
    xvfb_environment_LIBGL_DRIVERS_PATH: '$dri'
    xvfb_argument_change: none
    client_environment_change: none
  tests:
    complete_fixture_contains_swrast_provider: true
    missing_swrast_rejected: true
    escaping_swrast_rejected: true
    xvfb_source_contract_added: true
    client_no_dri_env_leak_contract_added: true
hosted_validation:
  implementation_head_with_validator: cf9f361389972dcfe3f8c29db2ecd1c4c147c3ab
  validator_run: 31966128631
  validator_job: 95211462614
  result: SUCCESS
  shell_syntax: PASS
  canonical_session_tests: 14_of_14_PASS
  canonical_transition_tests: 9_of_9_PASS
  canonical_guard_tests: 3_of_3_PASS
  canonical_lease_tests: 14_of_14_PASS
  minimal_xvfb_dri_source_contract: PASS
  temporary_validator_removed: true
prior_governance:
  implementation_head: a57d7671f23335f43fd189991ac138dee9064315
  run: 31966079573
  deterministic_policy_audit: SUCCESS
  fresh_admission_behavior_audit: SUCCESS
final_validation:
  governance: PENDING_EXACT_FINAL_HEAD
  repository_ci: PENDING_EXACT_FINAL_HEAD
  physical_e2e: NOT_APPLICABLE_WITH_REASON
  physical_e2e_reason: hosted-only worker implementation; physical runtime may execute only after coordinator promotion to trusted main and fresh RUNTIME admission
evidence:
  - docs/agents/evidence/OTC-20260816-track-a-canonical-xvfb-dri-path-fix/20260816-hosted-validation.md
audit:
  result: PASS_PENDING_EXACT_FINAL_HEAD_CHECKS
  material_findings_open: 0
  notes:
    - the dedicated hosted validator exercised session, transition, guard and lease suites
    - no temporary workflow remains in the delivery diff
    - no Synology or official-client runtime execution occurred in this implementation PR
acceptance:
  - worker syntax: PASS
  - session unit/contract tests: PASS
  - transition/guard/lease suites: PASS
  - DRI containment/source contracts: PASS
  - temporary validation workflow removed: PASS
  - exact-final-head normal governance and CI: PENDING
  - physical runtime execution: NOT_APPLICABLE_WITH_REASON
last_completed_step: implemented the minimal fail-closed contained DRI provider contract and Xvfb-only LIBGL_DRIVERS_PATH assignment; hosted validator run 31966128631/job 95211462614 passed all targeted suites and source contracts, then the temporary workflow was removed
next_action: obtain exact-final-head normal Track A governance and repository CI, update the terminal handoff without changing code semantics, and leave the Draft for coordinator promotion; only after promotion may RUNTIME redispatch from trusted main
---

# Track A canonical Xvfb DRI-path fix — terminal candidate

The repository repair is implemented and hosted-validated. No physical success is claimed; the next physical attempt is gated on coordinator promotion and a fresh trusted-main RUNTIME admission.