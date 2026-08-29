---
task_id: OTC-20260828-current-login-field6-runtime
status: ready
agent: ChatGPT
session_id: chatgpt-20260829-field6-v4-admission-v2
session_role: implementer
policy_version: 2
project_lane: otclient
lane: RUNTIME_RESEARCH
track_id: official-client-re
task_kind: reverse_engineering_runtime
phase: live_admission
branch: fix/OTC-20260829-field6-v4-admission-v2
base_branch: main
base_main: 0c9c4e1021b09eb0c2de6fe426ad0688e4539173
created: 2026-08-28T19:00:00+02:00
updated: 2026-08-29T17:29:00+02:00
risk: high
execution_class: synology_physical_runtime
execution_mode: github_actions_ephemeral_isolated
execution_reason: one fresh exact-current scalar-only V4 login observation after trusted static generation and historical-rerun revocation
persistent_session_role: canonical_runtime_owner
physical_e2e_required: true
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260828-current-login-field6-runtime
runtime_namespace: field6-runtime-ephemeral-OTC-20260828-v4-display131-port25441
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: true
credentials_allowed: true
login_allowed: true
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: true
process_control_authorized: true
network_payload_capture_allowed: false
physical_action_budget: 1
physical_action_count: 0
implementation_authorized: true
live_runtime_authorization_source: PR_758_COMMENT_5457904227
related_pr: 796
context_pressure: medium
context_growth: stable
context_score: 9
estimate_confidence: medium
decomposition_decision: phased
decomposition_reason: field6 proof remains one sequential evidence chain; Track B is a separate consumer phase after scalar promotion
validation_level: exact_head
last_completed_step: local admission/security/field6/boundary audit GREEN after #798; final one-commit restack ready for exact-head hosted validation
session_rotation_count: 1
heavy_validation_runs: 0
stale_takeover_count: 0
human_interruptions: 0
invocation_started_at: 2026-08-28T22:50:00+02:00
last_progress_at: 2026-08-29T17:29:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: v4_admission_v2_final_restack
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 1
stall_warnings: 0
owned_paths:
  - .github/scripts/test_track_a_current_client_package_parallel.py
  - .github/scripts/test_track_a_current_login_field6_runtime.py
  - .github/scripts/test_track_a_current_login_field6_security_contract.py
  - .github/scripts/audit_track_a_current_login_field6_admission.py
  - .github/scripts/track_a_current_client_package_materialize.py
  - .github/scripts/track_a_current_client_package_acquire.sh
  - .github/scripts/track_a_current_login_field6_runtime.sh
  - .github/scripts/track_a_current_login_field6_runtime_secret_wrapper.sh
  - .github/workflows/track-a-current-client-package-materializer.yml
  - .github/workflows/track-a-current-login-field6-runtime.yml
  - docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md
  - docs/agents/reports/OTC-20260829-field6-v4-admission-v2.md
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
  - merged PR #783 static V4 generation and historical-rerun guard
  - merged PR #785 non-overlapping gameWindowState ELF mapping-base repair
  - merged PR #795 self-hosted secret-runner boundary and independent audit
  - merged PR #798 reusable self-hosted boundary audit repair
  - PR #758 owner V4 admission comment 5457904227
blocks:
  - OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE
---

# Objective

Recover the exact current public scalar carried in `edx` when the official Linux Tibia client enters the statically proven `GameclientMessageLogin` producer at `PIE + 0xe25620`, then promote that scalar as the only admissible Track B field6 input.

# Terminal prior-generation evidence

The terminal V3 owner comment produced run `33202129157` / job `98953921602` against trusted main `32146659213cba71910cbe8d46aa4c2f6ded607c`. WARP/SOCKS setup passed, but the then-serial full-package materializer exceeded the job-level 18-minute deadline. Authorization consumption, credential exposure, official-client execution and login were skipped.

```text
TRACK_A_FIELD6_PACKAGE_WARP=PASS attempt=1
TRACK_A_FIELD6_PACKAGE_CLEANUP=PASS
physical_action_count=0
login_submit_count=0
FIELD6_VALUE=UNKNOWN
```

V1, V2 and V3 are consumed historical generations and must never be rerun or replayed. The exact consumed V3 trigger literal is intentionally absent from this active task so the historical V3 workflow cannot satisfy its own current-main generation grep. Immutable terminal evidence remains in `docs/agents/evidence/OTC-20260828-current-login-field6-runtime/20260828-v3-terminal-pre-action-timeout.md`.

# Trusted V4 implementation boundary

Materializer repair PR #775 is trusted as `5e9293f78e1757eafb88ca0b21cec8bf3d1d246a`. It uses bounded deterministic concurrency while retaining complete package verification, every packed/unpacked size/hash check, exact `bin/client` verification, task-owned WARP/SOCKS, no downloaded-content execution, atomic publication and fail-closed cleanup. The justified job deadline remains `18` minutes.

Static generation PR #783 is trusted on `main` as `0720ddc77affefc4206afc7e09da03b77dc8c26f`. It rotates the only executable current workflow trigger to V4 and adds a current-main generation contract that rejects the consumed V3 generation. Its final exact-head field6/materializer/governance/CI checks were GREEN, and independent exact-head Codex review reported no major issues after the P1 historical-rerun guard was repaired.

