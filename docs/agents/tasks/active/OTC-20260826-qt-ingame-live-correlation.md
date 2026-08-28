---
task_id: OTC-20260826-qt-ingame-live-correlation
status: waiting
phase: waiting_owner_manual_login
agent: ChatGPT
session_role: owner
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: experiment
policy_version: 2
branch: docs/OTC-20260826-qt-ingame-live-correlation-checkpoint
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
logger_pr: 718
logger_merge_commit: e621a1407d124a71dc9437912e1676aa8929cc11
view_proxy_fix_pr: 720
view_proxy_fix_merge_commit: ce0884d5ef2d69a11bab3189f62ed4fef22b0ff6
owner_comment_trigger_pr: 723
owner_comment_trigger_merge_commit: faf3018d520f58ad7841cf3819b16ef159f27148
network_probe_fix_pr: 726
network_probe_fix_merge_commit: e81c1c67d33adfa541d4e4222d796cc2c1198ad3
persistent_lan_view_pr: 727
persistent_lan_view_merge_commit: 39f46d3c64c28e2f02366ca9fac5c58e743b8bf0
persistent_lan_frontend: http://192.168.1.21:16084/
persistent_lan_websocket: https://192.168.1.21:16083/websockify
persistent_lan_endpoint_probe: PASS_HTTP_200_AND_WEBSOCKET_101_RFB_003_008
correlation_workflow_ready: true
correlation_dispatch_pending: true
owner_comment_trigger_attempt_comment: 5450054574
owner_comment_trigger_attempt_run: 33154083180
owner_comment_trigger_attempt_result: PASS
correlation_dispatch_attempt_run: 33154087797
correlation_dispatch_attempt_result: SKIPPED_PRE_RUNTIME
correlation_dispatch_attempt_actor: github-actions[bot]
trigger_repair_root_cause: GITHUB_TOKEN_WORKFLOW_DISPATCH_LOSES_OWNER_ACTOR
trigger_repair_tdd_red: PASS_EXPECTED_FAILURE
trigger_repair_tdd_green: PASS
trigger_repair_scope: actor-preserving reusable workflow_call plus deterministic source contract
last_progress_at: 2026-08-28T10:05:33+02:00
current_blocker: WAITING_OWNER_MANUAL_LOGIN_CAPABILITY
next_action: when the owner is ready to authenticate manually, dispatch exactly one trusted-main ONE_SHOT_QT_INGAME_CORRELATION run and capture the login -> character selection -> world transition; the agent performs zero GUI input/login/character selection/gameplay and does not promote semantics from an incomplete observation
---

# Qt in-game live correlation

One bounded physical observation experiment on the already-running exact official client. The agent does not type, click, log in, select a character, move the character or access credentials. The owner performs authentication and character selection manually through the remote-view UI.

The logger may retain only timestamped secret-free state: exact Qt authentication `QStateMachine` lifecycle state, player-state mirrored coordinates, binary window-context state, and aggregate per-process TCP metadata such as connection count/queue or byte-counter deltas when available. It must never retain keyboard input, email, password, tokens, cookies, session secrets, process environment, packet payloads, chat text or raw window titles.

Fresh trusted-main preflight run `33018520505` on `synology-otclient-01` proved one exact target, one matching Tibia window, canonical registration/lease generation 35, target uniqueness PROVEN and read-only admission for PID 646/start 1394843. Current auth lifecycle was `authentication_state_machine_running=false`; player-state remained AVAILABLE with mirrored coordinates, demonstrating that player-state availability alone is not sufficient IN_GAME proof.
