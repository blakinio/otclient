---
task_id: OTC-20260816-track-a-worldmap-extent-static-re
status: waiting
agent: ChatGPT
session_id: chatgpt-worldmap-static-unblock-20260816
session_role: static_re_researcher
project_lane: otclient
lane: STATIC-RE
track_id: official-client-re
task_kind: discovery
phase: investigate
implementation_authorized: false
branch: research/OTC-20260816-track-a-worldmap-extent-static-re
base_branch: main
base_main: dbd9520e2f8cc5a26f556bffaae2a83e139615f9
live_main_observed: 845adabba5f6d2bfecb6d54bc13834c47cc61c94
consumer_head_before_resume: bc0ac9b966ee7ac0d91bbeef519756d78b18fbc1
pr: 367
risk: medium
updated: 2026-08-16T23:28:52+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-worldmap-extent-static-re.md
  - .github/scripts/tibia-official-client-re-worldmap-extent-static.py
  - docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/**
  - docs/agents/reports/OTCLIENT-20260816-worldmap-extent-static-re.md
modules_touched: []
reuses:
  - docs/agents/reports/OTCLIENT-20260816-official-client-map-viewport-feasibility.md
  - PR #365 merged feasibility checkpoint
  - run 31821458677 artifact 9227370490 retained historical runtime geometry evidence
  - run 31804083206 job 94778661881 exact fenced handler disassembly log
  - complete retained artifact inventory evidence 20260816-complete-retained-artifact-inventory.md
  - PR #437 / OTC-20260816-track-a-worldmap-exact-static-evidence as NEW bounded sanitized exact-client producer
  - PR #437 source artifact 9270235755 and hosted final artifact 9270276361
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: consume newly available sanitized exact-client producer evidence and continue bounded static dependency recovery without live runtime access
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_pressure: high
context_growth: stable
context_score: 10
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: one cohesive graph spans extent ownership, protocol/storage updates and render/camera/picker consumers; continue the same task/PR
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
runtime_access: none
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: false
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
owner_funded_ai_api_authorized: false
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runtime_platform: official_native_linux_only
invocation_started_at: 2026-08-16T23:28:52+02:00
last_progress_at: 2026-08-16T23:28:52+02:00
ci_checks_for_current_head: 0
ci_check_generation: exact-static-unblock-consumption
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
heavy_validation_runs: 0
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
new_exact_static_producer:
  task: OTC-20260816-track-a-worldmap-exact-static-evidence
  pr: 437
  head: ce8b1f59d02bfc7ecc498dd80f73b09cf2970510
  WORLD_MAP_STATIC_EVIDENCE_READY: true
  source_run: 31972743782
  source_job: 95227595548
  source_artifact: 9270235755
  source_artifact_sha256: 039d22fe5f88a07784c4ddc32cf6b1d9c2d07a34e90ed5902ffd21d3acd5735b
  hosted_run: 31972915689
  hosted_job: 95228024727
  hosted_artifact: 9270276361
  hosted_artifact_sha256: 0dc8d0a44e5a2550ef79c219bda14787796ef7accc0ab1627fecd7c6d55330bc
  independent_zip_digest_match: PASS
  hosted_validation: PASS
  raw_client_uploaded: false
  client_executed: false
  client_bytes_mutated: false
original_static_blocker:
  kind: EXACT_STATIC_BYTES_NOT_DURABLY_STAGED
  status: RESOLVED_BY_PR_437
  repeated_retained_inventory_scan: false
  repeated_failed_cdn_fetch: false
identity_results:
  protocol_handler:
    window: 0x030871c8..0x030871d7
    vptr: 0x030871d8
    bytes: 0000000000000000b85f080300000000
    typeinfo: 0x03085fb8
    rtti: tibia::worldmap::TWorldmapProtocolMessageHandler
    classification: PROVEN
  historical_geometry_object:
    window: 0x0308ce60..0x0308ce6f
    vptr: 0x0308ce70
    bytes: 0000000000000000f0b5080300000000
    typeinfo: 0x0308b5f0
    rtti: tibia::worldmap::TWorldMapStorage
    classification: PROVEN
  historical_geometry_control:
    window: 0x02f683c0..0x02f683cf
    vptr: 0x02f683d0
    bytes: 000000000000000020fb070300000000
    typeinfo: 0x0307fb20
    rtti: std::_Sp_counted_ptr_inplace<tibia::worldmap::TWorldMapStorage,...>
    classification: PROVEN
superseded_inference:
  old_claim: historical 18x14 object/control block strongly correlated with TWorldMapViewport
  corrected_to: exact TWorldMapStorage object plus counted TWorldMapStorage control block
  status: SUPERSEDED_BY_DIRECT_RTTI
storage_geometry:
  constructor: 0x00cbf37a
  embedded_extent_vptr: 0x02f61578
  embedded_extent_typeinfo: 0x0306fc60
  requested_offsets_initialized: [+0x18, +0x1c, +0x30, +0x34, +0x48, +0x4c]
  slot_12_mutator: 0x00cc6cd0
  priority_pair_writer: 0x00cc6d2c
  priority_pair_source: rsi+0x38 QWORD
  requested_offsets_mutated: [+0x18, +0x1c, +0x30, +0x34, +0x48, +0x4c]
  slot_14_bounds_reader: 0x00cb01d0
  lower_xyz: [+0x18, +0x1c, +0x20]
  upper_xyz: [+0x30, +0x34, +0x38]
  bounds_semantics: half_open_lower_inclusive_upper_exclusive
  slot_13_extent_snapshot: 0x00cb0180
  extent_driven_oob_eviction: PROVEN
  tree_state_offsets: [+0x68, +0x70, +0x78]
  live_collection_count_offset: +0x88
  maximum_capacity: UNKNOWN
  upstream_dynamic_origin_of_18_14: UNKNOWN
viewport_recovery:
  exact_vptr: 0x0308c9a8
  typeinfo: 0x0308b590
  constructor: 0x00cbf680
  adjacent_geometry_update: 0x00cbf700
  own_embedded_extent_vptr: 0x02f61578
  constructor_constant_at_0x48: 8
  constructor_constant_at_0x60: 4
  signed_shift_by_5_in_geometry_update: PROVEN
  direct_storage_to_viewport_ownership_edge: UNKNOWN
downstream_recovery:
  render_provider:
    vptr: 0x02f6c258
    first_staged_slot: 0x00820970
    staged_semantics: destructor_cleanup_only_for_current_question
    clipping_culling_iteration_constraints: UNKNOWN_NEEDS_NON_DESTRUCTOR_WINDOWS
  camera:
    vptr: 0x03083968
    first_staged_slot: 0x00dedda0
    staged_semantics: trivial_metaobject_like_only_for_current_question
    projection_scale_constraints: UNKNOWN_NEEDS_NON_META_WINDOWS
  picker:
    vptr: 0x02f6b7c8
    first_staged_slot: 0x008205c0
    staged_semantics: destructor_ownership_cleanup_only_for_current_question
    screen_world_transform_constraints: UNKNOWN_NEEDS_NON_DESTRUCTOR_WINDOWS
static_classification: MORE_STATIC_RE_NEEDED
static_patch_graph_ready: false
remaining_static_blocker:
  status: WAITING_FOR_NEW_BOUNDED_EVIDENCE
  kind: DOWNSTREAM_EXACT_WORLD_MAP_CONSUMER_WINDOWS_NOT_DURABLY_STAGED
  effect: render/camera/picker dependency constraints and final safe mutation graph remain incomplete
  evidence: docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260816-new-exact-static-unblock-and-downstream-recovery.md
next_action: obtain a NEW bounded exact-client producer bundle for the caller/upstream producer of TWorldMapStorage slot 12 input rsi+0x38 and non-destructor/non-meta TWorldMapRenderProvider, TWorldMapCamera and TWorldMapPicker consumer windows; then resume this same task/PR to finish clipping/culling/projection/picking and fixed-allocation/mask/packing audits before any mutation design
---

# Track A worldmap extent static RE

## Current result

The original `BLOCKED_EXACT_STATIC_BYTES_NOT_DURABLY_STAGED` condition is resolved by the new bounded sanitized exact-client producer in Draft PR #437. All three requested identity windows and direct mutation coverage for all six requested geometry DWORDs are now durable and independently digest-checked.

The most important correction is exact: the historical object containing retained `18/14` at `+0x48/+0x4c` is `TWorldMapStorage`, and its adjacent counted block is the counted Storage wrapper. The previous Viewport correlation for that object is superseded.

Storage recovery now proves half-open 3D lower/upper bounds, dynamic geometry replacement, extent-driven out-of-bounds node removal, a live collection-count relation, and extent-aware coordinate-indexed traversal. A distinct exact `TWorldMapViewport` constructor and geometry update were also recovered from the new bounded bytes.

The task is not complete. The producer bundle does not stage enough non-destructor/non-meta `TWorldMapRenderProvider`, `TWorldMapCamera`, or `TWorldMapPicker` code to prove the final clipping/culling/projection/picking constraints. `STATIC_PATCH_GRAPH_READY=false`; no client-byte mutation or patch design is authorized.

Durable continuation evidence:

`docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260816-new-exact-static-unblock-and-downstream-recovery.md`
