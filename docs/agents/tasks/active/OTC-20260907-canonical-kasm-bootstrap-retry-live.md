---
task_id: OTC-20260907-canonical-kasm-bootstrap-retry-live
status: ready
agent: ChatGPT
session_id: canonical-kasm-bootstrap-retry-live-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: canonical_runtime_bootstrap
phase: live_admission
branch: fix/OTC-20260907-kasm-bootstrap-launch-readiness
base_branch: main
base_main: 7352d49dc3ba0cabfea3f020859ba8d26feabc15
execution_mode: github_actions_owner_comment
execution_class: synology_physical_runtime
physical_e2e_required: true
runtime_access: canonical_bootstrap
runtime_owner_task: OTC-20260907-canonical-kasm-bootstrap-retry-live
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
live_runtime_authorization_source: OWNER_CHAT_20260907_EXECUTE_FULL_CHAIN_AFTER_IDENTITY_BOUND_ROLLBACK
parent_task: OTC-20260907-kasm-bootstrap-launch-readiness
depends_on:
  - OTC-20260907-same-boot-zero-client-bootstrap-v2-live
canonical_scope_contract: TRACK_A_CANONICAL_KASM_RUNTIME_SCOPE_V1
---

# Canonical Kasm bootstrap retry — live admission

The previous recovery-v2 transaction already invalidated the stale same-boot registration and then rolled back the newly launched client after adoption proof failed. This task does **not** authorize another invalidation.

## PRECHECK

One owner-triggered PRECHECK may acquire a fresh canonical lease and prove under `guard-run`:

- authoritative registration is still ABSENT;
- exactly one canonical container `otclient-track-a-kasmvnc` exists;
- exact current package identity is present;
- canonical display `:1` is available;
- canonical container has zero official-client candidates and zero Tibia main windows.

PRECHECK creates no client and accesses no credentials.

## EXECUTE

Only after PRECHECK PASS on the exact same trusted `main`, one owner-triggered EXECUTE may consume one process-creation budget and run one scoped `kasm-bootstrap` transaction using the repaired worker/probe. Success requires one exact-current client and canonical registration with:

- `state: UNKNOWN`;
- `proof_kind: existing_runtime_adoption_v1`;
- `candidate_count: 1`;
- `inventory_scope: canonical_kasm_container`;
- `inventory_complete: true`.

The existing transition's identity-bound rollback remains mandatory on failure. No credential source, auth, login, character selection, GUI input or gameplay is authorized.
