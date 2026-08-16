---
task_id: OTC-20260816-track-a-xkbcomp-support-inventory
status: ready
agent: ChatGPT
session_id: chatgpt-xkbcomp-inventory-20260816-1717
session_role: runtime_observer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_infrastructure_inventory
phase: coordinator-promotion-ready
branch: ci/OTC-20260816-track-a-xkbcomp-support-inventory
base_branch: main
base_main: 917b8ab943fd9aa1fded50c9a0b8b4e1dfeb5cbb
risk: low
updated: 2026-08-16T17:20:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-xkbcomp-support-inventory.md
  - docs/agents/evidence/OTC-20260816-track-a-xkbcomp-support-inventory/**
modules_touched: []
reuses:
  - docs/agents/evidence/OTC-20260816-track-a-isolated-xvfb-startup-discriminator/20260816-xvfb-startup.md from merged PR #387
  - upstream Xorg XkbBinDirectory source correlation
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-toolroot-layout-fix.md
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
execution:
  run: 31955054478
  job: 95184310959
  runner: synology-otclient-01
  result: SUCCESS
  workflow_removed_after_capture: true
result:
  classification: PROVEN_CONTAINED_XKBCOMP_SYSTEM_ABSOLUTE_PATH_MISSING
  contained_path: /work/_otclient_tibia_re_state/toolroot/usr/bin/xkbcomp
  contained_realpath: /work/_otclient_tibia_re_state/toolroot/usr/bin/xkbcomp
  contained_mode: 755
  contained_uid: 0
  contained_executable: true
  contained_sha256: 0967e7e7b03b077327cea74567726b265bd304b4fdf59f87bf7fdfe1074e7591
  contained_current_container_dpkg_owner: UNOWNED
  system_path: /usr/bin/xkbcomp
  system_state: ABSENT
  system_package_x11_xkb_utils: NOT_INSTALLED
  system_package_xkbcomp: NOT_INSTALLED
root_cause:
  isolated_xvfb_failure: packaged Xvfb invokes compile-time absolute /usr/bin/xkbcomp while the exact helper already exists only inside the persistent trusted support root
  xkbdir_argument_limitation: upstream Xorg source shows -xkbdir changes XkbBaseDirectory, not XkbBinDirectory
  safe_immediate_repair: bounded runner-support operation may materialize a bit-identical /usr/bin/xkbcomp from the proven contained source only if job identity/path preflight permits it; otherwise require runner image provisioning
  durability_note: /usr/bin is container-local and a successful immediate repair does not replace declarative runner-image provisioning
evidence_path: docs/agents/evidence/OTC-20260816-track-a-xkbcomp-support-inventory/20260816-xkbcomp-layout.md
validation:
  physical_inventory_result: SUCCESS
  exact_head_governance: PENDING_AFTER_WORKFLOW_REMOVAL
  exact_head_repository_ci: PENDING_AFTER_WORKFLOW_REMOVAL
  review_threads_open: 0
  physical_e2e: NOT_APPLICABLE_WITH_REASON
  physical_e2e_reason: support-filesystem metadata only; xkbcomp/Xvfb/client/runtime were not executed in this inventory
audit:
  result: PASS
  material_findings_open: 0
  notes:
    - contained helper is directly proven regular/root-owned/executable with exact SHA
    - system absolute helper path is directly proven absent
    - no package/network operation is needed to test an immediate bounded repair
    - no official-client/canonical process/registration/display/VNC/network/login/credential state was observed
last_completed_step: captured one read-only xkbcomp support inventory, removed the one-shot workflow and persisted the exact contained-vs-system helper layout
next_action: obtain exact-head governance/CI and promote sanitized evidence; then execute one separately reviewed bounded system-helper repair that either atomically materializes exact /usr/bin/xkbcomp and validates isolated Xvfb, or fails closed as an explicit runner-image deployment blocker
---

# xkbcomp support inventory

The helper already exists inside the persistent trusted support root with SHA `0967e7e7...`, while this Xvfb build invokes absent absolute `/usr/bin/xkbcomp`. This is now a runner-support path problem, not a missing Xvfb binary/library problem and not a reason to retry the canonical client.
