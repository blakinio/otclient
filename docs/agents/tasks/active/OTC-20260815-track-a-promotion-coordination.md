---
task_id: OTC-20260815-track-a-promotion-coordination
status: active
agent: ChatGPT
session_id: chatgpt-track-a-coordinator-20260815-2106
session_role: coordinator
session_rotation_count: 9
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
updated: 2026-08-15T21:18:00+02:00
lease_expires_at: 2026-08-15T21:57:00+02:00
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
invocation_started_at: 2026-08-15T21:06:00+02:00
last_progress_at: 2026-08-15T21:18:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: coordinator-rotation-9-loader-promotion
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
stop_reason: null
last_verified_integration_head: ce933e8fe28ea61669da28ffcc10cf21675a62b0
last_verified_integration_ci_run: 31893876568
last_verified_integration_ci_state: success
pending_integration_head: 2d5edaa546d8a88c78a60f86f4ceb150c98e2412
pending_integration_ci_run: not_checked_yet
last_promotion:
  source_pr: 307
  disposition: ACCEPT_WITH_EDITS
  source_head: 229d4bdb4051ab707f436f3c1e1602712e76ecb5
  source_exact_head_ci_run: 31894342104
  source_exact_head_ci_state: success
  semantic_result: CURRENT_LOADER_AND_QXCB_DEPENDENCIES_RESOLVE_CACHE_METADATA_ONLY_CANDIDATE
  canonical_evidence: docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/runtime-loader-diagnostic/20260815-pr307-disposition.md
active_operation:
  - terminate source PR 307 unmerged after bounded promotion
  - review PR 308 released semantic artifact without mutating its waiting researcher branch
  - reconcile stale PR 303 ownership before any RUNTIME mutation
next_action: close source Draft PR 307 unmerged after promotion, then independently classify PR 308 artifact and perform stale-takeover preflight for PR 303; do not read/copy canonical cache payloads
---

# Objective

Keep canonical Track A (`official-client-re`) true, reproducible and progressively complete. Researchers remain Draft-only. This coordinator is the promotion/integration authority subject to repository governance. Track B remains outside mutation authority.

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
- #279 fail-closed worldmap reconstruction tooling; real capture/mappings/complete OTBM remain UNKNOWN.
- #290 historical login/recovery procedure retained only as revalidation input.
- #304 quantitative coverage baseline; source Draft closed unmerged.
- #301 retained TProtocolWriter branch; source Draft closed unmerged.
- #305 intermediate-vtable/type correction; source Draft closed unmerged.
- #302 bounded static P0 facts only; direct authoritative XYZ remains UNKNOWN.
- #306 retained intermediate -> TProtocolWriter QDataStream serialization evidence; source Draft closed unmerged. `0xc10960` and `0xc20290` prove serialization on the retained writer branch; adjacent `0xc20c70` constructs QBuffer, but relation/order remains UNKNOWN.
- #307 exact-client loader/platform diagnostic. Source head `229d4bdb4051ab707f436f3c1e1602712e76ecb5`; exact-head CI `31894342104` SUCCESS; review submissions/threads zero. Independently promoted facts: current bundled-Qt/libproxy/toolroot loader resolves `RC=0`; literal historical `$runtime/lib:$tool_lib` replay fails on today's toolroot and is rejected as a fix; `libqxcb.so` and `libqxcb-glx-integration.so` are present and both dependency chains resolve `RC=0`. `.cache/CipSoft GmbH` metadata (4 files / 6937 B) is retained only as an `UNKNOWN` support-state candidate; contents/sensitivity/causality remain unknown and copying/reading payloads is not authorized by this promotion. Canonical disposition: `docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/runtime-loader-diagnostic/20260815-pr307-disposition.md`.

# Rotation 9 live reconciliation

- `main` remains `8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45` at the invocation preflight.
- Prior coordinator CI run `31893876568` on `ce933e8fe28ea61669da28ffcc10cf21675a62b0` is terminal `SUCCESS`; that head is the last verified integration generation. Current coordinator head has advanced due to rotation-9 checkpoint/promotion and therefore still needs later exact-head CI after the coherent batch.
- #307 is coordinator-reviewed `ACCEPT_WITH_EDITS` as above. Its next useful RUNTIME consumer is sanitized `QT_DEBUG_PLUGINS=1` plus mapped/unmapped X11 window and extension inventory; no cache payload read/copy.
- #308 code-bearing semantic run `31903141897` on `5d7f4bb1aadc782f9bc69b1e292577d88fe0c4a2` is now terminal `SUCCESS`; code-bearing CI `31903144036` is also SUCCESS; artifact `9251635451` digest `sha256:118810016d53f5bc234f6216b1d2f45876422041d7539b32a942a285317c6c32` is available for coordinator review. Source task is still `waiting/unassigned` at docs-only head `4eba544e712b58d3aa52b1044f7f853a3c1af4f9`, so coordinator must not pretend the worker Draft handoff gate is complete or mutate its branch.
- #303 run `31893122418` reproduced historical patched-Xvfb cwd on task-owned `:115` but still failed before login with `client_gen_1_window_missing`; cleanup passed. This disproves Xvfb cwd as the missing isolated cause. The #303 task record still carries an old active lease and must not be mutated until stale-takeover rules are satisfied.
- #302 remains waiting on a bounded live exact-client in-game observation window; direct player XYZ remains `UNKNOWN/INCONCLUSIVE`.

# Canonical non-completion boundary

```yaml
P2: PARTIAL_writer_retention_intermediate_type_and_qdatastream_serialization_proven_pipeline_order_final_egress_harness_open
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

- finish P2 QDataStream -> buffer/framing/pipeline-order/final-egress/harness evidence;
- recover live RUNTIME restart/relogin and provide a bounded P0/P1 observation window;
- prove direct P0 reads and live P1 authority/restart stability;
- prove A3/A4 action parity where required;
- close semantic protocol/QMeta coverage and finite P0/P1 denominators;
- reconcile #295/#291 ownership lifecycle without Track B contamination;
- perform final programme audit/E2E/exact-head CI/PR hygiene/archive/ownership release.
