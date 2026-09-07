---
task_id: OTC-20260907-official-linux-entrypoint-bootstrap
status: blocked
agent: ChatGPT
session_id: official-linux-entrypoint-bootstrap-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: canonical_runtime_bootstrap
phase: consumed_schema_blocker
branch: fix/OTC-20260907-official-linux-entrypoint-bootstrap
base_branch: main
base_main: 1b69a1f79ba5ab5bc63a73433670079276a6c7f8
execution_mode: github_actions_owner_comment
execution_class: synology_physical_runtime
physical_e2e_required: true
runtime_access: canonical_bootstrap
runtime_owner_task: OTC-20260907-official-linux-entrypoint-bootstrap
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
implementation_authorized: false
live_runtime_authorization_source: OWNER_CHAT_20260907_EXACT_CURRENT_LOGIN_CLOSURE
live_runtime_authorization_consumed: true
parent_task: OTC-20260907-kasm-bin-launch-root-v2
depends_on:
  - OTC-20260907-canonical-kasm-bootstrap-retry-v2-live
canonical_scope_contract: TRACK_A_CANONICAL_KASM_RUNTIME_SCOPE_V1
superseded_by: OTC-20260907-official-entrypoint-transition-compat-bootstrap
---

# Exact-current Linux entrypoint bootstrap — consumed live admission

Trusted implementation merged as PR #981 on `main` commit `ef6301df117700ca4170d40c922bc94175a146d1`.

The prior v2 direct package-client launch had already failed in run `34124555199`, job `101750043876`; immediate Surveyor `34124687615`, job `101750488697`, proved authoritative registration `ABSENT` and `TARGET_NAMESPACE_CLIENTS=0`. PR #981 therefore changed the launch hypothesis to the official Linux top-level `Tibia` entrypoint while preserving the exact-current package fence `15.32.be4f48` / `52105824` / `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`.

## Consumed PRECHECK

Owner-triggered PRECHECK run `34131050885`, job `101770990388`, passed on trusted `main`. It proved:

- authoritative registration `ABSENT`;
- exactly one canonical container `otclient-track-a-kasmvnc`;
- exact current package identity;
- canonical display `:1` available;
- zero official game-client candidates and zero Tibia main windows;
- exactly one safe top-level Linux entrypoint named `Tibia` outside the package-game directory;
- no process creation and no credential access.

The one-shot PRECHECK authorization is consumed and must not be reused.

## Consumed EXECUTE

Owner-triggered EXECUTE run `34131140019`, job `101771284041`, consumed the one EXECUTE attempt but failed before process creation with:

`TRACK_A_CANONICAL_TRANSITION_ERROR=kasm_bootstrap_record_invalid`

Root cause: the PR #981 compatible worker emits launcher-bound PRECHECK/LAUNCH record fields and launch method `docker_exec_detached_official_linux_entrypoint`, while the existing canonical transition record reader still accepts only the historical direct-client exact key sets and launch method.

The failure occurred before credential access and before any exact official game-client process was created. Post-failure read-only Surveyor run `34131763597`, job `101773293609`, again proved authoritative registration `ABSENT` and `TARGET_NAMESPACE_CLIENTS=0`.

This admission is terminally consumed. `mutation_authorized: false`, and neither its PRECHECK nor EXECUTE may be retried.

## Successor

Continuation moved to `OTC-20260907-official-entrypoint-transition-compat-bootstrap`, which is allowed to land one narrow scoped transition compatibility correction and then use its own fresh one-shot PRECHECK/EXECUTE admission after that correction reaches trusted `main`.