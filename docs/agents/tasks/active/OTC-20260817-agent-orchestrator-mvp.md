---
task_id: OTC-20260817-agent-orchestrator-mvp
project_lane: otclient
status: implementing
branch: feat/OTC-20260817-agent-orchestrator-mvp
base_branch: main
created: 2026-08-17
updated: 2026-08-17
related_pr: ""
policy_version: 2
task_kind: implementation
phase: implement
execution_mode: github
execution_reason: repository-native Python tooling and GitHub Actions smoke workflow are sufficient; no owner-funded AI execution is authorized
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
last_progress_at: 2026-08-17T09:48:00Z
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

- [ ] `orchestrator.py plan` selects a bounded wave only from READY tasks whose declared dependencies are satisfied and whose owned paths do not overlap within the wave.
- [ ] Planner output is deterministic JSON containing selected work, held work with explicit reasons, a wave identifier, and compact resume commands/bundles rather than chat history.
- [ ] Context governor never invents an exact token count; it consumes the repository's 0-15 five-dimension pressure model and blocks/rotates `high`/`unbounded` work before dispatch, with configurable handling for rising medium pressure.
- [ ] A worker-result contract validates task identity, branch/head identity, status, changed paths, validation/evidence references, context pressure, and exactly one `next_action` while incomplete.
- [ ] `orchestrator.py barrier` can ingest independent worker results, reject malformed/mismatched results, overlay completed dependency state, and produce the next deterministic wave.
- [ ] GitHub-hosted smoke workflow proves real matrix fan-out/fan-in with simulated workers and unlocks a dependent second wave without invoking any AI service.
- [ ] Focused tests cover independent parallel selection, dependency hold/unlock, path-overlap serialization, context rotation, max-parallel limits, malformed result rejection, branch mismatch rejection, and deterministic ordering.
- [ ] Documentation explains the one-coordinator/many-worker lifecycle, context rotation semantics, trust boundary, executor adapter boundary, and how to port the harness to another repository.
- [ ] Exact-head PR CI and the dedicated orchestrator smoke workflow pass before any merge claim.

## Safety and non-goals

- No owner-funded or credential-backed AI/model invocation.
- No automatic mutation of arbitrary task branches in this MVP.
- No shared branch/worktree between workers.
- No bypass of repository ownership, dependency, runtime, review, CI, or merge gates.
- No use of `ACTIVE_WORK.md` as a lock.
- No claim that the smoke workers are AI agents; they prove orchestration mechanics only.
- No exact remaining-context/token claim unless a future executor exposes a verified provider signal.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-17T09:48:00Z
head: c55e3523e6e9d50df511e65dce9145a8f951a5f5
branch: feat/OTC-20260817-agent-orchestrator-mvp
pr: none
status: implementing
context_routes:
  - agent-control-room
  - context-handoff
  - github-actions-smoke
owned_paths:
  - tools/agents/orchestrator.py
  - tools/agents/test_orchestrator.py
  - tools/agents/orchestrator_worker_result.schema.json
  - tools/agents/testdata/orchestrator/**
  - docs/agents/AGENT_ORCHESTRATOR.md
  - docs/agents/AGENT_ORCHESTRATOR.json
  - .github/workflows/agent-orchestrator-smoke.yml
  - docs/agents/tasks/active/OTC-20260817-agent-orchestrator-mvp.md
proven:
  - Main at task start is c55e3523e6e9d50df511e65dce9145a8f951a5f5.
  - Existing tools/agents provides checkpoint.py, resume.py and control_room.py; no open PR found claiming tools/agents paths.
  - EXECUTION_PROTOCOL policy v2 already defines five context-pressure dimensions, 0-15 scoring bands, and rotation of the same task under high pressure.
  - AUTONOMOUS_PROGRAM_CONTINUATION permits parallel work only for independent owned paths and keeps one coordinator responsible for shared state, acceptance, barrier review and integration.
  - Root AGENTS.md forbids owner-funded AI/model quota without explicit permission for the current use.
derived:
  - The smallest safe MVP is a deterministic planner/result collector plus real GitHub Actions fan-out/fan-in smoke, with the model executor kept as a later pluggable boundary.
unknown:
  - Whether the first live PR smoke will expose actionlint/YAML or task-parser edge cases not covered by focused tests.
conflicts: []
first_failure:
  marker: none
  evidence: none
rejected_hypotheses:
  - Direct parallel AI invocation in this task is rejected because no explicit current authorization exists to consume owner-funded AI quota.
  - Exact token-threshold rotation is rejected because the current agent/tool surface exposes no verified remaining-token signal.
changed_paths:
  - docs/agents/tasks/active/OTC-20260817-agent-orchestrator-mvp.md
validation:
  - command: repository governance and overlap preflight
    result: PASS
    evidence: root/nested agent contracts, execution/context/anti-stall policies and live open-PR search inspected; no tools/agents owner found
blockers: []
next_action: Implement the deterministic planner, result collector, fixtures and focused tests on this branch, then open the draft PR and run the GitHub-hosted smoke workflow.
```
