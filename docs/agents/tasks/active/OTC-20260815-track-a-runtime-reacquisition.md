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
updated: 2026-08-15T14:26:00+02:00
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
code_bearing_head: 972936ffef081318b6103a6c799feeb3ce36fc92
invocation_started_at: 2026-08-15T14:14:00+02:00
last_progress_at: 2026-08-15T14:26:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: runtime
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 2
identical_failure_retries: 0
repair_cycles_for_current_gate: 3
context_reconstruction_attempts: 1
stall_warnings: 0
claim_check: passed against waiting task, open Draft PR #303, exact main@8fca1c3 and changed paths wholly inside declared RUNTIME ownership
active_operation:
  type: execute_exact_runtime_reacquisition_after_selector_and_source_state_recovery
  run_id: 31884531727
  job_id: 95011797563
  execution_head: 972936ffef081318b6103a6c799feeb3ce36fc92
  runner_id: 21
  runner_name: synology-otclient-01
last_checkpoint:
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-runner-selector-recovery.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-upstream-source-state-recovery.md
next_action: inspect the first material state transition from existing run 31884531727 only; do not dispatch a conceptual duplicate while job 95011797563 is active
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

# Scheduling recovery — FACT

Run `31883846172` / job `95010096196` requested `[self-hosted, otclient, synology]` and remained unassigned with `runner_id=0`. During the same interval P0 jobs using `[otclient, synology]` executed on runner id `21`, `synology-otclient-01`.

Workflow head `4f5314cfefa4dfeb150f4e5d912ef4180c4efc67` fenced and retired only that exact stale queued run and changed RUNTIME scheduling to the proven selector `[otclient, synology]`. New job `95010941902` was immediately assigned to runner id `21`. The selector blocker is closed.

Evidence: `20260815-runner-selector-recovery.md`.

# First executable bootstrap — FACT

Run `31884181155` / job `95010941902` passed checkout, explicit run-request verification and exact helper syntax/blob fences. It then failed before generation 1 with:

```text
TRACK_A_RUNTIME_ERROR=upstream_wireproxy_unavailable
```

The concrete missing path was canonical `/home/runner/_work/_otclient_tibia_re_state/runtime/wireproxy.pid`. Login did not run. Cleanup completed successfully, reported no X11 residue and removed task-ephemeral state. No gameplay action occurred.

Historical successful exact-build job `94785974126` on the same runner had selected `/work/_otclient_tibia_re_state` whenever `/work` was writable. This proves a runner-layout mismatch between source-state discovery and canonical task-state ownership.

# Read-only source-state recovery — FACT

Task-owned mutable state remains canonical. The workflow now derives a task-local effective helper from the exact hash-fenced repository helper and changes only source discovery:

- source client must match exact SHA/size;
- toolroot/client/Xvfb source may come from proven `/work/_otclient_tibia_re_state` or canonical state;
- wireproxy PID files are inspected read-only;
- exactly one distinct live upstream PID with the Track A marker is required;
- SOCKS port `25354` must listen;
- Cloudflare trace must report `warp=on` or `warp=plus`;
- zero or multiple eligible upstream processes fail closed;
- the task never starts/stops/rewrites the shared upstream wireproxy.

Workflow head `4573900d7c3c4b042881f22c33ff00a19c684fd5` had a YAML serialization defect in embedded transform strings and never created a RUNTIME job. No runtime side effect occurred. Head `972936ffef081318b6103a6c799feeb3ce36fc92` corrected only that serialization defect.

Run `31884531727` parsed correctly. Preflight `95011788055` succeeded and `reacquire` `95011797563` was assigned to runner id `21`, `synology-otclient-01`.

Evidence: `20260815-upstream-source-state-recovery.md`.

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

# Current UNKNOWN pending existing run

- whether a single eligible upstream Track A wireproxy is still alive in the proven source state;
- whether WARP through `25354` verifies;
- source toolroot/Xvfb dependency availability;
- protected login-secret availability/acceptance;
- generation-1 structural `IN_GAME`;
- generation-2 fresh PID/PIE and structural reacquisition;
- final transport confinement and cleanup outcome.

# Next action

Inspect the existing run `31884531727` / job `95011797563` when it makes a material state transition. Do not issue an identical retry while it is active. Repair only the first new evidence-backed failure, preserving all ownership, credential, transport and cleanup gates.
