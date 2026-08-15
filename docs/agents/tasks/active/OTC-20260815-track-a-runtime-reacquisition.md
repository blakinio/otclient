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
updated: 2026-08-15T13:12:53+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-runtime-reacquisition.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/**
  - .github/workflows/tibia-official-client-re-runtime-reacquisition.yml
  - .github/scripts/tibia-official-client-re-runtime-reacquisition.sh
depends_on:
  - coordinator-retained exact-build structural world evidence
  - historical login procedure in PR #290 as untrusted/revalidation-required input only
  - PR #283 bridge evidence as reference only; no ownership of its paths
blocks:
  - separately owned P0 run 31880617510 / job 95002559098 is queued with runner_id=0 in the same official-client-re-runtime concurrency group
  - runtime run 31881287155 has not materialized/assigned its self-hosted reacquire job; direct runner inventory is unavailable through the current GitHub integration (HTTP 403)
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
last_checkpoint: docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-runtime-reacquisition-waiting.md
code_bearing_head: 9d5734ced2155cf01ab6cbdfabfb2eb2707b7152
---

# Objective

Prove or disprove restart/relogin/reacquisition stability for the already-established Track A exact-build structural world read path, without repeating basic world-entry or one-off movement proof as the hypothesis.

# Dispatch contract

```yaml
TASK_ID: OTC-20260815-track-a-runtime-reacquisition
TASK_RECORD: docs/agents/tasks/active/OTC-20260815-track-a-runtime-reacquisition.md
PROJECT_LANE: otclient
LANE: RUNTIME
BASE_MAIN: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
BRANCH: research/OTC-20260815-track-a-runtime-reacquisition
WORKTREE: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-runtime-reacquisition
OWNED_PATHS:
  - docs/agents/tasks/active/OTC-20260815-track-a-runtime-reacquisition.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/**
  - .github/workflows/tibia-official-client-re-runtime-reacquisition.yml
  - .github/scripts/tibia-official-client-re-runtime-reacquisition.sh
DEPENDENCIES:
  - exact-build structural world evidence retained by coordinator PR #300
  - PR #290 procedure is evidence input only, not authority
  - PR #283 bridge/profile evidence is reference-only
```

Research output is DRAFT-ONLY. Promotion belongs to coordinator PR #300.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
runner: synology-otclient-01
```

# Starting facts and safety corrections

- later exact-build evidence proves `synology-otclient-01` has executed Track A jobs; old #280/#281 'no self-hosted runner available' checkpoints are not current facts;
- a single live structural world observer + reversible transition was previously proven for this exact build;
- historical login/session procedure in #290 is `REVALIDATION_REQUIRED`, not current runtime proof;
- rejected #289 contains a material safety finding: credentials must **not** be job-scoped into persistent child process environments;
- rejected #289 also demonstrates that shared X display sockets/locks must never be deleted without task ownership proof.

# Hypothesis

A task-owned Track A runtime can be restarted and, when protected credentials are available through repository secrets, relogged into the world such that the structural world observer/read path is deterministically reacquired without reusing stale PID/PIE/object state.

# Required discrimination

Test at least two generations of runtime identity when authorized state exists:

```text
generation N structural IN_GAME/read proof
-> clean task-owned client/observer teardown
-> fresh client start/login under the same isolated task namespace
-> fresh PID/PIE/profile/observer acquisition
-> generation N+1 structural IN_GAME/read proof
```

If credentials or safe login prerequisites are unavailable, stop with an exact evidence-backed WAITING/BLOCKED classification; do not fabricate restart stability from process-only checks.

# Credential and namespace rules

- credentials may exist only as protected secret inputs to the minimal login helper invocation;
- do not define credentials at job scope;
- explicitly ensure persistent X/DBus/client/observer processes are launched without credential values in their environments;
- never print, persist, OCR, artifact, or inspect credential values;
- task must use only its own display/socket/state/PID files and verify ownership before cleanup;
- do not touch Track B runtime/state/display/ports/processes.

# Live runtime namespace

The following concrete namespace is reserved by this task for its bounded validation run:

```yaml
runtime_namespace:
  state_directory: /home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260815-track-a-runtime-reacquisition
  display: ':115'
  task_socks_port: 25415
  upstream_track_a_socks_port: 25354
  upstream_track_a_socks_mode: read_only_dependency
  process_marker: OTCLIENT_TIBIA_RE_TASK=OTC-20260815-track-a-runtime-reacquisition
  track_marker: OTCLIENT_TIBIA_RE_TRACK=official-client-re
  concurrency_group: official-client-re-runtime
cleanup_contract:
  - never delete an X11 lock or socket that pre-existed this task
  - never signal a process without both the task marker and expected executable/role evidence
  - never stop or reconfigure the shared upstream Track A WARP/wireproxy process
  - task client connects only to the task-local relay port 25415
```

Active Track A draft contracts #301, #302 and #304 use disjoint repository-owned paths; #301/#304 are static, while #302 is a passive runtime reader serialized by `official-client-re-runtime`. Track B #284 is outside authority and uses its own container/display namespace. Any unexpected live collision on `:115`, port `25415`, or the task state directory is an abort condition rather than a cleanup target.

# Acceptance gate

- [ ] exact client SHA/size rechecked on every generation;
- [ ] fresh PID and PIE base proven after restart; no stale address reuse;
- [ ] WARP/SOCKS confinement verified, with no direct client TCP and no client UDP where the canonical login model requires it;
- [ ] structural `IN_GAME`/world state proved independently of keypress/socket existence;
- [ ] structural observer/read path reacquired after at least one clean restart/relogin cycle, or an exact prerequisite blocker recorded;
- [ ] persistent child environments verified free of credential variables;
- [ ] task-owned namespace cleanup cannot delete another task's display/socket/state;
- [ ] no gameplay action beyond what is strictly required for safe read discrimination;
- [ ] exact-head CI terminal before Draft handoff.

# Side-effect budget

Login/session recovery and clean process restart only. No market/trade/forge/currency effects. Movement is not part of the hypothesis and should not be repeated unless a single reversible step is necessary solely to distinguish live structural world state; if used, verify inverse restoration.

# Planned discriminator

For each generation, arm the exact-build structural Worldmap breakpoint at static offset `0x19a8ea3` before credentials are supplied. Require a bounded logged-out `NO_STIMULUS` baseline with zero valid Worldmap records, then use the protected login helper and require multiple validated `(x,y,z,order)` Worldmap records after character activation. This tests the existing structural read path without repeating movement. Repeat the same resolver procedure after a clean task-owned client/observer restart and require a fresh PID/PIE.

# Current checkpoint

### FACT

- Draft PR #303 remains open and Draft-only on `research/OTC-20260815-track-a-runtime-reacquisition` against `main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`.
- The task-owned helper/workflow are implemented at code-bearing head `9d5734ced2155cf01ab6cbdfabfb2eb2707b7152` with the credential, namespace, transport, negative-control and fresh-PID/PIE fences described above.
- Standard PR CI for that code-bearing head completed `success` in run `31881289268`.
- Earlier runtime workflow runs `31880945751` and `31881193523` were cancelled before a task self-hosted runtime job appeared in the GitHub jobs inventory; they provide no runtime semantic evidence.
- Current runtime run `31881287155` targets the code-bearing head and is `in_progress`, but its jobs inventory contains only auxiliary `luacheck`/`cppcheck` check-runs; no `reacquire` self-hosted job has yet materialized/been assigned.
- Separately owned P0 run `31880617510` / job `95002559098` remains `queued` with `runner_id=0` and uses the same `official-client-re-runtime` concurrency group. Its own task record is `waiting` on that job.
- Direct self-hosted runner inventory returned HTTP `403 Resource not accessible by integration`; current `online/busy` runner state cannot be verified through this connector.
- Durable waiting evidence is recorded at `docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-runtime-reacquisition-waiting.md`.

### UNKNOWN

- Current online/busy state of a matching self-hosted runner.
- Whether protected login secrets are currently populated and accepted; the protected login step has not executed.
- Generation 1 structural `IN_GAME`, generation 2 fresh PID/PIE, restart/relogin reacquisition, runtime credential-environment assertions and runtime cleanup outcome.
- Bridge `session_epoch` / R4 semantics.
- Action gates A3 and A4; historical reversible GUI movement is not sufficient to promote them.

# Resume condition

Resume when the serialized Track A runtime lane can assign this task's `reacquire` job on `synology-otclient-01` without cancelling/bypassing separately owned P0 work. Re-fetch current `main`, PR/task ownership and the exact Draft head before execution. Inspect exact runtime logs/artifacts before classifying any semantic claim.

# Execution-budget checkpoint

```yaml
invocation_started_at: 2026-08-15T12:49:00+02:00
checkpoint_at: 2026-08-15T13:12:53+02:00
code_bearing_head: 9d5734ced2155cf01ab6cbdfabfb2eb2707b7152
ordinary_exact_head_checks: 1
repair_cycles: 2
identical_failure_retries: 0
runtime_semantic_runs_completed: 0
no_progress_state: false
context_pressure: medium
next_action: resume exact runtime run only after the separately owned queued P0/self-hosted lane releases; do not poll indefinitely or bypass ownership
```

# Deliverable

Draft PR only with the task-scoped workflow/helper and sanitized evidence. Preserve failures and unavailable credentials/prerequisites as explicit WAITING/BLOCKED results rather than weakening the gate.
