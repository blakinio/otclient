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
live_main_observed: ffe954be315ee29825c726b996a30fea8475a0f3
pr: 367
risk: medium
updated: 2026-08-16T18:23:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-worldmap-extent-static-re.md
  - .github/scripts/tibia-official-client-re-worldmap-extent-static.py
  - docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/**
  - docs/agents/reports/OTCLIENT-20260816-worldmap-extent-static-re.md
modules_touched: []
reuses:
  - docs/agents/reports/OTCLIENT-20260816-official-client-map-viewport-feasibility.md
  - docs/agents/evidence/OTC-20260816-official-client-map-viewport-feasibility/20260816-evidence.md
  - PR #365 merged feasibility checkpoint
  - PR #310 hosted exact-client staging failure evidence
  - run 31892019505 artifact 9248797952 historical exact-binary static evidence
  - run 31883967070 artifact 9246756211 richer historical exact-static census
  - run 31821458677 artifact 9227370490 retained raw provenance/strip/GDB evidence
  - run 31804083206 job 94778661881 exact fenced handler disassembly log
  - commits caa938463356ce9a8ece92e9ae908ba507f501a9 and 734f845deace5a26efa09b96a168bea0c05272f0 observer producer source
  - user-supplied tibia.x64.tar.gz artifact 9264329820 exact archive fence
depends_on: []
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: static/artifact reverse engineering remains deterministic and GitHub-hosted; retained same-repo evidence was exhausted to a bounded missing-static-window blocker
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
last_progress_at: 2026-08-16T18:23:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: exact-static-evidence-blocker
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
retained_evidence_research_path: BLOCKED_NEW_EXACT_STATIC_EVIDENCE_REQUIRED
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
  viewport_18x14_interpretation: INFERENCE
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
  status: EXHAUSTED_FOR_CURRENT_DOWNLOADED_SET
  evidence: docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260816-retained-identity-window-exhaustion.md
  missing_vptr_header_bytes: true
  missing_geometry_field_writers_xrefs: true
  repeated_scan_allowed: false
static_blocker:
  status: BLOCKED
  kind: NEW_EXACT_STATIC_EVIDENCE_REQUIRED
  effect: class identities and safe field patch sites cannot be proven from the current retained set
  acceptable_unblockers:
    - previously uninspected same-repository retained artifact containing the exact windows/relocations
    - governance-compliant staging of the fenced exact client sufficient to extract only bounded missing static evidence
  forbidden_duplicate_action: repeat identical official CDN staging attempt
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
next_action: obtain NEW exact static evidence for at least one identity window or geometry writer/xref; do not rescan the current retained set or repeat identical CDN fetches; after unblocking, resume the same PR/task with storage/render/camera/picker dependency recovery
---

# Track A worldmap extent static RE

## Objective
Recover the full static patch/dependency graph for `TWorldMapExtent`, `TWorldMapSubfieldExtent`, `TWorldMapViewport`, `TWorldMapStorage`, `TWorldmapProtocolMessageHandler`, `TWorldMapRenderProvider`, `TWorldMapCamera` and `TWorldMapPicker` before any client-byte mutation.

## Current classification

```yaml
static_classification: MORE_STATIC_RE_NEEDED
fresh_exact_binary_materialization: BLOCKED
retained_evidence_research_path: BLOCKED_NEW_EXACT_STATIC_EVIDENCE_REQUIRED
runtime_discriminator_required: false
```

The current downloaded retained evidence set has been exhausted for the exact identity/writer questions that now gate safe patch design. This is a static-input blocker, not a reason to create a new task or PR.

No new runtime, GUI/session, client-byte mutation, Synology static RE, credentials, Codex/OpenAI API or owner-funded token use occurred.

## Durable evidence

- `20260816-retained-provenance-recovery.md` — raw geometry, exact prefixes and type/container census.
- `20260816-user-supplied-linux-launcher-artifact.md` / `20260816-owner-upload-launcher-package.md` — exact user upload fence and GitHub artifact provenance.
- `20260816-exact-handler-disassembly-recovery.md` — producer-source labels plus exact fenced FullMap/Create/Change/Delete/MapDescription disassembly graph.
- `20260816-retained-owner-geometry-object.md` — direct `owner+0x10` object fields, exact stored `18/14`, candidate bound deltas and static vptr `0x0308ce70`.
- `20260816-owner-vptr-storage-scale-coupling.md` — common handler-owner static vptr `0x030871d8`, exact identity windows, and `0xced1b0 -> self+0x30/+0xd0` float coupling.
- `20260816-retained-identity-window-exhaustion.md` — bounded search proving that the current retained set lacks the required vtable-header/typeinfo windows and geometry-field writer/xrefs.

## Major current facts

- A concrete object on the proven `owner+0x10` path stores exact DWORDs `18/14` at `+0x48/+0x4c`; two candidate bound pairs in the same object differ independently by `18/14`.
- Its exact historical static vptr is `0x0308ce70`; exact class identity remains `UNKNOWN`.
- The common historical map-handler owner has exact static vptr `0x030871d8`; `TWorldmapProtocolMessageHandler` is a strong but unproven semantic correlation.
- `FullMap@0xcec8d0` multiplies two payload integers by exactly 32 before a worldmap-owner virtual call.
- `MapDescription@0x19a8a80` uses descriptor grid/divisor fields `+0x38/+0x3c/+0x40/+0x48` and coordinate-transform inputs `+0x08/+0x0c/+0x10`.
- `0xced1b0` rebuilds a bucketed 0x20-byte-node hash structure and later consumes a float at dependency `self+0x30/+0xd0`; exact class and semantic meaning remain `UNKNOWN`.
- The exact-static census contains all target type names, full counted viewport string start `0x1cabb60`, full counted protocol-handler string start `0x1cdba40`, and literal `tibia::worldmap::TWorldMapExtentX` at `0x1cd9ad7`.
- Recursive retained-file search found no preserved `vptr-16/vptr-8` header bytes for `0x030871d8`, `0x0308ce70` or `0x02f683d0`, and no direct geometry `+0x48/+0x4c` writer/xrefs.

## Acceptance progress

- [x] exact historical installed-client fence retained;
- [x] all eight target type surfaces present;
- [x] shared-lifetime/control-block surfaces recovered;
- [x] raw 18-sample horizontal groups and Y delta 14 preserved;
- [x] concrete worldmap dependency object stores exact `18/14`;
- [x] candidate bound-pair differences independently equal `18/14`;
- [x] common handler owner vptr recovered;
- [x] observer label-source provenance recovered;
- [x] retained disassembly recovered for bounded map-handler/description ranges;
- [x] protocol-side ×32 conversion proven;
- [x] descriptor grid/divisor accesses proven;
- [x] candidate hash rebuild and post-rebuild float coupling proven;
- [x] current retained identity-window search bounded and exhausted;
- [ ] exact class identity for static vptr `0x0308ce70`;
- [ ] exact class identity for static vptr `0x030871d8`;
- [ ] semantic names/units for geometry fields;
- [ ] extent/subfield/viewport fields semantically identified;
- [ ] constructors/default writers and complete readers/writers recovered;
- [ ] storage direct-member relation and capacity/eviction rules proven;
- [ ] render/camera/picker clipping/culling/transform dependencies traced;
- [ ] fixed allocations/loop bounds/masks/packing audited completely;
- [ ] coherent patch/dependency graph ready for mutation design.

## Exact blocker

Further progress now requires **new exact static evidence**, not another pass over the same retained files. Any future continuation must resume this same task/PR and first obtain one of:

1. a previously uninspected same-repository artifact containing one of the exact identity windows/relocations; or
2. a governance-compliant staging of the fenced exact client sufficient to extract only the bounded missing bytes/relocations/writer xrefs.

Do not repeat the already-failed identical official CDN staging attempt. Do not use Synology as an unauthorized static fallback.