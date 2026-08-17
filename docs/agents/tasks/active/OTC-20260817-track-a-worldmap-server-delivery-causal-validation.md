---
task_id: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
status: implementing
agent: ChatGPT
session_id: chatgpt-worldmap-server-delivery-causal-20260818-v19
session_role: isolated_runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: baseline_native_game_login_v19_world_entry_screenshot
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
base_branch: main
updated: 2026-08-18T00:45:00+02:00
risk: critical
related_pr: 475
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
runtime_namespace: worldmap-causal-baseline-ephemeral-v1
PHYSICAL_E2E_REQUIRED: true
credentials_allowed: true
login_allowed: true
gameplay_allowed: true
ninth_baseline_login_attempt_authorized: true
second_live_session_authorized: false
owner_authorization_source: current conversation
owner_authorization_text: "dokoncz zadanie"
owner_authorization_scope: exactly one additional sequential baseline login attempt for v19 after v18 consumed the eighth attempt; reuse the already-proven legitimate account-login and native single-character confirmation path unchanged; observe the exact downstream native game-login state-machine events; only if the v18 character confirmation has built controller-owned TCharacterLoginData and emitted requestCharacterLogin but the connected authentication transition does not fire, v19 may invoke the original TAuthenticationProcessController QMeta method requestCharacterGameserverLogin() on its unique live post-auth object after runtime-address and Qt-thread-affinity proof; no auth/session fabrication, no packet synthesis, no coordinate/OCR character control; completion remains FullMap plus >=10 strips plus post-structural screenshot; no parallel session
owner_funded_ai_api_authorized: false
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
native_character_control:
  character_selection_static_metacall_va: '0x00d46550'
  on_character_selection_confirmed_method_index: 11
  on_character_selection_confirmed_impl_va: '0x00856550'
  request_character_signal_activate_va: '0x00856880'
  character_selection_vptr: '0x0308ed68'
native_auth_control:
  auth_static_metacall_va: '0x00cfabb0'
  auth_vptr: '0x0307f1b0'
  request_character_gameserver_login_method_index: 5
  request_character_gameserver_login_case_va: '0x00cfb2e7'
  start_game_server_login_case_va: '0x00cfb122'
native_gameclient_control:
  gameclient_vptr: '0x03076908'
  connect_existing_credentials_va: '0x00d06660'
  on_connect_gameserver_va: '0x00d06810'
  abort_gameserver_connect_va: '0x00d067b0'
  game_session_connected_va: '0x00d066e0'
  game_session_login_successful_va: '0x00d066c8'
  game_session_login_error_va: '0x00d064d8'
  game_session_disconnected_va: '0x00d064c8'
launch_budget:
  baseline_ephemeral_login_max: 9
  baseline_ephemeral_login_consumed: 8
  patched_ephemeral_login_max: 1
  patched_ephemeral_login_consumed: 0
  simultaneous_logged_in_sessions_max: 1
safety:
  direct_unapproved_egress: forbidden
  warp_socks_required: true
  raw_client_commit_or_upload: forbidden
  credentials_in_logs_or_artifacts: forbidden
  screenshots_or_ocr_artifacts: map_only_post_structural_screenshot_authorized
  ocr: forbidden
  transient_xwd_only: true
  screenshot_source_xwd_must_be_deleted: true
  screenshot_login_or_character_selection: forbidden
  broad_process_cleanup: forbidden
  canonical_source_patch_in_place: forbidden
  rollback_required: true
  coordinate_character_selection_control: forbidden
ci_check_generation: v19_downstream_game_login
---

# Objective

Reach the real game world on the exact official Linux client, prove `IN_GAME` structurally with pre-Storage `FullMap` plus at least 10 map-description strip records, and persist one cropped map-only screenshot. The owner stop condition remains successful world entry plus screenshot.

# Proven upstream chain

The following are now physically proven and are no longer hypotheses:

```text
LEGITIMATE_ACCOUNT_LOGIN=PASS
POST_LOGIN_TRANSPORT_ACTIVITY=PASS
POST_LOGIN_UI_TRANSITION=PASS
POSTAUTH_CHARACTER_CONTROLLER_PROVENANCE=PASS
NATIVE_CHARACTER_LIST_COUNT=1
NATIVE_SELECTION_INDEX=0
QT_THREAD_AFFINITY_FOR_CHARACTER_CONFIRMATION=PASS
NATIVE_CHARACTER_CONFIRMATION_QMETA=PASS
TCHARACTERLOGINDATA_VECTOR_BEFORE=0
TCHARACTERLOGINDATA_VECTOR_AFTER=1
REQUEST_CHARACTER_LOGIN_SIGNAL_EMISSION=PROVEN_STATIC_AT_0x856880
```

V18 physical run `32076063134 / 95529595652` consumed baseline login 8 and emitted:

