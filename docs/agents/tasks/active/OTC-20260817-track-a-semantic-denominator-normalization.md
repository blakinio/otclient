---
task_id: OTC-20260817-track-a-semantic-denominator-normalization
status: implementing
agent: ChatGPT
session_id: chatgpt-semantic-denominator-20260817
session_role: coverage_integration_coordinator
project_lane: otclient
lane: COVERAGE-AUDIT
track_id: official-client-re
task_kind: implementation
phase: normalize_denominators
branch: docs/OTC-20260817-track-a-semantic-denominator-normalization
base_branch: main
base_main: c55e3523e6e9d50df511e65dce9145a8f951a5f5
risk: medium
created: 2026-08-17T11:45:00+02:00
updated: 2026-08-17T11:45:00+02:00
invocation_started_at: 2026-08-17T11:38:00+02:00
last_progress_at: 2026-08-17T11:45:00+02:00
lease_expires_at: 2026-08-17T12:30:00+02:00
policy_version: 2
prompting_standard_version: 2.1
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
execution_mode: github-only
execution_reason: canonical coverage registry is on main and all remaining denominator work is deterministic repository/evidence normalization
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
context_pressure: high
context_growth: stable
context_score: 10
estimate_confidence: medium
decomposition_decision: phased
decomposition_reason: one finding requires four related finite denominator registries sharing the same canonical source/provenance and validator
feature_scope:
  type: data_pipeline
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: internal_only
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-semantic-denominator-normalization.md
  - docs/agents/tasks/archive/OTC-20260817-track-a-semantic-denominator-normalization.md
  - docs/agents/evidence/OTC-20260817-track-a-semantic-denominator-normalization/**
  - docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/protocol_message_semantics.jsonl
  - docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/runtime_type_semantics.jsonl
  - docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/p0_items.jsonl
  - docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/p1_items.jsonl
  - docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/coverage-summary.json
  - docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/current-main-overlay.json
  - docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/validate_registry.py
  - docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/README.md
  - docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/blockers.json
  - docs/agents/reports/OTCLIENT-20260816-track-a-coverage-audit-refresh.md
modules_touched: []
reuses:
  - canonical coverage registry merged by PR #454 and closeout correction #456
  - exact #304 bounded baseline retained byte-for-byte
  - physical XRes identity PR #457 and archive #459 as current RUNTIME input only
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_CENSUS_EXTENSION.md
blocks:
  - AUD-COV-002
acceptance:
  e51:
    denominator: 349
    every_protocol_identifier_itemized: true
    every_item_has_family: true
    every_item_has_semantic_state: true
    unknown_or_unclassified_allowed: true
    assumptions_forbidden: true
  e52:
    finite_runtime_type_denominator_required: true
    every_item_has_scope_decision: true
    ignored_with_reason_allowed: true
    unknown_or_unclassified_allowed: true
  p0:
    finite_item_level_read_action_denominator_required: true
    top_level_16_groups_not_used_as_item_denominator: true
  p1:
    finite_item_level_field_evidence_denominator_required: true
    seven_bridge_discovery_targets_not_used_as_global_denominator: true
  canonical:
    immutable_source_blobs_unchanged: true
    deterministic_validator_required: true
    inventory_completion_not_semantic_completion: true
    AUD-COV-002_resolved_only_if_all_four_denominators_materialized: true
    AUD-COV-003_004_007_not_silently_closed: true
validation:
  focused: pending
  component: pending
  audit: pending
  e2e:
    result: NOT_APPLICABLE
    reason: deterministic repository coverage/denominator normalization; no runtime or user-facing behavior
ci_checks_for_current_head: 0
ci_check_generation: implementation
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
additional_task_allowance_consumed: true
last_completed_step: fresh uniqueness check found no existing E51/E52/AUD-COV-002 owner; claimed one phased current-main task
next_action: derive four finite canonical denominator registries from current trusted repository evidence with explicit UNKNOWN/UNCLASSIFIED retention, extend the validator, then independently audit the resulting coverage accounting
---

# Track A semantic denominator normalization

This task resolves only the missing-denominator portion of `AUD-COV-002`. A complete denominator is not a claim that every item is semantically proven: uncertain records remain explicitly `UNKNOWN` or `UNCLASSIFIED` with provenance and a concrete follow-up where available.
