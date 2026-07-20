---
task_id: OTC-20260720-agent-required-reads
status: implementing
branch: docs/agent-required-reads-20260720
base_branch: main
created: 2026-07-20
updated: 2026-07-20
related_pr: ""
owned_paths:
  - docs/agents/tasks/TASK_TEMPLATE.md
  - docs/agents/tasks/active/OTC-20260720-agent-required-reads.md
  - tools/agents/resume.py
required_reads:
  - AGENTS.md
  - docs/agents/CONTEXT_HANDOFF.md
search_first: []
optional_reads: []
---

# Add required-read routing to compact resume

## Goal

Make compact continuation prompts carry task-specific architecture and contract reads without copying those documents into the handover.

## Acceptance criteria

- task metadata supports `required_reads`, `search_first`, and `optional_reads`;
- resume output emits those sections before evidence and `NEXT_ACTION`;
- `AGENTS.md` and `CONTEXT_HANDOFF.md` are default required reads;
- old task records without routing metadata continue to work through the default fallback;
- no client runtime, protocol, Lua, assets, or build behavior changes.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-07-20T19:20:00+02:00
head: db50a327a70f9902d4018a3b87f1a144b9d4c70a
branch: docs/agent-required-reads-20260720
pr: none
status: implementing
context_routes:
  - agent-governance
owned_paths:
  - docs/agents/tasks/TASK_TEMPLATE.md
  - docs/agents/tasks/active/OTC-20260720-agent-required-reads.md
  - tools/agents/resume.py
proven:
  - Existing portable resume carried checkpoint evidence but did not emit required architecture or contract reads.
  - Task template already had stable frontmatter suitable for portable read-routing metadata.
derived:
  - Keeping read routing in task frontmatter avoids changing checkpoint schema and preserves compatibility with existing active checkpoints.
unknown:
  - Final exact-head CI outcome.
conflicts: []
first_failure:
  marker: none
  evidence: none
rejected_hypotheses: []
changed_paths:
  - docs/agents/tasks/TASK_TEMPLATE.md
  - docs/agents/tasks/active/OTC-20260720-agent-required-reads.md
  - tools/agents/resume.py
validation:
  - command: changed-file design audit
    result: PASS
    evidence: rollout is limited to agent handoff tooling and templates
blockers: []
next_action: Open the draft PR, verify exact-head CI and changed-file scope, then merge only if repository gates pass.
```
