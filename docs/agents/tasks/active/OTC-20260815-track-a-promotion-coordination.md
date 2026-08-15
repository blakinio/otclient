---
task_id: OTC-20260815-track-a-promotion-coordination
status: active
agent: ChatGPT
session_id: chatgpt-track-a-coordinator-20260815-2133
session_role: coordinator
session_rotation_count: 11
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
updated: 2026-08-15T21:36:00+02:00
lease_expires_at: 2026-08-15T22:21:00+02:00
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
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
invocation_started_at: 2026-08-15T21:33:00+02:00
last_progress_at: 2026-08-15T21:36:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: coordinator-rotation-11-post-p2-promotion
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
stop_reason: null
last_verified_integration_head: ce933e8fe28ea61669da28ffcc10cf21675a62b0
last_verified_integration_ci_run: 31893876568
last_verified_integration_ci_state: success
last_promotion:
  source_pr: 308
  disposition: ACCEPT_WITH_EDITS
  source_final_head: 7153ba4f0799a2c6b81eeeb62e4b1320e386c924
  source_code_bearing_head: 34f73b0c48198ba452caa505b4c0f3ae7e5b61d7
  semantic_run: 31903490468
  semantic_state: success
  source_release_head_ci_run: 31903882606
  source_release_head_ci_state: success
  canonical_evidence: docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/p2-buffer-boundary/20260815-pr308-disposition.md
active_operation:
  - close source PR 308 unmerged after bounded promotion
  - select next safe READY P2 or RUNTIME programme lane based on live ownership
  - preserve P0/P1/ACTION/COVERAGE UNKNOWN boundaries until separately proven
next_action: close PR 308 unmerged; inspect current open Draft/task ownership and continue next non-overlapping high-information Track A lane
---

# Objective

Keep canonical Track A (`official-client-re`) true, reproducible and progressively complete. Researchers remain Draft-only. Coordinator owns promotion/integration. Track B remains outside mutation authority.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Promoted bounded state

## ACCEPT
- #283 bounded read-only runtime bridge; live authority/session epoch remains UNKNOWN.
- exact-build reversible structural world transition from run `31806312967` / job `94785974126`; standalone player XYZ and A3/A4 remain unproven.

## ACCEPT_WITH_EDITS
- #279 fail-closed worldmap reconstruction tooling; real capture coverage/mappings/complete OTBM remain UNKNOWN.
- #290 historical login/recovery procedure retained only as revalidation input.
- #304 quantitative coverage baseline; source Draft closed unmerged.
- #301 retained TProtocolWriter branch; source Draft closed unmerged.
- #305 intermediate-vtable/type correction; source Draft closed unmerged.
- #302 bounded static P0 facts only; direct authoritative XYZ remains UNKNOWN.
- #306 retained intermediate -> TProtocolWriter QDataStream serialization; `0xc10960` and `0xc20290` prove serialization on the retained writer branch; global temporal order remained UNKNOWN.
- #307 loader/platform negative diagnostics: current exact-client bundled Qt/libproxy/toolroot dependencies and qxcb/GLX plugin chains resolve; canonical cache remains metadata-only UNKNOWN; source Draft closed unmerged.
- #308 post-serialization byte-container boundary: hardened exact-build proof establishes a persistent QBuffer-backed QIODevice bound into helper `0x1960340`, retained through `TProtocolWriter+0x18/+0x20`, the retained intermediate, and `TProtocolClientMessageProcessor`; retained QDataStream serialization therefore writes into a QBuffer-backed byte container. Local object lifecycle order (binding constructed before serializer use) is proven. Global protocol-stage order, framing, sequence, compression, encryption, final binary egress and causal local harness remain UNKNOWN. Canonical disposition: `docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/p2-buffer-boundary/20260815-pr308-disposition.md`.

# RUNTIME/P0 boundary

- #303 cache metadata classifier identifies 3 `.qsb` shader-class files plus one 80-byte gpu/cache-class file, 6937 B total, metadata only in the accepted classifier. Cache-seed run `31903627907` is `INCONCLUSIVE_HARNESS_FAILURE`: it reached exact client running but exited `127` before any all/visible window counts. Cache causality remains UNKNOWN; further persistent-cache payload seeding is returned for evidence. Coordinator comment `5303842133` requires no-payload mapped/unmapped X11 + Qt diagnostics.
- #302 remains waiting for a bounded live exact-client in-game observation window. Direct authoritative player XYZ remains `UNKNOWN/INCONCLUSIVE`.

# Map-observation ownership boundary

- #295 remains `RETURN_FOR_EVIDENCE / OWNERSHIP_LIFECYCLE_BLOCKED`; merged #291 left `docs/agents/tasks/active/OTC-20260813-map-observation-export.md` active/blocked on main while still owning `MAP_OBSERVATION_V1.md`, overlapping the #295 correction task. Four material review threads remain unresolved. Do not mutate the contract until lifecycle authority is repaired.

# Canonical non-completion boundary after #308 promotion

```yaml
P2: PARTIAL_retained_qdatastream_to_persistent_qbuffer_backed_byte_container_proven_protocol_stage_order_framing_final_egress_harness_open
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

# Remaining programme gates

- continue P2 from the promoted persistent QBuffer-backed byte container to the first exact downstream consumer/transform toward framing/final egress; then prove ordering/harness where possible;
- recover live RUNTIME restart/relogin and provide a bounded P0/P1 observation window;
- prove direct P0 reads and live P1 authority/restart stability;
- prove A3/A4 action parity where required;
- close semantic protocol/QMeta coverage and finite P0/P1 denominators;
- repair #295/#291 ownership lifecycle before map-observation contract mutation;
- perform final programme audit/E2E/exact-head CI/PR hygiene/archive/ownership release.
