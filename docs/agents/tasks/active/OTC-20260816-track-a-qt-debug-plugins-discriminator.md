---
task_id: OTC-20260816-track-a-qt-debug-plugins-discriminator
status: ready
agent: ChatGPT
session_id: chatgpt-qt-debug-plugins-20260816
session_role: runtime_researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_discriminator
phase: coordinator-promotion-ready
branch: diag/OTC-20260816-track-a-qt-debug-plugins
base_branch: main
base_main: a1bab5e7197aba484ac72a4dbcb2d8fddeaeacc2
risk: high
updated: 2026-08-16T19:48:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-qt-debug-plugins-discriminator.md
  - docs/agents/evidence/OTC-20260816-track-a-qt-debug-plugins-discriminator/**
modules_touched: []
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-qsg-glx-egl-rhi-discriminator.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-xcbgl-plugin-inventory.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: one governance-compliant ephemeral-isolated QT_DEBUG_PLUGINS run proved the bundled Qt platform plugin path and libqxcb metadata are discovered while the exact client remains alive with no visible windows; xcbglintegrations-specific loader lines remain unknown because the 426-line sanitized log was connector-truncated, so further mutation is disabled and a narrower filtered discriminator is selected
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: heavy
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260816-track-a-qt-debug-plugins-discriminator
runtime_namespace: track-a-qt-debug-plugins-discriminator-v1
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: false
persistent_session_role: none
physical_e2e_required: true
owner_funded_ai_api_authorized: false
canonical_boundary:
  read_or_write_canonical_lease: false
  read_or_write_canonical_registration: false
  publish_registration: false
  canonical_namespace_access: false
  credentials_allowed: false
  login_allowed: false
  gameplay_allowed: false
  track_b_access: false
exact_client_fence:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
semantic_run:
  run: 31962559445
  job: 95202662909
  governance_run: 31962559402
  governance_result: SUCCESS
  result: SUCCESS
  source_blob: 1616edcc982be50ef2c95b8077160ec8fe9291fe
  patch_count: 3
  canonical_state_access: NONE
  display: ':231'
  vnc_port: 6200
  client_pid: 25426
  client_pgid: 25426
  client_alive_t05: true
  client_alive_t15: true
  client_alive_t35: true
  visible_windows_t05: 0
  visible_windows_t15: 0
  visible_windows_t35: 0
  cleanup: COMPLETE
result:
  classification: PROVEN_BUNDLED_QXCB_PLATFORM_PLUGIN_DISCOVERED_METADATA_VALID_XCBGLINTEGRATION_DISCOVERY_LOAD_INIT_UNKNOWN
  bundled_platform_plugin_dir_scanned: true
  bundled_libqxcb_metadata_found: true
  bundled_libqxcb_key_xcb_found: true
  general_bundled_plugin_loader_operational: true
  xcbglintegration_specific_discovery: UNKNOWN_CONNECTOR_LOG_TRUNCATION
  xcbglintegration_specific_load: UNKNOWN
  xcbglintegration_specific_initialization: UNKNOWN
  visible_window: NONE_THROUGH_35S
one_shot_workflow_removed: true
evidence:
  - docs/agents/evidence/OTC-20260816-track-a-qt-debug-plugins-discriminator/20260816-qt-plugin-discovery.md
audit:
  result: PASS
  material_findings_open: 0
acceptance:
  - immutable source blob and exact patch sites fenced: PASS
  - task-owned isolated startup and exact client fence: PASS
  - QT_DEBUG_PLUGINS enabled without forcing backend: PASS
  - bundled platform plugin discovery and libqxcb metadata captured: PASS
  - cleanup complete and canonical state untouched: PASS
  - xcbglintegrations-specific load/init remains explicitly UNKNOWN rather than inferred
last_completed_step: run 31962559445/job 95202662909 proved bundled platforms/libqxcb discovery and metadata validity while the exact client stayed alive and windowless through 35 seconds; one-shot workflow removed
next_action: coordinator-promote/archive this discriminator; then run one separately admitted narrow filtered ephemeral-isolated discriminator emitting only xcbglintegrations/libqxcb-glx/libqxcb-egl/load-error/QXcbIntegration/GLX/EGL lines, without backend forcing or canonical bootstrap
---

# Track A Qt plugin discovery discriminator — terminal candidate

The general bundled Qt plugin loader and xcb platform plugin discovery are proven. The remaining load-bearing gap is the exact xcbglintegrations discovery/load/initialization sequence.