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
phase: runtime_admission
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
base_branch: main
base_sha: e1ae4054b17792607c88552f72cdc68ef3a1f294
created: 2026-08-17T13:20:00+02:00
updated: 2026-08-17T13:20:00+02:00
risk: critical
related_pr: pending
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
execution_reason: Repository/GitHub controls the task and evidence; the authorized physical runtime experiment must execute on the canonical Synology Track A runner.
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
canonical_registration: UNKNOWN
canonical_lease_generation: UNKNOWN
registration_lease_generation: UNKNOWN
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: REQUIRED_NOT_PROVEN
target_uniqueness: UNKNOWN
mutation_authorized: false
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

Execute the separately owner-authorized causal runtime discriminator frozen by the merged server-delivery report. Determine whether changing the exact client-local worldmap pair from `[18,14]` to the conservative one-byte `[19,14]` can cause additional authoritative server-delivered map data to arrive, while keeping authoritative inbound delivery, Storage capacity and rendered/pickable extent as separate measurements.

# Required causal comparison

Baseline exact client and the first patched task-owned copy must be compared under bounded, serialized physical runtime conditions. Record at minimum:

```text
SERVER_MAP_DELIVERY_MODEL=CLIENT_DRIVEN|SERVER_DRIVEN|NEGOTIATED|FIXED_PROTOCOL|UNKNOWN
PATCH_CAUSES_ADDITIONAL_AUTHORITATIVE_MAP_DATA=true|false|UNKNOWN
BASELINE_AUTHORITATIVE_INBOUND_EXTENT=<measured or UNKNOWN>
PATCHED_AUTHORITATIVE_INBOUND_EXTENT=<measured or UNKNOWN>
OUTBOUND_EXTENT_NEGOTIATION_CHANGE=true|false|UNKNOWN
STORAGE_EXTENT_CHANGE=true|false|UNKNOWN
RENDER_PICKER_EXTENT_CHANGE=true|false|UNKNOWN
```

Do not infer server delivery from Storage/render growth. The authoritative inbound discriminator must be placed before Storage mutation, using the smallest currently proven exact handler/map-description surface or another directly verified pre-Storage boundary.

# Authorization boundary

The owner has now explicitly authorized the physical runtime and exact client-byte mutation needed for this experiment. This removes the prior #466/#469 owner-authority stop. It does not bypass runtime governance: before any launch/login/mutation the task must establish fresh lease/admission, authoritative registration state, Gate A/required bootstrap/rebind/Gate B, exact identity and uniqueness.

The current admission is deliberately fail-closed discovery state:

```yaml
runtime_access: canonical_bootstrap
canonical_registration: UNKNOWN
gate_a: REQUIRED_NOT_PROVEN
bootstrap: REQUIRED_NOT_PROVEN
mutation_authorized: false
```

No live operation beyond a controller-plane admission inventory is legal until the task checkpoint is updated from fresh direct evidence.

# Execution phases

1. **Admission inventory** — under the current self-hosted runner, read only canonical controller metadata permitted by governance. Do not inspect client/X11/process state yet.
2. **Canonical baseline bootstrap/reuse** — if registration is absent, use the reviewed #371 implementation under current authoritative lease and canonical flock. If present, use required rebind/Gate B. Never create a second exact logged-in canonical session.
3. **Baseline login/world entry** — owner-authorized bounded credential injection; verify SOCKS-only transport and structural/independent IN_GAME state. Credentials must be absent from persistent processes and artifacts.
4. **Baseline pre-Storage capture** — instrument the proven inbound worldmap handler/map-description boundary and record authoritative coordinate/extent/floor envelope plus relevant outbound generic-message serialization where safely recoverable.
5. **Baseline bounded stimulus** — at most one safe adjacent movement plus inverse if needed, closed-loop and structurally confirmed.
6. **Sequential transition** — end/unregister/clean the exact baseline session before any patched login; do not overlap logged-in sessions.
7. **Patched `[19,14]` run** — create a task-owned copy only, verify exact preimage/one-byte diff/patched SHA, launch in an isolated unique namespace with the same confinement, login under the separately authorized one-run budget, and repeat the identical capture/stimulus.
8. **Rollback** — terminate only task-owned patched descendants, remove patched copy, prove original exact source hash unchanged, leave no credential-bearing helper or temporary runtime tooling.
9. **Classification/audit** — compare authoritative inbound envelope before Storage, outbound negotiation, Storage and render/picker separately; preserve `UNKNOWN` for any unmeasured plane. Remove one-shot workflow before final merge.

# Stop criteria

Stop fail-closed on registration/lease/generation drift, competing official-client candidate/session, inability to prove target uniqueness, credential or egress confinement failure, UI/state ambiguity that prevents structural IN_GAME proof, parser/instrumentation anomaly, source/preimage/hash mismatch, unexpected gameplay/account side effect, crash, or inability to cleanly separate baseline and patched sessions.

# Checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-17T13:20:00+02:00
base_main: e1ae4054b17792607c88552f72cdc68ef3a1f294
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
status: investigating
phase: runtime_admission
runtime_access: canonical_bootstrap
last_completed_step: fresh physical task claimed from current main with explicit owner authorization recorded; prior static/design/startup evidence will be reused without repetition
blockers: []
next_action: Run one controller-plane Synology admission inventory that reads only canonical lease/registration metadata; update admission before any process/X11/client observation or launch.
```