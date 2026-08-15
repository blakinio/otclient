---
task_id: OTC-20260815-track-a-runtime-reacquisition
status: active
agent: ChatGPT
session_id: chatgpt-runtime-researcher-20260815-1414
session_role: researcher
session_rotation_count: 2
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
updated: 2026-08-15T14:39:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-runtime-reacquisition.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/**
  - .github/workflows/tibia-official-client-re-runtime-reacquisition.yml
  - .github/scripts/tibia-official-client-re-runtime-reacquisition.sh
depends_on:
  - coordinator-retained exact-build structural world evidence
  - historical login procedure in PR #290 as revalidation-required input only
  - PR #283 bridge evidence as read-only reference only
blocks: []
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
code_bearing_head: 22885f000370fc3e1543e71795101d4a763871f3
invocation_started_at: 2026-08-15T14:14:00+02:00
last_progress_at: 2026-08-15T14:39:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: runtime
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 4
context_reconstruction_attempts: 1
stall_warnings: 0
claim_check: passed against released task, Draft PR #303 and RUNTIME-only changed paths
active_operation:
  type: read_only_locate_xkbcomp_dependency
  run_id: 31885075194
  job_id: 95013088148
  execution_head: d4a376bfa9ba24db1e3fe02bb69fd0709bdd1a6f
  runner_id: 21
  runner_name: synology-otclient-01
last_checkpoint:
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-cross-step-process-lifecycle-recovery.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-xvfb-bootstrap-exit.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-xkbcomp-root-cause.md
next_action: use only the read-only dependency-location result from run 31885075194 to repair Xvfb launch cwd/path; do not issue another runtime bootstrap before that evidence exists
---

# Objective

Prove or disprove restart/relogin/reacquisition stability for the existing exact-build structural Worldmap read path in the official native Linux Tibia client. Research output remains Draft-only; promotion belongs to coordinator PR #300.

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

Credentials may exist only in protected login steps. Persistent runtime processes must be secret-free. Track B, shared upstream ownership and irreversible gameplay/economic effects remain out of scope. No movement is part of this RUNTIME hypothesis.

# Closed infrastructure gates — FACT

- runner selector `[otclient, synology]` is proven on runner id `21`; the stale `[self-hosted, otclient, synology]` run was fenced and retired;
- source state `/work/_otclient_tibia_re_state` is exact-client fenced;
- upstream Track A wireproxy PID `16739` and WARP through port `25354` were proven in executable runtime runs;
- task-local SOCKS relay on `25415` is reproducibly started with exact Track/Task/Role markers and no credential variables;
- failed run `31884531727` residue was recovered fail-closed before run #9.

# Run #9 — direct failure classification

Run `31884912160` / job `95012697134` at head `22885f000370fc3e1543e71795101d4a763871f3` completed `FAILURE` before generation 1.

It again proved source state, upstream WARP, exact client and task relay. The lifecycle helper used `setsid`, but bootstrap then failed with:

```text
TRACK_A_RUNTIME_ERROR=xvfb_exited
```

Generation 1, login, client and GDB observer were never started. Artifact id: `9247009047`, ZIP SHA-256 `1e0390c04fc219d33130f5affb137f3995b4dc6294f6867a8f9eeaee57104edb`.

Evidence: `20260815-xvfb-bootstrap-exit.md`.

# Read-only Xvfb diagnostic — FACT

Run `31885018787` / job `95012954293` completed `SUCCESS` without starting/stopping/signalling any runtime process. It inspected only task-owned failed-run residue.

Failed Xvfb PID `22489` and relay PID `22453` were both dead; no `:115` lock/socket remained. The source Xvfb binary exists and is executable.

Sanitized `runtime/xvfb.log` gives the direct root cause:

```text
sh: 1: ./xkbcomp: not found
sh: 1: ./xkbcomp: not found
XKB: Failed to compile keymap
Keyboard initialization failed. This could be a missing or incorrect setup of xkeyboard-config.
(EE) Fatal server error:
(EE) Failed to activate virtual core keyboard: 2(EE)
```

Diagnostic artifact id: `9247024733`, ZIP SHA-256 `299cb6b7004213f1f726d336c3f2fafbb4eaa6e86b3e2b516cb8c02bc3dd88ce`.

Evidence: `20260815-xkbcomp-root-cause.md`.

# Current discriminator

### FACT

The failure is now isolated to Xvfb's relative `./xkbcomp` invocation. It is not a runner, WARP, exact-client, relay, secret/login or gameplay failure.

### INFERENCE

The narrow repair is to launch Xvfb from the exact directory containing the source-state `xkbcomp`, but only after that location/executable is proven read-only.

### UNKNOWN

The exact `xkbcomp` path under the proven toolroot remains pending. Run `31885075194` / job `95013088148` is the sole active read-only dependency-location diagnostic. Runtime generation 1/2 and P0 live handoff remain untested.

# Acceptance gate

- [ ] exact client SHA/size rechecked on both live generations;
- [ ] fresh PID/PIE proven after restart;
- [ ] WARP/SOCKS confinement proved with no forbidden direct client transport;
- [ ] structural `IN_GAME` proved independently of GUI/network liveness;
- [ ] structural read reacquired after clean restart/relogin;
- [ ] persistent child environments proved credential-variable-free;
- [x] runner scheduling recovered;
- [x] source/upstream WARP discovery recovered without taking ownership;
- [x] failed-run residue recovery is fail-closed;
- [x] Xvfb bootstrap failure has a direct stderr root cause;
- [x] no unauthorized gameplay effect has occurred in recovery/diagnostic runs;
- [ ] final exact-head repository CI terminal before Draft handoff.

# Next action

Consume only the result of diagnostic run `31885075194`. If it proves an executable `xkbcomp`, repair only Xvfb launch cwd/path and restore the previously fenced runtime workflow. If it does not, retain the exact missing dependency as the real blocker; do not retry bootstrap blindly.
