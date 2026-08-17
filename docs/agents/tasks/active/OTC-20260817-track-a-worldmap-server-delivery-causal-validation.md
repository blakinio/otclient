---
task_id: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
status: implementing
agent: ChatGPT
session_id: chatgpt-worldmap-server-delivery-causal-20260817-v14
session_role: isolated_runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: baseline_dynamic_character_activation_v14_world_entry_screenshot
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
base_branch: main
base_sha: 4d6b6f8f8cbf7d1c579d451cf8f9d91fee7b4691
updated: 2026-08-17T23:04:00+02:00
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
fifth_baseline_login_attempt_authorized: true
sixth_baseline_login_attempt_authorized: true
second_live_session_authorized: false
owner_authorization_source: current conversation
owner_authorization_text: "dokoncz zadanjie w momencie zalogowania sie do gry i przedstawienia screnshota"
owner_authorization_scope: exactly one additional sequential real baseline login attempt for v14 after v13 consumed the fifth attempt; account-login transport and persistent post-login UI transition are already physically proven; v14 may use a bounded set of character-selection stimuli but must accept character activation only by native RequestCharacterLogin or structural FullMap; IN_GAME remains FullMap plus map-description strips; one map-only screenshot only after structural IN_GAME; no parallel session
owner_funded_ai_api_authorized: false
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
mutation_design:
  source_pr: 452
  target_va: '0x01cdd958'
  preimage_16_hex: 120000000e0000000800000006000000
  baseline_pair: [18,14]
  canary_pair: [19,14]
  canary_postimage_prefix_8_hex: 130000000e000000
  changed_bytes_expected: 1
launch_budget:
  canonical_exact_bootstrap_consumed: 1
  canonical_xres_repair_launch_consumed: 0
  baseline_ephemeral_client_launches_consumed: 23
  baseline_ephemeral_login_max: 6
  baseline_ephemeral_login_consumed: 5
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
  canonical_runtime_namespace_use: forbidden_for_ephemeral_phase
  canonical_source_patch_in_place: forbidden
  patched_copy_task_owned_only: true
  rollback_required: true
  owner_funded_ai_api: forbidden
ci_check_generation: v14_dynamic_character_activation_world_entry
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
---

# Objective

Reach the real game world on the exact baseline client, prove `IN_GAME` structurally with pre-Storage `FullMap` plus map-description strip records, and persist one cropped map-only screenshot. The wider baseline-vs-`[19,14]` causal comparison remains downstream, but the owner's current stop condition is the successful world entry plus screenshot.

# Durable same-launch safety contract

```text
EXACT_XID=x11-window:12582929
X11_GEOMETRY=1920x1080
XRES_OWNER=PASS
GDB_ATTACH=PASS
PRE_STORAGE_OBSERVER=ARMED
VNC_MAPPING=PRESERVED
EMAIL_FIELD_EDITABLE=PASS
PASSWORD_FIELD_EDITABLE=PASS
LOGIN_FORM=PROVEN_EDITABLE_FIELDS
PRESECRET_READY=true
```

No alternate XID, root capture, resize, reparent, window recreation, OCR, login-screen screenshot or character-selection screenshot is permitted. Credentials enter only through the mode-0600 FIFO after the same-launch gates above.

# Proven Login control and protected field occupancy

V10 physically identified the actual Login control on the exact current topology:

```text
WORLDMAP_V10_PRESS_BBOX=998,593,1084,613
WORLDMAP_V10_LOGIN_BUTTON_TARGET=1030,603
```

V11/v13 independently proved protected values are actually rendered into both fields without reading or persisting their contents:

```text
WORLDMAP_V11_EMAIL_OCCUPANCY_CHANGED=523
WORLDMAP_V11_PASSWORD_OCCUPANCY_CHANGED=838
WORLDMAP_BASELINE_SECRET_FIELD_OCCUPANCY=PASS
```

# V13 terminal discriminator — account login proven

