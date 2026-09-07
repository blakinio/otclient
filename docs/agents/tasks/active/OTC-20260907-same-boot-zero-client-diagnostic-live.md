---
task_id: OTC-20260907-same-boot-zero-client-diagnostic-live
status: ready
agent: ChatGPT
session_id: same-boot-zero-client-diagnostic-live-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: canonical_runtime_recovery_diagnostic
phase: live_admission
branch: fix/OTC-20260907-same-boot-recovery-diagnostics
base_branch: main
base_main: 5e72f5a44a52a43b47dae83dccca656682d118a3
execution_mode: github_actions_owner_comment
execution_class: synology_physical_runtime
physical_e2e_required: false
runtime_access: canonical_recovery
runtime_owner_task: OTC-20260907-same-boot-zero-client-diagnostic-live
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
diagnostic_attempt_limit: 1
implementation_authorized: true
live_runtime_authorization_source: OWNER_CHAT_20260907_CONTINUE_FROM_AUTHORIZED_NATIVE_LOGIN_TASK
parent_task: OTC-20260907-same-boot-recovery-diagnostics
depends_on:
  - OTC-20260907-same-boot-zero-client-invalidation-live
---

# Same-boot zero-client diagnostic — live admission

This admission becomes executable only after the diagnostic implementation is merged to trusted `main`. It authorizes one serialized read-only evaluation of the existing approved Kasm bootstrap worker's `collect_preflight()` against the current canonical physical host.

The diagnostic may acquire a newer canonical recovery lease and run under canonical `guard-run` so the all-container inventory is stable while observed. It may read Docker container inventory, exact package identity, boot identity, display availability, official-client candidate inventory and Tibia-window count exactly as the existing bootstrap preflight already does.

It MUST NOT invalidate or rewrite registration, create a bootstrap marker, launch or signal a client, run the bootstrap transition, access credentials, authenticate, select a character, send GUI input, inspect process memory or continue into login. Its only output is PASS metadata or one strict sanitized hardcoded worker error code.

On completion, release the recovery lease. The resulting code is diagnostic evidence only; it does not authorize recovery, bootstrap or login. A separate reviewed action must be selected from that evidence.
