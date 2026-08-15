---
task_id: OTC-20260815-track-a-promotion-coordination
status: active
agent: ChatGPT
session_id: chatgpt-coordinator-20260815-1708
session_role: coordinator
session_rotation_count: 5
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
updated: 2026-08-15T17:08:00+02:00
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
last_progress_at: 2026-08-15T17:08:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: coordinator-rotation-5
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
- #301 bounded P2 writer retention; exact source snapshot promoted; source Draft closed unmerged; coordinator CI `31883767739` SUCCESS.
- #305 bounded P2 intermediate-vtable/type correction. Exact source final head `9329e338235b7f9997d74d4db5313f329662378b`; final task-specific run `31884379539` SUCCESS; final PR CI `31884381191` including `CI / Required` SUCCESS; review threads 0. Exact source blobs copied under coordinator-owned `p2-writer-vtable-group/source-snapshot/` in commit `a5ba8557e54b2d5345b48b816167a5b8131d2084`; campaign report updated in `8dacacba5d13c39e490108e6cedb0fcebdc2dd52` and coordinator integration checkpoint `0ade6404c5b43f5fe468b8dd748846406d4c856e` passed CI run `31884644268`.

Accepted #305 boundary:
```yaml
intermediate_vptr_0x2f69e30: FACT
intermediate_typeinfo_0x3080748: FACT
separate_allocated_object_receives_vptr: FACT
simple_secondary_TProtocolWriter_interpretation: DISPROVEN
0x7de7f0_0x7dfd60_role: INFERENCE_TEARDOWN_LIKE
rtti_0x3080748_semantic_name: UNKNOWN
rtti_0x3080748_base_relation: UNKNOWN
first_writer_transform_boundary: UNKNOWN
framing_order: UNKNOWN
final_binary_egress: UNKNOWN
P2_complete: false
```

## LIVE STATE
- #302 P0: independently active rotation on Draft head `9060e83036c6a50a59f055c5248b4071aa47b946`. Exact-ELF static work recovered `TPlayerData` / `playerPosition` / `IPlayerDataProvider` structural leads while direct authoritative XYZ remains UNKNOWN. Runtime ownership remains with #303; coordinator must not mutate #302 while active.
- #303 RUNTIME: independently active rotation on Draft head `5b7a9707e5b1594f5cc62fb0a1ad67f7556226eb`. Prior exact-client launch prerequisites, loader, bundled Qt, software renderer, X11/HOME and Xvfb hypotheses are bounded; latest durable checkpoint requires lint repair before one canonical-HOME-package-path/cwd discriminator. Restart/relogin stability remains UNKNOWN. Coordinator must not mutate #303 while active.

## RETURN_FOR_EVIDENCE
- #295 material review findings plus Track B ownership collision.

## REJECT/SUPERSEDE
- #289 broad stale continuation and superseded P2 model;
- #296 stale lifecycle Draft after accepted correction integration;
- #277 stale Oteryn-dependent handover;
- #280 superseded only as active Track A dependency; broader infrastructure remains separately owned/open.

# Canonical non-completion boundary

```yaml
P2: PARTIAL_writer_retention_and_intermediate_type_structure_proven_transform_order_final_egress_harness_open
P1: PARTIAL_read_only_bridge_integrated_live_authority_unknown
P0: PARTIAL_structural_world_transition_fact_direct_player_state_unknown
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
- [x] #304 independently reviewed, accepted with edits, promoted as a bounded source snapshot and source Draft closed unmerged.
- [x] #301 independently reviewed, accepted with edits, promoted as a bounded source snapshot and source Draft closed unmerged.
- [x] #305 independently reviewed and assigned `ACCEPT_WITH_EDITS`.
- [x] exact #305 evidence/result/reproducer/workflow blobs promoted under coordinator ownership.
- [x] campaign report updated with FACT/INFERENCE/DISPROVEN/UNKNOWN boundaries.
- [x] coordinator integration head `0ade6404c5b43f5fe468b8dd748846406d4c856e` passed CI run `31884644268` before this rotation checkpoint.
- [x] #305 source Draft closed unmerged after validated promotion.
- [ ] active #302 and #303 results reconciled when their current researchers release ownership.
- [ ] next disjoint P2 serialization/transform hypothesis dispatched without duplicating queued final-socket run `31825417040`.
- [ ] P2 actual transform/framing order, final binary egress and causal harness closed.
- [ ] P0 direct authoritative reads and P1 live authority/restart stability closed.
- [ ] A3/A4 action parity closed where required.
- [ ] semantic protocol/QMeta coverage and finite P0/P1 item-level denominators closed.
- [ ] final programme audit/CI/PR hygiene/archive/ownership release complete.

# Next action

Create one disjoint Draft-only P2 dispatch from exact `main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45` for the first concrete serialization/transform boundary on the accepted `TProtocolClientMessageProcessor -> retained writer` branch. It must consume coordinator PR #300 accepted P2 evidence only as a pinned unmerged dependency, avoid final-socket run `31825417040`, generic QIODevice enumeration, vtable adjacency and superseded sink models, and use unique task/evidence/workflow/script ownership.