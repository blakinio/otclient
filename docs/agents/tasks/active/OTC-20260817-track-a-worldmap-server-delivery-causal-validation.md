---
task_id: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
status: implementing
agent: ChatGPT
session_id: chatgpt-worldmap-server-delivery-causal-20260817-v7
session_role: isolated_runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: baseline_character_selection_native_activation_v7
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
base_branch: main
base_sha: 8a5fcfd72f2554261eef91a2129c9cc076e730ea
created: 2026-08-17T13:20:00+02:00
updated: 2026-08-17T21:34:00+02:00
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
  - .github/scripts/track-a-worldmap-causal-ui-window.py
  - .github/scripts/track-a-worldmap-causal-ui-geometry-repair.py
  - .github/scripts/track-a-worldmap-causal-ui-field-discriminator-v3-repair.py
  - .github/scripts/track-a-worldmap-causal-ui-field-discriminator-v4-repair.py
  - .github/scripts/track-a-worldmap-causal-ui-field-final-roi-v5-repair.py
  - .github/scripts/track-a-worldmap-causal-baseline-login-v6-repair.py
  - .github/scripts/track-a-worldmap-causal-character-selection-v7-repair.py
  - .github/scripts/track-a-worldmap-causal-patched-copy-repair.py
modules_touched:
  - track-a-runtime
  - agent-evidence
reuses:
  - merged PRs #371, #452, #462, #465, #473, #474
  - PR #498 exact-SHA static auth/session control-surface findings
  - docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-causal-validation/20260817-exact-window-xwd-geometry-causal-discriminator.md
  - docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-causal-validation/20260817-v5-presecret-pass-v6-login-terminal-discriminator.md
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
live_runtime_authorization_source: owner_current_conversation_2026-08-17_worldmap_causal_validation_v7
client_byte_mutation_authorized: true
bootstrap_for_worldmap_authorized: true
login_for_worldmap_authorized: true
second_baseline_login_attempt_authorized: true
second_live_session_authorized: false
owner_authorization_source: current conversation
owner_authorization_text: "wykonaj"
owner_authorization_scope: explicit increase of the baseline login budget by one additional sequential real baseline login attempt, continuing the already-authorized exact baseline versus first [19,14] causal experiment; simultaneous logged-in sessions remain forbidden
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
  baseline_ephemeral_client_launches_consumed: 15
  baseline_ephemeral_login_max: 2
  baseline_ephemeral_login_consumed: 1
  patched_ephemeral_login_max: 1
  patched_ephemeral_login_consumed: 0
  simultaneous_logged_in_sessions_max: 1
safety:
  direct_unapproved_egress: forbidden
  warp_socks_required: true
  raw_client_commit_or_upload: forbidden
  credentials_in_logs_or_artifacts: forbidden
  screenshots_or_ocr_artifacts: forbidden
  transient_xwd_only: true
  broad_process_cleanup: forbidden
  canonical_runtime_namespace_use: forbidden_for_ephemeral_phase
  canonical_source_patch_in_place: forbidden
  patched_copy_task_owned_only: true
  rollback_required: true
  owner_funded_ai_api: forbidden
invocation_started_at: 2026-08-17T21:34:00+02:00
last_progress_at: 2026-08-17T21:34:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: v7_native_character_activation_authorized
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Objective

Compare exact baseline `[18,14]` against the first task-owned `[19,14]` mutation while measuring authoritative inbound worldmap delivery before Storage separately from Storage/render/picker effects.

# Owner authority change

The preceding v6 generation consumed the original `1/1` baseline login budget and stopped after proving account login reached character selection. The owner then replied `wykonaj` directly to the explicit requirement for a changed baseline-login limit and a second real baseline login. This is persisted as authority for exactly one additional sequential baseline login. It does not authorize parallel sessions or relax any secret, WARP, XRes, VNC, cleanup or source-integrity requirement.

```yaml
baseline_ephemeral_login_max: 2
baseline_ephemeral_login_consumed: 1
second_baseline_login_attempt_authorized: true
simultaneous_logged_in_sessions_max: 1
```

# Proven prerequisites

## Exact window / XWD / VNC

```text
WORLDMAP_BASELINE_WINDOW_IDENTITY=x11-window:12582929
WORLDMAP_UI_EXACT_GEOMETRY=1920x1080
WORLDMAP_XWD_PIXMAP_GEOMETRY=1920x1080
WORLDMAP_XWD_WINDOW_GEOMETRY=1920x1080
WORLDMAP_UI_EXACT_XRES_PID_MATCH=PASS
WORLDMAP_BASELINE_GDB_ATTACH=PASS
WORLDMAP_BASELINE_PRE_STORAGE_OBSERVER=ARMED
WORLDMAP_BASELINE_VNC_MAPPING_PRESERVED=MANIFEST_RUNTIME_UNCHANGED
```

The original `1920 != 1020` defect is resolved as stale fixed proof geometry. No alternate XID, root capture, resize, reparent or recreate is allowed.

