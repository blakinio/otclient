---
task_id: OTC-20260802-agent-governance-sync
status: implementing
branch: docs/OTC-20260802-agent-governance-sync
base_branch: main
created: 2026-08-02
updated: 2026-08-02
related_pr: ""
owned_paths:
  - AGENTS.override.md
  - docs/agents/AGENTS.md
  - docs/agents/ANTI_STALL_AND_EXECUTION_BUDGET.md
  - docs/agents/AUTONOMOUS_PROGRAM_CONTINUATION.md
  - docs/agents/DELIVERY_COMPLETENESS_AND_CLOSEOUT.md
  - docs/agents/GITHUB_ONLY_EXECUTION.md
  - docs/agents/GOVERNANCE_CONTRACT.json
  - docs/agents/CONTEXT_HANDOFF.md
  - docs/agents/tasks/TASK_TEMPLATE.md
required_reads:
  - AGENTS.md
  - docs/agents/CONTEXT_HANDOFF.md
  - docs/agents/ANTI_STALL_AND_EXECUTION_BUDGET.md
  - docs/agents/AUTONOMOUS_PROGRAM_CONTINUATION.md
search_first: []
optional_reads: []
---

# Synchronize shared agent governance

## Goal

Apply the backward-compatible portfolio governance correction without changing OTClient product code.

## Acceptance criteria

- Shared status, budget, validation, audit and authority semantics are internally consistent.
- Checkpoint validation accepts waiting/completed and NOT_APPLICABLE.
- Exact-head governance checks pass on the final PR head.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-02T12:33:00Z
head: UNKNOWN
branch: docs/OTC-20260802-agent-governance-sync
pr: none
status: implementing
context_routes:
  - agent-governance
owned_paths:
  - AGENTS.override.md
  - docs/agents/AGENTS.md
  - docs/agents/ANTI_STALL_AND_EXECUTION_BUDGET.md
  - docs/agents/AUTONOMOUS_PROGRAM_CONTINUATION.md
  - docs/agents/DELIVERY_COMPLETENESS_AND_CLOSEOUT.md
  - docs/agents/GITHUB_ONLY_EXECUTION.md
  - docs/agents/GOVERNANCE_CONTRACT.json
  - docs/agents/CONTEXT_HANDOFF.md
  - docs/agents/tasks/TASK_TEMPLATE.md
proven:
  - The current governance contract rejects waiting and completed checkpoint states.
  - The current task-count key conflicts with the documented next-task rule.
derived:
  - Additive accepted values preserve all existing version 1 checkpoints.
unknown:
  - Exact governance workflow results on the future PR head.
conflicts: []
first_failure:
  marker: none
  evidence: none
rejected_hypotheses: []
changed_paths:
  - docs/agents/tasks/active/OTC-20260802-agent-governance-sync.md
validation:
  - command: Agent Governance workflow
    result: NOT_RUN
    evidence: PR not yet opened
blockers: []
next_action: update the shared governance documents and portable checkpoint contract
```
