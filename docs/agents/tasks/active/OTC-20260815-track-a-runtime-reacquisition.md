---
task_id: OTC-20260815-track-a-runtime-reacquisition
status: active
agent: ChatGPT
session_id: chatgpt-runtime-researcher-20260815-1529
session_role: researcher
session_rotation_count: 3
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
updated: 2026-08-15T15:29:00+02:00
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
invocation_started_at: 2026-08-15T15:29:00+02:00
last_progress_at: 2026-08-15T15:29:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: runtime
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 6
context_reconstruction_attempts: 1
stall_warnings: 0
claim_check: takeover after prior task checkpoint lease expired; live main remained 8fca1c3, PR #303 remained open Draft/mergeable, run #17 was terminal SUCCESS, PR head d0e11895415266b1f3cf8904d67f5e3a8aa54577 had no newer active operation, and all planned writes remain inside RUNTIME ownership
active_operation:
  type: repair_exact_client_loader_path_and_resume_reacquisition
  discriminator_run_id: 31886223175
  discriminator_job_id: 95015803600
  discriminator_head: 5b213ca776cbf55a235742f8a799000d41e4dc02
  exact_libpxbackend: /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/libproxy/libpxbackend-1.0.so
last_checkpoint:
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-client-loader-pxbackend-failure.md
next_action: add only the proven libproxy directory to the exact-client loader path, restore the full bounded reacquisition workflow with all prior safety/materialization gates, recover only exact task-owned residue, and inspect the next semantic run
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

Run `31885192604` / job `95013369670`, head `e5d73eb092968479782bd77061ca12c449b9f62f`, reached the exact client launch after all infrastructure gates. It failed before login at client ownership discovery. No credentials or gameplay effects occurred.

# Run #16 — exact loader failure

Run `31885896845` / job `95015034558`, head `527369447672a355b6fc0a3f8a4f9c2b39f33b67`, passed helper materialization, residue recovery, bootstrap and persistence, then failed before login with:

```text
client: error while loading shared libraries: libpxbackend-1.0.so: cannot open shared object file: No such file or directory
```

Evidence: `20260815-client-loader-pxbackend-failure.md`.

# Run #17 — loader discriminator result

Read-only run `31886223175` / job `95015803600`, head `5b213ca776cbf55a235742f8a799000d41e4dc02`, completed `SUCCESS` and proved the required existing library at:

```text
/work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/libproxy/libpxbackend-1.0.so
```

The exact failed-run residue at observation time contained one task-owned live SOCKS relay, dead Xvfb/client, no active X11 lock/socket, and the task-local SOCKS port still listening. The next repair must reuse this existing library; installing/downloading a replacement is not authorized or necessary.

# Acceptance gate

- [ ] exact client SHA/size rechecked on both successful live generations;
- [ ] fresh PID/PIE proven after restart;
- [ ] WARP/SOCKS confinement proved with no forbidden direct client transport;
- [ ] structural `IN_GAME` proved independently of GUI/network liveness;
- [ ] structural read reacquired after clean restart/relogin;
- [x] runner/source/WARP/relay/Xvfb prerequisites recovered and independently evidenced;
- [x] persistent relay/Xvfb survive a step boundary with no-secret ownership proof;
- [x] exact missing `libpxbackend-1.0.so` location proven read-only;
- [x] no unauthorized gameplay effect has occurred;
- [ ] final exact-head CI terminal before Draft handoff.

# Next action

Patch only the exact-client loader search path with the proven `toolroot/usr/lib/x86_64-linux-gnu/libproxy` directory, restore and execute the full bounded reacquisition workflow, and classify the first new semantic result. Do not change protected login semantics, exact client fence, Track B isolation, or effect budget.
