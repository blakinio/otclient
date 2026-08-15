---
task_id: OTC-20260815-track-a-novnc-display-diagnostic
status: investigating
agent: ChatGPT
session_id: chatgpt-novnc-display-diagnostic-20260815-2141
session_role: researcher
session_rotation_count: 2
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
updated: 2026-08-15T21:41:00+02:00
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
execution_reason: the successful Docker-gateway path exposes a new bounded discriminator: probe conventional direct RFB ports for displays 88/98/115 and compare sanitized RFB fingerprints with websockify 6082
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
user_communication: terminal_only
context_pressure: low
context_growth: stable
context_score: 4
estimate_confidence: high
decomposition_decision: single
invocation_started_at: 2026-08-15T21:41:00+02:00
last_progress_at: 2026-08-15T21:41:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: direct-rfb-fingerprint
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
stop_reason: null
next_action: through the already-proven Docker default gateway, read-only probe direct RFB ports 5988/5998/6015 and compare protocol/server-init fingerprints against websockify 6082; do not authenticate with VNC credentials or mutate any runtime
---

# Objective

Determine whether the owner's `synology:6082` noVNC endpoint can be mapped to a concrete X11 display, and recover enough read-only server characteristics to compare it with Track A PR #303's isolated `:115` runtime.

# Authority and safety boundary

This remains read-only discovery. The task may connect to the already-proven host-facing gateway and perform unauthenticated RFB metadata handshakes only. It must not launch or stop Tibia, use account/VNC credentials, signal or attach to processes, restart/reconfigure X/VNC, control Docker, enter a host namespace, perform gameplay actions, read another task's environment, or touch Track B.

PR #303 owns its runtime workflow, display `:115`, process lifecycle and task state. This task does not mutate those paths or processes.

# Acceptance inventory

- [x] Verify diagnostic jobs run on `synology-otclient-01`.
- [x] Establish hostname `synology` is not resolvable from the runner container namespace.
- [x] Inventory persistent X11 Unix sockets: exactly `:98` was present in both prior probes.
- [x] Derive the runner container default IPv4 gateway without printing the private address.
- [x] Prove TCP `6082` is reachable through that gateway.
- [x] Prove gateway `6082` serves HTTP noVNC, WebSocket `/websockify`, and unauthenticated RFB 3.8 metadata with framebuffer `1920x1080`.
- [ ] Probe only conventional direct RFB ports `5988`, `5998`, `6015` corresponding to the disputed/relevant displays `:88`, `:98`, `:115`.
- [ ] For any reachable direct RFB endpoint, compare a sanitized fingerprint of protocol version, security types, framebuffer dimensions, pixel format and hashed desktop name against the RFB stream exposed through `6082`.
- [ ] Reclassify the backend mapping strictly from observed network equivalence; keep exact websockify target configuration `UNKNOWN` unless evidence directly proves it.
- [ ] Persist the result and one exact next action if any ambiguity remains.

# Existing validation

First runner probe: `31903692616` / `95058202023` PASS.  
Docker-gateway probe: `31904447945` / `95059984786` PASS.

Proven prior markers include:

```text
DOCKER_GATEWAY_TCP_6082_REACHABLE=true
DOCKER_GATEWAY_NOVNC_HTTP_STATUS=200
DOCKER_GATEWAY_WEBSOCKIFY_UPGRADE_STATUS=101
DOCKER_GATEWAY_RFB_PROTOCOL_VERSION=003.008
DOCKER_GATEWAY_RFB_FRAMEBUFFER_WIDTH=1920
DOCKER_GATEWAY_RFB_FRAMEBUFFER_HEIGHT=1080
X11_SOCKET_DISPLAYS=:98
```

Durable evidence:

- `docs/agents/evidence/OTC-20260815-track-a-novnc-display-diagnostic/20260815-runner-probe.md`
- `docs/agents/evidence/OTC-20260815-track-a-novnc-display-diagnostic/20260815-docker-gateway-probe.md`

# Comparison boundary

## FACT

Historical positive-control run `31730884814`, attempt 14, job `94785048338` used `TRACK_DISPLAY=:98` for the same exact fenced official Linux client and created a visible `Tibia` window, submitted login and rendered a probable world view while SOCKS-confined.

PR #303 run `31903196011` used task-owned `DISPLAY=:115` and failed before login with `client_gen_1_window_missing`; its sanitized display-wide census recorded `visible_window_count=0`.

## Current inference

`:98` is the strongest backend candidate because it is the historical working display, the only persistent X11 socket visible to the runner, and its known-good screen profile is `1920x1080`, matching the RFB framebuffer exposed through `6082`.

## Current unknown

The RFB desktop name exposed through `6082` contains no numeric display hint. The exact websockify target remains unproven. The next network-equivalence probe is materially different from the completed gateway probe because it tests candidate direct RFB ports and compares their server fingerprints rather than repeating the 6082 handshake.

# Checkpoint

```yaml
status: investigating
proven:
  - gateway:6082 is reachable and exposes noVNC/websockify/RFB 3.8 with a 1920x1080 framebuffer.
  - exactly one persistent X11 Unix socket was visible during prior probes: :98.
  - historical positive-control Track A used :98 and rendered the official client successfully.
  - PR #303 isolated :115 currently fails before login with no visible window.
derived:
  - :98 is the strongest backend candidate.
unknown:
  - whether gateway direct RFB port 5998 is reachable and fingerprint-equivalent to the RFB stream through 6082.
  - exact configured websockify target display/port.
  - provenance of the earlier :88 observation.
conflicts: []
blockers: []
next_action: probe gateway direct RFB ports 5988/5998/6015 and compare sanitized fingerprints against 6082.
```
