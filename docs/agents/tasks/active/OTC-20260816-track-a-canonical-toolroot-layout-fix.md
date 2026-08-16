---
task_id: OTC-20260816-track-a-canonical-toolroot-layout-fix
status: implementing
agent: ChatGPT
session_id: chatgpt-toolroot-fix-20260816-1628
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_infrastructure_fix
phase: implement
branch: fix/OTC-20260816-track-a-canonical-toolroot-layout
base_branch: main
base_main: c66e8b563f748e0595e3b7144c3fac3dc744c60c
risk: medium
updated: 2026-08-16T16:28:00+02:00
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/test_tibia_official_client_re_canonical_live_session.py
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-toolroot-layout-fix.md
  - .github/workflows/tibia-official-client-re-canonical-toolroot-layout-fix.yml
modules_touched: []
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-bootstrap-implementation.md
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md on PR #376
  - historical PR #303 runtime evidence for the physical runner toolroot layout
  - .github/scripts/test_tibia_official_client_re-canonical-live-transition.py
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
  current_worker_assumption: /home/runner/_work/_otclient_tibia_re_state/toolroot
  proven_physical_runner_layout: /work/_otclient_tibia_re_state/toolroot
  historical_source: PR #303 runtime workflow/effective helper
objective: resolve one complete support-toolroot from a fixed allowlist of canonical runner layouts, reject partial/symlink roots, persist the selected root for later probes, and keep production paths non-overridable by environment
acceptance:
  - production resolver considers only the two fixed canonical layouts and chooses the first complete root
  - completeness requires Xvfb, x11vnc, xdotool, XKB data and libproxychains.so.4 under the same real root
  - arbitrary environment cannot redirect the production resolver
  - test-only candidate injection is available only when TRACK_A_CANONICAL_WORKER_CONTRACT_TEST=1
  - bootstrap persists the selected support root and probe requires that same root to remain complete
  - missing PID files during rollback do not emit shell redirection noise
  - existing bootstrap/probe/rollback contract shape and credential stripping remain unchanged
  - hosted focused tests plus existing transition tests pass before promotion
  - no Synology/client/X11/VNC/login/runtime mutation occurs in this task
last_completed_step: physical RUNTIME #376 proved the canonical runner is reachable but the trusted worker cannot find Xvfb through its hard-coded support-toolroot layout
next_action: implement fixed-allowlist support-toolroot resolution and contract tests on GitHub-hosted, remove temporary validator workflow after proof, then coordinator review/promote to trusted main
---

# Canonical support-toolroot layout fix

This is a no-runtime repair for the physical bootstrap defect discovered by RUNTIME #376. It does not grant or perform physical mutation. A later fresh RUNTIME dispatch will consume the promoted fix under normal admission gates.
