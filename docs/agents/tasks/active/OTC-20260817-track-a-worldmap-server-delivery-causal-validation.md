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
phase: baseline_ephemeral_observer_repair
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
base_branch: main
base_sha: e1ae4054b17792607c88552f72cdc68ef3a1f294
created: 2026-08-17T13:20:00+02:00
updated: 2026-08-17T13:52:00+02:00
risk: critical
related_pr: 475
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-worldmap-server-delivery-causal-validation.md
  - docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-causal-validation/
  - docs/agents/reports/OTCLIENT-20260817-worldmap-server-delivery-causal-validation.md
  - .github/workflows/track-a-worldmap-server-delivery-causal-validation.yml
  - .github/scripts/track-a-worldmap-causal-ephemeral-baseline.sh
modules_touched:
  - track-a-runtime
  - agent-evidence
reuses:
  - docs/agents/reports/OTCLIENT-20260817-worldmap-server-delivery-extent.md
  - docs/agents/tasks/archive/OTC-20260817-track-a-worldmap-server-delivery-extent.md
  - docs/agents/tasks/archive/OTC-20260817-track-a-worldmap-mutation-design.md
  - docs/agents/tasks/archive/OTC-20260817-track-a-worldmap-mutation-physical-validation.md
  - merged PRs #371, #452, #462, #465, #473, #474
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-control-plus-synology-ephemeral-runtime
execution_reason: The canonical bootstrap one-shot was consumed before registration by an obsolete worker composition; repository admission explicitly supports task-owned ephemeral_isolated physical sessions without canonical registration or lease mutation.
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_pressure: high
context_growth: stable
context_score: 11
estimate_confidence: medium
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
owner_authorization_source: current conversation after explicit statement that physical runtime plus client-byte mutation required separate authorization
owner_authorization_text: "wykonaj i czekam na wyniki"
owner_authorization_scope: bounded baseline exact-client versus first [19,14] causal worldmap server-delivery experiment, including required login/relogin, reversible movement, instrumentation and rollback
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
  baseline_ephemeral_client_launches_consumed: 1
  baseline_ephemeral_login_max: 1
  baseline_ephemeral_login_consumed: 0
  baseline_ephemeral_observer_repair_max: 1
  baseline_ephemeral_observer_repairs_consumed: 0
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
last_progress_at: 2026-08-17T13:52:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: baseline-observer-repair
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Objective

Execute the owner-authorized causal runtime discriminator frozen by merged #473/#474. Compare the exact baseline `[18,14]` with the conservative one-byte `[19,14]` task-owned mutation and determine whether additional authoritative map data arrives from the server. Authoritative inbound delivery, Storage and rendered/pickable extent remain separate measurements.

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

# Canonical boundary

Controller inventory run `32025074618` proved released generation-7 lease and absent registration. Canonical bootstrap run `32025398762` physically launched once and failed the obsolete raw-worker `client_window_missing` selector before registration, credentials or login. Cleanup run `32025665881` proved generation-8 lease released, registration/session/token absent and zero canonical-marked survivors. A proposed canonical XRes retry was then correctly refused pre-launch by governance in run `32025860356` because canonical bootstrap is one-shot. This guardrail remains intact.

# Ephemeral baseline attempt 1

Run `32026662197`, job `95377398485`, head `68e1bbaa75305c54689b8d7e1d2015a112f55c0c` directly proved the task-owned isolated path works through exact client/XRes identity:

```text
WORLDMAP_CAUSAL_EPHEMERAL_BASELINE_ADMISSION=PASS
WORLDMAP_BASELINE_CANONICAL_CONTROLLER_IDLE=PASS
WORLDMAP_BASELINE_PREEXISTING_NAMESPACE_PROCESS_COUNT=0
TRACK_A_CANONICAL_XRES_ADAPTER=PASS
WORLDMAP_BASELINE_EPHEMERAL_XRES_WORKER=PASS
TRACK_A_CANONICAL_STAGE=warp_egress_probe_pass
TRACK_A_CANONICAL_STAGE=client_window_wait_pass
WORLDMAP_BASELINE_MANIFEST_FENCE=PASS
WORLDMAP_BASELINE_CLIENT_PID=25587
WORLDMAP_BASELINE_WINDOW_IDENTITY=x11-window:12582929
WORLDMAP_BASELINE_TARGET_UNIQUENESS=PROVEN
```

The run then stopped before any account credential was used because the pre-Storage GDB observer process exited before attachment could be proven:

```text
WORLDMAP_BASELINE_ERROR=gdb_observer_not_alive
WORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=PASS
WORLDMAP_BASELINE_CLEANUP=COMPLETE
```

No login was submitted, no gameplay input occurred, and no structural evidence artifact was uploaded. Durable record: `docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-causal-validation/20260817-ephemeral-baseline-attempt-1.md`.

Historical accepted observer commit `734f845deace5a26efa09b96a168bea0c05272f0` ran the same toolroot GDB under task/toolroot `HOME`, `DISPLAY`, `PATH` and `LD_LIBRARY_PATH`. The attempt-1 harness supplied the GDB executable path but omitted that toolroot runtime environment. This is the single current evidence-based repair hypothesis. The repair must also emit a sanitized pre-login GDB diagnostic on another attach failure; no credential values exist at that gate.

# Execution phases

1. **DONE — canonical admission / one-shot boundary and rollback.**
2. **DONE — exact ephemeral client/XRes/WARP namespace path physically proven.**
3. **ACTIVE — one pre-login observer repair with toolroot GDB runtime environment.**
4. **PENDING — baseline login + structural FullMap/map-description capture + Right/Left.**
5. **PENDING — persist baseline measured extent and prove cleanup.**
6. **PENDING — fresh patched namespace uniqueness/source/preimage admission.**
7. **PENDING — task-owned `[19,14]` ephemeral run with identical capture/stimulus.**
8. **PENDING — patched rollback/source rehash/cleanup.**
9. **PENDING — causal comparison/classification/audit/workflow+helper removal/CI/review/merge/archive.**

# Stop criteria

Fail closed on non-idle canonical controller state, namespace collision, target ambiguity, WARP/credential confinement failure, missing secret/tooling before safe login, second observer attach failure after the one materially changed repair, ambiguous character selection, absence of structural FullMap/map-description proof, instrumentation anomaly, source/preimage/hash mismatch, unexpected gameplay/account side effect, crash, inability to cleanly terminate the exact session, or inability to prove baseline and patched sessions are non-overlapping.

# Checkpoint

```yaml
checkpoint_version: 5
updated_at: 2026-08-17T13:52:00+02:00
base_main: e1ae4054b17792607c88552f72cdc68ef3a1f294
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
pr: 475
status: investigating
phase: baseline_ephemeral_observer_repair
runtime_access: ephemeral_isolated
last_completed_step: exact isolated client/XRes path proven; attempt stopped pre-credentials at observer attach and cleaned up with source rehash PASS
blockers: []
next_action: Supply historical toolroot HOME/DISPLAY/PATH/LD_LIBRARY_PATH to GDB, expose a sanitized pre-login attach diagnostic if it still exits, then execute exactly one repaired baseline attempt.
```