## Pre-secret v5

Run/job `32058144974 / 95472948299 = SUCCESS` physically proved:

```text
WORLDMAP_BASELINE_EMAIL_FIELD_EDITABLE=PASS
WORLDMAP_BASELINE_PASSWORD_FIELD_EDITABLE=PASS
WORLDMAP_BASELINE_LOGIN_FORM=PROVEN_EDITABLE_FIELDS
WORLDMAP_BASELINE_PRESECRET_READY=true
```

The same gates were repeated successfully in the v6 login launch before credentials.

## V6 login result

Run/job `32059988893 / 95478896813` proved:

```text
WORLDMAP_BASELINE_CREDENTIAL_HANDOFF=RECEIVED_AFTER_PRESECRET_GATES
WORLDMAP_BASELINE_LOGIN_SUBMISSION_METHOD=PASSWORD_TAB_RETURN
WORLDMAP_BASELINE_LOGIN_SUBMITTED=true
WORLDMAP_BASELINE_CHARACTER_SELECTION_TRANSITION=PROVEN_AGGREGATE
```

Then the translated historical row target failed:

```text
WORLDMAP_BASELINE_ERROR=character_row_interaction_not_observed
WORLDMAP_BASELINE_LOGIN_BUDGET_CONSUMED=1
WORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=PASS
WORLDMAP_BASELINE_CLEANUP=COMPLETE
WORLDMAP_FINAL_NAMESPACE_PROCESS_COUNT=0
```

# V7 materially new hypothesis

Do **not** repeat the failed translated-row target. PR #498 provides exact-SHA native control boundaries:

```text
TAuthenticationProcessController::onShowCharacterSelectionStateEntered @ 0xcfb374
TCharacterSelectionController::requestCharacterLogin(TCharacter) @ 0xd47300
TAuthenticationProcessController::requestCharacterGameserverLogin() @ 0xcfb2e7
TAuthenticationProcessController::onStartGameServerLoginStateEntered @ 0xcfb122
```

V7 must add read-only GDB event breakpoints for those native boundaries and drive only bounded keyboard activation after the native `ShowCharacterSelection` event is proven. A character activation is accepted only when `requestCharacterLogin` is observed; world entry is accepted only when `FullMap` plus map-description strips meet the structural threshold. No historical row coordinate may be used.

The underlying permission, gate and hypothesis have materially changed, so anti-stall counters for this new gate are reset to zero; previous repair history remains preserved in durable evidence and is not erased.

# Execution order

1. Fresh no-client inventory and target uniqueness.
2. Compose exact GDB/XRes/XWD/v5/v7 helper and static safety validation.
3. Launch exact client with no secrets in helper environment.
4. Re-prove XRes/GDB/pre-Storage observer/v5 editability in that same launch.
5. Hand credentials through mode-0600 FIFO only after `PRESECRET_READY=true`.
6. Submit login; consume baseline login budget `2/2` once `LOGIN_SUBMITTED=true` appears.
7. Require native `ShowCharacterSelection` breakpoint event.
8. Use bounded keyboard-only activation; require native `requestCharacterLogin`, then game-login state events.
9. Require structural `FullMap` + map-description strips before one reversible movement pair.
10. Cleanup and exact source rehash.
11. Only if baseline structural capture succeeds may the first task-owned `[19,14]` patched run be admitted.

# Result boundary before v7

```text
SERVER_MAP_DELIVERY_MODEL=UNKNOWN
PATCH_CAUSES_ADDITIONAL_AUTHORITATIVE_MAP_DATA=UNKNOWN
BASELINE_AUTHORITATIVE_INBOUND_EXTENT=UNKNOWN
PATCHED_AUTHORITATIVE_INBOUND_EXTENT=UNKNOWN
OUTBOUND_EXTENT_NEGOTIATION_CHANGE=UNKNOWN
STORAGE_EXTENT_CHANGE=UNKNOWN
RENDER_PICKER_EXTENT_CHANGE=UNKNOWN
```

# Blocker

None before v7 static composition. Runtime remains no-client until the new helper and workflow are statically fenced.

# Next action

Implement and statically validate the v7 native character-selection breakpoint/keyboard activation transform, then perform fresh physical admission for the newly authorized single additional baseline login.

# Checkpoint

```yaml
checkpoint_version: 20
status: implementing
phase: baseline_character_selection_native_activation_v7
base_main: 8a5fcfd72f2554261eef91a2129c9cc076e730ea
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
pr: 475
runtime_access: ephemeral_isolated
target_uniqueness: UNKNOWN
baseline_login_max: 2
baseline_login_consumed: 1
patched_login_consumed: 0
last_completed_step: owner explicitly authorized exactly one additional sequential baseline login after v6 consumed the original budget
blockers: []
next_action: implement v7 native character-selection event proof and bounded keyboard activation; keep workflow no-client until static validation passes
```
