---
task_id: OTC-20260828-current-qt-world-correlation
status: implementing
phase: deep_qt_transition_logger_preparation
agent: ChatGPT
session_role: runtime_observer
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: experiment
policy_version: 2
branch: research/OTC-20260828-qt-lifecycle-transition-logger
base_branch: main
base_sha: adb64111976e3dfe896992267b53e7640b188969
risk: high
execution_mode: github_only
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
canonical_boot_epoch_recovery: NOT_APPLICABLE
canonical_recovery: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
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
current_client_version: 15.32.75d4a0
current_client_size: 52105824
current_client_sha256: d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
window_transition_run: 33156199089
window_transition_world_context_at: 2026-08-28T10:42:10.702+02:00
owner_world_visible_marker: 2026-08-28T10:42:41+02:00
positive_world_snapshot_run: 33157939977
positive_world_snapshot_job: 98805119085
character_select_snapshot_run: 33158299105
character_select_snapshot_job: 98806302500
login_screen_snapshot_run: 33158689867
login_screen_snapshot_job: 98807590332
three_state_same_pid: 13947
three_state_same_start_ticks: 51652120
three_state_auth_member_offset: 0x8d0
three_state_auth_qstate_raw: 0
three_state_auth_qstate_running: false
three_state_player_protocol_handler_count: 1
three_state_gameserver_game_session_count: 1
three_state_worldmap_protocol_handler_count: 1
three_state_disconnect_reaction_controller_count: 1
three_state_discriminator_result: REJECTED_LONG_LIVED_OBJECT_MARKERS
current_blocker: DEEP_QT_TRANSITION_LOGGER_NOT_ON_TRUSTED_MAIN
next_action: qualify and merge a deep read-only lifecycle logger that tracks candidate QState values for authentication/gameserver-login/character-selection/disconnect controllers plus PID-owned TCP counts and boolean window context, then start it at LOGIN_SCREEN and have the owner authenticate manually only after LOGGER_READY
---

# Current Qt world correlation

The exact-current positive world sample, character-selection control and login-screen control all used the same official-client PID `13947` and start ticks `51652120`. The previously sampled markers were identical across all three states: auth member `+0x8d0`, auth QState raw `0` / running `false`, plus one heap vptr hit each for player protocol handler, gameserver game session, worldmap handler and disconnect-reaction controller.

Those markers are therefore rejected as standalone `IN_GAME` discriminators. Their object lifetimes outlive world exit and account logout.

The successor experiment is a bounded read-only transition logger. It may dynamically resolve exact-current RTTI/vptr identities and retain only candidate QState lifecycle integers, type hit counts, PID-owned TCP socket counts, boolean window context and exact process identity. It must retain no heap bytes, addresses, socket endpoints, credentials, session secrets, packet payloads, process environment or raw window titles.

The owner will perform any future authentication and character selection manually only after `LOGGER_READY=true`. The agent performs no GUI input, login, character selection or gameplay. No `IN_GAME` semantic promotion is allowed until a discriminator is causally observed through the login -> character selection -> world transition and independently reviewed.
