---
task_id: OTC-20260802-anti-stall-budget-v1
status: validating
agent: "GPT-5.6 Thinking"
track: agent-governance
workstream: anti-stall-budget
parallel_wave: GOVERNANCE-V1
parallel_lane: ANTI-STALL
parallel_lane_state: validating
branch: docs/anti-stall-budget-v1-20260802
base_branch: main
created: 2026-08-02T10:29:00+02:00
updated: 2026-08-02T10:42:00+02:00
related_pr: "#168"
risk: low
owned_paths:
  - AGENTS.override.md
  - docs/agents/AGENTS.md
  - docs/agents/ANTI_STALL_AND_EXECUTION_BUDGET.md
  - docs/agents/tasks/active/OTC-20260802-anti-stall-budget-v1.md
---

# Anti-stall and execution budget v1

## Goal

Prevent autonomous agents from becoming unbounded polling, retry, repair, or task-selection loops while preserving client, protocol, asset and repository safety.

## Acceptance

- [x] Add the normative anti-stall contract.
- [x] Require it from the automatically loaded root bootstrap.
- [x] Route local execution through it.
- [x] Limit CI checks, unchanged states, identical failures, repair cycles, context reconstruction, command duration, runtime and no-progress time.
- [ ] Pass exact-head required CI.
- [ ] Merge and archive.

## Context checkpoint

```yaml
checkpoint_version: 1
policy_version: 2
updated_at: 2026-08-02T10:42:00+02:00
head: a62d3cfdc000382cc63c45f13c3ab8aec270dccb
branch: docs/anti-stall-budget-v1-20260802
pr: 168
status: validating
phase: validate
session_id: chat-20260802-anti-stall-budget-v1
session_role: coordinator
execution_mode: chat-github
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_routes:
  - agent-governance
owned_paths:
  - AGENTS.override.md
  - docs/agents/AGENTS.md
  - docs/agents/ANTI_STALL_AND_EXECUTION_BUDGET.md
  - docs/agents/tasks/active/OTC-20260802-anti-stall-budget-v1.md
proven:
  - Root and local routing require the anti-stall contract before long-running or autonomous work.
  - The policy preserves client, protocol, asset and production restrictions.
derived:
  - Pending CI can no longer justify indefinite polling in one invocation.
unknown:
  - Exact-head required CI after this checkpoint update.
conflicts: []
first_failure:
  marker: none
  evidence: no implementation-gate failure observed
rejected_hypotheses:
  - autonomous continuation permits unlimited retries
changed_paths:
  - AGENTS.override.md
  - docs/agents/AGENTS.md
  - docs/agents/ANTI_STALL_AND_EXECUTION_BUDGET.md
  - docs/agents/tasks/active/OTC-20260802-anti-stall-budget-v1.md
validation: []
blockers: []
invocation_started_at: 2026-08-02T10:29:00+02:00
last_progress_at: 2026-08-02T10:42:00+02:00
runtime_limit_minutes: 60
no_progress_minutes: 15
ci_checks_for_current_head: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
next_action: verify exact-head required CI for PR 168
```
