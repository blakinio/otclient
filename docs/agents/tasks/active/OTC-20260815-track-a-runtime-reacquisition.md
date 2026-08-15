---
task_id: OTC-20260815-track-a-runtime-reacquisition
status: waiting
agent: chatgpt-runtime-researcher
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
updated: 2026-08-15T13:28:53+02:00
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
  - separately owned P0 run 31880617510 / job 95002559098 is still queued with runner_id=0 in the same official-client-re-runtime concurrency group
  - runtime self-hosted reacquisition cannot execute until that serialized lane is assigned; direct runner inventory remains unavailable through the current GitHub integration (HTTP 403)
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
code_bearing_head: 4bd5cbc47fbfd816a6ab5dd66b57c88b3ff981f4
last_checkpoint:
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-runtime-reacquisition-waiting.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-observer-cleanup-hardening.md
---

# Objective

Prove or disprove restart/relogin/reacquisition stability for the existing exact-build structural Worldmap read path in the official native Linux Tibia client. The task must not promote canonical Track A claims; promotion belongs to coordinator PR #300.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
runner: synology-otclient-01
```

Every live generation must recheck this exact identity before build-specific offsets are used.

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

The task never owns the shared upstream Track A wireproxy process. It must not touch Track B state/processes, pre-existing X11 locks/sockets or a process whose task role/executable markers cannot be verified.

# Credential and effect boundary

Credentials may exist only in protected secret inputs to the minimal login step. Persistent client/X/observer/relay processes are launched without `TIBIA_TEST_EMAIL` or `TIBIA_TEST_PASSWORD`, and their environments are checked before semantic use. Secret values must never be printed, persisted, OCRed, inspected or artifacted.

Allowed side effects are login/session recovery and clean task-owned process restart only. No market, trade, forge, currency or irreversible gameplay effect is authorized. Movement is not part of this hypothesis.

# Planned discriminator

For each generation:

1. verify exact client SHA/size and task-local WARP/SOCKS confinement;
2. launch a fresh client with task-local HOME/display/relay and no credential variables in its environment;
3. arm the exact-build structural Worldmap breakpoint at static offset `0x19a8ea3` before login;
4. require a bounded logged-out `NO_STIMULUS` baseline with zero valid Worldmap records;
5. use protected credentials only in the login step;
6. require multiple validated `(x,y,z,order)` Worldmap records plus sustained task-local SOCKS use with zero direct client TCP/UDP escape;
7. cleanly stop the task-owned observer/client;
8. repeat with a fresh PID and PIE base;
9. accept only if both generations independently satisfy the structural gate and PID/PIE are fresh.

A running process, click/key submission or socket existence is not `IN_GAME` proof.

# Safety repair

At code-bearing head `4bd5cbc47fbfd816a6ab5dd66b57c88b3ff981f4`, the workflow was hardened around a fail-open cleanup edge:

- generation-1 stop now verifies the run-local observer PID is no longer alive before generation 2 begins;
- final cleanup invokes both generation stops without suppressing failure;
- each observer PID is rechecked before namespace deletion;
- task-root cleanup is reached only after those stop checks pass.

This preserves task-local recovery evidence when observer shutdown or ownership cannot be proven. The repair is documented in `20260815-observer-cleanup-hardening.md`. It does not constitute runtime semantic evidence.

# Current verified state

### FACT

- `main` remains `8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45` at this checkpoint.
- Draft PR #303 remains the sole RUNTIME research PR for this task.
- Previous code-bearing PR CI at `9d5734ced2155cf01ab6cbdfabfb2eb2707b7152` completed successfully in run `31881289268`.
- Previous checkpoint-head CI at `0270b1f3b6e75c995649b405758f058bae026c88` completed successfully in run `31881523546`.
- Runtime run `31881287155` never produced a self-hosted `reacquire` job in the observed jobs inventory and therefore provides no runtime semantic result.
- P0 run `31880617510` remains queued on the same serialized Track A runtime group; it is separately owned and must not be cancelled or bypassed by this task.
- cleanup hardening was committed at `4bd5cbc47fbfd816a6ab5dd66b57c88b3ff981f4`; exact-head CI for the subsequent documentation checkpoint is the remaining repository validation gate.

### UNKNOWN

- current `synology-otclient-01` online/busy state;
- whether protected Tibia login secrets are currently populated and accepted;
- generation-1 structural `IN_GAME`;
- generation-2 fresh PID/PIE and structural read reacquisition;
- live runtime credential-environment assertions;
- final runtime cleanup outcome;
- bridge `session_epoch` / R4 semantics;
- A3 and A4.

# Acceptance gate

- [ ] exact client SHA/size rechecked on every generation;
- [ ] fresh PID and PIE proven after restart;
- [ ] WARP/SOCKS confinement proved with no forbidden direct client transport;
- [ ] structural `IN_GAME` proved independently of GUI/network liveness;
- [ ] structural read reacquired after at least one clean restart/relogin cycle, or an exact prerequisite blocker retained;
- [ ] persistent child environments proved credential-variable-free;
- [x] workflow cleanup fails closed before deleting task-local state when observer stop cannot be proven;
- [ ] no unauthorized gameplay effect occurred;
- [ ] exact final-head repository CI terminal before Draft handoff.

# Execution-budget checkpoint

```yaml
invocation_started_at: 2026-08-15T13:20:00+02:00
last_progress_at: 2026-08-15T13:28:53+02:00
ci_checks_for_current_head: 1
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 1
stall_warnings: 0
runtime_semantic_runs_completed: 0
```

# Next action

When the separately owned P0/self-hosted lane releases, inspect the existing/new serialized RUNTIME run on the exact current Draft head. Classify generation 1/2 only from exact logs/artifacts; do not create a conceptual duplicate, cancel P0 or weaken the acceptance gate.
