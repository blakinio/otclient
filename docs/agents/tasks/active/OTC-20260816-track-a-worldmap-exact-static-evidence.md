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
phase: consumer-ready-exact-static-evidence
branch: research/OTC-20260816-track-a-worldmap-exact-static-evidence
base_branch: main
base_main: b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4
current_main_at_admission: b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260816-track-a-worldmap-exact-static-evidence
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
updated: 2026-08-16T23:22:42+02:00
producer_pr: 437
producer_evidence_head: d605640d5d949067e4e178e5086bf5b8873e9989
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
  - PR #367 / OTC-20260816-track-a-worldmap-extent-static-re as consumer only; its branch is not owned or modified by this producer
  - PR #405 / runtime v7 as historical client_window_missing evidence only
  - PR #431/#432/#434 as the fresh post-v7 GUI discriminator and exact-source selector precedent
  - immutable exact-source selector in commit cb557da12ebb41c597340909b2db717ee59cdfe1
  - PR #435 as read-only source-staging precedent only; its stale retained-run path was not reused
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
  reason: user-directed RUNTIME continuation required physical exact-file evidence for PR #367; current routing permits bounded read-only host-local exact-file staging when retained GitHub evidence is insufficient
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
  requested_identity_windows:
    - 0x030871c8..0x030871d7 for vptr 0x030871d8
    - 0x0308ce60..0x0308ce6f for vptr 0x0308ce70
    - 0x02f683c0..0x02f683cf for vptr 0x02f683d0
  requested_geometry_offsets:
    - +0x18
    - +0x1c
    - +0x30
    - +0x34
    - +0x48
    - +0x4c
  priority_values:
    - +0x48 = 18
    - +0x4c = 14
  physical_confirmation_owner: RUNTIME
researcher_delivery: draft_only
WORLD_MAP_STATIC_EVIDENCE_READY: true
programme_complete: false
delivery_state: CONSUMER_READY_DRAFT
identity_results:
  recovered: 3
  total: 3
  protocol_handler:
    vptr: 0x030871d8
    typeinfo: 0x03085fb8
    rtti: tibia::worldmap::TWorldmapProtocolMessageHandler
  storage:
    vptr: 0x0308ce70
    typeinfo: 0x0308b5f0
    rtti: tibia::worldmap::TWorldMapStorage
  control_block:
    vptr: 0x02f683d0
    typeinfo: 0x0307fb20
    rtti: std::_Sp_counted_ptr_inplace<tibia::worldmap::TWorldMapStorage,...>
geometry_results:
  constructor: 0x00cbf37a
  storage_writer_vtable_slot_12: 0x00cc6cd0
  storage_bounds_reader_vtable_slot_14: 0x00cb01d0
  storage_paired_reader_vtable_slot_13: 0x00cb0180
  embedded_extent_vptr: 0x02f61578
  embedded_extent_typeinfo: 0x0306fc60
  embedded_extent_rtti: tibia::worldmap::TWorldMapExtent
  requested_offsets_initialized: [+0x18, +0x1c, +0x30, +0x34, +0x48, +0x4c]
  requested_offsets_mutated: [+0x18, +0x1c, +0x30, +0x34, +0x48, +0x4c]
  requested_offsets_direct_bounds_read: [+0x18, +0x1c, +0x30, +0x34]
  requested_extent_pair_read: [+0x48, +0x4c]
  extent_pair_read_abi_role: INFERENCE_HIDDEN_SRET
  priority_pair_writer: 0x00cc6d2c
  priority_pair_writer_semantics: copies one QWORD from argument rsi+0x38 into TWorldMapStorage+0x48, covering +0x48/+0x4c
  direct_immediate_18_writer_found: false
  direct_immediate_14_writer_found: false
  exact_dynamic_upstream_origin_of_18_14: UNKNOWN
  configured_vs_computed_vs_parser_derived: UNKNOWN
  classification: MUTABLE_COPY_DRIVEN_AT_TWORLDMAPSTORAGE_LAYER
