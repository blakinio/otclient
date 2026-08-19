---
task_id: OTC-20260819-track-a-one-shot-native-login
status: active
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: bounded_runtime_login
branch: runtime/OTC-20260819-track-a-one-shot-native-login
base_branch: main
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260819-track-a-one-shot-native-login
runtime_namespace: docker:otclient-track-a-kasmvnc/display:1
target_uniqueness: PROVEN
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
mutation_authorized: true
credentials_allowed: true
credentials_scope: bounded_one_shot_native_auth_only
gui_input_authorized: false
second_live_session_authorized: false
owned_paths:
  - docs/agents/tasks/active/OTC-20260819-track-a-one-shot-native-login.md
modules_touched:
  - Track A KasmVNC runtime
reuses:
  - tools/tibia_runtime_bridge/current_sha_native_login_gate.py
  - tools/tibia_runtime_bridge/current_sha_secret_ingress.cpp
  - tools/tibia_runtime_bridge/experimental_character_control_current.cpp
  - docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md
---

# Goal
Perform exactly one owner-authorized native login on the existing unique Track A KasmVNC sandbox without GUI credential entry, then prove structural IN_GAME.

# Admission facts
Fresh preflight on Synology proved container `otclient-track-a-kasmvnc` running, `DISPLAY=:1` connectable, exactly one official client PID `11365`, executable `/home/kasm-user/otclient-track-a/Tibia-32177065988-1/bin/client`, size `52109920`, SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`.

The Kasm container is treated as the task-owned isolated namespace for this one-shot operation. It is not declared canonical and no canonical registration/lease state is fabricated. Current owner instruction explicitly authorizes one use of `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD` only through bounded native-auth ingress. No GUI login, OCR, image matching, coordinate input, blind keyboard/mouse, TLS/auth bypass or second account session is authorized.

# Success gate
`CHARACTER_ACTUALLY_LOGGED_INTO_GAME=YES` plus exactly one validated hit for `player_protocol_handler`, `gameserver_game_session`, and `worldmap_handler`. If native character count is not exactly one, fail closed.