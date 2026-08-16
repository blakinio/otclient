---
task_id: OTC-20260816-track-a-runner-support-layout-inventory
status: implementing
agent: ChatGPT
session_id: chatgpt-runner-support-inventory-20260816-1650
session_role: runtime_observer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_infrastructure_inventory
phase: read-only-support-layout-observation
branch: ci/OTC-20260816-track-a-runner-support-layout-inventory
base_branch: main
base_main: 67e5dc88ff4d6c241d90a046527dac4aa9f831d8
risk: low
updated: 2026-08-16T16:50:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-runner-support-layout-inventory.md
  - docs/agents/evidence/OTC-20260816-track-a-runner-support-layout-inventory/**
  - .github/workflows/tibia-official-client-re-runner-support-layout-inventory.yml
modules_touched: []
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-toolroot-layout-fix.md
  - physical failure evidence from PR #381 run 31953635875/job 95180815033
  - PR #280 proposed dedicated-runner Dockerfile as design input only, not current deployment proof
depends_on: []
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: exact support paths exist only on the physical dedicated runner; observation is bounded to package/path metadata and does not inspect the official client or canonical runtime surface
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
runtime_owner_task: NOT_APPLICABLE_SUPPORT_FILESYSTEM_ONLY
runtime_namespace: runner-support-layout
canonical_registration: NOT_OBSERVED
canonical_lease_generation: NOT_OBSERVED
registration_lease_generation: NOT_OBSERVED
gate_a: NOT_APPLICABLE_NO_CANONICAL_RUNTIME_SURFACE_ACCESS
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
owner_funded_ai_api_authorized: false
observation_allowlist:
  - /home/runner/_work/_otclient_tibia_re_state/toolroot
  - /work/_otclient_tibia_re_state/toolroot
  - /usr/bin/Xvfb
  - /usr/bin/x11vnc
  - /usr/bin/xdotool
  - /usr/share/X11/xkb
  - /usr/lib/x86_64-linux-gnu/libproxychains.so.4
  - /lib/x86_64-linux-gnu/libproxychains.so.4
  - dpkg metadata for xvfb/x11vnc/xdotool/proxychains4
forbidden_observation:
  - official client files or processes
  - /proc process inventory
  - canonical runtime registration/lease/session directories
  - X11 display/window state
  - VNC listener or endpoint state
  - network/game/login state
  - credentials or environment secrets
  - Track B PR #284 surfaces
acceptance:
  - exactly one read-only job runs on synology-otclient-01 using [otclient, synology]
  - output reports existence/type/realpath for only allowlisted roots/components and package installation metadata
  - output classifies which support-root completeness requirement failed without executing X11 tools or inspecting client/runtime state
  - workflow is removed immediately after evidence capture before task checkpoint updates
  - sanitized findings drive a GitHub-hosted repair or an explicit external runner-image deployment blocker; no blind bootstrap retry follows directly
last_completed_step: RUNTIME #381 proved both hardened candidate support roots fail completeness on the current runner before WARP/X11/client, while static PR #280 design input installs xvfb/xdotool/proxychains4 systemwide but omits x11vnc
next_action: run one bounded support-layout inventory and persist only its sanitized path/package facts
---

# Track A dedicated-runner support layout inventory

This task observes only fixed support-tool filesystem/package metadata needed to explain `toolroot_unavailable`. It does not inspect or operate the official client, canonical registration, X11/VNC runtime, network/game state or credentials.
