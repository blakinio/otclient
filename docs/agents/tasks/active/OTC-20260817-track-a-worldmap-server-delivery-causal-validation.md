---
task_id: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
status: implementing
agent: ChatGPT
session_id: chatgpt-worldmap-server-delivery-causal-20260817-v15
session_role: isolated_runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: baseline_native_semantic_character_v15_world_entry_screenshot
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
base_branch: main
updated: 2026-08-17T23:26:00+02:00
risk: critical
related_pr: 475
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
runtime_namespace: worldmap-causal-baseline-ephemeral-v1
PHYSICAL_E2E_REQUIRED: true
target_uniqueness: UNKNOWN
mutation_authorized: false
credentials_allowed: true
login_allowed: true
gameplay_allowed: true
client_byte_mutation_authorized: true
bootstrap_for_worldmap_authorized: true
login_for_worldmap_authorized: true
sixth_baseline_login_attempt_authorized: true
seventh_baseline_login_attempt_authorized: true
second_live_session_authorized: false
owner_authorization_source: current conversation
owner_authorization_text: "dokoncz zadanjie w momencie zalogowania sie do gry i przedstawienia screnshota"
owner_authorization_scope: one additional sequential real baseline login attempt is authorized for v15 only after native controller object provenance, ABI entrypoint identity and GUI-thread invocation preconditions are proven without secrets; coordinate/pixel/Tab character-selection control is closed; target character must be selected semantically by exact name Invalid Monk; IN_GAME remains FullMap plus map-description strips; one map-only screenshot only after structural IN_GAME; no parallel session
owner_funded_ai_api_authorized: false
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
native_qmeta:
  auth_static_metacall_va: '0x00cfabb0'
  character_selection_static_metacall_va: '0x00d46550'
  request_character_login_method_index: 0
  request_character_login_target_va: '0x00d47300'
  advance_direct_character_selection_method_index: 2
  advance_direct_character_selection_target_va: '0x00cfadcb'
  provenance: PR-498 exact-SHA final static synthesis
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
  owner_funded_ai_api: forbidden
  coordinate_character_selection_control: forbidden_after_v14
ci_check_generation: v15_native_semantic_bridge
---

# Objective

Reach the real game world on the exact official Linux client, prove `IN_GAME` structurally with pre-Storage `FullMap` plus map-description strip records, and persist one cropped map-only screenshot. The current user stop condition is successful world entry plus screenshot.

# Proven account-login chain

V13 physical rerun `32067963829 / 95506276673` proved:

```text
WORLDMAP_BASELINE_CREDENTIAL_HANDOFF=RECEIVED_AFTER_PRESECRET_GATES
WORLDMAP_BASELINE_SECRET_FIELD_OCCUPANCY=PASS
WORLDMAP_BASELINE_LOGIN_SUBMITTED=true
WORLDMAP_V12_LOCAL_SOCKS_MAX=1
WORLDMAP_BASELINE_LOGIN_TRANSPORT_ACTIVITY=PASS
WORLDMAP_BASELINE_POST_LOGIN_UI_TRANSITION=PASS
```

Therefore account authentication is not the current blocker.

# V14 terminal discriminator

Run `32069479572`, physical job `95509250730`, consumed the sixth baseline login. All mandatory same-launch gates and account-login transport/UI proof passed. The following bounded UI stimuli all failed to increase the native `RequestCharacterLogin` counter and no `FullMap` was observed:

```text
RETURN_ONLY
CENTER_735_408
UP_735_384
DOWN_735_432
RIGHT_785_408
LEGACY_TRANSLATED_685_408
DOUBLECLICK_CENTER_735_408
```

Terminal boundary:

```text
WORLDMAP_BASELINE_ERROR=native_character_request_not_observed_after_bounded_v14_candidates
WORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=PASS
WORLDMAP_BASELINE_CLEANUP=COMPLETE
WORLDMAP_FINAL_NAMESPACE_PROCESS_COUNT=0
```

Coordinate/pixel/Tab character-selection control is therefore closed.

# Current-main native-first contract

`main@42aafde73f45ae997ec7629a5d321e2a49b110d6` promoted `OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME.md` (#501). It requires native object provenance and semantic character selection rather than UI coordinates.

Exact-SHA PR #498 established:

```text
TAuthenticationProcessController::qt_static_metacall @ 0xcfabb0
advanceStateMachineDirectlyToCharacterSelection() method index 2
TCharacterSelectionController::qt_static_metacall @ 0xd46550
requestCharacterLogin(...) method index 0
TCharacterSelectionController::requestCharacterLogin native target @ 0xd47300
```

The QMeta static-metacall boundary is preferred over direct jumps into internal switch-case targets.

# V15 execution contract

1. recover exact primary vptrs for `TAuthenticationProcessController`, `TCharacterSelectionController`, `TGameClient` and `TLoginRequestUploader` statically on the exact SHA;
2. launch one no-secret isolated client and repeat XID/XRes/GDB/pre-Storage/editability gates;
3. before secret handoff, scan writable mappings read-only for relocated controller vpointers and require deterministic live-instance provenance;
4. prove the invocation thread is the Qt/main GUI thread before any native method call;
5. if valid retained native play-session state can be proven, prefer the zero-user-argument auth-controller transition to character selection; otherwise use the already-proven credential path;
6. after account auth, enumerate the native character model/list and require exactly one semantic match for `Invalid Monk`; do not choose by row index/order;
7. invoke character login through the proven native controller/QMeta boundary with the real native argument object; do not construct or guess a character struct from arbitrary memory;
8. require native `RequestCharacterLogin`, then normal game-login state and structural `FullMap` plus >=10 map-description strip records;
9. only after structural `IN_GAME`, capture the manifest-owned XID to transient XWD, export cropped PNG, delete XWD, verify confinement and cleanup, and persist screenshot.

# Required immediate result

```text
NATIVE_OBJECT_PROVENANCE=PASS
SEMANTIC_CHARACTER_MATCH=Invalid Monk;count=1
CHARACTER_ACTIVATION=RequestCharacterLogin
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
checkpoint_version: 26
status: implementing
phase: baseline_native_semantic_character_v15_world_entry_screenshot
baseline_login_max: 7
baseline_login_consumed: 6
patched_login_consumed: 0
last_completed_step: v14 falsified bounded coordinate character activation while account-login transport remained proven; cleanup/source rehash passed
blockers: []
next_action: finish exact-SHA controller vptr recovery, then perform no-secret live object-provenance scan before any seventh login
```
