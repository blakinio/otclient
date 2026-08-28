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
branch: docs/OTC-20260828-field6-runtime-v2-admission
base_branch: main
base_main: 658715b3709b0290cdbb43fe44fce03ce5ef7060
created: 2026-08-28T19:00:00+02:00
updated: 2026-08-28T20:45:00+02:00
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
live_runtime_authorization_source: PR_758_COMMENT_5456414584
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
  - PR #758 owner V2 admission comment 5456414584
blocks:
  - OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE
---

# Objective

Recover the exact current public scalar value carried in `edx` when official Linux Tibia enters the statically proven `GameclientMessageLogin` producer at `PIE + 0xe25620`, then promote that value as the only admissible Track B field6 input.

# V1 terminal pre-action evidence

The first admitted V1 execution trigger was PR #758 comment `5455709588`. Run `33195339335`, job `98930921032`, consumed that exact trigger but failed with:

```text
TRACK_A_FIELD6_RUNTIME_ERROR=exact_current_source_package_missing
```

That failure occurred before WARP, Xvfb, GDB, the official client, credential entry or login submission. The proven physical action count therefore remains exactly zero. Comment `5455709588` is consumed historical evidence and MUST NOT be replayed, reused, edited into a new trigger or treated as authority for V2.

# Trusted V2 repair boundary

Merged PR #764 is trusted on `main` at `658715b3709b0290cdbb43fe44fce03ce5ef7060`. It repairs only the pre-action exact-current package acquisition path:

- a task-owned WARP acquisition tunnel uses SOCKS port `25442`;
- the current public Linux package manifest and every declared package file are acquired through that tunnel;
- every packed size/hash and unpacked size/hash is verified;
- the exact `bin/client` fence is reasserted before runtime;
- downloaded Tibia package content is never executed by acquisition;
- acquisition WARP ownership is persisted across workflow shells and cleanup is ownership-checked and zombie-safe;
- the exact package preflight completes before a V2 execution trigger can be consumed;
- sanitized scalar evidence is validated and uploaded before final package cleanup.

The existing runtime observer remains separately task-owned. It uses display `:131` and runtime WARP SOCKS port `25441` under:

```text
/home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260828-current-login-field6-runtime/runs/$GITHUB_RUN_ID
```

It does not attach to any canonical or unrelated process and does not reuse a canonical Track A or Track B runtime. Canonical registration, leases, Gate A, generation rebind, Gate B and bootstrap remain `NOT_APPLICABLE` for this isolated task-owned sandbox.

# Exact source boundary

Only this exact official native Linux client is admitted:

- version `15.32.75d4a0`;
- unpacked size `52105824`;
- unpacked SHA-256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`;
- packed `bin/client` SHA-256 `075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f`;
- exact producer entry `0xe25620` promoted by merged PR #752;
- current authoritative pre-observation result `FIELD6_VALUE=UNKNOWN`.

If the current public client moves from any exact fence above, the admitted V2 run must fail closed before login rather than reinterpret or guess the producer input.

# V2 mutation and credential boundary

Owner admission is recorded by PR #758 comment `5456414584`:

```text
AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V2 admission=true previous_trigger=5455709588 previous_run=33195339335 physical_action_count=0 scope=one_login_scalar_only
```

This docs-only admission grants exactly one logical account-login form submission after all trusted-main and package preflight checks pass. It grants no relog, restart, character selection, character activation, world entry or gameplay. Network payload capture is forbidden.

The observer remains GDB-as-parent, never attach. ASLR remains enabled, the exact child PIE is resolved after `exec`, and the single breakpoint at `PIE + 0xe25620` retains only `uint32(edx)` plus bounded process/client identity. It may not retain stack bytes, packet payloads, credentials, process environment, unrelated registers or raw memory.

The protected credential wrapper removes the export attribute from `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD`, proves those names are absent from child-process environments, and keeps the values only as non-exported shell variables until the one login-form submit.

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

# V2 execution trigger

This live-admission PR MUST NOT start the official client. After this one-file admission is reviewed, GREEN and merged to fresh trusted `main`, live execution still requires a new top-level repository-owner comment on merged PR #758 whose body is exactly:

```text
AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V2 once=true
```

The workflow must reject any non-exact body or non-owner author. It records the new comment id once in task-owned persistent authorization state. The V1 trigger id is not reusable. Exact-current package materialization must finish successfully before the new V2 trigger is consumed or credentials are used.

# Completion

`FIELD6_VALUE=UNKNOWN` remains authoritative until one separately triggered trusted-main V2 run produces a sanitized scalar-only artifact with `FIELD6_VALUE_PROVEN=true`. This task completes only after that scalar is independently reviewed/promoted and then consumed by Track B without guessing.
