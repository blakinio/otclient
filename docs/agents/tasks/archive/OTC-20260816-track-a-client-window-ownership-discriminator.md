---
task_id: OTC-20260816-track-a-client-window-ownership-discriminator
status: completed
agent: ChatGPT
session_id: chatgpt-window-discriminator-20260816
session_role: runtime_researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_discriminator
phase: archived
base_branch: main
implementation_pr: 398
implementation_head: ef97a362dbcbd7bd5edb2465ea5a0693c92aee18
implementation_merge_commit: 207dd9956c09222393904f505cd6612b7ad13e88
risk: high
updated: 2026-08-16T18:31:00+02:00
owned_paths: []
ownership_released: true
modules_touched: []
policy_version: 2
prompting_standard_version: 2.1
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
physical_e2e_completed: true
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
exact_client_fence:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
result:
  classification: PROVEN_CLIENT_ALIVE_ZERO_VISIBLE_WINDOWS_WITH_QT_GL_CONTEXT_FAILURES
  semantic_classification: CLIENT_ALIVE_NO_VISIBLE_WINDOWS_ON_ISOLATED_DISPLAY
  exact_client_alive_through_seconds: 35
  visible_windows_t05: 0
  visible_windows_t15: 0
  visible_windows_t35: 0
  marker_owned_descendants_observed: 0
  observed_graphics_errors:
    - QXcbIntegration cannot create platform OpenGL context; neither GLX nor EGL enabled
    - QRhiGles2 failed to create temporary context
    - QXcbIntegration cannot create platform offscreen surface; neither GLX nor EGL enabled
    - QRhiGles2 failed to create context
  positive_startup_evidence:
    - Asset loading complete
    - task-owned proxied HTTPS startup activity proceeded
  graphics_error_as_sole_root_cause: UNKNOWN
physical_validation:
  final_wrapper_head: d65a883baa75e6de7b356c6f66b555b9aeb93a6c
  run: 31958546334
  job: 95192878995
  result: SUCCESS
  immutable_source_blob: 1616edcc982be50ef2c95b8077160ec8fe9291fe
  source_blob_fence: PASS
  bash_n: PASS
  ancestry_only_cleanup: PASS
  canonical_state_access: NONE
  task_cleanup: COMPLETE
  credentials_used: false
  login_attempted: false
  gameplay_input_used: false
validation:
  exact_head_governance_run: 31958720125
  exact_head_governance_result: SUCCESS
  exact_head_ci_run: 31958720501
  exact_head_ci_result: SUCCESS
  ready_state_ci_run: 31958764005
  ready_state_ci_result: SUCCESS
  review_threads_open: 0
audit:
  result: PASS
  material_findings_open: 0
evidence:
  - docs/agents/evidence/OTC-20260816-track-a-client-window-ownership-discriminator/20260816-first-run-harness-pgid-failure.md
  - docs/agents/evidence/OTC-20260816-track-a-client-window-ownership-discriminator/20260816-second-run-snapshot-local-failure.md
  - docs/agents/evidence/OTC-20260816-track-a-client-window-ownership-discriminator/20260816-final-no-visible-window-gl-context.md
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
  canonical_registration: ABSENT
acceptance:
  - bounded window/process/startup discriminator completed
  - exact client remained alive while isolated display had zero visible windows at all bounded snapshots
  - simple wrong-title and visible child-owned-window hypotheses were excluded for the observation window
  - direct Qt GLX/EGL/QRhiGles2 context failures were captured without promoting them to sole root cause
  - every task-owned process/display/network helper was cleaned
  - no canonical lease/registration mutation, credentials, login or gameplay occurred
  - implementation PR #398 merged through protected checks
next_action: GitHub-hosted RUNTIME-INFRA graphics-stack compatibility analysis/fix must identify and validate the minimal safe graphics/render-backend correction before any new physical canonical bootstrap
---

# Track A client-window ownership/startup discriminator — archived

The discriminator is terminal. It proved that the exact client remains alive while the isolated X11 display has zero visible windows through 35 seconds, and it captured direct Qt GLX/EGL/QRhiGles2 context-creation failures. This does not prove that the graphics-context failure is the sole root cause. No further physical retry belongs to this task; ownership and mutation authority are released.
