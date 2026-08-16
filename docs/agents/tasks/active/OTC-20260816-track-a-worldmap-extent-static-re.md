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
updated: 2026-08-16T14:49:00+02:00
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
last_progress_at: 2026-08-16T14:49:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: retained-evidence-recovery
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
heavy_validation_runs: 1
hosted_staging_attempts_this_task: 1
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
retained_handler_leads:
  observer_assigned_create_on_map: 0x00cecc70
  observer_assigned_change_on_map: 0x00cecf40
  common_helper_from_change_prefix: 0x00ceca50
  worldmap_partial_handler_lead: 0x00cd4e20
  viewport_shift_candidate_3: 0x00cec8d0
  common_capture: 0x019a8ea3
next_action: continue retained-evidence xref/provenance recovery for 0xceca50/0xcecc70/0xcecf40/0xcd4e20/0xcec8d0 and target type/control-block anchors; keep fresh exact-client staging blocked and do not use Synology or runtime as a shortcut
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

Fresh GitHub-hosted materialization of the exact executable remains unavailable, but the task is no longer terminally blocked because existing same-repository exact-client artifacts preserve additional raw machine code, strip rows and static type census material that had not been consumed by the feasibility checkpoint.

## New durable evidence

`docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260816-retained-provenance-recovery.md` records:

- raw artifact `9227370490` with 90 strip rows;
- two Z=7 horizontal groups with 18 directly retained consecutive X coordinates and exact Y difference 14;
- observer-assigned `CreateOnMap`/`ChangeOnMap` function-pointer leads at static `0xcecc70` / `0xcecf40`;
- offline disassembly facts from retained 256-byte exact-client code samples;
- shared owner/event field accesses and virtual dispatch paths;
- common helper lead `0xceca50`;
- richer exact-static type/control-block census from artifact `9246756211`;
- coordinate-to-`shared_ptr<TWorldMapTile>` unordered-map instantiation;
- explicit UNKNOWN boundaries where object ownership/field semantics remain unproven.

No client bytes, GUI, live runtime, Synology static execution, credentials or owner-funded AI/API resources were used.

## Acceptance progress

- [x] exact client fence retained;
- [x] all eight target type surfaces present;
- [x] richer shared-lifetime/control-block surfaces recovered;
- [x] raw 18-sample horizontal groups and Y delta 14 directly preserved;
- [x] exact code prefixes for two map-event handler leads recovered offline;
- [ ] original observer label-source provenance recovered;
- [ ] extent/subfield/viewport dimension fields recovered;
- [ ] constructors/default writers and complete readers/writers recovered;
- [ ] storage backing/member relation and capacity/eviction rules proven;
- [ ] protocol parser/full-map/strip/floor assumptions traced;
- [ ] render/camera/picker clipping/culling/transform dependencies traced;
- [ ] fixed allocations/loop bounds/masks/packing audited completely;
- [ ] coherent patch/dependency graph ready for mutation design.

The task remains active while retained evidence continues producing new facts.