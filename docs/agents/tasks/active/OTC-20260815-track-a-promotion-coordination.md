---
task_id: OTC-20260815-track-a-promotion-coordination
status: waiting
agent: unassigned
session_id: null
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
updated: 2026-08-15T17:24:00+02:00
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
last_progress_at: 2026-08-15T17:24:00+02:00
ci_checks_for_current_head: 2
ci_check_generation: p0-static-promotion
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
last_integration_head_before_release: ed3754ad7f87ce205586b3e26324d0c4b24873d0
last_integration_ci_run: 31892460506
last_integration_ci_state_at_release: in_progress
last_integration_ci_terminal_claimed: false
waiting_reason: active_runtime_research_plus_unassigned_independent_p2_dispatch_and_nonterminal_coordinator_ci
lease_released_at: 2026-08-15T17:24:00+02:00
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
- #305 bounded P2 intermediate-vtable/type correction; exact source snapshot promoted; source Draft closed unmerged; prior integration generation `0ade6404c5b43f5fe468b8dd748846406d4c856e` passed CI `31884644268`.
- #302 bounded static P0 slice from reviewed source head `6f838d1089968d216e506cd272e7b98680da9fc8`. Static run `31892019505` / job `95029600292` SUCCESS, artifact `9248797952` digest `sha256:04835ab0bac7ffc43e161e8b2118c90a3d2197f7011385a6758cd7706c93a584`, source exact-head CI `31892202128` SUCCESS, review threads 0. Promoted FACT: `playerPosition` literal `0x1cdde3f` (supersedes stale `0x1cddd3f`), distinct `playerPositionChanged` control context, relocation-backed provider/worldmap/TPlayerData anchors, exact `TPlayerData` vptr/typeinfo boundary. EDIT: `0x8367c1` is INFERENCE / structural byte-pattern xref lead until a real disassembler confirms the instruction boundary; `0x8367c2` is decoder overlap; nearby semantic ownership/accessor graph remains INFERENCE. Durable boundary: `docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/p0-player-position-static/PROMOTION_BOUNDARY.md`.

## ACTIVE / READY RESEARCH
- #302 overall objective is still `RETURN_FOR_EVIDENCE / WAITING_ON_RUNTIME`. Direct authoritative XYZ, member/accessor/encoding, direct-vs-render-copy discrimination, causal controls, repeated live observations and fresh PID/relogin stability remain UNKNOWN. Research lease is released.
- #303 RUNTIME remains actively and independently owned at last refresh; current task validates its workflow-quality gate before one canonical-HOME package-path/cwd discriminator. Restart/relogin semantic proof remains UNKNOWN.
- #306 P2 first-transform-boundary remains READY/unassigned with separate ownership. A fresh independent researcher must claim it; the coordinator must not become a serial researcher.

## RETURN_FOR_EVIDENCE
- #295 map-observation ownership correction remains not promotable: four unresolved material review threads, overlapping `MAP_OBSERVATION_V1.md` ownership, weakened raw-packet/authorization/protocol-version constraints, and stale source base.

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
- [ ] latest coordinator head exact-head CI terminal green; run `31892460506` on integration head `ed3754ad7f87ce205586b3e26324d0c4b24873d0` was still `in_progress` after both allowed observations, and this release checkpoint creates a newer docs-only head, so no terminal PASS is claimed for the latest head.
- [ ] active #303 and ready #306 results reconciled after independent researcher handoff.
- [ ] P2 actual transform/framing order, final binary egress and causal harness closed.
- [ ] P0 direct authoritative reads and P1 live authority/restart stability closed.
- [ ] A3/A4 action parity closed where required.
- [ ] semantic protocol/QMeta coverage and finite P0/P1 item-level denominators closed.
- [ ] #295 ownership/review conflict either remediated by its owner or terminally superseded with bounded unique content preserved.
- [ ] final programme audit/CI/PR hygiene/archive/ownership release complete.

# Stop / release rationale

The coordinator has no further non-overlapping review or promotion work at this checkpoint. #303 is actively owned by another researcher; #306 is a concrete independent READY task that requires a fresh researcher session; #302 is waiting on the RUNTIME prerequisite; #295 cannot be mutated under current ownership while its overlap/review defects remain. Two allowed observations of coordinator CI run `31892460506` remained nonterminal, so further polling is forbidden. No worker should stay active only to wait.

# Next action

A fresh independent P2 researcher should claim Draft #306 and execute its static exact-build transform-boundary task. Reacquire this coordinator only when #303 or #306 publishes a reviewable handoff (or on the next explicit coordinator invocation); first refetch exact `main`, latest #300 head/CI, and the released Draft head before assigning the next disposition.