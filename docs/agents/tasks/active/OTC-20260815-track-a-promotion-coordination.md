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
updated: 2026-08-15T14:03:00+02:00
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
last_progress_at: 2026-08-15T14:03:00+02:00
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

Rotation 3 claimed after rotation 2 released this task to `ready` and P2 researcher #301 independently reached a `ready` handoff. Two intervening coordinator-owned login-revalidation evidence commits (`9ae9eeee...`, `d582548b...`) did not claim the task or modify the task record; they are retained and will be reviewed as part of final reconciliation.

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
- #290 bounded historical login/recovery procedure retained as `REVALIDATION_REQUIRED`.
- #304 bounded exact-build quantitative coverage baseline; source head `43a60bd96cc644b656b200c9edbfb75578b330b6`, source CI `31882010038` SUCCESS, exact accepted blobs promoted under coordinator ownership, source Draft closed unmerged.

## REVIEW_REQUIRED_THIS_ROTATION

- #301 final P2 writer-ownership handoff head `50e2d95c7dc8b0759eb6233a3751f73434958e88`: researcher proposes `ACCEPT_WITH_EDITS`; final task-specific provenance run `31883456870` SUCCESS and final required PR CI `31883459362` SUCCESS. Must be independently reviewed before promotion.
- #302 P0 live state changed after prior checkpoint: stale run `31880617510` is now cancelled and branch head advanced to `ab22e9c495daea050f45e90b3e38b78062539d59`; do not retain the old queued-blocker statement without revalidation.
- #303 RUNTIME must be rechecked after P0 lane state changed; existing cleanup hardening is safety evidence only.

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

Inventory completeness is not semantic completion.

# Canonical non-completion boundary

```yaml
P2: OPEN_writer_retention_review_transform_order_final_egress_harness
P1: PARTIAL_read_only_bridge_integrated_live_authority_unknown
P0: PARTIAL_structural_world_transition_fact_direct_player_state_unknown
RUNTIME: PARTIAL_one_generation_world_evidence_restart_relogin_unknown
ACTION: A3_A4_NOT_PROVEN
COMPLETE: false
```

# Next action

Independently review exact #301 head `50e2d95c7dc8b0759eb6233a3751f73434958e88`, its task/evidence/reproducer, changed paths, zero review threads, source artifact fence and final exact-head CI. Assign one coordinator disposition. If accepted, promote only the bounded writer-retention fact/inference under coordinator-owned evidence, update the campaign report, validate exact coordinator head and close #301 unmerged. Then immediately re-evaluate the changed P0/RUNTIME live state before choosing the next independent lane.
