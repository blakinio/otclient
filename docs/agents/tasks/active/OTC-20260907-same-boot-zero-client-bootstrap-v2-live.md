---
task_id: OTC-20260907-same-boot-zero-client-bootstrap-v2-live
status: ready
agent: ChatGPT
session_id: same-boot-zero-client-bootstrap-v2-live-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: canonical_runtime_bootstrap
phase: live_admission
branch: fix/OTC-20260907-docker-candidate-inventory-compatibility
base_branch: main
base_main: 9736b38e9c8aa54833716ac63a75e93e5415cc92
execution_mode: github_actions_owner_comment
execution_class: synology_physical_runtime
physical_e2e_required: true
runtime_access: canonical_bootstrap
runtime_owner_task: OTC-20260907-same-boot-zero-client-bootstrap-v2-live
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
live_runtime_authorization_source: OWNER_CHAT_20260907_CONTINUE_NATIVE_LOGIN_CLOSURE
parent_task: OTC-20260907-docker-candidate-inventory-compatibility
depends_on:
  - OTC-20260907-same-boot-zero-client-recovery-v2-live
---

# Plain exact-current Kasm restore v2 — live bootstrap admission

This task becomes executable only after the v2 same-boot invalidation has atomically removed the stale registration under its own current canonical lease.

The task authorizes exactly one reviewed `kasm-bootstrap` create-new transition for the canonical container `otclient-track-a-kasmvnc`, under `TRACK_A_CANONICAL_KASM_RUNTIME_SCOPE_V1`. Candidate uniqueness is scoped to that container only. Unrelated containers on the Synology host are outside Track A and are not inspected or executed into.

The scoped worker/probe retain the existing exact size/SHA/start, window, package, boot and registration proofs inside canonical Kasm. The scoped transition records truthful provenance as `inventory_scope: canonical_kasm_container` while remaining backward-compatible with the existing stale registration.

The transition must freshly prove registration absence, exactly one canonical Kasm container/display, exact current package identity, zero official-client candidates/windows inside that container and current canonical lease before launching anything. It may create one plain exact-current official Linux client and must stop at `existing_runtime_adoption_v1`, `candidate_count: 1`, `inventory_scope: canonical_kasm_container`, `state: UNKNOWN`.

No credential source, native auth, login, character selection, GUI input, gameplay or helper preload is authorized. The process-creation budget is consumed even if later bootstrap/adoption registration proof fails.

After PASS, the parent native-login programme must run a fresh trusted-main proven-login PRECHECK before any instrumented replacement or credential-bearing action.
