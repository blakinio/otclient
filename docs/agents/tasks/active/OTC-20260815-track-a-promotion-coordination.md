---
task_id: OTC-20260815-track-a-promotion-coordination
status: waiting
agent: unassigned
session_id: null
session_role: coordinator
session_rotation_count: 7
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
updated: 2026-08-15T17:43:00+02:00
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
invocation_started_at: 2026-08-15T17:30:00+02:00
last_progress_at: 2026-08-15T17:43:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: coordinator-waiting-checkpoint
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
last_verified_integration_head: da96c97b91c236be6f97e4edf80214f77b4b2492
last_verified_integration_ci_run: 31893397505
last_verified_integration_ci_state: success
lease_released_at: 2026-08-15T17:43:00+02:00
waiting_reason: active_independent_runtime_and_p2_research_plus_p0_runtime_dependency_and_unresolved_map_observation_ownership_lifecycle
---

# Objective

Keep canonical Track A (`official-client-re`) true, reproducible and progressively complete. Research branches remain Draft-only; this task promotes only bounded independently reviewed evidence. Track B remains outside mutation authority.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Promotion ledger

## ACCEPT

- #283 bounded read-only runtime bridge; live authority/session epoch remains UNKNOWN.
- exact-build reversible structural world transition from run `31806312967` / job `94785974126`; standalone player XYZ and A3/A4 remain unproven.

## ACCEPT_WITH_EDITS

- #279 fail-closed worldmap reconstruction tooling; real capture/mappings/complete OTBM remain UNKNOWN.
- #290 bounded historical login/recovery procedure retained only as revalidation input.
- #304 bounded quantitative coverage baseline; exact source snapshot promoted; source Draft closed unmerged. Inventory completeness is not semantic completion.
- #301 bounded P2 writer-retention evidence; exact source snapshot promoted; source Draft closed unmerged.
- #305 bounded P2 intermediate-vtable/type correction; exact source snapshot promoted; source Draft closed unmerged; integration generation `0ade6404c5b43f5fe468b8dd748846406d4c856e` passed CI `31884644268`.
- #302 bounded static P0 slice from reviewed source head `6f838d1089968d216e506cd272e7b98680da9fc8`. Static run `31892019505` / job `95029600292` SUCCESS, artifact `9248797952` digest `sha256:04835ab0bac7ffc43e161e8b2118c90a3d2197f7011385a6758cd7706c93a584`, source exact-head CI `31892202128` SUCCESS, review threads 0. Promoted FACT: `playerPosition` literal `0x1cdde3f` (supersedes stale `0x1cddd3f`), distinct `playerPositionChanged` control context, relocation-backed provider/worldmap/TPlayerData anchors, exact `TPlayerData` vptr/typeinfo boundary. EDIT: `0x8367c1` is INFERENCE / structural byte-pattern xref lead until a real disassembler confirms the instruction boundary; `0x8367c2` is decoder overlap; nearby semantic ownership/accessor graph remains INFERENCE. Direct authoritative XYZ remains UNKNOWN.

## ACTIVE / WAITING RESEARCH

- #302 overall P0 objective remains `RETURN_FOR_EVIDENCE / WAITING_ON_RUNTIME`. Direct authoritative XYZ, member/accessor/encoding, direct-vs-render-copy discrimination, causal controls, repeated live observations and fresh PID/relogin stability remain UNKNOWN. Its research lease is released.
- #303 RUNTIME is actively owned by session `chatgpt-runtime-researcher-20260815-1730`; current Draft head observed at `4cb98e0b149a5eae21261be468618ec269a8a976`. The lane has recovered runner/WARP/relay/Xvfb/loader/bundled-Qt/software-renderer prerequisites and falsified several isolated launch hypotheses, but restart/relogin semantic proof remains UNKNOWN. Current discriminator changes only task-owned Xvfb cwd provenance on display `:115`; coordinator must not mutate its branch/runtime.
- #306 P2 first-transform-boundary is actively owned by session `chatgpt-p2-transform-researcher-20260815-1724`. Initial head `2816c5d9fc1b62b99afaa920c63d2113d678d6fb` failed CI `31892928343` at actionlint/ShellCheck `SC2129`; coordinator posted the exact failure. Researcher advanced to `da94bcb21d82a05f043a4ec8c87816820342090e`, repairing the grouped append. On the last permitted observation its custom run `31893175624` and repository CI `31893179860` were still executing; no semantic result is promoted from that active head.

## RETURN_FOR_EVIDENCE

