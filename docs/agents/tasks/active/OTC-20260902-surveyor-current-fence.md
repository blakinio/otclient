---
task_id: OTC-20260902-surveyor-current-fence
status: validating
agent: ChatGPT
session_role: implementer
worker_alias: OTC-SURVEYOR-CURRENT-FENCE
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: bugfix
phase: wave_3_execution_path_repair
branch: fix/OTC-20260902-surveyor-current-fence
base_branch: main
base_main: a7c7eb8aa2cc69d70442578401d88be9262055e4
pr: null
created: 2026-09-02T20:16:06+02:00
updated_at: 2026-09-02T20:16:06+02:00
risk: medium
execution_class: repository_only
execution_mode: chat
execution_reason: advance existing owner-gated read-only Surveyor workflow to the canonical current-client fence without changing its authority
context_pressure: low
context_growth: stable
context_score: 2
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one stale workflow fence plus one focused regression guard
continuation_policy: continue_until_real_stop
task_completion_policy: return_to_coordinator_for_classification
policy_version: 2
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
implementation_authorized: true
mutation_authorized: false
credentials_allowed: false
login_allowed: false
relogin_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
anti_idle_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
process_memory_access_allowed: false
physical_action_budget: 0
physical_action_count: 0
owner_funded_ai_api_authorized: false
red_head: e0d3379e900e2d039825eb0ff3cc3a25cfa7ab7e
implementation_head: cc4b09307b03c4cdc583a48ff225152fb034a2c1
owned_paths:
  - .github/workflows/track-a-surveyor-v2-readonly.yml
  - tests/tools/tibia_re_surveyor/test_operator_semantics.py
  - docs/agents/tasks/active/OTC-20260902-surveyor-current-fence.md
  - .github/workflows/tibia-re-control-center-core.yml
current_blocker: package_a_exact_exception_pending
next_action: validate the exact PR-bound Package A exception and all Surveyor/current-fence/governance tests
---

# Objective

Advance the existing owner-gated `Track A Surveyor v2 read-only` workflow to the canonical current official Linux client fence `15.32.be4f48 / 52105824 / 552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`.

# Frozen scope

- Change only the Surveyor workflow's exact expected client size/SHA.
- Add one focused regression guard requiring the current fence and rejecting the superseded fence in this workflow.
- Preserve read-only authority, owner gate, zero credential access, zero GUI input, zero process control and zero semantic promotion.
- Do not change Surveyor runtime code, capture code, Qwen, transport or reconciliation behavior.
- Keep any Package A exception exact to this task, branch, base, repository and the three repair-owned paths.

# Acceptance

1. Focused test is RED on the stale Surveyor fence and GREEN after the two-value workflow update.
2. Full Surveyor tests and canonical current-client fence tests pass.
3. Track A governance, YAML parse, compile and diff-check pass.
4. Package A exact case passes while wrong branch, wrong base and fork cases fail closed.
5. No runtime observation occurs in this repair task; direct Codex usage remains zero.
