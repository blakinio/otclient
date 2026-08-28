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
branch: work/OTC-20260828-current-login-field6-runtime
base_branch: main
base_main: 87a8351f6f6d3faae9869a119f165fc30882ab53
created: 2026-08-28T19:00:00+02:00
updated: 2026-08-28T19:33:00+02:00
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
live_runtime_authorization_source: PR_758_COMMENT_5455680140
related_pr: 758
owned_paths:
  - .github/scripts/test_track_a_current_login_field6_runtime.py
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
  - PR #758 owner authorization comment 5455680140
blocks:
  - OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE
---

# Objective

Recover the exact current public scalar value carried in `edx` when official Linux Tibia enters the statically proven `GameclientMessageLogin` producer at `PIE + 0xe25620`, then promote that value as the only admissible Track B field6 input.

# Live admission

The repository-side observer implementation is trusted on `main` at merge `87a8351f6f6d3faae9869a119f165fc30882ab53`. The owner explicitly authorized one separately admitted isolated login experiment in PR #758 comment `5455680140`.

This checkpoint reclassifies only this task to `ephemeral_isolated`. It does not grant canonical authority and it does not touch, attach to, reuse, signal, stop, inject into, or clean any canonical Track A or Track B runtime. Canonical registration, lease, Gate A, Gate B, rebind and bootstrap are `NOT_APPLICABLE` by design for this task-owned sandbox.

The namespace is task-owned and non-canonical:

```text
state root: /home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260828-current-login-field6-runtime/runs/$GITHUB_RUN_ID
display: :131
WARP SOCKS port: 25441
client/process ownership: OTCLIENT_TIBIA_RE_TASK=OTC-20260828-current-login-field6-runtime + exact run id + role
```

`target_uniqueness: PROVEN` refers to the reviewed task-owned namespace selection and fail-closed ownership model. The trusted helper still refuses execution before login if the run root, display, WARP port, exact client fence, toolroot, window, tracer-child identity, or ownership markers are not uniquely valid at runtime.

# Exact source boundary

Only this exact official native Linux client is admitted:

- version `15.32.75d4a0`;
- size `52105824`;
- SHA-256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`;
- exact producer entry `0xe25620` promoted by merged PR #752;
- current authoritative pre-observation result `FIELD6_VALUE=UNKNOWN`.

The historical closed/unmerged PR #303 remains discovery input only for the Yama-safe parent-GDB shape. None of its old client hashes, displays, ports, branches, tasks or runtime records are authority.

# Mutation and credential boundary

The live physical-action budget is exactly one logical account-login form submission. No relog or restart is authorized. Character selection, character activation, world entry and gameplay are explicitly forbidden.

The observer is GDB-as-parent, never attach. ASLR remains enabled, the exact child PIE is resolved after `exec`, and the one breakpoint at `PIE + 0xe25620` retains only `uint32(edx)`. It may not retain stack bytes, packet payloads, credentials, process environment, unrelated registers, raw memory or unrelated process state.

The protected-step credential environment is scrubbed before any helper preflight child process: the task-owned wrapper removes the export attribute from `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD`, proves those names are absent from `env`, and only then sources the helper in the same shell. The values remain non-exported shell variables solely until the one login-form submit.

The admitted outcome must preserve:

```text
login_submit_count=1
character_selection_performed=false
world_entry_performed=false
gameplay_performed=false
network_payload_capture_performed=false
```

# Execution trigger

This live admission PR itself MUST NOT start the official client. After this admission is reviewed, GREEN and merged to trusted `main`, live execution still requires a new top-level owner comment on merged PR #758 whose body is exactly:

```text
AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V1 once=true
```

The workflow accepts only that exact repository-owner comment, consumes its GitHub comment id once in task-owned persistent authorization state, checks out fresh `main`, revalidates this live task state and repository governance, then performs at most the one admitted login submit. Replaying the same comment id is refused.

# Completion

This task is complete only when one admitted trusted-main run produces a sanitized scalar-only artifact with `FIELD6_VALUE_PROVEN=true`, that evidence is independently reviewed/promoted, and the value is consumed by Track B without guessing. Until then, `FIELD6_VALUE=UNKNOWN` remains authoritative.