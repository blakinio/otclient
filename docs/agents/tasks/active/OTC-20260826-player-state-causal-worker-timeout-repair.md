---
task_id: OTC-20260826-player-state-causal-worker-timeout-repair
status: validating
agent: ChatGPT
session_id: chatgpt-causal-worker-timeout-repair-20260826
session_role: owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: repository_repair
phase: validate
policy_version: 2
branch: fix/OTC-20260826-player-state-causal-worker-timeout-repair
base_branch: main
base_sha: 3db06bb0ec3ef17fa92b493f344da326ec6be793
risk: high
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
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
  - .github/scripts/test_tibia_official_client_re_causal_worker_timeout_contract.py
  - .github/scripts/test_tibia_official_client_re_causal_worker_dispatch_boundary.py
  - .github/workflows/track-a-causal-worker-timing.yml
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
last_progress_at: 2026-08-26T19:22:00+02:00
validation_level: focused
focused_validation_result: pass
focused_validation_note: worker and timeout suites passed on hosted run 32992814821; remaining failure was isolated to the dispatch-boundary fixture and repaired without production-code change
self_review_finding: pre-start dispatch deadline was initially overclassified as AMBIGUOUS/effect_count=1; production repair now distinguishes not-started from started dispatch
latest_ci_failure_run: 32992814821
latest_ci_failure_job: 98254362146
latest_ci_failure_signature: dispatch-boundary fixture exhausted budget before precondition and received SEMANTIC_PRECONDITION_TIMEOUT instead of reaching dispatch-before-start boundary
latest_ci_failure_disposition: fixture repaired by allowing baseline to complete before consuming the final non-write second; production worker unchanged
pre_fixture_repair_head: c0a2e9869dde3cea5578ad5eb4d1f0f99e8533a2
fixture_repair_commit: 71a27151cc46c6350c88b20f60131cfbce9753a1
heavy_validation_runs: 2
ci_checks_for_current_head: 0
ci_check_generation: synchronize_after_fixture_repair
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
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

## Implemented contract

- one monotonic absolute worker deadline starts at worker process entry;
- outer guarded-dispatch default remains 30 s; worker total budget is 27 s, leaving 3 s parent/scheduling margin;
- 2 s of the worker budget is reserved from tool/read/dispatch/reconciliation waits for durable result publication;
- every subprocess timeout and reconciliation sleep is capped to the remaining non-write budget;
- pre-effect semantic/read timeout is `REFUSED/effect_count=0`;
- dispatch deadline/spawn failure before child creation is `REFUSED/effect_count=0`;
- once dispatch starts, timeout/nonzero exit is conservatively `AMBIGUOUS/effect_count=1` and is never retried;
- post-dispatch slow/hung reader, unexpected delta, or reconciliation exhaustion is `AMBIGUOUS/effect_count=1` and never dispatches again;
- durable result uses mode-restricted temp file, file fsync, atomic replace, directory fsync and deadline admission; inability to prove durability exits nonzero;
- current parent already rejects worker nonzero/process death before accepting any result, and a regression test locks that behavior.

## Validation evidence so far

- repository-only focused behavioral smoke: PASS; no runtime was accessed;
- hosted exact-head predecessor run `32992814821` / job `98254362146`: worker suite 18/18 PASS and timeout-contract suite 3/3 PASS; the only failure was the newly added dispatch-boundary fixture;
- that failure was not a product regression: the fixture began with only the 2 s write reserve, so the worker correctly returned `SEMANTIC_PRECONDITION_TIMEOUT` before reaching dispatch;
- fixture repair `71a27151cc46c6350c88b20f60131cfbce9753a1` now gives baseline one non-write second, consumes it after the valid baseline, and then proves dispatch cannot spawn when only the durable-write reserve remains;
- TDD covers slow/hung baseline reader, slow dispatch, dispatch-before-start deadline, spawn failure, post-dispatch hung reader, reconciliation exhaustion, result-write deadline, outer-timeout compatibility, exact one-dispatch semantics and parent process-death rejection;
- retained GitHub-hosted workflow `.github/workflows/track-a-causal-worker-timing.yml` runs the causal worker tests plus canonical guarded-dispatch, Kasm probe and typed player-state resolver regressions on exact checkout.

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

## Next action

Consume the fresh exact-head GitHub-hosted checks generated by this checkpoint; if all required checks pass, perform the fresh validator-role audit and merge hygiene on that exact unchanged head.
