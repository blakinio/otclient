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
phase: baseline_presecret_ui_discriminator
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
base_branch: main
base_sha: 8a5fcfd72f2554261eef91a2129c9cc076e730ea
restack_commit: 91759e0a8d9db1c2a736c88f7e48d2bb5a3ffc59
created: 2026-08-17T13:20:00+02:00
updated: 2026-08-17T18:49:00+02:00
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
target_uniqueness: PROVEN
mutation_authorized: true
credentials_allowed: true
login_allowed: true
gameplay_allowed: true
live_runtime_authorization_source: owner_current_conversation_2026-08-17_worldmap_causal_validation
client_byte_mutation_authorized: true
bootstrap_for_worldmap_authorized: true
login_for_worldmap_authorized: true
second_live_session_authorized: false
owner_authorization_source: current conversation
owner_authorization_text: "wykonaj i czekam na wyniki"; reaffirmed "kontynuuj prace i masz moje zgody"; reaffirmed "wykonaj bo czekam na wynik logowania"
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
  baseline_ephemeral_client_launches_consumed: 11
  baseline_ephemeral_login_max: 1
  baseline_ephemeral_login_consumed: 0
  baseline_ephemeral_observer_repairs_consumed: 1
  baseline_ephemeral_ui_locator_repairs_consumed: 6
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
last_progress_at: 2026-08-17T18:46:43+02:00
ci_checks_for_current_head: 3
ci_check_generation: presecret_exact_window_geometry_pass_field_semantics_zero_candidates
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 2
repair_cycles_for_current_gate: 10
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

All physical repair runs through the current pre-secret generation stopped **before credential submission**. Every launched exact-client repair generation ended with original-source rehash PASS and cleanup COMPLETE.

Load-bearing established chain:

- isolated exact-client + WARP + raw-XRes target ownership is physically proven in prior task-owned repair generations;
- pre-Storage FullMap/map-description observer is physically proven ARMED;
- GDB toolroot environment and XWD toolroot library closure are proven;
- historical normalized `1020x650` generations physically existed and were useful for earlier bounded UI discriminators, but they are no longer an assumption for the current native restacked helper;
- current native runtime physically selects the manifest-owned raw-XRes exact-PID top-level client window at `1920x1080`;
- run `32046786429 / 95436438152` proved the exact runtime/UI/XWD target remained `x11-window:12582929`, actual X11 geometry was `1920x1080`, root geometry was `1920x1080`, the window was a borderless direct root child, and there were zero child or same-PID alternate viewable drawables;
- the same run proved XWD pixmap geometry `1920x1080`, XWD window-header geometry `1920x1080`, stride `7680`, and exact-XID capture identity without root fallback;
- therefore the earlier `XwdError:shape_width:1920!=1020` was a stale fixed geometry assertion in the XWD parser/proof, not a wrong XID, XRes failure, root fallback, decorator mismatch or hidden `1020x650` child drawable;
- `.github/scripts/track-a-worldmap-causal-xwd-compare.py` now keeps strict XWD format/depth/mask validation while accepting geometry only when it matches the separately inspected exact manifest-owned X11 window;
- `.github/scripts/track-a-worldmap-causal-ui-window.py` now inspects only the supplied manifest XID and cannot select a replacement window;
- the pre-secret transform keeps `UI_WIN="$WIN"`, prohibits root capture/window geometry mutation, and contains no credential/login path in its physical diagnostic generation;
- the current coordinate-free Tab/text-growth/masked-variant discriminator reached the repaired XWD boundary but classified zero unique text-field candidates (`unmasked=0;masked=0`), so email/password editability remains NOT_PROVEN;
- no protected credential was handed off, no login was submitted, and the baseline login budget remains `0/1`.

Fresh persistent-HOME parity discriminators, all on `synology-otclient-01` without client execution or secret use:

