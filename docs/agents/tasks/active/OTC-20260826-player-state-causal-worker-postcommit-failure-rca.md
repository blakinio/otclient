---
task_id: OTC-20260826-player-state-causal-worker-postcommit-failure-rca
status: validating
agent: ChatGPT
session_id: chatgpt-player-state-causal-worker-postcommit-rca-20260826
session_role: owner
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: debugging
phase: validating
policy_version: 2
branch: debug/OTC-20260826-player-state-causal-worker-postcommit-failure-rca
base_branch: main
base_sha: 64189859ae360205c0467b8fcd2ead1ff78df679
risk: high
decomposition_decision: single
decomposition_reason: one causal failure chain traced end-to-end before implementation change
execution_mode: github_plus_local_deterministic_tests
execution_reason: RCA is runtime-free; live client/runtime access is forbidden
owned_paths:
  - .github/scripts/tibia-official-client-re-player-state-causal-worker.py
  - .github/scripts/test_tibia_official_client_re-player-state-causal-worker.py
  - .github/scripts/test_tibia_official_client_re_causal_worker_dispatch_boundary.py
  - .github/scripts/test_tibia_official_client_re_causal_worker_timeout_contract.py
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - docs/agents/evidence/OTC-20260826-player-state-causal-worker-postcommit-failure-rca/**
  - docs/agents/tasks/active/OTC-20260826-player-state-causal-worker-postcommit-failure-rca.md
  - docs/agents/tasks/archive/OTC-20260826-player-state-causal-worker-postcommit-failure-rca.md
reuses:
  - terminal runtime evidence from OTC-20260826-player-state-semantic-promotion-e2e-retry-3
  - merged durable causal worker repair PR #701
  - archive/ownership closeout PR #702
  - retry-3 closeout/archive PRs #703/#704/#705
track_a_runtime_admission_version: 1
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
repair_status: IMPLEMENTED_AND_HOSTED_VALIDATED
implementation_pr: 708
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
independent_audit_material_findings_open: 0
exact_final_head: PENDING_EVIDENCE_CLOSEOUT_HEAD
exact_final_head_ci: REQUIRED
exact_final_head_governance: REQUIRED
exact_final_head_timing: REQUIRED
ownership_released: false
task_archived: false
current_blocker: NONE_IMPLEMENTATION_CLOSEOUT_ONLY
next_action: run fresh exact-final-head audit and hosted timing/governance/CI on the evidence-bound closeout head, merge PR #708, archive task, and release ownership
---

# Player-state causal worker post-COMMIT failure RCA

The retry-3 `guarded_dispatch_worker_failed` root cause is proven without runtime access. A late post-dispatch subprocess timeout can consume the nominal durable-result reserve during Python timeout cleanup. The worker can therefore derive the correct conservative `AMBIGUOUS/effect_count=1` result but fail to durably publish it before its absolute deadline, causing nonzero exit and the parent-level no-valid-result failure.

The repair adds two fail-closed layers. First, a measured baseline-read headroom gate avoids starting obviously doomed late reconciliation reads without double-counting the write reserve. Second, after exactly one successful dispatch and before reconciliation, the worker durably writes a separate `AMBIGUOUS/effect_count=1/POST_DISPATCH_RECONCILIATION_INCOMPLETE` checkpoint. The parent may recover that checkpoint after worker nonzero/timeout only by exact equality; it never accepts `CONFIRMED` from the fallback path and preserves the ordinary final-result contract when the worker exits zero.

Hosted exact technical validation on `2f816aa7b443152911001b07f7150dd5830ba99e` is PASS across causal timing, Track A runtime governance, canonical live governance, hosted XRes integration, repository CI and `CI / Required`. Fresh validator review `5034750238` reports zero material findings.

`RETRY_4_SAFE_TO_AUTHORIZE=true` means only that this specific post-COMMIT no-valid-result failure mode is deterministically reproduced and repaired. `retry_4_authorized=false` remains binding. This task has performed no gameplay, login/session action, live runtime observation, COMMIT, movement, or other physical action. Durable detail is in `docs/agents/evidence/OTC-20260826-player-state-causal-worker-postcommit-failure-rca/root-cause-and-repair.md`.