---
task_id: OTC-20260816-track-a-client-window-ownership-discriminator
status: completed
agent: ChatGPT
session_role: runtime_researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_discriminator
phase: archived
implementation_pr: 398
implementation_head: ef97a362dbcbd7bd5edb2465ea5a0693c92aee18
implementation_merge_commit: 207dd9956c09222393904f505cd6612b7ad13e88
base_main: 05d4a7136e234b874f7f112ad8c92f01b0aabd51
updated: 2026-08-16T18:32:00+02:00
policy_version: 2
prompting_standard_version: 2.1
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: ephemeral_isolated
runtime_namespace: track-a-client-window-discriminator-v1
target_uniqueness: PROVEN
mutation_authorized: true
persistent_session_role: none
physical_e2e_required: true
owner_funded_ai_api_authorized: false
canonical_state_access: NONE
credentials_login_gameplay: NONE
final_discriminator:
  governance_run: 31958546329
  run: 31958546334
  job: 95192878995
  result: SUCCESS
  display: ':231'
  exact_client_pid: 22224
  exact_client_alive_through_seconds: 35
  visible_windows_t05: 0
  visible_windows_t15: 0
  visible_windows_t35: 0
  marker_owned_descendants_observed: 0
  classification: CLIENT_ALIVE_NO_VISIBLE_WINDOWS_ON_ISOLATED_DISPLAY
  cleanup: COMPLETE
observed_graphics_errors:
  - QXcbIntegration cannot create platform OpenGL context; neither GLX nor EGL enabled
  - QRhiGles2 failed to create temporary context
  - QXcbIntegration cannot create platform offscreen surface; neither GLX nor EGL enabled
  - QRhiGles2 failed to create context
semantic_result: PROVEN_CLIENT_ALIVE_ZERO_VISIBLE_WINDOWS_WITH_QT_GL_CONTEXT_FAILURES
unknowns:
  - whether the GLX/EGL context failure is the sole cause of the missing visible window
  - exact graphics-stack/environment correction required
final_validation:
  final_head: ef97a362dbcbd7bd5edb2465ea5a0693c92aee18
  track_a_governance_run: 31958720125
  track_a_governance_result: SUCCESS
  repository_ci_run: 31958720501
  repository_ci_required_result: SUCCESS
  ready_state_repository_ci_run: 31958764005
  ready_state_repository_ci_required_result: SUCCESS
  review_threads_open: 0
coordinator_review:
  disposition: ACCEPT
  review_id: 4946641568
evidence:
  - docs/agents/evidence/OTC-20260816-track-a-client-window-ownership-discriminator/20260816-first-run-harness-pgid-failure.md
  - docs/agents/evidence/OTC-20260816-track-a-client-window-ownership-discriminator/20260816-second-run-snapshot-local-failure.md
  - docs/agents/evidence/OTC-20260816-track-a-client-window-ownership-discriminator/20260816-final-no-visible-window-gl-context.md
audit:
  result: PASS
  material_findings_open: 0
ownership: released
next_action: GitHub-hosted RUNTIME-INFRA graphics-stack compatibility research/fix; no further physical retry from this task
---

# Client-window ownership/startup discriminator — terminal archive

The terminal isolated diagnostic proved that the exact client remains alive while the isolated X11 display has zero visible windows through 35 seconds. The sanitized startup log directly records XCB/QRhiGles2 context creation failures with neither GLX nor EGL enabled. The task-owned sandbox was fully cleaned and no canonical runtime state, credentials or login were used. Ownership is released; graphics-stack compatibility is the selected next hosted-only boundary.
