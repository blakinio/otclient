---
task_id: OTC-20260815-track-a-runtime-reacquisition
status: waiting
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
updated: 2026-08-15T14:12:00+02:00
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
  - exact self-hosted run 31883846172 / job 95010096196 exists but remained queued across the two allowed unchanged-state observations; semantic execution has not started
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
invocation_started_at: 2026-08-15T14:05:00+02:00
last_progress_at: 2026-08-15T14:12:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: runtime
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 2
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
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

# Durable resume state

### FACT

- P0 owner fenced and cancelled stale run `31880617510`; it is no longer the serialized runtime blocker.
- P0 run `31883178675` executed on `synology-otclient-01`.
- P0 run `31883422477` / job `95009054487` proved zero currently live exact Track A client processes; P0 remains UNKNOWN and waits for a RUNTIME-created live observation window.
- The latest pre-resume runtime helper is exact Git blob `c1b88d4cc17edf2684b93d7e516f9c694e37966a` from code-bearing head `4bd5cbc47fbfd816a6ab5dd66b57c88b3ff981f4`.
- GitHub refused direct retry of cancelled run `31882125124`, so an explicit task-owned `runtime-run-request.json` was persisted and fenced.
- Workflow head `950ce8f5f7cf22b457e82cdb20e9eec285438d9c` validates the run request, exact helper blob, branch/repository/runner identity and exact client fence before runtime work.
- This created run `31883846172`, job `95010096196` (`reacquire`).
- Observation 1: queued. Observation 2: queued. No semantic step has started.
- Full resume/queue evidence is in `20260815-resume-dispatch-queued.md`.

### UNKNOWN

- runner assignment/busy state; runner inventory remains unavailable to the current GitHub integration;
- protected login-secret availability/acceptance;
- generation-1 structural `IN_GAME`;
- generation-2 fresh PID/PIE and structural read reacquisition;
- transport confinement and credential-environment results;
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

# Real stop condition

The task has no further safe local mutation while the exact self-hosted job is queued. `EXECUTION_PROTOCOL.md` forbids keeping an active worker alive only to wait/poll, and `ANTI_STALL_AND_EXECUTION_BUDGET.md` forbids a third unchanged check. The lease is therefore released with `status: waiting` rather than fabricating progress or dispatching a duplicate.

# Next action

Resume only after run `31883846172` materially changes state. Inspect job `95010096196` logs/artifacts first. If it executes, classify generation 1/2 from structural records, PID/PIE, transport and environment evidence; if it remains unassigned at the next authorized barrier, retain the exact external blocker without another conceptual duplicate.
