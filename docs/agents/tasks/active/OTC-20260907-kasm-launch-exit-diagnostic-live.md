---
task_id: OTC-20260907-kasm-launch-exit-diagnostic-live
status: ready
agent: ChatGPT
session_id: kasm-launch-exit-diagnostic-live-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: canonical_runtime_bootstrap_diagnostic
phase: live_admission
branch: diag/OTC-20260907-kasm-launch-exit-proof
base_branch: main
base_main: 1b69a1f79ba5ab5bc63a73433670079276a6c7f8
execution_mode: github_actions_owner_comment
execution_class: synology_physical_runtime
physical_e2e_required: true
runtime_access: canonical_bootstrap
runtime_owner_task: OTC-20260907-kasm-launch-exit-diagnostic-live
runtime_namespace: canonical-live-runtime
canonical_registration: ABSENT
canonical_lease_generation: UNKNOWN
registration_lease_generation: NOT_APPLICABLE
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: PASS
target_uniqueness: UNKNOWN
mutation_authorized: true
bootstrap_mode: create_new
bootstrap_attempt_limit: 1
credentials_allowed: false
login_allowed: false
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: true
network_payload_capture_allowed: false
process_memory_access_allowed: false
physical_action_budget: 1
physical_action_count: 0
diagnostic_attempt_limit: 1
implementation_authorized: true
live_runtime_authorization_source: OWNER_CHAT_20260907_CONTINUE_FULL_CHAIN_CHANGED_PROOF_MODE
parent_task: OTC-20260907-kasm-launch-exit-proof
depends_on:
  - OTC-20260907-canonical-kasm-bootstrap-retry-v2-live
canonical_scope_contract: TRACK_A_CANONICAL_KASM_RUNTIME_SCOPE_V1
---

# Launch-exit diagnostic — live admission

The authoritative starting state is the post-rollback Surveyor evidence from run `34124687615`, job `101750488697`: `CANONICAL_REGISTRATION=ABSENT` and `TARGET_NAMESPACE_CLIENTS=0` in `otclient-track-a-kasmvnc`.

This is a changed proof mode after two bounded bootstrap failures. It authorizes exactly one diagnostic client creation, not another bootstrap/adoption attempt.

## Preconditions

Before process creation, the diagnostic must prove under the canonical lease guard:

- authoritative registration remains ABSENT;
- exactly one canonical Kasm container exists and display `:1` is available;
- exact-current client package identity matches the current fence;
- canonical Kasm contains zero exact-current candidates and zero Tibia windows.

## Authorized physical action

Exactly one plain exact-current client may be launched from `.../packages/Tibia/bin` using HOME, DISPLAY, XAUTHORITY and `LD_LIBRARY_PATH=bin:bin/lib`, with credential, helper, preload and canonical lease variables explicitly removed from the child environment.

The diagnostic may observe only process identity/liveness, numeric exit status, visible Tibia-window count and task-local stdout/stderr files. Raw stdout/stderr must never be printed. Stderr may only be mapped to an allowlisted class.

If any exact-current client remains alive at diagnostic termination, the diagnostic may SIGTERM only exact-current candidate PID(s) proven to have appeared after the initial zero-state preflight, then must prove they are gone. Canonical registration must remain ABSENT throughout.

Success of the diagnostic means the observation and cleanup contract completed, regardless of whether the client itself exited or became window-ready. It does not qualify bootstrap, auth or login.
