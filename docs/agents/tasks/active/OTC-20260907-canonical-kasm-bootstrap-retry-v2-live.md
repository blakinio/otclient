---
task_id: OTC-20260907-canonical-kasm-bootstrap-retry-v2-live
status: ready
agent: ChatGPT
session_id: canonical-kasm-bootstrap-retry-v2-live-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: canonical_runtime_bootstrap
phase: live_admission
branch: fix/OTC-20260907-kasm-bin-launch-root-v2
base_branch: main
base_main: 5edbb7585e1877dea45b91f8c0dc005fc3598bfa
execution_mode: github_actions_owner_comment
execution_class: synology_physical_runtime
physical_e2e_required: true
runtime_access: canonical_bootstrap
runtime_owner_task: OTC-20260907-canonical-kasm-bootstrap-retry-v2-live
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
precheck_attempt_limit: 1
execute_attempt_limit: 1
implementation_authorized: true
live_runtime_authorization_source: OWNER_CHAT_20260907_CONTINUE_FULL_CHAIN_AFTER_ZERO_STATE_SURVEY
parent_task: OTC-20260907-kasm-bin-launch-root-v2
depends_on:
  - OTC-20260907-canonical-kasm-bootstrap-retry-live
canonical_scope_contract: TRACK_A_CANONICAL_KASM_RUNTIME_SCOPE_V1
---

# Canonical Kasm bootstrap retry v2 — live admission

The previous bootstrap retry consumed its one process-creation attempt and failed before registration. Immediate read-only Surveyor run `34122156989`, job `101742448722`, subsequently proved the authoritative registration is ABSENT and the canonical Kasm container contains zero `client` processes. This v2 task therefore authorizes one new create-new attempt only after the bin-root launcher correction is merged to trusted `main`.

This task does **not** authorize another registration invalidation.

## PRECHECK

One owner-triggered PRECHECK may acquire a fresh canonical lease and prove under `guard-run`:

- authoritative registration is still ABSENT;
- exactly one canonical container `otclient-track-a-kasmvnc` exists;
- exact current package identity is present;
- canonical display `:1` is available;
- canonical container has zero official-client candidates and zero Tibia main windows.

PRECHECK creates no process and accesses no credentials.

## EXECUTE

Only after PRECHECK PASS on the exact same trusted `main`, one owner-triggered EXECUTE may consume one process-creation budget and run one scoped `kasm-bootstrap` transaction using the corrected bin-root worker and canonical-Kasm probe.

Success requires one exact-current client and canonical registration with:

- `state: UNKNOWN`;
- `proof_kind: existing_runtime_adoption_v1`;
- `candidate_count: 1`;
- `inventory_scope: canonical_kasm_container`;
- `inventory_complete: true`.

The worker launch must use the exact executable directory `.../packages/Tibia/bin` as cwd and loader root, matching the physically successful historical Kasm launcher evidence.

On failure, rollback remains mandatory. If the process exits before launch identity is persisted, rollback may report success only when a fresh canonical-Kasm preflight re-proves the original zero-client/zero-window state with unchanged container, boot and exact client fence.

No credential source, auth, login, character selection, GUI input or gameplay is authorized by this task.
