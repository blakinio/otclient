---
task_id: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
status: implementing
agent: ChatGPT
session_id: chatgpt-worldmap-server-delivery-causal-20260817-v17
session_role: isolated_runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: baseline_native_semantic_character_v17_world_entry_screenshot
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
base_branch: main
updated: 2026-08-17T23:58:00+02:00
risk: critical
related_pr: 475
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
runtime_namespace: worldmap-causal-baseline-ephemeral-v1
PHYSICAL_E2E_REQUIRED: true
credentials_allowed: true
login_allowed: true
gameplay_allowed: true
seventh_baseline_login_attempt_authorized: true
second_live_session_authorized: false
owner_authorization_source: current conversation
owner_authorization_text: "dokoncz zadanie"
owner_authorization_scope: one additional sequential real baseline login attempt may be used only by the native-semantic v17 path after exact-SHA static vptr/QMeta/ABI proof and the already-completed no-secret lifecycle discriminator; because AUTH/CHARSEL are proven lifecycle-dependent and absent at the login form, their live object provenance must be established after legitimate account authentication and before any semantic character invocation; no character identity may be imported from memory/chat; character choice must come only from current native runtime state; IN_GAME remains FullMap plus map-description strips; one map-only screenshot only after structural IN_GAME; no parallel session
owner_funded_ai_api_authorized: false
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
native_qmeta_corrected:
  character_selection_static_metacall_va: '0x00d46550'
  invoke_method_jump_table_va: '0x01d7701c'
  property_read_jump_table_va: '0x01d77084'
  request_character_login_method_index: 0
  request_character_login_case_va: '0x00d46930'
  on_character_selection_confirmed_method_index: 11
  on_character_selection_confirmed_case_va: '0x00d46900'
  on_character_selection_confirmed_impl_va: '0x00856550'
  old_d47300_classification: property_read_accountPremiumStatus
  old_d47130_classification: property_read_case_not_character_confirmation
native_vptrs:
  authentication_process_controller: '0x0307f1b0'
  character_selection_controller: '0x0308ed68'
  game_client: '0x03076908'
  login_request_uploader: '0x030d36f8'
launch_budget:
  baseline_ephemeral_login_max: 7
  baseline_ephemeral_login_consumed: 6
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
ci_check_generation: v17_native_semantic_character_login
---

# Objective

Reach the real game world on the exact official Linux client, prove `IN_GAME` structurally with pre-Storage `FullMap` plus at least 10 map-description strip records, and persist one cropped map-only screenshot. The current user stop condition is successful world entry plus screenshot.

# Proven account-login chain

V13 physical rerun `32067963829 / 95506276673` proved protected credential handoff, non-empty protected fields, real Login submission, local SOCKS activity and persistent post-login UI transition. Account authentication is not the current blocker.

# V14 correction

Run `32069479572 / 95509250730` consumed the sixth baseline login and did not produce `FullMap`. Its historical negative `RequestCharacterLogin` discriminator is invalid because the breakpoint was placed at `0xd47300`.

Exact-SHA v16 QMeta recovery proved:

```text
TCharacterSelectionController::qt_static_metacall = 0xd46550
InvokeMetaMethod jump table                         = 0x1d7701c
requestCharacterLogin method index 0               = case 0xd46930
onCharacterSelectionConfirmed method index 11      = case 0xd46900
PropertyRead jump table                             = 0x1d77084
0xd47300                                             = accountPremiumStatus property read
```

Therefore v14 proves only that its bounded GUI stimuli did not produce structural world entry. It does not prove that native `requestCharacterLogin` was absent.

# Native model proof

Exact-SHA static recovery proved:

```text
characterList     : QList<QObject*>
lastSelectedIndex : int
getCharacterIndexForSearchString(QString) -> int
```

`onCharacterSelectionConfirmed(QList<int>)` implementation is `0x856550`. It consumes selected native character indexes, validates them against the controller's live list, resolves native character model/session data, creates `TCharacterLoginData`, and drives the native request path.

The controller also owns a native `TCharacterLoginData` vector at offsets `+0x140..+0x148`, with `0x70`-byte elements. A v17 direct semantic request is permitted only when this current-session vector contains exactly one live element; no synthetic `TCharacterLoginData` may be constructed.

# Lifecycle/object-provenance correction

The no-secret physical discriminator found exactly one live `TGameClient` at the login form but zero AUTH/CHARSEL/UPLOADER controller instances. This is a lifecycle result, not a provenance failure: character-selection objects are created after legitimate account authentication.

V17 therefore requires:

1. exact SHA, XID/XRes, GDB and pre-Storage gates before secrets;
2. normal proven account-login submission and transport/UI proof;
3. only then read-only scan for the exact relocated `TCharacterSelectionController` primary vptr and require exactly one live instance;
4. verify its executable mapping/load bias and `qt_static_metacall` instruction bytes;
5. switch GDB to the main LWP and prove Qt thread affinity by comparing `QObject::thread(charsel)` with `QThread::currentThread()`;
6. inspect only non-secret structural model values: character-list cardinality and current native selected-login-data cardinality;
7. require exactly one current native selected `TCharacterLoginData` element; do not choose by name, order, row or memory from another session;
8. call `TCharacterSelectionController::qt_static_metacall(this, InvokeMetaMethod, 0, argv)` with an argv pointer to that already-live native `TCharacterLoginData` object;
9. allow the original client to perform game-server login;
10. accept success only on `FullMap` plus >=10 strip records;
11. only then capture the exact manifest-owned XID, export the cropped PNG, delete transient XWD and persist the screenshot.

If step 7 is not satisfied, v17 fails closed without inventing a character or fabricating a non-trivial Qt/C++ object.

# Required result

```text
ACCOUNT_LOGIN_TRANSPORT=PASS
POSTAUTH_CHARACTER_CONTROLLER_PROVENANCE=PASS
QT_THREAD_AFFINITY=PASS
NATIVE_CHARACTER_LIST_DISCOVERY=PASS
NATIVE_SELECTED_LOGIN_DATA_COUNT=1
NATIVE_CHARACTER_QMETA_INVOCATION=PASS
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
checkpoint_version: 28
status: implementing
phase: baseline_native_semantic_character_v17_world_entry_screenshot
baseline_login_max: 7
baseline_login_consumed: 6
patched_login_consumed: 0
last_completed_step: exact-SHA v16 recovered the correct character QMeta method table, native character model properties, controller primary vptr and onCharacterSelectionConfirmed implementation; no-secret runtime proved GameClient exists preauth while AUTH/CHARSEL are lifecycle-dependent
blockers: []
next_action: static-compose v17 GDB post-auth semantic invocation, then execute the seventh sequential baseline login and stop only at FullMap+screenshot or a genuine fail-closed native-model condition
```
