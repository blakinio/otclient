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
phase: baseline_ephemeral_behavioral_login_capture
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
base_branch: main
base_sha: c1adcf491580e28d40f215356a9e559af2ccadc4
restack_commit: 91759e0a8d9db1c2a736c88f7e48d2bb5a3ffc59
created: 2026-08-17T13:20:00+02:00
updated: 2026-08-17T17:36:00+02:00
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
  - .github/scripts/track-a-worldmap-causal-xwd-compare.py
  - .github/scripts/track-a-worldmap-causal-ui-window.py
  - .github/scripts/track-a-worldmap-causal-ui-geometry-repair.py
  - .github/scripts/track-a-worldmap-causal-patched-copy-repair.py
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
execution_reason: Repository admission supports task-owned ephemeral_isolated physical sessions; canonical one-shot remains consumed and is not bypassed.
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
target_uniqueness: UNKNOWN
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
  baseline_ephemeral_client_launches_consumed: 10
  baseline_ephemeral_login_max: 1
  baseline_ephemeral_login_consumed: 0
  baseline_ephemeral_observer_repairs_consumed: 1
  baseline_ephemeral_ui_locator_repairs_consumed: 5
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
  transient_xwd_only: true
  broad_process_cleanup: forbidden
  canonical_runtime_namespace_use: forbidden_for_ephemeral_phase
  canonical_source_patch_in_place: forbidden
  patched_copy_task_owned_only: true
  rollback_required: true
  owner_funded_ai_api: forbidden
invocation_started_at: 2026-08-17T13:20:00+02:00
last_progress_at: 2026-08-17T17:36:00+02:00
ci_checks_for_current_head: 2
ci_check_generation: native_presecret_static_pass
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 2
repair_cycles_for_current_gate: 8
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

All physical repair runs through `32031856344 / 95393435891` stopped **before credential submission**. Every launched exact-client repair generation ended with original-source rehash PASS and cleanup COMPLETE.

Load-bearing established chain:

- isolated exact-client + WARP + raw-XRes target ownership is physically proven in prior task-owned repair generations;
- pre-Storage FullMap/map-description observer is physically proven ARMED;
- GDB toolroot environment and XWD toolroot library closure are proven;
- both baseline and future patched arm are normalized to the identical task-owned Xvfb `1020x650` environment;
- manifest `WIN` is accepted only after raw-XRes `LocalClientPid` matches the exact task PID under the task-local 1020x650 owner helper;
- runs `32031603546 / 95392645496` and `32031856344 / 95393435891` proved live XWD shape `1020x650` but falsified the retained grayscale/color gate as an authoritative login-form discriminator; neither submitted credentials;
- evidence label for artifact `9221131366` is corrected: its producing run `31805408522 / 94783011926` captured character selection, not an empty login form;
- historical effective exact-client controls remain `email 535,275`, `password 535,304`, `login 590,388`, first row `285,193`;
- replacement pre-secret proof uses harmless dummy text plus localized aggregate XWD pixel changes to prove both expected fields are editable before any real credential is exposed;
- after real login submission, the helper requires a >5000-pixel aggregate transition, then a localized first-row selection change before `Return`; world entry itself remains structural `FullMap + >=10 map-description strips`.

Fresh persistent-HOME parity discriminators, all on `synology-otclient-01` without client execution or secret use:

- `32038805389 / 95414327705 = SUCCESS`: persistent `.local/share/CipSoft GmbH/Tibia/Tibia` resolves to a FILE rather than the `packages/Tibia` directory;
- `32039597397 / 95416437252 = SUCCESS`: the symlink target is outside `packages/Tibia`, is not the exact package client, while `packages/Tibia/bin/client` still matches the exact SHA;
- `32039652204 / 95416574213 = SUCCESS`: the target is an executable ELF named `Tibia`, size `1460808`, SHA-256 `a5fc6e8ee8246868263c438539a54ea045bd048a1bea45f968fc2f498b682ca0`, outside the persistent HOME and not the exact client;
- historical successful world-entry `31736998731 / 94570936207` was re-inspected at source workflow commit `4392cf4c01703afa344ba074495894a292048eb9` and also launched `packages/Tibia/bin/client` directly with `HOME=/data/home`; therefore the external `Tibia` ELF is not required as the historical successful launch entrypoint;
- `32039938342 / 95417353337 = SUCCESS`: sanitized omitted-state manifest contains exactly 10 entries, digest `9e03d67e62bfda836583f8430b6054a7e4f0bfa11aa919b6936135902ee5b709`; outside package + `launchermetadata.json` these are Qt shader/pipeline cache objects, the external-ELF symlink and `log` directory. No CipSoft/Tibia-named state was found under `.config` or `.local/state` by this bounded inventory.

# Current interpretation boundary

