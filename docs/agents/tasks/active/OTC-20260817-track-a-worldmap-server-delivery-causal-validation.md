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
phase: canonical_baseline_bootstrap
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
base_branch: main
base_sha: e1ae4054b17792607c88552f72cdc68ef3a1f294
created: 2026-08-17T13:20:00+02:00
updated: 2026-08-17T13:31:00+02:00
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
bootstrap_attempt_limit: 1
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
  canonical_exact_bootstrap_max: 1
  patched_ephemeral_login_max: 1
  simultaneous_logged_in_sessions_max: 1
  consumed_canonical_exact_bootstrap: 0
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

# Fresh admission evidence

Controller-plane inventory run `32025074618`, job `95372681355`, exact head `9ce5c5cafebb833275f6d375fdfeca21049e1c0c`, runner `synology-otclient-01` completed successfully and directly proved:

```yaml
lease: PRESENT
lease_status: released
lease_generation_before_new_task_acquire: 7
lease_controller_task: null
lease_controller_session: null
lease_expired: false
canonical_registration: ABSENT
admission_result: REGISTRATION_ABSENT
control_metadata_unchanged: true
process_observation: false
x11_observation: false
client_mutation: false
```

Track A runtime governance on that exact head: run `32025074494` / #786 = SUCCESS.

Because registration is directly proven ABSENT and the reviewed bootstrap implementation from #371 is present on trusted main, this checkpoint authorizes exactly one bootstrap transaction. The bootstrap transaction itself may launch only the exact fenced client plus canonical Xvfb/VNC/WARP helpers. It may not use credentials, login or gameplay. Those require a later admission update after authoritative registration/lease/identity are proven.

# Execution phases

1. **DONE — admission inventory.** Controller metadata only; no process/X11/client observation.
2. **ACTIVE — canonical baseline bootstrap.** Acquire a fresh task-owned canonical lease, execute the reviewed cancellation-safe bootstrap transaction and require exact identity, uniqueness, WARP, window and registration publication.
3. **PENDING — baseline login/world entry.** Update admission first; then owner-authorized bounded credential injection and structural/independent IN_GAME proof.
4. **PENDING — baseline pre-Storage capture.** Instrument the accepted `FullMap @ 0x00cec8d0` / `MapDescription @ 0x019a8a80` surface before Storage and record authoritative coordinate/floor envelope.
5. **PENDING — bounded baseline stimulus.** At most one safe adjacent movement plus inverse, closed-loop.
6. **PENDING — sequential transition.** End/unregister/clean exact session before patched login; never overlap logged-in sessions.
7. **PENDING — patched `[19,14]` run.** Task-owned copy only; exact preimage/one-byte diff/SHA; same confinement and equivalent capture.
8. **PENDING — rollback.** Remove only task-owned patched descendants/copy and prove original source hash unchanged.
9. **PENDING — classification/audit/cleanup.** Preserve UNKNOWN for any unmeasured plane; remove one-shot workflow before merge.

# Stop criteria

Fail closed on lease/generation/registration drift, competing exact-client candidate, inability to prove target uniqueness, WARP/credential confinement failure, ambiguous world entry, instrumentation anomaly, source/preimage/hash mismatch, crash, unexpected gameplay/account side effect, or inability to separate baseline and patched sessions.

# Checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-17T13:31:00+02:00
base_main: e1ae4054b17792607c88552f72cdc68ef3a1f294
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
pr: 475
status: investigating
phase: canonical_baseline_bootstrap
runtime_access: canonical_bootstrap
last_completed_step: fresh controller-plane inventory proved registration absent and released generation-7 lease with no live observation or mutation
blockers: []
next_action: Acquire a new task-owned canonical lease and execute exactly one reviewed #371 bootstrap transaction with credentials/login/gameplay disabled; persist resulting registration/lease/identity before any login.
```