---
task_id: OTC-20260815-track-a-novnc-display-diagnostic
status: investigating
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
updated: 2026-08-15T21:35:00+02:00
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
execution_reason: a materially new read-only access path is available by probing the runner container default gateway, which may be the Synology Docker host, without taking ownership of PR #303 runtime
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
last_progress_at: 2026-08-15T21:35:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: docker-gateway-diagnostic
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
stop_reason: null
next_action: extend the existing read-only workflow to derive the runner container default IPv4 gateway without printing the private address, probe only TCP/HTTP/WebSocket port 6082 on that gateway, and if reachable perform the same sanitized unauthenticated RFB metadata handshake to determine whether the backend exposes an X display hint
---

# Objective

Determine whether the owner's `synology:6082` noVNC endpoint can be mapped to a concrete X11 display, and recover enough read-only server characteristics to compare it with Track A PR #303's isolated `:115` runtime.

# Authority and safety boundary

This is a read-only discovery task. It may add or refine a temporary branch-local workflow and inspect only non-secret runtime/network metadata from `synology-otclient-01`.

Forbidden:

- launching or stopping the Tibia client;
- login, account credentials, cookies or session material;
- signalling or attaching to processes;
- modifying, removing or restarting any X server, VNC service, container or port;
- Docker control or host-namespace mutation;
- gameplay or account effects;
- reading another task's process environment;
- touching Track B state or paths.

PR #303 owns its runtime workflow, display `:115`, process lifecycle and task state. This task does not mutate those paths or processes.

# Acceptance inventory

- [x] Verify the first diagnostic job ran on `synology-otclient-01`.
- [x] Resolve whether hostname `synology` is reachable from the runner: it is not resolvable in the runner network namespace.
- [x] Attempt the bounded HTTP/WebSocket/RFB probe without authentication or secret access; direct hostname access failed at DNS resolution.
- [x] Inventory currently visible X11 Unix display sockets: exactly `:98` was present during the first probe.
- [x] Record whether first-probe metadata directly identifies the X display behind `6082`: it does not.
- [x] Compare against PR #303: historical positive control is `:98`; fresh isolated failing reacquisition is `:115`.
- [ ] Test the materially new Docker-default-gateway access path to TCP `6082` without printing the gateway address.
- [ ] If gateway `6082` is reachable, perform only sanitized HTTP/WebSocket/RFB metadata negotiation and record a display hint if the unauthenticated protocol exposes one.
- [ ] Reclassify `6082 -> :98` as PROVEN, DISPROVEN, or still UNKNOWN from direct evidence.
- [ ] Preserve one concrete next action while any required mapping remains UNKNOWN.

# Validation to date

First read-only diagnostic workflow:

```text
head=fe57c76db37056f3df0e66b5c6bcb71f96565d3b
run=31903692616
job=95058202023
runner=synology-otclient-01
job_result=SUCCESS
```

Sanitized material results:

```text
SYNLOGY_HOSTNAME_RESOLVED=false
NOVNC_HTTP_REACHABLE=false
WEBSOCKIFY_RFB_PROBE_COMPLETE=false
X11_SOCKET_DISPLAY_COUNT=1
X11_SOCKET_DISPLAYS=:98
XDPYINFO_AVAILABLE=true
X11_DISPLAY_98_QUERY=unavailable
TRACK_A_NOVNC_READONLY_PROBE_COMPLETE=true
```

Durable evidence:

`docs/agents/evidence/OTC-20260815-track-a-novnc-display-diagnostic/20260815-runner-probe.md`

# Comparison boundary

## FACT

Historical positive-control run `31730884814`, attempt 14, job `94785048338` used `TRACK_DISPLAY=:98` for the same exact fenced official Linux client and successfully created the visible `Tibia` window, submitted login and rendered a probable world view while remaining SOCKS-confined.

PR #303 run `31903196011` used task-owned `DISPLAY=:115` and failed before login with `client_gen_1_window_missing`; its sanitized display-wide census recorded `visible_window_count=0`.

At the first noVNC diagnostic time, the dedicated runner namespace exposed exactly one X11 Unix socket, `:98`. Neither `:88` nor `:115` was present.

## INFERENCE — high confidence

`:98` is the strongest current candidate for the persistent GUI environment the owner expects to observe because it is both the verified historical working display and the only persistent X11 socket visible to the dedicated runner.

## UNKNOWN

`6082 -> :98` is not yet proven. The browser-facing hostname `synology` did not resolve from the GitHub Actions runner network namespace and the repository contains no canonical `6082`/websockify mapping.

The owner's earlier observation involving `:88` remains unverified in current canonical repository/runtime evidence.

# Continuation discriminator

The previous blocker is narrowed by a new non-destructive hypothesis: `synology-otclient-01` runs inside a container and its default IPv4 route may terminate at the Synology Docker host. The next probe may derive that gateway from `/proc/net/route`, keep the private address out of logs, and test only whether port `6082` presents the expected noVNC/WebSocket/RFB service. This is a materially new access path, not an identical retry of hostname resolution.

No host process inspection, Docker API use, namespace entry, client launch, VNC authentication, process control or configuration mutation is authorized.

# Checkpoint

```yaml
status: investigating
proven:
  - current main remains 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45 at continuation start.
  - PR #309 remains Draft/open and task-owned at prior head d19b4c177750364a21a046167ab2cc90fcb1accf before this checkpoint.
  - first diagnostic run 31903692616 job 95058202023 succeeded on synology-otclient-01.
  - runner namespace could not resolve hostname synology.
  - exactly one X11 Unix socket was visible during the first probe: :98.
  - historical positive-control Track A runtime used :98 and created the visible official-client window.
  - PR #303 fresh isolated runtime uses :115 and currently fails before login with no visible window.
derived:
  - :98 is the strongest current candidate for the persistent GUI environment, but it is not a proven 6082 backend mapping.
unknown:
  - whether the runner container default gateway is the host path exposing port 6082.
  - exact X display served by browser endpoint synology:6082.
  - host-side websockify/RFB listener target and configuration.
  - provenance of the owner's earlier :88 observation in current canonical state.
conflicts: []
blockers: []
next_action: derive and probe only the runner default gateway port 6082 through the bounded read-only workflow and classify the resulting noVNC/RFB evidence.
```
