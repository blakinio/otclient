---
task_id: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
status: implementing
agent: ChatGPT
session_id: chatgpt-worldmap-server-delivery-causal-20260817-v18
session_role: isolated_runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: baseline_native_single_character_confirmation_v18_world_entry_screenshot
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
base_branch: main
updated: 2026-08-18T00:22:00+02:00
risk: critical
related_pr: 475
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
runtime_namespace: worldmap-causal-baseline-ephemeral-v1
PHYSICAL_E2E_REQUIRED: true
credentials_allowed: true
login_allowed: true
gameplay_allowed: true
eighth_baseline_login_attempt_authorized: true
second_live_session_authorized: false
owner_authorization_source: current conversation
owner_authorization_text: "dokoncz zadanie"
owner_authorization_scope: exactly one additional sequential baseline login attempt for v18 after v17b consumed the seventh attempt; v18 may only use current-session native character state discovered after legitimate account authentication; the authenticated native characterList cardinality is runtime-proven as exactly one, therefore native index 0 is the only deterministic selection; no character name, row order, screenshot/OCR or memory from another session may influence selection; invoke native onCharacterSelectionConfirmed so the original client itself constructs TCharacterLoginData and performs game login; accept completion only on FullMap plus at least 10 map-description strips and one post-structural map screenshot; no parallel session
owner_funded_ai_api_authorized: false
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
native_qmeta_corrected:
  character_selection_static_metacall_va: '0x00d46550'
  invoke_method_jump_table_va: '0x01d7701c'
  request_character_login_method_index: 0
  request_character_login_case_va: '0x00d46930'
  on_character_selection_confirmed_method_index: 11
  on_character_selection_confirmed_case_va: '0x00d46900'
  on_character_selection_confirmed_impl_va: '0x00856550'
  property_read_jump_table_va: '0x01d77084'
  old_d47300_classification: property_read_accountPremiumStatus
native_vptrs:
  character_selection_controller: '0x0308ed68'
  game_client: '0x03076908'
launch_budget:
  baseline_ephemeral_login_max: 8
  baseline_ephemeral_login_consumed: 7
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
ci_check_generation: v18_native_single_character_confirmation
---

# Objective

Reach the real game world on the exact official Linux client, prove `IN_GAME` structurally with pre-Storage `FullMap` plus at least 10 map-description strip records, and persist one cropped map-only screenshot. The owner stop condition remains successful world entry plus screenshot.

# Proven account login

V13 and later physical runs prove protected credential handoff, non-empty protected fields, real Login submission, local SOCKS activity and persistent post-login UI transition. Account authentication is not the blocker.

# Corrected native character control

Exact-SHA static recovery proves:

```text
TCharacterSelectionController::qt_static_metacall = 0xd46550
InvokeMetaMethod table                              = 0x1d7701c
requestCharacterLogin method index 0               = case 0xd46930
onCharacterSelectionConfirmed method index 11      = case 0xd46900
onCharacterSelectionConfirmed implementation       = 0x856550
PropertyRead table                                  = 0x1d77084
0xd47300                                             = accountPremiumStatus property read
```

The generated QMeta case for method 11 is a direct non-owning pass-through:

```asm
d46900: mov rsi, qword ptr [r12 + 8]
...
d46916: jmp 0x856550
```

Thus argv[1] is passed as `QList<int> const&` to the implementation without a QMeta-side copy.

# V17b terminal discriminator

Run `32074894984`, physical job `95525929518`, consumed the seventh baseline login. Mandatory pre-secret gates, account login, transport and post-login transition passed. Sanitized native runtime markers:

```text
WORLDMAP_V17_POSTAUTH_CHARSEL_INSTANCE_COUNT=1
WORLDMAP_V17_RUNTIME_ADDRESS_PROVEN=PASS
WORLDMAP_V17_NATIVE_CHARACTER_LIST_COUNT=1
WORLDMAP_V17_NATIVE_SELECTED_LOGIN_DATA_COUNT=0
WORLDMAP_V17_SEMANTIC_RESULT=FAIL:single_native_selected_login_data_not_proven
```

Cleanup/source rehash passed. This is a material positive discriminator: the current authenticated account exposes exactly one native character object. No external identity is needed; index `0` is the only possible current-session selection.

# Exact onCharacterSelectionConfirmed behavior

Static run `32075412911 / 95527418954` proves `0x856550`:

1. receives `this` in RDI and `QList<int> const&` in RSI;
2. clears the controller-owned previous `TCharacterLoginData` vector at `this+0x140..+0x148`;
3. reads the incoming selection list data pointer at `list+0x8` and size at `list+0x10`;
4. validates every selected index against native `characterList` count at `this+0x108`;
5. fetches the corresponding native QObject from `this+0x100 + index*8`;
6. QMeta-casts it to the character information model;
7. copies/refcounts the real model/session fields and constructs controller-owned `TCharacterLoginData` objects;
8. emits/activates the native request path using those client-owned objects.

Therefore v18 must invoke method 11 with the single current-session index `0`. It must not synthesize `TCharacterLoginData`.

# V18 execution contract

1. repeat exact SHA/XID/XRes/GDB/pre-Storage/editability gates;
2. perform the already-proven legitimate account login;
3. require exactly one post-auth `TCharacterSelectionController` instance;
4. require `characterList` cardinality exactly `1`;
5. prove the exact callee only observes the input `QList<int>` selection range and does not take ownership of it; use an ABI-proven transient const selection frame for exactly one integer `0`, or a Qt-owned constructed list if the static gate finds a suitable constructor/allocator;
6. switch to the main LWP and require Qt thread affinity before invocation;
7. invoke `qt_static_metacall(charsel, InvokeMetaMethod, 11, argv)` so the native client executes `onCharacterSelectionConfirmed`;
8. require the client-owned selected `TCharacterLoginData` vector to become non-empty and the normal native game-login chain to continue;
9. accept success only when `FullMap` plus >=10 map-description strips are observed;
10. only then capture exact manifest-owned XID, export map PNG, delete transient XWD, persist screenshot and cleanup.

# Required result

```text
ACCOUNT_LOGIN_TRANSPORT=PASS
POSTAUTH_CHARACTER_CONTROLLER_PROVENANCE=PASS
NATIVE_CHARACTER_LIST_COUNT=1
NATIVE_SELECTION_INDEX=0
QT_THREAD_AFFINITY=PASS
NATIVE_CHARACTER_CONFIRMATION_QMETA=PASS
NATIVE_SELECTED_LOGIN_DATA_AFTER_CONFIRMATION>=1
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
checkpoint_version: 29
status: implementing
phase: baseline_native_single_character_confirmation_v18_world_entry_screenshot
baseline_login_max: 8
baseline_login_consumed: 7
patched_login_consumed: 0
last_completed_step: v17b physically proved one post-auth character controller, exact runtime address, and native characterList count exactly 1; its direct request path failed only because selected TCharacterLoginData cache is correctly empty before confirmation; cleanup/source rehash passed
blockers: []
next_action: finish exact-SHA const-QList selection-frame ownership proof, then run v18 method-11 native confirmation for the sole runtime character index 0 and require FullMap plus screenshot
```
