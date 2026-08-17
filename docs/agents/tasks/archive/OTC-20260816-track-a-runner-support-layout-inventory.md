---
task_id: OTC-20260816-track-a-runner-support-layout-inventory
status: completed
agent: ChatGPT
session_role: runtime_observer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_infrastructure_inventory
phase: closeout
implementation_pr: 382
implementation_merge_commit: 0485a23786bf5452125312bf6cfa49abeb1883a5
risk: low
updated: 2026-08-16T16:55:00+02:00
execution_mode: github-only
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: read_only
persistent_session_role: none
physical_e2e_required: false
runtime_owner_task: OTC-20260816-track-a-runner-support-layout-inventory
runtime_namespace: runner-support-layout
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: false
owner_funded_ai_api_authorized: false
execution:
  run: 31953830754
  job: 95181286228
  result: SUCCESS
result:
  classification: PROVEN_SPLIT_SUPPORT_LAYOUT
  home_work_root: ABSENT
  work_root: /work/_otclient_tibia_re_state/toolroot
  work_root_Xvfb: PRESENT_EXECUTABLE_CONTAINED
  work_root_xdotool: PRESENT_EXECUTABLE_CONTAINED
  work_root_XKB: PRESENT_CONTAINED
  work_root_libproxychains: PRESENT_CONTAINED
  work_root_x11vnc: ABSENT
  system_x11vnc: /usr/bin/x11vnc
  system_x11vnc_package: x11vnc_0.9.16-10_INSTALLED
  system_Xvfb: ABSENT
  system_xdotool: ABSENT
  system_XKB: ABSENT
  system_libproxychains: ABSENT
root_cause: the hardened one-root worker fails because the persistent toolroot lacks only x11vnc while the current runner provides x11vnc as a system package
safe_repair_boundary: keep the hardened one-root worker unchanged and stage the verified system /usr/bin/x11vnc into the contained persistent /work toolroot under a separate bounded runner-infrastructure repair
validation:
  initial_repository_ci_run: 31953921816
  initial_repository_ci_result: SUCCESS
  corrected_governance_run: 31953980543
  corrected_governance_result: SUCCESS
  corrected_repository_ci_run: 31953980663
  corrected_repository_ci_result: SUCCESS
  ready_state_ci_run: 31954058597
  ready_state_required_job: 95181871168
  ready_state_required_result: SUCCESS
  coordinator_review_id: 4946451027
  review_threads_open: 0
audit:
  result: PASS
  material_findings_open: 0
  notes:
    - the first governance failure was task-metadata-only and was corrected without repeating the physical observation
    - the one-shot workflow was removed before checkpoint updates
    - no official-client/canonical runtime/process/display/VNC/network/login/credential state was observed
e2e:
  result: NOT_APPLICABLE_WITH_REASON
  reason: bounded support-filesystem metadata observation only
ownership_released: true
next_action: execute a separately reviewed runner-support repair that verifies the installed system x11vnc package/binary and stages an identical contained copy into /work/_otclient_tibia_re_state/toolroot/usr/bin/x11vnc; then fresh-current-main RUNTIME bootstrap may retry once
---

# Dedicated runner support-layout inventory — terminal closeout

The live dedicated runner has a proven split support layout. The persistent contained toolroot has every required component except x11vnc, while `/usr/bin/x11vnc` is installed as package version `0.9.16-10`. The next repair should complete the existing contained toolroot rather than weakening the trusted worker's one-root/realpath containment boundary.
