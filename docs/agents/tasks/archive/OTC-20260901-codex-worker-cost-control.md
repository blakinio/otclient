---
task_id: OTC-20260901-codex-worker-cost-control
status: completed
agent: ChatGPT
session_role: closeout
project_lane: otclient
lane: AGENT-ORCHESTRATION
track_id: repository-governance
task_kind: documentation
phase: close
source_branch: docs/OTC-20260901-codex-cost-control
archive_branch: docs/OTC-20260901-codex-cost-control-closeout
branch: docs/OTC-20260901-codex-cost-control-closeout
base_branch: main
base_sha: 427a9e3ddca0f2c184b75741fb9b067a8a6520e5
created: 2026-09-01T23:48:30+02:00
updated_at: 2026-09-02T00:07:38+02:00
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
owned_paths: []
modules_touched: []
depends_on:
  - merged Codex model/effort benchmark PR #841
  - merged coordinator-managed dispatch prompt PR #844
blocks: []
cross_repository_task_ids: []
related_pr: 849
implementation_pr: 849
archive_pr: null
implementation_final_head: efce79ad26b1b2b85579f4b07ff10fd57b4a22cc
implementation_merge: 6c21ef021875aab15663505629b6e72655b1fcf1
merged_at: 2026-09-01T22:07:12Z
ownership_released: true
invocation_started_at: 2026-09-01T23:48:30+02:00
last_progress_at: 2026-09-02T00:07:38+02:00
ci_checks_for_current_head: 2
ci_check_generation: final-green-efce79ad26b1
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
audit_result: PASS
audit_evidence: deterministic prompt-contract 1.2.0 readback, 8-path scope, local dispatcher 33/33 tests, zero GitHub review findings
e2e_result: NOT_APPLICABLE
e2e_reason: documentation/prompt/execution-policy hardening only; no product/runtime/input/credential behavior changed
current_blocker: none
next_action: publish and merge the lifecycle-only archive PR, then no follow-up is required
---

# Codex worker cost-control guard

## Objective

Persist the measured root causes of the 2026-09-01 coordinator token burn and make the safe execution path fail closed: bounded bridge first, no Codex for coordination-only work, no worker CI polling/main chasing, exact-head audit deduplication, final-confidence-only second opinions, and no quota-driven provider spillover.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-02T00:07:38+02:00
head: 6c21ef021875aab15663505629b6e72655b1fcf1
head_semantics: merged_implementation_main_before_archive_commit
branch: docs/OTC-20260901-codex-cost-control-closeout
pr: 849
status: completed
context_routes:
  - agent-governance
  - codex-model-routing
  - vision-p2-coordination
  - execution-budget
owned_paths: []
proven:
  - PR #849 final exact head efce79ad26b1b2b85579f4b07ff10fd57b4a22cc passed CI 33564501009 and Track A governance 33564500676 with zero review threads/reviews and behind=0.
  - PR #849 squash-merged as 6c21ef021875aab15663505629b6e72655b1fcf1.
  - PR #849 exact head 2f29896a989e655cfaf900fd5d19b9bc222f535e passed CI run 33564319173 and Track A governance run 33564319040 with zero review threads/reviews and behind=0 from main.
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
  - docs/agents/tasks/archive/OTC-20260901-codex-worker-cost-control.md
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
next_action: publish and merge the lifecycle-only archive PR, then no follow-up is required
```
