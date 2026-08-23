---
task_id: OTC-20260822-tibia-re-control-center-package-c
status: waiting
agent: ChatGPT
project_lane: otclient
lane: P3-SURVEYOR-INTEGRATION
track_id: official-client-re
task_kind: implementation
phase: final_ci
risk: medium
branch: feat/OTC-20260822-tibia-re-control-center-package-c
base_branch: main
created: 2026-08-22T18:04:00+02:00
updated: 2026-08-23T17:05:00+02:00
execution_mode: remote_desktop+github_connector+github_actions
execution_budget_minutes: 120
execution_budget_reason: cohesive Package C provider implementation, repository-only E2E, exact-head audit, merge and mandatory archive closeout
invocation_started_at: 2026-08-22T17:51:00+02:00
last_progress_at: 2026-08-23T17:05:00+02:00
policy_version: 2
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one read-only producer-to-provider normalization slice with one shared schema/provenance boundary
ci_checks_for_current_head: 2
ci_check_generation: final_exact_head_7e4c6435c3715b7e97d8b7827ca052cf33743cf8
terminal_ci_wait_started_at: 2026-08-23T16:15:00+02:00
terminal_ci_checks_for_current_generation: 2
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
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
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
network_listener_allowed: false
official_client_access: false
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
feature_scope:
  type: data_pipeline
  user_facing: false
  backend_required: true
  frontend_required: false
  integration_required: true
  e2e_required: true
  completion_claim: partial_producer
