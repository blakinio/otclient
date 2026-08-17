---
task_id: OTC-20260817-agent-orchestrator-mvp
project_lane: otclient
status: validating
branch: feat/OTC-20260817-agent-orchestrator-mvp
base_branch: main
created: 2026-08-17
updated: 2026-08-17
related_pr: "#463"
policy_version: 2
task_kind: implementation
phase: validate
execution_mode: github
execution_reason: repository-native Python tooling and GitHub Actions smoke are sufficient; no owner-funded AI execution is authorized
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: one reusable orchestrator MVP with deterministic planner, fan-out/fan-in smoke, context gate, live plan-only audit and exact-head validation
session_id: gpt-5.6-sol-20260817-orchestrator-01
session_role: implementer
session_rotation_count: 0
heavy_validation_runs: 2
stale_takeover_count: 0
human_interruptions: 0
invocation_started_at: 2026-08-17T09:48:00Z
last_progress_at: 2026-08-17T10:15:00Z
ci_checks_for_current_head: 3
ci_check_generation: exact-head-pre-ready
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
owned_paths:
  - tools/agents/orchestrator.py
  - tools/agents/orchestrator_core.py
  - tools/agents/orchestrator_results.py
  - tools/agents/test_orchestrator.py
  - tools/agents/orchestrator_worker_result.schema.json
  - tools/agents/testdata/orchestrator/**
  - docs/agents/AGENT_ORCHESTRATOR.md
  - docs/agents/AGENT_ORCHESTRATOR.json
  - .github/workflows/agent-orchestrator-smoke.yml
  - docs/agents/tasks/active/OTC-20260817-agent-orchestrator-mvp.md
modules_touched:
  - agent coordination tooling
reuses:
  - tools/agents/control_room.py
  - tools/agents/checkpoint.py
  - tools/agents/resume.py
  - docs/agents/EXECUTION_PROTOCOL.md context-pressure policy
  - docs/agents/CONTEXT_HANDOFF.md durable checkpoint contract
depends_on: []
blocks: []
cross_repo_tasks: []
required_reads:
  - AGENTS.md
  - docs/agents/AGENTS.md
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/AUTONOMOUS_PROGRAM_CONTINUATION.md
  - docs/agents/ANTI_STALL_AND_EXECUTION_BUDGET.md
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/CONTEXT_HANDOFF.md
  - docs/agents/PROJECT_LANES.json
  - docs/agents/BUILD_TEST_MATRIX.md
search_first:
  - tools/agents/**
  - .github/workflows/**
optional_reads: []
---

# Repository-native agent orchestrator MVP

## Goal

Provide a safe, testable repository-native control plane that lets one coordinator select independent READY tasks, fan them out as a bounded wave, collect standardized worker results, recompute barriers, and rotate sessions before context pressure becomes unsafe without pretending to know an exact remaining-token count.

## Feature scope

```yaml
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: true
  completion_claim: internal_only
```

The MVP does not invoke Codex, the OpenAI API, ChatGPT subscriptions, paid AI review services, or any owner-funded model quota. Its worker executor is deliberately dry-run/simulated; a real model executor is a later adapter requiring separately verified authority and funding policy.

## Acceptance criteria

- [x] `orchestrator.py plan` selects a bounded wave only from READY tasks whose declared dependencies are satisfied and whose owned paths do not overlap within the wave.
- [x] Planner output is deterministic JSON containing selected work, held work with explicit reasons, a wave identifier, and compact resume commands rather than chat history.
- [x] Context governor never invents an exact token count; it consumes the repository 0-15 five-dimension pressure model and rotates `high`/`unbounded` work, rising medium pressure, or an optional verified low provider-context ratio.
- [x] A worker-result contract validates task identity, branch/head identity, status, changed paths, validation/evidence references, context pressure, and one `next_action` while incomplete.
- [x] `orchestrator.py barrier` ingests independent worker results, rejects malformed/mismatched results, overlays completed dependency state, and produces the next deterministic wave.
- [x] GitHub-hosted smoke workflow proves real matrix fan-out/fan-in with simulated workers and unlocks a dependent second wave without invoking any AI service.
- [x] Focused tests cover independent selection, dependency hold/unlock, overlap serialization, context rotation, capacity, malformed result rejection, branch mismatch, provider ratio validation and deterministic ordering.
- [x] Live repo plan-only audit parses the real active task inventory and fails closed rather than guessing when context/head evidence is missing.
- [x] Fresh falsification audit independently exercises trust-boundary, ownership-overlap, context-rotation and result-base binding negatives.
- [x] Documentation explains lifecycle, context rotation, trust boundary, executor adapter boundary, staged rollout and cross-repository porting.
- [ ] Final metadata head has exact-head required CI and Agent Orchestrator Smoke green before merge.

## Safety and non-goals

- No owner-funded or credential-backed AI/model invocation.
- No automatic mutation of arbitrary task branches in this MVP.
- No shared branch/worktree between workers.
- No bypass of ownership, dependency, runtime, review, CI, or merge gates.
- No use of `ACTIVE_WORK.md` as a lock.
- No claim that smoke workers are AI agents; they prove orchestration mechanics only.
- No exact remaining-context/token claim unless a future executor exposes a verified provider signal.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-17T10:15:00Z
head: 08208e7f9923ab3badaeb6129868eaaf5f14b69c
branch: feat/OTC-20260817-agent-orchestrator-mvp
pr: 463
status: validating
context_routes:
  - agent-control-room
  - context-handoff
  - github-actions-smoke
  - live-plan-only
  - fresh-falsification-audit
owned_paths:
  - tools/agents/orchestrator.py
  - tools/agents/orchestrator_core.py
  - tools/agents/orchestrator_results.py
  - tools/agents/test_orchestrator.py
  - tools/agents/orchestrator_worker_result.schema.json
  - tools/agents/testdata/orchestrator/**
  - docs/agents/AGENT_ORCHESTRATOR.md
  - docs/agents/AGENT_ORCHESTRATOR.json
  - .github/workflows/agent-orchestrator-smoke.yml
  - docs/agents/tasks/active/OTC-20260817-agent-orchestrator-mvp.md
proven:
  - Existing checkpoint.py, resume.py and control_room.py are reused; no open PR was found claiming tools/agents paths.
  - Repository policy defines the five-dimension 0-15 context model and requires same-task rotation rather than guessing exact token capacity.
  - AUTONOMOUS_PROGRAM_CONTINUATION permits parallel independent owned paths while one coordinator retains barrier and integration responsibility.
  - Root AGENTS.md forbids owner-funded AI/model quota without explicit current authorization; this MVP invokes none.
  - Main advanced from c55e3523e6e9d50df511e65dce9145a8f951a5f5 to 0b3bdec0a4145f558806448a4657413664d80729 during implementation; compare showed no overlap with orchestrator-owned paths, and 0b3bdec0a4145f558806448a4657413664d80729 is an explicit parent of implementation merge commit 5b071e4f2e3c908658aaef77f0d1189f3b0fde7f.
  - Local focused suite passes 14 tests after module refactor and includes CLI execution rather than py_compile-only evidence.
  - Fixture wave 1 deterministically selects OTC-TEST-A and OTC-TEST-B; barrier unlocks OTC-TEST-C in wave 2 while high-context OTC-TEST-D stays held.
  - GitHub run 32018747718 on head 5b071e4f2e3c908658aaef77f0d1189f3b0fde7f completed SUCCESS and proved two matrix workers on distinct hosted runners followed by successful fan-in.
  - GitHub run 32019049767 on head 08208e7f9923ab3badaeb6129868eaaf5f14b69c completed SUCCESS with focused tests, real inventory plan-only audit, parallel simulated workers, fan-in and fresh falsification audit.
  - Live repo plan-only artifact 9284623311 reported selected=0, held=2, inactive=9; both held READY tasks were rejected with CONTEXT_UNKNOWN and HEAD_UNKNOWN rather than guessed into a wave.
  - Fresh audit job 95354812788 emitted FRESH_ORCHESTRATOR_AUDIT_PASS=true after proving malicious next_action text is not propagated as an execution command, broad ownership conflicts serialize, high context rotates, and a mismatched result base SHA blocks the next wave.
  - General CI run 32019049951 on head 08208e7f9923ab3badaeb6129868eaaf5f14b69c completed SUCCESS, including yamllint, pinned-source actionlint and informational static analysis.
  - Track A governance run 32019049806 completed SUCCESS on the same head.
  - PR #463 has no submitted reviews and no inline review threads as of this checkpoint.
derived:
  - The safe first production shape is deterministic control-plane mechanics plus a disabled model-executor boundary, followed by explicit authorization and a read-only real-worker stage before parallel writers.
  - Real active task inventory currently exposes no dispatchable otclient task under the new gates; metadata repair or future READY tasks will be needed before a real plan selects work.
unknown:
  - Exact-head workflow result for the metadata checkpoint commit created by this update.
conflicts: []
first_failure:
  marker: refactor-cli-missing-valid-growth-import
  evidence: discovered by executing the refactored CLI; fixed before publication and the CLI plus 14-test suite then passed
rejected_hypotheses:
  - Direct parallel AI invocation is rejected because no explicit current authorization exists to consume owner-funded AI quota.
  - Exact token-threshold rotation is rejected because the current agent/tool surface exposes no verified remaining-token signal.
changed_paths:
  - tools/agents/orchestrator.py
  - tools/agents/orchestrator_core.py
  - tools/agents/orchestrator_results.py
  - tools/agents/test_orchestrator.py
  - tools/agents/orchestrator_worker_result.schema.json
  - tools/agents/testdata/orchestrator/config.json
  - tools/agents/testdata/orchestrator/active/OTC-TEST-A.md
  - tools/agents/testdata/orchestrator/active/OTC-TEST-B.md
  - tools/agents/testdata/orchestrator/active/OTC-TEST-C.md
  - tools/agents/testdata/orchestrator/active/OTC-TEST-D.md
  - tools/agents/testdata/orchestrator/active/OTC-TEST-E.md
  - tools/agents/testdata/orchestrator/active/OTC-TEST-F.md
  - docs/agents/AGENT_ORCHESTRATOR.md
  - docs/agents/AGENT_ORCHESTRATOR.json
  - .github/workflows/agent-orchestrator-smoke.yml
  - docs/agents/tasks/active/OTC-20260817-agent-orchestrator-mvp.md
validation:
  - command: repository governance, live PR ownership and main-drift preflight
    result: PASS
    evidence: no open tools/agents owner; current main 0b3bdec0a4145f558806448a4657413664d80729 was integrated as an implementation parent without owned-path overlap
  - command: PYTHONPATH=tools/agents python tools/agents/test_orchestrator.py
    result: PASS
    evidence: 14 tests passed including dependency, overlap, context, result-contract and deterministic-order cases
  - command: orchestrator CLI plan -> simulate A/B -> barrier -> assess-context
    result: PASS
    evidence: wave-1-9310b608fb68ad59 selected A+B; wave-2-f338f66bcf8a3d63 selected C+E; score 10 high produced rotate
  - command: GitHub Actions Agent Orchestrator Smoke run 32018747718
    result: PASS
    evidence: exact implementation head 5b071e4f2e3c908658aaef77f0d1189f3b0fde7f; two parallel matrix workers and fan-in succeeded
  - command: GitHub Actions Agent Orchestrator Smoke run 32019049767
    result: PASS
    evidence: exact pre-checkpoint head 08208e7f9923ab3badaeb6129868eaaf5f14b69c; seven jobs including live plan-only and fresh falsification completed successfully
  - command: live repo plan-only audit
    result: PASS
    evidence: artifact 9284623311; selected=0 held=2 inactive=9; held tasks fail closed on CONTEXT_UNKNOWN and HEAD_UNKNOWN
  - command: fresh falsification audit
    result: PASS
    evidence: job 95354812788 emitted FRESH_ORCHESTRATOR_AUDIT_PASS=true
  - command: general CI run 32019049951
    result: PASS
    evidence: exact pre-checkpoint head 08208e7f9923ab3badaeb6129868eaaf5f14b69c; CI completed SUCCESS
  - command: exact-head final metadata CI
    result: NOT_RUN
    evidence: this checkpoint update creates the final metadata head and triggers the required workflows
blockers: []
next_action: Verify exact-head workflows on the metadata checkpoint commit; if green and review state remains clean, mark PR #463 ready, merge it, then archive the task through the repository lifecycle closeout path.
```
