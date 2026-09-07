---
task_id: OTC-20260907-same-boot-zero-client-bootstrap-live
status: ready
agent: ChatGPT
session_id: same-boot-zero-client-bootstrap-live-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: canonical_runtime_bootstrap
phase: live_admission
branch: fix/OTC-20260907-proven-login-replacement-recovery
base_branch: main
base_main: c2e191de82b805eb1ec950e20d83b04edb358429
execution_mode: github_actions_owner_comment
execution_class: synology_physical_runtime
physical_e2e_required: true
runtime_access: canonical_bootstrap
runtime_owner_task: OTC-20260907-same-boot-zero-client-bootstrap-live
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
live_runtime_authorization_source: OWNER_CHAT_20260907_CONTINUE_FROM_AUTHORIZED_NATIVE_LOGIN_TASK
parent_task: OTC-20260907-proven-login-replacement-recovery
depends_on:
  - OTC-20260907-same-boot-zero-client-invalidation-live
---

# Plain exact-current Kasm restore — live bootstrap admission

This future admission becomes executable only after PR #975 is merged to trusted `main` and the separate same-boot invalidation task has atomically made the canonical registration absent.

## Allowed action

The task authorizes exactly one existing reviewed `kasm-bootstrap` create-new transition in `otclient-track-a-kasmvnc` on display `:1`. The transition must freshly prove registration absence, zero official-client candidates, zero Tibia main windows, exact current package identity and current canonical lease under its reviewed bootstrap supervisor before launching anything.

The only client action is creation of one **plain exact-current** official Linux client. The task stops at a canonical `existing_runtime_adoption_v1` registration with fail-closed `state: UNKNOWN`.

No credential source, native auth, login, character selection, GUI input, gameplay, process-memory observation or helper preload is authorized. The one process-creation budget is consumed even if later bootstrap registration proof fails.

## Handoff

After successful restore, release bootstrap authority. The parent native-login programme must perform a fresh trusted-main PRECHECK and a new Gate A/rebind/Gate B sequence before any instrumented replacement or credential-bearing action. This task itself must never continue into login.
