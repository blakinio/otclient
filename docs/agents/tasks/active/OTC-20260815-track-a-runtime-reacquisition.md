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
updated: 2026-08-15T14:35:00+02:00
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
last_progress_at: 2026-08-15T14:35:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: runtime
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 2
identical_failure_retries: 0
repair_cycles_for_current_gate: 4
context_reconstruction_attempts: 1
stall_warnings: 0
claim_check: passed against the released/waiting task, open Draft PR #303, exact main@8fca1c3 and RUNTIME-only changed paths
active_operation:
  type: lifecycle_hardened_exact_runtime_reacquisition
  run_id: 31884912160
  job_id: 95012697134
  execution_head: 22885f000370fc3e1543e71795101d4a763871f3
  runner_id: 21
  runner_name: synology-otclient-01
  current_gate: bootstrap
  failed_run_residue_recovery: success
last_checkpoint:
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-runner-selector-recovery.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-upstream-source-state-recovery.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-cross-step-process-lifecycle-recovery.md
next_action: inspect only the next material state transition from run 31884912160 / job 95012697134; do not dispatch a duplicate while it is active
---

# Objective

Prove or disprove restart/relogin/reacquisition stability for the existing exact-build structural Worldmap read path in the official native Linux Tibia client. Research output remains Draft-only; promotion belongs to coordinator PR #300.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
runner: synology-otclient-01
```

# Runtime ownership and safety

```yaml
state_directory: /home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260815-track-a-runtime-reacquisition
display: ':115'
task_socks_port: 25415
upstream_track_a_socks_port: 25354
process_marker: OTCLIENT_TIBIA_RE_TASK=OTC-20260815-track-a-runtime-reacquisition
track_marker: OTCLIENT_TIBIA_RE_TRACK=official-client-re
concurrency_group: official-client-re-runtime
```

Credentials may exist only in protected login-step inputs. Persistent client/X/observer/relay environments must remain free of credential variables. The task must not touch Track B, shared upstream wireproxy ownership, foreign display locks/sockets or irreversible gameplay/economic effects. Movement is not part of this hypothesis.

# Closed infrastructure gates — FACT

## Runner selector

Run `31883846172` / job `95010096196` requested `[self-hosted, otclient, synology]` and stayed unassigned. Independent P0 jobs using `[otclient, synology]` executed on runner id `21`. The exact stale queued run was fenced and retired; RUNTIME now uses the proven two-label selector. Subsequent RUNTIME jobs are assigned to `synology-otclient-01`.

Evidence: `20260815-runner-selector-recovery.md`.

## Proven source state and upstream WARP

Run `31884181155` first exposed hardcoded canonical-source discovery. Historical successful exact-build execution proved `/work/_otclient_tibia_re_state` as the runner source when `/work` is writable. The task now keeps mutable task state canonical while source client/toolroot/upstream discovery is read-only and exact-client fenced across proven legacy/canonical states.

Run `31884531727` then proved:

```text
TRACK_A_RUNTIME_SOURCE_STATE=/work/_otclient_tibia_re_state
TRACK_A_UPSTREAM_WARP_VERIFIED=true pid=16739 source_state=/work/_otclient_tibia_re_state
TRACK_A_EXACT_CLIENT_VERIFIED size=51965216 sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
TRACK_A_TASK_SOCKS_RELAY_VERIFIED=true port=25415 pid=21755
TRACK_A_TASK_XVFB_VERIFIED=true display=:115 pid=21792
TRACK_A_RUNTIME_NAMESPACE_READY=true
```

The task does not start, stop or rewrite the shared upstream wireproxy.

Evidence: `20260815-upstream-source-state-recovery.md`.

# Cross-step lifecycle failure and repair — FACT

Run `31884531727` lost Xvfb ownership after bootstrap but before generation 1:

```text
TRACK_A_RUNTIME_ERROR=xvfb_not_owned
```

The same Xvfb PID had passed exact Track/Task/Role and credential-environment checks during bootstrap. Client/login/GDB generation work never started. Final cleanup also failed before complete X11/task-state cleanup, making residue recovery necessary.

Workflow head `22885f000370fc3e1543e71795101d4a763871f3` now:

- uses `setsid` for task-local relay, Xvfb, generation client and GDB observer, all still launched without `RUNNER_TRACKING_ID` and without credential variables;
- removed the no-longer-needed Actions-write stale-run cancellation preflight after that run became terminal;
- recovers only exact failed run `31884531727` residue;
- terminates only PIDs whose Track/Task/Role ownership can be proved from `/proc/<pid>/environ`;
- removes stale X11 lock/socket only when attributable to the failed Xvfb and inactive;
- requires task SOCKS port `25415` to be free after residue recovery;
- adds a new workflow-step boundary gate that re-proves relay and Xvfb liveness, role ownership and no-secret environments before a client may launch.

Evidence: `20260815-cross-step-process-lifecycle-recovery.md`.

# Current run #9 — FACT

Run `31884912160` / job `95012697134` is the sole active semantic RUNTIME operation at code-bearing head `22885f000370fc3e1543e71795101d4a763871f3` and is assigned to runner id `21`, `synology-otclient-01`.

Completed successfully so far:

1. checkout;
2. explicit resume request + exact helper/client fence;
3. runner-layout/lifecycle compatibility materialization;
4. fail-closed recovery of exact task-owned residue from failed run `31884531727`.

The run is currently in bootstrap. After two unchanged bootstrap-state observations no further identical polling is allowed until a material transition occurs.

# Acceptance gate

- [ ] exact client SHA/size rechecked on every generation;
- [ ] fresh PID and PIE proven after restart;
- [ ] WARP/SOCKS confinement proved with no forbidden direct client transport;
- [ ] structural `IN_GAME` proved independently of GUI/network liveness;
- [ ] structural read reacquired after one clean restart/relogin cycle, or an exact prerequisite blocker retained;
- [ ] persistent child environments proved credential-variable-free across step boundaries;
- [x] failed-run residue recovery is fail-closed on exact task ownership;
- [x] no unauthorized gameplay effect has occurred in any recovery run so far;
- [ ] exact final-head repository CI terminal before Draft handoff.

# Current UNKNOWN pending existing run

- whether `setsid` preserves the task-local relay/Xvfb across the bootstrap step boundary;
- generation-1 client/GDB preparation;
- protected login-secret availability/acceptance;
- generation-1 structural `IN_GAME`;
- clean generation-1 stop;
- generation-2 fresh PID/PIE and structural reacquisition;
- final confinement and cleanup outcome.

# Next action

Inspect the existing run `31884912160` / job `95012697134` only after it makes a material state transition. Repair only the first new evidence-backed failure; do not dispatch a conceptual duplicate while this job is active.
