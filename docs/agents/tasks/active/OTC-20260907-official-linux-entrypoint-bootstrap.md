---
task_id: OTC-20260907-official-linux-entrypoint-bootstrap
status: ready
agent: ChatGPT
session_id: official-linux-entrypoint-bootstrap-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: canonical_runtime_bootstrap
phase: live_admission
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
live_runtime_authorization_source: OWNER_CHAT_20260907_EXACT_CURRENT_LOGIN_CLOSURE
parent_task: OTC-20260907-kasm-bin-launch-root-v2
depends_on:
  - OTC-20260907-canonical-kasm-bootstrap-retry-v2-live
canonical_scope_contract: TRACK_A_CANONICAL_KASM_RUNTIME_SCOPE_V1
---

# Exact-current Linux entrypoint bootstrap — live admission

Current trusted `main` is `1b69a1f79ba5ab5bc63a73433670079276a6c7f8`. The prior v2 bootstrap EXECUTE was consumed by run `34124555199`, job `101750043876`; exact-current `15.32.be4f48` launched via direct `packages/Tibia/bin/client` exited before one exact candidate could become ready and rollback passed. Immediate read-only Surveyor run `34124687615`, job `101750488697`, proved authoritative registration `ABSENT` and `TARGET_NAMESPACE_CLIENTS=0` in the canonical Kasm namespace.

The earlier physically stable exact-current `15.32.be4f48` evidence came from the official Linux launcher/install path, not from a direct package-client launch. Current CipSoft Linux support documentation states that the extracted top-level `Tibia` binary must be executed from its own extracted directory and warns that launching from a different location can prevent required files from being found. This task therefore changes the launch hypothesis rather than retrying the direct package client.

This task does **not** authorize another registration invalidation and does not authorize any credential access or login.

## PRECHECK

One owner-triggered PRECHECK may acquire a fresh canonical lease and, under the guarded canonical bootstrap boundary, prove:

- authoritative registration is still `ABSENT`;
- exactly one canonical container `otclient-track-a-kasmvnc` exists;
- exact current package identity `15.32.be4f48` / `52105824` / `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1` is present;
- canonical display `:1` is available;
- the canonical container has zero official game-client candidates and zero Tibia main windows;
- exactly one safe top-level Linux entrypoint candidate named `Tibia` is discoverable inside the canonical Kasm container, outside the package-game directory, as a regular non-symlink executable with its supporting launcher directory.

PRECHECK creates no process, reads no credential source, and inspects only the canonical Kasm container.

## EXECUTE

Only after PRECHECK PASS on the exact same trusted `main`, one owner-triggered EXECUTE may consume the one process-creation budget and run one scoped `kasm-bootstrap` transaction using the existing compatible worker with the official Linux top-level entrypoint launch shape.

The launch must:

- execute the discovered top-level `Tibia` binary from its own directory;
- preserve only the minimal canonical Kasm GUI environment (`HOME`, `DISPLAY`, `XAUTHORITY`) and explicitly remove task/secret/instrumentation variables;
- never scan or mutate other Synology containers;
- accept success only after exactly one exact-current package game `client` process and one Tibia main window are proven;
- preserve exact current package version/size/SHA and canonical display identity;
- rollback only task-created exact process identities and re-prove the original zero-client/zero-window state on failure.

A launcher process that remains as conflicting residue is not a successful safe-detach state.

No credential source, HTTP auth, native login, character selection, GUI input or gameplay is authorized by this task. Those operations remain a later transition after stable canonical registration and fresh Gate B.
