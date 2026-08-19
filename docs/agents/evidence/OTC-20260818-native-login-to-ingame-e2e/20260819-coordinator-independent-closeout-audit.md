# Native-login E2E — independent coordinator closeout audit

Date: 2026-08-19  
Source PR: #528  
Source head: `8e029f5849a1d51f69486adcc3716c80f139e60e`  
Coordinator decision: `ACCEPT_WITH_EDITS`

## Scope

This audit independently falsified the final current-SHA native-login package without repeating the already-proven credential-bearing E2E event.

```yaml
runtime_access: none
physical_client_execution: false
real_secret_access: false
login_performed: false
gui_input: false
gameplay: false
client_mutation: false
```

The existing physical proof point is consumed as durable historical causal evidence. No second credential attempt was made for closeout.

## Source exact-head validation

The frozen source head had already passed:

```text
CI                                      32239719607 = SUCCESS
Track A agent runtime governance        32239719365 = SUCCESS
Track A native auth bridge validation   32239719372 = SUCCESS
review threads                           0
```

Fresh comparison against coordinator-start `main@aaf6706cfcd02e70511e5fa7e9ef9b0d7e1f0d12` proved the long-lived source branch was stale in Git ancestry:

```text
ahead_by  = 160
behind_by = 6
merge_base = e4357137e47836d67eb19ceb13a8e313f69bf778
```

Therefore the source branch must not merge directly; accepted task material is restacked through a clean current-main promotion.

## Material validation gap found and repaired

The source final bridge workflow compiled the pre-existing `experimental_auth.cpp` path, but did not compile/falsify all three new final-source current-SHA helper files:

```text
tools/tibia_runtime_bridge/current_sha_native_login_gate.py
tools/tibia_runtime_bridge/current_sha_secret_ingress.cpp
tools/tibia_runtime_bridge/experimental_character_control_current.cpp
```

This was a validation gap, not a demonstrated behavioral failure. Coordinator audit PR #575 was created solely to close it on the frozen source head.

### Helper build and secret-ingress falsification

Independent hosted audit proved:

```text
current_sha_native_login_gate.py             py_compile PASS
current_sha_secret_ingress.cpp               compile PASS
experimental_character_control_current.cpp   shared-library compile PASS
sealed memfd full seal set                    PASS
SCM_RIGHTS one-fd transfer                    PASS
same-UID / exact expected peer PID            PASS
synthetic credential header+payload           PASS
synthetic native-auth success response parse  PASS
REAL_SECRET_ACCESS=false
OFFICIAL_CLIENT_EXECUTED=false
```

The test used only fixed synthetic strings. No Tibia credential value was read or exposed.

One compiler warning remains non-material: `experimental_character_control_current.cpp` defines an unused local helper `errorJson`.

## Audit repair history

Two failed audit generations are retained as falsification history and are not source findings.

### Generation 1 — audit lifetime bug

Run `32242202262` successfully completed helper compile/synthetic ingress and the exact current public-package fence, then failed because the audit step's own `EXIT` trap deleted the temporary client before the next source-gate step.

Classification:

```text
AUDIT_BUG=TEMP_CLIENT_REMOVED_BETWEEN_STEPS
SOURCE_FINDING=false
```

### Generation 2 — inapplicable discovery assumption

Run `32242561205` successfully completed:

```text
helper compile/synthetic ingress = PASS
current package fence             = PASS
source current-SHA gate           = PASS
TGameClient strict binding        = PASS
CharacterSelection strict binding = PASS
```

It then failed only because the coordinator parser required `TAuthenticationProcessController` to be discoverable as one relocation-backed static QMetaObject. The source gate does not make that assumption; it uses independently recovered QMeta metadata/string/table addresses. The audit requirement was therefore narrowed to the actual claim: prove the table has a real generated switch xref.

Classification:

```text
AUDIT_ASSUMPTION=INAPPLICABLE_RELOCATION_BACKED_CLASS_DISCOVERY_REQUIREMENT
SOURCE_FINDING=false
```

### Generation 3 — targeted table-xref discriminator

