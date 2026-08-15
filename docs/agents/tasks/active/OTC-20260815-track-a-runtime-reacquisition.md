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
updated: 2026-08-15T14:43:00+02:00
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
runtime_code_bearing_head: e5d73eb092968479782bd77061ca12c449b9f62f
invocation_started_at: 2026-08-15T14:14:00+02:00
last_progress_at: 2026-08-15T14:43:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: runtime
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 2
identical_failure_retries: 0
repair_cycles_for_current_gate: 5
context_reconstruction_attempts: 1
stall_warnings: 0
claim_check: passed against released task, open Draft PR #303, exact main@8fca1c3 and RUNTIME-only paths
active_operation:
  type: read_only_client_pid_marker_discriminator
  run_id: 31885303986
  job_id: 95013631491
  execution_head: c632cb8f519c78f85e4209a0ef3c8484f2193ef2
  runner_id: 21
  runner_name: synology-otclient-01
last_checkpoint:
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-xkbcomp-root-cause.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-xkbcomp-location.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-xkb-recovered-client-ownership-failure.md
next_action: consume only diagnostic run 31885303986; repair the exact client PID/marker lifecycle failure it proves, then resume generation-1 preparation without changing login semantics
---

# Objective

Prove or disprove restart/relogin/reacquisition stability for the existing exact-build structural Worldmap path in the official native Linux Tibia client. Output remains Draft-only; promotion belongs to coordinator PR #300.

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

# Closed prerequisite gates — FACT

- runner scheduling recovered to proven selector `[otclient, synology]`, runner id `21`;
- exact source state `/work/_otclient_tibia_re_state` and exact client fence are reproducible;
- upstream Track A wireproxy/WARP through port `25354` is proven without taking ownership;
- task-local SOCKS relay `25415` is proven with Track/Task/Role and no-secret markers;
- Xvfb `./xkbcomp` root cause was proven read-only;
- exact executable `xkbcomp` was proven at `/work/_otclient_tibia_re_state/toolroot/usr/bin/xkbcomp`;
- Xvfb launch cwd repair is proven by runtime run #12;
- relay/Xvfb both survive a workflow-step boundary with exact ownership/no-secret checks.

# Run #12 — first exact-client generation launch

Run `31885192604` / job `95013369670`, head `e5d73eb092968479782bd77061ca12c449b9f62f`, reached farther than all prior recovery runs.

Completed `SUCCESS` before generation launch:

1. exact resume-request/helper fences;
2. XKB/lifecycle compatibility materialization;
3. exact failed-run residue recovery;
4. source/WARP/exact-client bootstrap;
5. task relay and Xvfb startup;
6. cross-step persistence gate for relay and Xvfb.

Key proof:

```text
TRACK_A_RUNTIME_PERSISTENT_CHILD_VERIFIED role=socks-relay pid=23997
TRACK_A_RUNTIME_PERSISTENT_CHILD_VERIFIED role=xvfb pid=24032
TRACK_A_RUNTIME_PERSISTENT_RELAY_LISTENING=true
```

`Prepare generation 1` then reverified the exact package client and failed after launch/PID capture but before window/GDB/login:

```text
TRACK_A_EXACT_CLIENT_VERIFIED size=51965216 sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
TRACK_A_RUNTIME_ERROR=client_gen_1_ownership_failed
```

Artifact id `9247072540`, ZIP SHA-256 `dacb6fe4ac20eece815003dcb409fc393b32e749883234f0d8edcb4986c12f46`.

No login step ran. No credential values were injected into the client launch. No movement/gameplay/economic action occurred. Generation-1 GDB observer was not armed. Generation 2 was not attempted.

Evidence: `20260815-xkb-recovered-client-ownership-failure.md`.

# Current discriminator

The helper failure occurs after `$!` is written to `client-gen-1.pid`, after `/proc/$pid/maps` becomes readable, at `role_owned "$pid" "client-gen-1" "$client"`.

### UNKNOWN

Current evidence does not yet distinguish whether:

- `$!` is a transient `setsid`/wrapper PID while the marked client is a child;
- client startup re-execs/forks to another PID;
- exact executable identity differs at the recorded PID;
- one Track/Task/Role marker is absent.

Read-only diagnostic run `31885303986` / job `95013631491` is inspecting exact failed-run residue: recorded PID, PID/exe/PPID, exact task/role matches across `/proc`, immediate children, Xvfb/relay state, X11 residue and sanitized `client.log`. It does not start/stop/signal processes and does not access credentials.

# Acceptance gate

- [ ] exact client SHA/size rechecked on both successful live generations;
- [ ] fresh PID/PIE proven after restart;
- [ ] WARP/SOCKS confinement proved with no forbidden direct client transport;
- [ ] structural `IN_GAME` proved independently of GUI/network liveness;
- [ ] structural read reacquired after clean restart/relogin;
- [x] runner/source/WARP/relay/Xvfb prerequisites recovered and independently evidenced;
- [x] persistent relay/Xvfb survive a step boundary with no-secret ownership proof;
- [x] no unauthorized gameplay effect has occurred;
- [ ] final exact-head CI terminal before Draft handoff.

# Next action

Consume the existing read-only client-ownership diagnostic only. Apply one evidence-backed PID/marker lifecycle repair, recover only exact task-owned run #12 residue, and resume generation-1 preparation. Do not change protected login semantics or dispatch an identical runtime retry without the discriminator result.
