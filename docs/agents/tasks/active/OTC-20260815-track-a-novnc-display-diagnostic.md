---
task_id: OTC-20260815-track-a-novnc-display-diagnostic
status: blocked
agent: ChatGPT
session_id: chatgpt-novnc-display-diagnostic-20260815-2135
session_role: researcher
session_rotation_count: 1
project_lane: otclient
lane: RUNTIME-DIAGNOSTIC
track_id: official-client-re
task_kind: discovery
phase: investigate
branch: research/OTC-20260815-track-a-novnc-display-diagnostic
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-novnc-display-diagnostic
worktree_mode: isolated_branch_checkout_equivalent
risk: low
related_pr: 309
updated: 2026-08-15T21:40:00+02:00
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
execution_reason: a materially new read-only Docker-default-gateway access path was tested on the dedicated Synology runner without taking ownership of PR #303 runtime
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
user_communication: terminal_only
context_pressure: low
context_growth: stable
context_score: 4
estimate_confidence: high
decomposition_decision: single
invocation_started_at: 2026-08-15T21:35:00+02:00
last_progress_at: 2026-08-15T21:40:00+02:00
ci_checks_for_current_head: 1
ci_check_generation: docker-gateway-diagnostic
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
stop_reason: host_listener_mapping_unavailable_from_runner_namespace
next_action: from the Synology host or another authorized host/LAN tool, inspect read-only the listener/process/config owning TCP 6082 and record its websockify/RFB target display or VNC port without restarting, signalling, authenticating to, or reconfiguring any VNC/X11/runtime process
---

# Objective

Determine whether the owner's `synology:6082` noVNC endpoint can be mapped to a concrete X11 display, and recover enough read-only server characteristics to compare it with Track A PR #303's isolated `:115` runtime.

# Authority and safety boundary

This is a read-only discovery task. The diagnostic did not launch or stop the Tibia client, use credentials, signal/attach to processes, restart or reconfigure X/VNC, control Docker, enter the host namespace, perform gameplay actions, read another task's environment, or touch Track B.

PR #303 owns its runtime workflow, display `:115`, process lifecycle and task state. This task did not mutate those paths or processes.

# Acceptance inventory

- [x] Verify diagnostic jobs run on `synology-otclient-01`.
- [x] Establish that hostname `synology` is not resolvable from the runner container namespace.
- [x] Inventory persistent X11 Unix sockets: exactly `:98` was present in both probes.
- [x] Derive the runner container default IPv4 gateway without printing the private gateway address.
- [x] Prove TCP `6082` is reachable through that gateway.
- [x] Prove gateway `6082` serves HTTP noVNC and accepts `/websockify` WebSocket upgrade.
- [x] Complete a sanitized unauthenticated RFB metadata handshake without using a VNC password.
- [x] Record framebuffer dimensions and whether RFB metadata directly exposes an X display hint.
- [x] Reclassify `6082 -> :98`: still `UNKNOWN`; direct numeric binding was not exposed by RFB metadata.
- [x] Compare against PR #303: historical positive control remains `:98`; fresh isolated failing reacquisition remains `:115`.
- [x] Preserve one concrete next action while mapping remains UNKNOWN.

# Validation

## First runner probe

```text
head=fe57c76db37056f3df0e66b5c6bcb71f96565d3b
run=31903692616
job=95058202023
runner=synology-otclient-01
job_result=SUCCESS
```

Material result: hostname `synology` was not resolvable and the runner exposed exactly one X11 socket, `:98`.

Evidence:

`docs/agents/evidence/OTC-20260815-track-a-novnc-display-diagnostic/20260815-runner-probe.md`

## Docker-gateway probe

```text
head=dff39e99d4669229a66826e5f51805a95be10185
run=31904447945
job=95059984786
runner=synology-otclient-01
job_result=SUCCESS
```

Material markers:

