---
task_id: OTC-20260815-track-a-novnc-display-diagnostic
status: investigating
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
related_pr: null
updated: 2026-08-15T21:18:00+02:00
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
execution_reason: live Synology-side endpoint and X11 metadata can be inspected safely through a bounded self-hosted runner probe without taking ownership of PR #303 runtime
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
last_progress_at: 2026-08-15T21:18:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: diagnostic
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
next_action: run one bounded read-only Synology runner probe that resolves synology:6082, performs a sanitized noVNC/WebSocket/RFB handshake when reachable, inventories visible X11 sockets/server characteristics without process control, and compare the result with PR #303 display :115
---

# Objective

Determine whether the owner's `synology:6082` noVNC endpoint can be mapped to a concrete X11 display, and recover enough read-only server characteristics to compare it with Track A PR #303's isolated `:115` runtime.

# Authority and safety boundary

This is a read-only discovery task. It may add a temporary branch-local workflow and inspect only non-secret runtime metadata from `synology-otclient-01`.

Forbidden:

- launching or stopping the Tibia client;
- login, account credentials, cookies or session material;
- signalling or attaching to processes;
- modifying, removing or restarting any X server, VNC service, container or port;
- Docker control;
- gameplay or account effects;
- reading another task's process environment;
- touching Track B state or paths.

PR #303 owns its runtime workflow, display `:115`, process lifecycle and task state. This task does not mutate those paths or processes.

# Acceptance inventory

- [ ] Verify the job runs on `synology-otclient-01`.
- [ ] Resolve whether hostname `synology` is reachable from the runner and whether TCP/HTTP port `6082` responds.
- [ ] If `/websockify` is reachable, perform only a bounded protocol handshake and report sanitized RFB protocol/server metadata; never authenticate with or retrieve a VNC secret.
- [ ] Inventory currently visible X11 Unix display sockets and query only non-secret display/server properties where possible.
- [ ] Record whether any observed metadata directly identifies the X display behind `6082`.
- [ ] Compare the observable profile against PR #303's exact `:115` configuration and latest failure without claiming an unproven mapping.
- [ ] Preserve one concrete next action if mapping remains UNKNOWN.

# Known comparison boundary

PR #303 exact head `1147062b1f91298055f8623043457298c5797600`, run `31903196011`, used task-owned `DISPLAY=:115` and failed before login with `client_gen_1_window_missing`. The effective run set the software Qt Quick backend, disabled XCB GL integration and removed explicit GLX Xvfb flags. This task treats those facts as read-only comparison input and does not rerun or alter PR #303.

# Checkpoint

```yaml
status: investigating
proven:
  - main is 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45 at task start.
  - PR #303 separately owns Track A runtime reacquisition and display :115.
  - repository search on current main found no canonical 6082/websockify mapping.
unknown:
  - exact backend X display served by synology:6082.
  - whether the noVNC service is visible from the dedicated runner network namespace.
conflicts: []
blockers: []
next_action: run the bounded read-only runner diagnostic described above.
```
