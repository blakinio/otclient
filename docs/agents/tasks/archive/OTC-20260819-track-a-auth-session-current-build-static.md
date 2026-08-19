---
task_id: OTC-20260819-track-a-auth-session-current-build-static
status: completed
session_role: released
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: reverse_engineering_protocol
phase: closed
source_pr: 556
source_branch: research/OTC-20260819-track-a-auth-session-current-build-static
source_head: 411d0e287d08406c682ef063fb3f3f61341d9295
source_disposition: closed_unmerged_superseded
coordinator_review: 4970802493
coordinator_decision: ACCEPT_WITH_EDITS
open_material_findings_after_repair: 0
audit_pr: 568
audit_disposition: closed_unmerged_consumed
audit_head: 4d377f8088e07e68f3680558212f16e532201f70
strict_audit_run: 32239540646
strict_audit_result: SUCCESS
strict_artifact: 9360231314
strict_artifact_sha256: f81ab45076a2f31d7fa9bfc34793009a1a52347e4dd26ad6ce73225e274d12b7
promotion_base: e4357137e47836d67eb19ceb13a8e313f69bf778
promotion_pr: 569
promotion_head: 9d98566d2f1ea839a9241d11b9b64d8fb599369b
promotion_merge: fe5f17a3ea4fe9341fa3f4d2720a4186f3b8995d
promotion_merge_method: squash
promotion_changed_paths: 6
promotion_ahead_by: 7
promotion_behind_by: 0
promotion_ci_run: 32239950338
promotion_ci_result: SUCCESS
promotion_review: 4970837047
promotion_review_threads_open: 0
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
physical_e2e_required: false
e2e_result: NOT_APPLICABLE
e2e_reason: static GitHub-hosted evidence/audit promotion; no official-client runtime operation was part of this bounded task
ownership_released: true
---

# TIBIA-RE-AUTH-SESSION — terminal current-build static revalidation archive

## Terminal disposition

The bounded current-build static auth/session task is completed and ownership is released.

Source researcher PR #556 was preserved as provenance and closed unmerged as superseded after coordinator promotion. Temporary coordinator audit PR #568 was also closed unmerged after its strict result was consumed into canonical evidence.

Clean promotion PR #569 squash-merged to `main` as:

```text
fe5f17a3ea4fe9341fa3f4d2720a4186f3b8995d
```

## Exact current build

```text
packed size / SHA-256   10214529 / 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked size / SHA-256 52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
ELF build ID             d803d9695868713ef6ab0c3cf65f91212c9c6a62
```

Trusted current-client fence authority is #555 merge `2e572789a2bc4b64c5e906c4515c15c625f6bc9e` plus #561 closeout.

## Independent strict audit

Coordinator review `4970802493` classified source #556 `ACCEPT_WITH_EDITS`, with zero open material findings after correction.

Strict audit run `32239540646` on audit head `4d377f8088e07e68f3680558212f16e532201f70` independently re-fetched the exact current package and required one complete QMeta invoke-switch chain rather than accepting an executable-looking table alone. Artifact `9360231314` independently reproduced GitHub SHA-256:

```text
f81ab45076a2f31d7fa9bfc34793009a1a52347e4dd26ad6ce73225e274d12b7
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

The two SIGNAL targets are not call-safe business implementations.

## Preserved UNKNOWN

This task does not establish current non-QMeta state-machine targets, `TPlaySessionData` / `TAuthenticationAndEncryptionInfo` field provenance, password requirement semantics, live object/thread provenance, helper call safety, login success, character/world entry, causal `IN_GAME`, or restart/relogin/session-retention stability.

The source producer's 19/19 auth/session structural-name inventory is canonical only as bounded name/type presence for entries not independently target-bound.

## Validation and safety

Promotion #569 changed six documentation/evidence/archive paths, was `behind_by=0`, passed exact-head CI `32239950338`, final review `4970837047`, and had zero open review threads before merge.

No official-client execution, Synology/KasmVNC observation, credentials, login, process-memory access, GUI input, gameplay, client mutation, or physical E2E occurred in the coordinator audit/promotion/closeout.

Ownership is released. Any future live auth/session work requires a new current task, fresh Track A admission, and separate authority for any state-changing operation.
