---
task_id: OTC-20260829-track-a-kasm-canonical-bootstrap-invalidation-live
status: validating
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: reverse_engineering_runtime
phase: live_admission
branch: fix/OTC-20260830-kasm-bootstrap-live-admission
base_branch: main
base_main: 9f79685f6d073c160397eeefdbc2beb27e8921ad
risk: high
execution_class: synology_physical_runtime
execution_mode: github_actions_owner_dispatch
physical_e2e_required: true
runtime_access: canonical_recovery
runtime_owner_task: OTC-20260829-track-a-kasm-canonical-bootstrap-invalidation-live
runtime_namespace: canonical-live-runtime
canonical_registration: PRESENT
canonical_lease_generation: UNKNOWN
registration_lease_generation: 43
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: UNKNOWN
mutation_authorized: false
recovery_mode: prior_boot_zero_client_invalidation_v1
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
live_runtime_authorization_source: PR_758_COMMENT_5470597018
---

# Canonical prior-boot zero-client invalidation

Current direct Synology readback proves the authoritative registration is exact-client fenced but belongs to an older host boot, while `otclient-track-a-kasmvnc` is running on display `:1` with zero `client` processes. This task authorizes only the reviewed metadata-only `prior_boot_zero_client_invalidation_v1` transition under a fresh canonical lease and coordination lock.

It does not authorize credentials, login, GUI input, debugger attach, process-memory access, client stop/restart, character selection or gameplay. The transition must fail closed on any nonzero client count, window/candidate ambiguity, same-boot result, container drift, lease drift or registration race.
