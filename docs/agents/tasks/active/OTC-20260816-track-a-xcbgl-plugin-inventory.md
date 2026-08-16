---
task_id: OTC-20260816-track-a-xcbgl-plugin-inventory
status: implementing
agent: ChatGPT
session_id: chatgpt-xcbgl-plugin-inventory-20260816
session_role: runtime_infrastructure_researcher
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: runtime_inventory
phase: physical-readonly-plugin-inventory
branch: diag/OTC-20260816-track-a-xcbgl-plugin-inventory
base_branch: main
base_main: a3363557ad02e1421e78e02ea4b09864bd01b84d
risk: medium
updated: 2026-08-16T19:33:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-xcbgl-plugin-inventory.md
  - docs/agents/evidence/OTC-20260816-track-a-xcbgl-plugin-inventory/**
  - .github/workflows/tibia-official-client-re-xcbgl-plugin-inventory.yml
modules_touched: []
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-qsg-glx-egl-rhi-discriminator.md
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: the terminal QSG discriminator proved Vulkan/llvmpipe works while XCB GLX/EGL platform contexts remain unavailable; a read-only runner/package inventory is needed before any backend forcing or canonical retry
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: read_only
runtime_owner_task: OTC-20260816-track-a-xcbgl-plugin-inventory
runtime_namespace: track-a-xcbgl-plugin-inventory-v1
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
physical_e2e_required: false
owner_funded_ai_api_authorized: false
canonical_boundary:
  read_or_write_canonical_lease: false
  read_or_write_canonical_registration: false
  launch_client: false
  process_mutation: false
  credentials_allowed: false
  login_allowed: false
  track_b_access: false
exact_client_fence:
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
acceptance:
  - locate and exact-fence the installed source package without launching it
  - inventory xcbglintegrations/xcb_glx/xcb_egl and platform plugin files in package/toolroot
  - report Qt plugin directory candidates and relevant environment-independent paths
  - run ldd/readelf only on located Qt plugin shared objects and classify missing dependencies
  - do not inspect canonical runtime process/session state
  - do not launch the client or mutate runner files
last_completed_step: QSG discriminator #406/#407 proved QRhi Vulkan on llvmpipe while XCB GLX/EGL contexts remained unavailable
next_action: execute one read-only filesystem/plugin/dependency inventory and persist sanitized evidence
---

# Track A XCB GL integration plugin inventory

Read-only physical inventory only. No client launch and no canonical runtime mutation.