- `external_launcher_required_for_successful_login = DISPROVEN` by the historical successful direct-package-client workflow;
- `missing_persistent_account_or_login_layout_state_in_scanned_XDG_paths = NOT_OBSERVED`; this weakens but does not prove false every possible HOME-state hypothesis;
- the strongest blocker remains semantic pre-secret UI discrimination, but the execution contract is now native to `.github/scripts/track-a-worldmap-causal-ephemeral-baseline.sh` rather than supplied only by a later transformer;
- the native helper now fails if `TIBIA_TEST_EMAIL` or `TIBIA_TEST_PASSWORD` is present in its environment before the pre-secret gates, proves both fields with harmless dummy text, clears both fields, creates a mode-0600 FIFO, and only then waits for credential handoff;
- legacy OCR/tesseract anchors are absent from the native helper;
- exact-head hosted workflow run `32042635828 / 95424571898 = SUCCESS` physically emitted `WORLDMAP_STATIC_NATIVE_PRESECRET_CONTRACT=PASS`; its physical Synology job was `skipped`;
- exact-head Track A runtime-governance run `32042635853 = SUCCESS`;
- current `main` was re-read after those runs and remains `c1adcf491580e28d40f215356a9e559af2ccadc4`;
- trusted-base restack itself is `91759e0a8d9db1c2a736c88f7e48d2bb5a3ffc59`; current task head after native-source/workflow/checkpoint commits was `f97457aab2c5824cb58b455c6e2b86b9a0859e8b` before this task-checkpoint update.

Durable evidence includes:

- `20260817-presecret-ui-loader-repairs.md`
- `20260817-xres-ui-window-boundary.md`
- `20260817-1020-desktop-normalization.md`
- `20260817-manifest-owned-ui-window.md`
- `20260817-prelogin-behavioral-proof.md`
- `20260817-restack-native-presecret-source.md`

# Workflow safety state

The PR workflow is now fail-closed in three explicit physical modes: `inventory_only`, `presecret_only`, and `baseline_login`. Pull-request execution runs only the deterministic hosted native composition check; the physical job is skipped unless deliberately activated. The `baseline_login` step is the only workflow block that references protected login secrets, and it can run only after the helper has emitted both editability PASS markers plus `WORLDMAP_BASELINE_PRESECRET_READY=true`. The helper itself never receives those secrets through its environment; credential values cross only the mode-0600 task-owned FIFO after the gates.

# Execution phases

1. **DONE** canonical boundary / cleanup.
2. **DONE** isolated exact-client WARP/XRes path.
3. **DONE** pre-Storage observer gate.
4. **DONE** 1020x650 normalization, manifest XRes identity, loader/GDB repair and native aggregate behavioral pre-login composition validation.
5. **ACTIVE / BLOCKED_ON_POST_RESTACK_READMISSION** run `inventory_only` with no client/no secret; persist fresh target uniqueness; then run `presecret_only` and stop before secret handoff; only after both proofs may the single baseline login budget be used.
6. **PENDING** patched namespace/preimage/target-uniqueness admission.
7. **PENDING** one task-owned `[19,14]` login/capture under identical 1020x650 instrumentation.
8. **PENDING** patched rollback/source rehash/cleanup.
9. **PENDING** causal classification, audit, temporary-resource removal, exact-head CI/review/merge/archive.

# Stop criteria

Fail closed on main drift, non-idle/competing official-client candidate state, namespace collision, target ambiguity, observer regression, 1020x650 XRes identity failure, failure of either harmless editable-field probe, any credential-bearing environment before handoff, WARP/credential confinement failure, post-submit visual-transition failure, first-row interaction failure, absence of FullMap/map-description proof, source/preimage/hash mismatch, unexpected gameplay/account side effect, crash, or incomplete cleanup.

Any failure **after** `WORLDMAP_BASELINE_LOGIN_SUBMITTED=true` consumes the one baseline login budget and must not be silently retried.

# Checkpoint

```yaml
checkpoint_version: 14
updated_at: 2026-08-17T17:36:00+02:00
base_main: c1adcf491580e28d40f215356a9e559af2ccadc4
current_main_observed: c1adcf491580e28d40f215356a9e559af2ccadc4
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
pr: 475
status: investigating
phase: baseline_ephemeral_behavioral_login_capture
runtime_access: ephemeral_isolated
target_uniqueness: UNKNOWN
mutation_authorized: false
workflow_mode: manual_inventory_presecret_login_with_hosted_static_gate
baseline_client_launches_consumed: 10
baseline_login_consumed: 0
patched_login_consumed: 0
last_completed_step: restacked PR #475 onto current main and made the pre-secret editability/FIFO contract native to the baseline helper; exact-head hosted static composition and Track A governance both passed without running the physical job
blockers:
  - post_restack_target_uniqueness_not_yet_reproven
next_action: execute exactly one no-client/no-secret inventory_only pass on synology-otclient-01; if and only if it proves zero task-namespace processes and zero official-client candidates, persist target_uniqueness=PROVEN before any client launch. Then execute presecret_only and require both dummy editability gates plus exact cleanup with no login submission before exposing any protected credential.
```
