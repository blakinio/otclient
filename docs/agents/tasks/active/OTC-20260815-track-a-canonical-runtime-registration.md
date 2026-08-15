---
task_id: OTC-20260815-track-a-canonical-runtime-registration
status: active
agent: ChatGPT
session_id: chatgpt-canonical-runtime-registration-20260815-2333
session_role: researcher
session_rotation_count: 0
project_lane: otclient
lane: RUNTIME-DIAGNOSTIC
track_id: official-client-re
task_kind: discovery
phase: read-only-runtime-registration
branch: research/OTC-20260815-track-a-canonical-runtime-registration
base_branch: main
base_main: f6fa2264904c6ffb3734d4a63e1edbb29260fcc1
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-canonical-runtime-registration
worktree_mode: isolated_branch_checkout_equivalent
risk: low
related_pr: null
updated: 2026-08-15T23:33:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-canonical-runtime-registration.md
  - docs/agents/evidence/OTC-20260815-track-a-canonical-runtime-registration/**
  - .github/scripts/tibia-official-client-re-canonical-runtime-registration.py
  - .github/workflows/tibia-official-client-re-canonical-runtime-registration.yml
depends_on:
  - merged PR #312 canonical-live lease manager
  - merged PR #313 lease concurrency remediation
  - PR #311 policy v4 as pending governance dependency
  - coordinator-promoted PR #309 display-candidate evidence as bounded read-only input
blocks: []
policy_version: 4
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: bounded read-only discovery of persistent display/process identity; no controller mutation or overlap with PR #303 task-owned :115 runtime
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: low_noise
implementation_authorized: true
last_progress_at: 2026-08-15T23:33:00+02:00
ci_check_generation: initial-registration-probe
---

# Objective

Determine whether the persistent Track A display candidate `:98` currently hosts a live exact-fenced official Linux Tibia client that can later be registered as the canonical live runtime. This task is **read-only** and does not grant or exercise controller mutation authority.

# Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Allowed read-only observations

- enumerate persistent X11 Unix sockets;
- query X11 top-level/visible windows on `:98` without input/focus mutation;
- recover window `_NET_WM_PID`/PID when exposed;
- inspect only `/proc/<pid>/exe`, `/proc/<pid>/stat` process-start metadata and executable size/SHA;
- read Linux boot ID for PID-reuse fencing;
- query host-facing noVNC/websockify `6082` RFB metadata;
- inspect the RFB desktop name **in memory only** and emit sanitized booleans such as whether it explicitly references display 98; do not print the raw name;
- emit only non-secret registration metadata and classifications.

# Forbidden

- no client launch/stop/restart/login/logout;
- no keyboard/mouse/input/focus actions;
- no ptrace/GDB/LD_PRELOAD/injection;
- no process signals;
- no credential/session/environment reads;
- no screenshot/framebuffer payload export;
- no VNC input or password use;
- no Docker/host control;
- no modification of display `:98` or PR #303 display `:115`;
- no Track B access.

# Required semantic outcomes

- `EXACT_LIVE_RUNTIME_CANDIDATE_PROVEN`: live `:98` window -> current PID/process-start identity -> exact client fence all proven;
- `PERSISTENT_DISPLAY_NO_LIVE_CLIENT`: `:98` exists but no live official-client candidate is found;
- `LIVE_CLIENT_IDENTITY_MISMATCH`: a candidate exists but exact fence fails;
- `INCONCLUSIVE`.

Exact `6082 -> :98` mapping is a separate optional discriminator. If the sanitized RFB desktop name explicitly identifies `:98`, record that fact; otherwise preserve mapping as UNKNOWN.

# Acceptance gate

- [ ] exact runner verified;
- [ ] persistent X11 socket census recorded;
- [ ] window/PID identity recovered read-only or boundedly absent;
- [ ] PID reuse fence uses boot ID + process start ticks;
- [ ] exact executable size/SHA verified for any positive candidate;
- [ ] no secrets/environment/framebuffer content logged;
- [ ] `6082` mapping overclaim prevented;
- [ ] result stored as machine-readable/sanitized evidence;
- [ ] exact-head CI terminal green;
- [ ] task released for coordinator review rather than merged.

# Next action

Open the Draft PR, implement one bounded self-hosted read-only probe on `synology-otclient-01`, execute once, and classify the current persistent runtime candidate without mutating it.