- `32038805389 / 95414327705 = SUCCESS`: persistent `.local/share/CipSoft GmbH/Tibia/Tibia` resolves to a FILE rather than the `packages/Tibia` directory;
- `32039597397 / 95416437252 = SUCCESS`: the symlink target is outside `packages/Tibia`, is not the exact package client, while `packages/Tibia/bin/client` still matches the exact SHA;
- `32039652204 / 95416574213 = SUCCESS`: the target is an executable ELF named `Tibia`, size `1460808`, SHA-256 `a5fc6e8ee8246868263c438539a54ea045bd048a1bea45f968fc2f498b682ca0`, outside the persistent HOME and not the exact client;
- historical successful world-entry `31736998731 / 94570936207` was re-inspected at source workflow commit `4392cf4c01703afa344ba074495894a292048eb9` and also launched `packages/Tibia/bin/client` directly with `HOME=/data/home`; therefore the external `Tibia` ELF is not required as the historical successful launch entrypoint;
- `32039938342 / 95417353337 = SUCCESS`: sanitized omitted-state manifest contains exactly 10 entries, digest `9e03d67e62bfda836583f8430b6054a7e4f0bfa11aa919b6936135902ee5b709`; outside package + `launchermetadata.json` these are Qt shader/pipeline cache objects, the external-ELF symlink and `log` directory. No CipSoft/Tibia-named state was found under `.config` or `.local/state` by this bounded inventory.

Fresh exact-window physical discriminator:

- `32046786429 / 95436438152` on `synology-otclient-01`;
- exact current-main merge fence: `8a5fcfd72f2554261eef91a2129c9cc076e730ea` = PASS;
- `WORLDMAP_PRESECRET_TASK_NAMESPACE_PROCESS_COUNT=0`;
- `WORLDMAP_PRESECRET_OFFICIAL_CLIENT_CANDIDATE_COUNT=0`;
- `WORLDMAP_PRESECRET_TARGET_UNIQUENESS=PROVEN`;
- `WORLDMAP_BASELINE_WINDOW_IDENTITY=x11-window:12582929`;
- `WORLDMAP_BASELINE_GDB_ATTACH=PASS`;
- `WORLDMAP_BASELINE_PRE_STORAGE_OBSERVER=ARMED`;
- `WORLDMAP_UI_EXACT_GEOMETRY=1920x1080`;
- `WORLDMAP_XWD_PIXMAP_GEOMETRY=1920x1080`;
- `WORLDMAP_XWD_WINDOW_GEOMETRY=1920x1080`;
- `WORLDMAP_BASELINE_XWD_GEOMETRY_PROOF=PASS`;
- `WORLDMAP_BASELINE_VNC_MAPPING_PRESERVED=MANIFEST_RUNTIME_UNCHANGED`;
- terminal semantic discriminator: `unique_field_classes_required:unmasked=0;masked=0`;
- `WORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=PASS`;
- `WORLDMAP_BASELINE_CLEANUP=COMPLETE`;
- `WORLDMAP_FINAL_NAMESPACE_PROCESS_COUNT=0`.

# Current interpretation boundary

- `external_launcher_required_for_successful_login = DISPROVEN` by the historical successful direct-package-client workflow;
- `missing_persistent_account_or_login_layout_state_in_scanned_XDG_paths = NOT_OBSERVED`; this weakens but does not prove false every possible HOME-state hypothesis;
- `XWD_1920_VS_1020_ROOT_CAUSE = STALE_FIXED_PROOF_GEOMETRY`; this is physically proven by exact X11 topology plus XWD header/pixmap geometry on the same manifest XID;
- `WRONG_WINDOW_ID = DISPROVEN` for the current discriminator; runtime identity, UI identity and exact inspected XID were all `12582929`;
- `ROOT_WINDOW_FALLBACK = NOT_USED`; the command remained `xwd -id "$UI_WIN"`, and static composition rejected root capture;
- `DECORATOR_OR_CHILD_GEOMETRY_MISMATCH = NOT_OBSERVED`; the target was a borderless direct root child with no children or same-PID alternate viewable drawables;
- `VNC_MAPPING_PRESERVED = PROVEN_WITHIN_CURRENT_RUNTIME_CONTRACT`; VNC startup passed, the manifest runtime/window identity remained unchanged, and the proof performed no resize/reparent/recreate operation;
- the remaining blocker is now **after** geometry proof: the coordinate-free semantic Tab scan did not establish any email/password field on the `1920x1080` startup surface;
- this semantic zero-candidate result is the required causal discriminator for the failed pre-secret gate and must not be retried unchanged;
- the workflow is now a no-client hold. No physical retry and no protected credential path may be armed until a materially new UI-state/editability discriminator is designed and statically validated.

