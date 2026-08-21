---
task_id: OTC-20260821-surveyor-action-protocol-reader
status: implementing
phase: validate
agent: ChatGPT
project_lane: otclient
lane: P0-ACTION
track_id: official-client-re
task_kind: implementation
risk: medium
policy_version: 2
runtime_access: read_only
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: canonical-live-runtime
canonical_registration: UNKNOWN
canonical_lease_generation: UNKNOWN
registration_lease_generation: UNKNOWN
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: false
gui_input_authorized: false
process_control_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
base_main: 13b3f02a07a176662d766352d9af39619775a73d
branch: fix/OTC-20260821-surveyor-action-protocol-elf-resolver
implementation_pr: 645
implementation_merge_sha: f80dd43f741c39ce5ee4296396cb07891d04c324
acceptance_pr: 646
acceptance_merge_sha: b7fa88ef2d772c70ca7250b587e7f584327ee37b
repair_pr: 648
selected_gap: action_protocol_typed_reader
physical_e2e_required: true
physical_e2e_result: FAIL_REPAIR_IN_PROGRESS
last_physical_run: 32494958152
---

# Surveyor v2 — action protocol typed reader acceptance

## Current checkpoint

Implementation PR #645 merged as `f80dd43f741c39ce5ee4296396cb07891d04c324`. Read-only acceptance authority PR #646 merged as `b7fa88ef2d772c70ca7250b587e7f584327ee37b`.

Physical run `32494958152` proved the runtime/control preflight but failed the reader acceptance. Verified preflight facts from that run were: one exact client in the declared namespace, one matching visible window, exact size/SHA, stable PID/start identity, `target_uniqueness=PROVEN`, and matching canonical registration. The passive Surveyor collect still returned 169 rows / 12 aliases / 8 repository-known missing readers / privacy PASS, but `action_protocol_typed_reader` was `UNAVAILABLE` with `READ_FAILED:RuntimeError`.

The failure was localized to the reader's static current-build discovery path: it depended on external `strings` and `readelf` commands in the target container before opening process memory. Repair PR #648 replaces that dependency with a bounded pure-Python ELF64 parser over the exact-fenced `/proc/PID/exe`. It resolves the unique mangled RTTI string, `R_X86_64_RELATIVE` typeinfo relation and unique primary vptr, then runs the existing bounded `/proc/PID/mem` `O_RDONLY` typed-presence probe. Failures are separated into `STATIC_LAYOUT_FAILED:*` and `LIVE_TYPED_PROBE_FAILED:*` without weakening acceptance.

## Read-only admission checkpoint

Historical PID/start/registration/lease values are not admitted as current truth. Every physical retry must freshly re-read all of them and fail before process-memory access unless the current exact target is unique, exact-fenced, display-owned and non-conflicting.

The workflow must revalidate from scratch:

- target container running;
- exactly one `client` process in the declared target namespace;
- current PID and process start ticks;
- executable path, size and SHA-256;
- display `:1` availability;
- exactly one visible Tibia window owned by that PID;
- no fresh active canonical lease owned by another task;
- canonical registration identity consistency when registration exists;
- implementation/repair ancestry from trusted `main`.

Only after those checks may Surveyor open `/proc/PID/mem` with `O_RDONLY` and execute passive `--collect-all`.

## Acceptance contract

PASS requires:

- 169 canonical rows;
- 12 aliases;
- privacy PASS;
- `action_protocol_typed_reader` `AVAILABLE`;
- exact `tibia::game::TPlayerProtocolMessageHandler` typed object count = 1;
- `typed_object_identity=PROVEN`;
- `process_memory_access=read_only`;
- semantic state `TYPED_ACTION_PROTOCOL_OBJECT_IDENTITY_ONLY`;
- `action_to_protocol_connection_claimed=false`;
- `serialized_message_semantics_claimed=false`;
- `protocol_opcodes_claimed=false`;
- `packet_payloads_retained=false`;
- `in_game_claimed=false`;
- missing typed readers `9 -> 8`;
- no runtime mutation.

## Hard safety boundary

No login/logout/relogin, credentials, GUI/gameplay input, process control, attach/debug/injection, process-memory writes, client/container restart, target-network mutation, item/economy action or local-model use is authorized. Structural presence is not packet/action semantics and is not `IN_GAME` proof.
