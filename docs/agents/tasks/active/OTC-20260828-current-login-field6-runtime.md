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
branch: docs/OTC-20260828-field6-v4-continuation-checkpoint
base_branch: main
base_main: b61f70e73575582d10af3789d2cfb7cb01087b6d
created: 2026-08-28T19:00:00+02:00
updated: 2026-08-28T23:00:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
execution_reason: persist exact post-repair continuation after separate canonical recovery authority was released
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
related_pr: 775
continuation_checkpoint_pr: 781
context_pressure: medium
context_growth: stable
context_score: 9
estimate_confidence: medium
decomposition_decision: phased
decomposition_reason: field6 proof is one sequential evidence chain; Track B remains a separate consumer phase after promotion
validation_level: exact_head
last_completed_step: closed stale V3 checkpoint PR #773 and reached exact-head GREEN on continuation checkpoint before final refresh
session_rotation_count: 1
heavy_validation_runs: 0
stale_takeover_count: 0
human_interruptions: 0
invocation_started_at: 2026-08-28T22:50:00+02:00
last_progress_at: 2026-08-28T23:00:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
owned_paths:
  - .github/scripts/test_track_a_current_client_package_parallel.py
  - .github/scripts/track_a_current_client_package_materialize.py
  - .github/scripts/track_a_current_client_package_acquire.sh
  - .github/scripts/track_a_current_login_field6_runtime.sh
  - .github/scripts/track_a_current_login_field6_runtime_secret_wrapper.sh
  - .github/workflows/track-a-current-client-package-materializer.yml
  - .github/workflows/track-a-current-login-field6-runtime.yml
  - docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md
  - docs/agents/evidence/OTC-20260828-current-login-field6-runtime/**
  - docs/superpowers/plans/2026-08-28-field6-materializer-repair.md
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

Exact existing owner trigger comment `5456592899`, body `AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V3 once=true`, created run `33202129157`, job `98953921602`, against trusted main `32146659213cba71910cbe8d46aa4c2f6ded607c`. The earlier locator `5456601015` is rejected because GitHub live state returns `404 Not Found`. WARP/SOCKS setup passed, but full package materialization exceeded the job-level 18-minute deadline and GitHub cancelled the job before authorization consumption, credential exposure, official-client execution, or login.

```text
TRACK_A_FIELD6_PACKAGE_WARP=PASS attempt=1
TRACK_A_FIELD6_PACKAGE_CLEANUP=PASS
physical_action_count=0
login_submit_count=0
FIELD6_VALUE=UNKNOWN
```

V1, V2, and V3 triggers are consumed historical evidence and must not be rerun or replayed. Detailed terminal evidence is `docs/agents/evidence/OTC-20260828-current-login-field6-runtime/20260828-v3-terminal-pre-action-timeout.md`.

# Merged materializer repair

PR #775 was squash-merged as `5e9293f78e1757eafb88ca0b21cec8bf3d1d246a`. It replaces cumulative serial package acquisition with bounded deterministic concurrency while preserving:

- complete official package materialization;
- every packed size/hash and unpacked size/hash check;
- the exact `bin/client` version, size, packed hash, and unpacked hash fence;
- task/run-owned WARP/SOCKS routing and storage;
- no execution of downloaded Tibia content in preflight;
- no global or legacy CipSoft package fallback;
- fail-closed partial/cancelled cleanup.

The existing 18-minute live observer deadline remains unchanged; the repair addressed the proven cumulative serial bottleneck rather than masking it with an arbitrary timeout increase.

# Fresh continuation checkpoint — 2026-08-28 23:00 CEST

GitHub live state was reconstructed and this checkpoint is based on protected `main@b61f70e73575582d10af3789d2cfb7cb01087b6d`.

Repository/runtime facts at this checkpoint:

- PR #778 is merged and had returned the first exact-current identity reconciliation authority to `runtime_access: none`.
- A later memory-free gameWindowState preflight observed fresh runtime identity drift, so PR #779 re-admitted only the separate task `OTC-20260828-canonical-client-fence-reconciliation` with `runtime_access: canonical_recovery`.
- That separate metadata-only recovery run `33210019599` completed `success` on exact `main@fd7a47308581dceda6fd6aa3613f0614a816d150`.
- PR #780 merged as `main@b61f70e73575582d10af3789d2cfb7cb01087b6d` and returned that separate recovery task to `runtime_access: none`, `runtime_owner_task: NOT_APPLICABLE`, `physical_action_budget: 0`.
- No client mutation, process-memory observation, GUI/input, credentials, login, character selection, gameplay, or payload capture was authorized or performed by that recovery path.
- This field6 task remains `runtime_access: none`, `physical_action_budget: 0`, `physical_action_count: 0`. No V4 admission or V4 trigger has been created by this checkpoint.
- Draft PR #773 was closed unmerged as superseded. Its V3-in-progress snapshot is replaced by terminal V3 evidence already merged through PR #775; no unique runtime/code change was lost.

This checkpoint did not modify or claim the separate canonical-recovery task.

# Exact client and observer locator

The last promoted fence remains a locator pending fresh V4 verification:

- version `15.32.75d4a0`;
- unpacked size `52105824`;
- unpacked SHA-256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`;
- packed `bin/client` SHA-256 `075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f`;
- producer entry `0xe25620`;
- authoritative scalar `FIELD6_VALUE=UNKNOWN`.

Any current-fence movement must fail closed and requires a new exact-current binding. No value may be guessed.

# Validation before merge

Exact-head checks are required after this final checkpoint refresh: field6 runtime static contract, package materializer contract, Track A governance, and CI. Independent documentation review must report zero material findings. This PR performs no live action.

# Next action

After this checkpoint PR is exact-head GREEN, independently reviewed, and merged, prepare the separate static-safe V4 observer-generation PR from fresh `main`; do not issue any live V4 trigger from this checkpoint branch.
