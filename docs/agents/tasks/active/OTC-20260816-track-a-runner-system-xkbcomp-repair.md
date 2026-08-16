---
task_id: OTC-20260816-track-a-runner-system-xkbcomp-repair
status: implementing
agent: ChatGPT
session_id: chatgpt-system-xkbcomp-repair-20260816-1722
session_role: runtime_infrastructure_maintainer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runner_infrastructure_repair
phase: bounded-system-helper-repair
branch: ci/OTC-20260816-track-a-runner-system-xkbcomp-repair
base_branch: main
base_main: 22089c5ca65228379c409dd33561a096eea00b16
risk: medium
updated: 2026-08-16T17:22:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-runner-system-xkbcomp-repair.md
  - docs/agents/evidence/OTC-20260816-track-a-runner-system-xkbcomp-repair/**
  - .github/workflows/tibia-official-client-re-runner-system-xkbcomp-repair.yml
modules_touched: []
reuses:
  - docs/agents/evidence/OTC-20260816-track-a-isolated-xvfb-startup-discriminator/20260816-xvfb-startup.md
  - xkbcomp support inventory run 31955054478/job 95184310959 from PR #388
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
depends_on: []
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: repair targets only the dedicated runner container support filesystem required by the packaged Xvfb absolute helper path; no official-client or canonical runtime surface is accessed
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
authorization_source: owner instruction 2026-08-16 to finish existing Track A tasks; bounded dedicated-runner support repair only, no client/canonical runtime mutation
repair_source:
  path: /work/_otclient_tibia_re_state/toolroot/usr/bin/xkbcomp
  required_realpath: /work/_otclient_tibia_re_state/toolroot/usr/bin/xkbcomp
  required_uid: 0
  required_mode: 755
  required_sha256: 0967e7e7b03b077327cea74567726b265bd304b4fdf59f87bf7fdfe1074e7591
  required_ldd_missing_count: 0
repair_target:
  path: /usr/bin/xkbcomp
  expected_pre_state: ABSENT_FROM_RUN_31955054478
  publication: atomic only if job uid is 0 and /usr/bin is writable
post_repair_validation:
  process: contained Xvfb only
  display_range: 199-220
  environment: exact trusted worker Xvfb PATH/LD_LIBRARY_PATH/XKB_CONFIG_ROOT/-xkbdir
  success: X11 socket created
  failure_cleanup: remove only newly created /usr/bin/xkbcomp plus task-owned Xvfb lock/socket/process
forbidden_surface:
  - official client files/processes
  - canonical registration/lease/session directories
  - canonical X11/VNC display state
  - WARP/game network/login state
  - credentials/environment secrets
  - Track B PR #284
acceptance:
  - source exact path/realpath/uid/mode/SHA are re-proven and ldd under contained libs has zero missing dependencies
  - job uid must be 0 and /usr/bin must be writable; otherwise fail closed with explicit RUNNER_IMAGE_DEPLOYMENT_REQUIRED and no mutation
  - target must be absent or already regular root-owned non-group/world-writable and bit-identical; any other pre-state fails closed
  - absent target is staged through same-directory temp file then atomically renamed
  - source/target SHA equality is proven after publication
  - one isolated Xvfb exact-invocation test creates a socket; no client/VNC/WARP/canonical state is touched
  - any post-publication failure removes the newly created target before exit
  - one-shot workflow is removed immediately after terminal result
  - successful system helper publication is classified as immediate container repair, not durable declarative runner-image provisioning
last_completed_step: read-only xkbcomp inventory proved the contained root already has root-owned executable xkbcomp SHA 0967e7e7..., while /usr/bin/xkbcomp and system xkbcomp packages are absent; Xvfb requires the absolute system path
next_action: run one bounded repair+isolated-Xvfb validation; if UID/path authority fails, persist external runner-image deployment blocker instead of retrying canonical bootstrap
---

# Dedicated runner system xkbcomp repair

This task satisfies the exact absolute helper path required by the current Xvfb build using only the already-proven contained helper. It is fail-closed on job privilege, target pre-state and isolated Xvfb validation, and never launches the official client.
