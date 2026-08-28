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
branch: fix/OTC-20260828-field6-current-client-materialize
base_branch: main
base_main: 79279315df2975e79558a15192e4c5c87b90194a
created: 2026-08-28T19:00:00+02:00
updated: 2026-08-28T20:39:00+02:00
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
related_pr: 764
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
blocks:
  - OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE
---

# Objective

Recover the exact current public scalar value carried in `edx` when official Linux Tibia enters the statically proven `GameclientMessageLogin` producer at `PIE + 0xe25620`, then promote that value as the only admissible Track B field6 input.

# Repair checkpoint

The first admitted V1 execution trigger was comment `5455709588`. Run `33195339335`, job `98930921032`, consumed that trigger but failed with:

```text
TRACK_A_FIELD6_RUNTIME_ERROR=exact_current_source_package_missing
```

The failure occurred before WARP, Xvfb, GDB, the official client, credential entry, or login submission. Therefore the observed physical action count remains exactly zero. The consumed V1 trigger is historical evidence only and MUST NOT be replayed or copied into a new execution admission.

This task is deliberately returned to `runtime_access: none` while PR #764 repairs only the pre-action package acquisition path. No runtime mutation, credential use, login, GUI input, process control, character selection, world entry, gameplay, or packet capture is authorized by this repair checkpoint.

# Exact source boundary

Only this exact official native Linux client remains admissible:

- version `15.32.75d4a0`;
- unpacked size `52105824`;
- unpacked SHA-256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`;
- packed `bin/client` SHA-256 `075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f`;
- exact producer entry `0xe25620` promoted by merged PR #752;
- current authoritative pre-observation result `FIELD6_VALUE=UNKNOWN`.

PR #764 adds `.github/scripts/track_a_current_client_package_materialize.py` and `.github/scripts/track_a_current_client_package_acquire.sh`. The acquisition preflight must use a task-owned WARP process, retrieve the current public package manifest and every declared file, verify every packed size/hash and unpacked size/hash, reassert the exact `bin/client` fence, and never execute downloaded Tibia package content during acquisition.

The acquisition root is task/run-owned. The legacy package path used by the already-reviewed runtime helper may only be a temporary symlink to that exact task-owned materialization and is removed by an ownership-checked cleanup step. The preflight WARP process is stopped before the runtime helper starts its separately owned login WARP process.

# Preserved runtime observer boundary

The merged runtime observer remains unchanged in purpose and authority:

- GDB is the parent of the exact official client, never an attaching debugger;
- ASLR remains enabled;
- the exact child PIE is resolved after `exec`;
- the single breakpoint is `PIE + 0xe25620`;
- only `uint32(edx)` is retained;
- no stack bytes, packet payloads, credentials, process environment, unrelated registers, raw memory, character selection or gameplay may be retained or performed.

The protected credential wrapper remains the only path that may receive login secrets after a future live admission. It removes the export attribute from the two login variables and proves they are absent from child-process environments before any runtime preflight child is launched.

# V2 execution gate

PR #764 may encode the next exact trigger string:

```text
AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V2 once=true
```

That string in workflow code is not an authorization by itself. While this task remains `runtime_access: none`, the trusted-main live-admission step must fail closed before package acquisition, authorization consumption, client start, or login.

After PR #764 is independently reviewed, GREEN and merged onto fresh trusted `main`, a separate docs-only live-admission transition is required. It must explicitly cite the V1 pre-action failure and `physical_action_count: 0`, restore only the bounded `ephemeral_isolated` one-login authority, and bind a new owner authorization source to V2. Only after that admission is merged may a new distinct repository-owner trigger comment be posted.

# Completion

This task is complete only when one separately admitted trusted-main V2 run produces a sanitized scalar-only artifact with `FIELD6_VALUE_PROVEN=true`, that evidence is independently reviewed/promoted, and the proven scalar is consumed by Track B without guessing. Until then, `FIELD6_VALUE=UNKNOWN` remains authoritative.
