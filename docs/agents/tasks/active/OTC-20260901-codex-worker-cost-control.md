---
task_id: OTC-20260901-codex-worker-cost-control
status: validating
agent: ChatGPT
session_role: coordinator_cost_guard_maintainer
project_lane: otclient
lane: AGENT-ORCHESTRATION
track_id: repository-governance
task_kind: documentation
phase: exact_head_validation
branch: docs/OTC-20260901-codex-cost-control
base_branch: main
base_sha: 427a9e3ddca0f2c184b75741fb9b067a8a6520e5
created: 2026-09-01T23:48:30+02:00
updated_at: 2026-09-01T23:59:11+02:00
risk: low
execution_class: local_owner_pc
execution_mode: remote_desktop_plus_github
preferred_execution: chat_github
execution_reason: persist measured Codex token-burn root causes and enforce bounded coordinator dispatch
context_pressure: medium
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
worktree: C:/Users/barte/otclient-codex-cost-control
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-codex-worker-cost-control.md
  - docs/agents/reports/OTC-20260901-codex-worker-cost-control.md
  - docs/agents/evidence/OTC-20260901-codex-worker-cost-control/observed-burn.json
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_ALIASES.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_PROMPT_EVAL_V1.md
modules_touched: []
depends_on:
  - merged Codex model/effort benchmark PR #841
  - merged coordinator-managed dispatch prompt PR #844
blocks: []
cross_repository_task_ids: []
invocation_started_at: 2026-09-01T23:48:30+02:00
last_progress_at: 2026-09-01T23:59:11+02:00
ci_checks_for_current_head: 0
ci_check_generation: current-main-restacked-d1d30ca45aad
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
current_blocker: none
next_action: commit and publish the validated prompt-contract 1.2.0 content, open a Draft PR, then require exact-head CI/governance and PR hygiene before merge
---

# Codex worker cost-control guard

## Objective

Persist the measured root causes of the 2026-09-01 coordinator token burn and make the safe execution path fail closed: bounded bridge first, no Codex for coordination-only work, no worker CI polling/main chasing, exact-head audit deduplication, final-confidence-only second opinions, and no quota-driven provider spillover.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T23:59:11+02:00
head: d1d30ca45aad70c918eee7db759428dd50da59b2
head_semantics: cost_control_content_commit_after_current_main_restack
branch: docs/OTC-20260901-codex-cost-control
pr: null
status: validating
context_routes:
  - agent-governance
  - codex-model-routing
  - vision-p2-coordination
  - execution-budget
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-codex-worker-cost-control.md
  - docs/agents/reports/OTC-20260901-codex-worker-cost-control.md
  - docs/agents/evidence/OTC-20260901-codex-worker-cost-control/observed-burn.json
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_ALIASES.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_PROMPT_EVAL_V1.md
proven:
  - direct Codex executions bypassed the local bounded dispatcher, verified GitHub snapshot and context budget.
  - an edge-transport Terra/high session repeatedly waited for CI and exceeded 23 million cumulative context tokens while the primary Codex rate-limit telemetry reached 94 percent used.
  - the same exact edge-transport head received two Sol/medium audits before material head change.
  - quota pressure triggered Spark worker substitution and the Spark five-hour primary limit reached 100 percent.
derived:
  - coordination-only waiting/status/restack work must never consume a Codex worker.
  - same-head audit generations require durable deduplication and explicit different-model final-confidence semantics.
unknown:
  - whether future non-safety implementation benchmarks change the preferred model/effort frontier.
conflicts: []
first_failure:
  marker: resolved
  evidence: prompt contract 1.2.0 and the hardened owner-PC dispatcher now make those direct wait/restack/duplicate paths fail closed.
rejected_hypotheses:
  - higher model effort is the primary cause of the observed burn; the dominant cause was orchestration/context replay outside the bounded bridge.
  - provider quota pressure alone justifies switching to Spark or another owner-funded model.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-codex-worker-cost-control.md
  - docs/agents/reports/OTC-20260901-codex-worker-cost-control.md
  - docs/agents/evidence/OTC-20260901-codex-worker-cost-control/observed-burn.json
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_ALIASES.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_PROMPT_EVAL_V1.md
validation:
  - command: python verify_coord_prompt_v12.py
    result: PASS
    evidence: prompt contract 1.2.0, exactly eight aliases, and cost scenarios P2-E31..P2-E38 are present.
  - command: python -m json.tool observed-burn.json
    result: PASS
    evidence: summarized owner-PC burn evidence parses as JSON.
  - command: python tools/agents/checkpoint.py <task> --require-checkpoint
    result: PASS
    evidence: required context checkpoint validates.
  - command: git diff --check
    result: PASS
    evidence: candidate documentation/prompt delta has no whitespace errors.
  - command: python tools/agents/control_room.py --format markdown
    result: PASS
    evidence: task is recognized as policy-v2 documentation work.
  - command: Track A runtime governance changed-from 427a9e3ddca0f2c184b75741fb9b067a8a6520e5
    result: PASS
    evidence: TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true.
blockers: []
next_action: commit and publish the validated prompt-contract 1.2.0 content, open a Draft PR, then require exact-head CI/governance and PR hygiene before merge
```
