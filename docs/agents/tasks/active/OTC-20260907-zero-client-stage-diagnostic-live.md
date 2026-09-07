---
task_id: OTC-20260907-zero-client-stage-diagnostic-live
status: ready
agent: ChatGPT
session_id: zero-client-stage-diagnostic-live-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: canonical_runtime_recovery_diagnostic
phase: live_admission
branch: fix/OTC-20260907-zero-client-stage-diagnostics
base_branch: main
base_main: 0f342c9211a5b7214ed8fef8cea0f423115145ac
execution_mode: github_actions_owner_comment
execution_class: synology_physical_runtime
physical_e2e_required: false
runtime_access: canonical_recovery
runtime_owner_task: OTC-20260907-zero-client-stage-diagnostic-live
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
parent_task: OTC-20260907-zero-client-stage-diagnostics
depends_on:
  - OTC-20260907-same-boot-zero-client-diagnostic-live
---

# Zero-client stage diagnostic — live admission

This admission becomes executable only after its implementation is merged to trusted `main`. It authorizes exactly one serialized read-only stage decomposition of the already-approved Kasm bootstrap preflight.

The diagnostic may acquire a newer canonical recovery lease and execute under canonical `guard-run`. It may read the same Docker/container/display/package/boot/process/window evidence already used by `tibia-official-client-re-kasm-bootstrap-worker.py`. Candidate inventory must cover every running Docker container, but output may identify a failing container only as the canonical `target` or a fixed `non_target_N` ordinal; container names, stderr and raw command output must not be emitted.

It MUST NOT invalidate or rewrite canonical registration, create or reuse recovery/bootstrap markers, launch or signal a client, run a bootstrap transition, access credentials, authenticate, select a character, send GUI input or inspect process memory. A new task-local O_EXCL stage-diagnostic marker enforces `diagnostic_attempt_limit: 1`.

The result is diagnostic evidence only. It may identify a fixed stage plus strict sanitized error code, or prove the full zero-client preflight. It does not authorize recovery, bootstrap or login.
