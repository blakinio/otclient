---
task_id: OTC-20260828-current-qt-world-correlation
status: implementing
phase: world_entered_semantic_anchor_static_recovery
agent: ChatGPT
session_role: runtime_observer
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: experiment
policy_version: 2
branch: research/OTC-20260828-world-entered-semantic-anchor
base_branch: main
base_sha: 7a7a7cc4d09dee08ea07f8c91144d8ac869111b7
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
deep_lifecycle_entry_run_1: 33159662745
deep_lifecycle_reverse_control_run: 33161071475
deep_lifecycle_entry_run_2: 33162761241
deep_lifecycle_same_pid: 13947
deep_lifecycle_same_start_ticks: 51652120
deep_lifecycle_causal_corridor: REPEATABLE_NOT_PROMOTED
deep_lifecycle_durable_evidence: docs/agents/evidence/OTC-20260828-current-qt-world-correlation
world_entered_historical_owner_type: tibia::game::TPlayerProtocolMessageHandler
world_entered_exact_current_anchor: UNKNOWN
current_blocker: EXACT_CURRENT_WORLD_ENTERED_SEMANTIC_ANCHOR_NOT_RECOVERED
next_action: recover exact-current TPlayerProtocolMessageHandler::worldEntered QMeta/signal anchor without historical address reuse; build a read-only semantic observer only after static recovery; preserve IN_GAME_CLAIMED=false until causal live validation and independent review
---

# Current Qt world correlation

The long-lived object-presence and authentication-running markers are rejected as standalone `IN_GAME` authority. Positive-world, character-selection and login-screen snapshots all used the same exact client process and produced the same object-presence/auth-running values.

The merged deep lifecycle logger then captured three secret-free same-process runs. Two owner-marked entries and one observer-only entry segment repeat the same causal corridor: authentication lifecycle transient -> gameserver-login QState candidate becomes unresolved -> PID-owned TCP count rises -> boolean world/character window context becomes true. The reverse control proves the transient auth/TCP/gameserver-login observations also participate in world exit and therefore are not durable gameplay state.

Durable evidence is retained at `docs/agents/evidence/OTC-20260828-current-qt-world-correlation/`, including exact JSONL from runs `33159662745`, `33161071475` and `33162761241`, artifact hashes, owner markers, reverse control and the explicit no-promotion verdict.

The next frontier is static exact-current recovery of the native `tibia::game::TPlayerProtocolMessageHandler::worldEntered` signal or a durable state directly caused by that signal. Historical QMeta addresses may be used only as background semantic evidence, never as current lookup keys. Any current anchor must be recovered from the exact `15.32.75d4a0` / `d1a16819...` ELF and independently reviewed.

The previous runtime container is no longer present on the Docker host. This is not evidence about client state. Any future live validation requires a fresh canonical runtime admission and exact process identity.

`IN_GAME_CLAIMED=false` and `semantic_promotion_performed=false` remain mandatory.
