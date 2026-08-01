---
task_id: OTC-20260801-agent-governance-v2-1
status: validating
agent: "GPT-5.6 Thinking"
track: agent-governance
workstream: governance-v2-1
parallel_wave: GOVERNANCE-V2-1
parallel_lane: PROMPT-CONTEXT-CLOSEOUT
parallel_lane_state: validating
coordinator_task: none
branch: docs/agent-governance-v2-1-20260801
base_branch: main
created: 2026-08-01T23:46:00+02:00
updated: 2026-08-02T00:10:00+02:00
last_verified_commit: "54b31694ace56999179d0a34c4f89c17ca677a45"
required_base_commit: "f4eb8eef601a90a9f660672911f3e914f5ffae94"
risk: low
related_pr: "#161"
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
  - autonomous programme continuation v2.1
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
  - blakinio/canary#1052
  - blakinio/freqtrade#985
  - blakinio/Oteryn-Platform#442
  - blakinio/Otheryn#298
performance_evidence:
  - documentation-only; no runtime or performance claim
security_evidence:
  - client, protocol, asset, Canary, upstream and production gates remain unchanged
---

# OTC-20260801 — Agent governance v2.1

## Goal

Extend v2 with evaluated prompts, trust/context boundaries, outcome verification, complete vertical slices, and mandatory PR hygiene, fresh audit, E2E, exact-head final CI, archival, and autonomous continuation.

## Scope

Exactly the listed documentation/governance paths. No client runtime, protocol, proprietary asset, production, Canary, upstream, workflow or deployment mutation is authorized.

## Acceptance criteria

- [x] Prompt changes are versioned and regression-evaluated with balanced cases and repeated trials where useful.
- [x] Environment outcome, not a worker claim, controls completion.
- [x] Retrieved natural-language content remains untrusted data.
- [x] User-facing work requires all applicable frontend/backend consumers and observable states.
- [x] Closeout requires a fresh audit, real E2E, exact-head final CI, resolved review threads, terminal related PRs, archive, and ownership release.
- [x] Autonomous coordination continues after closeout when more READY work exists.
- [ ] Exact-head required CI passes.
- [ ] This task is archived after merge.

## Context checkpoint

```yaml
checkpoint_version: 1
policy_version: 2
updated_at: 2026-08-02T00:10:00+02:00
head: 54b31694ace56999179d0a34c4f89c17ca677a45
branch: docs/agent-governance-v2-1-20260801
pr: 161
status: validating
phase: audit_and_ci
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
  - Compare main...branch contains exactly eight authorized governance/task paths and no client runtime or workflow code.
  - All v2.1 contract paths exist and entry points route to them consistently.
  - Client, protocol, asset, Canary, upstream, production and deployment restrictions remain authoritative.
  - Proportionate documentation audit found no missing reference, contradictory completion rule or material defect.
  - Runtime E2E is NOT_APPLICABLE_WITH_REASON because only governance documentation changes; exact-head CI and lifecycle validation remain required.
derived:
  - The contract set prevents isolated client/backend producers and stale PRs from being reported as complete product work.
unknown:
  - Exact-head required CI after this checkpoint commit.
  - Fresh final PR diff and review-thread state.
conflicts: []
first_failure:
  marker: none
  evidence: no exact-head failure classified yet
rejected_hypotheses:
  - encode durable rules only in chat
  - call an isolated producer a complete user-facing feature
  - allow required E2E to be skipped without blocking completion
changed_paths:
  - docs/agents/AUTONOMOUS_PROGRAM_CONTINUATION.md
  - docs/agents/END_TO_END_FEATURE_COMPLETENESS.md
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPT_EVAL_STANDARD.md
  - docs/agents/TASK_CLOSEOUT_AUDIT_E2E.md
  - docs/agents/TRUST_AND_CONTEXT_BOUNDARIES.md
  - docs/agents/tasks/active/OTC-20260801-agent-governance-v2-1.md
validation:
  - command: compare main...docs/agent-governance-v2-1-20260801
    result: PASS
    evidence: exactly eight authorized documentation/governance paths
  - command: cross-reference and contradiction audit
    result: PASS
    evidence: all contract paths exist and completion rules agree
  - command: runtime E2E applicability review
    result: NOT_APPLICABLE_WITH_REASON
    evidence: no executable product behavior changed
blockers: []
next_action: verify exact-head required CI and fresh PR review for PR 161, then merge and archive the task
```
