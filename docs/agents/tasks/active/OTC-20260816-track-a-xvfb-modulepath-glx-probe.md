---
task_id: OTC-20260816-track-a-xvfb-modulepath-glx-probe
status: ready
agent: ChatGPT
session_id: chatgpt-xvfb-modulepath-glx-20260816
session_role: runtime_infrastructure_researcher
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: runtime_discriminator
phase: coordinator-promotion-ready
branch: diag/OTC-20260816-track-a-xvfb-modulepath-glx-probe
base_branch: main
base_main: d3f186414256151c9d5e03f34c5a9026b1fba500
risk: medium
updated: 2026-08-16T20:43:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-xvfb-modulepath-glx-probe.md
  - docs/agents/evidence/OTC-20260816-track-a-xvfb-modulepath-glx-probe/**
modules_touched: []
reuses:
  - PR #416 contained-Xvfb capability evidence as unpromoted research input only
  - PR #417 explicit-GLX differential as unpromoted research input only
  - exact contained Xvfb/libglx/module-root fences from those tasks
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: the exact contained Xvfb has GLX code and a contained libglx.so module, but default and explicit +extension GLX launches both advertise GLX absent; one isolated modulepath discriminator tested whether an Xorg-style explicit module path is a valid server mechanism
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260816-track-a-xvfb-modulepath-glx-probe
runtime_namespace: track-a-xvfb-modulepath-glx-probe-v1
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
  official_client_allowed: false
  vnc_allowed: false
  warp_allowed: false
  credentials_allowed: false
  login_allowed: false
  gameplay_allowed: false
  track_b_access: false
exact_support_fence:
  toolroot: /work/_otclient_tibia_re_state/toolroot
  xvfb: /work/_otclient_tibia_re_state/toolroot/usr/bin/Xvfb
  xvfb_sha256: 2c7f5a9534410fed5092d782a69ca7ffd9fce80e98b81ffe4944d703dd11d3b1
  attempted_modulepath: /work/_otclient_tibia_re_state/toolroot/usr/lib/xorg/modules
  libglx: /work/_otclient_tibia_re_state/toolroot/usr/lib/xorg/modules/extensions/libglx.so
  libglx_sha256: 373b75559ee9a17449dfb84871bb7e5e306da7bd3aecd3282c7f03831ccf961a
  xkb_root: /work/_otclient_tibia_re_state/toolroot/usr/share/X11/xkb
  xkbcomp: /usr/bin/xkbcomp
  xkbcomp_sha256: 0967e7e7b03b077327cea74567726b265bd304b4fdf59f87bf7fdfe1074e7591
execution:
  pr: 418
  dispatch_head: 201a2764ecc87faa53c2878402b69ac4cfe679c5
  governance_run: 31965191001
  governance_result: SUCCESS
  semantic_run: 31965191048
  semantic_job: 95209182706
  semantic_result: SUCCESS_DISCRIMINATOR
  server_started: false
  canonical_state_access: NONE
  client_started: false
  vnc_started: false
  warp_started: false
  cleanup: COMPLETE
result:
  classification: PROVEN_CONTAINED_XVFB_REJECTS_MODULEPATH_OPTION_GLX_MODULEPATH_CLI_HYPOTHESIS_DISPROVEN
  support_fence_passed: true
  failure_stage: ARGUMENT_PARSE_BEFORE_X11_SOCKET
  error: 'Unrecognized option: -modulepath'
  modulepath_cli_supported: false
  glx_runtime_toggle_listed_by_help: true
  iglx_option_listed_by_help: true
  libglx_loadability_via_modulepath_tested: false
  canonical_bootstrap_retry_authorized: false
one_shot_workflow_removed: true
evidence:
  - docs/agents/evidence/OTC-20260816-track-a-xvfb-modulepath-glx-probe/20260816-modulepath-option-rejected.md
audit:
  result: PASS_PENDING_EXACT_FINAL_HEAD_CHECKS
  material_findings_open: 0
  notes:
    - dispatch-head governance passed both admission audits
    - the isolated Xvfb exited during argument parsing before creating a display
    - no official client/VNC/WARP/canonical state was touched
    - one-shot workflow removed before terminal evidence/task commits
acceptance:
  - exact support fences: PASS
  - argument-path discriminator captured: PASS
  - no unintended client/canonical mutation: PASS
  - cleanup: PASS
  - exactly one semantic physical workflow run: PASS
last_completed_step: run 31965191048/job 95209182706 proved this Xvfb rejects `-modulepath` before server startup; the modulepath CLI hypothesis is eliminated without touching the official client or canonical runtime
next_action: coordinator-promote/archive this Draft after exact-final-head checks; separately perform read-only contained Mesa/GLVND/DRI provider inventory to identify exact software-GLX provider/search paths before any further Xvfb-only environment experiment
---

# Track A Xvfb modulepath GLX probe — terminal candidate

`-modulepath` is not a valid mechanism for this Xvfb. The remaining frontier is GLX provider/software-renderer discovery under the server's actual fixed loader environment.