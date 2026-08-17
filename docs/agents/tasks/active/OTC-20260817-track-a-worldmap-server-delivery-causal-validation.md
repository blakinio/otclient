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
phase: baseline_ephemeral_observer_repair_confirmed
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
base_branch: main
base_sha: 7fa86095667dcc71005fbf366921c4cb565ebc3f
restack_commit: d14b3f6449ba45307e0889cb5f52d45a5722bbdd
created: 2026-08-17T13:20:00+02:00
updated: 2026-08-17T13:55:00+02:00
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
  - docs/agents/tasks/archive/OTC-20260817-track-a-worldmap-mutation-design.md
  - docs/agents/tasks/archive/OTC-20260817-track-a-worldmap-mutation-physical-validation.md
  - merged PRs #371, #452, #462, #465, #473, #474
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-control-plus-synology-ephemeral-runtime
execution_reason: Repository admission explicitly supports task-owned ephemeral_isolated physical sessions without canonical registration or lease mutation; the canonical bootstrap one-shot remains consumed and is not bypassed.
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
owner_authorization_source: current conversation after explicit statement that physical runtime plus client-byte mutation required separate authorization
owner_authorization_text: "wykonaj i czekam na wyniki"
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
last_progress_at: 2026-08-17T13:55:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: baseline-observer-repair-confirmed
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Objective

Execute the owner-authorized causal discriminator from merged #473/#474. Compare the exact `[18,14]` baseline against the first task-owned `[19,14]` mutation and measure authoritative inbound worldmap delivery before Storage independently from Storage/render/picker effects.

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

# Current verified boundary

- Controller inventory `32025074618 / 95372681355`: released canonical generation 7; registration absent; no live process/X11 observation.
- Canonical bootstrap `32025398762 / 95373646537`: one physical exact-client launch; obsolete raw selector failed before registration/credentials/login. Cleanup `32025665881 / 95374436911`: released generation 8, registration/session/token absent, zero canonical survivors.
- Canonical XRes repair `32025860356 / 95375014679`: refused by governance before worker/client launch because canonical bootstrap is one-shot.
- Ephemeral baseline attempt 1 `32026662197 / 95377398485`: current XRes path and task-owned namespace physically proved through a verified exact-client window and target uniqueness; observer exited before credentials, login or gameplay. Source rehash and cleanup passed.
- Deterministic GDB isolation `32027110459 / 95378725544` on restacked head `d14b3f6449ba45307e0889cb5f52d45a5722bbdd`: raw toolroot GDB returned `127` because `libpython3.12.so.1.0` was unavailable; the same binary with toolroot runtime library environment returned `0`. The observer failure root cause is therefore directly proven.
- Main drift from `e1ae4054...` to `7fa86095667dcc71005fbf366921c4cb565ebc3f` contained only independent agent-orchestrator tooling/lifecycle files. Branch restack commit: `d14b3f6449ba45307e0889cb5f52d45a5722bbdd`.

Durable evidence:
- `docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-causal-validation/20260817-baseline-bootstrap-attempt-1.md`
- `docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-causal-validation/20260817-ephemeral-baseline-attempt-1.md`
- `docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-causal-validation/20260817-gdb-environment-isolation.md`

# Active repair

The only permitted baseline observer repair is to preserve the exact baseline experiment while launching the observer with the proven toolroot GDB runtime library environment. This is not an identical retry. The repair must still arm the observer before credential use; a second attach failure stops this gate.

# Execution phases

1. **DONE** canonical boundary and cleanup.
2. **DONE** isolated exact client/XRes/WARP path proven.
3. **DONE** observer failure root cause mechanically proven without client launch.
4. **ACTIVE** one repaired exact baseline attempt with toolroot GDB environment.
5. **PENDING** persist measured baseline extent and terminal cleanup.
6. **PENDING** fresh patched namespace uniqueness/source/preimage admission.
7. **PENDING** `[19,14]` task-owned ephemeral run with identical capture/stimulus.
8. **PENDING** patched rollback/source rehash/cleanup.
9. **PENDING** causal classification, independent audit, temporary resource removal, exact-head CI/review/merge/archive.

# Checkpoint

```yaml
checkpoint_version: 6
updated_at: 2026-08-17T13:55:00+02:00
base_main: 7fa86095667dcc71005fbf366921c4cb565ebc3f
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
pr: 475
status: investigating
phase: baseline_ephemeral_observer_repair_confirmed
runtime_access: ephemeral_isolated
last_completed_step: branch restacked on current main and GDB observer root cause directly isolated to missing toolroot libpython runtime path
blockers: []
next_action: Re-enable exactly one baseline workflow generation with the proven toolroot GDB LD_LIBRARY_PATH supplied only to the observer process; preserve all other baseline gates and stop on any second observer attach failure.
```
