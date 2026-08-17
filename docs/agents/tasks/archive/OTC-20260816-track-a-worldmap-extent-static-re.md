---
task_id: OTC-20260816-track-a-worldmap-extent-static-re
status: completed
agent: ChatGPT
session_id: chatgpt-coord-worldmap-extent-closeout-20260817
session_role: promotion_integration_coordinator
project_lane: otclient
lane: STATIC-RE
track_id: official-client-re
task_kind: discovery
phase: archived
branch: research/OTC-20260816-track-a-worldmap-extent-static-re
base_branch: main
terminal_main_observed_before_consumer_cleanup: 8212765956a9bfafd2d8a7687440c02716c87170
pr: 367
risk: medium
execution_class: github_hosted
runtime_access: none
mutation_authorized: false
implementation_authorized: false
physical_e2e_required: false
owner_funded_ai_api_authorized: false
ownership_released: true
owned_paths: []
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
producer_437:
  pr: 437
  accepted_evidence_source_head: 3e14d079a1e6d09a21c838a4a82c4fc51b7b7e74
  strict_main_terminal_head: 8b34175e873ee1a950c3fe21b07f1292696cf309
  strict_main_terminal_ci: 32007165687
  strict_main_terminal_ci_result: SUCCESS
  canonical_merge: f753b5aa94e9aeb6b5554fd5bb827823bda80256
  final_cross_check_run: 32004839610
  final_source_artifact: 9279649834
  final_hosted_artifact: 9279654629
producer_446:
  pr: 446
  accepted_evidence_source_head: f7f16af614a88100cc82ff7ecf0b112cb2e0605c
  strict_main_terminal_head: 034d2bf5c2c0f3bf40f64889b9e342b61ef61622
  strict_main_terminal_ci: 32007282137
  strict_main_terminal_ci_result: SUCCESS
  canonical_merge: 8212765956a9bfafd2d8a7687440c02716c87170
  broad_run: 32001356705
  targeted_run: 32002326947
  camera_run: 32003150333
accepted_result:
  static_classification: STATIC_DEPENDENCY_GRAPH_RECOVERED
  STATIC_PATCH_GRAPH_READY: true
  MUTATION_DESIGN_READY: false
  client_byte_mutation_authorized: false
  handler_constructor_default_18_14: PROVEN
  handler_snapshot_to_exact_storage_slot12: PROVEN
  storage_extent_bounds_and_eviction: PROVEN
  viewport_default_and_recompute: PROVEN
  render_fixed_32_clipping_indexing_iteration: PROVEN
  picker_fixed_32_screen_world_transform: PROVEN
  camera_layout_and_viewport_coownership: PROVEN
  camera_direct_extent_mutation_edge: NOT_RECOVERED_BOUNDED
carried_unknowns:
  - complete post-construction writer census for Handler +0xb0/+0xb4
  - exact source-level member names/units for geometry fields
  - named Camera projection formula or indirect coupling outside bounded exact-vptr neighborhoods
  - any network/parser extent ceiling not proven by the accepted packages
  - semantic interpretation of the RenderProvider 65535 x 10-byte allocation as a world-map ceiling
  - any safe client-byte mutation design
safety_boundary:
  runtime_access: none
  client_executed: false
  process_memory_accessed: false
  canonical_runtime_accessed: false
  client_bytes_mutated: false
  raw_client_uploaded: false
  owner_funded_ai_api_used: false
validation:
  coordinator_decision: ACCEPT_WITH_EDITS_COMPLETED
  producer_437_canonical: PASS
  producer_446_canonical: PASS
  consumer_full_terminal_diff_audit_required_before_merge: true
  consumer_exact_terminal_head_ci_required_before_merge: true
  unresolved_review_threads_at_cleanup_start: 0
e2e:
  status: NOT_APPLICABLE
  reason: static reverse-engineering evidence closeout only; no user-facing or live-runtime behavior is changed
cleanup:
  one_shot_analyzer_terminal_tree: removed
  active_task_terminal_tree: removed
  durable_evidence_promoted: true
  final_report_refreshed: true
  continuation_handover_refreshed: true
closeout:
  ownership_released: true
  archive_complete: true
  no_new_static_producer_required: true
next_action: none for this STATIC-RE task; any client-byte mutation design or physical validation requires separate explicit authorization and must consume the frozen static graph
---

# Worldmap extent static dependency graph — archived

The coordinator accepts the completed static graph after canonical producer merges #437 and #446. `STATIC_PATCH_GRAPH_READY=true` closes bounded dependency discovery only; it does not authorize or define a client-byte mutation. All unresolved later-writer, Camera projection/indirect-coupling, possible protocol ceilings and safe-mutation questions remain explicit constraints for any separately authorized follow-on task.
