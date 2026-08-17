---
task_id: OTC-20260817-real-agent-executor
project_lane: otclient
status: validating
phase: validate
task_kind: implementation
branch: feat/OTC-20260817-real-agent-executor
base_branch: main
created: 2026-08-17
updated: 2026-08-17
related_pr: "479"
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
  - tools/agents/test_orchestrator.py
  - tools/agents/test_orchestrator_executor.py
  - tools/agents/testdata/orchestrator/fake_real_worker.py
  - docs/agents/AGENT_ORCHESTRATOR.md
  - docs/agents/AGENT_ORCHESTRATOR.json
  - docs/agents/MODULE_CATALOG.md
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
  - open PRs/tasks owning tools/agents/orchestrator*
optional_reads: []
---

# Real agent executor adapter

## Goal

Replace the simulator-only execution boundary with a fail-closed external-process executor adapter that can launch independently isolated worker processes from deterministic plan entries, build each prompt from the durable `resume.py` bundle, enforce fresh task/dependency/ownership state plus exact dispatch/worktree/result identity, and feed accepted worker-result-v1 records into the existing barrier. Keep the repository default disabled until a separately authorized concrete model/provider is configured.

## Acceptance criteria

- [x] A selected worker receives a compact repository-derived continuation prompt and structured dispatch metadata, never prior chat history.
- [x] The executor creates one temporary detached Git worktree per selected task at the exact dispatch head; Git worktree metadata operations are serialized while worker processes may run concurrently.
- [x] The worker command is a fixed trusted argv supplied by executor configuration, invoked without a shell; task prose cannot supply commands.
- [x] Each worker has a finite timeout and bounded parallelism.
- [x] The current task inventory is rediscovered and the original selected dispatch set is revalidated before any worker mutation; stale dependency/ownership/context/branch/head selection fails closed and requires a new plan.
- [x] Returned worker-result-v1 is validated against task id, branch, dispatch base, actual descendant worktree HEAD, clean worktree, actual Git changed paths and declared ownership before fan-in.
- [x] Protected/default worker branches, malformed output, timeout, non-zero exit, dirty worktree, head mismatch or ownership escape fail closed.
- [x] Worker environment is allowlisted; `HOME` and unlisted variables are excluded unless the authorized provider configuration explicitly opts them into `pass_env`.
- [x] Existing dry-run behavior remains the repository default and requires no model credentials or owner-funded AI.
- [x] A writer with non-empty changed paths must use `publish_results: true`; normal non-force publication refuses a moved existing task branch and verifies the remote head before result acceptance.
- [x] Focused tests cover successful committed/published execution plus authorization, environment, stale-plan, protected-branch, malformed-output, timeout/non-zero, dirty-worktree, head-mismatch, missing-publication, moved-remote and ownership-escape failures using deterministic temporary Git repositories.
- [ ] Exact-final-head GitHub-hosted Agent Orchestrator Smoke and required CI pass.
- [ ] Full final diff self-review and required independent audit have no unresolved material finding.
- [x] No live AI/model call is claimed; a concrete provider/model/funding/credential use remains a separate activation gate under root AGENTS policy.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-17T13:02:00Z
head: 5dbcfc7cf6f2bb03c613b889cbb65bc19fbcdd65
branch: feat/OTC-20260817-real-agent-executor
pr: 479
status: validating
context_routes:
  - agent-governance
  - testing
owned_paths:
  - tools/agents/orchestrator.py
  - tools/agents/orchestrator_executor.py
  - tools/agents/test_orchestrator.py
  - tools/agents/test_orchestrator_executor.py
  - tools/agents/testdata/orchestrator/fake_real_worker.py
  - docs/agents/AGENT_ORCHESTRATOR.md
  - docs/agents/AGENT_ORCHESTRATOR.json
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/tasks/active/OTC-20260817-real-agent-executor.md
proven:
  - main@83034227280dc3bfdf589a991f0fdbbabab7dc87 at admission includes merged orchestrator MVP #463, archive #476 and catalogue reconciliation #478.
  - PR #479 is the sole live owner found for this executor-adapter scope.
  - Repository default config remains dry_run with real_model_executor_enabled=false and owner_funded_ai_allowed=false.
  - The adapter now enforces fixed argv/no shell, finite timeout, explicit environment allowlisting, fresh plan revalidation, branch safety, isolated detached worktrees, descendant HEAD proof, actual Git diff/ownership verification and durable normal-push publication for writers.
  - Intermediate Agent Orchestrator Smoke run 32031599802 job 95392633636 executed the integrated suite on b6acd7b6fb2e6d80d2c0357a6fb97cb14c21beb0 with 24 tests PASS; later hardening intentionally invalidated that result for final readiness.
  - Self-review found and repaired stale-plan revalidation, protected-branch/ancestry checking, implicit HOME exposure, acceptance of non-durable writer commits and a malformed MODULE_CATALOG table separator.
  - Git worktree file isolation is not treated as a hostile-provider sandbox; provider-specific Git-metadata, credential, network and process confinement is explicitly retained as an activation gate.
derived:
  - A fixed external-process protocol is the smallest provider-neutral adapter that can support a separately authorized Codex or other agent runtime without coupling untrusted task prose to executable shell syntax.
unknown:
  - Which concrete model/provider, if any, the owner will separately authorize for the first live AI worker wave.
  - Whether a permitted otclient execution environment exposes that authorized provider's authenticated CLI/runtime.
conflicts: []
first_failure:
  marker: direct_main_write_rejected
  evidence: An initial task-file write attempt against protected main was rejected by GitHub with 409/required CI; no main mutation occurred and the task was then created correctly on its dedicated branch.
rejected_hypotheses:
  - Treating the #463 simulator as a real worker was rejected because its retained evidence explicitly proves orchestration mechanics only.
  - Inferring Codex/OpenAI authorization from an available credential, sibling-repository runner or prior unrelated task was rejected because root AGENTS requires exact provider/use authorization.
  - Accepting a plan solely because task head/branch still matched was rejected; the executor recomputes fresh selection and refuses stale dependency/ownership/context state before worker launch.
  - Treating detached writer commits as durable without branch publication was rejected; non-empty changed paths now require verified publication before acceptance.
changed_paths:
  - tools/agents/orchestrator.py
  - tools/agents/orchestrator_executor.py
  - tools/agents/test_orchestrator.py
  - tools/agents/test_orchestrator_executor.py
  - tools/agents/testdata/orchestrator/fake_real_worker.py
  - docs/agents/AGENT_ORCHESTRATOR.md
  - docs/agents/AGENT_ORCHESTRATOR.json
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/tasks/active/OTC-20260817-real-agent-executor.md
validation:
  - command: live overlap and trusted-base preflight
    result: PASS
    evidence: main, #463/#476/#478, active task inventory, open PRs and governing orchestrator contracts inspected
  - command: Agent Orchestrator Smoke / Focused planner and context tests
    result: PASS
    evidence: run 32031599802 job 95392633636; 24 tests passed on superseded intermediate head b6acd7b6fb2e6d80d2c0357a6fb97cb14c21beb0
  - command: live AI/model provider execution
    result: NOT_APPLICABLE
    evidence: no concrete provider/model/funding/credential use is authorized for this task; adapter delivery is provider-neutral and default-disabled
blockers: []
next_action: Verify exact-final-head Agent Orchestrator Smoke and required CI, then perform full-diff self-review and the pre-existing exact-head falsification audit before readiness.
```
