---
task_id: OTC-20260907-canonical-kasm-bootstrap-retry-v2-live
status: blocked
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
mutation_authorized: false
bootstrap_mode: create_new
bootstrap_attempt_limit: 1
credentials_allowed: false
login_allowed: false
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
process_memory_access_allowed: false
physical_action_budget: 1
physical_action_count: 1
precheck_attempt_limit: 1
precheck_attempt_count: 1
execute_attempt_limit: 1
execute_attempt_count: 1
implementation_authorized: true
live_runtime_authorization_source: OWNER_CHAT_20260907_CONTINUE_FULL_CHAIN_AFTER_ZERO_STATE_SURVEY
parent_task: OTC-20260907-kasm-bin-launch-root-v2
depends_on:
  - OTC-20260907-canonical-kasm-bootstrap-retry-live
canonical_scope_contract: TRACK_A_CANONICAL_KASM_RUNTIME_SCOPE_V1
superseded_by: OTC-20260907-official-linux-entrypoint-bootstrap
last_physical_run: 34124555199
last_physical_job: 101750043876
post_failure_survey_run: 34124687615
post_failure_survey_job: 101750488697
---

# Canonical Kasm bootstrap retry v2 — consumed live admission

This admission is **consumed** and must not be reused. Run `34124555199`, job `101750043876`, consumed the one EXECUTE attempt on trusted `main` after the bin-root/cwd correction. PRECHECK passed, but the exact-current package `client` exited before a ready exact candidate could be established; rollback passed. No credentials were accessed.

Immediate read-only Surveyor run `34124687615`, job `101750488697`, subsequently proved:

- authoritative canonical registration: `ABSENT`;
- canonical Kasm target namespace clients: `0`;
- no credential-bearing attempt occurred.

The direct `packages/Tibia/bin/client` launch hypothesis is therefore closed for this task. A third materially identical direct launch is not authorized.

The successor task is `OTC-20260907-official-linux-entrypoint-bootstrap`, which changes the launch hypothesis to the current official Linux top-level `Tibia` entrypoint and carries a separate one-shot admission/budget.

This consumed task does **not** authorize registration invalidation, process creation, process control, credentials, login, character selection, GUI input or gameplay.
