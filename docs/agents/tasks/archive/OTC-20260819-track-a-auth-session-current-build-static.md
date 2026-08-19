---
task_id: OTC-20260819-track-a-auth-session-current-build-static
status: promotion_ready
session_role: coordinator
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: reverse_engineering_protocol
phase: coordinator-promotion
source_pr: 556
source_branch: research/OTC-20260819-track-a-auth-session-current-build-static
source_head: 411d0e287d08406c682ef063fb3f3f61341d9295
source_disposition: close_unmerged_after_promotion
coordinator_review: 4970802493
coordinator_decision: ACCEPT_WITH_EDITS
open_material_findings_after_repair: 0
audit_pr: 568
audit_head: 4d377f8088e07e68f3680558212f16e532201f70
strict_audit_run: 32239540646
strict_audit_result: SUCCESS
strict_artifact: 9360231314
strict_artifact_sha256: f81ab45076a2f31d7fa9bfc34793009a1a52347e4dd26ad6ce73225e274d12b7
promotion_base: e4357137e47836d67eb19ceb13a8e313f69bf778
promotion_pr: 569
promotion_head: pending_final_exact_head
promotion_merge: pending
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
physical_e2e_required: false
ownership_release_state: pending_promotion_merge
---

# TIBIA-RE-AUTH-SESSION — coordinator promotion archive checkpoint

## Coordinator decision

Source Draft #556 is `ACCEPT_WITH_EDITS` after an independent exact-current-build strict control-flow audit.

The exact public client identity remains:

```text
packed size / SHA-256   10214529 / 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked size / SHA-256 52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
ELF build ID             d803d9695868713ef6ab0c3cf65f91212c9c6a62
```

Current trusted fence authority is canonical #555 merge `2e572789a2bc4b64c5e906c4515c15c625f6bc9e` plus #561 closeout. Source wording that still describes #555 as an unmerged Draft is stale and is superseded by this coordinator package.

## Independent strict proof

Coordinator strict run `32239540646` on audit head `4d377f8088e07e68f3680558212f16e532201f70` succeeded. Artifact `9360231314` has GitHub SHA-256 and independently reproduced downloaded ZIP SHA-256:

```text
f81ab45076a2f31d7fa9bfc34793009a1a52347e4dd26ad6ce73225e274d12b7
```

The strict discriminator required a complete QMeta invoke-switch chain rather than an executable-looking jump table alone:

```text
cmp edx, method_count - 1
RIP-relative LEA table
movsxd target, dword ptr [table + rdx*4]
add target, table
jmp target
```

Accepted exact-build bindings:

```text
TGameClient::onRequestLoginWithCredentials
  QMeta index 17 / METHOD / void(QString,QString) -> 0xd196f0

TGameClient::connectClientToGameserverWithExistingCredentials
  QMeta index 11 / METHOD / void() -> 0xd19500

TLoginRequestUploader::loginSuccessful
  QMeta index 0 / SIGNAL -> signal activation dispatch target 0xd10200

TCharacterSelectionController::requestCharacterLogin
  QMeta index 0 / SIGNAL -> signal activation dispatch target 0xd52050
```

The two signal targets are not promoted as call-safe business implementations.

## Preserved unknowns

This bounded package does not prove:

- current executable targets for non-QMeta methods such as `advanceStateMachineDirectlyToCharacterSelection`, `requestCharacterGameserverLogin`, or `onStartGameServerLoginStateEntered`;
- `TPlaySessionData` / `TAuthenticationAndEncryptionInfo` field provenance or password requirement semantics;
- live objects, vptr instances, Qt thread affinity or helper call safety;
- login success, character selection, game-server connection, causal `IN_GAME`, restart/relogin or session-retention stability.

The source producer's 19/19 bounded auth/session structural-name presence is accepted only as names/type continuity for entries not independently target-bound.

## Safety boundary

`runtime_access:none`; no official-client execution, Synology/KasmVNC observation, login, credentials, gameplay, session mutation, process-memory access, GUI input or client mutation occurred in the coordinator audit/promotion.

## Lifecycle

Promotion PR #569 remains Draft until its final exact head passes required CI/review/freshness gates. Do not close source #556 or release ownership before promotion merges. After merge, close #556 unmerged as superseded and finalize this archive to `status: completed`, `session_role: released`, `ownership_released: true` in a lifecycle-only closeout.
