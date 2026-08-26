---
task_id: OTC-20260826-player-state-causal-worker-timeout-repair
status: completed
result: DONE
phase: archived
agent: ChatGPT
session_id: chatgpt-causal-worker-timeout-repair-20260826
session_role: released
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: repository_repair
policy_version: 2
branch: docs/OTC-20260826-player-state-causal-worker-timeout-repair-closeout
base_branch: main
base_sha: b8a5007ae4d86c951d9ca44d8b780e0caeaef8f3
risk: high
execution_mode: github_only
execution_class: github_hosted
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
physical_retry_performed: false
physical_retry_after_merge_forbidden: true
source_pr: 698
source_runtime_run: 32944297164
source_runtime_job: 98101615158
source_terminal_result: AMBIGUOUS_POST_COMMIT_NO_VALID_RESULT
implementation_pr: 701
implementation_exact_head: 0aa3f4dc58a5d4c20939bb6ce239a031af82b3ec
implementation_merge_commit: b8a5007ae4d86c951d9ca44d8b780e0caeaef8f3
causal_timing_run: 32994066909
causal_timing_result: PASS
track_a_governance_run: 32994066917
track_a_governance_result: PASS
ci_run: 32994067664
ci_result: PASS
ci_required_job: 98259212152
ci_required_result: PASS
duplicate_ci_run_repaired: 32994067929
duplicate_ci_required_job_after_rerun: 98261917845
duplicate_ci_required_result_after_rerun: PASS
independent_audit: PASS
independent_audit_review: 5033262455
independent_audit_material_findings_open: 0
e2e_result: NOT_APPLICABLE
e2e_reason: repository-only timing-contract repair; physical Official Tibia runtime execution was explicitly forbidden
open_material_findings: 0
unresolved_review_threads: 0
ownership_released: true
task_archived: true
archive_pr: 702
archive_independent_audit: PASS
archive_independent_audit_review: 5033377846
archive_independent_audit_material_findings_open: 0
archive_final_exact_head_ci_required: true
last_progress_at: 2026-08-26T19:40:00+02:00
current_blocker: none
next_action: NONE
---

# Player-state causal-worker timeout repair — terminal closeout

The repository-only repair exposed by terminal PR #698 is implemented and merged through PR #701 as `b8a5007ae4d86c951d9ca44d8b780e0caeaef8f3`. No Official Tibia runtime, KasmVNC, Synology physical session, login, credentials, input, movement, gameplay, process-memory access or physical retry was used by this repair.

The repaired causal worker now starts one absolute monotonic deadline at process entry. The canonical guarded-dispatch outer worker timeout remains 30 seconds; the worker owns a 27-second total budget, reserves 2 seconds from ordinary work for durable result publication, and leaves 3 seconds outside the worker budget for supervisor return/scheduling margin. Tool checks, typed reads, dispatch, reconciliation sleeps and reconciliation reads are all capped by the remaining budget rather than independent fixed worst cases.

Pre-effect semantic/read timeout remains `REFUSED/effect_count=0`. Deadline exhaustion or spawn failure before the dispatch subprocess actually starts is also `REFUSED/effect_count=0`. Once dispatch has started, timeout/nonzero uncertainty is conservatively `AMBIGUOUS/effect_count=1`; post-dispatch slow/hung reads, unexpected delta and reconciliation exhaustion are likewise `AMBIGUOUS/effect_count=1`. No post-COMMIT path dispatches a second physical action. Durable result publication uses a mode-restricted temporary file, file `fsync`, atomic replace and directory `fsync`; inability to establish a durable result exits nonzero. The parent guarded-dispatch controller continues to reject worker process death/nonzero termination even if a valid-looking result file exists.

TDD covers slow/hung baseline reads, slow dispatch, the not-started/started dispatch boundary, spawn failure, post-dispatch hung reads, reconciliation exhaustion, result-write deadline admission, outer-timeout compatibility, exact one-dispatch semantics and parent process-death rejection. During implementation an initial overclassification of pre-start dispatch deadline as ambiguous was found and repaired. A later hosted failure was isolated to a test fixture that exhausted the budget before reaching the intended dispatch boundary; the fixture was corrected without changing production semantics.

Final implementation head `0aa3f4dc58a5d4c20939bb6ce239a031af82b3ec` passed Track A causal timing run `32994066909`, Track A governance run `32994066917` and CI run `32994067664`, including `CI / Required` job `98259212152`. A duplicate CI generation on the same SHA had been cancelled by concurrency and left a stale failing `CI / Required`; its cancelled root job was rerun once without code changes, producing successful required job `98261917845` in run `32994067929`. No branch protection was bypassed.

Fresh implementation validator-role audit review `5033262455` reported PASS with zero material findings. Fresh docs-only archive audit review `5033377846` likewise reported PASS with zero material findings on the pre-evidence-binding archive head. This archive PR remains subject to the repository's required exact-final-head CI and a final audit refresh before merge; those merge gates are PR evidence and are not predeclared as passing in this record.

Physical E2E is `NOT_APPLICABLE` because the owner explicitly constrained this repair to repository-only deterministic validation. The terminal evidence from #698 is unchanged: after its already-consumed COMMIT, absence of causal confirmation remains `POSSIBLY_DISPATCHED/AMBIGUOUS`, `NO_RETRY=true`; this repair does not retroactively prove movement or authorize another attempt. After merge, no physical retry is to be executed.
