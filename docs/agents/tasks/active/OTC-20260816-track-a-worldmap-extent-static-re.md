---
task_id: OTC-20260816-track-a-worldmap-extent-static-re
status: investigating
agent: ChatGPT
session_id: chatgpt-viewport-static-retained-20260816
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
live_main_observed: d7a2d4168816cb42267fc7b20aacb88ae1b13b8e
pr: 367
risk: medium
updated: 2026-08-16T19:20:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-worldmap-extent-static-re.md
  - .github/scripts/tibia-official-client-re-worldmap-extent-static.py
  - docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/**
  - docs/agents/reports/OTCLIENT-20260816-worldmap-extent-static-re.md
modules_touched: []
reuses:
  - docs/agents/reports/OTCLIENT-20260816-official-client-map-viewport-feasibility.md
  - PR #365 merged feasibility checkpoint
  - PR #310 hosted exact-client staging failure evidence
  - run 31892019505 artifact 9248797952 historical exact-binary static evidence
  - run 31883967070 artifact 9246756211 richer historical exact-static census
  - run 31821458677 artifact 9227370490 retained raw provenance/strip/GDB evidence
  - run 31804083206 job 94778661881 exact fenced handler disassembly log
  - complete retained artifact inventory evidence 20260816-complete-retained-artifact-inventory.md
  - main PRs #397 and #405 runtime discriminator read-only cross-checks
depends_on: []
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: complete GitHub artifact inventory review and targeted inspection of all admissible static/vtable/RTTI/provenance candidates now proves that the remaining identity/writer bytes were not durably staged; physical runtime remains a separate lane
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_pressure: high
context_growth: stable
context_score: 10
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: one cohesive graph spans extent ownership, protocol/storage updates and render/camera/picker consumers; no replacement task/PR is warranted
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
runtime_access: none
persistent_session_role: none
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
invocation_started_at: 2026-08-16T14:20:00+02:00
last_progress_at: 2026-08-16T19:20:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: complete-retained-artifact-inventory
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
heavy_validation_runs: 1
hosted_staging_attempts_this_task: 2
hosted_staging_result: INPUT_BLOCKED
fresh_exact_binary_materialization: BLOCKED
retained_evidence_research_path: BLOCKED_EXACT_STATIC_BYTES_NOT_DURABLY_STAGED
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
static_classification: MORE_STATIC_RE_NEEDED
new_gui_session_created: false
runtime_used: false
client_bytes_modified: false
synology_static_re_this_task: false
temporary_hosted_workflow_retained: false
analyzer_validation:
  python_syntax_on_hosted_boundary: PASS
  exact_binary_execution: NOT_RUN_INPUT_BLOCKED
retained_geometry:
  raw_strip_artifact: 9227370490
  two_z7_horizontal_groups_of_18: PROVEN
  y_difference_14: PROVEN
  direct_owner_plus_0x10_pair_18_14: PROVEN
  direct_owner_plus_0x10_pair_offsets: 0x48/0x4c
  candidate_bound_differences_18_14: PROVEN_ARITHMETIC
  owner_plus_0x10_static_vptr: 0x0308ce70
  owner_plus_0x10_exact_class_identity: UNKNOWN
  viewport_18x14_interpretation: VERY_STRONG_INFERENCE
geometry_control_block:
  runtime_address: 0x55867df448b0
  object_runtime_address: 0x55867df448c0
  object_offset_from_control: 0x10
  static_vptr: 0x02f683d0
  retained_refcount_dwords: [13, 1]
  inline_object_at_plus_0x10: PROVEN
  make_shared_sp_counted_ptr_inplace_layout: STRONG_INFERENCE
  direct_counted_viewport_rtti_link: UNKNOWN
handler_owner:
  historical_runtime_address: 0x55868276a460
  static_vptr: 0x030871d8
  exact_class_identity: UNKNOWN
  protocol_handler_identity: INFERENCE
  discriminator_window: 0x030871c8..0x030871d7
observer_source_provenance:
  status: RECOVERED
  create_on_map: 0x00cecc70
  change_on_map: 0x00cecf40
  delete_on_map: 0x00cd4e20
  full_map: 0x00cec8d0
  map_description_capture: 0x019a8ea3
exact_handler_disassembly:
  run: 31804083206
  job: 94778661881
  status: RECOVERED_FROM_RETAINED_JOB_LOG
  full_map_subfield_scale_x32: PROVEN
  map_description_grid_fields_0x38_0x3c_0x40_0x48: PROVEN_ACCESSES
  hash_table_rebuild_0xced1b0: PROVEN_STRUCTURE_INFERENCE_STORAGE
  hash_rebuild_self_0x30_float_0xd0_coupling: PROVEN
  hash_rebuild_self_0x30_exact_class_identity: UNKNOWN
exact_static_identity_frontier:
  handler_owner_vptr_header: 0x030871c8..0x030871d7
  geometry_object_vptr_header: 0x0308ce60..0x0308ce6f
  geometry_control_vptr_header: 0x02f683c0..0x02f683cf
  counted_viewport_type_string_start: 0x1cabb60
  counted_protocol_handler_type_string_start: 0x1cdba40
retained_identity_search:
  artifact_inventory_total: 493
  inventory_review: COMPLETE
  admissible_static_vtable_rtti_provenance_candidates: INSPECTED
  older_pages_4_5_track_a_artifacts: NONE
  evidence: docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260816-complete-retained-artifact-inventory.md
  missing_vptr_header_bytes: true
  missing_geometry_field_writers_xrefs: true
  repeated_scan_allowed: false
static_blocker:
  status: BLOCKED
  kind: EXACT_STATIC_BYTES_NOT_DURABLY_STAGED
  effect: exact class identities, safe field patch sites and complete render/camera/picker constraints cannot be proven from retained GitHub evidence
  acceptable_unblockers:
    - new admissible exact-client artifact containing one or more missing identity windows/relocations
    - governance-compliant bounded staging of the fenced exact client sufficient to extract the missing static bytes/writer xrefs
  forbidden_duplicate_action: repeat identical official CDN staging attempt
runtime_v7_crosscheck:
  main_pr: 405
  result: FAIL_CLOSED_CLIENT_WINDOW_MISSING_GOVERNANCE_INVALID
  official_exact_client_launch_stage_reached: true
  authoritative_registration_published: false
  gate_b_reached: false
  static_evidence_staged_for_this_task: false
  static_unblock: false
user_supplied_launcher:
  archive_size: 29477141
  archive_sha256: 04a87c801d3855f4da1b07e201dff1f79acc8528c57c984131c3a2a88cb60ea7
  github_artifact: 9264329820
  github_roundtrip_bit_identical: true
  installed_game_client_substitute: false
hosted_official_metadata_probe:
  run: 31949948886
  result: CLOUDFLARE_HTTP_403
  identical_retry_allowed: false
next_action: obtain NEW admissible exact static bytes for at least one identity window and geometry writer/xref; do not rescan the retained inventory, do not repeat identical CDN fetches, and do not use physical Synology runtime as an unauthorized static fallback; after unblocking, resume this same PR/task and finish storage/render/camera/picker dependency auditing before mutation design
---

# Track A worldmap extent static RE

## Objective
Recover the full static patch/dependency graph for `TWorldMapExtent`, `TWorldMapSubfieldExtent`, `TWorldMapViewport`, `TWorldMapStorage`, `TWorldmapProtocolMessageHandler`, `TWorldMapRenderProvider`, `TWorldMapCamera` and `TWorldMapPicker` before any client-byte mutation.

## Current classification

```yaml
static_classification: MORE_STATIC_RE_NEEDED
fresh_exact_binary_materialization: BLOCKED
retained_evidence_research_path: BLOCKED_EXACT_STATIC_BYTES_NOT_DURABLY_STAGED
static_patch_graph_ready: false
```

The GitHub-retained evidence path is now genuinely bounded: the complete 493-artifact inventory was reviewed and all admissible Track A static/vtable/RTTI/provenance candidates were directly inspected. They do not retain the three required vtable-header/typeinfo windows or direct writer xrefs for the geometry fields. Further scanning of the same inventory is prohibited as duplicate work.

## Strongest new structural result

The concrete `owner+0x10` object still stores exact DWORDs `18/14` at `+0x48/+0x4c`, with candidate bound deltas independently equal to `18/14` and static vptr `0x0308ce70`.

Its companion at `owner+0x18` is exactly `0x10` bytes before the object, has static vptr `0x02f683d0`, retained count DWORDs `13/1`, and contains the object inline at companion `+0x10`. The paired structure repeats for adjacent owner dependencies.

**FACT:** inline polymorphic control-like block + counters + object-at-+0x10 layout is directly preserved.

**INFERENCE:** this is strongly consistent with libstdc++ `_Sp_counted_ptr_inplace<T>` / `make_shared<T>`. Combined with the exact counted `TWorldMapViewport` RTTI string, the `18×14` object is now a very strong viewport correlation.

**UNKNOWN:** the direct relocation from control vptr `0x02f683d0` to counted `TWorldMapViewport` typeinfo is not retained, so exact class identity remains unproven.

## Durable evidence

- `20260816-retained-provenance-recovery.md`
- `20260816-exact-handler-disassembly-recovery.md`
- `20260816-retained-owner-geometry-object.md`
- `20260816-owner-vptr-storage-scale-coupling.md`
- `20260816-retained-identity-window-exhaustion.md`
- `20260816-complete-retained-artifact-inventory.md`

## Acceptance progress

- [x] exact historical installed-client fence retained;
- [x] all eight target type surfaces present;
- [x] shared-lifetime/control-block surfaces recovered;
- [x] raw 18-sample horizontal groups and Y delta 14 preserved;
- [x] concrete worldmap dependency object stores exact `18/14`;
- [x] candidate bound-pair differences independently equal `18/14`;
- [x] concrete inline control-block/object layout recovered;
- [x] common handler owner vptr recovered;
- [x] observer label-source provenance recovered;
- [x] retained handler/description disassembly recovered;
- [x] protocol-side ×32 conversion proven;
- [x] descriptor grid/divisor accesses proven;
- [x] candidate hash rebuild and post-rebuild float coupling proven;
- [x] complete repository artifact inventory reviewed;
- [x] all admissible retained static/vtable/RTTI/provenance candidates inspected;
- [ ] exact class identity for static vptr `0x0308ce70`;
- [ ] exact class identity for static vptr `0x030871d8`;
- [ ] direct counted-viewport RTTI identity for control vptr `0x02f683d0`;
- [ ] semantic names/units and complete writers/readers for geometry fields;
- [ ] storage direct-member relation and capacity/eviction rules proven;
- [ ] render/camera/picker clipping/culling/transform dependencies traced;
- [ ] fixed allocations/loop bounds/masks/packing audited completely;
- [ ] coherent patch/dependency graph ready for mutation design.

## Exact blocker

Further progress requires new exact static bytes, not another analysis pass over retained GitHub evidence. Minimum useful evidence is one of the vtable-header/typeinfo windows `0x030871c8..0x030871d7`, `0x0308ce60..0x0308ce6f`, `0x02f683c0..0x02f683cf`, plus writer/xref evidence for geometry `+0x48/+0x4c` and enough downstream exact disassembly to finish render/camera/picker constraints.

RUNTIME v7 on main reached `client_start` but again failed closed at `client_window_missing`; it published no authoritative registration/Gate B and staged no static bytes for this lane. No current legal physical producer is available to this GitHub-hosted STATIC-RE task.

No client bytes were modified. No GUI/login/gameplay was used by this task. No owner-funded Codex/OpenAI API/token use occurred.
