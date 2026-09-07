---
task_id: OTC-20260907-same-boot-zero-client-recovery-v2-live
status: ready
agent: ChatGPT
session_id: same-boot-zero-client-recovery-v2-live-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: canonical_runtime_recovery
phase: live_admission
branch: fix/OTC-20260907-docker-candidate-inventory-compatibility
base_branch: main
base_main: 9736b38e9c8aa54833716ac63a75e93e5415cc92
execution_mode: github_actions_owner_comment
execution_class: synology_physical_runtime
physical_e2e_required: false
runtime_access: canonical_recovery
runtime_owner_task: OTC-20260907-same-boot-zero-client-recovery-v2-live
runtime_namespace: canonical-live-runtime
canonical_registration: PRESENT
canonical_lease_generation: UNKNOWN
registration_lease_generation: 55
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: UNKNOWN
mutation_authorized: false
recovery_mode: same_boot_zero_client_invalidation_v1
same_boot_zero_client_contract: TRACK_A_SAME_BOOT_ZERO_CLIENT_INVALIDATION_V1
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
physical_action_budget: 0
physical_action_count: 0
precheck_attempt_limit: 1
recovery_attempt_limit: 1
implementation_authorized: true
live_runtime_authorization_source: OWNER_CHAT_20260907_CONTINUE_NATIVE_LOGIN_CLOSURE
parent_task: OTC-20260907-docker-candidate-inventory-compatibility
depends_on:
  - OTC-20260907-zero-client-stage-diagnostics
---

# Same-boot zero-client recovery v2 — live admission

This admission exists only because trusted-main stage diagnostic `34110414865 / 101705085690` proved that the first recovery attempt failed on unrelated-container userspace compatibility, not on canonical target state.

The registration remains the same same-boot exact-current record bound to lease generation `55`; the failed recovery and diagnostics never invalidated it and never created a client. The canonical Kasm target remains a zero-client state by the latest direct Surveyor/stage evidence.

## PRECHECK

One owner-triggered PRECHECK may acquire a fresh canonical lease and run only the compatibility bootstrap worker's zero-client preflight under `guard-run`. It must cover all running Docker containers through daemon-side process census and may deep-inspect only official-looking candidates. It creates no client and does not change registration. Failure consumes only the v2 PRECHECK authorization and requires a new reviewed repair; it must not fall through into EXECUTE.

## EXECUTE

Only after a fresh PRECHECK PASS, one separately owner-triggered EXECUTE may:

1. consume a separate v2 recovery authorization;
2. acquire a newer canonical recovery lease and run the reviewed same-boot metadata invalidator using the compatibility worker;
3. require same boot, zero exact/current candidates, zero main windows, dead registered PID/start identity and stable proofs before/after atomic registration invalidation;
4. release recovery authority with canonical registration absent;
5. hand off only to `OTC-20260907-same-boot-zero-client-bootstrap-v2-live`.

No credentials, auth, GUI input, client process control or gameplay are authorized by this task.
