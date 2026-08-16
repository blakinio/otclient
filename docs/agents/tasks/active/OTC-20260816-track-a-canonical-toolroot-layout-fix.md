---
task_id: OTC-20260816-track-a-canonical-toolroot-layout-fix
status: ready
agent: ChatGPT
session_id: chatgpt-toolroot-fix-20260816-1628
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_infrastructure_fix
phase: coordinator-promotion-ready
branch: fix/OTC-20260816-track-a-canonical-toolroot-layout
base_branch: main
base_main: c66e8b563f748e0595e3b7144c3fac3dc744c60c
current_main: c66e8b563f748e0595e3b7144c3fac3dc744c60c
risk: medium
updated: 2026-08-16T16:34:00+02:00
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/test_tibia_official_client_re_canonical_live_session.py
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-toolroot-layout-fix.md
modules_touched: []
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-bootstrap-implementation.md
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md on PR #376
  - historical PR #303 runtime evidence for the physical runner toolroot layout
  - .github/scripts/test_tibia_official_client_re_canonical_live_transition.py
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
depends_on: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: deterministic support-layout resolver and contract tests require no physical runtime
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: component
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
trigger_evidence:
  runtime_pr: 376
  run: 31952484701
  job: 95177998199
  runner: synology-otclient-01
  selector: [otclient, synology]
  pre_admission_lease_status: absent
  acquired_lease_generation: 1
  failure: TRACK_A_CANONICAL_SESSION_ERROR=xvfb_unavailable
  registration_published: false
layout_evidence:
  previous_worker_assumption: /home/runner/_work/_otclient_tibia_re_state/toolroot
  proven_physical_runner_layout: /work/_otclient_tibia_re_state/toolroot
  historical_source: PR #303 runtime workflow/effective helper
implementation:
  production_allowlist:
    - /home/runner/_work/_otclient_tibia_re_state/toolroot
    - /work/_otclient_tibia_re_state/toolroot
  complete_root_requires: [Xvfb, x11vnc, xdotool, XKB_DATA, libproxychains.so.4]
  rejects_symlink_root: true
  rejects_partial_root: true
  production_environment_override: false
  contract_test_override_only: true
  bootstrap_persists_selected_root: true
  probe_reuses_persisted_root: true
  missing_pid_read_is_quiet: true
validation:
  focused_head: bb868d5835bf65d5836bd529dbbe1f0719fca4c8
  focused_run: 31952903530
  focused_job: 95179036978
  focused_result: SUCCESS
  focused_scope:
    - bash syntax for canonical session worker
    - new toolroot resolver behavioral tests
    - existing canonical transition/bootstrap/rebind/Gate-B tests
    - static no-login assertion
  focused_governance_run: 31952903485
  focused_governance_result: SUCCESS
  temporary_validator_workflow: REMOVED
  final_checkpoint_head: PENDING_AFTER_THIS_UPDATE
  final_track_a_governance: PENDING
  final_repository_ci: PENDING
  physical_e2e: NOT_APPLICABLE_WITH_REASON
  physical_e2e_reason: this task is hosted-only infrastructure code; physical bootstrap validation belongs to fresh RUNTIME after trusted-main promotion
audit:
  result: PASS
  material_findings_open: 0
  notes:
    - resolver is a fixed allowlist rather than a caller-controlled production path
    - a root is accepted only if all support binaries/data/preload required by the worker are co-located and complete
    - probe is bound to the same root selected at bootstrap rather than silently switching layout
    - worker still contains no login_e2e surface and no credential-bearing persistent environment
acceptance:
  - production resolver considers only the two fixed canonical layouts and chooses the first complete root
  - completeness requires Xvfb, x11vnc, xdotool, XKB data and libproxychains.so.4 under the same real root
  - arbitrary environment cannot redirect the production resolver
  - test-only candidate injection is available only when TRACK_A_CANONICAL_WORKER_CONTRACT_TEST=1
  - bootstrap persists the selected support root and probe requires that same complete root to remain complete
  - missing PID files during rollback do not emit shell redirection noise
  - existing bootstrap/probe/rollback contract shape and credential stripping remain unchanged
  - hosted focused tests plus existing transition tests pass before promotion
  - no Synology/client/X11/VNC/login/runtime mutation occurs in this task
last_completed_step: implemented fixed-allowlist support-toolroot resolution, passed hosted behavioral/transition validation, removed the temporary validator and completed an independent exact-diff audit with zero material findings
next_action: obtain final exact-head governance/repository CI, coordinator review, mark ready and merge; archive task, then refresh RUNTIME #376 from the new trusted main and retry bootstrap once
---

# Canonical support-toolroot layout fix

The physical failure was not a missing runner: it was a support-layout mismatch. This hosted-only repair resolves one complete root from the two repository-known canonical layouts, persists the selected root for probe consistency and fails closed for partial/ambiguous support trees. No physical runtime authority is exercised by this task.
