---
task_id: OTC-20260817-agent-orchestrator-mvp
project_lane: otclient
status: implementing
branch: feat/OTC-20260817-agent-orchestrator-mvp
base_branch: main
created: 2026-08-17
updated: 2026-08-17
related_pr: "#463"
policy_version: 2
task_kind: implementation
phase: implement
execution_mode: github
execution_reason: repository-native Python tooling and GitHub Actions smoke are sufficient; no owner-funded AI execution is authorized
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: one reusable orchestrator MVP with deterministic planner, fan-out/fan-in smoke, context gate, then exact-head validation
session_id: gpt-5.6-sol-20260817-orchestrator-01
session_role: implementer
session_rotation_count: 0
heavy_validation_runs: 0
stale_takeover_count: 0
human_interruptions: 0
invocation_started_at: 2026-08-17T09:48:00Z
last_progress_at: 2026-08-17T10:08:00Z
ci_checks_for_current_head: 0
ci_check_generation: draft
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
- [ ] GitHub-hosted smoke workflow proves real matrix fan-out/fan-in with simulated workers and unlocks a dependent second wave without invoking any AI service.
- [x] Focused tests cover independent selection, dependency hold/unlock, overlap serialization, context rotation, capacity, malformed result rejection, branch mismatch, provider ratio validation and deterministic ordering.
- [x] Documentation explains lifecycle, context rotation, trust boundary, executor adapter boundary, staged rollout and cross-repository porting.
- [ ] Exact-head PR CI and dedicated orchestrator smoke workflow pass before any merge claim.

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
updated_at: 2026-08-17T10:08:00Z
head: 3ae0ed05e7b3f1c09ebed6efec669d915c792d21
branch: feat/OTC-20260817-agent-orchestrator-mvp
pr: 463
status: implementing
context_routes:
  - agent-control-room
  - context-handoff
  - github-actions-smoke
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
  - Main advanced from c55e3523e6e9d50df511e65dce9145a8f951a5f5 to 0b3bdec0a4145f558806448a4657413664d80729 during implementation; compare shows three commits and no overlap with orchestrator-owned paths.
  - Local focused suite passes 14 tests after module refactor and includes CLI execution rather than py_compile-only evidence.
  - Fixture wave 1 deterministically selects OTC-TEST-A and OTC-TEST-B; barrier unlocks OTC-TEST-C in wave 2 while high-context OTC-TEST-D stays held.
derived:
  - The safe first production shape is deterministic control-plane mechanics plus a disabled model-executor boundary, followed by plan-only and read-only stages before any parallel writers.
unknown:
  - GitHub actionlint and the real hosted fan-out/fan-in result until PR #463 runs on the published implementation head.
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
    evidence: no open tools/agents owner; current main 0b3bdec0a4145f558806448a4657413664d80729 differs only on Track A/XRes/runtime-evidence paths
  - command: PYTHONPATH=tools/agents python tools/agents/test_orchestrator.py
    result: PASS
    evidence: 14 tests passed including dependency, overlap, context, result-contract and deterministic-order cases
  - command: orchestrator CLI plan -> simulate A/B -> barrier -> assess-context
    result: PASS
    evidence: wave-1-9310b608fb68ad59 selected A+B; wave-2-f338f66bcf8a3d63 selected C+E; score 10 high produced rotate
  - command: JSON and YAML parse checks
    result: PASS
    evidence: orchestrator configs/schema parse as JSON; agent-orchestrator-smoke.yml parses as YAML
  - command: GitHub Actions exact-head smoke and required CI
    result: NOT_RUN
    evidence: pending publication of implementation commit
blockers: []
next_action: Publish the implementation tree on top of current main and verify PR #463 exact-head Agent Orchestrator Smoke plus required CI.
```
