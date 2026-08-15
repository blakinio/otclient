---
task_id: OTC-20260815-track-a-promotion-coordination
status: ready
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
updated: 2026-08-15T14:14:00+02:00
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
last_progress_at: 2026-08-15T14:14:00+02:00
ci_checks_for_current_head: 1
ci_check_generation: terminal
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 1
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 3
stall_warnings: 0
stop_reason: P2 writer-retention promotion is validated and source PR #301 is closed; P0/RUNTIME live lanes remain independently owned/blocked, while a disjoint static P2 vtable-group task #305 is READY and can be executed serially only after coordinator release
---

# Objective

Keep canonical Track A (`official-client-re`) true, reproducible and progressively complete. Research branches remain Draft-only; this task alone performs campaign promotion/integration. Track B remains outside mutation authority.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Promotion ledger

## ACCEPT
- #283 bounded read-only runtime bridge implementation; live authority/session epoch still unproven.
- exact-build reversible structural world transition from run `31806312967` / job `94785974126`; standalone player XYZ and A3/A4 remain unproven.

## ACCEPT_WITH_EDITS
- #279 fail-closed worldmap reconstruction tooling; real capture/mappings/complete OTBM remain UNKNOWN.
- #290 bounded historical login/recovery procedure retained as revalidation input.
- #304 bounded quantitative coverage baseline; exact source snapshot promoted; source Draft closed unmerged.
- #301 bounded P2 writer retention: `TProtocolClientMessageProcessor -> retained intermediate object -> retained shared TProtocolWriter` FACT; writer position relative to `TGameserverDualConnection` is graph-relative upstream INFERENCE; direct DualConnection writer member NOT_PROVEN. Exact source snapshot promoted under coordinator ownership. Coordinator head `e6aab7a1898643f3a139413048af709a0ee04cf7` passed CI `31883767739`; source Draft #301 closed unmerged.

## LIVE STATE
- #302 P0: old queued run `31880617510` is cancelled. Corrected self-hosted run `31883521701` / job `95009093099` executed on `synology-otclient-01` but found `TRACK_A_P0_MATCHING_LIVE_PIDS=0`; direct player position remains UNKNOWN, not disproven. Current P0 waits for a canonical live exact-client runtime window.
- #303 RUNTIME: separately active researcher session. New run `31883846172` at head `950ce8f5f7cf22b457e82cdb20e9eec285438d9c` exists; job `95010096196` (`reacquire`) is currently queued. No runtime semantic result yet.

## READY RESEARCH
- #305 P2 writer-vtable-group: new disjoint Draft task on `research/OTC-20260815-track-a-p2-writer-vtable-group`, exact base main. Goal is to classify `0x2f69e30 / RTTI 0x3080748` structurally inside the canonical `TProtocolWriter` vtable group and narrow the first transform/framing boundary. It explicitly does not duplicate queued final-socket run `31825417040`.

## RETURN_FOR_EVIDENCE
- #295 material review findings plus Track B ownership collision.

## REJECT/SUPERSEDE
- #289 broad stale continuation and superseded P2 model;
- #296 stale lifecycle Draft after accepted correction integration;
- #277 stale Oteryn-dependent handover;
- #280 superseded only as active Track A dependency; broader infrastructure remains separately owned/open.

# Canonical non-completion boundary

```yaml
P2: PARTIAL_writer_retention_proven_transform_order_final_egress_harness_open
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

# Next action

Coordinator ownership is released (`status: ready`). Claim #305 as an isolated Draft researcher and execute only the `0x2f69e30 / RTTI 0x3080748` vtable-group/transform-boundary discriminator using reviewed exact-build artifacts. Do not write #300 while #305 is active. In parallel, observe active #303 read-only; when it yields a reviewable runtime result, return to #300 and reconcile it before P0/ACTION follow-up.
