---
task_id: OTC2-20260801-playability-p0-coordination
status: active
agent: "GPT-5.6 Thinking"
lane: otclient-v2
track: greenfield-rust
workstream: playability-p0
phase: launch
branch: docs/OTC2-20260801-playability-p0-coordination
base_branch: main
created: 2026-08-01T18:55:00+02:00
updated: 2026-08-01T18:55:00+02:00
last_verified_commit: "17f2a4bf86563609e6f9edb4c71ca40fbbda59b2"
required_base_commit: "17f2a4bf86563609e6f9edb4c71ca40fbbda59b2"
risk: medium
related_pr: null
depends_on:
  - full-playability programme PR #135 merge 72a45210aafd682d6d9e95c54c1fee55dca46abb
  - programme archive PR #138 merge 17f2a4bf86563609e6f9edb4c71ca40fbbda59b2
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-coordination.md
shared_path_lease: []
implementation_authorized: false
policy_version: 2
task_kind: discovery
execution_mode: chat
context_pressure: medium
decomposition_decision: split
validation_level: focused
---

# Goal

Launch the accepted P0 full-playability discovery wave without product implementation by creating five isolated worker tasks, branches and draft PRs with exclusive evidence paths and no shared source-path lease.

# Authorization and scope

This launch task may own only its coordinator checkpoint. It may inspect live Git, tasks, PRs, checks and accepted programme documents. It must not modify Rust, C++, Lua, OTUI, manifests, lockfiles, workflows, producer repositories or P0 worker report paths.

# Acceptance

- [ ] exact current `main`, plan/archive merges and open PR ownership are verified;
- [ ] five unique worker tasks, branches and draft PRs exist;
- [ ] every worker owns only its task plus two named report paths;
- [ ] no worker receives a shared source-path lease or implementation authorization;
- [ ] dispatch state records exact PR numbers and heads;
- [ ] coordinator PR contains only this task path and required CI passes.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T18:55:00+02:00
head: 17f2a4bf86563609e6f9edb4c71ca40fbbda59b2
branch: docs/OTC2-20260801-playability-p0-coordination
pr: none
status: implementing
context_routes:
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/CONTEXT_HANDOFF.md
  - oteryn-client/docs/agents/playability/WAVE_P0_DISCOVERY.md
  - oteryn-client/docs/agents/prompts/PLAYABILITY_COORDINATOR_AGENT.md
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-coordination.md
proven:
  - Current main is 17f2a4bf86563609e6f9edb4c71ca40fbbda59b2.
  - Programme PR #135 and lifecycle archive PR #138 are merged.
  - Open PRs #23, #48 and #97 do not overlap any proposed P0 task or report path.
  - Repository search found no existing playability-p0 task or report.
derived:
  - All launch gates permit five independent docs/evidence-only workers.
  - No shared source-path lease is required for P0.
unknown:
  - Exact worker PR numbers and heads until dispatch completes.
conflicts: []
first_failure:
  marker: none
  evidence: launch preflight is clean.
rejected_hypotheses:
  - Launch gameplay implementation now: rejected because P0 authorizes discovery only.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-coordination.md
validation:
  - command: live main/open PR/path ownership preflight
    result: PASS
    evidence: main 17f2a4bf; PR #23/#48/#97 changed paths are disjoint from all P0 outputs.
blockers: []
next_action: Create the five worker task branches and draft PRs, then update this dispatch checkpoint with exact PR numbers and heads.
```
