---
task_id: OTC-20260816-track-a-xvfb-glx-capability
status: implementing
agent: ChatGPT
session_id: chatgpt-xvfb-glx-capability-20260816
session_role: runtime_infrastructure_observer
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: runtime_infrastructure_inventory
phase: contained-xvfb-glx-capability-readonly
branch: diag/OTC-20260816-track-a-xvfb-glx-capability
base_branch: main
base_main: d3f186414256151c9d5e03f34c5a9026b1fba500
risk: low
updated: 2026-08-16T20:29:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-xvfb-glx-capability.md
  - docs/agents/evidence/OTC-20260816-track-a-xvfb-glx-capability/**
  - .github/workflows/tibia-official-client-re-xvfb-glx-capability.yml
modules_touched: []
reuses:
  - PR #415 terminal XCB GL runtime-trace evidence as unpromoted research input only
  - docs/agents/tasks/archive/OTC-20260816-track-a-runner-support-layout-inventory.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: the isolated runtime discriminator directly observed GLX absent on the task-owned Xvfb display while Qt successfully loaded the xcb_glx integration plugin; this task inspects only the fixed contained Xvfb support filesystem/binary surface to determine whether GLX support is present before any separate Xvfb-only execution
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: read_only
runtime_owner_task: OTC-20260816-track-a-xvfb-glx-capability
runtime_namespace: runner-support-xvfb-glx-capability
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
observation_allowlist:
  - /work/_otclient_tibia_re_state/toolroot/usr/bin/Xvfb
  - /work/_otclient_tibia_re_state/toolroot/usr/lib/xorg/modules/**
  - /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/** only as ldd-resolved dependencies of Xvfb or fixed GLX module candidates
  - ELF metadata, SHA-256, file metadata, bounded printable-string matches for GLX symbols/names
forbidden_observation:
  - official client package/files/processes
  - /proc process inventory
  - canonical runtime registration/lease/session directories
  - any X11 display/window/VNC state
  - network/game/login state
  - credentials or environment secrets
  - Track B and historical PR #303 runtime surfaces
acceptance:
  - exact fixed support root and Xvfb path validated as real non-symlink contained objects
  - Xvfb SHA-256 and ELF dependency surface recorded
  - fixed xorg module tree inventoried only for GLX/glamor-related files
  - any libglx module SHA/dependency metadata recorded
  - bounded Xvfb printable-string search classifies whether GLX names/symbols are compiled/referenced
  - no X server or official client is started
  - no canonical state access
  - one-shot workflow removed after capture
last_completed_step: PR #415 run 31964397523/job 95207211173 directly observed GLX absent from a task-owned contained-Xvfb display while Qt loaded libqxcb-glx-integration.so
next_action: perform exactly one read-only fixed-path contained-Xvfb GLX capability inventory; use its result to decide whether a separately admitted Xvfb-only +extension GLX execution is justified
---

# Track A contained Xvfb GLX capability inventory

Read-only support-filesystem evidence only. This task must not start Xvfb or the official client and must not inspect canonical runtime state.