```text
DOCKER_DEFAULT_GATEWAY_FOUND=true
DOCKER_GATEWAY_TCP_6082_REACHABLE=true
DOCKER_GATEWAY_NOVNC_HTTP_RESPONSE=true
DOCKER_GATEWAY_NOVNC_HTTP_STATUS=200
DOCKER_GATEWAY_WEBSOCKIFY_UPGRADE_STATUS=101
DOCKER_GATEWAY_WEBSOCKIFY_REACHABLE=true
DOCKER_GATEWAY_RFB_PROTOCOL_VERSION=003.008
DOCKER_GATEWAY_RFB_SECURITY_NONE_AVAILABLE=true
DOCKER_GATEWAY_RFB_SECURITY_VNC_AUTH_AVAILABLE=false
DOCKER_GATEWAY_RFB_AUTH_REQUIRED=false
DOCKER_GATEWAY_RFB_SECURITY_RESULT=0
DOCKER_GATEWAY_RFB_FRAMEBUFFER_WIDTH=1920
DOCKER_GATEWAY_RFB_FRAMEBUFFER_HEIGHT=1080
DOCKER_GATEWAY_RFB_DISPLAY_HINT=unknown
DOCKER_GATEWAY_RFB_DESKTOP_NAME_HAS_X11_TOKEN=false
DOCKER_GATEWAY_WEBSOCKIFY_RFB_PROBE_COMPLETE=true
X11_SOCKET_DISPLAY_COUNT=1
X11_SOCKET_DISPLAYS=:98
X11_DISPLAY_98_QUERY=unavailable
```

Evidence:

`docs/agents/evidence/OTC-20260815-track-a-novnc-display-diagnostic/20260815-docker-gateway-probe.md`

# Comparison boundary

## FACT

Historical positive-control run `31730884814`, attempt 14, job `94785048338` used `TRACK_DISPLAY=:98` for the same exact fenced official Linux client and successfully created the visible `Tibia` window, submitted login and rendered a probable world view while remaining SOCKS-confined.

PR #303 run `31903196011` used task-owned `DISPLAY=:115` and failed before login with `client_gen_1_window_missing`; its sanitized display-wide census recorded `visible_window_count=0`.

The Docker-gateway probe directly reached port `6082`, received HTTP `200`, WebSocket `101`, RFB `003.008`, no-auth success, and a `1920x1080` framebuffer. At the same time the runner namespace exposed only X11 socket `:98`.

## INFERENCE — high confidence

The Docker-default-gateway `:6082` endpoint is the same host-side noVNC service the owner reaches as `synology:6082`: it is the runner's host-facing default gateway on the same port and presents the expected noVNC/websockify/RFB stack while preserving `Host: synology:6082` in the protocol probe.

`:98` is the strongest candidate for the served GUI because it is the historical working Track A display, the only persistent X11 socket visible to the runner, and its known-good profile is `1920x1080`, matching the RFB framebuffer dimensions.

## UNKNOWN

`6082 -> :98` is not directly proven. The RFB desktop name has no X11 token or numeric display hint, and `xdpyinfo :98` is unavailable from the runner job. A VNC/websockify process in another namespace could theoretically expose the same framebuffer shape.

The owner's earlier `:88` observation remains unverified in current canonical evidence.

# Blocker

The remaining discriminator is host-side listener/process/config metadata for TCP `6082`. The runner can now reach the service over the Docker gateway but cannot inspect the host process/configuration that determines its RFB target. Repeating network handshakes cannot prove the target display number because the server does not expose it in RFB metadata.

# Checkpoint

```yaml
status: blocked
proven:
  - main remained 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45 at continuation start.
  - gateway diagnostic run 31904447945 job 95059984786 succeeded on exact tested head dff39e99d4669229a66826e5f51805a95be10185.
  - runner default gateway exposes the noVNC/websockify/RFB service on TCP 6082.
  - endpoint RFB framebuffer is 1920x1080 and permits the bounded no-auth metadata handshake.
  - exactly one X11 Unix socket was visible at the same probe time: :98.
  - historical positive-control Track A runtime used :98 and created the visible official-client window.
  - PR #303 fresh isolated runtime uses :115 and currently fails before login with no visible window.
derived:
  - gateway:6082 is the host-side service corresponding to the owner's synology:6082 with high confidence.
  - :98 is the strongest current backend-display candidate, but not a directly proven mapping.
unknown:
  - exact X display or VNC target port configured behind host TCP 6082.
  - provenance of the owner's earlier :88 observation in current canonical state.
conflicts: []
blockers:
  - no available authorized host-side process/config inspection path from this runner namespace.
next_action: inspect only the Synology host listener/process/config for TCP 6082 and record its websockify/RFB target display or VNC port.
```
