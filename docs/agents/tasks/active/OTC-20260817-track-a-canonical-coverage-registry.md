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
phase: canonical_registry_restack_after_xres_promotion
branch: docs/OTC-20260817-track-a-canonical-coverage-registry
base_branch: main
base_main: d9529da35ada6ab2a7bf4d2e70205cc0dd7b14ab
pr: 454
risk: medium
created: 2026-08-17T10:47:00+02:00
updated: 2026-08-17T10:57:00+02:00
invocation_started_at: 2026-08-17T10:47:00+02:00
last_progress_at: 2026-08-17T10:57:00+02:00
lease_expires_at: 2026-08-17T11:42:00+02:00
policy_version: 2
prompting_standard_version: 2.1
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
execution_mode: github-only
execution_reason: promote accepted #304 bounded registry and normalize current-main programme state without runtime access
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
decomposition_reason: one bounded current-main registry/data integration with deterministic validator and audit-report reconciliation
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
  - .github/workflows/tibia-official-client-re-coverage-registry.yml
modules_touched: []
reuses:
  - closed source Draft PR #304 exact head 43a60bd96cc644b656b200c9edbfb75578b330b6
  - coordinator disposition #304 comment 5302034228 ACCEPT_WITH_EDITS
  - merged coverage audit #451 / 2ad6565f6f598b15acaeb3d182a3ffb70d187ba6
  - source #304 baseline blobs and validator
depends_on: []
blocks:
  - AUD-COV-001
source_registry:
  pr: 304
  head: 43a60bd96cc644b656b200c9edbfb75578b330b6
  repository_ci_run: 31882010038
  disposition: ACCEPT_WITH_EDITS_BOUNDED_INVENTORY_ONLY
current_overlay:
  snapshot_main: d9529da35ada6ab2a7bf4d2e70205cc0dd7b14ab
  p2_promotion: cbc6388e8607bb92120281a9a15148577994d3a6
  worldmap_static_graph: f5daad1bbb7e00dcaa26acafc0a69d10a3a1b696
  worldmap_mutation_design: 1e6fcb5ab83c4bb8b762088326cc936857c8e64d
  raw_xres_promotion: d9529da35ada6ab2a7bf4d2e70205cc0dd7b14ab
  exact_resource_to_official_client_pid: UNKNOWN
acceptance:
  canonical_registry_on_main:
    - capabilities.jsonl
    - protocol_messages.jsonl
    - runtime_types.jsonl
  provenance_preserved: true
  unknown_disproven_superseded_preserved: true
  source_baseline_not_relabelled_as_semantic_completion: true
  current_main_overlay_present: true
  validator_present: true
  validator_fences_source_baseline_by_git_blob: true
  permanent_hosted_validation_workflow_present: true
  audit_cov_001_resolved_only_after_merge: true
  other_audit_findings_remain_open: true
  runtime_or_synology_use: forbidden
  owner_funded_ai_use: forbidden
validation_history:
  pre_xres_drift_head: 41986ab8965b634f25150f35565cd8b4e737f671
  pre_xres_drift_registry_run: 32012965642
  pre_xres_drift_repository_ci_run: 32012965784
  pre_xres_drift_governance_run: 32012965633
  invalidated_by_main_advance: d9529da35ada6ab2a7bf4d2e70205cc0dd7b14ab
ci_checks_for_current_head: 0
ci_check_generation: implementation-restack
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
last_completed_step: consumed merged raw-XRes helper #448 and advanced AUD-COV-004 next discriminator to separately admitted physical XID-to-PID identity without altering its HIGH/open classification
next_action: restack candidate on main@d9529da3, run deterministic registry/governance/repository CI, then perform fresh independent audit and terminal closeout
---

# Track A canonical coverage registry promotion

This task closes only `AUD-COV-001`. The accepted #304 baseline is byte-for-byte fenced; current programme state is a separate overlay. E51/E52, P0/P1 item-level denominators, 612-vs-1004 reconciliation and physical runtime semantics remain outside this task.
