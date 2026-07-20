---
task_id: OTC-20260720-agent-required-reads
status: validating
branch: docs/agent-required-reads-20260720
base_branch: main
created: 2026-07-20
updated: 2026-07-20
related_pr: "15"
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
updated_at: 2026-07-20T19:24:00+02:00
head: 4749055d7eb9938d6b145e57fcda0d398b67f503
branch: docs/agent-required-reads-20260720
pr: 15
status: validating
context_routes:
  - agent-governance
owned_paths:
  - docs/agents/tasks/TASK_TEMPLATE.md
  - docs/agents/tasks/active/OTC-20260720-agent-required-reads.md
  - tools/agents/resume.py
proven:
  - Existing portable resume carried checkpoint evidence but did not emit required architecture or contract reads.
  - Task template frontmatter now carries required_reads search_first and optional_reads without changing checkpoint schema.
  - Draft PR 15 is open against main and contains only agent handoff tooling and task metadata paths.
derived:
  - Existing active checkpoints remain compatible because missing routing metadata falls back to AGENTS.md and CONTEXT_HANDOFF.md.
unknown:
  - Final exact-head CI outcome after this checkpoint update.
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
next_action: Verify PR 15 exact-head CI, mergeability, review state and changed-file scope, then merge only if repository gates pass.
```
