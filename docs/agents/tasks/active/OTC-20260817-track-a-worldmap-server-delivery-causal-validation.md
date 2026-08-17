---
task_id: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
status: investigating
agent: ChatGPT
session_id: chatgpt-worldmap-server-delivery-causal-20260817
session_role: canonical_runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: canonical_baseline_bootstrap_repair
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
base_branch: main
base_sha: e1ae4054b17792607c88552f72cdc68ef3a1f294
created: 2026-08-17T13:20:00+02:00
updated: 2026-08-17T13:37:00+02:00
risk: critical
related_pr: 475
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-worldmap-server-delivery-causal-validation.md
  - docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-causal-validation/
  - docs/agents/reports/OTCLIENT-20260817-worldmap-server-delivery-causal-validation.md
  - .github/workflows/track-a-worldmap-server-delivery-causal-validation.yml
modules_touched:
  - track-a-runtime
  - agent-evidence
reuses:
  - docs/agents/reports/OTCLIENT-20260817-worldmap-server-delivery-extent.md
  - docs/agents/tasks/archive/OTC-20260817-track-a-worldmap-server-delivery-extent.md
  - docs/agents/tasks/archive/OTC-20260817-track-a-worldmap-mutation-design.md
  - docs/agents/tasks/archive/OTC-20260817-track-a-worldmap-mutation-physical-validation.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-bootstrap-implementation.md
  - merged PRs #371, #452, #462, #465, #473, #474
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only-control-plus-synology-runtime
execution_reason: Repository/GitHub controls task state and evidence; the owner-authorized physical experiment executes on the canonical Synology Track A runner.
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
RUNTIME_ACCESS: canonical_bootstrap
PERSISTENT_SESSION_ROLE: canonical_runtime_owner
PHYSICAL_E2E_REQUIRED: true
track_id_admission: official-client-re
runtime_access: canonical_bootstrap
runtime_owner_task: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
runtime_namespace: canonical-live-runtime
canonical_registration: ABSENT
canonical_lease_generation: UNKNOWN
registration_lease_generation: NOT_APPLICABLE
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: PASS
target_uniqueness: UNKNOWN
mutation_authorized: true
bootstrap_attempt_limit: 2
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
live_runtime_authorization_source: owner_current_conversation_2026-08-17_worldmap_causal_validation
client_byte_mutation_authorized: true
bootstrap_for_worldmap_authorized: true
login_for_worldmap_authorized: true
second_live_session_authorized: false
owner_authorization_source: current conversation after explicit statement that physical runtime plus client-byte mutation required separate authorization
owner_authorization_text: "wykonaj i czekam na wyniki"
owner_authorization_scope: bounded baseline exact-client versus first [19,14] causal worldmap server-delivery experiment, including required bootstrap/login/relogin, reversible movement, instrumentation and rollback
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
  patched_sha256_prior_startup_canary: 7c8d936fa43e4a026d2a69c32ff30fdea149bb7eff7938c1b1acfc173899b44c
launch_budget:
  canonical_exact_bootstrap_max: 2
  canonical_exact_bootstrap_repair_reason: attempt 1 used obsolete raw worker instead of trusted-main #465 XRes-composed worker; no login/gameplay and rollback independently clean
  patched_ephemeral_login_max: 1
  simultaneous_logged_in_sessions_max: 1
  consumed_canonical_exact_bootstrap: 1
  consumed_patched_ephemeral_login: 0
safety:
  direct_unapproved_egress: forbidden
  warp_socks_required: true
  raw_client_commit_or_upload: forbidden
  credentials_in_logs_or_artifacts: forbidden
  broad_process_cleanup: forbidden
  canonical_source_patch_in_place: forbidden
  patched_copy_task_owned_only: true
  rollback_required: true
  canonical_registration_manual_edit: forbidden
  owner_funded_ai_api: forbidden
invocation_started_at: 2026-08-17T13:20:00+02:00
last_progress_at: 2026-08-17T13:37:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: runtime-repair
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Objective

Execute the separately owner-authorized causal runtime discriminator frozen by merged #473/#474. Compare the exact baseline `[18,14]` with the conservative one-byte `[19,14]` task-owned mutation and determine whether additional authoritative map data arrives from the server. Authoritative inbound delivery, Storage and rendered/pickable extent are separate measurements.

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

# Admission and attempt history

Fresh controller-plane inventory run `32025074618`, job `95372681355`, exact head `9ce5c5cafebb833275f6d375fdfeca21049e1c0c` proved released generation-7 lease, no registration, unchanged metadata and no process/X11/client observation.

Bootstrap attempt 1: run `32025398762`, job `95373646537`, exact head `4296c2376fc8585fa62f6edf040ee88db453dbc3` acquired generation 8, proved WARP/Xvfb/VNC startup and physically reached `client_start`, then failed `client_window_missing` / `bootstrap_worker_failed`. No credentials/login/gameplay/mutation occurred.

The attempt used `.github/scripts/tibia-official-client-re-canonical-live-session.sh` directly, which still contains the legacy xdotool PID/name selector. Trusted main already contains merged #465 (`f8e628a255a18ec92839bbb45ef0e3b40bef8605`) whose explicit purpose is to generate a canonical worker replacing that selector with raw XRes XID→PID ownership. Therefore the first failure is an execution-composition defect, not a client/worldmap semantic failure.

Independent rollback audit run `32025665881`, job `95374436911`, head `4d011ebef3fe500a125caae7fda287ac8498ff52` proved generation-8 lease released, registration absent, session root absent, token absent and zero canonical-marked processes. Durable record: `docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-causal-validation/20260817-baseline-bootstrap-attempt-1.md`.

Under `ANTI_STALL_AND_EXECUTION_BUDGET.md`, this checkpoint authorizes exactly one evidence-based repair with materially changed input. It does not authorize an identical retry. Attempt 2 must generate the #465 XRes-composed worker, prove the legacy selector is absent, and pass that generated worker to the same reviewed #371 transition. Any second physical bootstrap failure is analyzed once; no third bootstrap is authorized by this checkpoint.

# Execution phases

1. **DONE — admission inventory.**
2. **ACTIVE — one XRes-corrected canonical baseline bootstrap repair.**
3. **PENDING — baseline login/world entry after fresh registration/Gate B admission update.**
4. **PENDING — baseline pre-Storage worldmap capture.**
5. **PENDING — bounded baseline movement stimulus.**
6. **PENDING — sequential exact-session teardown/unregister before patched run.**
7. **PENDING — task-owned patched `[19,14]` run.**
8. **PENDING — rollback/source rehash/cleanup.**
9. **PENDING — causal classification, audit, workflow removal, CI/review/merge/archive.**

# Stop criteria

Fail closed on lease/generation/registration drift, competing exact-client candidate, inability to prove target uniqueness, WARP/credential confinement failure, ambiguous world entry, instrumentation anomaly, source/preimage/hash mismatch, crash, unexpected gameplay/account side effect, inability to separate baseline and patched sessions, or exhaustion of the single XRes repair attempt.

# Checkpoint

```yaml
checkpoint_version: 3
updated_at: 2026-08-17T13:37:00+02:00
base_main: e1ae4054b17792607c88552f72cdc68ef3a1f294
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
pr: 475
status: investigating
phase: canonical_baseline_bootstrap_repair
runtime_access: canonical_bootstrap
last_completed_step: attempt-1 failure isolated to obsolete worker composition and independently proven rollback-clean
blockers: []
next_action: Generate the merged-#465 XRes canonical worker, verify the legacy selector is absent, then execute exactly one repaired bootstrap transaction with credentials/login/gameplay disabled.
```