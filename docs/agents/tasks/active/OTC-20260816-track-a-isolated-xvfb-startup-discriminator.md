---
task_id: OTC-20260816-track-a-isolated-xvfb-startup-discriminator
status: implementing
agent: ChatGPT
session_id: chatgpt-xvfb-discriminator-20260816-1712
session_role: runtime_observer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_infrastructure_diagnostic
phase: isolated-xvfb-startup
branch: ci/OTC-20260816-track-a-isolated-xvfb-startup-discriminator
base_branch: main
base_main: 917b8ab943fd9aa1fded50c9a0b8b4e1dfeb5cbb
risk: low
updated: 2026-08-16T17:12:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-isolated-xvfb-startup-discriminator.md
  - docs/agents/evidence/OTC-20260816-track-a-isolated-xvfb-startup-discriminator/**
  - .github/workflows/tibia-official-client-re-isolated-xvfb-startup-discriminator.yml
modules_touched: []
reuses:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md on PR #386
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-toolroot-layout-fix.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-runner-support-x11vnc-repair.md
depends_on: []
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: exact Xvfb startup failure exists only on the physical runner; the experiment is isolated to a task-owned temporary display/process and does not inspect or operate canonical/client surfaces
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: ephemeral_isolated
persistent_session_role: none
physical_e2e_required: false
runtime_owner_task: OTC-20260816-track-a-isolated-xvfb-startup-discriminator
runtime_namespace: runner-support-xvfb-diagnostic
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: true
owner_funded_ai_api_authorized: false
isolation:
  display_range: 199-220
  support_root: /work/_otclient_tibia_re_state/toolroot
  binary: /work/_otclient_tibia_re_state/toolroot/usr/bin/Xvfb
  exact_worker_environment: PATH/LD_LIBRARY_PATH/XKB_CONFIG_ROOT and -xkbdir matching trusted worker
  lifetime: job-bounded
  cleanup: task-owned process plus its own lock/socket only
forbidden_surface:
  - official client files/processes
  - canonical registration/lease/session directories
  - canonical display/VNC state
  - network/game/login state
  - credentials/environment secrets
  - Track B PR #284
acceptance:
  - exactly one Xvfb-only physical job runs on synology-otclient-01
  - a display is selected only when its lock/socket paths are absent before start
  - only the contained Xvfb binary and same worker library/XKB environment are used
  - output captures binary realpath, dynamic-library missing count, process exit/socket outcome and bounded Xvfb stderr
  - no x11vnc, xdotool action, client, WARP, canonical lease/registration or network operation occurs
  - task kills its Xvfb process and removes only its own stale lock/socket after ownership checks
  - workflow is removed immediately after the one result
last_completed_step: canonical bootstrap #386 passed support-root preflight and acquired lease generation 3 but failed closed at xvfb_socket_missing before client launch/registration
next_action: run one isolated exact-invocation Xvfb startup; persist its exit/socket/stderr discriminator and route any fix through hosted code/support repair before another canonical bootstrap
---

# Isolated Xvfb startup discriminator

This task reproduces only the Xvfb invocation used by the trusted canonical worker, on a high-number task-owned display and without any official-client/canonical runtime surface. Its purpose is to explain `xvfb_socket_missing`, then self-clean completely.