complete_control_center_programme: false
surveyor_schema_version: otclient.tibia-re-surveyor.collect-all.v2
surveyor_alias_schema_version: otclient.tibia-re-surveyor.alias-view.v2
surveyor_telemetry_schema_version: otclient.tibia-re-surveyor.telemetry.v2
surveyor_missing_readers_schema_version: otclient.tibia-re-surveyor.missing-readers.v2
producer_commit: 1affb3a094a06f2a250140e8173501b3a6938164
producer_acceptance_anchor: 815245ab3cac38a96f60f3ee3395b67f81b81c11
producer_tree_unchanged_since_acceptance_anchor: true
producer_interface:
  - tools/tibia_re_surveyor/survey.py::build_bundle output tree
  - tools/tibia_re_surveyor/collect_all.py::write_collect_all artifact tree
  - surveyor/agent_bundle.json
  - surveyor/runtime.json
  - surveyor/coverage.json
  - aliases/*.json
  - telemetry/*.json
  - missing-readers.json
  - privacy-scan.json
  - manifest.sha256
producer_file_blobs:
  collect_all.py: 43494964ed20cbadeb5e27cda6d441cf4c054b50
  survey.py: 17d54afa3bce401e6d88c85ea7dcf292e1d31f2c
  reader_registry.py: 62a2bc38687f48d6756d5f5eab9d637a110d9f26
  README.md: 5f544a6060fbe714ccf9106b929b97897bba2e5f
unavailable_inputs:
  live_runtime: NOT_REQUESTED
  live_freshness: NOT_AVAILABLE_IN_REPOSITORY_ONLY_E2E
  player_position_semantic_promotion: NOT_PROVEN_CURRENT_PRODUCER
owned_paths:
  - docs/agents/tasks/active/OTC-20260822-tibia-re-control-center-package-c.md
  - docs/agents/tasks/archive/OTC-20260822-tibia-re-control-center-package-c.md
  - docs/agents/evidence/OTC-20260822-tibia-re-control-center-package-c/**
  - tools/tibia_re_control_center/surveyor_provider.py
  - tests/tools/tibia_re_control_center/test_package_c_surveyor_provider.py
read_only_paths:
  - tools/tibia_re_surveyor/**
  - tests/tools/tibia_re_surveyor/**
  - tools/tibia_runtime_bridge/**
  - existing Package A core files
  - Package B and Package D branches/files
depends_on:
  - Package A terminal merge 13b3f02a07a176662d766352d9af39619775a73d
  - prompt family contract 1.0.1 and lifecycle closeout merge 1affb3a094a06f2a250140e8173501b3a6938164
  - Surveyor accepted producer tree present at producer_commit
blocks: []
ownership_released: false
next_action: verify CI run 32644841268 SUCCESS on head 7e4c6435c3715b7e97d8b7827ca052cf33743cf8, then merge PR #663 and perform terminal archive closeout
---

# Control Center Package C — Surveyor read-only integration

## Objective

Implement one fail-closed Surveyor provider that validates the accepted output bundle and maps only proven information into existing Control Center `RuntimeStatus`, `GameSnapshot`, `Capability` and source-quality/readiness views. No official-client access or mutation is permitted.

## Preflight evidence

Fresh live state on trusted `main@1affb3a094a06f2a250140e8173501b3a6938164` found no existing Package C task/branch, no active task owning `tools/tests/tibia_re_control_center`, and no open PR touching those paths. Surveyor code/tests/workflow are byte-identical to accepted closeout anchor `815245ab3cac38a96f60f3ee3395b67f81b81c11` across the inspected tree.
## Acceptance inventory

- [x] 01 exact Surveyor producer/schema/interface pin persisted
- [x] 02 strict accepted schema/version validation refuses mismatch
- [x] 03 bounded path/manifest parsing rejects missing/corrupt/duplicate/unsafe input
- [x] 04 no traversal or unbounded bundle ingestion
- [x] 05 repository-only bundle yields truthful repository-only status
- [x] 06 synthetic live-shaped fixture maps runtime identity without mutation authority
- [x] 07 typed-reader fields map only through explicitly accepted schema fields
- [x] 08 missing typed readers yield explicit unavailable/unsupported quality
- [x] 09 stale/incompatible/missing provenance remains explicit and fail-closed
- [x] 10 normalized status separates runtime/client/authority/capability/evidence/freshness/session
- [x] 11 GameSnapshot unknown/stale fields stay unknown/stale
- [x] 12 capability projection cannot create action capability
- [x] 13 Surveyor evidence/canonical statuses remain immutable
- [x] 14 no Official Tibia mutation/runtime-control imports or calls
- [x] 15 no physical Surveyor collection required
- [x] 16 deterministic current-schema fixture regression coverage
- [x] 17 schema downgrade/upgrade mismatch fails closed
- [x] 18 malformed/partial/privacy-risk bundles fail closed without leakage
- [x] 19 Package A regression suite remains green
- [x] 20 repository-only producer -> provider -> normalized read-model E2E passes
- [ ] 21 exact-head CI and fresh independent Package C audit pass
- [ ] 22 task/PR terminal and ownership released

## Validation evidence

Implementation and repository-only E2E are complete on candidate head `7e4c6435c3715b7e97d8b7827ca052cf33743cf8`; independent exact-head audit PASS and zero unresolved review threads are recorded below. Final repository CI run `32644841268` remains in progress. All physical Official Tibia inputs remain intentionally unavailable/not requested under `runtime_access:none`.


## Recovery checkpoint — 2026-08-23 17:05 CEST

```yaml
checkpoint:
  status: waiting
  implementation_pr: 663
  final_candidate_head: 7e4c6435c3715b7e97d8b7827ca052cf33743cf8
  last_restacked_base: 762436c25433b7bb192e6014cb4e46afc58dfc4b
  current_main_observed: 56499ec5767093f69f09c581c54957714382e107
  current_main_overlap_with_package_c_files: false
  independent_audit: PASS
  audit_comment: 5386480934
  unresolved_review_threads: 0
  local_windows_control_center: 210_passed_2_skipped_125_subtests
  local_posix_hardening: 4_passed
  ruff: PASS
  diff_check: PASS
  package_a_exact_head_workflow: 32644841117_SUCCESS
  repository_ci_run: 32644841268_IN_PROGRESS
  pending_ci_jobs:
    - linux-tests Run CMake
    - linux-release Run CMake
  official_client_access: NONE
  mutation_authorized: false
  ownership_released: false
  next_action: verify CI run 32644841268 SUCCESS on exact head, then merge PR 663 and archive/release ownership
```
