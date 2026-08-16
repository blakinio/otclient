---
task_id: OTC-20260816-track-a-canonical-xcb-gl-integration-fix
status: implementing
agent: ChatGPT
session_id: chatgpt-xcb-gl-fix-20260816
session_role: runtime_infrastructure_maintainer
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: runtime_worker_repair
phase: implement
branch: fix/OTC-20260816-track-a-canonical-xcb-gl-integration
base_branch: main
base_main: a482bba877c881d31ae903a6f8acad24debfb5c5
risk: medium
updated: 2026-08-16T18:35:00+02:00
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/test_tibia_official_client_re_canonical_live_session.py
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-xcb-gl-integration-fix.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-xcb-gl-integration-fix/**
  - .github/workflows/tibia-official-client-re-canonical-xcb-gl-integration-fix.yml
modules_touched: []
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-client-window-ownership-discriminator.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-client-window-wait-fix.md
  - official Qt 6.9.3 qtbase source: src/plugins/platforms/xcb/qxcbconnection.cpp
  - official Qt 6.9.3 qtbase source: src/plugins/platforms/xcb/qxcbintegration.cpp
depends_on: []
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: observed physical failure is deterministically correlated with a trusted-worker Qt environment override and official Qt 6.9.3 source; the smallest repair is fully reviewable/testable without physical runtime access
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
  evidence: docs/agents/evidence/OTC-20260816-track-a-client-window-ownership-discriminator/20260816-final-no-visible-window-gl-context.md
  physical_run: 31958546334
  physical_job: 95192878995
  classification: PROVEN_CLIENT_ALIVE_ZERO_VISIBLE_WINDOWS_WITH_QT_GL_CONTEXT_FAILURES
  observed_log:
    - QXcbIntegration cannot create platform OpenGL context; neither GLX nor EGL enabled
    - QXcbIntegration cannot create platform offscreen surface; neither GLX nor EGL enabled
    - QRhiGles2 failed to create temporary/context
current_worker_override:
  QT_QUICK_BACKEND: software
  QT_XCB_GL_INTEGRATION: none
qt_6_9_3_source_correlation:
  qxcbconnection_blob: e6d232d0ef95023e8b1586b706743fc7f01c3711
  behavior: default candidates are xcb_glx then xcb_egl; QT_XCB_GL_INTEGRATION=none clears the integration candidate list
  qxcbintegration_blob: 5066a079614efd00730ced3bdd206b7c1f815464
  behavior_1: createPlatformOpenGLContext emits the observed neither-GLX-nor-EGL warning when glIntegration is null
  behavior_2: createPlatformOffscreenSurface emits the observed neither-GLX-nor-EGL warning when glIntegration is null
implementation_boundary:
  remove_forced_QT_XCB_GL_INTEGRATION_none: true
  preserve_QT_QUICK_BACKEND_software: true
  set_new_rhi_backend: false
  add_new_graphics_packages: false
  weaken_exact_client_or_runtime_identity: false
claim_boundary:
  proven_after_fix: trusted worker no longer deterministically disables both Qt XCB GLX/EGL integration candidates
  unknown_until_physical_runtime: whether available plugins/libs initialize successfully and whether a visible client window maps
acceptance:
  - canonical client launch environment no longer sets QT_XCB_GL_INTEGRATION=none
  - no replacement value is forced; Qt 6.9.3 default priority xcb_glx then xcb_egl is allowed to execute
  - QT_QUICK_BACKEND=software and all exact-client/lease/registration/rollback/secret boundaries remain unchanged
  - tests fail if QT_XCB_GL_INTEGRATION=none returns to production client launch
  - official Qt source correlation and physical discriminator are persisted as evidence
  - canonical session/transition/guard/lease tests pass GitHub-hosted
  - temporary validator removed and final governance/CI green before promotion
last_completed_step: correlated the exact physical GLX/EGL warnings with official Qt 6.9.3 source and identified the trusted worker's QT_XCB_GL_INTEGRATION=none as a deterministic integration-disable override
next_action: remove only the forced QT_XCB_GL_INTEGRATION=none production launch override, add regression tests/source evidence, validate hosted, then promote before one fresh canonical RUNTIME attempt
---

# Canonical Qt XCB GL integration repair

The current trusted worker explicitly forces `QT_XCB_GL_INTEGRATION=none`. Official Qt 6.9.3 source clears both `xcb_glx` and `xcb_egl` candidates for that value, and the physical discriminator observed the exact warnings Qt emits when no GL integration exists. This task removes only that forced disabling override and leaves all other runtime and safety boundaries unchanged.
