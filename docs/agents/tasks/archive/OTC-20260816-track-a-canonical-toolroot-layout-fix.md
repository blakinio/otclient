---
task_id: OTC-20260816-track-a-canonical-toolroot-layout-fix
status: completed
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_infrastructure_fix
phase: closeout
implementation_pr: 379
implementation_merge_commit: ddc60eeed4583ed0d4df9a83f0abc5c6815d5d2a
risk: medium
updated: 2026-08-16T16:42:00+02:00
execution_mode: github-only
execution_class: github_hosted
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
mutation_authorized: false
owner_funded_ai_api_authorized: false
trigger_evidence:
  runtime_pr: 376
  run: 31952484701
  job: 95177998199
  runner: synology-otclient-01
  acquired_lease_generation: 1
  failure: TRACK_A_CANONICAL_SESSION_ERROR=xvfb_unavailable
  registration_published: false
result:
  production_allowlist:
    - /home/runner/_work/_otclient_tibia_re_state/toolroot
    - /work/_otclient_tibia_re_state/toolroot
  complete_root_requires: [Xvfb, x11vnc, xdotool, XKB_DATA, libproxychains.so.4]
  rejects_partial_root: true
  rejects_symlink_root: true
  rejects_intermediate_symlink_escape: true
  realpath_containment_required: true
  ambient_command_v_fallback: false
  bootstrap_persists_selected_root: true
  probe_reuses_persisted_root: true
validation:
  initial_focused_run: 31952903530
  initial_focused_job: 95179036978
  initial_focused_result: SUCCESS
  hardened_focused_run: 31953194192
  hardened_focused_result: SUCCESS
  hardened_governance_run: 31953194331
  hardened_governance_result: SUCCESS
  final_head: 4d01ede4407b08d60b4fe62b7803cd9cd6188011
  final_governance_run: 31953243120
  final_governance_result: SUCCESS
  final_repository_ci_run: 31953243231
  final_repository_ci_result: SUCCESS
  ready_state_ci_run: 31953363141
  ready_state_required_job: 95180317352
  ready_state_required_result: SUCCESS
  coordinator_review_id: 4946420289
  review_threads_open: 0
audit:
  result: PASS
  material_findings_open: 0
  notes:
    - an additional pre-merge review finding identified possible intermediate-symlink/ambient-tool substitution and was fixed before promotion
    - production root selection remains fixed and test candidate injection remains contract-test-only
    - no login/credential surface was added
e2e:
  result: NOT_APPLICABLE_WITH_REASON
  reason: hosted-only infrastructure repair; physical validation is the next fresh RUNTIME consumer
ownership_released: true
next_action: fresh-main redispatch OTC-20260816-track-a-canonical-runtime-e2e and retry canonical bootstrap exactly once under fresh admission
---

# Canonical support-toolroot layout fix — terminal closeout

PR #379 promoted the fail-closed support-toolroot resolver required by the physical canonical runtime. The worker now selects only one complete repository-known runner layout, requires support binaries/data to remain contained below that selected real root, persists the selection for probe consistency, and does not fall back to ambient X11 tools. Physical runtime creation remains separately RUNTIME-owned.
