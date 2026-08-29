---
task_id: OTC-20260829-field6-clean-runner-host-probe
status: ready
agent: ChatGPT
session_id: chatgpt-20260829-field6-clean-runner-host-probe
session_role: runtime_observer
policy_version: 2
project_lane: otclient
lane: RUNTIME_RESEARCH
track_id: official-client-re
task_kind: runtime_infrastructure_diagnostic
phase: host_control_discovery
branch: fix/OTC-20260829-field6-clean-runner-host-probe
base_branch: main
base_main: 08c31195fd2f44224badf1b6bdff85192495898b
created: 2026-08-29T17:35:00+02:00
updated: 2026-08-29T17:35:00+02:00
risk: medium
execution_class: synology_physical_runtime
execution_mode: github_actions_read_only_host_probe
execution_reason: discover a separate host-control path for provisioning the clean one-job V4 runner without exposing credentials or starting the official client
persistent_session_role: none
physical_e2e_required: false
runtime_access: read_only
runtime_owner_task: OTC-20260829-field6-clean-runner-host-probe
runtime_namespace: field6-clean-runner-host-probe
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: false
credentials_allowed: false
login_allowed: false
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
physical_action_budget: 0
physical_action_count: 0
implementation_authorized: true
live_runtime_authorization_source: owner_prompt_current_invocation
related_pr: 800
validation_level: exact_head
owned_paths:
  - .github/scripts/test_track_a_field6_clean_runner_host_probe.py
  - .github/workflows/track-a-field6-clean-runner-host-probe.yml
  - .github/workflows/track-a-field6-clean-runner-host-probe-contract.yml
  - docs/agents/tasks/active/OTC-20260816-track-a-isolated-xvfb-startup-discriminator.md
  - docs/agents/tasks/active/OTC-20260829-field6-clean-runner-host-probe.md
  - docs/agents/reports/OTC-20260829-field6-clean-runner-host-probe.md
depends_on:
  - merged PR #795 self-hosted secret-runner boundary
  - merged PR #798 reusable self-hosted boundary audit
  - merged PR #796 V4 field6 admission
blocks:
  - OTC-20260828-current-login-field6-runtime
  - OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE
---

# Objective

Use the currently online historical Synology runner only as a no-credential, no-client, read-only capability probe to discover whether a separate host-control channel can be established for clean-runner provisioning. This task is not and cannot become the V4 credential runner.

# Admission

The workflow exists only on trusted `main` as owner-only `workflow_dispatch`, requires `github.ref == refs/heads/main`, exact `RUNNER_NAME=synology-otclient-01`, `GITHUB_RUN_ATTEMPT=1`, and a fresh trusted-main checkout. It may report only booleans/counts about Docker/socket/container context and a count of remote-control-name matches. It must not reveal container names, mounts, environment, credentials, files, packet data, process memory, or official-client state.

# Security boundary

This potentially contaminated historical runner is explicitly untrusted for credentials and cannot attest its own cleanliness. A positive Docker/control result is only discovery evidence. V4 remains forbidden until a separately authenticated host-control path directly provisions and verifies a fresh disposable one-job runner satisfying `TRACK_A_SELF_HOSTED_SECRET_RUNNER_V1.md`.

# Next action

Merge the static contract on fresh main, then dispatch this read-only workflow once. Use its sanitized result only to choose the next host-control remediation step.
