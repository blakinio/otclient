---
task_id: OTC-20260818-native-login-to-ingame-e2e
status: promotion_pending
session_role: coordinator
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_reverse_engineering_semantic_control
phase: coordinator-promotion
source_pr: 528
source_branch: runtime/OTC-20260818-native-login-to-ingame-e2e-v3
source_head: 8e029f5849a1d51f69486adcc3716c80f139e60e
source_disposition: close_unmerged_after_promotion
coordinator_review: 4971140006
coordinator_decision: ACCEPT_WITH_EDITS
open_material_findings_after_repair: 0
audit_pr: 575
audit_final_head: c09f26d4a97f991dc1782416104786a6722ff160
audit_helper_validation_run: 32242561205
audit_table_validation_run: 32242788755
audit_table_validation_result: SUCCESS
promotion_base: aaf6706cfcd02e70511e5fa7e9ef9b0d7e1f0d12
promotion_pr: pending
promotion_head: pending
promotion_merge: pending
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
currently_logged_in_at_terminal_source_state: false
post_handoff_session_stability: FAIL_NOT_RETAINED
second_secret_attempt_performed: false
ownership_release_state: pending_promotion_merge
---

# OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME — archive checkpoint

## Coordinator disposition

Source PR #528 is accepted with closeout edits after independent post-implementation falsification.

The exact current official client at the successful proof point was:

```text
size   52109920
sha256 ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
```

## Physical E2E result

The task achieved its required native login-to-world event:

```text
RESULT=SUCCESS_AT_PROOF_POINT
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=YES
CAUSAL_PROOF=COMPLETE
STRUCTURAL_IN_GAME_AT_PROOF_POINT=PASS_3_OF_3
```

The proof point is bounded to the exact process/session recorded in durable evidence. It is not a statement that the account remained logged in forever.

## Post-proof stability result

The later process handoff did not retain the structural in-game session:

```text
CURRENTLY_LOGGED_IN=NO
POST_HANDOFF_SESSION_STABILITY=FAIL_NOT_RETAINED
SECOND_SECRET_ATTEMPT=NOT_PERFORMED
```

This negative stability result is part of the terminal outcome and must not be hidden by the successful E2E proof point.

## Secret boundary

One bounded owner-authorized native-auth ingress used the repository secrets during the proven task execution. Secret values were not printed, committed or retained. Coordinator closeout does not replay credentials and uses only static/synthetic audit inputs.

## Independent final audit

Coordinator review `4971140006` classified the frozen source `ACCEPT_WITH_EDITS`.

The source final workflow did not independently compile all three newly introduced current-SHA helper files. Audit PR #575 repaired that validation gap without touching the physical runtime:

```text
current_sha_native_login_gate.py             py_compile PASS
current_sha_secret_ingress.cpp               compile PASS
experimental_character_control_current.cpp   compile PASS
sealed memfd + required seals                PASS
SCM_RIGHTS synthetic ingress                 PASS
source current-SHA gate                      PASS
exact current public package fence            PASS
```

Targeted strict generated-QMeta table audit run `32242788755` then proved:

```text
TGameClient                    table=0x1d903c4 methods=44 switch LEA=0xd1910a
TCharacterSelectionController  table=0x1d98fe4 methods=26 switch LEA=0xd51c90
TAuthenticationProcessController table=0x1d8ff20 methods=51 switch LEA=0xd0f5ff
STRICT_ALL_NATIVE_LOGIN_QMETA_TABLES=PASS
RAW_CLIENT_RETAINED=false
OFFICIAL_CLIENT_EXECUTED=false
REAL_SECRET_ACCESS=false
```

Two earlier audit failures were audit-method defects and are recorded in the coordinator audit evidence; neither identified a source defect.

## Promotion rule

The long-lived source branch is stale in Git ancestry (`behind_by=6` against coordinator-start main). It must not merge directly. Clean promotion carries accepted durable evidence, v4 prompt and the three current-SHA helper sources onto current `main`, with no credential-bearing or temporary audit workflow.

After promotion merge:

1. close source #528 unmerged as superseded;
2. close audit #575 unmerged as audit-only/consumed;
3. lifecycle-update this archive to `status: completed`, `session_role: released`, `ownership_released: true`;
4. do not repeat the already-proven credential-bearing E2E solely for closeout.
