---
task_id: OTC-20260818-native-login-to-ingame-e2e
status: completed
session_role: released
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_reverse_engineering_semantic_control
phase: closed
source_pr: 528
source_branch: runtime/OTC-20260818-native-login-to-ingame-e2e-v3
source_audited_head: 8e029f5849a1d51f69486adcc3716c80f139e60e
source_late_terminal_head: 75c7deb9b2b673be7c869d1008d08509b8f1e5a1
source_disposition: closed_unmerged_superseded
source_late_delta_implementation_changed: false
coordinator_review: 4971140006
coordinator_decision: ACCEPT_WITH_EDITS
open_material_findings_after_repair: 0
audit_pr: 575
audit_disposition: closed_unmerged_consumed
audit_final_head: c09f26d4a97f991dc1782416104786a6722ff160
audit_helper_validation_run: 32242561205
audit_table_validation_run: 32242788755
audit_table_validation_result: SUCCESS
late_spark_audit_attempt: NO_MODEL_RESPONSE_AUTH_401
late_spark_audit_controlling: false
promotion_base: aaf6706cfcd02e70511e5fa7e9ef9b0d7e1f0d12
promotion_pr: 577
promotion_head: 31b252add74ac094067effd7bb3c0e4f888f09e4
promotion_merge: db41e9112383fd5993cba04437bbbd8f6963e6e7
promotion_merge_method: squash
promotion_changed_paths: 23
promotion_ahead_by: 4
promotion_behind_by: 0
promotion_ci_run: 32243674084
promotion_ci_result: SUCCESS
promotion_governance_run: 32243673952
promotion_governance_result: SUCCESS
promotion_native_auth_bridge_run: 32243673903
promotion_native_auth_bridge_result: SUCCESS
promotion_review: 4971210315
promotion_review_threads_open: 0
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
physical_e2e_required: true
physical_e2e_result: SUCCESS_AT_PROOF_POINT
character_actually_logged_into_game: true
causal_proof: COMPLETE
structural_in_game_at_proof_point: PASS_3_OF_3
currently_logged_in_at_terminal_governed_state: false
post_handoff_session_stability: FAIL_NOT_RETAINED
second_secret_attempt_performed: false
e2e_result: PASS_WITH_POST_HANDOFF_STABILITY_FAILURE
ownership_released: true
---

# OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME — terminal archive

## Terminal disposition

The bounded native-login-to-world task is completed and ownership is released.

Source PR #528 was preserved as provenance and closed unmerged as superseded after independently audited clean promotion PR #577 squash-merged to `main` as:

```text
db41e9112383fd5993cba04437bbbd8f6963e6e7
```

Temporary coordinator audit PR #575 was closed unmerged after its result was consumed into canonical evidence. No audit workflow or credential-bearing workflow from those branches was merged.

## Physical E2E result

The exact current official Linux client reached the game world through the bounded native path:

```text
RESULT=SUCCESS_AT_PROOF_POINT
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=YES
CAUSAL_PROOF=COMPLETE
STRUCTURAL_IN_GAME_AT_PROOF_POINT=PASS_3_OF_3
```

Proof-point identity:

```text
PID=27368
DISPLAY=:1
size=52109920
sha256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
```

At that proof point the three required structural discriminators each had exactly one validated hit.

## Post-proof stability result

A later native process handoff did not retain the governed structural in-game session:

```text
CURRENTLY_LOGGED_IN=NO
POST_HANDOFF_SESSION_STABILITY=FAIL_NOT_RETAINED
SECOND_SECRET_ATTEMPT=NOT_PERFORMED
```

This is part of the terminal result. The successful login-to-world event must not be rewritten as persistent session-retention success.

A later source-task note recorded an unadmitted diagnostic observation after the terminal check; the source itself classified it `NOT_ADMISSION_GRADE`. It is therefore not promoted over the governed terminal stability result.

## Secret boundary

One owner-authorized bounded native-auth ingress used repository secret variables during the proven physical task execution. Secret values were not printed, logged, committed or retained. They were not replayed for coordinator closeout.

## Independent post-implementation audit

Coordinator review `4971140006` classified the frozen source head `8e029f5849a1d51f69486adcc3716c80f139e60e` as `ACCEPT_WITH_EDITS`.

The source final workflow had not compiled/falsified all three newly introduced current-SHA helper files. Audit #575 closed that gap using GitHub-hosted static/synthetic validation only:

```text
current_sha_native_login_gate.py             py_compile PASS
current_sha_secret_ingress.cpp               compile PASS
experimental_character_control_current.cpp   compile PASS
sealed memfd + required seals                PASS
SCM_RIGHTS synthetic ingress                 PASS
source current-SHA gate                      PASS
exact current public package fence            PASS
REAL_SECRET_ACCESS=false
OFFICIAL_CLIENT_EXECUTED=false
```

Targeted strict generated-QMeta control-flow run `32242788755` succeeded:

```text
TGameClient                       table=0x1d903c4 methods=44 switch LEA=0xd1910a
TCharacterSelectionController     table=0x1d98fe4 methods=26 switch LEA=0xd51c90
TAuthenticationProcessController  table=0x1d8ff20 methods=51 switch LEA=0xd0f5ff
STRICT_ALL_NATIVE_LOGIN_QMETA_TABLES=PASS
```

Two earlier audit generations failed because of coordinator-audit methodology defects; neither identified a source implementation defect.

## Late source-branch reconciliation

After the coordinator audit freeze, another source continuation advanced #528 to `75c7deb9b2b673be7c869d1008d08509b8f1e5a1`. A fresh `8e029f...75c7deb` comparison found no changes to the three current-SHA helper sources or other task implementation code. The native-task-specific late additions were task metadata plus an attempted exact `gpt-5.3-codex-spark` independent audit.

That Spark invocation produced **no model response** because ChatGPT-managed Codex authentication returned HTTP 401 `token_invalidated` / `refresh_token_invalidated`. The failed authentication is neither evidence for nor against the implementation and is non-controlling because the separate coordinator independent audit above completed successfully.

## Run 32233929770 classification

The credential-bearing run reached the helper response phase only after bounded secret-source validation, sealed-memfd construction/sealing, Unix-socket peer UID/PID validation and `SCM_RIGHTS` dispatch. The terminal `NATIVE_AUTH_RESPONSE_FAILED` marker is therefore not evidence of missing secrets or local ingress failure.

Combined with the later same-current-build authenticated world proof and the absence of a second secret attempt, the task accepts the classification that the normal helper IPC response channel was lost across the native process handoff. This does not imply later session retention; that stability failed separately as recorded above.

## Promotion validation

Exact promotion head `31b252add74ac094067effd7bb3c0e4f888f09e4` passed:

```text
CI                                  32243674084 = SUCCESS
Track A governance                  32243673952 = SUCCESS
Track A native auth bridge          32243673903 = SUCCESS
promotion review                    4971210315
open review threads                 0
ahead_by                            4
behind_by                           0
```

The clean promotion contained accepted durable evidence, v4 prompt, the three exact current-SHA helper sources, coordinator audit evidence and a temporary `runtime_access:none` promotion-admission task. The temporary promotion task is removed by lifecycle closeout.

## Remaining programme gaps

This task is terminal, but it does **not** prove:

- reliable session retention across later native process handoffs;
- a general reusable guarantee that the client remains logged in after restart/re-exec;
- any broader gameplay/action correctness beyond reaching the causal in-game proof point;
- any authorization to repeat credential-bearing login for unrelated research.

Those are separate future research gates, not blockers on this completed login-to-world E2E task.
