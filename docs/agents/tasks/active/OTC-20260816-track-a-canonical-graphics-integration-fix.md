---
task_id: OTC-20260816-track-a-canonical-graphics-integration-fix
status: implementing
agent: ChatGPT
session_id: chatgpt-graphics-integration-fix-20260816
session_role: runtime_infrastructure_maintainer
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: runtime_worker_repair
phase: hosted-implementation
branch: fix/OTC-20260816-track-a-canonical-graphics-integration-fix
base_branch: main
base_main: a482bba877c881d31ae903a6f8acad24debfb5c5
risk: medium
updated: 2026-08-16T18:35:00+02:00
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/test_tibia_official_client_re_canonical_live_session.py
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-graphics-integration-fix.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-graphics-integration-fix/**
modules_touched: []
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-client-window-ownership-discriminator.md
  - docs/agents/evidence/OTC-20260816-track-a-client-window-ownership-discriminator/20260816-final-no-visible-window-gl-context.md
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - upstream Qt 6.9.3 src/plugins/platforms/xcb/qxcbconnection.cpp
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: direct runtime evidence selected a graphics-stack compatibility boundary, while Qt 6.9.3 primary source proves the trusted worker explicitly disables both XCB GLX and EGL integrations through QT_XCB_GL_INTEGRATION=none; correction can be implemented and contract-tested without physical runtime access
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
runner: github-hosted
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
source_runtime_evidence:
  discriminator_pr: 398
  discriminator_run: 31958546334
  discriminator_job: 95192878995
  classification: PROVEN_CLIENT_ALIVE_ZERO_VISIBLE_WINDOWS_WITH_QT_GL_CONTEXT_FAILURES
  observed_messages:
    - QXcbIntegration cannot create platform OpenGL context; neither GLX nor EGL enabled
    - QRhiGles2 failed to create temporary context
    - QXcbIntegration cannot create platform offscreen surface; neither GLX nor EGL enabled
    - QRhiGles2 failed to create context
qt_primary_source_evidence:
  repository: qt/qtbase
  version: v6.9.3
  path: src/plugins/platforms/xcb/qxcbconnection.cpp
  behavior:
    - default XCB GL integration priority is xcb_glx then xcb_egl
    - QT_XCB_GL_INTEGRATION is read from the environment
    - value none clears the XCB GL integration candidate list completely
selected_fix:
  remove_environment_assignment: QT_XCB_GL_INTEGRATION=none
  preserve_environment_assignment: QT_QUICK_BACKEND=software
  add_nonsecret_diagnostic_assignment: QSG_INFO=1
  force_specific_gl_backend: false
  rationale: restore Qt's own GLX/EGL integration selection without prematurely forcing a particular backend; retain software Qt Quick adaptation and improve non-secret scenegraph diagnostics
safety:
  exact_client_fence_unchanged: true
  lease_registration_gate_contracts_unchanged: true
  rollback_contract_unchanged: true
  credentials_login_contract_unchanged: true
  physical_success_claimed: false
acceptance:
  - canonical worker no longer exports QT_XCB_GL_INTEGRATION=none
  - canonical worker still exports QT_QUICK_BACKEND=software
  - canonical worker exports QSG_INFO=1 for bounded non-secret graphics initialization diagnostics
  - source-level tests pin all three invariants
  - existing canonical session/transition/guard/lease tests remain green
  - no Synology, X11/VNC, client launch, credentials or canonical runtime access is used by this task
  - exact-head governance and repository CI pass before promotion
last_completed_step: terminal window discriminator selected graphics-stack compatibility; Qt 6.9.3 primary source proved QT_XCB_GL_INTEGRATION=none disables both xcb_glx and xcb_egl integration candidates
next_action: implement the minimal worker environment correction and hosted contract tests, validate exact-head governance/CI, then coordinator-promote/archive; physical canonical validation belongs to a later invocation
---

# Track A canonical graphics integration fix

This hosted-only repair removes the worker's explicit XCB GL integration disablement while preserving the software Qt Quick backend. It does not claim that GLX/EGL is available on the runner or that a visible client window will result; those remain physical-validation questions for a later fresh RUNTIME admission.
