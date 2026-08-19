---
task_id: OTC-20260819-track-a-auth-session-current-build-static
status: promotion_pending
session_role: coordinator
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: reverse_engineering_protocol
phase: coordinator-audit
source_pr: 556
source_branch: research/OTC-20260819-track-a-auth-session-current-build-static
source_head: 411d0e287d08406c682ef063fb3f3f61341d9295
source_disposition: close_unmerged_after_promotion
coordinator_decision: PENDING_STRICT_AUDIT
promotion_base: e4357137e47836d67eb19ceb13a8e313f69bf778
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
physical_e2e_required: false
ownership_release_state: pending_promotion
---

# TIBIA-RE-AUTH-SESSION — coordinator promotion archive checkpoint

## Bounded source package

Source Draft #556 revalidated the exact current public native-Linux client:

```text
packed size / SHA-256   10214529 / 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked size / SHA-256 52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
ELF build ID             d803d9695868713ef6ab0c3cf65f91212c9c6a62
```

The current trusted fence is already canonical through #555 merge `2e572789a2bc4b64c5e906c4515c15c625f6bc9e` plus #561 closeout. Source wording that still describes #555 as an unmerged Draft is stale and will not be promoted.

## Independent audit gate

Coordinator audit plan is persisted at:

`docs/agents/evidence/OTC-20260819-track-a-auth-session-current-build-static-promotion/20260819-coordinator-audit-plan.md`.

The high-impact QMeta dispatch addresses remain pending an independent strict current-build control-flow discriminator. Until that discriminator reaches a terminal PASS, no address is canonically promoted by this checkpoint.

Pre-registered role correction:

- `onRequestLoginWithCredentials` and `connectClientToGameserverWithExistingCredentials` must classify as QMeta `METHOD` entries;
- `loginSuccessful` and `requestCharacterLogin` must classify as QMeta `SIGNAL` entries; their recovered targets are signal activation dispatch targets, not call-safe business implementations.

## Safety boundary

`runtime_access:none`; no official-client execution, Synology/KasmVNC observation, login, credentials, gameplay, session mutation, process-memory access or client mutation is part of this coordinator audit/promotion.

## Lifecycle

Do not close source #556 or release ownership until the strict audit is terminal, promotion exact-head checks pass, and the clean promotion merges. This archive will be finalized in a lifecycle-only closeout after promotion.
