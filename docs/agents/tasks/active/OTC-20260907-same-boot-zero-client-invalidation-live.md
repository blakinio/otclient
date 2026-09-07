---
task_id: OTC-20260907-same-boot-zero-client-invalidation-live
status: ready
agent: ChatGPT
session_id: same-boot-zero-client-invalidation-live-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: canonical_runtime_recovery
phase: live_admission
branch: fix/OTC-20260907-proven-login-replacement-recovery
base_branch: main
base_main: c2e191de82b805eb1ec950e20d83b04edb358429
execution_mode: github_actions_owner_comment
execution_class: synology_physical_runtime
physical_e2e_required: false
runtime_access: canonical_recovery
runtime_owner_task: OTC-20260907-same-boot-zero-client-invalidation-live
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
implementation_authorized: true
live_runtime_authorization_source: OWNER_CHAT_20260907_CONTINUE_FROM_AUTHORIZED_NATIVE_LOGIN_TASK
parent_task: OTC-20260907-proven-login-replacement-recovery
depends_on:
  - OTC-20260906-native-login-physical-executor
---

# Same-boot zero-client invalidation — live admission

This is a future trusted-main admission prepared by PR #975. It is not authority for PR-head runtime execution.

## Evidence boundary

Trusted-main native-login EXECUTE `34094162584 / 101654124268` acquired canonical lease generation `55`, completed rebind and Gate B, then terminated the registered exact-current client inside guarded replacement and failed before auth at `replacement_exact_current_runtime_not_ready`. Read-only Surveyor `34095184707 / 101657174020` immediately afterward proved `CANONICAL_REGISTRATION=PRESENT` with `TARGET_NAMESPACE_CLIENTS=0` and no credential access.

Because Gate B passed immediately before the guarded termination, the stale registration belongs to the same current boot. The registration remained bound to generation `55`; no later client or registration transition was accepted as current authority.

## Allowed transition

After this admission and `TRACK_A_SAME_BOOT_ZERO_CLIENT_INVALIDATION_V1` are merged to trusted `main`, one owner-triggered recovery invocation may:

1. acquire a newer canonical recovery lease;
2. enter canonical `guard-run`;
3. repeatedly prove the same boot, exact current fence, zero official-client candidates, zero Tibia main windows and dead registered PID/start identity;
4. atomically invalidate only `runtime-registration.json` into a private evidence tombstone;
5. leave canonical registration absent and release recovery authority.

No client process, credential, auth, login, GUI input, process memory or gameplay action is authorized by this task.

## Terminal handoff

On PASS, the only next transition is `OTC-20260907-same-boot-zero-client-bootstrap-live`. On any ambiguous or failed proof, stop with the stale registration or fail-closed absent registration exactly as produced by the reviewed transition; do not manually restore or rewrite registration metadata.
