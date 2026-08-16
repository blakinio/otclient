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
pr: 367
risk: medium
updated: 2026-08-16T15:39:00+02:00
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
execution_reason: static/artifact reverse engineering remains deterministic and GitHub-hosted; retained same-repo evidence permits continued progress despite unavailable fresh exact-client staging
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_pressure: high
context_growth: stable
context_score: 10
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: one cohesive graph spans extent ownership, protocol/storage updates and render/camera/picker consumers; retained evidence is still advancing the same task
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
last_progress_at: 2026-08-16T15:39:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: exact-handler-disassembly-recovery
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
retained_evidence_research_path: active
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
  viewport_18x14_interpretation: INFERENCE
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
next_action: recover remaining 0xceca50 body and retained typeinfo/vtable/xrefs; correlate 0xced1b0 with TWorldMapStorage/unordered_map; trace owner+0x70/+0x10/+0x80/+0xd8 into protocol/storage/render; then recover viewport/render/camera/picker bounds before any mutation design
---

# Track A worldmap extent static RE

## Objective
Recover the full static patch/dependency graph for `TWorldMapExtent`, `TWorldMapSubfieldExtent`, `TWorldMapViewport`, `TWorldMapStorage`, `TWorldmapProtocolMessageHandler`, `TWorldMapRenderProvider`, `TWorldMapCamera` and `TWorldMapPicker` before any client-byte mutation.

## Current classification

```yaml
static_classification: MORE_STATIC_RE_NEEDED
fresh_exact_binary_materialization: BLOCKED
retained_evidence_research_path: active
runtime_discriminator_required: false
```

Fresh GitHub-hosted materialization of the exact installed game-client ELF remains unavailable, but retained same-repository evidence continues to advance the graph. The owner-supplied Linux package has been preserved as exact GitHub artifact `9264329820`; static inspection proves it is the launcher/updater distribution and not the fenced 51,965,216-byte installed client.

## New durable evidence

- `20260816-retained-provenance-recovery.md` — raw geometry, exact prefixes and type/container census.
- `20260816-user-supplied-linux-launcher-artifact.md` / `20260816-owner-upload-launcher-package.md` — exact user upload fence and GitHub artifact provenance.
- `20260816-exact-handler-disassembly-recovery.md` — recovered producer-source labels plus exact fenced FullMap/Create/Change/Delete/MapDescription disassembly graph.

Major new static facts:

- observer-source provenance for `CreateOnMap`, `ChangeOnMap`, `DeleteOnMap`, `FullMap` and the `MapDescription` capture is recovered from historical workflow source;
- `FullMap@0xcec8d0` copies a three-DWORD map-state tuple and multiplies two payload integers by exactly 32 before an owner virtual call;
- `MapDescription@0x19a8a80` uses descriptor fields `+0x38/+0x3c/+0x40/+0x48` as multiplicative/divisor geometry parameters and `+0x08/+0x0c/+0x10` as coordinate-transform inputs;
- neighboring `0xced1b0` rebuilds a bucketed 0x20-byte-node hash structure and is a strong storage/unordered-map correlation candidate;
- Create/Change/Delete share the owner `+0x10 -> vslot +0xa0` family and repeated owner `+0xd8` map-state comparison paths.

No new runtime, GUI/session, client-byte mutation, Synology static RE, credentials, Codex/OpenAI API or owner-funded token use occurred.

## Acceptance progress

- [x] exact historical installed-client fence retained;
- [x] all eight target type surfaces present;
- [x] richer shared-lifetime/control-block surfaces recovered;
- [x] raw 18-sample horizontal groups and Y delta 14 directly preserved;
- [x] observer label-source provenance recovered;
- [x] full retained disassembly recovered for the five bounded map-handler/description ranges;
- [x] protocol-side x32 subfield/tile conversion surface proven;
- [x] descriptor grid/divisor field accesses proven in MapDescription;
- [ ] exact semantic names/units for descriptor geometry fields recovered;
- [ ] extent/subfield/viewport dimension fields recovered;
- [ ] constructors/default writers and complete readers/writers recovered;
- [ ] storage direct-member relation and capacity/eviction rules proven;
- [ ] render/camera/picker clipping/culling/transform dependencies traced;
- [ ] fixed allocations/loop bounds/masks/packing audited completely;
- [ ] coherent patch/dependency graph ready for mutation design.

The task remains active while retained evidence continues producing new facts.