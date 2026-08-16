---
task_id: OTC-20260816-track-a-mesa-glx-provider-inventory
status: ready
agent: ChatGPT
session_id: chatgpt-mesa-glx-provider-inventory-20260816
session_role: runtime_infrastructure_observer
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: runtime_infrastructure_inventory
phase: coordinator-promotion-ready
branch: diag/OTC-20260816-track-a-mesa-glx-provider-inventory
base_branch: main
base_main: d3f186414256151c9d5e03f34c5a9026b1fba500
risk: low
updated: 2026-08-16T20:48:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-mesa-glx-provider-inventory.md
  - docs/agents/evidence/OTC-20260816-track-a-mesa-glx-provider-inventory/**
modules_touched: []
reuses:
  - PR #416 contained-Xvfb capability evidence as unpromoted research input only
  - PR #417 explicit-GLX differential as unpromoted research input only
  - PR #418 modulepath rejection as unpromoted research input only
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: Xvfb contains GLX server code and contained libGL/libglx files, but default and explicit GLX launches advertise no GLX and Xvfb rejects -modulepath; this task proved the fixed contained Mesa/GLVND/DRI software-provider stack and its supported provider search-path override
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: read_only
runtime_owner_task: OTC-20260816-track-a-mesa-glx-provider-inventory
runtime_namespace: runner-support-mesa-glx-provider
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
execution:
  pr: 419
  dispatch_head: c4d4d3b06e8944863b91667491f3e2cf303d71e1
  governance_run: 31965397320
  governance_result: SUCCESS
  semantic_run: 31965397353
  semantic_job: 95209684373
  semantic_result: SUCCESS
  parser: python_stdlib_only
  xserver_started: false
  client_started: false
  canonical_state_access: NONE
result:
  classification: PROVEN_CONTAINED_MESA_GLVND_SWRAST_PROVIDER_STACK_PRESENT_DIRECT_DEPS_COMPLETE_LIBGL_DRIVERS_PATH_IS_SUPPORTED_OVERRIDE
  libGL_path: /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/libGL.so.1.7.0
  libGL_sha256: 67f471213576d225d38347a0b6d2a08a231980685301ff6461bd74d3994e5027
  libGLX_path: /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/libGLX.so.0.0.0
  libGLX_sha256: 16fc8a37eea9210dc83c57eeff5aedc10ab4c6673f2f97e8bb6ee103df657b40
  libGLX_mesa_path: /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/libGLX_mesa.so.0.0.0
  libGLX_mesa_sha256: 409f932670504cc5829c7526db466eb69a6b7f9997fd5df8afc8dfb1588278c2
  libGLdispatch_sha256: ca01a91104c8887b3d8e59499b58cbb8f604cc285666b50d9ec888eb0c915182
  xorg_libglx_path: /work/_otclient_tibia_re_state/toolroot/usr/lib/xorg/modules/extensions/libglx.so
  xorg_libglx_sha256: 373b75559ee9a17449dfb84871bb7e5e306da7bd3aecd3282c7f03831ccf961a
  dri_root: /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri
  swrast_present: true
  swrast_resolved_path: /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri/libdril_dri.so
  swrast_sha256: c28638b02783ebc96a78bb982fe59ad0d54230bc1faf53305af33edab29cd388
  load_bearing_missing_direct_dependencies: 0
  libgl_drivers_path_literal_present_in_xorg_libglx: true
  glvnd_mesa_vendor_manifest_present: true
  next_single_variable: LIBGL_DRIVERS_PATH
one_shot_workflow_removed: true
evidence:
  - docs/agents/evidence/OTC-20260816-track-a-mesa-glx-provider-inventory/20260816-contained-mesa-glx-provider.md
audit:
  result: PASS_PENDING_EXACT_FINAL_HEAD_CHECKS
  material_findings_open: 0
  notes:
    - dispatch-head governance passed both admission audits
    - no X server or client process was launched
    - one-shot workflow removed before terminal evidence/task commits
acceptance:
  - fixed provider roots inventoried: PASS
  - load-bearing GLVND/Mesa/swrast direct dependencies: PASS
  - DRI root and swrast exact path: PASS
  - provider/search-path strings: PASS
  - no X server/client/canonical state access: PASS
  - one-shot workflow removed: PASS
last_completed_step: run 31965397353/job 95209684373 proved the contained Mesa/GLVND/swrast provider stack is present with zero missing direct dependencies and that Xorg libglx supports the explicit LIBGL_DRIVERS_PATH override
next_action: coordinator-promote/archive this Draft after exact-final-head checks; separately admit one Xvfb-only experiment whose only new variable versus #417 is `LIBGL_DRIVERS_PATH=/work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri`
---

# Track A contained Mesa/GLX provider inventory — terminal candidate

The provider files are not missing. The next discriminator is whether the exact Xvfb GLX server code fails only because its software DRI provider search path is not bound to the contained DRI directory.