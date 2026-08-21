---
task_id: OTC-20260821-surveyor-action-protocol-reader
status: validating
phase: exact_head_ci_refresh
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
base_main: 532b54fa60d11ae10227ab16dc02cd0cadf39b23
branch: fix/OTC-20260821-surveyor-action-protocol-elf-resolver
implementation_pr: 645
implementation_merge_sha: f80dd43f741c39ce5ee4296396cb07891d04c324
acceptance_pr: 646
acceptance_merge_sha: b7fa88ef2d772c70ca7250b587e7f584327ee37b
repair_pr: 648
repair_pre_refresh_head: 9a26c0a750b1decd1f75b94f8826cde1e0c41b06
repair_hosted_validation_sha: 9a26c0a750b1decd1f75b94f8826cde1e0c41b06
repair_hosted_validation: PASS
repair_stalled_ci_run: 32508074696
repair_stalled_ci_jobs: [96853104389, 96853104458]
selected_gap: action_protocol_typed_reader
physical_e2e_required: true
physical_e2e_result: FAIL_REPAIR_IN_PROGRESS
last_physical_run: 32494958152
invocation_started_at: 2026-08-21T17:30:00Z
last_progress_at: 2026-08-21T17:31:35Z
ci_checks_for_current_head: 1
ci_check_generation: ready_refresh
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Surveyor v2 — action protocol typed reader acceptance

## Current checkpoint

Implementation PR #645 merged as `f80dd43f741c39ce5ee4296396cb07891d04c324`. Read-only acceptance authority PR #646 merged as `b7fa88ef2d772c70ca7250b587e7f584327ee37b`.

Physical run `32494958152` proved the runtime/control preflight but failed the reader acceptance. Verified preflight facts from that run were: one exact client in the declared namespace, one matching visible window, exact size/SHA, stable PID/start identity, `target_uniqueness=PROVEN`, and matching canonical registration. The passive Surveyor collect still returned 169 rows / 12 aliases / 8 repository-known missing readers / privacy PASS, but `action_protocol_typed_reader` was `UNAVAILABLE` with `READ_FAILED:RuntimeError`.

The failure was localized to the reader's static current-build discovery path: it depended on external `strings` and `readelf` commands in the target container before opening process memory. Repair PR #648 replaces that dependency with a bounded pure-Python ELF64 parser over the exact-fenced `/proc/PID/exe`. It resolves the unique mangled RTTI string, `R_X86_64_RELATIVE` typeinfo relation and unique primary vptr, then runs the existing bounded `/proc/PID/mem` `O_RDONLY` typed-presence probe. Failures are separated into `STATIC_LAYOUT_FAILED:*` and `LIVE_TYPED_PROBE_FAILED:*` without weakening acceptance.

Exact repair head `9a26c0a750b1decd1f75b94f8826cde1e0c41b06` passed Track A Surveyor validation run `32508074442`: compile PASS, 47/47 focused tests PASS, repository-only collect-all 169 rows / 12 aliases / 8 missing readers / privacy PASS. Track A agent runtime governance run `32508074428` also passed. Fresh validator-role audit recorded on PR #648 reported PASS with zero material findings and no unresolved review threads.

Required CI run `32508074696` did not reach a terminal result: both Linux build jobs `96853104389` and `96853104458` remained in progress at their `Run CMake` step for roughly two hours while all preceding jobs were green. The in-progress job log endpoint returned no live log payload. This checkpoint is a meaningful exact-state refresh before generating a new CI run; no test or branch-protection gate is bypassed or weakened.

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
