---
task_id: OTC-20260815-track-a-novnc-display-diagnostic
status: active
agent: ChatGPT
session_id: chatgpt-novnc-display-diagnostic-20260815-2317
session_role: researcher
session_rotation_count: 3
project_lane: otclient
lane: RUNTIME-DIAGNOSTIC
track_id: official-client-re
task_kind: discovery
phase: classify-completed-discriminator
branch: research/OTC-20260815-track-a-novnc-display-diagnostic
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-novnc-display-diagnostic
worktree_mode: isolated_branch_checkout_equivalent
risk: low
related_pr: 309
updated: 2026-08-15T23:17:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-novnc-display-diagnostic.md
  - docs/agents/evidence/OTC-20260815-track-a-novnc-display-diagnostic/**
  - .github/workflows/tibia-official-client-re-novnc-display-diagnostic.yml
depends_on:
  - PR #303 runtime state as read-only comparison input
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: stale waiting task reclaimed only to classify its already-completed read-only discriminator; no rerun or runtime mutation
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
user_communication: terminal_only
last_progress_at: 2026-08-15T23:17:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: classify-existing-run
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
stop_reason: null
completed_discriminator:
  run: 31904709435
  job: 95060619492
  state: SUCCESS
next_action: persist the exact read-only classification from run 31904709435, then release the Draft as reviewable without rerunning unchanged probes
---

# Objective

Classify the already-completed read-only noVNC/display discriminator so later canonical-runtime registration does not overclaim `:98`.

# Safety boundary

No client launch/stop/login, credentials, VNC password, process signal/attach, display cleanup, Docker control, host-namespace entry, framebuffer input, gameplay, Track B access or runtime mutation is authorized. This rotation performs no new semantic probe.

# Existing FACT

- `synology-otclient-01` is the runner.
- Persistent X11 socket census observed exactly `:98`.
- Gateway port `6082` exposes HTTP noVNC, WebSocket `/websockify`, RFB 3.8 metadata and a `1920x1080` framebuffer.
- Historical positive-control Track A used display `:98`, created a visible Tibia window and rendered probable world view.
- PR #303 task display `:115` is an isolated ephemeral runtime and is not the persistent candidate.

# Completed discriminator result

Run `31904709435`, job `95060619492` completed SUCCESS. It proved:

```text
DOCKER_GATEWAY_WEBSOCKIFY_RFB_COMPLETE=true
DOCKER_GATEWAY_RFB_PROTOCOL_VERSION=003.008
DOCKER_GATEWAY_RFB_FRAMEBUFFER=1920x1080
DIRECT_RFB_DISPLAY_88_REACHABLE=false
DIRECT_RFB_DISPLAY_98_REACHABLE=false
DIRECT_RFB_DISPLAY_115_REACHABLE=false
X11_SOCKET_DISPLAY_COUNT=1
X11_SOCKET_DISPLAYS=:98
TRACK_A_NOVNC_DIRECT_RFB_FINGERPRINT_PROBE_COMPLETE=true
```

Because all three conventional direct RFB ports refused connection, the probe could not fingerprint-match websockify `6082` to any candidate direct RFB endpoint. This is a bounded negative result, not proof that `6082` is unrelated to `:98`; websockify may target a Unix socket, internal non-published port or other host-local endpoint.

# Classification

```yaml
gateway_6082_novnc_rfb: FACT
persistent_x11_socket_98_only: FACT
historical_working_track_a_display_98: FACT
direct_rfb_5988_5998_6015: CONNECTION_REFUSED
exact_6082_backend_display: UNKNOWN
display_98_is_strongest_candidate: INFERENCE_HIGH_CONFIDENCE
display_98_is_canonical: NOT_PROVEN
```

# Next boundary

Do not rerun the same direct-port fingerprint probe. A future canonical-runtime registration may establish the relation by a different read-only discriminator, for example comparing sanitized framebuffer identity between the `6082` RFB stream and the persistent X11 display without exporting screen contents, or by authoritative host-side service configuration if that becomes available. Controller authority and runtime identity remain separate gates.