follow_on_rtti:
  TWorldMapViewport: {typeinfo: 0x0308b590, vptr: 0x0308c9a8, first_slot: 0x00dee920}
  TWorldMapStorage: {typeinfo: 0x0308b5f0, vptr: 0x0308ce70, first_slot: 0x00dee8e0}
  TWorldMapRenderProvider: {typeinfo: 0x03089b70, vptr: 0x02f6c258, first_slot: 0x00820970}
  TWorldMapCamera: {typeinfo: 0x03080500, vptr: 0x03083968, first_slot: 0x00dedda0}
  TWorldMapPicker: {typeinfo: 0x03086888, vptr: 0x02f6b7c8, first_slot: 0x008205c0}
source_validation:
  source_run: 31972743782
  source_job: 95227595548
  source_result: success
  source_artifact_id: 9270235755
  source_artifact_sha256: 039d22fe5f88a07784c4ddc32cf6b1d9c2d07a34e90ed5902ffd21d3acd5735b
  identity_windows_recovered: 3
  direct_vptr_xrefs: 9
  bounded_code_windows: 49
  bounded_code_raw_bytes: 52992
hosted_validation:
  recovery_run: 31972915689
  recovery_job: 95228024727
  recovery_result: success
  final_artifact_id: 9270276361
  final_artifact_sha256: 0dc8d0a44e5a2550ef79c219bda14787796ef7accc0ab1627fecd7c6d55330bc
  raw_client_present: false
  exact_fence_validated: true
  sanitized_boundary: pass
prior_failures_and_discriminators:
  - run: 31972285354
    job: 95226438379
    result: failed_precondition_before_selector
    repeated_identically: false
  - run: 31972499618
    job: 95226977563
    result: exact_source_candidate_1_proven_but_objdump_and_llvm_objdump_absent
    repeated_identically: false
  - run: 31972743782
    job: 95227676658
    result: hosted_derived_markdown_ordering_guard_only
    recovery: hosted_only_run_31972915689_from_preserved_source_artifact
    repeated_physical_read_for_recovery: false
durable_evidence:
  json:
    path: docs/agents/evidence/OTC-20260816-track-a-worldmap-exact-static-evidence/20260816-worldmap-exact-static-evidence.json
    commit: 400fe33cf66a3385a91063a74e8fba646b3369e0
  handoff:
    path: docs/agents/evidence/OTC-20260816-track-a-worldmap-exact-static-evidence/20260816-worldmap-exact-static-evidence.md
    commit: d605640d5d949067e4e178e5086bf5b8873e9989
curation:
  raw_generic_displacement_classifier_promoted_as_direct_field_proof: false
  stack_only_plus_0x4c_hit_promoted: false
  adjacent_TWorldMapViewport_plus_0x48_immediate_8_promoted_as_storage: false
  direct_storage_plus_0x4c_coverage: QWORD writes/reads at Storage+0x48 span both DWORD +0x48 and +0x4c
remaining_unknowns:
  - exact RTTI identity of embedded vptr 0x02f615a0 at Storage+0x10 and Storage+0x28
  - exact member names and units for the six requested DWORD fields
  - upstream producer of slot-12 input QWORD rsi+0x38 and exact dynamic origin of retained values 18/14
  - storage capacity/eviction and fixed allocation constraints
  - render clipping/culling and iteration bounds
  - camera projection/scale limits
  - picker screen/world limits
  - parser packing/masks beyond the recovered geometry writer path
  - any safe mutation or client patch design
next_action: PR #367 may consume the durable evidence above without Synology access; producer PR #437 remains Draft per researcher_delivery=draft_only and must not modify the consumer branch
---

# Track A world-map exact static evidence producer — consumer-ready Draft

The requested exact static evidence is now durable in GitHub and sufficient to unblock PR #367's next static-reasoning step. The three identity windows are exact; the historical geometry object is proven to be `TWorldMapStorage`; all six requested geometry DWORDs have exact initialization and mutation coverage through three QWORD pairs; `+0x48/+0x4c` are fields of an embedded exact `TWorldMapExtent`; and the Storage vtable exposes the direct pair writer and half-open bound reader.

The exact upstream producer of the observed runtime `18/14` pair remains unknown. This producer does not convert that unknown into a patch hypothesis and does not claim current live-runtime authority.