Run `32067963829`, physical rerun job `95506276673`, exact head `826ecee86ff2fbf21d2eb5c71a66d4b71a8ae461`:

```text
WORLDMAP_V13_PRESECRET_GATE=PASS
WORLDMAP_BASELINE_CREDENTIAL_HANDOFF=RECEIVED_AFTER_PRESECRET_GATES
WORLDMAP_BASELINE_SECRET_FIELD_OCCUPANCY=PASS
WORLDMAP_V12_LOCAL_SOCKS_BEFORE=0
WORLDMAP_BASELINE_LOGIN_SUBMISSION_METHOD=PRESS_BBOX_CENTER_CLICK_TRANSPORT_VISUAL_PROOF
WORLDMAP_BASELINE_LOGIN_SUBMITTED=true
WORLDMAP_V12_POST_LOGIN_UI_TRANSITION=PERSISTENT_LARGE_CHANGE
WORLDMAP_V12_LOCAL_SOCKS_MAX=1
WORLDMAP_BASELINE_LOGIN_TRANSPORT_ACTIVITY=PASS
WORLDMAP_BASELINE_POST_LOGIN_UI_TRANSITION=PASS
```

Therefore the current blocker is not account authentication or the Login button. It is character activation after the proven post-login transition.

The v13 character stimulus at the field-derived historical translation did not enter the world:

```text
WORLDMAP_BASELINE_CHARACTER_STIMULUS=FIELD_DERIVED_ROW_CLICK_RETURN
WORLDMAP_BASELINE_CHARACTER_STIMULUS_FALLBACK=FIELD_DERIVED_ROW_DOUBLECLICK_RETURN
WORLDMAP_BASELINE_ERROR=structural_world_entry_not_observed
WORLDMAP_BASELINE_LOGIN_BUDGET_CONSUMED=5
WORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=PASS
WORLDMAP_BASELINE_CLEANUP=COMPLETE
WORLDMAP_FINAL_NAMESPACE_PROCESS_COUNT=0
```

# V14 materially new hypothesis

After the already-proven account-login transport/UI transition, test a bounded set of character activation stimuli while the existing read-only GDB event recorder remains armed. `TCharacterSelectionController::requestCharacterLogin(TCharacter) @ 0xd47300` is the primary discriminator.

Execution order:

1. repeat the full mandatory same-launch pre-secret gates;
2. protected FIFO handoff and field-occupancy proof;
3. click the previously proven Login control;
4. require local-SOCKS activity plus persistent post-login UI transition;
5. record baseline `RequestCharacterLogin` count;
6. try in order: `Return` only, `(735,408)+Return`, `(735,384)+Return`, `(735,432)+Return`, `(785,408)+Return`, `(685,408)+Return`, then one bounded double-click fallback at `(735,408)`;
7. after every stimulus, accept the candidate only when native `RequestCharacterLogin` increases; if `FullMap` fires first, treat that as stronger direct success;
8. once native character request fires, wait for `FullMap` plus at least 10 map-description strip records;
9. only after structural `IN_GAME`, capture the exact manifest-owned `UI_WIN` to transient XWD, convert to cropped PNG, delete XWD, verify confinement and cleanup;
10. persist the map PNG and structural summary on the task branch.

# Required immediate result

```text
ACCOUNT_LOGIN_TRANSPORT=PASS
CHARACTER_ACTIVATION=RequestCharacterLogin|FullMap
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
checkpoint_version: 25
status: implementing
phase: baseline_dynamic_character_activation_v14_world_entry_screenshot
base_main: 4d6b6f8f8cbf7d1c579d451cf8f9d91fee7b4691
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
pr: 475
baseline_login_max: 6
baseline_login_consumed: 5
patched_login_consumed: 0
last_completed_step: v13 proved account-login transport plus persistent post-login UI transition; single translated character target and double-click fallback did not produce FullMap; cleanup/source rehash passed
blockers: []
next_action: run v14 bounded native RequestCharacterLogin discriminator and stop only after structural FullMap plus map screenshot
```
