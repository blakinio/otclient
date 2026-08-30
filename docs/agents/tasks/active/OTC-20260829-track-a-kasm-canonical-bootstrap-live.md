---
task_id: OTC-20260829-track-a-kasm-canonical-bootstrap-live
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
runtime_access: canonical_bootstrap
runtime_owner_task: OTC-20260829-track-a-kasm-canonical-bootstrap-live
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
implementation_authorized: true
live_runtime_authorization_source: PR_758_COMMENT_5470597018
---

# Canonical Kasm create-new bootstrap

After the separate invalidation task proves canonical registration absent, this task authorizes exactly one reviewed `kasm_create_new_v1` launch of the already-present exact official client in `otclient-track-a-kasmvnc` on display `:1`. The expected client fence is `15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`.

This bootstrap stops at an idle `state: UNKNOWN` canonical registration. It does not authorize credentials, login, GUI input, debugger attach, process-memory observation, relogin, character selection or gameplay. The one process-creation action is consumed even if later registration proof fails; no identical bootstrap retry is allowed without a fresh admission.
