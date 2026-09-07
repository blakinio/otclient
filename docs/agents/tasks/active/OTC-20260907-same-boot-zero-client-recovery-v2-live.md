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

The first recovery attempt exposed an accidental scope expansion: candidate uniqueness was being evaluated across unrelated Docker containers on the Synology host. The corrected Track A runtime boundary is the canonical Kasm container `otclient-track-a-kasmvnc` only.

The registration remains the same same-boot exact-current record bound to lease generation `55`; prior failed recovery and diagnostics never invalidated it and never created a client. Latest direct evidence showed zero client and zero Tibia main windows in canonical Kasm.

## PRECHECK

One owner-triggered PRECHECK may acquire a fresh canonical lease and run only the scoped Kasm worker's zero-client preflight under `guard-run`.

It must prove, inside `otclient-track-a-kasmvnc` only:

- exactly one canonical Kasm container identity;
- current package/display/boot identity;
- zero official-client candidates;
- zero Tibia main windows;
- current boot/display consistency with the stale registration.

Unrelated Synology containers are outside this runtime namespace and must not be executed into or inspected for Tibia candidates. PRECHECK creates no client and does not change registration.

## EXECUTE

Only after a fresh PRECHECK PASS, one separately owner-triggered EXECUTE may:

1. consume a separate v2 recovery authorization;
2. acquire a newer canonical recovery lease and run the reviewed same-boot metadata invalidator using the scoped Kasm worker;
3. require same boot, zero canonical-container candidates, zero canonical Tibia windows, dead registered PID/start identity and stable proofs before/after atomic registration invalidation;
4. release recovery authority with canonical registration absent;
5. hand off only to `OTC-20260907-same-boot-zero-client-bootstrap-v2-live`.

No credentials, auth, GUI input, client process control or gameplay are authorized by this task.
