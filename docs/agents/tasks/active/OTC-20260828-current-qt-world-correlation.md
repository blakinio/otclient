---
task_id: OTC-20260828-current-qt-world-correlation
status: implementing
phase: positive_world_snapshot_preparation
agent: ChatGPT
session_role: runtime_observer
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: experiment
policy_version: 2
branch: research/OTC-20260828-current-qt-world-correlation
base_branch: main
base_sha: 653d0ade05833ae5e56381e074458c0f7758bf24
risk: high
execution_mode: self_hosted
runtime_access: read_only
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: synology:otclient-track-a-kasmvnc:display-1
canonical_registration: PRESENT
canonical_lease_generation: UNKNOWN
registration_generation: UNKNOWN
registration_lease_generation: UNKNOWN
gate_a: NOT_APPLICABLE
canonical_boot_epoch_recovery: NOT_APPLICABLE
canonical_recovery: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: false
credentials_allowed: false
login_allowed: false
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
physical_action_budget: 0
physical_action_count: 0
semantic_promotion_performed: false
source_world_visible_owner_marker: 2026-08-28T10:42:41+02:00
source_window_observer_run: 33156199089
source_window_observer_job: 98799434315
source_window_observer_target_admission: PASS
current_client_version: 15.32.75d4a0
current_client_size: 52105824
current_client_sha256: d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
current_blocker: SNAPSHOT_WORKFLOW_NOT_YET_ON_TRUSTED_MAIN
next_action: qualify and merge the bounded read-only Qt world snapshot, then capture one positive-world sample from the already owner-authenticated session without input or gameplay
---

# Current Qt world correlation

Capture one bounded positive-world sample while the owner is already authenticated and visibly in the game world. The agent performs no GUI input, login, character selection, movement, gameplay, process control or credential access.

The snapshot may read the exact process memory only to resolve already-identified RTTI/vptr object identities, dynamically prove the `TGameClient -> TAuthenticationProcessController` member relation, and read the exact-fenced Qt `QStateMachine::isRunning()`-equivalent lifecycle field when the mapped StateMachine library hash matches the previously reviewed layout. Heap bytes, arbitrary fields, credentials, session secrets, packet payloads, process environment and raw window titles are never retained.

This sample is positive correlation evidence only. It must keep `in_game_claimed=false` and `semantic_promotion_performed=false` until separately captured login/character-select negative/control samples establish a discriminator that survives the known `BRIDGE_3_OF_3` false positive.
