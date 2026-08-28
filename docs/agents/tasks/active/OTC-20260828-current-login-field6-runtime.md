---
task_id: OTC-20260828-current-login-field6-runtime
status: live_authorized_pending_trigger
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME_RESEARCH
track_id: official-client-re
task_kind: reverse_engineering_runtime
phase: live_admission
branch: docs/OTC-20260828-field6-runtime-v3-admission
base_branch: main
base_main: eb316cd4ce4b9926ade8b170babe2b3d7053b531
created: 2026-08-28T19:00:00+02:00
updated: 2026-08-28T21:04:00+02:00
risk: high
execution_class: self_hosted
execution_mode: github_actions_ephemeral_isolated
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260828-current-login-field6-runtime
runtime_namespace: field6-runtime-ephemeral-OTC-20260828-display131-port25441
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
live_runtime_authorization_source: PR_758_COMMENT_5456573590
related_pr: 758
owned_paths:
  - .github/scripts/test_track_a_current_login_field6_runtime.py
  - .github/scripts/track_a_current_client_package_materialize.py
  - .github/scripts/track_a_current_client_package_acquire.sh
  - .github/scripts/track_a_current_login_field6_runtime.sh
  - .github/scripts/track_a_current_login_field6_runtime_secret_wrapper.sh
  - .github/workflows/track-a-current-login-field6-runtime.yml
  - docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md
  - docs/agents/evidence/OTC-20260828-current-login-field6-runtime/**
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
  - PR #758 owner V3 admission comment 5456573590
blocks:
  - OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE
---

# Objective

Recover the exact current public scalar value carried in `edx` when official Linux Tibia enters the statically proven `GameclientMessageLogin` producer at `PIE + 0xe25620`, then promote that value as the only admissible Track B field6 input.

# Prior terminal pre-action evidence

V1 trigger comment `5455709588` produced run `33195339335` / job `98930921032` and failed at `exact_current_source_package_missing` before WARP, Xvfb, GDB, client, credentials or login. Its proven physical action count is zero and that trigger remains consumed historical evidence.

V2 trigger comment `5456454545` produced run `33200939531` / job `98949936038`. Trusted-main admission passed, but package preflight failed with `TRACK_A_FIELD6_PACKAGE_ERROR=legacy_source_collision`. Authorization consumption, protected credential use, runtime capture and login were skipped, and `physical_action_count` remained zero. That V2 trigger is terminal preflight evidence and MUST NOT be rerun or replayed.

# Trusted V3 repair boundary

Merged PR #769 is trusted on `main` at `eb316cd4ce4b9926ade8b170babe2b3d7053b531`. It removes the global legacy CipSoft package path from the runtime handoff. The only admissible package source is now the task/run-owned materialization:

```text
/home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260828-current-login-field6-runtime/package-acquisition/$GITHUB_RUN_ID/current-package
```

The acquisition preflight must:

- create its own WARP tunnel on SOCKS port `25442`;
- fetch the current public Linux package manifest and every declared package file through that tunnel;
- verify every packed size/hash and unpacked size/hash;
- reassert the exact `bin/client` fence;
- execute no downloaded Tibia content;
- stop its WARP process before runtime begins;
- leave all global/legacy CipSoft package locations untouched.

The runtime helper resolves only the task-owned package path above, verifies its exact client fence again, copies it into its isolated runtime HOME and emits `TRACK_A_FIELD6_DIRECT_PACKAGE_SOURCE=PASS` before continuing.

# Exact client and observer boundary

Only this exact official native Linux client is admitted:

- version `15.32.75d4a0`;
- unpacked size `52105824`;
- unpacked SHA-256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`;
- packed `bin/client` SHA-256 `075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f`;
- exact producer entry `0xe25620`;
- authoritative pre-observation result `FIELD6_VALUE=UNKNOWN`.

If any exact-current fence moves, V3 must fail closed before login rather than reinterpret or guess the scalar.

The observer remains GDB-as-parent, never attach. ASLR remains enabled, the exact child PIE is resolved after `exec`, and the single breakpoint at `PIE + 0xe25620` retains only `uint32(edx)` plus bounded client/process identity. Stack bytes, packet payloads, credentials, process environment, unrelated registers and raw memory may not be retained.

# V3 mutation and credential boundary

Owner admission is recorded by PR #758 comment `5456573590`:

```text
AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V3 admission=true previous_trigger=5456454545 previous_run=33200939531 physical_action_count=0 scope=one_login_scalar_only
```

This docs-only admission grants exactly one logical account-login form submission after all trusted-main and exact-current package preflight checks pass. It grants no relog, restart, character selection, character activation, world entry or gameplay. Network payload capture is forbidden.

The credential wrapper remains the only code path that may receive `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD`. It removes their export attribute, proves those names are absent from child-process environments and retains neither credentials nor environment data in the artifact.

The admitted outcome must preserve:

```text
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

# V3 execution trigger

This admission change MUST NOT start the official client. After this one-file docs admission is independently reviewed, GREEN and merged to fresh trusted `main`, execution still requires a new top-level repository-owner comment on merged PR #758 whose body is exactly:

```text
AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V3 once=true
```

The workflow rejects any non-exact body or non-owner author. Exact-current package materialization must complete successfully before that V3 trigger is consumed, credentials are exposed to the wrapper or a login is submitted.

# Completion

`FIELD6_VALUE=UNKNOWN` remains authoritative until one separately triggered trusted-main V3 run produces a sanitized scalar-only artifact with `FIELD6_VALUE_PROVEN=true`. This task completes only after that scalar is independently reviewed/promoted and consumed by Track B without guessing.
