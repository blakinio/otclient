---
task_id: OTC-20260816-beclient-findings-persistence
status: validating
agent: ChatGPT
session_id: chatgpt-beclient-findings-persistence-20260816
session_role: author
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: documentation
phase: validate
branch: docs/OTC-20260816-beclient-findings-persistence
base_branch: main
base_main: c4b1919e16fb2931c74f32cb310229703dbf893c
risk: low
related_pr: 333
updated: 2026-08-16T10:54:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-beclient-findings-persistence.md
  - docs/agents/reports/OTCLIENT-20260816-beclient-static-integration.md
modules_touched: []
reuses:
  - closed PR #326 BattlEye package-presence evidence
  - closed PR #327 BEClient.so static ELF/layout evidence
  - closed PR #330 exact-client QLibrary/Init ABI evidence
  - closed PR #332 exact client-side Init output/callback lifecycle evidence
depends_on: []
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
context_pressure: low
context_growth: stable
context_score: 4
estimate_confidence: high
decomposition_decision: single
decomposition_reason: documentation-only consolidation of already collected and validated exact-build evidence
validation_level: exact_head_pending_after_restack
heavy_validation_runs: 0
ci_checks_for_current_head: 0
ci_check_generation: ready
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
track_a_runtime_agent_admission_version: 1
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
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runtime_platform: official_native_linux_only
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
audit:
  result: PASS_AFTER_WORDING_REMEDIATION
  method: source-provenance cross-check against closed PR #326/#327/#330/#332 plus prior deterministic exact-byte validator 31935419481/95136403149
  material_findings_open: 0
  remediation:
    - downgraded QLibrary-to-BEClient concrete filename linkage from direct fact to high-confidence DERIVED because setFileName QString remains unresolved
    - removed intent attribution from unconventional .be0/.be1 mapping description
    - separated proven 32-byte region/calls from derived output-interface interpretation
e2e:
  result: NOT_APPLICABLE
  reason: documentation-only consolidation; no executable/runtime behavior changed
final_ci:
  result: PENDING_ON_RESTACKED_PR_HEAD
next_action: verify exact-head required checks after restack; when green and branch current, merge PR #333 through protection, then archive the task and release ownership in post-merge closeout
---

# Objective

Persist the already-established static findings about `BEClient.so` and the exact official Linux Tibia client integration into `main`, so future Track A workers do not need to reconstruct the evidence from closed diagnostic PRs.

# Safety boundary

Documentation only. No Tibia/BattlEye execution, runtime observation, live process access, attach/debug/injection, binary modification, network probing, anti-debug research, anti-cheat bypass/evasion, credentials, session mutation, or proprietary binary redistribution.

# Acceptance

- consolidate the exact client and `BEClient.so` fences;
- record the proven/derived role and loader lifecycle of `BEClient.so` without overstating unresolved filename flow;
- record the strongest safe static ELF/self-loader facts;
- record the `Init` call shape and client-side output/callback layout;
- preserve corrections and explicit `UNKNOWN` items;
- cite exact source PRs/runs/jobs;
- keep the report descriptive and non-operational with respect to anti-cheat internals;
- perform proportionate docs-only audit and exact-head repository validation before terminal closeout.
