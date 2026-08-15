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
updated: 2026-08-15T14:14:00+02:00
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
resume_dispatch_head: 950ce8f5f7cf22b457e82cdb20e9eec285438d9c
invocation_started_at: 2026-08-15T14:14:00+02:00
last_progress_at: 2026-08-15T14:14:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: runtime
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 1
stall_warnings: 0
claim_check: passed against waiting task, open Draft PR #303, exact main@8fca1c3 and seven changed files all inside declared RUNTIME ownership
active_operation:
  type: repair_verified_runner_selector_and_resume_exact_reacquisition
  stale_run_id: 31883846172
  stale_job_id: 95010096196
  stale_head: 950ce8f5f7cf22b457e82cdb20e9eec285438d9c
last_checkpoint: docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-resume-dispatch-queued.md
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

Credentials may exist only in protected login-step inputs. Persistent client/X/observer/relay environments must remain free of credential variables. The task must not touch Track B, shared upstream wireproxy ownership, foreign display locks/sockets, or irreversible gameplay/economic effects. Movement is not part of this hypothesis.

# Proven selector mismatch — 2026-08-15 14:14 +02

### FACT

- Previous RUNTIME resume run `31883846172` / `reacquire` job `95010096196` remains queued, has zero steps, `runner_id=0`, and requests `[self-hosted, otclient, synology]`.
- The RUNTIME workflow still declares `runs-on: [self-hosted, otclient, synology]`.
- During the same external-state interval, independently owned P0 static run `31883967070` / job `95010405800` requested `[otclient, synology]`, was assigned to runner id `21` / `synology-otclient-01`, and completed `SUCCESS`.
- Earlier P0 runtime job `95008500800` also executed on runner id `21` with `[otclient, synology]`.
- `main` remains exact `8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`.
- PR #303 remains open, Draft and mergeable; every changed path is inside this task's declared ownership.

### INFERENCE

The RUNTIME queue is no longer correctly classified as generic runner availability. The extra `self-hosted` label is incompatible with the known working registration of `synology-otclient-01` and is the specific scheduling blocker to repair. Removing only that label restores the selector already proven by two independent P0 jobs without weakening repository, runner-name, branch, exact-client, run-request or runtime safety fences.

### UNKNOWN

After scheduling is repaired, the first semantic runtime result remains unknown: protected-secret availability/acceptance, generation-1 structural `IN_GAME`, generation-2 fresh PID/PIE reacquisition, transport confinement, credential-environment assertions and cleanup outcome all still require execution.

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

Fence and retire only the exact stale RUNTIME run `31883846172` if it is still queued, change only the runner selector to `[otclient, synology]`, preserve the explicit resume request and all runtime/credential/cleanup fences, then inspect the first material execution result. Do not dispatch conceptual duplicates or weaken semantic gates.
