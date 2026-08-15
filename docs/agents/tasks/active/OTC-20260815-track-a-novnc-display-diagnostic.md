---
task_id: OTC-20260815-track-a-novnc-display-diagnostic
status: blocked
agent: ChatGPT
session_id: chatgpt-novnc-display-diagnostic-20260815-2118
session_role: researcher
session_rotation_count: 0
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
updated: 2026-08-15T21:24:00+02:00
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
execution_reason: live Synology-side endpoint and X11 metadata were inspected through a bounded self-hosted runner probe without taking ownership of PR #303 runtime
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
user_communication: terminal_only
context_pressure: low
context_growth: stable
context_score: 4
estimate_confidence: high
decomposition_decision: single
invocation_started_at: 2026-08-15T21:18:00+02:00
last_progress_at: 2026-08-15T21:24:00+02:00
ci_checks_for_current_head: 1
ci_check_generation: diagnostic
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
stop_reason: missing_synology_host_network_namespace_access
next_action: from the Synology host or another authorized tool in its LAN/host namespace, inspect read-only the listener/process/config backing TCP 6082 and record its websockify/RFB target display without restarting or signalling any VNC/X11/runtime process
---

# Objective

Determine whether the owner's `synology:6082` noVNC endpoint can be mapped to a concrete X11 display, and recover enough read-only server characteristics to compare it with Track A PR #303's isolated `:115` runtime.

# Authority and safety boundary

This is a read-only discovery task. The diagnostic did not launch or stop the Tibia client, use credentials, signal/attach to processes, restart or reconfigure X/VNC, control Docker, perform gameplay actions, read another task's environment, or touch Track B.

PR #303 owns its runtime workflow, display `:115`, process lifecycle and task state. This task did not mutate those paths or processes.

# Acceptance inventory

- [x] Verify the job runs on `synology-otclient-01`.
- [x] Resolve whether hostname `synology` is reachable from the runner: it is not resolvable in the runner network namespace.
- [x] Attempt the bounded HTTP/WebSocket/RFB probe without authentication or secret access; it cannot reach the endpoint because hostname resolution fails.
- [x] Inventory currently visible X11 Unix display sockets: exactly `:98` was present.
- [x] Record whether observed metadata directly identifies the X display behind `6082`: it does not.
- [x] Compare against PR #303: historical positive control is `:98`; fresh isolated failing reacquisition is `:115`.
- [x] Preserve one concrete next action while the mapping remains UNKNOWN.

# Validation

Read-only diagnostic workflow:

```text
head=fe57c76db37056f3df0e66b5c6bcb71f96565d3b
run=31903692616
job=95058202023
runner=synology-otclient-01
job_result=SUCCESS
```

The successful job result means the diagnostic itself executed as designed; it does not mean the noVNC mapping was established.

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

At the later noVNC diagnostic time, the dedicated runner namespace exposed exactly one X11 Unix socket, `:98`. Neither `:88` nor `:115` was present.

## INFERENCE — high confidence

`:98` is the strongest current candidate for the persistent GUI environment the owner expects to observe because it is both the verified historical working display and the only persistent X11 socket visible to the dedicated runner.

## UNKNOWN

`6082 -> :98` is not proven. The browser-facing hostname `synology` does not resolve from the GitHub Actions runner network namespace, the repository contains no canonical `6082`/websockify mapping, and no authorized NAS/SSH/host connector is available in this session.

The owner's earlier observation involving `:88` remains unverified in current canonical repository/runtime evidence.

# Blocker

The remaining discriminator exists outside the accessible runner namespace: host-side listener/process/config metadata for TCP `6082`. Repeating the same runner probe cannot resolve this and is forbidden without a materially new access path or hypothesis.

# Checkpoint

```yaml
status: blocked
proven:
  - main at task start is 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45.
  - diagnostic head fe57c76db37056f3df0e66b5c6bcb71f96565d3b ran successfully as run 31903692616 job 95058202023 on synology-otclient-01.
  - runner namespace cannot resolve hostname synology.
  - exactly one X11 Unix socket was visible at probe time: :98.
  - historical positive-control Track A runtime used :98 and created the visible official-client window.
  - PR #303 fresh isolated runtime uses :115 and currently fails before login with no visible window.
derived:
  - :98 is the strongest current candidate for the persistent GUI environment, but it is not a proven 6082 backend mapping.
unknown:
  - exact X display served by browser endpoint synology:6082.
  - host-side websockify/RFB listener target and configuration.
  - provenance of the owner's earlier :88 observation in current canonical state.
conflicts: []
blockers:
  - current GitHub-only runner cannot resolve/access the Synology LAN hostname and no authorized host/SSH connector is available.
next_action: from the Synology host or another authorized tool in its LAN/host namespace, inspect read-only the listener/process/config backing TCP 6082 and record its websockify/RFB target display without restarting or signalling any VNC/X11/runtime process.
```
