---
task_id: OTC-20260828-current-login-field6-runtime
status: implementing
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME_RESEARCH
track_id: official-client-re
task_kind: reverse_engineering_runtime
phase: repo_static_green
branch: work/OTC-20260828-current-login-field6-runtime
base_branch: main
base_main: 9b3c9fbd4bcac241082591508002ec766d42a1fa
created: 2026-08-28T19:00:00+02:00
updated: 2026-08-28T19:22:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
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
  - exact-current client fence from merged PR #754
blocks:
  - OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE
---

# Objective

Recover the exact current public scalar value carried in `edx` when official Linux Tibia enters the statically proven `GameclientMessageLogin` producer at `PIE + 0xe25620`, then promote that value as the only admissible Track B field6 input.

# Static implementation checkpoint

This branch is repository-only. `runtime_access: none`, `mutation_authorized: false`, `credentials_allowed: false`, and `login_allowed: false` are mandatory until the implementation is reviewed, merged to trusted `main`, and a separate live-admission change is reviewed and merged.

No live official-client observation, launch, login, GDB execution, X11 input, character selection, world entry, gameplay, or Track B E2E is authorized from PR #758 head.

# Exact source boundary

Trusted inputs are only:

- official native Linux client `15.32.75d4a0`;
- size `52105824`;
- SHA-256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`;
- exact producer entry `0xe25620` promoted by merged PR #752;
- the promoted bounded-negative static result `FIELD6_VALUE=UNKNOWN`.

The historical closed/unmerged PR #303 is discovery input only for the Yama-safe parent-GDB shape. It is not runtime authority and none of its old client hashes, displays, ports, branches, task ownership, or run records are accepted as current evidence.

# Intended trusted-main live boundary

After this implementation is merged, a separate live-admission PR may reclassify this task to `ephemeral_isolated` only. The admitted run must use a task-owned state root, display `:131`, task-owned WARP SOCKS `127.0.0.1:25441`, task-owned process markers, and the exact current client copied into a task-owned HOME.

The live action budget is one logical account-login submission. The observer is GDB-as-parent, never attach: ASLR remains enabled, the exact child PIE is resolved after `exec`, and a single breakpoint at `PIE + 0xe25620` retains only `uint32(edx)`. No stack bytes, packet payload, credentials, process environment, unrelated registers, or arbitrary process memory may be retained.

The protected-step credential environment is removed before any helper preflight child process: a tiny task-owned wrapper de-exports the two secret names, verifies they are absent from `env`, then sources the helper in the same shell so the values remain non-exported shell variables until the single login submit.

The live experiment must remain bounded by:

```text
login_submit_count=1
character_selection_performed=false
world_entry_performed=false
gameplay_performed=false
network_payload_capture_performed=false
```

A second logged-in Track A experiment is permitted only by a fresh, exact owner comment on PR #758 after live admission is on trusted `main`. The accepted trigger text is:

```text
AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V1 once=true
```

The workflow must reject rerunning the same authorization event and must not consume credentials if trusted-main admission, exact fence, namespace uniqueness, toolchain, display, port, or task-owned preflight fails.

# Completion

This task is complete only when one admitted trusted-main run produces a sanitized scalar-only artifact with `FIELD6_VALUE_PROVEN=true`, that evidence is independently reviewed/promoted, and the value is consumed by Track B without guessing. Until then, `FIELD6_VALUE=UNKNOWN` remains authoritative.