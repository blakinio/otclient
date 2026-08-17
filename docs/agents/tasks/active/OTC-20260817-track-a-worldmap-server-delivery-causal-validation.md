---
task_id: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
status: implementing
agent: ChatGPT
session_id: chatgpt-worldmap-server-delivery-causal-20260817-v11
session_role: isolated_runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: baseline_downstream_auth_state_v11_world_entry_screenshot
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
base_branch: main
base_sha: 4d6b6f8f8cbf7d1c579d451cf8f9d91fee7b4691
created: 2026-08-17T13:20:00+02:00
updated: 2026-08-17T22:18:00+02:00
risk: critical
related_pr: 475
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-worldmap-server-delivery-causal-validation.md
  - docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-causal-validation/
  - docs/agents/reports/OTCLIENT-20260817-worldmap-server-delivery-causal-validation.md
  - .github/workflows/track-a-worldmap-server-delivery-causal-validation.yml
  - .github/scripts/track-a-worldmap-causal-ephemeral-baseline.sh
  - .github/scripts/track-a-worldmap-causal-gdb-env-repair.py
  - .github/scripts/track-a-worldmap-causal-xwd-compare.py
  - .github/scripts/track-a-worldmap-causal-xwd-to-png.py
  - .github/scripts/track-a-worldmap-causal-ui-window.py
  - .github/scripts/track-a-worldmap-causal-ui-geometry-repair.py
  - .github/scripts/track-a-worldmap-causal-ui-field-discriminator-v3-repair.py
  - .github/scripts/track-a-worldmap-causal-ui-field-discriminator-v4-repair.py
  - .github/scripts/track-a-worldmap-causal-ui-field-final-roi-v5-repair.py
  - .github/scripts/track-a-worldmap-causal-baseline-login-v6-repair.py
  - .github/scripts/track-a-worldmap-causal-character-selection-v7-repair.py
  - .github/scripts/track-a-worldmap-causal-map-screenshot-v8-repair.py
  - .github/scripts/track-a-worldmap-causal-patched-copy-repair.py
modules_touched:
  - track-a-runtime
  - agent-evidence
reuses:
  - merged PRs #371, #452, #462, #465, #473, #474
  - PR #48 historical exact-SHA successful world-entry flow
  - PR #498 exact-SHA native auth/session control-surface findings
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-control-plus-synology-ephemeral-runtime
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
ROUTING_CONTRACT: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
EXECUTION_CLASS: synology_physical_runtime
RUNTIME_ACCESS: ephemeral_isolated
PERSISTENT_SESSION_ROLE: isolated_runtime_owner
PHYSICAL_E2E_REQUIRED: true
track_id_admission: official-client-re
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
runtime_namespace: worldmap-causal-baseline-ephemeral-v1
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: UNKNOWN
mutation_authorized: false
credentials_allowed: true
login_allowed: true
gameplay_allowed: true
client_byte_mutation_authorized: true
bootstrap_for_worldmap_authorized: true
login_for_worldmap_authorized: true
third_baseline_login_attempt_authorized: true
fourth_baseline_login_attempt_authorized: true
second_live_session_authorized: false
owner_authorization_source: current conversation
owner_authorization_text: "dokoncz zadanie i potwierdz wejscia do swiata gry na mape sascreenem"; reaffirmed "wykonaj"
owner_authorization_scope: one additional sequential real baseline login attempt for v11 after v10 consumed the third attempt; v11 uses the press-proven Login control, secret-safe field occupancy proof, downstream native auth-state acceptance, structural world entry, and one post-IN_GAME cropped map screenshot; no parallel session
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
  baseline_ephemeral_client_launches_consumed: 19
  baseline_ephemeral_login_max: 4
  baseline_ephemeral_login_consumed: 3
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
invocation_started_at: 2026-08-17T21:43:00+02:00
last_progress_at: 2026-08-17T22:18:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: v11_downstream_auth_state_and_screenshot
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Objective

Compare exact baseline `[18,14]` against the first task-owned `[19,14]` mutation while measuring authoritative inbound worldmap delivery before Storage separately from Storage/render/picker effects. Confirm real world entry structurally and, under the owner's new narrow authority, persist one cropped map-view screenshot only after structural `IN_GAME`.

# Proven prerequisites

- exact manifest-owned XID `x11-window:12582929` is XRes-owned by the exact client;
- actual X11 and XWD geometry are `1920x1080`;
- GDB attach and pre-Storage observer are proven;
- VNC mapping is preserved; no alternate XID/root capture/resize/reparent/recreate is permitted;
- v5 physically proved both editable fields, masked/unmasked semantics and `PRESECRET_READY=true`;
- credentials enter only through the mode-0600 FIFO after those gates.

# V6 / V7 corrections

V6 run/job `32059988893 / 95478896813` sent `PASSWORD_TAB_RETURN` and observed a large visual change, but no structural world entry. V7 run/job `32061749381 / 95484431620` repeated all pre-secret gates, sent credentials, then failed with:

```text
WORLDMAP_BASELINE_LOGIN_SUBMITTED=true
WORLDMAP_BASELINE_ERROR=native_character_selection_state_not_observed
WORLDMAP_BASELINE_LOGIN_BUDGET_CONSUMED=2
WORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=PASS
WORLDMAP_BASELINE_CLEANUP=COMPLETE
WORLDMAP_FINAL_NAMESPACE_PROCESS_COUNT=0
```

Therefore the prior visual `CHARACTER_SELECTION_TRANSITION=PROVEN_AGGREGATE` is demoted to a false-positive-capable visual transition. Account-auth success itself was not proven.

