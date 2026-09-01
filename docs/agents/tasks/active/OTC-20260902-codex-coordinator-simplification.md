---
task_id: OTC-20260902-codex-coordinator-simplification
status: validating
agent: ChatGPT
session_role: prompt_maintainer
project_lane: otclient
lane: AGENT-ORCHESTRATION
track_id: repository-governance
task_kind: documentation
phase: exact_head_validation
branch: docs/OTC-20260902-codex-coordinator-simplification
base_branch: main
base_sha: 154388feeb4057fed05ac3c5a1d5181a552e7f31
created: 2026-09-02T00:17:00+02:00
updated_at: 2026-09-02T00:29:32+02:00
risk: low
execution_class: local_owner_pc
execution_mode: remote_desktop_plus_github
preferred_execution: chat_github
execution_reason: simplify coordinator decision surface while retaining dispatcher-enforced cost guards
context_pressure: low
decomposition_decision: single
user_communication: low_noise
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: merge_then_archive
prompting_standard_version: 2.1
policy_version: 2
track_a_runtime_agent_admission_version: 1
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
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
worktree: C:/Users/barte/otclient-codex-coordinator-simplification
owned_paths:
  - docs/agents/tasks/active/OTC-20260902-codex-coordinator-simplification.md
  - docs/agents/reports/OTC-20260902-codex-coordinator-simplification.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_ALIASES.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_PROMPT_EVAL_V1.md
  - docs/agents/EXECUTION_PROTOCOL.md
modules_touched: []
depends_on:
  - merged Codex cost-control PR #849
  - merged cost-control closeout PR #850
blocks: []
cross_repository_task_ids: []
related_pr: 851
invocation_started_at: 2026-09-02T00:17:00+02:00
last_progress_at: 2026-09-02T00:29:32+02:00
ci_checks_for_current_head: 0
ci_check_generation: pr851-bound-pending
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
current_blocker: none
next_action: publish the PR-bound checkpoint, then require exact-head CI/governance, static prompt regression and clean review state before readiness/merge
---

# Codex coordinator simplification

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-02T00:28:26+02:00
head: 4d014bc0b6345ebc3c0dbb89c5cf7fe1a26385c0
head_semantics: validated_prompt_1_3_content_commit_before_pr_binding
branch: docs/OTC-20260902-codex-coordinator-simplification
pr: 851
status: validating
context_routes:
  - agent-governance
  - prompting-v2.1
  - codex-cost-control
owned_paths:
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_ALIASES.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_PROMPT_EVAL_V1.md
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/reports/OTC-20260902-codex-coordinator-simplification.md
  - docs/agents/tasks/active/OTC-20260902-codex-coordinator-simplification.md
proven:
  - prompt 1.2.0 retained cost guards but exposed too many bridge-internal details to the coordinator.
  - bounded dispatcher already enforces verified context, hard budgets, no CI wait/main chase and audit deduplication.
  - coordinator-specific execution text shrank from 618 words to 238 words (61.5% reduction) while retaining the same bridge guard authority.
derived:
  - coordinator prompt should expose only the small decision loop and delegate mechanical enforcement to the dispatcher.
unknown: []
conflicts: []
first_failure:
  marker: COORDINATOR_PROMPT_OVERCOMPLEX
  evidence: prompt 1.2.0 coordinator section mixed programme decisions with bridge implementation details.
rejected_hypotheses:
  - removing bridge guard details from the coordinator prompt requires removing the technical guards themselves.
changed_paths:
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_ALIASES.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_PROMPT_EVAL_V1.md
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/reports/OTC-20260902-codex-coordinator-simplification.md
  - docs/agents/tasks/active/OTC-20260902-codex-coordinator-simplification.md
validation:
  - command: python verify_coord_prompt_v13.py
    result: PASS
    evidence: prompt contract 1.3.0 with a six-step coordinator loop and dispatcher-owned mechanical guards.
  - command: python -m unittest test_codex_bridge.py -q
    result: PASS
    evidence: 33/33 bounded dispatcher regression tests pass; bridge safeguards remain enforced outside the coordinator prompt.
  - command: python -m py_compile otc_codex_dispatch.py
    result: PASS
    evidence: local dispatcher compiles cleanly.
  - command: checkpoint / Control Room / Track A governance / git diff --check
    result: PASS
    evidence: policy-v2 task, checkpoint valid, Track A governance green and no whitespace errors.
blockers: []
next_action: publish the PR-bound checkpoint, then require exact-head CI/governance, static prompt regression and clean review state before readiness/merge
```
