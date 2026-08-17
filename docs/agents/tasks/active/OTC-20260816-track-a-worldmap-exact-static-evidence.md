---
task_id: OTC-20260816-track-a-worldmap-exact-static-evidence
status: implementing
agent: ChatGPT
session_id: chatgpt-runtime-worldmap-static-producer-20260816
session_role: researcher_producer_under_coordinator_dispatch
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: evidence_staging
phase: second-pack-consumer-ready-exact-static-evidence
branch: research/OTC-20260816-track-a-worldmap-exact-static-evidence
base_branch: main
base_main: b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4
current_main_at_initial_admission: b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4
second_pack_main_at_preflight: 8c9486e2c6109a7a39b564804c8acd707659b5e0
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260816-track-a-worldmap-exact-static-evidence
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
updated: 2026-08-17T09:15:00+02:00
producer_pr: 437
producer_evidence_head: 93a9df8cb999e173658cee4c1763afa092973e15
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-worldmap-exact-static-evidence.md
  - docs/agents/evidence/OTC-20260816-track-a-worldmap-exact-static-evidence/**
  - .github/workflows/tibia-official-client-re-worldmap-exact-static-evidence.yml
  - .github/workflows/tibia-official-client-re-worldmap-exact-static-hosted-recovery.yml
  - .github/scripts/tibia-official-client-re-worldmap-exact-static-evidence.py
  - .github/scripts/tibia-official-client-re-worldmap-exact-static-evidence-v2.py
  - .github/scripts/tibia-official-client-re-worldmap-exact-static-evidence-v3.py
modules_touched: []
reuses:
  - PR #367 / OTC-20260816-track-a-worldmap-extent-static-re as read-only consumer; its branch is not owned or modified by this producer
  - PR #405 / runtime v7 as historical evidence only; no historical PID/session/display promoted as current
  - immutable exact-source selector precedent and existing first-pack #437 evidence
  - docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
policy_version: 2
prompting_standard_version: 2.1
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_mode: github-actions
execution_class: github_hosted
runtime_access: none
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
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: false
owner_funded_ai_api_authorized: false
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
source_staging_exception:
  coordinator_approved: true
  source_executor: synology-otclient-01
  source_access: read_only_file_only
  source_runtime_access: none
  source_candidate_index: 1
  canonical_state_access: forbidden
  client_process_access: forbidden
  process_memory_access: forbidden
  x11_vnc_access: forbidden
  login_session_access: forbidden
  network_access: forbidden
  gameplay_access: forbidden
  raw_client_upload: forbidden
  client_byte_mutation: forbidden
  allowed_output: bounded sanitized text/json evidence only
  hosted_validation_executor: ubuntu-latest
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
consumer_contract:
  pr: 367
  task: OTC-20260816-track-a-worldmap-extent-static-re
  consumer_branch: research/OTC-20260816-track-a-worldmap-extent-static-re
  consumer_branch_modified: false
researcher_delivery: draft_only
WORLD_MAP_STATIC_EVIDENCE_READY: true
WORLD_MAP_DOWNSTREAM_EVIDENCE_READY: true
STORAGE_EXTENT_UPSTREAM_SOURCE_PROVEN: true
RENDER_LIMITS_RECOVERED: true
CAMERA_GEOMETRY_RECOVERED: false
PICKER_BOUNDS_RECOVERED: true
FIXED_TILE_LIMIT_FOUND: UNKNOWN
programme_complete: false
delivery_state: CONSUMER_READY_DRAFT

first_pack:
  durable_json: docs/agents/evidence/OTC-20260816-track-a-worldmap-exact-static-evidence/20260816-worldmap-exact-static-evidence.json
  durable_handoff: docs/agents/evidence/OTC-20260816-track-a-worldmap-exact-static-evidence/20260816-worldmap-exact-static-evidence.md
  storage_vptr: 0x0308ce70
  storage_typeinfo: 0x0308b5f0
  storage_constructor: 0x00cbf37a
  storage_slot12: 0x00cc6cd0
  storage_slot12_extent_writer: 0x00cc6d2c
  storage_slot14_bounds: 0x00cb01d0

second_pack:
  durable_json:
    path: docs/agents/evidence/OTC-20260816-track-a-worldmap-exact-static-evidence/20260817-worldmap-second-pack-evidence.json
    commit: a7853827d18a2551b72e126ccb030378b875b486
  durable_handoff:
    path: docs/agents/evidence/OTC-20260816-track-a-worldmap-exact-static-evidence/20260817-worldmap-second-pack-evidence.md
    commit: 93a9df8cb999e173658cee4c1763afa092973e15
  preflight:
    path: docs/agents/evidence/OTC-20260816-track-a-worldmap-exact-static-evidence/20260817-second-pack-preflight.md
    commit: 87ea0f679175d676d9cb2721b1d6f3f810481cb4
  runs:
    - {run: 32002543926, source_job: 95305539737, source_artifact: 9278903625, hosted_job: 95305685220, final_artifact: 9278908515, result: success}
    - {run: 32003065517, source_job: 95307020627, source_artifact: 9279071635, hosted_job: 95307179088, final_artifact: 9279075470, result: success}
    - {run: 32003607118, source_job: 95308578004, source_artifact: 9279245326, hosted_job: 95308725378, final_artifact: 9279250068, result: success}
    - {run: 32004356610, source_job: 95310743900, source_artifact: 9279498428, hosted_job: 95310922681, final_artifact: 9279503543, result: success}
    - {run: 32004614539, source_job: 95311482128, source_artifact: 9279577899, hosted_job: 95311635844, final_artifact: 9279583871, result: success}
    - {run: 32004839610, source_job: 95312106162, source_artifact: 9279649834, hosted_job: 95312291576, final_artifact: 9279654629, result: success}

upstream_results:
  protocol_handler:
    vptr: 0x030871d8
    typeinfo: 0x03085fb8
    static_metaobject: 0x03087800
    static_metacall: 0x00df2a60
    constructor: 0x00803ab0
    hardcoded_pair_source: 0x01cdd958
    hardcoded_pair: [18, 14]
    master_pair_fields: [+0xb0, +0xb4]
    snapshot_method: 0x00cdb770
  snapshot_builder:
    function: 0x00bc6350
    source_pair_load: 0x00bc6372
    output_pair_store: 0x00bc63af
    output_pair_offset: +0x38
  storage_feed:
    handler_dependency_offset: +0x10
    virtual_call: 0x00cdb7ab
    virtual_slot: 12
    exact_storage_slot12: 0x00cc6cd0
    exact_storage_pair_write: 0x00cc6d2c
    exact_storage_pair_fields: [+0x48, +0x4c]
  receiver_identity_static_structure: INFERENCE
  receiver_identity_retained_vptr_cross_check: FACT
  complete_later_writer_census_for_handler_master_pair: UNKNOWN

viewport_results:
  constructor: 0x00cbf680
  constructor_default_source: 0x01cdd958
  constructor_default_pair: [18, 14]
  constructor_margin_source: 0x01d32ef0
  constructor_margin_prefix: [1, 2, 1, 2]
  recompute: 0x00cbf700
  recompute_base_source: 0x01d63cd0
  recompute_base_pair: [15, 11]
  dynamic_extent_setter: 0x00cb2220
  dynamic_extent_formula: ceil(pixel_dimension/32)+paired_margins
  extent_output_fields: [+0x40, +0x44]
  extent_aggregate: 0x00cb07b0
  direct_viewport_to_storage_edge: NOT_PROVEN

render_results:
  vptr: 0x02f6c258
  typeinfo: 0x03089b70
  constructor_xref: 0x00ccfa02
  dynamic_bounds_indexer: 0x00cd2260
  fixed32_record_iteration: 0x00cd08b0
  other_load_bearing_functions: [0x00cea540, 0x00cd1e50, 0x00ce9700]
  fixed_allocation_bytes: 0x9fff6
  fixed_record_stride: 0x0a
  fixed_record_count: 65535
  fixed_allocation_is_tile_limit: UNKNOWN
  independent_18_14_limit: NOT_RECOVERED

picker_results:
  vptr: 0x02f6b7c8
  typeinfo: 0x03086888
  fixed32_transform: 0x00cd0400
  other_load_bearing_functions: [0x00cd65b0, 0x00ce7aa0, 0x00ce80c0]
  independent_18_14_limit: NOT_RECOVERED

camera_results:
  vptr: 0x03083968
  typeinfo: 0x03080500
  default_scalar_plus_d0: 1.0
  dependency_function: 0x00ced1b0
  dependency_field_chain: self+0x30 -> dependency+0xd0
  multiplier_address: 0x029505a8
  multiplier_double: 32.0
  dependency_type: UNKNOWN
  named_world_to_screen_formula: UNKNOWN
  named_screen_to_world_formula: UNKNOWN

limit_audit:
  hardcoded_18_14: FACT
  hardcoded_18_14_address: 0x01cdd958
  fixed32_shift5_mask31: FACT
  render_65535_x_10_table: FACT
  render_table_is_tile_ceiling: UNKNOWN
  storage_fixed_capacity_ceiling: NOT_RECOVERED
  network_payload_extent_ceiling: NOT_RECOVERED
  fixed_tile_limit: UNKNOWN

patch_candidate_graph:
  safe_single_parameter_proven: false
  client_modified: false
  summary: 0x01cdd958 -> Handler+0xb0/+0xb4 -> 0x00bc6350 snapshot+0x38 -> Handler+0x10 vslot12 -> Storage+0x48/+0x4c; separately the same literal initializes Viewport+0x40/+0x44 while 0x00cb2220 later recomputes Viewport from pixel size /32 plus margins; RenderProvider and Picker consume the fixed-32 representation.
  warning: do not treat the shared literal as a safe one-byte/one-QWORD patch until Handler later-writer, protocol/network and capacity effects are fully proven

remaining_unknowns:
  - complete post-construction writer census for ProtocolHandler master +0xb0/+0xb4
  - exact static class identity tying the 0x00804620 outer owner to the first-pack outer+0x2f8 Storage construction path without relying on retained vptr evidence
  - semantic role of RenderProvider fixed 65535 x 10-byte table as a possible tile/cache limit
  - named Camera world-to-screen / screen-to-world projection functions and exact type behind 0x00ced1b0 self+0x30
  - any network/parser limit that could cap live map delivery beyond the retained Storage extent
  - a safe mutation design; mutation remains unauthorized
next_action: PR #367 may consume the second-pack durable evidence without source-host access; producer PR #437 remains Draft and must not modify the consumer branch
---

# Track A world-map exact-static evidence producer — second package consumer-ready

The second package resolves the previous primary unknown: the packed `18/14` pair originates as a hardcoded exact ProtocolHandler constructor default at `0x01cdd958` and is copied through `0x00bc6350` into the geometry snapshot consumed by the Handler's dependency slot 12. Existing retained exact-vptr evidence plus first-pack RTTI closes that dependency as `TWorldMapStorage` without claiming any historical runtime is current.

The package also proves that `TWorldMapViewport` has a dynamic `/32 + margins` extent setter, recovers RenderProvider clipping/indexing and Picker fixed-32 transform dependencies, and records a bounded Camera geometry dependency without inventing a named projection method. No client bytes were changed and no safe standalone extent patch is claimed.
