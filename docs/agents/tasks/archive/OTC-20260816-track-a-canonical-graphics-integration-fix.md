---
task_id: OTC-20260816-track-a-canonical-graphics-integration-fix
status: completed
agent: ChatGPT
session_id: chatgpt-graphics-integration-fix-20260816
session_role: runtime_infrastructure_maintainer
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: runtime_worker_repair
phase: archived
base_branch: main
implementation_pr: 402
implementation_head: 74d5c09f53db42e69c703b06d06c4327a4913cec
implementation_merge_commit: 8b04ffd0c2a9c25b3a8fba942b55ccb6ca450044
risk: medium
updated: 2026-08-16T18:50:00+02:00
owned_paths: []
ownership_released: true
modules_touched: []
policy_version: 2
prompting_standard_version: 2.1
execution_class: github_hosted
runner: github-hosted
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
physical_e2e_completed: false
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
qt_primary_source_evidence:
  repository: qt/qtbase
  version: v6.9.3
  path: src/plugins/platforms/xcb/qxcbconnection.cpp
  blob: e6d232d0ef95023e8b1586b706743fc7f01c3711
  default_integrations: [xcb_glx, xcb_egl]
  qt_xcb_gl_integration_none_effect: clears_integration_candidate_list
implemented_fix:
  removed_environment_assignment: QT_XCB_GL_INTEGRATION=none
  preserved_environment_assignment: QT_QUICK_BACKEND=software
  added_nonsecret_diagnostic_assignment: QSG_INFO=1
  forced_specific_gl_backend: false
hosted_validation:
  semantic_head: c47b2acb06ad4e27f78b36e0130e350e8fb599bc
  run: 31959453898
  job: 95195086514
  result: SUCCESS
  session_tests: 11_PASS
  transition_tests: 9_PASS
  guard_tests: 3_PASS
  lease_tests: 14_PASS
  graphics_contract: PASS
  bash_n: PASS
  runtime_access: none
  physical_e2e: false
  temporary_validator_workflow_removed: true
final_validation:
  exact_head_governance_run: 31959541472
  exact_head_governance_result: SUCCESS
  exact_head_ci_run: 31959541458
  exact_head_ci_result: SUCCESS
  ready_state_ci_run: 31959655901
  ready_state_ci_result: SUCCESS
  review_threads_open: 0
audit:
  result: PASS
  material_findings_open: 0
safety:
  exact_client_fence_unchanged: true
  lease_registration_gate_contracts_unchanged: true
  rollback_contract_unchanged: true
  credentials_login_contract_unchanged: true
  physical_visible_window_success: UNKNOWN
  synology_glx_egl_availability: UNKNOWN
evidence_path: docs/agents/evidence/OTC-20260816-track-a-canonical-graphics-integration-fix/20260816-hosted-graphics-integration-fix.md
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
  canonical_registration: ABSENT
acceptance:
  - Qt XCB GL integration is no longer explicitly disabled by the canonical worker
  - software Qt Quick adaptation remains selected
  - QSG_INFO non-secret diagnostics are enabled
  - no specific QSG RHI backend is forced without physical evidence
  - hosted session/transition/guard/lease suites and graphics contract passed
  - implementation PR #402 merged through protected checks
  - no physical runtime, credentials, login or gameplay occurred in this task
next_action: fresh canonical RUNTIME bootstrap from current trusted main in a later owner invocation; it must re-run admission/support/identity gates and use QSG_INFO output to classify actual GLX/EGL/backend behavior before any success claim
---

# Track A canonical graphics integration fix — archived

The hosted repair is terminal. The canonical worker no longer sets `QT_XCB_GL_INTEGRATION=none`, preserves `QT_QUICK_BACKEND=software`, and adds `QSG_INFO=1`. Hosted contract validation and protected CI passed. Physical GLX/EGL availability and visible-window success remain intentionally unproven until a later fresh RUNTIME admission.