- #295 map-observation ownership correction remains not promotable. Four material review threads are unresolved: overlapping `MAP_OBSERVATION_V1.md` ownership, weakened unconditional raw-packet prohibition, weakened external-consumer authorization boundary and dropped non-negative integer `producer.protocol_version` constraint. Source base is stale.
- The ownership finding remains current rather than historical: merged PR #291 left `docs/agents/tasks/active/OTC-20260813-map-observation-export.md` on `main` with `status: blocked` and `docs/agents/contracts/MAP_OBSERVATION_V1.md` still in its `owned_paths`. #295 cannot safely claim or rewrite that contract until lifecycle/ownership is deliberately reconciled.

## RELATED NON-TRACK-A IMPLEMENTATION

- #292 remains open OTClient `Map`/`Tile` observation recorder and is not official-client Track A runtime authority. Coordinator does not mutate it.
- #284 remains Track B and outside Track A authority.

## REJECT / SUPERSEDE

- #289 broad stale continuation and superseded P2 model;
- #296 stale lifecycle Draft after accepted correction integration;
- #277 stale Oteryn-dependent handover;
- #280 superseded only as active Track A dependency; broader infrastructure remains separately owned/open.

# Canonical non-completion boundary

```yaml
P2: PARTIAL_writer_retention_and_intermediate_type_structure_proven_transform_order_final_egress_harness_open
P1: PARTIAL_read_only_bridge_integrated_live_authority_unknown
P0: PARTIAL_static_playerPosition_anchor_plus_structural_world_transition_direct_authoritative_player_state_unknown
RUNTIME: PARTIAL_historical_single_generation_world_evidence_restart_relogin_unknown
ACTION: A3_A4_NOT_PROVEN
COMPLETE: false
```

# Quantitative baseline

```yaml
protocol_identifier_inventory: 349/349
generated_message_semantic_support: UNKNOWN/349
protocol_direct_inbound_qmeta_links: 27/349
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

# Coordinator integration validation

### FACT

- `main` was reverified at `8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45` during this rotation.
- coordinator integration head `6fd1df4f1687e4ca0c1196caad4d4d1d1916079f` passed repository CI `31892866367`.
- a subsequent full-scope audit found unrelated W7/OTClient-v2 drift in shared `docs/agents/MODULE_CATALOG.md`: two existing W7 documentation/context fields had been changed while integrating Track A.
- coordinator-owned scope repair restored those unrelated rows exactly and retained only the Track A catalogue additions. Re-audited `MODULE_CATALOG.md` diff now contains only the review-date update plus the two official-client research tooling rows.
- repaired integration head `da96c97b91c236be6f97e4edf80214f77b4b2492` passed exact-head repository CI `31893397505` with conclusion `success`.
- PR #300 had zero unresolved review threads at the last review-thread check.

The present waiting-checkpoint commit is documentation-only and intentionally follows that verified integration generation; its own CI must not be used to expand any capability claim.

# Acceptance inventory

- [x] #304 independently reviewed, promoted boundedly and source Draft closed unmerged.
- [x] #301 independently reviewed, promoted boundedly and source Draft closed unmerged.
- [x] #305 independently reviewed, promoted boundedly and source Draft closed unmerged.
- [x] #302 released static slice independently reviewed and promoted with classification edits; overall P0 objective stays RETURN_FOR_EVIDENCE.
- [x] next disjoint P2 serialization/transform hypothesis dispatched as Draft #306 and claimed by an independent researcher.
- [x] #300 shared-file scope audit performed; unrelated W7 catalogue drift removed; repaired integration generation exact-head CI passed.
- [x] current #295 review findings, stale #291 lifecycle ownership and related #292 implementation rechecked.
- [ ] active #303 and #306 results reconciled after independent researcher handoff.
- [ ] P2 actual transform/framing order, final binary egress and causal harness closed.
- [ ] P0 direct authoritative reads and P1 live authority/restart stability closed.
- [ ] A3/A4 action parity closed where required.
- [ ] semantic protocol/QMeta coverage and finite P0/P1 item-level denominators closed.
- [ ] #295/#291 ownership lifecycle either remediated by the owning lane or terminally superseded under explicit non-overlapping ownership with bounded unique content preserved.
- [ ] final programme audit/E2E classification/exact-head CI/PR hygiene/archive/ownership release complete.

# Stop / release rationale

No further coordinator mutation is safe at this checkpoint. #303 and #306 both have fresh independent researcher leases and must not share branch/worktree ownership with the coordinator. #302 waits on #303. #295 cannot be mutated because the merged #291 task remains `blocked` on `main` while claiming the same contract, and its four review findings remain unresolved. #292/#284 are outside Track A mutation authority. Repeated polling of active researcher CI/runtime would violate the anti-stall contract.

# Next action

Reacquire this coordinator after #303 or #306 releases a reviewable Draft handoff, or after the #295/#291 owner lifecycle is deliberately reconciled. First refetch exact `main`, #300 head/CI, relevant Draft head/task/CI/reviews and ownership. Promote only independently verified bounded evidence; otherwise preserve UNKNOWN/RETURN_FOR_EVIDENCE.