Durable evidence includes:

- `20260817-presecret-ui-loader-repairs.md`
- `20260817-xres-ui-window-boundary.md`
- `20260817-1020-desktop-normalization.md`
- `20260817-manifest-owned-ui-window.md`
- `20260817-prelogin-behavioral-proof.md`
- `20260817-restack-native-presecret-source.md`
- `20260817-exact-window-xwd-geometry-causal-discriminator.md`

# Workflow safety state

The PR is in an explicit **no-client hold** after `32046786429 / 95436438152`. Protected credentials remain forbidden until a future physical generation independently passes both harmless editability gates and emits `WORLDMAP_BASELINE_PRESECRET_READY=true`. The baseline login budget remains unconsumed.

# Execution phases

1. **DONE** canonical boundary / cleanup.
2. **DONE** isolated exact-client WARP/XRes path.
3. **DONE** pre-Storage observer gate.
4. **DONE** exact manifest-window topology and dynamic XWD geometry proof; stale fixed `1020x650` parser assumption removed without changing XID/VNC/window topology.
5. **ACTIVE / BLOCKED_ON_NEW_UI_DISCRIMINATOR** physical exact-window pre-secret run reached semantic field discovery but returned zero masked/unmasked text-field candidates; credentials skipped, login budget `0/1`, cleanup complete.
6. **PENDING** patched namespace/preimage/target-uniqueness admission.
7. **PENDING** one task-owned `[19,14]` login/capture after baseline is physically completed.
8. **PENDING** patched rollback/source rehash/cleanup.
9. **PENDING** causal classification, audit, temporary-resource removal, exact-head CI/review/merge/archive.

# Stop criteria

Fail closed on main drift, non-idle/competing official-client candidate state, namespace collision, target ambiguity, observer regression, failure to prove exact manifest XID ownership/topology/XWD geometry, failure of either harmless editable-field probe, any credential-bearing state before handoff, WARP/credential confinement failure, post-submit visual-transition failure, first-row interaction failure, absence of FullMap/map-description proof, source/preimage/hash mismatch, unexpected gameplay/account side effect, crash, or incomplete cleanup.

Any failure **after** `WORLDMAP_BASELINE_LOGIN_SUBMITTED=true` consumes the one baseline login budget and must not be silently retried.

# Checkpoint

```yaml
checkpoint_version: 16
updated_at: 2026-08-17T18:49:00+02:00
base_main: 8a5fcfd72f2554261eef91a2129c9cc076e730ea
current_main_observed: 8a5fcfd72f2554261eef91a2129c9cc076e730ea
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
pr: 475
status: investigating
phase: baseline_presecret_ui_discriminator
runtime_access: ephemeral_isolated
target_uniqueness: PROVEN
mutation_authorized: true
workflow_mode: no_client_hold_after_presecret_discriminator
baseline_client_launches_consumed: 11
baseline_login_consumed: 0
patched_login_consumed: 0
last_completed_step: physical exact-window run 32046786429 / 95436438152 proved manifest XID 12582929, XRes ownership, GDB attach, pre-Storage observer, actual X11 geometry 1920x1080 and matching XWD geometry 1920x1080 without changing window topology; coordinate-free semantic field discovery then returned zero masked/unmasked candidates and failed closed before credentials
blockers:
  - presecret_semantic_field_discriminator_zero_candidates
next_action: design and statically validate a materially new no-secret UI-state/editability discriminator using the now-proven exact 1920x1080 manifest window; do not rerun the same Tab/text-growth classifier, do not arm credential handoff, and keep the workflow no-client until the new discriminator has a distinct causal hypothesis.
```