Protected `main@4c751870b5dcd51d5b984b78a4f06625306be961` is the fresh admission base. The intervening PR #785 changed only `.github/scripts/test_track_a_game_window_state_qualification.py` and `.github/scripts/track_a_game_window_state_qualification.py`; it does not overlap this field6 admission repair.

# Fresh V4 owner admission

A distinct repository-owner admission record exists on merged PR #758 as comment `5457904227`:

```text
AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 admission=true previous_generation=V3 previous_run=33202129157 previous_physical_action_count=0 scope=one_login_scalar_only physical_action_budget=1 relogin=false restart=false character_selection=false world_entry=false gameplay=false network_payload_capture=false
```

This text is deliberately **not** the exact live workflow trigger. It records authority for a later one-shot login only after this admission is independently reviewed, GREEN, clean-restacked and merged to fresh trusted `main`.

Merged PR #795 (`ed0b048f72b93613ea87a177ce6c5a3ea9bfa92b`) is now the trusted self-hosted secret-runner boundary. V4 execution additionally requires an offline-by-default fresh one-job runner with disposable work/state, no restored historical runner state, no Docker socket/privileged host access, exact queued-job uniqueness, and post-job destruction. If that clean-runner provenance cannot be proven, credentials/login remain forbidden and the exact V4 trigger MUST NOT be posted.

Because that fresh runner intentionally does not preserve the historical `COMMENT_ID.used` file, the live workflow rejects any `GITHUB_RUN_ATTEMPT != 1` in the first trusted-main admission step, before authorization consumption, credential exposure, client execution, or physical action. A GitHub rerun therefore fails before the one-shot boundary can be reused.

The routing refresh now explicitly classifies the physical step as `synology_physical_runtime`, records `persistent_session_role: canonical_runtime_owner`, and marks `physical_e2e_required: true` as required by the hybrid routing contract. Fresh active-task searches immediately before this admission found no other active `canonical_recovery`, `ephemeral_isolated`, or `mutation_authorized: true` task. This V4 runtime is isolated to its task/run-owned state, Xvfb display `:131`, runtime WARP SOCKS port `25441`, and package-acquisition WARP SOCKS port `25442`; every collision fails closed.

# Exact client and observer boundary

The current trusted workflow will freshly verify before login:

- version `15.32.75d4a0`;
- unpacked size `52105824`;
- unpacked SHA-256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`;
- packed `bin/client` SHA-256 `075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f`;
- producer entry `0xe25620`;
- authoritative pre-observation scalar `FIELD6_VALUE=UNKNOWN`.

These values remain locators until the V4 live preflight verifies the current official package. Any fence movement fails closed before authorization consumption, credentials or login and requires a fresh exact-current producer binding. No scalar may be guessed.

The observer remains GDB as parent, never attach. ASLR remains enabled; the child PIE is resolved after `exec`; the only scalar capture is `uint32(edx)` at `PIE + 0xe25620`. Stack bytes, packet payloads, credentials, process environment, unrelated registers and arbitrary/raw process memory may not be retained.

# V4 mutation and credential boundary

This admission grants exactly one logical account-login form submission after all trusted-main and exact-current package preflight gates pass. It grants no relog, restart, character selection, character activation, world entry or gameplay. Network payload capture is forbidden.

The credential wrapper remains the only path that may receive `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD`; it removes their export attribute and proves those names are absent from child-process environments. The runtime helper now sends both login strings to `xdotool type --file -` through stdin, so neither email nor password is present in the xdotool process argv. Credentials and process environment are not retained in evidence.

The only admissible successful artifact must prove:

```text
TRACK_A_FIELD6_RUNTIME_CAPTURED=true
FIELD6_VALUE=<uint32>
FIELD6_VALUE_PROVEN=true
login_submit_count=1
character_selection_performed=false
world_entry_performed=false
gameplay_performed=false
network_payload_capture_performed=false
credentials_retained=false
packet_payloads_retained=false
process_environment_retained=false
raw_memory_retained=false
```

# V4 execution trigger

This admission change MUST NOT start the official client. After this PR is independently reviewed, GREEN and squash-merged to a freshly revalidated `main`, execution still requires one new top-level repository-owner comment on merged PR #758 whose body is exactly:

```text
AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 once=true
```

That exact comment is the single V4 execution trigger and becomes consumed historical evidence immediately after use. It must never be replayed or rerun. Package materialization must complete before its one-shot authorization marker is consumed and before credentials or login are reachable.

# Completion

`FIELD6_VALUE=UNKNOWN` remains authoritative until one trusted-main V4 run produces sanitized scalar-only evidence with `FIELD6_VALUE_PROVEN=true`. After the run, a separate repository-only evidence PR must return this task to `runtime_access: none`, disarm credentials/login/mutation authority, preserve the terminal physical action count and promote only sanitized scalar evidence. Track B may consume field6 only after that promotion reaches trusted `main`.

# Next action

Verify exact-head security contract, field6 contract, materializer, governance, independent admission audit and CI; clean-restack and squash-merge on fresh main. Then prove/provision the #795 clean one-job runner boundary. Only after that host-level gate is freshly proven may exactly one distinct V4 execution trigger be created on PR #758.
