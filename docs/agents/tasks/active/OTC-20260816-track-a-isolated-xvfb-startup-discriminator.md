---
task_id: OTC-20260816-track-a-isolated-xvfb-startup-discriminator
status: completed
agent: ChatGPT
session_id: chatgpt-xvfb-discriminator-20260816-1712
session_role: runtime_observer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_infrastructure_diagnostic
phase: terminal
branch: ci/OTC-20260816-track-a-isolated-xvfb-startup-discriminator
base_branch: main
base_main: 917b8ab943fd9aa1fded50c9a0b8b4e1dfeb5cbb
risk: low
updated: 2026-08-29T17:35:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-isolated-xvfb-startup-discriminator.md
  - docs/agents/evidence/OTC-20260816-track-a-isolated-xvfb-startup-discriminator/**
modules_touched: []
reuses:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md on PR #386
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-toolroot-layout-fix.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-runner-support-x11vnc-repair.md
  - upstream Xorg server source for XkbBinDirectory semantics
depends_on: []
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: exact Xvfb startup failure exists only on the physical runner; experiment was isolated to a task-owned temporary display/process and did not inspect or operate canonical/client surfaces
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
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
isolation:
  display: ':199'
  support_root: /work/_otclient_tibia_re_state/toolroot
  binary: /work/_otclient_tibia_re_state/toolroot/usr/bin/Xvfb
  binary_sha256: 2c7f5a9534410fed5092d782a69ca7ffd9fce80e98b81ffe4944d703dd11d3b1
  lifetime: job-bounded
  cleanup: completed; task-owned process exited before socket creation and one-shot workflow removed
execution:
  run: 31954834760
  job: 95183766554
  runner: synology-otclient-01
  result: FAIL_EXACT_INVOCATION
  ldd_missing_count: 0
  process_rc: 1
  socket_created: false
  exact_stderr_discriminator:
    - 'sh: 1: /usr/bin/xkbcomp: not found'
    - 'XKB: Failed to compile keymap'
    - 'Keyboard initialization failed. This could be a missing or incorrect setup of xkeyboard-config.'
    - 'Failed to activate virtual core keyboard: 2'
result:
  classification: PROVEN_XVFB_START_FAILURE_XKBCOMP_ABSOLUTE_PATH_MISSING
  missing_shared_library_hypothesis: FALSIFIED_FOR_THIS_INVOCATION
  xkb_data_path_only_fix_sufficient: false
  next_missing_dependency: /usr/bin/xkbcomp
source_correlation:
  upstream: Xorg server
  observation: XkbBaseDirectory and XkbBinDirectory are separate compile-time/runtime variables; RunXkbComp constructs helper command from XkbBinDirectory plus xkbcomp
  claim_boundary: direct runtime stderr proves this packaged Xvfb attempts /usr/bin/xkbcomp; upstream source explains why -xkbdir does not redirect that helper
workflow_status: REMOVED_AFTER_ONE_RESULT
evidence_path: docs/agents/evidence/OTC-20260816-track-a-isolated-xvfb-startup-discriminator/20260816-xvfb-startup.md
validation:
  physical_result: terminal_fail_discriminator_captured
  exact_head_governance: PENDING_AFTER_WORKFLOW_REMOVAL
  exact_head_repository_ci: PENDING_AFTER_WORKFLOW_REMOVAL
  review_threads_open: 0
  physical_e2e: NOT_APPLICABLE_WITH_REASON
  physical_e2e_reason: isolated Xvfb support-process diagnostic only; no canonical client/runtime behavior exercised
audit:
  result: PASS
  material_findings_open: 0
  notes:
    - Xvfb binary resolved inside contained support root and all dynamic libraries resolved
    - process failed before socket creation exclusively at XKB helper invocation according to captured stderr
    - one-shot workflow was removed before durable checkpoint update
    - no official-client, canonical lease/registration/session, VNC, game network/login or credentials were touched
last_completed_step: reproduced the trusted Xvfb invocation once on isolated display :199, captured exact /usr/bin/xkbcomp missing failure with ldd missing count zero, cleaned the task-owned process/display and removed the one-shot workflow
next_action: none; terminal diagnostic authority revoked after cleanup, with any future support inventory requiring a new task
---

# Isolated Xvfb startup discriminator

The trusted Xvfb invocation is now understood: the contained Xvfb binary and its shared libraries are valid, but its XKB helper lookup is compiled/configured to execute `/usr/bin/xkbcomp`, which is absent. No X11 socket or canonical client/runtime state was created.

## 2026-08-29 authority reconciliation

The diagnostic workflow had already been removed and cleanup was terminal on 2026-08-16. Its stale active metadata is now explicitly revoked (`status: completed`, `runtime_access: none`, `mutation_authorized: false`) so it cannot collide with the separately admitted V4 field6 runtime. Historical execution/evidence above is unchanged.
