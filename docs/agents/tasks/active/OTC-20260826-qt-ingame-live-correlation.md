---
task_id: OTC-20260826-qt-ingame-live-correlation
status: active
phase: runtime_preparation
agent: ChatGPT
session_role: owner
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: experiment
policy_version: 2
branch: runtime/OTC-20260826-qt-ingame-live-correlation
base_branch: main
base_sha: 8c7bc507aa5c1118aca0b8252dc422675add1be0
risk: high
execution_mode: self_hosted
runtime_access: read_only
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: synology:otclient-track-a-kasmvnc:display-1
canonical_registration: PRESENT
canonical_lease_generation: 35
registration_generation: 8
registration_lease_generation: 35
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
owner_manual_login_expected: true
owner_manual_character_selection_expected: true
network_payload_capture_allowed: false
network_metadata_capture_allowed: true
physical_action_budget: 0
physical_action_count: 0
semantic_promotion_performed: false
preflight_workflow_run: 33018520505
preflight_job: 98342820641
preflight_result: PASS
preflight_pid: 646
preflight_process_start_ticks: 1394843
preflight_auth_state_machine_running: false
preflight_player_position_available: true
current_blocker: NONE_LOGGER_INSTALL_PENDING
next_action: install a trusted-main owner-gated read-only live correlation workflow, then run it while the owner manually authenticates and selects a character
---

# Qt in-game live correlation

One bounded physical observation experiment on the already-running exact official client. The agent does not type, click, log in, select a character, move the character or access credentials. The owner performs authentication and character selection manually through the remote-view UI.

The logger may retain only timestamped secret-free state: exact Qt authentication `QStateMachine` lifecycle state, player-state mirrored coordinates, binary window-context state, and aggregate per-process TCP metadata such as connection count/queue or byte-counter deltas when available. It must never retain keyboard input, email, password, tokens, cookies, session secrets, process environment, packet payloads, chat text or raw window titles.

Fresh trusted-main preflight run `33018520505` on `synology-otclient-01` proved one exact target, one matching Tibia window, canonical registration/lease generation 35, target uniqueness PROVEN and read-only admission for PID 646/start 1394843. Current auth lifecycle was `authentication_state_machine_running=false`; player-state remained AVAILABLE with mirrored coordinates, demonstrating that player-state availability alone is not sufficient IN_GAME proof.
