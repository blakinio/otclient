---
task_id: OTC-20260815-track-a-runtime-reacquisition
status: active
agent: ChatGPT
session_id: chatgpt-runtime-researcher-20260815-1405
session_role: researcher
session_rotation_count: 1
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
updated: 2026-08-15T14:05:00+02:00
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
code_bearing_head: 4bd5cbc47fbfd816a6ab5dd66b57c88b3ff981f4
invocation_started_at: 2026-08-15T14:05:00+02:00
last_progress_at: 2026-08-15T14:05:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: runtime
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
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

# Runtime ownership

```yaml
state_directory: /home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260815-track-a-runtime-reacquisition
display: ':115'
task_socks_port: 25415
upstream_track_a_socks_port: 25354
process_marker: OTCLIENT_TIBIA_RE_TASK=OTC-20260815-track-a-runtime-reacquisition
track_marker: OTCLIENT_TIBIA_RE_TRACK=official-client-re
concurrency_group: official-client-re-runtime
```

The task never owns the shared upstream Track A wireproxy process and must not touch Track B state/processes, pre-existing X11 locks/sockets or a process whose task role/executable markers cannot be verified.

# Credential and effect boundary

Credentials may exist only in protected secret inputs to the minimal login step. Persistent client/X/observer/relay processes are launched without `TIBIA_TEST_EMAIL` or `TIBIA_TEST_PASSWORD` and their environments are checked before semantic use. Secret values must never be printed, persisted, OCRed, inspected or artifacted.

Allowed side effects are login/session recovery and clean task-owned process restart only. No market, trade, forge, currency or irreversible gameplay effect is authorized. Movement is not part of this hypothesis.

# Planned discriminator

For each generation:

1. verify exact client SHA/size and task-local WARP/SOCKS confinement;
2. launch a fresh client with task-local HOME/display/relay and no credential variables in its environment;
3. arm the exact-build structural Worldmap breakpoint at static offset `0x19a8ea3` before login;
4. require a logged-out zero-record negative baseline;
5. use protected credentials only in the login step;
6. require multiple valid `(x,y,z,order)` Worldmap records and sustained task-local SOCKS with zero direct TCP/UDP escape;
7. cleanly stop task-owned observer/client;
8. repeat with a fresh PID and PIE base;
9. accept only if both generations independently satisfy the structural gate and PID/PIE are fresh.

# Safety repair retained

Code-bearing head `4bd5cbc47fbfd816a6ab5dd66b57c88b3ff981f4` fails closed on observer cleanup before starting generation 2 or deleting task-local state. Compare to current PR head proves the only later files are this task record and `20260815-observer-cleanup-hardening.md`; runtime implementation is unchanged.

# Resume preflight — 2026-08-15 14:05 +02

### FACT

- `main` remains `8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`.
- P0 stale queued run `31880617510` was fenced and cancelled by its owning task; it is no longer a concurrency blocker.
- P0 run `31883178675` executed on `synology-otclient-01`, proving the selector can currently reach the dedicated runner.
- P0 run `31883422477` / job `95009054487` found zero currently live exact Track A client processes and left P0 `waiting` on RUNTIME ownership for a bounded live process window.
- The latest RUNTIME code-bearing workflow run `31882125124` at `4bd5cbc47fbfd816a6ab5dd66b57c88b3ff981f4` was cancelled while the old serialized dependency existed; it produced no semantic reacquisition result.

### INFERENCE

The original RUNTIME waiting prerequisite is materially changed: the serialized P0 blocker is released and the matching runner is proven reachable. Re-running the existing exact code-bearing RUNTIME workflow is now a distinct authorized retry under changed external state, not an identical blind retry.

### UNKNOWN

- whether protected Tibia login secrets are populated/accepted;
- generation-1 structural `IN_GAME`;
- generation-2 fresh PID/PIE and read reacquisition;
- live credential-environment assertions;
- cleanup outcome;
- bridge `session_epoch` / R4 semantics;
- A3/A4.

# Acceptance gate

- [ ] exact client SHA/size rechecked on every generation;
- [ ] fresh PID and PIE proven after restart;
- [ ] WARP/SOCKS confinement proved with no forbidden direct client transport;
- [ ] structural `IN_GAME` proved independently of GUI/network liveness;
- [ ] structural read reacquired after one clean restart/relogin cycle, or an exact prerequisite blocker retained;
- [ ] persistent child environments proved credential-variable-free;
- [x] workflow cleanup fails closed before deleting task-local state when observer stop cannot be proven;
- [ ] no unauthorized gameplay effect occurred;
- [ ] exact final-head repository CI terminal before Draft handoff.

# Next action

Re-run cancelled workflow run `31882125124` on exact code-bearing head `4bd5cbc47fbfd816a6ab5dd66b57c88b3ff981f4` now that the serialized P0 dependency is released. Inspect exact job logs/artifacts and classify the first material runtime result; do not weaken gates or create a conceptual duplicate.
