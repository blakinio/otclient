---
task_id: OTC-20260816-track-a-canonical-xcb-gl-integration-fix
status: ready
agent: ChatGPT
session_id: chatgpt-xcb-gl-fix-clean-replay-20260816
session_role: runtime_infrastructure_maintainer
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: runtime_worker_repair
phase: coordinator-promotion-ready
branch: fix/OTC-20260816-track-a-canonical-xcb-gl-integration-v2
base_branch: main
base_main: a482bba877c881d31ae903a6f8acad24debfb5c5
risk: medium
updated: 2026-08-16T18:45:00+02:00
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/test_tibia_official_client_re_canonical_xcb_gl_integration.py
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-xcb-gl-integration-fix.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-xcb-gl-integration-fix/**
modules_touched: []
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-client-window-ownership-discriminator.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-client-window-wait-fix.md
  - official Qt 6.9.3 qtbase source qxcbconnection.cpp
  - official Qt 6.9.3 qtbase source qxcbintegration.cpp
supersedes_pr: 401
depends_on: []
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: clean promotion replay of a hosted-validated one-line trusted-worker environment repair; no physical runtime access is required or authorized
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
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
owner_funded_ai_api_authorized: false
source_discriminator:
  physical_pr: 398
  run: 31958546334
  job: 95192878995
  classification: PROVEN_CLIENT_ALIVE_ZERO_VISIBLE_WINDOWS_WITH_QT_GL_CONTEXT_FAILURES
  exact_client_alive_seconds: 35
  visible_windows_t05_t15_t35: [0, 0, 0]
  observed_qt_warnings:
    - Cannot create platform OpenGL context neither GLX nor EGL enabled
    - Cannot create platform offscreen surface neither GLX nor EGL enabled
    - QRhiGles2 failed to create context
source_correlation:
  qt_tag: v6.9.3
  qxcbconnection_blob: e6d232d0ef95023e8b1586b706743fc7f01c3711
  qxcbintegration_blob: 5066a079614efd00730ced3bdd206b7c1f815464
  default_candidate_order: [xcb_glx, xcb_egl]
  none_behavior: clears_candidate_list
implementation:
  remove_forced_QT_XCB_GL_INTEGRATION_none: true
  preserve_QT_QUICK_BACKEND_software: true
  force_replacement_xcb_integration: false
  force_new_rhi_backend: false
  add_graphics_packages: false
  exact_client_identity_changes: false
  lease_registration_gate_changes: false
semantic_validation:
  source_pr: 401
  source_head: 780fb47791109751570800f7af2e7d6342e37379
  run: 31959622751
  result: SUCCESS
  worker_shell_syntax: PASS
  xcb_gl_regression_tests: PASS
  canonical_session_tests: PASS
  canonical_transition_tests: PASS
  canonical_guard_tests: PASS
  canonical_lease_tests: PASS
  official_qt_blob_fences: PASS
  official_qt_source_invariants: PASS
  runtime_access: none
  physical_e2e: false
promotion_replay:
  temporary_validator_workflow_present: false
  semantic_change_equivalent_to_source_pr: true
  final_governance: PENDING
  final_repository_ci: PENDING
  review_threads_open: PENDING
claim_boundary:
  proven_after_fix: trusted worker no longer deterministically disables Qt XCB GLX/EGL integration candidates
  unknown_until_physical_runtime:
    - whether xcb_glx or xcb_egl is loadable on exact runtime
    - whether visible client window maps
    - whether canonical bootstrap publishes registration and passes Gate B
acceptance:
  - production client launch contains no QT_XCB_GL_INTEGRATION assignment
  - QT_QUICK_BACKEND=software remains present
  - no replacement XCB integration/RHI/OpenGL backend is forced
  - exact-client/WARP/lease/registration/Gate-B/rollback/secret boundaries are unchanged
  - hosted semantic validator passed all regression and canonical contract tests
  - clean promotion branch contains no task-owned temporary validator workflow
  - exact-head Track A governance and repository CI pass before promotion
last_completed_step: replayed the hosted-validated worker/test/evidence package onto a clean promotion branch without the temporary validator workflow
next_action: open clean Draft PR, close validated-source PR #401 as superseded, obtain final exact-head governance/CI/review hygiene, coordinator-promote and archive, then fresh RUNTIME validation from resulting trusted main
---

# Canonical Qt XCB GL integration repair — clean promotion replay

This clean replay removes only the forced `QT_XCB_GL_INTEGRATION=none` assignment from the canonical client launch environment. The change was already validated on GitHub-hosted infrastructure against exact official Qt 6.9.3 source and the full canonical session/transition/guard/lease test suite. Physical behavior remains unknown until a separately admitted fresh RUNTIME attempt after promotion.
