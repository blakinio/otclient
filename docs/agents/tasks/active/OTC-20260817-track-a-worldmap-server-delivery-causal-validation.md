---
task_id: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
status: investigating
agent: ChatGPT
session_id: chatgpt-worldmap-server-delivery-causal-20260817
session_role: isolated_runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: baseline_ephemeral_login_capture
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
base_branch: main
base_sha: 83034227280dc3bfdf589a991f0fdbbabab7dc87
restack_commit: f6848a59224ce891067b12a8b3f65da1609ee985
created: 2026-08-17T13:20:00+02:00
updated: 2026-08-17T14:42:00+02:00
risk: critical
related_pr: 475
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-worldmap-server-delivery-causal-validation.md
  - docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-causal-validation/
  - docs/agents/reports/OTCLIENT-20260817-worldmap-server-delivery-causal-validation.md
  - .github/workflows/track-a-worldmap-server-delivery-causal-validation.yml
  - .github/scripts/track-a-worldmap-causal-ephemeral-baseline.sh
  - .github/scripts/track-a-worldmap-causal-screen-geometry-repair.py
  - .github/scripts/track-a-worldmap-causal-gdb-env-repair.py
  - .github/scripts/track-a-worldmap-causal-xwd-classify.py
  - .github/scripts/track-a-worldmap-causal-ui-window.py
  - .github/scripts/track-a-worldmap-causal-ui-geometry-repair.py
modules_touched:
  - track-a-runtime
  - agent-evidence
reuses:
  - docs/agents/reports/OTCLIENT-20260817-worldmap-server-delivery-extent.md
  - docs/agents/tasks/archive/OTC-20260817-track-a-worldmap-mutation-design.md
  - docs/agents/tasks/archive/OTC-20260817-track-a-worldmap-mutation-physical-validation.md
  - merged PRs #371, #452, #462, #465, #473, #474
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-control-plus-synology-ephemeral-runtime
execution_reason: Repository admission explicitly supports task-owned ephemeral_isolated physical sessions; canonical one-shot remains consumed and is not bypassed.
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_pressure: high
context_growth: stable
context_score: 11
estimate_confidence: high
decomposition_decision: phased
feature_scope:
  type: protocol
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: true
  completion_claim: internal_only
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
target_uniqueness: PROVEN
mutation_authorized: false
credentials_allowed: true
login_allowed: true
gameplay_allowed: true
live_runtime_authorization_source: owner_current_conversation_2026-08-17_worldmap_causal_validation
client_byte_mutation_authorized: true
bootstrap_for_worldmap_authorized: true
login_for_worldmap_authorized: true
second_live_session_authorized: false
owner_authorization_source: current conversation
owner_authorization_text: "wykonaj i czekam na wyniki"; reaffirmed "kontynuuj prace i masz moje zgody"
owner_authorization_scope: bounded exact baseline versus first [19,14] causal worldmap server-delivery experiment, including login/relogin, one reversible movement pair, instrumentation and rollback
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
  prior_physical_patched_sha256: 7c8d936fa43e4a026d2a69c32ff30fdea149bb7eff7938c1b1acfc173899b44c
launch_budget:
  canonical_exact_bootstrap_consumed: 1
  canonical_xres_repair_launch_consumed: 0
  baseline_ephemeral_client_launches_consumed: 7
  baseline_ephemeral_login_max: 1
  baseline_ephemeral_login_consumed: 0
  baseline_ephemeral_observer_repairs_consumed: 1
  baseline_ephemeral_ui_locator_repairs_consumed: 3
  baseline_ephemeral_pre_secret_loader_repairs_consumed: 1
  patched_ephemeral_login_max: 1
  patched_ephemeral_login_consumed: 0
  simultaneous_logged_in_sessions_max: 1
safety:
  direct_unapproved_egress: forbidden
  warp_socks_required: true
  raw_client_commit_or_upload: forbidden
  credentials_in_logs_or_artifacts: forbidden
  screenshots_or_ocr_artifacts: forbidden
  broad_process_cleanup: forbidden
  canonical_runtime_namespace_use: forbidden_for_ephemeral_phase
  canonical_source_patch_in_place: forbidden
  patched_copy_task_owned_only: true
  rollback_required: true
  owner_funded_ai_api: forbidden