```text
WORLDMAP_V18_POSTAUTH_CHARSEL_INSTANCE_COUNT=1
WORLDMAP_V18_RUNTIME_ADDRESS_PROVEN=PASS
WORLDMAP_V18_NATIVE_CHARACTER_LIST_COUNT=1
WORLDMAP_V18_NATIVE_CHARACTER_LIST_DISCOVERY=PASS
WORLDMAP_V18_NATIVE_SELECTION_INDEX=0
WORLDMAP_V18_QT_THREAD_AFFINITY=PASS
WORLDMAP_V18_SELECTED_LOGIN_DATA_BEFORE=0
WORLDMAP_V18_CONST_SELECTION_VIEW=PASS
WORLDMAP_V18_SELECTED_LOGIN_DATA_AFTER=1
WORLDMAP_V18_NATIVE_CHARACTER_CONFIRMATION_QMETA=PASS
WORLDMAP_V18_SEMANTIC_RESULT=PASS
```

It then failed only because `FullMap` was not observed. Cleanup/source rehash passed.

# Exact downstream static correction/proof

Exact-SHA QMeta enumeration v19 revalidated AUTH and GAMECLIENT addresses. The relevant original client transitions are:

```text
TAuthenticationProcessController::requestCharacterGameserverLogin() -> 0xcfb2e7
TAuthenticationProcessController::onStartGameServerLoginStateEntered   -> 0xcfb122
TGameClient::connectClientToGameserverWithExistingCredentials()       -> 0xd06660
TGameClient::onConnectClientToGameserver                              -> 0xd06810
TGameClient::abortClientConnectToGameserver                           -> 0xd067b0
TGameClient::onGameSessionConnected                                   -> 0xd066e0
TGameClient::onGameSessionLoginSuccessful                             -> 0xd066c8
TGameClient::onGameSessionLoginError                                  -> 0xd064d8
TGameClient::onGameSessionDisconnected                                -> 0xd064c8
```

Static confirmation-tail run `32076966187 / 95532124926` proves `onCharacterSelectionConfirmed` emits QMeta signal index 0 at `0x856880` after building the selected `TCharacterLoginData`. Thus the current blocker is strictly propagation from that emitted native character-login signal into the authentication/game-server state machine.

# V19 execution contract

1. repeat the exact v18 account-login + native method-11 confirmation path unchanged;
2. arm correct pre-Storage breakpoints before login for:
   - `0x856880` request-character signal activation;
   - `0xcfb2e7` request-character-gameserver-login;
   - `0xcfb122` start-game-server-login;
   - `0xd06660` connect-existing-credentials;
   - `0xd06810` on-connect-gameserver;
   - `0xd067b0` abort-gameserver-connect;
   - `0xd066e0` game-session-connected;
   - `0xd066c8` game-session-login-successful;
   - `0xd064d8` game-session-login-error;
   - `0xd064c8` game-session-disconnected;
3. after native character confirmation PASS, wait a short bounded interval and compute event deltas without logging payloads;
4. if `RequestCharacterLoginSignalActivate>0` and `RequestCharacterGameserverLogin==0`, locate exactly one post-auth `TAuthenticationProcessController` by relocated vptr, prove current exact-SHA runtime address and Qt thread affinity, then invoke its original `qt_static_metacall(this, InvokeMetaMethod, method_id=5, argv)` with no user arguments;
5. do not perform that fallback if the normal connected transition has already fired;
6. after any allowed fallback, require downstream progress and surface only sanitized event counts/categories;
7. any explicit GameSessionLoginError/Abort is a fail-closed runtime result, not a reason to synthesize a protocol packet;
8. success remains only `FullMap` plus >=10 strip records;
9. only after structural IN_GAME, capture exact manifest-owned XID, export cropped PNG, delete transient XWD, persist screenshot and cleanup.

# Required result

```text
ACCOUNT_LOGIN_TRANSPORT=PASS
NATIVE_CHARACTER_CONFIRMATION_QMETA=PASS
REQUEST_CHARACTER_SIGNAL>0
REQUEST_CHARACTER_GAMESERVER_LOGIN>0
START_GAME_SERVER_LOGIN>0
GAME_SERVER_CONNECT_STARTED>0
GAME_SESSION_CONNECTED_OR_LOGIN_SUCCESS>0
STRUCTURAL_IN_GAME=PASS
MAP_SCREENSHOT=PASS
```

# Wider causal result boundary

```text
SERVER_MAP_DELIVERY_MODEL=UNKNOWN
PATCH_CAUSES_ADDITIONAL_AUTHORITATIVE_MAP_DATA=UNKNOWN
BASELINE_AUTHORITATIVE_INBOUND_EXTENT=UNKNOWN
PATCHED_AUTHORITATIVE_INBOUND_EXTENT=UNKNOWN
OUTBOUND_EXTENT_NEGOTIATION_CHANGE=UNKNOWN
STORAGE_EXTENT_CHANGE=UNKNOWN
RENDER_PICKER_EXTENT_CHANGE=UNKNOWN
```

# Checkpoint

```yaml
checkpoint_version: 30
status: implementing
phase: baseline_native_game_login_v19_world_entry_screenshot
baseline_login_max: 9
baseline_login_consumed: 8
patched_login_consumed: 0
last_completed_step: v18 physically completed native single-character confirmation and built one client-owned TCharacterLoginData; v19 static proof confirms the confirmation emits requestCharacterLogin signal index 0, while no FullMap followed
blockers: []
next_action: execute one v19 downstream state-machine discriminator with conditional original-AUTH QMeta transition only if the normal character signal does not propagate, then stop only at FullMap+screenshot or an explicit native game-login failure state
```
