---
task_id: OTC-20260816-track-a-xkbcomp-support-inventory
status: implementing
agent: ChatGPT
session_id: chatgpt-xkbcomp-inventory-20260816-1717
session_role: runtime_observer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_infrastructure_inventory
phase: read-only-xkbcomp-support-observation
branch: ci/OTC-20260816-track-a-xkbcomp-support-inventory
base_branch: main
base_main: 917b8ab943fd9aa1fded50c9a0b8b4e1dfeb5cbb
risk: low
updated: 2026-08-16T17:17:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-xkbcomp-support-inventory.md
  - docs/agents/evidence/OTC-20260816-track-a-xkbcomp-support-inventory/**
  - .github/workflows/tibia-official-client-re-xkbcomp-support-inventory.yml
modules_touched: []
reuses:
  - docs/agents/evidence/OTC-20260816-track-a-isolated-xvfb-startup-discriminator/20260816-xvfb-startup.md from PR #387
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-toolroot-layout-fix.md
depends_on: []
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: helper-path existence/package facts are physical runner support metadata; observation is bounded to two fixed xkbcomp paths and package database only
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
runtime_owner_task: OTC-20260816-track-a-xkbcomp-support-inventory
runtime_namespace: runner-support-xkbcomp-inventory
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
  - /work/_otclient_tibia_re_state/toolroot/usr/bin/xkbcomp
  - /usr/bin/xkbcomp
  - dpkg metadata/ownership for x11-xkb-utils and whichever package owns an observed xkbcomp path
forbidden_observation:
  - official client files/processes
  - /proc process inventory
  - canonical registration/lease/session directories
  - X11/VNC display/runtime state
  - network/game/login state
  - credentials/environment secrets
  - Track B PR #284
acceptance:
  - exactly one read-only job runs on synology-otclient-01
  - output reports only existence/type/realpath/mode/uid/SHA for the two fixed xkbcomp paths plus package ownership/version/status
  - no helper process is executed
  - no Xvfb/client/VNC/WARP/canonical lease or registration operation occurs
  - one-shot workflow is removed after result capture
  - sanitized result selects a bounded repair or explicit external runner-image blocker; canonical bootstrap is not retried directly
last_completed_step: isolated Xvfb run 31954834760/job 95183766554 proved Xvfb exits rc1 because it attempts missing absolute /usr/bin/xkbcomp, with all shared libraries resolved
next_action: run one bounded xkbcomp support inventory and persist exact contained/system path/package facts
---

# xkbcomp support inventory

This task observes only the two xkbcomp helper paths relevant to the proven Xvfb failure and their package metadata. It does not start Xvfb or inspect the canonical/client runtime.
