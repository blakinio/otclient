---
task_id: OTC-20260817-agent-orchestrator-mvp
project_lane: otclient
status: final_ci
branch: feat/OTC-20260817-agent-orchestrator-mvp
base_branch: main
created: 2026-08-17
updated: 2026-08-17
related_pr: "#463"
policy_version: 2
task_kind: implementation
phase: final_ci
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
heavy_validation_runs: 4
stale_takeover_count: 0
human_interruptions: 1
invocation_started_at: 2026-08-17T09:48:00Z
last_progress_at: 2026-08-17T12:35:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: exact-head-final-metadata
terminal_ci_wait_started_at: 2026-08-17T12:35:00+02:00
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
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
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
  - docs/agents/TASK_CLOSEOUT_AUDIT_E2E.md
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
- [x] Reusable-module discovery is current in `MODULE_CATALOG.md` and the architecture change is recorded in `CHANGELOG.md`.
- [ ] Final metadata head has exact-head required CI and Agent Orchestrator Smoke green before merge.

## Safety and non-goals

- No owner-funded or credential-backed AI/model invocation.
- No automatic mutation of arbitrary task branches in this MVP.
- No shared branch/worktree between workers.
- No bypass of ownership, dependency, runtime, review, CI, or merge gates.
- No use of `ACTIVE_WORK.md` as a lock.
- No claim that smoke workers are AI agents; they prove orchestration mechanics only.
- No exact remaining-context/token claim unless a future executor exposes a verified provider signal.

## Final-CI checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-17T12:35:00+02:00
pre_metadata_head: f99f571b92d5216d4413fad7b70083196a76fd5c
branch: feat/OTC-20260817-agent-orchestrator-mvp
pr: 463
status: final_ci
base_main: f99ec371bafd0b9dbccb8fd6f4c8a3137e7d963b
restack_merge: 2b2342cdd9085f73603410934a6528628096b64c
context_routes:
  - agent-control-room
  - context-handoff
  - github-actions-smoke
  - live-plan-only
  - fresh-falsification-audit
proven:
  - The planner/result/barrier/context-governor implementation is covered by 14 focused tests and CLI execution.
  - GitHub-hosted Agent Orchestrator Smoke run 32019049767 completed SUCCESS on implementation head 08208e7f9923ab3badaeb6129868eaaf5f14b69c with focused tests, live inventory plan-only audit, parallel simulated workers, fan-in and fresh falsification.
  - Live plan-only artifact 9284623311 selected no unsafe work and held incomplete READY tasks on CONTEXT_UNKNOWN/HEAD_UNKNOWN rather than guessing.
  - Fresh audit job 95354812788 emitted FRESH_ORCHESTRATOR_AUDIT_PASS=true for malicious-next-action, broad ownership conflict, high-context rotation and result-base mismatch negatives.
  - General CI run 32019049951 and Track A governance run 32019049806 completed SUCCESS on the same coherent implementation generation.
  - Main drift was rechecked as non-overlapping and integrated without force-push in merge commit 2b2342cdd9085f73603410934a6528628096b64c with parents 140c2338ebc511ff9f5bd463b2b16e8be6ab8646 and f99ec371bafd0b9dbccb8fd6f4c8a3137e7d963b.
  - On restacked head 2b2342cdd9085f73603410934a6528628096b64c, CI run 32022927574, Track A governance run 32022927450 and Agent Orchestrator Smoke run 32022927403 all completed SUCCESS.
  - PR #463 was changed from Draft to Ready only after that exact-head success and had no submitted reviews or unresolved review threads.
  - Related-PR search by task ID returned only PR #463; no duplicate/superseded task PR was found.
  - `MODULE_CATALOG.md` was updated narrowly with the orchestrator entry and its prior provenance was rechecked after correcting an intermediate manual-copy error before final CI.
  - `CHANGELOG.md` records the architecture change and explicitly preserves the simulated-worker/no-paid-AI boundary.
derived:
  - The safe first production shape is deterministic control-plane mechanics plus a disabled model-executor boundary, followed by explicit authorization and a read-only real-worker stage before parallel writers.
unknown:
  - Exact-head workflow result for the final metadata checkpoint commit created by this update.
conflicts: []
first_failure:
  marker: module-catalog-manual-copy-provenance
  evidence: diff inspection detected one accidental existing SHA mutation; it was corrected immediately and the resulting catalog patch contains only the intended date/entry plus newline normalization
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
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - .github/workflows/agent-orchestrator-smoke.yml
  - docs/agents/tasks/active/OTC-20260817-agent-orchestrator-mvp.md
validation:
  - command: PYTHONPATH=tools/agents python tools/agents/test_orchestrator.py
    result: PASS
    evidence: 14 tests passed including dependency, overlap, context, result-contract and deterministic-order cases
  - command: GitHub Actions Agent Orchestrator Smoke run 32019049767
    result: PASS
    evidence: seven jobs including live plan-only and fresh falsification completed successfully
  - command: fresh falsification audit
    result: PASS
    evidence: job 95354812788 emitted FRESH_ORCHESTRATOR_AUDIT_PASS=true
  - command: exact restacked-head workflow generation
    result: PASS
    evidence: head 2b2342cdd9085f73603410934a6528628096b64c; CI 32022927574, Track A governance 32022927450, Agent Orchestrator Smoke 32022927403 all SUCCESS
  - command: final metadata exact-head workflows
    result: RUNNING
    evidence: this checkpoint commit is the terminal pre-merge head and must pass all required workflows before merge
blockers: []
next_action: verify final metadata exact-head CI and Agent Orchestrator Smoke; if green, merge PR #463, archive this task with exact merge evidence, release ownership, and verify terminal main
```
