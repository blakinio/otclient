---
task_id: OTC-20260816-track-a-client-window-ownership-discriminator
status: ready
agent: ChatGPT
session_id: chatgpt-window-discriminator-20260816
session_role: runtime_researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_discriminator
phase: coordinator-promotion-ready
branch: ci/OTC-20260816-track-a-client-window-ownership-discriminator
base_branch: main
base_main: 05d4a7136e234b874f7f112ad8c92f01b0aabd51
risk: high
updated: 2026-08-16T18:30:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-client-window-ownership-discriminator.md
  - docs/agents/evidence/OTC-20260816-track-a-client-window-ownership-discriminator/**
modules_touched: []
reuses:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/20260816-v6-client-window-missing.md
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
depends_on: []
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: final physical discriminator completed in one task-owned ephemeral namespace, proved the missing-window state and cleaned all task-owned resources; no canonical lease/registration state was touched
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260816-track-a-client-window-ownership-discriminator
runtime_namespace: track-a-client-window-discriminator-v1
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: true
persistent_session_role: none
physical_e2e_required: true
owner_funded_ai_api_authorized: false
canonical_boundary:
  read_or_write_canonical_lease: false
  read_or_write_canonical_registration: false
  publish_registration: false
  login_allowed: false
  credentials_allowed: false
  gameplay_allowed: false
  track_b_access: false
exact_client_fence:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
prior_harness_failures:
  - run: 31957940075
    job: 95191373266
    result: CLIENT_NOT_ISOLATED_GROUP_BEFORE_OBSERVATION
    cleanup: COMPLETE
  - run: 31958323922
    job: 95192357706
    result: SNAPSHOT_LOCAL_LABEL_UNBOUND_BEFORE_WINDOW_CAPTURE
    cleanup: COMPLETE
final_discriminator:
  head: d65a883baa75e6de7b356c6f66b555b9aeb93a6c
  governance_run: 31958546329
  governance_result: SUCCESS
  run: 31958546334
  job: 95192878995
  result: SUCCESS
  immutable_source_blob: 1616edcc982be50ef2c95b8077160ec8fe9291fe
  source_blob_fence: PASS
  bash_n: PASS
  ancestry_only: PASS
  canonical_state_access: NONE
  exact_source_fence: PASS
  display: ':231'
  vnc_port: 6200
  warp: PASS
  launchermetadata_branch: SOURCE_ABSENT_OR_UNSAFE
  xvfb: PASS
  vnc: PASS
  client_pid: 22224
  client_pgid: 22224
  client_start: PASS
  t05_client_alive: true
  t05_visible_windows: 0
  t15_client_alive: true
  t15_visible_windows: 0
  t35_client_alive: true
  t35_visible_windows: 0
  marker_owned_descendants_observed: 0
  client_log_total_lines: 86
  classification: CLIENT_ALIVE_NO_VISIBLE_WINDOWS_ON_ISOLATED_DISPLAY
  cleanup: COMPLETE
observed_graphics_errors:
  - QXcbIntegration cannot create platform OpenGL context; neither GLX nor EGL enabled
  - QRhiGles2 failed to create temporary context
  - QXcbIntegration cannot create platform offscreen surface; neither GLX nor EGL enabled
  - QRhiGles2 failed to create context
  - failed to acquire GL context to resolve capabilities, using defaults
other_positive_startup_evidence:
  - Asset loading complete
  - HTTPS to static.tibia.com passed through task-owned proxy
  - HTTPS to www.tibia.com passed through task-owned proxy
result:
  classification: PROVEN_CLIENT_ALIVE_ZERO_VISIBLE_WINDOWS_WITH_QT_GL_CONTEXT_FAILURES
  proven:
    - exact client remained alive through 35 seconds
    - zero visible X11 windows existed at 5, 15 and 35 seconds on isolated display
    - no marker-owned descendant window/process was observed in bounded ancestry
    - Qt log reports GLX/EGL/QRhiGles2 context creation failures
    - asset loading and HTTPS startup activity proceeded
  unknown:
    - whether GL context failure is sole cause of missing visible window
    - exact graphics environment correction required for visible window
    - canonical runtime identity, which remains unregistered
one_shot_workflows_removed: true
evidence:
  - docs/agents/evidence/OTC-20260816-track-a-client-window-ownership-discriminator/20260816-first-run-harness-pgid-failure.md
  - docs/agents/evidence/OTC-20260816-track-a-client-window-ownership-discriminator/20260816-second-run-snapshot-local-failure.md
  - docs/agents/evidence/OTC-20260816-track-a-client-window-ownership-discriminator/20260816-final-no-visible-window-gl-context.md
audit:
  result: PASS
  material_findings_open: 0
acceptance:
  - semantic window/startup discriminator captured: PASS
  - task-owned cleanup: PASS
  - canonical state untouched: PASS
  - credentials/login/gameplay absent: PASS
  - no further physical retry from this task
last_completed_step: final run 31958546334/job 95192878995 proved exact client alive with zero visible windows through 35 seconds and direct Qt GLX/EGL/QRhiGles2 context failures; cleanup completed and final evidence was persisted
next_action: promote/archive this discriminator, update canonical RUNTIME blocker, then execute GitHub-hosted RUNTIME-INFRA graphics-stack compatibility research/fix before any new physical canonical bootstrap
---

# Track A client-window ownership/startup discriminator — terminal candidate

The isolated physical discriminator is complete. It rules out a simple window-title/PID mismatch: the exact client remains alive but the task-owned X11 display has zero visible windows through 35 seconds. The startup log directly reports failure to create Qt OpenGL/offscreen contexts because neither GLX nor EGL is enabled. This evidence selects graphics-stack compatibility as the next hosted-only research/fix boundary; no further physical retry belongs to this task.
