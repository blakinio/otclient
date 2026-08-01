---
task_id: OTC-20260801-agent-governance-v2-1
status: implementing
agent: "GPT-5.6 Thinking"
track: agent-governance
workstream: governance-v2-1
parallel_wave: GOVERNANCE-V2-1
parallel_lane: PROMPT-CONTEXT-CLOSEOUT
parallel_lane_state: implementing
coordinator_task: none
branch: docs/agent-governance-v2-1-20260801
base_branch: main
created: 2026-08-01T23:46:00+02:00
updated: 2026-08-01T23:46:00+02:00
last_verified_commit: "UNKNOWN"
required_base_commit: "UNKNOWN"
risk: low
related_pr: ""
depends_on: []
integration_after: []
owned_paths:
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/AUTONOMOUS_PROGRAM_CONTINUATION.md
  - docs/agents/PROMPT_EVAL_STANDARD.md
  - docs/agents/TRUST_AND_CONTEXT_BOUNDARIES.md
  - docs/agents/END_TO_END_FEATURE_COMPLETENESS.md
  - docs/agents/TASK_CLOSEOUT_AUDIT_E2E.md
  - docs/agents/tasks/active/OTC-20260801-agent-governance-v2-1.md
shared_path_lease: []
contract_role: producer
contracts_produced:
  - prompt evaluation and regression contract v2.1
  - trust and context boundary contract v2.1
  - end-to-end feature completeness contract v2.1
  - task closeout audit and E2E contract v2.1
contracts_consumed:
  - autonomous programme continuation v2
  - checkpoint contract v1
  - execution policy v2
crates_touched: []
features_touched: []
contracts_touched:
  - agent prompting and task completion only
modules_touched:
  - agent-governance
reuses:
  - existing active/archive task lifecycle
  - existing checkpoint and ownership contracts
public_interfaces: []
cross_repo_tasks:
  - blakinio/canary
  - blakinio/freqtrade
  - blakinio/Oteryn-Platform
  - blakinio/Otheryn
performance_evidence:
  - documentation-only; no runtime or performance claim
security_evidence:
  - client, protocol, asset, Canary, upstream and production gates remain unchanged
---

# OTC-20260801 — Agent governance v2.1

## Goal

Extend v2 with eval-driven prompts, trust/context boundaries, outcome verification, complete vertical slices, and mandatory PR hygiene, fresh audit, E2E, exact-head final CI, archival, and autonomous continuation.

## Scope

Exactly the listed documentation/governance paths. No client runtime, protocol, proprietary asset, production, Canary, upstream, workflow, or deployment mutation is authorized.

## Acceptance criteria

- [ ] Prompt changes are versioned and regression-evaluated with balanced cases and repeated trials where useful.
- [ ] Environment outcome, not a worker claim, controls completion.
- [ ] Retrieved natural-language content remains untrusted data.
- [ ] User-facing work requires all applicable frontend/backend consumers and observable states.
- [ ] Closeout requires a fresh audit, real E2E, exact-head final CI, resolved review threads, terminal related PRs, archive, and ownership release.
- [ ] Autonomous coordination continues after closeout when more READY work exists.
- [ ] Exact-head required CI passes.
- [ ] This task is archived after merge.

## Context checkpoint

```yaml
checkpoint_version: 1
policy_version: 2
updated_at: 2026-08-01T23:46:00+02:00
head: UNKNOWN
branch: docs/agent-governance-v2-1-20260801
pr: UNKNOWN
status: implementing
phase: implement
session_id: chat-20260801-governance-v2-1
session_role: coordinator
execution_mode: chat
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_routes:
  - agent-governance
owned_paths:
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/AUTONOMOUS_PROGRAM_CONTINUATION.md
  - docs/agents/PROMPT_EVAL_STANDARD.md
  - docs/agents/TRUST_AND_CONTEXT_BOUNDARIES.md
  - docs/agents/END_TO_END_FEATURE_COMPLETENESS.md
  - docs/agents/TASK_CLOSEOUT_AUDIT_E2E.md
  - docs/agents/tasks/active/OTC-20260801-agent-governance-v2-1.md
proven:
  - Autonomous programme continuation v2 is already merged on main.
  - The owner explicitly authorized this cross-repository governance update.
derived:
  - Supporting contracts should be consumed by the existing prompting entry points.
unknown:
  - Exact PR number and exact-head workflow results until the draft PR is opened.
conflicts: []
first_failure:
  marker: none
  evidence: no exact-head failure classified yet
rejected_hypotheses:
  - encode durable rules only in chat
  - call an isolated producer a complete user-facing feature
changed_paths:
  - docs/agents/tasks/active/OTC-20260801-agent-governance-v2-1.md
validation: []
blockers: []
next_action: add the v2.1 normative contracts and update the prompting entry points
```
