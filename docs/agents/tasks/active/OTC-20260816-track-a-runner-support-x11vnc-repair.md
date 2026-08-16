---
task_id: OTC-20260816-track-a-runner-support-x11vnc-repair
status: implementing
agent: ChatGPT
session_id: chatgpt-runner-x11vnc-repair-20260816-1657
session_role: runtime_infrastructure_maintainer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runner_infrastructure_repair
phase: bounded-support-root-repair
branch: ci/OTC-20260816-track-a-runner-support-x11vnc-repair
base_branch: main
base_main: c2e1466b4c0ac11deb96b104830f90aae9c35a97
risk: medium
updated: 2026-08-16T16:57:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-runner-support-x11vnc-repair.md
  - docs/agents/evidence/OTC-20260816-track-a-runner-support-x11vnc-repair/**
  - .github/workflows/tibia-official-client-re-runner-support-x11vnc-repair.yml
modules_touched: []
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-runner-support-layout-inventory.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-toolroot-layout-fix.md
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
depends_on: []
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: repair targets only the dedicated runner support-tool filesystem needed by the trusted canonical worker; no official-client runtime surface is observed or mutated
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
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
runner_filesystem_mutation_authorized: true
owner_funded_ai_api_authorized: false
authorization_source: owner instruction 2026-08-16 to finish the existing Track A tasks; bounded runner-support repair only, no canonical runtime/client mutation
repair_source:
  path: /usr/bin/x11vnc
  required_realpath: /usr/bin/x11vnc
  required_package: x11vnc
  required_package_version: 0.9.16-10
repair_target:
  root: /work/_otclient_tibia_re_state/toolroot
  path: /work/_otclient_tibia_re_state/toolroot/usr/bin/x11vnc
  expected_pre_state: ABSENT_FROM_RUN_31953830754
forbidden_surface:
  - official client files/processes
  - canonical registration/lease/session directories
  - /proc process inventory
  - X11 displays/windows or VNC listeners/endpoints
  - network/game/login state
  - credentials/environment secrets
  - Track B PR #284
acceptance:
  - source x11vnc is a regular executable at exact realpath /usr/bin/x11vnc, owned by root and not group/world writable
  - dpkg proves installed package x11vnc exact version 0.9.16-10 owns the source and package verification reports no mismatch
  - target root is the exact real /work/_otclient_tibia_re_state/toolroot and all previously proven components remain contained
  - an unexpected pre-existing different target fails closed rather than overwriting it
  - source is staged through a temporary file and atomically renamed inside the contained root
  - source and target SHA-256 are identical after publication
  - trusted worker contract-test `toolroot` command resolves the completed /work root without touching client/runtime state
  - any post-copy failure removes the newly created target before job exit
  - exactly one physical repair job runs; its workflow is removed after evidence capture
last_completed_step: read-only inventory #382/#383 proved the current persistent toolroot lacks only x11vnc while exact system package x11vnc 0.9.16-10 provides /usr/bin/x11vnc
next_action: run one bounded support-root repair and persist sanitized source/target hash plus trusted-worker resolver result
---

# Track A runner support x11vnc repair

This task completes the existing hardened contained toolroot instead of weakening the trusted worker. It copies only the already installed, package-verified system x11vnc executable into the one missing contained path. It does not observe or operate the official client or canonical runtime.
