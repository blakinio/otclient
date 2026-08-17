---
task_id: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
status: implementing
agent: ChatGPT
session_id: chatgpt-worldmap-server-delivery-causal-20260817-v12
session_role: isolated_runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: baseline_transport_visual_structural_v12_world_entry_screenshot
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
base_branch: main
base_sha: 4d6b6f8f8cbf7d1c579d451cf8f9d91fee7b4691
updated: 2026-08-17T22:34:00+02:00
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
second_live_session_authorized: false
owner_authorization_source: current conversation
owner_authorization_text: "dokocz prace"
owner_authorization_scope: exactly one additional sequential real baseline login attempt for v12 after v11 consumed the fourth attempt; v12 reuses the physically proven Login control and proven field occupancy, removes brittle auth-QMeta events as acceptance gates, requires new local-SOCKS activity plus a large persistent post-login UI transition, then applies the historical exact-SHA character stimulus; only structural FullMap plus map-description strips may prove IN_GAME; one post-IN_GAME cropped map screenshot; no parallel session
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
  baseline_ephemeral_client_launches_consumed: 20
  baseline_ephemeral_login_max: 5
  baseline_ephemeral_login_consumed: 4
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
ci_check_generation: v12_transport_visual_structural_world_entry
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
---

# Objective

Compare exact baseline `[18,14]` with the first task-owned `[19,14]` mutation while measuring authoritative inbound worldmap delivery before Storage separately from Storage/render/picker effects. Confirm real world entry structurally and persist one cropped map-only screenshot only after structural `IN_GAME`.

# Durable physical facts

```text
EXACT_XID=x11-window:12582929
X11_GEOMETRY=1920x1080
XRES_OWNER=PASS
GDB_ATTACH=PASS
PRE_STORAGE_OBSERVER=ARMED
VNC_MAPPING=PRESERVED
EMAIL_FIELD_EDITABLE=PASS
PASSWORD_FIELD_EDITABLE=PASS
PRESECRET_READY=true
```

No alternate XID, root capture, resize, reparent or window recreation is allowed.

# Login-control proof

V10 run `32064354985`, physical rerun job `95493198150`, physically identified the real Login control without submitting credentials:

```text
WORLDMAP_V10_FIELD_DERIVED_TRANSLATION=400,215
WORLDMAP_V10_PRESS_CANCEL=PASS
WORLDMAP_V10_PRESS_BBOX=998,593,1084,613
WORLDMAP_V10_LOGIN_BUTTON_TARGET=1030,603
WORLDMAP_V10_PRESECRET_LOGIN_BUTTON=PROVEN_PRESS_CANCEL
```

# V11 discriminator

V11 run `32065920513`, physical job `95497986845`, passed exact-main, authority, fresh inventory, composition and all pre-secret gates. Protected credentials were handed through the gated FIFO. Pixel-count-only occupancy proof showed both fields were populated without reading or persisting their values:

```text
WORLDMAP_V11_EMAIL_OCCUPANCY_CHANGED=523
WORLDMAP_V11_PASSWORD_OCCUPANCY_CHANGED=823
WORLDMAP_V11_SECRET_FIELD_OCCUPANCY=PASS
WORLDMAP_V11_LOGIN_BUTTON_CENTER=1041,603
WORLDMAP_BASELINE_LOGIN_SUBMITTED=true
```

The generation failed only because no selected auth-state breakpoint fired:

```text
WORLDMAP_BASELINE_ERROR=native_login_activation_state_not_observed
WORLDMAP_BASELINE_LOGIN_BUDGET_CONSUMED=4
WORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=PASS
WORLDMAP_BASELINE_CLEANUP=COMPLETE
WORLDMAP_FINAL_NAMESPACE_PROCESS_COUNT=0
```

This proves the form, field population, physical Login control and click path independently. It does not prove account-auth success or `IN_GAME`.

# V12 materially new hypothesis

Do not use auth QMeta breakpoint presence as an acceptance gate. Follow the historical successful exact-SHA execution model from PR #48:

1. repeat all pre-secret/XRes/GDB/window gates;
2. press-cancel prove the same Login control;
3. protected FIFO handoff and field-occupancy proof;
4. click the press-proven Login control;
5. require post-click client activity through the local WARP/SOCKS endpoint and a large persistent UI transition from the login form;
6. apply the historical character stimulus translated from live field geometry; coordinates are stimulus only;
7. accept `IN_GAME` only when pre-Storage `FullMap` plus at least 10 map-description strip records are observed;
8. only then capture a cropped map PNG from the same exact `UI_WIN`, delete transient XWD, verify WARP/SOCKS confinement and execute one reversible movement pair;
9. cleanup and exact source rehash;
10. only after baseline succeeds, execute the separate single patched `[19,14]` run.

# Current result boundary

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
checkpoint_version: 24
status: implementing
phase: baseline_transport_visual_structural_v12_world_entry_screenshot
base_main: 4d6b6f8f8cbf7d1c579d451cf8f9d91fee7b4691
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
pr: 475
baseline_login_max: 5
baseline_login_consumed: 4
patched_login_consumed: 0
last_completed_step: v11 proved protected field occupancy and press-proven Login click, then failed only on brittle native auth-state instrumentation; cleanup/source rehash passed
blockers: []
next_action: static-compose and run v12 transport+visual+structural baseline; if structural baseline succeeds, immediately run patched [19,14] comparator
```
