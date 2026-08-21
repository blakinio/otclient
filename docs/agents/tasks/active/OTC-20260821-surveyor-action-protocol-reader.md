---
task_id: OTC-20260821-surveyor-action-protocol-reader
status: implementing
phase: live_diagnostic_repair
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
canonical_registration: PRESENT
canonical_lease_generation: 19
registration_lease_generation: 19
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
feature_scope:
  type: backend_only
  user_facing: false
  backend_required: true
  frontend_required: false
  integration_required: true
  e2e_required: true
base_main: dbc05824fb539a5dfffb0bd8cb48dbfb3a9a01e1
branch: fix/OTC-20260821-surveyor-action-protocol-live-diagnostics
owned_paths:
  - tools/tibia_re_surveyor/action_protocol.py
  - tools/tibia_re_surveyor/action_protocol_presence.py
  - tests/tools/tibia_re_surveyor/test_action_protocol_presence.py
  - docs/agents/tasks/active/OTC-20260821-surveyor-action-protocol-reader.md
modules_touched:
  - tibia_re_surveyor
reuses:
  - tools/tibia_re_surveyor/typed_presence.py
  - tools/tibia_re_surveyor/runtime.py
depends_on:
  - PR-645
  - PR-646
  - PR-648
blocks: []
implementation_pr: 645
implementation_merge_sha: f80dd43f741c39ce5ee4296396cb07891d04c324
acceptance_pr: 646
acceptance_merge_sha: b7fa88ef2d772c70ca7250b587e7f584327ee37b
repair_pr: 648
repair_merge_sha: dbc05824fb539a5dfffb0bd8cb48dbfb3a9a01e1
diagnostic_repair_pr: PENDING
selected_gap: action_protocol_typed_reader
physical_e2e_required: true
physical_e2e_result: FAIL_LIVE_TYPED_PROBE_DIAGNOSTIC_REPAIR
last_physical_run: 32511156780
last_physical_job: 96862518180
last_physical_trigger_pr: 651
physical_static_vptr_offset: 0x30bf620
physical_static_typeinfo_offset: 0x30bf298
invocation_started_at: 2026-08-21T17:30:00Z
last_progress_at: 2026-08-21T18:06:18Z
ci_checks_for_current_head: 0
ci_check_generation: diagnostic_repair
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Surveyor v2 — action protocol typed reader acceptance

## Current verified checkpoint

Implementation PR #645 merged as `f80dd43f741c39ce5ee4296396cb07891d04c324`. Read-only acceptance authority PR #646 merged as `b7fa88ef2d772c70ca7250b587e7f584327ee37b`. Repair PR #648 removed the unavailable `strings`/`readelf` runtime dependency and merged as `dbc05824fb539a5dfffb0bd8cb48dbfb3a9a01e1` after exact-head Surveyor, Track A governance, audit and required CI PASS.

Fresh physical request-only trigger PR #651 used exact trusted base `dbc05824fb539a5dfffb0bd8cb48dbfb3a9a01e1`. Workflow run `32511156780`, authority job `96862488233`, proved owner trigger authority; acceptance job `96862518180` executed only trusted-main code and remained read-only.

Fresh runtime preflight PASS on that run:

- one exact client in `otclient-track-a-kasmvnc`;
- PID `19590`, process start ticks `76611792`;
- executable `/home/kasm-user/otclient-track-a/Tibia-32177065988-1/bin/client`;
- size `52109920`, SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`;
- display `:1`, exactly one matching visible Tibia window;
- target uniqueness `PROVEN`;
- canonical registration present and identity-matching, generation `2`, lease generation `19`;
- lease generation `19`, status released/expired;
- no credential access, GUI input, process control, process-memory write, network mutation or runtime mutation.

The passive collect produced 169 rows, 12 aliases, 8 repository-known missing readers and `READ_ONLY_ADMITTED`. Exact-current static RTTI resolution succeeded for `tibia::game::TPlayerProtocolMessageHandler` with typeinfo `0x30bf298` and primary vptr `0x30bf620`. Live typed-presence still failed closed as `LIVE_TYPED_PROBE_FAILED:RuntimeError`; no semantic promotion occurred.

## Current repair hypothesis

The generic presence probe additionally filters an aligned exact-vptr match by assuming the word at `object + 8` is a non-zero pointer into a writable mapping. That discriminator has not been physically proven for `TPlayerProtocolMessageHandler`. The current repair does **not** remove the discriminator or claim object identity. It adds action-protocol-specific bounded diagnostics that expose only two integer counts on failure: exact-vptr matches before the filter and matches after the filter. Arbitrary child stderr, object addresses, memory bytes, packet payloads and gameplay data remain unexposed. The probe remains exact-fenced, bounded and `O_RDONLY`.

## Read-only admission checkpoint

Every physical retry must freshly re-read target container, one exact client PID/start, executable path/size/SHA, display, one matching window, lease/control state, registration identity and trusted-main ancestry. Only after these checks may Surveyor open `/proc/PID/mem` with `O_RDONLY` and run passive `--collect-all`.

## Acceptance contract

PASS requires all of:

- 169 canonical rows and 12 aliases;
- privacy PASS;
- `action_protocol_typed_reader` `AVAILABLE`;
- exact `tibia::game::TPlayerProtocolMessageHandler` object count = 1;
- `typed_object_identity=PROVEN`;
- `process_memory_access=read_only`;
- semantic state `TYPED_ACTION_PROTOCOL_OBJECT_IDENTITY_ONLY`;
- action-to-protocol, serialized-message, opcode, packet-payload and `IN_GAME` claims all false;
- missing typed readers `9 -> 8`;
- no runtime mutation.

## Hard safety boundary

No login/logout/relogin, credentials, GUI/gameplay input, character movement, process control, attach/debug/injection, process-memory writes, client/container restart, target-network mutation, inventory/item/economy action, attack, trade or local-model use is authorized. Structural/static evidence is never promoted to semantic truth without an appropriate causal/structural discriminator.
