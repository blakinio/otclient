---
task_id: OTC-20260815-track-a-promotion-coordination
status: active
agent: ChatGPT
session_id: chatgpt-coordinator-20260815-1745
session_role: coordinator
session_rotation_count: 8
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
updated: 2026-08-15T17:48:00+02:00
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
invocation_started_at: 2026-08-15T17:45:00+02:00
last_progress_at: 2026-08-15T17:48:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: p2-serialization-promotion
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
active_operation:
  type: dispatch_next_p2_post_serialization_boundary
last_promotion:
  source_pr: 306
  disposition: ACCEPT_WITH_EDITS
  source_head: c13e6d8946d1407c880a07d76fcfd5f4bf07c80b
  source_final_static_run: 31893391887
  source_final_ci_run: 31893395016
  source_final_artifact: 9249137864
  source_final_artifact_digest: sha256:c80014c2cc9b3db5b3406540e7d6d4efeef0301f63fd5858379614179b59398d
  semantic_result: SERIALIZATION_ONLY_PROVEN
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
- #304 bounded quantitative coverage baseline; exact source snapshot promoted; source Draft closed unmerged.
- #301 bounded P2 writer-retention evidence; exact source snapshot promoted; source Draft closed unmerged.
- #305 bounded P2 intermediate-vtable/type correction; exact source snapshot promoted; source Draft closed unmerged.
- #302 bounded static P0 slice; direct authoritative XYZ remains UNKNOWN.
- **#306 bounded first concrete retained-writer serialization evidence.** Exact source final static run `31893391887` SUCCESS; final source CI `31893395016` SUCCESS; review threads 0; final artifact `9249137864`, digest `sha256:c80014c2cc9b3db5b3406540e7d6d4efeef0301f63fd5858379614179b59398d`. Promoted FACT: processor retains distinct intermediate AP `0x2f69e30` / RTTI `0x3080748`; intermediate retains TProtocolWriter AP `0x2f69dd0` / RTTI `0x3080728`; first two intermediate slots are lifecycle-like; slot `+0x10 -> 0xc10960` accesses retained writer at `+0x18` and invokes `QDataStream::operator<<(signed char)` on a message-derived value; slot `+0x18 -> 0xc20290` serializes structured fields `+0x30/+0x34` through `QDataStream::operator<<(signed short)`; adjacent `+0x20 -> 0xc20c70` constructs QBuffer. Coordinator EDIT: "first" means the first concrete non-lifecycle slot directly demonstrated in this intermediate vtable, **not** the temporally first transform in the complete outbound pipeline. Durable boundary: `docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/p2-first-serialization-boundary/PROMOTION_BOUNDARY.md`.

## ACTIVE / WAITING RESEARCH
- #302 P0 remains `RETURN_FOR_EVIDENCE / WAITING_ON_RUNTIME` for direct authoritative XYZ and causal live controls.
- #303 RUNTIME remains independently owned; do not mutate its branch/runtime. Restart/relogin semantic proof remains UNKNOWN.

## RETURN_FOR_EVIDENCE
- #295 remains blocked by four material review threads plus overlapping/stale Track B ownership lifecycle.

# Canonical non-completion boundary

```yaml
P2: PARTIAL_writer_retention_intermediate_type_and_qdatastream_serialization_proven_pipeline_order_final_egress_harness_open
P1: PARTIAL_read_only_bridge_integrated_live_authority_unknown
P0: PARTIAL_static_playerPosition_anchor_plus_structural_world_transition_direct_authoritative_player_state_unknown
RUNTIME: PARTIAL_historical_single_generation_world_evidence_restart_relogin_unknown
ACTION: A3_A4_NOT_PROVEN
COMPLETE: false
```

# P2 promoted representation boundary

```text
structured/typed object argument
  -> retained TProtocolWriter-associated QDataStream serialization sink
```

Explicitly still `UNKNOWN`:

- temporal first operation in complete outbound pipeline;
- QBuffer temporal/data-flow relation to proven serializers;
- framing order;
- sequence-number order;
- compression boundary/order;
- encryption boundary/order;
- final binary egress/socket ownership for this retained branch;
- causal local harness.

Direct DualConnection writer ownership remains `NOT_PROVEN`.

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

# Coordinator integration validation retained

- main reverified at `8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`.
- integration head `6fd1df4f1687e4ca0c1196caad4d4d1d1916079f` passed CI `31892866367`.
- unrelated W7/OTClient-v2 catalogue drift was removed from coordinator scope.
- repaired integration head `da96c97b91c236be6f97e4edf80214f77b4b2492` passed exact-head CI `31893397505`.
- source #306 final handoff gates were independently verified before promotion.

# Acceptance inventory

- [x] #304 independently reviewed/promoted boundedly.
- [x] #301 independently reviewed/promoted boundedly.
- [x] #305 independently reviewed/promoted boundedly.
- [x] #302 bounded static slice independently reviewed/promoted; overall P0 stays open.
- [x] #306 independently reviewed and promoted `ACCEPT_WITH_EDITS` with global temporal-order correction.
- [ ] close #306 source Draft unmerged after promotion bookkeeping.
- [ ] dispatch next disjoint P2 post-serialization buffer/data-flow/framing hypothesis to a fresh Draft; coordinator must not research it serially.
- [ ] exact-head coordinator CI terminal green after #306 promotion/dispatch bookkeeping.
- [ ] reconcile #303 after independent researcher handoff.
- [ ] P2 pipeline order/final egress/causal harness closeout.
- [ ] P0 direct authoritative reads and P1 live authority/restart stability.
- [ ] A3/A4 action parity.
- [ ] semantic protocol/QMeta coverage and finite P0/P1 denominators.
- [ ] #295/#291 ownership lifecycle terminal reconciliation.
- [ ] final programme audit/E2E/exact-head CI/PR hygiene/archive/ownership release.

# Next action

Close source #306 unmerged, dispatch a fresh independent P2 task that traces exact data flow from the proven QDataStream serialization state toward the adjacent QBuffer/byte-container boundary without inferring order from vtable adjacency, then validate the coordinator exact head. Preserve framing/sequence/compression/encryption/final egress/harness as UNKNOWN until directly discriminated.
