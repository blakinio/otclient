---
task_id: OTC-20260817-real-agent-executor
project_lane: otclient
status: implementing
phase: implement
task_kind: implementation
branch: feat/OTC-20260817-real-agent-executor
base_branch: main
created: 2026-08-17
updated: 2026-08-17
related_pr: ""
policy_version: 2
execution_mode: github
execution_reason: GitHub-only implementation and Actions validation; no model invocation without a provider-specific owner grant.
decomposition_decision: single
context_pressure: medium
context_growth: stable
context_score: 7
orchestrator_priority: 10
owned_paths:
  - tools/agents/orchestrator.py
  - tools/agents/orchestrator_executor.py
  - tools/agents/test_orchestrator_executor.py
  - tools/agents/testdata/orchestrator/fake_real_worker.py
  - tools/agents/testdata/orchestrator/executor_config.json
  - docs/agents/AGENT_ORCHESTRATOR.md
  - docs/agents/AGENT_ORCHESTRATOR.json
  - docs/agents/MODULE_CATALOG.md
  - .github/workflows/agent-orchestrator-smoke.yml
  - docs/agents/tasks/active/OTC-20260817-real-agent-executor.md
depends_on: []
required_reads:
  - AGENTS.md
  - AGENTS.override.md
  - docs/agents/AGENTS.md
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/DELIVERY_COMPLETENESS_AND_CLOSEOUT.md
  - docs/agents/ANTI_STALL_AND_EXECUTION_BUDGET.md
  - docs/agents/SESSION_RECOVERY_AND_ORPHANED_EXECUTION.md
  - docs/agents/GITHUB_ONLY_EXECUTION.md
  - docs/agents/AUTONOMOUS_PROGRAM_CONTINUATION.md
  - docs/agents/TERMINAL_CI_AND_COMMUNICATION_OVERRIDE.md
  - docs/agents/AGENT_ORCHESTRATOR.md
search_first:
  - open PRs/tasks owning tools/agents/orchestrator* or .github/workflows/agent-orchestrator-smoke.yml
optional_reads: []
---

# Real agent executor adapter

## Goal

Replace the simulator-only execution boundary with a fail-closed external-process executor adapter that can launch one independently isolated worker process per selected task, build its prompt from the durable `resume.py` bundle, enforce exact dispatch/worktree/result identity, and feed worker-result-v1 into the existing barrier. Keep the repository default disabled until a separately authorized concrete model/provider is configured.

## Acceptance criteria

- A selected worker receives a compact repository-derived continuation prompt and structured dispatch metadata, never prior chat history.
- The executor uses one temporary detached Git worktree per selected task at the exact dispatch head and never shares a worktree between workers.
- The worker command is a fixed trusted argv supplied by executor configuration/CLI, invoked without a shell; task prose cannot supply commands.
- Each worker has a finite timeout and bounded parallelism.
- Returned worker-result-v1 is validated against task id, branch, dispatch base, actual worktree HEAD, clean worktree, actual changed paths and declared ownership before fan-in.
- Malformed output, timeout, non-zero exit, dirty worktree, head mismatch or ownership escape fail closed.
- Existing dry-run behavior remains the default and requires no model credentials or owner-funded AI.
- Focused tests exercise success, malformed output, timeout/non-zero failure, head mismatch and changed-path escape using a deterministic fake process and temporary Git repositories.
- GitHub-hosted smoke proves the executor plumbing with the deterministic fake process; it does not claim a live AI/model call.
- A real model/provider call is made only if a concrete provider/model/funding/credential use is separately authorized by the owner and available in the execution environment.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-17T12:35:00Z
head: 83034227280dc3bfdf589a991f0fdbbabab7dc87
branch: feat/OTC-20260817-real-agent-executor
pr: none
status: implementing
context_routes:
  - agent-governance
  - testing
owned_paths:
  - tools/agents/orchestrator.py
  - tools/agents/orchestrator_executor.py
  - tools/agents/test_orchestrator_executor.py
  - tools/agents/testdata/orchestrator/fake_real_worker.py
  - tools/agents/testdata/orchestrator/executor_config.json
  - docs/agents/AGENT_ORCHESTRATOR.md
  - docs/agents/AGENT_ORCHESTRATOR.json
  - docs/agents/MODULE_CATALOG.md
  - .github/workflows/agent-orchestrator-smoke.yml
  - docs/agents/tasks/active/OTC-20260817-real-agent-executor.md
proven:
  - main@83034227280dc3bfdf589a991f0fdbbabab7dc87 includes merged orchestrator MVP #463, archive #476 and catalogue reconciliation #478.
  - Current orchestrator is simulator/dry-run only and documents a real external model executor as a separately authorized adapter boundary.
  - No open executor task/PR or branch was found owning this scope at admission.
  - Repository policy forbids owner-funded AI/model credentials without an exact provider/use authorization; this task implements and deterministically proves the adapter without making an unauthorized model call.
derived:
  - A fixed external-process protocol is the smallest provider-neutral adapter that can support Codex or another agent runtime later without coupling task data to credentials or shell syntax.
unknown:
  - Which concrete model/provider the owner wants this adapter to invoke for the first live AI worker wave.
  - Whether a permitted runner currently exposes that provider's authenticated CLI for this repository.
conflicts: []
first_failure:
  marker: none
  evidence: none
rejected_hypotheses:
  - Treating the simulator as a real worker was rejected because #463 explicitly proves orchestration mechanics only.
  - Inferring a Codex/OpenAI provider from an available credential or sibling-repository runner was rejected because trusted-base policy requires exact provider/use authorization.
changed_paths:
  - docs/agents/tasks/active/OTC-20260817-real-agent-executor.md
validation:
  - command: live overlap and trusted-base preflight
    result: PASS
    evidence: main, #463/#476/#478, active task inventory, open PRs and governing orchestrator contracts inspected
blockers: []
next_action: Implement the fail-closed external-process executor and deterministic tests on this branch, then open a draft PR.
```
