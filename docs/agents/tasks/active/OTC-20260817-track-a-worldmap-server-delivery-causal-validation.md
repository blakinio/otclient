---
task_id: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
status: blocked
agent: ChatGPT
session_id: chatgpt-worldmap-server-delivery-causal-20260817
session_role: isolated_runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: baseline_login_budget_exhausted_after_character_selection_transition
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
base_branch: main
base_sha: 8a5fcfd72f2554261eef91a2129c9cc076e730ea
created: 2026-08-17T13:20:00+02:00
updated: 2026-08-17T21:26:52+02:00
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
  - .github/scripts/track-a-worldmap-causal-patched-copy-repair.py
modules_touched:
  - track-a-runtime
  - agent-evidence
reuses:
  - merged PRs #371, #452, #462, #465, #473, #474
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
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
live_runtime_authorization_source: owner_current_conversation_2026-08-17_worldmap_causal_validation
client_byte_mutation_authorized: true
bootstrap_for_worldmap_authorized: true
login_for_worldmap_authorized: false
second_live_session_authorized: false
owner_authorization_source: current conversation
owner_authorization_scope: bounded exact baseline versus first [19,14] causal worldmap server-delivery experiment; existing baseline login budget is now exhausted
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
  baseline_ephemeral_login_max: 1
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
last_progress_at: 2026-08-17T21:26:52+02:00
ci_check_generation: terminal_baseline_login_failure_after_character_selection_transition
identical_failure_retries: 0
repair_cycles_for_current_gate: 14
---

# Objective

Compare the exact baseline `[18,14]` against the first task-owned `[19,14]` mutation while measuring authoritative inbound worldmap delivery before Storage separately from Storage/render/picker effects.

# Current verified state

## XWD / window / VNC defect — RESOLVED

Physical evidence proved the original `1920 != 1020` error was a stale fixed geometry assertion in the XWD proof, not a wrong window target.

Current proven contract:

```text
window identity: x11-window:12582929
actual X11 geometry: 1920x1080
XWD pixmap geometry: 1920x1080
XWD window-header geometry: 1920x1080
XRes exact PID: PASS
GDB attach: PASS
pre-Storage observer: ARMED
root-window fallback: NOT USED
alternate XID: NOT USED
resize/reparent/recreate: NOT USED
VNC mapping: PRESERVED
```

## Pre-secret gate — PHYSICALLY PASSED

Run/job `32058144974 / 95472948299 = SUCCESS` physically proved:

```text
WORLDMAP_BASELINE_EMAIL_FIELD_EDITABLE=PASS
WORLDMAP_BASELINE_PASSWORD_FIELD_EDITABLE=PASS
WORLDMAP_BASELINE_LOGIN_FORM=PROVEN_EDITABLE_FIELDS
WORLDMAP_BASELINE_PRESECRET_READY=true
```

V5 final local probes had overlap `1.000000`, residual `0` for both fields and used transient XWD only. Login was not submitted and budget remained `0/1` in that run.

## Baseline login generation — TERMINAL FAILURE AFTER SUBMIT

Run/job `32059988893 / 95478896813` repeated all v5 pre-secret gates in the same launch before credentials. The helper environment contained no credential variables before the handoff step.

Then the protected FIFO handoff occurred and the helper emitted:

```text
WORLDMAP_BASELINE_CREDENTIAL_HANDOFF=RECEIVED_AFTER_PRESECRET_GATES
WORLDMAP_BASELINE_LOGIN_SUBMISSION_METHOD=PASSWORD_TAB_RETURN
WORLDMAP_BASELINE_LOGIN_SUBMITTED=true
WORLDMAP_BASELINE_CHARACTER_SELECTION_TRANSITION=PROVEN_AGGREGATE
```

The login therefore reached the post-auth/character-selection transition boundary.

The translated historical row target was used only after that transition as a target, never as proof:

```text
WORLDMAP_BASELINE_CHARACTER_ROW_TARGET=685,408
WORLDMAP_BASELINE_CHARACTER_ROW_ROI=500,380,1300,445
```

No required localized row-selection change was observed:

```text
WORLDMAP_BASELINE_ERROR=character_row_interaction_not_observed
```

No `WORLDMAP_BASELINE_STRUCTURAL_IN_GAME=PASS`, FullMap count or authoritative baseline extent was obtained.

## Login budget — EXHAUSTED

```yaml
baseline_ephemeral_login_max: 1
baseline_ephemeral_login_consumed: 1
patched_ephemeral_login_max: 1
patched_ephemeral_login_consumed: 0
```

The task contract explicitly states that a failure after `WORLDMAP_BASELINE_LOGIN_SUBMITTED=true` consumes the baseline login budget and must not be silently retried. Therefore another baseline login is forbidden under the current task authority.

## Cleanup / source integrity

The terminal failed generation still proved:

```text
WORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=PASS
WORLDMAP_BASELINE_CLEANUP=COMPLETE
WORLDMAP_FINAL_NAMESPACE_PROCESS_COUNT=0
WORLDMAP_FINAL_CLEANUP_FENCE=PASS
```

The workflow is now an explicit terminal **no-client hold**. Later documentation commits cannot launch a client or expose credentials.

# Result boundary

```text
SERVER_MAP_DELIVERY_MODEL=UNKNOWN
PATCH_CAUSES_ADDITIONAL_AUTHORITATIVE_MAP_DATA=UNKNOWN
BASELINE_AUTHORITATIVE_INBOUND_EXTENT=UNKNOWN
PATCHED_AUTHORITATIVE_INBOUND_EXTENT=UNKNOWN
OUTBOUND_EXTENT_NEGOTIATION_CHANGE=UNKNOWN
STORAGE_EXTENT_CHANGE=UNKNOWN
RENDER_PICKER_EXTENT_CHANGE=UNKNOWN
```

The patched `0/1` login budget cannot repair the missing authoritative baseline comparator by itself.

# Blocker

`baseline_login_budget_exhausted_after_character_selection_transition_without_structural_world_entry`

# Next action

Do not run another client/login under the current contract. Continuation requires an explicit owner decision that **changes the existing baseline login budget/authority** and accepts a second real baseline login attempt. Any such continuation must first design a new character-selection locator/proof that does not repeat the failed translated-row target, then re-run fresh admission/target uniqueness before the newly authorized physical action.

# Checkpoint

```yaml
checkpoint_version: 19
status: blocked
phase: baseline_login_budget_exhausted_after_character_selection_transition
base_main: 8a5fcfd72f2554261eef91a2129c9cc076e730ea
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
pr: 475
runtime_access: ephemeral_isolated
target_uniqueness: UNKNOWN
mutation_authorized: false
baseline_client_launches_consumed: 15
baseline_login_consumed: 1
patched_login_consumed: 0
last_completed_step: v6 physically repeated v5 pre-secret PASS, handed credentials through FIFO, submitted login and proved character-selection transition; row interaction failed; cleanup and source rehash passed
blockers:
  - baseline_login_budget_exhausted_after_character_selection_transition_without_structural_world_entry
next_action: explicit owner authorization is required to increase/change the baseline login budget before any further physical login attempt; first replace the failed translated-row locator with a materially new character-selection proof
```
