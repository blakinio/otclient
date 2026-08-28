---
task_id: OTC-20260828-current-login-field6-runtime
status: repair_pending_merge
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME_RESEARCH
track_id: official-client-re
task_kind: reverse_engineering_runtime
phase: implementation_repair
branch: fix/OTC-20260828-field6-direct-package-source
base_branch: main
base_main: 763806fecc7a0cc1b56fe785dfcadb62ad2dfb9a
created: 2026-08-28T19:00:00+02:00
updated: 2026-08-28T21:01:00+02:00
risk: high
execution_class: self_hosted
execution_mode: github_actions_ephemeral_isolated
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
related_pr: 769
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
blocks:
  - OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE
---

# Objective

Recover the exact current public scalar value carried in `edx` when official Linux Tibia enters the statically proven `GameclientMessageLogin` producer at `PIE + 0xe25620`, then promote that value as the only admissible Track B field6 input.

# Terminal pre-action evidence

V1 trigger comment `5455709588` produced run `33195339335` / job `98930921032` and failed at `exact_current_source_package_missing` before WARP, Xvfb, GDB, client, credentials or login. Its proven physical action count is zero and that trigger remains consumed historical evidence.

V2 trigger comment `5456454545` produced run `33200939531` / job `98949936038`. Trusted-main admission passed, but exact-current package preflight failed with:

```text
TRACK_A_FIELD6_PACKAGE_ERROR=legacy_source_collision
```

The workflow then skipped `Consume exact owner authorization once`, `Capture field6 with protected login inputs`, scalar validation and artifact upload. Cleanup also failed closed with `cleanup_source_ownership_refused` because the same pre-existing legacy path was intentionally not owned by this task. No official client process, credential entry or login submission occurred. Therefore `physical_action_count` remains exactly `0`.

Comment `5456454545` is treated as terminal preflight evidence and MUST NOT be rerun or replayed even though its authorization-consumption step was skipped.

# Repair boundary

This repair removes the legacy package path from the acquisition/runtime handoff entirely. The exact-current materializer remains unchanged in purpose: it retrieves every current public Linux package file through task-owned WARP, verifies every packed and unpacked manifest size/hash, reasserts the exact `bin/client` fence, and executes no downloaded Tibia content.

The only admissible runtime source after repair is the deterministic task/run-owned path:

```text
/home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260828-current-login-field6-runtime/package-acquisition/$GITHUB_RUN_ID/current-package
```

The runtime helper must resolve that exact path directly and independently verify its exact client fence before copying it into its own isolated HOME. It must not read, replace, symlink, delete or otherwise depend on either global legacy package path:

```text
/home/runner/_work/_otclient_tibia_re_state/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia
/work/_otclient_tibia_re_state/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia
```

Any pre-existing content at those locations is outside this task's ownership and is intentionally left untouched.

# Exact source boundary

Only this exact official native Linux client remains admissible:

- version `15.32.75d4a0`;
- unpacked size `52105824`;
- unpacked SHA-256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`;
- packed `bin/client` SHA-256 `075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f`;
- exact producer entry `0xe25620`;
- authoritative result remains `FIELD6_VALUE=UNKNOWN`.

# Runtime boundary preserved

The runtime observer remains GDB-as-parent, never attach. ASLR remains enabled. The exact child PIE is resolved after `exec`; the single breakpoint is `PIE + 0xe25620`; only `uint32(edx)` plus bounded client/process identity may be retained. Character selection, world entry, gameplay and network payload capture remain forbidden.

This repair task is deliberately `runtime_access: none`. It cannot receive credentials, start the official client or perform login. The next executable generation is V3 and may be encoded as:

```text
AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V3 once=true
```

That workflow string is not authority by itself. After the repair is independently reviewed, GREEN and merged to fresh trusted `main`, a separate docs-only V3 live admission and a new distinct repository-owner authorization/trigger are required. V1 and V2 comments are not reusable.

# Completion

`FIELD6_VALUE=UNKNOWN` remains authoritative until a separately admitted trusted-main runtime produces sanitized evidence with `FIELD6_VALUE_PROVEN=true`. The proven scalar must then be independently reviewed/promoted before Track B may consume it.
