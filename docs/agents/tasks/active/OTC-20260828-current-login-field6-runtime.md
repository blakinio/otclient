---
task_id: OTC-20260828-current-login-field6-runtime
status: implementing
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME_RESEARCH
track_id: official-client-re
task_kind: reverse_engineering_runtime
phase: materializer_repair
branch: fix/OTC-20260828-field6-materializer-parallel
base_branch: main
base_main: 7edf5bc44c08b762be7ac34104e840b391747fd6
created: 2026-08-28T19:00:00+02:00
updated: 2026-08-28T22:09:00+02:00
risk: high
execution_class: github_hosted
execution_mode: github_actions_static
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

# Current static-safe repair

The exact V3 materializer processes manifest rows serially. PR #775 adds bounded deterministic parallel file acquisition while preserving:

- complete official package materialization;
- every packed size/hash and unpacked size/hash check;
- the exact `bin/client` version, size, packed hash, and unpacked hash fence;
- task/run-owned WARP/SOCKS routing and storage;
- no execution of downloaded Tibia content in preflight;
- no global or legacy CipSoft package fallback;
- fail-closed partial/cancelled cleanup.

This task is now `runtime_access: none`. This repair has no credentials, login, GUI/input, process-control, character selection, world entry, gameplay, or network-payload authority.

# Exact client and observer locator

The last promoted fence remains a locator pending fresh V4 verification:

- version `15.32.75d4a0`;
- unpacked size `52105824`;
- unpacked SHA-256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`;
- packed `bin/client` SHA-256 `075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f`;
- producer entry `0xe25620`;
- authoritative scalar `FIELD6_VALUE=UNKNOWN`.

Any current-fence movement must fail closed and requires a new exact-current binding. No value may be guessed.

# Next action

Complete RED/GREEN/REFACTOR and squash-merge the static repair after exact-head hosted checks and independent review. Then create a separate docs-only V4 admission with `physical_action_budget: 1`, `physical_action_count: 0`, no relog/restart/character selection/gameplay/payload capture, and a new distinct owner trigger. The repair branch itself must never execute a live login.
