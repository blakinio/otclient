---
task_id: OTC-20260904-be4f48-sendlogin-adapter-semantics
status: implementing
agent: Codex
session_id: login-closure-20260904-ae070f034ee4
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: implementation
phase: implement
branch: ai/OTC-20260904-be4f48-sendlogin-adapter-semantics
base_branch: main
base_main: 04a4ca71b658dcc374aaf40dbb8135de43d49cb7
created: 2026-09-04T22:06:00Z
updated_at: 2026-09-04T22:06:00Z
invocation_started_at: 2026-09-04T22:06:00Z
last_progress_at: 2026-09-04T22:06:00Z
policy_version: 2
prompting_standard_version: 2.1
execution_mode: codex
execution_reason: isolated checkout and deterministic local tests; exact client qualification on GitHub-hosted runner
execution_class: github_hosted
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
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
implementation_authorized: true
feature_scope:
  type: contract_producer
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one connection construction and one adapter/member boundary
foreground_runtime_budget_minutes: 120
foreground_budget_reason: explicit sequential source qualification and clean promotion/archive programme
ci_checks_for_current_head: 0
ci_check_generation: red
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
owned_paths:
  - tools/tibia_re_be4f48_sendlogin_adapter_semantics/**
  - .github/workflows/tibia-re-be4f48-sendlogin-adapter-semantics.yml
  - docs/agents/tasks/active/OTC-20260904-be4f48-sendlogin-adapter-semantics.md
  - docs/agents/evidence/OTC-20260904-be4f48-sendlogin-adapter-semantics/**
modules_touched: []
reuses:
  - docs/agents/prompts/OTC_BE4F48_SENDLOGIN_ADAPTER_BD3050_RECEIVER_SEMANTICS.md
  - docs/agents/evidence/OTC-20260904-be4f48-post899-900-promotion/result.json
  - PR 899 transient hosted qualification pattern (not its consumed type scan)
depends_on: []
blocks:
  - clean coordinator consumption of this exact source result
cross_repository_task_ids: []
ownership_released: false
next_action: qualify bounded dataflow on exact client; complete QSlot and adapter control-flow analysis before any source terminal claim
---

# Objective and authority

Execute `OTC-BE4F48-SENDLOGIN-ADAPTER-BD3050-RECEIVER-SEMANTICS`.
Only inspect the exact connection construction at 0x7c6b9f, its QSlot callable,
adapter 0xbd3050, and at most one unique identity-preserving adapter member edge.
No owner/caller/global census. Source PR stays Draft and never self-merges.

# Acceptance

- Behavioral synthetic tests reject missing, ambiguous and clobbered provenance.
- Exact version/size/SHA fence precedes source analysis.
- Determine invocation ABI and receiver/member binding only from exact evidence.
- Preserve UNKNOWN for unproven class identity, Field6, order and final writer.
- Deterministic sanitized JSON; no raw client bytes in logs, Git or artifacts.
- Fresh whole-diff falsification and exact-head focused/CI/governance/boundary checks.
- Independent clean docs-only promotion, close source unmerged, separate archive.

# FACT

Live main 04a4ca71b658dcc374aaf40dbb8135de43d49cb7.
Track B #284 remains Draft at 62383aded3acbeb5f405a12fe1f93849cd8e35f9.
No open PR for either new alias in the authenticated PR listing.
Current manifest: 15.32.be4f48 / 52105824 /
552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1.

# UNKNOWN

Receiver class, complete causal binding, final writer, Field6 value,
pre-success ordering and safe Track B delta remain unproven.

# Safety

runtime_access=none; official_client_executed=false; login_performed=false;
credentials_used=false; process_memory_access=false; packet_capture=false;
ocr_vision_used=false; official_service_e2e_count=0; track_b_pr_284_modified=false.
E2E NOT_APPLICABLE for this static producer: official-client execution is forbidden.

# Recovery checkpoint

Resume the existing source task and branch after rechecking live ownership and exact head.
No source result or programme completion is claimed.

Repository-only RED: five expected failures at 1e5ceb8e45cd74220fe5500e57c8d85266ed5820 because analyzer was absent. Local minimal GREEN: five behavioral tests pass. Initial dataflow probe intentionally reports ANALYSIS_INCOMPLETE, never SOURCE_BLOCKER; full source semantics remain to implement. No client bytes materialized locally.
