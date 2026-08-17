---
task_id: OTC-20260817-real-agent-executor
project_lane: otclient
status: completed
phase: closeout
task_kind: implementation
branch: feat/OTC-20260817-real-agent-executor
base_branch: main
created: 2026-08-17
updated: 2026-08-17
related_pr: "479"
policy_version: 2
execution_mode: github
execution_reason: GitHub-only implementation and Actions validation; no live model/provider invocation was authorized or claimed.
decomposition_decision: single
context_pressure: medium
context_growth: stable
context_score: 7
owned_paths: []
depends_on: []
---

# Real agent executor adapter — terminal archive

## Result

`REAL-AGENT-EXECUTOR` delivered the provider-neutral real external-process worker boundary for the repository-native orchestrator and completed implementation lifecycle through merged PR #479.

The adapter is real process/worktree/Git execution infrastructure, but the repository default remains fail-closed `dry_run` with `real_model_executor_enabled: false`. No concrete AI/model provider, credential, ChatGPT/Codex/OpenAI API call or owner-funded AI quota was used or claimed by this task.

## Delivered acceptance

- [x] compact `resume.py`-derived worker request instead of chat-history sharing;
- [x] deterministic live-wave revalidation before worker mutation;
- [x] fixed trusted argv, `shell=False`, finite timeout and bounded parallelism;
- [x] per-worker detached Git worktree with serialized worktree metadata operations;
- [x] protected/default branch rejection and descendant-HEAD proof;
- [x] clean-worktree, actual Git diff and declared path-ownership verification;
- [x] allowlisted worker environment with `HOME` excluded unless explicitly authorized through `pass_env`;
- [x] writer durability: non-empty changes require verified normal non-force publication to the task branch;
- [x] fail-closed moved-remote, stale-plan, malformed JSON, non-zero exit, timeout, dirty worktree, head mismatch, missing-publication and ownership-escape behavior;
- [x] repository default stays no-model/no-credential;
- [x] concrete provider activation remains separately authorization- and sandbox-gated.

## Terminal implementation evidence

```yaml
implementation_pr: 479
implementation_final_head: 7ea80cb91e52cb9c99ba00153795feec9cbf3ab2
implementation_base_main: 2ba207cef6d53dc847542b33ec94e7b53fd35b1f
implementation_merge: a39ba79a0ea09f204166c51fb2f8f3c4cb315029
changed_paths: 9
agent_orchestrator_smoke:
  run: 32033447594
  conclusion: SUCCESS
  focused_tests_job: 95398385003
  focused_tests: 30/30 PASS
  barrier_job: 95398528927
  barrier: SUCCESS
  fresh_falsification_audit_job: 95398572369
  fresh_falsification_audit: SUCCESS
ci:
  run: 32033448039
  conclusion: SUCCESS
  required_check: 95398437677
  required_check_conclusion: SUCCESS
track_a_agent_runtime_governance:
  run: 32033447670
  conclusion: SUCCESS
review_submissions: 0
unresolved_review_threads: 0
full_diff_self_review: PASS
runtime_browser_gameplay_model_e2e: NOT_APPLICABLE
runtime_e2e_reason: orchestration tooling only; no physical Track A/runtime/model-provider operation
source_branch: feat/OTC-20260817-real-agent-executor
source_branch_disposition: auto_deleted_after_merge
source_branch_evidence: exact branch search after PR #479 merge returned no matching branch
```

## Material findings repaired before merge

1. stale plan could otherwise miss changed dependency/context/ownership state — repaired with fresh plan recomputation;
2. protected branch and descendant ancestry validation were missing — repaired;
3. inherited `HOME` could expose provider/Git credential state — excluded by default and tested;
4. detached writer commits could be accepted without durable reachability — writers now require verified task-branch publication;
5. remote branch race required explicit fail-closed behavior — normal push plus before/after remote-head verification added;
6. a temporary `MODULE_CATALOG.md` table-format regression was repaired before final validation.

## Activation boundary

The merged adapter does **not** authorize a provider. A live AI worker wave requires a separate exact authorization naming the concrete provider/model/funding/credential use plus an appropriate trusted wrapper and provider-specific boundary for repository-global Git metadata, credentials, network and process authority. Credential availability alone is not authorization.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-17T13:12:00Z
head: a39ba79a0ea09f204166c51fb2f8f3c4cb315029
branch: docs/OTC-20260817-real-agent-executor-closeout
pr: pending
status: completed
context_routes:
  - agent-governance
owned_paths: []
proven:
  - PR #479 merged by squash as a39ba79a0ea09f204166c51fb2f8f3c4cb315029 after exact current-main reconciliation.
  - CI / Required, Agent Orchestrator Smoke, 30/30 focused tests, Track A governance and Fresh falsification audit passed on final implementation head 7ea80cb91e52cb9c99ba00153795feec9cbf3ab2.
  - The implementation source branch is absent after merge.
  - No live AI/model/provider call occurred in this task.
derived: []
unknown: []
conflicts: []
first_failure:
  marker: direct_main_write_rejected
  evidence: initial task-file direct-main attempt was rejected before mutation; work then proceeded correctly through dedicated branch/PR.
rejected_hypotheses:
  - simulator evidence is not a live model claim
  - worktree isolation is not a hostile-provider sandbox
changed_paths:
  - docs/agents/tasks/archive/OTC-20260817-real-agent-executor.md
  - docs/agents/tasks/active/OTC-20260817-real-agent-executor.md
  - docs/agents/MODULE_CATALOG.md
validation:
  - command: implementation exact-head GitHub Actions
    result: PASS
    evidence: runs 32033447594, 32033448039, 32033447670
  - command: source branch closeout
    result: PASS
    evidence: branch search returned no feat/OTC-20260817-real-agent-executor branch after merge
blockers: []
next_action: Merge the lifecycle-only closeout PR after its exact-head lightweight governance/CI passes, then verify closeout source-branch deletion.
```

## Source branch closeout

```yaml
source_branch_disposition: auto_delete_after_merge
source_branch_reason: implementation PR #479 merged terminally; no durable purpose remains for the implementation branch
source_branch_evidence: branch search after merge returned no `feat/OTC-20260817-real-agent-executor` ref
```
