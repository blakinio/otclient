---
task_id: OTC-20260815-track-a-runtime-reacquisition
status: waiting
agent: ChatGPT
session_id: chatgpt-runtime-researcher-20260815-1706
session_role: researcher
session_rotation_count: 4
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime-research
phase: restart-relogin-reacquisition
branch: research/OTC-20260815-track-a-runtime-reacquisition
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-runtime-reacquisition
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
related_pr: 303
updated: 2026-08-15T17:23:00+02:00
lease_released_at: 2026-08-15T17:23:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-runtime-reacquisition.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/**
  - .github/workflows/tibia-official-client-re-runtime-reacquisition.yml
  - .github/scripts/tibia-official-client-re-runtime-reacquisition.sh
depends_on:
  - coordinator-retained exact-build structural world evidence
  - historical login procedure in PR #290 as revalidation-required input only
  - PR #283 bridge evidence as read-only reference only
blocks:
  - terminal result of current task-owned Actions run 31892440526
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
runtime_code_bearing_head: 3327b8731e7c9babb53e9cc9c0f27428ede8ee5c
workflow_quality_head: 093cd60501e1a60529545e03baf2a73c6eab39ca
last_progress_at: 2026-08-15T17:23:00+02:00
ci_checks_for_current_head: 1
ci_check_generation: crashdump-discriminator
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 1
stall_warnings: 0
stop_reason: current task-owned semantic run remains in progress and partial logs are unavailable; lease released so another disjoint programme task can progress without polling
active_operation:
  type: clear_task_local_copied_crashdump_then_launch
  run_id: 31892440526
  job_id: 95030622195
  head: 093cd60501e1a60529545e03baf2a73c6eab39ca
  expected_marker: TRACK_A_RUNTIME_TASK_CRASHDUMP_CLEARED
last_checkpoint:
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-bundled-qt-loader-shadow.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-software-backend-required.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-x11-home-state-discriminator.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-minimal-home-falsified-xvfb-profile.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-xvfb-profile-falsified-rotation.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-canonical-package-path-falsified.md
next_action: on the first terminal state of run 31892440526, read job 95030622195 logs and artifact exactly; if login was reached, continue gen1/gen2 structural classification; if the copied crashdump was cleared and visible window is still absent, use at most one further repair cycle in this rotation and test physical task-owned package placement directly under the canonical task-local HOME rather than a symlink
---

# Objective

Prove or disprove restart/relogin/reacquisition stability for the existing exact-build structural Worldmap path in the official native Linux Tibia client. Research output remains Draft-only; promotion belongs to coordinator PR #300.

# Exact client and safety fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
runner: synology-otclient-01
task_state: /home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260815-track-a-runtime-reacquisition
display: ':115'
task_socks_port: 25415
upstream_track_a_socks_port: 25354
concurrency_group: official-client-re-runtime
```

Credentials may exist only in protected login steps. Persistent runtime processes must be credential-variable-free. Track B, shared upstream ownership, movement and irreversible gameplay/economic effects remain out of scope.

# Proven prerequisites and bounded negative results

FACT:
- exact source state `/work/_otclient_tibia_re_state`, exact client fence, `synology-otclient-01`, upstream WARP `25354`, task SOCKS relay `25415`, task-local Xvfb, process ownership/no-secret checks and cleanup are reproducible;
- exact existing `libpxbackend-1.0.so` loader path is repaired;
- official bundled Qt 6.9 precedence is repaired;
- software Qt Quick backend is active (`QSGSoftwareRenderThread` observed);
- repeated isolated X11 census is `visible_window_count=0` rather than a wrong title/PID;
- minimal non-secret launcher HOME alone is insufficient;
- historical Xvfb `1920x1080x24 -nolisten tcp -noreset` profile alone is insufficient;
- run `31892205905` proved the logical canonical task-HOME package pathname/argv was actually used and still failed at `client_gen_1_window_missing` before login;
- no protected login, movement, gameplay or economic effect occurred in runs #18-#26.

Positive control retained:
- historical run `31730884814`, attempt 14, job `94785048338` completed SUCCESS for this exact client on the same runner, resolved a visible `^Tibia$` window, entered probable world view and proved client transport local SOCKS `7`, direct established `0`, UDP `0`;
- attempt 15 failed later and must not replace attempt-14 evidence.

# Rotation-4 workflow quality gate

The workflow SC2016/SC2251/SC2015/SC2318 findings were repaired without intended runtime-semantic change. PR CI run `31892045307` completed SUCCESS. Canonical-path head CI `31892208631` completed SUCCESS. Current crashdump-discriminator head CI `31892441838` also completed SUCCESS.

# Run #26 — canonical logical package path

Run `31892205905` / job `95030054619` / head `01b130a9e42a1f313d84f5480bd103f08f1c1b86` emitted:

```text
TRACK_A_RUNTIME_CANONICAL_PACKAGE_LAUNCH generation=1 path=/home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260815-track-a-runtime-reacquisition/runs/31892205905/home-gen-1/.local/share/CipSoft GmbH/Tibia/packages/Tibia
TRACK_A_EXACT_CLIENT_VERIFIED size=51965216 sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
TRACK_A_CREDENTIAL_ENV_CLEAR role=client-gen-1 pid=3892
TRACK_A_RUNTIME_ERROR=client_gen_1_window_missing
```

Artifact `9248852812`, digest `sha256:370d6a94e3dc83a0b2ec622f02dbe94a36b5092f7e64c4471711baa2d7a8dc37`, records `visible_window_count=0`. Durable evidence: `20260815-canonical-package-path-falsified.md`.

This run discriminates logical pathname/argv through the task-local symlink. It does **not** yet prove that a process whose physical package inode/cwd lives under canonical HOME is equivalent to the historical positive control.

# Run #27 — in flight

Run `31892440526` / job `95030622195`, head `093cd60501e1a60529545e03baf2a73c6eab39ca`, keeps run-26 semantics and additionally deletes only contents of the copied task-owned `runs/<id>/package/crashdump` after bootstrap, records the prior entry count, and verifies it empty. The persistent source package/crashdump is never mutated.

At lease release the job is still in `Setup isolated runtime and arm generation 1`; protected login steps have not started and GitHub does not yet expose partial job logs.

# Acceptance gate

- [ ] exact client SHA/size rechecked on both successful live generations;
- [ ] fresh PID/PIE proven after restart;
- [ ] WARP/SOCKS confinement proved with no forbidden direct client transport;
- [ ] structural `IN_GAME` proved independently of GUI/network liveness;
- [ ] structural read reacquired after clean restart/relogin;
- [x] runner/source/WARP/relay/Xvfb prerequisites recovered and independently evidenced;
- [x] loader, bundled Qt, software renderer, visible-window census, minimal-HOME, Xvfb-profile and logical canonical-path hypotheses discriminated;
- [x] workflow exact-head repository CI restored and retained green through the current discriminator head;
- [x] no unauthorized gameplay effect occurred through run #26;
- [ ] classify run #27 terminally;
- [ ] final exact-head CI terminal green before Draft handoff.
