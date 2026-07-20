---
task_id: OTC-20260720-agent-handoff-core
status: implementing
branch: docs/agent-handoff-core-20260720
base_branch: main
created: 2026-07-20
updated: 2026-07-20
related_pr: "13"
owned_paths:
  - docs/agents/CONTEXT_HANDOFF.md
  - docs/agents/GOVERNANCE_CONTRACT.json
  - docs/agents/tasks/TASK_TEMPLATE.md
  - docs/agents/tasks/active/OTC-20260720-agent-handoff-core.md
  - tools/agents/checkpoint.py
  - tools/agents/resume.py
  - tools/agents/test_checkpoint_resume.py
---

# Portable checkpoint resume workflow

## Goal

Add a compact durable handoff mechanism so a new agent can resume from repository state without receiving the previous chat transcript.

## Acceptance criteria

- checkpoint contract v1 is documented and machine-readable;
- checkpoints have deterministic structural validation and compactness ceilings;
- `resume.py` emits a bounded continuation prompt with one concrete next action;
- task template and handoff documentation describe the workflow;
- no runtime, protocol, asset, gameplay or upstream changes;
- PR merges only after required exact-head checks pass.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-07-20T13:40:00Z
head: ae87a3a00f14700e9d8d1930d9ef26e167881389
branch: docs/agent-handoff-core-20260720
pr: 13
status: validating
context_routes:
  - agent-governance
owned_paths:
  - docs/agents/CONTEXT_HANDOFF.md
  - docs/agents/GOVERNANCE_CONTRACT.json
  - docs/agents/tasks/TASK_TEMPLATE.md
  - docs/agents/tasks/active/OTC-20260720-agent-handoff-core.md
  - tools/agents/checkpoint.py
  - tools/agents/resume.py
  - tools/agents/test_checkpoint_resume.py
proven:
  - Branch changes are limited to agent governance and tooling paths.
  - The portable validator and resume design passed representative local compile and smoke tests before repository rollout.
derived:
  - The new continuation path can replace long chat handovers when the checkpoint is kept current.
unknown:
  - Required GitHub checks on the final PR head are not yet verified.
conflicts: []
first_failure:
  marker: none
  evidence: none
rejected_hypotheses: []
changed_paths:
  - docs/agents/CONTEXT_HANDOFF.md
  - docs/agents/GOVERNANCE_CONTRACT.json
  - docs/agents/tasks/TASK_TEMPLATE.md
  - docs/agents/tasks/active/OTC-20260720-agent-handoff-core.md
  - tools/agents/checkpoint.py
  - tools/agents/resume.py
  - tools/agents/test_checkpoint_resume.py
validation:
  - command: representative portable-core compile and smoke tests
    result: PASS
    evidence: local pre-rollout validation
blockers: []
next_action: Verify the updated PR head, required CI checks, review state and changed-file scope, then merge only if the repository merge gate passes.
```
