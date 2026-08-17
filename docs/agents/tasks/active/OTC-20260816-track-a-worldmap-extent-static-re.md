---
task_id: OTC-20260816-track-a-worldmap-extent-static-re
status: completed
agent: ChatGPT
session_id: chatgpt-worldmap-static-unblock-20260816
session_role: static_re_researcher
project_lane: otclient
lane: STATIC-RE
track_id: official-client-re
task_kind: discovery
phase: static_dependency_graph_complete
implementation_authorized: false
branch: research/OTC-20260816-track-a-worldmap-extent-static-re
base_branch: main
base_main: dbd9520e2f8cc5a26f556bffaae2a83e139615f9
live_main_observed: 8c9486e2c6109a7a39b564804c8acd707659b5e0
consumer_head_before_final_consumption: a69179e5cf4681a9d41014a562a0bfd0d1cd9ffb
pr: 367
risk: medium
updated: 2026-08-17T09:02:00+02:00
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
  - PR #437 / OTC-20260816-track-a-worldmap-exact-static-evidence exact identity/writer producer
  - PR #446 / OTC-20260817-track-a-worldmap-downstream-exact-static-evidence downstream exact dependency producer
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: consume governance-bounded sanitized exact-client evidence and finish the static dependency graph without live runtime access or client-byte mutation
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_pressure: high
context_growth: stable
context_score: 10
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: one cohesive graph spans extent ownership, protocol/storage updates and render/camera/picker consumers
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
last_progress_at: 2026-08-17T09:02:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: final-static-graph
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
producer_437:
  pr: 437
  head: ce8b1f59d02bfc7ecc498dd80f73b09cf2970510
  WORLD_MAP_STATIC_EVIDENCE_READY: true
  source_run: 31972743782
  source_job: 95227595548
  source_artifact: 9270235755
  hosted_run: 31972915689
  hosted_job: 95228024727
  hosted_artifact: 9270276361
producer_446:
  pr: 446
  head: f7f16af614a88100cc82ff7ecf0b112cb2e0605c
  WORLD_MAP_DOWNSTREAM_STATIC_EVIDENCE_READY: true
  governance_run: 32003664983
  governance_result: SUCCESS
  repository_ci_run: 32003665239
  repository_ci_result: SUCCESS
  required_ci_job: 95309109578
  required_ci_result: SUCCESS
  broad_source_run: 32001356705
  broad_source_job: 95302168871
  broad_source_artifact: 9278519216
  broad_hosted_job: 95302411849
  broad_final_artifact: 9278527206
  targeted_run: 32002326947
  targeted_source_job: 95304896213
  targeted_source_artifact: 9278827774
  targeted_hosted_job: 95305039463
  targeted_final_artifact: 9278833445
  camera_run: 32003150333
  camera_source_job: 95307268007
  camera_source_artifact: 9279105537
  camera_hosted_job: 95307487191
  camera_final_artifact: 9279111731
identity_results:
  protocol_handler: {vptr: 0x030871d8, typeinfo: 0x03085fb8, rtti: tibia::worldmap::TWorldmapProtocolMessageHandler, classification: PROVEN}
  storage: {vptr: 0x0308ce70, typeinfo: 0x0308b5f0, rtti: tibia::worldmap::TWorldMapStorage, classification: PROVEN}
  storage_control: {vptr: 0x02f683d0, typeinfo: 0x0307fb20, rtti: counted_TWorldMapStorage, classification: PROVEN}
  viewport: {vptr: 0x0308c9a8, typeinfo: 0x0308b590, rtti: tibia::worldmap::TWorldMapViewport, classification: PROVEN}
  render_provider: {vptr: 0x02f6c258, typeinfo: 0x03089b70, classification: PROVEN}
  camera: {vptr: 0x03083968, typeinfo: 0x03080500, classification: PROVEN}
  picker: {vptr: 0x02f6b7c8, typeinfo: 0x03086888, classification: PROVEN}
