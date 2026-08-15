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
updated: 2026-08-15T14:09:00+02:00
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
invocation_started_at: 2026-08-15T14:05:00+02:00
last_progress_at: 2026-08-15T14:09:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: runtime
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
active_operation:
  type: exact_build_runtime_reacquisition
  run_id: 31883846172
  job_id: 95010096196
  workflow: .github/workflows/tibia-official-client-re-runtime-reacquisition.yml
  execution_head: 950ce8f5f7cf22b457e82cdb20e9eec285438d9c
  first_observed_status: queued
  source_code_blob: c1b88d4cc17edf2684b93d7e516f9c694e37966a
  run_request: docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/runtime-run-request.json
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

Credentials may exist only in protected login-step inputs. Persistent client/X/observer/relay environments must remain free of credential variables. The task must not touch Track B, shared upstream wireproxy ownership, foreign display locks/sockets, or irreversible gameplay/economic effects.

# Changed prerequisite and dispatch

### FACT

- P0 owner fenced and cancelled stale run `31880617510`; it no longer holds the serialized runtime lane.
- P0 run `31883178675` executed on `synology-otclient-01`.
- P0 run `31883422477` / job `95009054487` proved zero currently live exact Track A client processes and left P0 waiting on RUNTIME to create a bounded live process window.
- Latest RUNTIME implementation before resume is helper blob `c1b88d4cc17edf2684b93d7e516f9c694e37966a` from code-bearing head `4bd5cbc47fbfd816a6ab5dd66b57c88b3ff981f4`; later pre-resume changes were task/evidence only.
- GitHub API refused direct retry of cancelled run `31882125124` (`403 This workflow run cannot be retried`).
- A durable request `runtime-run-request.json` now fences the changed prerequisite, exact client, code-bearing head and authorized/forbidden effects.
- Workflow head `950ce8f5f7cf22b457e82cdb20e9eec285438d9c` validates that request and exact helper Git blob before runtime work; push created run `31883846172`, job `95010096196`.
- First job observation: `queued`.

### UNKNOWN pending exact run

- protected-secret availability/acceptance;
- generation-1 structural `IN_GAME`;
- generation-2 fresh PID/PIE and read reacquisition;
- transport confinement/credential-environment assertions;
- cleanup result;
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

Inspect run `31883846172` only after material state change or within the bounded external-operation policy. Consume the first material runtime result and artifacts, classify FACT/UNKNOWN without weakening gates, then checkpoint and release the RUNTIME task if an external blocker remains.
