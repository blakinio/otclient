---
task_id: OTC-20260815-track-a-promotion-coordination
status: active
agent: ChatGPT
session_id: chatgpt-coordinator-20260815-1718
session_role: coordinator
session_rotation_count: 6
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
updated: 2026-08-15T17:22:00+02:00
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
invocation_started_at: 2026-08-15T17:07:00+02:00
last_progress_at: 2026-08-15T17:22:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: coordinator-rotation-6
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Objective

Keep canonical Track A (`official-client-re`) true, reproducible and progressively complete. Research branches remain Draft-only; this task alone promotes accepted evidence. Track B remains outside mutation authority.

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
- #290 bounded historical login/recovery procedure retained as revalidation input.
- #304 bounded quantitative coverage baseline; exact source snapshot promoted; source Draft closed unmerged.
- #301 bounded P2 writer retention; exact source snapshot promoted; source Draft closed unmerged.
- #305 bounded P2 intermediate-vtable/type correction; exact source snapshot promoted; source Draft closed unmerged; coordinator integration generation `0ade6404c5b43f5fe468b8dd748846406d4c856e` passed CI run `31884644268`.
- #302 **bounded static P0 slice only** from reviewed head `6f838d1089968d216e506cd272e7b98680da9fc8`: run `31892019505` / job `95029600292` SUCCESS on `synology-otclient-01`, artifact `9248797952` digest `sha256:04835ab0bac7ffc43e161e8b2118c90a3d2197f7011385a6758cd7706c93a584`, reviewed-head CI `31892202128` SUCCESS, review threads 0. Promoted facts are the exact `playerPosition` literal `0x1cdde3f`, distinct `playerPositionChanged` substring/control context, relocation-backed provider/worldmap/TPlayerData anchors, and existing exact `TPlayerData` vptr/typeinfo boundary. Classification edit: `0x8367c1` is only an `INFERENCE / STRUCTURAL_XREF_LEAD` because the custom decoder is byte-wise and full GDB disassembly failed; `0x8367c2` is decoder overlap. The nearby semantic ownership/accessor graph remains INFERENCE. Durable boundary: `docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/p0-player-position-static/PROMOTION_BOUNDARY.md`.

## ACTIVE / READY RESEARCH
- #302 overall objective remains `RETURN_FOR_EVIDENCE / WAITING_ON_RUNTIME`; direct authoritative XYZ, backing member/accessor/encoding, causal controls, repeatability and restart stability remain UNKNOWN. Research lease is released.
- #303 RUNTIME remains independently owned while active; coordinator must not mutate its paths.
- #306 P2 first-transform-boundary remains a separate Draft-only task; coordinator must not become its researcher.

## RETURN_FOR_EVIDENCE
- #295 map-observation ownership correction remains not promotable due four unresolved material review threads, overlapping ownership and stale source base.

## RELATED NON-TRACK-A IMPLEMENTATION
- #292 remains open Draft OTClient `Map`/`Tile` observation recorder and is not official-client Track A runtime authority.

## REJECT/SUPERSEDE
- #289 broad stale continuation and superseded P2 model;
- #296 stale lifecycle Draft after accepted correction integration;
- #277 stale Oteryn-dependent handover;
- #280 superseded only as active Track A dependency; broader infrastructure remains separately owned/open.

# Canonical non-completion boundary

```yaml
P2: PARTIAL_writer_retention_and_intermediate_type_structure_proven_transform_order_final_egress_harness_open
P1: PARTIAL_read_only_bridge_integrated_live_authority_unknown
P0: PARTIAL_static_playerPosition_anchor_plus_structural_world_transition_direct_authoritative_player_state_unknown
RUNTIME: PARTIAL_one_generation_world_evidence_restart_relogin_unknown
ACTION: A3_A4_NOT_PROVEN
COMPLETE: false
```

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

# Acceptance inventory
- [x] #304 independently reviewed, promoted boundedly and source Draft closed unmerged.
- [x] #301 independently reviewed, promoted boundedly and source Draft closed unmerged.
- [x] #305 independently reviewed, promoted boundedly and source Draft closed unmerged.
- [x] #302 released static slice independently reviewed and promoted with classification edits; overall P0 objective stays RETURN_FOR_EVIDENCE.
- [x] next disjoint P2 serialization/transform hypothesis dispatched as Draft #306.
- [x] current #295 overlap/review findings and related #292 implementation rechecked.
- [ ] active #303 and ready/active #306 results reconciled after independent researcher handoff.
- [ ] P2 actual transform/framing order, final binary egress and causal harness closed.
- [ ] P0 direct authoritative reads and P1 live authority/restart stability closed.
- [ ] A3/A4 action parity closed where required.
- [ ] semantic protocol/QMeta coverage and finite P0/P1 item-level denominators closed.
- [ ] #295 ownership/review conflict either remediated by its owner or terminally superseded with bounded unique content preserved.
- [ ] final programme audit/CI/PR hygiene/archive/ownership release complete.

# Next action

Refresh #303 and #306 exactly once. If either has released a reviewable result, review it immediately under the coordinator contract; otherwise checkpoint `waiting` and release this coordinator lease without polling.