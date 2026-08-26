---
task_id: OTC-20260826-player-state-causal-worker-postcommit-failure-rca
status: completed
result: ROOT_CAUSE_PROVEN_AND_REPAIRED
phase: archived
agent: ChatGPT
session_id: chatgpt-player-state-causal-worker-postcommit-rca-20260826
session_role: released
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: debugging
policy_version: 2
branch: docs/OTC-20260826-player-state-causal-worker-postcommit-failure-rca-archive
base_branch: main
base_sha: 2103570b500934256486a048f1809623ce56cf29
pr: 708
risk: high
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
canonical_boot_epoch_recovery: NOT_APPLICABLE
canonical_recovery: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
semantic_preconditions: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
physical_action_budget: 0
physical_action_count: 0
ready: false
commit: false
possibly_dispatched: false
no_auto_retry_after_commit: true
retry_4_safe_to_authorize: true
retry_4_authorized: false
root_cause: PROVEN_SUBPROCESS_TIMEOUT_CLEANUP_CAN_OVERRUN_RESULT_WRITE_RESERVE
reproduction: PROVEN_DETERMINISTIC_FAKE_CLOCK
repair_required: true
repair_status: MERGED_TO_TRUSTED_MAIN
implementation_pr: 708
implementation_merge_commit: 2103570b500934256486a048f1809623ce56cf29
initial_timing_fix_head: 8671a462329205b4ca61264445aae905594f6714
checkpoint_red_head: 0b2f070e78dc250abdf46fa1b3b807c4ef204237
worker_checkpoint_head: fc1c3d5859f74fdb0dbcdd4ecb52da81e645c2aa
parent_red_fixture_head: 361f6a6d61ce7842a9f359a47cfcfdf7a574fa72
parent_repair_head: ed1c35b69aea7d28977df5105c6f2c7f7cfdb0ed
final_technical_head: 2f816aa7b443152911001b07f7150dd5830ba99e
final_technical_timing_run: 33010066853
final_technical_governance_run: 33010066998
final_technical_canonical_governance_run: 33010066920
final_technical_xres_run: 33010066891
final_technical_ci_run: 33010067149
final_technical_ci_required_job: 98313912896
independent_audit: PASS
independent_audit_review_initial: 5034750238
independent_audit_review_exact_final_head: 5034765463
independent_audit_material_findings_open: 0
exact_final_head: 2cb78e380598f1db65e3291a16f326893350ada9
exact_final_head_timing_run: 33010300021
exact_final_head_timing: PASS
exact_final_head_governance_run: 33010299981
exact_final_head_governance: PASS
exact_final_head_canonical_governance_run: 33010299982
exact_final_head_canonical_governance: PASS
exact_final_head_xres_run: 33010299993
exact_final_head_xres: PASS
exact_final_head_ci_run: 33010300271
exact_final_head_ci: PASS
exact_final_head_required_context: CI / Required
exact_final_head_required_job: 98315253600
ownership_released: true
task_archived: true
archive_pr: PENDING
archive_independent_audit: REQUIRED
archive_independent_audit_review: PENDING
archive_independent_audit_material_findings_open: UNKNOWN
archive_exact_head_ci: REQUIRED
archive_exact_head_governance: REQUIRED
current_blocker: NONE_ARCHIVE_CLOSEOUT_ONLY
next_action: open archive PR, run fresh archive audit and exact-head CI/governance, then merge and bind terminal archive metadata
---

# Player-state causal worker post-COMMIT failure RCA — terminal archive

The retry-3 post-COMMIT `guarded_dispatch_worker_failed` has a proven repository-level root cause and merged repair. The failure was not the canonical parent's 30-second outer timeout. A post-dispatch player-state subprocess timeout could consume the worker's nominal result-write reserve during Python timeout cleanup, leaving a correct conservative AMBIGUOUS result unable to be durably published before the worker deadline. The resulting nonzero worker exit was then correctly rejected by the old parent as `guarded_dispatch_worker_failed`.

The repaired worker on trusted main measures fresh baseline-read cost before starting later reconciliation reads and, after exactly one successful dispatch but before reconciliation, durably writes a separate conservative fallback checkpoint fixed to `AMBIGUOUS`, `effect_count=1`, exact action hash, and `POST_DISPATCH_RECONCILIATION_INCOMPLETE`. The ordinary final result remains separate.

The repaired parent accepts that fallback only after worker nonzero/timeout and only by exact equality. A missing, malformed, mismatched, or `CONFIRMED` fallback is refused and preserves the previous failure/timeout behavior. Worker exit zero still requires the ordinary final result path. One-dispatch/no-retry semantics are unchanged.

PR #708 merged the repair as `2103570b500934256486a048f1809623ce56cf29`. Its frozen exact final head `2cb78e380598f1db65e3291a16f326893350ada9` passed fresh validator review `5034765463`, causal timing run `33010300021`, Track A governance `33010299981`, canonical live governance `33010299982`, hosted XRes validation `33010299993`, repository CI `33010300271`, and `CI / Required` job `98315253600`.

`RETRY_4_SAFE_TO_AUTHORIZE=true` is a terminal recommendation about this repaired failure mode only. `retry_4_authorized=false` remains binding. Any future retry-4 requires a separate explicit owner authorization and fresh fail-closed Track A admission from then-current trusted main.

This RCA performed no live runtime observation, gameplay, input, movement, READY, COMMIT, login, credentials, relog, restart, character selection, or process-memory mutation. Durable technical evidence remains at `docs/agents/evidence/OTC-20260826-player-state-causal-worker-postcommit-failure-rca/root-cause-and-repair.md`.