---
task_id: OTC-20260817-track-a-canonical-coverage-registry
status: implementing
agent: ChatGPT
session_id: chatgpt-canonical-coverage-registry-20260817
session_role: implementation_and_integration
project_lane: otclient
lane: COVERAGE-AUDIT
track_id: official-client-re
task_kind: implementation
phase: canonicalize_accepted_registry
branch: docs/OTC-20260817-track-a-canonical-coverage-registry
base_branch: main
base_main: 2ad6565f6f598b15acaeb3d182a3ffb70d187ba6
risk: medium
created: 2026-08-17T10:47:00+02:00
updated: 2026-08-17T10:47:00+02:00
invocation_started_at: 2026-08-17T10:47:00+02:00
last_progress_at: 2026-08-17T10:47:00+02:00
lease_expires_at: 2026-08-17T11:32:00+02:00
policy_version: 2
prompting_standard_version: 2.1
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
execution_mode: github-only
execution_reason: accepted PR #304 registry package can be promoted and normalized from current main using repository/GitHub data only
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
persistent_session_role: none
physical_e2e_required: false
owner_funded_ai_api_authorized: false
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one bounded current-main data package promotion with validator, audit-report reconciliation, and terminal closeout
validation_level: component
implementation_authorized: true
feature_scope:
  type: data_pipeline
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: internal_only
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-canonical-coverage-registry.md
  - docs/agents/tasks/archive/OTC-20260817-track-a-canonical-coverage-registry.md
  - docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/**
  - docs/agents/reports/OTCLIENT-20260816-track-a-coverage-audit-refresh.md
modules_touched: []
reuses:
  - closed source Draft PR #304 exact head 43a60bd96cc644b656b200c9edbfb75578b330b6
  - coordinator disposition #304 comment 5302034228 ACCEPT_WITH_EDITS
  - merged coverage audit #451 / main 2ad6565f6f598b15acaeb3d182a3ffb70d187ba6
  - source validator docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/validate_registry.py
depends_on: []
blocks:
  - AUD-COV-001
source_registry:
  pr: 304
  head: 43a60bd96cc644b656b200c9edbfb75578b330b6
  repository_ci_run: 31882010038
  disposition: ACCEPT_WITH_EDITS_BOUNDED_INVENTORY_ONLY
acceptance:
  canonical_registry_on_main:
    - capabilities.jsonl
    - protocol_messages.jsonl
    - runtime_types.jsonl
  provenance_preserved: true
  unknown_disproven_superseded_preserved: true
  source_baseline_not_relabelled_as_semantic_completion: true
  current_main_overlay_required: true
  validator_required: true
  validator_must_fence_source_baseline: true
  audit_cov_001_resolved_only_after_merge: true
  other_audit_findings_must_remain_open: true
  runtime_or_synology_use: forbidden
  owner_funded_ai_use: forbidden
ci_checks_for_current_head: 0
ci_check_generation: implementation
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
last_completed_step: fresh ownership/uniqueness/admission preflight selected accepted #304 as the sole bounded source for closing AUD-COV-001
next_action: promote the accepted #304 machine-readable registry package, add a current-main manifest/overlay and validator fences, reconcile the coverage audit report, then run independent validation
---

# Track A canonical coverage registry promotion

This task closes only `AUD-COV-001`: absence of the accepted machine-readable coverage registry from trusted `main`.

It must preserve the #304 bounded evidence/provenance boundary. It does not complete E51/E52, normalize the unresolved P0/P1 semantic denominators, resolve the 612-vs-1004 QMeta denominator conflict, or prove canonical live runtime semantics.