invocation_started_at: 2026-08-17T13:20:00+02:00
last_progress_at: 2026-08-17T14:42:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: desktop-1020-static-pass
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 1
repair_cycles_for_current_gate: 5
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Objective

Compare exact baseline `[18,14]` against the first task-owned `[19,14]` mutation while measuring authoritative inbound worldmap delivery before Storage separately from Storage/render/picker effects.

# Required result

```text
SERVER_MAP_DELIVERY_MODEL=CLIENT_DRIVEN|SERVER_DRIVEN|NEGOTIATED|FIXED_PROTOCOL|UNKNOWN
PATCH_CAUSES_ADDITIONAL_AUTHORITATIVE_MAP_DATA=true|false|UNKNOWN
BASELINE_AUTHORITATIVE_INBOUND_EXTENT=<measured or UNKNOWN>
PATCHED_AUTHORITATIVE_INBOUND_EXTENT=<measured or UNKNOWN>
OUTBOUND_EXTENT_NEGOTIATION_CHANGE=true|false|UNKNOWN
STORAGE_EXTENT_CHANGE=true|false|UNKNOWN
RENDER_PICKER_EXTENT_CHANGE=true|false|UNKNOWN
```

# Verified progression

All physical repair runs so far stopped before credential submission; every launched exact-client repair generation ended with original-source rehash PASS and cleanup COMPLETE.

Load-bearing current chain:

- isolated exact-client + WARP + raw-XRes target ownership is proven;
- pre-Storage FullMap/map-description observer is physically proven ARMED;
- GDB toolroot environment and XWD toolroot library closure are proven;
- OCR-free raw-XWD classifier is calibrated from retained exact-client 1020x650 login/selection artifacts;
- current 1920x1080 run `32030582178 / 95389455836` proved no separate viewable 1020x650 XRes-owned UI candidate exists and stopped before secret use;
- historical exact-client `31805408522 / 94783011926` proves the retained successful login flow used a 1020x650 window;
- task-owned desktop normalization now requires both baseline and patched arms to use identical Xvfb 1020x650 and an XRes owner narrowed to the same geometry;
- no-client static composition `32030958692 / 95390632587 = SUCCESS` validates screen normalization -> XRes identity -> GDB repair -> raw-XWD UI repair with no executable legacy PID selector and no OCR surface.

Durable evidence:

- `20260817-presecret-ui-loader-repairs.md`
- `20260817-xres-ui-window-boundary.md`
- `20260817-1020-desktop-normalization.md`

# Execution phases

1. **DONE** canonical boundary / cleanup.
2. **DONE** isolated exact-client WARP/XRes path.
3. **DONE** pre-Storage observer gate.
4. **DONE** OCR-free UI/loader/XRes repair and 1020x650 task-owned desktop normalization static validation.
5. **ACTIVE** one baseline login + FullMap/map-description extent + Right/Left stimulus + transport confinement + cleanup.
6. **PENDING** patched namespace/preimage/target-uniqueness admission.
7. **PENDING** one task-owned `[19,14]` login/capture under the identical 1020x650 environment and instrumentation.
8. **PENDING** patched rollback/source rehash/cleanup.
9. **PENDING** causal classification, audit, temporary-resource removal, exact-head CI/review/merge/archive.

# Stop criteria

Fail closed on main drift, non-idle canonical controller state, namespace collision, target ambiguity, observer regression, 1020x650 XRes identity failure, live XWD classification mismatch, WARP/credential confinement failure, character-selection geometry failure, absence of FullMap/map-description proof, source/preimage/hash mismatch, unexpected gameplay/account side effect, crash, or incomplete cleanup.

# Checkpoint

```yaml
checkpoint_version: 11
updated_at: 2026-08-17T14:42:00+02:00
base_main: 83034227280dc3bfdf589a991f0fdbbabab7dc87
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
pr: 475
status: investigating
phase: baseline_ephemeral_login_capture
runtime_access: ephemeral_isolated
target_uniqueness: PROVEN
baseline_login_consumed: 0
patched_login_consumed: 0
last_completed_step: task-owned 1020x650 desktop normalization statically validated on 32030958692 / 95390632587 after the 1920 desktop proved no separate 1020 UI candidate
blockers: []
next_action: Execute one normalized 1020x650 baseline generation. Require current-main admission, idle controller, exact XRes identity, pre-Storage observer ARMED and live LOGIN_FORM before secret submission.
```
