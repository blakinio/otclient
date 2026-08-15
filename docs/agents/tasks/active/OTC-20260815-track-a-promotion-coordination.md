---
task_id: OTC-20260815-track-a-promotion-coordination
status: active
agent: ChatGPT
session_id: chatgpt-coordinator-20260815-1403
session_role: coordinator
session_rotation_count: 3
project_lane: otclient
lane: track-a-coordination
track_id: official-client-re
task_kind: integration
phase: promotion-review-integration
branch: docs/OTC-20260815-track-a-promotion-coordination
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/docs/OTC-20260815-track-a-promotion-coordination
worktree_mode: isolated_branch_checkout_equivalent
created: 2026-08-15T12:23:00+02:00
updated: 2026-08-15T14:08:00+02:00
risk: medium
related_pr: 300
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-promotion-coordination.md
  - docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/**
  - docs/agents/reports/OTCLIENT-20260815-track-a-promotion-coordination.md
  - docs/agents/tasks/archive/OTC-20260814-official-client-capability-experiment-sweep.md
  - tools/tibia_worldmap_reconstruction/**
  - tests/tools/tibia_worldmap_reconstruction/**
  - docs/agents/reports/OTC-20260812-worldmap-reconstruction.md
  - tools/tibia_runtime_bridge/**
  - tests/tools/tibia_runtime_bridge/**
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
modules_touched:
  - agent-coordination
  - tibia-worldmap-reconstruction
  - tibia-runtime-bridge
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_pressure: high
context_growth: controlled
decomposition_decision: phased
invocation_started_at: 2026-08-15T12:48:00+02:00
last_progress_at: 2026-08-15T14:08:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: current
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 3
stall_warnings: 0
---

# Objective

Keep canonical Track A (`official-client-re`) true, reproducible and progressively complete. Research branches remain Draft-only; this task alone performs campaign promotion/integration. Track B remains outside mutation authority.

# Live-state contract

```yaml
TASK_ID: OTC-20260815-track-a-promotion-coordination
TASK_RECORD: docs/agents/tasks/active/OTC-20260815-track-a-promotion-coordination.md
PROJECT_LANE: otclient
BASE_MAIN: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
BRANCH: docs/OTC-20260815-track-a-promotion-coordination
WORKTREE: github-only://blakinio/otclient/refs/heads/docs/OTC-20260815-track-a-promotion-coordination
```

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Promotion ledger

## ACCEPT

- #283 bounded read-only runtime bridge implementation; `session-status` remains DERIVED until live structural correlation.
- exact-build reversible structural world transition from run `31806312967` / job `94785974126`; standalone player XYZ and A3/A4 remain unproven.

## ACCEPT_WITH_EDITS

- #279 fail-closed worldmap reconstruction tooling; real capture/mappings/complete OTBM remain UNKNOWN.
- #290 bounded historical login/recovery procedure retained as `REVALIDATION_REQUIRED`; coordinator login-update evidence corrects the stale assumption that a newer child binary is currently required.
- #304 bounded exact-build quantitative coverage baseline; exact accepted evidence snapshot is coordinator-owned; source Draft closed unmerged.
- #301 bounded P2 writer-retention provenance; exact final source head `50e2d95c7dc8b0759eb6233a3751f73434958e88`; final provenance run `31883456870` SUCCESS; final required PR CI `31883459362` SUCCESS; review threads `0`; exact accepted evidence/result/reproducer/workflow blobs copied under coordinator-owned `p2-writer-ownership/source-snapshot/` in commit `6e299fdec0615b24db5512ff2813fe7d6cacafda`.

Accepted #301 boundary:

```yaml
TProtocolClientMessageProcessor_retains_writer_branch: FACT
writer_intermediate_class: UNKNOWN
writer_relative_to_DualConnection: INFERENCE_UPSTREAM_ON_CLIENT_PROCESSOR_BRANCH
direct_DualConnection_writer_member: NOT_PROVEN
framing_order: UNKNOWN
transform_boundary: UNKNOWN
final_binary_egress: UNKNOWN
causal_local_harness: UNKNOWN
P2_complete: false
```

## REVALIDATION_REQUIRED

- #302 P0 current state changed: old run `31880617510` is cancelled and branch advanced beyond the previously reviewed head; current exact task/runs must be refetched before disposition.
- #303 RUNTIME must be refetched after the P0 serialized-lane state change; cleanup hardening remains safety evidence only.

## RETURN_FOR_EVIDENCE

- #295 material review findings plus Track B ownership collision.

## REJECT/SUPERSEDE

- #289 broad stale continuation and superseded P2 model;
- #296 stale lifecycle Draft after accepted correction integration;
- #277 stale Oteryn-dependent handover with unique negative history preserved;
- #280 superseded only as active Track A dependency; broader infrastructure remains separately owned/open.

# Quantitative baseline

```yaml
protocol_identifier_inventory: 349/349
generated_message_semantic_support: UNKNOWN/349
protocol_handler_qmeta_records: 47/47
direct_qt_connection_raw_census: 2184/2184
direct_qt_connection_semantic_classification: UNKNOWN/2184
legacy_qobject_connect_edges: 40/41
high_information_gameaction_sender_metaobjects: 29/31
p0_top_level_requirement_registry: 16/16
p0_live_read_coverage: UNKNOWN/UNKNOWN
bridge_v1_profile_target_inventory: 7/7
p1_overall_field_evidence_coverage: UNKNOWN/UNKNOWN
restart_relogin_stability: UNKNOWN/1
```

Inventory completeness is not semantic completion. The prior `p2_chain_closure: UNKNOWN/5` registry remains a historical quantitative baseline until its item mapping is explicitly reconciled with the newly accepted retention fact; no numerator is invented here.

# Canonical non-completion boundary

```yaml
P2: PARTIAL_writer_retention_proven_transform_order_final_egress_harness_open
P1: PARTIAL_read_only_bridge_integrated_live_authority_unknown
P0: PARTIAL_structural_world_transition_fact_direct_player_state_unknown
RUNTIME: PARTIAL_one_generation_world_evidence_restart_relogin_unknown
ACTION: A3_A4_NOT_PROVEN
COMPLETE: false
```

# Acceptance inventory

- [x] #301 exact final head independently reviewed after researcher release;
- [x] #301 exact source final CI/provenance green and review threads clear;
- [x] #301 bounded retention fact/inference promoted by exact Git blob SHA under coordinator ownership;
- [x] campaign report updated without claiming direct DualConnection writer membership or P2 completion;
- [ ] exact-head coordinator CI terminal for this P2 integration generation;
- [ ] source #301 closed unmerged after validated promotion;
- [ ] #302 current exact head/task/runs revalidated;
- [ ] #303 current exact head/task/runs revalidated after P0 lane change;
- [ ] next highest-information unresolved P2/P0/RUNTIME/ACTION hypothesis dispatched/executed;
- [ ] final programme audit/CI/PR hygiene/task archive/ownership release complete.

# Next action

Validate the exact coordinator integration head for the #301 promotion. If green, close #301 Draft unmerged. Then immediately refetch #302 and #303 exact live state/runs and continue whichever lane has new evidence or an executable unblocked hypothesis. Do not retain stale `queued`/serialization claims without current evidence.
