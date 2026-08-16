---
task_id: OTC-20260816-track-a-runner-support-layout-inventory
status: ready
agent: ChatGPT
session_id: chatgpt-runner-support-inventory-20260816-1650
session_role: runtime_observer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_infrastructure_inventory
phase: coordinator-promotion-ready
branch: ci/OTC-20260816-track-a-runner-support-layout-inventory
base_branch: main
base_main: 67e5dc88ff4d6c241d90a046527dac4aa9f831d8
risk: low
updated: 2026-08-16T16:54:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-runner-support-layout-inventory.md
  - docs/agents/evidence/OTC-20260816-track-a-runner-support-layout-inventory/**
modules_touched: []
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-toolroot-layout-fix.md
  - physical failure evidence from PR #381 run 31953635875/job 95180815033
  - PR #280 proposed dedicated-runner Dockerfile as design input only, not current deployment proof
depends_on: []
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
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
observation_allowlist:
  - /home/runner/_work/_otclient_tibia_re_state/toolroot
  - /work/_otclient_tibia_re_state/toolroot
  - /usr/bin/Xvfb
  - /usr/bin/x11vnc
  - /usr/bin/xdotool
  - /usr/share/X11/xkb
  - /usr/lib/x86_64-linux-gnu/libproxychains.so.4
  - /lib/x86_64-linux-gnu/libproxychains.so.4
  - dpkg metadata for xvfb/x11vnc/xdotool/proxychains4
forbidden_observation:
  - official client files or processes
  - /proc process inventory
  - canonical runtime registration/lease/session directories
  - X11 display/window state
  - VNC listener or endpoint state
  - network/game/login state
  - credentials or environment secrets
  - Track B PR #284 surfaces
execution:
  run: 31953830754
  job: 95181286228
  runner: synology-otclient-01
  result: SUCCESS
  one_shot_workflow: REMOVED_AFTER_CAPTURE
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
  system_xvfb_package: NOT_INSTALLED
  system_xdotool_package: NOT_INSTALLED
  system_proxychains4_package: NOT_INSTALLED
root_cause:
  finding: trusted one-root completeness gate fails only because the persistent /work toolroot lacks x11vnc, while current runner provides x11vnc at a fixed system path
  safe_repair_boundary: preserve /work toolroot for Xvfb/xdotool/XKB/libproxychains and permit only literal /usr/bin/x11vnc as an explicit system exception with ownership/mode/package checks; no ambient PATH discovery or generic system fallback
evidence_path: docs/agents/evidence/OTC-20260816-track-a-runner-support-layout-inventory/20260816-support-layout.md
validation:
  physical_inventory_result: SUCCESS
  governance_after_workflow_removal: RECHECK_AFTER_ADMISSION_NORMALIZATION
  repository_ci_after_workflow_removal: SUCCESS_RUN_31953921816
  review_threads_open: 0
  physical_e2e: NOT_APPLICABLE_WITH_REASON
  physical_e2e_reason: support-filesystem metadata observation only; no client/runtime behavior exercised
audit:
  result: PASS
  material_findings_open: 0
  notes:
    - current running runner layout is directly proven and supersedes historical assumptions about a complete toolroot
    - PR #280 Dockerfile remains design input only and is not used as proof of current deployment
    - no canonical runtime/client/process/display/VNC/network/credential state was observed
    - initial deterministic governance failure was task-metadata-only: read_only admission now uses the contract's exact NOT_APPLICABLE gates and target_uniqueness PROVEN
last_completed_step: completed one read-only physical support-layout inventory, removed the one-shot workflow, persisted the exact split-layout root cause and normalized the durable read-only admission record
next_action: obtain exact-head governance/CI and merge this sanitized evidence; then implement/promote a hosted-only explicit split-layout worker repair before any further bootstrap attempt
---

# Track A dedicated-runner support layout inventory

The current runner has a proven split support layout: Xvfb/xdotool/XKB/libproxychains are contained in `/work/_otclient_tibia_re_state/toolroot`, while `x11vnc` is installed only as `/usr/bin/x11vnc` (`0.9.16-10`). This explains the hardened worker's fail-closed `toolroot_unavailable` without inspecting or operating the official client/runtime surface.