Run `32242788755` completed successfully. It independently fetched and fenced the exact current public package, ran the frozen source gate, then scanned executable code for full generated QMeta switch chains.

Terminal markers:

```text
CURRENT_PUBLIC_PACKAGE_FENCE=PASS
SOURCE_CURRENT_SHA_GATE=PASS
STRICT_TABLE_SWITCH=TGameClient;TABLE=0x1d903c4;METHODS=44;LEA=0xd1910a
STRICT_TABLE_SWITCH=TCharacterSelectionController;TABLE=0x1d98fe4;METHODS=26;LEA=0xd51c90
STRICT_TABLE_SWITCH=TAuthenticationProcessController;TABLE=0x1d8ff20;METHODS=51;LEA=0xd0f5ff
STRICT_ALL_NATIVE_LOGIN_QMETA_TABLES=PASS
RAW_CLIENT_RETAINED=false
OFFICIAL_CLIENT_EXECUTED=false
REAL_SECRET_ACCESS=false
```

The strict discriminator required a generated control-flow shape rather than merely trusting an executable-looking relative table:

```text
cmp method-index, method_count - 1
RIP-relative LEA table
movsxd target, dword ptr [table + method-index*4]
add target, table
indirect jmp target
```

The source gate's exact current-build targets are therefore independently supported, including:

```text
TGameClient::onRequestLoginWithCredentials                 index 17 -> 0xd196f0
TGameClient::connectClientToGameserverWithExistingCredentials index 11 -> 0xd19500
TCharacterSelectionController::requestCharacterLogin      index 0  -> 0xd52050
TCharacterSelectionController::onCharacterSelectionConfirmed index 11 -> 0xd52020
TAuthenticationProcessController::requestCharacterGameserverLogin index 5 -> 0xd0fd27
TAuthenticationProcessController::onStartGameServerLoginStateEntered index 27 -> 0xd0fb62
```

## Physical E2E result boundary

The task's already-retained physical evidence proves one exact-current-client native login-to-world event:

```text
RESULT=SUCCESS_AT_PROOF_POINT
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=YES
CAUSAL_PROOF=COMPLETE
STRUCTURAL_IN_GAME_AT_PROOF_POINT=PASS_3_OF_3
proof PID=27368
proof executable size=52109920
proof executable SHA256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
```

At the proof point the durable evidence records one validated object for each required structural discriminator:

```text
TPlayerProtocolMessageHandler   = 1
TGameserverGameSession          = 1
TWorldmapProtocolMessageHandler = 1
```

The later process handoff is a separate negative stability result and must remain visible:

```text
CURRENTLY_LOGGED_IN=NO
POST_HANDOFF_SESSION_STABILITY=FAIL_NOT_RETAINED
SECOND_SECRET_ATTEMPT=NOT_PERFORMED
```

The successful proof point is not erased by later session loss, and the later session loss must not be rewritten as a persistent-login success claim.

## Run 32233929770 classification

The credential-bearing run reached the native helper response phase only after bounded non-empty secret checks, sealed-memfd construction/sealing, Unix-socket peer UID/PID validation and `SCM_RIGHTS` dispatch. The terminal `NATIVE_AUTH_RESPONSE_FAILED` marker is therefore not evidence of a missing secret or local ingress failure.

Combined with the later same-current-build authenticated world proof and no second credential attempt, the durable task classification that the helper IPC response channel was lost across native process handoff is accepted for this task. It does not generalize into a claim that session retention survives later native process handoffs; the opposite was observed.

## Coordinator decision

```yaml
source_pr: 528
source_head: 8e029f5849a1d51f69486adcc3716c80f139e60e
coordinator_review: 4971140006
coordinator_decision: ACCEPT_WITH_EDITS
open_material_findings_after_repair: 0
physical_e2e_result: SUCCESS_AT_PROOF_POINT
post_handoff_session_stability: FAIL_NOT_RETAINED
credential_replay_for_closeout: false
```

Required edits are promotion/lifecycle edits only: integrate the independently audited current-SHA helper/evidence package on fresh `main`, replace the active task record with terminal archive state, preserve the success-vs-stability distinction, and record the independent audit. Do not rerun credentials merely to manufacture duplicate evidence.