# Materially new v9 hypothesis

Historical exact-SHA successful world-entry logic in PR #48 used a direct login-button click, not `Tab+Return`, and armed native events:

```text
ACCOUNT_LOGIN_UPLOADER_SUCCESS @ 0xcfb7c0
ACCOUNT_LOGIN_UPLOADER_FAILED  @ 0xcfb790
LOGIN_FINISHED_SUCCESSFULLY    @ 0xcfaeb4
LOGIN_FAILED_STATE_ENTERED     @ 0xcfb404
CHARACTER_SELECTION_STATE_ENTERED @ 0xcfb374
CHARACTER_SELECTION_CONFIRMED  @ 0xd47130
START_GAMESERVER_LOGIN_STATE_ENTERED @ 0xcfb122
GAME_SESSION_CONNECTED @ 0xd066e0
```

The old successful UI surface was `1020x650`; the current exact surface is `1920x1080`. Center translation is exactly `+450,+215`. This translation is independently corroborated by the current physical field Y coordinates: historical email/password Y `275/304` become `490/519`, matching the dynamically discovered current fields at approximately `490/520`.

V9 must, before secret handoff, prove a localized hover/change at translated login-button target `(1040,603)`. Only then may credentials be handed off. After credentials it must click that proven button and require native account-auth success/failure events. Character selection may only proceed after native auth success and native character-selection state. The corrected translated first-row target is `(735,408)` with ROI `(550,380)-(1350,445)`; interaction is accepted only by native `CHARACTER_SELECTION_CONFIRMED` / `requestCharacterLogin` and then native game-login states, never by coordinates alone.

# Screenshot authority

After `FullMap` plus the required map-description strip count prove structural `IN_GAME`, capture the exact manifest-owned `UI_WIN` to transient XWD, convert it with the task-owned pure-Python exporter, persist only a centered map-view PNG, delete the source XWD, and record its SHA-256. No login, confirmation or character-selection screenshot is allowed. OCR remains forbidden.

# Execution order

1. Fresh no-client inventory and target uniqueness.
2. Static-compose base helper -> v5 -> v6 -> v7 -> v9 -> screenshot gate; verify no root/alternate-XID/window mutation path.
3. Launch exact client with no secrets and repeat all pre-secret gates.
4. Prove translated login-button hover/localized target before credentials.
5. FIFO handoff; direct proven login-button click.
6. Require native uploader success and `LOGIN_FINISHED_SUCCESSFULLY`; fail closed on uploader/login failure.
7. Require native character-selection state; activate corrected translated row and require native character confirmation/request.
8. Require native game-login state and structural `FullMap` + map strips.
9. Capture cropped map screenshot from exact `UI_WIN`; delete transient XWD.
10. Verify WARP/SOCKS confinement, one reversible movement pair, cleanup and exact source rehash.
11. Only after baseline structural capture may the single `[19,14]` patched login/capture run proceed for causal comparison.

# Result boundary before v9

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
checkpoint_version: 21
status: implementing
phase: baseline_auth_submit_button_v9_world_entry_screenshot
base_main: 4d6b6f8f8cbf7d1c579d451cf8f9d91fee7b4691
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
pr: 475
runtime_access: ephemeral_isolated
target_uniqueness: UNKNOWN
baseline_login_max: 4
baseline_login_consumed: 3
patched_login_consumed: 0
last_completed_step: v7 disproved Tab+Return as sufficient auth-success proof; cleanup/source rehash passed
blockers: []
next_action: implement v9 translated login-button hover/native auth-success gate plus corrected row activation and post-IN_GAME screenshot, then static validate before the single authorized third baseline login
```


# V10 physical discriminator and V11 authority

V10 run `32064354985`, physical rerun job `95493198150`, preserved the exact XID/VNC contract and passed all pre-secret gates. Press-cancel physically identified the Login control without activating it:

```text
WORLDMAP_V10_FIELD_DERIVED_TRANSLATION=400,215
WORLDMAP_V10_PRESS_CANCEL=PASS
WORLDMAP_V10_PRESS_BBOX=998,593,1084,613
WORLDMAP_V10_LOGIN_BUTTON_TARGET=1030,603
WORLDMAP_V10_PRESECRET_LOGIN_BUTTON=PROVEN_PRESS_CANCEL
```

The protected FIFO handoff then occurred and the third baseline login submission was emitted, consuming `3/3`. No explicit native uploader/login failure was observed; the generation stopped because v10 required one specific uploader-success event:

```text
WORLDMAP_BASELINE_LOGIN_SUBMISSION_METHOD=PRESS_CANCEL_PROVEN_BUTTON_CLICK
WORLDMAP_BASELINE_LOGIN_SUBMITTED=true
WORLDMAP_BASELINE_ERROR=native_account_login_uploader_success_not_observed
WORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=PASS
WORLDMAP_BASELINE_CLEANUP=COMPLETE
WORLDMAP_FINAL_NAMESPACE_PROCESS_COUNT=0
```

V11 is materially different: it clicks the center of the physically observed pressed-state bbox; proves both protected fields are visibly occupied using changed-pixel counts only; accepts the stronger downstream native `ShowCharacterSelection` state even when an intermediate uploader/LoginFinished breakpoint is not observed; and emits only safe event counters on failure.

The owner's latest `wykonaj` authorizes exactly one additional sequential v11 baseline login:

```yaml
baseline_ephemeral_login_max: 4
baseline_ephemeral_login_consumed: 3
fourth_baseline_login_attempt_authorized: true
```

No parallel session is authorized. Screenshot authority remains map-only and strictly post-structural-IN_GAME.