upstream_18_14:
  static_literal_address: 0x01cdd958
  packed_qword: 0x0000000e00000012
  handler_constructor_default: PROVEN
  handler_master_offsets: [+0xb0, +0xb4]
  snapshot_builder: 0x00bc6350
  snapshot_pair_offset: +0x38
  storage_dispatch: 0x00cdb770
  storage_slot_12: 0x00cc6cd0
  storage_pair_offsets: [+0x48, +0x4c]
  end_to_end_chain: PROVEN
  handler_complete_later_writer_census: UNKNOWN
storage_geometry:
  constructor: 0x00cbf37a
  embedded_extent_vptr: 0x02f61578
  requested_offsets_initialized: [+0x18, +0x1c, +0x30, +0x34, +0x48, +0x4c]
  slot_12_mutator: 0x00cc6cd0
  requested_offsets_mutated: [+0x18, +0x1c, +0x30, +0x34, +0x48, +0x4c]
  slot_14_bounds_reader: 0x00cb01d0
  bounds_semantics: half_open_lower_inclusive_upper_exclusive
  extent_driven_oob_eviction: PROVEN
  live_collection_count_offset: +0x88
  maximum_capacity: UNKNOWN
viewport_recovery:
  constructor: 0x00cbf680
  exact_vptr: 0x0308c9a8
  constructor_18_14_default: PROVEN
  geometry_update: 0x00cbf700
  geometry_recomputed: PROVEN
  signed_shift_by_5: PROVEN
render_recovery:
  primary_vtable_slots: 0..21
  clipping_culling_iteration: PROVEN
  fixed_32_grid_arithmetic: PROVEN
  extent_and_subfield_extent_state: PROVEN
picker_recovery:
  primary_vtable_slots: 0..7
  screen_world_fixed_32_transform: PROVEN
  range_bounds: PROVEN
camera_recovery:
  primary_vtable_slots: 0..4
  exact_layout: PROVEN
  higher_level_viewport_camera_coownership: PROVEN
  exact_vptr_neighborhoods_staged: 11
  direct_camera_field_to_storage_or_master_extent_edge: NOT_RECOVERED_BOUNDED
  named_projection_formula: UNKNOWN
  preidentified_mutation_site: false
  post_change_validation_dependency: true
fixed_representation:
  packed_18_14: PROVEN
  packed_viewport_delta_15_11: PROVEN
  mask_0x1f: PROVEN
  shift_5_scale_32: PROVEN
  fixed_record_sizes_0x18_0x20_0x28_0x30: PROVEN
static_classification: STATIC_DEPENDENCY_GRAPH_RECOVERED
static_patch_graph_ready: true
mutation_design_ready: false
client_byte_mutation_authorized: false
remaining_static_blocker:
  status: NONE_FOR_STATIC_DEPENDENCY_DISCOVERY
  carried_unknowns:
    - complete post-construction writer census for Handler master 18/14 pair
    - source-level member names/units for geometry pairs
    - named Camera projection formula / indirect coupling outside bounded exact-vptr neighborhoods
  effect: must be carried into any separately authorized mutation-design/physical-validation task; no additional patch sites may be invented from these unknowns
final_evidence: docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260817-downstream-exact-static-consumption.md
next_action: none for this STATIC-RE discovery task; a separately authorized mutation-design task may consume STATIC_PATCH_GRAPH_READY=true, but client-byte mutation remains forbidden here
---

# Track A worldmap extent static RE

The original exact-static blocker and the later downstream consumer blocker are both resolved by bounded exact-client producers #437 and #446. The final durable consumer checkpoint records the exact upstream `18/14` chain, Storage/Viewport separation and recomputation, RenderProvider clipping/culling/indexing, Picker fixed-32 transforms, and the bounded Camera coordination result.

`STATIC_PATCH_GRAPH_READY=true` now means the static dependency graph is recovered sufficiently to close discovery. It does **not** authorize or design a client-byte mutation. `MUTATION_DESIGN_READY=false` and all client-byte mutation remains forbidden in this task.
