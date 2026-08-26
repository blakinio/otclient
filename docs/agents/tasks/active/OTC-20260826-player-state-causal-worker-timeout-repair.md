---
task_id: OTC-20260826-player-state-causal-worker-timeout-repair
status: implementing
agent: ChatGPT
session_id: chatgpt-causal-worker-timeout-repair-20260826
session_role: owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: repository_repair
phase: implementing
policy_version: 2
branch: fix/OTC-20260826-player-state-causal-worker-timeout-repair
base_branch: main
base_sha: 3db06bb0ec3ef17fa92b493f344da326ec6be793
risk: high
decomposition_decision: single
decomposition_reason: one timing contract spans the causal worker/result boundary; parallel edits would increase shared-contract risk
execution_mode: github_only
execution_reason: repository-only repair and deterministic hosted validation; no physical runtime is authorized or required
execution_class: github_hosted
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: false
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
owned_paths:
  - .github/scripts/tibia-official-client-re-player-state-causal-worker.py
  - .github/scripts/test_tibia_official_client_re_player_state_causal_worker.py
  - docs/agents/tasks/active/OTC-20260826-player-state-causal-worker-timeout-repair.md
  - docs/agents/tasks/archive/OTC-20260826-player-state-causal-worker-timeout-repair.md
modules_touched:
  - track-a-canonical-live-runtime
  - tibia-re-player-state-causal-worker
reuses:
  - PR #698 terminal post-COMMIT evidence
  - workflow run 32944297164 / job 98101615158
  - guarded-dispatch outer worker_timeout contract on current main
  - historical causal worker/test from exact runtime head 56f60bbf5d84eb43d5722349e445e99c5cb3839d
depends_on:
  - PR #698 merged
  - PR #700 merged archive/release
blocks: []
track_a_runtime_admission_version: 1
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
physical_action_budget: 0
physical_action_count: 0
no_physical_retry_after_merge: true
source_pr: 698
source_runtime_run: 32944297164
source_runtime_job: 98101615158
source_runtime_head: 56f60bbf5d84eb43d5722349e445e99c5cb3839d
source_terminal_result: AMBIGUOUS_POST_COMMIT_NO_VALID_RESULT
invocation_started_at: 2026-08-26T18:44:00+02:00
last_progress_at: 2026-08-26T18:53:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Causal worker timeout repair

## Objective

Repair the post-COMMIT causal worker/result timing contract exposed by terminal PR #698 without touching an Official Tibia runtime. The worker must finish ordinary slow/timeout reconciliation paths with a durable explicit `AMBIGUOUS` or pre-effect `REFUSED` result before the existing 30-second guarded-dispatch supervisor timeout.

## Source evidence

- trusted base at implementation: `main@3db06bb0ec3ef17fa92b493f344da326ec6be793`
- terminal source: PR #698, merged as `ca687efa72eb8bcea6a31f1840a07f89500f4ab8`; lifecycle archived/released by merged PR #700
- runtime: run `32944297164`, job `98101615158`, head `56f60bbf5d84eb43d5722349e445e99c5cb3839d`
- terminal causal sequence: READY -> one budget reservation -> COMMIT -> post-COMMIT worker exceeded guarded-dispatch `worker-timeout=30` -> `worker_timeout`
- conservative terminal classification remains `POSSIBLY_DISPATCHED=true`, `NO_RETRY=true`, physical action count `1`; causal proof was not established.

## Acceptance criteria

1. Use one deterministic monotonic worker deadline compatible with the known 30-second outer guarded-dispatch contract, with explicit reserved margin for durable result persistence and parent return/scheduling.
2. Bound every causal-worker subprocess, typed read, dispatch wait, reconciliation sleep/read cycle and result-write admission to the remaining deadline budget; no inner fixed timeout may extend the worker worst-case beyond the worker deadline.
3. Before effect, slow or timed-out semantic preconditions fail closed as explicit `REFUSED` with `effect_count=0`.
4. After dispatch is attempted exactly once, slow/hung reads, dispatch timeout/uncertainty, or reconciliation deadline exhaustion return explicit `AMBIGUOUS` with `effect_count=1` and never retry the dispatch.
5. Reserve enough budget for atomic durable result publication including file `fsync`, `os.replace`, and directory `fsync`; if result durability cannot be established, exit nonzero rather than presenting success.
6. Do not mask actual worker/process death or nonzero termination as a successful result.
7. Add TDD for slow/hung reader, slow dispatch, result-write deadline admission, reconciliation exhaustion, outer-timeout compatibility, and no-retry post-COMMIT semantics.
8. Full applicable Track A deterministic regression must pass on the exact final head. Physical E2E is `NOT_APPLICABLE`: this task is explicitly repository-only and must not start, observe, login to, move, or otherwise touch Official Tibia runtime state.
9. Independent audit must PASS with zero material findings before merge.
10. Merge by squash only after exact-head required CI passes; archive this task and release ownership. Do not perform a physical retry after merge.

## Safety boundary

`runtime_access:none`. No Official Tibia process/runtime observation, no Synology physical runtime, no KasmVNC, no input, no movement, no gameplay, no login, no credentials, no process-memory access, no physical retry.

## Current diagnosis

The historical causal worker could execute a 10-second tool check, a 20-second baseline reader, one 10-second dispatch, and up to 12 reconciliation reads each with a 20-second subprocess timeout plus sleeps. Its internal worst-case therefore exceeded the guarded-dispatch outer `worker-timeout=30`. The repair turns those independent fixed waits into slices of one monotonic budget and preserves a durable-result margin.

## Next action

Implement the deadline-bounded causal worker and focused timing-contract tests on this branch, then validate through GitHub-hosted CI only.
