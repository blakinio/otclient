---
task_id: OTC-20260828-current-login-field6-runtime
status: validating
agent: ChatGPT
session_id: chatgpt-20260828-2255-field6-v4
session_role: implementer
policy_version: 2
project_lane: otclient
lane: RUNTIME_RESEARCH
track_id: official-client-re
task_kind: reverse_engineering_runtime
phase: validate
branch: fix/OTC-20260828-field6-v4-generation
base_branch: main
base_main: 72565873d89f0e626a0be9397d5d913dc164c0d1
created: 2026-08-28T19:00:00+02:00
updated: 2026-08-28T23:18:00+02:00
risk: high
execution_class: github_hosted
execution_mode: github_actions_static
execution_reason: TDD replacement of consumed V3 exact trigger with a non-executable-until-admitted V4 generation plus historical-rerun revocation guard
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
physical_action_budget: 0
physical_action_count: 0
implementation_authorized: true
live_runtime_authorization_source: NOT_APPLICABLE
related_pr: 783
context_pressure: medium
context_growth: stable
context_score: 9
estimate_confidence: medium
decomposition_decision: phased
decomposition_reason: field6 proof remains one sequential evidence chain; Track B is a separate consumer phase after scalar promotion
validation_level: exact_head
last_completed_step: Codex P1 historical V3 rerun guard GREEN; non-overlapping main drift through PR #784 classified before final restack
session_rotation_count: 1
heavy_validation_runs: 0
stale_takeover_count: 0
human_interruptions: 0
invocation_started_at: 2026-08-28T22:50:00+02:00
last_progress_at: 2026-08-28T23:18:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: review_repair_1_restack
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 1
stall_warnings: 0
owned_paths:
  - .github/scripts/test_track_a_current_client_package_parallel.py
  - .github/scripts/test_track_a_current_login_field6_runtime.py
  - .github/scripts/track_a_current_client_package_materialize.py
  - .github/scripts/track_a_current_client_package_acquire.sh
  - .github/scripts/track_a_current_login_field6_runtime.sh
  - .github/scripts/track_a_current_login_field6_runtime_secret_wrapper.sh
  - .github/workflows/track-a-current-client-package-materializer.yml
  - .github/workflows/track-a-current-login-field6-runtime.yml
  - docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md
  - docs/agents/evidence/OTC-20260828-current-login-field6-runtime/**
  - docs/superpowers/plans/2026-08-28-field6-materializer-repair.md
  - docs/superpowers/plans/2026-08-28-field6-v4-observation.md
modules_touched:
  - track-a-ephemeral-runtime-research
depends_on:
  - merged PR #752 exact-current field6 scalar-owner promotion
  - merged PR #754 exact-current client fence
  - merged PR #758 runtime observation implementation
  - merged PR #762 one-shot V1 live admission
  - failed pre-action run 33195339335 / job 98930921032
  - merged PR #764 exact-current package reacquisition repair
  - merged PR #768 one-shot V2 live admission
  - failed pre-action V2 run 33200939531 / job 98949936038
  - merged PR #769 direct task-owned package source repair
  - merged PR #771 one-shot V3 live admission
  - cancelled pre-action V3 run 33202129157 / job 98953921602
  - merged PR #775 bounded exact-current package materialization repair
  - merged PR #780 canonical identity reconciliation retry closeout
blocks:
  - OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE
---

# Objective

Recover the exact current public scalar carried in `edx` when the official Linux Tibia client enters the statically proven `GameclientMessageLogin` producer at `PIE + 0xe25620`, then promote that scalar as the only admissible Track B field6 input.

# Terminal V3 result

Exact owner trigger comment `5456592899` created run `33202129157`, job `98953921602`, against trusted main `32146659213cba71910cbe8d46aa4c2f6ded607c`. Its exact consumed V3 trigger body is intentionally omitted from this **active task**; immutable terminal evidence records it. The earlier locator `5456601015` is invalid because GitHub live state returns `404 Not Found`. WARP/SOCKS setup passed, but serial full-package materialization exceeded the job-level 18-minute deadline and GitHub cancelled the job before authorization consumption, credential exposure, official-client execution, or login.

```text
TRACK_A_FIELD6_PACKAGE_WARP=PASS attempt=1
TRACK_A_FIELD6_PACKAGE_CLEANUP=PASS
physical_action_count=0
login_submit_count=0
FIELD6_VALUE=UNKNOWN
```

V1, V2, and V3 triggers are consumed historical evidence and must never be rerun or replayed. Terminal evidence is `docs/agents/evidence/OTC-20260828-current-login-field6-runtime/20260828-v3-terminal-pre-action-timeout.md`.

# Merged materializer repair

PR #775 squash-merged as `5e9293f78e1757eafb88ca0b21cec8bf3d1d246a`. It replaces cumulative serial package acquisition with bounded deterministic concurrency while preserving complete official package materialization, every packed/unpacked size/hash check, the exact client fence, task-owned WARP/SOCKS, non-execution, atomic publication, and fail-closed cleanup. The existing 18-minute live deadline remains unchanged.

# Fresh V4 static-generation boundary

Protected `main@72565873d89f0e626a0be9397d5d913dc164c0d1` is the verified fresh base. It includes merged PR #782 (`fix(track-a): bind read-only admission to current exact target`) and PR #784 (`fix(track-a): normalize canonical Docker container identity`). Both changed only the independent gameWindowState contract/workflow/task and do not overlap this field6 PR's four paths. PR #780 had already returned the separate canonical-recovery task to `runtime_access: none`. Draft PR #773 and intermediate checkpoint PR #781 were closed unmerged as superseded; their durable terminal facts are preserved here and by merged PR #775.

This V4 generation branch remains strictly static-safe:

```yaml
runtime_access: none
mutation_authorized: false
credentials_allowed: false
login_allowed: false
physical_action_budget: 0
physical_action_count: 0
```

No V4 admission comment or exact V4 trigger has been created. The PR event cannot run the live observer; its live job is required to be `skipped`.

# V4 generation TDD evidence

## Generation RED

Exact RED head `1d34ef0bbe081573769e2e5a275e222036dd8204` changed only the static contract to require the new exact trigger generation and reject executable V3 while leaving the workflow on V3.

Hosted run/job:

```text
run=33210889241
contract_job=98983552850
live_job=98983553990
live_job_conclusion=skipped
```

The first relevant error was exactly:

```text
FIELD6_RUNTIME_CONTRACT_RED: .github/workflows/track-a-current-login-field6-runtime.yml missing ['AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 once=true']
```

This falsifies the old generation without client execution, credentials, login, or runtime mutation.

## Generation GREEN

Minimal implementation head `d043245995c1bd12817e01e55b8e563a6180eb0d` changes only the two executable workflow literals from V3 to exact V4:

```text
AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 once=true
```

Exact-head results:

```text
Track A current login field6 runtime observation  run 33210959567  success
Track A current client package materializer       run 33210959460  success
Track A agent runtime governance                  run 33210959476  success
CI                                                 run 33210959885  success
```

The 18-minute live deadline, exact package/client fence, materializer, runtime helper, secret wrapper, GDB parent observer, scalar schema, upload and cleanup boundaries are unchanged. The static contract also rejects any executable V3 trigger literal in the **current workflow**.

# Historical V3 rerun revocation guard

Independent exact-head Codex review of `894c8334d7c5e203848c2cf32dd68a0f1af4db4b` identified a P1: the cancelled historical V3 run stopped before its authorization-consumption marker, and a GitHub rerun would execute the original V3 workflow/event while its checkout step reads current `main`. If a later V4 admission reused generic live fields **and** the active task retained the old exact V3 trigger literal, that historical rerun could pass the old workflow's own task grep and create an unintended extra login.

The repair uses the old workflow's existing fail-closed generation check against it: the current active task permanently omits the exact V3 trigger literal, while the current V4 contract now requires that omission. Therefore a historical V3 rerun cannot satisfy its own `grep` against current `main`, regardless of whether a later V4 admission sets generic `ephemeral_isolated`/login fields.

## Review-repair RED

Exact RED head `a72a8c954504020ac52024a95aee3f4fef2d1a06` added only the current-task generation contract while deliberately leaving the stale V3 literal in this task.

```text
run=33211602343
contract_job=98985865455
live_job=98985866668
live_job_conclusion=skipped
```

The first relevant failure was exactly:

```text
FIELD6_RUNTIME_CONTRACT_RED: current task must omit consumed V3 trigger literal to block historical reruns
```

This reproduces the review finding without executing any client or live login.

## Review-repair GREEN invariant

Current task text now contains exact V4 admission text:

```text
AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 once=true
```

and intentionally contains **no exact V3 trigger literal**. `.github/scripts/test_track_a_current_login_field6_runtime.py` enforces both invariants. Because the historical V3 workflow itself greps the active task for its old exact literal after checking out current `main`, any rerun is refused before package materialization, authorization consumption, credential use, client execution, or login.

Focused GREEN on pre-restack repair head `10d4de845bc5baaf8bf1566c4955393237372e5a`:

```text
Track A current login field6 runtime observation  run 33211701909  success
  contract job 98986196785  success
  live job     98986198371  skipped
Track A current client package materializer       run 33211701877  success
Track A agent runtime governance                  run 33211701795  success
```

# Exact client and observer locator

The last promoted fence is only a locator until the V4 live preflight freshly verifies it:

- version `15.32.75d4a0`;
- unpacked size `52105824`;
- unpacked SHA-256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`;
- packed `bin/client` SHA-256 `075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f`;
- producer entry `0xe25620`;
- authoritative scalar `FIELD6_VALUE=UNKNOWN`.

Any current-fence movement must fail closed before login and requires fresh exact-current producer binding. No scalar may be guessed.

# V4 plan

Implementation and validation steps are frozen in `docs/superpowers/plans/2026-08-28-field6-v4-observation.md`. The static generation PR changes only the exact trigger generation/contract plus this task/plan; it does not touch secrets, runtime helper, materializer implementation, Track B, timeout, artifact schema, or live admission fields.

# Next action

Clean-restack PR #783 into one commit on `main@72565873d89f0e626a0be9397d5d913dc164c0d1`, rerun exact-head field6/materializer/governance/CI checks, obtain a fresh independent exact-head review with zero material findings, then squash-merge. Only a later separate docs-only V4 admission may set `runtime_access: ephemeral_isolated`; no V4 live trigger is legal from this PR.
